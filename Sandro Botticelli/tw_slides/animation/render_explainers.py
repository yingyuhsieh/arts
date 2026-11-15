"""Render nine 4K Mandarin explainers from supplied slide PNGs and source narration."""
from pathlib import Path
import json,math,re,subprocess,sys
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'animation'
W,H,FPS=3840,2160,30
GREEN='#284d40';GOLD='#aa7c38';INK='#233d32';MUTED='#6d7567';CREAM='#fffcf3'
FONT='/System/Library/Fonts/STHeiti Medium.ttc'
PREFIX='波提切利的線條：超越維納斯的視野'
NUMS=[8,9,10,12,13,15,21,24,25]
MANIFEST=json.loads((ROOT/f'video/{PREFIX}_narration_manifest.json').read_text())['slides']
BLOCKS=re.findall(r'(?ms)^\[([^\]]+\.png)\]\s*\n(.*?)(?=^\[|\Z)',(ROOT/f'subtitle/{PREFIX}.txt').read_text())
IMAGES={n:Image.open(ROOT/f'update/{PREFIX}_slide_{n:04d}.png').convert('RGB') for n in NUMS}
def font(s):return ImageFont.truetype(FONT,round(s*2))
def txt(d,xy,s,size=28,color=INK):d.text((round(xy[0]*2),round(xy[1]*2)),s,font=font(size),fill=color)
def line(d,pts,color=GOLD,width=3):d.line([(round(x*2),round(y*2)) for x,y in pts],fill=color,width=width*2,joint='curve')
def rect(d,box,fill=CREAM,outline='#cabea2',width=1,r=14):d.rounded_rectangle(tuple(round(v*2) for v in box),radius=r*2,fill=fill,outline=outline,width=width*2)
def ell(d,box,fill=CREAM,outline=GOLD,width=2):d.ellipse(tuple(round(v*2) for v in box),fill=fill,outline=outline,width=width*2)
def ease(t):return 1-(1-max(0,min(1,t)))**3
def source(n,box=None):return IMAGES[n].crop(box) if box else IMAGES[n]
# All artwork details below come from the user-supplied PNGs.
FRESCO=source(8,(404,151,875,406))
MOSES=source(9,(391,222,890,526))
SPRING=source(12,(262,141,1014,620))
VENUS=source(15,(105,195,686,556))
PALACE=source(13,(731,48,1241,494))
DANTE=source(24,(424,163,1270,595))
MUSEUM=source(25,(575,191,1186,481))

def fit(canvas,img,box,border=True):
    x,y,w,h=box
    if border:rect(ImageDraw.Draw(canvas),(x-8,y-8,x+w+8,y+h+8),fill='#f5efdf',outline='#baa77d',r=5)
    fitted=ImageOps.contain(img,(round(w*2),round(h*2)),Image.Resampling.LANCZOS).convert('RGBA')
    px=round(x*2)+(round(w*2)-fitted.width)//2;py=round(y*2)+(round(h*2)-fitted.height)//2
    canvas.alpha_composite(fitted,(px,py))
    return (px/2,py/2,fitted.width/2,fitted.height/2)

def label(canvas,xy,title,body,width=300):
    d=ImageDraw.Draw(canvas);txt(d,xy,title,30);txt(d,(xy[0],xy[1]+48),body,22,MUTED)

def panel_image(img,note='原投影片圖像',path=None):
    c=Image.new('RGBA',(2200,1440));fit(c,img,(28,40,1044,620));txt(ImageDraw.Draw(c),(30,690),note,20,MUTED)
    return c,path

def gallery(images,labels):
    c=Image.new('RGBA',(2200,1440));count=len(images)
    if count==2:boxes=[(24,50,500,520),(566,50,500,520)]
    elif count==3:boxes=[(20,70,330,500),(383,70,330,500),(746,70,330,500)]
    elif count==4:boxes=[(25,18,490,280),(585,18,490,280),(25,380,490,280),(585,380,490,280)]
    else:raise ValueError(count)
    for i,(im,box) in enumerate(zip(images,boxes)):
        fit(c,im,box)
        txt(ImageDraw.Draw(c),(box[0]+4,box[1]+box[3]+27),labels[i],23)
    return c,None

