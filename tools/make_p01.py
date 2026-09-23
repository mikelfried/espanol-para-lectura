#!/usr/bin/env python3
"""Regenerate the house plate SVG (data/plates/p01.json).

Hand-placing several hundred SVG coordinates in JSON is unmaintainable, so the
drawing is generated from this script and the result stored in the plate file.
Edit here, run, rebuild.
"""
import json
import pathlib

DEFS = '''<defs>
<pattern id="wood" width="72" height="16" patternUnits="userSpaceOnUse">
 <rect width="72" height="16" fill="#eddcbe"/>
 <path d="M0 16h72" stroke="#dcc7a2" stroke-width="1"/>
 <path d="M24 0v16M56 0v16" stroke="#dcc7a2" stroke-width=".8"/></pattern>
<pattern id="ktile" width="24" height="24" patternUnits="userSpaceOnUse">
 <rect width="24" height="24" fill="#eef2f4"/>
 <path d="M24 0v24M0 24h24" stroke="#dde5e9" stroke-width="1"/></pattern>
<pattern id="btile" width="15" height="15" patternUnits="userSpaceOnUse">
 <rect width="15" height="15" fill="#e8f1f3"/>
 <path d="M15 0v15M0 15h15" stroke="#d3e3e7" stroke-width="1"/></pattern>
<pattern id="conc" width="38" height="38" patternUnits="userSpaceOnUse">
 <rect width="38" height="38" fill="#eceae5"/>
 <path d="M38 0v38M0 38h38" stroke="#e0ddd6" stroke-width="1.2"/></pattern>
<pattern id="lawn" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
 <rect width="11" height="11" fill="#e2edd4"/>
 <path d="M0 0v11" stroke="#c7dcb2" stroke-width="1.1"/></pattern>
</defs>'''

STYLE = ('<style>.w{fill:none;stroke:#1d2229;stroke-width:7}'
 '.iw{fill:none;stroke:#1d2229;stroke-width:4}'
 '.rm{font-size:18px;fill:#1d2229;font-weight:600}'
 '.sm{font-size:12px;fill:#79818d}'
 '.f{stroke:#8e97a2;stroke-width:1.4}'
 '.fl{stroke:#a7b0ba;stroke-width:1.1;fill:none}'
 '.sw{fill:none;stroke:#b3bac2;stroke-width:1;stroke-dasharray:4 3}'
 '.bn{fill:#1d2229}.bt{font-size:12.5px;fill:#fff;font-weight:700}'
 '.ld{stroke:#1d2229;stroke-width:1.1}</style>')

P = []
a = P.append

# ---------- garden strip, west of the house, reached by the front door ----
a('<rect x="24" y="60" width="162" height="340" rx="3" fill="url(#lawn)" stroke="#a9bd96" stroke-width="1.4"/>')
for cx, cy, r in ((68, 182, 26), (150, 196, 18), (62, 332, 26), (152, 344, 19)):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#c7ddb1" stroke="#a5c48b" stroke-width="1.4"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{round(r * 0.4)}" fill="#aecb96"/>')
a('<rect x="94" y="286" width="54" height="14" rx="3" fill="#d9c9ae" stroke="#bfae91" stroke-width="1.2"/>')
a('<path d="M96 300v8M146 300v8" stroke="#bfae91" stroke-width="1.6"/>')
for cx in (178, 157, 136, 115):
    a(f'<ellipse cx="{cx}" cy="262" rx="9" ry="6.4" fill="#e0d8c8" stroke="#c6bba6" stroke-width="1.1"/>')

# ---------- floors --------------------------------------------------------
a('<rect x="200" y="60" width="180" height="170" fill="url(#ktile)"/>')
a('<rect x="380" y="60" width="180" height="170" fill="url(#wood)"/>')
a('<rect x="560" y="60" width="200" height="170" fill="url(#wood)"/>')
a('<rect x="200" y="230" width="560" height="60" fill="url(#wood)"/>')
a('<rect x="200" y="290" width="210" height="110" fill="url(#wood)"/>')
a('<rect x="410" y="290" width="120" height="110" fill="url(#btile)"/>')
a('<rect x="530" y="290" width="230" height="110" fill="url(#conc)"/>')

