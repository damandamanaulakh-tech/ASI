"""THE ENGINE PAGE — /engine: ask, watch the ladder light, adopt by hand.

His orders: chat bar on top; below it the full work like a car engine in a
transparent box; the ladder lights (10 segments -> 200 containers -> 3,072
parameters); every name clickable, expanding with its reasoning; EVERY
parameter of an expanded container visible and selectable — lit or not;
deselect or force-select anything and the system adopts: the real engine
runs again without / with those brains; the answer comes last.

This page invents nothing: unfilled slots say they await his workbook.
"""

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>THE ENGINE — Sourceborn</title><style>
:root{--bg:#070809;--panel:#0f1219;--panel2:#0b0e14;--line:#1c2230;--line2:#262d3d;
--ink:#eef2f8;--mut:#7d8699;--acc:#7c8bff;--ok:#34d399;--warn:#fbbf24;--red:#f87171;
--pur:#a78bfa;--grad:linear-gradient(135deg,#7c8bff,#a78bfa 60%,#f0abfc)}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(900px 520px at 85% -8%,rgba(124,139,255,.12),transparent 60%),var(--bg);
color:var(--ink);font:15px/1.5 'Inter',-apple-system,Segoe UI,Roboto,sans-serif}
.app{max-width:1200px;margin:0 auto;padding:0 16px 80px}
.bar{position:sticky;top:0;z-index:9;padding:14px 0 12px;background:linear-gradient(180deg,rgba(7,8,9,.94),rgba(7,8,9,.5));
backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.bar .row{display:flex;gap:10px}
.bar input{flex:1;background:var(--panel);border:1px solid var(--line2);border-radius:12px;
padding:13px 16px;color:var(--ink);font:inherit;font-size:16px}
.bar button{background:var(--grad);border:0;border-radius:12px;padding:0 22px;
color:#0a0a14;cursor:pointer;font:inherit;font-weight:700}
.bar .tag{font-size:12px;color:var(--mut);margin-top:7px}
.engine{margin-top:18px;border:1px dashed var(--line2);border-radius:16px;padding:16px;position:relative}
.engine>.lbl{position:absolute;top:-9px;left:18px;background:var(--bg);padding:0 10px;
font-size:11px;letter-spacing:.18em;color:var(--mut)}
.stages{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.st{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:6px 13px;
font-size:12.5px;color:var(--mut);display:flex;gap:8px;align-items:center}
.st b{color:var(--ink);font-weight:600}
.st .d{width:8px;height:8px;border-radius:50%;background:var(--ok);box-shadow:0 0 8px var(--ok)}
.split{display:grid;grid-template-columns:minmax(300px,640px) 1fr;gap:16px}
@media(max-width:900px){.split{grid-template-columns:1fr}}
.ringbox{background:var(--panel2);border:1px solid var(--line);border-radius:14px;padding:6px}
.ringbox svg{width:100%;height:auto;display:block}
.ringcap{text-align:center;color:var(--mut);font-size:12px;padding:4px 0 8px}
.rail h3{margin:6px 0 8px;font-size:12px;letter-spacing:.16em;color:var(--mut)}
.rail h3 em{color:var(--warn);font-style:normal}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:12px}
.chip{border:1px solid var(--line2);background:var(--panel);border-radius:999px;padding:6px 12px;
font-size:12.5px;cursor:pointer;color:var(--ink);display:flex;gap:7px;align-items:center;font:inherit}
.chip .d{width:8px;height:8px;border-radius:50%;flex:none}
.chip.seg .d{background:var(--pur)}.chip.con .d{background:var(--red)}
.chip.par .d{background:#fff;box-shadow:0 0 6px var(--red)}
.chip.off{opacity:.38;text-decoration:line-through}
.chip.forced{border-color:var(--ok)}
.chip:hover{border-color:var(--acc)}
.chip.open{border-color:var(--acc);box-shadow:0 0 0 3px rgba(124,139,255,.18)}
.count{color:var(--mut);font-size:12px;margin:-4px 0 10px}
.card{background:var(--panel);border:1px solid var(--acc);border-radius:14px;padding:14px 16px;margin-bottom:14px}
.card h4{margin:0 0 2px;font-size:15px}
.card .k{font-size:11px;letter-spacing:.14em;color:var(--mut);margin:10px 0 3px}
.card p{margin:0;font-size:13.5px}
.card .tog{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}
.tog button{font:inherit;font-size:12.5px;border-radius:9px;border:1px solid var(--line2);
background:var(--panel2);color:var(--ink);padding:6px 14px;cursor:pointer}
.tog button.sel{background:rgba(52,211,153,.14);border-color:var(--ok);color:var(--ok)}
.tog button.des{background:rgba(248,113,113,.12);border-color:var(--red);color:var(--red)}
.plist{max-height:300px;overflow:auto;border:1px solid var(--line);border-radius:10px;
margin-top:6px;background:var(--panel2)}
.prow{display:flex;gap:10px;align-items:center;padding:7px 12px;border-top:1px solid var(--line);
font-size:13px;cursor:pointer}
.prow:first-child{border-top:0}
.prow:hover{background:rgba(124,139,255,.06)}
.prow .st2{font-size:10.5px;border:1px solid var(--line2);border-radius:999px;padding:1px 8px;color:var(--mut);flex:none}
.prow.lit .st2{color:var(--ok);border-color:var(--ok)}
.prow.parked{opacity:.45}.prow.parked .st2{color:var(--red);border-color:var(--red)}
.prow.forced .st2{color:var(--acc);border-color:var(--acc)}
.prow .nm{flex:1}
.answer{margin-top:18px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.answer.pulse{animation:pulse .7s ease}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(124,139,255,.5)}100%{box-shadow:0 0 0 14px rgba(124,139,255,0)}}
.answer h2{margin:0 0 3px;font-size:13px;letter-spacing:.16em;color:var(--mut)}
.cls{display:inline-block;font-size:12px;border:1px solid var(--warn);color:var(--warn);
border-radius:999px;padding:2px 11px;margin:6px 0 10px}
.atext{white-space:pre-wrap;font-size:14.5px;margin:8px 0}
.claim{border-left:2px solid var(--line2);padding:6px 0 6px 14px;margin:6px 0;font-size:13.5px}
.claim .src{font-size:11.5px;color:var(--acc)}
.confrow{display:flex;align-items:center;gap:12px;margin:14px 0 4px}
.confbar{flex:1;height:8px;border-radius:999px;background:var(--panel2);border:1px solid var(--line);overflow:hidden}
.confbar i{display:block;height:100%;background:var(--grad);transition:width .5s}
.conflab{font-size:13px;font-weight:600;min-width:150px;text-align:right}
.gap{margin-top:12px;border-top:1px dashed var(--line2);padding-top:10px;font-size:13px;color:var(--warn)}
.adopt{margin-top:8px;font-size:12.5px;color:var(--acc)}
.note{margin-top:16px;color:var(--mut);font-size:12.5px}
.spin{display:none;color:var(--acc);font-size:13px;margin-left:8px}
svg text{font-family:'Inter',-apple-system,Segoe UI,sans-serif}
.dot{cursor:pointer}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
@media(prefers-reduced-motion:reduce){.answer.pulse{animation:none}.confbar i{transition:none}}
</style></head><body><div class=app>
<div class=bar>
 <div class=row><input id=q placeholder="ask — your words are Point Zero" aria-label=ask>
 <button id=askbtn onclick="ask(false)">ASK</button></div>
 <div class=tag id=regline>loading the registry…<span class=spin id=spin> · the engine is running…</span></div>
</div>
<div class=engine><span class=lbl>THE ENGINE — TRANSPARENT BOX</span>
 <div class=stages id=stages></div>
 <div class=split>
  <div><div class=ringbox><svg id=ring viewBox="0 0 660 660" role=img aria-label="the ladder ring"></svg>
   <div class=ringcap>the ladder, outward from POINT ZERO: 10 segments (purple) · 200 containers (red) ·
   <b>3,072 parameters — the dust ring, where the work happens</b></div></div></div>
  <div class=rail>
   <h3>10 SEGMENTS — LIT</h3><div class=chips id=segchips></div>
   <h3>200 CONTAINERS — LIT (the frame)</h3><div class=count id=concount></div><div class=chips id=conchips></div>
   <h3>3,072 PARAMETERS — SPEAKING <em>· the work happens here</em></h3>
   <div class=count id=parcount></div><div class=chips id=parchips></div>
   <div id=moveswrap style="display:none">
     <h3 style="display:flex;align-items:center;gap:8px">YOUR MOVES — IN ORDER
       <button id=movesclear title="clear your selection"
         style="margin-left:auto;font:inherit;font-size:11px;border:1px solid var(--line2);
         background:var(--panel2);color:var(--mut);border-radius:7px;padding:2px 9px;cursor:pointer">reset</button></h3>
     <ol id=moves style="margin:0;padding-left:22px;font-size:12.5px;color:var(--ink)"></ol>
   </div>
   <div id=detail></div>
  </div>
 </div>
</div>
<div class=answer id=ans><h2>THE ANSWER — LAST, AS YOU ASKED</h2>
<div class=atext>Ask above. The full walk shows here: what lit, why, what each brain said — and the answer, last.</div></div>
<div class=note>Deselect any brain — or open a container and force-select a parameter that did not fire — and the REAL engine
runs again with your hand applied. Nothing is deleted: parked brains return on click. Unfilled slots say plainly that they
await the workbook; the engine never invents a brain.</div>
</div><script>
let REG=null,LIT={segments:[],containers:[],parameters:[]},LAST=null,openId=null;
const DES=new Set(),SEL=new Set();
let MOVES=[];                 // his ordered park/force/unpark/release log
const $=q=>document.querySelector(q);
const pname=id=>{const p=REG&&REG.parameters.find(x=>x.id===id);return p?p.name||'':''};
function persist(){try{localStorage.setItem('sb_engine',JSON.stringify(
  {q:$('#q').value,des:[...DES],sel:[...SEL],moves:MOVES}));}catch(e){}}
function logMove(a,id){MOVES.push({a,id,at:Date.now()});persist();drawMoves()}
function drawMoves(){
 const w=$('#moveswrap'),ol=$('#moves');
 if(!MOVES.length){w.style.display='none';return}
 w.style.display='';
 const verb={park:'parked',unpark:'returned',force:'forced in',release:'released'};
 ol.innerHTML=MOVES.map(m=>`<li><b>${verb[m.a]||m.a}</b> ${esc(m.id)}${
   pname(m.id)?' <span style="color:var(--mut)">'+esc(pname(m.id))+'</span>':''}</li>`).join('');
}
async function j(u,opt){const r=await fetch(u,opt);return r.json()}
const NS='http://www.w3.org/2000/svg',CX=330,CY=330,R_PAR=304,R_CON=238,R_SEG=132;
function pt(r,i,n){const a=-Math.PI/2+2*Math.PI*i/n;return[CX+r*Math.cos(a),CY+r*Math.sin(a)]}
function el(t,at){const e=document.createElementNS(NS,t);for(const k in at)e.setAttribute(k,at[k]);return e}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
const segIx=id=>REG.segments.findIndex(s=>s.id===id);
const conIx={},parIx={};
function indexRing(){let k=0;REG.containers.forEach(c=>{conIx[c.id]=Math.round(k*200/REG.containers.length);k++});}
function litP(){return LIT.parameters.filter(p=>!DES.has(p.id))}
function speakingIds(){const s=new Set(litP().map(p=>p.id));SEL.forEach(x=>s.add(x));DES.forEach(x=>s.delete(x));return s}
function drawRing(){
 const svg=$('#ring');svg.innerHTML='';
 for(let i=0;i<200;i++){const[x1,y1]=pt(R_CON,i,200),[x2,y2]=pt(R_SEG,i%10,10);
  svg.appendChild(el('line',{x1,y1,x2,y2,stroke:'#a78bfa',opacity:.04}))}
 const dust=el('g',{});dust.appendChild(el('title',{})).textContent=
  REG.totals.parameters+' parameter slots · '+REG.totals.parameters_filled+' filled — the rest await the workbook';
 for(let i=0;i<REG.totals.parameters;i+=4){const[x,y]=pt(R_PAR,i,REG.totals.parameters);
  dust.appendChild(el('circle',{cx:x,cy:y,r:.9,fill:'#f87171',opacity:.26}))}
 svg.appendChild(dust);
 const speak=[...speakingIds()];
 speak.forEach((pid,k)=>{const p=LIT.parameters.find(x=>x.id===pid)||REG.parameters.find(x=>x.id===pid);
  if(!p)return;const ci=conIx[p.container]??0;
  const di=Math.round((k+1)*REG.totals.parameters/(speak.length+1));
  const[x1,y1]=pt(R_PAR,di,REG.totals.parameters),[x2,y2]=pt(R_CON,ci,200);
  const c=REG.containers.find(x=>x.id===p.container)||{};
  svg.appendChild(el('line',{x1,y1,x2,y2,stroke:'#fff',opacity:.7,'stroke-width':1.2}));
  if(c.segment&&c.segment!=='CROSS'){const[x3,y3]=pt(R_SEG,segIx(c.segment),10);
   svg.appendChild(el('line',{x1:x2,y1:y2,x2:x3,y2:y3,stroke:'#7c8bff',opacity:.75,'stroke-width':1.4}))}
  const d=el('circle',{cx:x1,cy:y1,r:5.4,fill:'#fff',stroke:'#f87171','stroke-width':2,class:'dot',tabindex:0});
  d.appendChild(el('title',{})).textContent=p.id+' · '+(p.name||'');
  d.addEventListener('click',()=>openCard(p.id));svg.appendChild(d)});
 REG.containers.forEach(c=>{const i=conIx[c.id];const[x,y]=pt(R_CON,i,200);
  const lit=LIT.containers.some(x=>x.id===c.id)&&!DES.has(c.id);
  const d=el('circle',{cx:x,cy:y,r:lit?6.4:3.8,fill:'#f87171',
   opacity:c.filled?(lit?1:.6):.3,stroke:lit?'#fff':'none','stroke-width':1.1,class:'dot',tabindex:0});
  d.appendChild(el('title',{})).textContent=c.id+(c.name?' · '+c.name:' — unfilled, awaits the workbook')
   +(c.target?' · '+c.target+' parameters':'');
  d.addEventListener('click',()=>openCard(c.id));svg.appendChild(d)});
 REG.segments.forEach((s,i)=>{const[x,y]=pt(R_SEG,i,10);
  const lit=LIT.segments.some(x=>x.id===s.id)&&!DES.has(s.id);
  const d=el('circle',{cx:x,cy:y,r:lit?10:7,fill:'#a78bfa',opacity:lit?1:.55,
   stroke:lit?'#fff':'none','stroke-width':1.2,class:'dot',tabindex:0});
  d.appendChild(el('title',{})).textContent=s.id+' · '+s.name+' · '+s.target+' parameters';
  d.addEventListener('click',()=>openCard(s.id));svg.appendChild(d);
  const[lx,ly]=pt(R_SEG-36,i,10);
  const t=el('text',{x:lx,y:ly,'font-size':10.5,fill:'#a78bfa','text-anchor':'middle'});
  t.textContent=s.id;svg.appendChild(t)});
 const t=el('text',{x:CX,y:CY+4,'font-size':11,fill:'#7d8699','text-anchor':'middle'});
 t.textContent='POINT ZERO';svg.appendChild(t);
}
function chip(id,label,cls,extra){const b=document.createElement('button');
 b.className='chip '+cls+(DES.has(id)?' off':'')+(SEL.has(id)?' forced':'')+(openId===id?' open':'');
 b.innerHTML='<span class=d></span>'+esc(label)+(extra||'');b.onclick=()=>openCard(id);return b}
function drawRail(){
 const sc=$('#segchips');sc.innerHTML='';
 LIT.segments.forEach(s=>sc.appendChild(chip(s.id,s.id+' · '+s.name.split(',')[0],'seg')));
 if(!LIT.segments.length)sc.innerHTML='<span class=count>none lit yet — ask above</span>';
 const cc=$('#conchips');cc.innerHTML='';
 LIT.containers.forEach(c=>cc.appendChild(chip(c.id,(c.name||c.id)+(c.target?' · '+c.target:''),'con')));
 $('#concount').textContent=LIT.containers.filter(c=>!DES.has(c.id)).length+' of '+REG.totals.containers+
  ' lit · click one — EVERY parameter under it shows, each selectable';
 const pc=$('#parchips');pc.innerHTML='';
 const sp=speakingIds();
 [...sp].forEach(pid=>{const p=REG.parameters.find(x=>x.id===pid);
  if(p)pc.appendChild(chip(p.id,p.id+' '+(p.name||''),'par'))});
 $('#parcount').textContent=sp.size+' speaking of '+REG.totals.parameters_filled+
  ' filled ('+REG.totals.parameters+' slots) · every claim below is one of these';
}
function pstate(id){return DES.has(id)?'PARKED':SEL.has(id)?'FORCED':
 LIT.parameters.some(p=>p.id===id)?'LIT':'idle'}
function openCard(id){
 openId=id;const d=$('#detail');
 const p=REG.parameters.find(x=>x.id===id),
       c=REG.containers.find(x=>x.id===id),
       s=REG.segments.find(x=>x.id===id);
 if(p){const lp=LIT.parameters.find(x=>x.id===id);
  d.innerHTML=`<div class=card><h4>${esc(p.id)} · ${esc(p.name||'')}</h4>
  <div class=k>LADDER</div><p>${esc(p.id)} → ${esc(p.container)} → ${esc((REG.containers.find(x=>x.id===p.container)||{}).segment||'CROSS')}</p>
  <div class=k>WHAT IT HOLDS</div><p>${esc(p.contains||'')}</p>
  <div class=k>WHY IT FIRED</div><p>${esc(lp?lp.reason:(SEL.has(id)?'forced in by your hand':'did not fire on this question — you can force it in'))}</p>
  <div class=tog><button class="${DES.has(id)?'des':'sel'}" onclick="togglePark('${p.id}')">${DES.has(id)?'PARKED — click to return':'click to PARK'}</button>
  <button class="${SEL.has(id)?'sel':''}" onclick="toggleForce('${p.id}')">${SEL.has(id)?'FORCED IN — click to release':'FORCE INTO THE ANSWER'}</button></div></div>`}
 else if(c){const mine=REG.parameters.filter(x=>x.container===c.id);
  const unfilled=(c.target||0)-mine.length;
  d.innerHTML=`<div class=card><h4>${esc(c.id)} · ${esc(c.name||'— unfilled, awaits the workbook')}</h4>
  <div class=k>SEGMENT</div><p>${esc(c.segment||'not assigned yet')}</p>
  <div class=k>EVERY PARAMETER UNDER IT — each selectable, as you asked</div>
  <div class=plist id=plist></div>
  ${unfilled>0?`<p style="margin-top:8px;color:var(--mut);font-size:12.5px">+ ${unfilled} more slots — unfilled, they appear here the moment the workbook lands, each selectable.</p>`:''}
  ${!mine.length&&!c.target?`<p style="margin-top:8px;color:var(--mut);font-size:12.5px">size unknown until the workbook lands.</p>`:''}
  <div class=tog><button class="${DES.has(id)?'des':'sel'}" onclick="togglePark('${c.id}')">${DES.has(id)?'PARKED — click to return (its parameters return too)':'click to PARK (parks its parameters too)'}</button></div></div>`;
  const pl=document.getElementById('plist');
  if(!mine.length)pl.innerHTML='<div class=prow><span class=nm style="color:var(--mut)">no filled parameters yet</span></div>';
  mine.forEach(x=>{const st=pstate(x.id);
   const r=document.createElement('div');r.className='prow '+st.toLowerCase();
   r.innerHTML=`<span class=st2>${st}</span><span class=nm>${esc(x.id)} · ${esc(x.name)}</span>`;
   r.onclick=()=>openCard(x.id);pl.appendChild(r)})}
 else if(s){d.innerHTML=`<div class=card><h4>${esc(s.id)} · ${esc(s.name)}</h4>
  <div class=k>HOLDS</div><p>${s.target} parameters across its containers.</p>
  <div class=tog><button class="${DES.has(id)?'des':'sel'}" onclick="togglePark('${s.id}')">${DES.has(id)?'PARKED — click to return':'click to PARK (parks its containers and their parameters)'}</button></div></div>`}
 drawRail();
}
function togglePark(id){
 if(DES.has(id)){DES.delete(id);logMove('unpark',id);}
 else{DES.add(id);SEL.delete(id);logMove('park',id);}
 if(LAST)ask(true);else{drawRing();drawRail();if(openId)openCard(openId)}}
function toggleForce(id){
 if(SEL.has(id)){SEL.delete(id);logMove('release',id);}
 else{SEL.add(id);DES.delete(id);logMove('force',id);}
 if(LAST)ask(true);else{drawRing();drawRail();if(openId)openCard(openId)}}
function drawStages(){
 $('#stages').innerHTML=[["POINT ZERO",LAST?'his exact words locked':'waiting'],
 ["10 SEGMENTS",LIT.segments.length+' lit'],
 ["200 CONTAINERS",LIT.containers.length+' lit — the frame'],
 [REG.totals.parameters+" PARAMETERS",speakingIds().size+' speaking — the work'],
 ["7 FILTERS","Ground · Sequence · Source · Mask · Fact · Halt · Loop"],
 ["WITNESS CAP ½","one voice = Medium max"],
 ["ANSWER",LAST?'below — recomposes on your hand':'—']]
 .map(x=>`<span class=st><span class=d></span><b>${x[0]}</b> ${esc(x[1])}</span>`).join('');
}
function renderAnswer(adopted){
 const a=$('#ans');if(!LAST){return}
 const o=LAST.payload.output||{},sp=LAST.hand.speaking||[];
 a.innerHTML=`<h2>THE ANSWER — LAST, AS YOU ASKED</h2>
 <span class=cls>CLASSIFICATION: ${esc(o.classification||'—')}</span>
 <div class=atext>${esc(o.answer||'')}</div>
 ${sp.map(p=>`<div class=claim>${esc(p.id)} ${esc(p.name||'')} — ${esc(p.reason||'')}<br>
  <span class=src>${esc((p.contains||'').slice(0,160))}</span></div>`).join('')}
 <div class=confrow><div class=confbar><i style="width:${o.confidence==='High'?86:o.confidence==='Medium'?52:22}%"></i></div>
 <div class=conflab>${esc(o.confidence||'—')} · ${LAST.payload.walk?LAST.payload.walk.hold_count+' holds':''}</div></div>
 ${(LAST.payload.halts||[]).length?`<div class=gap>HALT, named: ${esc(LAST.payload.halts.join(' · '))}</div>`:''}
 ${(LAST.hand.deselected||[]).length||(LAST.hand.forced||[]).length?
  `<div class=adopt>ADOPTED — the engine ran again with your hand: ${
   (LAST.hand.deselected||[]).length?'without '+LAST.hand.deselected.join(', '):''} ${
   (LAST.hand.forced||[]).length?'· forced in '+LAST.hand.forced.join(', '):''}. Nothing deleted — parked brains return on click.</div>`:''}`;
 if(adopted){a.classList.remove('pulse');void a.offsetWidth;a.classList.add('pulse')}
}
async function ask(isAdopt){
 const q=$('#q').value.trim();if(!q)return;
 $('#spin').style.display='inline';$('#askbtn').disabled=true;
 try{
  const r=await j('/engine/ask',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({question:q,deselect:[...DES],select:[...SEL],actions:MOVES})});
  if(r.error){alert(r.error);return}
  LIT=r.lit;LAST=r;persist();
  drawRing();drawRail();drawStages();drawMoves();renderAnswer(isAdopt);
  if(openId)openCard(openId);
 }finally{$('#spin').style.display='none';$('#askbtn').disabled=false}
}
function restore(){
 try{const s=JSON.parse(localStorage.getItem('sb_engine')||'null');if(!s)return;
  if(s.q)$('#q').value=s.q;
  (s.des||[]).forEach(x=>DES.add(x));(s.sel||[]).forEach(x=>SEL.add(x));
  MOVES=Array.isArray(s.moves)?s.moves:[];
 }catch(e){}
}
function resetMoves(){DES.clear();SEL.clear();MOVES=[];persist();
 drawRing();drawRail();drawStages();drawMoves();if(openId)openCard(openId);}
async function boot(){
 REG=await j('/engine/registry');indexRing();restore();
 $('#regline').innerHTML='registry v'+REG.version+' · '+REG.totals.parameters_filled+' of '
  +REG.totals.parameters+' parameters filled — the rest await the workbook (upload lands them here, each selectable)'
  +'<span class=spin id=spin> · the engine is running…</span>';
 drawRing();drawRail();drawStages();drawMoves();
 $('#movesclear').addEventListener('click',resetMoves);
 document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter')ask(false)});
}
boot();
</script></body></html>"""
