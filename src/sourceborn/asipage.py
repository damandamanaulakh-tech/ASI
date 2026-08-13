"""THE PYRAMID page — his answer on screen, at /asi.

He wrote the structure and said "my reading u shit that is ASI / which u supposed
to build". So this page shows the machine's run, not a comparison against a
hand-note: the PRIOR/CURRENT split, the SAME EVENT SHELL, his two epistemic
tiers over SB-HFR-P0001..P3204, the behaviour-is-not-a-state block, the causal
gap with the branches open, and his pattern candidate with its four guards.

Every value interpolated into the page is escaped — an ask is untrusted input.
"""

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>THE PYRAMID — one ask over his 3,204</title>
<style>
:root{--bg:#07090c;--ink:#e8eef6;--dim:#8fa3b8;--line:#1b2430;--card:#0d1218;
--strong:#4ade80;--cand:#fbbf24;--halt:#f87171;--his:#60a5fa}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
header{padding:18px 20px 12px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:15px;letter-spacing:.14em}
.sub{color:var(--dim);font-size:12px;margin-top:6px}
main{padding:18px 20px 60px;max-width:1180px}
.ask{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
textarea{flex:1 1 520px;min-height:66px;background:var(--card);color:var(--ink);
border:1px solid var(--line);border-radius:6px;padding:10px;font:inherit}
button{background:#16202c;color:var(--ink);border:1px solid var(--line);
border-radius:6px;padding:9px 15px;cursor:pointer;font:inherit}
button:hover{border-color:#33506e}
button.go{background:#15304a;border-color:#22507a}
h2{font-size:12px;letter-spacing:.16em;color:var(--dim);margin:26px 0 8px;
border-bottom:1px solid var(--line);padding-bottom:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:12px 14px;margin-bottom:10px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:820px){.two{grid-template-columns:1fr}}
.k{color:var(--dim);font-size:11px;letter-spacing:.1em}
.clause{padding:3px 0}
.shell{font-size:19px;letter-spacing:.1em;color:var(--his);text-align:center;
padding:8px 0}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;color:var(--dim);font-weight:400;font-size:11px;
letter-spacing:.1em;padding:5px 8px;border-bottom:1px solid var(--line)}
td{padding:5px 8px;border-bottom:1px solid #121a24;vertical-align:top}
.pid{color:var(--his);white-space:nowrap}
.t-strong{color:var(--strong)}
.t-cand{color:var(--cand)}
.mine{color:var(--dim);font-size:11px}
.count{display:flex;gap:18px;flex-wrap:wrap;align-items:baseline}
.count b{font-size:24px;font-weight:600}
.halt{color:var(--halt)}
.pill{display:inline-block;border:1px solid var(--line);border-radius:99px;
padding:1px 9px;font-size:11px;color:var(--dim);margin:2px 3px 2px 0}
pre{margin:0;white-space:pre-wrap;font:inherit;color:var(--dim)}
.chart{overflow-x:auto}
.chart pre{white-space:pre;color:var(--ink);font-size:12px}
ul{margin:4px 0 0 18px;padding:0}li{margin:2px 0}
.note{color:var(--cand);font-size:11.5px;margin-top:4px}
</style></head><body>
<header>
  <h1>THE PYRAMID — ONE ASK OVER HIS 3,204</h1>
  <div class=sub>SB-HFR-P0001..SB-HFR-P3204 &middot; 1 - 10 - 8 - 40 &middot;
  historical pattern vs current exception &middot; the visible event stays the
  same, the active micro-Pyramid changes</div>
</header>
<main>
  <div class=ask>
    <textarea id=q placeholder="one ask">Samrath never like to go to school, he always cry, but today is his birthday, he went very happy.</textarea>
    <button class=go id=run>RUN</button>
  </div>
  <div id=out></div>
</main>
<script>
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,
  c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}

function rows(list){
  return list.map(r=>`<tr>
    <td class=pid>${esc(r.p)}</td>
    <td>${esc(r.name)}</td>
    <td class="${r.tier.indexOf('STRONG')===0?'t-strong':'t-cand'}">${
      r.tier.indexOf('STRONG')===0?'STRONG':'CANDIDATE'}</td>
    <td>${esc(r.why)}${r.his_note?`<div class=note>${esc(r.his_note)}</div>`:''}</td>
    <td class=pid>${esc(r.container)}</td>
    <td class=mine>${esc(r.by)}</td></tr>`).join('');
}

function draw(d){
  const o=[];
  const sc=d.scopes, sh=d.shell, c=d.activation.counts;

  o.push('<h2>THE SPLIT — NOT ONE FLAT SENTENCE</h2><div class=two>');
  [['PRIOR / REPEATED SEQUENCES','PRIOR / REPEATED'],
   ['CURRENT / TODAY SEQUENCE','CURRENT / TODAY']].forEach(([label,key])=>{
    const list=sc[key]||[];
    o.push(`<div class=card><div class=k>${esc(label)}</div>`+
      (list.length?list.map(r=>`<div class=clause>"${esc(r.clause)}"`+
        (r.prior_markers.concat(r.current_markers,r.contrast).map(m=>
          `<span class=pill>${esc(m)}</span>`).join(''))+
        (r.scope_inherited?'<span class=pill>scope inherited</span>':'')+
        '</div>').join(''):'<div class=mine>nothing in this scope</div>')+
      '</div>');
  });
  o.push('</div>');
  o.push(`<div class=card><div class=k>SAME EVENT SHELL</div>
    <div class=shell>${esc(sh.shell||'(no shell found)')}</div>
    <div class=mine>${sh.unchanged?'held ONCE with two routes — the event did not change':
      'only one route present — no contrast in this ask'}</div></div>`);

  o.push('<h2>THE TINY WORDS DO MOST OF THE WORK</h2><div class=card><table>'+
    '<tr><th>word</th><th>what it does</th><th>scope</th></tr>'+
    d.tiny_words.map(t=>`<tr><td class=pid>"${esc(t.word)}"</td><td>${
      t.does.map(esc).join(' &middot; ')}</td><td class=mine>${esc(t.scope)}${
      t.seeded_by_class?' (same class as his table)':''}</td></tr>`).join('')+
    '</table></div>');

  o.push('<h2>WORKING ACTIVE SET</h2><div class=card><div class=count>'+
    `<div><div class=k>CONFIRMED / STRONG</div><b class=t-strong>${c.strong}</b></div>`+
    `<div><div class=k>CANDIDATE / INFERRED</div><b class=t-cand>${c.candidate}</b></div>`+
    `<div><div class=k>WORKING / BANK</div><b>${c.working} / ${c.bank}</b></div>`+
    `<div><div class=k>OF THE BANK</div><b>${c.pct}%</b></div>`+
    `<div><div class=k>INACTIVE FOR THIS READING</div><b class=mine>${c.inactive}</b></div>`+
    '</div></div>');
  o.push('<div class=card><table><tr><th>id</th><th>his name for it</th>'+
    '<th>tier</th><th>why</th><th>container</th><th>assigned by</th></tr>'+
    rows(d.activation.strong)+rows(d.activation.candidate)+'</table></div>');

  if(d.behaviour_not_state.readings.length){
    o.push('<h2>BEHAVIOUR IS A SIGNAL, NOT A STATE</h2>');
    d.behaviour_not_state.readings.forEach(b=>{
      o.push(`<div class=card><div class=k>${esc(b.behaviour.toUpperCase())}</div>
        <div>${esc(b.behaviour)} = ${esc(b.is)} &nbsp;&nbsp; <span class=halt>&ne; ${
        esc(b.is_not)}</span></div>
        <div>${b.possible.map(p=>`<span class=pill>${esc(p)}</span>`).join('')}</div>
        <div class=halt>= ${esc(b.status)}</div>
        <div class=mine>${esc(d.behaviour_not_state.his_rule)}</div></div>`);
    });
  }

  const df=d.difference;
  o.push('<h2>THE DIFFERENCE, AND THE CAUSAL GAP</h2><div class=card>');
  if(df.same.length) o.push('<div>'+df.same.map(s=>
    `<span class=pill>${esc(s)}</span>`).join('+ ')+
    (df.different?` + <span class=pill style="border-color:#22507a;color:#60a5fa">${
      esc(df.different)}</span>`:'')+'</div>');
  if(df.equals) o.push(`<div class=shell style=font-size:14px>= ${esc(df.equals)}</div>`);
  o.push('<div class=two>');
  o.push('<div><div class=k>WE KNOW</div><ul>'+df.we_know.map(x=>
    `<li>${esc(x)}</li>`).join('')+'</ul></div>');
  o.push('<div><div class=k>WE DO NOT KNOW</div><ul>'+df.we_do_not_know.map(x=>
    `<li class=halt>${esc(x)}</li>`).join('')+'</ul></div>');
  o.push('</div>');
  o.push(`<div class=halt style=margin-top:8px>${esc(df.status)}</div>`+
    `<div class=mine>${esc(df.strength)}</div>`);
  if(df.hidden_branches.length)
    o.push('<div class=k style=margin-top:8px>OPENED AS HYPOTHESES, NOT INVENTED</div><div>'+
      df.hidden_branches.map(b=>`<span class=pill>${esc(b)}</span>`).join('')+'</div>');
  o.push(`<div class=mine style=margin-top:8px>${esc(df.fabrication_example)}</div></div>`);

  if(d.intent.candidates.length){
    o.push('<h2>INTENT — TWO ROUTES, NEVER BLENDED</h2><div class=two>');
    d.intent.candidates.forEach(cd=>o.push(`<div class=card>
      <div class=k>${esc(cd.id)} &middot; ${esc(cd.scope)}</div>
      <pre>${cd.route.map(esc).join('\n  |\n  v\n')}</pre>
      <div style=margin-top:6px>${esc(cd.reads)}</div></div>`));
    o.push('</div>');
  }

  const pc=d.pattern_candidate;
  o.push('<h2>PATTERN CANDIDATE</h2><div class=card>'+
    `<div class=k>${esc(pc.id)} &middot; ${pc.assembled?'ASSEMBLED':'NOT ASSEMBLED'}</div>`+
    `<pre>${pc.form.map(esc).join('\n+\n')}\n=\n${esc(pc.equals)}</pre>`);
  if(pc.missing && pc.missing.length)
    o.push('<div class=note>absent from his form: '+pc.missing.map(esc).join(' &middot; ')+
      (pc.unnamed_shape?' — this is a real shape he has not named yet':'')+'</div>');
  o.push('<div class=k style=margin-top:8px>GUARDS</div><div>'+
    Object.keys(pc.guards).map(k=>`<span class=pill>${esc(k)} = ${
      esc(pc.guards[k])}</span>`).join('')+'</div>');
  o.push('<div class=k style=margin-top:8px>REFUSED</div><ul>'+pc.refused.map(r=>
    `<li class=halt>"${esc(r.claim)}" — ${esc(r.why)}</li>`).join('')+'</ul>');
  o.push('<div class=k style=margin-top:8px>THEN</div><div>'+pc.next.map(n=>
    `<span class=pill>${esc(n)}</span>`).join('')+'</div></div>');

  o.push('<h2>THE RULE</h2><div class=card>'+
    `<div>${esc(d.rule.plain)}</div>`+
    `<pre style=margin-top:8px>${d.rule.machine.map(esc).join('\n')}\n\nCURRENT INTENT\n=\n${
      d.rule.sum.map(esc).join('\n+\n')}</pre>`+
    `<div class=note>${esc(d.rule.his_words)}</div></div>`);

  o.push('<h2>SEQUENCE RUNTIME — NOT PARAMETERS</h2><div class=card><table>'+
    d.runtime.objects.map(x=>`<tr><td class=pid>${x.n}</td><td>${esc(x.what)}</td>`+
      `<td class=mine>${esc(x.detail)}</td></tr>`).join('')+'</table>'+
    '<div style=margin-top:8px>'+d.runtime.then.map(t=>
      `<span class=pill>${esc(t)}</span>`).join(' &rarr; ')+'</div>'+
    `<div class=mine>${esc(d.runtime.his_rule)}</div></div>`);

  o.push('<h2>HIS ARROW CHART, GENERATED FROM THIS RUN</h2>'+
    `<div class="card chart"><pre>${esc(d.chart)}</pre></div>`);

  document.getElementById('out').innerHTML=o.join('');
}

async function go(){
  const q=document.getElementById('q').value;
  document.getElementById('out').innerHTML='<div class=card>reading&hellip;</div>';
  try{
    const r=await fetch('/asi/run',{method:'POST',
      headers:{'content-type':'application/json'},body:JSON.stringify({ask:q})});
    if(!r.ok) throw new Error('HTTP '+r.status);
    draw(await r.json());
  }catch(e){
    document.getElementById('out').innerHTML=
      '<div class=card><span class=halt>'+esc(e.message)+'</span></div>';
  }
}
document.getElementById('run').addEventListener('click',go);
go();
</script></body></html>"""
