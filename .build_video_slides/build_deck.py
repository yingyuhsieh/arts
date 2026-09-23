from __future__ import annotations

import datetime as dt
import html
import os
import shutil
import zipfile
from pathlib import Path


ROOT = Path('/Users/yingyuhsieh/Desktop/mcp/arts')
BUILD = ROOT / '.build_video_slides'
OUT = ROOT / 'output' / '霧海上的漫遊者_解開名畫謎團.pptx'
STAGE = BUILD / 'pptx_pkg'

W, H = 12192000, 6858000
FONT = 'PingFang TC'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def emu(px: float) -> int:
    return round(px * 9525)


def color(hex_color: str) -> str:
    return hex_color.replace('#', '').upper()


def shape_rect(idx, name, x, y, w, h, fill, alpha=100000, line=None, radius=False):
    geom = 'roundRect' if radius else 'rect'
    line_xml = '<a:ln><a:noFill/></a:ln>' if not line else f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{color(line)}"/></a:solidFill></a:ln>'
    return f'''<p:sp>
      <p:nvSpPr><p:cNvPr id="{idx}" name="{esc(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
      <a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{color(fill)}"><a:alpha val="{alpha}"/></a:srgbClr></a:solidFill>{line_xml}</p:spPr>
      <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="zh-TW"/></a:p></p:txBody>
    </p:sp>'''


def text_box(idx, name, text, x, y, w, h, size=24, fill='#263532', bold=False,
             align='l', valign='mid', font=FONT, margin=0, italic=False):
    lines = text.split('\n')
    paras = []
    for line in lines:
        paras.append(f'''<a:p><a:pPr algn="{align}"/><a:r><a:rPr lang="zh-TW" sz="{int(size*100)}" b="{1 if bold else 0}" i="{1 if italic else 0}"><a:solidFill><a:srgbClr val="{color(fill)}"/></a:solidFill><a:latin typeface="{esc(font)}"/><a:ea typeface="{esc(font)}"/><a:cs typeface="{esc(font)}"/></a:rPr><a:t>{esc(line)}</a:t></a:r><a:endParaRPr lang="zh-TW" sz="{int(size*100)}"/></a:p>''')
    return f'''<p:sp>
      <p:nvSpPr><p:cNvPr id="{idx}" name="{esc(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
      <p:txBody><a:bodyPr wrap="square" anchor="{valign}" lIns="{emu(margin)}" rIns="{emu(margin)}" tIns="{emu(margin)}" bIns="{emu(margin)}"/><a:lstStyle/>{''.join(paras)}</p:txBody>
    </p:sp>'''


def line_shape(idx, x1, y1, x2, y2, stroke='#566B67', width=2):
    return f'''<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{idx}" name="Line {idx}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>
    <p:spPr><a:xfrm><a:off x="{emu(x1)}" y="{emu(y1)}"/><a:ext cx="{emu(x2-x1)}" cy="{emu(y2-y1)}"/></a:xfrm><a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="{emu(width)}"><a:solidFill><a:srgbClr val="{color(stroke)}"/></a:solidFill></a:ln></p:spPr></p:cxnSp>'''


def pic(idx, name, rid, x, y, w, h, line='#D8D7CF'):
    line_xml = '<a:ln><a:noFill/></a:ln>' if not line else f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{color(line)}"/></a:solidFill></a:ln>'
    return f'''<p:pic><p:nvPicPr><p:cNvPr id="{idx}" name="{esc(name)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
    <p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
    <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{line_xml}</p:spPr></p:pic>'''


def slide_xml(elements):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
{''.join(elements)}
</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


