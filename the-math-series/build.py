# -*- coding: utf-8 -*-
import sys, html
sys.path.insert(0,'/tmp/claude-0/-home-user-Sakshamsharma/fc7f77a9-0059-5e0a-800f-2bda6f23326d/scratchpad')
from syllabus import DOMAINS, CUTS

e = lambda t: html.escape(t, quote=False)
LEVEL = {
 "ground":      ("Your ground", "You teach this from the room. Needs no research, needs your examples."),
 "adjacent":    ("Adjacent", "You're credible here. Each unit needs one real case to land."),
 "translation": ("Translation", "You're explaining someone else's mechanics. Verify every figure."),
}

n_units = sum(len(u) for _,_,_,cl in DOMAINS for _,u,_ in cl)
n_q     = sum(len(q) for _,_,_,cl in DOMAINS for _,_,q in cl)
n_cl    = sum(len(cl) for _,_,_,cl in DOMAINS)

CSS = """
:root{
  --ground:#E9EEE6; --surface:#F5F8F2; --surface-2:#DEE6D9; --sunk:#E1E8DC;
  --ink:#141C17; --ink-2:#3B4940; --muted:#66756B; --rule:#C6D1C0;
  --accent:#A81F55; --accent-soft:#F3DCE5; --brass:#856A20;
  --display:"Fraunces",Georgia,"Times New Roman",serif;
  --body:"Karla",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#121711; --surface:#1A211A; --surface-2:#242C23; --sunk:#0D120C;
  --ink:#E7ECE3; --ink-2:#C3CDBE; --muted:#8D9B88; --rule:#2F382D;
  --accent:#F2739F; --accent-soft:#3B1C28; --brass:#D3B25D;}}
:root[data-theme="dark"]{
  --ground:#121711; --surface:#1A211A; --surface-2:#242C23; --sunk:#0D120C;
  --ink:#E7ECE3; --ink-2:#C3CDBE; --muted:#8D9B88; --rule:#2F382D;
  --accent:#F2739F; --accent-soft:#3B1C28; --brass:#D3B25D;}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--body);font-size:17px;
  line-height:1.6;margin:0;-webkit-font-smoothing:antialiased}
.wrap{max-width:1140px;margin:0 auto;padding-inline:22px;padding-block:0 90px}
h1,h2,h3,h4{font-family:var(--display);text-wrap:balance;margin:0;line-height:1.14;font-weight:600}
p{margin:0}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
.eyebrow{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);font-weight:500}
header.mast{border-bottom:1px solid var(--rule);padding-block:54px 38px;display:flex;
  flex-direction:column;gap:20px}
.mast h1{font-size:clamp(2.7rem,8vw,4.8rem);letter-spacing:-.02em;font-weight:700}
.mast h1 em{font-style:italic;color:var(--accent)}
.logline{font-family:var(--display);font-size:clamp(1.08rem,2.5vw,1.36rem);font-style:italic;
  color:var(--ink-2);max-width:44ch;line-height:1.35}
.meta{display:flex;flex-wrap:wrap;gap:9px 26px;font-family:var(--mono);font-size:.73rem;
  letter-spacing:.05em;color:var(--muted)}
.meta b{color:var(--ink);font-weight:500}
section{padding-block:48px;border-bottom:1px solid var(--rule)}
section:last-of-type{border-bottom:none}
.sechead{display:flex;flex-direction:column;gap:9px;margin-bottom:26px}
.sechead h2{font-size:clamp(1.6rem,4.2vw,2.25rem);letter-spacing:-.01em}
.lede{font-size:1.03rem;color:var(--ink-2);max-width:66ch}
.note{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--accent);
  padding:22px 26px;display:flex;flex-direction:column;gap:13px}
.note p{max-width:68ch}
.note .kick{font-family:var(--display);font-size:1.18rem;line-height:1.35;font-weight:600}
/* index */
.index{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule)}
.index a{background:var(--surface);padding:14px 16px;display:grid;
  grid-template-columns:30px 1fr;gap:11px;text-decoration:none;color:var(--ink);align-items:baseline}
.index a:hover{background:var(--surface-2)}
.index .n{font-family:var(--mono);font-size:.82rem;color:var(--accent);font-weight:600}
.index .t{font-family:var(--display);font-size:1rem;font-weight:600;line-height:1.25}
.index .c{grid-column:2;font-family:var(--mono);font-size:.66rem;color:var(--muted);letter-spacing:.07em}
/* domains */
.domain{padding-top:44px;scroll-margin-top:12px}
.dhead{border-bottom:2px solid var(--ink);padding-bottom:13px;display:flex;flex-wrap:wrap;
  gap:6px 16px;align-items:baseline}
.dhead .n{font-family:var(--mono);font-size:1.02rem;font-weight:600;color:var(--accent);
  font-variant-numeric:tabular-nums}
.dhead h3{font-size:clamp(1.35rem,3.4vw,1.75rem);letter-spacing:-.01em}
.dhead .lvl{margin-left:auto;font-family:var(--mono);font-size:.64rem;letter-spacing:.12em;
  text-transform:uppercase;padding:3px 9px;border:1px solid var(--rule);white-space:nowrap;color:var(--muted)}
.dhead .lvl.ground{color:var(--accent);border-color:var(--accent)}
.dhead .lvl.adjacent{color:var(--brass);border-color:var(--brass)}
.dkick{font-size:.97rem;color:var(--ink-2);max-width:70ch;padding-top:13px}
.cluster{display:grid;grid-template-columns:minmax(0,230px) minmax(0,1fr);gap:26px;
  padding-block:22px;border-bottom:1px solid var(--rule);align-items:start}
.cluster > h4{font-size:1.06rem;line-height:1.3;position:sticky;top:14px}
.cbody{display:flex;flex-direction:column;gap:14px;min-width:0}
ul.units{margin:0;padding:0;list-style:none;columns:2;column-gap:30px}
ul.units li{font-size:.93rem;color:var(--ink-2);line-height:1.45;margin-bottom:7px;
  break-inside:avoid;padding-left:13px;position:relative}
ul.units li::before{content:"";position:absolute;left:0;top:.62em;width:5px;height:1px;
  background:var(--brass)}
.qs{background:var(--sunk);border-left:2px solid var(--accent);padding:11px 15px;
  display:flex;flex-direction:column;gap:7px}
.qs .lab{font-family:var(--mono);font-size:.63rem;letter-spacing:.13em;text-transform:uppercase;
  color:var(--accent);font-weight:600}
.qs p{font-family:var(--display);font-style:italic;font-size:.99rem;line-height:1.42;color:var(--ink)}
/* cuts */
.cuts{display:flex;flex-direction:column;gap:26px}
.cut{border:1px solid var(--rule);background:var(--surface)}
.cut .ch{padding:18px 24px;border-bottom:1px solid var(--rule);background:var(--surface-2);
  display:flex;flex-direction:column;gap:6px}
.cut .ch h4{font-size:1.14rem}
.cut .ch p{font-size:.89rem;color:var(--ink-2);max-width:72ch}
.cut ol{margin:0;padding:20px 24px 22px 24px;list-style:none;counter-reset:d;
  columns:3;column-gap:26px}
.cut ol li{counter-increment:d;font-size:.88rem;color:var(--ink-2);line-height:1.4;
  margin-bottom:7px;break-inside:avoid;padding-left:26px;position:relative}
.cut ol li::before{content:counter(d,decimal-leading-zero);position:absolute;left:0;
  font-family:var(--mono);font-size:.72rem;color:var(--accent);font-variant-numeric:tabular-nums}
/* gaps */
.gaps{display:flex;flex-direction:column;border-top:1px solid var(--rule)}
.gap-row{display:grid;grid-template-columns:minmax(0,215px) minmax(0,1fr);gap:18px;
  padding-block:16px;border-bottom:1px solid var(--rule);align-items:start}
.gap-row dt{font-family:var(--mono);font-size:.79rem;font-weight:500;color:var(--accent)}
.gap-row dd{margin:0;font-size:.92rem;color:var(--ink-2);line-height:1.55}
.legend{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:20px;font-size:.86rem;color:var(--muted)}
.legend span b{font-family:var(--mono);font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;
  padding:2px 7px;border:1px solid var(--rule);margin-right:7px}
.legend .g b{color:var(--accent);border-color:var(--accent)}
.legend .a b{color:var(--brass);border-color:var(--brass)}
@media (max-width:860px){
  .cluster{grid-template-columns:1fr;gap:11px}
  .cluster > h4{position:static}
  .cut ol{columns:2}
}
@media (max-width:560px){
  body{font-size:16px}
  ul.units,.cut ol{columns:1}
  .gap-row{grid-template-columns:1fr;gap:5px}
  .dhead .lvl{margin-left:0}
}
"""

