#!/usr/bin/env python3
"""Render five source-grounded, narrated artwork explainers at native UHD."""
from functools import lru_cache
from pathlib import Path
import argparse
import json
import math
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT.parent / 'images'
W, H, S, FPS = 3840, 2160, 2, 30
GOLD, CREAM, MUTED = '#d5ac67', '#f9ebcc', '#c1ab88'
SANS = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SERIF = '/System/Library/Fonts/Supplemental/Georgia.ttf'
FILES = {
    'anthony': 'Ascetic_images/IMG-001_The_Torment_of_Saint_Anthony.jpg',
    'bellini': 'Ascetic_images/IMG-002_Saint_Francis_in_the_Desert.jpg',
    'leonardo': 'Ascetic_images/IMG-003_Saint_Jerome_in_the_Wilderness.jpg',
    'durer': 'Ascetic_images/IMG-004_Saint_Jerome_in_His_Study.jpg',
    'jerome': 'Ascetic_images/IMG-005_Saint_Jerome_in_Penitence_El_Greco.jpg',
    'francis': 'Ascetic_images/IMG-006_Saint_Francis_in_Meditation.jpg',
    'magdalen': 'Ascetic_images/IMG-007_The_Penitent_Magdalen.jpg',
    'bosch': 'Ascetic_images/IMG-008_Temptation_of_Saint_Anthony_Triptych.jpg',
    'hospitality': 'Ascetic_images/IMG-009_Saint_Anthony_Abbot_and_Saint_Paul_the_Hermit.jpg',
    'serapion': 'Ascetic_images/IMG-010_Saint_Serapion.jpg',
    'paul': 'Ascetic_images/IMG-011_Saint_Paul_the_Hermit.jpg',
    'latour': 'Ascetic_images/IMG-012_Saint_Jerome_in_Penitence_La_Tour.jpg',
    'meditation': 'Francisco de Zurbarán 默想中的聖方濟各 Saint Francis in Meditation.jpg',
    'schongauer': '馬丁·肖高爾 聖安東尼的誘惑 Martin Schongauer The Temptation of St Anthony.jpg',
}
GALLERY = ['anthony','bellini','leonardo','durer','jerome','francis','magdalen','bosch','hospitality','serapion','paul','latour']

