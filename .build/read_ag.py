from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
root = Path('D:/mcp/arts')
for p in (root/'American Gothic').rglob('*'):
    if p.is_file():
        print('FILE', p.relative_to(root), p.stat().st_size)
        if p.name == 'Artworks similar to American Gothic.txt' or p.parent.name == 'artworks' and p.name in ('Grant Wood 1929 Woman with Plants.md', 'Grant Wood 1932 Daughters of Revolution.md', 'Grant Wood 1934 Dinner for Threshers.md'):
            try: print(p.read_text(encoding='utf-8'))
            except Exception as e: print('READ ERROR', e)
print('PRESENTATION SKILL')
print(Path('C:/Users/yingyuhsieh/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations/SKILL.md').read_text(encoding='utf-8'))
