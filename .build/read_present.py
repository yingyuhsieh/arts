from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
r=Path('C:/Users/yingyuhsieh/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations')
for n in ('references/implementation.md','artifact_tool_docs/API_QUICK_START.md','references/finalization.md','style_guidelines.md'):
    print('\n\nFILE',n)
    print((r/n).read_text(encoding='utf-8'))