def rels_xml(rels):
    body = ''.join(f'<Relationship Id="{rid}" Type="{typ}" Target="{esc(target)}"/>' for rid, typ, target in rels)
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>'


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def add_slide(n, content_builder, media_paths):
    rels = [('rId1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', '../slideLayouts/slideLayout1.xml')]
    rid_map = {}
    for i, pth in enumerate(media_paths, start=2):
        ext = Path(pth).suffix.lower().lstrip('.')
        target_name = f's{n}_img{i-1}.{ext}'
        shutil.copy2(pth, STAGE / 'ppt' / 'media' / target_name)
        rid = f'rId{i}'
        rid_map[Path(pth).name] = rid
        rels.append((rid, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', f'../media/{target_name}'))
    elems = content_builder(rid_map)
    write(STAGE / 'ppt' / 'slides' / f'slide{n}.xml', slide_xml(elems))
    write(STAGE / 'ppt' / 'slides' / '_rels' / f'slide{n}.xml.rels', rels_xml(rels))


def bg(rids, idx=2):
    return pic(idx, 'Misty oil landscape background', rids['misty_background.png'], 0, 0, 1280, 720, line=None)


def footer(idx, text):
    return text_box(idx, 'Source', text, 70, 677, 1140, 20, 10.5, '#4D5E5B', False, 'r', 'mid')


def build():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    (STAGE / 'ppt' / 'media').mkdir(parents=True)

    background = BUILD / 'misty_background.png'
    painting = BUILD / 'painting.jpg'
    monk = BUILD / 'monk_art.jpg'
    composite = BUILD / 'composite.jpg'
    portrait = BUILD / 'portrait_art.jpg'
    rugen = BUILD / 'rugen_art.jpg'
    window = BUILD / 'window_art.jpg'
    moon = BUILD / 'moon_art.jpg'
    title_img = BUILD / 'title.jpg'

    def s1(r):
        return [bg(r), shape_rect(3,'Title veil',55,80,790,420,'#F2F3EF',82000, radius=True),
                text_box(4,'Title','霧海上的漫遊者',85,135,720,95,50,'#26332F',True,'l','mid'),
                text_box(5,'Subtitle','解開名畫謎團',90,235,650,60,27,'#465C57',False,'l','mid'),
                text_box(6,'Question','為何一個沒有臉的背影，\n能讓兩百年後的觀眾看見自己？',90,330,650,110,25,'#2F3E3A',False,'l','mid'),
                text_box(7,'Artwork','Caspar David Friedrich，約 1817 年',90,510,600,35,15,'#5E6C68',False,'l','mid'),
                footer(8,'內容來源：〈霧海上的漫遊者：解開名畫謎團〉影片')]

    def s2(r):
        return [bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',87000, radius=True),
                text_box(4,'Title','背影人物：一場強迫性的邀請',75,60,1020,58,34,'#253631',True,'l','mid'),
                text_box(5,'German term','Rückenfigur',75,130,430,48,24,'#60736D',False,'l','mid',italic=True),
                text_box(6,'Body','觀眾看不見人物的表情，只能沿著他的視線望向霧海。\n\n空白的臉讓情緒投射成為可能。背影人物因此成為觀眾在畫中的替身，也成為人與自然之間的橋樑。',75,195,650,300,22,'#293936',False,'l','top'),
                pic(7,'Wanderer artwork crop',r['painting.jpg'],825,135,330,422),
                text_box(8,'Caption','沒有表情，卻容納每位觀眾的情緒',780,575,420,35,17,'#425651',True,'c','mid'),
                footer(9,'影片 01:43–02:21')]

    def s3(r):
        return [bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',88000, radius=True),
                text_box(4,'Title','尺度與構圖改變了觀看的位置',75,60,1100,58,34,'#253631',True,'l','mid'),
                text_box(5,'Intro','《霧海上的漫遊者》把人物放大並置於中央。《海邊的修士》則讓人幾乎消失在天地之間。',75,125,1110,55,20,'#334641',False,'l','mid'),
                pic(6,'Wanderer composition',r['painting.jpg'],95,205,330,420),
                pic(7,'Monk by the Sea',r['monk_art.jpg'],600,235,560,337),
                text_box(8,'Left caption','人物主導畫面\n勝利感與不安同時存在',445,315,135,110,17,'#40544F',True,'c','mid'),
                text_box(9,'Right caption','人物被自然壓縮成微小尺度',635,585,485,30,17,'#40544F',True,'c','mid'),
                footer(10,'影片 02:27–03:32')]

    def s4(r):
        return [bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',90000, radius=True),
                text_box(4,'Title','現實中不存在的觀景台',75,60,1100,58,34,'#253631',True,'l','mid'),
                text_box(5,'Body','這幅風景不是單一地點的紀錄。\n\n弗里德里希把薩克森瑞士與波西米亞的岩石、遠山和寫生素材重新組合，形成一個屬於內在經驗的虛構風景。',75,155,475,260,22,'#293936',False,'l','top'),
                text_box(6,'Key point','自然提供素材，畫家重新安排觀看的世界',75,455,475,70,20,'#4A615B',True,'l','mid'),
                pic(7,'Composite landscape explanation',r['composite.jpg'],600,165,570,321),
                text_box(8,'Caption','影片中的地理與拼貼示意',650,505,470,35,16,'#51625E',False,'c','mid'),
                footer(9,'影片 03:36–04:11')]

    def s5(r):
        return [bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',90000, radius=True),
                text_box(4,'Title','漫遊者的身份仍無定論',75,60,1100,58,34,'#253631',True,'l','mid'),
                text_box(5,'Hypotheses','薩克森的森林官員\n\n陣亡的普魯士軍官\n\n詩人約翰・沃夫岡・馮・歌德\n\n畫家弗里德里希本人',90,150,520,330,23,'#2A3A36',False,'l','top'),
                pic(6,'Friedrich portrait',r['portrait_art.jpg'],790,135,350,399),
                shape_rect(7,'Conclusion panel',90,525,1050,76,'#DCE5E1',88000, radius=True),
                text_box(8,'Conclusion','沒有決定性史料能證實任何一種說法。無臉也因此讓他可以成為任何人。',115,537,1000,50,21,'#294039',True,'c','mid'),
                footer(9,'影片 04:13–04:55')]

    def s6(r):
        return [bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',90000, radius=True),
                text_box(4,'Title','細節讓自畫像說法變得矛盾',75,60,1100,58,34,'#253631',True,'l','mid'),
                pic(5,'Friedrich portrait detail',r['portrait_art.jpg'],85,155,350,399),
                pic(6,'Wanderer detail',r['painting.jpg'],835,155,300,384),
                text_box(7,'Comparison','史料與肖像顯示弗里德里希有紅棕色頭髮。\n\n畫中的漫遊者卻呈現明顯的金色捲髮。\n\n深綠長外套也可能指向都市旅行、戰爭記憶或古德意志政治象徵。',490,170,290,320,20,'#2E403B',False,'l','top'),
                text_box(8,'Takeaway','細節沒有關閉謎團，反而擴大了解讀空間',270,565,750,40,20,'#455E57',True,'c','mid'),
                footer(9,'影片 04:57–05:59')]

    def s7(r):
        return [bg(r), shape_rect(3,'Content veil',45,35,1190,630,'#F6F5F0',90000, radius=True),
                text_box(4,'Title','背影人物構成一整個觀看宇宙',70,55,1120,55,34,'#253631',True,'l','mid'),
                pic(5,'Chalk Cliffs on Rügen',r['rugen_art.jpg'],65,145,335,422),
                pic(6,'Woman at a Window',r['window_art.jpg'],472,145,298,422),
                pic(7,'Two Men Contemplating the Moon',r['moon_art.jpg'],845,175,360,292),
                text_box(8,'Rugen caption','《呂根島的白堊崖》\n美與墜落危機並存',65,575,335,55,16.5,'#374B45',True,'c','mid'),
                text_box(9,'Window caption','《窗邊的女人》\n室內通往精神世界',455,575,335,55,16.5,'#374B45',True,'c','mid'),
                text_box(10,'Moon caption','《兩人觀月》\n背影也能代表陪伴',845,575,360,55,16.5,'#374B45',True,'c','mid'),
                footer(11,'影片 06:12–07:22')]

    def s8(r):
        return [bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',90000, radius=True),
                text_box(4,'Title','經典畫名其實來得很晚',75,60,1100,58,34,'#253631',True,'l','mid'),
                text_box(5,'Body','弗里德里希沒有留下今日通行的畫名。\n「霧海上的漫遊者」到 1950 年代才逐漸確立。',95,145,1080,78,21,'#2D403A',False,'c','mid'),
                pic(6,'Naming history frame',r['title.jpg'],150,250,980,551),
                shape_rect(7,'Mask lower crop',130,566,1020,112,'#F4F3EE',100000),
                text_box(8,'Naming comparison','1950 年代：詩意名稱逐漸固定\n1959 年英國展覽：仍稱「迷霧風景中的登山者」',160,570,960,78,19,'#354943',True,'c','mid'),
                footer(9,'影片 07:28–07:56')]

    def s9(r):
        e=[bg(r), shape_rect(3,'Content veil',50,38,1180,620,'#F6F5F0',91000, radius=True),
           text_box(4,'Title','收藏史留下約 120 年的空白',75,60,1100,58,34,'#253631',True,'l','mid'),
           text_box(5,'Intro','作品約在 1817 年完成，但可追查的流傳紀錄直到 1938 年左右才重新出現。',90,130,1080,55,21,'#31443E',False,'l','mid'),
           line_shape(6,145,340,1135,340,'#627771',3),
           shape_rect(7,'Gap highlight',145,318,515,44,'#B9C8C3',48000, radius=True),
           text_box(8,'Gap label','約 120 年紀錄空白',265,250,280,45,20,'#40564F',True,'c','mid')]
        points=[(145,'約 1817','完成'),(660,'1938／39','重新出現'),(810,'1950','畫名固定'),(955,'1959','英國展覽'),(1135,'1970','進入漢堡美術館收藏')]
        idx=9
        for x,year,label in points:
            e.append(shape_rect(idx,f'Point {year}',x-8,332,16,16,'#6C3F2D',100000,radius=True)); idx+=1
            e.append(text_box(idx,f'Year {year}',year,x-65,370,130,28,16,'#2C3E38',True,'c','mid')); idx+=1
            e.append(text_box(idx,f'Label {label}',label,x-85,405,170,45,13.5,'#53635F',False,'c','top')); idx+=1
        e += [shape_rect(idx,'Caveat',100,520,1080,72,'#E5E8E3',90000,radius=True),
              text_box(idx+1,'Caveat text','影片提到 1930 年代畫商與納粹時期藝術估價的關聯，但目前沒有證據顯示本畫涉及不當掠奪。',125,530,1030,52,18,'#384A45',False,'c','mid'),
              footer(idx+2,'影片 07:57–08:36')]
        return e

    def s10(r):
        return [bg(r), shape_rect(3,'Closing veil',70,70,1140,570,'#EDEFEA',76000, radius=True),
                text_box(4,'Title','崇高感來自無法消除的不確定',105,105,1070,68,35,'#263832',True,'c','mid'),
                text_box(5,'Summary','霧氣揭露山峰，也隱藏深淵。\n沒有臉的男人、拼貼的風景、斷裂的歷史，\n共同把畫作變成承接恐懼、渴望與迷惘的容器。',160,220,960,160,25,'#30443D',False,'c','mid'),
                text_box(6,'Question','你準備好成為步入未知的漫遊者了嗎？',135,450,1010,75,31,'#4D3329',True,'c','mid'),
                footer(7,'影片 08:37–09:43')]

    slides = [
        (s1,[background]), (s2,[background,painting]), (s3,[background,painting,monk]),
        (s4,[background,composite]), (s5,[background,portrait]), (s6,[background,portrait,painting]),
        (s7,[background,rugen,window,moon]), (s8,[background,title_img]), (s9,[background]), (s10,[background])
    ]
    for n,(builder,media) in enumerate(slides,1):
        add_slide(n,builder,media)

    slide_ids = ''.join(f'<p:sldId id="{255+n}" r:id="rId{n+1}"/>' for n in range(1,11))
    write(STAGE/'ppt'/'presentation.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{slide_ids}</p:sldIdLst><p:sldSz cx="{W}" cy="{H}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/></p:presentation>''')
    pres_rels=[('rId1','http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster','slideMasters/slideMaster1.xml')]
    pres_rels += [(f'rId{n+1}','http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide',f'slides/slide{n}.xml') for n in range(1,11)]
    write(STAGE/'ppt'/'_rels'/'presentation.xml.rels', rels_xml(pres_rels))

    write(STAGE/'ppt'/'slideMasters'/'slideMaster1.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>''')
    write(STAGE/'ppt'/'slideMasters'/'_rels'/'slideMaster1.xml.rels', rels_xml([
        ('rId1','http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout','../slideLayouts/slideLayout1.xml'),
        ('rId2','http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme','../theme/theme1.xml')]))
    write(STAGE/'ppt'/'slideLayouts'/'slideLayout1.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>''')
    write(STAGE/'ppt'/'slideLayouts'/'_rels'/'slideLayout1.xml.rels', rels_xml([('rId1','http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster','../slideMasters/slideMaster1.xml')]))

    write(STAGE/'ppt'/'theme'/'theme1.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Misty Romanticism"><a:themeElements><a:clrScheme name="Misty"><a:dk1><a:srgbClr val="253631"/></a:dk1><a:lt1><a:srgbClr val="F5F4EE"/></a:lt1><a:dk2><a:srgbClr val="4B3A31"/></a:dk2><a:lt2><a:srgbClr val="DDE5E3"/></a:lt2><a:accent1><a:srgbClr val="617A74"/></a:accent1><a:accent2><a:srgbClr val="6C3F2D"/></a:accent2><a:accent3><a:srgbClr val="82958F"/></a:accent3><a:accent4><a:srgbClr val="AFA98F"/></a:accent4><a:accent5><a:srgbClr val="415B65"/></a:accent5><a:accent6><a:srgbClr val="80766B"/></a:accent6><a:hlink><a:srgbClr val="415B65"/></a:hlink><a:folHlink><a:srgbClr val="6C3F2D"/></a:folHlink></a:clrScheme><a:fontScheme name="Misty Fonts"><a:majorFont><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:majorFont><a:minorFont><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:minorFont></a:fontScheme><a:fmtScheme name="Misty Format"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"/></a:gs><a:gs pos="100000"><a:schemeClr val="phClr"/></a:gs></a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill><a:noFill/></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="25400"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="38100"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>''')

    write(STAGE/'ppt'/'presProps.xml','''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>''')
    write(STAGE/'ppt'/'viewProps.xml','''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:normalViewPr/><p:slideViewPr/><p:notesTextViewPr/><p:gridSpacing cx="72008" cy="72008"/></p:viewPr>''')
    write(STAGE/'ppt'/'tableStyles.xml','''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>''')

    write(STAGE/'docProps'/'app.xml','''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>10</Slides><Notes>0</Notes><HiddenSlides>0</HiddenSlides><MMClips>0</MMClips><ScaleCrop>false</ScaleCrop><Company>OpenAI</Company><AppVersion>1.0</AppVersion></Properties>''')
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
    write(STAGE/'docProps'/'core.xml',f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>霧海上的漫遊者：解開名畫謎團</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>''')
    write(STAGE/'_rels'/'.rels', rels_xml([
        ('rId1','http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument','ppt/presentation.xml'),
        ('rId2','http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties','docProps/core.xml'),
        ('rId3','http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties','docProps/app.xml')]))

    overrides=''.join(f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for n in range(1,11))
    defaults='<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="jpg" ContentType="image/jpeg"/>'
    write(STAGE/'[Content_Types].xml',f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">{defaults}<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/><Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/><Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>{overrides}</Types>''')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
        for p in STAGE.rglob('*'):
            if p.is_file():
                z.write(p,p.relative_to(STAGE).as_posix())
    print(OUT)


if __name__ == '__main__':
    build()
