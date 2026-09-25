from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
root=Path('D:/mcp/arts/.build/ag_render')
for lang in ('tw','en'):
    ims=[]
    for p in sorted((root/lang).glob('*.png')):
        im=Image.open(p).convert('RGB').resize((640,360))
        ims.append(im)
    out=Image.new('RGB',(1280,1440),'white')
    for i,im in enumerate(ims):out.paste(im,((i%2)*640,(i//2)*360))
    out.save(root/f'{lang}_montage.jpg',quality=85)
