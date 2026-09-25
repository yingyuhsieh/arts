"""Rebuild the requested American Gothic PNG slides with exact source images and text."""

import ctypes
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
IMAGES = ROOT / "images"
OUT = Path(__file__).resolve().parent
PREFIX = "圖像解剖：解碼《美國哥德式》_slide_"
W, H = 1280, 720
INK = "#19343b"
MUTED = "#4c6264"
TEAL = "#087e7b"
PALE = "#e4f1ed"
CREAM = "#faf6eb"
GOLD = "#b77a36"
WHITE = "#fffdf7"
FONT = "C:/Windows/Fonts/msjh.ttc"
BOLD = "C:/Windows/Fonts/msjhbd.ttc"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def text(draw, xy, value, size=30, fill=INK, bold=False, width=None, gap=8):
    x, y = xy
    f = font(size, bold)
    lines = []
    for paragraph in value.split("\n"):
        if not width:
            lines.append(paragraph)
            continue
        line = ""
        for char in paragraph:
            trial = line + char
            if line and draw.textlength(trial, font=f) > width:
                lines.append(line)
                line = char
            else:
                line = trial
        lines.append(line)
    step = size + gap
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += step
    return y


def base(section, title, subtitle=None):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 13), fill=TEAL)
    d.rectangle((0, H - 20, W, H), fill="#d9e9e2")
    d.ellipse((-210, 480, 360, 950), outline="#d8e2d7", width=4)
    d.ellipse((1110, -300, 1510, 130), outline="#d8e2d7", width=4)
    d.text((62, 35), "圖像解剖  /  美國哥德式", font=font(19, True), fill=TEAL)
    d.text((1115, 37), section, font=font(18), fill=MUTED)
    text(d, (62, 79), title, 46, INK, True, 1120)
    if subtitle:
        text(d, (64, 143), subtitle, 23, MUTED, width=1120)
    d.line((63, 190, 1216, 190), fill="#c8d9d1", width=2)
    return im, d


