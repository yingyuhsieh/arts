---
name: create-youtube-slides
description: Create source-grounded Traditional Chinese and English 16:9 PowerPoint decks with page-matched narration files and separately saved slide backgrounds for YouTube videos about artists or artworks. Use when the user supplies art-history source material and a visual-style description and wants bilingual slides plus subtitles; do not use for editing an existing video or merely translating an existing deck.
---

# Create YouTube Slides

Turn the supplied sources into an inviting visual story for viewers with little or no art-history background. Create both language editions as native, editable PowerPoint files and keep each narration entry synchronized to its slide.

## Inputs and setup

- Treat the user's supplied files as the primary factual and visual sources. Inspect all relevant files before outlining.
- Use the supplied art-style description to define the background atmosphere, palette, texture, and graphic motifs. Do not imitate a living artist's style; translate such a request into high-level visual traits.
- Infer `<topic>` and a concise filesystem-safe `<file_topic>` from the sources when the user has not specified them. Keep the project with the relevant artist or story.
- Before authoring `.pptx` files, read and follow the available presentation-authoring skill. If original bitmap backgrounds are needed, read and follow the `imagegen` skill before generating them.
- Use the bundled channel sticker at `assets/end_sticker.png` for the required final slide. Resolve this path relative to this skill's directory, not the user's current project directory.
- The official channel name is `Our Famous Artists`. Treat this exact spelling as immutable branding. Whenever the channel name appears in visible content, narration, metadata, or filenames, reproduce it verbatim.
- Search the web only when a material fact, attribution, date, collection, interpretation, or image credit is uncertain or missing. Prefer museum collection pages, catalogues raisonnés, scholarly institutions, and other primary or authoritative sources. Distinguish documented facts from interpretation.

## Story and content

Build a coherent sequence rather than a catalogue. The opening should create curiosity, the middle should help viewers see and understand, and the ending should leave them with a memorable insight. For each substantive slide, answer as appropriate:

1. What am I looking at?
2. What should I notice?
3. Why does it matter?

Use one dominant artwork, detail, or documented artist portrait whenever possible. Preserve enough scale to appreciate the image. Give each slide one clear idea and a short headline that expresses the hook rather than merely repeating a name.

Include essential identification where relevant: artist, title, date, medium, and collection. Keep it visually secondary. Explain significance in plain language for an intelligent general audience. Highlight two to four meaningful details through restrained crops, arrows, circles, or callouts when they genuinely help viewers see the point.

Major sale or market information may be included when it materially advances the story, but verify it, provide context, and avoid sensationalizing or overstating monetary figures.

Write the Chinese edition in natural Traditional Chinese with Taiwan wording. Adapt the English edition for idiomatic English rather than translating mechanically. Keep the same slide order, visual evidence, and core claims across both editions while allowing headlines and narration to read naturally in each language.

## Visual direction

- Use a 16:9 canvas (13.333 x 7.5 inches, corresponding to 1280 x 720).
- Aim for a museum-quality editorial composition: artwork-led, spacious, restrained, historically sympathetic, and free of generic corporate slide styling.
- Make titles and essential text readable on a phone. Use large type, short sentences, strong contrast, and limited text per slide.
- Ensure text remains legible over the requested background with solid panels, gradients, overlays, shadows, or alternate placement as needed.
- Do not cover faces, focal gestures, signatures, or other important artwork details.
- Use only images that the user supplied, that are reliably sourced, or that are newly generated as non-factual decorative backgrounds. Never generate, reconstruct, or stylistically alter an artwork and present it as the historical original.
- Keep generated backgrounds subordinate to the artwork. Avoid decorative elements that compete with it.
- Add compact image/source credits on-slide or in speaker notes without weakening readability.

### Separately saved backgrounds

Save the background of every slide as a separate 1280 x 720 PNG in a shared `slide_backgrounds` directory. A background contains only the bottom visual layer: color, gradient, texture, pattern, and non-factual decorative motifs. Exclude headlines, body text, historical artworks or portraits, labels, callouts, arrows, credits, page numbers, and the channel sticker. This keeps the exported files reusable for either language edition.