def timeline():
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    xs=[80,425,770]
    line(d,[(95,170),(980,170)],'#d0c2a4',3)
    for x,year,desc,n,box in zip(xs,['1492','1494','1498'],[['羅倫佐・德・美第奇','去世'],['法軍進入義大利','美第奇家族被逐'],['薩佛納羅拉','遭到處死']],[21]*3,[(74,465,416,644),(468,465,812,644),(863,465,1203,644)]):
        ell(d,(x,150,x+40,190),fill=GOLD);txt(d,(x-4,65),year,47)
        txt(d,(x-8,230),desc[0],23);txt(d,(x-8,274),desc[1],24)
        fit(c,source(n,box),(x-7,365,290,205))
    txt(d,(70,650),'短短幾年，城市的權力與信仰接連改變。',25,MUTED)
    return c,[(95,170),(445,170),(790,170)]

def factors(labels,title='一起理解畫風的轉變'):
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    points=[(550,150),(220,470),(880,470)]
    line(d,points+[points[0]],'#c8b89b',3)
    for (x,y),s in zip(points,labels):
        ell(d,(x-118,y-83,x+118,y+83),fill=CREAM,outline=GREEN,width=2)
        txt(d,(x-len(s)*16,y-18),s,32)
    txt(d,(280,625),title,30,GREEN)
    return c,points+[points[0]]

def room():
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    rect(d,(50,35,1040,640),fill='#efe5cf',outline='#bcac8b',r=2)
    line(d,[(50,530),(1040,530)],'#b6a17a',2)
    fit(c,SPRING,(250,90,600,350));rect(d,(215,485,885,540),fill='#a18459',outline='#6d583b',r=3)
    for x in [235,835]:rect(d,(x,540,x+30,610),fill='#876b47',outline='#6d583b',r=1)
    txt(d,(65,675),'陳列關係示意：畫作、長箱椅與住宅空間',23,MUTED)
    return c,[(165,265),(245,265),(245,490),(220,490)]

def projects():
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    for x,title,sub in [(40,'1481 年印刷本','插圖設計'),(595,'羊皮紙系列','另一項創作計畫')]:
        rect(d,(x,65,x+460,570),fill=CREAM,outline=GOLD,width=2)
        # Native line drawings distinguish a printed book from a manuscript sheet.
        if x==40:
            line(d,[(x+80,175),(x+220,155),(x+220,350),(x+80,370),(x+80,175)],GREEN,3)
            line(d,[(x+220,155),(x+365,175),(x+365,370),(x+220,350)],GREEN,3)
            for yy in [205,245,285,325]:line(d,[(x+245,yy),(x+337,yy+10)],GOLD,2)
        else:
            rect(d,(x+120,155,x+340,355),fill='#efe1bf',outline=GREEN,r=1)
            line(d,[(x+150,315),(x+186,245),(x+217,270),(x+252,212),(x+307,315)],GOLD,3)
        txt(d,(x+40,425),title,32);txt(d,(x+40,490),sub,24,MUTED)
    txt(d,(100,655),'兩個計畫分開理解，避免混為同一套作品。',25,MUTED)
    return c,None

def materials():
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    fit(c,VENUS,(25,30,490,350));fit(c,SPRING,(585,30,490,350))
    for x,title,mat in [(25,'維納斯的誕生','畫布蛋彩'),(585,'春','木板蛋彩')]:
        txt(d,(x+20,430),title,32);txt(d,(x+20,493),mat,32,GOLD)
        rect(d,(x+15,570,x+465,622),fill='#e2d2b2',outline='#a58b5f',r=3)
        for j in range(8):line(d,[(x+25,575+j*5),(x+455,575+j*5)],'#bfa47c',1)
    txt(d,(95,676),'觀察題材，也留意作品的材料與支撐。',25,MUTED)
    return c,None

