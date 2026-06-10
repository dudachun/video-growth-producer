#!/usr/bin/env python3
"""Compose a 3:4 title cover over a background image."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise SystemExit("Pillow is required: pip install pillow") from exc

    parser = argparse.ArgumentParser()
    parser.add_argument("--background", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--out", required=True)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument("--font", default="")
    args = parser.parse_args()

    bg = Image.open(args.background).convert("RGB")
    tw, th = args.width, args.height
    scale = max(tw / bg.width, th / bg.height)
    bg = bg.resize((int(bg.width * scale), int(bg.height * scale)), Image.Resampling.LANCZOS)
    left = (bg.width - tw) // 2
    top = (bg.height - th) // 2
    canvas = bg.crop((left, top, left + tw, top + th)).convert("RGBA")

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(tw):
        alpha = int(max(0, 190 * (1 - x / (tw * 0.72))))
        d.line([(x, 0), (x, th)], fill=(0, 0, 0, alpha))
    canvas = Image.alpha_composite(canvas, overlay)

    font_path = Path(args.font) if args.font else None
    if not font_path or not font_path.exists():
        candidates = [
            Path(r"C:\Windows\Fonts\msyhbd.ttc"),
            Path(r"C:\Windows\Fonts\simhei.ttf"),
            Path(r"C:\Windows\Fonts\Arial.ttf"),
        ]
        font_path = next((p for p in candidates if p.exists()), None)
    if not font_path:
        raise SystemExit("No usable font found. Pass --font.")

    title_font = ImageFont.truetype(str(font_path), 132)
    subtitle_font = ImageFont.truetype(str(font_path), 48)
    draw = ImageDraw.Draw(canvas)

    y = 120
    for line in args.title.replace("\\n", "\n").splitlines():
        draw.text((58 + 6, y + 8), line, font=title_font, fill=(0, 0, 0, 220), stroke_width=6, stroke_fill=(0, 0, 0, 220))
        draw.text((58, y), line, font=title_font, fill=(255, 232, 132, 255), stroke_width=4, stroke_fill=(7, 16, 31, 255))
        box = draw.textbbox((58, y), line, font=title_font, stroke_width=4)
        y += int((box[3] - box[1]) * 1.02)

    if args.subtitle:
        box = draw.textbbox((0, 0), args.subtitle, font=subtitle_font)
        x, y = 58, min(th - 180, y + 42)
        draw.rounded_rectangle((x, y, x + box[2] + 44, y + box[3] + 30), radius=22, fill=(240, 92, 28, 242))
        draw.text((x + 22, y + 12), args.subtitle, font=subtitle_font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(80, 18, 8, 180))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out, quality=95)
    print(f"cover={out.resolve()}")


if __name__ == "__main__":
    main()

