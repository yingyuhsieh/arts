---
name: tw-make-video
description: Create a 4K Chinese static-slide narration video from a UTF-8 subtitle file and a directory of named PNG images. Use when the user provides a subtitle path and image-folder path and wants a natural Taiwan Mandarin male voice, preserved image text and artwork, no camera motion, and no large external subtitles.
---

# TW Make Video

## Overview

Turn slide-named Traditional Chinese narration and matching PNG files into a polished 4K UHD 3840 x 2160 MP4. The workflow uses the Taiwan Mandarin male neural voice `zh-TW-YunJheNeural`, keeps the voice at a natural conversational rate, converts subtitle-style line wrapping into punctuation-guided spoken phrasing, adds short pauses between slide sections, and holds each image completely still. It never adds a competing full-screen subtitle layer.

## Inputs

Require:

1. `--subtitle`: UTF-8 text file with one block per image:

   ```text
   [洛倫澤蒂：錫耶納的哲學畫家_slide_0001.png]
   第一段旁白。

   [洛倫澤蒂：錫耶納的哲學畫家_slide_0002.png]
   第二段旁白。
   ```

2. `--images-dir`: directory containing every PNG named in the bracketed headers.

The header order is the video order. Do not infer order from filesystem modification time.

## Default outputs

With an images directory such as `<author-dir>/tw_slides/update`, write:

```text
<author-dir>/tw_slides/audio/<video-name>_narration_male_natural.wav
<author-dir>/tw_slides/video/<video-name>_natural_male.mp4
```

Override the video directory with `--output-dir` when needed. The script derives `<video-name>` from the subtitle filename.

## Workflow

### 1. Validate the source pair

- Read the subtitle as UTF-8 and extract exact `[filename.png]` headers.
- Require nonempty narration for every block.
- Resolve each header against `--images-dir`; stop if any image is missing.
- Inspect image dimensions and require one common width and height.
- Preserve the image content, including text and artwork. Do not restyle, crop, distort, or regenerate the images. The encoder may only scale each complete slide proportionally to fit the 4K UHD canvas and add centered padding when its aspect ratio is not 16:9.

### 2. Generate natural male narration

Run the bundled script, which calls Edge TTS sequentially with `zh-TW-YunJheNeural` and a slight `-3%` conversational adjustment. Keep the default voice and rate unless the user explicitly requests another male voice or speaking rate.

```text
python scripts/make_tw_video.py \
  --subtitle <subtitle-path> \
  --images-dir <images-directory>
```

Before synthesis, the script normalizes narration inside each slide block so that single line breaks become short Chinese clause boundaries and paragraph endings become sentence boundaries. This prevents Edge TTS from treating every source line wrap as a long standalone pause. Existing punctuation is preserved, and the source subtitle file is never modified.

The script adds a default 0.6-second silence between narration blocks. This is a brief slide-transition pause, not a speed change. Use `--pause` to adjust transitions when the user requests a different rhythm. Reject negative pause values.

Do not use `atempo`, time compression, pitch shifting, or speech trimming. Let the output runtime follow the generated narration and pauses. If the runtime is longer than an arbitrary target, report the actual duration.

### 3. Build the static video

For each block, hold its matching image for the actual normalized audio duration plus the inter-block pause. Encode as 4K UHD 3840 x 2160 H.264 video with AAC audio at 30 fps. Scale proportionally with high-quality Lanczos resampling and center-pad when necessary; never crop or stretch the slide.

The visual layer must:

- contain only the supplied images;
- use hard cuts or static holds, with no zoom, pan, horizontal translation, crop, or Ken Burns effect;
- contain no externally rendered subtitles, captions, title cards, or large text overlays;
- retain all text and illustrations already present inside each image.

### 4. Verify

- Confirm every subtitle header has exactly one matching image and the sequence has no gaps.
- Confirm the MP4 contains one video and one audio stream, with matching durations within a small encoding tolerance.
- Confirm the MP4 video stream is exactly 3840 x 2160 with square pixels and every frame is the complete source image held static, proportionally scaled and center-padded when necessary.
- Confirm the audio is nonempty and the voice is `zh-TW-YunJheNeural` unless the user chose another male voice.
- Confirm subtitle-style line breaks were punctuation-normalized before synthesis and report the effective inter-slide pause.
- Confirm no `atempo`, speed-up, pitch-shift, external subtitle, zoom, or pan filter was used.
- Report the absolute paths of the MP4, narration WAV, actual runtime, slide count, source dimensions, 4K UHD output dimensions, and voice.

## Dependencies

Install when missing:

```text
python -m pip install edge-tts imageio-ffmpeg av pillow
```

The bundled script discovers FFmpeg through `imageio-ffmpeg`; a system `ffmpeg` on PATH is an accepted fallback.

## Bundled resource

- `scripts/make_tw_video.py`: validates subtitle/image mapping, synthesizes natural male narration, adds pauses, and encodes the static MP4 without motion or external subtitles.
