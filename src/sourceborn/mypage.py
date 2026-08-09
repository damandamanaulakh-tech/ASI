"""MY PAGE — the page HE edits from inside the app.

His ask, verbatim: "give me App web page to edit, and let me define what
where how it should show" — and Phase-5 before it: "App itself having the
capacity when i want to change any link or ID for that it will be done
from there, means what i'm writing here i should do there."

So every block on this page carries his three words as its three fields:

    WHAT  — which content the block shows (a live feed, his text, his links)
    WHERE — which section it sits in, and its order there
    HOW   — the form it takes (card · list · table · number · text · links)

House laws, enforced here the same as everywhere else:
  - nothing is removed: a block is PARKED, never deleted, and comes back;
  - every save is a NEW version, all versions kept; restoring an old layout
    saves a new version that references it — the old one is never reopened;
  - no external CDN, no framework — the page works on the offline lane.

Storage:  <SB_ROOT>/mypage/layout.json          (current)
          <SB_ROOT>/mypage/versions/vNNNN.json  (every save, forever)
"""
from __future__ import annotations

import json
import os

from .models import _now

# ---------------------------------------------------------------- WHAT
# Sources a block can show. "live" ones are resolved by the server at view
# time; "his" ones hold what he typed, inside the layout itself.
SOURCES = {
    "health": "engine — model · brains · weekly update",
    "memory": "memory report — corpus · wisdom · live fact",
    "chats": "last chats — question · confidence · holds",
    "library": "library — uploaded and ingested files",
    "brains": "the 95 brains — 70 SB + 25 URR",
    "ladder": "System-1 ladder — locked, Phase-1 done",
    "filters": "the seven filters, in order",
    "routes": "route registry v1 — the 11 re-sequence routes",
    "phases": "the phases — done · in progress · waiting",
    "open": "open on his word — the red list",
    "text": "his words — free text, kept verbatim",
    "links": "his links and IDs — name + target, editable here",
}
HOWS = ("card", "list", "table", "number", "text", "links")


def _dir(root: str) -> str:
    d = os.path.join(root, "mypage")
    os.makedirs(os.path.join(d, "versions"), exist_ok=True)
    return d


def default_layout() -> dict:
    """First-run starter. He reshapes everything from inside the page."""
    return {
        "version": 0,
        "saved_at": _now(),
        "note": "starter layout — his to reshape",
        "references": None,
        "sections": [
            {"id": "s1", "title": "NOW", "cols": 3, "blocks": [
                {"id": "b1", "title": "Engine", "what": "health",
                 "how": "card", "parked": False},
                {"id": "b2", "title": "The Ladder — Phase-1 done",
                 "what": "ladder", "how": "table", "parked": False},
                {"id": "b3", "title": "Phases", "what": "phases",
                 "how": "list", "parked": False},
            ]},
            {"id": "s2", "title": "HIS DESK", "cols": 2, "blocks": [
                {"id": "b4", "title": "My words", "what": "text",
                 "how": "text", "parked": False,
                 "text": "write here — this box keeps your exact words"},
                {"id": "b5", "title": "My links and IDs", "what": "links",
                 "how": "links", "parked": False,
                 "links": [{"name": "chats", "url": "/chats"},
                           {"name": "library", "url": "/library"},
                           {"name": "brains", "url": "/brains"},
                           {"name": "memory report", "url": "/memory/report"}]},
            ]},
        ],
    }


def load_layout(root: str) -> dict:
    fp = os.path.join(_dir(root), "layout.json")
    if not os.path.exists(fp):
        return default_layout()
    with open(fp, encoding="utf-8") as f:
        return json.load(f)


