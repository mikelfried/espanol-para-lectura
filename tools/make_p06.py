#!/usr/bin/env python3
"""Generate the table setting plate (data/plates/p06.json).

A laid place seen from above. These are the words you need the moment you sit
down in a restaurant, and several of them are traps: la copa is a wine glass,
not a cup; la taza is the cup; el vaso is a tumbler.
"""
import json
import pathlib

MET = 'fill:#d9dee4;stroke:#7b8794;stroke-width:1.6'
STYLE = ('<style>'
 '.met{' + MET + '}'
 '.chi{fill:#fdfdfc;stroke:#aeb6c0;stroke-width:1.8}'
 '.chi2{fill:#f4f6f8;stroke:#aeb6c0;stroke-width:1.6}'
 '.gls{fill:#eef4f7;stroke:#8fa3ad;stroke-width:1.7}'
 '.cloth{fill:#fbf7ef;stroke:#e0d7c6;stroke-width:1.6}'
 '.nap{fill:#eef2f6;stroke:#b6c0ca;stroke-width:1.6}'
 '.fold{fill:none;stroke:#c6cfd8;stroke-width:1.2}'
 '.pap{fill:#fdfbf6;stroke:#b9b0a1;stroke-width:1.6}'
 '.pln{stroke:#d3cbbd;stroke-width:1.6;stroke-linecap:round}'
 '.wd{fill:none;stroke:#c2a983;stroke-width:1.2}'
 '.bn{fill:#1d2229}.bt{font-size:12px;fill:#fff;font-weight:700;text-anchor:middle}'
 '.ld{stroke:#1d2229;stroke-width:1.1;fill:none}.dot{fill:#1d2229}'
 '</style>')

DEFS = '''<defs>
<pattern id="oak" width="148" height="34" patternUnits="userSpaceOnUse">
 <rect width="148" height="34" fill="#e6cfa8"/>
 <path d="M0 17h148M0 34h148" stroke="#d6bb8d" stroke-width="1.1"/>
 <path d="M52 0v17M118 0v17M14 17v17M86 17v17" stroke="#d6bb8d" stroke-width="1"/>
 <path d="M20 8h44M96 25h38" stroke="#dcc49c" stroke-width="1"/></pattern>
<g id="fork">
 <rect x="-4" y="50" width="8" height="82" rx="4" style="''' + MET + '''"/>
 <path d="M-10 30h20v14q0 8-10 8t-10-8z" style="''' + MET + '''"/>
 <rect x="-9.4" y="0" width="3.4" height="32" rx="1.7" style="''' + MET + '''"/>
 <rect x="-3.2" y="0" width="3.4" height="32" rx="1.7" style="''' + MET + '''"/>
 <rect x="3" y="0" width="3.4" height="32" rx="1.7" style="''' + MET + '''"/>
 <rect x="9.2" y="0" width="3.4" height="32" rx="1.7" style="''' + MET + '''"/>
</g>
<g id="knife">
 <path d="M0 0c6 8 9 20 9 36v26H-7V36C-7 20-5 8 0 0z" style="''' + MET + '''"/>
 <rect x="-6" y="60" width="12" height="70" rx="5" style="''' + MET + '''"/>
</g>
<g id="spoon">
 <ellipse cx="0" cy="22" rx="13" ry="22" style="''' + MET + '''"/>
 <rect x="-4" y="44" width="8" height="86" rx="4" style="''' + MET + '''"/>
</g>
</defs>'''

P = []
a = P.append

# table, then cloth laid over it
a('<rect x="24" y="24" width="732" height="504" rx="4" fill="url(#oak)" stroke="#a8844f" stroke-width="2"/>')
a('<rect x="96" y="58" width="592" height="436" rx="6" class="cloth"/>')
a('<path d="M392 58v436" class="fold"/>')

# napkin, folded, to the far left
a('<rect x="150" y="248" width="76" height="112" rx="4" class="nap"/>')
a('<path d="M150 276h76M150 304h76" class="fold"/>')

# cutlery
a('<use href="#fork" transform="translate(256,232)"/>')
a('<use href="#knife" transform="translate(500,232)"/>')
a('<use href="#spoon" transform="translate(536,234)"/>')

# dinner plate with a soup bowl set on it
a('<circle cx="382" cy="300" r="86" class="chi"/>')
a('<circle cx="382" cy="300" r="70" class="chi2"/>')
a('<circle cx="383" cy="302" r="51" fill="#dfe4ea"/>')
a('<circle cx="382" cy="300" r="50" class="chi"/>')
a('<circle cx="382" cy="300" r="37" class="chi2"/>')
a('<circle cx="382" cy="300" r="24" class="chi"/>')

