#!/usr/bin/env python3
"""Render supplemental text/image slides from a reviewed JSON specification."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit("Missing dependency. Install pillow.") from exc


FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/msjh.ttc"),
    Path("C:/Windows/Fonts/microsoftjhenghei.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="UTF-8 JSON file containing a slides list")
    parser.add_argument("--output-dir", required=True, help="Existing update directory")
    parser.add_argument("--background", required=True, help="Reusable generated background")
    parser.add_argument("--reference-slide", required=True, help="PNG providing output dimensions")
    parser.add_argument("--font", help="Optional TrueType/OpenType/TTC font")
    parser.add_argument("--overwrite", action="store_true", help="Replace specified PNGs")
    return parser.parse_args()


def choose_font(explicit: str | None) -> Path:
    candidates = [Path(explicit).expanduser().resolve()] if explicit else FONT_CANDIDATES
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("No suitable font found; pass --font explicitly")


def tokens(text: str) -> list[str]:
    # Keep Latin words together while allowing CJK text to wrap at character boundaries.
    return re.findall(r"[\u3400-\u9fff]|[^\s\u3400-\u9fff]+\s*|\s+", text)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for token in tokens(paragraph):
            candidate = current + token
            if current and draw.textlength(candidate, font=font) > width:
                lines.append(current.rstrip())
                current = token.lstrip()
            else:
                current = candidate
        if current:
            lines.append(current.rstrip())
    return lines


def body_font_and_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: Path,
    max_width: int,
    max_height: int,
    slide_height: int,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    for size in range(round(slide_height * 0.045), round(slide_height * 0.025) - 1, -2):
        font = ImageFont.truetype(str(font_path), size)
        spacing = max(8, round(size * 0.45))
        lines = wrap_text(draw, text, font, max_width)
        height = len(lines) * size + max(0, len(lines) - 1) * spacing
        if height <= max_height:
            return font, lines, spacing
    raise ValueError("Supplemental slide body is too long; split it into more slides")


def resolve_spec_image(value: object, spec_path: Path) -> Path | None:
    if value is None or str(value).strip() == "":
        return None
    path = Path(str(value)).expanduser()
    if not path.is_absolute():
        path = spec_path.parent / path
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Supplemental image not found: {path}")
    return path


def place_image(
    canvas: Image.Image,
    image_path: Path,
    box: tuple[int, int, int, int],
    fit_mode: str,
) -> None:
    x1, y1, x2, y2 = box
    target_size = (x2 - x1, y2 - y1)
    with Image.open(image_path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    if fit_mode == "cover":
        placed = ImageOps.fit(image, target_size, Image.Resampling.LANCZOS)
        position = (x1, y1)
    else:
        placed = ImageOps.contain(image, target_size, Image.Resampling.LANCZOS)
        position = (x1 + (target_size[0] - placed.width) // 2, y1 + (target_size[1] - placed.height) // 2)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=max(8, round(canvas.height * 0.012)), fill=(247, 244, 237, 255))
    canvas.paste(placed.convert("RGBA"), position)
    draw.rounded_rectangle(box, radius=max(8, round(canvas.height * 0.012)), outline=(151, 137, 113, 255), width=2)


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    background_path = Path(args.background).expanduser().resolve()
    reference_path = Path(args.reference_slide).expanduser().resolve()
    for path in (spec_path, background_path, reference_path):
        if not path.is_file():
            raise FileNotFoundError(path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    slides = data.get("slides") if isinstance(data, dict) else data
    if not isinstance(slides, list) or not slides:
        raise ValueError("Spec must be a nonempty list or an object with a nonempty slides list")
    font_path = choose_font(args.font)
    with Image.open(reference_path) as image:
        dimensions = image.size
    with Image.open(background_path) as image:
        background = ImageOps.fit(image.convert("RGB"), dimensions, Image.Resampling.LANCZOS)

    output_dir.mkdir(parents=True, exist_ok=True)
    width, height = dimensions
    left = round(width * 0.10)
    top = round(height * 0.12)
    panel = (round(width * 0.065), round(height * 0.065), round(width * 0.935), round(height * 0.91))
    written: list[str] = []
    images_used: list[str] = []
    for item in slides:
        if not isinstance(item, dict):
            raise ValueError("Each supplemental slide must be an object")
        filename = str(item.get("filename", ""))
        title = str(item.get("title", "")).strip()
        body = item.get("body", "")
        if isinstance(body, list):
            body = "\n".join(f"• {str(value).strip()}" for value in body if str(value).strip())
        body = str(body).strip()
        image_path = resolve_spec_image(item.get("image"), spec_path)
        image_fit = str(item.get("image_fit", "contain")).strip().lower()
        image_caption = str(item.get("image_caption", "")).strip()
        if image_fit not in {"contain", "cover"}:
            raise ValueError(f"Slide {filename!r} image_fit must be contain or cover")
        if Path(filename).name != filename or not re.fullmatch(r".+_slide_\d{4}\.png", filename):
            raise ValueError(f"Invalid slide filename: {filename!r}")
        if not title or not body:
            raise ValueError(f"Slide {filename!r} requires nonempty title and body")
        destination = output_dir / filename
        if destination.exists() and not args.overwrite:
            raise FileExistsError(f"Slide already exists: {destination}")

        canvas = background.copy().convert("RGBA")
        overlay = Image.new("RGBA", dimensions, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle(panel, radius=round(height * 0.025), fill=(255, 255, 255, 218))
        canvas.alpha_composite(overlay)
        draw = ImageDraw.Draw(canvas)
        title_font = ImageFont.truetype(str(font_path), round(height * 0.062))
        max_width = round(width * 0.80)
        title_lines = wrap_text(draw, title, title_font, max_width)
        if len(title_lines) > 2:
            raise ValueError(f"Title is too long on {filename}; shorten it")
        title_spacing = round(height * 0.012)
        title_height = len(title_lines) * title_font.size + max(0, len(title_lines) - 1) * title_spacing
        y = top
        draw.multiline_text(
            (left, y),
            "\n".join(title_lines),
            font=title_font,
            fill=(35, 43, 52, 255),
            spacing=title_spacing,
        )
        y += title_height + round(height * 0.055)
        if image_path is not None:
            max_width = round(width * 0.37)
            image_x1 = round(width * 0.53)
            image_x2 = round(width * 0.88)
            image_y1 = y
            caption_space = round(height * 0.07) if image_caption else 0
            image_y2 = panel[3] - round(height * 0.05) - caption_space
            place_image(canvas, image_path, (image_x1, image_y1, image_x2, image_y2), image_fit)
            if image_caption:
                caption_font = ImageFont.truetype(str(font_path), round(height * 0.023))
                caption_lines = wrap_text(draw, image_caption, caption_font, image_x2 - image_x1)
                if len(caption_lines) > 2:
                    raise ValueError(f"Image caption is too long on {filename}; keep it to two lines")
                draw.multiline_text(
                    (image_x1, image_y2 + round(height * 0.012)),
                    "\n".join(caption_lines),
                    font=caption_font,
                    fill=(78, 75, 68, 255),
                    spacing=round(height * 0.006),
                )
            images_used.append(str(image_path))
        max_body_height = panel[3] - y - round(height * 0.05)
        body_font, body_lines, spacing = body_font_and_lines(
            draw, body, font_path, max_width, max_body_height, height
        )
        draw.multiline_text(
            (left, y),
            "\n".join(body_lines),
            font=body_font,
            fill=(48, 55, 64, 255),
            spacing=spacing,
        )
        canvas.convert("RGB").save(destination, "PNG", compress_level=6)
        written.append(str(destination))

    print(
        json.dumps(
            {
                "count": len(written),
                "slides": written,
                "dimensions": f"{width}x{height}",
                "font": str(font_path),
                "images_used": images_used,
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
