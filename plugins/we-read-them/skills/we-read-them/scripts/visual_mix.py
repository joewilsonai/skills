#!/usr/bin/env python3
"""Measure primary picture time and overlapping visual layers from a tab-separated log."""

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Interval:
    line: int
    start: float
    end: float
    primary: str | None
    secondary: list[str]
    part: str | None


def seconds(value, location):
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{location} must be numeric seconds") from None
    if not math.isfinite(number):
        raise ValueError(f"{location} must be finite")
    return number


def read_log(path, duration, method):
    required = {"in_s", "out_s", "primary"}
    if method == "sample":
        required.add("at_s")
    allowed = required | {"also", "part", "at_s"}
    intervals = []
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, delimiter="\t", strict=True)
        header = next(reader, [])
        missing = required - set(header)
        extra = set(header) - allowed
        if missing or extra or len(header) != len(set(header)):
            raise ValueError(f"invalid header {header!r}; required {sorted(required)}, allowed {sorted(allowed)}")
        for fields in reader:
            if not fields:
                continue
            line = reader.line_num
            if len(fields) != len(header):
                raise ValueError(f"line {line}: expected {len(header)} tab-separated fields, found {len(fields)}")
            row = dict(zip(header, (field.strip() for field in fields)))
            start = seconds(row["in_s"], f"line {line} in_s")
            end = seconds(row["out_s"], f"line {line} out_s")
            if not 0 <= start < end <= duration:
                raise ValueError(f"line {line}: require 0 <= in_s < out_s <= duration")
            if method == "sample" or row.get("at_s"):
                point = seconds(row.get("at_s"), f"line {line} at_s")
                if not start <= point < end:
                    raise ValueError(f"line {line}: at_s must lie in [in_s, out_s)")
            primary = row["primary"]
            if not primary:
                raise ValueError(f"line {line}: supply a primary picture label or 'unknown'")
            secondary = [tag.strip() for tag in row["also"].split("|")] if row.get("also") else []
            normalized = [tag.casefold() for tag in secondary]
            if "" in normalized or len(normalized) != len(set(normalized)):
                raise ValueError(f"line {line}: empty or duplicate secondary label in also")
            if primary.casefold() in normalized:
                raise ValueError(f"line {line}: the primary label is repeated in also")
            if primary.casefold() == "unknown":
                primary = None
            intervals.append(Interval(line, start, end, primary, secondary, row.get("part") or None))
    if not intervals:
        raise ValueError("the log contains no intervals")
    intervals.sort(key=lambda item: item.start)
    for previous, current in zip(intervals, intervals[1:]):
        if current.start < previous.end:
            raise ValueError(f"overlapping or duplicate intervals on lines {previous.line} and {current.line}")
    return intervals, "part" in header


def percentage(value, denominator):
    return round(value / denominator * 100, 4) if denominator else None


def category_totals(totals, denominator, basis):
    return {
        label: {"seconds": round(value, 6), f"percent_of_{basis}": percentage(value, denominator)}
        for label, value in sorted(totals.items())
    }


def summarize(intervals, duration=None):
    primary = Counter()
    secondary = Counter()
    unknown = 0.0
    for item in intervals:
        span = item.end - item.start
        if item.primary is None:
            unknown += span
        else:
            primary[item.primary] += span
        for tag in item.secondary:
            secondary[tag] += span
    known = math.fsum(primary.values())
    logged = math.fsum(item.end - item.start for item in intervals)
    result = {
        "interval_count": len(intervals),
        "logged_s": round(logged, 6),
        "known_primary_s": round(known, 6),
        "unknown_primary_s": round(unknown, 6),
    }
    if duration is None:
        # Part boundaries are not inferred across a gap. Only its logged rows contribute.
        result["primary"] = category_totals(primary, known, "known_primary")
        result["secondary"] = category_totals(secondary, logged, "logged")
    else:
        unlogged = max(0.0, duration - logged)
        result["unlogged_s"] = round(unlogged, 6)
        result["coverage_percent_of_duration"] = {
            "logged": percentage(logged, duration),
            "known_primary": percentage(known, duration),
            "unknown_primary": percentage(unknown, duration),
            "unlogged": percentage(unlogged, duration),
        }
        result["primary"] = category_totals(primary, duration, "duration")
        result["secondary"] = category_totals(secondary, duration, "duration")
    return result


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=("TSV columns: in_s, out_s, primary; optional also (labels separated by |), part. "
                "Use 'unknown' for a logged but unidentified primary. Sample logs require at_s "
                "inside each half-open interval. A sample represents that interval's duration. "
                "Unlogged time stays separate. Secondary layers can overlap."))
    parser.add_argument("log", type=Path, metavar="LOG.tsv")
    parser.add_argument("--duration", required=True, metavar="SECONDS", help="full length of the cut or excerpt")
    parser.add_argument("--method", required=True, choices=("timeline", "sample"))
    args = parser.parse_args()
    try:
        duration = seconds(args.duration, "--duration")
        if duration <= 0:
            raise ValueError("--duration must be positive")
        intervals, has_parts = read_log(args.log, duration, args.method)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        parser.error(str(error))
    report = {
        "method": args.method,
        "interpretation": ("Interval-weighted estimate from one observed point per logged interval."
                           if args.method == "sample" else "Screen time of coded timeline intervals."),
        "duration_s": duration,
        **summarize(intervals, duration),
    }
    if has_parts:
        parts = defaultdict(list)
        for interval in intervals:
            parts[interval.part].append(interval)
        report["parts"] = [{"part": label, **summarize(rows)} for label, rows in parts.items()]
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
