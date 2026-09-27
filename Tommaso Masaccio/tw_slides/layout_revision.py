"""Rebuild slides 02–20 from original artwork and the supplied background."""
from pathlib import Path
from datetime import datetime
import json
import re
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tw_slides' / 'update'
STAGE = ROOT / 'tw_slides' / 'layout_revision_rendered'
STAGE.mkdir(exist_ok=True)
ASSETS = ROOT / 'images'
S = 2
BG = Image.open(ROOT / 'en_slides' / 'Masaccio__Giving_Art_Weight_background.png').convert('RGB').resize((2560, 1440), Image.Resampling.LANCZOS)
INK = '#302c27'
ACCENT = '#85503a'
TEAL = '#316962'
CREAM = '#fffaf0'
FONT = 'C:/Windows/Fonts/msjh.ttc'
BOLD = 'C:/Windows/Fonts/msjhbd.ttc'
PREFIX = '馬薩喬：讓繪畫重新站在地面上_slide_'
records = []


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, int(size*S))


def rect(box, fill=CREAM, outline='#c9b59b', radius=12):
    d.rounded_rectangle(tuple(int(v*S) for v in box), radius=radius*S, fill=fill, outline=outline, width=2)


def text(value, box, size=25, bold=False, color=INK, align='left'):
    x, y, w, h = box
    f = font(size, bold)
    lines = []
    for paragraph in value.split('\n'):
        line = ''
        # Keep English words intact while permitting Chinese character wrapping.
        for token in re.findall(r'[A-Za-z0-9]+(?:[’\-][A-Za-z0-9]+)*|[^A-Za-z0-9]', paragraph):
            if line and d.textlength(line + token, font=f) > w*S:
                lines.append(line.rstrip())
                line = token.lstrip()
            else:
                line += token
        lines.append(line.rstrip())
    step = size * 1.42
    if len(lines)*step > h + 3:
        raise ValueError(f'Text overflows {box}: {value}')
    for i, line in enumerate(lines):
        xx = x*S
        if align == 'center':
            xx += (w*S-d.textlength(line, font=f))/2
        d.text((xx, (y+i*step)*S), line, font=f, fill=color, anchor='lt')


def artwork(name, box, frame=True, crop=None):
    x, y, w, h = box
    src = ImageOps.exif_transpose(Image.open(ASSETS/name)).convert('RGB')
    if crop:
        src = src.crop(tuple(int(v*(src.width if i%2==0 else src.height)) for i,v in enumerate(crop)))
    fit = ImageOps.contain(src, (int(w*S), int(h*S)), Image.Resampling.LANCZOS)
    px = int(x*S+(w*S-fit.width)/2)
    py = int(y*S+(h*S-fit.height)/2)
    if frame:
        d.rectangle((px-5, py-5, px+fit.width+5, py+fit.height+5), fill='#fffaf0', outline='#a88d6b', width=2)
    canvas.paste(fit, (px, py))


def start(n, title, subtitle=''):
    global canvas, d
    canvas = BG.copy()
    d = ImageDraw.Draw(canvas)
    rect((44, 28, 1236, 119), fill='#fff8eb', outline='#cfb899')
    text(title, (67, 42, 1146, 54), 35, True)
    if subtitle:
        text(subtitle, (69, 89, 1125, 27), 17, color=ACCENT)
    text('馬薩喬｜讓繪畫重新站在地面上', (52, 686, 600, 25), 14, color='#675648')
    text(f'{n:02d}', (1177, 683, 50, 29), 18, color=ACCENT, align='center')
    records.append({'slide': n, 'title': title})


def card(heading, body, box, size=25):
    x, y, w, h = box
    rect((x, y, x+w, y+h))
    text(heading, (x+21, y+17, w-42, 46), 27, True, TEAL)
    text(body, (x+21, y+66, w-42, h-77), size)


def caption(value, box, size=20):
    text(value, box, size, color=ACCENT, align='center')


def arrow(x1, y1, x2, y2):
    d.line((x1*S,y1*S,x2*S,y2*S), fill=ACCENT, width=4*S)
    if x2>x1:
        d.polygon(((x2*S,y2*S),((x2-10)*S,(y2-7)*S),((x2-10)*S,(y2+7)*S)), fill=ACCENT)
    else:
        d.polygon(((x2*S,y2*S),((x2-7)*S,(y2-10)*S),((x2+7)*S,(y2-10)*S)), fill=ACCENT)


def save(n):
    canvas.resize((1280,720), Image.Resampling.LANCZOS).save(STAGE/f'{PREFIX}{n:04d}.png')