# ---------- cocina --------------------------------------------------------
a('<rect x="206" y="66" width="168" height="32" fill="#dcd6ca" class="f"/>')
a('<rect x="216" y="72" width="44" height="20" rx="4" fill="#f3f6f7" class="f"/>')
a('<circle cx="238" cy="82" r="3.4" fill="#aeb6bd"/>')
a('<rect x="286" y="70" width="52" height="24" rx="3" fill="#cfc9be" class="f"/>')
for cx, cy in ((299, 77), (325, 77), (299, 88), (325, 88)):
    a(f'<circle cx="{cx}" cy="{cy}" r="5" fill="none" stroke="#8e97a2" stroke-width="1.3"/>')
a('<rect x="206" y="98" width="32" height="76" fill="#dcd6ca" class="f"/>')
a('<rect x="206" y="180" width="38" height="44" rx="3" fill="#e6e9ec" class="f"/>')
a('<path d="M206 202h38" class="fl"/>')
a('<rect x="286" y="180" width="80" height="42" rx="4" fill="#d3bc99" class="f"/>')

# ---------- comedor -------------------------------------------------------
a('<ellipse cx="470" cy="120" rx="76" ry="52" fill="#f2e7d4" stroke="#e0d2b9" stroke-width="1.2"/>')
for x, y in ((455, 66), (455, 160)):
    a(f'<rect x="{x}" y="{y}" width="30" height="16" rx="5" fill="#cbb695" class="f"/>')
for x, y in ((396, 108), (524, 108)):
    a(f'<rect x="{x}" y="{y}" width="16" height="30" rx="5" fill="#cbb695" class="f"/>')
a('<ellipse cx="470" cy="120" rx="50" ry="35" fill="#d3bc99" class="f"/>')
a('<ellipse cx="470" cy="120" rx="38" ry="25" fill="none" stroke="#c0a882" stroke-width="1"/>')

# ---------- sala ----------------------------------------------------------
a('<rect x="574" y="94" width="172" height="124" rx="6" fill="#f1ece2" stroke="#e2dacc" stroke-width="1.2"/>')
a('<rect x="588" y="194" width="140" height="30" rx="5" fill="#ccd5dd" class="f"/>')
a('<rect x="588" y="188" width="140" height="9" rx="4" fill="#b4c0cb" class="f"/>')
a('<path d="M635 194v30M681 194v30" class="fl"/>')
a('<rect x="566" y="108" width="34" height="46" rx="7" fill="#ccd5dd" class="f"/>')
a('<rect x="628" y="158" width="62" height="24" rx="4" fill="#d3bc99" class="f"/>')
a('<rect x="618" y="66" width="86" height="11" rx="2" fill="#3a4047"/>')
a('<rect x="722" y="86" width="26" height="60" rx="2" fill="#d3bc99" class="f"/>')
a('<path d="M722 106h26M722 126h26" class="fl"/>')
a('<circle cx="738" cy="168" r="14" fill="#cfe0c2" class="f"/>')
a('<circle cx="738" cy="168" r="7" fill="#aecb96"/>')

# ---------- pasillo -------------------------------------------------------
a('<rect x="400" y="246" width="240" height="28" rx="3" fill="#ece3d3" stroke="#ddd0ba" stroke-width="1.2"/>')
a('<rect x="666" y="238" width="80" height="14" rx="2" fill="#d3bc99" class="f"/>')

# ---------- cuarto: pillows at the short end, so the bed has a head -------
a('<rect x="214" y="322" width="132" height="76" rx="4" fill="#f4efe4" stroke="#e3dbcb" stroke-width="1.2"/>')
a('<rect x="222" y="330" width="116" height="60" rx="4" fill="#eef2f5" class="f"/>')
a('<rect x="222" y="330" width="9" height="60" rx="3" fill="#cbb695" class="f"/>')
a('<rect x="235" y="334" width="26" height="24" rx="5" fill="#fff" class="f"/>')
a('<rect x="235" y="362" width="26" height="24" rx="5" fill="#fff" class="f"/>')
a('<rect x="266" y="330" width="72" height="60" fill="#ccd9e3" class="f"/>')
a('<rect x="266" y="330" width="13" height="60" fill="#b9cad7" class="f"/>')
a('<rect x="206" y="334" width="14" height="20" rx="2" fill="#dcd6ca" class="f"/>')
a('<rect x="352" y="298" width="52" height="30" rx="2" fill="#dcd6ca" class="f"/>')
a('<path d="M378 298v30" class="fl"/>')

