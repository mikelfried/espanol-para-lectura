#!/usr/bin/env python3
"""Build the mobile reader/trainer: docs/index.html, self-contained.

Not a port of the book. The PDF is the reading artifact; this is the
complement — search across all 1003 entries, retrieval practice with Leitner
scheduling, and the plates with a label toggle. No framework, no build step,
no network at runtime.

Output goes to docs/ so GitHub Pages can serve it from that folder.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (reuse scope_svg, so plate styles cannot collide)

DATA = {
    "units": build.units(),
    "grammar": build.load("grammar.json"),
    "cognates": build.load("cognates.json"),
    "plates": [
        {**p, "svg": build.scope_svg(p["svg"], p["id"])}
        for p in build.plates()
    ],
}

CSS = r"""
:root {
  --bg:#fbfaf8; --card:#fff; --ink:#15181c; --dim:#6b7280; --faint:#9aa1ab;
  --rule:#e3e0da; --tint:#efece5; --accent:#2f5d55; --warnbar:#1d2229;
  --serif:"Iowan Old Style","Charter",Georgia,serif;
  --ui:-apple-system,system-ui,"Helvetica Neue",sans-serif;
  --tabh:calc(52px + env(safe-area-inset-bottom));
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#15171a; --card:#1d2024; --ink:#e9e6e1; --dim:#9aa1ab; --faint:#6b7280;
    --rule:#2c3035; --tint:#262a2f; --accent:#7fc0b2; --warnbar:#c9c3b8;
  }
}
* { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
html { -webkit-text-size-adjust:100%; }
body {
  margin:0; background:var(--bg); color:var(--ink); font-family:var(--ui);
  font-size:17px; line-height:1.5; padding-bottom:var(--tabh);
  overscroll-behavior-y:contain;
}
/* ---- top bar ---------------------------------------------------------- */
header {
  position:sticky; top:0; z-index:20; background:var(--bg);
  border-bottom:1px solid var(--rule);
  padding:calc(env(safe-area-inset-top) + 8px) 16px 8px;
}
.hrow { display:flex; align-items:baseline; gap:10px; }
h1 { font-family:var(--serif); font-size:19px; font-weight:600; margin:0; }
h1 small { font-weight:400; color:var(--faint); font-size:13px; }
.back {
  font:inherit; font-size:16px; color:var(--accent); background:none;
  border:0; padding:6px 8px 6px 0; margin:0 0 0 -8px; min-height:44px;
}
#q {
  width:100%; margin-top:8px; font:inherit; font-size:17px; padding:10px 12px;
  border:1px solid var(--rule); border-radius:10px; background:var(--card);
  color:var(--ink); -webkit-appearance:none;
}
/* ---- lists ------------------------------------------------------------ */
main { padding:12px 16px 24px; }
.ulist { list-style:none; margin:0; padding:0; }
.ulist li { border-bottom:1px solid var(--rule); }
.ulist button {
  width:100%; text-align:left; background:none; border:0; color:var(--ink);
  font:inherit; padding:13px 2px; min-height:44px; display:flex;
  align-items:baseline; gap:10px;
}
.un { color:var(--faint); font-size:13px; min-width:22px; text-align:right;
      font-variant-numeric:tabular-nums; }
.ut { flex:1; }
.uc { color:var(--faint); font-size:13px; }
.lead { color:var(--dim); font-size:15px; font-style:italic; margin:0 0 14px; }
.sect { font-size:12px; letter-spacing:1.2px; text-transform:uppercase;
        color:var(--faint); margin:22px 0 8px; }
/* ---- entries ---------------------------------------------------------- */
.e { border-bottom:1px solid var(--rule); padding:13px 0; }
.e:last-child { border-bottom:0; }
.eh { font-family:var(--serif); font-size:19px; font-weight:600; }
.pos { font-family:var(--ui); font-size:12px; color:var(--faint);
       font-weight:400; margin-left:6px; }
