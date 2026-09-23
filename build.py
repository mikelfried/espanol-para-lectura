#!/usr/bin/env python3
"""Build a printable A4 PDF vocabulary booklet from the JSON data in data/.

Pipeline: JSON -> HTML (paged-media CSS) -> headless Chrome --print-to-pdf.
Chrome is used because it handles Hebrew RTL and Spanish diacritics natively
with system fonts, which the pure-Python PDF libraries do not.
"""

import html
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = ROOT / "out"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PRONOUNS = ["yo", "tú", "él/ella", "nosotros", "ellos/ustedes"]


def e(s):
    return html.escape(str(s))


def he(s):
    """Hebrew gloss, marked RTL so mixed punctuation renders correctly."""
    return f'<span class="he" dir="rtl" lang="he">{e(s)}</span>'


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def units():
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((DATA / "units").glob("*.json"))]


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def render_entry(n, entry):
    parts = [f'<div class="entry">']
    pos = f'<span class="pos">{e(entry["pos"])}</span>' if entry.get("pos") else ""
    parts.append(f'<div class="hd">'
                 f'<span class="es">{e(entry["es"])}</span>{pos}</div>')
    parts.append(f'<div class="en">{e(entry["en"])}</div>')
    if entry.get("he"):
        parts.append(f'<div class="hel">{he(entry["he"])}</div>')
    if entry.get("note"):
        parts.append(f'<div class="note">{e(entry["note"])}</div>')
    if entry.get("warn"):
        parts.append(f'<div class="warn"><b>Watch out</b>{e(entry["warn"])}</div>')
    if entry.get("conj"):
        c = entry["conj"]
        cells = " ".join(
            f'<span class="cf"><i>{e(p)}</i>{e(f)}</span>'
            for p, f in zip(PRONOUNS, c["forms"])
        )
        parts.append(
            f'<div class="conj"><span class="clab">{e(c.get("label", "pres."))}</span>{cells}</div>'
        )
    for ex in entry.get("ex", []):
        tag = f'<span class="tag">{e(ex["tag"])}</span>' if ex.get("tag") else ""
        parts.append(
            f'<div class="ex"><div class="exs">{tag}{e(ex["es"])}</div>'
            f'<div class="exe">{e(ex["en"])}</div></div>'
        )
    parts.append("</div>")
    return "".join(parts)


def unit_fs(u):
    """Fallback size, used only if the measuring pass cannot run."""
    return 8.0


# A4 minus @page margins, minus the column gap, split in two.
COL_W_MM = (210 - 9 - 9 - 7) / 2
# Usable column length on one page: two columns of the text height, less the
# unit heading and intro.
# 0.87 accounts for space lost to column balancing and unbreakable entries.
PAGE_COL_MM = 2 * (297 - 10 - 10 - 19) * 0.87
REF_FS = 10.0
FS_MAX, FS_MIN = 8.9, 7.6


def measure_units(us):
    """Lay each unit out in a single column of the real width and measure it.

    Height scales with the square of the font size (a smaller face fits more
    characters per line *and* more lines), so one measurement at a reference
    size is enough to solve for the size that fills exactly one page.
    """
    blocks = []
    for u in us:
        body = "".join(render_entry(i + 1, en) for i, en in enumerate(u["entries"]))
        blocks.append(
            f'<div class="cols m" id="{e(u["id"])}" '
            f'style="--fs: {REF_FS}pt">{body}</div>'
        )
    doc = (f'<!DOCTYPE html><meta charset="utf-8"><style>{CSS}\n'
           f'.m {{ column-count: 1; width: {COL_W_MM}mm; }}</style>'
           + "".join(blocks) +
           '<script>document.title = JSON.stringify(Object.fromEntries('
           '[...document.querySelectorAll(".m")].map(d => '
           '[d.id, d.getBoundingClientRect().height])));</script>')

    path = OUT / ".measure.html"
    path.write_text(doc, encoding="utf-8")
    dom = run_chrome(["--dump-dom", path.as_uri()], capture=True,
                     profile="measure")
    path.unlink(missing_ok=True)

    m = re.search(r"<title>(.*?)</title>", dom, re.S)
    if not m:
        return {}
    px = json.loads(html.unescape(m.group(1)))
    sizes = {}
    for uid, height_px in px.items():
        mm = height_px * 25.4 / 96          # CSS px -> mm
        fs = REF_FS * (PAGE_COL_MM / mm) ** 0.5 if mm else FS_MAX
        sizes[uid] = round(max(FS_MIN, min(FS_MAX, fs)), 2)
    return sizes


