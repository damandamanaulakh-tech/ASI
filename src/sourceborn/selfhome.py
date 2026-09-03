"""THE REWRITE — the new home page, prepared around his choice (2026-09-03).

His words that shaped it: *"as m feeding example and setting some rules in
the system i want an app where i keep changing n it should rewrite its own
code and make changes"* and *"accordignly the dashboard will prepared not
what we have."* He picked **Self-patch, full auto** from the four paths put
to him, so the page is built around that loop and nothing else:

    TEACH (his words in) -> THE PEN WRITES -> THE SUITE IN SHADOW ->
    green: pushed + deployed  ·  red/refused: FILED, shown whole ->
    THE FEED (every patch, its diff, its verdict, his one-click REVERT)

Nothing typed into the markup — every figure comes from GET /selfpatch, and
every rendered value is escaped, because ledger rows can arrive from a
restored backup and his teachings are free text. The reactor is NOT removed:
it stands whole at /reactor, the old desk at /desk (nothing is deleted in
this project, pages included). Light ground — his ruling, no black anywhere.
"""

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Sourceborn — The Rewrite</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Exo+2:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --ground:#f2f6fb; --ground2:#e9f0f8;
  --glass:rgba(255,255,255,.66); --glass2:rgba(255,255,255,.85);
  --edge:#c9dcee; --edge2:#a8c6de;
  --ink:#0e2438; --mut:#5b7a94;
  --beam:#0891b2; --lit:#06b6d4;
  --his:#b45309; --ok:#0f9d76; --bad:#c2410c; --hold:#b45309;
}
*{box-sizing:border-box;margin:0}
body{color:var(--ink);
  font:15px/1.6 'IBM Plex Sans',-apple-system,'Segoe UI',sans-serif;
  background:
    radial-gradient(1100px 520px at 18% -6%, rgba(56,189,248,.14), transparent 60%),
    radial-gradient(900px 600px at 100% 30%, rgba(8,145,178,.10), transparent 55%),
    linear-gradient(180deg, var(--ground), var(--ground2));
  min-height:100vh; padding-bottom:90px}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
.top{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;padding:20px 0 6px}
.name{font:600 22px 'Exo 2',sans-serif;letter-spacing:.02em}
.name small{color:var(--mut);font-weight:500;margin-left:10px;font-size:13px}
.top a{color:var(--beam);text-decoration:none;font-size:13.5px}
.top a:hover{text-decoration:underline}
.lede{color:var(--mut);font-size:13.5px;max-width:88ch;margin:2px 0 14px}
.lede b{color:var(--ink)}
.hud{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:10px;margin:6px 0 18px}
.st{background:var(--glass);border:1px solid var(--edge);border-radius:13px;padding:10px 13px;
  backdrop-filter:blur(8px)}
.st .n{font:600 21px 'Exo 2',sans-serif;font-variant-numeric:tabular-nums}
.st .l{color:var(--mut);font-size:11px;line-height:1.35;margin-top:2px}
.st.on .n{color:var(--ok)} .st.off .n{color:var(--bad)}
.cols{display:grid;grid-template-columns:minmax(340px,5fr) minmax(280px,3fr);gap:16px}
@media(max-width:900px){.cols{grid-template-columns:1fr}}
.panel{background:var(--glass);border:1px solid var(--edge);border-radius:16px;
  padding:16px 18px;backdrop-filter:blur(10px);margin-bottom:16px}
.panel h2{font:600 12.5px 'Exo 2',sans-serif;letter-spacing:.16em;text-transform:uppercase;
  color:var(--mut);margin:0 0 10px}
textarea{width:100%;min-height:110px;border:1px solid var(--edge2);border-radius:12px;
  padding:11px 13px;font:14.5px/1.55 'IBM Plex Sans',sans-serif;color:var(--ink);
  background:var(--glass2);resize:vertical}
textarea:focus{outline:2px solid var(--lit)}
.teachrow{display:flex;gap:10px;align-items:center;margin-top:10px;flex-wrap:wrap}
select{border:1px solid var(--edge2);border-radius:10px;padding:8px 10px;font:13.5px 'IBM Plex Sans';
  color:var(--ink);background:var(--glass2);max-width:240px}
button{border:0;border-radius:11px;padding:10px 18px;font:600 14px 'Exo 2',sans-serif;
  letter-spacing:.03em;cursor:pointer;color:#fff;
  background:linear-gradient(135deg,var(--beam),var(--lit))}
