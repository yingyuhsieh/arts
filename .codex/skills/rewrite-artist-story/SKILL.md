---
name: rewrite-artist-story
description: Rewrite an artist-focused Markdown source into an engaging, source-checked biographical blog article and save it beside the source with a _blog.md suffix. Use when the user supplies an artist .md file and asks to rewrite, transform, expand, or research it as a readable artist story rather than a chronological or encyclopedia-style biography.
---

# Rewrite Artist Story

Turn source notes into a vivid artist biography that uses story to invite readers in, artworks to hold their attention, and a human life to make the artist memorable.

## Workflow

1. Resolve the user-provided `.md` file and read it completely as UTF-8. Treat its directory as the project directory and its stem as `source_stem`.
2. Inspect nearby research notes and image assets when their relationship to the artist is clear. Do not rename or alter source files.
3. Identify the article's language, reliable facts, central contradiction, major life and artistic turning points, representative works, professional relationships, reception history, and missing evidence.
4. Search the web for required or missing facts. Prefer museum collection records, artist foundations or estates, catalogue raisonnés, archives, universities, and reputable scholarly publications. Cross-check disputed or consequential claims with more than one reliable source.
5. Rewrite the article using the long-form structure and voice below. Build a narrative argument while retaining enough chronology, artwork analysis, relationships, reception history, and reference material to make the article useful for serious readers.
6. Review every H2 and H3 section individually before saving. Merge adjacent prose paragraphs that continue the same subject, artwork, scene, period, or line of reasoning; each narrative section should normally read as one cohesive paragraph unless it contains a genuine internal shift that requires separation.
7. Save the completed article beside the source as `<source_stem>_blog.md`. Never overwrite the supplied source.
8. Reopen the output and verify its facts, links, structure, language, filename, Markdown rendering, and section-by-section paragraph cohesion.

## Voice and Writing Style

Model the prose on the supplied reference article `Jan van Goyen_claude.md`. The goal is not to imitate wording sentence-by-sentence, but to reproduce its **editorial behavior**: high factual density, strong narrative tension, concrete visual description, explicit causal logic, careful qualification, and readable long-form art history.

### Core voice

- Write like a knowledgeable art historian speaking to an intelligent general reader, not like an encyclopedia entry and not like lyrical museum copy.
- Favor **specific nouns, dates, quantities, places, people, institutions, techniques, prices, dimensions, and documented relationships** over broad adjectives.
- Build paragraphs around a claim or tension, then support it with evidence. Use formulations such as “真正的轉折發生在……”, “值得注意的是……”, “有趣的是……”, “換句話說……”, and “必須強調的是……” when natural, but do not mechanically repeat them.
- Use contrast aggressively when it clarifies the story: success vs. debt, realism vs. invention, speed vs. skill, reputation in life vs. reputation after death, early style vs. mature style.
- Explain **why a fact matters**. Do not merely state that an event happened; connect it to artistic practice, market strategy, reputation, technique, or later reception.
- Prefer direct, declarative Traditional Chinese. Keep specialist terminology, but immediately explain it in plain language or with a visible example.
- Use natural Taiwan Traditional Chinese punctuation and vocabulary. Keep artist names, artwork titles, institutions, and specialist terms in the original language in parentheses when useful.

### Sentence and paragraph behavior

- Prefer cohesive medium-to-long paragraphs over frequent paragraph breaks. Treat one central claim, scene, artwork, time period, or causal chain as one paragraph, and combine consecutive sentences that develop the same idea instead of placing each sentence in its own paragraph.
- Start a new paragraph only when the argument, scene, period, artwork, or analytical focus genuinely changes. Within a subsection, keep closely related setup, evidence, visual analysis, and conclusion together in a single paragraph whenever readability permits.
- Apply this rule chapter by chapter, not only to the opening: inspect the prose under every H2 and H3 heading and consolidate unnecessary breaks. Default to one continuous prose paragraph per narrative section when its content follows one coherent focus; use multiple paragraphs only when the section contains clearly distinct subarguments, scenes, periods, or artworks.
- Mix short emphatic sentences with longer evidence-rich sentences, but normally keep a short sentence attached to the paragraph it concludes or introduces. Avoid standalone one- or two-sentence paragraphs unless an exceptional turning point needs deliberate emphasis.
- Avoid empty literary flourishes. Visual language must correspond to something observable in the artwork: horizon height, cloud mass, hue, brushwork, scale, figures, reflections, architecture, spatial depth, or surface.
- Use rhetorical questions sparingly, mainly in the opening or conclusion. The body should answer questions with evidence rather than continually asking them.
- Bold selectively for pivotal dates, concepts, names, or conclusions; never bold whole paragraphs.

### Evidence-aware phrasing

- Clearly separate documented fact, scholarly interpretation, and inference.
- When scholarship disagrees, present the older/common interpretation and the newer or competing interpretation, identify the evidence behind the disagreement, and state what can safely be concluded.
- Prefer calibrated phrases such as “根據……記載”, “學者……認為”, “推測”, “很可能”, “現有可靠史料所能支持的說法”, “目前並無明確一手史料佐證”, and “不宜過度推測”.
- Never manufacture motives, emotions, conversations, quotations, or causal links.

