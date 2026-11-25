#!/usr/bin/env python3
"""Prepare a blinded local comparison and record the editor's decision."""

import argparse
import fcntl
import hashlib
import json
import os
import secrets
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path


def nonblank(text):
    if not text.strip():
        raise argparse.ArgumentTypeError("provide nonempty text")
    return text.strip()


def digest(path):
    with path.open("rb") as file:
        sha = hashlib.sha256()
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


@contextmanager
def locked_directory(directory):
    # Lock the directory inode: replacing edit.json cannot invalidate the lock.
    fd = os.open(directory, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield fd
    finally:
        os.close(fd)


def sync_path(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def prompt(question):
    return (
        "# Independent edit review\n\n" + question + "\n\n"
        "Start with your assigned first file. Before opening the other, write what "
        "you understood and where. Then inspect the other file and record the order "
        "you used. Cite a cue or timestamp for each, then choose A, B, or tie. "
        "Flag any loss of accuracy, clarity, readability or continuity. "
        "State which parts of the files you could actually inspect.\n"
    )


def write_state(path, state):
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8",
                                     prefix=".edit-state-", delete=False) as output:
        temporary = Path(output.name)
        try:
            json.dump(state, output, indent=2, ensure_ascii=False)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
            os.replace(temporary, path)
            sync_path(path.parent)
        finally:
            temporary.unlink(missing_ok=True)


def load_trial(trial):
    state = json.loads((trial / "edit.json").read_text(encoding="utf-8"))
    if state.get("version") != 1:
        raise ValueError("unrecognized edit trial")
    if state["order"] not in ({"A": "baseline", "B": "candidate"},
                              {"A": "candidate", "B": "baseline"}):
        raise ValueError("invalid A/B order in the trial manifest")
    if digest(trial / "review/prompt.md") != state["prompt_sha256"]:
        raise ValueError("review prompt changed after preparation")
    for label, role in state["order"].items():
        path = trial / "review" / (label + state["suffix"])
        if digest(path) != state["inputs"][role]["sha256"]:
            raise ValueError(f"review file {label} changed after preparation")
    return state


def prepare(args):
    trial = args.trial.absolute()
    paths = {"baseline": args.before.resolve(), "candidate": args.candidate.resolve()}
    suffix = args.before.suffix.lower()
    if not suffix or suffix != args.candidate.suffix.lower():
        raise ValueError("supply two files with the same nonempty extension")
    for path in paths.values():
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"missing or empty input: {path}")
    inputs = {role: {"source": str(path), "sha256": digest(path)}
              for role, path in paths.items()}
    if inputs["baseline"]["sha256"] == inputs["candidate"]["sha256"]:
        raise ValueError("the two files have identical content")
    settings = {"version": 1, "inputs": inputs, "question": args.question,
                "check": args.check, "suffix": suffix}
    trial.parent.mkdir(parents=True, exist_ok=True)
    with locked_directory(trial.parent) as parent_fd:
        if os.path.lexists(trial):
            state = load_trial(trial)
            if any(state[key] != value for key, value in settings.items()):
                raise ValueError("different inputs or review criteria; choose a new trial path")
        else:
            roles = ["baseline", "candidate"]
            if secrets.randbelow(2):
                roles.reverse()
            state = {**settings, "order": dict(zip(("A", "B"), roles)), "status": "prepared"}
            with tempfile.TemporaryDirectory(dir=trial.parent, prefix=".edit-trial-") as stage:
                root = Path(stage)
                review = root / "review"
                review.mkdir()
                for label, role in state["order"].items():
                    target = review / (label + suffix)
                    shutil.copyfile(paths[role], target)
                    if digest(target) != inputs[role]["sha256"]:
                        raise ValueError(f"{role} changed during staging; prepare again")
                    sync_path(target)
                (review / "prompt.md").write_text(prompt(args.question), encoding="utf-8")
                state["prompt_sha256"] = digest(review / "prompt.md")
                sync_path(review / "prompt.md")
                sync_path(review)
                write_state(root / "edit.json", state)
                root.rename(trial)
                os.fsync(parent_fd)
    print(trial / "review")


def decide(args):
    raw = args.review.read_bytes()
    review = raw.decode("utf-8")
    if not review.strip() or "\0" in review:
        raise ValueError("review evidence must be nonempty UTF-8 text")
    with locked_directory(args.trial):
        state = load_trial(args.trial)
        role = state["order"].get(args.choice, "baseline")
        selected_label = next(label for label, name in state["order"].items() if name == role)
        decision = {"choice": args.choice, "reason": args.reason, "selected_role": role,
                    "selected_file": f"review/{selected_label}{state['suffix']}",
                    "review_text": review, "review_sha256": hashlib.sha256(raw).hexdigest()}
        if state.get("decision") is not None:
            if state["decision"] != decision:
                raise ValueError("a different decision is already recorded; use a new trial")
        else:
            state.update(status="decided", decision=decision)
            write_state(args.trial / "edit.json", state)
    print(f"{args.choice}: {role} ({args.trial / decision['selected_file']})")


def playback(args):
    trial = args.trial.resolve()
    review = trial / "review"
    template = (Path(__file__).resolve().parents[1] / "templates/first-view.html").read_text(
        encoding="utf-8"
    )
    with locked_directory(trial):
        state = load_trial(trial)
        suffix = state["suffix"]
        if suffix not in {".mp4", ".m4v", ".mov", ".webm", ".ogv", ".ogg"}:
            raise ValueError("playback pages require two staged browser-playable video files")
        # The viewer receives only neutral labels, the viewer question and a trial fingerprint.
        hashes = [state["inputs"][state["order"][label]]["sha256"] for label in ("A", "B")]
        trial_tag = hashlib.sha256(("\n".join([*hashes, state["question"]])).encode()).hexdigest()
        with tempfile.TemporaryDirectory(dir=review, prefix=".playback-") as stage:
            for first in ("A", "B"):
                config = json.dumps({"first": first, "suffix": suffix, "trial": trial_tag,
                                     "question": state["question"]}, ensure_ascii=True)
                name = f"watch-{first}-first.html"
                page = Path(stage) / name
                page.write_text(template.replace("__VIEW_CONFIG__", config.replace("<", "\\u003c")),
                                encoding="utf-8")
                sync_path(page)
            for page in sorted(Path(stage).iterdir()):
                os.replace(page, review / page.name)
            sync_path(review)
    for first in ("A", "B"):
        print(review / f"watch-{first}-first.html")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("prepare", help="stage two neutral files in a new trial")
    start.add_argument("trial", type=Path)
    start.add_argument("before", type=Path)
    start.add_argument("candidate", type=Path)
    start.add_argument("--question", required=True, type=nonblank)
    start.add_argument("--check", required=True, type=nonblank, help="private success criterion")
    start.set_defaults(run=prepare)
    watch = commands.add_parser("playback", help="build local first-view playback pages for a video trial")
    watch.add_argument("trial", type=Path)
    watch.set_defaults(run=playback)
    end = commands.add_parser("decide", help="verify the staged files and save one decision")
    end.add_argument("trial", type=Path)
    end.add_argument("--choice", choices=("A", "B", "tie", "revise", "blocked"), required=True)
    end.add_argument("--review", required=True, type=Path, help="independent review in UTF-8 text")
    end.add_argument("--reason", required=True, type=nonblank)
    end.set_defaults(run=decide)
    args = parser.parse_args()
    try:
        args.run(args)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"edit trial: {error}\n")


if __name__ == "__main__":
    main()
