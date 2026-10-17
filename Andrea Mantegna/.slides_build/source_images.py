import urllib.request,re,json,html,concurrent.futures
from pathlib import Path
base=Path(__file__).parent
pages=['Andrea_Mantegna','Ovetari_Chapel','Presentation_at_the_Temple_(Mantegna)','Saint_Sebastian_(Mantegna)','San_Zeno_Altarpiece','Agony_in_the_Garden_(Mantegna)','Camera_degli_Sposi','Lamentation_of_Christ_(Mantegna)','Triumphs_of_Caesar','Madonna_della_Vittoria','Parnassus_(Mantegna)','Triumph_of_the_Virtues_(Mantegna)']
def get(p):
 try:
  t=urllib.request.urlopen(urllib.request.Request('https://en.wikipedia.org/wiki/'+p,headers={'User-Agent':'ArtEducation/1.0'}),timeout=40).read().decode()
  (base/(p+'.html')).write_text(t,encoding='utf8')
  imgs=[]
  for tag in re.findall(r'<img[^>]+>',t):
   a=dict(re.findall(r'([\w-]+)="([^"]*)"',tag))
   if '/commons/' in a.get('src','') and '.svg' not in a.get('src',''): imgs.append({k:html.unescape(a.get(k,'')) for k in ['resource','src','data-file-width','data-file-height']})
  return p,imgs
 except Exception as e:return p,str(e)
results=dict(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(get,pages))
(base/'image_candidates.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
for p,items in results.items():
 print(p)
 if isinstance(items,list):
  for i,a in enumerate(items): print(i,a['resource'].split('File:')[-1],a['data-file-width'],a['data-file-height'])
 else: print(items)
