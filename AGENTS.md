# Repository Guidelines

## Project Structure & Module Organization

This repository is an art-history media archive organized mainly by artist or story. Top-level directories such as `Edgar Degas/`, `Simone Martini/`, and `Agapanthus Triptych/` contain source artwork, research notes, scripts, subtitles, and finished graphics. Shared imagery belongs in `02.images/`; bilingual publishing copy belongs in `00.social/`. Some projects use a `YouTube/` folder for final platform assets or a working subfolder such as `YY/` for selected material. Keep new files with the relevant artist or story rather than creating generic catch-all directories.

## Development & Validation Commands

There is no application build or automated test suite. Validate contributions with lightweight checks:

```sh
git status --short
git diff --check
python3 "Paul Gauguin/list_images.py"
```

The first two commands review the change set and catch whitespace errors. The Python utility reports image dimensions and sizes for its current directory; it requires Pillow (`python3 -m pip install Pillow`) and can be copied or adapted when auditing another collection. Open changed images, Markdown, subtitles, and videos in an appropriate viewer before committing.

## Content Style & Naming Conventions

Preserve UTF-8 text and the language used by the surrounding project. Use descriptive image names in the established pattern, typically `Artist Work Title.jpg`; retain historical accents and Traditional Chinese where applicable. Do not rename existing assets solely to normalize spacing or capitalization, because scripts or published material may reference them. For Python, use four-space indentation, `snake_case` functions, and standard-library paths where practical. Keep Markdown concise, with meaningful headings and one blank line around headings and lists.

## Testing Guidelines

Verification is asset-focused. Confirm that new media opens without errors, filenames match references in scripts or subtitles, and image resolution is suitable for its destination. For social copy, verify all four expected bilingual deliverables when applicable: English and Traditional Chinese YouTube descriptions and social posts. Review `git diff --check` before every commit.

## Commit & Pull Request Guidelines

History is sparse and uses short checkpoint messages, so prefer clearer imperative commits such as `Add Simone Martini social copy` or `Correct Degas artwork captions`. Keep each commit scoped to one artist, story, or production task. Pull requests should summarize the content added or changed, identify source/credit considerations, list manual checks performed, and include previews for visual changes. Link the related issue or production request when one exists; avoid committing caches, temporary files, or generated logs.
