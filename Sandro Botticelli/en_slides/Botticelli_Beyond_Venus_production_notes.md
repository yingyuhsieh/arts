# Botticelli Beyond Venus — production notes

- Detected language: English (probability 0.9991).
- Source video: 549.732426 seconds, 1280 × 720, 24 fps.
- Complete extracted AAC audio: 549.731995 seconds (about 9:09.73); no speed or pitch changes.
- Original slides: 21. Supplemental slides: 2. Final updated PNGs: 23.
- All 23 final PNGs were opened and visually inspected at 1280 × 720; all PNGs decode successfully.
- All 23 subtitle blocks exactly match final PNG filenames, once each, in final order; no timestamps.
- The updated slides have the lower-right Gemini Notebook wordmark removed.
- The original final page was reflowed to retain its exact wording around the sticker, then moved from 0021 to 0023. The reorder script verified its SHA-256 before applying the complete centered 468 × 468 end sticker.
- Original scene PNGs and the timing manifest retain the source order. Updated order is 0001–0020, Dante 0021, reception 0022, original ending 0023.
- Source video and unrelated pre-existing files were left untouched.

## Audio and supplemental narration

The M4A is the complete original video audio. The two added pages have new English narration text in their matching subtitle blocks, but that new narration has not been synthesized or inserted into the source audio. No new video has been exported. The M4A therefore follows the original 21-page timing manifest, rather than the reordered 23-page sequence. For a later narrated video, synthesize the two new blocks at natural rate and insert them before the original ending; let the resulting runtime grow.

## Markdown reviewed

- Sandro Botticelli (complete).md
- Sandro Botticelli chatgpt.md
- Sandro Botticelli claude.md
- Sandro Botticelli 最重要的的作品.md
- sandro_botticelli_youtube_en.md
- sandro_botticelli_youtube_tw.md

All six directly contained Markdown files were read. Where older drafts disagree with the consolidated article, the consolidated article and the more cautious, source-attributed interpretation were preferred for supplemental content. The artwork checklist and bilingual outlines were also compared with the source transcript. No subdirectory Markdown or images were used for additions.

## Supplemental content and support

| Final page | Added topic | Author-directory support |
|---|---|---|
| 0021 | Dante: Line Becomes a Journey | Sandro Botticelli (complete).md — 但丁圖稿：讓線條承載一場旅程; Sandro Botticelli chatgpt.md — 替但丁尋找圖像 |
| 0022 | How Venus Became an Icon | Sandro Botticelli (complete).md — 被重新觀看的波提切利; Sandro Botticelli chatgpt.md — 1510年之後 |

No directly contained candidate artwork image files were present in the author directory, so both supplemental pages are text-only. They do not duplicate topics actually developed in the source slides or spoken transcript.

## Transcription corrections

Ten supported recognition, spelling, punctuation, or title-capitalization corrections were applied; no historical claim in the spoken narration was silently rewritten.

| Before | After |
|---|---|
| of Sondro Botticelli. | of Sandro Botticelli. |
| They're slightly tilted heads | Their slightly tilted heads |
| the merchants court in Florence | the merchants’ court in Florence |
| a Lutuccio | a lettuccio |
| in Palace in the Centaur | in Pallas and the Centaur |
| Botticelli through his own | Botticelli threw his own |
| the Calumni of Appellis | the Calumny of Apelles |
| forward by Calumni and deceit | forward by Calumny and deceit |
| intensity totally piques in the mystic nativity | intensity totally peaks in the Mystic Nativity |
| in the events in the life of Moses | in the Events in the Life of Moses |

Names and artwork titles are supported by the author Markdown. The homophones their/they’re, threw/through, peaks/piques and the possessive punctuation were resolved from their spoken grammatical context.

## Image identification clarification

Page 0012 retains the source caption “Events of Moses on the Sistine Chapel side wall.” Its displayed fresco is The Punishment of Korah, Dathan and Abiram, a different subject within the Moses cycle. An explicit image-clarification callout was added above the original wording. The following page’s Moses narrative was retained. Support: Sandro Botticelli (complete).md, “羅馬牆上的律法與權威,” and its source 12; independently checked against [Aix-Marseille University / Utpictura18](https://utpictura18.univ-amu.fr/en/notice/10139-the-punishment-of-korah-datan-and-abiram-sistine-chapel-botticelli) and the [Vatican Museums Moses cycle](https://www.museivaticani.va/content/museivaticani/en/collezioni/musei/cappella-sistina/parete-sud/storie-di-mose.html).

## Readability and visual treatment

The original text and pictorial content were restyled deterministically. Original full pages were not generated again. Readability changes affect pages 0002, 0004, 0006, 0009, 0013, 0014, 0016 and the final page: clean ivory text backings, larger labels, stronger title weight, clear spacing and exact-word reflow. The four Moses nodes retain their wording and sequence, with aligned cards and darker sage arrows. Ambiguous decorative lettering inside the source illustrations was preserved rather than guessed. Both supplemental pages use 43-pixel titles and 33-pixel body text. The reusable background is 16:9, with no people, text, logos, or watermark.

## Deliverables

- Background: /Users/yingyuhsieh/Desktop/mcp/arts/Sandro Botticelli/en_slides/Botticelli_Beyond_Venus_background.png
- Updated slides: /Users/yingyuhsieh/Desktop/mcp/arts/Sandro Botticelli/en_slides/update
- Audio: /Users/yingyuhsieh/Desktop/mcp/arts/Sandro Botticelli/en_slides/audio/Botticelli_Beyond_Venus_audio.m4a
- Subtitle / narration text: /Users/yingyuhsieh/Desktop/mcp/arts/Sandro Botticelli/en_slides/subtitle/Botticelli_Beyond_Venus.txt
- Original scene timing: /Users/yingyuhsieh/Desktop/mcp/arts/Sandro Botticelli/en_slides/Botticelli_Beyond_Venus_slide_manifest.json
- Reorder record: /Users/yingyuhsieh/Desktop/mcp/arts/Sandro Botticelli/en_slides/update/Botticelli_Beyond_Venus_slide_reorder.json

## Background generation

Generated with the built-in image_gen tool. The original generated image was copied into the project and resized from 1672 × 941 to the exact source dimensions, 1280 × 720. Final prompt:

Use case: productivity-visual
Asset type: reusable 16:9 presentation background, landscape.
Primary art direction, verbatim: Use an elegant Early Italian Renaissance style inspired by Sandro Botticelli, with delicate ivory, soft rose, pale turquoise, muted ultramarine, sage green, warm golden ochre, and subtle coral tones, combining refined egg-tempera textures with graceful flowing contours, elongated idealized figures, ethereal facial expressions, intricately patterned fabrics, and rhythmic windswept drapery, incorporating classical mythological motifs, delicate floral meadows, orange groves, gently rippling seas, seashell forms, and harmonious Florentine landscapes, with subtle gold accents and decorative linear patterns evoking The Birth of Venus and Primavera, creating a poetic atmosphere of timeless beauty, humanist elegance, mythological enchantment, and spiritual refinement, while preserving spacious softly illuminated negative space, restrained botanical ornament, and gentle tonal contrasts so the artwork, titles, and subtitles remain visually dominant.
Composition constraints for this background asset: interpret the style through botanical and seashell ornaments and faint landscape only. No people or figures despite figurative references in the art direction. No foreground paintings. Very quiet nearly plain pale ivory center spanning 80% of the canvas, with delicate low-contrast ornamental edges and corners only. High legibility for dark presentation text. No text, letters, numbers, logos, or watermark. Exact 16:9 aspect ratio.

