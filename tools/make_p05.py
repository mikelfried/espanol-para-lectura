#!/usr/bin/env python3
"""Generate the clock plate (data/plates/p05.json).

Nine clock faces. One clock can only show one time, so the grid does the
teaching: the singular es la una against the plural son las, the y half and the
menos half of the hour, and the two ways past the half hour are said.
"""
import json
import math
import pathlib

R = 62
STYLE = ('<style>'
 '.face{fill:#fbfaf7;stroke:#2b3138;stroke-width:3}'
 '.tick{stroke:#8d949c;stroke-width:2;stroke-linecap:round}'
 '.tickm{stroke:#2b3138;stroke-width:3.2;stroke-linecap:round}'
 '.num{font-size:11px;fill:#6b7280;text-anchor:middle;font-weight:600;stroke:#fbfaf7;stroke-width:3.4;paint-order:stroke;stroke-linejoin:round}'
 '.hh{stroke:#1d2229;stroke-width:6.5;stroke-linecap:round}'
 '.mh{stroke:#1d2229;stroke-width:4;stroke-linecap:round}'
 '.pin{fill:#1d2229}'
 '.cap{font-size:15px;fill:#1d2229;font-weight:700;font-style:normal;text-anchor:middle}'
 '.sub{font-size:11px;fill:#79818d;font-style:normal;text-anchor:middle}'
 '.cel{fill:#fff;stroke:#e2e6ea;stroke-width:1}.sun{fill:#f0c75e;stroke:#c9a23f;stroke-width:1.4}.ray{stroke:#c9a23f;stroke-width:1.8;stroke-linecap:round}.moon{fill:#cdd6e2;stroke:#8d97a6;stroke-width:1.4}'
 '.bn{fill:#1d2229}.bt{font-size:12px;fill:#fff;font-weight:700;text-anchor:middle}'
 '</style>')


def pt(cx, cy, deg, length):
    r = math.radians(deg)
    return cx + length * math.sin(r), cy - length * math.cos(r)


def clock(cx, cy, h, m):
    s = [f'<circle cx="{cx}" cy="{cy}" r="{R}" class="face"/>']
    for i in range(12):
        deg = i * 30
        major = i % 3 == 0
        x1, y1 = pt(cx, cy, deg, R - (12 if major else 7))
        x2, y2 = pt(cx, cy, deg, R - 3)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'class="{"tickm" if major else "tick"}"/>')
    hx, hy = pt(cx, cy, (h % 12) * 30 + m * 0.5, R - 28)
    mx, my = pt(cx, cy, m * 6, R - 12)
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" class="hh"/>')
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" class="mh"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" class="pin"/>')
    for i, lbl in ((0, '12'), (3, '3'), (6, '6'), (9, '9')):
        x, y = pt(cx, cy, i * 30, R - 31)
        s.append(f'<text x="{x:.1f}" y="{y + 4.5:.1f}" class="num">{lbl}</text>')
    return ''.join(s)


def sun(cx, cy, r=9):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" class="sun"/>']
    for k in range(8):
        d = math.radians(k * 45)
        x1, y1 = cx + (r + 3) * math.cos(d), cy + (r + 3) * math.sin(d)
        x2, y2 = cx + (r + 7) * math.cos(d), cy + (r + 7) * math.sin(d)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="ray"/>')
    return ''.join(out)


def moon(cx, cy, r=10):
    return (f'<path d="M{cx + r * 0.35:.1f} {cy - r:.1f}'
            f'a{r} {r} 0 1 0 {r * 0.75:.1f} {r * 1.7:.1f}'
            f'a{r * 0.82:.1f} {r * 0.82:.1f} 0 1 1 {-r * 0.75:.1f} {-r * 1.7:.1f}z" class="moon"/>')


# (n, hour, minute, Spanish, English, glyph)
CELLS = [
    (1, 1, 0,  'Es la una.',                  "It is one o'clock.",        None),
    (2, 3, 0,  'Son las tres.',               "It is three o'clock.",      None),
    (3, 3, 10, 'Son las tres y diez.',        'Ten past three.',           None),
    (4, 7, 15, 'Son las siete y cuarto.',     'Quarter past seven.',       None),
    (5, 3, 30, 'Son las tres y media.',       'Half past three.',          None),
    (6, 3, 45, 'Son las cuatro menos cuarto.', 'Quarter to four.',         None),
    (7, 3, 50, 'Son las cuatro menos diez.',  'Ten to four.',              None),
    (8, 8, 20, 'Son las ocho y veinte de la mañana.', '8:20 a.m.',           'sun'),
    (9, 10, 40, 'Son las once menos veinte de la noche.', '10:40 p.m.',      'moon'),
]

P = []
a = P.append
for i, (n, h, m, es, en, glyph) in enumerate(CELLS):
    col, row = i % 3, i // 3
    x, y = 14 + col * 251, 14 + row * 224
    a(f'<rect x="{x}" y="{y}" width="250" height="223" rx="4" class="cel"/>')
    a(clock(x + 125, y + 86, h, m))
    small = ' style="font-size:12.5px"' if len(es) > 30 else ''
    a(f'<text x="{x + 125}" y="{y + 182}" class="cap lab"{small}>{es}</text>')
    a(f'<text x="{x + 125}" y="{y + 199}" class="sub lab">{en}</text>')
    if glyph == 'sun':
        a(sun(x + 216, y + 30))
    elif glyph == 'moon':
        a(moon(x + 216, y + 30))
    a(f'<circle cx="{x + 28}" cy="{y + 28}" r="13" class="bn"/>'
      f'<text x="{x + 28}" y="{y + 33}" class="bt">{n}</text>')

svg = ' '.join((f'<svg viewBox="0 0 780 700" xmlns="http://www.w3.org/2000/svg">'
                f'{STYLE}{"".join(P)}</svg>').split())

out = {
    "id": "p05",
    "title": "¿Qué hora es? · telling the time",
    "intro": ("Spanish counts the hours as feminine and plural, because las horas is "
              "understood: son las tres. One o'clock is the lone exception — es la una. "
              "Up to the half hour you add with y; after it you subtract from the next "
              "hour with menos. Mexico and much of Central America prefer un cuarto para "
              "las cuatro to las cuatro menos cuarto; both are given below. There is no "
              "a.m. or p.m. in Spanish: you add de la mañana, de la tarde or de la "
              "noche. Midday is mediodía, midnight medianoche."),
    "svg": svg,
    "items": [
        {"n": 1, "es": "Es la una.", "en": "1:00 — singular, the only one"},
        {"n": 2, "es": "Son las tres.", "en": "3:00 — plural for every other hour"},
        {"n": 3, "es": "Son las tres y diez.", "en": "3:10 — add the minutes with y"},
        {"n": 4, "es": "Son las siete y cuarto.", "en": "7:15 — cuarto, not quince"},
        {"n": 5, "es": "Son las tres y media.", "en": "3:30 — media, feminine"},
        {"n": 6, "es": "Son las cuatro menos cuarto.", "en": "3:45 — or un cuarto para las cuatro"},
        {"n": 7, "es": "Son las cuatro menos diez.", "en": "3:50 — or diez para las cuatro"},
        {"n": 8, "es": "Son las ocho y veinte de la mañana.", "en": "8:20 a.m."},
        {"n": 9, "es": "Son las once menos veinte de la noche.", "en": "10:40 p.m."},
    ],
}
path = pathlib.Path(__file__).parent.parent / 'data/plates/p05.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("p05 svg:", len(svg), "chars")