.gl { margin:2px 0 0; font-family:var(--serif); font-size:17px; }
.he { margin:1px 0 0; font-size:16px; color:var(--dim); }
.note { margin:5px 0 0; font-size:14.5px; color:var(--dim); }
.conj { margin:6px 0 0; font-size:13.5px; color:var(--dim); background:var(--tint);
        border-radius:8px; padding:7px 9px; display:flex; flex-wrap:wrap;
        gap:2px 12px; }
.conj i { color:var(--faint); font-style:normal; font-size:12px; margin-right:3px; }
.conj span { white-space:nowrap; color:var(--ink); }
.warn { margin:7px 0 0; font-size:14.5px; background:var(--tint);
        border-left:3px solid var(--warnbar); border-radius:0 8px 8px 0;
        padding:8px 10px; }
.warn b { display:inline-block; background:var(--warnbar);
          color:var(--bg); font-size:11px; font-weight:700; letter-spacing:.8px;
          text-transform:uppercase; padding:2px 6px; border-radius:4px;
          margin-right:6px; vertical-align:1px; }
.ex { margin:7px 0 0; padding-left:14px; position:relative; }
.ex::before { content:"·"; position:absolute; left:3px; color:var(--faint); }
.ex .tag { font-size:12px; color:var(--faint); font-style:italic; margin-right:5px; }
.ex .s { font-family:var(--serif); }
.ex .t { display:block; color:var(--dim); font-size:15px; }
/* self-test: hide the meanings, keep the Spanish */
.hidden .gl, .hidden .he, .hidden .ex .t { visibility:hidden; }
.tgl { font:inherit; font-size:14px; color:var(--accent); background:none;
       border:1px solid var(--rule); border-radius:999px; padding:7px 14px;
       min-height:44px; margin:0 8px 14px 0; }
.tgl[aria-pressed="true"] { background:var(--accent); color:var(--bg);
                            border-color:var(--accent); }
/* ---- plates ----------------------------------------------------------- */
.plate { margin:0 0 26px; }
.plate h2 { font-family:var(--serif); font-size:18px; margin:0 0 2px; }
.pfig { background:#fff; border:1px solid var(--rule); border-radius:10px;
        padding:8px; overflow-x:auto; -webkit-overflow-scrolling:touch;
        cursor:zoom-in; }
.pfig svg { width:100%; height:auto; display:block; }
.pfig.zoom { cursor:zoom-out; }
.pfig.zoom svg { width:820px; max-width:none; }
.phint { font-size:12px; color:var(--faint); margin:6px 0 0; }
.hidelab .lab { visibility:hidden; }
.pkey { list-style:none; margin:10px 0 0; padding:0; font-size:15px;
        column-count:2; column-gap:16px; }
.pkey li { margin-bottom:3px; break-inside:avoid; }
.pkey b { font-family:var(--serif); font-weight:600; }
.pkey span { color:var(--dim); }
/* ---- practice --------------------------------------------------------- */
.card { background:var(--card); border:1px solid var(--rule); border-radius:14px;
        padding:26px 18px; text-align:center; margin:8px 0 16px; }
.prompt { font-family:var(--serif); font-size:30px; line-height:1.25; }
.promptsub { color:var(--faint); font-size:14px; margin-top:6px; }
.answer { margin-top:16px; padding-top:16px; border-top:1px solid var(--rule);
          font-family:var(--serif); font-size:19px; }
.answer .t { display:block; color:var(--dim); font-size:15px;
             font-family:var(--ui); margin-top:8px; }
.btnrow { display:flex; gap:10px; }
.btn { flex:1; font:inherit; font-size:16px; padding:14px 10px; min-height:48px;
       border-radius:12px; border:1px solid var(--rule); background:var(--card);
       color:var(--ink); }
