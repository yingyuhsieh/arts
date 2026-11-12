const fs = require('fs');
const path = require('path');
const {spawn} = require('child_process');
const root = path.resolve(__dirname, '../..');
const output = path.join(root, 'tw_slides/ascetic_en');
const build = path.join(__dirname, '.render');
fs.mkdirSync(output, {recursive:true}); fs.mkdirSync(build, {recursive:true});
const files = fs.readdirSync(path.join(root,'images'));
function art(prefix) {const f=files.find(f=>f.startsWith(prefix)); if(!f)throw Error(prefix);return path.join(root,'images',f);}
const A={m:art('Michelangelo '),b:art('Hieronymus Bosch '),f:art('Giovanni Bellini '),z:art('Francisco de Zurbarán 默'),l:art('Leonardo '),d:art('Albrecht '),e:art('El Greco '),j:art('懺悔中的'),v:art('聖塞拉皮翁 '),r:art('Jusepe '),s:art('Francisco de Zurbarán 聖'),g:art('Georges '),c:art('Ascetic_images_4x3')};
const names={m:'The Torment of Saint Anthony',b:'The Temptations of St. Anthony',f:'St. Francis in the Desert',z:'Saint Francis in Meditation',l:'Saint Jerome Praying in the Wilderness',d:'Saint Jerome in His Study',e:'Saint Jerome in Penitence',j:'Saint Jerome in Penitence',v:'St Anthony Abbot and St Paul the Hermit',r:'Saint Paul the Hermit',s:'Saint Serapion',g:'The Penitent Magdalen'};
const people={m:'Michelangelo',b:'Hieronymus Bosch',f:'Giovanni Bellini',z:'Francisco de Zurbarán',l:'Leonardo da Vinci',d:'Albrecht Dürer',e:'El Greco',j:'Georges de La Tour',v:'Diego Velázquez',r:'Jusepe de Ribera',s:'Francisco de Zurbarán',g:'Georges de La Tour'};
const slides=[
{n:7,title:'Anthony holds still among demons',kind:'pair',keys:['m','b'],bottom:'Michelangelo concentrates the struggle in midair.\nBosch spreads temptation across an entire world.'},
{n:8,title:'A panel regains a name',key:'m',lead:'A young artist, rediscovered',points:['Sold as a Ghirlandaio workshop painting.','The Kimbell acquired it in 2009 as the earliest known Michelangelo painting.','Technical study reveals drawing beneath the paint.'],meta:'1487 · Kimbell Art Museum'},
{n:10,title:'A quiet center in the ruins',key:'b',crop:'bosch',lead:'Faith within the disorder',points:['Anthony kneels and turns toward us.','Christ and a white-covered altar wait in the shadows behind him.','Our gaze returns to this small, steady center.'],meta:'1505–1506 · Museu Nacional de Arte Antiga · detail'},
{n:11,title:'Poverty and contemplation',kind:'pair',keys:['f','z'],bottom:'Bellini opens the view toward light and landscape.\nZurbarán gathers attention into prayer and shadow.'},
{n:12,title:'The landscape becomes part of prayer',key:'f',lead:'Open hands, open landscape',points:['Francis steps barefoot onto the rock and turns toward the light.','Plants, animals and distant homes surround his retreat.','Poverty leaves room for a connection with the world.'],meta:'c. 1475–1480 · The Frick Collection'},
{n:13,title:'A retreat still holds daily work',key:'f',crop:'francis',lead:'Books, water and a tended garden',points:['A simple dwelling still supports study and care.','A trimmed upper edge does not prove that an angel once appeared.','Material evidence helps us weigh what we imagine.'],meta:'Giovanni Bellini · The Frick Collection · detail'},
{n:14,title:'Prayer gathers in the shadows',key:'z',lead:'Rough cloth makes poverty visible',points:['Side light reveals patches and heavy folds.','A skull guides meditation on mortality.','Once criticized for its darkness, the painting now invites close attention.'],meta:'c. 1635–1639 · National Gallery, London'},
{n:15,title:'Study and penitence',kind:'four',keys:['l','d','e','j'],bottom:'Four visions of Saint Jerome\nBodily struggle and patient study express an inner discipline.'},
{n:16,title:'Prayer involves the whole body',key:'l',lead:'An unfinished painting, a damaged panel',points:['Head, arm and torso pull together in a strained pose.','Unfinished layers reveal Leonardo’s working process.','Later cut into five pieces, the panel was acquired by Pius IX in 1856.'],meta:'c. 1481–1482 · Vatican Museums'},
{n:17,title:'Discipline at a desk',key:'d',lead:'A room made for sustained attention',points:['Window light and perspective lead toward the scholar.','A skull and hourglass bring mortality and time into the room.','Engraved lines give wood, glass and fur their texture.'],meta:'1514 · Engraving · Impressions in several collections'},
{n:18,title:'Penitence comes close',key:'e',lead:'A stone, a crucifix and a searching gaze',points:['Tight space brings Jerome’s prayer close to us.','Books and a skull connect scholarship with penitence.','The red cardinal’s hat is a later artistic convention.'],meta:'c. 1595–1600 · National Galleries of Scotland'},
{n:19,title:'The weight of an aging body',key:'j',lead:'Penitence has a physical weight',points:['One knee meets the ground as the other leg supports him.','Loose skin and exposed bones make his age tangible.','Books and the red hat recall the scholar within the penitent.'],meta:'c. 1630 · Nationalmuseum, Sweden'},
{n:20,title:'Meeting and sharing',kind:'pair',keys:['v','r'],bottom:'Anthony seeks Paul of Thebes.\nA raven’s bread connects solitude with hospitality.'},
{n:21,title:'Hospitality in the wilderness',key:'v',lead:'Enough bread for two',points:['A raven brings bread as Anthony visits Paul.','The shared meal joins divine provision with human welcome.','A royal setting once housed this vision of a secluded life.'],meta:'c. 1634 · Museo del Prado'},
{n:22,title:'One landscape, several moments',key:'v',lead:'A journey unfolds across the scene',points:['Anthony appears more than once along the road.','Search, arrival and later events share the same landscape.','The distant figures let our eyes follow the story through time.'],meta:'Diego Velázquez · Museo del Prado'},
{n:23,title:'Ribera brings old age close',key:'r',lead:'Food, mortality and prayer',points:['Strong light reveals skin, ribs and shoulder bones.','A raven carries bread above the praying hermit.','The skull recalls life’s limits. Even a saint needs food.'],meta:'c. 1638 · The Walters Art Museum'},
{n:24,title:'Sacrifice and inner change',kind:'pair',keys:['s','g'],bottom:'Serapion carries a community’s memory of martyrdom.\nMagdalen’s penitence reflects a later religious tradition.'},
{n:25,title:'White cloth carries his weight',key:'s',lead:'A community remembers Serapion',points:['Bound wrists and a lowered head reveal violence’s aftermath.','Heavy folds make the falling body tangible.','Painted for a Mercedarian monastery in Seville.'],meta:'1628 · Wadsworth Atheneum Museum of Art'},
{n:26,title:'The hand has a restoration history',key:'s',crop:'serapion',lead:'Looking closely at conservation',points:['Treatment in 2015–2016 revealed subtler tones in the white habit.','The saint’s right hand had lost much of its original paint.','Reversible inpainting includes modern judgments about the missing form.'],meta:'Francisco de Zurbarán · Wadsworth Atheneum · detail'},
{n:27,title:'Magdalen turns toward a flame',key:'g',lead:'Stillness makes inner life visible',points:['Her turned face leaves her thoughts partly hidden.','A skull rests before her in the candlelight.','This penitent image grew from later tradition around a Gospel witness.'],meta:'c. 1640 · The Metropolitan Museum of Art'},
{n:28,title:'Two flames, one candle',key:'g',crop:'magdalen',lead:'A reflection redirects our attention',points:['The second flame appears in the mirror.','She looks toward the light rather than her own reflection.','The skull and remaining jewels invite reflection on what holds her attention.'],meta:'Georges de La Tour · The Metropolitan Museum of Art · detail'},
{n:29,title:'A word becomes a way of looking',kind:'closing',key:'c',lead:'What holds their attention?',points:['Steadiness amid temptation.','Attention through study, prayer and sharing.','Each figure has a different story.'],bottom:'Which work makes you want to stay longer?'}
];
function data(file){return 'data:image/'+(file.endsWith('.png')?'png':'jpeg')+';base64,'+fs.readFileSync(file).toString('base64');}
const bg=data(path.join(root,'en_slides/Ascetic_Masterpieces_background.png'));
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;');
function figure(k,cls=''){return `<figure><div class="art ${cls}"><img src="${data(A[k])}"></div><figcaption><strong>${people[k]||''}</strong><span>${names[k]||''}</span></figcaption></figure>`;}
const htmlTw=require('./tw_style_layout.cjs')({root,A,names,people,data,esc,bg});
async function run(){
const browser=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--disable-gpu','--no-first-run','--remote-debugging-port=9243',`--user-data-dir=${path.join(build,'edge-profile')}`,'about:blank'],{windowsHide:true,stdio:'ignore'});
try{
let targets;for(let i=0;i<80;i++){try{targets=await(await fetch('http://127.0.0.1:9243/json')).json();if(targets.length)break;}catch{}await new Promise(r=>setTimeout(r,250));}
const ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));let serial=0;const pending=new Map();ws.addEventListener('message',e=>{let m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}});const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
await call('Page.enable');await call('Emulation.setDeviceMetricsOverride',{width:1280,height:720,deviceScaleFactor:1,mobile:false});
const report=[];
for(const s of slides.filter(s=>!process.env.SLIDES || process.env.SLIDES.split(',').map(Number).includes(s.n))){const filename=`new_ascetic_en.${String(s.n).padStart(3,'0')}.png`;const source=path.join(build,`${s.n}.html`);fs.writeFileSync(source,htmlTw(s));await call('Page.navigate',{url:'file:///'+source.replaceAll('\\','/')});
await new Promise(r=>setTimeout(r,180));await call('Runtime.evaluate',{expression:`Promise.all([document.fonts.ready,...Array.from(document.images).map(i=>i.decode().catch(()=>{}))])`,awaitPromise:true});
await call('Runtime.evaluate',{expression:'new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))',awaitPromise:true});await new Promise(r=>setTimeout(r,800));
const check=await call('Runtime.evaluate',{expression:`JSON.stringify({missing:Array.from(document.images).filter(i=>!i.naturalWidth).length,overflow:Array.from(document.querySelectorAll('h1,.copy,.identity,figcaption,.paircopy,.fourintro,.closecopy,.attrfooter,.dates')).filter(e=>{const r=e.getBoundingClientRect();return r.right>1220||r.bottom>656||e.scrollWidth>e.clientWidth+2}).map(e=>e.tagName+':'+e.textContent)})`,returnByValue:true});
const result=JSON.parse(check.result.value);if(result.missing||result.overflow.length)throw Error(filename+':'+JSON.stringify(result));
const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(output,filename),Buffer.from(shot.data,'base64'));report.push({filename,...result});console.log(filename);}
fs.writeFileSync(path.join(build,'validation.json'),JSON.stringify(report,null,2));await call('Browser.close');ws.close();
}finally{browser.kill();}}
run().catch(e=>{console.error(e);process.exitCode=1;});
