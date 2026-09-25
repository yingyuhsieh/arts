from pathlib import Path
import urllib.request
root=Path('D:/mcp/arts')
for p in root.rglob('*'):
    if p.is_file() and any(x in p.name.lower() for x in ('plants','daughters','threshers','gothic')): print('IMAGE',p)
for p in (Path('C:/Users/yingyuhsieh/.codex/plugins/cache/openai-primary-runtime')).rglob('artifact-tool'):
    print('ARTIFACT',p)
u='https://commons.wikimedia.org/wiki/Special:Redirect/file/Woman_with_Plants%2C_by_Grant_Wood.jpg'
try:
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'CodexArtResearch/1.0'}),timeout=15)
    print('URL',r.status,r.geturl(),r.headers.get('Content-Type'))
except Exception as e: print('NETWORK ERROR',repr(e))