out = []
w = out.append
w('<title>The Math Syllabus</title>')
w('<link rel="preconnect" href="https://fonts.googleapis.com">')
w('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
w('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,ital,wght@9..144,0,400;9..144,0,600;9..144,0,700;9..144,1,400;9..144,1,600&family=Karla:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">')
w(f'<style>{CSS}</style>')
w('<div class="wrap">')

# masthead
w('<header class="mast">')
w('<div class="eyebrow">Domain map &middot; v2 &middot; 11 Sep 2026</div>')
w('<h1>The <em>Math</em> Syllabus</h1>')
w('<p class="logline">How money and power move through the creative economy &mdash; the whole territory, not a shooting schedule.</p>')
w(f'<div class="meta"><span><b>{len(DOMAINS)}</b> domains</span><span><b>{n_cl}</b> topic clusters</span>'
  f'<span><b>{n_units}</b> teachable units</span><span><b>{n_q}</b> open questions</span>'
  '<span>For the corporate baddie, not the finance bro</span></div>')
w('</header>')

# what changed
w('<section><div class="sechead"><div class="eyebrow">What changed</div>'
  '<h2>Canva is one unit inside one cluster now</h2></div>')
w('<div class="note">')
w('<p class="kick">The last version took a single example and stretched it across thirty slots. This is the territory instead &mdash; you cut the series out of it.</p>')
w('<p>The Canva tender lives in domain 03, cluster one, as one unit among four. It is an illustration of a mechanism, not a subject. Everything that was a &ldquo;day&rdquo; before is now a <strong>unit</strong>, and units are smaller than videos &mdash; several of them can share one script, or one of them can carry three.</p>')
w('<p>The map is deliberately over-built. Two hundred-odd units is more than a year of daily posting, which is the point: a thirty-day run should be a <em>selection</em> with an argument behind it, and you should be able to draw a different thirty next quarter without rebuilding anything. Three example cuts are at the bottom.</p>')
w("<p>Each domain is marked for how close it sits to your own practice &mdash; which tells you where you are teaching from the room and where you are translating someone else&rsquo;s mechanics and need to check the figures.</p>")
w('</div>')
w('<div class="legend">'
  '<span class="g"><b>Your ground</b>From the room. Needs your examples, not research.</span>'
  '<span class="a"><b>Adjacent</b>You\'re credible. Each unit wants one real case.</span>'
  '<span><b>Translation</b>Someone else\'s mechanics. Verify every figure.</span></div>')
w('</section>')

# index
w('<section><div class="sechead"><div class="eyebrow">The territory</div><h2>Ten domains</h2></div>')
w('<div class="index">')
for i,(name,kick,lvl,cls) in enumerate(DOMAINS,1):
    u = sum(len(x) for _,x,_ in cls)
    w(f'<a href="#d{i:02d}"><span class="n">{i:02d}</span><span class="t">{e(name)}</span>'
      f'<span class="c">{len(cls)} clusters &middot; {u} units</span></a>')
w('</div></section>')

# domains
w('<section>')
for i,(name,kick,lvl,cls) in enumerate(DOMAINS,1):
    lab,_ = LEVEL[lvl]
    w(f'<div class="domain" id="d{i:02d}">')
    w(f'<div class="dhead"><span class="n">{i:02d}</span><h3>{e(name)}</h3>'
      f'<span class="lvl {lvl}">{e(lab)}</span></div>')
    w(f'<p class="dkick">{e(kick)}</p>')
    for cname, units, qs in cls:
        w('<div class="cluster">')
        w(f'<h4>{e(cname)}</h4>')
        w('<div class="cbody">')
        w('<ul class="units">' + ''.join(f'<li>{e(u)}</li>' for u in units) + '</ul>')
        if qs:
            w('<div class="qs"><span class="lab">Questions it answers</span>'
              + ''.join(f'<p>{e(q)}</p>' for q in qs) + '</div>')
        w('</div></div>')
    w('</div>')
w('</section>')

# cuts
w('<section><div class="sechead"><div class="eyebrow">Selection</div>'
  '<h2>Three ways to cut thirty days out of it</h2></div>')
w('<p class="lede" style="margin-bottom:24px">Same map, three different arguments. Each is a running order, not a set of scripts &mdash; pick the argument first, then write. None of them uses more than about a seventh of the material.</p>')
w('<div class="cuts">')
for title, desc, days in CUTS:
    w('<div class="cut"><div class="ch">'
      f'<h4>{e(title)}</h4><p>{e(desc)}</p></div>')
    w('<ol>' + ''.join(f'<li>{e(d)}</li>' for d in days) + '</ol></div>')
w('</div></section>')

# gaps
w('<section><div class="sechead"><div class="eyebrow">Open</div>'
  '<h2>What this is still missing</h2></div>')
rows = [
 ("Rad School of Growth",
  "It's a Claude Project, and nothing in this session can open one — no tool exists for it, and it isn't in your Drive either (I searched). Domains 07, 08 and 09 are where your existing frameworks belong, and right now they're carrying my language instead of yours. Paste the Project files here or drop them in a Drive folder and I'll fold them in."),
 ("The creator partnerships session",
  "Same problem — a different conversation, not reachable from here. Domain 05 is the biggest in the map and the one you actually teach, so it's also the one most likely to be wrong in the details. Treat it as a first pass until that research lands."),
 ("Sub-clusters under domain 05",
  "If the partnerships material is as deep as I think, domain 05 probably splits into two — the deal itself, and the relationship around it. I've left it as one until I can see what you already have."),
 ("Your examples",
  "Every unit marked as your ground needs a real case attached before it becomes a script. That's the part I can't write and won't invent."),
 ("Business of Creativity (2020)",
  "Your book of fifteen interviews with Indian creatives is sitting in your Drive and is the most non-substitutable source here. It belongs in domains 08, 09 and 10. Say the word and I'll read it and mark which units it strengthens."),
]
w('<dl class="gaps">')
for dt,dd in rows:
    w(f'<div class="gap-row"><dt>{e(dt)}</dt><dd>{e(dd)}</dd></div>')
w('</dl></section>')
w('</div>')

open('/home/user/Sakshamsharma/the-math-series/index.html','w').write('\n'.join(out))
print("written")
