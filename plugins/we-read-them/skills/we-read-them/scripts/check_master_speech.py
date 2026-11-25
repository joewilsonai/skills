#!/usr/bin/env python3
"""Compare a chaptered countdown master's decoded sound with its reviewed vertical reels."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from scipy.signal import correlate

RATE = 12000
MAX_LAG = round(0.08 * RATE)
QUIET = 0.0005
ORDER = [0, *range(10, 0, -1)]


def decode(path):
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-xerror", "-i", str(path),
           "-map", "0:a:0", "-ac", "1", "-ar", str(RATE), "-f", "f32le", "pipe:1"]
    data = np.frombuffer(subprocess.check_output(cmd), dtype="<f4")
    if not data.size or not np.isfinite(data).all():
        raise ValueError(f"{path} has no finite decoded audio")
    return data


def reviewed_short(folder, meta):
    expected = folder / f"reel-{int(folder.name[1:]):02d}-{meta.get('slug', '')}.mp4"
    if expected.is_file():
        return expected
    candidates = sorted(p for p in folder.glob("reel-*.mp4")
                        if not p.stem.endswith(("-phone", "-small", "-wide", "-preview")))
    if len(candidates) != 1:
        raise ValueError(f"Expected one reviewed Short in {folder}, found {candidates}")
    return candidates[0]


def compare(source, target):
    """Compare amplitude and waveform, treating a pair of quiet intervals as equivalent."""
    lx = float(np.sqrt(np.mean(source * source)))
    ly = float(np.sqrt(np.mean(target * target)))
    if max(lx, ly) <= QUIET:
        return 1.0, 0.0
    level = float(20 * np.log10(max(ly, 1e-10) / max(lx, 1e-10)))
    x = source - source.mean()
    y = target - target.mean()
    norm = float(np.linalg.norm(x) * np.linalg.norm(y))
    similarity = float(np.dot(x, y) / norm) if norm > 0 else 0.0
    return similarity, level


def align(source, target):
    # Use the whole spoken span. An intro pause, room tone or a musical hit alone
    # can otherwise choose the wrong codec offset.
    signal = source.astype(np.float64)
    signal -= signal.mean()
    if np.max(np.abs(signal)) < QUIET:
        raise ValueError("The reviewed Short contains no measurable signal during its spoken cues")
    padded = np.pad(target.astype(np.float64), MAX_LAG)
    correlations = correlate(padded, signal, mode="valid", method="fft")
    highest = float(correlations.max())
    candidates = np.flatnonzero(correlations >= highest - max(abs(highest) * 1e-8, 1e-12))
    return int(min(candidates - MAX_LAG, key=abs))


def sample(seconds):
    return round(float(seconds) * RATE)


def inspect_chapter(folder, info, master, last):
    metadata_path = folder / "wide/meta.json"
    meta = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
    title = info.get("tags", {}).get("title", "")
    if meta.get("chapter") and title != meta["chapter"]:
        raise ValueError(f"expected chapter {meta['chapter']!r}, found {title!r}")
    short = reviewed_short(folder, meta)
    source = decode(short)
    first, stop = sample(info["start_time"]), sample(info["end_time"])
    if first < 0 or first >= stop or stop > len(master) + RATE // 30:
        raise ValueError(f"chapter bounds {first / RATE:.3f}–{stop / RATE:.3f}s exceed master audio")
    target = master[first:stop]
    if not last and "endcard_at" in meta:
        expected = round(float(meta["endcard_at"]) * 30) * (RATE // 30)
        if abs((stop - first) - expected) > RATE // 30:
            raise ValueError(f"chapter length {(stop - first) / RATE:.3f}s differs from the "
                             f"reviewed end-card boundary {expected / RATE:.3f}s")
    rows = json.loads((folder / "takes.json").read_text())["takes"]
    if not rows:
        raise ValueError("takes.json has no utterances")
    cues = []
    for row in rows:
        begin, end = sample(row["t0"]), sample(row["t1"])
        if not 0 <= begin < end <= len(source):
            raise ValueError(f"Invalid utterance times in reviewed Short: {row['text']!r}")
        cues.append(("utterance", row["text"], begin, end))
        for word, a, b in row.get("words") or []:
            a, b = sample(a), sample(b)
            if not 0 <= a <= b <= len(source):
                raise ValueError(f"Invalid word times in reviewed Short: {word!r}")
            # Word boundaries are estimates. Keep neighbouring consonants for very short words.
            cues.append(("word", word, max(begin, a - RATE // 25), min(end, max(b, a + 1) + RATE // 25)))
    lo = min(a for _, _, a, _ in cues)
    hi = max(b for _, _, _, b in cues)
    if hi > len(target) + MAX_LAG:
        raise ValueError(f"chapter ends before the final utterance ({hi / RATE:.3f}s)")
    # Context on either side of the spoken span preserves real samples for offset estimation.
    a = max(0, lo - MAX_LAG)
    b = min(len(source), len(target), hi + MAX_LAG)
    lag = align(source[a:b], target[a:b])
    start = max(0, -lag)
    end = min(len(source), len(target) - lag)
    # Alignment can leave up to 80 ms outside comparison at the join. Codec padding
    # can be quiet; an inserted click or clipped opening must still fail the check.
    prefix = target[:lag] if lag > 0 else source[:start]
    if prefix.size and np.max(np.abs(prefix)) > 0.01:
        raise ValueError(f"unexpected sound in the unmatched {len(prefix) / RATE:.3f}s at the chapter opening")
    if lo < start - RATE // 200 or hi > end + RATE // 200:
        raise ValueError(f"master clips a spoken cue at the chapter edge (offset {lag / RATE:.3f}s)")
    # longform.py can round/pad the final frame; only silence may fall outside the reviewed file.
    overhang = target[max(0, len(source) + lag):]
    if len(overhang) > RATE // 15 or (overhang.size and np.max(np.abs(overhang)) > 0.01):
        raise ValueError("master extends past the reviewed Short with unexpected duration or sound")
    # Interior Shorts intentionally keep their standalone end card after the cut.
    # The finale carries its whole reviewed mix, including sound after the last word.
    tail = source[end:]
    if last and tail.size and np.max(np.abs(tail)) > 0.01:
        raise ValueError(f"master omits audible sound from the final {len(tail) / RATE:.3f}s of the Short")
    checks = cues + [("window", "", i, min(i + RATE // 2, end))
                     for i in range(start, end, RATE // 4)]
    minimum = {kind: 1.0 for kind in ("word", "utterance", "window")}
    counts = dict.fromkeys(minimum, 0)
    for kind, label, a, b in checks:
        a, b = max(start, a), min(end, b)
        if a >= b:
            raise ValueError(f"{kind} {label!r} has no samples inside the chapter")
        x, y = source[a:b], target[a + lag:b + lag]
        threshold = 0.75 if kind == "word" else 0.85
        candidates = [compare(x, y)]
        # The canonical stitch intentionally fades the last 350 ms of inner chapters.
        fade = round(.35 * RATE)
        if not last and b + lag > len(target) - fade:
            envelope = np.clip((len(target) - np.arange(a + lag, b + lag)) / fade, 0, 1)
            candidates.append(compare(x * envelope, y))
        accepted = [similarity for similarity, db in candidates if similarity >= threshold and abs(db) <= 6]
        if not accepted:
            similarity, db = max(candidates, key=lambda item: item[0])
            raise ValueError(f"{kind} {label!r} at {a / RATE:.3f}–{b / RATE:.3f}s differs "
                             f"(correlation {similarity:.3f}, level change {db:+.1f} dB)")
        counts[kind] += 1
        minimum[kind] = min(minimum[kind], max(accepted))
    return {"title": title, "short": short.name, "offset_ms": round(1000 * lag / RATE, 3),
            "checked": counts, "minimum_correlation": {k: round(v, 5) if counts[k] else None
                                                      for k, v in minimum.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("master", type=Path)
    parser.add_argument("reels", type=Path, help="Case directory containing r0, r10 through r1")
    parser.add_argument("--report", type=Path, help="Write results and discrepancies as JSON")
    args = parser.parse_args()
    if args.report:
        destination = args.report.resolve()
        inputs = [args.master, *args.reels.glob("r*/reel-*.mp4"), *args.reels.glob("r*/takes.json"),
                  *args.reels.glob("r*/wide/meta.json")]
        if destination in {path.resolve() for path in inputs}:
            parser.error("--report would overwrite an input file")
    result = {"master": str(args.master), "sample_rate_hz": RATE, "chapters": [], "errors": []}
    try:
        master = decode(args.master)
        with args.master.open("rb") as stream:
            result["master_sha256"] = hashlib.file_digest(stream, "sha256").hexdigest()
        chapters = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_chapters",
                                                       "-of", "json", str(args.master)]))["chapters"]
        if len(chapters) != len(ORDER):
            raise ValueError(f"Expected {len(ORDER)} chapters, found {len(chapters)}")
        previous_end = 0
        for rank, chapter in zip(ORDER, chapters):
            if abs(sample(chapter["start_time"]) - previous_end) > RATE // 500:
                raise ValueError(f"r{rank}: chapter boundary skips or overlaps its predecessor")
            previous_end = sample(chapter["end_time"])
            try:
                report = inspect_chapter(args.reels / f"r{rank}", chapter, master, rank == ORDER[-1])
                result["chapters"].append({"rank": rank, **report})
                print(f"r{rank}: {report['checked']}, offset {report['offset_ms']} ms")
            except (OSError, ValueError, LookupError, TypeError, subprocess.CalledProcessError) as exc:
                result["errors"].append(f"r{rank}: {exc}")
        if abs(len(master) - previous_end) > RATE // 15:
            raise ValueError("Master audio extends beyond the chapter table or ends early")
    except (OSError, ValueError, LookupError, TypeError, subprocess.CalledProcessError) as exc:
        result["errors"].append(str(exc))
    result["passed"] = not result["errors"]
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=args.report.parent, delete=False) as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(stream.name, args.report)
    for error in result["errors"]:
        print("FAIL:", error, file=sys.stderr)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
