#!/usr/bin/env python3
"""Generate the colour plate (data/plates/p07.json).

The only plate where the drawing *is* the answer: a colour name needs no
picture of a thing, just the colour itself. Printed as real swatches.
"""
import json
import pathlib

SWATCHES = [
    (1, 'blanco', 'white', '#ffffff'),
    (2, 'negro', 'black', '#1d2229'),
    (3, 'gris', 'grey', '#9aa2ab'),
    (4, 'rojo', 'red', '#c9352c'),
    (5, 'azul', 'blue', '#2f5d9e'),
    (6, 'verde', 'green', '#3f8a4d'),
    (7, 'amarillo', 'yellow', '#f0c518'),
    (8, 'naranja', 'orange', '#e2822c'),
    (9, 'rosado', 'pink', '#e58fa8'),
    (10, 'morado', 'purple', '#7a4b9b'),
    (11, 'café · marrón', 'brown', '#7d5334'),
    (12, 'azul claro', 'light blue', '#8fb4dd'),
    (13, 'azul oscuro', 'dark blue', '#1d3054'),
    (14, 'dorado', 'gold', '#c9a227'),
    (15, 'plateado', 'silver', '#c2c8ce'),
]

COLS, W, H, GAP = 5, 138, 116, 12
STYLE = ('<style>'
 '.sw{stroke:#7c838b;stroke-width:1.4}'
 '.nm{font-size:15px;fill:#1d2229;font-weight:700;text-anchor:middle}'
 '.en{font-size:11px;fill:#79818d;text-anchor:middle}'
 '.bn{fill:#fff;stroke:#1d2229;stroke-width:1.6}'
 '.bt{font-size:11.5px;fill:#1d2229;font-weight:700;text-anchor:middle}'
 '</style>')

P = []
a = P.append
for i, (n, es, en, hexv) in enumerate(SWATCHES):
    col, row = i % COLS, i // COLS
    x = 14 + col * (W + GAP)
    y = 14 + row * (H + 56)
    a(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="6" fill="{hexv}" class="sw"/>')
    a(f'<circle cx="{x + 20}" cy="{y + 20}" r="12" class="bn"/>'
      f'<text x="{x + 20}" y="{y + 24.5}" class="bt">{n}</text>')
    a(f'<text x="{x + W / 2}" y="{y + H + 22}" class="nm lab">{es}</text>')
    a(f'<text x="{x + W / 2}" y="{y + H + 38}" class="en lab">{en}</text>')

rows = (len(SWATCHES) + COLS - 1) // COLS
height = 14 + rows * (H + 56)
svg = ' '.join((f'<svg viewBox="0 0 764 {height}" xmlns="http://www.w3.org/2000/svg">'
                f'{STYLE}{"".join(P)}</svg>').split())

out = {
    "id": "p07",
    "title": "Los colores · the colours",
    "intro": ("The one plate that needs no drawing of a thing: the colour is the answer. "
              "Colours are adjectives and follow their noun, agreeing with it — una puerta "
              "roja, unos zapatos negros. Those ending in -e or a consonant have one form "
              "for both genders: verde, azul, gris. claro and oscuro go after the colour "
              "and do not agree: unas paredes azul claro."),
    "svg": svg,
    "items": [{"n": n, "es": es, "en": en} for n, es, en, _ in SWATCHES],
}
path = pathlib.Path(__file__).parent.parent / 'data/plates/p07.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("p07 svg:", len(svg), "chars")