# Each text entrance follows a phrase break in the supplied narration.
DATA = {
7: {'title':'Anthony among the demons', 'footer':'MICHELANGELO  /  THE TORMENT OF SAINT ANTHONY  /  KIMBELL ART MUSEUM', 'scenes':[
 {'start':0,'heading':['A young artist.','An early painting.'],'eyebrow':'1487  /  ABOUT TWELVE YEARS OLD','notes':[(0.8,['Michelangelo learns','by looking closely.'])],'layout':'hero','arts':['anthony'],'captions':['Michelangelo · The Torment of Saint Anthony']},
 {'start':7.98,'heading':['Frantic movement.','A composed face.'],'eyebrow':'LOOK AT THE CONTRAST','notes':[(8.3,['Monsters pull at his clothing.']),(12.35,['Anthony holds his expression.'])],'layout':'hero','arts':['anthony'],'captions':['Turmoil around him · stillness at the center'],'focus':[(8.4,.72,.40,.13),(12.35,.43,.28,.075)]},
 {'start':16.32,'heading':['Borrowed lines.','A new painting.'],'eyebrow':'LEARNING THROUGH IMITATION','notes':[(16.7,['Schongauer’s engraving']),(20.28,['Color · animal textures','a quiet landscape']),(24.66,['Fish-market study:','reported by early biographers'])],'layout':'duo','arts':['schongauer','anthony'],'captions':['Martin Schongauer · engraving','Michelangelo · painting'],'connector':True},
 {'start':29.30,'heading':['Imitation becomes','an individual vision.'],'eyebrow':'THE COMMISSION REMAINS UNCERTAIN','notes':[(31.66,['Learning from a model.']),(36.03,['Making the image his own.']),(38.38,['Return to Anthony’s face.'])],'layout':'hero','arts':['anthony'],'captions':['Restless creatures · a still expression'],'focus':[(38.38,.43,.28,.075)]},
]},
8: {'title':'A panel regains a name', 'footer':'MICHELANGELO  /  THE TORMENT OF SAINT ANTHONY  /  ATTRIBUTION AND OBJECT HISTORY', 'scenes':[
 {'start':0,'heading':['Research changes','an artwork’s identity.'],'eyebrow':'AN ATTRIBUTION UNDER REVIEW','notes':[(.7,['The same panel.','A changing understanding.'])],'layout':'hero','arts':['anthony'],'captions':['The painting as a physical object']},
 {'start':4.45,'heading':['2008 to 2009'],'eyebrow':'A MODERN TURNING POINT','notes':[(4.8,['2008 · Changed hands as a','Ghirlandaio workshop attribution.']),(10.25,['Cleaning and further study.']),(13.79,['2009 · Acquired by the Kimbell','as Michelangelo’s earliest painting.'])],'layout':'hero','arts':['anthony'],'captions':['Attribution develops through research'],'timeline':True},
 {'start':19.53,'heading':['Beneath the surface.','Beyond the image.'],'eyebrow':'LAYERS OF EVIDENCE','notes':[(19.8,['Imaging reveals drawings','beneath the painted surface.']),(22.95,['Study helps reconstruct','how the work developed.']),(25.97,['Early ownership still has gaps.'])],'layout':'hero','arts':['anthony'],'captions':['Painting · underdrawing · ownership history'],'evidence':True},
 {'start':29.28,'heading':['An image has','an object history.'],'eyebrow':'THE RECORD IS STILL INCOMPLETE','notes':[(29.7,['Religious scene','and material object.']),(36.08,['The visible image is','part of the evidence.']),(39.35,['Childhood biographies cannot','fill every ownership gap.'])],'layout':'duo','arts':['schongauer','anthony'],'captions':['A source for the composition','A panel with its own history'],'gaps':True},
]},
14: {'title':'Prayer gathers in the shadows', 'footer':'FRANCISCO DE ZURBARÁN  /  SAINT FRANCIS IN MEDITATION  /  NATIONAL GALLERY, LONDON', 'scenes':[
 {'start':0,'heading':['Saint Francis','in Meditation'],'eyebrow':'C. 1635–1639','notes':[(3.31,['Francisco de Zurbarán']),(7.35,['National Gallery, London'])],'layout':'hero','arts':['meditation'],'captions':['A rough habit · a skull · concentrated prayer']},
 {'start':9.86,'heading':['Light finds','the rough cloth.'],'eyebrow':'POVERTY MADE VISIBLE','notes':[(10.2,['Patches and heavy folds.']),(14.8,['A face held in shadow.']),(16.74,['Raised head.','Hands around a skull.'])],'layout':'hero','arts':['meditation'],'captions':['Follow the light, then the hands'],'focus':[(10.2,.44,.55,.14),(14.8,.64,.19,.10),(16.74,.70,.48,.13)]},
 {'start':21.45,'heading':['A skull becomes','a focus for prayer.'],'eyebrow':'MORTALITY AND DEVOTION','notes':[(21.8,['Mortality and Christ’s','crucifixion.']),(26.11,['Catholic reform’s','devotional culture.']),(28.84,['An image that sustains prayer.'])],'layout':'hero','arts':['meditation'],'captions':['The skull invites reflection'],'focus':[(21.8,.68,.43,.12)]},
 {'start':31.42,'heading':['An expansive world.','A concentrated image.'],'eyebrow':'TWO VISUAL EXPERIENCES','notes':[(33.77,['Cloth.']),(35.81,['Light.']),(36.76,['Gesture.'])],'layout':'duo','arts':['bellini','meditation'],'captions':['Bellini · the open landscape','Zurbarán · a spare setting']},
 {'start':39.68,'heading':['Where does','your eye settle?'],'eyebrow':'LOOKING WITH ATTENTION','notes':[(42.3,['Little surrounding detail.']),(44.84,['Stillness becomes','hard to leave.'])],'layout':'hero','arts':['meditation'],'captions':['A head raised · hands gathered'],'focus':[(40,.64,.19,.1),(44.84,.70,.48,.13)]},
 {'start':49.50,'heading':['Stillness.','Different responses.'],'eyebrow':'A HISTORY OF RECEPTION','notes':[(50,['Its austerity once','drew criticism.']),(52.63,['Viewers have not always','responded in the same way.'])],'layout':'hero','arts':['meditation'],'captions':['A spare image can hold a complex response']},
]},
24: {'title':'Different paths of religious commitment', 'footer':'SAINT SERAPION  /  THE PENITENT MAGDALEN  /  DISTINCT STORIES AND CONTEXTS', 'scenes':[
 {'start':0,'heading':['At the edges','of asceticism.'],'eyebrow':'KEEP THE STORIES DISTINCT','notes':[(.7,['Two images.','Different religious traditions.'])],'layout':'duo','arts':['serapion','magdalen'],'captions':['Zurbarán · Saint Serapion','La Tour · The Penitent Magdalen']},
 {'start':3.78,'heading':['Serapion:','remembered as a martyr.'],'eyebrow':'MARTYRDOM','notes':[(6.74,['Violence inflicted on him.']),(11.29,['Chosen poverty and discipline','require a different context.'])],'layout':'hero','arts':['serapion'],'captions':['A community remembers martyrdom']},
 {'start':12.68,'heading':['Magdalen:','a penitential tradition.'],'eyebrow':'LATER RELIGIOUS INTERPRETATION','notes':[(17.28,['A familiar image developed','through later traditions.']),(19.93,['Its context extends beyond','the Gospel accounts.'])],'layout':'hero','arts':['magdalen'],'captions':['A later tradition pictures penitence']},
 {'start':21.86,'heading':['From a white habit','to a candle flame.'],'eyebrow':'LOOK AT THE VISUAL LANGUAGE','notes':[(22.3,['Both suggest deep','religious commitment.']),(27.08,['Their subjects arrive there','through different stories.'])],'layout':'duo','arts':['serapion','magdalen'],'captions':['White cloth · martyrdom','Candlelight · penitence']},
 {'start':30.45,'heading':['Looking carefully','means knowing the story.'],'eyebrow':'CONTEXT SHAPES UNDERSTANDING','notes':[(30.8,['Chosen discipline.']),(33.98,['Inflicted suffering.']),(35.6,['Later traditions of repentance.'])],'layout':'duo','arts':['serapion','magdalen'],'captions':['Serapion · martyrdom','Magdalen · penitential tradition']},
]},
29: {'title':'A word becomes a way of looking', 'footer':'ASCETIC  /  LIGHT, CLOTH, LINES AND BODIES  /  ATTENTION MADE VISIBLE', 'scenes':[
 {'start':0,'heading':['One word.','Many ways of living.'],'eyebrow':'ASCETIC','notes':[(1.6,['Anthony · enduring turmoil.']),(4.77,['Francis · choosing poverty.']),(6.94,['Jerome · studying.']),(8.95,['Paul · welcoming a guest.'])],'layout':'gallery','arts':GALLERY,'captions':[],'gallery_focus':[(1.6,0),(4.77,5),(6.94,3),(8.95,8)]},
 {'start':12.32,'heading':['Different lives.','Different contexts.'],'eyebrow':'SERAPION AND MAGDALEN','notes':[(12.7,['Chosen discipline.']),(16.52,['Inflicted suffering.']),(18.5,['Later traditions of repentance.'])],'layout':'duo','arts':['serapion','magdalen'],'captions':['Martyrdom','Penitential tradition']},
 {'start':21.89,'heading':['The inward life','becomes visible.'],'eyebrow':'HOW ARTISTS SHOW COMMITMENT','notes':[(22.1,['Light.']),(23.66,['Cloth.']),(25.3,['Engraved lines.']),(27.1,['Bodies.'])],'layout':'quad','arts':['magdalen','meditation','durer','anthony'],'captions':['LIGHT','CLOTH','ENGRAVED LINES','BODIES']},
 {'start':29.23,'heading':['Pause over','one small action.'],'eyebrow':'A WAY OF LOOKING','notes':[(29.6,['Hands in prayer.']),(30.88,['A head over a book.']),(33.3,['A face toward light.'])],'layout':'trio','arts':['meditation','durer','bellini'],'captions':['Hands in prayer','A head over a book','A face toward light']},
 {'start':37.12,'heading':['Where is','their attention?'],'eyebrow':'LOOK AGAIN','notes':[(37.5,['What are they trying','to sustain?'])],'layout':'gallery','arts':GALLERY,'captions':[]},
]},
}


