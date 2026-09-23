---
name: video-to-slides
description: Convert a Chinese or English slideshow-style video into language-prefixed work folders, prefixed PNG scene frames, a complete audio track, and slide-named subtitles. Convert Chinese text to Traditional Chinese with Taiwan wording, apply an artistic background, remove a lower-right NotebookLM mark, compare subtitles with author-directory Markdown, correct supported errors, add useful missing content as new PNG slides using relevant author-directory images when available, move the video's original final slide behind all additions, add an end sticker, and preserve natural narration speed when additions extend the runtime. Use when the user provides a local video path plus a background-style description and wants presentation frames, audio, subtitles, source enrichment, or redesigned slides.
---

# Video to Slides

Require only:

1. Video path
2. Background style description

Use the video filename without its extension as `<video-name>`. Treat the source video's parent directory as `<author-dir>`. Prefix every persistent generated file with `<video-name>`.

Choose the work directory from the detected speech language:

- English: `<author-dir>/en_slides/`
- Chinese: `<author-dir>/tw_slides/`

Use exactly `en_slides` and `tw_slides`, including the underscore. For a silent video, determine the language from visible slide text; ask only if it is genuinely ambiguous.

Default layout:

```text
<author-dir>/<en_slides-or-tw_slides>/
  <video-name>_background.png
  <video-name>_slide_0001.png
  <video-name>_slide_manifest.json
  ...
  audio/<video-name>_audio.m4a
  subtitle/<video-name>.txt
  update/<video-name>_slide_0001.png
  ...
  update/<video-name>_slide_reorder.json  # only when supplemental pages were inserted
```

## Workflow

### 1. Inspect inputs and detect language

- Confirm the video exists and read its duration, resolution, frame rate, and audio stream.
- Treat the background description verbatim as the art direction.
- Do not modify the source video.
- Preserve unrelated files and files belonging to another video.
- Install `faster-whisper` and `opencc-python-reimplemented` only when unavailable.

Extract complete audio to a temporary directory, then detect the language:

```text
python scripts/extract_audio.py --video <video> --output-dir <temporary-dir>
python scripts/transcribe_audio.py --audio <temporary-audio> --detect-only
```

Use `folder_prefix` from the JSON result: `en` selects `en_slides`; `tw` selects `tw_slides`. If automatic detection is wrong, repeat with `--language en` or `--language zh`. Move or re-extract the complete audio as `<work-dir>/audio/<video-name>_audio.m4a`, then delete the temporary copy.

### 2. Extract scene frames and timing manifest

Run:

```text
python scripts/extract_scenes.py --video <video> --output-dir <work-dir>
```

Write `<video-name>_slide_0001.png`, `<video-name>_slide_0002.png`, and so on, plus `<video-name>_slide_manifest.json`. The manifest records the start time and filename of every extracted slide for subtitle alignment. Defaults: include the first frame, scene threshold `0.18`, minimum gap `0.5` seconds. Retry with `--threshold 0.12` for missed slow fades or `--threshold 0.24` for duplicates.

### 3. Transcribe into slide-named sections

Run:

```text
python scripts/transcribe_audio.py \
  --audio <work-dir>/audio/<video-name>_audio.m4a \
  --video <video> \
  --slide-manifest <work-dir>/<video-name>_slide_manifest.json \
  --output-dir <work-dir>/subtitle
```

Use automatic language detection and the `small` model on CPU/int8 by default. Convert Chinese segments with OpenCC `s2twp`; leave English text unchanged. Group speech by the midpoint of each segment and the scene start times.

Write UTF-8 `subtitle/<video-name>.txt` without timestamps. Include every slide, even one without speech, in this form:

```text
[<video-name>_slide_0001.png]
Spoken text associated with this slide.

[<video-name>_slide_0002.png]
Next slide's spoken text.
```

Keep the bracketed filename exact so each subtitle section maps to one PNG.

### 4. Generate one reusable background

Use the available image-generation capability and follow the `imagegen` skill when present. Generate one clean 16:9 background from the user's style description, not one full slide per frame. Require:

- quiet, low-contrast center and decorative edges
- no people, foreground paintings, text, letters, logos, or watermark
- high legibility for dark presentation text

Save it permanently as `<work-dir>/<video-name>_background.png`. Preserve this reusable background slide image as a final deliverable after all slide generation and verification are complete; do not delete it during cleanup.

### 5. Restyle while preserving content

Install `pillow`, `numpy`, and `opencv-python-headless` only when necessary. Run:

```text
python scripts/style_slides.py \
  --video <video> \
  --slides-dir <work-dir> \
  --background <work-dir>/<video-name>_background.png \
  --output-dir <work-dir>/update \
  --contact-sheet <work-dir>/<video-name>_contact-check.png
```