# tumbler and a cup on its saucer
a('<circle cx="540" cy="132" r="27" class="gls"/>')
a('<circle cx="540" cy="132" r="21" class="gls"/>')
a('<circle cx="444" cy="128" r="25" class="gls"/>')
a('<circle cx="444" cy="128" r="14" class="gls"/>')
a('<circle cx="444" cy="128" r="4" fill="#8fa3ad"/>')
a('<circle cx="626" cy="170" r="35" class="chi"/>')
a('<circle cx="626" cy="170" r="22" class="chi2"/>')
a('<path d="M648 162a11 11 0 0 1 0 16" fill="none" stroke="#aeb6c0" stroke-width="3"/>')

# bottle, salt and pepper
a('<circle cx="286" cy="128" r="23" class="gls"/>')
a('<circle cx="286" cy="128" r="11" fill="#8d949c" stroke="#6a7178" stroke-width="1.4"/>')
a('<circle cx="286" cy="128" r="5" fill="#aeb6bd"/>')
a('<circle cx="348" cy="118" r="13" class="chi"/>')
a('<circle cx="382" cy="118" r="13" class="chi2"/>')
a('<g fill="#8d949c"><circle cx="345" cy="115" r="1.5"/><circle cx="351" cy="115" r="1.5"/>'
  '<circle cx="348" cy="121" r="1.5"/>'
  '<circle cx="379" cy="115" r="1.5"/><circle cx="385" cy="115" r="1.5"/>'
  '<circle cx="382" cy="121" r="1.5"/><circle cx="379" cy="121" r="1.5"/></g>')

# the menu, lying on the cloth
a('<rect x="600" y="330" width="86" height="126" rx="4" class="pap"/>')
a('<g class="pln">' + ''.join(f'<path d="M614 {y}h58"/>' for y in range(352, 446, 16)) + '</g>')

# chair back, just off the edge of the cloth
a('<rect x="320" y="548" width="124" height="58" rx="7" class="chi2"/>')
a('<rect x="314" y="596" width="136" height="14" rx="7" class="chi"/>')
a('<path d="M334 548v-14M430 548v-14" stroke="#aeb6c0" stroke-width="4"/>')

CALL = [
    (1, 52, 44, 108, 40),        # la mesa
    (2, 52, 106, 106, 84),       # el mantel
    (8, 118, 214, 158, 250),     # la servilleta
    (5, 232, 190, 250, 234),     # el tenedor
    (3, 296, 194, 330, 228),     # el plato
    (4, 382, 428, 382, 346),     # el plato hondo
    (6, 522, 204, 502, 238),     # el cuchillo
    (7, 578, 216, 538, 244),     # la cuchara
    (15, 406, 78, 440, 110),     # la copa
    (9, 596, 80, 556, 110),      # el vaso
    (10, 690, 152, 658, 164),    # la taza
    (11, 240, 108, 266, 122),    # la botella
    (12, 344, 70, 352, 102),     # la sal y la pimienta
    (13, 716, 300, 674, 334),    # la carta
    (14, 254, 576, 318, 576),    # la silla
]
for n, bx, by, ax, ay in CALL:
    a(f'<line x1="{bx}" y1="{by}" x2="{ax}" y2="{ay}" class="ld"/>')
    a(f'<circle cx="{ax}" cy="{ay}" r="3" class="dot"/>')
    a(f'<circle cx="{bx}" cy="{by}" r="13" class="bn"/>'
      f'<text x="{bx}" y="{by + 4.5}" class="bt">{n}</text>')

svg = ' '.join((f'<svg viewBox="0 0 780 622" xmlns="http://www.w3.org/2000/svg">'
                f'{DEFS}{STYLE}{"".join(P)}</svg>').split())

items = [
    (1, "la mesa", "table"), (2, "el mantel", "tablecloth"),
    (3, "el plato", "plate"), (4, "el plato hondo", "bowl"),
    (5, "el tenedor", "fork"), (6, "el cuchillo", "knife"),
    (7, "la cuchara", "spoon"), (8, "la servilleta", "napkin"),
    (9, "el vaso", "glass, tumbler"), (10, "la taza", "cup, mug"),
    (11, "la botella", "bottle"), (12, "la sal · la pimienta", "salt · pepper"),
    (13, "la carta · el menú", "menu"), (14, "la silla", "chair"),
    (15, "la copa", "wine glass"),
]

out = {
    "id": "p06",
    "title": "La mesa · a place setting",
    "intro": ("What is in front of you the moment you sit down. Three of these are worth "
              "separating carefully: el vaso is a tumbler for water, la copa is a "
              "stemmed wine glass, and la taza is a cup for coffee — English cup covers "
              "the last two and Spanish does not. La carta is the menu; el menú often "
              "means the set meal of the day."),
    "svg": svg,
    "items": [{"n": n, "es": es, "en": en} for n, es, en in items],
}
path = pathlib.Path(__file__).parent.parent / 'data/plates/p06.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("p06 svg:", len(svg), "chars")
