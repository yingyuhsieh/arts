import urllib.request,urllib.parse,json,re,html,concurrent.futures
from pathlib import Path
b=Path(__file__).parent
c=json.loads((b/'image_candidates.json').read_text('utf8')); sel=json.loads((b/'selection.json').read_text('utf8'))
assets=b.parent/'images'; assets.mkdir(exist_ok=True)
def fetch(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ArtEducation/1.0 (educational slides)'}),timeout=60).read()
def get(item):
 key,(page,i)=item; a=c[page][i]; src=a['src'].split('?')[0]; src='https:'+src if src.startswith('//') else src
 src=src.replace('upload.wikimedia.org','thumb.wikimedia.org')
 original=src.replace('/thumb/','/').rsplit('/',1)[0]
 url=re.sub(r'/[0-9]+px-', '/1280px-',src)
 filepage='https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(urllib.parse.unquote(a['resource'].split('File:')[1]))
 try:
  data=fetch(url); ext='.png' if '.png' in original.lower() else '.jpg'; fn='Andrea Mantegna '+key+ext; (assets/fn).write_bytes(data)
  try:
   t=fetch(filepage).decode(); (b/(key+'_credit.html')).write_text(t,encoding='utf8')
   licenses=re.findall(r'(?:Public domain|CC BY-SA[^<]{0,25}|CC BY[^<]{0,25}|Creative Commons[^<]{0,80})',t,re.I)
  except Exception as e: licenses=[str(e)]
  return key,dict(path=str(assets/fn),url=url,page=filepage,licenses=list(set(licenses))[:8])
 except Exception as e:return key,dict(error=str(e),url=url,page=filepage)
r=dict(concurrent.futures.ThreadPoolExecutor(max_workers=2).map(get,sel.items())); (b/'assets.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
for k,v in r.items():print(k,v.get('error','OK'),v.get('licenses',''))
