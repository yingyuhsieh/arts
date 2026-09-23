#!/usr/bin/env python3
"""Detect language or transcribe audio into slide-aligned UTF-8 text."""

from __future__ import annotations

import argparse
import bisect
import json
import sys
from pathlib import Path

from extract_scenes import output_stem


def traditional_chinese_converter():
    """Return an OpenCC converter for Traditional Chinese with Taiwan wording."""
    try:
        from opencc import OpenCC
    except ImportError as exc:
        raise RuntimeError(
            "Install OpenCC before Chinese transcription: pip install opencc-python-reimplemented"
        ) from exc
    return OpenCC("s2twp")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", required=True, help="Input audio path")
    parser.add_argument("--video", help="Video path used for the output filename")
    parser.add_argument("--output-dir", help="Subtitle text directory")
    parser.add_argument("--slide-manifest", help="JSON manifest produced by extract_scenes.py")
    parser.add_argument("--model", default="small", help="faster-whisper model name or path")
    parser.add_argument("--language", choices=["auto", "zh", "en"], default="auto")
    parser.add_argument("--device", default="cpu", help="faster-whisper device")
    parser.add_argument("--compute-type", default="int8", help="faster-whisper compute type")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing transcript")
    parser.add_argument(
        "--detect-only",
        action="store_true",
        help="Print detected language and work-folder prefix without writing a transcript",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Install faster-whisper before transcription: pip install faster-whisper") from exc

    audio = Path(args.audio).expanduser().resolve()
    if not audio.is_file():
        raise FileNotFoundError(f"Audio not found: {audio}")
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    language = None if args.language == "auto" else args.language
    segments, info = model.transcribe(
        str(audio),
        language=language,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=True,
    )
    detected_language = info.language.lower()
    if args.detect_only:
        if detected_language.startswith("zh"):
            folder_prefix = "tw"
        elif detected_language.startswith("en"):
            folder_prefix = "en"
        else:
            raise RuntimeError(
                f"Detected unsupported language {info.language!r}; select --language zh or en"
            )
        print(
            json.dumps(
                {
                    "audio": str(audio),
                    "language": info.language,
                    "language_probability": info.language_probability,
                    "folder_prefix": folder_prefix,
                    "work_directory": f"{folder_prefix}_slides",
                    "model": args.model,
                },
                ensure_ascii=False,
            )
        )
        return 0

    if not args.video or not args.output_dir or not args.slide_manifest:
        raise ValueError(
            "--video, --output-dir, and --slide-manifest are required unless --detect-only is used"
        )
    video = Path(args.video).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    manifest_path = Path(args.slide_manifest).expanduser().resolve()
    if not video.is_file():
        raise FileNotFoundError(f"Video not found: {video}")
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Slide manifest not found: {manifest_path}")
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    slide_entries = manifest_data.get("slides")
    if not isinstance(slide_entries, list) or not slide_entries:
        raise ValueError("Slide manifest has no slides")
    slide_names: list[str] = []
    slide_starts: list[float] = []
    for entry in slide_entries:
        if not isinstance(entry, dict) or "filename" not in entry or "start" not in entry:
            raise ValueError("Every manifest slide must contain filename and start")
        slide_names.append(str(entry["filename"]))
        slide_starts.append(float(entry["start"]))
    if slide_starts != sorted(slide_starts):
        raise ValueError("Slide manifest timestamps are not sorted")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{output_stem(video)}.txt"
    if destination.exists() and not args.overwrite:
        raise FileExistsError(f"Transcript already exists: {destination}; use --overwrite only when intended")

    converter = traditional_chinese_converter() if detected_language.startswith("zh") else None
    grouped: list[list[str]] = [[] for _ in slide_names]
    count = 0
    for segment in segments:
        text = segment.text.strip()
        if not text:
            continue
        if converter is not None:
            text = converter.convert(text)
        midpoint = (float(segment.start) + float(segment.end)) / 2
        slide_index = max(0, bisect.bisect_right(slide_starts, midpoint) - 1)
        slide_index = min(slide_index, len(grouped) - 1)
        grouped[slide_index].append(text)
        count += 1
    if not count:
        raise RuntimeError("Transcription produced no text")
    blocks: list[str] = []
    for slide_name, texts in zip(slide_names, grouped):
        blocks.append("\n".join([f"[{slide_name}]", *texts]))
    destination.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "audio": str(audio),
                "subtitle": str(destination),
                "language": info.language,
                "language_probability": info.language_probability,
                "traditional_chinese": converter is not None,
                "segments": count,
                "slides": len(slide_names),
                "slide_manifest": str(manifest_path),
                "model": args.model,
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
