"""Render requested Traditional Chinese slide revisions with original artwork."""
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'images'
OUT = ROOT / 'tw_slides' / 'update'
W, H = 1920, 1080
NAVY = '#233540'
GOLD = '#a87a3e'
IVORY = '#faf5e9'
FONT = '/System/Library/Fonts/STHeiti Medium.ttc'
BACKGROUND = Image.open(ASSETS / 'background/high_renaissance_light.jpg').convert('RGB').resize((W, H), Image.Resampling.LANCZOS)
SLIDES = {}

def font(size):
    return ImageFont.truetype(FONT, size)

def text(im, value, x, y, size=36, width=1600, color=NAVY, leading=1.35):
    draw = ImageDraw.Draw(im)
    f = font(size)
    for paragraph in value.split('\n'):
        line = ''
        for char in paragraph:
            if draw.textlength(line + char, font=f) > width and line and char not in '，。；：！？、）』」':
                draw.text((x, y), line, font=f, fill=color)
                y += int(size * leading)
                line = ''
            line += char
        draw.text((x, y), line, font=f, fill=color)
        y += int(size * leading)
    assert y <= H - 20, (value, y)
    return y

def panel(im, box, fill=IVORY):
    ImageDraw.Draw(im).rounded_rectangle(box, radius=22, fill=fill, outline='#c6ad83', width=2)

