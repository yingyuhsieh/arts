---
name: youtube-and-social-media-post
description: Create publish-ready English and Traditional Chinese YouTube descriptions, detailed emoji-rich bilingual social posts, and a concise Taiwan Traditional Chinese Threads post from supplied media or source files. Use when Codex needs source-grounded YouTube and social campaign copy under ./00.social.
---

# YouTube and Social Media Post

Turn the user's source files into five paste-ready marketing assets: English and Taiwan Traditional Chinese versions of a YouTube description and a detailed, emoji-rich narrative social media post, plus a concise Taiwan Traditional Chinese Threads post. Ground every factual claim in the supplied materials and save all results under `./00.social` relative to the current working directory.

## Inputs

- Accept any number of explicitly supplied files or directories.
- When given a directory, inspect relevant files recursively. Exclude `00.social`, hidden tool directories, generated caches, and unrelated build output.
- Read text-bearing formats directly. Extract text from documents, PDFs, presentations, and subtitles with the appropriate available tools. Inspect images and transcribe audio or video only when they add useful source content.
- Treat the user's prompt as the editorial brief. Follow the requested audience, platform, tone, length, link, call to action, and required wording.
- Produce both English and Traditional Chinese unless the user explicitly requests only one language. Use natural Taiwan wording for Chinese. Write each language as native promotional copy rather than a literal line-by-line translation.
- Preserve official names, titles, and intentional quotations in their source language when appropriate. Keep facts and emphasis aligned across language versions.
- Ask a question only when a missing fact or unresolved contradiction would materially change the deliverables. Otherwise make a conservative editorial choice and continue.

## Workflow

### 1. Inventory and synthesize the sources

Identify the video's central subject, audience, value proposition, notable topics, named people or works, credits, URLs, dates, and calls to action.

Use this priority when sources disagree:

1. Explicit instructions in the current user prompt
2. Files marked final, approved, revised, or otherwise authoritative
3. Final transcript, subtitles, or narration actually used in the video
4. Scripts, presentations, research notes, and supporting material
5. Inference from visuals, audio, filenames, or metadata

Do not use filesystem modification time as proof that content is authoritative. Omit uncertain details that are not essential. Never invent quotes, timestamps, URLs, credits, affiliations, dates, or claims. Keep terminology and proper nouns consistent across all five deliverables.

### 2. Draft both YouTube descriptions

Write separate English and Traditional Chinese descriptions with this content order:

1. A compelling opening of one or two sentences stating what the viewer will discover
2. A concise summary of the video's focus and value
3. Optional scan-friendly details in natural prose or a short list only when they improve readability
4. A natural call to watch, subscribe, visit, or share based on the supplied brief
5. Relevant credits, references, or links only when present in the sources
6. Three to eight focused hashtags on the final line

Do not ask viewers to answer a question, share their answer, or leave their opinion in the comments. Do not use comment engagement as the YouTube call to action.

Do not introduce content with formulaic labels meaning "Video highlights include," "Key topics include," or "In this video, you will learn" in either English or Chinese. Weave topics into flowing prose, or move directly into an unlabeled short list when bullets materially improve scanability.

Do not add a suggested title, chapter timestamps, boilerplate disclaimers, or unsupported links unless requested. If the user requires a link but supplies none, use `[YouTube URL]` rather than fabricating one.

Adapt phrasing, rhythm, and cultural references naturally for each language while preserving the same factual scope and editorial emphasis.

### 3. Draft both detailed social media posts

Write separate English and Traditional Chinese standalone posts that complement rather than copy the YouTube descriptions. Make each post a lively, explanatory mini-essay rather than a short caption. Use the voice of an informed curator or teacher speaking directly to social followers: conversational, vivid, and accessible without losing factual precision.

Use this structure:

