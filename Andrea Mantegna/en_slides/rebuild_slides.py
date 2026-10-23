"""Compose the English YouTube slides at 4K, preserving supplied artwork."""

from functools import lru_cache
from pathlib import Path
import json
import re
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ART = ROOT.parent / "images"
OUT = ROOT / "update"
STEM = "Mantegna__The_Vantage_Point"
SIZE = (3840, 2160)
BACKGROUND = ROOT / "design_assets/renaissance_sky.png"
BG = Image.open(BACKGROUND).convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)
INK, RUST, GOLD, MUTED = "#29241F", "#48271E", "#AE8043", "#62584A"
IVORY = "#FCF8F0"
LAMENT = "1480 哀悼死去的基督 Lamentation over the Dead Christ.jpg"
OCULUS = "1465-1474 新婚夫婦之室天頂 Oculus of the Camera degli Sposi.jpg"
PARNA = "帕納索斯山 Parnassus.jpg"
records = []


@lru_cache(maxsize=128)
def font(size, style="body"):
    names = {"title": "Georgia Bold.ttf", "body": "Arial.ttf", "bold": "Arial Bold.ttf", "serif": "Georgia.ttf"}
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/" + names[style], round(size * 2))


class Slide:
    def __init__(self, number, section):
        self.number = number
        self.im = BG.copy()
        self.d = ImageDraw.Draw(self.im)
        self.images, self.texts = [], []

    def line(self, coords, width=2):
        # The generated background supplies the decoration.
        pass

    def text(self, value, box, size=42, style="body", color=INK, align="left", gap=0.25):
        x, y, w, h = box
        f = font(size, style)
        lines = []
        for paragraph in value.split("\n"):
            line = ""
            for word in paragraph.split():
                candidate = (line + " " + word).strip()
                if self.d.textlength(candidate, font=f) > w * 2 and line:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        advance = round(size * (1 + gap) * 2)
        assert (len(lines) - 1) * advance + size * 2 <= h * 2 + 2, (self.number, value, size, h, len(lines))
        assert x >= 0 and y >= 0 and x + w <= 1920 and y + h <= 1080
        for i, line in enumerate(lines):
            width = self.d.textlength(line, font=f)
            assert width <= w * 2 + 2, (self.number, line)
            tx = x * 2 + ((w * 2 - width) / 2 if align == "center" else (w * 2 - width if align == "right" else 0))
            self.d.text((round(tx), round(y * 2 + i * advance)), line, fill=color, font=f, anchor="lt")
        self.texts.append({"text": value, "box": box, "font_size_at_4k": size * 2})

    def title(self, value, size=62):
        self.text(value, (245, 116, 1430, 85), size, "title", RUST, "center")

    def image(self, name, box, crop=None, framed=True):
        path = (ART / name).resolve()
        source = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
        original_size = source.size
        if crop:
            source = source.crop(crop)
        x, y, w, h = box
        placed = ImageOps.contain(source, (round(w * 2), round(h * 2)), Image.Resampling.LANCZOS)
        px, py = round(x * 2 + (w * 2 - placed.width) / 2), round(y * 2 + (h * 2 - placed.height) / 2)
        if framed:
            frame = Image.open(ROOT / "design_assets/gilded_frame.png").convert("RGBA")
            # Nine-slice the generated frame to preserve ornament proportions.
            edge = 150
            border = 48
            target_w, target_h = placed.width + border * 2, placed.height + border * 2
            sx = [0, edge, frame.width - edge, frame.width]
            sy = [0, edge, frame.height - edge, frame.height]
            dx = [0, border + 12, target_w - border - 12, target_w]
            dy = [0, border + 12, target_h - border - 12, target_h]
            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:
                        continue
                    tile = frame.crop((sx[col], sy[row], sx[col + 1], sy[row + 1]))
                    tile = tile.resize((dx[col + 1] - dx[col], dy[row + 1] - dy[row]), Image.Resampling.LANCZOS)
                    self.im.paste(tile, (px - border + dx[col], py - border + dy[row]), tile)
        self.im.paste(placed, (px, py), placed)
        self.images.append({"source": os.path.relpath(path, ROOT.parent), "source_size": original_size, "source_crop": crop, "placed_box_4k": [px, py, placed.width, placed.height], "fit": "contain", "kind": "original slide illustration" if "design_backup" in str(path) else "supplied artwork or photograph"})

    def bullets(self, values, x, y, w, size=40, spacing=130):
        for i, value in enumerate(values):
            yy = y + i * spacing
            self.text("•", (x, yy, 20, spacing - 15), size, color=GOLD)
            self.text(value, (x + 27, yy, w - 27, spacing - 15), size)

    def save(self):
        path = OUT / f"{STEM}_slide_{self.number:04d}.png"
        if len(sys.argv) == 1 or str(self.number) in sys.argv[1:]:
            self.im.save(path, optimize=True)
        records.append({"slide": self.number, "file": str(path.relative_to(ROOT)), "size": SIZE, "text": self.texts, "images": self.images})
        print(f"Saved {self.number:04d}", flush=True)


