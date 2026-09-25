from pathlib import Path
import win32com.client
root=Path('D:/mcp/arts/American Gothic')
app=win32com.client.DispatchEx('PowerPoint.Application')
try:
    for lang in ('tw','en'):
        p=root/('tw_slides' if lang=='tw' else 'en_slides')/'Grant_Wood_Three_Works.pptx'
        out=Path('D:/mcp/arts/.build/ag_render')/lang
        out.mkdir(parents=True,exist_ok=True)
        deck=app.Presentations.Open(str(p),WithWindow=False,ReadOnly=True)
        try:
            for i,s in enumerate(deck.Slides,1):s.Export(str(out/f'{i:02}.png'),'PNG',1280,720)
            print(lang,len(deck.Slides),deck.PageSetup.SlideWidth,deck.PageSetup.SlideHeight)
        finally:deck.Close()
finally:app.Quit()
