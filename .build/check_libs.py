import importlib.util,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
for n in ('pptx','PIL','fitz','cairosvg'):
 print(n, bool(importlib.util.find_spec(n)))
for n in ('soffice','libreoffice','node'):
 print(n,shutil.which(n))
