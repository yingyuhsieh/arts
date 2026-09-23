---
name: verify-youtube-scripts
description: Review and revise Chinese or English YouTube narration scripts so AI text-to-speech reads them naturally, especially by removing brackets around artwork titles and rewriting parenthetical material that creates awkward pauses. Use for narration copy, voice-over scripts, or slide-by-slide scripts; do not use for factual research or subtitle timing unless separately requested.
---

# Verify YouTube Scripts

Revise the supplied scripts for smooth AI narration while preserving their meaning, factual claims, language, tone, section order, and file format. Treat this as a spoken-language editing task, not a factual review or a broad rewrite.

## Edit the scripts

Read each complete script before editing so sentence rhythm and references remain coherent. If the user supplies a directory, identify the narration-script files from context and ignore unrelated research notes, images, and generated media. Ask for a path only when no target can be determined safely.

Check every sentence by imagining it read aloud at a natural pace. Revise passages that contain:

- sentences that are too long, overloaded with clauses, or difficult to breathe through;
- stiff written phrasing, awkward inversions, repeated sentence openings, or unclear pronoun references;
- punctuation or symbols that cause unnatural pauses, clipped delivery, or incorrect emphasis;
- dense lists, slashes, repeated dashes, semicolons, colons, ellipses, citations, abbreviations, numerals, or mixed-language fragments that a TTS voice may misread;
- adjacent short fragments that sound choppy and should be joined, or long sentences that should be divided;
- wording that is grammatically valid on the page but unnatural when spoken.

Prefer clear, conversational sentences and ordinary spoken transitions. Use punctuation to guide breathing, but do not insert commas so frequently that the narration becomes halting. Spell out abbreviations, symbols, and ambiguous numerals only when doing so improves pronunciation in the script's language. Preserve intentional headings and slide or scene labels that are not meant to be narrated.

## Handle brackets and parentheses

Remove the opening and closing brackets around artwork titles. Preserve the title itself and integrate it naturally into the sentence. Apply this to Chinese and Western bracket styles, including `《》`, `〈〉`, `「」`, `『』`, `（）`, and `()` when they enclose an artwork title.

For other parenthetical or bracketed material that would make the AI pause unnaturally:

- keep meaningful information, but rewrite it as part of the sentence or as a separate sentence;
- remove only material that is clearly a drafting note, pronunciation cue, redundant aside, or non-narrated production instruction;
- do not delete dates, names, translations, qualifications, or factual context merely because they appear in brackets;
- retain brackets that are required by the file format or belong to non-narrated structure, such as Markdown links, subtitle timestamps, or explicit scene labels.

Do not mechanically strip every bracket character. The result must remain grammatical and preserve the intended information.

## Preserve source integrity

Do not invent facts, change uncertain claims into certainties, translate the script, or alter the author's argument. Keep artwork names, personal names, dates, and specialist terms accurate. When a sentence cannot be made speakable without resolving an ambiguous meaning, leave it unchanged and flag the ambiguity to the user.

Preserve UTF-8 encoding, existing Markdown headings, slide boundaries, subtitle numbering, and other structural markers. For subtitle files, revise only spoken text unless the user also asks for retiming; do not change timestamps by default.

## Deliver the result

When the user asks to check and modify supplied files, edit those files in place unless the user names a different destination. Review the edited text once more for natural read-aloud flow and confirm that disruptive title brackets and parenthetical pauses have been resolved.

Report which files were changed and summarize the main kinds of revisions. Mention any ambiguous passages left for the user, but do not produce a verbose line-by-line change log unless requested. Match the language of the user's request or source material, using Traditional Chinese for Traditional Chinese scripts.
