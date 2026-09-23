#!/usr/bin/env python3
"""Create a static Chinese narration video from slide-named subtitle blocks."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


HEADER_RE = re.compile(r"(?ms)^\[([^\]]+\.png)\]\s*\n(.*?)(?=^\[|\Z)")
SLIDE_HEADER_RE = re.compile(
    r"(?ms)^SLIDE\s+(\d+)\s*\|[^\n]*\n(.*?)(?=^={3,}\s*$|^SLIDE\s+\d+\s*\||\Z)"
)
LOCALIZED_SLIDE_HEADER_RE = re.compile(
    r"(?ms)^━+\s*\n第\s*(\d+)\s*頁｜[^\n]*\n━+\s*\n(.*?)(?=^━+\s*$|\Z)"
)
PAGE_HEADER_RE = re.compile(
    r"(?ms)^\[Page\s+(\d+)\]\s*\n(.*?)(?=^\s*-{3,}\s*$|^\[Page\s+\d+\]|\Z)"
)
OUTPUT_DIMENSIONS = (3840, 2160)
CLAUSE_ENDINGS = frozenset("，、；：,;:。！？!?…")
SENTENCE_ENDINGS = frozenset("。！？!?…")
TRAILING_CLOSERS = frozenset("」』）》】”’\"')")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ffmpeg_path() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        path = shutil.which("ffmpeg")
        if path:
            return path
        raise RuntimeError("ffmpeg is required; install imageio-ffmpeg or add ffmpeg to PATH")


def audio_duration(path: Path) -> float:
    import av

    with av.open(str(path)) as container:
        if container.duration is None:
            raise RuntimeError(f"Cannot read audio duration: {path}")
        return float(container.duration / av.time_base)


def normalize_narration(text: str) -> str:
    """Turn subtitle-style line wrapping into natural spoken punctuation."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    spoken_paragraphs: list[str] = []
    for paragraph in re.split(r"\n\s*\n", normalized):
        lines = [" ".join(line.split()) for line in paragraph.splitlines() if line.strip()]
        if not lines:
            continue
        clauses: list[str] = []
        for index, line in enumerate(lines):
            is_last = index == len(lines) - 1
            split_at = len(line)
            while split_at > 0 and line[split_at - 1] in TRAILING_CLOSERS:
                split_at -= 1
            core, closers = line[:split_at], line[split_at:]
            if not core:
                core, closers = line, ""
            if not is_last and core[-1] not in CLAUSE_ENDINGS:
                core += "，"
            elif is_last and core[-1] not in SENTENCE_ENDINGS:
                if core[-1] in CLAUSE_ENDINGS:
                    core = core[:-1] + "。"
                else:
                    core += "。"
            clauses.append(core + closers)
        spoken_paragraphs.append("".join(clauses))
    return "".join(spoken_paragraphs)


async def synthesize(text: str, target: Path, voice: str, rate: str) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError("edge-tts is required for natural Chinese narration") from exc
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        volume="+0%",
        pitch="+0Hz",
    )
    await communicate.save(str(target))


