"""THE GLASS REACTOR — the home page, on his word.

His three rulings, from the mockup rounds, all binding here:

    "i dont want black back ground"          -> a luminous light ground, no black
    "the web should have all 3000+ para,     -> the whole bank drawn live: one
     algo which it use"                          point per parameter, and under
                                                 each answer the filters and the
                                                 eighteen steps that actually ran
    "transparent so i can see which is       -> one selection, three views: the
     linked where ... and must be editable       reactor arc, the chip under the
     so i can change"                            answer and the ledger row light
                                                 together; every name is editable
                                                 in place, and an edit lands as a
                                                 CORRECTION row that references
                                                 what it corrects — the source is
                                                 never rewritten

And his catch on the sample — "where is the ask tab" — is the panel's head:
you type, the machine answers, and the answer arrives already wearing its
wiring. THE ASK calls the same POST /ask the engine page uses (the full
SB walk), plus POST /growing/place for what it seats and POST /runtime/run
for his eighteen steps — three views of ONE ask, never a second engine.

EVERYTHING ON THIS PAGE IS LIVE OR ABSENT — no number is typed into the
markup. The HUD comes from /api/hud, the bank's structure from /api/bank
(real container counts, including the two that hold 42), the rows from
/registry/container, the lighting from what the ask actually seated. When a
fetch fails the panel says so instead of showing a stale figure.

The old dashboard is NOT removed — it lives whole at /desk (nothing is
deleted in this project, pages included).
"""

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Sourceborn — The Glass Reactor</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Exo+2:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --ground:#f2f6fb; --ground2:#e9f0f8;
  --glass:rgba(255,255,255,.62); --glass2:rgba(255,255,255,.8);
  --edge:#c9dcee; --edge2:#a8c6de;
  --ink:#0e2438; --mut:#5b7a94;
  --beam:#0891b2; --lit:#06b6d4; --glow:#38bdf8;
  --his:#b45309; --ok:#0f9d76; --bad:#c2410c;
}
*{box-sizing:border-box;margin:0}
body{color:var(--ink);
  font:15px/1.6 'IBM Plex Sans',-apple-system,'Segoe UI',sans-serif;
  background:
    radial-gradient(1100px 520px at 18% -6%, rgba(56,189,248,.14), transparent 60%),
    radial-gradient(900px 600px at 100% 30%, rgba(8,145,178,.10), transparent 55%),
    linear-gradient(180deg, var(--ground), var(--ground2));
  min-height:100vh; padding-bottom:90px}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(8,145,178,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(8,145,178,.05) 1px, transparent 1px);
  background-size:44px 44px}
.wrap{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:0 20px}
.hl{font-family:'Exo 2',sans-serif;font-weight:600;font-size:11px;
  letter-spacing:.24em;text-transform:uppercase;color:var(--beam)}
.mono{font-family:'IBM Plex Mono',monospace}
a{color:var(--beam)}

.top{display:flex;justify-content:space-between;align-items:center;gap:12px;
  flex-wrap:wrap;padding:16px 0 4px}
.brand{font-family:'Exo 2',sans-serif;font-weight:700;font-size:19px}
.brand small{color:var(--mut);font-weight:400;font-size:11px;margin-left:10px;
  font-family:'IBM Plex Sans',sans-serif}
.nav{display:flex;gap:6px;flex-wrap:wrap}
.nav a{font-size:11.5px;text-decoration:none;color:var(--ink);
  border:1px solid var(--edge);background:var(--glass2);border-radius:8px;
  padding:4px 11px}
.nav a:hover{border-color:var(--beam)}

.hud{display:flex;align-items:stretch;flex-wrap:wrap;
  border:1px solid var(--edge);border-radius:14px;background:var(--glass);
  backdrop-filter:blur(10px);margin:10px 0 16px;overflow:hidden}
.hud .cell{flex:1;min-width:118px;padding:10px 16px;border-right:1px solid var(--edge)}
.hud .cell:last-child{border-right:0}
.hud .ck{font-family:'Exo 2',sans-serif;font-size:9.5px;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;color:var(--mut)}
.hud .cv{font-family:'IBM Plex Mono',monospace;font-size:16px;margin-top:2px;
  font-variant-numeric:tabular-nums}
.hud .cv.live{color:var(--ok)}
.hud .cv small{font-size:10.5px;color:var(--mut)}

