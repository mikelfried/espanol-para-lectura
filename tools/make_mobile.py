#!/usr/bin/env python3
"""Build the mobile trainer: docs/index.html, one self-contained file.

The PDF is the reading artifact; this is its complement. A path of units with
short lessons (meet a word, pick its meaning, pick the Spanish, type it),
spaced review, search, and the plates. No framework, no build step, no network.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (scope_svg keeps plate styles from colliding)

DATA = {
    "units": build.units(),
    "grammar": build.load("grammar.json"),
    "cognates": build.load("cognates.json"),
    "plates": [{**p, "svg": build.scope_svg(p["svg"], p["id"])} for p in build.plates()],
}

ICONS = {
    "path": '<path d="M12 3a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm-6 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm12 0a3 3 0 1 1 0 6 3 3 0 0 1 0-6z" fill="currentColor"/><path d="M10 8.5 7.5 12.3M14 8.5l2.5 3.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "review": '<path d="M20 11a8 8 0 1 0-2.3 5.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M20.5 5.5V11h-5.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>',
    "plates": '<rect x="3.5" y="4.5" width="17" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="2.1"/><path d="m4 17 5-5 4 4 2.5-2.5L20 18" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linejoin="round"/><circle cx="15.5" cy="9" r="1.8" fill="currentColor"/>',
    "flame": '<path d="M12.5 2.5c.6 3-1.4 4.6-2.7 6.2C8.4 10.4 7 12.1 7 14.6 7 18 9.3 21 12.5 21S18 18.4 18 15c0-2.6-1.4-4.3-2.3-5.3.1 1.6-.5 2.8-1.6 3.4.5-3.8-.6-8-1.6-10.6z" fill="currentColor"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    "book": '<path d="M4 5.5C4 4.7 4.7 4 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5zM20 5.5c0-.8-.7-1.5-1.5-1.5H13v16h5.5c.8 0 1.5-.7 1.5-1.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    "back": '<path d="M15 5 8 12l7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
}

CSS = r"""
:root{
  --bg:#f7f6f2; --card:#fff; --ink:#1f2328; --dim:#626973; --faint:#9aa1aa;
  --line:#e4e1da; --line2:#d4d0c7;
  --g:#2f8a5f; --gd:#236a48; --gl:#e2f3e9; --gt:#1c5c3d;
  --r:#d0473f; --rd:#a8352e; --rl:#fbe7e5; --rt:#8c2a24;
  --b:#3a7cc2; --bl:#e7f0fa;
  --fl:#ef8a2c;
  --round:ui-rounded,"SF Pro Rounded",-apple-system,system-ui,sans-serif;
  --serif:"Iowan Old Style",Charter,Georgia,serif;
  --tab:calc(58px + env(safe-area-inset-bottom));
}
@media (prefers-color-scheme:dark){:root{
  --bg:#141619; --card:#1e2125; --ink:#eceae6; --dim:#a4abb4; --faint:#6f7780;
  --line:#2c3035; --line2:#3a3f45;
  --g:#3fa673; --gd:#2c7a53; --gl:#17301f; --gt:#8fd9ae;
  --r:#e0605a; --rd:#b0433e; --rl:#3a1c1b; --rt:#f3a7a2;
  --b:#5a9ae0; --bl:#1b2a3b;
}}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.45 var(--round);
  padding-bottom:var(--tab)}
button{font:inherit;color:inherit}
svg.i{width:24px;height:24px;display:block}
.hide{display:none!important}

/* ---------- chunky buttons ------------------------------------------ */
.btn{display:block;width:100%;border:0;border-radius:16px;padding:15px 18px;
  font-size:17px;font-weight:700;letter-spacing:.2px;text-align:center;
  background:var(--g);color:#fff;box-shadow:0 4px 0 var(--gd);
  transform:translateY(0);transition:transform .06s,box-shadow .06s}
.btn:active{transform:translateY(4px);box-shadow:0 0 0 var(--gd)}
.btn.ghost{background:var(--card);color:var(--ink);
  box-shadow:0 4px 0 var(--line2);border:2px solid var(--line2)}
.btn.ghost:active{box-shadow:0 0 0 var(--line2)}
.btn.red{background:var(--r);box-shadow:0 4px 0 var(--rd)}
.btn:disabled{background:var(--line);color:var(--faint);box-shadow:0 4px 0 var(--line2)}

/* ---------- top bar --------------------------------------------------- */
.top{position:sticky;top:0;z-index:20;background:var(--bg);
  padding:calc(env(safe-area-inset-top) + 10px) 18px 10px;
  display:flex;align-items:center;gap:12px;border-bottom:2px solid var(--line)}
.top h1{margin:0;flex:1;font-size:21px;font-weight:800;letter-spacing:-.2px}
.chip{display:flex;align-items:center;gap:5px;font-weight:800;font-size:16px}
.chip .i{width:22px;height:22px}
.chip.fl{color:var(--fl)} .chip.off{color:var(--faint)}
.goal{position:relative;width:34px;height:34px}
.goal svg{width:34px;height:34px;transform:rotate(-90deg)}
.goal b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-size:10px;font-weight:800;color:var(--dim)}
.iconbtn{border:0;background:none;padding:8px;margin:-8px;color:var(--dim)}
main{padding:18px 18px 28px}

/* ---------- learn path ------------------------------------------------ */
.readfirst{display:flex;gap:14px;align-items:center;background:var(--card);
  border:2px solid var(--line);border-radius:18px;padding:14px 16px;margin-bottom:26px;
  box-shadow:0 3px 0 var(--line);width:100%;text-align:left}