async def synthesize_all(blocks: list[tuple[str, str]], out_dir: Path, voice: str, rate: str) -> None:
    for index, (_filename, text) in enumerate(blocks, 1):
        await synthesize(text, out_dir / f"seg_{index:04d}.mp3", voice, rate)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a static Chinese male-voice video from subtitle blocks and PNG slides."
    )
    parser.add_argument("--subtitle", required=True, type=Path, help="UTF-8 subtitle text with [slide.png] headers")
    parser.add_argument("--images-dir", required=True, type=Path, help="Directory containing the named PNG slides")
    parser.add_argument("--output-dir", type=Path, help="Video output directory (default: sibling video directory)")
    parser.add_argument("--voice", default="zh-TW-YunJheNeural", help="Edge TTS voice; default is a Taiwan Mandarin male voice")
    parser.add_argument("--rate", default="-3%", help="TTS rate adjustment; default is a slight conversational slowdown")
    parser.add_argument("--pause", type=float, default=0.6, help="Seconds of silence between slide narration blocks")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    subtitle = args.subtitle.resolve()
    images_dir = args.images_dir.resolve()
    if args.pause < 0:
        raise ValueError("--pause must be zero or greater")
    if not subtitle.is_file():
        raise FileNotFoundError(subtitle)
    if not images_dir.is_dir():
        raise NotADirectoryError(images_dir)
    output_dir = (args.output_dir or images_dir.parent / "video").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = images_dir.parent / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    stem = subtitle.stem

    raw = subtitle.read_text(encoding="utf-8")
    blocks = [(match.group(1), normalize_narration(match.group(2))) for match in HEADER_RE.finditer(raw)]
    if not blocks:
        blocks = [
            (f"{int(match.group(1)):02d}.png", normalize_narration(match.group(2)))
            for match in SLIDE_HEADER_RE.finditer(raw)
        ]
    if not blocks:
        blocks = [
            (f"Slide{int(match.group(1))}.PNG", normalize_narration(match.group(2)))
            for match in LOCALIZED_SLIDE_HEADER_RE.finditer(raw)
        ]
    if not blocks:
        blocks = [
            (f"Slide{int(match.group(1))}.PNG", normalize_narration(match.group(2)))
            for match in PAGE_HEADER_RE.finditer(raw)
        ]
    if not blocks:
        raise ValueError("No [slide.png] subtitle blocks found")
    if any(not text for _filename, text in blocks):
        raise ValueError("Every slide block must contain narration text")

    from PIL import Image

    image_paths = []
    dimensions = None
    for filename, _text in blocks:
        path = images_dir / Path(filename).name
        if path.name != filename or not path.is_file():
            raise FileNotFoundError(f"Missing image for subtitle block: {filename}")
        with Image.open(path) as image:
            size = image.size
        if dimensions is None:
            dimensions = size
        elif size != dimensions:
            raise ValueError(f"Image dimensions differ: {path} is {size}, expected {dimensions}")
        image_paths.append(path)

    ffmpeg = ffmpeg_path()
    with tempfile.TemporaryDirectory(prefix="tw-make-video-") as temp_name:
        temp = Path(temp_name)
        tts_dir = temp / "tts"
        norm_dir = temp / "norm"
        tts_dir.mkdir()
        norm_dir.mkdir()
        asyncio.run(synthesize_all(blocks, tts_dir, args.voice, args.rate))

        for index in range(1, len(blocks) + 1):
            run(
                [
                    ffmpeg,
                    "-y",
                    "-loglevel",
                    "error",
                    "-i",
                    str(tts_dir / f"seg_{index:04d}.mp3"),
                    "-ar",
                    "44100",
                    "-ac",
                    "1",
                    "-c:a",
                    "pcm_s16le",
                    str(norm_dir / f"seg_{index:04d}.wav"),
                ]
            )
        pause_path = temp / "pause.wav"
        run(
            [
                ffmpeg,
                "-y",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=44100:cl=mono",
                "-t",
                str(args.pause),
                "-c:a",
                "pcm_s16le",
                str(pause_path),
            ]
        )

        audio_concat = temp / "audio_concat.txt"
        audio_lines = []
        for index in range(1, len(blocks) + 1):
            audio_lines.append(f"file '{(norm_dir / f'seg_{index:04d}.wav').as_posix()}'")
            if index < len(blocks):
                audio_lines.append(f"file '{pause_path.as_posix()}'")
        audio_concat.write_text("\n".join(audio_lines) + "\n", encoding="utf-8")
        audio_out = audio_dir / f"{stem}_narration_male_natural.wav"
        run(
            [
                ffmpeg,
                "-y",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(audio_concat),
                "-c:a",
                "pcm_s16le",
                "-ar",
                "44100",
                "-ac",
                "1",
                str(audio_out),
            ]
        )

        durations = []
        pause_duration = audio_duration(pause_path)
        for index in range(1, len(blocks) + 1):
            duration = audio_duration(norm_dir / f"seg_{index:04d}.wav")
            if index < len(blocks):
                duration += pause_duration
            durations.append(duration)

        video_concat = temp / "slides_concat.txt"
        video_lines = []
        for index, image_path in enumerate(image_paths):
            video_lines.append(f"file '{image_path.as_posix()}'")
            video_lines.append(f"duration {durations[index]:.6f}")
        # The concat demuxer needs the last image repeated to honor its duration.
        video_lines.append(f"file '{image_paths[-1].as_posix()}'")
        video_concat.write_text("\n".join(video_lines) + "\n", encoding="utf-8")
        video_out = output_dir / f"{stem}_natural_male.mp4"
        total_duration = sum(durations)
        run(
            [
                ffmpeg,
                "-y",
                "-loglevel",
                "warning",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(video_concat),
                "-i",
                str(audio_out),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-t",
                f"{total_duration:.6f}",
                "-vf",
                (
                    f"scale={OUTPUT_DIMENSIONS[0]}:{OUTPUT_DIMENSIONS[1]}:"
                    "force_original_aspect_ratio=decrease:flags=lanczos,"
                    f"pad={OUTPUT_DIMENSIONS[0]}:{OUTPUT_DIMENSIONS[1]}:"
                    "(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,"
                    f"tpad=stop_mode=clone:stop_duration={durations[-1]:.6f}"
                ),
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-r",
                "30",
                "-fps_mode",
                "cfr",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                "-movflags",
                "+faststart",
                str(video_out),
            ]
        )

    print(
        json.dumps(
            {
                "video": str(video_out),
                "audio": str(audio_out),
                "voice": args.voice,
                "pause_seconds": args.pause,
                "line_breaks": "punctuation_normalized",
                "slides": len(blocks),
                "duration_seconds": round(total_duration, 3),
                "source_dimensions": dimensions,
                "dimensions": OUTPUT_DIMENSIONS,
                "motion": "none",
                "external_subtitles": False,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