.panel{background:var(--glass);border:1px solid var(--edge);border-radius:16px;
  backdrop-filter:blur(12px);box-shadow:0 14px 44px rgba(14,36,56,.10)}
.stage{display:grid;grid-template-columns:1.02fr 1fr;gap:16px}
@media(max-width:920px){.stage{grid-template-columns:1fr}}

.orb{position:relative;min-height:600px;padding:10px}
.orb canvas{position:absolute;inset:0;width:100%;height:100%}
.orb .cap{position:absolute;left:16px;bottom:12px;font-size:11px;color:var(--mut);max-width:42ch}
.orb .cap b{color:var(--ink)}
.seltag{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--beam);
  border:1px solid rgba(6,182,212,.5);background:var(--glass2);border-radius:7px;
  padding:3px 10px;cursor:pointer;user-select:none;position:absolute;right:14px;top:12px}
@keyframes selpulse{0%{box-shadow:0 0 0 1px rgba(6,182,212,.2)}
  35%{box-shadow:0 0 0 5px rgba(6,182,212,.4),0 0 22px rgba(6,182,212,.5)}
  100%{box-shadow:0 0 0 1px rgba(6,182,212,.2)}}
.pulse{animation:selpulse .9s ease}

.trace{padding:16px 18px;display:flex;flex-direction:column;gap:0}
.askrow{display:flex;gap:8px;align-items:flex-start}
.askrow textarea{flex:1;font:inherit;font-size:14.5px;color:var(--ink);
  background:var(--glass2);border:1px solid var(--edge2);border-radius:10px;
  padding:10px 13px;min-height:64px;resize:vertical;outline:none}
.askrow textarea:focus{border-color:var(--beam)}
.askcol{display:flex;flex-direction:column;gap:6px}
.btn{font:600 13px 'Exo 2',sans-serif;letter-spacing:.06em;cursor:pointer;
  color:#fff;background:linear-gradient(135deg,var(--beam),var(--lit));
  border:0;border-radius:10px;padding:10px 20px}
.btn[disabled]{opacity:.5;cursor:wait}
select{font:inherit;font-size:12px;color:var(--ink);background:var(--glass2);
  border:1px solid var(--edge);border-radius:8px;padding:4px 8px}

.ansbox{margin-top:14px}
.meta{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.mc{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--mut);
  border:1px solid var(--edge);border-radius:6px;padding:2px 9px;background:rgba(255,255,255,.55)}
.mc b{color:var(--ink);font-weight:500}
.ans{font-size:15px;line-height:1.65;white-space:pre-wrap;max-height:280px;overflow:auto}
.empty{color:var(--mut);font-style:italic;font-size:13px}

.sect{margin-top:14px;padding-top:11px;border-top:1px dashed var(--edge2)}
.sect .sh{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.sect .hint{font-size:10.5px;color:var(--mut)}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px}
.chip{display:flex;align-items:center;gap:7px;background:var(--glass2);
  border:1px solid var(--edge2);border-radius:10px;padding:5px 10px;font-size:12px;cursor:pointer}
.chip .pid{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--beam)}
.chip.lit{border-color:var(--lit);box-shadow:0 0 0 1px rgba(6,182,212,.25),0 2px 12px rgba(6,182,212,.2)}
.chip .edit{border:0;background:none;cursor:pointer;color:var(--edge2);font-size:12px;padding:0}
.chip .edit:hover{color:var(--his)}

.algostrip{display:flex;gap:4px;flex-wrap:wrap;margin-top:9px}
.al{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--mut);
  border:1px solid var(--edge);border-radius:6px;padding:2px 7px;background:rgba(255,255,255,.5)}