.readfirst .i{color:var(--b);width:30px;height:30px;flex:none}
.readfirst b{display:block;font-size:16px}
.readfirst span{color:var(--dim);font-size:14px}
.path{position:relative;display:flex;flex-direction:column;align-items:center;gap:44px;
  padding-bottom:10px}
.node{position:relative;display:flex;flex-direction:column;align-items:center;
  background:none;border:0;padding:0;width:170px}
.ring{width:84px;height:84px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;position:relative}
.disc{width:66px;height:66px;border-radius:50%;background:var(--card);
  border:2px solid var(--line2);box-shadow:0 5px 0 var(--line2);
  display:flex;align-items:center;justify-content:center;
  font-size:22px;font-weight:800;color:var(--dim);transition:transform .06s,box-shadow .06s}
.node:active .disc{transform:translateY(5px);box-shadow:0 0 0 var(--line2)}
.node.done .disc{background:var(--g);border-color:var(--gd);color:#fff;box-shadow:0 5px 0 var(--gd)}
.node.now .disc{background:var(--g);border-color:var(--gd);color:#fff;box-shadow:0 5px 0 var(--gd)}
.node.now .ring::after{content:"";position:absolute;inset:-6px;border-radius:50%;
  border:3px solid var(--g);opacity:.35}
.node .nl{margin-top:8px;font-size:14px;font-weight:700;text-align:center;line-height:1.25}
.node .ns{font-size:12px;color:var(--faint);font-weight:600}
.startflag{position:absolute;top:-30px;background:var(--card);color:var(--g);
  border:2px solid var(--line2);border-radius:10px;padding:3px 10px;font-size:12px;
  font-weight:800;letter-spacing:.8px;text-transform:uppercase;white-space:nowrap}
.startflag::after{content:"";position:absolute;left:50%;bottom:-7px;width:10px;height:10px;
  background:var(--card);border-right:2px solid var(--line2);border-bottom:2px solid var(--line2);
  transform:translateX(-50%) rotate(45deg)}

/* ---------- bottom sheet --------------------------------------------- */
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.32);z-index:40;opacity:0;
  pointer-events:none;transition:opacity .2s}
.scrim.on{opacity:1;pointer-events:auto}
.sheet{position:fixed;left:0;right:0;bottom:0;z-index:41;background:var(--card);
  border-radius:22px 22px 0 0;padding:10px 20px calc(env(safe-area-inset-bottom) + 22px);
  transform:translateY(105%);transition:transform .25s cubic-bezier(.2,.8,.2,1)}
.sheet.on{transform:none}
.grab{width:40px;height:5px;border-radius:3px;background:var(--line2);margin:0 auto 14px}
.sheet .k{font-size:12px;letter-spacing:1.2px;text-transform:uppercase;color:var(--faint);font-weight:800}
.sheet h2{margin:2px 0 6px;font-size:23px;font-weight:800;letter-spacing:-.3px}
.sheet p{margin:0 0 14px;color:var(--dim);font-size:15px}
.bar{height:12px;border-radius:6px;background:var(--line);overflow:hidden;margin:4px 0 6px}
.bar i{display:block;height:100%;background:var(--g);border-radius:6px}
.sheet .row{display:flex;flex-direction:column;gap:12px;margin-top:18px}

/* ---------- reading lists -------------------------------------------- */
.lead{color:var(--dim);font-size:15px;margin:0 0 16px}
.e{background:var(--card);border:2px solid var(--line);border-radius:16px;
  padding:13px 15px;margin-bottom:10px}
.eh{font-family:var(--serif);font-size:21px;font-weight:600}
.pos{font:600 12px var(--round);color:var(--faint);margin-left:7px}
.gl{margin:1px 0 0;font-size:16px}
.he{margin:2px 0 0;color:var(--dim);font-size:16px}
.note{margin:7px 0 0;font-size:14px;color:var(--dim)}
.conj{margin:9px 0 0;display:flex;flex-wrap:wrap;gap:4px 12px;font-size:14px;
  background:var(--bg);border-radius:10px;padding:8px 10px}
.conj span{white-space:nowrap} .conj i{font-style:normal;color:var(--faint);font-size:12px;margin-right:3px}
.warn{margin:9px 0 0;font-size:14px;background:var(--rl);color:var(--rt);
  border-radius:12px;padding:9px 11px}
.warn b{display:block;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px}
.ex{margin:9px 0 0}
.ex .tag{display:inline-block;font-size:11px;font-weight:800;color:var(--faint);
  text-transform:uppercase;letter-spacing:.6px;margin-bottom:1px}
.ex .s{display:block;font-family:var(--serif);font-size:17px}
.ex .t{display:block;color:var(--dim);font-size:14.5px}
.hidden .gl,.hidden .he,.hidden .ex .t{filter:blur(6px);transition:filter .15s}
.hidden .e:active .gl,.hidden .e:active .he,.hidden .e:active .ex .t{filter:none}
.seg{display:inline-flex;background:var(--line);border-radius:12px;padding:3px;margin:0 0 16px}
.seg button{border:0;background:none;padding:7px 14px;border-radius:9px;font-size:14px;font-weight:700;color:var(--dim)}
.seg button.on{background:var(--card);color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.12)}
.sect{font-size:12px;letter-spacing:1.2px;text-transform:uppercase;color:var(--faint);font-weight:800;margin:22px 0 8px}
.cog{list-style:none;margin:0;padding:0;columns:2;column-gap:14px;font-size:15px}
.cog li{margin-bottom:4px;break-inside:avoid} .cog b{font-family:var(--serif);font-weight:600}
.cog span{color:var(--dim);font-size:13px}