def archives():
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    txt(d,(85,50),'現存圖頁的主要收藏地',37)
    for x,name in [(80,'柏林'),(640,'梵蒂岡')]:
        rect(d,(x,180,x+390,470),fill=CREAM,outline=GREEN,width=2)
        for k in range(3):
            rect(d,(x+95+k*22,230+k*15,x+255+k*22,365+k*15),fill='#f5ecd6',outline=GOLD,r=2)
            line(d,[(x+115+k*22,280+k*15),(x+230+k*22,280+k*15)],GREEN,2)
        txt(d,(x+137,408),name,32)
    line(d,[(470,320),(640,320)],GOLD,3)
    txt(d,(90,565),'1882',60,GOLD);txt(d,(350,590),'柏林購藏一大批圖稿',29)
    txt(d,(90,660),'收藏與出版，讓圖稿獲得更多研究。',26,MUTED)
    return c,[(470,320),(640,320)]

def question_graph(labels,title):
    c=Image.new('RGBA',(2200,1440));d=ImageDraw.Draw(c)
    txt(d,(65,38),title,38)
    xs=[70,420,770]
    for j,(x,s) in enumerate(zip(xs,labels)):
        ell(d,(x,245,x+250,495),fill=CREAM,outline=GREEN,width=2)
        txt(d,(x+125-len(s)*18,340),s,36)
        if j<2:line(d,[(x+267,370),(x+330,370),(x+315,358),(x+330,370),(x+315,382)],GOLD,2)
    txt(d,(120,620),'讓每一個觀察，都回到畫面中的具體細節。',25,MUTED)
    return c,[(195,500),(545,500),(895,500)]

