import urllib.request,re,json
u='https://en.wikipedia.org/wiki/Andrea_Mantegna'
r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ArtEducation/1.0'}),timeout=30)
s=r.read().decode()
print(r.status)
print(re.findall(r'<img[^>]+>',s)[:10])
