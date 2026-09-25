from pathlib import Path
import urllib.request
from PIL import Image
root=Path('D:/mcp/arts/American Gothic')
out=root/'images'
out.mkdir(exist_ok=True)
files={
 'Woman with Plants.jpg':'Woman_with_Plants%2C_by_Grant_Wood.jpg',
 'Daughters of Revolution.jpg':'Daughters_of_Revolution.jpg',
 'Dinner for Threshers.jpg':'Grant_Wood_-_Dinner_for_Threshers.jpg',
}
for name,wiki in files.items():
    req=urllib.request.Request('https://commons.wikimedia.org/wiki/Special:Redirect/file/'+wiki,headers={'User-Agent':'CodexArtResearch/1.0 (art slides)'})
    with urllib.request.urlopen(req,timeout=30) as r:
        b=r.read(); url=r.geturl()
    p=out/name;p.write_bytes(b)
    im=Image.open(p); im.verify()
    print(name,len(b),url)
