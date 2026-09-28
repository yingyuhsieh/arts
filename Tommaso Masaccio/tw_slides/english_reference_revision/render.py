"""Traditional Chinese slides aligned by topic to the revised English set.

Original artwork is composited directly, without repainting or cropping.
"""
from pathlib import Path
from datetime import datetime
import json
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'tw_slides/update'
WORK = Path(__file__).resolve().parent
PREFIX = '馬薩喬：讓繪畫重新站在地面上_slide_'
S = 2
SIZE = (1672, 941)
FONT = '/System/Library/Fonts/Supplemental/Songti.ttc'
INK = '#29231e'
ACCENT = '#985535'
BG = Image.open(ROOT / 'en_slides/Masaccio__Giving_Art_Weight_background.png').convert('RGB').resize((2560, 1440), Image.Resampling.LANCZOS)
records = []


def text(value, box, size=25, bold=False, center=False, color=INK):
    x, y, w, h = box
    f = ImageFont.truetype(FONT, size * S, index=2 if bold else 7)
    lines = []
    for para in value.split('\n'):
        line = ''
        for char in para:
            if line and draw.textlength(line + char, font=f) > w * S:
                lines.append(line)
                line = char
            else:
                line += char
        lines.append(line)
    step = size * 1.42
    if len(lines) * step > h:
        raise ValueError(f'Overflow: {value} in {box}')
    for i, line in enumerate(lines):
        xx = x * S + ((w * S - draw.textlength(line, font=f)) / 2 if center else 0)
        draw.text((xx, (y + i * step) * S), line, font=f, fill=color, anchor='lt')


def line(x1, y1, x2, y2):
    draw.line((x1*S, y1*S, x2*S, y2*S), fill='#b6805b', width=2)


def art(name, box):
    p = ROOT / 'images' / name
    if name.startswith('../'):
        p = ROOT.parent / name[3:]
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    x, y, w, h = box
    fit = ImageOps.contain(im, (int(w*S), int(h*S)), Image.Resampling.LANCZOS)
    px, py = int(x*S+(w*S-fit.width)/2), int(y*S+(h*S-fit.height)/2)
    draw.rectangle((px-4,py-4,px+fit.width+3,py+fit.height+3), fill='#b39671')
    canvas.paste(fit,(px,py))


def start(n, title, refs):
    global canvas, draw
    canvas = BG.copy()
    draw = ImageDraw.Draw(canvas)
    text(title,(80,34,1120,74),40,True,True)
    line(165,110,1115,110)
    records.append({'slide':n,'title':title,'english_reference_slides':refs})


def save(n):
    text(f'{n:02d}',(1180,685,40,24),14,center=True,color=ACCENT)
    canvas.resize(SIZE,Image.Resampling.LANCZOS).save(WORK/f'{PREFIX}{n:04d}.png')


def single(n,title,image,caption,sections,refs):
    start(n,title,refs)
    art(image,(78,143,490,452))
    text(caption,(66,610,516,68),19,center=True,color=ACCENT)
    y=160
    for head,body in sections:
        text(head,(625,y,553,48),29,True,color=ACCENT)
        text(body,(625,y+52,553,112),25)
        y+=166
    save(n)


def pair(n,title,left,right,refs):
    start(n,title,refs)
    line(640,138,640,665)
    for x,(name,caption,body) in zip((60,660),(left,right)):
        art(name,(x+30,140,500,390))
        text(caption,(x,546,560,73),23,True,True)
        text(body,(x+12,626,536,66),21,center=True)
    save(n)


pair(2,'兩位畫家，兩種觀看方式',
 ('Temptation of Adam and Eve by Masolino da Panicale.jpg','亞當與夏娃受誘惑\n馬索利諾（Masolino）','優雅的姿態、柔和的輪廓，\n流露克制而平靜的情緒。'),
 ('Expulsion from the Garden of Eden.jpg','逐出伊甸園\n馬薩喬（Masaccio）','結實的身體、投向地面的陰影，\n以表情與姿態呈現悲痛。'),[3])