.btn.primary { background:var(--accent); border-color:var(--accent); color:var(--bg); }
.stats { color:var(--dim); font-size:14px; margin:0 0 14px; }
.tiny { font-size:13px; color:var(--faint); }
/* ---- tab bar ---------------------------------------------------------- */
nav {
  position:fixed; left:0; right:0; bottom:0; z-index:30; display:flex;
  background:var(--bg); border-top:1px solid var(--rule);
  padding-bottom:env(safe-area-inset-bottom);
}
nav button {
  flex:1; background:none; border:0; color:var(--faint); font:inherit;
  font-size:11px; padding:7px 0 5px; min-height:52px; display:flex;
  flex-direction:column; align-items:center; gap:3px;
}
nav button[aria-current="true"] { color:var(--accent); }
nav .ic { font-size:19px; line-height:1; }
.empty { color:var(--faint); text-align:center; padding:40px 0; }
"""

JS = r"""
const D = window.__DATA__;
const $ = (s, r=document) => r.querySelector(s);
const el = (t, c) => { const n = document.createElement(t); if (c) n.className = c; return n; };
const esc = s => String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));
const fold = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

/* every entry gets a stable id so practice progress survives a rebuild */
const ALL = [];
D.units.forEach(u => u.entries.forEach(e => ALL.push({
  ...e, unit: u.title, unitNum: parseInt(u.id.slice(1), 10),
  id: u.id + '|' + e.es,
})));
ALL.forEach(e => {
  e._hay = fold([e.es, e.en, e.he || '', e.note || '', e.warn || '',
    ...(e.ex || []).flatMap(x => [x.es, x.en])].join(' '));
});

/* ---------- rendering an entry ---------------------------------------- */
function entryHTML(e, showUnit) {
  let h = '<div class="e">';
  h += `<div class="eh">${esc(e.es)}${e.pos ? `<span class="pos">${esc(e.pos)}</span>` : ''}` +
       (showUnit ? `<span class="pos">unit ${e.unitNum}</span>` : '') + '</div>';
  h += `<p class="gl">${esc(e.en.replace(/; /g, ' · '))}</p>`;
  if (e.he) h += `<p class="he" dir="rtl" lang="he">${esc(e.he)}</p>`;
  if (e.note) h += `<p class="note">${esc(e.note)}</p>`;
  if (e.warn) h += `<p class="warn"><b>Watch out</b>${esc(e.warn)}</p>`;
  if (e.conj) {
    const p = ['yo', 'tú', 'él/ella', 'nosotros', 'ellos'];
    h += '<p class="conj">' + e.conj.forms
      .map((f, i) => `<span><i>${p[i]}</i>${esc(f)}</span>`).join('') + '</p>';
  }
  (e.ex || []).forEach(x => {
    h += '<p class="ex">' + (x.tag ? `<span class="tag">${esc(x.tag)}</span>` : '') +
         `<span class="s">${esc(x.es)}</span><span class="t">${esc(x.en)}</span></p>`;
  });
  return h + '</div>';
}

/* ---------- state ------------------------------------------------------ */
const KEY = 'esp.progress.v1';
let prog = {};
try { prog = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (_) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(prog)); } catch (_) {} };

let tab = 'browse', openUnit = null, hideMode = false;
const BOX_DAYS = [0, 1, 3, 7, 21];
const today = () => Math.floor(Date.now() / 864e5);

/* ---------- screens ---------------------------------------------------- */
function viewBrowse() {
  const m = $('#view');
  if (openUnit === null) {
    let h = '<p class="lead">Fifty themed units. Frequency chose the words; theme sets the order.</p><ul class="ulist">';
    h += `<li><button data-u="G"><span class="un">—</span><span class="ut">${esc(D.grammar.title)}</span><span class="uc">${D.grammar.items.length}</span></button></li>`;
    D.units.forEach(u => {
      h += `<li><button data-u="${u.id}"><span class="un">${parseInt(u.id.slice(1), 10)}</span>` +
           `<span class="ut">${esc(u.title)}</span><span class="uc">${u.entries.length}</span></button></li>`;
    });
    h += `<li><button data-u="A"><span class="un">—</span><span class="ut">Appendix: words you already know</span></button></li></ul>`;
    m.innerHTML = h;
    m.querySelectorAll('[data-u]').forEach(b =>
      b.onclick = () => { openUnit = b.dataset.u; hideMode = false; render(); });
    return;
  }
  if (openUnit === 'G') return viewGrammar();
  if (openUnit === 'A') return viewAppendix();
  const u = D.units.find(x => x.id === openUnit);
  m.innerHTML =
    `<p class="lead">${esc(u.intro || '')}</p>` +
    `<button class="tgl" id="ht" aria-pressed="${hideMode}">${hideMode ? 'Show meanings' : 'Hide meanings'}</button>` +
    `<div class="${hideMode ? 'hidden' : ''}">${u.entries.map(e => entryHTML(e)).join('')}</div>`;
  $('#ht').onclick = () => { hideMode = !hideMode; render(); };
}

