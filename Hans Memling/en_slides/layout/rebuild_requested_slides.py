"""Compose requested Traditional Chinese slides from unmodified source artwork."""

from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SLIDES = ROOT / 'en_slides'
OUT = SLIDES / 'update'
IMAGES = ROOT / 'images'
PREFIX = 'Hans_Memling_s_Conquest'
SCALE = 2
SIZE = (3840, 2160)
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
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
        for word in paragraph.split(' '):
            candidate = (line + ' ' + word).strip()
            if line and d.textlength(candidate, font=font(size)) > width * SCALE:
                result.append(line)
                line = word
            else:
                line = candidate
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
    file = OUT / f'{PREFIX}_slide_{number:04d}.png'
    canvas.convert('RGB').save(file, optimize=True)
    MANIFEST.append({'slide': number, 'file': file.name, 'images': ASSETS})
    print(f'Saved {number:02d}', flush=True)


def description(content, y=900, h=116, size=36):
    panel((100, y, 1820, y + h))
    text(content, (126, y + 19, 1668, h - 27), size, align='center')


def notes(items, box, size=40):
    x, y, w, h = box
    panel((x, y, x+w, y+h))
    gap = h / len(items)
    for i, (heading, body) in enumerate(items):
        text(heading, (x+30, y+25+i*gap, w-60, 65), size+3, MUTED)
        text(body, (x+30, y+90+i*gap, w-60, gap-100), size, spacing=1.22)


start(2, 'The Last Judgment | 1467–1473')
art('最後的審判三聯畫 The Last Judgment Triptych (close).jpg',
    (110, 190, 590, 810), 'The Last Judgment Triptych (close)', 31)
art('最後的審判三聯畫 The Last Judgment Triptych.jpg',
    (770, 190, 1040, 810), 'The Last Judgment Triptych (open)', 34)
finish()

start(3, 'The Last Judgment: A Journey Through History')
events = [
    ('1473', 'Seized at sea', 'Hijacked on the Baltic Sea by pirates.'),
    ('1807', 'Taken to Paris', 'Looted by Napoleon’s army and transported to Paris.'),
    ('1944', 'Wartime evacuation', 'Evacuated to Thuringia during World War II.'),
    ('1956', 'Return to Poland', 'Finally returned to Poland.'),
]
for i, (year, heading, body) in enumerate(events):
    x = 110+i*440
    panel((x, 290, x+390, 870))
    text(year, (x+20, 330, 350, 115), 76, align='center')
    text(heading, (x+25, 490, 340, 135), 41, align='center')
    text(body, (x+30, 665, 330, 170), 34, align='center', spacing=1.3)
    if i < 3:
        d = ImageDraw.Draw(canvas)
        ax, bx, yy = (x+195)*2, (x+635)*2, 245*2
        d.line((ax, yy, bx-18, yy), fill=INK, width=6)
        d.polygon(((bx, yy), (bx-24, yy-13), (bx-24, yy+13)), fill=INK)
finish()

start(4, 'The Outsider in Bruges', 'An Undocumented Painter')
art('(p6) Bruges 布魯日.jpg', (240, 205, 1440, 795), 'Bruges', 40)
finish()

start(5, 'From Emotional Drama to Elegant Calm')
art('(p7) The Descent from the Cross.small by Rogier van der Weyden.png',
    (110, 185, 830, 650), 'The Descent from the Cross by Rogier van der Weyden', 31)
art('(p7) Hans Memling - Diptych of Maarten Nieuwenhove.jpg',
    (980, 185, 830, 650), 'Diptych of Maarten Nieuwenhove by Hans Memling', 31)
panel((110, 860, 940, 1015))
panel((980, 860, 1810, 1015))
text('Emotional drama, intense grief,\nand tear-filled faces.', (140, 888, 770, 110), 41)
text('Balanced restraint, elegant calm,\nand a slower visual rhythm.', (1010, 888, 770, 110), 41)
finish()

start(6, 'Bruges Market in 1465')
art('(p11) Hans Memling portraits 2x2 transparent.png', (120, 190, 700, 815))
notes([
    ('International commerce', 'A thriving commercial center.'),
    ('International patrons', 'Italian and British merchants.'),
    ('Religious portraits', 'Strong demand for devotional imagery.'),
    ('Visual identity', 'Portraits expressed status and belief.'),
], (890, 200, 920, 800), 39)
finish()

start(7, 'Faces in the Landscape', 'A New Spatial Order')
art('Sibylla Sambetha.jpg', (190, 200, 650, 800), 'Sibylla Sambetha', 34)
art('Portrait of a Young Man before a Landscape.jpg',
    (1010, 200, 700, 800), 'Portrait of a Young Man before a Landscape', 32)
finish()

