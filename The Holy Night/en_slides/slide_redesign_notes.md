# English YouTube slide redesign

Updated slides 0002–0021 in `update/` as 1920 × 1080 PNGs, using `Correggio_s_Holy_Night_background.png`. Images were composited from original files without AI repainting. English wording was shortened where needed to improve readability while retaining the original slide topics.

- Removed large chapter numerals on slides 4, 7, 10, 13 and 17.
- Slide 8 uses a five-step arrow sequence; slide 19 uses the 1522 → 1640 → 1746 timeline.
- Slide 20 reads exactly “Commission Fee: 208 liras regias” and includes both requested Mengs images and captions.
- Slides 9 and 16 identify the framed painting as the Boulanger copy, consistent with the existing source inventory and narration.
- All 20 files opened successfully; text was measured against layout boxes and all pages were visually reviewed.

## Resolved image locations

The following requested filenames were found in `Hans Memling/images/` and copied unchanged into `The Holy Night/images/`:

- `(e p3) Giorgio Vasari.jpg`
- `Parma Dome.jpg`
- `Diana as Personification of the Night.jpg`

The requested `聖波羅斯貝聖殿 Reggio Emilia San Prospero at night.png` was absent. Slide 2 uses a downloaded replacement photograph, saved as `San Prospero at night - replacement.jpg`.

## Night photograph credit

Basilica di San Prospero – Reggio Emilia, Italy – January 8, 2022. Photograph by **Giorgio Galeotti**, licensed **CC BY 4.0**. Resized and placed in the slide layout; the photo itself was not recolored.

- [Original file and attribution](https://commons.wikimedia.org/wiki/File:Basilica_di_San_Prospero_-_Reggio_Emilia,_Italy_-_January_8,_2022.jpg)
- [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)

Suggested video-description credit: “San Prospero night photograph: Giorgio Galeotti, Wikimedia Commons, CC BY 4.0; resized for this presentation.” Include the source and license links above when publishing.

Other existing image credits remain in `../images/SOURCES_AND_RIGHTS.md`. The Parma Cathedral dome photograph (`IMG-006_Parma_Dome.jpg`) is credited there to Livioandronico2013 under CC BY-SA 4.0.

## Reproduction

Run `python3 "The Holy Night/en_slides/compose_youtube_slides.py"` from the repository root. `slide_redesign_manifest.json` records the text and image inputs for each updated slide.