function viewGrammar() {
  const g = D.grammar;
  let h = `<p class="lead">${esc(g.intro)}</p>`;
  g.items.forEach(it => {
    h += `<div class="e"><div class="eh">${esc(it.word)}</div>`;
    h += `<p class="gl">${esc(it.gloss)}</p>`;
    if (it.he) h += `<p class="he" dir="rtl" lang="he">${esc(it.he)}</p>`;
    it.senses.forEach(s => {
      h += `<p class="ex"><span class="tag">${esc(s.label)}</span>${esc(s.text)}`;
      (s.ex || []).forEach(x => { h += `<span class="t">${esc(x.es)} — ${esc(x.en)}</span>`; });
      h += '</p>';
    });
    if (it.pitfall) h += `<p class="warn"><b>Watch out</b>${esc(it.pitfall)}</p>`;
    h += '</div>';
  });
  $('#view').innerHTML = h;
}

function viewAppendix() {
  const c = D.cognates;
  let h = `<p class="lead">${esc(c.intro)}</p>`;
  c.groups.forEach(gr => {
    h += `<p class="sect">${esc(gr.label)}</p><ul class="pkey">`;
    gr.words.forEach(w => {
      h += `<li><b>${esc(w.es)}</b>${w.en ? ` <span>${esc(w.en)}</span>` : ''}</li>`;
    });
    h += '</ul>';
  });
  $('#view').innerHTML = h;
}

function viewSearch() {
  const q = fold($('#q').value.trim());
  if (q.length < 2) {
    $('#view').innerHTML = '<p class="empty">Type two letters or more.<br>Searches Spanish, English, Hebrew and every example sentence.</p>';
    return;
  }
  // rank: headword, then gloss or Hebrew, then notes and sentences
  const rank = e => {
    const h = fold(e.es);
    if (h === q || h.split(/[\s·/]+/).includes(q)) return 0;
    if (h.includes(q)) return 1;
    if (fold(e.en + ' ' + (e.he || '')).includes(q)) return 2;
    return 3;
  };
  const hits = ALL.filter(e => e._hay.includes(q))
    .map(e => [rank(e), e]).sort((a, b) => a[0] - b[0])
    .map(x => x[1]).slice(0, 120);
  $('#view').innerHTML = hits.length
    ? `<p class="lead">${hits.length}${hits.length === 120 ? '+' : ''} match${hits.length === 1 ? '' : 'es'}</p>` +
      hits.map(e => entryHTML(e, true)).join('')
    : '<p class="empty">Nothing found.</p>';
}

function viewPlates() {
  $('#view').innerHTML = D.plates.map((p, i) =>
    `<div class="plate"><h2>${esc(p.title)}</h2>` +
    `<button class="tgl" data-p="${i}" aria-pressed="false">Hide labels</button>` +
    `<div class="pfig" id="fig${i}">${p.svg}</div>` +
    '<p class="phint">Tap the drawing to zoom, then swipe to pan.</p>' +
    '<ul class="pkey">' + p.items.map(it =>
      `<li><b>${esc(it.es)}</b> <span>${esc(it.en)}</span></li>`).join('') +
    '</ul></div>').join('');
  $('#view').querySelectorAll('.pfig').forEach(f => f.onclick = () => {
    f.classList.toggle('zoom');
    if (!f.classList.contains('zoom')) f.scrollLeft = 0;
  });
  $('#view').querySelectorAll('[data-p]').forEach(b => b.onclick = () => {
    const fig = $('#fig' + b.dataset.p);
    const on = fig.classList.toggle('hidelab');
    b.setAttribute('aria-pressed', on);
    b.textContent = on ? 'Show labels' : 'Hide labels';
  });
}

