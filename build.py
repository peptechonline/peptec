#!/usr/bin/env python3
"""Pep Tech Solution static site builder. Edit CONFIG + GUIDES, run: python3 build.py"""
import re, os, json, html, shutil, sys

SRC = sys.argv[1]            # original index.html (CSS is reused from it)
OUT = sys.argv[2]
SITE = "https://YOUR-DOMAIN.com"          # TODO: your real domain (used for canonical + sitemap)
CONTACT = "hello@example.com"             # TODO: real contact email
NEWSLETTER_URL = ""                       # TODO: form action from MailerLite / Brevo etc.
YT = "https://www.youtube.com/@PepTechSolution"
NAME = "Pep Tech Solution"

CATS = {"troubleshooting": ("📱", "Mobile Troubleshooting", "Common smartphone problems and practical fixes."),
        "tools": ("🧰", "Repair Tools & Boxes", "UFI Box, programmers and workshop equipment."),
        "hardware": ("🔥", "Hardware & Soldering", "Repair equipment, components and techniques."),
        "software": ("💻", "Software & Setup", "Drivers, utilities, setup and device workflows.")}

# Add every video here (id from the YouTube URL). 'steps' = YOUR verified written steps.
GUIDES = [
 dict(id="FxGqZhsXJUY", slug="mobile-power-button-not-working", cat="troubleshooting", dur="",
      title="Mobile Power Button Missing / Not Working — Screen On & Off",
      desc="Ways to wake and lock a phone when the power button is missing or broken, and when to get a hardware repair.",
      prep=["Double-tap-to-wake or lift-to-wake (Settings → Display / Gestures, if your phone has it)",
            "Scheduled power on/off (Settings → Accessibility on many Android phones)",
            "Accessibility menu or a screen-off app as a temporary lock option",
            "Check whether the button is stuck or physically damaged before opening the phone"], steps=[]),
 dict(id="vcJXDBhyyKM", slug="jio-bharat-k1-karbonn-hard-reset-flash", cat="troubleshooting", dur="11:58",
      title="Jio Bharat K1 Karbonn 4G — Hard Reset & Flash File",
      desc="Device-specific hard reset and firmware flashing walkthrough for the Jio Bharat K1 Karbonn 4G.",
      prep=["Back up anything you can; a hard reset or flash erases user data",
            "Charge the phone well before starting",
            "Use only firmware that matches the exact model and variant",
            "Use a good USB cable and a stable PC connection"], steps=[]),
 dict(id="SMxfQaCmshU", slug="ufi-box-installation-setup", cat="tools", dur="20:11",
      title="How to Install UFI Box — Setup Tutorial",
      desc="Preparation and setup checklist for installing UFI Box software and drivers on a repair PC.",
      prep=["Confirm your Windows version is supported by the UFI software you downloaded",
            "Download only from the official source",
            "Install the box drivers before connecting the box",
            "Temporarily check antivirus alerts and re-enable protection afterwards"], steps=[]),
 dict(id="pzCbPmyspxE", slug="t12x-soldering-station-overview", cat="hardware", dur="13:30",
      title="T12X Soldering Iron Station — Tool Overview",
      desc="What repair technicians should know about the T12X soldering station: features, temperature habits and tip care.",
      prep=["Work in a ventilated space and use a proper stand",
            "Keep tips tinned and clean to extend their life",
            "Start at lower temperatures and increase only as needed",
            "Never leave the iron on and unattended"], steps=[]),
]

def esc(s): return html.escape(s, quote=True)
def thumb(g): return f"https://i.ytimg.com/vi/{g['id']}/hqdefault.jpg"

def head(title, desc, path, r, extra=""):
    url = f"{SITE}/{path}"
    fav = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%232563eb'/%3E%3Ctext x='32' y='44' font-size='36' font-weight='900' text-anchor='middle' fill='white' font-family='sans-serif'%3EP%3C/text%3E%3C/svg%3E"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#faf7f2">
