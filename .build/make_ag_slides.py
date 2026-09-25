from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import shutil, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('D:/mcp/arts/American Gothic')
IMG=ROOT/'images'
BG=ROOT/'slide_backgrounds'
BG.mkdir(exist_ok=True)
TOPIC='Grant_Wood_Three_Works'
STYLE=Path('C:/Users/yingyuhsieh/.codex/generated_images/01a0d3dd-3c82-7c13-9017-d870d37b9539/exec-0c18bd07-b855-4b1f-bd23-84ca5cbbce03.png')
STICKER=Path('D:/mcp/arts/.codex/skills/create-youtube-slides/assets/end_sticker.png')
W,H=13.333,7.5
bg=Image.open(STYLE).convert('RGB')
bw,bh=bg.size
target_ratio=16/9
if bw/bh>target_ratio:
    nw=int(bh*target_ratio); bg=bg.crop(((bw-nw)//2,0,(bw+nw)//2,bh))
else:
    nh=int(bw/target_ratio); bg=bg.crop((0,(bh-nh)//2,bw,(bh+nh)//2))
bg=bg.resize((1280,720),Image.Resampling.LANCZOS)
for i in range(1,8): bg.save(BG/f'{TOPIC}_background_{i:03}.png')
Image.new('RGB',(1280,720),(243,239,226)).save(BG/f'{TOPIC}_background_008.png')

slides=[
 dict(image='Woman with Plants.jpg',layout='portrait',kind='hook',
      tw_title='名畫之前的一張臉',en_title='A face before the icon',
      tw_body='從母親肖像到美國鄉村，伍德讓平凡人物帶著難以讀透的表情直視我們。',
      en_body='Before American Gothic, Wood gave ordinary people a poised, hard-to-read presence.',
      tw_id='格蘭特・伍德，《手捧植物的婦人》，1929\n油彩、Upson 板｜錫達拉皮茲藝術博物館',
      en_id='Grant Wood, Woman with Plants, 1929\nOil on Upson board | Cedar Rapids Museum of Art',
      source='https://www.crma.org/exhibitions/current/Grant_Wood_From_Farm_Boy_to_American_Icon',
      image_url='https://commons.wikimedia.org/wiki/File:Woman_with_Plants,_by_Grant_Wood.jpg'),
 dict(image='Woman with Plants.jpg',layout='portrait',kind='detail',
      tw_title='植物撐起端正姿態',en_title='The plant holds the pose',
      tw_body='筆直的虎尾蘭、交疊的雙手、平靜的面容，讓母親像一座安靜的紀念碑。',
      en_body='Upright leaves, folded hands, and a steady face give his mother a monument-like stillness.',
      tw_id='《手捧植物的婦人》細看｜1929',en_id='Woman with Plants, closer look | 1929',
      source='https://www.crma.org/grant-wood',image_url='https://commons.wikimedia.org/wiki/File:Woman_with_Plants,_by_Grant_Wood.jpg'),
 dict(image='Daughters of Revolution.jpg',layout='wide',kind='artwork',
      tw_title='愛國肖像裡的刺',en_title='A patriotic portrait with a bite',
      tw_body='三位婦女站在華盛頓渡河圖前。莊重的排列，藏著尖銳的幽默。',
      en_body='Three women stand before Washington crossing the Delaware. The formal pose carries a sharp joke.',
      tw_id='格蘭特・伍德，《革命之女》，1932\n油彩、Masonite 板｜辛辛那提美術館',
      en_id='Grant Wood, Daughters of Revolution, 1932\nOil on Masonite | Cincinnati Art Museum',
      source='https://collection.cincinnatiartmuseum.org/objects/118432/daughters-of-revolution',
      image_url='https://commons.wikimedia.org/wiki/File:Daughters_of_Revolution.jpg'),
 dict(image='Daughters of Revolution.jpg',layout='wide',kind='detail',
      tw_title='茶杯與歷史畫的反問',en_title='A cup, a painting, a question',
      tw_body='小小的茶杯和背後的《華盛頓橫渡德拉瓦河》，把家常儀式與國家神話放在同一個畫面。',
      en_body='A small teacup meets an epic national image, turning a polite gathering into a question about patriotism.',
      tw_id='《革命之女》細看｜1932',en_id='Daughters of Revolution, closer look | 1932',
      source='https://www.cincinnatiartmuseum.org/art/exhibitions/exhibition-archive/2014-exhibitions/conversations-around-american-gothic/',
      image_url='https://commons.wikimedia.org/wiki/File:Daughters_of_Revolution.jpg'),
 dict(image='Dinner for Threshers.jpg',layout='panorama',kind='artwork',
      tw_title='剖開農舍的一餐',en_title='A farmhouse opened like a stage',
      tw_body='伍德把整棟農舍攤開：屋外、長桌和廚房，同時進入我們的視線。',
      en_body='Wood opens the farmhouse so we can see the yard, the long table, and the kitchen at once.',
      tw_id='格蘭特・伍德，《打穀工的晚餐》，1934\n油彩、硬質纖維板｜舊金山美術館',
      en_id='Grant Wood, Dinner for Threshers, 1934\nOil on hardboard | Fine Arts Museums of San Francisco',
      source='https://www.nga.gov/stories/articles/west-east/modernist-barns-and-modern-farmers',
      image_url='https://www.nga.gov/sites/default/files/styles/image_scale_height__700/public/migrate_images/content/dam/ngaweb/stories/2024/west-to-east---midwest/grantwood_dinnerforthreshers.jpg?itok=f84AJFIs'),
 dict(image='Dinner for Threshers.jpg',layout='panorama',kind='detail',
      tw_title='誰讓這頓飯成為可能？',en_title='Who makes the meal possible?',
      tw_body='男人坐在長桌旁，女人在右側廚房備餐。畫面同時呈現收成與照料的勞動。',
      en_body='Men gather at the table while women prepare food at right. The harvest depends on both kinds of work.',
      tw_id='《打穀工的晚餐》細看｜1934',en_id='Dinner for Threshers, closer look | 1934',
      source='https://whitney.org/media/36752',image_url='https://www.nga.gov/sites/default/files/styles/image_scale_height__700/public/migrate_images/content/dam/ngaweb/stories/2024/west-to-east---midwest/grantwood_dinnerforthreshers.jpg?itok=f84AJFIs'),
 dict(image=None,layout='synthesis',kind='conclusion',
      tw_title='同一畫風，三種情緒',en_title='One style, three moods',
      tw_body='端正的母親、挖苦的群像、忙碌的農舍。伍德的精準畫法，讓日常生活充滿張力。',
      en_body='A solemn mother, a pointed satire, and a busy farmhouse reveal the range inside Wood’s careful style.',
      tw_id='伍德，1929–1934',en_id='Wood, 1929–1934',
      source='https://www.crma.org/grant-wood',image_url=''),
]

nar={
'tw':[
'《美國哥德式》讓伍德家喻戶曉，但在那把草叉之外，他還畫過什麼？我們從一張母親肖像出發，接著看三位自信的婦女，最後走進一棟正在吃晚餐的農舍。三件作品都以精準的線條描繪中西部生活，情緒卻各不相同。',
'這位婦人是伍德的母親海蒂。她身穿黑衣，綠色圍裙的邊緣被一道道花邊仔細勾出。先看她交疊的手，再看從盆中直直長出的虎尾蘭。植物和身體都幾乎不偏不倚，讓肖像顯得沉穩。遠處的農舍與田地卻把她留在真實生活裡。錫達拉皮茲藝術博物館指出，伍德在慕尼黑研究北方文藝復興繪畫後，開始以這樣精密的方式安排人物、衣著和物件。畫中的尊嚴來自這位母親本身，也來自畫家給日常細節的耐心。',
'再看這三位站在一起的婦女。伍德把她們放在一幅《華盛頓橫渡德拉瓦河》的圖像前，像是在替愛國精神拍一張正式合照。題名《革命之女》也讓人想到美國革命女兒會。辛辛那提美術館把此作與《美國哥德式》並置，邀請觀眾思考小鎮生活、刻板印象與美國身分。畫面表面安靜，眼神和嘴角卻讓這份莊重顯得有些僵硬。我們可以讀出諷刺，但不必假裝每個表情都有唯一答案。',
'請注意中間婦女舉起的茶杯。那個日常小動作，剛好擋在她們身後的宏大歷史畫前。後方畫的是華盛頓率眾渡河的英雄場面，前方則是三張幾乎不露情緒的臉。兩種尺度被壓在同一平面上，讓崇高的國家故事突然變得可以被質疑。這種幽默並不需要人物大笑。伍德以整齊的姿態、緊密的人物排列和冷靜的筆法，把不舒服的感覺留給觀眾。你看到的是敬意、挖苦，還是兩者並存？',
'到了《打穀工的晚餐》，伍德把人物肖像擴展成整棟農舍。這幅長而窄的畫，讓我們像站在舞台前，看見左側屋外、中間的餐桌與右側的廚房。打穀季的勞動需要大量人手，吃飯也成為農場一天的重要節點。畫家沒有只畫一位英雄，而是讓許多人同時出現。整齊的空間與排列使場面近乎儀式，卻仍保留家務與農務的具體動作。這種把平凡生活安排得如此莊重的方式，是伍德地域主義繪畫令人難忘的力量。',
'把眼光從長桌移向畫面右邊。坐著吃飯的工人是最先吸引人的群體，但廚房裡也有人正在備餐。伍德的剖面構圖讓兩種勞動同時可見，觀眾能看見一頓飯如何被組織起來。左側的屋外場景又提醒我們，這餐與田間的收成緊緊相連。整幅畫像一條橫向的時間線，把工作、用餐與照料連成一件事。它很有秩序，也讓我們思考：誰的工作通常被看見，誰的工作容易退到背景？',
'回頭看這三件作品，伍德的畫法始終精確，情緒卻從親密走向挖苦，再轉成集體的忙碌。母親手中的盆栽、婦女舉起的茶杯、農舍裡的一張長桌，都是日常物件。伍德把它們安排得異常清晰，於是我們開始重新看待那些看似熟悉的美國生活。',
'感謝你的觀看，期待下次再一起看畫！'],
'en':[
'American Gothic made Grant Wood famous, but what else did he paint beyond that pitchfork? We begin with a portrait of his mother, then meet three women posing before a patriotic image, and finally enter a farmhouse at dinnertime. The same exacting style holds these scenes together, while each carries a different mood.',
'This is Wood’s mother, Hattie. Her black dress and green apron are described with deliberate care. Follow her folded hands, then the long leaves rising straight from the pot. The plant and the figure share an upright stillness, yet the farm buildings behind her keep the portrait tied to ordinary life. The Cedar Rapids Museum of Art explains that Wood studied Northern Renaissance painting during a trip to Munich and then began staging people, clothes, objects, and landscapes with great precision. Here that precision gives a familiar person uncommon gravity. The painting asks us to spend time with a face that reveals little, while the hands and the plant quietly carry much of its meaning.',
'Now the portrait widens to three women. They stand before an image of Washington crossing the Delaware, as if they have assembled for a formal photograph of patriotic virtue. The title points to the Daughters of the American Revolution. Cincinnati Art Museum has placed this painting beside American Gothic to invite questions about small town life, stereotypes, and national identity. The women remain composed, yet their fixed expressions make the ceremony feel tense. Wood leaves room for humor and discomfort. We can recognize the satire without pretending that every look on every face has only one meaning.',
'Look first at the teacup in the central woman’s hand. This small, polite gesture sits in front of a dramatic history painting of Washington leading his troops across the river. Wood compresses a domestic ritual and a national legend into the same shallow space. The contrast makes the grand story feel open to scrutiny. No one needs to laugh for the picture to be funny. The tight grouping, stiff posture, and calm paint surface do the work. Its question lingers after we look away: are these women honoring a national ideal, guarding it, or exposing how awkwardly it can be performed?',
'Dinner for Threshers expands Wood’s stage from a portrait to an entire farmhouse. The long, narrow composition opens the building like a cutaway. We can see the outdoor yard at left, a crowded meal at the center, and food preparation at right. Threshing season demanded many hands, and a shared dinner marked a pause in that work. Wood gives us no single hero. Instead, he organizes a community across the length of the picture. The measured architecture and repeated figures make the event feel almost ceremonial, while the everyday tasks remain visible. This is one way his Regionalist painting grants weight to ordinary rural life.',
'Move your eye from the long table to the kitchen on the right. The seated workers catch our attention first, but other people are still preparing the meal. Wood’s open-house composition allows both kinds of work to appear at once. The yard on the left links the dinner to labor in the fields. Across the painting, work, eating, and care form one continuous scene. Its orderly structure can make the household look harmonious, yet it also invites a sharper question. Whose work becomes the center of the story, and whose work is usually pushed to its edge? The painting gives us enough space to notice both.',
'Across these three works, Wood’s careful surfaces stay consistent while the feeling changes. His mother’s plant carries quiet dignity. A teacup sharpens a satire. A long table turns farm labor into a collective scene. Each object is ordinary, but Wood arranges it so precisely that familiar American life begins to feel strange again. That tension is part of what keeps these pictures alive.',
'Thank you for watching. I hope you will join us for another look at art soon!']}

nar['tw'][1]+=' 她身後的地平線低而平，讓人先遇見她的目光，再慢慢注意到故鄉景色。盆栽遮住部分衣襟，卻把粗糙的手襯得更醒目。這些選擇不是照片式的偶然，而是畫家一步步安排出的觀看順序。'
nar['tw'][2]+=' 畫中的背景並非真正的戰場，而是另一幅名畫的再現。伍德讓歷史圖像變成室內裝飾，也讓站在前方的人物像在替它作證。'
nar['tw'][3]+=' 再比較三人的位置。她們肩膀相近，卻沒有真正互相交談；視線更像越過觀眾或停在觀眾身上。茶杯帶來社交場合的禮節，畫中的沉默卻使這份禮節變得緊張。伍德沒有在畫面寫下判決，而是讓物件與表情彼此牽制。'
nar['tw'][4]+=' 從左到右觀看，空間一段接著一段，卻沒有被牆完全隔開。這種安排讓觀眾可以同時看見農場運作的不同環節，也讓畫面看起來像一座精心搭建的模型。'
nar['tw'][5]+=' 屋外有人停下來，屋內有人就座，廚房仍有動作。這些差異讓畫面不只是同一瞬間的合照，更像對一天節奏的整理。長桌提供視覺中心，兩端的空間則提醒我們，一頓飯從來不只發生在餐桌上。'
nar['tw'][6]+=' 下一次再看到《美國哥德式》的嚴肅面孔，也許可以想想：同一位畫家如何在另一張臉、一只茶杯和一座農舍裡，留下截然不同的問題。'
nar['en'][1]+=' The low horizon behind her slows our gaze. We meet her face first, then discover the small buildings and fields. The pot partly covers her clothing but makes her working hands more noticeable. These are deliberate choices about how we encounter a person, not the accidents of a snapshot.'
nar['en'][2]+=' The scene behind them is not a battlefield seen through a window. It is an image of another painting, brought into the room as decoration. Wood lets the women stand in front of a national story, as if they might speak for it.'
nar['en'][3]+=' Notice how close the women stand without seeming to speak to one another. Their gazes travel outward, or settle on us, rather than meeting across the group. The cup suggests sociable manners, while the silence makes those manners feel strained. Wood offers no written verdict. He lets objects and expressions pull against each other, so the viewer has to decide how far the joke reaches.'
nar['en'][4]+=' Follow the painting from left to right. One space leads into the next, yet the walls never completely hide what is happening elsewhere. That arrangement lets us see several parts of farm life at the same time. The building begins to resemble a carefully assembled model, scaled to make a complex working day legible.'
nar['en'][5]+=' Outside, someone pauses. Inside, others sit down, while movement continues in the kitchen. These differences make the scene more than a group portrait of one instant. The long table anchors our view, but the spaces at either end remind us that a meal begins before anyone takes a seat and continues beyond the diners we notice first.'
nar['en'][6]+=' The next time you meet the stern faces of American Gothic, remember that the same painter could use another face, a teacup, or a farmhouse to ask a very different question.'

def add_text(slide,text,x,y,w,h,size,color,bold=False,align=None,font='Aptos'):
    box=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=box.text_frame; tf.clear(); tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(.02); tf.margin_top=tf.margin_bottom=0
    p=tf.paragraphs[0]; p.text=text; p.font.name=font; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor(*color)
    if align is not None: p.alignment=align
    return box

def add_art(slide,path,x,y,w,h):
    im=Image.open(path); iw,ih=im.size
    ratio=min(w/iw,h/ih); rw=iw*ratio; rh=ih*ratio
    slide.shapes.add_picture(str(path),Inches(x+(w-rw)/2),Inches(y+(h-rh)/2),width=Inches(rw),height=Inches(rh))

def add_paper_band(slide,x,y,w,h):
    band=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    band.fill.solid();band.fill.fore_color.rgb=RGBColor(248,246,237)
    band.line.fill.background()

for lang in ('tw','en'):
    out=ROOT/('tw_slides' if lang=='tw' else 'en_slides'); out.mkdir(exist_ok=True)
    prs=Presentation();prs.slide_width=Inches(W);prs.slide_height=Inches(H)
    for idx,data in enumerate(slides,1):
        slide=prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(str(BG/f'{TOPIC}_background_{idx:03}.png'),0,0,width=prs.slide_width,height=prs.slide_height)
        title=data[f'{lang}_title'];body=data[f'{lang}_body'];ident=data[f'{lang}_id']
        font='Microsoft JhengHei' if lang=='tw' else 'Aptos'
        if data['layout']=='portrait':
            add_art(slide,IMG/data['image'],0.85,1.42,5.0,5.65)
            add_paper_band(slide,6.15,5.31,6.12,1.83)
            add_text(slide,title,6.30,1.46,6.1,1.18,35,(43,48,43),True,font=font)
            add_text(slide,body,6.30,3.06,5.93,1.67,21,(51,57,52),font=font)
            add_text(slide,ident,6.30,5.48,5.9,.78,14,(81,81,71),font=font)
            add_text(slide,'Cedar Rapids Museum of Art / Wikimedia Commons',6.30,6.82,5.9,.24,9,(92,91,77),font=font)
        elif data['layout']=='wide':
            add_text(slide,title,1.06,.55,11.4,.68,34,(42,48,43),True,font=font)
            add_art(slide,IMG/data['image'],1.09,1.64,11.16,3.85)
            add_paper_band(slide,.92,5.49,11.51,1.58)
            add_text(slide,body,1.11,5.58,11.0,.82,19,(45,52,47),font=font)
            add_text(slide,ident,1.11,6.37,9.25,.56,11,(77,80,69),font=font)
            add_text(slide,'Cincinnati Art Museum / Wikimedia Commons',9.00,6.87,3.35,.19,8,(95,93,81),align=PP_ALIGN.RIGHT,font=font)
        elif data['layout']=='panorama':
            add_text(slide,title,1.04,.55,11.4,.68,34,(42,48,43),True,font=font)
            add_art(slide,IMG/data['image'],.72,1.75,11.9,3.76)
            add_paper_band(slide,.91,5.54,11.53,1.54)
            add_text(slide,body,1.05,5.63,11.2,.80,18,(45,52,47),font=font)
            add_text(slide,ident,1.05,6.40,9.5,.52,11,(77,80,69),font=font)
            add_text(slide,'© Figge Art Museum / VAGA; image: NGA',8.62,6.89,3.63,.18,8,(95,93,81),align=PP_ALIGN.RIGHT,font=font)
        else:
            add_text(slide,title,1.03,.62,11.4,.73,34,(42,48,43),True,font=font)
            pics=['Woman with Plants.jpg','Daughters of Revolution.jpg','Dinner for Threshers.jpg']
            for j,pic in enumerate(pics): add_art(slide,IMG/pic,1.00+j*4.12,1.70,3.72,3.33)
            add_paper_band(slide,.91,5.49,11.53,1.58)
            add_text(slide,body,1.03,5.58,11.2,1.02,20,(45,52,47),font=font)
            add_text(slide,ident,1.03,6.77,5.2,.23,10,(77,80,69),font=font)
            add_text(slide,'CRMA · Cincinnati Art Museum · NGA / © Figge Art Museum / VAGA',5.43,6.77,6.87,.23,8,(95,93,81),align=PP_ALIGN.RIGHT,font=font)
        slide.notes_slide.notes_text_frame.text=f"Sources: {data['source']}\nArtwork image: {data['image_url']}"
    slide=prs.slides.add_slide(prs.slide_layouts[6])
    bgp=BG/f'{TOPIC}_background_008.png'
    # Required end slide uses a plain fill and one centered sticker object.
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb=RGBColor(243,239,226)
    sw,sh=Image.open(STICKER).size
    hh=4.5; ww=hh*sw/sh
    slide.shapes.add_picture(str(STICKER),Inches((W-ww)/2),Inches((H-hh)/2),width=Inches(ww),height=Inches(hh))
    prs.save(out/f'{TOPIC}.pptx')
    lines=[]
    for i,s in enumerate(nar[lang],1): lines.extend([f'[Page {i}]',s])
    (out/f'{TOPIC}_subtitle.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(out/f'{TOPIC}.pptx',len(prs.slides))
print('backgrounds',len(list(BG.glob(f'{TOPIC}_background_*.png'))))