/* ---------- search ---------------------------------------------------- */
.sbox{position:relative;margin-bottom:14px}
.sbox .i{position:absolute;left:13px;top:13px;color:var(--faint);width:22px;height:22px}
#q{width:100%;font:17px var(--round);padding:12px 14px 12px 44px;border-radius:14px;
  border:2px solid var(--line2);background:var(--card);color:var(--ink);-webkit-appearance:none}
#q:focus{outline:0;border-color:var(--b)}
.empty{text-align:center;color:var(--faint);padding:40px 10px;font-size:15px}

/* ---------- plates ---------------------------------------------------- */
.plate{margin-bottom:28px}
.plate h2{font-size:18px;font-weight:800;margin:0 0 10px}
.pfig{background:#fff;border:2px solid var(--line);border-radius:16px;padding:8px;
  overflow-x:auto;-webkit-overflow-scrolling:touch}
.pfig svg{width:100%;height:auto;display:block}
.pfig.zoom svg{width:820px;max-width:none}
.pfig.nolab .lab{visibility:hidden}
.ptools{display:flex;gap:8px;margin:10px 0}
.pill{border:2px solid var(--line2);background:var(--card);border-radius:999px;
  padding:6px 13px;font-size:14px;font-weight:700;color:var(--dim)}
.pill.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}

/* ---------- review hub ------------------------------------------------ */
.hero{background:var(--card);border:2px solid var(--line);border-radius:22px;
  padding:22px 20px;text-align:center;margin-bottom:18px}
.hero .big{font-size:52px;font-weight:800;line-height:1;letter-spacing:-1px}
.hero .cap{color:var(--dim);font-size:15px;margin:6px 0 18px}
.stats3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}
.stat{background:var(--card);border:2px solid var(--line);border-radius:16px;padding:12px 8px;text-align:center}
.stat b{display:block;font-size:22px;font-weight:800}
.stat span{font-size:12px;color:var(--faint);font-weight:700}
.tiny{font-size:13px;color:var(--faint);text-align:center;margin:18px 0 10px}
.linkrow{display:flex;gap:10px}
.linkrow .btn{font-size:15px;padding:12px}

/* ---------- tab bar --------------------------------------------------- */
nav{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;background:var(--bg);
  border-top:2px solid var(--line);padding:6px 6px env(safe-area-inset-bottom)}
nav button{flex:1;border:0;background:none;display:flex;flex-direction:column;align-items:center;
  gap:2px;padding:4px 0 6px;color:var(--faint);font-size:11px;font-weight:700;border-radius:12px}
nav button .i{width:26px;height:26px}
nav button.on{color:var(--g)}
.badge{position:absolute;margin:-4px 0 0 20px;background:var(--r);color:#fff;border-radius:9px;
  font-size:10px;font-weight:800;padding:1px 5px;min-width:17px}

/* ---------- lesson ---------------------------------------------------- */
#lesson{position:fixed;inset:0;z-index:50;background:var(--bg);display:flex;flex-direction:column;
  padding-top:env(safe-area-inset-top)}
.lh{display:flex;align-items:center;gap:14px;padding:12px 18px}
.lh .iconbtn{margin:0;padding:6px}
.lbar{flex:1;height:16px;border-radius:8px;background:var(--line);overflow:hidden}
.lbar i{display:block;height:100%;background:var(--g);border-radius:8px;
  transition:width .35s cubic-bezier(.2,.8,.2,1);box-shadow:inset 0 -4px 0 rgba(0,0,0,.08)}
.lbody{flex:1;overflow-y:auto;padding:10px 20px 20px}
.kind{font-size:13px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:var(--b);margin:6px 0 10px}
.q{font-size:26px;font-weight:800;line-height:1.2;letter-spacing:-.3px;margin:0 0 22px}
.q.es{font-family:var(--serif);font-weight:600;font-size:34px;letter-spacing:0}
.opts{display:flex;flex-direction:column;gap:12px}
.opt{border:2px solid var(--line2);background:var(--card);border-radius:16px;padding:14px 16px;
  text-align:left;font-size:17px;font-weight:600;box-shadow:0 4px 0 var(--line2);
  transition:transform .06s,box-shadow .06s;display:flex;gap:12px;align-items:center}
.opt:active{transform:translateY(4px);box-shadow:0 0 0 var(--line2)}
.opt .n{flex:none;width:26px;height:26px;border-radius:8px;border:2px solid var(--line2);
  display:flex;align-items:center;justify-content:center;font-size:13px;color:var(--faint);font-weight:800}
.opt.es{font-family:var(--serif);font-size:20px}
.opt.sel{border-color:var(--b);background:var(--bl);box-shadow:0 4px 0 var(--b)}
.opt.sel .n{border-color:var(--b);color:var(--b)}
.opt.ok{border-color:var(--g);background:var(--gl);box-shadow:0 4px 0 var(--g)}
.opt.bad{border-color:var(--r);background:var(--rl);box-shadow:0 4px 0 var(--r)}
.opt[disabled]{pointer-events:none}
.meet{background:var(--card);border:2px solid var(--line);border-radius:22px;padding:22px 20px;text-align:center}
.meet .new{display:inline-block;background:var(--bl);color:var(--b);font-size:12px;font-weight:800;
  letter-spacing:1px;text-transform:uppercase;border-radius:8px;padding:3px 9px;margin-bottom:12px}
