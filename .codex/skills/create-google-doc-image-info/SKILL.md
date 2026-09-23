---
name: create-google-doc-image-info
description: Create a native Google Doc image-reference sheet from supplied files, image URLs, or image paths, download local copies of the referenced images, and include one named image block per image with visible public-use warnings when needed. Use when preparing an artist or artwork image catalog for NotebookLM or later video production; do not use for general prose documents or image research without a requested Google Doc.
---

# Create Google Doc Image Info

Create one basic native Google Doc containing every image referenced by the user's input, in source order, and save a local copy of every collected image. The document and local images are visual references for NotebookLM or later video production, so completeness and actual image insertion matter more than decorative layout.

## Required Google Docs Route

Use the `google-drive:google-docs` skill and connected Google Drive/Docs tools. This is a net-new basic native document: follow that skill's blank/basic native-creation route and read its image-insertion guidance before writing. Use only connector-supported image insertion and readback; do not use browser UI, clipboard automation, or a text placeholder as a substitute for an image.

## Collect the Images

1. Inspect every supplied source file and resolve relative image paths from the directory containing that source file.
2. Collect images referenced through Markdown image syntax, HTML image elements, explicit image URLs, local image filenames or paths, and images embedded in a supplied document when the available reader can extract them.
3. Preserve first-mention order. Create one block per distinct image source, unless the source clearly presents repeated uses as separate entries.
4. Use the source's explicit caption, label, or image name. Otherwise use meaningful alt text, then the filename stem. Do not invent an artwork title from visual appearance alone.
5. Do not silently omit an inaccessible, missing, unsupported, or non-image source. Resolve it safely when possible; otherwise stop before claiming completion and report the affected image.

## Download Local Copies

Save every collected image in a local `images/` folder associated with the artist or artwork project. Reuse an existing local image folder for that project when one is clearly established; otherwise create `images/` beside the primary supplied source file, or in the relevant artist or artwork directory when the input is only a URL.

- Download remote images at their best available original resolution. A linked asset page is not itself an image; resolve its actual downloadable image URL when needed.
- Copy locally supplied images into the destination folder only when they are not already there. Do not move, rename, or overwrite the user's source files.
- Preserve a meaningful original filename when possible. Sanitize only characters that are unsafe for the local filesystem, and add a stable numeric suffix when different sources would collide.
- Verify that each saved file is non-empty and opens as an image. Keep the local inventory in the same order as the document blocks.
- Downloading an image does not change its rights status. Apply the same rights evidence and warnings to the Google Doc.

## Name the Document

Name the Google Doc exactly for the artist or artwork, without a file extension or generic suffix. Prefer, in order: an explicit user-provided name, the source's clear title or primary heading, then the relevant artist/artwork directory or filename. Ask only when these sources identify multiple unrelated subjects and no single accurate title can be inferred.

## Rights Status

Use only explicit rights or license evidence in the supplied source, image metadata, or linked asset page. Online availability alone does not mean an image is reusable.

- If the image is explicitly restricted, private, copyrighted without reuse permission, or otherwise not cleared, append ` — ⚠ Not cleared for public use` to its displayed image name.
- If the status cannot be established, append ` — Public-use status unverified` rather than asserting that it is public or restricted.
- If explicit evidence establishes public-domain or appropriately licensed reuse, show only the image name unless the user requests license details.
- Do not change sharing permissions or publish a private image merely to obtain an insertable URL.

## Document Format

For each image, create exactly this block, with the name before the image:

```text
<image name>[ — rights warning when applicable]
<inserted image>
```

Use a readable heading or standalone paragraph for the image name and a separate paragraph for the inline image. Do not add descriptions, source lists, tables, or other prose unless the user asks. Keep images at a readable size without intentional cropping when the connector supports size control.

## Completion Checks

Before handoff, verify through connector readback that:

1. the file is a native Google Doc with the correct artist/artwork title
2. the number and order of blocks match the collected image inventory
3. every block contains the intended image name followed by a connector-visible image object
4. every explicitly non-public image has the required warning and every unknown status is labeled unverified
5. no placeholders, broken image references, duplicated accidental blocks, or unrelated content remain

Also verify locally that the image folder exists, contains one valid file for every collected image, and has no filename collisions or partial downloads created by the task.

Return the Google Doc link and the local image-folder path. Briefly disclose any aspect of rendered image sizing or placement that could not be visually verified.