single(3,'如何觀看馬薩喬','Masaccio-book.png','圖像書封｜Masaccio: Paintings (Annotated)',[
 ('從具體的線索開始','留意身體的重量、光線的方向、\n空間的深度，以及人物的手勢。'),
 ('把畫中人物看成有重量的人','思考每一個細節如何讓人物\n彷彿站在我們眼前。'),
 ('從觀察走向比較','比較不同畫家的作品，\n找出體積、情緒與空間感的差異。')],[13,14])

single(4,'會投下陰影的身體','shadow.image.png','聖彼得以影子治癒病人｜局部',[
 ('光線塑造身體','臉部、衣褶與肢體的明暗，\n讓人物呈現立體量感。'),
 ('腳步連接地面','人物站立的位置與投下的陰影，\n讓身體具有可以感受的重量。'),
 ('宗教故事走入街道','建築、人物與地面互相呼應，\n形成可信的生活空間。')],[2,14])

single(5,'逐出伊甸園：悲痛也有重量','Expulsion from the Garden of Eden.jpg','逐出伊甸園｜馬薩喬',[
 ('明暗塑造肉身','方向鮮明的光線，\n讓軀幹與四肢呈現體積。'),
 ('腳步承受重量','雙腳踏向地面，陰影隨之延伸，\n使離開樂園的動作更加具體。'),
 ('姿態傳達悲痛','亞當掩面，夏娃仰頭哭喊；\n失落透過身體與表情被看見。')],[3])

single(6,'空間與故事：布蘭卡契禮拜堂','Brancacci Kapelle (Gesamtansicht), S.Maria del Carmine, Florenz.JPG','布蘭卡契禮拜堂｜佛羅倫斯聖母聖衣聖殿',[
 ('神聖故事有了可信的場景','結實的人物、連貫的光線，\n以及可以理解的空間深度，\n把故事帶進觀者的世界。'),
 ('畫面與建築互相呼應','壁畫位於真實的禮拜堂中；\n牆面、光線與觀看位置，\n共同影響我們對畫面的感受。')],[4])

start(7,'短暫的生涯，深遠的改變',[2,11])
art('Masaccio.jpg',(80,148,220,348))
text('馬薩喬\n1401—1428',(70,523,240,80),25,True,True)
timeline=[('1401','生於聖喬瓦尼瓦爾達諾。'),('1422','在聖朱維納爾三聯畫上留下紀年。'),('1426','受託繪製比薩多聯祭壇畫。'),('1428','於羅馬去世，年僅二十多歲。')]
for i,(date,body) in enumerate(timeline):
    y=156+i*108
    text(date,(368,y,145,55),36,True,color=ACCENT)
    text(body,(537,y+8,641,67),26)
    if i<3: line(370,y+82,1170,y+82)
text('一四二〇年代：布蘭卡契禮拜堂壁畫與聖三位一體，\n重新探索身體、光線與繪畫空間。',(359,610,831,78),23,center=True)
save(7)

start(8,'納稅銀：一個空間，三個時刻',[5])
art('The Tribute Money.jpg',(82,137,1116,337))
blocks=[('第二幕｜左側','彼得在湖邊，\n從魚口取出錢幣。'),('第一幕｜中央','收稅人要求繳納稅金；\n基督指示彼得前往湖邊。'),('第三幕｜右側','彼得把錢交給收稅人，\n完成繳納。')]
for i,(head,body) in enumerate(blocks):
    x=70+i*405
    text(head,(x,495,330,46),27,True,True,color=ACCENT)
    text(body,(x,548,330,90),23,center=True)
text('故事順序：中央 → 左側 → 右側',(160,657,960,45),29,True,True,color=ACCENT)
save(8)

