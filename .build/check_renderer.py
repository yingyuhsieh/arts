from pathlib import Path
import importlib.util
print('win32com',bool(importlib.util.find_spec('win32com')))
for p in [Path('C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE'),Path('C:/Program Files/LibreOffice/program/soffice.exe'),Path('C:/Program Files (x86)/LibreOffice/program/soffice.exe')]:print(p,p.exists())