def render_units(us, sizes):
    out = []
    n = 0
    for u in us:
        fs = sizes.get(u["id"], unit_fs(u))
        out.append(f'<section class="unit" data-run="{e(u["title"])}">')
        num = int(u["id"][1:])
        out.append(f'<h2><span class="ut">Unit {num}</span>'
                   f'<span class="utt">{e(u["title"])}</span></h2>')
        if u.get("intro"):
            out.append(f'<p class="intro">{e(u["intro"])}</p>')
        out.append(f'<div class="cols" style="--fs: {fs}pt">')
        for entry in u["entries"]:
            n += 1
            out.append(render_entry(n, entry))
        out.append("</div></section>")
    return "".join(out), n


def plates():
    d = DATA / "plates"
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(d.glob("*.json"))] if d.exists() else []


def scope_svg(svg, pid):
    """Confine a plate's <style> rules to that plate.

    A <style> block inside inline SVG is not scoped — it applies to the whole
    document. Two plates that both use a class named .cap or .sw silently
    overwrite each other, and a CSS `fill` beats a presentation attribute, so a
    collision can blank out artwork. Tag the svg with a per-plate class and
    prefix every selector with it.
    """
    cls = f"pl-{pid}"
    svg = re.sub(r"<svg\b", f'<svg class="{cls}"', svg, count=1)

    def fix(m):
        rules = []
        for rule in m.group(1).split("}"):
            if "{" not in rule:
                continue
            sel, decl = rule.split("{", 1)
            sels = ",".join(f".{cls} {s.strip()}"
                            for s in sel.split(",") if s.strip())
            if sels:
                rules.append(f"{sels}{{{decl}}}")
        return "<style>" + "".join(rules) + "</style>"

    return re.sub(r"<style>(.*?)</style>", fix, svg, flags=re.S)


def render_plate(p):
    """A numbered diagram, then the same diagram again with the key removed.

    The second copy is the study half: the numbers are still there, so you name
    each one from memory instead of reading it.
    """
    legend = "".join(
        f'<li><span class="pn">{i["n"]}</span>'
        f'<span class="pes">{e(i["es"])}</span>'
        f'<span class="pen">{e(i["en"])}</span></li>'
        for i in p["items"]
    )
    pnum = int(p["id"][1:])
    head = (f'<h2><span class="ut">Plate {pnum}</span>'
            f'<span class="utt">{e(p["title"])}</span></h2>')
    svg = scope_svg(p["svg"], p["id"])
    intro = f'<p class="intro">{e(p["intro"])}</p>' if p.get("intro") else ""

    return (
        f'<section class="unit plate" data-run="{e(p["title"])}">'
        f'{head}{intro}'
        f'<div class="pfig">{svg}</div>'
        f'<ol class="plegend">{legend}</ol>'
        '</section>'
        f'<section class="unit plate ptesting" data-run="{e(p["title"])}">'
        f'<h2><span class="ut">Plate {pnum}</span>'
        f'<span class="utt">{e(p["title"])}</span>'
        f'<span class="ptest">name each one</span></h2>'
        f'<div class="pfig">{svg}</div>'
        '</section>'
    )


def render_grammar(g):
    out = ['<section class="unit grammar" data-run="Function words">',
           f'<h2><span class="ut">Before you begin</span>'
           f'<span class="utt">{e(g["title"])}</span></h2>',
           f'<p class="intro">{e(g["intro"])}</p>', '<div class="gcols">']
    for item in g["items"]:
        out.append('<div class="gitem">')
        out.append(f'<div class="ghd"><span class="es">{e(item["word"])}</span>'
                   f'<span class="en">{e(item["gloss"])}</span></div>')
        if item.get("he"):
            out.append(f'<div class="hel">{he(item["he"])}</div>')
        for sense in item["senses"]:
            # The examples must sit inside .sbody. As siblings of .slab they
            # become grid items and get placed in the narrow label column.
            out.append(f'<div class="sense"><div class="slab">{e(sense["label"])}</div>'
                       f'<div class="sbody"><div>{e(sense["text"])}</div>')
            for ex in sense.get("ex", []):
                out.append(f'<div class="ex"><div class="exs">{e(ex["es"])}</div>'
                           f'<div class="exe">{e(ex["en"])}</div></div>')
            out.append("</div></div>")
        if item.get("pitfall"):
            out.append(f'<div class="pitfall"><b>Watch out</b>{e(item["pitfall"])}</div>')
        out.append("</div>")
    out.append("</div></section>")
    return "".join(out)