start(8, 'The Donne Triptych')
art('唐恩三聯畫 Donne Triptych.jpg', (160, 190, 1600, 660))
description('Featuring the Welsh courtier Sir John Donne.', y=895, h=115, size=48)
finish()

start(9, 'The Halved Composition')
art('Portrait of a Young Man before a Landscape.jpg', (120, 190, 650, 815),
    'Portrait of a Young Man before a Landscape', 31)
notes([
    ('Top', 'Hyper-detailed face against a calm, infinite sky.'),
    ('Bottom', 'Dark attire grounded by a sweeping natural landscape.'),
    ('Effect', 'Brings the subject intimately close while opening endless space behind.'),
], (840, 210, 970, 790), 40)
finish()

start(10, 'Time, Space, and Story', 'Walking Through a Canvas')
art('Hans_Memling_Passione.jpg', (260, 200, 1400, 805), 'Scenes from the Passion of Christ', 37)
finish()

start(11, 'Scenes from the Passion of Christ', 'Six Moments Within One Continuous Landscape')
overview = art('Hans_Memling_Passione.jpg', (535, 200, 850, 510))
panel((105, 225, 470, 460))
text('One city contains events from different moments in time.', (130, 255, 315, 175), 32)
panel((1430, 225, 1815, 465))
text('Follow the dashed lines to six details from the painting.', (1455, 255, 335, 180), 32)
details = [
    ('01_Entry_into_Jerusalem.png', 'Entry into Jerusalem', (.085, .215)),
    ('04_Last_Supper.png', 'Last Supper', (.102, .423)),
    ('06_Betrayal_and_Arrest.png', 'Betrayal and Arrest', (.201, .805)),
    ('11_Crowning_with_Thorns.png', 'Crowning with Thorns', (.570, .450)),
    ('16_Crucifixion.png', 'Crucifixion', (.595, .085)),
    ('20_Resurrection.png', 'Resurrection', (.941, .355)),
]
colors = ['#325b85', '#965d22', '#7d3650', '#33695c', '#73528f', '#985038']
d = ImageDraw.Draw(canvas)
for i, (file, label, pos) in enumerate(details):
    x, y, w, h = overview
    a = (x+pos[0]*w, y+pos[1]*h)
    b = (220+i*296, 785)
    distance = math.dist(a, b)
    for offset in range(0, int(distance), 15):
        end = min(offset+8, distance)
        points = [(round((a[0]+(b[0]-a[0])*v/distance)*2),
                   round((a[1]+(b[1]-a[1])*v/distance)*2)) for v in (offset, end)]
        d.line(points, fill=colors[i], width=4)
    ax, ay = a
    d.ellipse(((ax-14)*2, (ay-14)*2, (ax+14)*2, (ay+14)*2), fill=colors[i], outline='white', width=2)
    d.text((ax*2, ay*2), str(i+1), font=font(20), fill='white', anchor='mm')
for i, (file, label, pos) in enumerate(details):
    panel((88+i*296, 780, 352+i*296, 1030))
    art('Passion_Scenes/'+file, (100+i*296, 792, 240, 164))
    text(f'{i+1}  {label}', (98+i*296, 968, 244, 58), 24, align='center', spacing=1.1)
finish()

start(12, 'How to Read Simultaneous Narrative')
steps = [
    ('Follow Paths', 'Follow the winding paths and architecture.'),
    ('Spot Characters', 'Find the same characters reappearing in different locations.'),
    ('Read Chronology', 'Read the story chronologically across the landscape.'),
]
for i, (heading, body) in enumerate(steps):
    x = 120+i*590
    panel((x, 310, x+500, 830))
    text(heading, (x+35, 355, 430, 130), 47, align='center')
    text(body, (x+35, 555, 430, 225), 42, align='center')
    if i < 2:
        d = ImageDraw.Draw(canvas)
        d.line(((x+515)*2, 560*2, (x+570)*2, 560*2), fill=GOLD, width=8)
        d.polygon((((x+580)*2, 560*2), ((x+558)*2, 546*2), ((x+558)*2, 574*2)), fill=GOLD)
finish()

start(13, 'More Than Flat Wood', 'Renaissance Art in 3D')
art('Diptych of Maarten van Nieuwenhove.png', (250, 205, 1420, 790),
    'Diptych of Maarten van Nieuwenhove', 36)
finish()

start(14, 'Art You Were Meant to Hold')
art('(p14) Portrait of a Young Man Praying and Flowers in a Jug.jpg',
    (110, 250, 800, 680), 'Portrait of a Young Man Praying and Flowers in a Jug', 32)
notes([
    ('Not Two Paintings', 'A single three-dimensional object designed for tactile interaction.'),
    ('Ritual in Motion', 'Hinges allow the viewer to open, turn, and engage during prayer.'),
    ('Active Exterior', 'The reverse floral painting is an integral layer of the sacred object.'),
], (960, 200, 850, 810), 38)
finish()