def build_garden_comparison():
    s = Slide(6, "The Agony in the Garden")
    s.title("The Agony in the Garden", 64)
    s.image("1455-1456 客西馬尼園祈禱 Agony in the Garden.jpg", (225, 265, 650, 500))
    s.image("客西馬尼園祈禱 The Agony in the Garden (約 1459).jpg", (905, 265, 800, 500))
    s.text("By Andrea Mantegna", (225, 830, 650, 65), 37, "serif", RUST, "center")
    s.text("By Giovanni Bellini", (905, 830, 800, 65), 37, "serif", RUST, "center")
    s.text("Sharp, sculptural precision", (225, 900, 650, 55), 34, align="center")
    s.text("Soft, atmospheric warmth", (905, 900, 800, 55), 34, align="center")
    s.save()


def build():
    s = Slide(2, "The viewer's position")
    s.image(LAMENT, (250, 215, 780, 700))
    s.text("Why stand\nat the feet\nof a corpse?", (1120, 340, 560, 350), 66, "title", RUST)
    s.save()

    s = Slide(3, "The Lamentation")
    s.image(LAMENT, (245, 215, 895, 745))
    s.text("The Lamentation\nover the\nDead Christ", (1190, 310, 480, 300), 55, "title", RUST)
    s.line((1190, 670, 1665, 670))
    s.text("c. 1483", (1190, 735, 480, 80), 45, "serif")
    s.save()

    s = Slide(4, "Padua's Renaissance")
    s.title("Painting Like Sculpture", 65)
    s.text("Padua's Renaissance", (245, 240, 1430, 75), 47, "serif", INK, "center")
    s.image("Padua 義大利 帕多瓦.JPG", (245, 345, 1430, 560))
    s.text("Padua, Italy", (245, 935, 1430, 50), 37, "title", RUST, "center")
    s.save()

    s = Slide(5, "Painting like a sculptor")
    s.title("Painting Like a Sculptor", 64)
    s.image(f"../en_slides/design_backup_before_transfiguration/update/{STEM}_slide_0005.png", (245, 225, 1430, 558), crop=(490, 450, 3350, 1566))
    s.text("Surrounded by plaster casts and antiquities,\nhe painted like a sculptor.", (245, 845, 1430, 135), 47, "body", INK, "center")
    s.save()

    build_garden_comparison()

    s = Slide(7, "Two artists, one family")
    s.title("Two Artists, One Family", 65)
    s.image("Giovanni Bellini self-portrait.jpg", (250, 280, 340, 460))
    s.image("曼特尼亞 Andrea Mantegna.png", (650, 280, 340, 460))
    s.text("Giovanni Bellini", (225, 785, 390, 60), 33, "serif", RUST, "center")
    s.text("Andrea Mantegna", (625, 785, 390, 60), 33, "serif", RUST, "center")
    s.text("Mantegna married\nNicolosia Bellini.", (1060, 285, 610, 125), 43, "bold")
    s.bullets(["Shared compositions\nand ideas", "Mantegna: sharp,\nsculptural precision", "Bellini: soft,\natmospheric warmth"], 1060, 480, 610, 40, 155)
    s.save()

    s = Slide(8, "Architectural illusions")
    s.text("Breaking\nthe Ceiling", (250, 295, 580, 235), 70, "title", RUST)
    s.line((250, 585, 810, 585))
    s.text("Architectural\nIllusions", (250, 670, 580, 175), 49)
    s.image(OCULUS, (900, 235, 770, 705))
    s.save()

    s = Slide(9, "San Zeno Altarpiece")
    s.image("聖則諾祭壇畫 San Zeno Altarpiece.jpg", (245, 210, 780, 750))
    s.text("San Zeno\nAltarpiece", (1100, 300, 570, 225), 63, "title", RUST)
    s.line((1100, 580, 1665, 580))
    s.text("Extending physical\nspace into\nthe frame.", (1100, 660, 570, 240), 48)
    s.save()

    s = Slide(10, "The Gonzaga court")
    s.title("A Court Painter's Compensation", 58)
    s.text("180 ducats\na year", (260, 280, 830, 230), 77, "title", RUST)
    s.line((260, 565, 1080, 565))
    s.text("Lodging, firewood,\nand enough grain\nfor a family of six.", (260, 640, 830, 265), 50)
    s.image("House of Gonzaga.png", (1240, 300, 370, 430), framed=False)
    s.text("House of Gonzaga", (1140, 795, 555, 115), 41, "serif", RUST, "center")
    s.save()

    s = Slide(11, "Camera Picta")
    s.image(OCULUS, (245, 230, 895, 720))
    s.text("Camera\nPicta", (1190, 245, 480, 215), 68, "title", RUST)
    s.text("An open-air theater\ninside the palace.", (1190, 525, 480, 180), 43)
    s.line((1190, 755, 1660, 755))
    s.text("Peering servants\nThe peacock\nThe open sky", (1190, 800, 480, 160), 35, "serif", RUST)
    s.save()

    s = Slide(12, "The painted illusion")
    s.image("Camera picta_overview.png", (275, 220, 650, 740))
    s.text("The Illusion\nof Open Sky", (1040, 280, 625, 235), 63, "title", RUST)
    s.line((1040, 570, 1660, 570))
    s.text("Painted architecture\ntransforms the ceiling\ninto an opening\nto the sky.", (1040, 650, 625, 295), 44)
    s.save()

    s = Slide(13, "The Gonzaga years")
    s.text("Myths of\nthe Court", (250, 295, 490, 235), 67, "title", RUST)
    s.line((250, 585, 730, 585))
    s.text("The Gonzaga\nYears", (250, 665, 490, 175), 47)
    s.image("House of Gonzaga 扎加家族.jpg", (805, 265, 875, 630))
    s.text("Family of Gonzaga by Andrea Mantegna", (790, 940, 895, 45), 29, "serif", RUST, "center")
    s.save()

    s = Slide(14, "Duties of a court painter")
    s.title("Duties of a Court Painter", 63)
    s.image("凱撒的凱旋 Triumphs of Caesar 1-9 3x3.png", (245, 230, 770, 710))
    s.bullets(["Painting portraits\nand palace frescoes", "Designing theatrical sets", "Appraising classical\nantiquities", "Crafting intricate allegories", "Exporting original prints"], 1090, 280, 580, 38, 137)
    s.save()

    s = Slide(15, "The Battle of the Sea Gods")
    s.image("海神之戰 The Battle of Sea Gods, 1480.jpg", (245, 245, 930, 650))
    s.text("Battle of\nthe Sea Gods", (1230, 285, 440, 230), 57, "title", RUST)
    s.line((1230, 575, 1665, 575))
    s.text("Reproducible\nprints exported\nhis genius.", (1230, 655, 440, 250), 45)
    s.save()

    s = Slide(16, "Madonna della Vittoria")
    s.text("Who gets to\ncall it a\nvictory?", (250, 235, 675, 285), 63, "title", RUST)
    s.text("Madonna della Vittoria", (250, 570, 675, 120), 40, "serif")
    s.text("A kneeling ruler still occupies\nthe political center\nof the image.", (250, 725, 675, 180), 39)
    s.image("1496 勝利聖母 Madonna della Vittoria.jpg", (1060, 215, 600, 675))
    s.text("1495–1496 · Tempera on canvas\nMusée du Louvre, Paris", (980, 935, 750, 55), 23, color=MUTED, align="center", gap=0.15)
    s.save()

    s = Slide(17, "Parnassus")
    s.image(PARNA, (245, 210, 950, 750))
    s.text("Parnassus", (1250, 315, 420, 110), 61, "title", RUST)
    s.line((1250, 500, 1665, 500))
    s.text("A blend of\nclassical myth\nand courtly\nallegory.", (1250, 585, 420, 330), 45)
    s.save()

    s = Slide(18, "Minerva Expelling the Vices")
    s.text("An argument\nbecomes a\nvisible conflict", (245, 235, 570, 280), 53, "title", RUST)
    s.text("Minerva Expelling\nthe Vices", (245, 560, 570, 125), 39, "serif")
    s.text("Minerva enters the garden\nas strange figures\nscatter before her.", (245, 735, 570, 165), 38)
    s.text("c. 1500–1502 · Tempera on canvas\nMusée du Louvre, Paris", (245, 900, 570, 55), 23, color=MUTED, gap=0.15)
    s.image("密涅瓦驅逐惡習 Minerva Expelling the Vices.jpg", (865, 250, 810, 690))
    s.save()

    s = Slide(19, "Weight of perspective")
    s.image("1448-1457 奧韋塔里禮拜堂壁畫 Ovetari Chapel Frescoes.jpg", (245, 210, 760, 710))
    s.text("Ovetari Chapel Frescoes", (245, 945, 760, 45), 33, "serif", RUST, "center")
    s.text("Weight of\nPerspective", (1080, 295, 590, 230), 64, "title", RUST)
    s.line((1080, 590, 1665, 590))
    s.text("Emotional\nManipulation", (1080, 680, 590, 180), 49)
    s.save()

    s = Slide(20, "Perspective and emotion")
    s.image(LAMENT, (245, 225, 850, 735))
    s.text("Perspective\nand Emotion", (1150, 235, 520, 210), 55, "title", RUST)
    s.text("Severe perspective as an\nintentional narrative device.", (1150, 510, 520, 155), 37, "bold")
    s.bullets(["Adjusted proportions\npreserve sacred dignity", "Wounds pushed\ninto the foreground", "Compressed space\nintensifies tension"], 1150, 700, 520, 32, 94)
    s.save()

    s = Slide(21, "Where does the artist place you?")
    works = [("哀悼死去的基督 Lamentation over the Dead Christ.jpg", "Lamentation over the Dead Christ"), ("新婚夫婦之室 Camera degli Sposi.jpg", "Camera degli Sposi"), (PARNA, "Parnassus"), ("Crucifixion.jpg", "Crucifixion")]
    for i, (name, label) in enumerate(works):
        x, y = 245 + (i % 2) * 440, 235 + (i // 2) * 385
        s.image(name, (x, y, 400, 290))
        s.text(label, (x - 8, y + 312, 416, 65), 25, "serif", RUST, "center", gap=0.15)
    s.text("Where does\nthe artist\nplace you", (1180, 270, 490, 330), 64, "title", INK)
    s.line((1180, 655, 1670, 655))
    s.text("to change\nthe story?", (1180, 735, 490, 210), 64, "title", RUST)
    s.save()

    s = Slide(22, "End")
    s.image("../../end_sticker.png", (690, 295, 540, 540), framed=False)
    s.save()

    data = {"method": "Deterministic Pillow composition using original local images", "background": str(BACKGROUND.relative_to(ROOT)), "size": SIZE, "completed_slides": list(range(2, 23)), "unchanged_slides": [1], "artwork_policy": "All supplied artworks and photographs are proportionally resized in full, with no cropping or generation. The original illustration is retained on slide 5, cropped above its old text. The opening question uses the supplied Lamentation artwork. Decorative sky and frame assets were created with the built-in imagegen tool using The Transfiguration as the visual reference.", "removed_chapter_numerals": {"4": "1", "8": "2", "13": "3", "19": "4"}, "slides": records}
    (ROOT / "design_revision_log.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    previews()


def previews():
    review = ROOT / "review"
    review.mkdir(exist_ok=True)
    for first, last in [(2, 8), (9, 15), (16, 22)]:
        height = 1305 if last - first == 6 else 870
        sheet = Image.new("RGB", (1920, height), "#28231F")
        d = ImageDraw.Draw(sheet)
        for i, n in enumerate(range(first, last + 1)):
            thumb = Image.open(OUT / f"{STEM}_slide_{n:04d}.png").resize((640, 360), Image.Resampling.LANCZOS)
            x, y = (i % 3) * 640, (i // 3) * 435
            sheet.paste(thumb, (x, y + 50))
            d.text((x + 15, y + 10), f"{n:04d}", font=font(14, "serif"), fill="white")
        sheet.save(review / f"slides_{first:04d}_{last:04d}.jpg", quality=92)


if __name__ == "__main__":
    build()
