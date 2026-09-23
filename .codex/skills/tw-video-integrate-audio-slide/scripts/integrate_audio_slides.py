#!/usr/bin/env python3
"""Integrate supplied narration audio with timed static PNG slides."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


FILENAME_HEADER_RE = re.compile(r"(?ms)^\[([^\]]+\.png)\]\s*\n(.*?)(?=^\[|\Z)")
SLIDE_HEADER_RE = re.compile(
    r"(?ms)^(?:SLIDE|投影片|幻燈片)\s*(\d+)\s*[|｜]\s*([^\n]*)\n(.*?)(?=^={3,}\s*$|^(?:SLIDE|投影片|幻燈片)\s*\d+\s*[|｜]|\Z)"
)
PAGE_HEADER_RE = re.compile(r"(?ms)^\[(?:Page\s+|第\s*)(\d+)(?:\s*頁)?\]\s*\n(.*?)(?=^\[|\Z)")
TIME_RE = re.compile(r"(?<!\d)(?:(\d+):)?(\d{1,2}):(\d{2}(?:\.\d+)?)")


OUTPUT_DIMENSIONS = (3840, 2160)
OUTPUT_FPS = 30
VIDEO_FILTER = (
    "scale=3840:2160:force_original_aspect_ratio=decrease:flags=lanczos,"
    "pad=3840:2160:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=30"
    ",tpad=stop_mode=clone:stop_duration=1"
)


@dataclass(frozen=True)
class SlideBlock:
    filename: str
    narration: str
    start: float | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a static-slide MP4 using an existing narration audio track."
    )
    parser.add_argument("--subtitle", required=True, type=Path)
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--preset", default="medium")
    return parser.parse_args()


def ffmpeg_path() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        path = shutil.which("ffmpeg")
        if path:
            return path
        raise RuntimeError("FFmpeg is required; install imageio-ffmpeg or add ffmpeg to PATH")


def media_duration(path: Path) -> float:
    import av

    with av.open(str(path)) as container:
        if container.duration is None:
            raise RuntimeError(f"Cannot read duration: {path}")
        return float(container.duration / av.time_base)


def parse_time(value: str) -> float | None:
    match = TIME_RE.search(value)
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def parse_blocks(raw: str, images_dir: Path) -> list[SlideBlock]:
    filename_blocks = [
        SlideBlock(match.group(1), match.group(2).strip())
        for match in FILENAME_HEADER_RE.finditer(raw)
    ]
    if filename_blocks:
        return filename_blocks

    pages = list(PAGE_HEADER_RE.finditer(raw))
    if pages:
        pngs = sorted(images_dir.glob('*.png'), key=lambda p: [int(x) if x.isdigit() else x.casefold() for x in re.split(r'(\d+)', p.name)])
        numbers = [int(m.group(1)) for m in pages]
        if numbers != list(range(1, len(pngs) + 1)):
            raise ValueError('Page headers must cover every PNG exactly once in order, starting at 1')
        return [SlideBlock(p.name, m.group(2).strip()) for p, m in zip(pngs, pages)]

    numbered = list(SLIDE_HEADER_RE.finditer(raw))
    if not numbered:
        return []
    pngs = sorted(images_dir.glob("*.png"), key=lambda path: path.name.casefold())
    blocks: list[SlideBlock] = []
    for match in numbered:
        number = int(match.group(1))
        if number < 1 or number > len(pngs):
            raise ValueError(f"SLIDE {number:02d} has no corresponding sorted PNG")
        blocks.append(
            SlideBlock(
                filename=pngs[number - 1].name,
                narration=match.group(3).strip(),
                start=parse_time(match.group(2)),
            )
        )
    return blocks


def discover_manifest(images_dir: Path, subtitle_stem: str) -> Path | None:
    preferred = [
        images_dir / f"{subtitle_stem}_slide_manifest.json",
        images_dir / f"{subtitle_stem}_manifest.json",
    ]
    for path in preferred:
        if path.is_file():
            return path
    candidates = sorted(images_dir.glob("*_slide_manifest.json"))
    return candidates[0] if len(candidates) == 1 else None


def starts_from_manifest(manifest: Path, blocks: list[SlideBlock]) -> list[float]:
    payload = json.loads(manifest.read_text(encoding="utf-8-sig"))
    slides = payload.get("slides")
    if not isinstance(slides, list):
        raise ValueError(f"Manifest has no slides list: {manifest}")
    filenames = [Path(str(item.get("filename", ""))).name for item in slides]
    starts = [float(item["start"]) for item in slides]
    expected = [block.filename for block in blocks]
    if filenames != expected:
        raise ValueError("Manifest slide order does not exactly match the narration headers")
    return starts


def validate_starts(starts: list[float], audio_duration: float) -> list[float]:
    if not math.isfinite(audio_duration) or audio_duration <= 0:
        raise ValueError('Audio duration must be positive and finite')
    if any(not math.isfinite(value) or value < 0 for value in starts):
        raise ValueError('Slide start times must be finite and nonnegative')
    if not starts:
        raise ValueError("No slide timing values found")
    if starts[0] != 0:
        raise ValueError("The first slide must start at 0 seconds")
    if any(right <= left for left, right in zip(starts, starts[1:])):
        raise ValueError("Slide start times must be strictly increasing")
    if starts[-1] >= audio_duration:
        raise ValueError("The last slide starts at or after the end of the audio")
    durations = [right - left for left, right in zip(starts, starts[1:])]
    durations.append(audio_duration - starts[-1])
    if any(duration <= 0 for duration in durations):
        raise ValueError("Every slide must have a positive duration")
    return durations


def concat_quote(path: Path) -> str:
    normalized = path.resolve().as_posix().replace("'", "'\\''")
    return f"'{normalized}'"


def inspect_audio_codec(path: Path) -> str:
    import av

    with av.open(str(path)) as container:
        streams = list(container.streams.audio)
        if not streams:
            raise ValueError(f"No audio stream found: {path}")
        return streams[0].codec_context.name


def verify_output(path: Path, output_dimensions: tuple[int, int], expected_duration: float) -> dict:
    import av

    with av.open(str(path)) as container:
        video_streams = list(container.streams.video)
        audio_streams = list(container.streams.audio)
        subtitle_streams = list(container.streams.subtitles)
        if len(video_streams) != 1 or len(audio_streams) != 1 or subtitle_streams:
            raise RuntimeError("Output must contain one video stream, one audio stream, and no subtitles")
        video = video_streams[0]
        audio = audio_streams[0]
        video_duration = float(video.duration * video.time_base)
        audio_duration = float(audio.duration * audio.time_base)
        if (video.codec_context.width, video.codec_context.height) != output_dimensions:
            raise RuntimeError(f"Output dimensions must be {output_dimensions}")
        if video.codec_context.name != "h264" or audio.codec_context.name != "aac":
            raise RuntimeError("Output codecs must be H.264 video and AAC audio")
        if abs(float(video.average_rate) - float(OUTPUT_FPS)) > 0.001:
            raise RuntimeError("Output frame rate is not 30 fps")
        if audio_duration <= 0:
            raise RuntimeError("Output audio is empty")
        if abs(video_duration - audio_duration) > 0.1:
            raise RuntimeError("Video and audio durations differ by more than 0.1 seconds")
        if abs(audio_duration - expected_duration) > 0.1:
            raise RuntimeError("Output audio duration differs from the supplied audio")
        return {
            "video_codec": video.codec_context.name,
            "audio_codec": audio.codec_context.name,
            "video_duration_seconds": round(video_duration, 3),
            "audio_duration_seconds": round(audio_duration, 3),
            "fps": float(video.average_rate),
            "video_frames": video.frames,
            "subtitle_streams": len(subtitle_streams),
        }


def main() -> None:
    args = parse_args()
    subtitle = args.subtitle.resolve()
    images_dir = args.images_dir.resolve()
    audio = args.audio.resolve()
    if not subtitle.is_file():
        raise FileNotFoundError(subtitle)
    if not images_dir.is_dir():
        raise NotADirectoryError(images_dir)
    if not audio.is_file():
        raise FileNotFoundError(audio)
    if not 0 <= args.crf <= 51:
        raise ValueError("--crf must be between 0 and 51")

    blocks = parse_blocks(subtitle.read_text(encoding="utf-8-sig"), images_dir)
    if not blocks:
        raise ValueError("No supported narration blocks found")
    if any(not block.narration for block in blocks):
        raise ValueError("Every slide block must contain narration")
    if len({block.filename for block in blocks}) != len(blocks):
        raise ValueError("Narration headers contain duplicate image filenames")

    from PIL import Image

    image_paths: list[Path] = []
    dimensions: tuple[int, int] | None = None
    for block in blocks:
        image_path = images_dir / Path(block.filename).name
        if image_path.name != block.filename or not image_path.is_file():
            raise FileNotFoundError(f"Missing slide image: {block.filename}")
        with Image.open(image_path) as image:
            size = image.size
        if dimensions is None:
            dimensions = size
        elif size != dimensions:
            raise ValueError(f"Slide dimensions differ: {image_path} is {size}, expected {dimensions}")
        image_paths.append(image_path)
    assert dimensions is not None
    if dimensions[0] % 2 or dimensions[1] % 2:
        raise ValueError("Slide width and height must be even for yuv420p output")

    audio_duration = media_duration(audio)
    manifest = args.manifest.resolve() if args.manifest else discover_manifest(images_dir, subtitle.stem)
    if manifest:
        if not manifest.is_file():
            raise FileNotFoundError(manifest)
        starts = starts_from_manifest(manifest, blocks)
        timing_source = str(manifest)
    elif all(block.start is not None for block in blocks):
        starts = [float(block.start) for block in blocks if block.start is not None]
        timing_source = "subtitle headers"
    else:
        raise ValueError(
            "No reliable timing source. Provide --manifest or timestamp every SLIDE header."
        )
    durations = validate_starts(starts, audio_duration)

    output = (
        args.output.resolve()
        if args.output
        else (images_dir / "video" / f"{subtitle.stem}_4k.mp4").resolve()
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = ffmpeg_path()
    audio_codec = inspect_audio_codec(audio)

    with tempfile.TemporaryDirectory(prefix="tw-video-integrate-") as temp_name:
        concat_file = Path(temp_name) / "slides.ffconcat"
        lines = ["ffconcat version 1.0"]
        for image_path, duration in zip(image_paths, durations):
            lines.append(f"file {concat_quote(image_path)}")
            lines.append(f"duration {duration:.6f}")
        lines.append(f"file {concat_quote(image_paths[-1])}")
        concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        command = [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-t",
            f"{audio_duration:.6f}",
            "-c:v",
            "libx264",
            "-preset",
            args.preset,
            "-crf",
            str(args.crf),
            "-profile:v",
            "high",
            "-level:v",
            "5.1",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            VIDEO_FILTER,
            "-r",
            str(OUTPUT_FPS),
            "-fps_mode",
            "cfr",
        ]
        if audio_codec == "aac":
            command.extend(["-c:a", "copy"])
        else:
            command.extend(["-c:a", "aac", "-b:a", "192k"])
        command.extend(["-movflags", "+faststart", str(output)])
        subprocess.run(command, check=True)

    verification = verify_output(output, OUTPUT_DIMENSIONS, audio_duration)
    result = {
        "video": str(output),
        "file_bytes": output.stat().st_size,
        "source_audio": str(audio),
        "timing_source": timing_source,
        "slides": len(blocks),
        "expected_hard_cuts": len(blocks) - 1,
        "source_dimensions": list(dimensions),
        "dimensions": list(OUTPUT_DIMENSIONS),
        "scaling": "proportional Lanczos; no crop",
        "motion": "none",
        "external_subtitles": False,
        **verification,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
