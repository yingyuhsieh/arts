from pathlib import Path
from PIL import Image
import urllib.request
u='https://www.nga.gov/sites/default/files/styles/image_scale_height__700/public/migrate_images/content/dam/ngaweb/stories/2024/west-to-east---midwest/grantwood_dinnerforthreshers.jpg?itok=f84AJFIs'
p=Path('D:/mcp/arts/American Gothic/images/Dinner for Threshers.jpg')
req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req,timeout=30) as r:
 b=r.read(); print(r.status,r.headers.get('Content-Type'),r.geturl())
p.write_bytes(b)
im=Image.open(p);print(im.size)
extra=Path('D:/mcp/arts/American Gothic/images/Dinner for Threshers NGA.jpg')
if extra.exists(): extra.unlink()