# (audio-relative start, short display heading, two supporting lines, graphic, note)
CONFIG={
8:('西斯汀的敘事：線條如何說故事',[
    (0,'先看側牆，再看故事',['波提切利先參與側牆壁畫','跟著畫面中的人物展開閱讀'],lambda:panel_image(source(8))),
    (11.5,'懲罰可拉及其同黨',['在同一幅壁畫裡','安排彼此呼應的不同情節'],lambda:panel_image(FRESCO,'原投影片中的壁畫全景')),
    (17.18,'逼近、倒下、舉手',['人物的動作各不相同','手勢與衣褶連起敘事節奏'],lambda:gallery([source(8,(73,171,356,513)),source(8,(458,438,822,638)),source(8,(926,171,1201,435))],['驚慌與倒下','衝突的中心','逼近與保護'])),
    (23.58,'讓目光走過畫面',['尋找動作與手勢的呼應','把分散的情節串在一起'],lambda:panel_image(FRESCO,'連線為觀看順序示意',[(120,430),(430,485),(775,340),(1010,420)])),
    (34.84,'緊張感背後的權威',['摩西與亞倫的權威','在教宗禮拜堂裡獲得呼應'],lambda:panel_image(FRESCO,'回到作品的展示與委託脈絡')),
    (51.54,'線條，也傳達觀念',['既組織故事','也帶出宗教與權力的關係'],lambda:panel_image(source(8))) ]),
9:('摩西生平：一幅畫裡的不同時刻',[
    (0,'同一個人，反覆出現',['在同一片風景裡','辨認不同時刻的摩西'],lambda:panel_image(MOSES,'原投影片中的壁畫全景')),
    (15.68,'第一個情節：衝突',['擊殺欺壓希伯來人的埃及人','從人物動作辨認故事'],lambda:panel_image(source(9,(951,36,1198,292)),'原投影片局部：擊殺埃及人')),
    (19.7,'離開，然後幫助他人',['逃往米甸','在井邊幫助女子取水'],lambda:panel_image(source(9,(953,399,1195,591)),'原投影片局部：井邊取水')),
    (23.88,'在荊棘前接受呼召',['故事再一次向前推進','不同時間被放入同一幅畫'],lambda:panel_image(source(9,(84,38,327,290)),'原投影片局部：燃燒的荊棘')),
    (28.16,'把不同時刻連起來',['辨認衣著，再跟隨動作','讓目光成為閱讀故事的路徑'],lambda:panel_image(MOSES,'連線只示意觀看路徑',[(950,535),(605,480),(175,220)])),
    (40.96,'沒有框線的連環畫',['山坡、樹木、建築','幫我們分辨不同情節'],lambda:panel_image(source(9),'看人物，也看風景如何組織故事')) ]),
10:('神話花園：從美感走向意義',[
    (0,'第三站：神話花園',['女神、花朵、髮絲與衣裙','從熟悉的作品開始觀看'],lambda:panel_image(source(10))),
    (11.08,'美，是觀看的起點',['再多停留一會兒','問問人物與場景如何安排'],lambda:gallery([source(10,(92,235,342,620)),source(10,(394,281,779,586)),source(10,(816,284,1201,589))],['帕拉斯與半人馬','春','維納斯的誕生'])),
    (15.52,'當時的人看見什麼？',['神話人物承載什麼意義？','讓作品回到當時的觀看脈絡'],lambda:question_graph(['人物','意義','觀眾'],'不只看美，也追問意義')),
    (21.26,'為什麼樣的空間而畫？',['作品放在哪裡？','又希望讓誰看見？'],lambda:question_graph(['空間','作品','觀眾'],'把作品放回生活與觀看的環境')),
    (26.06,'回到人物之間',['看手勢、目光與彼此距離','讓花園的意義慢慢展開'],lambda:panel_image(SPRING,'由原投影片第 12 頁取用同一作品',[(230,365),(520,345),(850,390)])) ]),
12:('把目光放低：春的植物細節',[
    (0,'從女神身上移開目光',['看看人物腳邊','花草也值得仔細觀看'],lambda:panel_image(source(12))),
    (7.22,'花園就在腳邊',['散布的植物各有姿態','留意葉形、花瓣與生長方式'],lambda:panel_image(source(12,(267,494,1007,617)),'原投影片局部：人物腳邊的草地')),
    (10.96,'從形態分辨細節',['葉片、花瓣與果實','讓神話世界連向自然觀察'],lambda:gallery([source(12,(38,134,233,245)),source(12,(1047,133,1239,245)),source(12,(1047,325,1239,435))],['果實與花','葉形','花瓣'])),
    (18.74,'植物並非隨手點綴',['細節可以辨認','也讓想像中的花園更可感'],lambda:gallery([source(12,(37,324,234,434)),source(12,(37,510,234,619)),source(12,(1047,510,1239,619))],['香桃木','雛菊','鳶尾花'])),
    (28.26,'優雅與觀察並存',['人物線條之外','還有對花草形態的細膩留意'],lambda:panel_image(SPRING,'原投影片中的春')),
    (38.12,'連一朵小花都值得停留',['把視線移向下方','讓微小細節成為觀看的入口'],lambda:panel_image(source(12,(37,510,234,619)),'原投影片局部：前景小花',[(220,420),(480,300),(790,395)])) ]),
13:('春的真實脈絡：房間、展示與時間',[
    (0,'想像它在一間房裡',['畫作與家具、光線','曾經屬於同一個生活空間'],room),
    (11.16,'住宅中的藝術',['早期清冊記錄住宅的陳列','畫作下方是一張長箱椅'],room),
    (29.82,'今天並看，不等於原本成對',['春與維納斯的誕生','最初委託關係仍有討論空間'],lambda:gallery([SPRING,VENUS],['春','維納斯的誕生'])),
    (45.92,'時間也改變了花園',['部分顏料隨歲月變暗','今天的深色不等於最初的色貌'],lambda:panel_image(SPRING,'保留現有圖像；不模擬原色復原')),
    (60.48,'畫面也保存時間的痕跡',['看到畫家的筆觸','也看到作品走過的歲月'],lambda:panel_image(source(13))) ]),
15:('維納斯正在抵岸：停留在風裡的瞬間',[
    (0,'以誕生為名，畫的是抵岸',['約一四八五年','女神被海風吹向岸邊'],lambda:panel_image(VENUS,'原投影片中的維納斯的誕生')),
    (14.02,'從熟悉的女神，再看一次',['回到畫面本身','追尋風、髮絲與衣袍的關係'],lambda:panel_image(source(15))),
    (29.19,'從左側吹來的風',['長髮受到牽動','右側女子迎上前準備披袍'],lambda:panel_image(VENUS,'連線為構圖觀看示意',[(170,255),(510,285),(885,340)])),
    (37.51,'一切彷彿仍在進行',['風還在吹，髮絲還在飄','衣袍尚未落到女神身上'],lambda:panel_image(VENUS,'跟隨畫中的曲線',[(180,200),(360,250),(620,320),(910,265)])),
    (49.91,'題材之外，也比較材料',['維納斯的誕生：畫布','春：木板'],materials),
    (61.19,'傳說仍需證據',['具體委託人與模特兒身分','現有證據不足以定案'],lambda:question_graph(['委託人','證據','模特兒'],'暫時放下傳說，繼續觀察畫面')),
    (70.67,'抵達之前的一瞬間',['讓目光跟著線條走','看它如何把時間停留在風裡'],lambda:panel_image(VENUS,'原投影片中的維納斯的誕生',[(160,240),(490,280),(930,350)])) ]),
21:('危機與和解：理解晚期的轉變',[
    (0,'先看城市經歷了什麼',['一四九〇年代的佛羅倫斯','政治與宗教接連發生巨變'],timeline),
    (23.54,'熟悉的環境正在改變',['贊助、政治、宗教','共同構成畫家工作的背景'],lambda:factors(['贊助環境','政治秩序','宗教氣氛'],'把城市的變化放在一起看')),
    (35.71,'避免單一原因的解釋',['不能只憑激烈的畫面情緒','就推斷畫家的精神狀態'],lambda:factors(['作品情感','歷史證據','委託脈絡'],'回到作品與證據，理解轉變')),
    (47.65,'同時考慮三個面向',['時代環境、委託需求','以及持續探索的表現方式'],lambda:factors(['時代環境','委託需求','表現探索'])),
    (57.05,'接著，回到作品本身',['急促與緊密的線條','究竟帶來什麼樣的感受？'],lambda:panel_image(source(21))) ]),
24:('但丁圖稿：讓線條帶出一段旅程',[
    (0,'線條，也能組織時間',['走進但丁的神曲','看靜止的畫面如何展開旅程'],lambda:panel_image(source(24))),
    (3.66,'先區分兩個創作計畫',['一四八一年印刷本插圖','與後來的羊皮紙系列'],projects),
    (15.22,'人物在同一頁反覆出現',['但丁與嚮導維吉爾','藉由位置變化帶出前後時刻'],lambda:panel_image(DANTE,'原投影片的圖稿與局部標註')),
    (27.28,'跟著道路與地形走',['移動目光，串起不同位置','把一張靜止的圖讀成旅程'],lambda:panel_image(DANTE,'動畫線為觀看路徑示意',[(200,165),(830,250),(360,360),(700,455),(550,570)])),
    (39.9,'圖頁分藏，研究持續',['現今主要收藏地','柏林與梵蒂岡'],archives),
    (44.06,'一八八二年的購藏',['柏林購藏一大批圖稿','後續出版擴大了研究機會'],archives),
    (51.96,'光靠線條，也能說故事',['安排場景、帶出動作','讓複雜敘事慢慢展開'],lambda:panel_image(DANTE,'回到線條與人物位置的閱讀',[(200,165),(830,250),(360,360),(700,455),(550,570)])) ]),
25:('線條引領觀看：把方法帶到下一幅畫',[
    (0,'不再只想到維納斯',['從不同作品回望波提切利','看線條如何有了表情'],lambda:panel_image(source(25))),
    (6.38,'姿態、舞步、空隙、擁抱',['不同的線條安排','帶出不同的人物情感'],lambda:question_graph(['姿態','關係','情感'],'同一條觀看線索，串起不同作品')),
    (18.12,'讓抽象情感變得可感',['美德、欲望、敬畏、盼望','可以從人物與線條讀出'],lambda:question_graph(['線條','人物','情緒'],'畫中的形式，也能承載情緒')),
    (27.46,'下一次看畫，從這裡開始',['伸出的手、彎曲的衣褶','還有人物之間的距離'],lambda:question_graph(['手勢','衣褶','距離'],'讓目光跟著線條走')),
    (38.24,'向畫面提出問題',['誰被連在一起，誰彼此分開？','你感到安定，還是不安？'],lambda:question_graph(['連結','分離','感受'],'讓具體觀察引出自己的問題')),
    (45.24,'觀察，再對照作品解說',['那些原本沒有留意的小地方','可能正是打動你的關鍵'],lambda:panel_image(MUSEUM,'原投影片中的美術館觀看場景')),
    (54.82,'看懂藝術，從多停留開始',['把這條線索帶到下一幅畫','讓目光慢一點，細節就多一點'],lambda:panel_image(MUSEUM,'下一次站在畫前，你會先看哪裡？')) ])}