def save_layout(root: str, layout: dict, note: str = "",
                references: int | None = None) -> dict:
    """Every save is a new version; every version is kept forever."""
    d = _dir(root)
    prev = load_layout(root)
    version = int(prev.get("version", 0)) + 1
    layout = dict(layout)
    layout["version"] = version
    layout["saved_at"] = _now()
    layout["note"] = str(note or "")[:200]
    layout["references"] = references
    # sanitise: unknown WHAT/HOW are kept but flagged, never dropped
    for sec in layout.get("sections", []):
        for b in sec.get("blocks", []):
            if b.get("what") not in SOURCES:
                b["flag"] = f"unknown what: {b.get('what')}"
            if b.get("how") not in HOWS:
                b["flag"] = f"unknown how: {b.get('how')}"
    with open(os.path.join(d, "versions", f"v{version:04d}.json"), "w",
              encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=1)
    with open(os.path.join(d, "layout.json"), "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=1)
    return layout


def list_versions(root: str) -> list[dict]:
    vd = os.path.join(_dir(root), "versions")
    out = []
    for fn in sorted(os.listdir(vd)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(vd, fn), encoding="utf-8") as f:
                d = json.load(f)
            out.append({"version": d.get("version"), "saved_at": d.get("saved_at"),
                        "note": d.get("note", ""),
                        "references": d.get("references")})
        except Exception:
            continue
    return out


def get_version(root: str, n: int) -> dict | None:
    fp = os.path.join(_dir(root), "versions", f"v{int(n):04d}.json")
    if not os.path.exists(fp):
        return None
    with open(fp, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- feeds
# The locked, non-live sources — served from the spec, not invented.
LADDER_ROWS = [
    ("SYSTEM", "1", "ASI"),
    ("SEGMENT", "10", "the human ten"),
    ("CONTAINER", "200", "the frame stays 200 — filled over time"),
    ("PARAMETER", "3,072", "SB-ASI-P0001 …"),
    ("ELEMENT", "—", "empty; the name is his call"),
]
FILTERS = ["1 Ground", "2 Sequence", "3 Source", "4 Mask", "5 Fact",
           "6 Halt", "7 Loop"]
ROUTES = [
    "L1 AVAILABILITY → AVAILABILITY", "L2 QUALIFICATION → SELECTION",
    "L3 TESTING → DECISION/CHOICE", "L4 NO-branch → REQUIREMENT EMERGES",
    "L5 VERIFICATION → REQUIREMENT", "L6 FEEDBACK → PRIOR REALITY",
    "L7 MEMORY VALIDATION → INFORMATION", "L8 COMPRESSION → MEMORY",
    "L9 MEMORY UPDATE → ORIGIN/SOURCE",
    "L10 DECISION/CHOICE → SELECTION · pending first live case",
    "L11 RETURN → ENVIRONMENT/HOST · UNVALIDATED — awaits T-5",
]
PHASES = [
    "P1 · define Sequence — DONE, his word",
    "P2 · Human · AI · Holy Books · ASI — IN PROGRESS",
    "P2a · his uploads — his hand",
    "P3 · nodes + brain memory — waiting",
    "P4 · examples, RH his way — waiting",
    "P5 · live app, edit from inside — THIS PAGE is its first piece",
]
OPEN_ITEMS = [
    "element name (18.2)", "9.3 Para ID — merge or omit",
    "Rule-5 wording", "container-ID overlap 121–160 vs 081–160",
    "transition vs step (01B vs 01)", "contamination check (13.3)",
    "the model lock — locks on his word only",
]


PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>MY PAGE — Sourceborn</title><style>
:root{--bg:#070809;--panel:#0f1219;--elev:#141826;--line:#1c2230;--line2:#262d3d;
--ink:#eef2f8;--mut:#7d8699;--acc:#7c8bff;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;
--grad:linear-gradient(135deg,#7c8bff,#a78bfa 60%,#f0abfc)}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);font:15px/1.5 'Inter',-apple-system,Segoe UI,Roboto,sans-serif;
background:radial-gradient(900px 520px at 85% -8%,rgba(124,139,255,.14),transparent 60%),var(--bg)}
.app{max-width:1240px;margin:0 auto;padding:0 18px 80px}
.top{position:sticky;top:0;z-index:9;display:flex;justify-content:space-between;align-items:center;
gap:10px;padding:14px 2px;background:linear-gradient(180deg,rgba(7,8,9,.9),rgba(7,8,9,.4));
backdrop-filter:blur(12px);border-bottom:1px solid var(--line);flex-wrap:wrap}
.name{font-weight:700;font-size:18px}.name small{color:var(--mut);font-weight:400;margin-left:8px}
button,select,input,textarea{font:inherit;color:var(--ink);background:var(--panel);
border:1px solid var(--line2);border-radius:9px;padding:7px 12px}
button{cursor:pointer}button:hover{border-color:var(--acc)}
button.pri{background:var(--grad);border:0;color:#0a0a14;font-weight:700}
button.mini{padding:3px 9px;font-size:12px;border-radius:7px}
.sec{margin:26px 0 8px;display:flex;align-items:center;gap:10px}
.sec h2{margin:0;font-size:14px;letter-spacing:.14em;color:var(--mut)}
.sec input{font-size:14px;letter-spacing:.14em}
.grid{display:grid;gap:14px}
.blk{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;min-height:70px}
.blk h3{margin:0 0 8px;font-size:14px}
.blk .src{color:var(--mut);font-size:11.5px;margin-left:8px}
.blk table{width:100%;border-collapse:collapse;font-size:13.5px}
.blk td{padding:4px 6px;border-top:1px solid var(--line)}
.blk td:first-child{color:var(--mut)}
.blk ul{margin:4px 0;padding-left:18px;font-size:13.5px}
.blk li{margin:3px 0}
.blk .big{font-size:34px;font-weight:700;background:var(--grad);
-webkit-background-clip:text;background-clip:text;color:transparent}
.blk .txt{white-space:pre-wrap;font-size:14px}
.blk a{color:var(--acc);text-decoration:none}.blk a:hover{text-decoration:underline}
.ctl{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;padding-top:10px;border-top:1px dashed var(--line2)}
.ctl select,.ctl input{padding:3px 8px;font-size:12px;border-radius:7px}
.parked{opacity:.55;border-style:dashed}
.shelf{margin-top:34px;border-top:1px solid var(--line2);padding-top:10px}
.note{color:var(--mut);font-size:12.5px}
textarea{width:100%;min-height:90px}
.badge{font-size:11px;border:1px solid var(--line2);border-radius:999px;padding:2px 9px;color:var(--mut)}
</style></head><body><div class=app>
<div class=top>
 <div class=name>MY PAGE<small>what · where · how — yours to define</small></div>
 <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
  <span class=badge id=ver></span>
  <select id=versions title="every save is kept"></select>
  <button class=mini onclick="loadVersion()">load version</button>
  <button id=mode onclick="toggle()">EDIT</button>
  <button class=pri id=save onclick="save()" style="display:none">SAVE — new version</button>
  <a href="/" style="color:var(--mut);font-size:13px;margin-left:6px">← app</a>
 </div>
</div>
<div id=root></div>
<div class=shelf id=shelf style="display:none"></div>
<div class=note style="margin-top:26px">Nothing here is deleted — a block is <b>parked</b> and returns.
Every save is a new version and every version is kept; loading an old one saves a new version that references it.</div>
</div><script>
let L=null,E=false,FEEDS={},SRC={},HOWS=[];
const $=q=>document.querySelector(q);
async function j(u,opt){const r=await fetch(u,opt);return r.json()}
async function boot(){
 const m=await j('/page/meta');SRC=m.sources;HOWS=m.hows;
 L=await j('/page/layout');
 FEEDS=await j('/page/data');
 const vs=await j('/page/versions');const sel=$('#versions');sel.innerHTML='';
 vs.slice().reverse().forEach(v=>{const o=document.createElement('option');
  o.value=v.version;o.textContent='v'+v.version+' · '+(v.note||v.saved_at);sel.appendChild(o)});
 if(location.hash==='#edit')E=true;
 render();
}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function feedHTML(b){
 const d=FEEDS[b.what];
 if(b.what==='text')return '<div class=txt>'+esc(b.text||'')+'</div>';
 if(b.what==='links')return '<ul>'+(b.links||[]).map(l=>'<li><a href="'+esc(l.url)+'">'+esc(l.name)+'</a> <span class=src>'+esc(l.url)+'</span></li>').join('')+'</ul>';
 if(!d)return '<div class=note>no feed</div>';
 if(b.how==='number'){const n=(typeof d.number!=='undefined')?d.number:(Array.isArray(d.rows)?d.rows.length:'—');
  return '<div class=big>'+esc(n)+'</div><div class=note>'+esc(d.label||'')+'</div>'}
 if(b.how==='table'&&d.rows)return '<table>'+d.rows.map(r=>'<tr>'+r.map(c=>'<td>'+esc(c)+'</td>').join('')+'</tr>').join('')+'</table>';
 if(d.rows)return '<ul>'+d.rows.map(r=>'<li>'+esc(Array.isArray(r)?r.join(' — '):r)+'</li>').join('')+'</ul>';
 return '<div class=note>'+esc(JSON.stringify(d))+'</div>';
}
function blockHTML(b,si,bi){
 let h='<div class="blk'+(b.parked?' parked':'')+'"><h3>'+esc(b.title||SRC[b.what]||b.what)
   +'<span class=src>'+esc(b.what)+' · '+esc(b.how)+'</span></h3>'+feedHTML(b);
 if(E){
  h+='<div class=ctl>'
   +'<input value="'+esc(b.title||'')+'" placeholder=title onchange="upd('+si+','+bi+',\'title\',this.value)">'
   +'<select onchange="upd('+si+','+bi+',\'what\',this.value)">'+Object.keys(SRC).map(k=>'<option'+(k===b.what?' selected':'')+'>'+k+'</option>').join('')+'</select>'
   +'<select onchange="upd('+si+','+bi+',\'how\',this.value)">'+HOWS.map(k=>'<option'+(k===b.how?' selected':'')+'>'+k+'</option>').join('')+'</select>'
   +'<button class=mini onclick="mv('+si+','+bi+',-1)">↑</button>'
   +'<button class=mini onclick="mv('+si+','+bi+',1)">↓</button>'
   +'<button class=mini onclick="hop('+si+','+bi+')">→ section</button>'
   +'<button class=mini onclick="park('+si+','+bi+')">'+(b.parked?'return':'park')+'</button>';
  if(b.what==='text')h+='<textarea onchange="upd('+si+','+bi+',\'text\',this.value)">'+esc(b.text||'')+'</textarea>';
  if(b.what==='links')h+='<textarea placeholder="one per line:  name | url-or-id" onchange="setLinks('+si+','+bi+',this.value)">'
    +esc((b.links||[]).map(l=>l.name+' | '+l.url).join('\n'))+'</textarea>';
  h+='</div>';
 }
 return h+'</div>';
}
function render(){
 $('#ver').textContent='v'+L.version+' · '+(L.saved_at||'');
 const R=$('#root');R.innerHTML='';
 L.sections.forEach((s,si)=>{
  const head=document.createElement('div');head.className='sec';
  head.innerHTML=E?('<input value="'+esc(s.title)+'" onchange="L.sections['+si+'].title=this.value">'
    +'<select onchange="L.sections['+si+'].cols=+this.value;render()">'+[1,2,3,4].map(c=>'<option'+(c==s.cols?' selected':'')+'>'+c+'</option>').join('')+'</select>'
    +'<button class=mini onclick="addBlock('+si+')">+ block</button>')
   :('<h2>'+esc(s.title)+'</h2>');
  R.appendChild(head);
  const g=document.createElement('div');g.className='grid';
  g.style.gridTemplateColumns='repeat('+(s.cols||2)+',1fr)';
  s.blocks.forEach((b,bi)=>{if(b.parked&&!E)return;
   const d=document.createElement('div');d.innerHTML=blockHTML(b,si,bi);g.appendChild(d.firstChild)});
  R.appendChild(g);
 });
 if(E){const add=document.createElement('button');add.textContent='+ section';
  add.onclick=()=>{L.sections.push({id:'s'+Date.now(),title:'NEW SECTION',cols:2,blocks:[]});render()};
  add.style.marginTop='20px';R.appendChild(add)}
 $('#save').style.display=E?'':'none';$('#mode').textContent=E?'VIEW':'EDIT';
}
function upd(si,bi,k,v){L.sections[si].blocks[bi][k]=v;render()}
function setLinks(si,bi,v){L.sections[si].blocks[bi].links=v.split('\n').filter(x=>x.trim())
 .map(x=>{const p=x.split('|');return{name:(p[0]||'').trim(),url:(p[1]||'').trim()}});render()}
function mv(si,bi,d){const a=L.sections[si].blocks;const t=bi+d;
 if(t<0||t>=a.length)return;[a[bi],a[t]]=[a[t],a[bi]];render()}
function hop(si,bi){const t=(si+1)%L.sections.length;
 L.sections[t].blocks.push(L.sections[si].blocks.splice(bi,1)[0]);render()}
function park(si,bi){const b=L.sections[si].blocks[bi];b.parked=!b.parked;render()}
function addBlock(si){L.sections[si].blocks.push({id:'b'+Date.now(),title:'',what:'text',how:'text',text:'',parked:false});render()}
function toggle(){E=!E;render()}
async function save(){
 const note=prompt('name this version (optional)')||'';
 L=await j('/page/save',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({layout:L,note})});
 E=false;await boot();
}
async function loadVersion(){
 const n=$('#versions').value;if(!n)return;
 const old=await j('/page/version?n='+n);
 if(old.error)return alert(old.error);
 L=await j('/page/save',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({layout:old,note:'restored from v'+n,references:+n})});
 await boot();
}
boot();
</script></body></html>"""
