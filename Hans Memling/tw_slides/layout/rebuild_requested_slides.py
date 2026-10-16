"""Compose requested Traditional Chinese slides from unmodified source artwork."""

from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SLIDES = ROOT / 'tw_slides'
OUT = SLIDES / 'update'
IMAGES = ROOT / 'images'
PREFIX = '漢斯・梅姆林：藝術公關與視覺敘事先驅'
SCALE = 2
SIZE = (3840, 2160)
FONT = '/System/Library/Fonts/STHeiti Medium.ttc'
INK = '#183247'
MUTED = '#5b4733'
GOLD = '#ab8247'
BG = Image.open(SLIDES / f'{PREFIX}_background.png').convert('RGB').resize(SIZE, Image.Resampling.LANCZOS)
MANIFEST = []
TEXT_BOXES = []


def font(size):
    return ImageFont.truetype(FONT, round(size * SCALE))


def panel(box, fill=(255, 250, 238, 244), radius=14):
    layer = Image.new('RGBA', SIZE)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(tuple(round(v * SCALE) for v in box), radius=radius * SCALE,
                        fill=fill, outline=GOLD, width=2)
    canvas.alpha_composite(layer)


def wrapped(text, size, width):
    d = ImageDraw.Draw(canvas)
    result = []
    for paragraph in text.split('\n'):
        line = ''
        for char in paragraph:
            if line and d.textlength(line + char, font=font(size)) > width * SCALE:
                result.append(line)
                line = char
            else:
                line += char
        result.append(line)
    return result


def text(content, box, size=34, color=INK, align='left', spacing=1.35):
    x, y, w, h = box
    lines = wrapped(content, size, w)
    line_h = size * spacing
    if len(lines) * line_h > h + 2:
        raise ValueError(f'Slide {number}: text overflow: {content!r}, {len(lines)*line_h} > {h}')
    d = ImageDraw.Draw(canvas)
    for i, line in enumerate(lines):
        width = d.textlength(line, font=font(size)) / SCALE
        tx = x + (w - width) / 2 if align == 'center' else x
        d.text((round(tx * SCALE), round((y + i * line_h) * SCALE)), line,
               font=font(size), fill=color, anchor='lt')
    TEXT_BOXES.append({'slide': number, 'text': content, 'box': box, 'font_px': size * SCALE})


def art(name, box, caption=None, caption_size=29):
    path = IMAGES / name
    original = ImageOps.exif_transpose(Image.open(path)).convert('RGBA')
    x, y, w, h = box
    cap_h = max(58, 25 + len(wrapped(caption, caption_size, w-20))*caption_size*1.15) if caption else 0
    avail_h = h - cap_h
    ratio = min(w * SCALE / original.width, avail_h * SCALE / original.height)
    original = original.resize((round(original.width * ratio), round(original.height * ratio)),
                               Image.Resampling.LANCZOS)
    px = round((x + w / 2) * SCALE - original.width / 2)
    py = round((y + avail_h / 2) * SCALE - original.height / 2)
    canvas.alpha_composite(original, (px, py))
    if caption:
        panel((x, y + h - cap_h + 4, x + w, y + h), radius=8)
        text(caption, (x + 10, y + h - cap_h + 14, w - 20, cap_h - 14),
             caption_size, align='center', spacing=1.15)
    ASSETS.append(name)
    return (px / SCALE, py / SCALE, original.width / SCALE, original.height / SCALE)


def start(n, title, subtitle=None):
    global canvas, number, ASSETS
    number = n
    ASSETS = []
    canvas = BG.convert('RGBA').copy()
    panel((80, 48, 1840, 180 if subtitle else 145))
    text(title, (110, 67, 1700, 78), 52, align='center')
    if subtitle:
        text(subtitle, (120, 127, 1680, 49), 35, align='center')