for n,title,blocks in [
 (9,'納稅銀：用光影塑造群像',[('身體具有量感','明暗轉折描繪臉孔與衣褶，\n讓人物彷彿有體積與重量。'),('光線統一空間','人物在同一場景中受光，\n彼此形成可信的空間關係。'),('手勢推動敘事','基督與彼得指向湖邊，\n引導觀者追蹤故事發展。')]),
 (10,'納稅銀：風景連接不同時刻',[('同一人物，重複出現','彼得出現在中央、左側與右側，\n分別參與故事的不同時刻。'),('連續風景，串起事件','山脈、湖岸與建築，\n把三段情節連成同一個世界。'),('先看中央，再向兩側閱讀','從吩咐、取錢到繳納，\n透過動作辨認事件的先後。')])]:
    start(n,title,[5])
    art('The Tribute Money.jpg',(80,139,1120,332))
    for i,(head,body) in enumerate(blocks):
        x=72+i*404
        text(head,(x,503,340,47),27,True,True,color=ACCENT)
        text(body,(x,565,340,110),23,center=True)
    save(n)

single(11,'馬薩喬之前：金地繪畫的傳統','Crucifixion by Orcagna (1365).jpg','耶穌受難｜奧爾卡尼亞（Orcagna），1365',[
 ('金色營造神聖世界','金色背景與華麗框架，\n強調宗教圖像的莊嚴。'),
 ('傳統形式中的新探索','馬薩喬的比薩祭壇畫保留金地，\n同時賦予人物更鮮明的體積\n與符合觀看位置的身體比例。')],[7])

single(12,'為仰視而設計的身體','IMG-010 Masaccio《耶穌受難》（比薩祭壇畫）.jpg','耶穌受難｜比薩祭壇畫，1426',[
 ('畫作原本位於觀者上方','這塊祭壇畫板設置在高處，\n觀者必須抬頭觀看。'),
 ('縮短的比例回應視角','基督頸部與軀幹的壓縮，\n配合由下往上的觀看角度。'),
 ('從正確位置理解畫面','透視縮短法讓身體在仰視時，\n呈現更可信的形態。')],[9])

pair(13,'從優雅衣褶，到立體量感',
 ('../Melchior Broederlam/images/IMG-07_Visitation_detail.jpg','聖母訪親\n梅爾基奧·布羅德拉姆','流動的輪廓與細緻衣飾，\n強調人物的優雅。'),
 ('Virgin and Child with Saint Anne.jpg','聖安娜與聖母子\n馬薩喬與馬索利諾','光影賦予聖母與聖嬰\n如雕塑般的體積與重量。'),[8])

single(14,'線性透視：牆壁裡的禮拜堂',"Masaccio 'Holy Trinity' (Santa Maria Novella).png",'聖三位一體｜佛羅倫斯新聖母大殿',[
 ('線條匯聚，建立深度','畫中向後延伸的建築線條，\n朝向觀者視平線上的消失點。'),
 ('平面牆壁彷彿向內打開','柱列與穹頂形成空間幻覺，\n讓人彷彿看見一座\n深入牆內的禮拜堂。')],[6])

single(15,'聖三位一體：把牆面打開','The Holy Trinity.jpg','聖三位一體｜馬薩喬',[
 ('建築引導視線','柱子、拱門與格狀穹頂，\n把視線帶向畫面的深處。'),
 ('人物共享可信的空間','神聖人物與跪姿捐贈者，\n透過位置與尺度形成層次。'),
 ('觀看位置成為畫作的一部分','線性透視把畫中空間\n與站在壁畫前的觀者連結。')],[6])

start(16,'死亡的提醒：聖三位一體下方的墓穴',[15])
text('「我曾是你如今的模樣；\n你也將成為我現在的樣子。」',(120,148,1040,122),36,True,True)
text('下方的骷髏提醒觀者生命終將結束；\n上方的神聖場景，則指向救贖的希望。',(140,292,1000,83),26,center=True)
art('The Holy Trinity bottom.png',(173,392,934,257))
text('聖三位一體｜下方墓穴局部',(250,666,780,34),20,center=True,color=ACCENT)
save(16)

single(17,'從細節讀懂畫中的人','The Distribution of Alms and the Death of Ananias.jpg','分發施捨與亞拿尼亞之死｜馬薩喬',[
 ('先看身體如何站立','觀察腳步與地面的接觸，\n以及人物前後排列的位置。'),
 ('再看人物如何互動','沿著手勢、目光與動作，\n理解人物之間的關係。'),
 ('讓形式與故事連在一起','身體的重量與空間的深度，\n使宗教事件成為可感的經驗。')],[13,14])

