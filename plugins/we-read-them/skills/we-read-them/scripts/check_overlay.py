#!/usr/bin/env python3
"""Check a persistent graphic in the decoded video. Supply its rectangle and an interior RGB color."""
import argparse
import json
import subprocess
import sys
from fractions import Fraction

def inspect(path, region, color, tolerance, start, end):
    x, y, w, h = region
    probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                     "-show_entries", "stream=width,height,avg_frame_rate", "-of", "json", path])
    stream = json.loads(probe)["streams"][0]
    if min(x, y) < 0 or min(w, h) <= 0 or x + w > stream["width"] or y + h > stream["height"]:
        raise ValueError(f"{path}: rectangle outside {stream['width']}×{stream['height']}")
    rate = Fraction(stream["avg_frame_rate"])
    seek = ["-ss", str(start)] if start else []
    length = ["-t", str(end-start)] if end is not None else []
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-threads", "2", *seek, "-i", path, *length,
           "-map", "0:v:0", "-an", "-vf", f"crop={w}:{h}:{x}:{y}:exact=1,format=rgb24", "-fps_mode", "passthrough",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"]
    missing = []
    frames = 0
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        while block := proc.stdout.read(w*h*3):
            if len(block) != w*h*3:
                raise ValueError(f"{path}: truncated decoded frame")
            matches = sum(all(abs(a-b) <= tolerance for a,b in zip(block[i:i+3], color))
                          for i in range(0, len(block), 3))
            visible = matches * 2 >= w * h
            if not visible:
                if missing and missing[-1][1] == frames:
                    missing[-1][1] += 1
                else:
                    missing.append([frames,frames+1])
            frames += 1
        if proc.wait():
            raise ValueError(f"{path}: FFmpeg could not decode the requested span")
    if not frames:
        raise ValueError(f"{path}: no frames in requested span")
    print(f"{path} • {frames} decoded frames")
    for a, b in missing:
        print(f"  mark missing on frames {a}–{b-1}, approximately {start+a/float(rate):.3f}–{start+b/float(rate):.3f} s")
    return not missing

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("videos", nargs="+")
    p.add_argument("--region", required=True, type=int, nargs=4, metavar=("X","Y","W","H"))
    p.add_argument("--color", required=True, help="Expected sRGB hex, e.g. FF4A2E")
    p.add_argument("--tolerance", type=int, default=40, help="Maximum error per channel from encoding")
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--end", type=float)
    args = p.parse_args()
    try: color = bytes.fromhex(args.color.removeprefix("#"))
    except ValueError: p.error("color must have six hexadecimal digits")
    if len(color) != 3 or not 0 <= args.tolerance <= 255:
        p.error("use a six-digit RGB color and a tolerance of 0–255")
    if args.start < 0 or args.end is not None and args.end <= args.start:
        p.error("end must be later than the nonnegative start time")
    okay = True
    for file in args.videos:
        okay = inspect(file, args.region, color, args.tolerance, args.start, args.end) and okay
    return 0 if okay else 1

if __name__ == "__main__":
    sys.exit(main())
