"""Rebuild the requested PNG slides from unaltered local artwork files."""

from pathlib import Path
from functools import lru_cache
import json
import re
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ART = ROOT.parent / "images"
OUT = ROOT / "update"
STEM = "安德烈亞·曼特尼亞：透視與空間大師"
SCALE = 2
SIZE = (3840, 2160)
BG = Image.open(ROOT / f"{STEM}_background.png").convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)
INK = "#30271F"
RUST = "#793D31"
GOLD = "#AE8043"
MUTED = "#62584A"
IVORY = "#FCF8F0"
SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"
HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
LATIN = "/System/Library/Fonts/Supplemental/Georgia.ttf"

LAMENT = "1480 哀悼死去的基督 Lamentation over the Dead Christ.jpg"
CEILING = "Camera picta.jpg"
PARNA = "帕納索斯山 Parnassus.jpg"
records = []


@lru_cache(maxsize=128)
def font(size, style="body"):
    path, index = (SONG, 2) if style == "title" else ((LATIN, 0) if style == "latin" else (HEITI, 0))
    return ImageFont.truetype(path, round(size * SCALE), index=index)


class Slide:
    def __init__(self, number, section):
        self.number = number
        self.im = BG.copy()
        self.draw = ImageDraw.Draw(self.im)
        self.images = []
        self.texts = []
        overlay = Image.new("RGBA", SIZE)
        d = ImageDraw.Draw(overlay)
        d.rounded_rectangle((380, 220, 3460, 2040), radius=32, fill=(252, 248, 240, 232))
        self.im = Image.alpha_composite(self.im.convert("RGBA"), overlay).convert("RGB")
        self.draw = ImageDraw.Draw(self.im)
        self.line((235, 186, 1685, 186), 1.5)
        self.line((235, 990, 1685, 990), 1)
        self.text("ANDREA MANTEGNA", (240, 1030, 600, 25), 17, style="latin", color=MUTED)
        self.text(f"{section}  /  {number:02d}", (1120, 1030, 560, 25), 17, color=MUTED, align="right")

    def line(self, coords, width=2, fill=GOLD):
        self.draw.line(tuple(round(v * SCALE) for v in coords), fill=fill, width=round(width * SCALE))

    def text(self, value, box, size=44, style="body", color=INK, align="left", gap=0.28):
        x, y, w, h = box
        f = font(size, style)
        lines = []
        for para in value.split("\n"):
            # Keep English words intact and wrap CJK at character boundaries.
            tokens = re.findall(r"[A-Za-z0-9]+(?:[’'.,–-][A-Za-z0-9]+)*|[^A-Za-z0-9]", para)
            line = ""
            for token in tokens:
                proposed = line + token
                if self.draw.textlength(proposed, font=f) > w * SCALE and line:
                    if token in "，。；：！？、）》」』":
                        last = line[-1]
                        lines.append(line[:-1].rstrip())
                        line = last + token
                    else:
                        lines.append(line.rstrip())
                        line = token.lstrip()
                else:
                    line = proposed
            lines.append(line.rstrip())
        line_height = round(size * (1 + gap) * SCALE)
        used_h = (len(lines) - 1) * line_height + size * SCALE
        assert used_h <= h * SCALE + 2, (self.number, value, size, used_h / SCALE, h)
        assert x >= 0 and y >= 0 and x + w <= 1920 and y + h <= 1080
        for i, line in enumerate(lines):
            length = self.draw.textlength(line, font=f)
            assert length <= w * SCALE + 2, (self.number, line)
            tx = x * SCALE
            if align == "center":
                tx += (w * SCALE - length) / 2
            elif align == "right":
                tx += w * SCALE - length
            ty = round(y * SCALE + i * line_height)
            # macOS TC fonts lack these two name separators. Draw their simple
            # centered-dot forms explicitly instead of allowing tofu squares.
            cursor = tx
            for part in re.split(r"([·・])", line):
                advance = self.draw.textlength(part, font=f)
                if part in ("·", "・"):
                    cx = cursor + advance / 2
                    cy = ty + size * SCALE * 0.48
                    radius = size * SCALE * 0.055
                    self.draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
                elif part:
                    self.draw.text((round(cursor), ty), part, fill=color, font=f, anchor="lt")
                cursor += advance
        self.texts.append({"text": value, "box": box, "font_size_at_4k": size * SCALE})

    def title(self, value, size=65):
        self.text(value, (245, 115, 1430, 83), size, "title", RUST)

    def art(self, name, box, framed=True):
        path = (ART / name).resolve()
        source = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        x, y, w, h = box
        # Contain the complete source image: no cropping, retouching or regeneration.
        target = ImageOps.contain(source, (round(w * SCALE), round(h * SCALE)), Image.Resampling.LANCZOS)
        px = round(x * SCALE + (w * SCALE - target.width) / 2)
        py = round(y * SCALE + (h * SCALE - target.height) / 2)
        if framed:
            self.draw.rectangle((px - 12, py - 12, px + target.width + 12, py + target.height + 12), fill="#E5D4B8")
            self.draw.rectangle((px - 8, py - 8, px + target.width + 8, py + target.height + 8), outline=GOLD, width=3)
        self.im.paste(target, (px, py))
        self.images.append({"source": str(path.relative_to(ROOT.parent)), "source_size": source.size, "placed_box_4k": [px, py, target.width, target.height], "fit": "contain; full image; no crop"})

    def bullets(self, values, x, y, w, size=39, spacing=125):
        for i, value in enumerate(values):
            yy = y + i * spacing
            self.draw.ellipse((x * SCALE, (yy + 14) * SCALE, (x + 9) * SCALE, (yy + 23) * SCALE), fill=GOLD)
            self.text(value, (x + 25, yy, w - 25, spacing - 15), size)

    def save(self):
        path = OUT / f"{STEM}_slide_{self.number:04d}.png"
        self.im.save(path, optimize=True)
        records.append({"slide": self.number, "status": "updated", "file": str(path.relative_to(ROOT)), "size": SIZE, "images": self.images, "text": self.texts})
        print(f"Saved {self.number:04d}", flush=True)


