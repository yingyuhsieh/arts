from pathlib import Path
import os
r=Path('C:/Users/yingyuhsieh/.codex/plugins/cache/openai-primary-runtime')
print('R EXISTS',r.exists())
print({k:v for k,v in os.environ.items() if k.startswith('RUNTIME_')})
for p in (r/'presentations/26.905.11957/skills/presentations/container_tools').iterdir(): print('TOOL',p.name)
for q in (Path('D:/mcp/arts/.codex/skills/create-youtube-slides/assets/end_sticker.png'),Path('C:/Users/yingyuhsieh/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/node_modules')): print('EXISTS',q,q.exists())
for q in (Path('C:/Users/yingyuhsieh/AppData/Roaming/npm/node_modules/@oai/artifact-tool'), Path('D:/mcp/arts/node_modules/@oai/artifact-tool')): print('PKG',q,q.exists())
print((r/'presentations/26.905.11957/skills/presentations/container_tools/runtime_helpers.mjs').read_text(encoding='utf-8')[:10000])