<link rel="canonical" href="{url}"><link rel="icon" href="{fav}"><link rel="alternate" hreflang="en" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600&amp;family=Space+Grotesk:wght@400;500;600;700&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="{r}assets/styles.css">{extra}</head><body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(r):
    return f"""<div class="topbar"><div class="wrap"><span>Practical tech guides, repair tips &amp; tutorials in Hindi</span><span>Follow <a href="{YT}" target="_blank" rel="noopener">Pep Tech Solution on YouTube ↗</a></span></div></div>
<header class="header"><div class="wrap nav"><a class="brand" href="{r or './'}"><span class="logo">P</span><span>PEP TECH <span style="color:#c2410c">SOLUTION</span></span></a>
<nav class="navlinks" id="navlinks" aria-label="Main"><a href="{r}#home">Home</a><a href="{r}#tutorials">Video Tutorials</a><a href="{r}#categories">Categories</a><a href="{r}#articles">Guides</a><a href="{r}#about">About</a></nav>
<div class="navright"><a class="btn" href="{YT}?sub_confirmation=1" target="_blank" rel="noopener">▶ Subscribe</a><button class="menu" id="menu" aria-label="Toggle navigation" aria-expanded="false" aria-controls="navlinks">☰</button></div></div></header>
"""

def footer(r):
    return f"""<footer class="footer"><div class="wrap"><div class="footer-grid">
<div><a class="brand" href="{r or './'}" style="color:#fff"><span class="logo">P</span><span>PEP TECH SOLUTION</span></a><p>A Guide For All The Tech Learners. Practical smartphone troubleshooting, repair tools and technology tutorials.</p><a href="{YT}" target="_blank" rel="noopener">▶ YouTube Channel ↗</a></div>
<div><h4>Explore</h4><a href="{r}#tutorials">Video Tutorials</a><a href="{r}#categories">Categories</a><a href="{r}#articles">Guides</a></div>
<div><h4>Popular topics</h4>{''.join(f'<a href="{r}#articles" data-go="{k}">{v[1]}</a>' for k, v in list(CATS.items())[:3])}</div>
<div><h4>Information</h4><a href="{r}#about">About</a><a href="mailto:{CONTACT}">Contact</a><a href="{r}privacy/">Privacy Policy</a><a href="{r}affiliate-disclosure/">Affiliate Disclosure</a></div>
</div><div class="copyright"><span>© <span id="year">2026</span> {NAME}. All rights reserved.</span><span>Built for learning • Repair responsibly</span></div></div></footer>
<script src="{r}assets/app.js" defer></script></body></html>"""

def yt(g, title=None):
    return (f'<div class="yt" data-id="{g["id"]}" data-title="{esc(title or g["title"])}"><button type="button" aria-label="Play video: {esc(g["title"])}">'
            f'<img src="{thumb(g)}" width="480" height="360" loading="lazy" alt="" onerror="this.remove()"><span class="play">▶</span></button></div>')

def card(g, r):
    c = CATS[g["cat"]]
    dur = f'<span class="duration">{g["dur"]}</span>' if g["dur"] else ""
    return (f'<article class="post" data-cat="{g["cat"]}" data-search="{esc((g["title"]+" "+g["desc"]+" "+c[1]).lower())}">'
            f'<a class="thumb cover c-{g["cat"]}" href="{r}guides/{g["slug"]}/" tabindex="-1" aria-hidden="true"><span class="ico">{c[0]}</span><img src="{thumb(g)}" width="480" height="360" loading="lazy" alt="" onerror="this.remove()">{dur}</a>'
            f'<div class="post-body"><span class="tag">{c[1]}</span><h3><a href="{r}guides/{g["slug"]}/">{esc(g["title"])}</a></h3><p>{esc(g["desc"])}</p>'
            f'<div class="playrow"><span class="meta">Video + written guide</span><a href="{r}guides/{g["slug"]}/">Read guide →</a></div></div></article>')

def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