def photo(im, name, box, crop=None, cover=False):
    src = Image.open(ASSETS / name).convert('RGB')
    if crop:
        src = src.crop(crop)
    x, y, r, b = box
    panel(im, (x - 8, y - 8, r + 8, b + 8))
    src = (ImageOps.fit if cover else ImageOps.contain)(src, (r - x, b - y), Image.Resampling.LANCZOS)
    im.paste(src, (x + (r - x - src.width) // 2, y + (b - y - src.height) // 2))

def slide(n, title, subtitle=''):
    im = BACKGROUND.copy()
    panel(im, (100, 62, 1820, 200))
    text(im, title, 132, 83, 54, 1640)
    if subtitle:
        text(im, subtitle, 135, 150, 26, 1630, GOLD)
    text(im, '西斯汀禮拜堂天頂畫  ·  米開朗基羅', 120, 1017, 24, 1500, IVORY)
    SLIDES[n] = im
    return im

def description(im, title, body, box=(1120, 270, 1810, 950)):
    panel(im, box)
    x, y, r, b = box
    compact = b - y < 250
    end = text(im, title, x + 32, y + 20, 32 if compact else 40, r - x - 64, GOLD)
    body_size = 29 if compact else (30 if r - x < 420 else 35)
    end = text(im, body, x + 32, end + (12 if compact else 25), body_size, r - x - 64, leading=1.35 if compact else 1.55)
    assert end < b - 15, (title, end, b)

def wide(n, title, asset, line1, line2='', crop=None):
    im = slide(n, title)
    photo(im, asset, (130, 235, 1790, 815), crop)
    panel(im, (120, 855, 1800, 989))
    text(im, line1, 155, 875, 37, 1600)
    if line2:
        text(im, line2, 155, 932, 29, 1600, GOLD)
    return im

def render():
    im = slide(2, '九幅中央場景｜三組主題，讀懂創世故事', '以下由祭壇端往入口端排列；畫面位置不完全等於事件順序。')
    titles = ['分離光與暗', '創造日月與植物', '水陸分離', '創造亞當', '創造夏娃', '原罪與逐出伊甸園', '諾亞獻祭', '大洪水', '諾亞醉酒']
    scenes = sorted((ASSETS / '9 central view').iterdir())
    groups = ['宇宙的創造', '人類的創造與墮落', '諾亞的故事']
    for row in range(3):
        y = 220 + row * 255
        panel(im, (120, y, 1800, y + 240))
        text(im, groups[row], 145, y + 10, 30, 1600, GOLD)
        for col in range(3):
            idx = row * 3 + col
            x = 145 + col * 555
            photo(im, str(scenes[idx].relative_to(ASSETS)), (x, y + 56, x + 510, y + 180), cover=True)
            text(im, titles[idx], x + 5, y + 195, 28, 510)
    wide(3, '創造亞當｜生命懸在指尖之間', 'Creation of Adam.jpg', '上帝主動伸手；亞當的手腕仍然低垂。', '兩指尚未相碰，讓生命即將甦醒的期待，停留在永恆的瞬間。')
    wide(4, '把指尖放回整片天頂', 'IMG-001西斯汀禮拜堂天頂全景_horizantal.png', '創造亞當只是整體的一部分：創世、墮落與救贖的盼望彼此呼應。', '人物的姿態與畫出的建築框架，共同組織這個宏大的視覺世界。')
    im = slide(5, '看懂天頂畫的五條線索')
    photo(im, 'IMG-001西斯汀禮拜堂天頂全景.jpg', (135, 235, 475, 965))
    items = [('雕塑家的挑戰', '教宗的委託，如何改變他的創作？'), ('解構穹頂', '畫出的梁柱，如何建立空間秩序？'), ('身體與時間', '肌肉、重心與手勢，如何推動故事？'), ('畫框之外', '先知、西比拉與青年，如何呼應中央場景？'), ('活著的傑作', '歷史、修復與今日的觀看，如何交會？')]
    for i, (title, body) in enumerate(items):
        y = 232 + i * 150
        panel(im, (530, y, 1795, y + 130))
        text(im, title, 565, y + 17, 39, 1150, GOLD)
        text(im, body, 565, y + 77, 31, 1150)
    im = slide(6, '雕塑家的挑戰', '從大理石到濕壁畫：教宗儒略二世的天頂委託')
    photo(im, 'Michelangelo di Lodovico.jpg', (140, 250, 780, 960))
    description(im, '1508年，一場新的考驗', '以雕塑聞名的米開朗基羅，\n接下裝飾弧形天頂的任務。\n\n他必須用色彩塑造體積，\n並駕馭高處的巨大畫面。', (850, 270, 1790, 920))
    im = slide(7, '教宗的委託與雕塑家的身分', '1508年，儒略二世委託33歲的米開朗基羅繪製天頂。')
    photo(im, 'Pope_Julius_II.jpg', (145, 250, 645, 790))
    photo(im, 'David.jpg', (700, 250, 1175, 790))
    panel(im, (135, 835, 1185, 960))
    text(im, 'Pope Julius II', 165, 866, 35, 490)
    text(im, 'David', 735, 866, 35, 400)
    description(im, '從鑿刀轉向畫筆', '大衛像已展現他的雕塑成就。\n\n天頂畫則要求他掌握濕壁畫：\n趁灰泥未乾完成預定區域，\n讓色彩與牆面結合。', (1230, 260, 1790, 970))
    im = slide(8, '站在鷹架上，仰頭作畫', '主要工作姿勢是站立仰頭，而非平躺。')
    photo(im, 'The Agony and the Ecstasy, Twentieth Century Fox.png', (140, 255, 1120, 845))
    panel(im, (130, 875, 1130, 970))
    text(im, 'The Agony and the Ecstasy · Twentieth Century Fox', 155, 899, 26, 950)
    description(im, '傑作背後的身體代價', '長時間仰頭、抬臂，\n讓頸背承受極大負擔。\n\n他曾以自嘲的詩與速寫，\n描述顏料滴落臉上的痛苦。\n\n電影畫面是戲劇再現。', (1180, 250, 1790, 965))
    im = slide(9, '解構穹頂｜從星空到創世世界')
    photo(im, 'The ceiling as it may have looked before Michelangelo painted it.jpg', (135, 255, 1100, 850))
    panel(im, (130, 875, 1105, 970))
    text(im, 'Ceiling before｜原天頂的可能樣貌', 160, 900, 33, 930)
    description(im, '畫出的空間秩序', '原天頂是綴滿星辰的藍色天空。\n\n米開朗基羅以虛擬梁柱、\n壁柱與簷口劃分畫面，\n讓故事與人物各有位置。', (1160, 260, 1790, 970))
    im = slide(10, '中央九幅畫｜主題與空間位置', '從入口走向祭壇，整體觀看方向是向創世源頭回溯。')
    photo(im, 'the.9.png', (145, 235, 390, 970))
    x, y = 470, 270
    rows = [('主題', '位置'), ('宇宙的創造', '靠近祭壇端'), ('人類的創造與墮落', '天頂中段'), ('諾亞的故事', '靠近入口端')]
    for i, (a, b) in enumerate(rows):
        yy = y + i * 130
        panel(im, (x, yy, 1785, yy + 115), '#e6dbc6' if i == 0 else IVORY)
        text(im, a, x + 32, yy + 32, 38, 770)
        text(im, b, 1340, yy + 32, 38, 420)
    description(im, '觀看方向 ≠ 故事時間線', '個別場景並非完全按事件先後排列；施工大致從入口端向祭壇端推進。', (465, 825, 1790, 975))
    im = slide(11, '天頂布局｜中央故事與周邊人物相互呼應')
    photo(im, 'Plan of the pictorial elements of the ceiling showing the division of the narrative scenes into three-part themes.png', (125, 225, 1795, 855))
    panel(im, (120, 895, 1800, 988))
    text(im, '中央：創世記九景　｜　周邊：先知、西比拉、基督祖先與角隅拯救故事', 150, 921, 33, 1610)
    im = slide(12, '身體與時間', '肌肉、重心與手勢，讓靜止的壁畫充滿敘事張力。')
    photo(im, 'IMG-002 創造亞當.jpg', (140, 260, 1160, 865))
    description(im, '姿態推動故事', '伸展、扭轉與重心的轉移，\n讓人物顯得有重量。\n\n動作尚未完成，\n觀眾卻已感到下一刻\n即將發生。', (1220, 260, 1790, 945))
    im = slide(13, '兩種甦醒的姿態｜亞當與夏娃')
    photo(im, 'p12.left.jpg', (135, 250, 910, 760))
    photo(im, 'p.12.right.jpg', (1000, 250, 1785, 760))
    for box, label, body in [((125, 810, 920, 975), 'Creation of Adam', '橫向舒展、手腕低垂：等待生命喚醒。'), ((990, 810, 1795, 975), 'Creation of Eve', '向上挺起、雙手合十：敬畏地回應上帝。')]:
        panel(im, box)
        text(im, label, box[0] + 25, 830, 39, 730, GOLD)
        text(im, body, box[0] + 25, 902, 29, 750)
    wide(14, '原罪與逐出伊甸園｜一個畫框，兩個時刻', 'The Fall and Expulsion from Paradise.jpg', '左側：伸手接近誘惑。　右側：抵擋、退縮，承受被逐的痛苦。', '同一對人物出現兩次；目光由左向右移動，故事的時間也隨之推進。')
    im = slide(15, '畫框之外｜周邊人物也在說故事')
    photo(im, 'Sistine Chapel Ceiling 2.jpg', (140, 245, 880, 970))
    description(im, '向外延伸的視覺世界', '先知與西比拉閱讀、沉思、轉身，\n呼應救主降臨的盼望。\n\n框架邊緣的裸體青年，\n以不同姿態帶出力量與節奏。\n\n他們讓中央場景與周邊空間\n連成完整的天頂。', (960, 260, 1790, 970))
    im = slide(16, '利比亞西比拉｜從人體研究到壁畫')
    photo(im, 'Studies for the Libyan Sibyl.jpg', (135, 250, 700, 970))
    photo(im, 'The Libyan Sibyl.jpg', (770, 250, 1210, 865))
    description(im, '雕塑家的眼光', '紅粉筆習作研究\n肩背、軀幹的扭轉。\n\n以男性模特兒研究人體，\n再轉化為女預言者的姿態。\n\n承重與平衡，\n使人物顯得立體而有力。', (1260, 250, 1790, 970))
    wide(17, '大洪水｜災難中的恐懼與扶持', 'IMG-005 大洪水.jpg', '有人奔向高地，有人爭奪船位，也有人背負、扶持身旁的人。', '密集的人群讓目光不斷移動；求生、脆弱與牽掛，並存於同一場災難。')
    wide(18, '活著的傑作｜重新仰望整片天頂', 'IMG-001西斯汀禮拜堂天頂全景_horizantal.png', '從16世紀到今天，人物、色彩與構圖仍牽動我們的目光。', '走過故事與細節，再看整體：創造、掙扎與救贖的盼望彼此相連。')
    im = slide(19, '西斯汀禮拜堂｜藝術、信仰與儀式交會')
    assets = [('Sistine Chapel.jpg', '禮拜堂外觀'), ('Scrutiny during the conclave of 1903.jpg', '1903年秘密會議：檢視選票'), ('Illustration of the burning of ballots (1939).jpg', '1939年插圖：焚燒選票'), ('White smoke in the Sistine Chapel, indicating that a pope has been elected by the College of Cardinals.jpg', '白煙：新教宗已選出')]
    for i, (name, label) in enumerate(assets):
        x = 140 + (i % 2) * 630
        y = 240 + (i // 2) * 360
        photo(im, name, (x, y, x + 570, y + 280))
        panel(im, (x - 8, y + 300, x + 578, y + 345))
        text(im, label, x + 8, y + 307, 26, 548)
    description(im, '延續至今的場所', '樞機主教在此投票，\n選出新任教宗。\n\n仰望天頂的創世故事，\n再看祭壇後方的\n最後的審判。\n\n兩個時期的作品，\n在同一空間中呼應。', (1430, 250, 1790, 970))
    im = slide(20, '從創作到修復｜重新看見色彩')
    milestones = [('1508年', '接受委託', '儒略二世委託米開朗基羅\n重新裝飾天頂。'), ('1512年', '天頂畫完成', '歷經約四年的工程，\n創世故事展開於穹頂。'), ('20世紀末', '修復與重新發現', '清除積塵與覆蓋物，\n鮮明色彩重新顯現。')]
    for i, (year, label, body) in enumerate(milestones):
        x = 135 + i * 575
        panel(im, (x, 280, x + 500, 680))
        text(im, year, x + 30, 315, 52, 440, GOLD)
        text(im, label, x + 30, 413, 37, 440)
        text(im, body, x + 30, 505, 31, 440)
        if i < 2:
            text(im, '→', x + 512, 433, 50, 60)
    description(im, '線條、體積與色彩共同塑造天頂的力量', '修復讓明亮的粉紅、綠與藍重新受到注目；清理是否影響原有表面細節，也曾引發爭論。', (130, 745, 1790, 965))
    wide(21, '從兩根手指，看見一個宏大的世界', 'Creation of Adam.jpg', '指尖之間的期待，連接著整片天頂中的生命、恐懼、愛與盼望。', '下次再看見創造亞當，試著把目光拉遠，重新看見它所屬的世界。')

def main():
    render()
    backup = Path('/private/tmp/sistine-tw-slides-before-revision')
    backup.mkdir(exist_ok=True)
    for n, im in sorted(SLIDES.items()):
        suffix = '006' if n == 6 else f'{n:04d}'
        path = OUT / f'解碼西斯汀禮拜堂天頂畫_slide_{suffix}.png'
        if not (backup / path.name).exists():
            shutil.copy2(path, backup / path.name)
        im.save(path)
    sheet = Image.new('RGB', (1920, 1080), '#17232b')
    for i, (n, im) in enumerate(sorted(SLIDES.items())):
        thumb = im.resize((384, 216), Image.Resampling.LANCZOS)
        x, y = (i % 5) * 384, (i // 5) * 270
        sheet.paste(thumb, (x, y))
        text(sheet, f'{n:02d}', x + 12, y + 218, 22, 350, IVORY)
    sheet.save(ROOT / 'tw_slides' / 'requested_slides_review.png')
    print(f'Saved {len(SLIDES)} slides and review sheet; backup: {backup}')

if __name__ == '__main__':
    main()