start(15, 'St. Ursula Shrine: A Story Told in the Round')
art('(p15-1) St. Ursula Shrine.jpg', (105, 200, 500, 650), 'St. Ursula Shrine', 30)
shrine = [
    ('(p15-2) Virgin and Child.jpg', 'Virgin and Child'),
    ('(p15-3) Arrival in Rome.jpg', 'Arrival in Rome'),
    ('(p15-4) Martyrdom.jpg', 'Martyrdom'),
    ('(p15-5) Arrival in Cologne.jpg', 'Arrival in Cologne'),
    ('(p15-6) St. Ursula shields the Holy Virgins beneath her cloak.png', 'St. Ursula shelters the Holy Virgins'),
]
for i, (name, label) in enumerate(shrine):
    art(name, (650+i*235, 210, 215, 640), label, 24)
description('A miniature Gothic chapel: move around the shrine to follow its story.', y=895, h=115, size=42)
finish()

start(16, 'A Shrine That Rewards Movement')
art('Shrine of St. Ursula.jpg', (140, 195, 770, 810), 'Shrine of St. Ursula', 38)
notes([
    ('Architecture in miniature', 'A Gothic structure frames the painted stories.'),
    ('A sequence of scenes', 'The narrative unfolds across several surfaces.'),
    ('An active viewer', 'Walk around the object to discover the whole.'),
], (980, 210, 810, 780), 40)
finish()

start(17, 'Memling’s Lasting Legacy', 'The Master of Calm')
art('St. John Altarpiece Mystic Marriage of St. Catherine.jpg',
    (330, 205, 1260, 800), 'Mystic Marriage of St. Catherine', 38)
finish()

start(18, 'A Booming Career, Shifting Critical Favor')
art('(p11) Portrait of a Man at a Loggia.jpg', (120, 200, 550, 800))
panel((730, 200, 1810, 410))
text('August 1494: Considerable Wealth', (765, 230, 1010, 75), 44)
text('He left a thriving workshop. His reputation would fluctuate over the next five centuries.',
     (765, 310, 1010, 100), 34)
reception = [
    ('15th century', 'In High Demand', 'Celebrated across Europe during his lifetime.'),
    ('19th century', 'Romantic Adoration', 'Admired for his quiet, gentle piety.'),
    ('20th century', 'Critical Dismissal', 'Sometimes overshadowed by predecessors with more dramatic styles.'),
]
for i, (era, heading, body) in enumerate(reception):
    x = 730+i*370
    panel((x, 460, x+340, 990))
    text(era, (x+25, 490, 290, 65), 32, MUTED)
    text(heading, (x+25, 585, 290, 120), 39)
    text(body, (x+25, 750, 290, 225), 32)
finish()

start(19, 'Precision with Purpose')
art('基督與奏樂歌唱的天使 Christ with Singing and Music-Making Angels.jpg',
    (110, 210, 1700, 510))
description('His precision served his clients’ needs;\nit did not limit his emotional range.', y=790, h=205, size=53)
finish()

start(20, 'What Do We Lose When Art Becomes a Flat Image?')
art('最後的審判三聯畫 The Last Judgment Triptych.jpg', (110, 260, 780, 640))
notes([
    ('Physical Context', 'Three-dimensional objects made for real architectural spaces.'),
    ('Hidden Backs & Outer Panels', 'Exterior paintings and coats of arms set the tone before opening.'),
    ('Hinges & Interactive Ritual', 'Opening, closing, and turning could form part of prayer.'),
], (950, 205, 860, 800), 38)
finish()

(SLIDES / 'layout' / 'revision_manifest.json').write_text(json.dumps({
    'size': SIZE, 'slides': MANIFEST, 'text_boxes': TEXT_BOXES,
    'source_notes': [
        'Requested background was absent from tw_slides; used the matching English background in en_slides.',
        'Slide 11 path corrected to en_slides/update/Hans_Memling_s_Conquest_slide_0011.png.',
        'Mislabeled (p12) image is St John Altarpiece; used Hans_Memling_Passione.jpg on slides 10–11.',
        'Truncated slide 14 sentence completed with: an integral layer of the sacred object.',
        'Artwork composited directly without generative changes.'
    ]}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for group in range(3):
    sheet = Image.new('RGB', (1440, 1160), '#e5e0d6')
    d = ImageDraw.Draw(sheet)
    for index, n in enumerate(range(2+group*7, min(9+group*7, 21))):
        im = Image.open(OUT / f'{PREFIX}_slide_{n:04d}.png')
        im.thumbnail((700, 260), Image.Resampling.LANCZOS)
        x, y = (index % 2)*720+10, (index // 2)*290+25
        sheet.paste(im, (x, y))
        d.text((x, y-20), f'{n:02d}', fill='black')
    sheet.save(SLIDES / 'layout' / f'review_{group+1}.jpg', quality=93)