.meet .w{font-family:var(--serif);font-size:38px;font-weight:600;line-height:1.1}
.meet .p{color:var(--faint);font-size:13px;font-weight:700;margin-top:4px}
.meet .m{font-size:19px;font-weight:700;margin-top:14px}
.meet .h{color:var(--dim);font-size:17px;margin-top:3px}
.meet .x{margin-top:16px;padding-top:14px;border-top:2px solid var(--line);text-align:left}
.meet .x .s{font-family:var(--serif);font-size:18px}
.meet .x .t{color:var(--dim);font-size:15px}
.meet .warn{text-align:left}
.meet .conj{justify-content:center}
.type{width:100%;font:22px var(--serif);padding:14px 16px;border-radius:16px;border:2px solid var(--line2);
  background:var(--card);color:var(--ink);-webkit-appearance:none}
.type:focus{outline:0;border-color:var(--b)}
.hint{color:var(--faint);font-size:14px;margin-top:10px}
.lfoot{padding:14px 20px calc(env(safe-area-inset-bottom) + 16px);border-top:2px solid var(--line);background:var(--bg)}
.lfoot.ok{background:var(--gl);border-color:transparent}
.lfoot.bad{background:var(--rl);border-color:transparent}
.fb{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px}
.fb .dot{flex:none;width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff}
.fb .dot .i{width:20px;height:20px}
.lfoot.ok .dot{background:var(--g)} .lfoot.bad .dot{background:var(--r)}
.fb b{display:block;font-size:19px;font-weight:800}
.lfoot.ok .fb b{color:var(--gt)} .lfoot.bad .fb b{color:var(--rt)}
.fb span{display:block;font-size:15px}
.lfoot.ok .fb span{color:var(--gt)} .lfoot.bad .fb span{color:var(--rt)}
.fb .ans{font-family:var(--serif);font-size:18px;font-weight:600}
.done{text-align:center;padding-top:30px}
.done .medal{width:112px;height:112px;border-radius:50%;background:var(--gl);color:var(--g);
  margin:0 auto 18px;display:flex;align-items:center;justify-content:center;border:4px solid var(--g)}
