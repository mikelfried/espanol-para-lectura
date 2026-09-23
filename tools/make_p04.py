#!/usr/bin/env python3
"""Generate the family tree plate (data/plates/p04.json).

Kinship is relational, so a list teaches it badly: el sobrino only means
anything once you can see whose child he is. Everything hangs off yo.
"""
import json
import pathlib

W, H = 112, 50          # box size
STYLE = ('<style>'
 '.bx{fill:#f5f2ea;stroke:#4a5159;stroke-width:2;}'
 '.me{fill:#e6ece9;stroke:#2f6b55;stroke-width:2.6}'
 '.es{font-size:13.5px;fill:#1d2229;font-weight:700;text-anchor:middle}'
 '.en{font-size:9.5px;fill:#79818d;text-anchor:middle}'
 '.ln{fill:none;stroke:#4a5159;stroke-width:2}'
 '.mar{fill:none;stroke:#4a5159;stroke-width:2}'
 '.rel{fill:none;stroke:#2f6b55;stroke-width:1.8;stroke-dasharray:6 5}'
 '.frame{fill:none;stroke:#c3cad2;stroke-width:1.4;stroke-dasharray:7 6}'
 '.bn{fill:#1d2229}.bt{font-size:11.5px;fill:#fff;font-weight:700;text-anchor:middle}'
 '.gn{fill:#2f6b55}'
 '</style>')

P = []
a = P.append
a('<rect x="26" y="26" width="748" height="496" rx="12" class="frame"/>')

def box(cx, y, es, en, n, me=False):
    x = cx - W / 2
    a(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="9" '
      f'class="{"me" if me else "bx"}"/>')
    a(f'<text x="{cx}" y="{y + 22}" class="es lab">{es}</text>')
    a(f'<text x="{cx}" y="{y + 37}" class="en lab">{en}</text>')
    a(f'<circle cx="{x}" cy="{y}" r="12" class="bn"/>'
      f'<text x="{x}" y="{y + 4.5}" class="bt">{n}</text>')

def badge(cx, cy, n, green=False):
    a(f'<circle cx="{cx}" cy="{cy}" r="12" class="{"gn" if green else "bn"}"/>'
      f'<text x="{cx}" y="{cy + 4.5}" class="bt">{n}</text>')

# ---- generation 1: the grandparents --------------------------------------
GY = 58
box(332, GY, 'el abuelo', 'grandfather', 2)
box(468, GY, 'la abuela', 'grandmother', 3)
a(f'<path d="M388 {GY + 25}h24" class="mar"/>')
a(f'<path d="M400 {GY + 25}V152" class="ln"/>')
badge(400, 116, 4)

# ---- generation 2: their children and those children's spouses -----------
BY = 178
a('<path d="M256 152h288" class="ln"/>')
a(f'<path d="M256 152v{BY - 152}M544 152v{BY - 152}" class="ln"/>')
box(120, BY, 'el tío', 'uncle', 8)
box(256, BY, 'la tía', 'aunt', 9)
box(544, BY, 'el padre', 'father', 5)
box(680, BY, 'la madre', 'mother', 6)
a(f'<path d="M176 {BY + 25}h24M600 {BY + 25}h24" class="mar"/>')
a(f'<path d="M188 {BY + 25}v95M612 {BY + 25}v46" class="ln"/>')
badge(188, 238, 16)
badge(612, 238, 7)

# ---- generation 3: me, my sibling, my cousin -----------------------------
CY = 298
a('<path d="M460 272h160" class="ln"/>')
a(f'<path d="M460 272v{CY - 272}M620 272v{CY - 272}" class="ln"/>')
box(188, CY, 'el primo', 'cousin', 11)
box(460, CY, 'yo', 'me', 12, me=True)
box(620, CY, 'la hermana', 'sister', 10)

# ---- generation 4: my child, my sibling's child --------------------------
DY = 428
a(f'<path d="M460 {CY + H}v80" class="ln"/>')
box(460, DY, 'el hijo · la hija', 'son · daughter', 13)
a(f'<path d="M620 {CY + H}v46h46v34" class="ln"/>')
box(666, DY, 'el sobrino', 'nephew', 15)

# ---- the one link a tree cannot show by position: grandson ---------------
a('<path d="M400 152C366 208 364 258 402 300" class="rel"/>')
badge(372, 232, 14, green=True)

badge(26, 26, 1)
svg = ' '.join((f'<svg viewBox="0 0 800 548" xmlns="http://www.w3.org/2000/svg">'
                f'{STYLE}{"".join(P)}</svg>').split())

items = [
    (1, "la familia", "family"),
    (2, "el abuelo", "grandfather"),
    (3, "la abuela", "grandmother"),
    (4, "los abuelos", "grandparents"),
    (5, "el padre", "father"),
    (6, "la madre", "mother"),
    (7, "los padres", "parents"),
    (8, "el tío", "uncle"),
    (9, "la tía", "aunt"),
    (10, "el hermano · la hermana", "brother · sister"),
    (11, "el primo · la prima", "cousin"),
    (12, "yo", "me"),
    (13, "el hijo · la hija", "son · daughter"),
    (14, "el nieto · la nieta", "grandson · granddaughter"),
    (15, "el sobrino · la sobrina", "nephew · niece"),
    (16, "el esposo · la esposa", "husband · wife"),
]

out = {
    "id": "p04",
    "title": "La familia · a family tree",
    "intro": ("Kinship words only mean something in relation to somebody, so everything "
              "here hangs off yo. The short double line joins a married couple; the "
              "green dashed line marks the one relationship a tree cannot show by "
              "position — you are your grandparents' nieto. Plural forms take the "
              "masculine: los padres is parents, los abuelos is grandparents, los hijos "
              "is children."),
    "svg": svg,
    "items": [{"n": n, "es": es, "en": en} for n, es, en in items],
}
path = pathlib.Path(__file__).parent.parent / 'data/plates/p04.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("p04 svg:", len(svg), "chars")