def render_cognates(c):
    out = ['<section class="unit appendix" data-run="Words you already know">',
           f'<h2><span class="ut">Appendix</span>'
           f'<span class="utt">{e(c["title"]).replace("Appendix A · ", "")}</span></h2>',
           f'<p class="intro">{e(c["intro"])}</p>',
           '<div class="cogcols">']
    for grp in c["groups"]:
        out.append(f'<div class="coggrp"><h3>{e(grp["label"])}</h3><ul>')
        for w in grp["words"]:
            gloss = f' <i>{e(w["en"])}</i>' if w.get("en") else ""
            out.append(f'<li>{e(w["es"])}{gloss}</li>')
        out.append("</ul></div>")
    out.append("</div></section>")
    return "".join(out)


def render_toc(g, us, cog, folios=None):
    folios = folios or {}

    def ref(title):
        n = folios.get(title)
        return f' <span class="tp">{n}</span>' if n else ''

    rows = [f'<li><span class="tn">&mdash;</span> {e(g["title"])}{ref(g["title"])}</li>']
    for u in us:
        rows.append(f'<li><span class="tn">{int(u["id"][1:])}</span> {e(u["title"])}'
                    f'{ref(u["title"])}</li>')
    rows.append('<li><span class="tn">&mdash;</span> Appendix: words you already '
                f'know{ref(cog["title"].replace("Appendix A · ", ""))}</li>')
    return ('<section class="toc"><h2>Contents</h2>'
            '<ol>' + "".join(rows) + "</ol></section>")