def build_intro():
    s = Slide(2, "觀看的位置")
    # Restore the original illustrated feet and question mark, rather than
    # substituting the Lamentation painting. Cover only its old text panel.
    s.art(f"../tw_slides/update copy/{STEM}_slide_0002.png", (245, 210, 1430, 760))
    s.draw.rounded_rectangle((930, 910, 2910, 1410), radius=30, fill=IVORY, outline=GOLD, width=3)
    s.text("想像一下，", (500, 478, 920, 100), 76, "title", RUST, "center")
    s.text("你正站在一具屍體的腳邊", (500, 595, 920, 95), 68, "title", INK, "center")
    s.save()


def build_portrait_comparison():
    s = Slide(8, "曼特尼亞與貝里尼")
    s.title("兩種觀看，兩種情感")
    s.art("Giovanni Bellini self-portrait.jpg", (390, 235, 410, 500))
    s.art("曼特尼亞 Andrea Mantegna.png", (1100, 235, 410, 500))
    s.text("喬凡尼・貝里尼", (285, 755, 620, 65), 46, "title", RUST, "center")
    s.text("安德烈亞·曼特尼亞", (985, 755, 650, 65), 46, "title", RUST, "center")
    s.text("嚴整的造型與強烈的悲痛，\n對照貝里尼的柔和光線。", (300, 865, 1320, 115), 43, align="center")
    s.save()


def build_art_influences():
    s = Slide(6, "古典藝術的啟發")
    s.title("古典藝術的啟發")
    s.art("多納太羅 Donatello Possible self-portrait, c. 1446-1449.jpg", (245, 290, 330, 495))
    s.text("多納太羅", (230, 820, 360, 60), 42, "title", RUST, "center")
    s.art("Donatello David at the Bargello in Florence.jpg", (630, 245, 390, 585))
    s.text("Donatello David\nat the Bargello\nin Florence", (610, 855, 430, 125), 29, "latin", INK, "center", 0.2)
    s.bullets(["斯夸爾喬內工坊的\n古物與石膏翻模", "多納太羅：\n雕像般的堅實造型", "古羅馬建築遺跡\n與銘文", "佛羅倫斯新風格的\n強烈戲劇性"], 1100, 280, 560, 40, 166)
    s.save()


