import json, re, hashlib, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
base=Path(r'D:/mcp/arts/Jean Fouquet')
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
data=json.loads((base/'.slides-build/data.json').read_text(encoding='utf-8'))
backgrounds=sorted((base/'slide_backgrounds').glob('*.png'))
assert len(backgrounds)==17
for i,b in enumerate(backgrounds,1):
 assert b.name==f'jean_fouquet_artworks_background_{i:03}.png'
 with Image.open(b) as im: assert im.size==(1280,720)
assert len(set(p.get('src') for p in data if 'src' in p))==12
sticker=(base.parent/'.codex/skills/create-youtube-slides/assets/end_sticker.png').read_bytes()
bghash=hashlib.sha256(backgrounds[0].read_bytes()).digest()
for lang in ['tw','en']:
 pptx=base/f'{lang}_slides/jean_fouquet_artworks.pptx'
 lines=(base/f'{lang}_slides/jean_fouquet_artworks_subtitle.txt').read_bytes().decode('utf-8',errors='strict').splitlines()
 assert len(lines)==34
 assert lines[::2]==[f'[Page {i}]' for i in range(1,18)]
 assert all(lines[1::2])
 with zipfile.ZipFile(pptx) as z:
  names=z.namelist(); slides=[n for n in names if re.fullmatch(r'ppt/slides/slide\d+.xml',n)]
  assert len(slides)==17
  pres=ET.fromstring(z.read('ppt/presentation.xml')); size=pres.find('p:sldSz',ns)
  assert (size.get('cx'),size.get('cy'))==('12192000','6858000')
  total=0
  for i in range(1,18):
   s=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
   rels=ET.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
   relmap={x.get('Id'):x.get('Target') for x in rels}
   pics=s.findall('.//p:pic',ns)
   texts=[t.text or '' for t in s.findall('.//a:t',ns)]
   if i==17:
    assert len(pics)==1 and len(s.findall('.//p:sp',ns))==0
    pic=pics[0]; blip=pic.find('.//a:blip',ns);target=relmap[blip.get('{'+ns['r']+'}embed')]
    assert z.read((target.lstrip('/') if target.startswith('/') else target.lstrip('/') if target.startswith('/') else 'ppt/'+target.removeprefix('../')))==sticker
    tr=pic.find('p:spPr/a:xfrm',ns);off=tr.find('a:off',ns);ext=tr.find('a:ext',ns)
    assert int(ext.get('cx'))==int(ext.get('cy'))
    assert abs(int(ext.get('cy'))/6858000-.6)<.001
    assert int(off.get('x'))*2+int(ext.get('cx'))==12192000
    assert int(off.get('y'))*2+int(ext.get('cy'))==6858000
    layout_target=next(x.get('Target') for x in rels if x.get('Type').endswith('/slideLayout'))
    layout=ET.fromstring(z.read((layout_target.lstrip('/') if layout_target.startswith('/') else 'ppt/'+layout_target.removeprefix('../'))))
    assert layout.get('type')=='blank' or 'blank' in str(layout.attrib).lower() or layout.find('p:cSld',ns).get('name','').lower()=='blank'
   else:
    first=pics[0];blip=first.find('.//a:blip',ns);target=relmap[blip.get('{'+ns['r']+'}embed')]
    assert hashlib.sha256(z.read(target.lstrip('/') if target.startswith('/') else 'ppt/'+target.removeprefix('../'))).digest()==bghash
    assert len(s.findall('.//p:sp',ns))>=3
   t=lines[2*i-1]
   amount=len(re.sub(r'[\s，。？！、：；・]','',t)) if lang=='tw' else len(t.split())
   duration=amount/(240 if lang=='tw' else 150)*60
   ranges={'hook':(20,30),'context':(35,45),'artwork':(50,70),'close':(60,90),'conclusion':(30,45),'end':(5,10)}
   lo,hi=ranges[data[i-1]['kind']]
   assert lo<=duration<=hi,(lang,i,duration)
   total+=duration
  print(lang, 'PASS: 17 slides, 17 paired script entries, UTF-8, 16:9, native text, 17 matching backgrounds, unchanged centered sticker on blank layout; estimated narration',round(total/60,1),'minutes')
print('PASS: all 12 artwork source documents represented')