BACKGROUND=Image.open(ROOT/f'{PREFIX}_background.png').convert('RGBA').resize((W,H),Image.Resampling.LANCZOS)
BACKGROUND=Image.alpha_composite(BACKGROUND,Image.new('RGBA',(W,H),(255,249,232,140)))

def prepare(n):
    title,scenes=CONFIG[n];base=BACKGROUND.copy();d=ImageDraw.Draw(base)
    txt(d,(100,60),'波提切利的線條  /  圖文解說',21,GOLD)
    txt(d,(100,110),title,46)
    line(d,[(100,200),(1820,200)],'#c8b999',1)
    rect(d,(745,224,1835,955),fill='#fffaf0',outline='#d3c4a6',width=1,r=16)
    txt(d,(100,1018),'跟著線條看，讓目光帶出故事。',18,MUTED)
    txt(d,(1710,1018),f'{n:02d} / 26',18,GOLD)
    rendered=[]
    for i,(start,heading,body,make) in enumerate(scenes):
        textlayer=Image.new('RGBA',(W,H));td=ImageDraw.Draw(textlayer)
        txt(td,(100,281),f'{i+1:02d}  /  {len(scenes):02d}',22,GOLD)
        # Wrap long headings deliberately; supporting lines remain comfortably inside the text column.
        titlelines=[heading[k:k+13] for k in range(0,len(heading),13)]
        for j,s in enumerate(titlelines):txt(td,(100,346+j*67),s,40)
        yy=380+len(titlelines)*67
        for j,s in enumerate(body):txt(td,(103,yy+j*55),s,27,MUTED)
        image,path=make()
        rendered.append((textlayer,image,path))
    return base,rendered