.done .medal .i{width:56px;height:56px}
.done h2{font-size:28px;font-weight:800;margin:0 0 6px;letter-spacing:-.4px}
.done p{color:var(--dim);margin:0 0 24px}
.pop{animation:pop .28s cubic-bezier(.2,.8,.3,1.4)}
@keyframes pop{from{transform:scale(.85);opacity:0}to{transform:none;opacity:1}}
.shake{animation:shake .32s}
@keyframes shake{25%{transform:translateX(-6px)}50%{transform:translateX(6px)}75%{transform:translateX(-3px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = r"""
const D=window.__DATA__, IC=window.__ICONS__;
const $=(s,r=document)=>r.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));
const fold=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
const icon=(n,c='i')=>`<svg class="${c}" viewBox="0 0 24 24">${IC[n]}</svg>`;
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const today=()=>Math.floor((Date.now()-new Date().getTimezoneOffset()*6e4)/864e5);

/* ---------- words -------------------------------------------------- */
const ALL=[];
D.units.forEach((u,ui)=>u.entries.forEach(e=>ALL.push({...e,u:ui,un:ui+1,unit:u.title,id:u.id+'|'+e.es})));
ALL.forEach(e=>e._hay=fold([e.es,e.en,e.he||'',e.note||'',e.warn||'',...(e.ex||[]).flatMap(x=>[x.es,x.en])].join(' ')));
const first=e=>e.en.split(';')[0].trim();                 // first sense, for prompts
const typeable=e=>!/[·\/(]/.test(e.es)&&e.es.split(' ').length<=3;
const ART=/^(el|la|los|las|un|una)\s+/;

/* ---------- state -------------------------------------------------- */
const load=(k,d)=>{try{return JSON.parse(localStorage.getItem(k))||d}catch(_){return d}};
let prog=load('esp.progress.v1',{}), meta=load('esp.meta.v1',{days:[],goalDay:0,goalN:0});
const save=()=>{try{localStorage.setItem('esp.progress.v1',JSON.stringify(prog));localStorage.setItem('esp.meta.v1',JSON.stringify(meta))}catch(_){}};
const GOAL=20, BOX=[0,1,3,7,21,60];
const goalToday=()=>meta.goalDay===today()?meta.goalN:0;
function streak(){
  const s=new Set(meta.days);let n=0,d=today();
  if(!s.has(d))d--;                         // today not done yet still keeps yesterday's run
  while(s.has(d)){n++;d--}return n;
}
const learned=ui=>D.units[ui].entries.filter(e=>prog[D.units[ui].id+'|'+e.es]).length;
const dueList=()=>{const t=today();return ALL.filter(e=>prog[e.id]&&prog[e.id].due<=t)};

/* ---------- shell -------------------------------------------------- */
let tab='learn', read=null;
const TABS=[['learn','Learn','path'],['review','Review','review'],['search','Search','search'],['plates','Plates','plates']];
function topBar(title,back){
  const g=goalToday(),st=streak(),C=2*Math.PI*14,f=Math.min(1,g/GOAL);
  return `<div class="top">${back?`<button class="iconbtn" id="bk">${icon('back')}</button>`:''}
  <h1>${esc(title)}</h1>
  <span class="chip ${st?'fl':'off'}">${icon('flame')}${st}</span>
  <span class="goal" title="Daily goal"><svg viewBox="0 0 34 34"><circle cx="17" cy="17" r="14" fill="none" stroke="var(--line)" stroke-width="4"/>
  <circle cx="17" cy="17" r="14" fill="none" stroke="var(--g)" stroke-width="4" stroke-linecap="round"
  stroke-dasharray="${C}" stroke-dashoffset="${C*(1-f)}"/></svg><b>${Math.min(g,GOAL)}</b></span></div>`;
}
function navHTML(){
  const due=dueList().length;
  return TABS.map(([t,l,ic])=>`<button data-t="${t}" class="${t===tab?'on':''}">${icon(ic)}${
    t==='review'&&due?`<span class="badge">${due>99?'99+':due}</span>`:''}${l}</button>`).join('');
}
function render(){
  $('nav').innerHTML=navHTML();
  document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{tab=b.dataset.t;read=null;render();scrollTo(0,0)});
  ({learn:vLearn,review:vReview,search:vSearch,plates:vPlates})[tab]();
}

/* ---------- learn -------------------------------------------------- */
function vLearn(){
  if(read!==null)return vRead();
  const nowU=D.units.findIndex((u,i)=>learned(i)<u.entries.length);
  const offs=[0,48,70,48,0,-48,-70,-48];
  let h=topBar('Español')+'<main>';
  h+=`<button class="readfirst" data-r="G">${icon('book')}<div><b>Read this first</b><span>${esc(D.grammar.title)} · 13 words</span></div></button>`;
  h+='<div class="path">';
  D.units.forEach((u,i)=>{
    const n=learned(i),t=u.entries.length,f=n/t,cls=n===t?'done':i===nowU?'now':'';
    const ring=`conic-gradient(var(--g) ${f*360}deg,var(--line) 0)`;
    h+=`<button class="node ${cls}" data-u="${i}" style="transform:translateX(${offs[i%8]}px)">
      ${i===nowU?'<span class="startflag">'+(n?'Continue':'Start')+'</span>':''}
      <span class="ring" style="background:${ring}"><span class="disc">${n===t?icon('check'):i+1}</span></span>
      <span class="nl">${esc(u.title)}</span><span class="ns">${n} / ${t}</span></button>`;
  });
  h+=`</div><button class="readfirst" data-r="A" style="margin-top:30px">${icon('book')}<div><b>Words you already know</b><span>Cognates and false friends</span></div></button></main>`;
  $('#app').innerHTML=h;
  document.querySelectorAll('[data-u]').forEach(b=>b.onclick=()=>openSheet(+b.dataset.u));
  document.querySelectorAll('[data-r]').forEach(b=>b.onclick=()=>{read=b.dataset.r;render();scrollTo(0,0)});
  const cur=document.querySelector('.node.now');
  if(cur&&!vLearn.scrolled){vLearn.scrolled=1;cur.scrollIntoView({block:'center'})}
}
function openSheet(i){
  const u=D.units[i],n=learned(i),t=u.entries.length;
  $('#sheet').innerHTML=`<div class="grab"></div><div class="k">Unit ${i+1}</div><h2>${esc(u.title)}</h2>
  <p>${esc(u.intro||'')}</p><div class="bar"><i style="width:${n/t*100}%"></i></div>
  <div class="tiny" style="text-align:left;margin:0">${n} of ${t} words learned</div>
  <div class="row"><button class="btn" id="go">${n===t?'Practise again':n?'Next lesson':'Start first lesson'}</button>
  <button class="btn ghost" id="rd">Read the unit</button></div>`;
  $('#scrim').classList.add('on');$('#sheet').classList.add('on');
  $('#go').onclick=()=>{closeSheet();startLesson(i)};
  $('#rd').onclick=()=>{closeSheet();read=i;render();scrollTo(0,0)};
}
function closeSheet(){$('#scrim').classList.remove('on');$('#sheet').classList.remove('on')}

function entryHTML(e,unit){
  let h=`<div class="e"><div class="eh">${esc(e.es)}<span class="pos">${esc(e.pos||'')}${unit?' · unit '+e.un:''}</span></div>`;
  h+=`<p class="gl">${esc(e.en.replace(/; /g,' · '))}</p>`;
  if(e.he)h+=`<p class="he" dir="rtl" lang="he">${esc(e.he)}</p>`;
  if(e.warn)h+=`<div class="warn"><b>Watch out</b>${esc(e.warn)}</div>`;
  if(e.note)h+=`<p class="note">${esc(e.note)}</p>`;
  if(e.conj){const p=['yo','tú','él','nos.','ellos'];h+='<div class="conj">'+e.conj.forms.map((f,k)=>`<span><i>${p[k]}</i>${esc(f)}</span>`).join('')+'</div>'}
  (e.ex||[]).forEach(x=>h+=`<div class="ex">${x.tag?`<span class="tag">${esc(x.tag)}</span>`:''}<span class="s">${esc(x.es)}</span><span class="t">${esc(x.en)}</span></div>`);
  return h+'</div>';
}
let hideM=false;
function vRead(){
  let title,body;
  if(read==='G'){
    title='Read this first';
    body=`<p class="lead">${esc(D.grammar.intro)}</p>`+D.grammar.items.map(it=>{
      let h=`<div class="e"><div class="eh">${esc(it.word)}</div><p class="gl">${esc(it.gloss)}</p>`;
      if(it.he)h+=`<p class="he" dir="rtl" lang="he">${esc(it.he)}</p>`;
      it.senses.forEach(s=>{h+=`<div class="ex"><span class="tag">${esc(s.label)}</span><span class="t">${esc(s.text)}</span>`+
        (s.ex||[]).map(x=>`<span class="s">${esc(x.es)}</span><span class="t">${esc(x.en)}</span>`).join('')+'</div>'});
      if(it.pitfall)h+=`<div class="warn"><b>Watch out</b>${esc(it.pitfall)}</div>`;
      return h+'</div>'}).join('');
  }else if(read==='A'){
    title='Words you know';
    body=`<p class="lead">${esc(D.cognates.intro)}</p>`+D.cognates.groups.map(g=>`<div class="sect">${esc(g.label)}</div><ul class="cog">`+
      g.words.map(w=>`<li><b>${esc(w.es)}</b>${w.en?` <span>${esc(w.en)}</span>`:''}</li>`).join('')+'</ul>').join('');
  }else{
    const u=D.units[read];title=u.title;
    body=`<p class="lead">${esc(u.intro||'')}</p><div class="seg"><button class="${hideM?'':'on'}" data-h="0">Show all</button><button class="${hideM?'on':''}" data-h="1">Quiz myself</button></div>`+
      (hideM?'<p class="lead" style="margin-top:-6px">Meanings are blurred. Press and hold a word to check it.</p>':'')+
      `<div class="${hideM?'hidden':''}">${u.entries.map(e=>entryHTML(e)).join('')}</div>`;
  }
  $('#app').innerHTML=topBar(title,true)+'<main>'+body+'</main>';
  $('#bk').onclick=()=>{read=null;hideM=false;render()};
  document.querySelectorAll('[data-h]').forEach(b=>b.onclick=()=>{hideM=b.dataset.h==='1';render()});
}

/* ---------- review hub --------------------------------------------- */
function vReview(){
  const due=dueList(),seen=Object.keys(prog).length;
  const strong=Object.values(prog).filter(p=>p.box>=3).length;
  let h=topBar('Review')+'<main><div class="hero">';
  h+=due.length
    ?`<div class="big">${due.length}</div><div class="cap">word${due.length===1?'':'s'} ready to review</div><button class="btn" id="rv">Review now</button>`
    :`<div class="big" style="color:var(--g)">${icon('check','i" style="width:52px;height:52px;margin:0 auto')}</div><div class="cap">${seen?"You're all caught up. New reviews appear as words come due.":'Learn a few words first. They show up here when it is time to review them.'}</div>`;
  h+=`</div><div class="stats3"><div class="stat"><b>${seen}</b><span>learned</span></div>
  <div class="stat"><b>${strong}</b><span>strong</span></div><div class="stat"><b>${streak()}</b><span>day streak</span></div></div>
  <div class="tiny">Progress is saved in this browser. Keep a copy somewhere safe.</div>
  <div class="linkrow"><button class="btn ghost" id="exp">Copy backup</button><button class="btn ghost" id="imp">Restore</button></div></main>`;
  $('#app').innerHTML=h;
  if(due.length)$('#rv').onclick=()=>startReview();
  $('#exp').onclick=async()=>{const t=JSON.stringify({prog,meta});try{await navigator.clipboard.writeText(t);alert('Backup copied.')}catch(_){prompt('Copy this backup:',t)}};
  $('#imp').onclick=()=>{const t=prompt('Paste a backup:');if(!t)return;try{const d=JSON.parse(t);
    if(d.prog){prog=d.prog;meta=d.meta||meta}else prog=d;save();alert('Restored.');render()}catch(_){alert("That doesn't look like a backup.")}};
}

/* ---------- search ------------------------------------------------- */
let lastQ='';
function vSearch(){
  $('#app').innerHTML=topBar('Search')+`<main><div class="sbox">${icon('search')}<input id="q" type="search" placeholder="Spanish, English or Hebrew"
    autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="search"></div><div id="res"></div></main>`;
  const q=$('#q');q.value=lastQ;q.oninput=()=>{lastQ=q.value;results()};results();
}
function results(){
  const q=fold(lastQ.trim());
  if(q.length<2){$('#res').innerHTML='<div class="empty">Search every word, meaning and example sentence.<br>Accents are optional.</div>';return}
  const rank=e=>{const h=fold(e.es);if(h.split(/[\s·/]+/).includes(q)||h===q)return 0;if(h.includes(q))return 1;
    if(fold(e.en+' '+(e.he||'')).includes(q))return 2;return 3};
  const hits=ALL.filter(e=>e._hay.includes(q)).map(e=>[rank(e),e]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]).slice(0,80);
  $('#res').innerHTML=hits.length?`<p class="lead">${hits.length}${hits.length===80?'+':''} result${hits.length===1?'':'s'}</p>`+hits.map(e=>entryHTML(e,1)).join('')
    :'<div class="empty">No matches.</div>';
}

/* ---------- plates ------------------------------------------------- */
function vPlates(){
  $('#app').innerHTML=topBar('Plates')+'<main><p class="lead">Tap a drawing to zoom in. Hide the labels to test yourself.</p>'+D.plates.map((p,i)=>
    `<div class="plate"><h2>${esc(p.title)}</h2><div class="pfig" id="f${i}">${p.svg}</div>
    <div class="ptools"><button class="pill" data-l="${i}">Hide labels</button></div></div>`).join('')+'</main>';
  document.querySelectorAll('.pfig').forEach(f=>f.onclick=()=>{f.classList.toggle('zoom');if(!f.classList.contains('zoom'))f.scrollLeft=0});
  document.querySelectorAll('[data-l]').forEach(b=>b.onclick=()=>{const on=$('#f'+b.dataset.l).classList.toggle('nolab');
    b.classList.toggle('on',on);b.textContent=on?'Show labels':'Hide labels'});
}

/* ---------- lesson engine ------------------------------------------ */
// A lesson is a queue of steps. Missed questions are appended once more at the
// end, so a lesson only ends when everything in it has been answered right.
let L=null;
function distractors(w,field,n=3){
  const key=x=>fold(field==='en'?first(x):x.es.replace(ART,''));
  const pool=shuffle(ALL.filter(x=>x!==w&&key(x)!==key(w)));
  const same=pool.filter(x=>x.u===w.u),other=pool.filter(x=>x.u!==w.u&&x.pos===w.pos);
  const out=[],seen=new Set([key(w)]);
  for(const x of [...same,...other,...pool]){if(out.length===n)break;if(!seen.has(key(x))){seen.add(key(x));out.push(x)}}
  return out;
}
function startLesson(ui){
  const u=D.units[ui];
  const all=u.entries.map(e=>ALL.find(x=>x.id===u.id+'|'+e.es));
  let fresh=all.filter(w=>!prog[w.id]).slice(0,5),steps=[];
  if(fresh.length){
    fresh.forEach(w=>{steps.push({k:'meet',w},{k:'pickEn',w})});
    shuffle(fresh).forEach(w=>steps.push({k:'pickEs',w}));
    shuffle(fresh.filter(typeable)).slice(0,2).forEach(w=>steps.push({k:'type',w}));
  }else{
    // unit already learned: practise its weakest words
    const weak=all.slice().sort((a,b)=>(prog[a.id].box-prog[b.id].box)||Math.random()-.5).slice(0,8);
    weak.forEach(w=>steps.push(stepFor(w)));
  }
  run(steps,`Unit ${ui+1}`);
}
function stepFor(w){
  const b=(prog[w.id]||{box:0}).box;
  if(b>=3&&typeable(w))return{k:'type',w};
  return{k:b>=2?'pickEs':'pickEn',w};
}
function startReview(){run(shuffle(dueList()).slice(0,15).map(stepFor),'Review')}
function run(steps,label){
  L={steps,i:0,label,right:0,asked:0,missed:new Set(),words:new Set(steps.map(s=>s.w.id)),retried:new Set()};
  $('#lesson').classList.remove('hide');document.body.style.overflow='hidden';step();
}
function quit(){$('#lesson').classList.add('hide');document.body.style.overflow='';L=null;render()}
function progressBar(){return `<div class="lh"><button class="iconbtn" id="lx">${icon('close')}</button>
  <div class="lbar"><i style="width:${L.i/L.steps.length*100}%"></i></div></div>`}
function step(){
  const s=L.steps[L.i];if(!s)return finish();
  const w=s.w;let body='',foot='';
  if(s.k==='meet'){
    body=`<div class="kind">New word</div><div class="meet pop"><span class="new">Unit ${w.un}</span>
      <div class="w">${esc(w.es)}</div><div class="p">${esc(w.pos||'')}</div>
      <div class="m">${esc(w.en.replace(/; /g,' · '))}</div>${w.he?`<div class="h" dir="rtl" lang="he">${esc(w.he)}</div>`:''}
      ${w.conj?'<div class="conj">'+w.conj.forms.map((f,k)=>`<span><i>${['yo','tú','él','nos.','ellos'][k]}</i>${esc(f)}</span>`).join('')+'</div>':''}
      ${w.warn?`<div class="warn"><b>Watch out</b>${esc(w.warn)}</div>`:''}
      ${(w.ex||[])[0]?`<div class="x"><div class="s">${esc(w.ex[0].es)}</div><div class="t">${esc(w.ex[0].en)}</div></div>`:''}</div>`;
    foot=`<button class="btn" id="nx">Got it</button>`;
  }else if(s.k==='pickEn'||s.k==='pickEs'){
    const toEn=s.k==='pickEn';
    if(!s.opts)s.opts=shuffle([w,...distractors(w,toEn?'en':'es')]);
    body=`<div class="kind">${toEn?'What does this mean?':'Which is the Spanish?'}</div>
      <div class="q ${toEn?'es':''}">${esc(toEn?w.es:first(w))}</div><div class="opts">`+
      s.opts.map((o,k)=>`<button class="opt ${toEn?'':'es'}" data-o="${k}"><span class="n">${k+1}</span>${esc(toEn?first(o):o.es)}</button>`).join('')+'</div>';
    foot=`<button class="btn" id="ck" disabled>Check</button>`;
  }else{
    body=`<div class="kind">Type it in Spanish</div><div class="q">${esc(first(w))}</div>
      <input class="type" id="ty" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" lang="es" enterkeyhint="done" placeholder="${/^(el|la|los|las) /.test(w.es)?'with el or la':'Spanish'}">
      <div class="hint">Accents are forgiven, but noticed.</div>`;
    foot=`<button class="btn" id="ck" disabled>Check</button>`;
  }
  $('#lesson').innerHTML=progressBar()+`<div class="lbody">${body}</div><div class="lfoot" id="ft">${foot}</div>`;
  $('#lx').onclick=()=>{if(L.i===0||confirm('Leave the lesson? Words you already answered are saved.'))quit()};
  if(s.k==='meet'){
    $('#nx').onclick=()=>{if(!prog[w.id])prog[w.id]={box:0,due:today(),intro:today()};save();L.i++;step()};
    return;
  }
  let pick=null;
  if(s.k==='type'){
    const ty=$('#ty');setTimeout(()=>ty.focus(),60);
    ty.oninput=()=>{$('#ck').disabled=!ty.value.trim()};
    ty.onkeydown=e=>{if(e.key==='Enter'&&ty.value.trim())$('#ck').click()};
  }else{
    document.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{
      document.querySelectorAll('.opt').forEach(x=>x.classList.remove('sel'));b.classList.add('sel');pick=+b.dataset.o;$('#ck').disabled=false});
  }
  $('#ck').onclick=()=>{
    let ok,msg='',ans='';
    if(s.k==='type'){[ok,msg]=checkTyped($('#ty').value,w);$('#ty').readOnly=true;ans=w.es}
    else{
      const toEn=s.k==='pickEn',right=s.opts.indexOf(w);ok=pick===right;
      document.querySelectorAll('.opt').forEach((b,k)=>{b.disabled=true;b.classList.remove('sel');
        if(k===right)b.classList.add('ok');else if(k===pick)b.classList.add('bad')});
      ans=toEn?first(w):w.es;
    }
    grade(s,ok);
    const ex=(w.ex||[])[0];
    $('#ft').className='lfoot '+(ok?'ok':'bad');
    $('#ft').innerHTML=`<div class="fb pop"><span class="dot">${icon(ok?'check':'close')}</span><div>
      <b>${ok?(msg?'Correct, nearly':['Nice','Correct','That’s it','Exactly'][Math.floor(Math.random()*4)]):'Not quite'}</b>
      ${!ok?`<span>Correct answer:</span><span class="ans">${esc(ans)}</span>`:''}
      ${msg?`<span>${esc(msg)}</span>`:''}
      ${ex?`<span style="margin-top:6px;opacity:.85">${esc(ex.es)}</span>`:''}</div></div>
      <button class="btn ${ok?'':'red'}" id="nx">Continue</button>`;
    if(!ok)$('.lbody').classList.add('shake');
    $('#nx').onclick=()=>{L.i++;step()};
  };
}
function checkTyped(raw,w){
  const clean=s=>s.trim().toLowerCase().replace(/[¿?¡!.,]/g,'').replace(/\s+/g,' ');
  const got=clean(raw),want=clean(w.es);
  if(got===want)return[true,''];
  const ga=(got.match(ART)||[''])[0].trim(),wa=(want.match(ART)||[''])[0].trim();
  const gc=got.replace(ART,''),wc=want.replace(ART,'');
  const same=gc===wc,near=fold(gc)===fold(wc);
  if(!same&&!near)return[false,''];
  if(wa&&ga&&ga!==wa)return[false,`It is ${want} — mind the gender.`];
  const notes=[];
  if(!same)notes.push(`Mind the accent: ${w.es}`);
  if(wa&&!ga)notes.push(`Learn it with its article: ${w.es}`);
  return[true,notes.join('. ')];
}
function grade(s,ok){
  const w=s.w;L.asked++;
  if(meta.goalDay!==today()){meta.goalDay=today();meta.goalN=0}
  meta.goalN++;if(!meta.days.includes(today()))meta.days.push(today());
  const retry=L.retried.has(s);
  if(ok){if(!retry)L.right++}
  else{
    L.missed.add(w.id);
    if(!retry){const again={...s,opts:null};L.retried.add(again);L.steps.push(again)}
  }
  // only the first answer in a session moves the word between boxes
  if(!L.graded)L.graded=new Set();
  if(!L.graded.has(w.id)){
    L.graded.add(w.id);
    const p=prog[w.id]||{box:0,intro:today()};
    p.box=ok?Math.min(p.box+1,BOX.length-1):0;
    p.due=today()+BOX[p.box];prog[w.id]=p;
  }
  save();
}
function finish(){
  const pct=L.asked?Math.round(L.right/(L.asked-L.retried.size)*100):100;
  const n=L.words.size,st=streak();
  $('#lesson').innerHTML=`<div class="lbody done"><div class="medal pop">${icon('check')}</div>
    <h2>${L.label==='Review'?'Review done':'Lesson complete'}</h2>
    <p>${n} word${n===1?'':'s'} practised${L.missed.size?`, ${L.missed.size} to keep an eye on`:''}.</p>
    <div class="stats3"><div class="stat"><b>${Math.max(0,Math.min(100,pct))}%</b><span>first try</span></div>
    <div class="stat"><b>${goalToday()}</b><span>of ${GOAL} today</span></div><div class="stat"><b>${st}</b><span>day streak</span></div></div></div>
    <div class="lfoot"><button class="btn" id="nx">Continue</button></div>`;
  $('#nx').onclick=quit;
}

$('#scrim').onclick=closeSheet;
render();
"""


def main():
    html = (
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#f7f6f2" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#141619" media="(prefers-color-scheme: dark)">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Español">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="apple-touch-icon" href="icon-180.png">\n'
        '<title>Español</title>\n'
        f'<style>{CSS}</style></head><body>\n'
        '<div id="app"></div><nav></nav>\n'
        '<div id="scrim" class="scrim"></div><div id="sheet" class="sheet"></div>\n'
        '<div id="lesson" class="hide"></div>\n'
        '<script>window.__DATA__=' + json.dumps(DATA, ensure_ascii=False, separators=(",", ":")) +
        ';window.__ICONS__=' + json.dumps(ICONS) + ';</script>\n'
        f'<script>{JS}</script>\n</body></html>\n'
    )
    out = ROOT / "docs" / "index.html"
    out.write_text(html, encoding="utf-8")
    (ROOT / "docs" / "manifest.webmanifest").write_text(json.dumps({
        "name": "Español para lectura", "short_name": "Español", "start_url": ".",
        "display": "standalone", "background_color": "#f7f6f2", "theme_color": "#f7f6f2",
        "icons": [{"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=2) + "\n", encoding="utf-8")
    print(f"docs/index.html  {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