start(18,'五個步驟，仔細觀看馬薩喬',[14])
steps=[('腳步','人物是否穩穩站在地面上？'),('光線','亮部與陰影如何塑造身體？'),('空間','向後延伸的建築線條在哪裡匯聚？'),('手勢','雙手與表情如何引導故事？'),('比較','重量、深度與情緒有哪些不同？')]
for i,(head,body) in enumerate(steps):
    y=152+i*103
    text(f'{i+1:02d}',(134,y,98,64),40,True,color=ACCENT)
    text(head,(270,y+3,162,60),34,True)
    text(body,(460,y+9,690,68),28)
    if i<4: line(135,y+78,1150,y+78)
save(18)

single(19,'今天所見，也包含修復的歷史','The Holy Trinity.jpg','聖三位一體｜遮蔽、搬移與重新整合',[
 ('十六世紀：遭到遮蔽','壁畫被後來增設的祭壇遮住，\n一度離開觀者的視線。'),
 ('十九世紀：重新顯露','上半部再度被發現，\n之後被揭取並移至教堂內別處。'),
 ('二十世紀：重見完整構圖','下方墓穴重新被發現，\n促成上、下部分的重新整合。')],[])

single(20,'布蘭卡契禮拜堂：後世大師的學校','Brancacci Kapelle (Gesamtansicht), S.Maria del Carmine, Florenz.JPG','布蘭卡契禮拜堂｜佛羅倫斯',[
 ('在壁畫前學習觀看','後來的藝術家研究這些壁畫，\n學習有重量的身體、\n富有表情的動作與可信的空間。'),
 ('影響延續至下一代','馬薩喬的人物畫，\n成為文藝復興繪畫\n持續借鑑的重要典範。')],[12])

single(21,'短暫的一生，長久的影響','The Death of Masaccio, 1817, by Auguste Couder.jpg','馬薩喬之死｜奧古斯特·庫德，1817',[
 ('二十多歲，生命驟然停下','馬薩喬於一四二八年在羅馬去世，\n當時仍十分年輕。'),
 ('光影、身體與空間留下影響','他對人物體積與空間的處理，\n深刻影響後來的文藝復興繪畫。'),
 ('這是後世想像的場景','庫德在十九世紀繪製此畫，\n並非死亡事件的目擊紀錄。')],[10])

existing_backups = sorted((ROOT/'tw_slides').glob('backup_before_english_reference_*'))
backup = existing_backups[0] if existing_backups else ROOT/'tw_slides'/('backup_before_english_reference_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
backup.mkdir(exist_ok=True)
for n in range(2,22):
    p=DEST/f'{PREFIX}{n:04d}.png'
    if not (backup/p.name).exists():
        shutil.copy2(p,backup/p.name)
    generated=WORK/p.name
    with Image.open(generated) as check:
        check.verify()
    shutil.copy2(generated,p)

sheet=Image.new('RGB',(1600,5*255),'#e9dfce')
sd=ImageDraw.Draw(sheet)
for i,n in enumerate(range(2,22)):
    thumb=Image.open(DEST/f'{PREFIX}{n:04d}.png').resize((390,220),Image.Resampling.LANCZOS)
    x=(i%4)*400+5;y=(i//4)*255
    sd.text((x,y+2),f'Slide {n:02d}',fill=INK)
    sheet.paste(thumb,(x,y+25))
sheet.save(WORK/'contact_sheet.jpg',quality=95)
(WORK/'manifest.json').write_text(json.dumps({'method':'Direct compositing of original artwork; Traditional Chinese adaptation by topic of revised English slides.','preserved_sequence':22,'unchanged_slides':[1,22],'backup':str(backup),'output_size':SIZE,'slides':records},ensure_ascii=False,indent=2)+'\n')
print(f'Updated {len(records)} slides; retained cover and closing slide. Backup: {backup}')