existing_backups = sorted((ROOT/'tw_slides').glob('backup_before_layout_*'))
backup = existing_backups[0] if existing_backups else ROOT/'tw_slides'/('backup_before_layout_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
if not backup.exists():
    backup.mkdir()
    for n in range(2,21):
        shutil.copy2(OUT/f'{PREFIX}{n:04d}.png', backup)

start(2, '從優雅輪廓，到有重量的身體', '同一座禮拜堂裡，兩位畫家如何表現亞當與夏娃？')
for x in (54,650):
    rect((x,135,x+576,668))
artwork('Temptation of Adam and Eve by Masolino da Panicale.jpg',(80,145,525,380))
artwork('Expulsion from the Garden of Eden.jpg',(675,145,527,380))
caption('Temptation of Adam and Eve\n(Masolino da Panicale)',(78,537,530,65),21)
caption('Expulsion from the Garden of Eden\n(Masaccio)',(673,537,530,65),21)
text('姿態平靜、輪廓柔和，呈現優雅的身體。',(78,614,530,43),22)
text('踏地步伐、明暗與表情，強化重量與悲痛。',(673,614,530,43),22)
save(2)

start(3,'觀看馬薩喬的六條線索','從身體、空間與敘事，走進早期文藝復興')
rect((54,141,344,665))
artwork('Masaccio-book.png',(70,169,258,376))
caption('Masaccio\nPaintings (Annotated)',(70,561,258,73),21)
items=[('會投下陰影的身體','從光影與步伐，感受身體重量。'),('佛羅倫斯的視覺革命','人體與幾何，改變空間的表現。'),('一個空間，三個時刻','沿著手勢，讀懂連續敘事。'),('金地祭壇畫的突破','傳統形式中，建立立體量感。'),('牆壁裡的禮拜堂','用線性透視，打開畫中深度。'),('如何觀看馬薩喬','腳步、光源、空間與手勢。')]
for i,(head,body) in enumerate(items):
    x=369+(i%2)*438; y=143+(i//2)*177
    card(f'{i+1:02d}  {head}',body,(x,y,413,159),22)
save(3)

start(4,'會投下陰影的身體','光有方向，人物也有可以感受的重量')
artwork('shadow.image.png',(71,142,465,494))
caption('聖彼得以影子治癒病人｜局部',(65,644,477,30),18)
card('光線塑造身體','臉部、衣褶與肢體的明暗，\n讓人物產生立體量感。',(585,163,620,185),27)
card('身體進入真實街道','腳步、地面與人物的相對位置，\n把宗教故事帶入可感的空間。',(585,371,620,208),27)
text('觀察重點：光從哪裡來？人物如何站立？',(600,610,600,47),24,True,ACCENT)
save(4)

start(5,'逐出伊甸園：悲痛也有重量','Expulsion from the Garden of Eden — Masaccio')
artwork('Expulsion from the Garden of Eden.jpg',(73,137,386,535))
card('明暗，塑造肉身','強烈而有方向的光線，\n讓軀幹與四肢呈現體積。',(507,146,694,151),25)
card('腳步，承受重量','雙腳接觸地面，陰影延伸，\n使前行的動作變得具體。',(507,316,694,151),25)
card('姿態，傳達悲痛','亞當掩面，夏娃仰頭哭喊；\n失落透過身體與表情被看見。',(507,486,694,166),25)
save(5)

start(6,'佛羅倫斯的視覺革命','布蘭卡契禮拜堂：繪畫、建築與真實光線相遇')
artwork('Brancacci Kapelle (Gesamtansicht), S.Maria del Carmine, Florenz.JPG',(65,148,626,466))
caption('Brancacci Chapel｜Santa Maria del Carmine, Florence',(67,630,622,38),18)
card('壁畫屬於一個空間','牆面位置、窗戶的光線，\n以及觀者的移動，\n共同影響我們如何看畫。',(730,153,481,239),25)
card('跨越年代的合作','馬索利諾與馬薩喬參與繪製，\n未完成的部分，後來由\n菲利皮諾・利皮接續。',(730,414,481,234),24)
save(6)

start(7,'短暫一生，持續探索','從聖喬瓦尼瓦爾達諾，到佛羅倫斯與羅馬')
rect((56,144,325,667))
artwork('Masaccio.jpg',(76,168,229,364))
caption('Masaccio',(77,552,226,40),25)
caption('1401—約 1428',(76,603,229,32),19)
timeline=[('1401','出生','生於聖喬瓦尼瓦爾達諾。'),('1422','早期作品','留下有紀年的聖朱維納爾三聯畫。'),('1426','比薩委託','受託繪製比薩多聯祭壇畫。'),('約 1428','羅馬與早逝','在羅馬去世；確切日期與死因不明。')]
for i,(date,head,body) in enumerate(timeline):
    y=150+i*129
    rect((364,y,1199,y+111))
    text(date,(384,y+24,181,48),30,True,ACCENT)
    text(head,(579,y+12,590,39),25,True,TEAL)
    text(body,(579,y+57,590,47),23)
    if i<3: arrow(445,y+114,445,y+126)
save(7)

start(8,'一個空間內的三個時刻','Masaccio Continuous Narrative')
artwork('The Tribute Money.jpg',(76,143,1128,315))
steps=[('中央｜吩咐','基督指示彼得前往湖邊。'),('左側｜取錢','彼得從魚口取出錢幣。'),('右側｜繳納','彼得把錢交給收稅人。')]
for i,(head,body) in enumerate(steps):
    card(head,body,(64+i*408,486,369,152),23)
    if i<2: arrow(439+i*408,560,462+i*408,560)
save(8)

start(9,'納稅銀：用光影塑造群像','The Tribute Money — Masaccio')
artwork('The Tribute Money.jpg',(80,139,1120,367))
card('明暗形成量體','衣褶、臉部與肢體，\n呈現如雕塑般的體積。',(65,524,365,140),22)
card('光線統一空間','一致的受光與投影，\n把人物連成同一個世界。',(456,524,365,140),22)
card('手勢連接敘事','基督與彼得的指向，\n引導我們閱讀不同時刻。',(847,524,365,140),22)
save(9)

start(10,'納稅銀：風景連接不同時刻','先看完整壁畫，再看湖邊彼得的動作')
artwork('The Tribute Money.jpg',(70,135,1140,325))
artwork('Peter.png',(79,484,295,174))
card('左側細節｜彼得從魚口取錢','彼得在湖邊俯身，與遠山、水岸相連。\n遠景較淡的色調加深空間感，\n讓三個時刻共存於連續的風景裡。',(412,476,790,187),24)
save(10)

start(11,'金地祭壇畫的突破','在傳統形式裡，發展身體與空間的真實感')
artwork('Altar in Roskilde Lutheran Cathedral.jpg',(65,148,633,421))
caption('Roskilde Cathedral｜多聯祭壇的形式示例',(66,587,631,31),20)
caption('此圖並非馬薩喬的比薩祭壇畫。',(68,628,627,30),19)
card('多聯祭壇的觀看方式','多塊圖像依照位置與層次排列，\n形成一個完整的宗教敘事。',(732,151,479,211),24)
card('馬薩喬的探索','在比薩祭壇畫中，金地與\n傳統外框仍在；身體量感與\n觀看角度卻成為重要實驗。',(732,386,479,253),24)
save(11)

start(12,'為仰視而設計的身體','Crucifixion (1426)')
artwork('IMG-010 Masaccio《耶穌受難》（比薩祭壇畫）.jpg',(71,140,493,526))
card('原本位於祭壇上層','觀者從下方向上看，\n這個位置影響人物的造形。',(615,160,586,170),26)
card('透視縮短，回應視角','基督頭部與軀幹的比例，\n須結合原來的觀看高度理解。',(615,351,586,170),26)
text('抹大拉高舉雙臂，將悲痛集中於十字架下。',(632,558,551,100),27,True,ACCENT)
save(12)

start(13,'金地之中，兩種身體與空間','從國際哥德式的精緻優雅，到馬薩喬的量體探索')
rect((55,140,626,666)); rect((652,140,1224,666))
artwork('The Wilton Diptych (tradtional Gothic).jpg',(71,154,539,370))
artwork('IMG-009 Masaccio《聖母子》（比薩祭壇畫）.jpg',(668,154,539,370))
caption('The Wilton Diptych',(76,540,529,40),25)
caption('Madonna and Child',(673,540,529,40),25)
text('金地、精緻線條與優雅姿態，\n營造莊嚴而理想化的聖域。',(79,590,521,70),23)
text('身體量感、寶座深度與傾斜光環，\n讓人物佔有可感的立體空間。',(676,590,522,70),23)
save(13)

start(14,'牆壁裡的禮拜堂','新聖母大殿與馬薩喬的聖三位一體')
artwork('Santa Maria Novella.jpg',(66,155,654,431))
caption('Basilica of Santa Maria Novella',(67,610,651,39),24)
card('佛羅倫斯｜新聖母大殿','聖三位一體繪於教堂內的牆面，\n以建築透視創造向內延伸的深度。',(755,162,458,219),24)
card('從外部走入畫中','接著觀察拱頂、柱列與人物，\n看平坦牆面如何呈現\n一座彷彿可進入的禮拜堂。',(755,408,458,231),24)
save(14)

start(15,'聖三位一體：把牆面打開','The Holy Trinity — Masaccio')
artwork('The Holy Trinity.jpg',(61,132,514,506),crop=(0,0,1,0.76))
caption('上部細節｜下方骷髏見下一頁',(65,649,505,28),18)
card('線性透視創造深度','拱頂與建築線條向消失點匯聚，\n讓畫中空間與觀者的位置相連。',(624,145,585,160),24)
card('人物共享建築尺度','捐贈者與神聖人物的比例相近，\n使他們進入同一個可信的空間。',(624,322,585,160),24)
card('構圖仍有層次','空間比例的統一，並不表示\n宗教身分與構圖層級完全消失。',(624,499,585,160),24)
save(15)

start(16,'向下看：死亡的提醒','聖三位一體下方的骷髏與銘文')
artwork('The Holy Trinity bottom.png',(122,138,1036,303))
rect((118,458,1162,580))
text('「我曾經是你現在的樣子；\n你也將成為我現在的樣子。」',(143,477,994,97),30,True,align='center')
text('銘文意譯｜從死亡的提醒，向上觀看十字架與救贖的希望。',(125,611,1031,42),24,align='center')
save(16)

start(17,'如何觀看馬薩喬','從腳步、光源、空間與手勢，讀懂畫中的人')
artwork('The Distribution of Alms and the Death of Ananias.jpg',(63,140,638,439))
caption('The Distribution of Alms\nand the Death of Ananias',(68,594,628,67),22)
card('先看身體如何站立','人物與地面接觸，\n在街道中形成前後層次。',(746,152,463,204),25)
card('再看人物如何互動','手勢、視線與群體位置，\n讓施捨與死亡的事件\n發生在同一個社群之中。',(746,381,463,258),25)
save(17)

start(18,'四個步驟，讀懂畫面','從具體的視覺線索，走向故事與情感')
flow=[('01','看腳步','雙腳如何接觸地面？\n身體重心落在哪裡？'),('02','找光源','哪一側受到光照？\n陰影方向是否一致？'),('03','讀空間','沿建築線找消失點，\n辨認觀者的位置。'),('04','看手勢','連起視線與動作，\n讀懂人物間的故事。')]
for i,(num,head,body) in enumerate(flow):
    x=57+i*307
    rect((x,203,x+273,516))
    text(num,(x+23,226,220,67),44,True,ACCENT)
    text(head,(x+23,312,229,46),29,True,TEAL)
    text(body,(x+23,388,229,110),23)
    if i<3: arrow(x+279,359,x+302,359)
rect((155,563,1125,647))
text('身體的重量 ＋ 可信的空間 ＋ 可讀的動作 ＝ 可以感受的故事',(177,587,926,44),24,True,align='center')
save(18)

start(19,'今天所見，也包含修復的歷史','聖三位一體：遮蔽、搬移與重新發現')
artwork('The Holy Trinity.jpg',(68,137,364,537))
history=[('1570 年','瓦薩里設置的祭壇與畫作，遮蔽了壁畫。'),('十九世紀','上部重新顯露，後被揭取，移到教堂內另一處。'),('1952 年','下方骷髏部分重新被發現，促成上下構圖的復原。')]
for i,(date,body) in enumerate(history):
    card(date,body,(476,149+i*171,724,153),24)
save(19)

start(20,'短暫的一生，留下長久的提問','如果馬薩喬活得更久，繪畫會走向何方？')
artwork('The Death of Masaccio, 1817, by Auguste Couder.jpg',(65,141,492,470))
caption('The Death of Masaccio\nAuguste Couder, 1817',(68,620,488,53),18)
card('二十多歲，生命驟然停下','馬薩喬約於 1428 年在羅馬去世，\n確切日期與死因仍不明。',(608,155,598,174),25)
card('十九世紀的回望','庫德的畫作是後世對其死亡的想像，\n並非事件現場的紀錄。',(608,351,598,166),25)
text('他留下的光影、身體與空間，\n至今仍改變我們觀看繪畫的方式。',(630,550,550,101),27,True,TEAL)
save(20)

# A review sheet makes every deliverable easy to inspect together.
for n in range(2,21):
    source = STAGE/f'{PREFIX}{n:04d}.png'
    with Image.open(source) as checked:
        checked.load()
        assert checked.size == (1280,720)
    source.replace(OUT/source.name)
sheet=Image.new('RGB',(1280,5*206),'#e7e0d5')
sd=ImageDraw.Draw(sheet)
for i,n in enumerate(range(2,21)):
    thumb=Image.open(OUT/f'{PREFIX}{n:04d}.png').resize((312,176),Image.Resampling.LANCZOS)
    x=(i%4)*320+4; y=(i//4)*206
    sheet.paste(thumb,(x,y+24))
    sd.text((x+4,y+3),f'Slide {n:02d}',font=ImageFont.truetype(FONT,16),fill=INK)
sheet.save(ROOT/'tw_slides'/'layout_revision_contact.jpg',quality=94)
(ROOT/'tw_slides'/'layout_revision_manifest.json').write_text(json.dumps({'background':str(ROOT/'en_slides'/'Masaccio__Giving_Art_Weight_background.png'),'backup':str(backup),'size':[1280,720],'slides':records},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Updated {len(records)} slides. Backup: {backup}')
