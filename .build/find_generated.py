from pathlib import Path
r=Path('C:/Users/yingyuhsieh/.codex/generated_images')
print('EXISTS',r.exists())
if r.exists():
 for p in sorted(r.rglob('*'),key=lambda x:x.stat().st_mtime if x.exists() else 0,reverse=True)[:20]: print(p,p.stat().st_size)