def build_ovetari():
    s = Slide(7, "仰視透視實驗")
    s.art("1448-1457 奧韋塔里禮拜堂壁畫 Ovetari Chapel Frescoes.jpg", (250, 210, 730, 750))
    s.text("奧韋塔里\n禮拜堂壁畫", (1060, 300, 600, 215), 66, "title", RUST)
    s.line((1060, 565, 1655, 565))
    s.text("大膽的\n仰視透視實驗", (1060, 640, 600, 210), 57)
    s.save()


def build_garden_comparison():
    s = Slide(9, "客西馬尼園祈禱")
    s.title("客西馬尼園祈禱：兩位畫家的對照", 60)
    s.art("1455-1456 客西馬尼園祈禱 Agony in the Garden.jpg", (225, 265, 650, 500))
    s.art("客西馬尼園祈禱 The Agony in the Garden (約 1459).jpg", (905, 265, 800, 500))
    s.text("By Andrea Mantegna", (225, 825, 650, 60), 35, "latin", RUST, "center")
    s.text("By Giovanni Bellini", (905, 825, 800, 60), 35, "latin", RUST, "center")
    s.text("鑿刻般的岩石・銳利衣褶", (225, 920, 650, 55), 37, align="center")
    s.text("桃色黎明・柔和氛圍", (905, 920, 800, 55), 37, align="center")
    s.save()