Preserve colored illustrations and dark text, blend the background into light neutral regions, and remove the repeated lower-right NotebookLM mark. Use `--strength 0.65` through `0.90` if needed. Never regenerate original full pages when exact text and artwork must remain unchanged.

### 6. Review author Markdown and add or correct content

Read every `*.md` file directly inside `<author-dir>`. Also enumerate directly contained `*.jpg`, `*.jpeg`, `*.png`, `*.webp`, `*.tif`, and `*.tiff` files as candidate supplemental visuals. Do not recurse into subdirectories, language work directories, or `.codex`. If no Markdown exists, record that the review had no source files and continue.

Compare the Markdown with the slide-aligned subtitle for:

- key concepts or facts relevant to the video's topic but missing from both slides and subtitle
- examples, cautions, definitions, or conclusions that materially improve completeness
- speech-recognition errors, names, technical terms, or wording that the Markdown clearly resolves
- contradictions; prefer the audio for what was spoken and use Markdown only as evidence for corrections or explicit supplemental material

Correct supported errors directly inside the relevant subtitle block. Preserve the exact bracketed PNG filename and Traditional Chinese with Taiwan wording. Do not silently rewrite claims when the Markdown is uncertain or unrelated.

Create new slides only when the Markdown contains useful, relevant, non-duplicate material. Continue the existing four-digit sequence after the highest filename in `update`. Add one subtitle block for each new page containing a concise narration or explanation of its added material.

For every new page, inspect candidate author-directory images with `view_image` rather than trusting filenames alone. If an image clearly supports that page's subject, use it. Prefer a directly relevant artwork, portrait, map, diagram, or location image over generic decoration. Do not use an unrelated, illegible, corrupted, or misleading image. Use a text-only supplemental page only when no suitable author image exists.

Prepare a temporary UTF-8 JSON spec such as:

```json
{
  "slides": [
    {
      "filename": "<video-name>_slide_0013.png",
      "title": "補充重點",
      "body": ["First point", "Second point"],
      "image": "<author-dir>/relevant-artwork.jpg",
      "image_fit": "contain",
      "image_caption": "Artwork title or concise source label"
    }
  ]
}
```

Render the new PNGs directly into `update` with the same background and dimensions:

```text
python scripts/create_supplemental_slides.py \
  --spec <temporary-spec.json> \
  --output-dir <work-dir>/update \
  --background <work-dir>/<video-name>_background.png \
  --reference-slide <work-dir>/update/<video-name>_slide_0001.png
```

Use `image_fit: contain` by default to preserve an entire artwork. Use `cover` only when cropping is harmless. Omit `image`, `image_fit`, and `image_caption` together for a text-only page.

Split dense content across multiple pages instead of shrinking it excessively. If no material addition is justified, do not create a placeholder page. Delete the temporary JSON spec after verification.

### 7. Move the original final slide behind additions

When supplemental slides exist, first render and subtitle them with numbers after the original final slide. Then run:

```text
python scripts/reorder_final_slide.py \
  --manifest <work-dir>/<video-name>_slide_manifest.json \
  --update-dir <work-dir>/update \
  --subtitle <work-dir>/subtitle/<video-name>.txt
```

If the original video contains `N` slides and `K` supplemental slides, produce this final contiguous order:

```text
original 0001 ... original N-1
supplemental N ... supplemental N+K-1
original final slide renamed to N+K
```

Move the original final slide; do not leave a duplicate at its old number and do not create a substitute blank end page. The script also renames and reorders matching subtitle blocks and writes `<video-name>_slide_reorder.json` in `update` with the original-final hash. Skip this step when no supplemental slides were created.

### 8. Add the end sticker last

After all original and supplemental slides are final, run:

```text
python scripts/compose_end_sticker.py \
  --video <video> \
  --slides-dir <work-dir>/update
```

Use `assets/end_sticker.png` unless the user supplies another sticker. Overlay it centered on the final prefixed PNG at about 65% of slide height. This must occur after supplemental-page rendering and final-slide reordering so the moved original final slide receives the sticker.

### 9. Preserve narration speed when additions extend runtime

- Keep the selected narration voice's natural speaking rate and pitch. Do not accelerate, time-compress, or pitch-shift the audio to force the output back to the source video's duration or an arbitrary target such as ten minutes.
- When supplemental slides add narration, let the final audio and video become longer. Derive each slide's static hold duration from its actual narration segment, concatenate the segments without `atempo` speed-up, and extend the final video to the resulting audio duration.
- Do not trim spoken content to satisfy a target duration. If a user requests an approximate duration, report the actual duration and preserve intelligibility; only edit the script length when the user explicitly asks for a shorter narration.
- When additions are image-only, hold each new image for the requested/default reading duration without changing the speed of the existing narration.

### 10. Verify