def trace(d,path,progress,offset=(745,224)):
    if not path:return
    pts=[(x+offset[0],y+offset[1]) for x,y in path]
    lengths=[math.dist(a,b) for a,b in zip(pts,pts[1:])];total=sum(lengths);remaining=max(0,min(1,progress))*total
    drawn=[pts[0]]
    for a,b,length in zip(pts,pts[1:],lengths):
        if remaining>=length:drawn.append(b);remaining-=length
        else:
            u=remaining/length;drawn.append((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u));break
    if len(drawn)>1:
        line(d,drawn,'#fff5ce',8);line(d,drawn,GOLD,3)
    x,y=drawn[-1];ell(d,(x-10,y-10,x+10,y+10),fill='#fff9e8',outline=GOLD,width=3)

def render_frame(n,t,prepared,duration):
    base,layers=prepared;scenes=CONFIG[n][1]
    k=max(i for i,s in enumerate(scenes) if t>=s[0]);start=scenes[k][0]
    local=t-start;end=scenes[k+1][0] if k+1<len(scenes) else duration
    result=base.copy();textlayer,panel,path=layers[k]
    e=ease(local/.65)
    if e<1:
        textlayer=textlayer.copy();textlayer.putalpha(textlayer.getchannel('A').point(lambda a:int(a*e)))
    result.alpha_composite(textlayer,(0,round(25*(1-e)*2)))
    # The artwork opens with a short horizontal reveal; no invented movement is applied inside the painting.
    if e<1:
        cut=round(panel.width*e)
        if cut:result.alpha_composite(panel.crop((0,0,cut,panel.height)),(1490,448))
    else:result.alpha_composite(panel,(1490,448))
    d=ImageDraw.Draw(result)
    if path:
        trace(d,path,max(0,(local-.8)/max(2,end-start-1.2)))
    # A compact sequence of milestones keeps the narration's structure visible.
    count=len(scenes);step=540/max(1,count-1)
    line(d,[(110,840),(650,840)],'#d3c6aa',2)
    for j in range(count):
        x=110+j*step
        ell(d,(x-7,833,x+7,847),fill=GREEN if j<=k else '#e9deca',outline=GREEN if j==k else '#c7b99b',width=2)
    txt(d,(105,885),'觀察  →  線索  →  理解',23,GOLD)
    line(d,[(100,987),(1820,987)],'#c9bea7',1)
    line(d,[(100,987),(100+1720*min(1,t/duration),987)],GREEN,3)
    if n==21 and k==0:
        # Reveal each event as its year is spoken, rather than showing future events early.
        cover=Image.new('RGBA',(W,H));cd=ImageDraw.Draw(cover)
        for cue,x in [(4.44,80),(8.56,425),(14.74,770)]:
            alpha=round(248*(1-ease((t-cue)/.6)))
            if alpha:cd.rectangle(((745+x-20)*2,(224+44)*2,(745+x+310)*2,(224+600)*2),fill=(255,250,240,alpha))
        result=Image.alpha_composite(result,cover);d=ImageDraw.Draw(result)
        for cue,x in [(4.44,80),(8.56,425),(14.74,770)]:
            if t>=cue:
                ex=x+745;ell(d,(ex-5,224+145,ex+45,224+195),fill=GREEN,outline=GREEN,width=2)
    return result.convert('RGB')