# ---------- bano ----------------------------------------------------------
a('<rect x="416" y="330" width="36" height="62" rx="11" fill="#f4f9fa" class="f"/>')
a('<circle cx="434" cy="338" r="3" fill="#aeb6bd"/>')
a('<rect x="458" y="330" width="34" height="34" rx="3" fill="#f4f9fa" class="f"/>')
a('<path d="M458 330 492 364M492 330 458 364" stroke="#cfe0e4" stroke-width="1.2"/>')
a('<circle cx="475" cy="347" r="3" fill="#aeb6bd"/>')
a('<ellipse cx="470" cy="380" rx="12" ry="14" fill="#f4f9fa" class="f"/>')
a('<rect x="462" y="388" width="17" height="9" rx="3" fill="#e6eef0" class="f"/>')
a('<rect x="498" y="330" width="26" height="20" rx="4" fill="#f4f9fa" class="f"/>')
a('<circle cx="511" cy="340" r="7" fill="#fff" class="f"/>')

# ---------- garaje: car seen from directly above --------------------------
CX0 = 566
for wx in (CX0 + 26, CX0 + 132):
    a(f'<rect x="{wx}" y="330" width="15" height="18" rx="4" fill="#3a4047"/>')
    a(f'<rect x="{wx}" y="378" width="15" height="18" rx="4" fill="#3a4047"/>')
a(f'<path d="M{CX0 + 16} 336h132a16 16 0 0 1 16 16v22a16 16 0 0 1-16 16H{CX0 + 16}'
  f'a20 20 0 0 1-20-19v-16a20 20 0 0 1 20-19z" fill="#b9c6d4" stroke="#6f7c8a" stroke-width="1.6"/>')
a(f'<path d="M{CX0 + 60} 342h58a10 10 0 0 1 10 10v22a10 10 0 0 1-10 10h-58z" '
  f'fill="#9fb0c2" stroke="#6f7c8a" stroke-width="1.3"/>')
a(f'<path d="M{CX0 + 60} 342l-18 7v28l18 7z" fill="#dce5ed" stroke="#6f7c8a" stroke-width="1.2"/>')
a(f'<path d="M{CX0 + 128} 342l14 7v28l-14 7z" fill="#dce5ed" stroke="#6f7c8a" stroke-width="1.2"/>')
a(f'<rect x="{CX0 + 58}" y="331" width="9" height="7" rx="2" fill="#8d9aa8"/>')
a(f'<rect x="{CX0 + 58}" y="388" width="9" height="7" rx="2" fill="#8d9aa8"/>')
a(f'<rect x="{CX0 + 2}" y="344" width="9" height="10" rx="3" fill="#f2efe2" stroke="#6f7c8a" stroke-width="1"/>')
a(f'<rect x="{CX0 + 2}" y="372" width="9" height="10" rx="3" fill="#f2efe2" stroke="#6f7c8a" stroke-width="1"/>')
a(f'<rect x="{CX0 + 156}" y="346" width="7" height="8" rx="2" fill="#c96b60" stroke="#6f7c8a" stroke-width="1"/>')
a(f'<rect x="{CX0 + 156}" y="372" width="7" height="8" rx="2" fill="#c96b60" stroke="#6f7c8a" stroke-width="1"/>')
a(f'<path d="M{CX0 + 76} 352h34M{CX0 + 76} 366h34" stroke="#8d9aa8" stroke-width="1.1"/>')

# ---------- walls ---------------------------------------------------------
a('<rect x="200" y="60" width="560" height="340" class="w"/>')
a('<line x1="380" y1="60" x2="380" y2="230" class="iw"/>')
a('<line x1="560" y1="60" x2="560" y2="230" class="iw"/>')
a('<line x1="200" y1="230" x2="760" y2="230" class="iw"/>')
a('<line x1="200" y1="290" x2="760" y2="290" class="iw"/>')
a('<line x1="410" y1="290" x2="410" y2="400" class="iw"/>')
a('<line x1="530" y1="290" x2="530" y2="400" class="iw"/>')

doors = [(276, 230, 'up'), (462, 230, 'up'), (660, 230, 'up'),
         (300, 290, 'dn'), (446, 290, 'dn'), (600, 290, 'dn')]