/* ---------- practice: Leitner boxes ----------------------------------- */
let session = null;
const NEW_PER_DAY = 15;
function newToday() {
  // how many new cards were already introduced today
  return Object.values(prog).filter(p => p.intro === today()).length;
}
function reviewsDue() {
  const t = today();
  return ALL.filter(e => prog[e.id] && prog[e.id].due <= t);
}
function freshCards() {
  // new words come in book order, so practice tracks the units you have read
  const left = Math.max(0, NEW_PER_DAY - newToday());
  return ALL.filter(e => !prog[e.id]).slice(0, left);
}
function viewPractice() {
  const m = $('#view');
  const rev = reviewsDue(), fresh = freshCards();
  const due = [...rev, ...fresh];
  const seen = Object.keys(prog).length;
  if (!session) {
    m.innerHTML =
      `<p class="stats">${rev.length} review${rev.length === 1 ? '' : 's'} due · ` +
      `${fresh.length} new today · ${seen} of ${ALL.length} started</p>` +
      `<div class="btnrow"><button class="btn primary" id="go">Start review</button></div>` +
      `<p class="sect">Direction</p><div class="btnrow">` +
      `<button class="btn" id="d1">Spanish → English</button>` +
      `<button class="btn" id="d2">English → Spanish</button></div>` +
      `<p class="sect">Progress</p><p class="tiny">Saved in this browser. Copy a backup ` +
      `now and then, and paste it into Notes; Restore brings it back.</p>` +
      `<div class="btnrow"><button class="btn" id="exp">Copy backup</button>` +
      `<button class="btn" id="imp">Restore</button></div>` +
      `<div class="btnrow" style="margin-top:10px"><button class="btn" id="rst">Reset progress</button></div>`;
    let dir = localStorage.getItem('esp.dir') || 'es';
    const mark = () => {
      $('#d1').classList.toggle('primary', dir === 'es');
      $('#d2').classList.toggle('primary', dir === 'en');
    };
    mark();
    $('#d1').onclick = () => { dir = 'es'; localStorage.setItem('esp.dir', dir); mark(); };
    $('#d2').onclick = () => { dir = 'en'; localStorage.setItem('esp.dir', dir); mark(); };
    $('#go').onclick = () => {
      if (!due.length) { alert("Nothing due. You've done today's words."); return; }
      // reviews shuffled first, then the new words in order
      const shuffled = rev.slice().sort(() => Math.random() - 0.5);
      session = { queue: [...shuffled, ...fresh], i: 0, shown: false, dir };
      render();
    };
    $('#exp').onclick = async () => {
      const txt = JSON.stringify(prog);
      try { await navigator.clipboard.writeText(txt); alert('Backup copied. Paste it somewhere safe.'); }
      catch (_) { prompt('Copy this backup:', txt); }
    };
    $('#imp').onclick = () => {
      const txt = prompt('Paste a backup:');
      if (!txt) return;
      try {
        const data = JSON.parse(txt);
        if (typeof data !== 'object' || Array.isArray(data)) throw 0;
        prog = data; save(); alert('Restored.'); render();
      } catch (_) { alert("That doesn't look like a backup."); }
    };
    $('#rst').onclick = () => {
      if (confirm('Erase all practice progress?')) { prog = {}; save(); render(); }
    };
    return;
  }
  const c = session.queue[session.i];
  if (!c) { session = null; return render(); }
  const front = session.dir === 'es' ? c.es : c.en.replace(/; /g, ' · ');
  const back = session.dir === 'es' ? c.en.replace(/; /g, ' · ') : c.es;
  const ex = (c.ex || [])[0];
  m.innerHTML =
    `<p class="stats">${session.i + 1} of ${session.queue.length}</p>` +
    `<div class="card"><div class="prompt">${esc(front)}</div>` +
    `<div class="promptsub">unit ${c.unitNum} · ${esc(c.unit)}</div>` +
    (session.shown
      ? `<div class="answer">${esc(back)}` +
        (c.he ? `<span class="t" dir="rtl" lang="he">${esc(c.he)}</span>` : '') +
        (ex ? `<span class="t">${esc(ex.es)} — ${esc(ex.en)}</span>` : '') + '</div>'
      : '') +
    '</div>' +
    (session.shown
      ? `<div class="btnrow"><button class="btn" id="again">Again</button>` +
        `<button class="btn primary" id="good">Got it</button></div>`
      : `<div class="btnrow"><button class="btn primary" id="show">Show answer</button></div>`);
  if (session.shown) {
    $('#again').onclick = () => grade(c, false);
    $('#good').onclick = () => grade(c, true);
  } else {
    $('#show').onclick = () => { session.shown = true; render(); };
  }
}
function grade(c, ok) {
  const p = prog[c.id] || { box: 0, intro: today() };
  p.box = ok ? Math.min(p.box + 1, BOX_DAYS.length - 1) : 0;
  p.due = today() + BOX_DAYS[p.box];
  prog[c.id] = p; save();
  session.i++; session.shown = false; render();
}