def panel(draw, box, fill=WHITE, outline="#c8dad3", radius=22, width=2):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def picture(im, name, box, mode="cover", radius=16):
    path = IMAGES / name
    with Image.open(path) as src:
        src = ImageOps.exif_transpose(src)
        if "A" in src.getbands():
            background = Image.new("RGBA", src.size, "white")
            src = Image.alpha_composite(background, src.convert("RGBA")).convert("RGB")
        else:
            src = src.convert("RGB")
        w, h = box[2] - box[0], box[3] - box[1]
        if mode == "contain":
            fitted = ImageOps.contain(src, (w, h), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (w, h), WHITE)
            canvas.paste(fitted, ((w - fitted.width) // 2, (h - fitted.height) // 2))
        else:
            canvas = ImageOps.fit(src, (w, h), Image.Resampling.LANCZOS)
        mask = Image.new("L", (w, h))
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius, fill=255)
        im.paste(canvas, (box[0], box[1]), mask)
    ImageDraw.Draw(im).rounded_rectangle(box, radius, outline="#bdcdc4", width=2)


def label(draw, xy, value, size=21, width=None):
    return text(draw, xy, value, size, MUTED, width=width)


def bullet(draw, x, y, value, width=470, size=25):
    draw.ellipse((x, y + 12, x + 10, y + 22), fill=TEAL)
    return text(draw, (x + 25, y), value, size, INK, width=width - 25) + 10


def save(im, n):
    # An ASCII staging name avoids intermittent Windows shell encoding errors.
    im.save(OUT / f"_rendered_slide_{n:04d}.png", optimize=True)


def make_slides():
    im, d = base("導言", "為什麼兩張臉如此嚴肅？", "從人物、農舍與草叉，解開《美國哥德式》的謎團")
    picture(im, "faces.jpg", (540, 223, 1216, 624))
    panel(d, (63, 256, 494, 585))
    text(d, (93, 289), "一幅熟悉的畫，\n藏著三個問題", 34, INK, True)
    y = 410
    for line in ("他們是誰？", "小屋為何成為主角？", "草叉暗示了什麼？"):
        y = bullet(d, 95, y, line, 340)
    label(d, (547, 641), "格蘭特・伍德，《美國哥德式》局部，1930", 19)
    save(im, 2)

    im, d = base("觀看路線", "六個觀看線索", "依序觀察，讓畫面的疑問逐一浮現")
    cards = [(64, 225, 392, 345), (408, 225, 736, 345), (64, 365, 392, 485),
             (408, 365, 736, 485), (64, 505, 392, 625), (408, 505, 736, 625)]
    items = [("人物關係", "畫中兩人是誰？"), ("真實農舍", "尖拱窗從何而來？"),
             ("草叉象徵", "農具如何連結人物？"), ("畫框構圖", "線條如何引導視線？"),
             ("不同解讀", "諷刺或致敬？"), ("長久影響", "為何不斷被引用？")]
    for box, (head, body) in zip(cards, items):
        panel(d, box, PALE, radius=18)
        text(d, (box[0] + 20, box[1] + 19), head, 27, TEAL, True)
        text(d, (box[0] + 20, box[1] + 66), body, 21, INK)
    picture(im, "IMG-002_American_Gothic_House.jpg", (765, 225, 1215, 625))
    label(d, (772, 640), "愛荷華州埃爾登的美國哥德式小屋", 19)
    save(im, 3)

    im, d = base("人物", "似曾相識的謎團", "熟悉的面孔，卻讓人越看越疑惑")
    picture(im, "faces.jpg", (63, 233, 715, 615))
    panel(d, (750, 248, 1215, 595))
    text(d, (785, 285), "看似農家父女，\n其實是畫家安排的\n兩位模特兒。", 34, INK, True, 390, 15)
    label(d, (785, 500), "先看人物，再問這幅畫想說什麼。", 23, 390)
    save(im, 4)

    im, d = base("作品", "名畫其實不大", "近看才能細讀表情、衣紋與尖拱窗")
    picture(im, "yy.collection.JPEG", (95, 211, 548, 622), "contain")
    label(d, (96, 637), "我到芝加哥藝術博物館的伴手禮", 19)
    panel(d, (605, 255, 1200, 575))
    text(d, (645, 301), "《美國哥德式》", 39, INK, True)
    text(d, (645, 378), "畫布約 78 × 65.3 公分。", 31, TEAL, True)
    text(d, (645, 448), "作品不大，卻成為美國\n最廣為人知的圖像之一。", 27, INK, width=500)
    save(im, 5)

    im, d = base("農舍", "農舍才是故事的起點", "畫家先注意到尖拱窗，才想像屋前應該站著誰")
    picture(im, "map.png", (620, 217, 1210, 605), "contain")
    panel(d, (63, 239, 572, 576))
    text(d, (99, 273), "愛荷華州・埃爾登", 32, TEAL, True)
    text(d, (99, 346), "1930 年，格蘭特・伍德\n看見這棟木屋。", 29, INK, width=435)
    text(d, (99, 465), "屋頂的哥德式尖拱窗，\n成了畫作的視覺核心。", 26, INK, width=435)
    label(d, (633, 620), "地圖截圖：American Gothic House Center", 18)
    save(im, 6)

    im, d = base("農舍", "真實的迪布爾小屋", "正面與側面照片，對照畫中的建築")
    picture(im, "The Dibble House, Eldon, Iowa.jpg", (63, 222, 737, 567))
    picture(im, "This side view evinces the modest size of the house.jpg", (765, 222, 1215, 567), "contain")
    panel(d, (63, 584, 1215, 666), PALE, radius=14)
    text(d, (87, 600), "正面：醒目的尖拱窗", 23, TEAL, True)
    text(d, (765, 600), "側面：屋身其實相當小巧", 23, TEAL, True)
    save(im, 7)

    im, d = base("人物", "畫家想像的屋主", "伍德為真實農舍安排了兩位模特兒")
    picture(im, "icon.png", (681, 225, 1157, 620), "contain")
    panel(d, (63, 247, 623, 586))
    text(d, (98, 276), "畫中女人", 29, TEAL, True)
    text(d, (98, 319), "畫家的妹妹南・伍德・葛蘭姆", 24, INK, width=490)
    text(d, (98, 396), "畫中男人", 29, TEAL, True)
    text(d, (98, 439), "牙醫拜倫・麥基比博士", 24, INK, width=490)
    label(d, (690, 634), "照片：南・伍德・葛蘭姆與拜倫・麥基比", 18)
    save(im, 8)

    im, d = base("人物", "不是一對真正的農夫婦", "看似尋常的組合，其實由畫家精心安排")
    picture(im, "faces.jpg", (622, 231, 1215, 613))
    panel(d, (63, 257, 578, 565))
    text(d, (98, 289), "畫面：", 27, TEAL, True)
    text(d, (98, 337), "兩人並肩站在農舍前，\n容易被看成夫妻。", 26, INK, width=445)
    text(d, (98, 444), "現實：", 27, TEAL, True)
    text(d, (98, 490), "他們是分別受邀的模特兒。", 25, INK, width=445)
    save(im, 9)

    im, d = base("人物", "兩位模特兒的真實身分", "畫中的關係是畫家設計的角色設定")
    picture(im, "IMG-001_American_Gothic_1930.jpg", (62, 233, 461, 616), "contain")
    picture(im, "Nan Wood Graham (1899-1990) - Find a Grave Memorial.png", (749, 233, 1215, 549), "contain")
    panel(d, (486, 265, 717, 566), PALE)
    text(d, (512, 291), "南・伍德\n葛蘭姆", 27, TEAL, True, 180)
    text(d, (512, 404), "畫家的妹妹", 23, INK)
    text(d, (512, 471), "拜倫・麥基比\n畫家的牙醫", 21, INK, width=180)
    label(d, (750, 568), "右：兩位模特兒與畫作的合影", 18)
    save(im, 10)

    im, d = base("構圖", "畫框裡的張力", "尖拱、草叉與人物姿態互相呼應")
    picture(im, "Grant Wood American Gothic.jpg", (790, 218, 1177, 622), "contain")
    panel(d, (63, 250, 738, 584))
    y = 290
    for line in ("尖拱窗：屋頂的垂直焦點", "草叉：向上延伸的三齒形", "人物：僵直站姿與重複線條"):
        y = bullet(d, 99, y, line, 600, 29) + 24
    save(im, 11)

    im, d = base("細節", "草叉：工具，也是構圖線索", "三根叉齒呼應窗框、衣縫與人物挺直的姿態")
    picture(im, "3.png", (71, 225, 495, 615), "contain")
    picture(im, "Tine Forged Hay Fork.png", (750, 225, 1160, 615), "contain")
    panel(d, (515, 265, 730, 574), PALE)
    text(d, (541, 294), "畫中草叉", 26, TEAL, True)
    text(d, (541, 360), "三齒造型\n向上延伸", 25, INK, width=160)
    text(d, (541, 487), "與實物對照", 23, MUTED)
    label(d, (760, 634), "右：三齒乾草叉參考圖", 18)
    save(im, 13)

    im, d = base("構圖與風格", "細節重複，風格延伸", "先看《美國哥德式》的局部，再看伍德筆下的鄉村")
    detail_names = ["1.png", "2.png", "3.png", "4.png"]
    detail_labels = ["尖拱窗", "人物與農舍", "三齒草叉", "平行視線"]
    for idx, (name, caption) in enumerate(zip(detail_names, detail_labels)):
        x = 62 + idx * 303
        picture(im, name, (x, 215, x + 278, 346), "contain", 9)
        text(d, (x + 3, 351), caption, 19, TEAL, True)
    picture(im, "IMG-004_Stone_City_Iowa_1930.jpg", (62, 407, 616, 621), "contain")
    picture(im, "IMG-005_Midnight_Ride_Paul_Revere_1931.jpg", (663, 407, 1216, 621), "contain")
    text(d, (62, 633), "Grant Wood — Stone City, Iowa (1930)", 18, INK, True)
    text(d, (663, 633), "Grant Wood — The Midnight Ride of Paul Revere (1931)", 18, INK, True)
    save(im, 14)

    im, d = base("解讀", "諷刺，還是致敬？", "《美國哥德式》從問世起就引發相反的閱讀")
    picture(im, "Grant Wood American Gothic.jpg", (830, 231, 1175, 619), "contain")
    for y, head, body in ((245, "諷刺的讀法", "嚴肅面容與僵硬姿態，像是在挖苦鄉村保守生活。"),
                          (424, "致敬的讀法", "挺立的人物與簡樸農舍，也能象徵堅韌與自持。")):
        panel(d, (63, y, 781, y + 151), PALE)
        text(d, (94, y + 17), head, 29, TEAL, True)
        text(d, (94, y + 68), body, 24, INK, width=645)
    save(im, 15)

    im, d = base("解讀", "兩種相反的閱讀", "同一組線索，會因觀看立場而產生不同意義")
    panel(d, (63, 223, 1216, 620))
    d.rectangle((63, 223, 1216, 294), fill=TEAL)
    text(d, (94, 239), "觀看角度", 27, WHITE, True)
    text(d, (345, 239), "表情與姿態", 27, WHITE, True)
    text(d, (814, 239), "可能的理解", 27, WHITE, True)
    rows = [("諷刺", "緊繃、拘謹", "對鄉村保守形象的揶揄"),
            ("致敬", "堅定、克制", "對困境中韌性的讚賞")]
    for idx, row in enumerate(rows):
        top = 294 + idx * 161
        if idx == 1:
            d.rectangle((65, top, 1214, top + 161), fill="#eef5f0")
        d.line((63, top, 1216, top), fill="#cfdbd4", width=2)
        for x, val, maxw in zip((94, 345, 814), row, (200, 410, 355)):
            text(d, (x, top + 51), val, 28, INK, idx == 0, maxw)
    save(im, 16)

    im, d = base("傳播", "從畫展到大眾文化", "一幅畫如何成為反覆被引用的視覺符號")
    d.line((170, 377, 1110, 377), fill=TEAL, width=7)
    events = [(220, "1929", "經濟大蕭條\n開始"),
              (640, "1930", "畫作完成並獲\n芝加哥藝術博物館獎項"),
              (1050, "1942", "戈登・帕克斯\n以同名攝影回應")]
    for x, year, desc in events:
        d.ellipse((x - 17, 360, x + 17, 394), fill=TEAL)
        panel(d, (x - 135, 232, x + 135, 345), PALE)
        text(d, (x - 99, 252), year, 42, TEAL, True)
        text(d, (x - 145, 417), desc, 23, INK, width=290)
    save(im, 17)

    im, d = base("影響", "不斷被改寫的經典", "人物站姿、農舍與草叉，成了容易辨認的圖像語法")
    panel(d, (63, 222, 1216, 621))
    d.rectangle((63, 222, 1216, 291), fill=TEAL)
    for x, val in ((92, "原畫線索"), (392, "後來的改寫"), (850, "效果")):
        text(d, (x, 238), val, 27, WHITE, True)
    rows = [("人物並肩", "更換人物身分與服裝", "借用熟悉構圖傳達新議題"),
            ("草叉與農舍", "替換道具或背景", "保留辨識度，改變語意"),
            ("嚴肅表情", "改成幽默、抗議或廣告", "從名畫走入流行文化")]
    for idx, row in enumerate(rows):
        top = 291 + idx * 110
        if idx % 2 == 1:
            d.rectangle((65, top, 1214, top + 110), fill="#eef5f0")
        d.line((64, top, 1215, top), fill="#d0ddd6", width=2)
        for x, val, maxw in zip((92, 392, 850), row, (270, 420, 325)):
            text(d, (x, top + 28), val, 25, INK, width=maxw)
    save(im, 18)

    im, d = base("總結", "三個元素，組成一個圖像公式", "人物、農具與農舍在畫面中互相呼應")
    picture(im, "Grant Wood American Gothic.jpg", (63, 218, 463, 618), "contain")
    x0 = 504
    parts = [("人物", "並肩站立"), ("草叉", "垂直線條"), ("農舍", "尖拱窗與屋頂")]
    for idx, (head, body) in enumerate(parts):
        y = 233 + idx * 126
        panel(d, (x0, y, 1202, y + 104), PALE)
        text(d, (x0 + 25, y + 18), head, 30, TEAL, True)
        text(d, (x0 + 168, y + 24), body, 26, INK)
    text(d, (520, 632), "熟悉的元素，仍容許彼此矛盾的解讀。", 22, MUTED)
    save(im, 19)

    im, d = base("今日", "從畫中農舍到文化地標", "真實小屋仍在愛荷華州埃爾登，持續吸引參觀者")
    picture(im, "IMG-002_American_Gothic_House.jpg", (63, 222, 801, 612))
    panel(d, (835, 247, 1212, 592))
    text(d, (869, 283), "迪布爾小屋", 33, TEAL, True)
    text(d, (869, 362), "因畫作聞名，\n成為地方文化景點。", 27, INK, width=306)
    text(d, (869, 496), "畫中的想像，回到了\n現實中的地點。", 23, MUTED, width=306)
    save(im, 20)

    im, d = base("回望", "真實房屋，重新組成的場景", "把地圖、正面與側面照片放在一起，看清畫家的取捨")
    picture(im, "map.png", (63, 216, 540, 491), "contain")
    picture(im, "The Dibble House, Eldon, Iowa.jpg", (568, 216, 1216, 491))
    picture(im, "This side view evinces the modest size of the house.jpg", (63, 518, 445, 648), "contain")
    panel(d, (477, 518, 1215, 648), PALE, radius=16)
    text(d, (504, 533), "真實小屋提供尖拱窗與屋頂輪廓；\n人物、姿態與前景則由伍德重新安排。", 24, INK, width=670)
    save(im, 21)

    copy_file = ctypes.WinDLL("kernel32", use_last_error=True).CopyFileW
    copy_file.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_bool)
    copy_file.restype = ctypes.c_bool
    for n in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21):
        staging = OUT / f"_rendered_slide_{n:04d}.png"
        final = OUT / f"{PREFIX}{n:04d}.png"
        if not copy_file(str(staging), str(final), False):
            raise ctypes.WinError(ctypes.get_last_error())
        staging.unlink()


if __name__ == "__main__":
    make_slides()
