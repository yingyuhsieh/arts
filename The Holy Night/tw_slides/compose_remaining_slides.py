"""Compose slides 4, 6 and 19 using original artwork pixels and readable type."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT.parent / 'images'
PREFIX = '藝術解析：科雷喬《聖夜》'
GOLD = '#946321'
INK = '#29221D'
CREAM = '#FFF6E6'
SIZE = (1920, 1080)


def font(size, title=False, english=False):
    if english:
        return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size)
    path = '/System/Library/Fonts/Supplemental/Songti.ttc' if title else '/System/Library/Fonts/STHeiti Medium.ttc'
    return ImageFont.truetype(path, size, index=2 if title else 0)


def base():
    return Image.open(ROOT / f'{PREFIX}_background.png').convert('RGB').resize(SIZE, Image.Resampling.LANCZOS)


def panel(im, box):
    overlay = Image.new('RGBA', SIZE)
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(box, radius=24, fill=(255, 247, 232, 244), outline=GOLD, width=3)
    im.paste(Image.alpha_composite(im.convert('RGBA'), overlay).convert('RGB'))


def text(im, xy, value, size, color=INK, title=False, center=False, english=False):
    d = ImageDraw.Draw(im)
    f = font(size, title, english)
    assert d.textbbox((0, 0), value, font=f)[2] <= 1800, value
    d.text(xy, value, font=f, fill=color, anchor='mt' if center else 'lt')


def picture(im, name, box, crop=False):
    source = Image.open(IMAGES / name).convert('RGB')
    x, y, right, bottom = box
    size = (right-x, bottom-y)
    art = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS) if crop else ImageOps.contain(source, size, method=Image.Resampling.LANCZOS)
    px, py = x+(size[0]-art.width)//2, y+(size[1]-art.height)//2
    im.paste(art, (px, py))
    ImageDraw.Draw(im).rectangle((px-2, py-2, px+art.width+1, py+art.height+1), outline=GOLD, width=3)


def heading(im, value):
    panel(im, (150, 50, 1770, 195))
    text(im, (960, 79), value, 82, title=True, center=True)


def save(im, number):
    path = ROOT / 'update' / f'{PREFIX}_slide_{number:04d}.png'
    im.save(path)
    print(path.name, im.size)


def slide_four():
    im = base()
    heading(im, '跟著光，看懂《聖夜》')
    cards = [
        ('(p3) glowing.png', '先找光的中心', ['聖嬰是整個畫面', '最強的亮度中心']),
        ('(p11) 1 maria.png', '沿光看瑪利亞', ['留意由下方照亮', '聖母面容的光']),
        ('(p10) lady-shine.png', '找到遮眼女子', ['她的動作，讓強光', '成為可感受的強度']),
    ]
    for i, (name, title, lines) in enumerate(cards):
        x = 70+i*610
        panel(im, (x, 240, x+560, 1010))
        picture(im, name, (x+25, 270, x+535, 680))
        text(im, (x+280, 718), title, 64, color=GOLD, title=True, center=True)
        for j, line in enumerate(lines):
            text(im, (x+280, 822+j*70), line, 48, center=True)
    d = ImageDraw.Draw(im)
    for x in [630, 1240]:
        d.polygon([(x-10, 452), (x+30, 452), (x+30, 430), (x+64, 480), (x+30, 530), (x+30, 508), (x-10, 508)], fill=GOLD)
    save(im, 4)


def slide_six():
    im = base()
    panel(im, (65, 130, 1190, 970))
    picture(im, '(p6) The Assumption of the Virgin (1526-1530).jpg', (90, 165, 1165, 835))
    text(im, (628, 870), 'Assumption of the Virgin (1526-1530)', 48, center=True, english=True)
    panel(im, (1220, 240, 1855, 875))
    text(im, (1537, 309), '漩渦式的', 86, title=True, center=True)
    text(im, (1537, 421), '視覺導引', 98, color=GOLD, title=True, center=True)
    ImageDraw.Draw(im).line((1300, 568, 1775, 568), fill=GOLD, width=3)
    text(im, (1537, 620), '以光為軸心的', 62, center=True)
    text(im, (1537, 710), '旋轉空間', 72, center=True)
    save(im, 6)


def slide_nineteen():
    im = base()
    heading(im, '分辨三個亮度區域')
    cards = [
        ('(p3) glowing.png', '聖嬰', '集中亮光', ['照亮近旁肌膚', '與衣褶']),
        ('(p19) angels.png', '雲端', '柔和亮度', ['呈現天使', '與天界空間']),
        ('(p19) sky.png', '遠景', '微亮天際', ['建立夜景的', '空間深度']),
    ]
    for i, (name, title, sub, lines) in enumerate(cards):
        x = 70+i*610
        panel(im, (x, 235, x+560, 904))
        picture(im, name, (x+22, 257, x+538, 590))
        text(im, (x+280, 622), title, 70, color=GOLD, title=True, center=True)
        text(im, (x+280, 712), sub, 54, center=True)
        for j, line in enumerate(lines):
            text(im, (x+280, 789+j*51), line, 43, center=True)
    panel(im, (155, 940, 1765, 1032))
    text(im, (960, 962), '三個亮區是觀看分析，不代表三盞實體燈。', 48, center=True)
    save(im, 19)


if __name__ == '__main__':
    slide_four()
    slide_six()
    slide_nineteen()
    path = ROOT / 'slide_redesign_prompts.json'
    data = json.loads(path.read_text())
    data['mode'] = 'built-in image_gen; user-authorized Pillow compositing for slides 4, 6, 19'
    data['completed_slides'] = list(range(2, 21))
    data['pending_slides'] = []
    data['composited_slides'] = [4, 6, 19]
    data['composition_script'] = 'compose_remaining_slides.py'
    note = 'Slides 4, 6, 19 use original artwork files composited at 1920 × 1080 without AI repainting.'
    if note not in data['notes']:
        data['notes'].append(note)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
