"""THE GENERATION page — /generation.

His order: "now build this generation in the app". One locked identity, a
brain-state pack, the container x state addresses it generates, an optional
forked event, and every candidate sitting at REVIEW_REQUIRED.

Every interpolated value is escaped — an ask is untrusted input.
"""

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>THE GENERATION — same person, many brains</title>
<style>
:root{--bg:#07090c;--ink:#e8eef6;--dim:#8fa3b8;--line:#1b2430;--card:#0d1218;
--dom:#f87171;--act:#4ade80;--auto:#60a5fa;--comp:#fbbf24;--conf:#c084fc;
--sup:#64748b;--his:#60a5fa}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
header{padding:18px 20px 12px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:15px;letter-spacing:.14em}
.sub{color:var(--dim);font-size:12px;margin-top:6px}
main{padding:18px 20px 60px;max-width:1240px}
h2{font-size:12px;letter-spacing:.16em;color:var(--dim);margin:26px 0 8px;
border-bottom:1px solid var(--line);padding-bottom:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:12px 14px;margin-bottom:10px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
input,select{background:var(--card);color:var(--ink);border:1px solid var(--line);
border-radius:6px;padding:9px 10px;font:inherit}
input{min-width:220px}
button{background:#15304a;color:var(--ink);border:1px solid #22507a;
border-radius:6px;padding:9px 16px;cursor:pointer;font:inherit}
button:hover{border-color:#3a6fa0}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;color:var(--dim);font-weight:400;font-size:11px;
letter-spacing:.1em;padding:5px 8px;border-bottom:1px solid var(--line)}
td{padding:5px 8px;border-bottom:1px solid #121a24;vertical-align:top}
.k{color:var(--dim);font-size:11px;letter-spacing:.1em}
.mine{color:var(--dim);font-size:11px}
.pid{color:var(--his);white-space:nowrap}
.lock{font-size:17px;letter-spacing:.08em;color:var(--his)}
.st{display:inline-block;padding:1px 8px;border-radius:99px;font-size:11px;
border:1px solid currentColor}
.Dominant{color:var(--dom)}.Active{color:var(--act)}.Automatic{color:var(--auto)}
.Compensated{color:var(--comp)}.Conflicted{color:var(--conf)}
.Suppressed{color:var(--sup)}
.pill{display:inline-block;border:1px solid var(--line);border-radius:99px;
padding:1px 9px;font-size:11px;color:var(--dim);margin:2px 3px 2px 0}
.count{display:flex;gap:20px;flex-wrap:wrap;align-items:baseline}
.count b{font-size:23px;font-weight:600}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:10px}
.law{color:var(--dom);font-size:11.5px;margin-top:6px}
.zero{color:var(--act)}
pre{margin:0;white-space:pre-wrap;font:inherit;color:var(--dim)}
ul{margin:4px 0 0 18px;padding:0}li{margin:2px 0}
</style></head><body>
<header>
  <h1>THE GENERATION — SAME PERSON, MANY BRAINS</h1>
  <div class=sub>identity locked &middot; conditions change &middot; container
  &times; state generates a RUNTIME ADDRESS &middot; instantiated address is not
  a native parameter &middot; his source document is never rewritten, and the system GROWS &mdash; additions go to the growth ledger, nothing is ever removed</div>
</header>
<main>
  <div class=row>
    <input id=who placeholder="the person (identity is locked)" value="The King">
    <select id=pack></select>
    <select id=ev>
      <option value="">— no event fork —</option>
    </select>
    <button id=run>GENERATE</button>
  </div>
  <div id=out></div>
  <div id=led></div>
</main>
<script>
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,
  c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}

// the event list comes from the server, never from a copy typed in here — a
// hardcoded list is how his eleventh event would have stayed invisible
async function boot(){
  const r=await fetch('/generation/packs'); const d=await r.json();
  document.getElementById('pack').innerHTML=d.packs.map(p=>
    `<option value="${esc(p.id)}">${esc(p.id)} &middot; ${esc(p.name)} &middot; MODEL ${esc(p.model)}</option>`).join('');
  document.getElementById('ev').innerHTML+=(d.events||[]).map(e=>
    `<option value="${esc(e)}">${esc(String(e).replace(/_/g,' '))}</option>`).join('');
  ledger();
  go();
}

// HIS LIVE INTENT LEDGER — one event, ten states, ten falsifiers, none chosen
async function ledger(){
  let d; try{ d=await (await fetch('/ledger')).json(); }catch(e){ return; }
  const r=d.run, c=r.counts, o=[];
  o.push('<h2>HIS LIVE INTENT LEDGER &mdash; ONE EVENT, TEN STATES, TEN FALSIFIERS</h2>'+
    `<div class=card><div class=lock>&ldquo;${esc(r.event)}&rdquo;</div>`+
    `<div class=mine>actor: ${esc(r.actor)} &middot; shell ${esc(r.event_shell)}</div>`+
    '<div class=count style=margin-top:8px>'+
    `<div><div class=k>CANDIDATES</div><b>${c.generated}</b></div>`+
    `<div><div class=k>FALSIFIABLE</div><b class=zero>${r.all_falsifiable?c.generated:'NO'}</b></div>`+
    `<div><div class=k>TESTED</div><b>${c.tested}</b></div>`+
    `<div><div class=k>KILLED</div><b>${c.killed}</b></div>`+
    `<div><div class=k>SURVIVED</div><b>${c.survived}</b></div>`+
    `<div><div class=k>UNTESTED</div><b>${c.untested}</b></div>`+
    `<div><div class=k>DELETED</div><b class=zero>${c.deleted}</b></div>`+
    `<div><div class=k>CANONICAL</div><b class=zero>${d.stats.canonical_intents}</b></div>`+
    `</div><div class=law style=margin-top:6px>${esc(r.law)}</div>`+
    `<div class=mine>${esc(r.refuses)}</div></div>`);
  o.push('<div class=card><table><tr><th>id</th><th>brain-state</th>'+
    '<th>pack here</th><th>the intent he generated</th><th>&Delta;</th>'+
    '<th>what would flip it</th><th>status</th></tr>'+
    r.candidates.map(x=>`<tr><td class=pid>${esc(x.id)}</td>`+
      `<td>${esc(x.state)}</td><td class=mine>${esc(x.pack)}</td>`+
      `<td>${esc(x.intent)}</td><td class=mine>${esc(x.novelty_delta)}</td>`+
      `<td class=mine>${esc(x.falsifier)}</td>`+
      `<td class=${x.status==='KILLED'?'law':'zero'}>${esc(x.status)}`+
      (x.tested?'':' <span class=mine>untested</span>')+`</td></tr>`).join('')+
    '</table></div>');
  const ns=r.namespaces;
  o.push('<h2>THE TWO BANKS &mdash; MAPPED IN, NEVER MERGED</h2><div class=card><table>'+
    '<tr><th>bank</th><th>prefix</th><th>count</th><th>unit</th><th>grid</th></tr>'+
    [ns.workbook,ns.registry].map(b=>`<tr><td>${esc(b.source)}</td>`+
      `<td class=pid>${esc(b.ns)}</td><td><b>${b.count}</b></td>`+
      `<td>${esc(b.unit)}</td><td class=mine>${esc(b.grid)}</td></tr>`).join('')+
    `</table><div class=law>${esc(ns.collision)}</div>`+
    `<div class=mine>his rule: ${esc(ns.rule)} &middot; merged = ${ns.merged}</div></div>`);
  const a=d.audit;
  o.push(`<h2>WHAT HIS WORKBOOK ACTUALLY CONTAINS &mdash; ${a.counts.findings} FINDINGS, ${a.counts.corrections_made_to_his_file} CORRECTIONS</h2>`+
    '<div class=card><table><tr><th>#</th><th>where</th><th>finding</th>'+
    '<th>consequence</th></tr>'+
    a.findings.map(f=>`<tr><td class=pid>${esc(f.id)}</td>`+
      `<td class=mine>${esc(f.where)}</td><td>${esc(f.finding)}</td>`+
      `<td class=law>${esc(f.consequence)}</td></tr>`).join('')+
    `</table><div class=mine>${esc(a.rule)}</div></div>`);
  document.getElementById('led').innerHTML=o.join('');
}

function draw(d){
  const o=[], g=d.generation, c=g.counts, cap=d.capacity;

  o.push('<div class=card><div class=k>IDENTITY LOCK</div>'+
    `<div class=lock>${esc(g.identity.identity)}</div>`+
    `<div class=mine>${esc(g.identity.rule)}</div>`+
    `<div class=mine>NOT: ${esc(g.identity.not)}</div></div>`);

  const p=g.pack;
  o.push(`<h2>BRAIN-STATE ${esc(p.id)} &middot; ${esc(p.name)} &middot; MODEL ${esc(p.model)}</h2>`+
    '<div class=card><div class=k>CONDITIONS THAT RAISE IT</div><div>'+
    p.conditions.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>'+
    `<div class=mine style=margin-top:6px>evidence band ${esc(p.evidence)} &middot; ${esc(p.by)}</div>`+
    (p.pairs_with?`<div class=mine>pairs with ${esc(p.pairs_with)} — ${esc(p.pair_note||'')}</div>`:'')+
    (p.law?`<div class=law>${esc(p.law)}</div>`:'')+
    (p.holds?`<div class=mine>HELD: ${esc(p.holds)}</div>`:'')+
    (p.refuses?`<div class=mine>REFUSES: ${esc(p.refuses)}</div>`:'')+
    (p.chain?'<div class=k style=margin-top:8px>INNER MACHINE</div><pre>'+
       p.chain.map(esc).join('\n  |\n  v\n')+'</pre>':'')+
    (p.forks?'<div class=k style=margin-top:8px>THIS STATE ITSELF FORKS</div><ul>'+
       p.forks.map(x=>`<li>${esc(x)}</li>`).join('')+'</ul>':'')+
    (p.duties?'<div class=k style=margin-top:8px>ALL ACTIVE TOGETHER</div><div>'+
       p.duties.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>':'')+
    (p.must_distinguish?'<div class=k style=margin-top:8px>MUST DISTINGUISH</div><div>'+
       p.must_distinguish.map(x=>`<span class=pill>${esc(x)}</span>`).join(' vs ')+'</div>':'')+
    (p.same_circumstance_different_pyramid?
       '<div class=k style=margin-top:8px>SAME CIRCUMSTANCE, DIFFERENT PYRAMID</div><ul>'+
       p.same_circumstance_different_pyramid.map(x=>`<li>"${esc(x)}"</li>`).join('')+'</ul>':'')+
    '</div>');

  o.push('<h2>WHAT THE GENERATION MADE</h2><div class=card><div class=count>'+
    `<div><div class=k>CONTAINERS</div><b>${c.containers}</b></div>`+
    `<div><div class=k>STATES USED</div><b>${c.states_used}</b></div>`+
    `<div><div class=k>RUNTIME ADDRESSES</div><b>${c.addresses}</b></div>`+
    `<div><div class=k>NATIVE PARAMS ADDED</div><b class=zero>${c.native_parameters_added}</b></div>`+
    `<div><div class=k>NATIVE PARAMS MODIFIED</div><b class=zero>${c.native_parameters_modified}</b></div>`+
    '</div></div>');

  o.push('<div class=card><table><tr><th>runtime address</th><th>container</th>'+
    '<th>his name for it</th><th>state</th><th>native span</th><th>in bank?</th></tr>'+
    g.addresses.map(a=>`<tr><td class=pid>${esc(a.address)}</td>`+
      `<td class=mine>${esc(a.container)}</td><td>${esc(a.container_name)}</td>`+
      `<td><span class="st ${esc(a.state)}">${esc(a.state)}</span></td>`+
      `<td class=mine>P${a.native_span[0]}-P${a.native_span[1]}</td>`+
      `<td class=zero>NO</td></tr>`).join('')+'</table>'+
    `<div class=law>${esc(g.addresses.length?g.addresses[0].law:'')}</div></div>`);

  if(g.filters.length){
    o.push('<h2>FILTERS, AND THE ARGUMENT AXIS</h2><div class=card><div>'+
      g.filters.map(f=>`<span class=pill>${esc(f)}</span>`).join('')+'</div>'+
      (Object.keys(g.filter_arguments).length?
        '<div class=k style=margin-top:8px>PARAMETERISED — not in the 40-filter list</div>'+
        Object.keys(g.filter_arguments).map(k=>
          `<div class=mine>${esc(k)} -> ${g.filter_arguments[k].map(esc).join(' &middot; ')}</div>`).join(''):'')+
      '</div>');
  }

  const li=d.live_intent;
  if(li){
    const lc=li.counts;
    o.push('<h2>LIVE INTENT — GENERATED FROM THE ACTIVE PARAMETERS</h2>'+
      '<div class=card><div class=count>'+
      `<div><div class=k>ACTIVE CONTAINERS</div><b>${lc.active_containers}</b></div>`+
      `<div><div class=k>MOTIVES RAISED</div><b>${lc.motives_raised}</b> <span class=mine>of ${lc.motive_rows}</span></div>`+
      `<div><div class=k>FORMS APPLICABLE</div><b>${lc.forms_applicable}</b> <span class=mine>of ${lc.form_rows}</span></div>`+
      `<div><div class=k>INTENT CANDIDATES</div><b>${lc.intents_generated}</b></div>`+
      `<div><div class=k>ADDED TO BANK</div><b class=zero>${lc.native_parameters_added}</b></div>`+
      '</div>'+
      `<div class=law style=margin-top:6px>${esc(li.law)}</div>`+
      `<div class=mine>${esc(li.refuses)}</div>`+
      `<div class=mine>${esc(li.confidence.row)} = ${esc(li.confidence.level)} — ${esc(li.confidence.why)}</div>`+
      `<div class=mine>reachable but not active: ${lc.motives_reachable_not_active}</div></div>`);
    const seen={}, uniq=[];
    li.candidates.forEach(x=>{ if(!seen[x.why]){seen[x.why]=1; uniq.push(x);} });
    o.push('<div class=card><table><tr><th>the WHY (his motive row)</th>'+
      '<th>raised by</th><th>state</th><th>matched row</th><th>the SHAPE</th>'+
      '<th>status</th></tr>'+
      uniq.map(x=>`<tr><td>${esc(x.why)} <span class=mine>${esc(x.why_p)}</span></td>`+
        `<td class=pid>${esc(x.raised_by.container)}</td>`+
        `<td><span class="st ${esc(x.raised_by.state)}">${esc(x.raised_by.state)}</span></td>`+
        `<td class=mine>${esc(x.raised_by.matched_row)} ${esc(x.raised_by.matched_p)}</td>`+
        `<td class=mine>${esc(x.shape)} ${esc(x.shape_p)}</td>`+
        `<td class=zero>${esc(x.status)}</td></tr>`).join('')+
      `</table><div class=mine>one row per distinct motive; each is crossed with `+
      `${lc.forms_applicable} intent forms. chosen = ${esc(String(li.chosen))}</div></div>`);
  }

  if(d.fork){
    const f=d.fork;
    o.push(`<h2>EVENT FORK — ${esc(f.event)}</h2><div class=card>`);
    if(!f.known){ o.push(`<div class=mine>${esc(f.note)}</div>`); }
    else{
      o.push(`<div class=k>${f.count} INTENT ROUTES, NONE CHOSEN</div><ul>`+
        f.routes.map(x=>`<li>${esc(x)}</li>`).join('')+'</ul>');
      if(f.still_open.length) o.push('<div class=k style=margin-top:8px>STILL OPEN</div><div>'+
        f.still_open.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>');
      if(f.asks.length) o.push('<div class=k style=margin-top:8px>ASKS INSTEAD</div><div>'+
        f.asks.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>');
      if(f.retains.length) o.push('<div class=k style=margin-top:8px>MAY STILL RETAIN</div><div>'+
        f.retains.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>');
      o.push(`<div class=law>${esc(f.refuses)}</div>`);
      o.push(`<div class=law>${esc(f.law)}</div>`);
    }
    o.push('</div>');
  }
  if(d.formal_vs_functional){
    const fv=d.formal_vs_functional;
    o.push('<h2>FORMAL STATE vs FUNCTIONAL STATE</h2><div class=card>'+
      `<div>${esc(fv.formal_state)}</div>`+
      `<div class=law>${esc(fv.functional_state)}</div>`+
      '<div class=k style=margin-top:8px>MAY RETAIN</div><div>'+
      fv.may_retain.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>'+
      '<div class=k style=margin-top:8px>WATCH IN OTHER DOMAINS</div><div>'+
      fv.cross_domain_to_watch.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div>'+
      `<div class=mine style=margin-top:6px>${esc(fv.his_gate)}</div></div>`);
  }

  o.push('<h2>CAPACITY — ADDRESSES, NOT PARAMETERS</h2><div class=card><table>'+
    [['native bank (his 3,204)',cap.native_bank],
     ['containers',cap.containers],
     ['states he has named',cap.states_named_by_him+' of '+cap.states_total],
     ['states still unnamed',cap.states_unnamed],
     ['his 25 rubrics',cap.rubrics],
     ['container x state',cap.container_x_state],
     ['container x rubric  (his 2,000)',cap.container_x_rubric],
     ['capacity he stated  2560 x 40 x 12',cap.his_stated_capacity.toLocaleString()],
     ['at current fill  3204 x 40 x 12',cap.at_current_fill.toLocaleString()],
     ['generated by his packs',cap.generated_by_his_packs]].map(
      ([k,v])=>`<tr><td>${esc(k)}</td><td class=pid>${esc(v)}</td></tr>`).join('')+
    `</table><div class=law>${esc(cap.law)}</div></div>`);

  o.push('<h2>HIS SEVEN FINDINGS AGAINST HIS OWN WORKBOOK</h2><div class=card><table>'+
    '<tr><th>#</th><th>finding</th><th>verified here</th></tr>'+
    d.workbook_findings.map(f=>`<tr><td class=pid>${f.n}</td>`+
      `<td>${esc(f.finding)}</td><td class=mine>${esc(f.verified)}</td></tr>`).join('')+
    '</table></div>');

  o.push('<h2>CANDIDATES — ALL REVIEW_REQUIRED</h2><div class=two>'+
    d.candidates.map(x=>`<div class=card><div class=pid>${esc(x.id)}</div>`+
      `<pre>${x.form.map(esc).join('\n')}</pre>`+
      `<div class=mine style=margin-top:6px>found in: ${esc(x.found_in)}</div>`+
      (x.his_note?`<div class=law>${esc(x.his_note)}</div>`:'')+
      `<div style=margin-top:6px><span class=pill>support ${x.support}</span>`+
      `<span class=pill>canonical ${x.canonical}</span>`+
      `<span class=pill style="border-color:#8b5cf6;color:#c084fc">${esc(x.status)}</span></div>`+
      '</div>').join('')+'</div>');

  o.push('<div class=card><div class=k>PROMOTED</div>'+
    Object.keys(d.promoted).map(k=>
      `<span class=pill>${esc(k)} = <b class=zero>${d.promoted[k]}</b></span>`).join('')+
    `<div class=mine style=margin-top:6px>${esc(d.gate)}</div></div>`);

  o.push('<h2>NOT GENERATED — PROSE ONLY</h2><div class=card>'+
    '<div class=mine>twelve of his eighteen kings carry a written meaning and '+
    'NO container-state assignment. Recorded as un-generated, not counted as brains.</div><div>'+
    d.prose_only.map(x=>`<span class=pill>${esc(x)}</span>`).join('')+'</div></div>');

  document.getElementById('out').innerHTML=o.join('');
}

async function go(){
  const body={who:document.getElementById('who').value,
              pack:document.getElementById('pack').value,
              event:document.getElementById('ev').value};
  document.getElementById('out').innerHTML='<div class=card>generating&hellip;</div>';
  try{
    const r=await fetch('/generation/run',{method:'POST',
      headers:{'content-type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok) throw new Error('HTTP '+r.status);
    draw(await r.json());
  }catch(e){
    document.getElementById('out').innerHTML=
      '<div class=card style=color:#f87171>'+esc(e.message)+'</div>';
  }
}
document.getElementById('run').addEventListener('click',go);
document.getElementById('pack').addEventListener('change',go);
document.getElementById('ev').addEventListener('change',go);
boot();
</script></body></html>"""