- Confirm the work directory is `en_slides` for English or `tw_slides` for Chinese.
- Confirm the original slide count matches the manifest and `update` contains the original count plus any justified supplemental slides.
- When additions exist, confirm the original final slide appears exactly once, at the highest slide number, with supplemental slides immediately before it and no numbering gap. Confirm the reorder record's SHA-256 matched the moved final slide before the sticker was applied.
- Confirm all persistent outputs begin with `<video-name>`, except the `subtitle/<video-name>.txt` extension form.
- Confirm `<work-dir>/<video-name>_background.png` exists, opens correctly, is 16:9, and contains no text, people, logos, or watermark.
- Confirm each updated and supplemental PNG matches the source dimensions.
- Inspect the contact sheet plus title, text-heavy, image-heavy, supplemental, and final slides. Confirm each selected author-directory image is relevant, legible, uncropped when `contain` is requested, and not stretched.
- Verify the NotebookLM wordmark is absent and the actual final slide contains the complete end sticker.
- Confirm the audio is nonempty and matches the generated video duration. When supplemental slides exist, allow the generated audio/video duration to exceed the source duration and report the actual runtime; never treat that extension as a reason to accelerate the narration.
- Confirm every original and supplemental PNG has one exact bracketed filename block in the UTF-8 subtitle file, in slide order and without timestamps.
- Confirm Chinese subtitle and supplemental text use Traditional Chinese with Taiwan wording.
- Confirm every correction or addition is supported by the audio or an author-directory Markdown file.
- Delete temporary audio, contact sheet, and supplemental JSON only after the final readability pass. Keep `<video-name>_background.png` as a persistent output.
- Report the language, original slide count, supplemental slide count, Markdown files reviewed, corrections made, and absolute paths for the background, `update`, audio, and subtitle outputs.

### 11. Perform a final visual-readability pass on every updated slide

After every preceding action is complete, inspect every prefixed PNG in `<work-dir>/update/`, not only a contact-sheet sample. Open each slide at its actual output resolution and confirm that a viewer can read all text clearly during normal video playback.

- Check titles, body text, captions, labels, and text over images for adequate font size, contrast, line spacing, margins, and uncluttered placement.
- Treat clipped text, overly long lines, dense paragraphs, low-contrast lettering, text crossing artwork details, and inconsistent visual hierarchy as readability failures.
- Adjust every title that is not immediately readable. Use a clear title hierarchy, sufficient size and weight, strong contrast, concise line breaks, and generous spacing from slide edges and nearby content. Keep title styling consistent across the deck without changing the title's supported meaning.
- Inspect every flow diagram at full resolution. Improve its layout when needed so the reading direction is obvious, nodes are aligned and evenly spaced, connectors and arrowheads are unambiguous, labels do not collide with shapes or lines, and related steps share a restrained, consistent visual treatment.
- Beautify flow diagrams without adding unsupported claims or decorative clutter. Prefer simple shapes, balanced whitespace, a limited harmonious palette, consistent stroke widths and corner radii, and clear emphasis for the start, decision, key transition, and end states. Preserve the original logic, wording, and sequence.
- Redraw low-resolution diagram text, shapes, connectors, or arrows only when their content can be read with certainty. If any wording or relationship is ambiguous, preserve it and improve readability through contrast, spacing, or a clean backing panel instead of guessing.
- Adjust only the affected slides. Shorten or rewrap text without changing its supported meaning, enlarge type where needed, strengthen text/background contrast, and reposition text away from busy imagery.
- Split a dense supplemental slide into multiple consecutively numbered slides instead of shrinking its text. Keep the original final slide last, update subtitle blocks and the reorder record when numbering changes, and reapply the end sticker to the actual final slide.
- For original video slides, preserve the exact wording and artwork. Improve readability with safe layout, background, or contrast adjustments; do not recreate text with guessed wording or silently alter factual content.
- Reopen every adjusted PNG and verify it again at actual output resolution. Confirm that all text, titles, and flow-diagram labels are clear, that its subtitle filename still matches exactly, and that all updated PNGs retain the source dimensions.
- Never delete the reusable background. Do not delete the contact sheet or supplemental JSON until this pass and any required rerendering are complete.

## Resources

- `scripts/extract_scenes.py`: extract prefixed frames and write their timing manifest.
- `scripts/extract_audio.py`: extract prefixed AAC/M4A audio.
- `scripts/transcribe_audio.py`: detect language or create slide-named subtitles; convert Chinese to Traditional Chinese with Taiwan wording.
- `scripts/style_slides.py`: restyle prefixed slides and remove NotebookLM marks.
- `scripts/create_supplemental_slides.py`: render reviewed Markdown additions as numbered text/image PNGs, using relevant author-directory visuals when supplied.
- `scripts/reorder_final_slide.py`: insert supplemental pages before the original final slide and synchronize subtitle filenames/order.
- `scripts/compose_end_sticker.py`: add the bundled sticker to the actual final updated slide.
- `assets/end_sticker.png`: default transparent ending sticker.
