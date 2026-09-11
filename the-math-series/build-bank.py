# -*- coding: utf-8 -*-
import sys, html
sys.path.insert(0,'/tmp/claude-0/-home-user-Sakshamsharma/fc7f77a9-0059-5e0a-800f-2bda6f23326d/scratchpad')
from bank import CHAPTERS, FORMATS
e = lambda t: html.escape(t, quote=False)

n_ideas = sum(len(i) for _,_,i in CHAPTERS)
n_ver   = sum(1 for _,_,i in CHAPTERS for x in i if x[2])
n_tr    = sum(1 for _,_,i in CHAPTERS for x in i if x[3])

CSS = """
:root{
  --ground:#E9EEE6; --surface:#F5F8F2; --surface-2:#DEE6D9; --sunk:#E1E8DC;
  --ink:#141C17; --ink-2:#3B4940; --muted:#66756B; --rule:#C6D1C0;
  --accent:#A81F55; --accent-soft:#F3DCE5; --brass:#856A20;
  --display:"Fraunces",Georgia,"Times New Roman",serif;
  --body:"Karla",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;}
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
h1,h2,h3,h4{font-family:var(--display);text-wrap:balance;margin:0;line-height:1.16;font-weight:600}
p{margin:0}
a{color:var(--accent)}
.eyebrow{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);font-weight:500}
header.mast{border-bottom:1px solid var(--rule);padding-block:54px 38px;display:flex;
  flex-direction:column;gap:20px}
.mast h1{font-size:clamp(2.5rem,7.4vw,4.4rem);letter-spacing:-.02em;font-weight:700}
.mast h1 em{font-style:italic;color:var(--accent)}
.logline{font-family:var(--display);font-size:clamp(1.06rem,2.4vw,1.32rem);font-style:italic;
  color:var(--ink-2);max-width:46ch;line-height:1.36}
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
/* formats */
.fmts{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:0;
  border-top:1px solid var(--rule);border-left:1px solid var(--rule)}
.fmt{background:var(--surface);padding:20px 22px;display:flex;flex-direction:column;gap:9px;
  border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.fmt h4{font-size:1.04rem;line-height:1.28}
.fmt p{font-size:.89rem;color:var(--ink-2);line-height:1.52}
.fmt .ex{font-family:var(--display);font-style:italic;font-size:.95rem;line-height:1.42;
  color:var(--ink);border-left:2px solid var(--brass);padding-left:12px;margin-top:2px}
/* chapters */
.chap{padding-top:42px;scroll-margin-top:12px}
.chead{border-bottom:2px solid var(--ink);padding-bottom:12px;display:flex;flex-wrap:wrap;
  gap:6px 16px;align-items:baseline}
.chead .n{font-family:var(--mono);font-size:1rem;font-weight:600;color:var(--accent);
  font-variant-numeric:tabular-nums}
.chead h3{font-size:clamp(1.3rem,3.3vw,1.7rem);letter-spacing:-.01em}
.chead .ct{margin-left:auto;font-family:var(--mono);font-size:.68rem;color:var(--muted);
  letter-spacing:.07em;white-space:nowrap}
.ckick{font-size:.96rem;color:var(--ink-2);max-width:70ch;padding-top:12px;padding-bottom:4px}
.ideas{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:0;
  border-top:1px solid var(--rule);border-left:1px solid var(--rule);margin-top:18px}
.idea{background:var(--surface);padding:19px 21px 17px;display:flex;flex-direction:column;gap:10px;
  border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.idea h4{font-size:1.03rem;line-height:1.32}
.usual{display:flex;flex-direction:column;gap:5px}
.usual .lab{font-family:var(--mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--brass);font-weight:600}
.usual p{font-size:.9rem;color:var(--ink-2);line-height:1.53}
.flags{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto;padding-top:3px}
.flag{font-family:var(--mono);font-size:.6rem;letter-spacing:.11em;text-transform:uppercase;
  padding:2px 7px;border:1px solid var(--rule);color:var(--muted);white-space:nowrap}
.flag.v{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}
.flag.t{color:var(--brass);border-color:var(--brass)}
/* gaps */
.gaps{display:flex;flex-direction:column;border-top:1px solid var(--rule)}
.gap-row{display:grid;grid-template-columns:minmax(0,215px) minmax(0,1fr);gap:18px;
  padding-block:16px;border-bottom:1px solid var(--rule);align-items:start}
.gap-row dt{font-family:var(--mono);font-size:.79rem;font-weight:500;color:var(--accent)}
.gap-row dd{margin:0;font-size:.92rem;color:var(--ink-2);line-height:1.55}
.legend{display:flex;flex-wrap:wrap;gap:10px 24px;margin-top:20px;font-size:.87rem;color:var(--muted)}
.legend span b{font-family:var(--mono);font-size:.6rem;letter-spacing:.11em;text-transform:uppercase;
  padding:2px 7px;border:1px solid var(--rule);margin-right:8px}
.legend .v b{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}
.legend .t b{color:var(--brass);border-color:var(--brass)}
@media (max-width:560px){
  body{font-size:16px}
  .gap-row{grid-template-columns:1fr;gap:5px}
  .chead .ct{margin-left:0}
}
"""

