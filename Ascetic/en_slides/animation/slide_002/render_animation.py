#!/usr/bin/env python3
"""Render slide 002 as a narrated, 4K artwork explainer. No external assets."""
from pathlib import Path
import json
import math
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
SOURCE = ROOT / 'ascetic_en/ascetic_en.002.png'
AUDIO = ROOT / 'audio/ascetic_en_002_explainer_narration.wav'
OUTPUT = ROOT / 'video/ascetic_en_002_explainer_4k.mp4'
S = 2
W, H = 3840, 2160
FPS = 30
GOLD = '#d5ac67'
CREAM = '#f9ebcc'
MUTED = '#c1ab88'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SERIF = '/System/Library/Fonts/Supplemental/Georgia.ttf'


def font(size, kind=FONT):
    return ImageFont.truetype(kind, int(size * S))


def ease(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3


def text_layer(lines, size=44, kind=FONT, color=CREAM, spacing=1.23):
    f = font(size, kind)
    probe = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    width = max(probe.textbbox((0, 0), line, font=f)[2] for line in lines)
    height = int((size * spacing * len(lines) + 12) * S)
    layer = Image.new('RGBA', (width + 4 * S, height))
    d = ImageDraw.Draw(layer)
    for i, line in enumerate(lines):
        d.text((0, i * size * spacing * S), line, font=f, fill=color)
    return layer


def rect_layer(width, height, radius=12, fill='#211a12', outline=GOLD):
    im = Image.new('RGBA', (int(width * S), int(height * S)))
    ImageDraw.Draw(im).rounded_rectangle((1, 1, im.width - 2, im.height - 2), radius=radius*S, fill=fill, outline=outline, width=2)
    return im


def put(canvas, layer, x, y, alpha=1):
    if alpha <= 0:
        return
    if alpha < 0.999:
        layer = layer.copy()
        layer.putalpha(layer.getchannel('A').point(lambda a: int(a * alpha)))
    canvas.alpha_composite(layer, (round(x * S), round(y * S)))


def enter(canvas, layer, x, y, t, start, duration=.55, alpha=1):
    e = ease((t-start)/duration)
    put(canvas, layer, x, y + (1-e)*24, e*alpha)


source = Image.open(SOURCE).convert('RGB')
# The twelve complete artwork thumbnails in the reference slide, in reading order.
boxes = [
    (749,209,917,380), (937,209,1138,380), (1157,209,1316,380), (1335,209,1514,380),
    (749,397,922,569), (944,397,1125,568), (1144,397,1293,569), (1314,425,1514,541),
    (749,585,915,769), (936,585,1137,769), (1157,585,1330,769), (1347,585,1514,769),
]
artworks = [source.crop(box) for box in boxes]

# A native procedural background carries the reference slide's sepia and gold palette.
yy, xx = np.mgrid[0:H, 0:W]
glow = np.exp(-(((xx/W-.48)/.8)**2 + ((yy/H-.4)/.95)**2)*2)
grain = np.random.default_rng(2).normal(0, .45, (H,W))
arr = np.stack([25+17*glow+grain, 19+13*glow+grain, 13+8*glow+grain],axis=-1).clip(0,255).astype(np.uint8)
background = Image.fromarray(arr).convert('RGBA')
d = ImageDraw.Draw(background)
d.line((110*S,210*S,1810*S,210*S), fill='#705537', width=2)
d.line((110*S,1004*S,1810*S,1004*S), fill='#705537', width=2)
put(background,text_layer(['OUR FAMOUS ARTISTS  /  THE STORY BEHIND THE FILM'],18,BOLD,GOLD),110,48)
put(background,text_layer(['Why I made this video'],55,SERIF),110,95)
put(background,text_layer(['ONE WORD'],17,BOLD,MUTED),110,1021)
put(background,text_layer(['TWELVE ARTWORKS'],17,BOLD,MUTED),490,1021)
put(background,text_layer(['HUMAN STORIES'],17,BOLD,MUTED),965,1021)
put(background,text_layer(['02'],17,BOLD,GOLD),1760,1021)

cards=[]
for i, artwork in enumerate(artworks):
    card=rect_layer(198,192,8,'#100f0d','#5e4932')
    fit=ImageOps.contain(artwork,(182*S,164*S),Image.Resampling.LANCZOS).convert('RGBA')
    card.alpha_composite(fit,((card.width-fit.width)//2,12*S+(164*S-fit.height)//2))
    ImageDraw.Draw(card).text((10*S,175*S),f'{i+1:02d}',font=font(10,BOLD),fill=GOLD)
    cards.append(card)

labels={
 'word':text_layer(['ASCETIC'],87,SERIF),
 'intro':text_layer(['It began with a word.'],31,FONT,MUTED),
 'curious':text_layer(['Then curiosity took over.'],31,FONT,GOLD),
 'twelve':text_layer(['One question.', 'Twelve artworks.'],59,SERIF),
 'suggest':text_layer(['ChatGPT suggested works', 'connected with spiritual discipline.'],27,FONT,MUTED),
 'monsters':text_layer(['MONSTERS'],21,BOLD,GOLD),
 'wild':text_layer(['WILDERNESS'],21,BOLD,GOLD),
 'rooms':text_layer(['QUIET ROOMS'],21,BOLD,GOLD),
 'candle':text_layer(['CANDLELIGHT'],21,BOLD,GOLD),
 'qhead':text_layer(['The people behind', 'the paintings'],54,SERIF),
 'q1':text_layer(['Who were they?'],36,FONT),
 'q2':text_layer(['Why change their lives?'],36,FONT),
 'q3':text_layer(['Why did artists return', 'to their stories?'],36,FONT),
 'film':text_layer(['Those questions', 'became this film.'],60,SERIF),
 'choice':text_layer(['Following the choices', 'behind these lives.'],34,FONT,GOLD),
 'contrast':text_layer(['Different lives.', 'An inner world.'],58,SERIF),
 'struggle':text_layer(['DRAMATIC STRUGGLES'],23,BOLD,GOLD),
 'quiet':text_layer(['QUIETER MOMENTS'],23,BOLD,GOLD),
 'gesture':text_layer(['A small gesture.', 'A larger story.'],62,SERIF),
 'look':text_layer(['Look closely at the hands.'],32,FONT,GOLD),
 'francis':text_layer(['A gesture can reveal an inner life.'],23,FONT,MUTED),
}


def large_art(index,width,height):
    panel=rect_layer(width,height,12,'#100f0d','#795c38')
    fit=ImageOps.contain(artworks[index],(int((width-24)*S),int((height-24)*S)),Image.Resampling.LANCZOS).convert('RGBA')
    panel.alpha_composite(fit,((panel.width-fit.width)//2,(panel.height-fit.height)//2))
    return panel

large_struggle=large_art(0,392,570)
large_quiet=large_art(6,392,570)
large_gesture=large_art(5,730,610)


def gallery(canvas,t):
    for i,card in enumerate(cards):
        x=950+(i%4)*218
        y=286+(i//4)*220
        # Reveal the gallery as the narration moves from the word to artworks.
        start=4.65+i*.29
        e=ease((t-start)/.6)
        put(canvas,card,x,y+(1-e)*25,.18+.82*e)
    focus=None
    if 12.1<=t<13.7: focus=0
    elif 13.7<=t<14.7: focus=2
    elif 14.7<=t<15.95: focus=3
    elif 15.95<=t<17.2: focus=6
    if focus is not None:
        x=950+(focus%4)*218;y=286+(focus//4)*220
        draw=ImageDraw.Draw(canvas)
        draw.rounded_rectangle((x*S-4,y*S-4,(x+198)*S+4,(y+192)*S+4),radius=10*S,outline=GOLD,width=3*S)


def scene(canvas,t,index):
    if index<=3:
        gallery(canvas,t)
    if index==0:
        enter(canvas,labels['intro'],110,320,t,0)
        enter(canvas,labels['word'],105,378,t,.5)
        draw=ImageDraw.Draw(canvas)
        draw.line((110*S,499*S,(110+520*ease((t-.8)/1.5))*S,499*S),fill=GOLD,width=3*S)
        enter(canvas,labels['curious'],110,555,t,3.18)
    elif index==1:
        enter(canvas,labels['twelve'],110,300,t,5.62)
        enter(canvas,labels['suggest'],110,487,t,6.0)
        for key,x,y,start in [('monsters',110,638,12.15),('wild',402,638,13.72),('rooms',110,703,14.74),('candle',402,703,15.96)]:
            enter(canvas,labels[key],x,y,t,start,.35)
    elif index==2:
        enter(canvas,labels['qhead'],110,282,t,17.28)
        for key,y,start in [('q1',486,17.28),('q2',574,18.56),('q3',662,20.5)]:
            enter(canvas,labels[key],142,y,t,start,.4)
            if t>=start:
                a=ease((t-start)/.4)
                ImageDraw.Draw(canvas).ellipse((110*S,(y+14)*S,119*S,(y+23)*S),fill=GOLD)
    elif index==3:
        enter(canvas,labels['film'],110,321,t,22.63)
        enter(canvas,labels['choice'],110,555,t,24.74)
        # A drawn connector makes the progression from word to film visible.
        progress=ease((t-23)/2)
        draw=ImageDraw.Draw(canvas)
        draw.line((110*S,747*S,(110+620*progress)*S,747*S),fill=GOLD,width=3*S)
        for j in range(3):
            if progress>=j*.5:
                x=(110+j*310)*S
                draw.ellipse((x-7*S,740*S,x+7*S,754*S),fill=GOLD)
        for lines,x in [(['WORD'],110),(['QUESTION'],370),(['FILM'],670)]:
            enter(canvas,text_layer(lines,18,BOLD,MUTED),x,781,t,23,.5)
    elif index==4:
        enter(canvas,labels['contrast'],110,360,t,27.46)
        enter(canvas,large_struggle,950,285,t,27.46)
        enter(canvas,labels['struggle'],950,887,t,27.46)
        enter(canvas,large_quiet,1384,285,t,29.64)
        enter(canvas,labels['quiet'],1384,887,t,29.64)
    else:
        enter(canvas,labels['gesture'],110,365,t,31.31)
        enter(canvas,labels['look'],110,585,t,32.59)
        enter(canvas,large_gesture,1008,278,t,31.31)
        enter(canvas,labels['francis'],1008,920,t,32.59)
        # A restrained ring identifies the friar's hands, without animating the painting.
        e=ease((t-32.59)/.7)
        if e>0:
            draw=ImageDraw.Draw(canvas)
            cx,cy=1547*S,488*S
            radius=(50+9*math.sin(max(0,t-32.59)*1.7))*S
            draw.arc((cx-radius,cy-radius,cx+radius,cy+radius),-90,-90+359*e,fill=GOLD,width=3*S)
            draw.line((1740*S,488*S,(1740-120*e)*S,488*S),fill=GOLD,width=2*S)


CUTS=[0,5.62,17.28,22.63,27.46,31.31]

def frame(t):
    canvas=background.copy()
    index=max(i for i,start in enumerate(CUTS) if t>=start)
    scene(canvas,t,index)
    draw=ImageDraw.Draw(canvas)
    draw.line((110*S,1004*S,(110+1700*min(1,t/35.28))*S,1004*S),fill=GOLD,width=3*S)
    return canvas.convert('RGB')


def main():
    with wave.open(str(AUDIO)) as w:
        duration=w.getnframes()/w.getframerate()
    OUTPUT.parent.mkdir(exist_ok=True)
    samples=[2.5,11.5,16.5,21.9,26.8,30.8,34.5]
    sheet=Image.new('RGB',(1920,540*4),'#15100c')
    for i,t in enumerate(samples):
        im=frame(t)
        im.thumbnail((960,540))
        sheet.paste(im,((i%2)*960,(i//2)*540))
    sheet.save(WORK/'storyboard.jpg',quality=94)
    frame(21.9).save(WORK/'preview_4k.png')
    if '--preview' in __import__('sys').argv:
        return
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(AUDIO),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart',str(OUTPUT)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(math.ceil(duration*FPS)):
            process.stdin.write(frame(n/FPS).tobytes())
            if n%150==0: print(f'Rendered {n/FPS:.0f}/{duration:.2f} seconds',flush=True)
        process.stdin.close()
        if process.wait()!=0: raise RuntimeError('FFmpeg encoding failed')
    finally:
        if process.poll() is None: process.terminate()
    manifest={'source':str(SOURCE),'narration_source':str(ROOT/'ascetic_subtitle_en_20min.txt'),'narration_page':2,'audio':str(AUDIO),'video':str(OUTPUT),'dimensions':[W,H],'fps':FPS,'duration_seconds':duration,'voice':'en-US-AndrewMultilingualNeural','rate':'-3%','scenes':[{'start':v,'topic':topic} for v,topic in zip(CUTS,['A word sparks curiosity','Twelve artworks','Three questions','The film takes shape','Struggle and stillness','A small gesture'])]}
    (WORK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    main()