def build():
    build_intro()

    s = Slide(3, "哀悼死去的基督")
    s.art(LAMENT, (245, 225, 895, 735))
    s.text("哀悼死去的基督", (1190, 290, 470, 220), 65, "title", RUST)
    s.line((1190, 540, 1660, 540))
    s.text("被推到\n極端前景的\n釘痕", (1190, 600, 470, 290), 59)
    s.save()

    s = Slide(4, "透視縮短法")
    s.art(LAMENT, (245, 215, 895, 745))
    s.text("劇烈的\n透視縮短法", (1190, 290, 480, 230), 65, "title", RUST)
    s.line((1190, 565, 1655, 565))
    s.text("邊緣的哀悼者", (1190, 625, 475, 180), 54)
    s.save()

    s = Slide(5, "帕多瓦")
    s.title("從帕多瓦出發")
    s.text("他把透視法、人體結構與古羅馬雕刻知識，\n揉進繪畫。", (250, 230, 1410, 145), 46)
    s.art("Padua 義大利 帕多瓦.JPG", (250, 400, 1410, 500))
    s.text("義大利 帕多瓦", (250, 925, 1410, 55), 39, "title", RUST, "center")
    s.save()

    build_art_influences()
    build_ovetari()
    build_portrait_comparison()
    build_garden_comparison()

    s = Slide(10, "聖澤諾祭壇畫")
    s.art("Andrea_Mantegna_images/IMG-005_San_Zeno_Altarpiece.jpg", (245, 225, 970, 735))
    s.text("聖澤諾\n祭壇畫", (1265, 305, 410, 230), 69, "title", RUST)
    s.line((1265, 590, 1665, 590))
    s.text("統一的\n古典涼廊\n框架", (1265, 655, 410, 255), 53)
    s.save()

    s = Slide(11, "曼圖亞宮廷")
    s.title("宮廷畫家：空間掌控的全新維度", 61)
    s.art("House of Gonzaga.png", (340, 250, 250, 290), framed=False)
    s.text("貢扎加家族", (245, 570, 445, 60), 46, "title", RUST, "center")
    s.text("成為曼圖亞\n宮廷畫家後，\n空間掌控發展出\n全新維度。", (260, 680, 450, 285), 43)
    s.art("House of Gonzaga 扎加家族.jpg", (800, 250, 870, 660))
    s.text("Gonzaga family by Andrea Mantegna", (790, 935, 890, 45), 29, "latin", INK, "center")
    s.save()

    s = Slide(12, "夫婦廳天窗")
    s.art(CEILING, (240, 240, 990, 670))
    s.text("夫婦廳天窗", (1280, 325, 400, 200), 67, "title", RUST)
    s.line((1280, 565, 1670, 565))
    s.text("平坦天花板上的\n空間錯視", (1280, 645, 400, 240), 49)
    s.save()

    s = Slide(13, "仰視透視")
    s.title("仰視透視")
    s.art(CEILING, (255, 290, 780, 540))
    s.text("從觀眾頭頂上方逼近的\n空間錯視手法，創造\n三維空間的幻覺。", (1100, 290, 555, 300), 43)
    s.line((1100, 650, 1655, 650))
    s.text("可視為現代沉浸式\n體驗的先驅。", (1100, 725, 555, 160), 43, color=RUST)
    s.save()

    s = Slide(14, "創作歷程")
    s.title("從古典造型到天頂錯視", 67)
    steps = [("少年時期", "於帕多瓦\n接觸古物\n與石膏"), ("1450年代", "園中祈禱：\n展現雕塑般的\n堅實造型"), ("1460年代", "成為宮廷畫家\n服務貢扎加\n家族"), ("1470年代", "完成夫婦廳\n天窗，玩轉\n天頂錯視")]
    for i, (heading, body) in enumerate(steps):
        x = 245 + i * 365
        s.draw.rounded_rectangle((x * 2, 340 * 2, (x + 325) * 2, 840 * 2), radius=22, fill=IVORY, outline=GOLD, width=4)
        s.text(f"0{i + 1}", (x + 25, 375, 275, 50), 30, "latin", GOLD, "center")
        s.text(heading, (x + 15, 470, 295, 70), 43, "title", RUST, "center")
        s.line((x + 40, 565, x + 285, 565))
        s.text(body, (x + 15, 620, 295, 190), 37, align="center")
        if i < 3:
            xx = x + 334
            s.line((xx, 590, xx + 23, 590), 4)
            s.draw.polygon([(int((xx + 25) * 2), 1180), (int((xx + 12) * 2), 1160), (int((xx + 12) * 2), 1200)], fill=GOLD)
    s.save()

    s = Slide(15, "版畫與空間")
    s.title("海神之戰", 68)
    s.art("海神之戰 The Battle of Sea Gods, 1480.jpg", (245, 235, 1000, 655))
    s.art("Isabella d’Este.jpg", (1330, 275, 290, 470))
    s.text("伊莎貝拉・德斯特", (1265, 795, 415, 100), 37, "title", RUST, "center")
    s.text("用版畫線條，形塑強烈空間感。", (250, 930, 995, 55), 43, align="center")
    s.save()

    s = Slide(16, "帕納索斯山")
    s.art(PARNA, (245, 210, 965, 750))
    s.text("帕納索斯山", (1270, 320, 405, 210), 65, "title", RUST)
    s.line((1270, 585, 1670, 585))
    s.text("書房裡的\n神話場景\n與空間配置", (1270, 660, 405, 240), 49)
    s.save()

    s = Slide(17, "凱撒的凱旋")
    s.art("凱撒的凱旋 Triumphs of Caesar 1-9 3x3.png", (245, 210, 785, 750))
    s.text("讓古羅馬\n走過眼前", (1100, 250, 565, 210), 67, "title", RUST)
    s.bullets(["九幅大型畫布，\n連成行進隊列", "號手、戰利品與負重人體，\n延續浮雕般的造型", "這是文藝復興對古羅馬的\n想像，並非古代現場紀錄"], 1100, 530, 565, 36, 148)
    s.save()

    s = Slide(18, "畫框與觀看")
    s.text("畫框也參與\n這場相遇", (245, 235, 550, 220), 66, "title", RUST)
    s.text("獻聖嬰於聖殿", (245, 525, 550, 65), 43, "title")
    s.text("靠墊、雙手與面孔，\n都靠近畫面邊緣。", (245, 650, 550, 145), 41)
    s.text("1454・蛋彩於畫布\n柏林國立繪畫館", (245, 880, 550, 85), 28, color=MUTED)
    s.art("奉獻耶穌於聖殿Presentation of Jesus at the Temple.jpg", (845, 230, 835, 710))
    s.save()

    s = Slide(19, "神話的可見衝突")
    s.text("抽象的惡德\n化為可見的衝突", (245, 235, 550, 220), 55, "title", RUST)
    s.text("智慧女神驅逐惡德", (245, 520, 550, 100), 43, "title")
    s.text("密涅瓦衝入花園，\n怪異身影四散逃離。", (245, 675, 550, 145), 41)
    s.text("約1500–1502・蛋彩於畫布\n巴黎羅浮宮", (245, 885, 550, 80), 27, color=MUTED)
    s.art("密涅瓦驅逐惡習 Minerva Expelling the Vices.jpg", (845, 230, 835, 710))
    s.save()

    s = Slide(20, "聖塞巴斯提安")
    s.title("曼特尼亞的三幅聖塞巴斯提安", 61)
    data = [("Andrea_Mantegna_images/IMG-006_St_Sebastian_Vienna.jpg", "維也納藝術史博物館", "古典遺跡中的\n堅定信仰", "雕塑般的身體，\n呼應廢柱與碎石"), ("聖塞巴斯提安 Saint Sebastian 1480.jpg", "巴黎羅浮宮", "紀念碑般的\n莊嚴力量", "仰視構圖，凸顯\n受苦身軀的尊嚴"), ("聖塞巴斯提安 Saint Sebastian 1506.jpg", "威尼斯黃金宮", "暗背景中的\n痛苦與無常", "扭轉的身體與燭煙，\n提醒生命短暫")]
    for i, (name, museum, title, body) in enumerate(data):
        x = 255 + i * 505
        s.art(name, (x, 235, 390, 490))
        s.text(museum, (x - 30, 750, 450, 55), 31, "title", MUTED, "center")
        s.text(title, (x - 25, 815, 440, 100), 36, "title", RUST, "center", 0.18)
        s.text(body, (x - 25, 920, 440, 70), 30, align="center", gap=0.15)
    s.save()

    s = Slide(21, "回到冰冷的石板")
    s.art(LAMENT, (245, 225, 895, 735))
    s.text("回到冰冷的\n石板", (1190, 300, 480, 220), 65, "title", RUST)
    s.line((1190, 570, 1665, 570))
    s.text("直面\n赤裸裸的苦難", (1190, 655, 480, 210), 54)
    s.save()

    s = Slide(22, "畫家把你放在哪裡")
    s.art("Crucifixion.jpg", (245, 260, 880, 640))
    s.text("Crucifixion (1457-1460)", (240, 930, 890, 50), 34, "latin", RUST, "center")
    s.text("下次走進\n博物館，", (1180, 280, 490, 240), 68, "title")
    s.line((1180, 575, 1670, 575))
    s.text("畫家把你\n放在了哪裡？", (1180, 665, 490, 220), 62, "title", RUST)
    s.save()

    manifest = {"method": "Deterministic Pillow composition; user authorized on 2026-10-23", "background": f"{STEM}_background.png", "size": SIZE, "completed_slides": list(range(2, 23)), "unchanged": [], "artwork_policy": "Original local image pixels resized proportionally. No cropping, AI generation, retouching, recoloring or extra artwork details.", "notes": ["Requested 004 resolves to existing 0004.png", "San Zeno source found in images/Andrea_Mantegna_images/", "Camera picta.png absent; used Camera picta.jpg", "Only slides 0002 through 0022 overwritten"], "slides": records}
    (ROOT / "design_revision_log.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    make_previews()


def make_previews(ranges=((2, 8), (9, 15), (16, 22))):
    preview_dir = ROOT / "review"
    preview_dir.mkdir(exist_ok=True)
    for start, stop in ranges:
        sheet = Image.new("RGB", (1920, 1305), "#28231F")
        d = ImageDraw.Draw(sheet)
        for i, n in enumerate(range(start, stop + 1)):
            thumb = Image.open(OUT / f"{STEM}_slide_{n:04d}.png").resize((640, 360), Image.Resampling.LANCZOS)
            x, y = (i % 3) * 640, (i // 3) * 435
            sheet.paste(thumb, (x, y + 50))
            d.text((x + 15, y + 10), f"{n:04d}", font=font(14, "latin"), fill="white")
        sheet.save(preview_dir / f"slides_{start:04d}_{stop:04d}.jpg", quality=92)


if __name__ == "__main__":
    if "--slide-2-only" in sys.argv:
        build_intro()
        log_path = ROOT / "design_revision_log.json"
        manifest = json.loads(log_path.read_text(encoding="utf-8"))
        manifest["slides"] = [records[0] if item["slide"] == 2 else item for item in manifest["slides"]]
        manifest["notes"].append("Slide 0002 restored to the original illustrated image at the user's request; old text panel replaced with large type.")
        log_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        make_previews()
    else:
        build()