# ---------- CSS: reuse original, patch, extend ----------
orig = open(SRC, encoding="utf-8").read()
css = """
:root{--bg:#faf7f2;--panel:#ffffff;--panel2:#f4f0e8;--line:#e6e0d4;--ink:#1b1b1f;--muted:#5f5b55;--amber:#c2410c;--cyan:#0f766e;--blue:#2563eb;--r:16px;--sans:"Space Grotesk",ui-sans-serif,system-ui,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,Menlo,monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:var(--sans);color:var(--ink);background:var(--bg) radial-gradient(#00000010 1px,transparent 1px) 0 0/24px 24px;line-height:1.65}
a{color:inherit;text-decoration:none}button,input{font:inherit}.wrap{width:min(1160px,calc(100% - 40px));margin:auto}
.topbar{background:#1b1b1f;border-bottom:0;color:#d6d3d1;font:12px var(--mono)}.topbar .wrap{display:flex;justify-content:space-between;gap:15px;padding:8px 0}.topbar a{color:#fdba74}
.header{position:sticky;top:0;z-index:20;background:#faf7f2e6;backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav{height:72px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.brand{display:flex;align-items:center;gap:11px;font-weight:700;letter-spacing:-.3px;font-size:18px}
.logo{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--amber),#ff6b35);display:grid;place-items:center;color:#fff;font-weight:800;font-size:19px;box-shadow:0 0 24px #c2410c44}
.navlinks{display:flex;gap:26px;font-size:14px;font-weight:500;color:var(--muted)}.navlinks a:hover{color:var(--ink)}
.navright{display:flex;align-items:center;gap:10px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:11px 18px;border-radius:10px;background:var(--amber);color:#fff;font-weight:700;font-size:14px;border:1px solid var(--amber);cursor:pointer;transition:.2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px #c2410c33}.btn.outline{background:transparent;color:var(--ink);border-color:#d6cfc0}.btn.outline:hover{border-color:var(--cyan);box-shadow:none}
.menu{display:none;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:9px 12px}
.hero{position:relative;overflow:hidden;border-bottom:1px solid var(--line)}
.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(600px 320px at 85% 10%,#0f766e20,transparent 70%),radial-gradient(500px 300px at 0 100%,#c2410c14,transparent 70%)}
.hero-grid{position:relative;display:grid;grid-template-columns:1fr 1.05fr;gap:52px;align-items:center;padding:72px 0 80px}
.eyebrow{display:inline-flex;align-items:center;gap:9px;border:1px solid #d6cfc0;background:var(--panel);border-radius:99px;padding:6px 13px;color:var(--cyan);font:600 11px var(--mono);letter-spacing:1px;text-transform:uppercase}
.dot{width:7px;height:7px;border-radius:50%;background:var(--cyan);box-shadow:0 0 0 4px #0f766e22}
.hero h1{font-size:clamp(40px,5.4vw,66px);line-height:1.03;letter-spacing:-2.5px;margin:22px 0 18px}.hero h1 span{background:linear-gradient(90deg,#c2410c,#f97316);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{color:var(--muted);font-size:17px;max-width:540px;margin:0 0 28px}.hero-actions{display:flex;flex-wrap:wrap;gap:12px}
.hero-meta{display:flex;gap:30px;margin-top:38px;padding-top:22px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}.hero-meta .k{display:block;color:var(--ink);font-size:17px;font-weight:700}
.stage{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:12px;box-shadow:0 24px 60px #1b1b1f26,0 0 0 1px #0f766e12}
.stage-cap{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:14px 6px 4px;font-size:13px;color:var(--muted)}.stage-cap b{color:var(--ink);font-weight:600}.stage-cap a{color:var(--amber);font-weight:600;white-space:nowrap}
.section{padding:78px 0}.section.soft{background:#f1ece2;border-block:1px solid var(--line)}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:30px}
.kicker{color:var(--amber);font:600 12px var(--mono);letter-spacing:1.4px;text-transform:uppercase}
.section h2{font-size:clamp(28px,3.2vw,40px);line-height:1.12;letter-spacing:-1.2px;margin:8px 0}.section-head p{color:var(--muted);max-width:560px;margin:6px 0 0}
.categories{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.category{border:1px solid var(--line);border-radius:var(--r);padding:22px;background:var(--panel);transition:.2s;position:relative}
.category:hover,.post:hover{transform:translateY(-4px);border-color:#c2410c66;box-shadow:0 16px 36px #1b1b1f1f}
.cat-icon{width:46px;height:46px;border-radius:12px;display:grid;place-items:center;background:#c2410c18;font-size:22px;margin-bottom:14px}
.category h3{font-size:16px;margin:0 0 4px}.category p{font-size:13px;color:var(--muted);margin:0}
.post-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:20px}
.post{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;transition:.2s;display:flex;flex-direction:column}
.thumb{position:relative;aspect-ratio:16/9;overflow:hidden;display:block;background:#111}
.cover{background:linear-gradient(135deg,var(--c1),var(--c2))}.cover:before{content:"";position:absolute;inset:0;background:radial-gradient(#ffffff1f 1px,transparent 1px) 0 0/14px 14px}
.cover .ico{position:absolute;inset:0;display:grid;place-items:center;font-size:44px;filter:drop-shadow(0 6px 14px #0006)}
.cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.c-troubleshooting{--c1:#1e3a8a;--c2:#0e7490}.c-tools{--c1:#7c2d12;--c2:#ea580c}.c-hardware{--c1:#7f1d1d;--c2:#d97706}.c-software{--c1:#312e81;--c2:#0891b2}
.duration{position:absolute;bottom:9px;right:9px;background:#05080dd9;color:#fff;padding:3px 8px;border-radius:6px;font:600 11px var(--mono);z-index:2}
.post-body{padding:18px;display:flex;flex-direction:column;flex:1}
.tag{align-self:flex-start;color:var(--cyan);background:#0f766e14;border:1px solid #0f766e33;padding:3px 9px;border-radius:6px;font:600 10px var(--mono);text-transform:uppercase;letter-spacing:.7px}
.post-body h3{font-size:17px;line-height:1.3;margin:12px 0 8px}.post-body h3 a:hover{color:var(--amber)}.post-body p{font-size:13.5px;color:var(--muted);margin:0 0 14px}
.playrow{display:flex;align-items:center;justify-content:space-between;margin-top:auto;padding-top:12px;border-top:1px solid var(--line)}.playrow a{color:var(--amber);font-size:13px;font-weight:700}.meta{font-size:12px;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 auto 18px}.chip{border:1px solid #d6cfc0;background:var(--panel);color:var(--muted);border-radius:99px;padding:8px 16px;font-weight:600;font-size:13px;cursor:pointer;transition:.2s}.chip:hover{color:var(--ink)}.chip[aria-pressed=true]{background:var(--amber);color:#fff;border-color:var(--amber)}
.searchbar{display:flex;gap:8px;max-width:520px;margin:0 auto 30px}.searchbar input{width:100%;background:var(--panel);color:var(--ink);border:1px solid #d6cfc0;border-radius:10px;padding:12px 16px;outline:none}.searchbar input:focus{border-color:var(--cyan)}
.empty{display:none;text-align:center;color:var(--muted);padding:24px}.empty:not([hidden]){display:block}[hidden]{display:none!important}
.yt{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:linear-gradient(135deg,#1e3a8a,#0e7490)}.yt img,.yt iframe{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border:0}.yt button{position:absolute;inset:0;width:100%;border:0;background:transparent;cursor:pointer;padding:0;z-index:1}
.play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:76px;height:76px;border-radius:50%;background:var(--amber);color:#fff;display:grid;place-items:center;font-size:26px;padding-left:5px;box-shadow:0 0 0 10px #c2410c30,0 14px 36px #0004;transition:.2s}.yt button:hover .play{transform:translate(-50%,-50%) scale(1.08)}
.about-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:48px;align-items:center}
.about-mark{color:#fff;background:linear-gradient(145deg,#2a2a33,#1b1b1f);border:1px solid var(--line);border-radius:22px;padding:40px;min-height:270px;display:flex;flex-direction:column;justify-content:space-between}.about-mark .big{font-size:80px;font-weight:700;line-height:1;color:#fdba74}
.about-grid p{color:var(--muted)}.about-grid a:not(.btn){color:var(--amber)}
.newsletter{color:#fff;background:linear-gradient(115deg,#1b1b1f,#0f3d3a);border:0;border-radius:22px;padding:38px;display:flex;justify-content:space-between;align-items:center;gap:24px}.newsletter h2{margin:0 0 8px}.newsletter p{color:#d4d4d8;margin:0}
.newsletter form{display:flex;gap:8px;min-width:min(400px,100%)}.newsletter input{min-width:0;flex:1;background:#fff;color:var(--ink);border:1px solid #d6cfc0;border-radius:10px;padding:12px 14px}
.notice,.form-note{font-size:12px;color:var(--muted);margin-top:12px;min-height:1.2em}
.footer{background:#1b1b1f;border-top:0;color:#a8a29e;padding:56px 0 22px}.footer-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:30px}.footer p{font-size:13px;max-width:300px}.footer h4{color:#fff;margin:0 0 12px}.footer a{display:block;font-size:13px;margin:8px 0}.footer a:hover{color:#fdba74}.footer .brand{color:#fff}
.copyright{border-top:1px solid #3a3a42;margin-top:36px;padding-top:18px;font-size:12px;display:flex;justify-content:space-between;gap:15px}
.skip{position:absolute;left:-999px;top:8px}.skip:focus{left:10px;z-index:99;background:var(--amber);color:#fff;padding:9px 14px;border-radius:8px}
:focus-visible{outline:3px solid var(--cyan);outline-offset:2px}
.article{max-width:820px;margin:auto;padding:40px 0 80px}.crumbs{font:12px var(--mono);color:var(--muted)}.crumbs a{color:var(--amber)}
.article h1{font-size:clamp(30px,4.2vw,46px);line-height:1.1;letter-spacing:-1.5px;margin:14px 0}.article h2{font-size:22px;margin:36px 0 10px}.article li{margin:7px 0;color:#3f3b36}.article .lead{color:var(--muted);font-size:18px}
.article .yt{margin:26px 0 8px;border:1px solid var(--line)}
.callout{background:#c2410c12;border:1px solid #c2410c44;border-radius:12px;padding:14px 16px;font-size:14px}.todo{background:var(--panel);border:1px dashed #bdb4a2;border-radius:12px;padding:14px 16px;font-size:14px;color:var(--muted)}.todo code{color:var(--cyan)}
.related{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
@media(max-width:900px){.navlinks{display:none;position:absolute;top:72px;left:0;right:0;background:#faf7f2;border-bottom:1px solid var(--line);padding:18px 22px;flex-direction:column;gap:15px}.navlinks.open{display:flex}.menu{display:block}.navright .btn{display:none}
.hero-grid{grid-template-columns:1fr;gap:36px;padding:52px 0}.categories{grid-template-columns:repeat(2,1fr)}.footer-grid{grid-template-columns:1fr 1fr}.about-grid{grid-template-columns:1fr}.newsletter{display:block}.newsletter form{margin-top:18px;min-width:0}}
@media(max-width:600px){.wrap{width:calc(100% - 30px)}.topbar .wrap span:last-child{display:none}.section{padding:56px 0}.section-head{display:block}.hero h1{letter-spacing:-1.6px}.related{grid-template-columns:1fr}.copyright{display:block}.hero-meta{gap:18px}.newsletter{padding:24px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""
write("assets/styles.css", css)

write("assets/app.js", """(()=>{const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const menu=$('#menu'),nav=$('#navlinks');
if(menu){menu.addEventListener('click',()=>{const o=nav.classList.toggle('open');menu.setAttribute('aria-expanded',o)});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded',false)}))}
$$('.yt').forEach(box=>box.querySelector('button').addEventListener('click',()=>{
const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+box.dataset.id+'?autoplay=1&rel=0';
f.title=box.dataset.title;f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.allowFullscreen=true;box.replaceChildren(f);f.focus()}));
const y=$('#year');if(y)y.textContent=new Date().getFullYear();
const grid=$('#postGrid');if(grid){const cards=$$('#postGrid .post'),q=$('#search'),empty=$('#empty'),chips=$$('.chip');let cat='all';
function run(){const t=q.value.trim().toLowerCase();let n=0;cards.forEach(c=>{const ok=(cat==='all'||c.dataset.cat===cat)&&c.dataset.search.includes(t);c.hidden=!ok;if(ok)n++});empty.hidden=n>0;}
function setCat(c){cat=c;chips.forEach(b=>b.setAttribute('aria-pressed',b.dataset.cat===c));run()}
chips.forEach(b=>b.addEventListener('click',()=>setCat(b.dataset.cat)));
$$('[data-go]').forEach(a=>a.addEventListener('click',()=>setCat(a.dataset.go)));
$('#searchForm').addEventListener('submit',e=>{e.preventDefault();run()});q.addEventListener('input',run);
const h=location.hash.slice(1);if(CATS_OK(h))setCat(h);function CATS_OK(h){return chips.some(b=>b.dataset.cat===h)}}
const nl=$('#newsletter');if(nl){nl.addEventListener('submit',e=>{if(!nl.getAttribute('action')){e.preventDefault();
$('#nlNote').textContent='Newsletter is not connected yet — please follow on YouTube for now.'}})}})();
""")

# ---------- Home ----------
f = GUIDES[0]
cat_cards = "".join(f'<a class="category" href="#articles" data-go="{k}"><div class="cat-icon" aria-hidden="true">{v[0]}</div><h3>{v[1]}</h3><p>{v[2]}</p></a>' for k, v in CATS.items())
vid_cards = "".join(
    f'<article class="video-card"><a class="thumb" href="guides/{g["slug"]}/"><img src="{thumb(g)}" width="480" height="360" loading="lazy" alt="{esc(g["title"])}">'
    + (f'<span class="duration">{g["dur"]}</span>' if g["dur"] else "") +
    f'</a><div class="video-body"><span class="tag">{CATS[g["cat"]][1]}</span><h3><a href="guides/{g["slug"]}/">{esc(g["title"])}</a></h3><p>{esc(g["desc"])}</p>'
    f'<div class="playrow"><span class="meta">Pep Tech Solution</span><a href="https://www.youtube.com/watch?v={g["id"]}" target="_blank" rel="noopener">Watch on YouTube ↗</a></div></div></article>'
    for g in GUIDES[1:4])
chips = '<button class="chip" type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button class="chip" type="button" data-cat="{k}" aria-pressed="false">{v[1]}</button>' for k, v in CATS.items())
ld = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/", "inLanguage": ["en", "hi"],
                 "publisher": {"@type": "Organization", "name": NAME, "sameAs": [YT]}})
home = head(f"{NAME} — Mobile Repair & Tech Tutorials", "Practical mobile repair tutorials, smartphone troubleshooting, hardware tools, soldering tips and tech guides in Hindi.", "", "",
            f'<script type="application/ld+json">{ld}</script>') + header("") + f"""<main id="main">
<section class="hero" id="home"><div class="wrap hero-grid"><div><div class="eyebrow"><span class="dot"></span> Learn • Repair • Solve</div>
<h1>Understand Tech.<br><span>Fix It Yourself.</span></h1><p>A practical guide to smartphone troubleshooting, mobile hardware repair, repair tools and everyday technology — with step-by-step video tutorials from Pep Tech Solution.</p>
<div class="hero-actions"><a class="btn" href="#tutorials">▶ Explore tutorials</a><a class="btn outline" href="{YT}" target="_blank" rel="noopener">Visit YouTube channel ↗</a></div>
<div class="hero-meta"><div><span class="k">Hindi</span>Practical guides</div><div><span class="k">Step by step</span>Video + written</div><div><span class="k">Free</span>Tools &amp; tips</div></div></div>
<div class="stage">{yt(f)}<div class="stage-cap"><span><b>Featured:</b> {esc(f['title'])}</span><a href="guides/{f['slug']}/">Read guide →</a></div></div></div></section>
<section class="section" id="categories"><div class="wrap"><div class="section-head"><div><div class="kicker">Explore by topic</div><h2>What do you want to learn?</h2><p>Pick a topic to filter the guides below.</p></div></div><div class="categories">{cat_cards}</div></div></section>
<section class="section soft" id="articles"><span id="tutorials"></span><div class="wrap"><div class="section-head"><div><div class="kicker">Knowledge base</div><h2>Repair &amp; tech guides</h2><p>Search across every guide or filter by topic.</p></div></div>
<div class="chips" role="group" aria-label="Filter by topic">{chips}</div>
<form class="searchbar" id="searchForm" role="search"><input id="search" type="search" placeholder="Search tutorials and guides..." aria-label="Search guides"><button class="btn" type="submit">Search</button></form>
<div class="post-grid" id="postGrid">{''.join(card(g, '') for g in GUIDES)}</div><div class="empty" id="empty" hidden role="status">No matching guides. Try another search term.</div></div></section>
<section class="section soft" id="about"><div class="wrap about-grid"><div class="about-mark"><div class="big">P.</div><div><strong>Pep Tech Solution</strong><br><span style="color:#a9bdd1">A practical guide to mobile technology</span></div></div>
<div><div class="kicker">About the channel</div><h2>Learn practical tech, one fix at a time.</h2><p>Pep Tech Solution is a technology tutorial channel covering smartphone troubleshooting, mobile repair workflows, repair tools and related technical topics. This companion site makes those lessons easier to search, follow and revisit.</p>
<p>Every guide pairs the video with a written explanation, required tools, safety considerations and related guides. Some links on this site may be affiliate links — see the <a href="affiliate-disclosure/" style="color:var(--amber)">disclosure</a>.</p><a class="btn" href="{YT}" target="_blank" rel="noopener">Visit Pep Tech Solution ↗</a></div></div></section>
<section class="section"><div class="wrap"><div class="newsletter"><div><h2>Get new tech guides</h2><p>Join the mailing list for new tutorials and practical repair resources.</p></div>
<form id="newsletter" method="post" action="{NEWSLETTER_URL}"><input type="email" name="email" placeholder="Your email address" aria-label="Your email address" required><button class="btn" type="submit">Join newsletter</button></form></div><p class="form-note notice" id="nlNote" role="status" style="text-align:center"></p></div></section>
</main>""" + footer("")
write("index.html", home)

# ---------- Guide pages ----------
for g in GUIDES:
    r = "../../"; c = CATS[g["cat"]]
    rel = [x for x in GUIDES if x is not g and x["cat"] == g["cat"]] + [x for x in GUIDES if x is not g and x["cat"] != g["cat"]]
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "image": thumb(g),
                     "inLanguage": "en", "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME},
                     "mainEntityOfPage": f"{SITE}/guides/{g['slug']}/"})
    body = f"""<main id="main"><div class="wrap"><article class="article">
<div class="crumbs"><a href="{r}">Home</a> / <a href="{r}#articles" >Guides</a> / {c[1]}</div>
<h1>{esc(g['title'])}</h1><p class="lead">{esc(g['desc'])}</p>
{yt(g)}
<h2>Before you start</h2><ul>{''.join(f'<li>{esc(p)}</li>' for p in g['prep'])}</ul>
<h2>Written steps</h2>{('<ol>'+''.join(f'<li>{esc(s)}</li>' for s in g['steps'])+'</ol>') if g['steps'] else '<div class="todo"><strong>To add:</strong> write the exact steps from the video here (edit <code>steps</code> in <code>build.py</code>), plus screenshots and the tools used. Original, verified steps are what make this page rank and help readers.</div>'}
<h2>Safety</h2><div class="callout">Repair and flashing can erase data or damage a device if done incorrectly. Back up first, use files that match your exact model, and proceed at your own risk.</div>
<h2>Related guides</h2><div class="related">{''.join(card(x, r) for x in rel[:2])}</div>
</article></div></main>"""
    write(f"guides/{g['slug']}/index.html", head(f"{g['title']} | {NAME}", g["desc"], f"guides/{g['slug']}/", r, f'<script type="application/ld+json">{ld}</script>') + header(r) + body + footer(r))

# ---------- Legal / 404 ----------
def simple(path, title, inner, r):
    write(path, head(f"{title} | {NAME}", title, path, r) + header(r) + f'<main id="main"><div class="wrap"><article class="article"><h1>{title}</h1>{inner}</article></div></main>' + footer(r))
simple("privacy/index.html", "Privacy Policy", f"""<p class="todo"><strong>Template — review before publishing.</strong> This is a starting draft, not legal advice.</p>
<h2>What we collect</h2><p>This site does not require an account. If you subscribe to the newsletter, we collect your email address to send updates. Contact emails you send us are used only to reply.</p>
<h2>Third-party services</h2><p>Videos load from YouTube (youtube-nocookie.com) only after you click play. Thumbnails are loaded from YouTube's image servers. Your newsletter provider and any analytics or ad services you add should be listed here.</p>
<h2>Your choices</h2><p>You can unsubscribe at any time using the link in any email. To request removal of your data, write to <a href="mailto:{CONTACT}" style="color:var(--amber)">{CONTACT}</a>.</p>""", "../")
simple("affiliate-disclosure/index.html", "Affiliate Disclosure", f"""<p class="todo"><strong>Template — review before publishing.</strong> This is a starting draft, not legal advice.</p>
<p>Some links on this site may be affiliate links. If you buy through them, we may earn a commission at no extra cost to you. We only recommend tools we have used or reviewed, and commissions do not change our opinions.</p><p>Questions? <a href="mailto:{CONTACT}" style="color:var(--amber)">{CONTACT}</a></p>""", "../")
write("404.html", head(f"Page not found | {NAME}", "Page not found", "404.html", "") + header("") + '<main id="main"><div class="wrap"><article class="article"><h1>Page not found</h1><p class="lead">That page does not exist. Try the <a href="/" style="color:var(--amber)">homepage</a> or browse the guides.</p></article></div></main>' + footer(""))

# ---------- SEO files ----------
urls = ["", "privacy/", "affiliate-disclosure/"] + [f"guides/{g['slug']}/" for g in GUIDES]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
shutil.copy(__file__, os.path.join(OUT, "build.py"))
print("built", len(urls), "pages")
