#!/usr/bin/env python3
"""Apply a generated background to slide PNGs while preserving text and artwork."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from extract_scenes import output_stem

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Install pillow, numpy, and opencv-python-headless."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slides-dir", required=True, help="Directory containing prefixed slide PNGs")
    parser.add_argument("--video", help="Video path used to derive the slide prefix")
    parser.add_argument("--background", required=True, help="Generated background image")
    parser.add_argument("--output-dir", required=True, help="Directory for restyled PNGs")
    parser.add_argument("--strength", type=float, default=0.86, help="Background blend strength")
    parser.add_argument("--prefix", help="Slide prefix; defaults to <video-name>_slide")
    parser.add_argument("--contact-sheet", help="Optional contact sheet output path")
    parser.add_argument("--keep-watermark", action="store_true", help="Do not remove NotebookLM mark")
    parser.add_argument("--overwrite", action="store_true", help="Replace matching output PNGs")
    return parser.parse_args()


def notebooklm_consensus(images: list[np.ndarray]) -> dict[tuple[int, int], np.ndarray]:
    """Find dark pixels repeated at the NotebookLM position across many slides."""
    groups: dict[tuple[int, int], list[np.ndarray]] = {}
    for rgb in images:
        height, width = rgb.shape[:2]
        groups.setdefault((width, height), []).append(rgb)
    consensus: dict[tuple[int, int], np.ndarray] = {}
    for (width, height), group in groups.items():
        # NotebookLM can place its wordmark flush against the lower edge.
        # Consensus filtering still protects unrelated slide content.
        x1, x2 = round(width * 0.850), round(width * 0.998)
        y1, y2 = round(height * 0.900), round(height * 0.998)
        samples = []
        for rgb in group:
            gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
            samples.append(gray[y1:y2, x1:x2] < 155)
        frequency = np.mean(np.stack(samples, axis=0), axis=0)
        repeated = (frequency >= 0.35).astype(np.uint8) * 255
        repeated = cv2.dilate(repeated, np.ones((3, 3), np.uint8), iterations=1)
        mask = np.zeros((height, width), dtype=np.uint8)
        # A genuine wordmark contributes many repeated pixels; otherwise do nothing.
        if np.count_nonzero(repeated) >= 100:
            mask[y1:y2, x1:x2] = repeated
            # The mark also contains bright glyphs that a dark-pixel consensus
            # cannot detect. Its baseline is consistently flush with the lower
            # right edge, so remove that narrow strip as one unit.
            strip_x1 = round(width * 0.900)
            strip_y1 = round(height * 0.966)
            mask[strip_y1:round(height * 0.998), strip_x1:round(width * 0.998)] = 255
        consensus[(width, height)] = mask
    return consensus


def remove_notebooklm(rgb: np.ndarray, consensus: np.ndarray) -> np.ndarray:
    height, width = rgb.shape[:2]
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    # Remove only consensus pixels that are dark in this specific frame.
    dark_here = cv2.dilate((gray < 175).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
    mask = cv2.bitwise_and(consensus, dark_here)
    if not np.any(mask):
        return rgb
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    clean = cv2.inpaint(bgr, mask, 4, cv2.INPAINT_TELEA)
    return cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)


def restyle(rgb: np.ndarray, background: np.ndarray, strength: float) -> np.ndarray:
    source = rgb.astype(np.float32)
    backdrop = background.astype(np.float32)
    maximum = source.max(axis=2)
    minimum = source.min(axis=2)
    luminance = source.mean(axis=2)
    chroma = maximum - minimum
    light = np.clip((luminance - 198.0) / 52.0, 0.0, 1.0)
    neutral = 1.0 - np.clip((chroma - 18.0) / 72.0, 0.0, 1.0)
    alpha = (strength * light * neutral)[..., None]
    result = source * (1.0 - alpha) + backdrop * alpha
    return np.clip(result, 0, 255).astype(np.uint8)


def create_contact_sheet(paths: list[Path], destination: Path) -> None:
    thumbs: list[Image.Image] = []
    for path in paths:
        with Image.open(path) as image:
            thumb = ImageOps.fit(image.convert("RGB"), (320, 180), Image.Resampling.LANCZOS)
            thumb.load()
            thumbs.append(thumb.copy())
    columns = 5
    rows = math.ceil(len(thumbs) / columns)
    margin, padding = 4, 4
    width = columns * 320 + (columns - 1) * padding + margin * 2
    height = rows * 180 + (rows - 1) * padding + margin * 2
    sheet = Image.new("RGB", (width, height), "black")
    for index, thumb in enumerate(thumbs):
        x = margin + (index % columns) * (320 + padding)
        y = margin + (index // columns) * (180 + padding)
        sheet.paste(thumb, (x, y))
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, "PNG", compress_level=6)


def main() -> int:
    args = parse_args()
    if not 0 <= args.strength <= 1:
        raise ValueError("--strength must be between 0 and 1")
    slides_dir = Path(args.slides_dir).expanduser().resolve()
    background_path = Path(args.background).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not slides_dir.is_dir():
        raise FileNotFoundError(f"Slides directory not found: {slides_dir}")
    if not background_path.is_file():
        raise FileNotFoundError(f"Background not found: {background_path}")
    if args.prefix:
        prefix = args.prefix
    elif args.video:
        prefix = f"{output_stem(Path(args.video).expanduser())}_slide"
    else:
        prefix = None
    pattern = f"{prefix}_*.png" if prefix else "*_slide_*.png"
    slides = sorted(slides_dir.glob(pattern))
    if not slides:
        raise FileNotFoundError(f"No {pattern} files found in {slides_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(output_dir.glob(pattern))
    if existing and not args.overwrite:
        raise FileExistsError(
            f"{len(existing)} matching PNGs already exist in {output_dir}; use --overwrite only when intended"
        )
    if args.overwrite:
        for path in existing:
            path.unlink()

    with Image.open(background_path) as image:
        background_source = image.convert("RGB")
    loaded: list[tuple[Path, np.ndarray]] = []
    for slide in slides:
        with Image.open(slide) as image:
            loaded.append((slide, np.array(image.convert("RGB"))))
    watermark_masks = notebooklm_consensus([rgb for _, rgb in loaded]) if not args.keep_watermark else {}

    background_cache: dict[tuple[int, int], np.ndarray] = {}
    written: list[Path] = []
    source_dimensions: list[tuple[int, int]] = []
    for slide, rgb in loaded:
        height, width = rgb.shape[:2]
        dimensions = (width, height)
        source_dimensions.append(dimensions)
        if dimensions not in background_cache:
            fitted = ImageOps.fit(
                background_source,
                dimensions,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            background_cache[dimensions] = np.asarray(fitted)
        if not args.keep_watermark:
            rgb = remove_notebooklm(rgb, watermark_masks[dimensions])
        output = restyle(rgb, background_cache[dimensions], args.strength)
        destination = output_dir / slide.name
        Image.fromarray(output, "RGB").save(destination, "PNG", compress_level=6)
        written.append(destination)

    if args.contact_sheet:
        create_contact_sheet(written, Path(args.contact_sheet).expanduser().resolve())
    if len(written) != len(slides):
        raise RuntimeError("Output count does not match input count")
    print(
        json.dumps(
            {
                "slides_dir": str(slides_dir),
                "output_dir": str(output_dir),
                "count": len(written),
                "prefix": prefix,
                "dimensions": sorted({f"{w}x{h}" for w, h in source_dimensions}),
                "contact_sheet": str(Path(args.contact_sheet).expanduser().resolve())
                if args.contact_sheet
                else None,
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