1. Open with a strong conversational hook. Refer to a previous episode, week, or ongoing series only when the prompt or sources explicitly establish that continuity.
2. Add a concise context paragraph identifying the subject, historical setting, and why the comparison or story matters.
3. Establish a memorable contrast or interpretive frame when the sources support one, such as two artists occupying opposite ends of a spectrum. Clearly present metaphors as editorial interpretation, not literal historical fact.
4. Develop three to five compact mini-sections. Start each with one or two relevant emoji plus a short, punchy label, then explain a concrete work, technique, idea, person, or historical consequence in a short paragraph.
5. Include specific sourced details such as artwork titles, dates, visual devices, political context, or historical turning points. Build a narrative arc instead of listing disconnected facts.
6. Close with a memorable image, takeaway, or invitation that connects the history to what a viewer might notice or experience.
7. Include one clear call to action and the supplied YouTube link. Use `[YouTube URL]` when a link is required but unavailable.
8. End with six to ten focused plain hashtags. Do not generate long Facebook hashtag tracking URLs unless the user explicitly requests linked hashtags.

Aim for substantial but feed-friendly copy: typically 250-450 English words and 500-900 Traditional Chinese characters, unless the user or platform requires another length. Optimize for the named platform and its current constraints when specified. Otherwise write a Facebook-friendly post that also reads naturally on LinkedIn or a standard feed.

Use six to twelve relevant emoji throughout each post, including the mini-section labels. Choose emoji that reinforce the surrounding idea, artwork, place, technique, or emotion. Do not add emoji to every sentence or use unrelated decoration.

Avoid empty hype, clickbait, repetitive section formulas, hashtag stuffing, and claims stronger than the sources support. Treat user-provided sample copy as a style reference unless its factual claims are also supported by the supplied sources.

### 4. Draft the Taiwan Traditional Chinese Threads post

Write one standalone Threads post in natural Taiwan Traditional Chinese. It must complement rather than copy the longer Chinese social post or YouTube description.

- Open with an immediate, conversational hook that makes sense without prior context.
- Focus on one memorable artwork, contrast, detail, or interpretive idea instead of compressing the entire video summary.
- Use short paragraphs and a mobile-friendly rhythm. Keep it concise enough to paste as a single Threads post; do not create a numbered thread unless the user explicitly requests one.
- Include two to five relevant emoji, used sparingly for emphasis.
- End with one natural invitation to watch and the supplied YouTube link. Use `[YouTube URL]` when a link is required but unavailable.
- Use zero to three focused hashtags. Avoid hashtag stuffing, engagement bait, and requests to reply with an opinion.
- Preserve the same sourced facts, names, dates, and artwork titles used in the other deliverables. Do not introduce claims solely to make the post punchier.

### 5. Check quality

Before saving, verify that:

- All five assets accurately reflect the supplied files and each other.
- English and Chinese versions are natural adaptations with matching facts, not awkward literal translations.
- Names, artwork titles, dates, spellings, and links match the strongest source.
- YouTube and social openings are distinct, and no asset repeats long passages from another.
- YouTube descriptions contain no request to answer or share an opinion in the comments.
- YouTube descriptions contain no formulaic English or Chinese topic label meaning "Video highlights include" or "Key topics include."
- Each social post contains a strong hook, a clear narrative arc, three to five emoji-led mini-sections, meaningful context, and specific explanatory detail.
- Each social post uses six to twelve relevant emoji and six to ten plain hashtags without generated tracking URLs.
- The Threads post is a distinct, concise, single-post-ready Traditional Chinese adaptation with a strong hook, short paragraphs, two to five relevant emoji, no more than three hashtags, and no unsupported claims.
- References to a previous episode, week, or series appear only when explicitly supported by the prompt or sources.
- Every asset is complete, natural, and ready to paste without editorial notes.
- No fact, quotation, timestamp, URL, or credit was invented.

## Outputs

Create `./00.social` when it does not exist. Derive a short filesystem-safe `<video-slug>` from the video title or central subject, using lowercase Latin letters, digits, and hyphens when practical.

Write exactly:

```text
./00.social/<video-slug>-youtube-description-en.md
./00.social/<video-slug>-youtube-description-zh-tw.md
./00.social/<video-slug>-social-media-post-en.md
./00.social/<video-slug>-social-media-post-zh-tw.md
./00.social/<video-slug>-threads-post-zh-tw.md
```

Each file must contain only the final publish-ready copy, with no analysis, source inventory, confidence notes, language labels, or surrounding code fence. Preserve unrelated files.

If any target already exists, do not overwrite it unless the user clearly requests a revision. Otherwise add the smallest available numeric suffix to all five filenames so the complete set stays aligned.

Report the five saved paths and briefly note every visible placeholder such as `[YouTube URL]`.