def finish():
    if number in (15, 16, 17, 18):
        credit = ('Photo: Rainer Halama · Wikimedia Commons · CC0' if number == 17
                  else '圖像來源：Wikimedia Commons')
        panel((100, 1024, 1820, 1058), radius=5)
        text(credit, (120, 1029, 1680, 29), 20, MUTED)
    file = OUT / f'{PREFIX}_slide_{number:04d}.png'
    canvas.convert('RGB').save(file, optimize=True)
    MANIFEST.append({'slide': number, 'file': file.name, 'images': ASSETS})
    print(f'Saved {number:02d}', flush=True)


def description(content, y=900, h=116, size=36):
    panel((100, y, 1820, y + h))
    text(content, (126, y + 19, 1668, h - 27), size, align='center')


start(2, '如果你的天價家族祭壇畫，在海上被海盜劫持了呢？')
panel((80, 48, 1840, 240), fill=(255, 250, 238, 255))
text('如果你的天價家族祭壇畫，\n在海上被海盜劫持了呢？', (110, 67, 1700, 165), 64, align='center', spacing=1.25)
art('(p2) piracy.jpg', (110, 270, 1050, 720))
art('最後的審判三聯畫 The Last Judgment Triptych (close).jpg',
    (1220, 270, 580, 730), '最後的審判 (關閉狀態)', 31)
finish()

start(3, '海上劫掠，改變名畫的命運')
art('最後的審判三聯畫 The Last Judgment Triptych.jpg', (100, 185, 1130, 745))
art('(p2) piracy.jpg', (1280, 190, 530, 410))
panel((1260, 630, 1820, 960))
text('最後的審判\n1467–1473\n\n1473 年，畫作在海上\n遭保羅・貝內克截獲。', (1290, 657, 500, 290), 40)
finish()

start(4, '海上驚世劫案')
panel((110, 260, 1150, 850))
text('改變畫作命運的\n波羅的海劫掠', (155, 305, 950, 180), 62)
text('這幅畫展現了驚人的秩序感與細節。\n\n這位畫家，讓各國銀行家與富商\n趨之若鶩。', (155, 535, 950, 260), 44)
art('(p4) Hans Memling.jpg', (1250, 190, 550, 810), 'Hans Memling', 34)
finish()

start(5, '來自德國的藝術大師')
art('(p5) 德國塞利根施塔特 漢斯·姆林之家 (Hans-Memling-Haus).jpg',
    (120, 195, 1100, 650), '漢斯·姆林之家', 32)
art('(p5) Rogier van der Weyden 羅希爾·范德魏登.jpg',
    (1300, 195, 490, 650), '羅希爾·范德魏登', 31)
description('約 1430–1440 年生於德國塞利根施塔特。\n確切出生年份仍不詳。', y=875, h=140, size=41)
finish()

start(6, '謎樣畫家的崛起', '從無名小卒到布魯日大師')
art('(p6) Bruges 布魯日.jpg', (220, 190, 1480, 815), '布魯日', 34)
finish()

start(7, '從戲劇張力，到寧靜均衡')
art('(p7) The Descent from the Cross.small by Rogier van der Weyden.png',
    (100, 190, 840, 650), '羅希爾·范德魏登 下十字架', 29)
art('(p7) Hans Memling - Diptych of Maarten Nieuwenhove.jpg',
    (980, 190, 840, 650), '漢斯・梅姆林 馬丁·范·纽文霍夫雙聯畫', 28)
panel((100, 870, 940, 1015))
panel((980, 870, 1820, 1015))
text('強烈的戲劇張力、哀慟的面容，\n以及滑落的淚水。', (126, 897, 788, 100), 34)
text('安靜均衡、克制而祥和，\n保留了極致的優雅。', (1006, 897, 788, 100), 34)
finish()

start(8, '在布魯日，建立自己的藝術事業')
items = [
    ('(p8) Annunciation.JPG', '天使報喜'),
    ('(p8) 手持硬幣的男子肖像 Portrait of a Man with a Coin of the Emperor Nero.jpg', '手持硬幣的男子肖像'),
    ('(p8) 瑪利亞·波蒂納里肖像（瑪利亞·瑪達萊娜·巴倫切利） Portrait of Maria Portinari (Maria Maddalena Baroncelli).jpg', '瑪利亞·波蒂納里肖像'),
]
for i, (name, label) in enumerate(items):
    art(name, (130 + i * 570, 190, 520, 650), label, 29)