o=[]; w=o.append
w('<title>The Usual</title>')
w('<link rel="preconnect" href="https://fonts.googleapis.com">')
w('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
w('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,ital,wght@9..144,0,400;9..144,0,600;9..144,0,700;9..144,1,400;9..144,1,600&family=Karla:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">')
w(f'<style>{CSS}</style>')
w('<div class="wrap">')

w('<header class="mast">')
w('<div class="eyebrow">Content bank &middot; companion to The Math Syllabus &middot; 11 Sep 2026</div>')
w('<h1>The <em>Usual</em></h1>')
w('<p class="logline">For brand and creative people who want fuck-you money and were handed the same paperwork as the engineers with half the context.</p>')
w(f'<div class="meta"><span><b>{n_ideas}</b> ideas</span><span><b>{len(CHAPTERS)}</b> situations</span>'
  f'<span><b>{len(FORMATS)}</b> recurring formats</span><span><b>{n_ver}</b> need a verified number</span></div>')
w('</header>')

w('<section><div class="sechead"><div class="eyebrow">The angle</div>'
  '<h2>Norms are the product, not definitions</h2></div>')
w('<div class="note">')
w('<p class="kick">Everybody explains what a liquidation preference <em>is</em>. Almost nobody says what&rsquo;s normal &mdash; which is the only thing that tells you whether you&rsquo;re being had.</p>')
w('<p>That&rsquo;s the whole differentiation and it follows from where you actually sit. A lawyer will define an ISO more accurately than you ever will. A lawyer will not tell a 28-year-old brand lead that four years with a one-year cliff is the default, that ninety days is the usual exercise window, or that nobody ever asks about the preference stack and the asking is free. Calibration is the product. You have it because you&rsquo;ve been in the rooms; they don&rsquo;t because nobody has ever shown them a second example.</p>')
w('<p>So every idea below carries two parts &mdash; the hook, and <strong>the usual</strong>. If an idea has no norm attached, it&rsquo;s a definition and it belongs to somebody else.</p>')
w('<p>The wedge inside the audience: brand, design, content and partnerships people <em>inside</em> tech and startup companies. They hold the same instruments as the engineers, and every piece of equity content on the internet is written for someone who reads a term sheet for fun.</p>')
w('</div>')
w('<div class="legend">'
  '<span class="v"><b>Check the number</b>Do not say this on camera until you have a current source.</span>'
  '<span class="t"><b>Travels</b>Screenshot-shaped. Prioritise these when you need reach.</span></div>')
w('</section>')

w('<section><div class="sechead"><div class="eyebrow">Shapes</div>'
  '<h2>Eight recurring formats</h2></div>')
w('<p class="lede" style="margin-bottom:24px">Pick the shape before the topic. A format the audience recognises is what turns sixty-nine ideas into a series rather than sixty-nine posts &mdash; and the first one below is the franchise.</p>')
w('<div class="fmts">')
for name,desc,ex in FORMATS:
    w(f'<div class="fmt"><h4>{e(name)}</h4><p>{e(desc)}</p><p class="ex">{e(ex)}</p></div>')
w('</div></section>')

w('<section>')
for i,(title,kick,ideas) in enumerate(CHAPTERS,1):
    w(f'<div class="chap" id="c{i}">')
    w(f'<div class="chead"><span class="n">{i:02d}</span><h3>{e(title)}</h3>'
      f'<span class="ct">{len(ideas)} ideas</span></div>')
    w(f'<p class="ckick">{e(kick)}</p>')
    w('<div class="ideas">')
    for hook, usual, ver, tr in ideas:
        w('<div class="idea">')
        w(f'<h4>{e(hook)}</h4>')
        w(f'<div class="usual"><span class="lab">The usual</span><p>{e(usual)}</p></div>')
        fl=[]
        if ver: fl.append('<span class="flag v">Check the number</span>')
        if tr:  fl.append('<span class="flag t">Travels</span>')
        if fl:  w('<div class="flags">'+''.join(fl)+'</div>')
        w('</div>')
    w('</div></div>')
w('</section>')

w('<section><div class="sechead"><div class="eyebrow">Before you shoot</div>'
  '<h2>Where this still needs you</h2></div>')
rows=[
("The fifteen flagged numbers",
 "Every idea marked in pink states a benchmark I have not verified against a current source. Carta and Pave publish equity band data; agency multiples and utilisation rates vary enough by market that a single figure is misleading. Get the real number or reframe the idea so it doesn't need one — saying a wrong benchmark confidently is the one failure this whole series cannot survive."),
("Your side of the table",
 "Chapter 04 is the only one where you can say “I've written the brief your fee was in.” That sentence is worth more than any statistic here and it can't be borrowed. Mark which of those thirteen you've personally seen go wrong."),
("Rad School of Growth",
 "Still unreachable from this session — it's a Claude Project and no tool here opens one. Chapters 03 and 06 are the ones your existing frameworks should be carrying, and right now they're carrying mine."),
("The partnerships session",
 "Same. Chapter 04 is a first pass built from general practice. It's the chapter most likely to be wrong in the specifics and the one you're most qualified to correct."),
("What's deliberately missing",
 "No tax content, no investment advice, no “here's what to do with the money.” Different liability, different register, and the moment the series gives financial advice it stops being yours and starts being regulated."),
]
w('<dl class="gaps">')
for dt,dd in rows: w(f'<div class="gap-row"><dt>{e(dt)}</dt><dd>{e(dd)}</dd></div>')
w('</dl></section>')
w('</div>')

open('/home/user/Sakshamsharma/the-math-series/the-usual.html','w').write('\n'.join(o))
print('written')
