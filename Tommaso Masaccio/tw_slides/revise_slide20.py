"""Restyle the user-supplied three-artwork slide 20 without altering other slides."""
from pathlib import Path
from datetime import datetime
import ast
import shutil
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
helper_path = HERE / 'layout_revision.py'
tree = ast.parse(helper_path.read_text(encoding='utf-8'))
definitions = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'existing_backups' for t in node.targets):
        break
    definitions.append(node)
scope = {'__file__': str(helper_path), '__name__': 'slide20_helpers'}
exec(compile(ast.Module(body=definitions, type_ignores=[]), str(helper_path), 'exec'), scope)

target = HERE / 'update' / '馬薩喬：讓繪畫重新站在地面上_slide_0020.PNG'
backup = HERE / ('slide20_before_restyle_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png')
shutil.copy2(target, backup)
source = Image.open(backup).convert('RGB')
assert source.size == (1280, 720)

scope['start'](20, '一座給後世畫家的學校', '從街道、身體與量體，看見馬薩喬留給後世的觀看方法')
panels = [
    ((86,165,386,615), '街道中的空間', '聖彼得以影子治癒病人', '建築與人物前後排列，\n讓奇蹟發生在可信的街道中。'),
    ((467,165,824,615), '可感的身體', '新信徒受洗', '明暗塑造肌肉與姿態，\n讓身體的寒冷與緊張可被感受。'),
    ((920,165,1192,615), '穩定的量體', '聖安妮與聖母子', '衣褶、膝部與支撐的手勢，\n賦予聖母與聖嬰厚實的重量。'),
]
for i, (crop, heading, label, body) in enumerate(panels):
    x = 54 + i * 397
    scope['rect']((x, 140, x+378, 672))
    art = ImageOps.contain(source.crop(crop), (680, 666), Image.Resampling.LANCZOS)
    px = int((x+189)*2-art.width/2)
    py = int(155*2+(666-art.height)/2)
    scope['canvas'].paste(art, (px,py))
    scope['caption'](label, (x+14,501,350,30), 19)
    scope['text'](heading, (x+22,546,334,42), 27, True, scope['TEAL'])
    scope['text'](body, (x+22,598,334,66), 21)

scope['save'](20)
staged = scope['STAGE'] / (scope['PREFIX'] + '0020.png')
with Image.open(staged) as check:
    check.load()
    assert check.size == (1280,720)
staged.replace(target)
print(f'Saved: {target}')
print(f'Backup: {backup}')
