#!/usr/bin/env python3
"""Extract the first frame and visual scene changes from a slideshow-style video."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def output_stem(video: Path) -> str:
    """Return a filesystem-safe version of the video filename without extension."""
    stem = re.sub(r'[<>:"/\\|?*%]', "_", video.stem).strip(" .")
    return stem or "video"


def find_ffmpeg(explicit: str | None) -> str:
    if explicit:
        path = Path(explicit).expanduser()
        if path.is_file():
            return str(path)
        raise FileNotFoundError(f"FFmpeg not found: {path}")
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise RuntimeError(
            "FFmpeg is unavailable. Install FFmpeg or `pip install imageio-ffmpeg`."
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, help="Input video path")
    parser.add_argument("--output-dir", required=True, help="Directory for PNG slides")
    parser.add_argument("--threshold", type=float, default=0.18, help="Scene score threshold")
    parser.add_argument("--min-gap", type=float, default=0.5, help="Minimum seconds between frames")
    parser.add_argument("--prefix", help="Output prefix; defaults to <video-name>_slide")
    parser.add_argument(
        "--manifest",
        help="Scene manifest path; defaults to <output-dir>/<prefix>_manifest.json",
    )
    parser.add_argument("--ffmpeg", help="Explicit FFmpeg executable")
    parser.add_argument("--overwrite", action="store_true", help="Replace matching output PNGs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    video = Path(args.video).expanduser().resolve()
    output = Path(args.output_dir).expanduser().resolve()
    if not video.is_file():
        raise FileNotFoundError(f"Video not found: {video}")
    if not 0 < args.threshold < 1:
        raise ValueError("--threshold must be between 0 and 1")
    if args.min_gap < 0:
        raise ValueError("--min-gap must be nonnegative")
    prefix = args.prefix or f"{output_stem(video)}_slide"
    manifest = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else output / f"{prefix}_manifest.json"
    )

    output.mkdir(parents=True, exist_ok=True)
    existing = sorted(output.glob(f"{prefix}_*.png"))
    if existing and not args.overwrite:
        raise FileExistsError(
            f"{len(existing)} matching PNGs already exist in {output}; use --overwrite only when intended"
        )
    if manifest.exists() and not args.overwrite:
        raise FileExistsError(
            f"Scene manifest already exists: {manifest}; use --overwrite only when intended"
        )
    if args.overwrite:
        for path in existing:
            path.unlink()

    ffmpeg = find_ffmpeg(args.ffmpeg)
    expression = (
        f"select='eq(n,0)+gt(scene,{args.threshold})*"
        f"gte(t-prev_selected_t,{args.min_gap})'"
    )
    pattern = output / f"{prefix}_%04d.png"
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "info",
        "-i",
        str(video),
        "-an",
        "-vf",
        f"{expression},showinfo",
        "-fps_mode",
        "vfr",
        "-compression_level",
        "6",
        str(pattern),
    ]
    result = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
    )
    if result.returncode:
        tail = "\n".join(result.stderr.splitlines()[-20:])
        raise RuntimeError(f"FFmpeg scene extraction failed:\n{tail}")
    created = sorted(output.glob(f"{prefix}_*.png"))
    if not created:
        raise RuntimeError("No slide images were created")
    timestamps = [
        float(value)
        for value in re.findall(r"showinfo[^\r\n]*?pts_time:\s*([-+0-9.eE]+)", result.stderr)
    ]
    if len(timestamps) != len(created):
        raise RuntimeError(
            f"Found {len(created)} slides but {len(timestamps)} scene timestamps; "
            "cannot create a reliable slide/subtitle mapping"
        )
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "video": str(video),
                "prefix": prefix,
                "slides": [
                    {"filename": path.name, "start": timestamp}
                    for path, timestamp in zip(created, timestamps)
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "video": str(video),
                "output_dir": str(output),
                "count": len(created),
                "first": created[0].name,
                "last": created[-1].name,
                "prefix": prefix,
                "threshold": args.threshold,
                "min_gap": args.min_gap,
                "manifest": str(manifest),
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
