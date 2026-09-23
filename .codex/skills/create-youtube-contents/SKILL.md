---
name: create-youtube-contents
description: Create source-grounded Traditional Chinese and English YouTube content plans for artists, artworks, or art-history stories, including visual-first segments, verified image URLs and rights, a reusable asset list, and fact-checking notes. Use when the user supplies reference files and wants a bilingual video structure or production-ready content research rather than slides, narration, or a finished video.
---

# Create YouTube Contents

Turn the user's reference files into two detailed, visual-first Markdown plans for an art-history YouTube video. Build an engaging story for viewers without specialist knowledge; do not merely summarize the files or arrange an artist's life as a chronology.

## Inputs and source handling

- Read every user-supplied reference file relevant to the topic before outlining. Use the appropriate document, PDF, presentation, spreadsheet, image, audio, or video capability when a format requires it.
- Treat the supplied files as the primary research corpus, but verify material claims and image metadata against current authoritative sources. Search the web because the deliverables require usable image URLs, current collection data, rights information, and fact-checking.
- Prefer museum and gallery collection records, libraries and archives, Wikimedia Commons, Google Arts & Culture, Europeana, public-domain cultural institutions, universities, catalogues raisonnés, and scholarly sources. For factual conflicts, prioritize the most authoritative primary or institutional record and document the discrepancy.
- Do not invent missing stories or infer an image license. Write `Needs verification` when rights cannot be confirmed.
- Infer the main artist, artwork, or story and a concise English `<file_topic>` when the user has not named one. Use lowercase, replace spaces with underscores, remove unsuitable punctuation, and choose the artist's name for an artist-led video or the artwork title for a work-led video.
- Unless the user specifies another destination, save both outputs beside the primary reference file or in the common directory containing the supplied references. Keep the files with the relevant artist or story.

## Editorial approach

First identify, in two to four sentences, what genuinely makes the subject worth knowing. Use one core narrative to connect artist, artwork, historical context, visual analysis, and storytelling.

Organize the video into approximately 6–10 segments, assigning more space to major works and turning points. The sequence should usually include:

1. A hook built around a question, contradiction, revealing detail, surprising fact, or art-historical mystery—not a birth-date introduction.
2. Only the artist and historical context needed to understand the later works.
3. The formation of the artist's visual language through relevant teachers, cities, patrons, markets, courts, religion, politics, travel, or artistic influence.
4. Several key artworks as the main body of the video.
5. Legacy and why the work still matters to museum visitors.
6. A closing that returns to the opening question and gives viewers a new way to look at art.

Do not force this exact numbering when the sources support a stronger structure. By the end, a general viewer should recognize the artist's visual character, understand at least 3–5 important works when the corpus supports that many, know why they matter, and know what to notice in a museum.

For each major artwork, explain what the viewer sees, what to notice first, how composition, light, color, pose, symbols, technique, and material guide interpretation, how the work compares with relevant works, and why it matters. Use only the dimensions, collection history, patronage, provenance, or market information that advances the story.

## Segment content

Each segment must contain:

```markdown
## Segment X — [Title]

**Purpose**
[The segment's role in the whole video.]

**Key Message**
[The one idea viewers should retain.]

**Content**
[A detailed outline, not a finished voice-over. Aim for roughly 100–250 Chinese characters in the Traditional Chinese version and comparable depth in idiomatic English.]

**Artwork / Person / Place Mentioned**
- Artist: ...
- Artwork: ...
- Historical Person: ...
- Museum: ...
- City: ...
- Building: ...
- Historical Event: ...

**Visual Assets and Image URLs**
[Three to six educationally useful assets.]

**Suggested Visual Sequence**
1. ...
```

Omit empty entity categories or mark them with an em dash; do not fabricate an entry merely to fill the schema.

## Visual research

