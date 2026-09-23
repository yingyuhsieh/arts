#!/usr/bin/env python3
"""Extract a video's first complete audio stream to an AAC/M4A file."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from extract_scenes import find_ffmpeg, output_stem


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, help="Input video path")
    parser.add_argument("--output-dir", required=True, help="Directory for audio.m4a")
    parser.add_argument("--filename", help="Output filename; defaults to <video-name>_audio.m4a")
    parser.add_argument("--bitrate", default="192k", help="AAC bitrate")
    parser.add_argument("--ffmpeg", help="Explicit FFmpeg executable")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing audio file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    video = Path(args.video).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not video.is_file():
        raise FileNotFoundError(f"Video not found: {video}")
    filename = args.filename or f"{output_stem(video)}_audio.m4a"
    if Path(filename).name != filename or not filename.lower().endswith(".m4a"):
        raise ValueError("--filename must be a plain .m4a filename")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / filename
    if destination.exists() and not args.overwrite:
        raise FileExistsError(f"Audio already exists: {destination}; use --overwrite only when intended")

    ffmpeg = find_ffmpeg(args.ffmpeg)
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "warning",
        "-i",
        str(video),
        "-map",
        "0:a:0",
        "-vn",
        "-c:a",
        "aac",
        "-b:a",
        args.bitrate,
        "-movflags",
        "+faststart",
    ]
    if args.overwrite:
        command.append("-y")
    command.append(str(destination))
    subprocess.run(command, check=True)
    if not destination.is_file() or destination.stat().st_size < 1024:
        raise RuntimeError("Audio output was not created or is unexpectedly small")
    print(
        json.dumps(
            {
                "video": str(video),
                "audio": str(destination),
                "bytes": destination.stat().st_size,
                "codec": "AAC",
                "bitrate": args.bitrate,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(
            "error: FFmpeg could not extract audio. The video may not contain an audio stream.",
            file=sys.stderr,
        )
        raise SystemExit(exc.returncode or 1)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
