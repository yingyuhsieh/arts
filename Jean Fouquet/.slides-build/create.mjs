import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const ROOT='D:/mcp/arts/Jean Fouquet';
const BUILD=ROOT+'/.slides-build';
const RT='C:/Users/yingyuhsieh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const req=createRequire(RT+'/stub.cjs');
const sharp=req('sharp');
const {Presentation,PresentationFile}=await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const pages=JSON.parse(await fs.readFile(BUILD+'/data.json','utf8'));
const assets=JSON.parse(await fs.readFile(BUILD+'/asset-map.json','utf8'));
const sources=JSON.parse(await fs.readFile(BUILD+'/sources.json','utf8'));
const imageUrls=JSON.parse(await fs.readFile(BUILD+'/images.json','utf8'));
const bgDir=ROOT+'/slide_backgrounds';await fs.mkdir(bgDir,{recursive:true});
const bg=await sharp(await fs.readFile(BUILD+'/assets/background-master.png')).resize(1280,720,{fit:'fill'}).png().toBuffer();
for(let i=0;i<pages.length;i++){
 const dest=bgDir+'/jean_fouquet_artworks_background_'+String(i+1).padStart(3,'0')+'.png';
 if(i===pages.length-1) await sharp({create:{width:1280,height:720,channels:3,background:'#F7F1E5'}}).png().toFile(dest);
 else await fs.writeFile(dest,bg);
}
const navy='#172F63',red='#8E302C',ink='#34404B';
const rawCache=new Map();
async function addImage(s,file,box,alt){
 let bytes=rawCache.get(file);if(!bytes){bytes=await fs.readFile(file);rawCache.set(file,bytes);}
 const m=await sharp(bytes).metadata();const scale=Math.min(box.width/m.width,box.height/m.height);
 const w=m.width*scale,h=m.height*scale;
 return s.images.add({blob:new Uint8Array(bytes),contentType:m.format==='png'?'image/png':'image/jpeg',alt,fit:'contain',position:{left:box.left+(box.width-w)/2,top:box.top+(box.height-h)/2,width:w,height:h}});
}
function text(s,name,value,x,y,w,h,size,font,color=navy,bold=false){
 const q=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 q.text=value;q.text.style={fontSize:size,typeface:font,color,bold,autoFit:'none',wrap:'square',verticalAlignment:'top',insets:0};return q;
}
for(const [lang,idx] of [['tw',0],['en',1]]){
 const outDir=ROOT+'/'+lang+'_slides';await fs.mkdir(outDir,{recursive:true});await fs.mkdir(BUILD+'/renders/'+lang,{recursive:true});
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 const font=lang==='tw'?'Microsoft JhengHei':'Georgia';const bodyfont=lang==='tw'?'Microsoft JhengHei':'Arial';
 for(let i=0;i<pages.length;i++){
  const d=pages[i],s=p.slides.add();s.background.fill='#F7F1E5';
  if(d.kind==='end'){
   await addImage(s,assets.sticker,{left:424,top:144,width:432,height:432},'Our Famous Artists channel end sticker');
   s.speakerNotes.text=d[lang];
  }else{
   s.images.add({blob:new Uint8Array(bg),contentType:'image/png',alt:'Reusable decorative illuminated manuscript background',position:{left:0,top:0,width:1280,height:720}});
   if(d.kind==='context'){
    text(s,'title',d.title[idx],100,92,1080,90,48,font);
    text(s,'lost-work',d.body[idx],100,260,1080,150,40,font,red);
    text(s,'evidence',d.detail[idx],100,455,1000,100,28,bodyfont,ink);
   }else if(d.layout==='wide'){
    text(s,'title',d.title[idx],150,84,1000,78,46,font);
    await addImage(s,assets[d.image],{left:88,top:165,width:865,height:455},d.caption[1]);
    text(s,'observation',d.body[idx],985,270,205,235,lang==='tw'?27:25,bodyfont,red);
   }else{
    const cover=d.kind==='hook';
    text(s,'title',d.title[idx],100,cover?155:108,480,cover?205:180,cover?54:48,font);
    text(s,'observation',d.body[idx],100,cover?408:345,480,150,cover?28:27,bodyfont,cover?red:ink);
    await addImage(s,assets[d.image],{left:635,top:77,width:545,height:520},d.caption[1]);
   }
   text(s,'identification',d.caption[idx],210,632,920,58,17,bodyfont,ink);

   const src=sources[d.src]; const refs=(src.text.split('## 主要參考資料')[1]||'')+'\n'+(d.extraSource||'');
   s.speakerNotes.text=d[lang]+'\n\nSource document: artworks/'+src.n+'\n'+refs+'\nImage: user-supplied historical reproduction, '+(assets[d.image]||'No image used for the lost original.')+'\n'+(imageUrls[d.image]||'')+'\nVisual interpretation follows the supplied research. Decorative background is non-factual and separate from the historical image.';
  }
  await fs.writeFile(BUILD+'/renders/'+lang+'/slide-'+String(i+1).padStart(2,'0')+'.png',new Uint8Array(await (await p.export({slide:s,format:'png',scale:1})).arrayBuffer()));
  console.log(lang+' rendered '+(i+1));
 }
 const draft=BUILD+'/'+lang+'-draft.pptx';await (await PresentationFile.exportPptx(p)).save(draft);
 await fs.writeFile(outDir+'/jean_fouquet_artworks_subtitle.txt',pages.map((d,i)=>'[Page '+(i+1)+']\n'+d[lang]).join('\n')+'\n','utf8');
 
 console.log('DRAFT '+draft);
}