@lru_cache(maxsize=64)
def font(size, kind=SANS):
    return ImageFont.truetype(kind, round(size*S))


def ease(value):
    x=max(0,min(1,value))
    return 1-(1-x)**3


@lru_cache(maxsize=512)
def text(lines,size=34,kind=SANS,color=CREAM):
    f=font(size,kind)
    probe=ImageDraw.Draw(Image.new('RGB',(1,1)))
    width=max(probe.textbbox((0,0),line,font=f)[2] for line in lines)
    assert width<=1720*S,(lines,width)
    layer=Image.new('RGBA',(width+6*S,round((len(lines)*size*1.24+10)*S)))
    d=ImageDraw.Draw(layer)
    for i,line in enumerate(lines):d.text((0,round(i*size*1.24*S)),line,font=f,fill=color)
    return layer


def put(canvas,layer,x,y,alpha=1):
    if alpha<=0:return
    if alpha<.999:
        layer=layer.copy()
        layer.putalpha(layer.getchannel('A').point(lambda a:round(a*alpha)))
    canvas.alpha_composite(layer,(round(x*S),round(y*S)))


def enter(canvas,layer,x,y,t,start,duration=.55):
    e=ease((t-start)/duration)
    put(canvas,layer,x,y+24*(1-e),e)


@lru_cache(maxsize=24)
def artwork(key):
    with Image.open(ART/FILES[key]) as im:return im.convert('RGB')