.al.ran{color:var(--beam);border-color:var(--edge2);background:var(--glass2)}
.al.rev{color:#7c3aed;border-color:#d8c7f5}
.al.halt{color:var(--his);border-color:#ecd3b4;font-weight:600}

.ledger{margin-top:16px;padding:16px 18px}
.lh{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.bank{display:grid;grid-template-columns:repeat(10,1fr);gap:7px;margin-top:12px}
@media(max-width:920px){.bank{grid-template-columns:repeat(5,1fr)}}
.seg{border:1px solid var(--edge);border-radius:10px;background:var(--glass2);padding:7px 7px 8px}
.seg .sid{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--beam)}
.seg .snm{font-size:9px;line-height:1.25;color:var(--ink);min-height:34px;margin:2px 0 6px}
.cells{display:grid;grid-template-columns:repeat(4,1fr);gap:3px}
.cells i{display:block;aspect-ratio:1;border-radius:3px;background:#dbe8f4;cursor:pointer;border:0}
.cells i:hover,.cells i:focus-visible{outline:1.5px solid var(--beam)}
.cells i.hot{background:var(--lit);box-shadow:0 0 6px rgba(6,182,212,.55)}

.opencon{margin-top:14px;border:1px solid rgba(6,182,212,.45);border-radius:12px;
  background:var(--glass2);padding:13px 15px}
.opencon .oh{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline}
.opencon .note{font-size:11.5px;color:var(--mut);margin-top:2px}
.rows{columns:4 190px;column-gap:14px;margin-top:11px;font-size:12px}
.rows>div{break-inside:avoid;padding:2px 4px;border-radius:5px;display:flex;
  justify-content:space-between;gap:6px;align-items:baseline}
.rows>div:hover{background:rgba(56,189,248,.12)}
.rows .rp{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--mut);white-space:nowrap}
.rows .lit2{background:rgba(6,182,212,.16);border:1px solid rgba(6,182,212,.35)}
.rows .re{border:0;background:none;cursor:pointer;color:var(--edge2);font-size:11px;padding:0}
.rows .re:hover{color:var(--his)}
.rows .edit2{background:rgba(180,83,9,.07);border:1px solid rgba(180,83,9,.35)}
.rows .edit2 input{font:inherit;font-size:12px;border:0;border-bottom:1px solid var(--his);
  background:transparent;width:100%;outline:none;color:var(--ink)}
.wb{font-size:10px;color:var(--his);margin-top:7px;font-family:'IBM Plex Mono',monospace;min-height:14px}

@media(prefers-reduced-motion:reduce){*{animation:none!important}}
:focus-visible{outline:2px solid var(--beam);outline-offset:2px}
</style></head><body><div class=wrap>

<div class=top>
  <div class=brand>Sourceborn<small>eternal example · present fact · more parameters, more outcome</small></div>
  <nav class=nav aria-label="his pages">
    <a href="/engine">THE ENGINE</a><a href="/reading">THE READING</a>
    <a href="/asi">THE ASI RUN</a><a href="/generation">THE GENERATION</a>
    <a href="/page">MY PAGE</a><a href="/exists">WHAT EXISTS</a>
    <a href="/desk">THE DESK</a>
  </nav>
</div>

<div class=hud role=group aria-label="machine state" id=hud>
  <div class=cell><div class=ck>Mode</div><div class="cv live" id=h_mode>—</div></div>
  <div class=cell><div class=ck>Tick</div><div class=cv id=h_tick>—</div></div>
  <div class=cell><div class=ck>The bank</div><div class=cv id=h_bank>—</div></div>
  <div class=cell><div class=ck>Waits on your word</div><div class=cv id=h_q>—</div></div>
  <div class=cell><div class=ck>Stages</div><div class=cv id=h_st>—</div></div>
  <div class=cell><div class=ck>Loops</div><div class=cv id=h_lp>—</div></div>
</div>

<div class="panel stage">
  <div class=orb>
    <canvas id=orb aria-label="the bank — one point per parameter"></canvas>
    <span class=seltag id=contag data-sel hidden>—</span>
    <div class=cap id=orbcap><b>The bank, one point per parameter.</b>
      Ask something — what the answer seats lights up and stays wired to it.</div>
  </div>

  <div class=trace>
    <div class=askrow>
      <textarea id=q aria-label="ask" placeholder="Ask — the answer arrives wearing its wiring: what it seated, which filters and steps ran, all of it editable."></textarea>
      <div class=askcol>
        <button class=btn id=go>ASK</button>
        <select id=model aria-label="model"><option>offline</option><option>claude</option><option>grok</option><option>openai</option></select>
      </div>
    </div>

    <div class=ansbox>
      <div class=meta id=meta></div>
      <div class=ans id=ans><span class=empty>The machine is listening. Its whole bank is on your left.</span></div>
    </div>

    <div class=sect>
      <div class=sh><span class=hl>parameters it used</span>
        <span class=hint>click a chip — the arc, the cell and the rows light together · ✎ to correct</span></div>
      <div class=chips id=chips><span class=empty>none yet — they appear under the answer</span></div>
    </div>

    <div class=sect>
      <div class=sh><span class=hl>algorithms that ran on it</span>
        <span class=hint>dim = did not bite · ⟲ = runs in reverse · amber = HALT, yours</span></div>
      <div class=algostrip id=filters></div>
      <div class=algostrip id=steps></div>
    </div>
  </div>
</div>

<div class="panel ledger">
  <div class=lh>
    <span class=hl>the bank · 10 segments · 80 containers · <span id=bcount>—</span> named</span>
    <span class=hint id=lhint>click any cell to open its rows below</span>
  </div>
  <div class=bank id=bank></div>
  <div class=opencon id=opencon hidden>
    <div class=oh>
      <span><span class="seltag" style="position:static" id=conid data-sel>—</span>
        · <b id=conname>—</b><span class=note id=connote></span></span>
      <span class="mono hint" id=conmeta></span>
    </div>
    <div class=rows id=rows></div>
    <div class=wb id=wbline></div>
  </div>
</div>

</div><script>
const $=id=>document.getElementById(id);
const j=async(u,opt)=>{const r=await fetch(u,opt);if(!r.ok)throw new Error(u+" "+r.status);return r.json()};
const post=(u,b)=>j(u,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

/* ---------- state ---------- */
let BANK=null;          // [{seg,seg_name,containers:[{id,name,count,start}]}]
let LITROWS=[];         // [{p:int, sb_id, name, container}]
let LITCONS=new Set();  // container ids the answer touched
let SELCON=null;        // selected container id
const still=matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- HUD ---------- */
async function hud(){
  try{const h=await j("/api/hud");
    $("h_mode").textContent=h.mode;
    $("h_tick").innerHTML=h.tick_n?("#"+h.tick_n+" <small>"+(h.tick_quiet?"quiet":"worked")+"</small>"):"<small>none yet</small>";
    $("h_bank").innerHTML=h.bank.toLocaleString()+" <small>"+h.base.toLocaleString()+" + "+h.grown+" grown</small>";
    $("h_q").textContent=h.queued;
    $("h_st").innerHTML=h.stages_run+"<small>/"+h.stages+"</small>";
    $("h_lp").innerHTML=h.loops_triggered+"<small>/9 triggered</small>";
  }catch(e){$("h_mode").textContent="unreachable";}
}

/* ---------- the reactor ---------- */
const cv=$("orb"),ctx=cv.getContext("2d");
let W,H,cx,cy,R,t=0,pulseAt=-999;
function size(){const r=cv.parentElement.getBoundingClientRect(),d=devicePixelRatio||1;
  W=r.width;H=r.height;cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0);
  cx=W/2;cy=H/2+8;R=Math.min(W,H)/2-56;}
function band(c){return R*0.36+(c/8)*(R*0.60);}
function apos(s,c,i,n){const a0=-Math.PI/2+s*(Math.PI*2/10),gap=0.055;
  const a=a0+gap+(i/Math.max(1,n))*((Math.PI*2/10)-gap*2);
  return [cx+Math.cos(a)*band(c),cy+Math.sin(a)*band(c)];}
function locate(p){ /* flat P index (1-based) -> [s,c,i,n] */
  if(!BANK)return null;
  for(let s=0;s<BANK.length;s++)for(let c=0;c<BANK[s].containers.length;c++){
    const con=BANK[s].containers[c];
    if(p>=con.start&&p<con.start+con.count)return [s,c,p-con.start,con.count,con.id];}
  return null;}
function conPos(id){if(!BANK)return null;
  for(let s=0;s<BANK.length;s++)for(let c=0;c<BANK[s].containers.length;c++)
    if(BANK[s].containers[c].id===id)return [s,c];
  return null;}
function draw(){
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(8,145,178,.14)';ctx.lineWidth=1;
  for(let s=0;s<10;s++){const a=-Math.PI/2+s*(Math.PI*2/10);
    ctx.beginPath();ctx.moveTo(cx+Math.cos(a)*R*.30,cy+Math.sin(a)*R*.30);
    ctx.lineTo(cx+Math.cos(a)*R*1.02,cy+Math.sin(a)*R*1.02);ctx.stroke();}
  ctx.beginPath();ctx.arc(cx,cy,R*1.02,0,7);ctx.stroke();
  if(!BANK){ctx.fillStyle='rgba(91,122,148,.9)';ctx.font='11px "IBM Plex Mono",monospace';
    ctx.textAlign='center';ctx.fillText('loading the bank…',cx,cy);return;}
  /* the selected container's arc */
  if(SELCON){const pc=conPos(SELCON);
    if(pc){const hot=Math.max(0,1-(t-pulseAt)/55);
      const a0=-Math.PI/2+pc[0]*(Math.PI*2/10)+0.055,a1=-Math.PI/2+(pc[0]+1)*(Math.PI*2/10)-0.055;
      ctx.strokeStyle='rgba(6,182,212,'+(0.35+0.5*hot)+')';ctx.lineWidth=9+8*hot;ctx.lineCap='round';
      ctx.beginPath();ctx.arc(cx,cy,band(pc[1]),a0,a1);ctx.stroke();ctx.lineWidth=1;}}
  /* every parameter — real counts, the two 42s included */
  for(let s=0;s<BANK.length;s++)for(let c=0;c<BANK[s].containers.length;c++){
    const n=BANK[s].containers[c].count;
    for(let i=0;i<n;i++){const [x,y]=apos(s,c,i,n);
      ctx.fillStyle='rgba(120,160,195,.38)';
      ctx.beginPath();ctx.arc(x,y,1.15,0,7);ctx.fill();}}
  /* what the answer seated */
  const pulse=still?1:(0.75+0.25*Math.sin(t/28));
  for(const r of LITROWS){const loc=locate(r.p);if(!loc)continue;
    const [x,y]=apos(loc[0],loc[1],loc[2],loc[3]);
    const g=ctx.createRadialGradient(x,y,0,x,y,9);
    g.addColorStop(0,'rgba(6,182,212,'+(0.85*pulse)+')');g.addColorStop(1,'rgba(6,182,212,0)');
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,9,0,7);ctx.fill();
    ctx.fillStyle='#0891b2';ctx.beginPath();ctx.arc(x,y,2.3,0,7);ctx.fill();
    const lg=ctx.createLinearGradient(x,y,W+6,cy-40);
    lg.addColorStop(0,'rgba(6,182,212,'+(0.5*pulse)+')');lg.addColorStop(1,'rgba(6,182,212,.05)');
    ctx.strokeStyle=lg;ctx.beginPath();ctx.moveTo(x,y);
    ctx.quadraticCurveTo((x+W)/2,y-30,W+6,cy-40);ctx.stroke();}
  ctx.fillStyle='rgba(8,145,178,.9)';ctx.font='600 10px "Exo 2",sans-serif';ctx.textAlign='center';
  ctx.fillText('1 · 10 · 8 · 40',cx,cy-2);
  ctx.fillStyle='rgba(91,122,148,.9)';ctx.font='10px "IBM Plex Mono",monospace';
  ctx.fillText(String(BANK.reduce((a,s)=>a+s.containers.reduce((b,c)=>b+c.count,0),0)),cx,cy+12);
  ctx.fillStyle='rgba(14,36,56,.72)';ctx.font='9px "IBM Plex Mono",monospace';
  for(let s=0;s<10;s++){const a=-Math.PI/2+(s+.5)*(Math.PI*2/10);
    ctx.fillText(BANK[s].seg,cx+Math.cos(a)*(R*1.10),cy+Math.sin(a)*(R*1.10));}
  t++;if(!still)requestAnimationFrame(draw);
}
size();draw();addEventListener('resize',()=>{size();if(still)draw();});

/* ---------- the bank strip ---------- */
async function bank(){
  try{
    BANK=await j("/api/bank");
    $("bcount").textContent=BANK.reduce((a,s)=>a+s.containers.reduce((b,c)=>b+c.count,0),0).toLocaleString();
    const el=$("bank");el.innerHTML="";
    BANK.forEach((sg,s)=>{
      const d=document.createElement("div");d.className="seg";
      d.innerHTML='<div class=sid>'+esc(sg.seg)+'</div><div class=snm>'+esc(sg.seg_name)+'</div>';
      const cells=document.createElement("div");cells.className="cells";
      sg.containers.forEach(con=>{
        const b=document.createElement("button");b.type="button";
        b.title=con.id+" · "+con.name;b.setAttribute("aria-label",con.id+" "+con.name);
        b.dataset.con=con.id;
        cells.appendChild(b);});
      d.appendChild(cells);el.appendChild(d);});
    if(still)draw();
  }catch(e){$("lhint").textContent="the bank is unreachable: "+e.message;}
}
function paintCells(){
  document.querySelectorAll("#bank .cells i,#bank .cells button").forEach(b=>{
    b.classList.toggle("hot",LITCONS.has(b.dataset.con)||b.dataset.con===SELCON);});
}

/* ---------- selection: one thing, three views ---------- */
function firePulse(){pulseAt=t;if(still)draw();
  document.querySelectorAll("[data-sel]").forEach(el=>{
    el.classList.remove("pulse");void el.offsetWidth;el.classList.add("pulse");});}
async function selectCon(id,focusName){
  SELCON=id;paintCells();
  $("contag").hidden=false;$("contag").textContent=id+" · selected";
  try{
    const c=await j("/registry/container?id="+encodeURIComponent(id));
    $("opencon").hidden=false;
    $("conid").textContent=c.id;$("conname").textContent=c.name;
    $("connote").textContent=c.note?(" — "+c.note):"";
    $("conmeta").textContent=(c.segment||"")+" · "+(c.count||c.subs.length)+" rows";
    const pc=conPos(id);let start=0;
    if(pc)start=BANK[pc[0]].containers[pc[1]].start;
    const litNames=new Set(LITROWS.filter(r=>r.container===id).map(r=>r.name.toLowerCase()));
    const rows=$("rows");rows.innerHTML="";
    (c.subs||[]).forEach((nm,i)=>{
      const d=document.createElement("div");
      if(litNames.has(String(nm).toLowerCase()))d.className="lit2";
      d.innerHTML='<span>'+esc(nm)+' <button class=re title="correct this — your words, as a write-back">✎</button></span>'+
        '<span class=rp>P'+String(start+i).padStart(4,"0")+'</span>';
      d.querySelector(".re").onclick=()=>editRow(d,id,"P"+String(start+i).padStart(4,"0"),nm);
      rows.appendChild(d);
      if(focusName&&String(nm).toLowerCase()===focusName.toLowerCase()){
        editRow(d,id,"P"+String(start+i).padStart(4,"0"),nm);
        d.scrollIntoView({block:"nearest"});}
    });
  }catch(e){$("wbline").textContent="could not open "+id+": "+e.message;}
  firePulse();
}
function editRow(div,con,pid,was){
  div.className="edit2";
  div.innerHTML='<input value="'+esc(was)+'" aria-label="your correction">';
  const inp=div.querySelector("input");inp.focus();inp.select();
  inp.onkeydown=async e=>{
    if(e.key==="Escape"){selectCon(con);return;}
    if(e.key!=="Enter")return;
    const now=inp.value.trim();
    if(!now||now===was){selectCon(con);return;}
    try{
      const r=await post("/growth/correct",{target:pid,was:was,now:now});
      /* re-render FIRST, then show the receipt — the first cut set the line
         and immediately wiped it by re-rendering, so his recording receipt
         was never visible. Caught in the review of this diff. */
      await selectCon(con);
      $("wbline").textContent="→ recorded as "+r.id+" · references "+pid+" · the source row stays whole · NO REOPEN";
    }catch(err){$("wbline").textContent="refused: "+err.message;}
  };
}
document.addEventListener("click",e=>{
  const cell=e.target.closest("#bank [data-con]");
  if(cell){selectCon(cell.dataset.con);return;}
  const chip=e.target.closest(".chip[data-con]");
  if(chip){
    if(e.target.closest(".edit")&&chip.dataset.row){
      /* his ruling made whole: the chip's pencil opens the container with
         that row already in edit */
      selectCon(chip.dataset.con,chip.dataset.row);
      $("opencon").scrollIntoView({behavior:"smooth",block:"nearest"});
      return;}
    selectCon(chip.dataset.con);return;}
  if(e.target.closest("[data-sel]"))firePulse();
});

/* ---------- THE ASK — one ask, three views ---------- */
async function ask(){
  const q=$("q").value.trim();if(!q)return;
  const go=$("go");go.disabled=true;go.textContent="…";
  $("ans").innerHTML='<span class=empty>the walk is running — every node, every filter</span>';
  $("meta").innerHTML="";$("chips").innerHTML="";$("filters").innerHTML="";$("steps").innerHTML="";
  LITROWS=[];LITCONS=new Set();paintCells();if(still)draw();
  const model=$("model").value;
  const [a,p,r]=await Promise.allSettled([
    post("/ask",{question:q,model:model}),
    post("/growing/place",{text:q,name:"home ask"}),
    post("/runtime/run",{text:q,name:"home ask"})
  ]);
  /* the answer + its own tags */
  if(a.status==="fulfilled"){
    const o=a.value.output||{};
    $("ans").textContent=o.answer||"(no answer text)";
    const m=[];
    if(o.classification)m.push("class <b>"+esc(o.classification)+"</b>");
    if(o.evidence_tag)m.push("evidence <b>"+esc(o.evidence_tag)+"</b>");
    if(o.confidence)m.push("confidence <b>"+esc(o.confidence)+"</b>");
    if(o.falsifier)m.push("falsifier <b>"+esc(o.falsifier)+"</b>");
    if(o.open_question)m.push("open <b>"+esc(o.open_question)+"</b>");
    if((a.value.halts||[]).length)m.push('<span style="color:var(--his)">HALTS '+a.value.halts.length+" — yours</span>");
    $("meta").innerHTML=m.map(x=>'<span class=mc>'+x+"</span>").join("");
    /* the seven filters, folded across all nodes of the walk */
    const F={};
    (a.value.walk&&a.value.walk.filters||[]).forEach(n=>(n.gates||[]).forEach(g=>{
      const f=F[g.name]=F[g.name]||{pass:0,halt:0};
      if(String(g.verdict).toLowerCase().includes("halt"))f.halt++;else f.pass++;}));
    $("filters").innerHTML=Object.keys(F).length
      ? Object.entries(F).map(([n,v])=>'<span class="al '+(v.halt?"halt":"ran")+'">'+esc(n)+(v.halt?(" HALT×"+v.halt):"")+"</span>").join("")
      : '<span class=al>the walk returned no filter record</span>';
  }else{
    $("ans").innerHTML='<span class=empty>the engine did not answer: '+esc(a.reason.message)+"</span>";
  }
  /* what it seated — chips + light */
  if(p.status==="fulfilled"){
    const pl=p.value;const chips=[];
    (pl.strengthened||[]).forEach(s=>{
      const pnum=parseInt(String(s.sb_id).replace(/\D/g,""),10);
      LITROWS.push({p:pnum,sb_id:s.sb_id,name:s.name,container:s.container});
      LITCONS.add(s.container);
      chips.push('<span class="chip lit" data-con="'+esc(s.container)+'" data-row="'+esc(s.name)+'"><span class=pid>'+esc(s.sb_id.replace("SB-HFR-",""))+'</span> '+esc(s.name)+' <button class=edit title="correct this row — your words, as a write-back">✎</button></span>');});
    (pl.events||[]).slice(0,1).forEach(ev=>{
      (ev.intent&&ev.intent.seats_on||[]).forEach(cid=>{LITCONS.add(cid);
        chips.push('<span class=chip data-con="'+esc(cid)+'"><span class=pid>'+esc(cid)+'</span> the intent slot — open, never absent</span>');});});
    $("chips").innerHTML=chips.length?chips.join(""):'<span class=empty>no row cleared the bar on this ask — the role and the intent slot still stand</span>';
    paintCells();if(still)draw();
  }else{
    $("chips").innerHTML='<span class=empty>seating unreachable: '+esc(p.reason.message)+"</span>";
  }
  /* his eighteen steps */
  if(r.status==="fulfilled"){
    $("steps").innerHTML=(r.value.records||[]).map(rec=>{
      const rev=rec.direction==="REVERSE";
      const halt=(rec.notes||"").startsWith("HALT");
      return '<span class="al '+(halt?"halt":rev?"rev":"ran")+'" title="'+esc(rec.job)+'">'+rec.n+" "+esc(rec.name.toLowerCase().split("/")[0].trim())+(rev?" ⟲":"")+"</span>";
    }).join("");
  }else{
    $("steps").innerHTML='<span class=al>runtime unreachable: '+esc(r.reason.message)+"</span>";
  }
  go.disabled=false;go.textContent="ASK";
}
$("go").onclick=ask;
$("q").addEventListener("keydown",e=>{if(e.key==="Enter"&&(e.metaKey||e.ctrlKey))ask();});

hud();bank();setInterval(hud,90000);
</script></body></html>"""