description('1465 年 1 月 30 日，梅姆林付費取得布魯日的市民資格。', y=890, h=120, size=43)
finish()

start(9, '畫布上的公關術')
panel((110, 300, 1080, 800))
text('十五世紀的\n個人品牌塑造法', (160, 355, 870, 190), 64)
text('透過肖像，呈現委託人的\n身分、信仰與社會地位。', (160, 605, 870, 140), 44)
art('(p9) 托馬索·波蒂納里肖像 Portrait of Tommaso di Folco Portinari.jpg',
    (1180, 195, 620, 810), '托馬索·波蒂納里肖像', 31)
finish()

start(10, '莫雷爾三聯畫：家族記憶與神聖信仰')
art('莫雷爾三聯畫 Moreel Triptych.jpg', (100, 205, 1720, 670))
description('1484 年：將家族記憶與神聖信仰結合的莊嚴宣示。', y=900, h=110, size=44)
finish()

start(11, '梅姆林的肖像公式')
art('(p11) Hans Memling portraits 2x2 transparent.png', (110, 185, 720, 820))
panel((900, 230, 1810, 930))
text('四分之三側面\n拉近人物與觀者的距離。\n\n雙手輕靠擬真框緣\n建立與畫外世界的連結。\n\n精細臉部與廣闊風景\n共同構成肖像的空間。', (940, 270, 830, 500), 42)
text('家族群像可隨成員增加而更新。', (940, 835, 830, 55), 36, MUTED)
finish()

start(12, '時空的視覺魔術', '打破框架的全景敘事與立體體驗')
art('Hans_Memling_Passione.jpg', (260, 190, 1400, 810), '基督受難場景', 34)
finish()

start(13, '基督受難場景：一座城市，串起多個時刻')
overview = art('Hans_Memling_Passione.jpg', (535, 175, 850, 525))
panel((105, 215, 470, 450))
text('連續的城市風景，\n容納不同時間的故事。\n\n虛線連接六個局部。', (125, 240, 325, 190), 27)
panel((1430, 225, 1815, 460))
text('人物反覆出現，\n帶領目光穿梭於\n受難與復活的歷程。', (1457, 260, 330, 170), 30)
details = [
    ('01_進入耶路撒冷.png', '進入耶路撒冷', (.085, .215)),
    ('04_最後的晚餐.png', '最後的晚餐', (.102, .423)),
    ('06_猶大之吻與耶穌被捕.png', '猶大之吻與耶穌被捕', (.201, .805)),
    ('11_戴荊棘冠冕.png', '戴荊棘冠冕', (.570, .450)),
    ('16_十字架上的受難.png', '十字架上的受難', (.595, .085)),
    ('20_基督復活.png', '基督復活', (.941, .355)),
]
colors = ['#325b85', '#965d22', '#7d3650', '#33695c', '#73528f', '#985038']
d = ImageDraw.Draw(canvas)
for i, (file, label, pos) in enumerate(details):
    x, y, w, h = overview
    a = (x + pos[0] * w, y + pos[1] * h)
    b = (220 + i * 296, 785)
    # Dashed source-to-detail connector; distinct colors and keyed circles aid tracing.
    distance = math.dist(a, b)
    for offset in range(0, int(distance), 15):
        end = min(offset + 8, distance)
        points = [(int((a[0] + (b[0]-a[0])*v/distance)*SCALE),
                   int((a[1] + (b[1]-a[1])*v/distance)*SCALE)) for v in (offset, end)]
        d.line(points, fill=colors[i], width=4)
    ax, ay = a
    d.ellipse(((ax-14)*SCALE, (ay-14)*SCALE, (ax+14)*SCALE, (ay+14)*SCALE),
              fill=colors[i], outline='white', width=2)
    d.text((ax*SCALE, ay*SCALE), str(i+1), font=font(20), fill='white', anchor='mm')
