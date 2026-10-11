"""Compose English YouTube PNGs from original artwork and measured typography."""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / 'images'
OUT = ROOT / 'update'
W, H = 1920, 1080
INK, GOLD, BLUE = '#29231E', '#91601F', '#294556'
CREAM = '#FFF7E9'
PAINT = 'Correggio 1522-1530 The Holy Night.jpg'
GLOW = '(p3) glowing.png'
LADY = '(p10) lady-shine.png'
DRAWING = 'IMG-002_Related_Drawing.jpg'
COPY = 'IMG-004_Boulanger_Copy.png'
DOME = 'IMG-006_Parma_Dome.jpg'
BG = Image.open(ROOT / 'Correggio_s_Holy_Night_background.png').convert('RGB').resize((W, H), Image.Resampling.LANCZOS)
RECORD = {}
CURRENT = 0


def font(size, bold=False, serif=False):
    name = 'Georgia Bold.ttf' if serif else ('Arial Bold.ttf' if bold else 'Arial.ttf')
    return ImageFont.truetype('/System/Library/Fonts/Supplemental/' + name, size)


def new(n):
    global CURRENT
    CURRENT = n
    RECORD[n] = {'text': [], 'images': []}
    return BG.copy()


def panel(im, box, dark=False):
    layer = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, 22, fill=(36, 53, 64, 247) if dark else (255, 248, 233, 247), outline=GOLD, width=3)
    im.paste(Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB'))


def wrap(value, f, width):
    lines = []
    for para in value.split('\n'):
        line = ''
        for word in para.split():
            test = (line+' '+word).strip()
            if f.getlength(test) > width and line:
                lines.append(line)
                line = word
            else:
                line = test
        lines.append(line)
    return lines


def text(im, value, box, size=58, bold=False, serif=False, color=INK, align='left', valign='top'):
    x, y, r, b = box
    f = font(size, bold, serif)
    lines = wrap(value, f, r-x)
    advance = round(size*1.23)
    height = len(lines)*advance
    assert height <= b-y, (CURRENT, value, height, b-y)
    assert all(f.getlength(v) <= r-x for v in lines), (CURRENT, value)
    if valign == 'center':
        y += (b-y-height)//2
    d = ImageDraw.Draw(im)
    for line in lines:
        xx = x if align == 'left' else x+(r-x-f.getlength(line))/2
        d.text((xx, y), line, font=f, fill=color, anchor='lt')
        y += advance
    RECORD[CURRENT]['text'].append({'content': value, 'font_size': size, 'box': list(box)})


def pic(im, name, box, crop=None):
    src = Image.open(ASSETS/name).convert('RGB')
    if crop:
        src = src.crop(tuple(round(v*s) for v,s in zip(crop, [src.width,src.height,src.width,src.height])))
    x,y,r,b = box
    art = ImageOps.contain(src,(r-x,b-y),Image.Resampling.LANCZOS)
    x += (r-x-art.width)//2
    y += (b-y-art.height)//2
    im.paste(art,(x,y))
    ImageDraw.Draw(im).rectangle((x-2,y-2,x+art.width+1,y+art.height+1),outline=GOLD,width=3)
    RECORD[CURRENT]['images'].append({'filename': name, 'crop': crop})


def heading(im, value, size=76):
    panel(im,(65,40,1855,190))
    text(im,value,(100,65,1820,174),size,serif=True,align='center',valign='center')


def arrow(im, start, end):
    d=ImageDraw.Draw(im)
    d.line([start,end],fill=GOLD,width=10)
    a=math.atan2(end[1]-start[1],end[0]-start[0])
    pts=[end]+[(end[0]-28*math.cos(a+offset),end[1]-28*math.sin(a+offset)) for offset in [-0.55,0.55]]
    d.polygon(pts,fill=GOLD)


def save(im):
    im.save(OUT/f'Correggio_s_Holy_Night_slide_{CURRENT:04d}.png')


def split(n, image, title, subtitle, caption='', body='', title_size=88):
    im=new(n)
    panel(im,(65,65,895,1015))
    pic(im,image,(90,90,870,910 if caption else 990))
    if caption: text(im,caption,(95,927,865,1004),40,align='center')
    panel(im,(940,160,1855,920))
    text(im,title,(990,225,1800,585),title_size,serif=True,color=GOLD)
    text(im,subtitle,(995,580,1790,905),52)
    if body: text(im,body,(995,817,1790,891),32)
    save(im)


def compose():
    im=new(2)
    panel(im,(65,115,1015,965)); pic(im,'San Prospero at night - replacement.jpg',(90,145,990,820))
    text(im,'San Prospero at night\nReggio Emilia',(110,846,970,952),40,align='center')
    panel(im,(1060,160,1855,925))
    text(im,'Why is a night painting defined by blinding light?',(1120,225,1795,855),90,serif=True)
    save(im)

    im=new(3); heading(im,'Light that feels physically real')
    panel(im,(65,225,535,1020)); pic(im,'(e p3) Giorgio Vasari.jpg',(85,245,515,850))
    text(im,'Giorgio Vasari',(85,900,515,980),48,bold=True,align='center')
    panel(im,(565,225,1235,1020))
    text(im,'Angels seem to descend from the sky…',(615,300,1185,580),68,serif=True)
    text(im,'…she shades her eyes.',(615,605,1185,870),70,bold=True,color=GOLD)
    text(im,'Vasari’s observation, paraphrased',(610,925,1190,997),32)
    panel(im,(1265,225,1855,1020)); pic(im,PAINT,(1285,245,1835,995)); save(im)

    split(4,GLOW,'Light in the\nDarkness',"Correggio’s Technique")
    split(5,GLOW,'Softened\nTransitions','Outlines melt into shadow.\nSkin and fabric take on a soft, pearlescent glow.',title_size=84)
    split(6,DRAWING,'Planning\nthe Light','A Fitzwilliam Museum drawing reveals early lighting ideas.',caption='The Adoration of the Shepherds',title_size=88)
    im=new(7); panel(im,(65,115,1160,970))
    pic(im,'(p6) The Assumption of the Virgin (1526-1530).jpg',(90,145,1135,815))
    text(im,'Assumption of the Virgin (1526-1530)',(95,862,1130,953),46,align='center')
    panel(im,(1200,220,1855,880))
    text(im,'A Vortex of\nMovement',(1250,295,1805,640),83,serif=True,color=GOLD)
    text(im,'Guiding the Eye',(1250,696,1805,810),57); save(im)

    im=new(8); heading(im,'Follow the movement of light',70)
    steps=[('Glowing Baby','The brightest point draws us in.',GLOW,(80,245,600,565)),('Mary’s Face','Follow the light upward.','(p11) 1 maria.png',(700,245,1220,565)),('Reacting Crowd','Move left toward the shepherds.',PAINT,(1320,245,1840,565)),('Swirling Angels','Follow the diagonal into the clouds.','(p19) angels.png',(1320,685,1840,1005)),('Back to Baby','Spiral down to the center.',GLOW,(700,685,1220,1005))]
    for title,body,name,box in steps:
        x,y,r,b=box; panel(im,box)
        text(im,title,(x+25,y+20,r-25,y+85),44,bold=True,color=GOLD)
        pic(im,name,(x+25,y+103,x+200,b-22),crop=(0,0.30,0.46,0.86) if title=='Reacting Crowd' else None)
        text(im,body,(x+225,y+111,r-22,b-15),38)
    arrow(im,(605,405),(690,405)); arrow(im,(1225,405),(1310,405)); arrow(im,(1580,575),(1580,675)); arrow(im,(1310,845),(1230,845))
    panel(im,(80,685,600,1005),True)
    text(im,'A continuous\nvisual spiral',(115,752,570,950),58,serif=True,color=CREAM); save(im)

    im=new(9); heading(im,'Heaven and earth in one frame',72)
    for x,name,cap in [(65,DOME,'Parma Dome'),(985,COPY,'The Holy Night — Boulanger copy')]:
        panel(im,(x,220,x+870,1020)); pic(im,name,(x+25,245,x+845,900))
        text(im,cap,(x+30,930,x+840,1008),43,bold=True,align='center')
    save(im)
    split(10,'(e p10) Adoration of the Child.jpg','Humanity &\nthe Divine','Physical Reactions',caption='Adoration of the Child')

    im=new(11); heading(im,'Two responses to the same light',70)
    for x,name,title,body in [(65,GLOW,'Intimate care','Mary’s gentle gaze expresses\nmotherly closeness.'),(985,LADY,'Physical recoil','The woman shields her eyes\nfrom the brilliant light.')]:
        panel(im,(x,220,x+870,1020)); pic(im,name,(x+25,245,x+845,730))
        text(im,title,(x+30,768,x+840,850),58,serif=True,color=GOLD,align='center')
        text(im,body,(x+35,875,x+835,1007),43,align='center')
    save(im)

    im=new(12); panel(im,(65,55,825,1025)); pic(im,PAINT,(85,75,805,1005))
    panel(im,(865,100,1855,980)); text(im,'Varied Reactions',(915,140,1805,255),74,serif=True,color=GOLD)
    items=[('Mary','Intimate, motherly care'),('Shielding woman','A physical recoil from light'),('Shepherds','Shifting their weight in awe'),('Dog','Resting at the shepherds’ feet'),('Joseph','Tending the donkey in shadow')]
    for i,(label,desc) in enumerate(items):
        y=290+i*130
        text(im,label,(925,y,1795,y+60),46,bold=True)
        text(im,desc,(925,y+58,1795,y+120),43)
    save(im)

    split(13,'Parma Dome.jpg','Origins of\nHoly Light','Beyond the Gospel',title_size=86)
    split(14,GLOW,'The Glowing\nChild','The motif draws on early literature. The Gospel does not explicitly describe a glowing infant.',title_size=82)

    im=new(15); heading(im,'Sources of Light')
    entries=[('Early literature','Non-canonical\nProtevangelium of James'),('Mystical visions','Bridget of Sweden\n14th century'),('Painting traditions','Northern European\nNativity paintings'),('Theology','Gospel of John:\nJesus as Light of the World')]
    for i,(title,body) in enumerate(entries):
        x=65+(i%2)*920; y=235+(i//2)*395
        panel(im,(x,y,x+870,y+360),dark=i==3)
        text(im,title,(x+40,y+35,x+830,y+120),59,serif=True,color=CREAM if i==3 else GOLD)
        text(im,body,(x+40,y+150,x+830,y+330),54,color=CREAM if i==3 else INK)
    save(im)

    im=new(16); heading(im,'From drawing to final composition',66)
    for x,name,title,body in [(65,DRAWING,'Related drawing','Diffuse light • traditional pose\nConventional angel placement'),(985,COPY,'Final design — Boulanger copy','Intimate pose • spiraling angels\nConcentrated light • retained architecture')]:
        panel(im,(x,220,x+870,1020)); pic(im,name,(x+25,240,x+845,770))
        text(im,title,(x+30,790,x+840,865),43,bold=True,align='center')
        text(im,body,(x+30,892,x+840,1005),37,align='center')
    save(im)
    split(17,'Correggio_self_portrait.jpg','Journey\nThrough Time','A Masterpiece Moves',caption='Correggio',title_size=86)
    split(18,'聖波羅斯貝聖殿 Reggio Emilia San Prospero Frescoed interior.JPG','The Original\nSetting','San Prospero’s interior reveals the architectural scale of the altarpiece.',title_size=80)

    im=new(19); heading(im,'The journey of The Holy Night',70)
    entries=[('1522','Reggio Emilia','Commissioned for\nSan Prospero','聖波羅斯貝聖殿 Reggio Emilia San Prospero.jpg'),('1640','Modena','Moved by\nDuke Francesco I',"弗朗切斯科一世·埃斯特 Francesco I d'Este.jpg"),('1746','Dresden','Acquired for\nthe royal collection','Gemäldegalerie Alte Meister.JPG')]
    for i,(year,place,body,name) in enumerate(entries):
        x=65+i*610; panel(im,(x,235,x+570,1015))
        text(im,year,(x+25,266,x+545,385),90,serif=True,color=GOLD,align='center')
        text(im,place,(x+25,395,x+545,480),48,bold=True,align='center')
        pic(im,name,(x+25,495,x+545,790))
        text(im,body,(x+25,834,x+545,994),43,align='center')
    arrow(im,(625,330),(670,330)); arrow(im,(1235,330),(1280,330)); save(im)

    im=new(20); heading(im,'Commission Fee: 208 liras regias',72)
    panel(im,(65,225,775,1020)); pic(im,'Anton Raphael Mengs.jpg',(90,250,750,895))
    text(im,'Anton Raphael Mengs',(90,935,750,1005),44,bold=True,align='center')
    panel(im,(815,225,1855,1020)); pic(im,'Diana as Personification of the Night.jpg',(840,250,1830,835))
    text(im,'Diana as Personification of the Night\nby Anton Raphael Mengs (1765)',(845,875,1825,1007),42,align='center')
    save(im)

    compose_slide_21()
    compose_slide_22()


def compose_slide_21():
    im = new(21)
    heading(im, 'Reading the Light: Three Visual Zones', 68)
    entries = [
        (GLOW, 'Infant', 'Concentrated light', 'Shapes nearby faces\nand folds of fabric.'),
        ('(p19) angels.png', 'Clouds', 'Softer brightness', 'Gives the angels form\nand the heavenly space depth.'),
        ('(p19) sky.png', 'Distance', 'A pale horizon', 'Opens the night landscape\nand creates spatial depth.'),
    ]
    for i, (name, title, subtitle, body) in enumerate(entries):
        x = 65 + i * 610
        panel(im, (x, 225, x + 570, 905))
        pic(im, name, (x + 25, 250, x + 545, 605))
        text(im, title, (x + 25, 635, x + 545, 720), 66,
             serif=True, color=GOLD, align='center')
        text(im, subtitle, (x + 25, 734, x + 545, 795), 43,
             bold=True, align='center')
        text(im, body, (x + 25, 803, x + 545, 896), 35, align='center')
    panel(im, (150, 945, 1770, 1035), dark=True)
    text(im, 'Three visual zones do not imply three physical lamps.',
         (190, 965, 1730, 1030), 45, bold=True, color=CREAM, align='center')
    save(im)


def compose_slide_22():
    im = new(22)
    panel(im, (65, 55, 825, 1025))
    pic(im, PAINT, (85, 75, 805, 1005))
    panel(im, (865, 145, 1855, 945))
    text(im, 'Will you see', (930, 220, 1790, 335), 90, serif=True)
    text(im, 'a simple story,', (930, 345, 1790, 465), 96, serif=True)
    text(im, 'or a', (930, 492, 1790, 600), 86, serif=True)
    text(im, 'complex vortex?', (930, 620, 1790, 890), 100,
         serif=True, color=GOLD)
    save(im)


if __name__=='__main__':
    compose()
    assert sorted(RECORD)==list(range(2,23))
    (ROOT/'slide_redesign_manifest.json').write_text(json.dumps({'size':[W,H],'mode':'original-image compositing','slides':RECORD},ensure_ascii=False,indent=2)+'\n')
    for n in RECORD:
        with Image.open(OUT/f'Correggio_s_Holy_Night_slide_{n:04d}.png') as image:
            assert image.size==(W,H)
            image.verify()
    print('Validated 21 slides at 1920 × 1080; all text fits assigned boxes.')
