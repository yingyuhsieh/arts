"""Verify output streams, ordered static slides, audio and original inputs."""

from pathlib import Path
import hashlib
import json
import math
import subprocess
import wave

import av
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
STEM = "Mantegna__The_Vantage_Point"
VIDEO = ROOT / "video" / f"{STEM}_natural_male.mp4"
AUDIO = ROOT / "audio" / f"{STEM}_narration_male_natural.wav"


def main():
    source_manifest = json.loads((ROOT / "video" / f"{STEM}_inputs.json").read_text())
    timing = json.loads((ROOT / "video" / f"{STEM}_timings.json").read_text())
    meta = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(VIDEO)]))
    streams = meta["streams"]
    video = [s for s in streams if s["codec_type"] == "video"]
    audio = [s for s in streams if s["codec_type"] == "audio"]
    assert len(streams) == 2 and len(video) == len(audio) == 1
    assert (video[0]["width"], video[0]["height"]) == (3840, 2160)
    assert video[0]["sample_aspect_ratio"] == "1:1"
    assert video[0]["codec_name"] == "h264" and audio[0]["codec_name"] == "aac"
    assert video[0]["r_frame_rate"] == "30/1"
    assert abs(float(video[0]["duration"]) - float(audio[0]["duration"])) < 0.15

    thumbnails = []
    for item in source_manifest:
        path = Path(item["source"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        image = Image.open(path).convert("RGB")
        thumbnails.append(np.asarray(ImageOps.pad(image, (160, 90), method=Image.Resampling.LANCZOS), dtype=np.float32))
    references = np.stack(thumbnails)

    # A static slideshow's repeated GOP keyframes must classify as the same
    # supplied slide until a hard cut advances to the next supplied image.
    transitions = []
    max_rmse = 0.0
    with av.open(str(VIDEO)) as container:
        stream = container.streams.video[0]
        stream.codec_context.skip_frame = "NONKEY"
        stream.thread_type = "AUTO"
        last = None
        for frame in container.decode(stream):
            thumb = np.asarray(frame.to_image().resize((160, 90), Image.Resampling.LANCZOS), dtype=np.float32)
            errors = np.mean((references - thumb) ** 2, axis=(1, 2, 3))
            index = int(np.argmin(errors))
            rmse = math.sqrt(float(errors[index]))
            assert rmse < 8, (frame.time, index + 1, rmse)
            max_rmse = max(max_rmse, rmse)
            if index != last:
                transitions.append({"slide": index + 1, "time": round(float(frame.time), 6)})
                last = index
    assert [t["slide"] for t in transitions] == list(range(1, len(source_manifest) + 1))

    # Independently sample twice inside every scheduled slide hold.
    sample_count = 0
    with av.open(str(VIDEO)) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        for i, item in enumerate(timing["slides"]):
            for portion in (0.25, 0.75):
                target = item["start"] + item["duration"] * portion
                container.seek(round(target * av.time_base), backward=True)
                for frame in container.decode(stream):
                    if frame.time + 1 / 30 < target:
                        continue
                    thumb = np.asarray(frame.to_image().resize((160, 90), Image.Resampling.LANCZOS), dtype=np.float32)
                    errors = np.mean((references - thumb) ** 2, axis=(1, 2, 3))
                    assert int(np.argmin(errors)) == i, (i + 1, target)
                    assert math.sqrt(float(errors[i])) < 8
                    sample_count += 1
                    break
    assert sample_count == len(source_manifest) * 2

    with wave.open(str(AUDIO)) as wav:
        wav_duration = wav.getnframes() / wav.getframerate()
        samples = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
        rms = math.sqrt(float(np.mean(samples.astype(np.float64) ** 2)))
        assert rms > 100
    assert abs(float(video[0]["duration"]) - wav_duration) < 0.15
    report = {
        "video": str(VIDEO), "audio": str(AUDIO),
        "duration_seconds": wav_duration, "slide_count": len(source_manifest),
        "source_dimensions": sorted({tuple(s["dimensions"]) for s in source_manifest}),
        "output_dimensions": [3840, 2160], "fps": 30,
        "voice": "en-US-AndrewMultilingualNeural", "rate": "-3%", "inter_slide_pause": 1.5,
        "streams": {"video": 1, "audio": 1, "subtitles": 0},
        "hard_cuts": len(transitions) - 1, "ordered_slide_transitions": transitions,
        "static_hold_samples_verified": sample_count,
        "maximum_keyframe_thumbnail_rmse": max_rmse,
        "wav_rms": rms, "original_input_hashes_unchanged": True,
    }
    (ROOT / "video" / f"{STEM}_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