for i, (file, label, pos) in enumerate(details):
    panel((88+i*296, 780, 352+i*296, 1025))
    art('Passion_Scenes_TW/' + file, (100+i*296, 792, 240, 172))
    text(f'{i+1}  {label}', (98+i*296, 974, 244, 48), 21, align='center', spacing=1.05)
finish()

start(14, '祈禱青年與花瓶：翻轉畫板，延伸觀看')
art('(p14) Portrait of a Young Man Praying and Flowers in a Jug.jpg', (105, 210, 660, 620), '肖像與背面的花瓶', 28)
art('(p14) Een majolicavaas met een boeket van lelie, iris en akelei.jpg', (805, 190, 470, 650), '花瓶背面', 29)
art('(p14) Portrait of a Young Man praying.JPG', (1320, 190, 490, 650), '祈禱青年', 29)
description('打破單面觀看：正面肖像與背面花瓶，共同構成祈禱物件。', y=890, h=120, size=42)
finish()

start(15, '三塊畫板，共享一個世界', '三王來朝三聯畫')
art('三王來朝三聯畫 Adoration of the Magi Triptych (Prado Triptych).jpg', (105, 215, 1710, 580))
panel((100, 820, 1820, 1015))
text('左翼誕生 → 中間朝拜 → 右翼聖殿獻祭\n破舊建築與遠方城市，連接三個場景。', (130, 840, 1660, 120), 42, align='center')
text('漢斯・梅姆林｜1470–1472｜木板油畫｜馬德里普拉多博物館', (130, 965, 1660, 40), 25, MUTED, 'center')
finish()

start(16, '風景裡的故事，需要慢慢讀', '聖母七喜，又稱基督降臨與凱旋')
art('信仰七喜（聖母七喜） Scenes from the Joys of Mary (Seven Joys of the Virgin Advent and Triumph of Christ).jpg', (240, 180, 1440, 660))
panel((100, 850, 1820, 1020))
text('中央朝拜與三王旅程串起全景；道路、水域與城鎮引導目光。\n「七喜」題名之下，涵蓋更多敘事情節。', (130, 863, 1660, 110), 40, align='center')
text('漢斯・梅姆林｜1480｜木板油畫｜慕尼黑老繪畫館', (130, 977, 1660, 35), 25, MUTED, 'center')
finish()

start(17, '一面鏡子，連接兩塊畫板', '馬丁・范・紐文霍夫雙聯畫')
art('馬丁·范·紐文霍夫雙聯畫 Diptych of Maarten van Nieuwenhove.jpg', (110, 190, 950, 810))
panel((1110, 220, 1810, 985))
text('凸面鏡\n顯示兩人共處同一房間。\n\n窗戶紋章與祈禱書\n標示委託人的身分。\n\n畫框銘文\n記錄年份與二十三歲年齡。', (1145, 260, 630, 550), 42)
text('漢斯・梅姆林｜1487｜木板油畫\n布魯日聖約翰醫院博物館', (1145, 865, 630, 90), 26, MUTED)
finish()

start(18, '在畫裡看見天國音樂', '天父與歌唱、奏樂的天使')
art('基督與奏樂歌唱的天使 Christ with Singing and Music-Making Angels.jpg', (100, 225, 1720, 510))
panel((100, 770, 1820, 1015))
text('中央人物持水晶球，並作祝福手勢。\n歌唱天使居中，器樂天使分列兩側。\n原為西班牙納赫拉大型祭壇畫的上層。', (135, 795, 1650, 158), 39, align='center')
text('漢斯・梅姆林｜1483–1494｜木板油畫｜安特衛普皇家美術館', (130, 968, 1660, 40), 25, MUTED, 'center')
finish()

start(19, '聖烏蘇拉聖物箱：環繞觀看的微型教堂')
art('(p15-1) St. Ursula Shrine.jpg', (105, 200, 500, 650), '聖烏蘇拉聖物箱', 28)
shrine = [
    ('(p15-2) Virgin and Child.jpg', '聖母與聖嬰'),
    ('(p15-3) Arrival in Rome.jpg', '抵達羅馬'),
    ('(p15-4) Martyrdom.jpg', '殉道'),
    ('(p15-5) Arrival in Cologne.jpg', '抵達科隆'),
    ('(p15-6) St. Ursula shields the Holy Virgins beneath her cloak.png', '聖烏蘇拉庇護童貞女'),
]
for i, (name, label) in enumerate(shrine):
    art(name, (650+i*235, 215, 215, 630), label, 23)