### Narrative engine

Before drafting, identify one **central contradiction or question** that can carry the whole article. Examples: a commercially successful painter who died in debt; an artist famous in life but forgotten after death; a painter whose apparently realistic scenes were carefully rearranged inventions. Return to this tension throughout the article so the biography reads as an argument, not a chronology dump.

## Article Structure

Use a **layered long-form structure** like the reference article rather than restricting the biography to only three turning points or two or three artworks. The exact number of sections may vary with the source material.

### 0. Title and thesis line

- Use a memorable title in the pattern `Artist: a concrete paradox, achievement, or visual idea`.
- Immediately below it, add one bold thesis/question sentence that frames the central contradiction and gives the reader a reason to continue.

### 1. Opening scene

Begin with a concrete visual scene, surprising fact, paradox, or representative work. Make the reader see something before giving the conventional biography. Develop the opening as one cohesive paragraph when its scene and argument are continuous; split it only when there is a genuine shift in scene or analytical focus. Do not impose a 200-character ceiling. End the opening by stating the article's central idea in plain language.

### 2. Origins and formation

Explain birthplace, family background, social setting, training, teachers, travel, and early influences only when they help explain the artist's later choices. Use dates and names precisely. Highlight unusual training, networks, or circumstances.

### 3. Decisive stylistic or career turns

Give each major turning point its own descriptive section. For each one:

1. Establish what the artist was doing before the change.
2. State what changed and approximately when.
3. Describe the visual or technical difference concretely.
4. Explain the market, institutional, personal, intellectual, or artistic context supported by evidence.
5. Explain why this change matters to the artist's larger story.

Do not artificially limit the article to three turning points if the source supports more.

### 4. Life phases and professional network

When useful, organize important periods by city, decade, patronage system, workshop, family network, or market environment. Include teachers, students, collaborators, rivals, relatives, dealers, patrons, and institutions when their relationship changes how we understand the artist.

### 5. Important works: deep analysis

Include a substantial `重要作品深度解析` section when the source supports it. Number the works. For each selected work, combine:

- title, date, and collection in the heading when known;
- what is visibly present;
- technique/composition/color/light/space;
- where the work sits in the artist's development;
- **why it is important** to the story;
- relevant conservation, provenance, market, or scholarly evidence when genuinely useful.

Do not force every work into an identical three-question template. Some works may be important because they document a stylistic shift, commission, technical experiment, provenance story, or later reception.

### 6. Style: how to recognize the artist

When appropriate, add a concise section explaining how a museum visitor might recognize the artist's work. Use concrete recurring visual features, not generic praise. Include caveats where a popular visual explanation is misleading or disputed.

### 7. Relationships, influence, and reception

Distinguish direct documented influence from broader stylistic inheritance. Name specific artists or schools only when evidence supports the connection. Explain reputation during the artist's lifetime, posthumous decline or rise, rediscovery, and modern scholarship when relevant.

### 8. Late life and death

Treat late life factually. Financial trouble, illness, family events, commissions, or reduced output may be included when documented, but do not turn limited evidence into melodrama.

### 9. Why the artist still matters

Return to the opening contradiction. Give a concrete answer based on what the artist changed in visual language, artistic practice, the market, or later viewing habits. End with a resonant statement or one genuine question, not generic praise.

### 10. Reference sections

When the source is rich enough, append useful reference material after the narrative:

- `## 重要作品一覽` as a Markdown table;
- `## 藝術家人生時間線` as concise dated bullets;
- `## 對當代與後世藝術的影響摘要` when evidence supports it;
- `# Sources & Further Reading`, grouped into museum/institutional sources, academic sources, books/catalogues, and other reputable sources as appropriate.

These reference sections supplement the narrative; they do not replace it.

## Markdown and Images

- Use descriptive H2 and H3 headings that tell a story even when skimmed on a phone.
- Paragraph consolidation applies to narrative prose only. Preserve the Markdown separation required for headings, images and captions, blockquotes, artwork information cards, tables, timelines, lists, and source entries; do not flatten these structural elements into a prose paragraph.
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
- The title and opening establish a memorable central contradiction, scene, or question rather than beginning as a birth record.
- Major turning points connect chronology to concrete changes in style, technique, market position, or reputation.
- Important works are analyzed with specific visual evidence and an explicit explanation of why each matters.
- Scholarly disagreements and uncertain claims are clearly qualified rather than flattened into a single confident story.
- When source depth permits, the article includes a works table, timeline, influence summary, and grouped further-reading section.
- Claims, quotations, work data, images, and links are verified and not invented.
- Every H2 and H3 section has been reviewed individually; adjacent prose developing the same idea has been merged, and any remaining paragraph break marks a genuine change in argument, scene, period, artwork, or analytical focus.
- H2/H3 headings, cohesive paragraphs, selective bolding, artwork cards, and sources render cleanly, and structural Markdown elements retain their necessary separation.
- The ending echoes the opening and leaves the reader with one genuine question.