button:disabled{opacity:.5;cursor:wait}
button.rv{background:none;color:var(--bad);border:1px solid var(--bad);padding:5px 12px;
  font-size:12px;border-radius:9px}
.law{color:var(--mut);font-size:12.5px;margin-top:9px}
.law b{color:var(--his)}
.arm td{padding:5px 8px;font-size:13.5px;border-top:1px solid var(--edge);vertical-align:top}
.arm td:first-child{font-family:'IBM Plex Mono',monospace;font-size:12.5px;white-space:nowrap}
.arm{width:100%;border-collapse:collapse}
.yes{color:var(--ok);font-weight:600}.no{color:var(--bad);font-weight:600}
.row{background:var(--glass2);border:1px solid var(--edge);border-radius:14px;
  padding:13px 15px;margin:10px 0}
.row .his{font-size:14.5px}
.row .his:before{content:'\201C';color:var(--mut)}
.row .his:after{content:'\201D';color:var(--mut)}
.meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 4px}
.chip{font:600 10.5px 'Exo 2',sans-serif;letter-spacing:.06em;text-transform:uppercase;
  border-radius:999px;padding:3px 10px;border:1px solid var(--edge2);color:var(--mut)}
.chip.PUSHED{color:var(--ok);border-color:rgba(15,157,118,.5);background:rgba(15,157,118,.07)}
.chip.SHADOWRED,.chip.REFUSEDHELD,.chip.REFUSEDMALFORMED,.chip.REFUSEDPUSH,.chip.REFUSEDDOOROPEN,.chip.REFUSEDNOMODEL{
  color:var(--bad);border-color:rgba(194,65,12,.5);background:rgba(194,65,12,.06)}
