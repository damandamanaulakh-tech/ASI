"""THE READING — the microscope. His interpretation view, made real.

His spec, verbatim in substance:

    You want the tool to expose its internal structured reading:
      QUESTION SEQUENCE · detected entities · relevant prior Sequences ·
      repeated candidates · Human parameters activated ·
      possible emotional states [ ] … [+] OTHER ·
      possible interpretation · confidence · intent UNKNOWN / INFERRED ·
      Your interpretation [ editable ] · Your emotional meaning [ editable ] ·
      Your rule/boundary [ editable ] ·
      Save as [ occurrence only ] [ personal pattern ]
              [ candidate Human rubric ] [ relationship-specific rule ]
              [ general pattern ]

    RUBRIC VIEW — SHOW activated: P IDs · CON IDs · SEG IDs · relations ·
    patterns · emotions · intent · uncertainty · evidence
        ↓ YOU EDIT / CORRECT ↓ WRITE-BACK new Sequence ↓ PATTERN MEMORY
        ↓ repeated cases ↓ PATTERN CANDIDATE ↓ R-F-R / Doubt ↓ YOU APPROVE

    "You are not merely trying to make the ASI learn from you. You want to see
     what rubric combination produced its understanding and directly correct
     that representation."

    The first requirement is TRACEABLE UNDERSTANDING. Speed is not.

So this page is not a chat with a reasoning panel bolted on. The reading IS the
page, the answer sits inside it, and every field the machine produced can be
walked back to the sentence it came from.
"""
from __future__ import annotations

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>THE READING — Sourceborn</title><style>
:root{--bg:#070809;--panel:#0f1219;--elev:#141826;--line:#1c2230;--line2:#262d3d;
--ink:#eef2f8;--mut:#7d8699;--acc:#7c8bff;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;
--grad:linear-gradient(135deg,#7c8bff,#a78bfa 60%,#f0abfc)}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);font:15px/1.55 'Inter',-apple-system,Segoe UI,Roboto,sans-serif;
background:radial-gradient(900px 520px at 85% -8%,rgba(124,139,255,.14),transparent 60%),var(--bg)}
.app{max-width:1240px;margin:0 auto;padding:0 18px 100px}
.top{position:sticky;top:0;z-index:9;display:flex;justify-content:space-between;align-items:center;
gap:10px;padding:14px 2px;background:linear-gradient(180deg,rgba(7,8,9,.93),rgba(7,8,9,.5));
backdrop-filter:blur(12px);border-bottom:1px solid var(--line);flex-wrap:wrap}
.name{font-weight:700;font-size:18px}.name small{color:var(--mut);font-weight:400;margin-left:8px}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
button,select,input,textarea{font:inherit;color:var(--ink);background:var(--panel);
border:1px solid var(--line2);border-radius:9px;padding:8px 12px}
button{cursor:pointer}button:hover{border-color:var(--acc)}
button.pri{background:var(--grad);border:0;color:#0a0a14;font-weight:700}
button.mini{padding:3px 9px;font-size:12px;border-radius:7px}
textarea{width:100%;min-height:64px;resize:vertical}
.ask{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px;margin:16px 0}
.ask textarea{min-height:76px;border:0;background:transparent;padding:4px}
.bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px}
.sec{margin:26px 0 10px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;
border-bottom:1px solid var(--line);padding-bottom:8px}
.sec h2{margin:0;font-size:12.5px;letter-spacing:.15em;color:var(--mut);text-transform:uppercase}
.sec .n{font-size:12px;color:var(--mut);font-variant-numeric:tabular-nums}
.blk{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:13px 15px;margin:9px 0}
.blk h3{margin:0 0 8px;font-size:14.5px}
.kv{display:grid;grid-template-columns:190px 1fr;gap:4px 12px;font-size:13.5px}
.kv .k{color:var(--mut)}
.kv .v{white-space:pre-wrap}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0}
.chip{font-size:11.5px;border:1px solid var(--line2);border-radius:999px;padding:3px 9px;color:var(--mut)}
.chip.on{color:var(--ink);border-color:var(--acc)}
.chip.f{font-family:ui-monospace,Menlo,monospace;font-size:11px}
.ms{border-left:2px solid var(--line2);padding-left:12px;margin:10px 0}
.ms .raw{font-size:14.5px;margin-bottom:6px}
.ms .raw:before{content:'\201C'}.ms .raw:after{content:'\201D'}
.flow{display:flex;flex-wrap:wrap;gap:5px}
.fp{font-size:11px;border:1px solid var(--line2);border-radius:7px;padding:3px 7px;color:var(--mut)}
.fp.on{color:#9ff0d0;border-color:rgba(52,211,153,.45)}
.fp small{color:var(--mut);opacity:.7;margin-left:4px}
.cand{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--warn);
border-radius:13px;padding:14px 16px;margin:10px 0}
.cand.appr{border-left-color:var(--ok)}
.pat{white-space:pre-wrap;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;
background:var(--elev);border-radius:9px;padding:10px 12px;margin:8px 0;overflow-x:auto}
.six{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin-top:10px}
.six label{display:block;font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;
color:var(--mut);margin-bottom:4px}
.six .mine{border-left:2px solid var(--acc);padding-left:8px}
.note{color:var(--mut);font-size:13px}
.warnbox{border-left:3px solid var(--warn);padding-left:10px;color:#ffe2a3;font-size:13px;margin:8px 0}
.badge{font-size:11px;border:1px solid var(--line2);border-radius:999px;padding:2px 9px;color:var(--mut)}
.badge.ok{color:#9ff0d0;border-color:rgba(52,211,153,.45)}
.badge.warn{color:#ffe2a3;border-color:rgba(251,191,36,.45)}
.badge.bad{color:#ffc4c4;border-color:rgba(248,113,113,.5)}
details{margin:6px 0}summary{cursor:pointer;color:var(--mut);font-size:13px}
.ans{background:var(--elev);border:1px solid var(--line2);border-radius:13px;padding:14px 16px;margin:10px 0}
</style></head><body><div class=app>
<div class=top>
 <div class=name>THE READING<small>every sentence split, matched, routed &mdash; and yours to correct</small></div>
 <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
  <span class=badge id=stats>&hellip;</span>
  <a href="/engine">&#9881; ENGINE</a><a href="/exists">&#9672; WHAT EXISTS</a>
  <a href="/page">&#9638; MY PAGE</a><a href="/" style="color:var(--mut)">&larr; app</a>
 </div>
</div>

<div class=ask>
 <textarea id=q placeholder="Say it however it comes &mdash; vague is where this starts. e.g. Why do I feel uncomfortable with this person?"></textarea>
 <div class=bar>
  <button class=pri onclick=ask()>READ IT</button>
  <select id=model><option value=offline>Offline (no key)</option>
   <option value=claude>Claude</option><option value=grok>Grok</option>
   <option value=openai>OpenAI</option><option value=openrouter>OpenRouter</option></select>
  <span class=note id=stat></span>
 </div>
 <div class=note style="margin-top:8px">Nothing here concludes intent from one event, and nothing picks your feeling.
 Every sentence becomes a micro-sequence; a <b>pattern</b> only surfaces after it repeats, and only you approve it.</div>
</div>

<div id=root></div>
<div class=sec><h2>Pattern memory &mdash; candidates awaiting you</h2><span class=n id=pn></span></div>
<div id=pats></div>
</div><script>
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let LAST=null;
function chips(a,cls){return '<div class=chips>'+(a||[]).map(x=>'<span class="chip '+(cls||'')+'">'+esc(x)+'</span>').join('')+'</div>';}
function kv(rows){return '<div class=kv>'+rows.map(([k,v])=>'<div class=k>'+esc(k)+'</div><div class=v>'+(v==null||v===''?'<span class=note>(empty &mdash; and it says why)</span>':esc(v))+'</div>').join('')+'</div>';}

function microBlock(m){
  const ent=(m.entities||[]).map(e=>e.surface+' ('+e.side+(e.kind==='inherited from context'?', inherited':'')+')');
  const st=m.information_state||{};
  return '<div class=ms><div class=raw>'+esc(m.raw)+'</div>'+
    '<div class=chips>'+(m.structural_facts||[]).map(f=>'<span class="chip f">'+esc(f)+'</span>').join('')+'</div>'+
    kv([['ENTITY',ent.join(' · ')],['RELATION',(m.relation||[]).join(' · ')],
        ['ACTION',(m.actions||[]).map(a=>a.verb+' ['+a.classes.join('/')+']').join(' · ')],
        ['NEGATION',(m.negation||[]).join(' · ')],
        ['INFORMATION OBJECT',m.information_object],
        ['INFORMATION STATE',Object.keys(st).length?Object.entries(st).map(([k,v])=>k+' = '+v).join('\n'):''],
        ['EXPECTED INFORMATION',m.expected_information],
        ['ACTUAL INFORMATION',m.actual_information],
        ['TEMPORAL RELATION',m.temporal_relation],
        ['DEPENDENCY',m.dependency],
        ['EXPECTATION DIFFERENCE',m.expectation_difference],
        ['POSSIBLE HUMAN EFFECT',(m.possible_human_effect||[]).join(', ')],
        ['INTENT',m.intent.status+' — '+m.intent.why],
        ['UNCERTAINTY',(m.uncertainty||[]).join(', ')],
        ['REPETITION LINK',m.repetition_link],
        ['PATTERN CONTRIBUTION',m.pattern_contribution],
        ['id',m.id]])+'</div>';
}

function candBlock(c,open){
  const cf=c.confidence||{}, rfr=c.rfr||{};
  const appr=c.status==='approved';
  return '<div class="cand'+(appr?' appr':'')+'" id="c_'+esc(c.id)+'">'+
   '<h3>'+esc(c.id)+' <span class="badge '+(appr?'ok':'warn')+'">'+esc(c.status)+'</span> '+
   (c.name?'<span class=badge>'+esc(c.name)+'</span>':'')+'</h3>'+
   '<div class=note>OBSERVED PATTERN &mdash; the arrangement, with what each step actually rests on:</div>'+
   '<div class=pat>'+esc(c.observed_pattern)+'</div>'+
   kv([['EVIDENCE',(c.evidence_asks||[]).join(', ')+'  ('+(c.evidence||[]).length+' micro-sequences)'],
       ['REPETITION COUNT',String(c.repetition_count)],
       ['SURFACED AT THRESHOLD',String(c.surfaced_at_threshold)],
       ['INTENT STATUS',c.intent_status],
       ['CONFIDENCE',cf.value+'  ('+esc(cf.basis||'')+')'+(cf.cap?'  capped at '+cf.cap+' — '+esc(cf.cap_reason||''):'')],
       ['FORMULA',cf.formula]])+
   '<div class=note style="margin-top:8px">POSSIBLE INTERPRETATIONS &mdash; every reading the structure allows. <b>None is chosen.</b></div>'+
   chips(c.possible_interpretations)+
   '<div class=note>POSSIBLE HUMAN EFFECT &mdash; what this structure can produce in a person. <b>Not a claim about what you felt.</b></div>'+
   chips(c.possible_human_effect)+
   (rfr.r_f_r?'<details><summary>R-F-R / Doubt &mdash; the triple pass this candidate already went through '+
     (rfr.stands?'<span class="badge ok">stands</span>':'<span class="badge bad">does not stand yet</span>')+'</summary>'+
     rfr.r_f_r.map(p=>'<div class=warnbox><b>'+esc(p.pass)+'</b><br>'+esc(p.asks)+'<br>&rarr; '+esc(p.verdict)+'</div>').join('')+
     '<div class=note>doubt bites: '+(rfr.doubt&&rfr.doubt.bites?'yes':'no')+
     ((rfr.doubt&&rfr.doubt.fragilities||[]).length?' &mdash; '+esc(rfr.doubt.fragilities.join('; ')):'')+'</div>'+
     '<div class=note>'+esc(rfr.note||'')+'</div></details>':'')+
   '<div class=six>'+
    '<div><label>WHAT HAPPENED &mdash; machine</label><div class=note style="font-size:12px">held above, never merged with yours</div></div>'+
    six(c,'his_interpretation','WHAT I THINK IT MEANS')+
    six(c,'his_feeling','HOW I FELT')+
    six(c,'his_principle','WHAT PRINCIPLE I APPLY')+
    six(c,'his_decision','WHAT DECISION I MADE')+
    six(c,'his_result','WHAT RESULT FOLLOWED')+
   '</div>'+
   '<div class=bar style="margin-top:10px">'+
    '<input id="nm_'+esc(c.id)+'" placeholder="name this pattern" value="'+esc(c.name||'')+'" style="min-width:230px">'+
    '<select id="sv_'+esc(c.id)+'"><option value="">save as&hellip;</option>'+
    ['occurrence only','personal pattern','candidate Human rubric','relationship-specific rule','general pattern']
      .map(s=>'<option'+(c.save_as===s?' selected':'')+'>'+s+'</option>').join('')+'</select>'+
   '</div>'+
   '<div class=bar>'+
    ['approve','reject','rename','redefine'].map(a=>'<button class=mini onclick="act(\''+esc(c.id)+'\',\''+a+'\')">'+a+'</button>').join('')+
    '<button class=mini onclick="doSplit(\''+esc(c.id)+'\')">split</button>'+
    '<button class=mini onclick="doCombine(\''+esc(c.id)+'\')">combine</button>'+
    '<span class=note id="st_'+esc(c.id)+'"></span>'+
   '</div>'+
   (c.version>1?'<details><summary>NO REOPEN &mdash; '+(c.history||[]).length+' earlier version(s), kept whole</summary>'+
     (c.history||[]).map(h=>'<div class=note>v'+h.version+' &middot; '+esc(h.at)+' &middot; closed by <b>'+esc(h.action_that_closed_it)+
       '</b> &middot; status was '+esc(h.snapshot.status)+', your reading was '+
       (h.snapshot.his_interpretation?'&ldquo;'+esc(h.snapshot.his_interpretation)+'&rdquo;':'(none yet)')+'</div>').join('')+
     '</details>':'')+
   '</div>';
}
function six(c,f,label){
  return '<div class=mine><label>'+label+' &mdash; yours</label>'+
   '<textarea id="'+f+'_'+esc(c.id)+'" placeholder="only you write here">'+esc(c[f]||'')+'</textarea></div>';
}

async function act(id,action,extra){
  const g=f=>{const e=document.getElementById(f+'_'+id);return e?e.value:'';};
  const st=document.getElementById('st_'+id); if(st)st.textContent=action+'…';
  const fields={his_interpretation:g('his_interpretation'),his_feeling:g('his_feeling'),
    his_principle:g('his_principle'),his_decision:g('his_decision'),his_result:g('his_result'),
    name:(document.getElementById('nm_'+id)||{}).value||'',
    save_as:(document.getElementById('sv_'+id)||{}).value||''};
  Object.assign(fields,extra||{});
  try{
    const d=await (await fetch('/patterns/review',{method:'POST',headers:{'content-type':'application/json'},
      body:JSON.stringify({id,action,fields})})).json();
    if(d.error){if(st)st.textContent=d.error;return;}
    if(st)st.textContent='done — v'+d.candidate.version+' (write-back recorded, nothing overwritten)';
    loadPats();
  }catch(e){if(st)st.textContent='error'}
}
function doSplit(id){
  const s=prompt('split into which names? separate with a comma — the parent is kept, the children reference it');
  if(!s)return; act(id,'split',{into:s.split(',').map(x=>x.trim()).filter(Boolean)});
}
function doCombine(id){
  const s=prompt('combine with which candidate id(s)? comma separated — the absorbed ones are CLOSED, never deleted');
  if(!s)return; act(id,'combine',{with:s.split(',').map(x=>x.trim()).filter(Boolean)});
}

function flowBlock(fv){
  return '<div class=flow>'+(fv||[]).map(r=>'<span class="fp'+(r.reached?' on':'')+'">'+esc(r.position)+
    (r.segments.length?'<small>'+esc(r.segments.join(' '))+'</small>':'')+'</span>').join('')+'</div>';
}

function render(d){
  LAST=d; let h='';
  const w=d.walk||{}, out=(w.result&&w.result.output)||{};
  h+='<div class=sec><h2>Question sequence</h2><span class=n>'+esc(d.ask)+'</span></div>';
  h+='<div class=blk>'+kv([['your words',d.raw],['micro-sequences built',String((d.micro_sequences||[]).length)],
    ['kept to memory',String(d.stored)],['threshold now',String((d.threshold||{}).surface_at)+
      '  ('+esc((d.threshold||{}).reduction_rule||'')+')']])+'</div>';

  h+='<div class=sec><h2>The flow &mdash; where this run actually went</h2><span class=n>lit = reached, with the Human segments working there</span></div>';
  h+='<div class=blk>'+flowBlock(d.flow)+'</div>';

  h+='<div class=sec><h2>Ultra-micro decomposition</h2><span class=n>'+(d.micro_sequences||[]).length+' sentence(s), each its own micro-sequence</span></div>';
  h+='<div class=blk>'+(d.micro_sequences||[]).map(microBlock).join('')+'</div>';

  if((d.senses_fired||[]).length){
    h+='<div class=sec><h2>Your corrections to the parse</h2><span class=n>'+
      d.senses_fired.length+' fired &mdash; both readings kept, your sentence untouched</span></div>';
    const seen={};
    h+='<div class=blk>'+d.senses_fired.filter(o=>!seen[o.id]&&(seen[o.id]=1)).map(o=>
      '<div class=ms><div class=raw>'+esc(o.word)+'</div>'+
      kv([['SOURCE WORD',o.word],
          ['DEFAULT LANGUAGE INTERPRETATION',o.default_reading],
          ['YOUR CORRECTION',o.his_reading],
          ['STATUS',o.status],
          ['YOUR WORDS',o.his_words],
          ['REFUSES',o.refuses],
          ['blocked from the parse',(o.blocks_classes||[]).join(', ')],
          ['facts it adds',(o.adds_facts||[]).join(', ')],
          [o.id,'version '+o.version]])+'</div>').join('')+
      '<div class=note>A first linguistic parse is a guess. These are the places you told it otherwise &mdash; and the machine\'s own reading is kept beside yours, never replaced silently.</div></div>';
  }
  const rr=(d.micro_sequences||[]).map(m=>m.return_reading).filter(x=>x&&x.dimensions)[0];
  if(rr){
    h+='<div class=sec><h2>Return, per dimension</h2><span class=n>&ldquo;nothing&rdquo; is never read literally without its dimension</span></div>';
    h+='<div class=blk>'+kv(Object.entries(rr.dimensions).map(([k,v])=>[k,v]))+
      '<div class=note style="margin-top:6px">'+esc(rr.rule)+'</div></div>';
  }
  const mr=(d.micro_sequences||[]).map(m=>m.memory_reading).filter(x=>x&&x.valence)[0];
  if(mr){
    h+='<div class=sec><h2>Memory &mdash; valence and significance, two fields</h2></div>';
    h+='<div class=blk>'+kv([['VALENCE',mr.valence],['SIGNIFICANCE',mr.significance],
      ['YOUR RULE',mr.his_rule],['NEVER',mr.never]])+'</div>';
  }
  h+='<div class=sec><h2>Matched to existing IDs</h2><span class=n>the rubrics this ask touched</span></div>';
  const lit=d.rubrics_lit||{};
  // HIS CORRECTION: "attached details of each 3000 point, add it there instead
  // of just ID numbers." Every row now carries his own name for the thing, the
  // container it lives in, his note on that container, and what modulates it.
  // HIS RULING: Human = the physical human. Each word goes to ITS OWN brain.
  const WR=d.word_routes||{};
  h+='<div class=sec><h2>Which brain each word goes to</h2><span class=n>Human = the physical human, not the brain</span></div>';
  h+='<div class=blk>'+
    Object.entries(WR.classes||{}).map(([cls,words])=>
      '<div class=lane><b>'+esc(cls)+'</b> &nbsp;'+ (words||[]).map(w=>'<span class=chip>'+esc(w)+'</span>').join(' ')+'</div>').join('')+
    ((WR.excluded||[]).length?('<div class=warnbox style="margin-top:8px">'+
      WR.excluded.map(e=>'&ldquo;'+esc(e.text)+'&rdquo; &rarr; <b>'+esc(e.excludes)+
      '</b> is <b>OUT of scope</b> for this ask &mdash; '+esc(e.why)).join('<br>')+'</div>'):'')+
    ((WR.his_targets||[]).length?('<div class=note style="margin-top:8px">CONTAINERS YOU NAMED YOURSELF (not lexical hits):</div>'+
      WR.his_targets.filter(t=>t.container).map(t=>'<div class=lane><b>'+esc(t.container)+
      '</b> from &ldquo;'+esc(t.trigger)+'&rdquo; <span class=note>&mdash; '+esc(t.why)+'</span></div>').join('')):'')+
    '<div class=note style="margin-top:8px">'+esc(WR.rule||'')+'</div></div>';
  const BD=lit.by_domain||{};
  if(Object.keys(BD).length){
    h+='<div class=sec><h2>Container hits, split by brain</h2><span class=n>your source records untouched &mdash; this is an overlay</span></div>';
    h+='<div class=blk>'+Object.entries(BD).map(([dom,cs])=>
      '<div class=ms><div class=raw>'+esc(dom)+'</div>'+
      cs.map(c=>'<div class=lane><b>'+esc(c.id)+'</b> '+esc(c.name)+
        (c.his_assignment?' <span class="badge ok">you named it</span>':'')+
        (c.mixed?' <span class="badge warn">MIXED</span>':'')+
        '<div class=note>'+esc(c.reason||'')+'</div>'+
        (c.mixed?'<div class=warnbox>'+esc(c.mixed)+'</div>':'')+'</div>').join('')+
      '</div>').join('')+'</div>';
  }
  if((lit.out_of_scope||[]).length){
    h+='<div class=blk><div class=note>MOVED OUT OF SCOPE &mdash; kept with the reason, never deleted, so you can see the machine\'s first reading beside the corrected one:</div>'+
      lit.out_of_scope.map(c=>'<div class=lane><b>'+esc(c.id)+'</b> '+esc(c.name)+
        ' <span class=note>['+esc(c.domain)+'] &mdash; '+esc(c.why_out||'')+'</span></div>').join('')+'</div>';
  }
  const R=d.registry||{};
  h+='<div class=blk>'+
    '<div class=note style="margin-bottom:8px">Matched against <b>'+esc(String(R.parameters||0))+
    '</b> named sub-parameters in <b>'+esc(String(R.containers||0))+'</b> containers across <b>'+
    esc(String(R.segments||0))+'</b> segments &mdash; frame <b>'+esc(R.frame||'1 - 10 - 8 - 40')+
    '</b>. Every name below is yours, from '+esc(String(R.source||''))+'.</div>'+
    '<div class=note>SEGMENTS</div>'+
    ((lit.segments||[]).map(s=>'<div class=lane><b>'+esc(s.id)+'</b> '+esc(s.name)+
      ' <span class=note>'+(s.fired_containers||0)+' of its '+s.containers+' containers fired</span></div>').join('')
      ||'<div class=note>none</div>')+
    '<div class=note style="margin-top:8px">CONTAINERS</div>'+
    ((lit.containers||[]).map(c=>'<div class=ms><div class=raw>'+esc(c.id)+' &middot; '+esc(c.name)+'</div>'+
      kv([['segment',c.segment+' '+(c.segment_name||'')],
          ['your note on it',c.note],
          ['what modulates it',c.modulators],
          ['named sub-parameters',String(c.count)],
          ['why it fired',c.reason]])+'</div>').join('')||'<div class=note>none</div>')+
    '<div class=note style="margin-top:8px">SUB-PARAMETERS &mdash; your names, not ID numbers</div>'+
    ((lit.parameters||[]).map(p=>'<div class=lane><b>'+esc(p.id)+'</b> '+esc(p.name)+
      ' <span class=note>&mdash; '+esc(p.container_name)+' &middot; '+esc(p.segment_name)+
      ' &middot; matched: '+esc((p.matched||[]).join(', '))+'</span></div>').join('')
      ||'<div class=note>none</div>')+
    ((lit.dropped||0)?'<div class=note style="margin-top:6px">'+lit.dropped+
      ' further hit(s) not shown &mdash; capped so one container cannot flood the view. '+
      'The number is stated, never hidden.</div>':'')+
    '</div>';

  h+='<div class=sec><h2>Engine selection &mdash; from the structure, not the other way round</h2><span class=n>'+((d.route||{}).mechanisms||[]).length+' mechanism(s)</span></div>';
  h+='<div class=blk>'+((d.route||{}).mechanisms||[]).map(m=>
    '<div class=ms><div class=raw>'+esc(m.name)+'</div>'+
    (m.wired?'':'<div class=warnbox>NOT WIRED &mdash; '+esc(m.note||'')+'</div>')+
    '<div class=note>called because: '+m.why.map(esc).join(' · ')+'</div>'+
    '<div class=note style="font-family:ui-monospace;font-size:11.5px">'+esc(m.where)+'</div></div>').join('')+'</div>';

  if((d.relations_to_prior||[]).length){
    h+='<div class=sec><h2>Compared with prior sequences</h2><span class=n>'+d.relations_to_prior.length+' repeat(s) of an arrangement</span></div>';
    h+='<div class=blk>'+d.relations_to_prior.map(r=>'<div class=ms><div class=raw>'+esc(r.prior_sentence)+'</div>'+
      '<div class=note>'+esc(r.prior_ask)+' &middot; '+esc(r.why)+'</div>'+chips(r.core_shared,'f')+'</div>').join('')+'</div>';
  }
  if((d.pattern_hits||[]).length){
    h+='<div class=sec><h2>Your approved patterns bearing on this</h2></div><div class=blk>'+
      d.pattern_hits.map(p=>'<div class=ms><div class=raw>'+esc(p.name)+'</div>'+
      kv([['outcome',p.outcome],['why',p.why],['your reading',p.his_interpretation],
          ['your principle',p.his_principle],['missing from the pattern',(p.missing_from_pattern||[]).join(', ')]])+'</div>').join('')+'</div>';
  }
  if((d.contradictions||[]).length){
    h+='<div class=sec><h2>Where this goes AGAINST a pattern you approved</h2></div><div class=blk>'+
      d.contradictions.map(c=>'<div class=warnbox><b>'+esc(c.name)+'</b><br>'+esc(c.sentence)+'<br>'+esc(c.why)+'</div>').join('')+'</div>';
  }

  h+='<div class=sec><h2>Answer</h2><span class=n>last, as you asked</span></div>';
  h+='<div class=ans>'+esc(out.answer||'(no answer)')+
    '<div class=note style="margin-top:8px">confidence '+esc(String(out.confidence||''))+
    ' &middot; model '+esc((w.model||''))+'</div></div>';
  document.getElementById('root').innerHTML=h;
}

async function ask(){
  const q=document.getElementById('q').value.trim(); if(!q)return;
  const st=document.getElementById('stat'); st.textContent='splitting, matching, routing…';
  try{
    const d=await (await fetch('/reading/ask',{method:'POST',headers:{'content-type':'application/json'},
      body:JSON.stringify({question:q,model:document.getElementById('model').value})})).json();
    if(d.error){st.textContent=d.error;return;}
    st.textContent=''; render(d); loadPats();
  }catch(e){st.textContent='error: '+e}
}
async function loadPats(){
  try{const d=await (await fetch('/patterns')).json();
    const s=d.stats||{};
    document.getElementById('stats').textContent=
      s.micro_sequences+' micro · '+s.candidates_open+' open · '+s.approved+' approved · '+s.writebacks+' write-backs';
    document.getElementById('pn').textContent='surfaces at '+((s.threshold||{}).surface_at)+
      ' repeat(s) — '+((s.threshold||{}).status||'');
    const all=(d.candidates||[]);
    document.getElementById('pats').innerHTML=all.length
      ? all.map(c=>candBlock(c)).join('')
      : '<div class=blk><div class=note>Nothing has repeated enough yet. That is the point &mdash; a pattern from one occurrence is exactly what this refuses to invent.'+
        (((d.below||[]).length)?'<br><br>Below the threshold right now: '+d.below.map(b=>b.distinct_asks+' of '+b.needs).join(' · '):'')+'</div></div>';
  }catch(e){}
}
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.metaKey||e.ctrlKey))ask()});
loadPats();
</script></body></html>"""