@lru_cache(maxsize=80)
def panel(key,width,height):
    im=Image.new('RGBA',(round(width*S),round(height*S)))
    ImageDraw.Draw(im).rounded_rectangle((1,1,im.width-2,im.height-2),radius=10*S,fill='#100f0d',outline='#795c38',width=2)
    fitted=ImageOps.contain(artwork(key),(round((width-24)*S),round((height-24)*S)),Image.Resampling.LANCZOS).convert('RGBA')
    offset=((im.width-fitted.width)//2,(im.height-fitted.height)//2)
    im.alpha_composite(fitted,offset)
    return im,offset,fitted.size


def caption(canvas,lines,x,y,width,t,start):
    layer=text(tuple(lines),18,SANS,MUTED)
    # Captions must stay inside their artwork column.
    assert layer.width<=width*S,(lines,width,layer.width)
    enter(canvas,layer,x,y,t,start)


def base(n):
    # Build at logical size, then enlarge the texture; all text remains native UHD.
    yy,xx=np.mgrid[0:1080,0:1920]
    glow=np.exp(-(((xx/1920-.48)/.8)**2+((yy/1080-.4)/.95)**2)*2)
    grain=np.random.default_rng(2).normal(0,.45,glow.shape)
    arr=np.stack([25+17*glow+grain,19+13*glow+grain,13+8*glow+grain],axis=-1).clip(0,255).astype(np.uint8)
    bg=Image.fromarray(arr).resize((W,H),Image.Resampling.BICUBIC).convert('RGBA')
    d=ImageDraw.Draw(bg)
    for y in [210,1004]:d.line((110*S,y*S,1810*S,y*S),fill='#705537',width=2)
    put(bg,text(('OUR FAMOUS ARTISTS  /  LOOKING CLOSELY',),18,BOLD,GOLD),110,48)
    put(bg,text((DATA[n]['title'],),51,SERIF),110,100)
    put(bg,text((DATA[n]['footer'],),14,BOLD,MUTED),110,1024)
    put(bg,text((f'{n:02d}',),18,BOLD,GOLD),1765,1020)
    return bg


def art_layout(canvas,scene,t):
    start=scene['start'];layout=scene['layout'];keys=scene['arts'];captions=scene.get('captions',[])
    if layout=='hero':
        x,y,width,height=1050,248,690,688
        card,offset,size=panel(keys[0],width,height)
        enter(canvas,card,x,y,t,start,.65)
        caption(canvas,captions,x,953,width,t,start+.25)
        active=[f for f in scene.get('focus',[]) if t>=f[0]]
        if active:
            s,nx,ny,r=active[-1];e=ease((t-s)/.65)
            cx=x*S+offset[0]+nx*size[0];cy=y*S+offset[1]+ny*size[1]
            radius=r*min(size)*(1+.045*math.sin((t-s)*2))
            d=ImageDraw.Draw(canvas)
            d.arc((cx-radius,cy-radius,cx+radius,cy+radius),-90,-90+359*e,fill=GOLD,width=3*S)
            d.line((cx+radius,cy,cx+radius+70*S*e,cy),fill=GOLD,width=2*S)
    elif layout in ('duo','trio','quad'):
        if layout=='duo': width,height,cols,dx,dy,y0=400,596,2,442,0,280
        elif layout=='trio':width,height,cols,dx,dy,y0=264,560,3,288,0,294
        else:width,height,cols,dx,dy,y0=392,286,2,440,340,268
        for i,key in enumerate(keys):
            x=950+(i%cols)*dx;y=y0+(i//cols)*dy
            card,_,_=panel(key,width,height)
            enter(canvas,card,x,y,t,start+i*.2,.65)
            lines=split_caption(captions[i],29 if layout=='trio' else 39)
            caption(canvas,lines,x,y+height+18,width,t,start+i*.2+.2)
        if scene.get('connector'):
            e=ease((t-start-.7)/1.3);d=ImageDraw.Draw(canvas)
            d.line((1357*S,560*S,(1357+30*e)*S,560*S),fill=GOLD,width=3*S)
            if e>.95:d.polygon([(1387*S,560*S),(1377*S,554*S),(1377*S,566*S)],fill=GOLD)
    elif layout=='gallery':
        for i,key in enumerate(keys):
            x=950+(i%4)*218;y=270+(i//4)*220
            card,_,_=panel(key,196,188)
            enter(canvas,card,x,y,t,start+i*.055,.55)
        active=[f for f in scene.get('gallery_focus',[]) if t>=f[0]]
        if active:
            s,i=active[-1];x=950+(i%4)*218;y=270+(i//4)*220
            d=ImageDraw.Draw(canvas)
            d.rounded_rectangle((x*S-5,y*S-5,(x+196)*S+5,(y+188)*S+5),radius=11*S,outline=GOLD,width=3*S)


def split_caption(value,limit):
    words=value.split();lines=[];line=''
    for word in words:
        if len(line+' '+word)>limit and line:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    if line:lines.append(line)
    return lines


def render(n,t,bg,duration):
    scene=max((s for s in DATA[n]['scenes'] if s['start']<=t),key=lambda s:s['start'])
    start=scene['start'];canvas=bg.copy()
    enter(canvas,text((scene['eyebrow'],),19,BOLD,GOLD),110,275,t,start)
    heading=text(tuple(scene['heading']),54,SERIF)
    assert heading.width<810*S,(n,scene['heading'])
    enter(canvas,heading,110,332,t,start+.12)
    y=538 if len(scene['heading'])==2 else 465
    for when,lines in scene.get('notes',[]):
        layer=text(tuple(lines),28,SANS,MUTED)
        assert layer.width<790*S,(n,lines)
        enter(canvas,layer,137,y,t,when)
        if t>=when:
            d=ImageDraw.Draw(canvas)
            d.line((111*S,(y+13)*S,111*S,(y+37)*S),fill=GOLD,width=3*S)
        y+=len(lines)*35+28
    art_layout(canvas,scene,t)
    d=ImageDraw.Draw(canvas)
    if scene.get('timeline'):
        e=ease((t-start)/7)
        d.line((110*S,820*S,(110+650*e)*S,820*S),fill=GOLD,width=3*S)
        for x,label,when in [(110,'2008',start),(680,'2009',13.79)]:
            if t>=when:
                d.ellipse(((x-6)*S,814*S,(x+6)*S,826*S),fill=GOLD)
                enter(canvas,text((label,),21,BOLD,GOLD),x,845,t,when)
    if scene.get('gaps'):
        for x in range(110,660,28):
            d.line((x*S,840*S,(x+12)*S,840*S),fill='#8b7251',width=2*S)
        enter(canvas,text(('GAPS IN THE EARLY OWNERSHIP RECORD',),16,BOLD,GOLD),110,871,t,start+.4)
    if scene.get('evidence'):
        for i,label in enumerate(['PAINT','DRAWINGS','RECORDS']):
            x=110+i*220
            e=ease((t-start-i)/.7)
            d.line((x*S,850*S,(x+175*e)*S,850*S),fill=GOLD,width=2*S)
            enter(canvas,text((label,),17,BOLD,GOLD),x,870,t,start+i)
    d.line((110*S,1004*S,(110+1700*min(1,t/duration))*S,1004*S),fill=GOLD,width=3*S)
    return canvas.convert('RGB')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--slide',type=int,required=True,choices=sorted(DATA))
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args();n=args.slide
    folder=ROOT/f'animation/slide_{n:03d}';folder.mkdir(exist_ok=True)
    audio=ROOT/f'audio/ascetic_en_{n:03d}_explainer_narration.wav'
    output=ROOT/f'video/ascetic_en_{n:03d}_explainer_4k.mp4'
    with wave.open(str(audio)) as w:duration=w.getnframes()/w.getframerate()
    bg=base(n)
    samples=[]
    scenes=DATA[n]['scenes']
    for i,s in enumerate(scenes):
        end=scenes[i+1]['start'] if i+1<len(scenes) else duration
        samples.append(max(s['start']+.7,end-.7))
    sheet=Image.new('RGB',(1920,540*math.ceil(len(samples)/2)),'#15100c')
    for i,t in enumerate(samples):
        im=render(n,t,bg,duration);im.thumbnail((960,540));sheet.paste(im,((i%2)*960,(i//2)*540))
    sheet.save(folder/'storyboard.jpg',quality=94)
    render(n,samples[0],bg,duration).save(folder/'preview_4k.png')
    if args.preview:return
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(audio),'-map','0:v:0','-map','1:a:0','-vf','setsar=1','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart',str(output)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for frame in range(math.ceil(duration*FPS)):
            process.stdin.write(render(n,frame/FPS,bg,duration).tobytes())
            if frame%300==0:print(f'Slide {n:02d}: {frame/FPS:.0f}/{duration:.2f} seconds',flush=True)
        process.stdin.close()
        if process.wait()!=0:raise RuntimeError('FFmpeg encoding failed')
    finally:
        if process.poll() is None:process.terminate()
    raw=(ROOT/'ascetic_subtitle_en_20min.txt').read_text()
    narration=re.search(rf'(?ms)^\[Page {n}\]\s*\n(.*?)(?=^\[Page|\Z)',raw).group(1).strip()
    (folder/'narration_en.txt').write_text(narration+'\n')
    manifest={'slide':n,'source_slide':str(ROOT/f'ascetic_en/ascetic_en.{n:03d}.png'),'narration_source':str(ROOT/'ascetic_subtitle_en_20min.txt'),'video':str(output),'audio':str(audio),'duration_seconds':duration,'dimensions':[W,H],'fps':FPS,'voice':'en-US-AndrewMultilingualNeural','rate':'-3%','scenes':scenes,'artwork_files':{k:str(ART/FILES[k]) for k in set(key for s in scenes for key in s['arts'])}}
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Completed {output}',flush=True)


if __name__=='__main__':main()