description('需要移動身體、環繞觀看：建築造型與連續圖像，共同展開故事。', y=890, h=120, size=42)
finish()

start(20, '重構大師的全貌', '重新衡量梅姆林的歷史定位')
art('聖約翰祭壇畫（聖凱瑟琳神秘婚禮） St. John Altarpiece (Mystic Marriage of St. Catherine).jpg',
    (280, 185, 1360, 820), '聖約翰祭壇畫（聖凱瑟琳神秘婚禮）', 30)
finish()

start(21, '梅姆林的藝術生涯：五個關鍵時刻')
events = [
    ('1465', '取得市民資格', '在布魯日立足，\n展開藝術事業。'),
    ('1473', '名畫遭劫', '最後的審判\n運往義大利途中\n被截獲。'),
    ('1479', '大型祭壇畫', '為聖約翰醫院\n完成著名祭壇畫。'),
    ('1489', '立體敘事', '聖烏蘇拉聖物箱\n完成並取代舊匣。'),
    ('1494', '留下藝術遺產', '於布魯日逝世，\n留下深遠影響。'),
]
for i, (year, heading, body) in enumerate(events):
    x = 100 + i * 349
    panel((x, 310, x+324, 825))
    text(year, (x+15, 345, 294, 100), 65, align='center')
    text(heading, (x+18, 480, 288, 115), 35, align='center')
    text(body, (x+22, 630, 280, 160), 34, align='center', spacing=1.5)
    if i < 4:
        d = ImageDraw.Draw(canvas)
        ay = 260 * SCALE
        ax = (x+164)*SCALE
        bx = (x+513)*SCALE
        d.line((ax, ay, bx-15, ay), fill=INK, width=5)
        d.polygon(((bx, ay), (bx-22, ay-12), (bx-22, ay+12)), fill=INK)
description('從城市立足、跨國委託，到全景與立體敘事的藝術遺產。', y=895, h=110, size=36)
finish()

start(22, '開闔之間，才能看見完整的梅姆林')
art('Jan Floreins Altarpiece (close).jpg', (130, 195, 650, 635), '賢士來朝 (關閉狀態)', 31)
art('Jan Floreins Altarpiece (open).jpg', (850, 195, 950, 635), '賢士來朝 (展開狀態)', 31)
description('當可開闔的木板被拆開、孤立在白牆上，\n我們還能看見作品完整的觀看經驗嗎？', y=875, h=145, size=42)
finish()

(SLIDES / 'layout' / 'revision_manifest.json').write_text(
    json.dumps({'size': SIZE, 'slides': MANIFEST, 'text_boxes': TEXT_BOXES,
                'source_notes': [
                    'The supplied (p12) filename contains St John Altarpiece; used Hans_Memling_Passione.jpg for slides 12–13.',
                    'Missing image (p14) filename: substituted existing (p14) Portrait of a Young Man praying.JPG at right.',
                    'All artwork is directly composited; aspect ratios and image contents preserved.'
                ]}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Contact sheets are review artifacts, outside the update image sequence.
for group in range(3):
    sheet = Image.new('RGB', (1440, 4*290), '#e5e0d6')
    d = ImageDraw.Draw(sheet)
    for index, n in enumerate(range(2+group*7, min(9+group*7, 23))):
        im = Image.open(OUT / f'{PREFIX}_slide_{n:04d}.png')
        im.thumbnail((700, 260), Image.Resampling.LANCZOS)
        x = (index % 2)*720 + 10
        y = (index // 2)*290 + 25
        sheet.paste(im, (x, y))
        d.text((x, y-20), f'{n:02d}', fill='black')
    sheet.save(SLIDES / 'layout' / f'review_{group+1}.jpg', quality=92)
