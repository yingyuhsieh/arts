#!/usr/bin/env python3
"""Place the bundled end sticker on the final restyled slide."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Missing dependency. Install pillow.") from exc

from extract_scenes import output_stem


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slides-dir", required=True, help="Restyled update directory")
    parser.add_argument("--video", required=True, help="Video path used to derive the prefix")
    parser.add_argument("--sticker", help="Sticker PNG; defaults to the bundled asset")
    parser.add_argument("--height-ratio", type=float, default=0.65, help="Sticker height / slide height")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0.1 <= args.height_ratio <= 0.9:
        raise ValueError("--height-ratio must be between 0.1 and 0.9")
    slides_dir = Path(args.slides_dir).expanduser().resolve()
    video = Path(args.video).expanduser().resolve()
    sticker_path = (
        Path(args.sticker).expanduser().resolve()
        if args.sticker
        else Path(__file__).resolve().parent.parent / "assets" / "end_sticker.png"
    )
    prefix = f"{output_stem(video)}_slide"
    slides = sorted(slides_dir.glob(f"{prefix}_*.png"))
    if not slides:
        raise FileNotFoundError(f"No {prefix}_*.png files found in {slides_dir}")
    if not sticker_path.is_file():
        raise FileNotFoundError(f"Sticker not found: {sticker_path}")
    destination = slides[-1]
    with Image.open(destination) as image:
        slide = image.convert("RGBA")
    with Image.open(sticker_path) as image:
        sticker = image.convert("RGBA")
    target_height = round(slide.height * args.height_ratio)
    target_width = round(sticker.width * target_height / sticker.height)
    sticker = sticker.resize((target_width, target_height), Image.Resampling.LANCZOS)
    x = (slide.width - sticker.width) // 2
    y = (slide.height - sticker.height) // 2
    slide.alpha_composite(sticker, (x, y))
    slide.convert("RGB").save(destination, "PNG", compress_level=6)
    print(
        json.dumps(
            {
                "slide": str(destination),
                "sticker": str(sticker_path),
                "size": f"{sticker.width}x{sticker.height}",
                "position": [x, y],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