.chip.HELDUNARMED,.chip.SHADOWGREEN,.chip.DRAFTED{color:var(--hold);border-color:rgba(180,83,9,.5)}
.why{color:var(--mut);font-size:13px;margin:5px 0}
.files{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.files code{font:12px 'IBM Plex Mono',monospace;background:var(--glass);
  border:1px solid var(--edge);border-radius:7px;padding:2px 8px;cursor:pointer}
.files code:hover{border-color:var(--lit)}
pre.diff{display:none;font:11.5px/1.5 'IBM Plex Mono',monospace;background:#0e2438;color:#dbe9f6;
  border-radius:10px;padding:10px 12px;overflow-x:auto;margin:6px 0;max-height:340px}
pre.diff.open{display:block}
pre.diff .add{color:#7ee2b8}pre.diff .del{color:#ffb4a0}
.sha a{font:12px 'IBM Plex Mono',monospace;color:var(--beam)}
.never td{padding:4px 8px;font-size:12.5px;border-top:1px solid var(--edge);color:var(--mut)}
.never td:first-child{font-family:'IBM Plex Mono',monospace;color:var(--ink);white-space:nowrap}
.never{width:100%;border-collapse:collapse}
.busy{display:none;color:var(--his);font-size:13px;margin-top:8px}
.busy.on{display:block}
.err{color:var(--bad);font-size:13px;margin-top:8px}
</style></head><body><div class=wrap>
<div class=top>
 <div class=name>THE REWRITE<small>it rewrites its own code — full auto, on your word</small></div>
 <div style="margin-left:auto;display:flex;gap:14px;flex-wrap:wrap">
  <a href="/reactor">&#9883; the reactor</a><a href="/engine">&#9881; the engine</a>
  <a href="/reading">&#128300; the reading</a><a href="/exists">what exists</a>
  <a href="/desk">&#9638; desk</a><a href="/sbx">the split</a>
 </div>
</div>
<p class=lede>You teach; <b>the pen writes the patch</b>; the <b>whole suite runs
against a shadow copy</b>; green means it is <b>committed and deployed with no
approval step</b> — your choice. Your authority is after the fact and total:
every patch stands below with its before/after, and <b>revert is one click and
one new commit</b>. What the pen may never touch is listed at the right, and the
suite it must satisfy is the same one that pins every law already built.</p>
<div class=hud id=hud></div>
<div class=cols>
<div>
 <div class=panel>
  <h2>Teach — your words in, its code out</h2>
  <textarea id=t placeholder="an example, a rule, a correction — the pen writes the smallest change that carries it"></textarea>
  <div class=teachrow>
   <select id=tgt><option value="">let the pen pick the module</option></select>
   <button id=go>TEACH THE MACHINE</button>
  </div>
  <div class=busy id=busy>the pen is writing — the draft, then the whole suite in
  shadow (about two minutes). This page will show the row when it lands.</div>
  <div class=err id=err></div>
  <div class=law id=doorlaw></div>
 </div>
 <div class=panel>
  <h2>The feed — every patch, whole</h2>
  <div id=feed><span class=why>reading the ledger&hellip;</span></div>
 </div>
</div>
<div>
 <div class=panel>
  <h2>The arming — your three switches</h2>
  <table class=arm id=arm></table>
  <div class=law>Set these in Render &rarr; Environment. <b>SB_GITHUB_TOKEN</b>:
  a fine-grained token, Contents read&amp;write, this one repo.
  <b>SB_REPO</b>: owner/name of the deploy repo. A model key
  (<b>ANTHROPIC_API_KEY</b> or another) arms the drafter. Until all three
  exist, a green patch is <b>HELD-UNARMED</b> with the whole patch kept —
  nothing is lost by arming later. And the pen moves only behind your
  password: set <b>SB_ACCESS_PASS</b> or teach/revert refuse, because the pen
  writes into <i>your</i> GitHub.</div>
 </div>
 <div class=panel>
  <h2>What the pen may never touch</h2>
  <table class=never id=never></table>
 </div>
 <div class=panel>
  <h2>The four laws</h2>
  <div id=laws class=why></div>
 </div>
</div>
</div>
</div><script>
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cls=s=>String(s||'').replace(/[^A-Za-z]/g,'');
let REPO='';
function hud(s){
 const c=(n,l,mode)=>'<div class="st '+(mode||'')+'"><div class=n>'+n+'</div><div class=l>'+esc(l)+'</div></div>';
 document.getElementById('hud').innerHTML=
  c(esc(s.arming.armed?'ARMED':'NOT ARMED'),'the pen '+(s.arming.armed?'can push':'cannot push yet'),s.arming.armed?'on':'off')+
  c(esc(s.door.locked?'LOCKED':'OPEN'),'the front door'+(s.door.locked?'':' — set SB_ACCESS_PASS'),s.door.locked?'on':'off')+
  c(s.patches,'teachings filed')+
  c(s.pushed,'patches pushed &amp; deployed')+
  c(s.reverts,'reverts — his word, kept')+
  c(s.field.modules,'modules in the pen’s field')+
  c(Object.keys(s.field.held).length+s.field.never.length,'held from the pen');
}
function arm(a,d){
 const yn=v=>v?'<span class=yes>present</span>':'<span class=no>absent</span>';
 document.getElementById('arm').innerHTML=
  '<tr><td>SB_GITHUB_TOKEN</td><td>'+yn(a.SB_GITHUB_TOKEN)+'</td></tr>'+
  '<tr><td>SB_REPO</td><td>'+(a.SB_REPO?'<span class=yes>'+esc(a.SB_REPO)+'</span>':'<span class=no>absent</span>')+'</td></tr>'+
  '<tr><td>SB_BRANCH</td><td>'+esc(a.SB_BRANCH)+'</td></tr>'+
  '<tr><td>drafting model</td><td>'+(a.model_armed?'<span class=yes>'+esc(a.drafting_model)+'</span>':'<span class=no>offline &mdash; no key</span>')+'</td></tr>'+
  '<tr><td>SB_ACCESS_PASS</td><td>'+yn(d.locked)+'</td></tr>';
 document.getElementById('doorlaw').innerHTML=d.locked?'':('<b>the door is open:</b> '+esc(d.law));
}
function never(f){
 let h='';
 for(const [name,why] of Object.entries(f.held)) h+='<tr><td>'+esc(name)+'</td><td>'+esc(why)+'</td></tr>';
 for(const n of f.never) h+='<tr><td>'+esc(n.path)+'</td><td>'+esc(n.why)+'</td></tr>';
 document.getElementById('never').innerHTML=h;
}
function colordiff(d){
 return esc(d).split('\n').map(l=>l.startsWith('+')?'<span class=add>'+l+'</span>':l.startsWith('-')?'<span class=del>'+l+'</span>':l).join('\n');
}
function row(r){
 if(r.kind==='UNREADABLE')return '<div class=row><div class=why>UNREADABLE ledger line '+esc(r.line)+' &mdash; kept, never dropped: <code>'+esc(r.raw)+'</code></div></div>';
 if(r.kind==='REVERT')return '<div class=row><div class=meta><span class="chip PUSHED">REVERT</span>'+
   '<span class=why>'+esc(r.id)+' &middot; '+esc(r.at)+' &middot; restores what stood before '+esc(r.of)+'</span>'+
   (r.sha&&REPO?'<span class=sha><a target=_blank href="https://github.com/'+esc(REPO)+'/commit/'+esc(r.sha)+'">'+esc(String(r.sha).slice(0,10))+'</a></span>':'')+'</div></div>';
 let h='<div class=row><div class=his>'+esc(r.teaching)+'</div><div class=meta>'+
  '<span class="chip '+cls(r.stage)+'">'+esc(r.stage)+'</span>'+
  '<span class=why>'+esc(r.id)+' &middot; '+esc(r.at)+(r.target?' &middot; target: '+esc(r.target):'')+'</span>';
 if(r.sha&&REPO)h+='<span class=sha><a target=_blank href="https://github.com/'+esc(REPO)+'/commit/'+esc(r.sha)+'">'+esc(String(r.sha).slice(0,10))+'</a></span>';
 if(r.stage==='PUSHED')h+='<button class=rv onclick="doRevert(\''+esc(r.id)+'\')">revert &mdash; one new commit</button>';
 h+='</div>';
 if(r.why_the_pen_wrote_it)h+='<div class=why><b>the pen:</b> '+esc(r.why_the_pen_wrote_it)+'</div>';
 for(const s of (r.stages||[])){
  if(s.why)h+='<div class=why>'+esc(s.stage)+': '+esc(s.why)+'</div>';
  if(s.tests)h+='<div class=why>'+esc(s.stage)+': '+esc(s.tests)+'</div>';
  if(s.tail)h+='<pre class="diff open">'+esc(s.tail)+'</pre>';
 }
 if(r.diffs&&r.diffs.length){
  h+='<div class=files>'+r.diffs.map((d,i)=>'<code onclick="tog(this)">'+esc(d.path)+(d.created?' (new)':'')+'</code><pre class=diff>'+colordiff(d.diff)+'</pre>').join('')+'</div>';
 }
 return h+'</div>';
}
function tog(el){const p=el.nextElementSibling;if(p)p.classList.toggle('open');}
async function doRevert(id){
 if(!confirm('Revert '+id+'? A NEW commit restores what stood before; the patch row and its commit stay in history.'))return;
 try{
  const r=await(await fetch('/selfpatch/revert',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({id})})).json();
  if(r.refused)document.getElementById('err').textContent=r.refused;
 }catch(e){document.getElementById('err').textContent=String(e);}
 boot();
}
async function boot(){
 let s;
 try{s=await(await fetch('/selfpatch')).json();}
 catch(e){document.getElementById('feed').innerHTML='<div class=err>could not read the pen: '+esc(e)+'</div>';return;}
 REPO=(s.state.arming.SB_REPO||'');
 hud(s.state);arm(s.state.arming,s.state.door);never(s.state.field);
 document.getElementById('laws').innerHTML=s.state.laws.map(l=>'&bull; '+esc(l)).join('<br>');
 const f=document.getElementById('feed');
 f.innerHTML=(s.report.rows||[]).map(row).join('')||'<div class=why>nothing taught yet — the first row lands here, whatever its verdict.</div>';
 const sel=document.getElementById('tgt');
 if(sel.options.length<=1&&s.modules){for(const m of s.modules){const o=document.createElement('option');o.value=m;o.textContent=m;sel.appendChild(o);}}
}
document.getElementById('go').onclick=async()=>{
 const t=document.getElementById('t').value.trim();
 if(!t)return;
 const b=document.getElementById('go');b.disabled=true;
 document.getElementById('busy').classList.add('on');
 document.getElementById('err').textContent='';
 try{
  const r=await(await fetch('/selfpatch/teach',{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({text:t,target:document.getElementById('tgt').value})})).json();
  if(r.error)document.getElementById('err').textContent=r.error;
  else document.getElementById('t').value='';
 }catch(e){document.getElementById('err').textContent=String(e);}
 b.disabled=false;document.getElementById('busy').classList.remove('on');
 boot();
};
boot();
</script></body></html>"""


def annotations() -> list:
    return [
        ("accordignly the dashboard will prepared not what we have",
         "selfhome.PAGE"),
        ("the reactor is not removed — it stands whole at /reactor",
         "selfhome.PAGE"),
    ]