def main():
    preview='--preview' in sys.argv
    for n in NUMS:
        work=WORK/f'slide_{n:03d}';work.mkdir(exist_ok=True)
        start=MANIFEST[n-1]['start'];end=MANIFEST[n]['start'];duration=round(end-start,3)
        prepared=prepare(n);scenes=CONFIG[n][1]
        samples=[22 if n==21 and i==0 else min(duration-.4,s[0]+min(3,(scenes[i+1][0]-s[0])/2 if i+1<len(scenes) else 3)) for i,s in enumerate(scenes)]
        sheet=Image.new('RGB',(1920,540*math.ceil(len(samples)/2)),'#eee8d8')
        for i,t in enumerate(samples):
            f=render_frame(n,t,prepared,duration);f.thumbnail((960,540));sheet.paste(f,((i%2)*960,(i//2)*540))
        sheet.save(work/'storyboard.jpg',quality=94)
        render_frame(n,samples[min(2,len(samples)-1)],prepared,duration).save(work/'preview_4k.png')
        (work/'narration_tw.txt').write_text(BLOCKS[n-1][1].strip()+'\n')
        output=work/f'波提切利_{n:03d}_圖文解說動畫_4k.mp4'
        data={'source_slide':str((ROOT/f'update/{PREFIX}_slide_{n:04d}.png').resolve()),'narration_script':str((ROOT/f'subtitle/{PREFIX}.txt').resolve()),'narration_page':n,'source_audio':str((ROOT/'Sounrds.m4a').resolve()),'source_audio_excerpt_seconds':[start,end],'video':str(output.resolve()),'dimensions':[W,H],'fps':FPS,'duration_seconds':duration,'scenes':[{'start':s[0],'heading':s[1],'supporting_text':s[2]} for s in scenes],'assets':'Supplied PNGs, artwork details cropped from those PNGs, existing project background, native explanatory diagrams. Source images unchanged. Animated paths are reading guides.'}
        (work/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        if preview:continue
        if output.exists() and (work/'verification.json').exists():print(f'SKIP verified {n}',flush=True);continue
        audio=work/'narration_tw.wav'
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(start),'-i',str(ROOT/'Sounrds.m4a'),'-t',str(duration),'-c:a','pcm_s16le',str(audio)],check=True)
        cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','8','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart',str(output)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        print(f'PAGE {n} START duration={duration}',flush=True)
        try:
            for frame_no in range(math.ceil(duration*FPS)):
                proc.stdin.write(render_frame(n,frame_no/FPS,prepared,duration).tobytes())
                if frame_no%450==0:print(f'PAGE {n}: {frame_no/FPS:.0f}/{duration}',flush=True)
            proc.stdin.close()
            if proc.wait():raise RuntimeError(f'Encoding failed for page {n}')
        finally:
            if proc.poll() is None:proc.terminate()
        print(f'PAGE {n} COMPLETE {output.stat().st_size} bytes',flush=True)
if __name__=='__main__':main()
