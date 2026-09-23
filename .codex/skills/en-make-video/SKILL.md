---
name: en-make-video
description: Create a 4K English static-slide narration video from a UTF-8 slide narration file and a directory of matching PNG images. Use when the user provides English per-slide narration plus PNG slides and wants a natural English male voice, preserved image text and artwork, no camera motion, and no large external subtitles.
---

# EN Make Video

## Overview

Turn English per-slide narration and matching PNG files into a polished 4K UHD 3840 x 2160 MP4. Use the natural male neural voice `en-US-AndrewMultilingualNeural` at a slightly relaxed `-3%` rate, insert short pauses between slides, and hold every supplied image completely still. Do not add a competing subtitle layer.

## Inputs

Require:

1. `--subtitle`: a UTF-8 narration file in either supported format.

   Exact filename headers:

   ```text
   [01.png]
   Narration for the first slide.

   [02.png]
   Narration for the second slide.
   ```

   Numbered slide headers, mapped to zero-padded PNG names:

   ```text
   SLIDE 01 | 00:00-00:25
   Narration for the first slide.

   ========================================================================

   SLIDE 02 | 00:25-01:10
   Narration for the second slide.
   ```

   `SLIDE 01` maps to `01.png`. Header order determines video order; timestamps are descriptive and do not force the runtime.

2. `--images-dir`: a directory containing every referenced PNG.

## Workflow

### 1. Validate

- Parse every slide block and require nonempty narration.
- Resolve every header against `--images-dir` and stop on missing images.
- Require one common image width and height.
- Preserve the slide content, text, and artwork. Do not restyle, crop, distort, or regenerate slides. The encoder may only scale each complete slide proportionally to fit the 4K UHD canvas and add centered padding when its aspect ratio is not 16:9.

### 2. Generate narration and video

Run:

```text
python scripts/make_en_video.py \
  --subtitle <subtitle-path> \
  --images-dir <images-directory>
```

Defaults:

- voice: `en-US-AndrewMultilingualNeural`
- rate: `-3%`
- inter-slide pause: `1.5` seconds
- audio: `<images-parent>/audio/<subtitle-stem>_narration_male_natural.wav`
- video: `<images-parent>/video/<subtitle-stem>_natural_male.mp4`

Use `--voice`, `--rate`, `--pause`, or `--output-dir` only when the user explicitly requests a different setting. Do not use `atempo`, time compression, pitch shifting, or speech trimming. Let the runtime follow the generated narration and pauses.

### 3. Preserve the visual layer

- Use only the supplied images.
- Use static holds and hard cuts only.
- Do not zoom, pan, translate, crop, animate, or apply a Ken Burns effect.
- Do not render external subtitles, captions, title cards, or large text overlays.
- Encode 4K UHD 3840 x 2160 H.264 video and AAC audio at 30 fps. Use high-quality Lanczos proportional scaling and centered padding when necessary; never crop or stretch the slide.

### 4. Verify

- Confirm every narration block has exactly one matching image and the order has no gaps.
- Confirm the MP4 contains one video stream, one audio stream, and no subtitle stream.
- Confirm video and audio durations match within normal encoding tolerance.
- Confirm the MP4 video stream is exactly 3840 x 2160 with square pixels, the complete source slide is visible without distortion, and the audio is nonempty.
- Confirm the number of hard cuts equals the slide count minus one.
- Report absolute paths for the MP4 and WAV, actual runtime, slide count, source dimensions, 4K UHD output dimensions, and voice.

## Dependencies

Install only when missing:

```text
python -m pip install edge-tts imageio-ffmpeg av pillow
```

The script discovers FFmpeg through `imageio-ffmpeg`; a system `ffmpeg` on `PATH` is also accepted.

## Bundled resource

- `scripts/make_en_video.py`: validate narration/image mapping, synthesize natural English male narration, add pauses, and encode a static MP4 without motion or external subtitles.
