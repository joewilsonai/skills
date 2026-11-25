#!/usr/bin/env python3
"""Make blind artwork and paired-title previews from final YouTube covers."""

import argparse
from pathlib import Path
import re
import string

from PIL import Image, ImageDraw, ImageFont, ImageOps


def title_lines(title, font, width):
    """Wrap the title into the two lines visible in this feed mockup."""
    lines = []
    line = ""
    for word in title.split():
        candidate = f"{line} {word}".strip()
        if line and font.getlength(candidate) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    visible = lines[:2]
    for idx, part in enumerate(visible):
        if font.getlength(part) > width or (idx == 1 and len(lines) > 2):
            while part and font.getlength(part + "…") > width:
                part = part[:-1]
            visible[idx] = part.rstrip() + "…"
    return visible


def feed_image(image, width, duration, font):
    height = round(width * 9 / 16)
    preview = image.resize((width, height), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(preview)
    length = round(font.getlength(duration))
    right, bottom = width - 4, height - 4
    draw.rounded_rectangle((right - length - 8, bottom - 17, right, bottom),
                           radius=3, fill="#101010")
    draw.text((right - 4, bottom - 3), duration, font=font, fill="white", anchor="rs")
    return preview


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair", nargs=2, action="append", required=True,
                        metavar=("IMAGE", "TITLE"))
    parser.add_argument("--duration", required=True, help="The video's runtime, e.g. 8:25.")
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    if len(args.pair) > 3:
        parser.error("Use up to three candidates.")
    if not re.fullmatch(r"(?:\d+|\d+:[0-5]\d):[0-5]\d", args.duration):
        parser.error("Supply the duration as m:ss or h:mm:ss.")

    widths = (168, 320)
    padding = 18
    column_x = (padding, padding * 2 + widths[0])
    row_height = 285
    sheet_width = sum(widths) + padding * 3
    sheet_height = row_height * len(args.pair)
    font_path = Path(__file__).resolve().parents[1] / "templates/aibc-brand/Inter-Variable.ttf"
    title_font = ImageFont.truetype(str(font_path), 16)
    tag_font = ImageFont.truetype(str(font_path), 12)
    sheets = {name: Image.new("RGB", (sheet_width, sheet_height), "#191919")
              for name in ("art-only", "title-pairs")}
    output_paths = [args.out_dir / f"{name}.jpg" for name in sheets]
    if any(Path(art).resolve() == out.resolve() for art, _ in args.pair for out in output_paths):
        parser.error("Choose an output directory that keeps the proof separate from the artwork.")
    for index, (art, title) in enumerate(args.pair):
        if not title.strip():
            parser.error(f"Supply a title for {art}.")
        with Image.open(art) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGB")
        if abs(image.width / image.height - 16 / 9) > .01:
            parser.error(f"{art} has an unexpected aspect ratio for a long-form cover.")
        y = row_height * index
        for width, x in zip(widths, column_x):
            preview = feed_image(image, width, args.duration, tag_font)
            for name, sheet in sheets.items():
                draw = ImageDraw.Draw(sheet)
                draw.text((x, y + 12), f"{string.ascii_uppercase[index]}   {width} px",
                          fill="#aaaaaa", font=tag_font)
                pic_y = y + 32
                sheet.paste(preview, (x, pic_y))
                if name == "title-pairs":
                    for line_index, line in enumerate(title_lines(title, title_font, width)):
                        draw.text((x, pic_y + preview.height + 8 + line_index * 20),
                                  line, fill="white", font=title_font)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for sheet, out in zip(sheets.values(), output_paths):
        sheet.save(out, quality=94, subsampling=0)
        print(out)


if __name__ == "__main__":
    main()
