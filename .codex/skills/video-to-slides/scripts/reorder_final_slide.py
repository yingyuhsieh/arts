#!/usr/bin/env python3
"""Insert supplemental slides before the original final slide and reorder subtitles."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


HEADER_RE = re.compile(r"^\[([^\]]+\.png)\]$", re.MULTILINE)
NUMBER_RE = re.compile(r"^(.*_slide_)(\d{4})\.png$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Scene manifest from extract_scenes.py")
    parser.add_argument("--update-dir", required=True, help="Directory containing original and supplemental PNGs")
    parser.add_argument("--subtitle", required=True, help="Slide-named UTF-8 subtitle text file")
    return parser.parse_args()


def split_subtitle_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(HEADER_RE.finditer(text))
    if not matches:
        raise ValueError("Subtitle contains no bracketed PNG headers")
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[start:end].strip("\r\n")))
    return blocks


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def numbered_path(directory: Path, base: str, number: int) -> Path:
    return directory / f"{base}{number:04d}.png"


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    update_dir = Path(args.update_dir).expanduser().resolve()
    subtitle_path = Path(args.subtitle).expanduser().resolve()
    for path in (manifest_path, subtitle_path):
        if not path.is_file():
            raise FileNotFoundError(path)
    if not update_dir.is_dir():
        raise FileNotFoundError(update_dir)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("slides")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Manifest contains no slides")
    original_count = len(entries)
    original_final_name = str(entries[-1].get("filename", ""))
    match = NUMBER_RE.fullmatch(original_final_name)
    if not match or int(match.group(2)) != original_count:
        raise ValueError("Manifest final filename is not a contiguous four-digit slide number")
    base = match.group(1)
    record_path = update_dir / f"{base}reorder.json"
    if record_path.exists():
        raise FileExistsError(f"Final slide was already reordered: {record_path}")

    slides = sorted(update_dir.glob(f"{base}*.png"))
    numbered: dict[int, Path] = {}
    for slide in slides:
        slide_match = NUMBER_RE.fullmatch(slide.name)
        if slide_match and slide_match.group(1) == base:
            numbered[int(slide_match.group(2))] = slide
    if not numbered:
        raise FileNotFoundError(f"No {base}NNNN.png files found in {update_dir}")
    final_count = max(numbered)
    expected = set(range(1, final_count + 1))
    if set(numbered) != expected:
        raise ValueError("Update slide numbering must be contiguous before reordering")
    if final_count <= original_count:
        raise ValueError("No supplemental slides follow the original final slide")

    subtitle_text = subtitle_path.read_text(encoding="utf-8")
    blocks = split_subtitle_blocks(subtitle_text)
    block_names = [name for name, _ in blocks]
    slide_names = [numbered[index].name for index in range(1, final_count + 1)]
    if block_names != slide_names:
        raise ValueError("Subtitle headers must exactly match update PNGs before reordering")
    content_by_name = dict(blocks)

    old_final = numbered_path(update_dir, base, original_count)
    old_final_hash = sha256(old_final)
    temp_final = update_dir / f".{base}original-final.tmp"
    temp_subtitle = subtitle_path.with_suffix(subtitle_path.suffix + ".reorder.tmp")
    if temp_final.exists() or temp_subtitle.exists():
        raise FileExistsError("A previous reorder temporary file exists; inspect it before retrying")

    renames: list[dict[str, str]] = []
    reordered_blocks: list[tuple[str, str]] = []
    for index in range(1, original_count):
        name = numbered_path(update_dir, base, index).name
        reordered_blocks.append((name, content_by_name[name]))
    for old_index in range(original_count + 1, final_count + 1):
        old_name = numbered_path(update_dir, base, old_index).name
        new_name = numbered_path(update_dir, base, old_index - 1).name
        reordered_blocks.append((new_name, content_by_name[old_name]))
        renames.append({"from": old_name, "to": new_name})
    new_final_name = numbered_path(update_dir, base, final_count).name
    reordered_blocks.append((new_final_name, content_by_name[old_final.name]))
    new_subtitle = "\n\n".join(
        "\n".join(part for part in (f"[{name}]", content) if part)
        for name, content in reordered_blocks
    ) + "\n"
    temp_subtitle.write_text(new_subtitle, encoding="utf-8")

    try:
        old_final.rename(temp_final)
        for old_index in range(original_count + 1, final_count + 1):
            numbered_path(update_dir, base, old_index).rename(
                numbered_path(update_dir, base, old_index - 1)
            )
        temp_final.rename(numbered_path(update_dir, base, final_count))
        temp_subtitle.replace(subtitle_path)
    except Exception:
        if temp_subtitle.exists():
            temp_subtitle.unlink()
        raise

    if sha256(numbered_path(update_dir, base, final_count)) != old_final_hash:
        raise RuntimeError("Original final slide hash changed during reordering")
    record = {
        "manifest": str(manifest_path),
        "original_count": original_count,
        "supplemental_count": final_count - original_count,
        "original_final": {"from": old_final.name, "to": new_final_name, "sha256": old_final_hash},
        "supplemental_renames": renames,
        "subtitle": str(subtitle_path),
    }
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**record, "record": str(record_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