a('<g stroke="#fff" stroke-width="5">' + ''.join(
    f'<line x1="{x}" y1="{y}" x2="{x + 38}" y2="{y}"/>' for x, y, _ in doors) + '</g>')
for x, y, d in doors:
    s = -1 if d == 'up' else 1
    a(f'<path d="M{x} {y}v{38 * s}" stroke="#9aa2ad" stroke-width="1.4"/>')
    a(f'<path d="M{x} {y + 38 * s}a38 38 0 0 {1 if d == "up" else 0} 38 {-38 * s}" class="sw"/>')

win = [(250, 60, 350, 60), (420, 60, 500, 60), (620, 60, 720, 60), (760, 110, 760, 190)]
a('<g stroke="#fff" stroke-width="7">' + ''.join(
    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for x1, y1, x2, y2 in win)
  + '<line x1="200" y1="242" x2="200" y2="280"/></g>')
a('<g stroke="#1d2229" stroke-width="1.6">' + ''.join(
    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for x1, y1, x2, y2 in win) + '</g>')
a('<line x1="200" y1="242" x2="200" y2="280" stroke="#1d2229" stroke-width="2"/>')
a('<path d="M200 280a38 38 0 0 0 38-38" class="sw"/>')
a('<line x1="200" y1="280" x2="238" y2="280" stroke="#1d2229" stroke-width="2.4"/>')
a('<line x1="590" y1="400" x2="710" y2="400" stroke="#fff" stroke-width="7"/>')
a('<rect x="590" y="394" width="120" height="12" fill="#dcd6ca" stroke="#1d2229" stroke-width="1.6"/>')
a('<g stroke="#b3bac2" stroke-width="1">' + ''.join(
    f'<line x1="{x}" y1="394" x2="{x}" y2="406"/>' for x in range(605, 710, 15)) + '</g>')

# ---------- labels --------------------------------------------------------
a('<g text-anchor="middle">'
  '<text x="290" y="144" class="rm lab">la cocina</text>'
  '<text x="290" y="161" class="sm lab">kitchen</text>'
  '<text x="470" y="206" class="rm lab">el comedor</text>'
  '<text x="470" y="221" class="sm lab">dining room</text>'
  '<text x="660" y="133" class="rm lab">la sala</text>'
  '<text x="660" y="150" class="sm lab">living room</text>'
  '<text x="105" y="118" class="rm lab">el jardín</text>'
  '<text x="105" y="135" class="sm lab">garden, yard</text></g>')
a('<g><text x="300" y="266" class="rm lab">el pasillo</text>'
  '<text x="232" y="316" class="rm lab">el cuarto</text>'
  '<text x="436" y="316" class="rm lab">el baño</text>'
  '<text x="566" y="316" class="rm lab">el garaje</text></g>')

badges = [(290, 116, 2), (470, 178, 3), (660, 105, 4), (281, 261, 5), (213, 311, 6),
          (417, 311, 7), (547, 311, 8), (105, 86, 9), (776, 72, 1), (172, 306, 10),
          (300, 26, 11), (776, 340, 12)]
a('<g class="bn">' + ''.join(f'<circle cx="{x}" cy="{y}" r="13"/>' for x, y, _ in badges) + '</g>')
a('<g class="bt" text-anchor="middle">' + ''.join(
    f'<text x="{x}" y="{y + 5}">{n}</text>' for x, y, n in badges) + '</g>')
a('<g class="ld"><line x1="763" y1="72" x2="750" y2="66"/>'
  '<line x1="180" y1="295" x2="198" y2="272"/>'
  '<line x1="300" y1="39" x2="300" y2="57"/>'
  '<line x1="763" y1="340" x2="748" y2="340"/></g>')

svg = ' '.join((f'<svg viewBox="0 0 790 420" xmlns="http://www.w3.org/2000/svg">'
                f'{DEFS}{STYLE}{"".join(P)}</svg>').split())

path = pathlib.Path(__file__).parent.parent / 'data/plates/p01.json'
d = json.loads(path.read_text())
d["intro"] = ("An estate agent's plan of a small house, seen from above, with its garden "
              "and the path to the front door. Learn the rooms by where they sit and what "
              "stands in them — then turn the page, where the numbers stay and every name "
              "is gone, and say each one aloud.")
d["svg"] = svg
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("p01 svg:", len(svg), "chars")