Use the same numbered background for the corresponding Chinese and English slides. Name the files `<file_topic>_background_001.png`, `<file_topic>_background_002.png`, and so on, using three-digit numbering that matches `[Page N]`. If several slides use the same design, still save one correctly numbered PNG for each slide. Include the final channel end slide's plain background, without the sticker.

### Channel end slide

Append one blank-layout slide after the conclusion in both language editions. This must be the final slide and contain only the bundled `assets/end_sticker.png`, centered horizontally and vertically. Preserve its aspect ratio and transparency; do not crop, recolor, regenerate, distort, caption, or decorate it. Size it prominently while leaving comfortable empty space around it, approximately 55–65% of the slide height. Use a plain background that provides clean contrast with the sticker and add no title, body text, credits, page number, border, or other visible element.

## Narration files

Write narration that adds context and momentum instead of reading the visible text aloud. Each entry must correspond exactly to the same-numbered slide. Use exactly two lines per page: a bracketed page index followed by the narration on one line.

Calibrate the narration length for each slide according to its primary function:

| Slide function | Target narration time |
| --- | ---: |
| Hook or transition | 20–30 seconds |
| Artist background or historical context | 35–45 seconds |
| Style introduction | 40–50 seconds |
| Important artwork | 50–70 seconds |
| Close reading of an artwork | 60–90 seconds |
| Conclusion | 30–45 seconds |
| Channel end slide | 5–10 seconds |

When a slide serves more than one function, classify it by the dominant storytelling purpose rather than adding the ranges together. Treat these ranges as required pacing targets: adjust detail and sentence length to fit a natural spoken delivery in each language. Estimate with the intended narration voice when available; otherwise use a natural read-through. Do not force the Chinese and English scripts to have matching word or character counts—their slide function and target duration should match.

```text
[Page 1]
Narration for slide 1.
[Page 2]
Narration for slide 2.
```

Use `[Page N]` as the index in both languages so downstream tools can map entries reliably. Do not add blank separator lines, timestamps, duration labels, speaker names, headings, comments, or any other content to the subtitle files.

For the channel end slide, write only a natural, brief YouTube-style sign-off in the matching language. It must thank the viewer for watching and include a friendly closing greeting or invitation to return. For example, Chinese may say `感謝你的觀看，我們下次見！`, and English may say `Thank you for watching, and see you next time!` Adapt the wording naturally to the video's tone; do not copy these examples mechanically when a better matching sign-off is available. The narration may briefly invite viewers to follow the channel, but must not add unsupported claims or a long promotional message. Keep the slide itself free of visible text.

## Required outputs

Create these four primary deliverables and the accompanying background image set, making the directories when needed:

1. `./<topic>/tw_slides/<file_topic>.pptx`
2. `./<topic>/tw_slides/<file_topic>_subtitle.txt`
3. `./<topic>/en_slides/<file_topic>.pptx`
4. `./<topic>/en_slides/<file_topic>_subtitle.txt`

Save one background PNG per slide in:

5. `./<topic>/slide_backgrounds/<file_topic>_background_NNN.png`

The `en_slides` location resolves the duplicated `tw_slides` path in the original guide. The background files are supporting assets rather than additional primary deliverables. Do not add an extra report or source file unless the user requests one.

## Verification

Render both decks to images and inspect every slide before delivery. Iterate until there are no overlaps, clipping, unreadably small text, low-contrast labels, distorted images, or important details obscured by overlays. Also verify:

- both decks open successfully and use 16:9 dimensions;
- slide counts and order match between languages;
- the final slide in each deck uses a blank layout, contains only the centered bundled channel sticker, and follows the required sizing and empty-space treatment;
- every slide has exactly one matching two-line narration entry, continuously numbered as `[Page N]`;
- each narration entry fits the target duration for its slide function in both languages;
- identification, quotations, dates, market figures, and credits are source-supported;
- referenced media exists and filenames remain stable;
- the background directory contains exactly one 1280 x 720 PNG per slide, continuously numbered to match the decks and narration;
- each saved background contains no foreground content, and the corresponding Chinese and English slides use the same numbered background;
- the four primary output paths, background asset path, and UTF-8 subtitle encoding are correct.
- every occurrence of the channel name uses the exact official spelling `Our Famous Artists`.

Run `git diff --check` after creating the deliverables, and report the four primary file paths, the background directory, and the checks performed.