CSS = """
@page { size: A4; margin: 10mm 9mm 10mm 9mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  margin: 0; background: #fff;
  font-family: "Charter", "Georgia", "Times New Roman", serif;
  font-size: 8.2pt; line-height: 1.26; color: #14161a;
}
.he, [lang="he"] {
  font-family: "Arial Hebrew", "Narkisim", "Times New Roman", serif;
  font-size: 1.05em;
}

/* ---- cover ---- */
.cover { height: 262mm; display: flex; flex-direction: column;
         page-break-after: always; padding-top: 52mm; }
.cover h1 { font-size: 30pt; font-weight: 400; margin: 0 0 3mm;
            letter-spacing: -0.3pt; }
.cover h1::after { content: ""; display: block; width: 46mm; height: 0;
                   border-top: .8pt solid #1d2229; margin: 4mm 0 0; }
.cover .sub { font-size: 10pt; color: #55606e; margin: 4mm 0 auto;
              max-width: 112mm; line-height: 1.45; }
.cover .how { max-width: 112mm; font-size: 8.5pt; line-height: 1.45;
              color: #2b313a; border-top: .5pt solid #c9ced6; padding-top: 4mm; }
.cover .how p { margin: 0 0 2.2mm; }

/* ---- contents ---- */
.toc { page-break-after: always; }
.toc h2 { font-size: 9pt; font-weight: 400; letter-spacing: 1.5pt; margin: 0 0 5mm;
          text-transform: uppercase; border-bottom: .6pt solid #1d2229;
          padding-bottom: 2mm; }
.toc ol { list-style: none; padding: 0; margin: 0; column-count: 2; column-gap: 8mm; }
.toc li { margin-bottom: 1.5mm; break-inside: avoid; font-size: 8.8pt;
          padding-right: 2mm; }
.tn { display: inline-block; width: 7mm; color: #8a919c;
      text-align: right; margin-right: 2mm; }
.tc { color: #b3bac2; font-size: 7pt; }
.tp { float: right; color: #6b7280; }

/* ---- unit ---- */
.unit { page-break-before: always; }
.unit h2 { font-size: 13pt; font-weight: 400; margin: 0 0 2.4mm;
           border-bottom: .6pt solid #1d2229; padding-bottom: 1.6mm; }
.ut { display: block; font-size: 7.3pt; font-weight: 400; letter-spacing: 1.3pt;
      text-transform: uppercase; color: #8a919c; margin-bottom: .8mm; }
.utt { font-weight: 600; }
.intro { margin: 0 0 2.6mm; font-size: 7.8pt; line-height: 1.3; color: #4a525e;
         font-style: italic; }
.cols { column-count: 2; column-gap: 7mm; column-rule: 0.3pt solid #e2e6ea;
        font-size: var(--fs, 8.8pt); }

/* ---- entry ----
   Sized in em against the unit's --fs, so a dense unit scales down as a whole
   without the proportions drifting. build.py computes --fs per unit. */
.entry { break-inside: avoid; margin-bottom: 0.8em; }
.hd { display: flex; align-items: baseline; gap: 0.18em; }
.num { font-size: 0.74em; color: #aeb5be; min-width: 1.8em; }
.hd .es { font-weight: 700; font-size: 1.14em; }
.pos { font-size: 0.76em; color: #949ba6; font-style: italic; }
.en { margin-left: 1.6em; }
.hel { margin-left: 1.6em; color: #2b313a; }
.note { margin-left: 1.6em; font-size: 0.86em; line-height: 1.3; color: #626b78;
        margin-bottom: 0.1em; }
.conj { margin: 0.24em 0 0.24em 1.6em; font-size: 0.8em; background: #f2f4f7;
        border-left: 1.2pt solid #bcc3cc; padding: 0.2em 0.42em; line-height: 1.45;
        overflow-wrap: anywhere; }
.clab { color: #7a828e; font-style: italic; margin-right: 0.36em; }
.cf { margin-right: 0.58em; white-space: nowrap; }
.cf i { color: #a0a7b1; font-size: 0.86em; margin-right: 0.15em; }
.ex { margin: 0.26em 0 0 1.6em; }
.exs::before { content: "\\2022\\00a0"; color: #b4bac2; }
.exe { color: #6b7280; font-size: 0.89em; margin-left: 0.65em; line-height: 1.2; }
.tag { font-size: 0.8em; color: #6f7784; font-style: italic;
       margin-right: 0.4em; white-space: nowrap; }

/* ---- warnings on individual words ---- */
.warn { margin: .45em 0 .45em 1.6em; font-size: 0.86em; line-height: 1.32;
        color: #14161a; background: #e4e2db; border: .5pt solid #3f3f3b;
        border-left: 2.4pt solid #1d2229; padding: .3em .5em; }
.warn b { display: inline-block; background: #1d2229; color: #fff;
          font-size: .78em; font-weight: 700; letter-spacing: .9pt;
          text-transform: uppercase; padding: .08em .4em .12em;
          margin-right: .5em; }

/* ---- diagram plates ---- */
.plate .pfig { text-align: center; margin: 3mm 0 4mm; }
.plate svg { width: 100%; max-height: 165mm; }
.plate svg text { font-family: "Charter", "Georgia", serif; }
/* The test copy keeps the numbers and drops every name. */
.ptesting .lab { visibility: hidden; }
.ptest { float: right; font-size: 7.6pt; font-style: italic; font-weight: 400;
         color: #8a919c; letter-spacing: 0; text-transform: none; }
.plegend { list-style: none; margin: 0; padding: 0; column-count: 3;
           column-gap: 7mm; font-size: 8.6pt; }
.plegend li { break-inside: avoid; margin-bottom: 1.3mm;
              padding-left: 5.9mm; text-indent: -5.9mm; }
.pn { display: inline-block; min-width: 4.6mm; text-align: right;
      font-size: 7.2pt; color: #7a828e; margin-right: 1.3mm; }
.pes { font-weight: 700; margin-right: 1.1mm; }
.pen { color: #6b7280; font-size: 0.92em; }

/* ---- grammar section ---- */
.grammar .gcols { column-count: 2; column-gap: 7mm; column-rule: 0.3pt solid #e2e6ea; }
.gitem { break-inside: avoid; margin-bottom: 3.4mm; }
.ghd { display: flex; align-items: baseline; gap: 2mm; border-bottom: 0.3pt solid #dfe3e8;
       padding-bottom: 0.7mm; margin-bottom: 1mm; }
.ghd .es { font-weight: 700; font-size: 11pt; }
.ghd .en { margin-left: 0; color: #4a525e; font-size: 8pt; }
.grammar .hel { margin-left: 0; margin-bottom: 1mm; }
.sense { margin: 0 0 1.2mm 0; display: grid; grid-template-columns: 19mm 1fr; gap: 2mm; }
.slab { font-size: 7pt; line-height: 1.2; color: #7a828e; font-style: italic;
        text-align: right; }
.sbody { font-size: 8.1pt; }
.sense .ex { margin-left: 0; }
.pitfall { font-size: 7.6pt; line-height: 1.32; color: #14161a;
           background: #e4e2db; border: .5pt solid #3f3f3b;
           border-left: 2.4pt solid #1d2229; padding: 1mm 1.4mm;
           margin-top: 1.4mm; }
.pitfall b { display: inline-block; background: #1d2229; color: #fff;
             font-size: .8em; font-weight: 700; letter-spacing: .9pt;
             text-transform: uppercase; padding: .08em .4em .12em;
             margin-right: .5em; }

/* ---- cognate appendix ---- */
.appendix .cogcols { column-count: 4; column-gap: 6mm;
                     column-rule: .3pt solid #e4e8ec; }
.coggrp { break-inside: avoid; margin-bottom: 3mm; }
.coggrp h3 { font-size: 7.4pt; margin: 0 0 0.8mm; color: #7a828e;
             text-transform: uppercase; letter-spacing: 0.3pt; }
.coggrp ul { list-style: none; margin: 0; padding: 0; font-size: 8pt; line-height: 1.24; }
.coggrp li { margin-bottom: 0.3mm; }
.coggrp i { color: #8a919c; font-size: 6.9pt; }
"""