Plan three to six meaningful visual assets per segment. Favor the rhythm `Story → Artwork → Detail → Explanation → Comparison → Context → Artwork`. Prioritize artworks, revealing details, comparisons, portraits, historical photographs, manuscripts, maps, museums, churches, palaces, studios, cities, architecture, and historical documents. Avoid generic stock images, AI-generated substitutes for historical works, social-media reposts, personal blogs, unclear image hosts, watermarked commercial images, and visuals that do not teach the viewer anything.

For every externally sourced visual, provide:

- **Image ID:** stable `IMG-001` style identifier; reuse the same ID whenever the same source image appears again.
- **Artwork / Image**
- **Artist**
- **Date**
- **Museum / Source**
- **Purpose in Video**
- **Source Page:** the institutional or repository record, not a search-results page.
- **Direct Image URL:** a confirmed JPG, JPEG, PNG, or other actual image file when available. Do not relabel a collection page as a direct image URL; use `Not available` when no stable direct file is confirmed.
- **Rights:** the source's explicit status, such as `Public Domain`, `CC0`, `CC BY`, `Open Access`, or `Copyrighted`; otherwise `Needs verification`.

Prefer public-domain or open-access images. Confirm that URLs resolve and that each record identifies the intended work. If an artwork detail can be made from the verified high-resolution master, reuse its Image ID, say `Crop from high-resolution artwork image`, identify the crop target precisely, and do not invent a second source record.

For each segment, arrange the assets into an editable visual sequence. Use feasible effects such as `Slow Zoom In`, `Slow Zoom Out`, `Pan Left`, `Pan Right`, `Detail Crop`, `Cross Dissolve`, `Side-by-Side Comparison`, `Timeline`, `Map Zoom`, `Artwork Overlay`, or `Text Highlight`. These are production notes, not permission to crop, animate, or download files unless the user asks for those actions.

## Fact-checking

Verify, when present, artwork title and attribution, date, museum, dimensions, historical events, biography, commission and patron, technique, ownership and provenance, quotations, and image rights. Cite or link the authoritative source near the relevant record. Keep interpretation distinguishable from established fact.

Record source disagreements, corrected facts, unresolved disputes, missing evidence, and uncertain licenses under `Fact-Checking Notes`. Never silently preserve a claim contradicted by a stronger source.

## Required output structure

Create both complete files; do not merely print their contents in the response:

- `<file_topic>_youtube_tw.md` in natural Traditional Chinese with Taiwan wording.
- `<file_topic>_youtube_en.md` in idiomatic English adapted for English-language art education, not translated line by line.

Both files must follow this order:

1. `A. Video Core Narrative`
2. `B. Recommended Video Titles` with three inviting, accurate, non-clickbait options.
3. `C. Video Structure` listing all segments.
4. `D. Detailed Segment Plan`, with Purpose → Key Message → Content → Artwork / Person / Place Mentioned → Visual Assets and Image URLs → Suggested Visual Sequence for every segment.
5. `E. Complete Image Asset List`
6. `F. Missing Visuals`
7. `G. Fact-Checking Notes`

Use this complete asset table in section E:

```markdown
| ID | Segment | Artist | Artwork / Image | Date | Museum / Source | Purpose in Video | Source Page | Direct Image URL | Rights |
|---|---|---|---|---|---|---|---|---|---|
```

The two language files must have the same research structure, segment order, factual claims, Image IDs, Source Page URLs, Direct Image URLs, and Rights values. Titles, segment names, explanations, and other prose should read naturally in each language.

## Final verification

Before delivery, confirm that:

- both Markdown files exist at the intended location and use UTF-8;
- the segment count is within the intended range unless the sources justify a documented exception;
- every segment answers what the viewer should see on screen;
- every listed image has a stable ID and appears only once in the complete asset list;
- repeated images reuse their IDs across segments and languages;
- source pages and direct image URLs are distinguished and tested;
- rights are source-supported or marked `Needs verification`;
- the Chinese and English asset data match exactly;
- missing or disputed material is disclosed rather than invented;
- Markdown tables and links render cleanly; and
- `git diff --check` reports no whitespace errors in the created files.