/* ---------- shell ------------------------------------------------------ */
const TABS = [['browse', 'Browse', '☰'], ['search', 'Search', '⌕'],
              ['practice', 'Practice', '◉'], ['plates', 'Plates', '◫']];
function render() {
  const showBack = tab === 'browse' && openUnit !== null;
  $('#back').hidden = !showBack;
  $('#title').innerHTML = showBack
    ? esc(openUnit === 'G' ? D.grammar.title
        : openUnit === 'A' ? 'Appendix'
        : D.units.find(u => u.id === openUnit).title)
    : 'Español para lectura <small>1003 words</small>';
  $('#searchwrap').hidden = tab !== 'search';
  ({ browse: viewBrowse, search: viewSearch, practice: viewPractice, plates: viewPlates })[tab]();
  document.querySelectorAll('nav button').forEach(b =>
    b.setAttribute('aria-current', b.dataset.t === tab));
  if (tab === 'search') $('#q').focus();
}
document.querySelectorAll('nav button').forEach(b => b.onclick = () => {
  tab = b.dataset.t; session = null; render();
  window.scrollTo(0, 0);
});
$('#back').onclick = () => { openUnit = null; render(); window.scrollTo(0, 0); };
$('#q').oninput = () => viewSearch();
render();
"""


def main():
    nav = "".join(
        f'<button data-t="{t}"><span class="ic">{ic}</span>{label}</button>'
        for t, label, ic in [("browse", "Browse", "&#9776;"), ("search", "Search", "&#8981;"),
                             ("practice", "Practice", "&#9673;"), ("plates", "Plates", "&#9707;")]
    )
    html = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#fbfaf8" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#15171a" media="(prefers-color-scheme: dark)">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
        '<meta name="apple-mobile-web-app-title" content="Español">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="apple-touch-icon" href="icon-180.png">\n'
        '<title>Español para lectura</title>\n'
        f'<style>{CSS}</style>\n</head>\n<body>\n'
        '<header><div class="hrow">'
        '<button class="back" id="back" hidden>&#8249; Units</button>'
        '<h1 id="title"></h1></div>'
        '<div id="searchwrap" hidden><input id="q" type="search" '
        'placeholder="Search words, meanings, sentences" autocomplete="off" '
        'autocapitalize="off" spellcheck="false" enterkeyhint="search"></div>'
        '</header>\n<main id="view"></main>\n'
        f'<nav>{nav}</nav>\n'
        '<script>window.__DATA__=' +
        json.dumps(DATA, ensure_ascii=False, separators=(",", ":")) +
        ';</script>\n'
        f'<script>{JS}</script>\n</body>\n</html>\n'
    )
    out = ROOT / "docs" / "index.html"
    out.write_text(html, encoding="utf-8")

    manifest = {
        "name": "Español para lectura", "short_name": "Español",
        "start_url": ".", "display": "standalone",
        "background_color": "#fbfaf8", "theme_color": "#fbfaf8",
        "icons": [{"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }
    (ROOT / "docs" / "manifest.webmanifest").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"docs/index.html  {out.stat().st_size/1024:.0f} KB  "
          f"({len(ALL_COUNT)} entries)" if False else
          f"docs/index.html  {out.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