def build_html(g, us, cog, meta, sizes, pls, folios=None):
    body, count = render_units(us, sizes)
    doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>{e(meta['title'])}</title><style>{CSS}</style></head><body>
<div class="cover">
  <h1>{e(meta['title'])}</h1>
  <div class="sub">{e(meta['subtitle'])}</div>
  <div class="how">{''.join(f'<p>{e(p)}</p>' for p in meta['how'])}</div>
</div>
{render_toc(g, us, cog, folios)}
{render_grammar(g)}
{body}
{''.join(render_plate(p) for p in pls)}
{render_cognates(cog)}
</body></html>"""
    return doc, count


PLATE_NAME_CLASSES = ("cap", "rm", "sm", "sub", "es", "en")


def lint_plates(pls):
    """Any text in a plate that names something must carry class="lab".

    The self-test page hides exactly the `lab` elements. A label without it
    survives onto that page and gives the answer away, which is silent and easy
    to miss by eye.
    """
    problems = []
    for p in pls:
        for tag in re.findall(r"<text[^>]*>", p["svg"]):
            m = re.search(r'class="([^"]*)"', tag)
            if not m:
                continue
            classes = m.group(1).split()
            if any(c in PLATE_NAME_CLASSES for c in classes) and "lab" not in classes:
                problems.append(f'{p["id"]}: name-bearing text without lab: {tag}')
    return problems


def lint(us):
    """Every distinct sense in the gloss must be demonstrated by its own tagged
    sentence. Senses are separated by ';' in the `en` field."""
    problems = []
    for u in us:
        for entry in u["entries"]:
            senses = [s.strip() for s in entry["en"].split(";") if s.strip()]
            exs = entry.get("ex", [])
            if len(senses) > 1:
                tagged = [x for x in exs if x.get("tag")]
                if len(tagged) < len(senses):
                    problems.append(
                        f'{u["id"]} {entry["es"]}: {len(senses)} senses, '
                        f'{len(tagged)} tagged sentences'
                    )
            if not exs:
                problems.append(f'{u["id"]} {entry["es"]}: no example sentence')
    return problems


def run_chrome(args, capture=False, wait_for=None, profile="pdf"):
    """Run headless Chrome. Returns stdout when `capture` is set.

    The profile is reused between runs: recreating it costs ~40s of first-run
    setup every build. TMPDIR is redirected into it because Chrome's
    process-singleton socket lands there and aborts the run if it can't bind.
    """
    tmp = OUT / f".chrome-{profile}"
    tmp.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "TMPDIR": str(tmp)}
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={tmp}",
        "--no-first-run", "--no-default-browser-check",
        "--disable-extensions", "--disable-sync", "--disable-default-apps",
        "--disable-background-networking", "--disable-component-update",
        "--disable-client-side-phishing-detection", "--metrics-recording-only",
        "--virtual-time-budget=4000",
    ] + args

    if capture:
        # Chrome dumps the DOM and then hangs instead of exiting, so read until
        # the document is complete rather than waiting for the process to end.
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, env=env)
        chunks, deadline = [], time.time() + 60
        os.set_blocking(proc.stdout.fileno(), False)
        while time.time() < deadline:
            chunk = proc.stdout.read()
            if chunk:
                chunks.append(chunk)
                if b"</html>" in chunk:
                    break
            elif proc.poll() is not None:
                break
            else:
                time.sleep(0.05)
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=10)
        return b"".join(chunks).decode("utf-8", "replace")

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, env=env)
    # Chrome reliably writes the file but does not reliably exit afterwards, so
    # wait for it to stop growing and then kill it rather than join it.
    deadline, last, stable = time.time() + 60, -1, 0
    while time.time() < deadline:
        if proc.poll() is not None:
            break
        size = wait_for.stat().st_size if wait_for.exists() else -1
        stable = stable + 1 if size > 0 and size == last else 0
        last = size
        if stable >= 3:
            break
        time.sleep(0.25)
    if proc.poll() is None:
        proc.kill()
        proc.wait(timeout=10)
    return ""



# --------------------------------------------------------------------------
# compact edition
# --------------------------------------------------------------------------
# A review sheet, not a teaching book. It keeps every headword and gloss, and
# spends its remaining space only where meaning is genuinely at stake:
# multi-sense entries, false friends and the vulgarity warnings. Measured
# shares of the full book's text: glosses 18%, example sentences 47%, usage
# notes 30%. Dropping notes and most sentences is therefore most of the saving;
# letting units flow instead of starting each on a new page is the rest.

COMPACT_MAX_EX = 2       # sentences kept, only on entries that earn them


def needs_examples(entry):
    return len(entry["en"].split(";")) > 1 or entry.get("warn")


def render_entry_compact(n, entry):
    p = [f'<div class="entry">']
    pos = f'<span class="pos">{e(entry["pos"])}</span>' if entry.get("pos") else ""
    yo = ""
    if entry.get("conj"):
        # the yo form is where the irregularity lives; the rest is predictable
        yo = f'<span class="yo">{e(entry["conj"]["forms"][0])}</span>'
    p.append(f'<div class="hd"><span class="num">{n}</span>'
             f'<span class="es">{e(entry["es"])}</span>{pos}{yo}</div>')

    gloss = entry["en"].replace("; ", " · ")
    heb = f' {he(entry["he"])}' if entry.get("he") else ""
    p.append(f'<div class="en">{e(gloss)}{heb}</div>')

    if entry.get("warn"):
        p.append(f'<div class="warn"><b>Watch out</b>{e(entry["warn"])}</div>')

    # 19 pages without this; the budget is 25, so every entry can afford one
    # example, and the ambiguous ones two.
    keep = COMPACT_MAX_EX if needs_examples(entry) else 1
    if True:
        for ex in entry.get("ex", [])[:keep]:
            tag = f'<span class="tag">{e(ex["tag"])}</span>' if ex.get("tag") else ""
            p.append(f'<div class="ex">{tag}{e(ex["es"])}'
                     f'<span class="exe"> {e(ex["en"])}</span></div>')
    p.append("</div>")
    return "".join(p)


def render_units_compact(us):
    """One continuous multi-column flow. In the full book every unit starts a
    new page, which wastes up to half a page fifty times over."""
    out = []
    n = 0
    for u in us:
        out.append(f'<h3 class="cuh"><span class="cun">Unit {int(u["id"][1:])}</span>'
                   f'{e(u["title"])}</h3>')
        for entry in u["entries"]:
            n += 1
            out.append(render_entry_compact(n, entry))
    return "".join(out), n


def render_grammar_compact(g):
    out = [f'<h3 class="cuh"><span class="cun">Before you begin</span>'
           f'{e(g["title"])}</h3>']
    for item in g["items"]:
        out.append('<div class="entry">')
        out.append(f'<div class="hd"><span class="es">{e(item["word"])}</span></div>')
        heb = f' {he(item["he"])}' if item.get("he") else ""
        out.append(f'<div class="en">{e(item["gloss"])}{heb}</div>')
        for sense in item["senses"]:
            ex = sense.get("ex") or []
            first = f' <i>{e(ex[0]["es"])}</i>' if ex else ""
            out.append(f'<div class="ex"><span class="tag">{e(sense["label"])}</span>'
                       f'{e(sense["text"])}{first}</div>')
        if item.get("pitfall"):
            out.append(f'<div class="warn"><b>Watch out</b>{e(item["pitfall"])}</div>')
        out.append("</div>")
    return "".join(out)


COMPACT_CSS = """
@page { size: A4; margin: 9mm 8mm 13mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; background: #fff; font-family: "Charter","Georgia",serif;
       font-size: 8.15pt; line-height: 1.22; color: #14161a; }
.he, [lang="he"] { font-family: "Arial Hebrew","Narkisim",serif; font-size: 1.02em; }
h1 { font-size: 15pt; margin: 0 0 1mm; }
.sub { font-size: 8.4pt; color: #55606e; margin-bottom: 3mm; }
.hdr { border-bottom: 1pt solid #14161a; padding-bottom: 2mm; margin-bottom: 3mm; }
.ccols { column-count: 3; column-gap: 5.5mm; column-rule: .3pt solid #e4e8ec; }
.cuh { font-size: 8.4pt; font-weight: 600; margin: 3mm 0 1.3mm;
       padding-bottom: .6mm; border-bottom: .6pt solid #1d2229;
       break-after: avoid; break-inside: avoid; color: #1d2229; }
.cun { display: block; font-size: 6.5pt; font-weight: 400; letter-spacing: 1.1pt;
       text-transform: uppercase; color: #8a919c; margin-bottom: .3mm; }
.cuh:first-child { margin-top: 0; }
.entry { break-inside: avoid; margin-bottom: 1.15mm; }
.hd { display: flex; align-items: baseline; gap: .16em; flex-wrap: wrap; }
.num { font-size: .72em; color: #b3bac2; min-width: 1.9em; }
.hd .es { font-weight: 700; font-size: 1.06em; }
.pos { font-size: .74em; color: #9aa1ab; font-style: italic; }
.yo { font-size: .74em; color: #6f7784; }
.yo::before { content: "("; } .yo::after { content: ")"; }
.en { margin-left: 1.9em; }
.ex { margin-left: 1.9em; font-size: .93em; color: #3f4650; text-indent: -.7em;
      padding-left: .7em; }
.ex::before { content: "\\2022\\00a0"; color: #b4bac2; }
.exe { color: #7e8691; }
.tag { font-size: .76em; color: #6f7784; font-style: italic;
       margin-right: .45em; white-space: nowrap; }
.warn { margin: .5mm 0 .5mm 1.9em; font-size: .9em; line-height: 1.28;
        color: #14161a; background: #e4e2db; border: .5pt solid #3f3f3b;
        border-left: 2pt solid #1d2229; padding: .22em .42em; }
.warn b { display: inline-block; background: #1d2229; color: #fff;
          font-size: .78em; font-weight: 700; letter-spacing: .8pt;
          text-transform: uppercase; padding: .06em .35em .1em;
          margin-right: .45em; }
.capp { break-before: page; }
.capp .cogcols { column-count: 4; column-gap: 6mm;
                 column-rule: .3pt solid #e4e8ec; }
.coggrp { break-inside: avoid; margin-bottom: 2mm; }
.coggrp h4 { font-size: 7.1pt; margin: 0 0 .6mm; color: #7a828e;
             text-transform: uppercase; letter-spacing: .3pt; }
.coggrp ul { list-style: none; margin: 0; padding: 0; font-size: 7.5pt; }
.coggrp i { color: #8a919c; font-size: .9em; }
"""


def render_cognates_compact(c):
    out = [f'<h3 class="cuh"><span class="cun">Appendix</span>'
           f'{e(c["title"]).replace("Appendix A · ", "")}</h3>',
           '<div class="cogcols">']
    for grp in c["groups"]:
        out.append(f'<div class="coggrp"><h4>{e(grp["label"])}</h4><ul>')
        for w in grp["words"]:
            gloss = f' <i>{e(w["en"])}</i>' if w.get("en") else ""
            out.append(f'<li>{e(w["es"])}{gloss}</li>')
        out.append("</ul></div>")
    out.append("</div>")
    return "".join(out)


def build_compact(g, us, cog, meta):
    body, count = render_units_compact(us)
    doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><title>{e(meta['title'])} — compacto</title>
<style>{COMPACT_CSS}</style></head><body>
<div class="hdr"><h1>{e(meta['title'])} &middot; edición compacta</h1>
<div class="sub">{count} words in 50 themed units. Every entry keeps its gloss, one
example sentence, the Hebrew where English underdetermines, and the irregular yo
form; entries with more than one sense keep a sentence for each. The usage notes,
the remaining sentences and the seven plates are in the main edition.</div></div>
<div class="ccols">{render_grammar_compact(g)}{body}</div>
<div class="capp">{render_cognates_compact(cog)}</div>
</body></html>"""
    return doc, count



# --------------------------------------------------------------------------
# folios and running heads
# --------------------------------------------------------------------------
# Chrome does not support CSS margin boxes, so page numbers cannot be printed
# in the same pass as the text. They are stamped afterwards from a second,
# numbers-only PDF merged on top. The same pass learns which page each section
# begins on, which is what lets the contents carry real page references.

# title page and contents carry no folio in the full edition;
# the compact edition starts numbering at its first page


def section_starts(pdf_path, titles, front):
    """First page on which each section title appears, skipping the contents."""
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    found, pages = {}, []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    for i, text in enumerate(pages):
        if i < front:
            continue
        flat = " ".join(text.split())
        for t in titles:
            if t not in found and " ".join(t.split()) in flat:
                found[t] = i
    return found, len(pages)


def stamp_folios(pdf_path, heads, total, front):
    """Merge a numbers-and-running-heads layer onto every body page."""
    from pypdf import PdfReader, PdfWriter
    cells = []
    for i in range(total):
        if i < front:
            cells.append('<div class="p"></div>')
            continue
        head = heads.get(i, "")
        cells.append(f'<div class="p"><div class="f">'
                     f'<span class="h">{e(head)}</span>'
                     f'<span class="n">{i - front + 1}</span></div></div>')
    doc = ('<!DOCTYPE html><meta charset="utf-8"><style>'
           '@page { size: A4; margin: 0; }'
           'body { margin: 0; }'
           '.p { width: 210mm; height: 296.6mm; position: relative;'
           '     page-break-after: always; }'
           '.f { position: absolute; bottom: 5.4mm; left: 9mm; right: 9mm;'
           '     display: flex; justify-content: space-between; align-items: baseline;'
           '     font-family: "Charter","Georgia",serif; font-size: 7.4pt;'
           '     color: #8a919c; }'
           '.h { font-style: italic; }'
           '.n { font-variant-numeric: lining-nums; }'
           '</style>' + "".join(cells))

    layer_html = OUT / ".folios.html"
    layer_pdf = OUT / ".folios.pdf"
    layer_html.write_text(doc, encoding="utf-8")
    if layer_pdf.exists():
        layer_pdf.unlink()
    run_chrome(["--no-pdf-header-footer", f"--print-to-pdf={layer_pdf}",
                layer_html.as_uri()], wait_for=layer_pdf, profile="folios")

    layer = PdfReader(str(layer_pdf))
    if len(layer.pages) != total:
        print(f"  ! folio layer has {len(layer.pages)} pages, body has {total};"
              f" skipping stamp")
        return False
    body = PdfReader(str(pdf_path))
    out = PdfWriter()
    for page, over in zip(body.pages, layer.pages):
        page.merge_page(over)
        out.add_page(page)
    with open(pdf_path, "wb") as fh:
        out.write(fh)
    layer_html.unlink(missing_ok=True)
    layer_pdf.unlink(missing_ok=True)
    return True


def main():
    OUT.mkdir(exist_ok=True)
    g, cog, meta = load("grammar.json"), load("cognates.json"), load("meta.json")
    us = units()

    problems = lint(us) + lint_plates(plates())
    if problems:
        print("sense coverage:")
        for p in problems:
            print("  ! " + p)

    have_chrome = Path(CHROME).exists()
    compact = "--compact" in sys.argv
    sizes = {}
    if compact:
        doc, count = build_compact(g, us, cog, meta)
    else:
        sizes = measure_units(us) if have_chrome else {}
        doc, count = build_html(g, us, cog, meta, sizes, plates())

    html_path = OUT / ("spanish-compact.html" if compact else "spanish.html")
    html_path.write_text(doc, encoding="utf-8")

    pdf_path = OUT / ("spanish-compact.pdf" if compact else "spanish-vocab.pdf")
    if "--html" in sys.argv:
        print(f"{html_path}  ({count} word entries, {len(us)} units)")
        return
    if not have_chrome:
        print(f"Chrome not found at {CHROME}; wrote {html_path} only.")
        return

    if pdf_path.exists():
        pdf_path.unlink()
    run_chrome(["--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                html_path.as_uri()], wait_for=pdf_path)
    if not pdf_path.exists():
        raise SystemExit("Chrome failed to produce a PDF")

    # Second pass: learn where each section begins, put those numbers in the
    # contents, reprint, then stamp folios and running heads on top.
    front = 1 if compact else 2
    titles = ([g["title"]] + [u["title"] for u in us]
              + ([] if compact else [p["title"] for p in plates()])
              + [cog["title"].replace("Appendix A · ", "")])
    try:
        starts, total = section_starts(pdf_path, titles, front)
        if not compact:
            folios = {t: i - front + 1 for t, i in starts.items()}
            doc, count = build_html(g, us, cog, meta, sizes, plates(), folios)
            html_path.write_text(doc, encoding="utf-8")
            pdf_path.unlink()
            run_chrome(["--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                        html_path.as_uri()], wait_for=pdf_path)
            starts, total = section_starts(pdf_path, titles, front)
        heads = {}
        current = ""
        by_page = {i: t for t, i in sorted(starts.items(), key=lambda kv: kv[1])}
        for i in range(total):
            current = by_page.get(i, current)
            heads[i] = current
        stamp_folios(pdf_path, heads, total, front)
    except Exception as exc:
        print(f"  ! folio pass skipped: {exc}")

    pages = ""
    try:
        from pypdf import PdfReader
        pages = f", {len(PdfReader(str(pdf_path)).pages)} pages"
    except Exception:
        pass
    fits = "" if compact else " ".join(f"{k}:{v}pt" for k, v in sorted(sizes.items()))
    print(f"{pdf_path}  ({count} word entries, {len(us)} units{pages})")
    if fits:
        print(f"  unit type sizes: {fits}")


if __name__ == "__main__":
    sys.exit(main())
