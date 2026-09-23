---
name: rewrite-artist-story
description: Rewrite an artist-focused Markdown source into an engaging, source-checked biographical blog article and save it beside the source with a _blog.md suffix. Use when the user supplies an artist .md file and asks to rewrite, transform, expand, or research it as a readable artist story rather than a chronological or encyclopedia-style biography.
---

# Rewrite Artist Story

Turn source notes into a vivid artist biography that uses story to invite readers in, artworks to hold their attention, and a human life to make the artist memorable.

## Workflow

1. Resolve the user-provided `.md` file and read it completely as UTF-8. Treat its directory as the project directory and its stem as `source_stem`.
2. Inspect nearby research notes and image assets when their relationship to the artist is clear. Do not rename or alter source files.
3. Identify the article's language, reliable facts, central tension, three decisive life or artistic turning points, two or three work-based themes, and missing evidence.
4. Search the web for required or missing facts. Prefer museum collection records, artist foundations or estates, catalogue raisonnés, archives, universities, and reputable scholarly publications. Cross-check disputed or consequential claims with more than one reliable source.
5. Rewrite the article using the five-act structure and voice below. Integrate life and work instead of separating them into isolated timelines and catalogues.
6. Save the completed article beside the source as `<source_stem>_blog.md`. Never overwrite the supplied source.
7. Reopen the output and verify its facts, links, structure, language, filename, and Markdown rendering.

## Voice

Use roughly 70% story-driven literary reportage and 30% plain-language curatorial explanation. Sound like a perceptive guide walking beside the reader: warm, visual, specific, and informed. Prefer short sentences and keep ordinary paragraphs to no more than four lines where practical.

Use first person only for an honest observation grounded in material actually inspected. Never invent a museum visit, interview, studio scene, quotation, emotion, motive, or private thought. Distinguish documented fact from interpretation. Avoid claiming that a personal event directly caused an artwork unless reliable evidence supports that connection.

Translate technical art language into sensory description. Replace abstract praise such as "bold color" with concrete observations about hue, surface, light, scale, rhythm, gesture, space, or bodily effect. Ask occasional open questions so the reader can look and decide; do not lecture.

Preserve the language and regional usage of the source unless the user requests another language. For Traditional Chinese, use natural Taiwan wording and full-width Chinese punctuation.

## Five-Act Structure

### 0. Opening hook

Keep the opening under 200 Chinese characters or an equivalently brief passage in another language. Begin inside a representative artwork, charged moment, visual contradiction, or unresolved question. Do not begin with birth date and birthplace. Combine a visible scene, a tension or mystery, and a promise of what the article will reveal.

### 1. Who is this person?

Give the reader one memorable sentence that locates the artist without stacking titles or accolades.

### 2. Where did the artist come from?

Choose only three turning points: an awakening, a setback or low point, and the emergence of a distinct artistic language. For each, answer: how did this change what or how the artist made? Do not reproduce a complete chronology.

### 3. What are the works saying?

Devote about half the article to two or three thematic movements rather than a list of works. For each theme, examine only one or two representative works using this sequence:

1. What can the reader see?
2. Why might the artist have made these choices, based on evidence?
3. What might a viewer feel or reconsider?

Link biography to artworks at the relevant moments. Keep interpretation open where the evidence is incomplete.

### 4. What remains?

Explain what the artist changed: artistic practice, contemporary reception, later artists, institutions, or how viewers see. Prefer concrete influence over prize and exhibition lists. Answer why the work still merits attention now.

### 5. Closing echo

Return to the opening image or tension. End with a concise personal reflection grounded in the works and one meaningful question for the reader.

## Markdown and Images

- Use descriptive H2 and H3 headings that tell a story even when skimmed on a phone.
- Bold only a few key lines worth remembering; do not over-emphasize.
- Pair each major narrative beat with one relevant image when a suitable local or responsibly linkable image is available. Use nearby local assets preferentially and URL-encode paths when needed. Do not fabricate filenames, reuse an unrelated image, or download copyrighted media merely to fill space.
- Give every included image useful alt text and a concise caption or credit when known.
- Place a compact information card beside or immediately after each deeply discussed work:

  > **Work information**  
  > Year: ...  
  > Medium: ...  
  > Dimensions: ...  
  > Collection: ...

- Omit or clearly mark an unknown field rather than guessing.

## Research and Citation Rules

- Preserve useful source-file detail, but correct errors supported by stronger evidence.
- Cite researched facts with descriptive inline Markdown links near the relevant claim. Add a short `## Sources` list at the end for the most important references; do not dump raw search results.
- Attribute quotations to a traceable source and keep excerpts brief. Paraphrase when wording is not essential.
- Verify artwork title, date, medium, dimensions, and collection against the holding institution or another authoritative catalogue whenever possible.
- Do not silently turn legend, gossip, or retrospective diagnosis into fact. Label uncertainty and scholarly disagreement plainly.
- Do not add facts merely because they are interesting. Every researched addition must strengthen the narrative, explain a work, or fill a material gap.

## Final Check

Confirm all of the following before reporting completion:

- The output path is exactly `<source_stem>_blog.md` in the source directory.
- The original Markdown file is unchanged.
- The opening is a scene, tension, or question rather than a birth record.
- Three turning points connect life to artistic change.
- About half the article closely examines works through two or three themes.
- Claims, quotations, work data, images, and links are verified and not invented.
- H2/H3 headings, short paragraphs, selective bolding, artwork cards, and sources render cleanly.
- The ending echoes the opening and leaves the reader with one genuine question.
