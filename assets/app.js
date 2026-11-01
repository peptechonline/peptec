(()=>{const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
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
