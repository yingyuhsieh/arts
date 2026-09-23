---
name: create-youtube-artwork-contents
description: Create matched English and Traditional Chinese source-grounded narrative YouTube content files centered on one artwork, using supplied files plus targeted research to explain the artist, object, technique, meanings, reception, influence, modern relevance, and collection history. Use when the user wants segmented artwork analysis for AI or NotebookLM video generation rather than slides, a finished narration script, or a broad multi-work artist survey.
---

# Create YouTube Artwork Contents

Turn the user's artwork and reference files into matched English and Traditional Chinese, fact-checked segmented Markdown documents that can guide AI or NotebookLM in producing a video. Build the video around the experience of looking closely at one artwork; do not merely list facts or retell the artist's life chronologically.

## Inputs and research

- Read every supplied file relevant to the artwork before planning. Inspect images closely for visible details, but do not identify symbols, materials, condition, or technique from appearance alone when authoritative evidence is needed.
- Infer the principal artwork from the supplied material when it is unambiguous. If multiple works could be the subject and the choice would materially change the deliverable, ask the user which work to use.
- Treat supplied files as the primary corpus. Search the web when details are missing and verify material claims against authoritative current sources.
- Prefer museum collection records, catalogues raisonnés, conservation or technical studies, exhibition catalogues, peer-reviewed scholarship, artist foundations or estates, archives, and reputable academic publications. Use auction-house records only when they uniquely document provenance, market context, or technical evidence.
- Distinguish documented fact, scholarly interpretation, contested interpretation, and visual observation. Do not present a plausible reading as settled fact.
- Cite sources near the claims they support with descriptive Markdown links. Record unresolved disagreements explicitly. Never invent quotations, motives, provenance, reception, influence, or collection details.
- Keep sale prices peripheral unless a comparison reveals something important about reception, provenance, taste, or the work's cultural status.

## Narrative approach

Begin with the artwork, not the artist's birth date. Identify a visual detail, tension, contradiction, mystery, or question that gives viewers a reason to keep looking. Develop one core narrative that connects the work's appearance, making, historical circumstances, reception, and present-day meaning.

Organize the document into approximately 7–10 segments. The order should serve the story rather than mirror the required-topic list. Biography belongs only where it helps explain the artwork. Return to the opening question in the final segment and leave viewers with a concrete way to look at the work again.

Across the complete sequence, cover all of the following:

1. A concise artist biography focused on experiences relevant to the work.
2. Basic artwork data: accepted title, artist or attribution, date or range, medium, support, dimensions, and current collection.
3. The work's creation motive or circumstances, including commission, patron, intended setting or audience, historical context, and artistic problem when evidence supports them. Label hypotheses and unknowns.
4. Materials and working methods, explaining how technique shapes what viewers see. Incorporate conservation or technical evidence when available.
5. Close-looking guidance: composition, scale, color, light, space, gesture, gaze, surface, symbols, unusual devices, culturally specific meanings, ambiguities, and revealing details. Explain what is distinctive rather than assigning symbolism mechanically.
6. Art-historical importance and contemporary reception at the time of creation or first display. If reception evidence is scarce, say so instead of projecting modern fame backward.
7. Influence on later and contemporary art, supported by traceable examples or scholarship rather than resemblance alone.
8. Meaning for modern viewers and productive viewing angles, including how current perspectives may differ from the original audience's.
9. Collection information: present owner or museum, acquisition and provenance when documented, gallery location when current and useful, display status if verifiable, and rights or access links when relevant.

## Segment format

Give every segment a descriptive title and use this structure:

```markdown
## Segment X — [Narrative title]

**Narrative Purpose**
[How this segment advances the story and connects to the preceding segment.]

**Viewer Question**
[The question that guides attention.]

**Content**
[Detailed narrative-ready prose or direction for AI/NotebookLM.]

**What to Show**
- [Whole artwork, precise detail, comparison work, map, archival item, technical image, or contextual visual.]

**Key Facts and Interpretations**
- Fact: ... [source]
- Visual observation: ...
- Interpretation: ... [source or attribution]
- Disputed / unknown: ...

**Transition**
[A natural bridge or question leading to the next segment.]
```

Adapt the labels when doing so makes the result more natural, but preserve the distinction between evidence, observation, and interpretation. Each segment should offer an on-screen visual idea; avoid generic stock imagery when artwork details or historical sources can carry the explanation.

## Required output

Create both UTF-8 Markdown files beside the primary source file or in the common directory containing the supplied references:

- `<artwork>_en.md` — idiomatic English written for English-language art education.
- `<artwork>_tw.md` — natural Traditional Chinese with Taiwan wording.

Derive `<artwork>` from a concise, recognizable English artwork title. Use the same filename stem for both files, replace spaces with underscores, remove unsafe filename punctuation, and do not append extra suffixes. If the surrounding project already has an established artwork filename stem, preserve it.

The two files must use the same research scope, section order, segment count, factual claims, uncertainties, source URLs, and visual references. Adapt the prose, hooks, transitions, and titles naturally for each audience rather than translating line by line. Preserve original-language artwork titles where helpful and provide a translated title on first mention when it aids comprehension.

Use this document order in both files:

1. `A. Video Core Narrative` — the hook, central question, and two-to-four-sentence story promise.
2. `B. Recommended Video Titles` — three accurate, inviting, non-clickbait choices.
3. `C. Artwork Fact Card` — a compact sourced table of essential object data; show uncertainty explicitly.
4. `D. Video Structure` — segment titles and the role of each segment.
5. `E. Detailed Segment Plan` — all segments in the format above.
6. `F. Collection and Viewing Information` — provenance, acquisition, current collection, access or display information, and authoritative object-page link as available.
7. `G. Source and Fact-Checking Notes` — authoritative bibliography or links, source conflicts, uncertain claims, and research gaps.
8. `H. Coverage Check` — map each required topic to the segment or section that covers it.

Do not produce slides, subtitle timing, a finished word-for-word voice-over, downloaded images, or a video unless the user separately requests them.

## Final verification

Before delivery, confirm that:

- both `<artwork>_en.md` and `<artwork>_tw.md` exist at the intended location and use UTF-8;
- both files share the same filename stem, research structure, segment order, facts, uncertainties, sources, and visual references;
- the English reads idiomatically and the Chinese uses natural Traditional Chinese with Taiwan wording rather than literal translation;
- the narrative is centered on the artwork rather than dominated by biography;
- all required topics appear in the coverage check and are substantively addressed;
- dates, attribution, medium, dimensions, present collection, commission, provenance, reception, and technical claims are cited or clearly marked uncertain;
- visual observations agree with the supplied artwork image, while interpretations are attributed appropriately;
- original reception is not confused with later reputation;
- claims of influence name a documented pathway or example;
- collection and display information is current as of the research date;
- prices appear only when they advance the story; and
- Markdown headings, tables, lists, links, and spacing render cleanly, and `git diff --check` reports no whitespace errors.
