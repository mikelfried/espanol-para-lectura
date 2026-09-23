#!/usr/bin/env python3
"""Generate the body plate (data/plates/p03.json).

A front-view figure with numbered callouts, plus a small back view for the one
word a front view cannot show: la espalda.
"""
import json
import pathlib

SKIN = '#f0e6da'
LINE = '#4a5159'

STYLE = (f'<style>'
 f'.sk{{fill:{SKIN};stroke:{LINE};stroke-width:3;stroke-linejoin:round}}'
 f'.limb{{fill:none;stroke:{LINE};stroke-width:3}}'
 f'.limbf{{fill:none;stroke:{SKIN};stroke-linecap:round;stroke-linejoin:round}}'
 f'.limbs{{fill:none;stroke:{LINE};stroke-linecap:round;stroke-linejoin:round}}'
 f'.ft{{fill:none;stroke:#8d949c;stroke-width:2;stroke-linecap:round}}'
 f'.hair{{fill:#5d5148;stroke:{LINE};stroke-width:2.4;stroke-linejoin:round}}'
 f'.bn{{fill:#1d2229}}.bt{{font-size:12.5px;fill:#fff;font-weight:700;text-anchor:middle}}'
 f'.ld{{stroke:#1d2229;stroke-width:1.1;fill:none}}'
 f'.dot{{fill:#1d2229}}'
 f'.cap{{font-size:12px;fill:#79818d;text-anchor:middle;font-style:italic}}'
 f'</style>')

P = []
a = P.append

# ---- limbs: drawn as fat round strokes, outline first then a lighter core --
ARM_L = 'M336 168 308 262 296 382'
ARM_R = 'M444 168 472 262 484 382'
LEG_L = 'M362 330 352 466 348 580'
LEG_R = 'M418 330 428 466 432 580'
for d, w in ((ARM_L, 30), (ARM_R, 30), (LEG_L, 42), (LEG_R, 42)):
    a(f'<path d="{d}" class="limbs" stroke-width="{w + 6}"/>')
for d, w in ((ARM_L, 30), (ARM_R, 30), (LEG_L, 42), (LEG_R, 42)):
    a(f'<path d="{d}" class="limbf" stroke-width="{w}"/>')

# hands and feet
a(f'<path d="M296 376c-12 0-19 9-19 21 0 11 6 20 17 20 10 0 16-7 17-17l2-18zm-19 14c-6 1-9 5-8 10 1 4 5 6 8 4z" class="sk"/>')
a(f'<path d="M484 376c12 0 19 9 19 21 0 11-6 20-17 20-10 0-16-7-17-17l-2-18zm19 14c6 1 9 5 8 10-1 4-5 6-8 4z" class="sk"/>')
a(f'<path d="M348 578c-20 2-32 8-32 15 0 6 10 9 26 9 14 0 24-3 24-10z" class="sk"/>')
a(f'<path d="M432 578c20 2 32 8 32 15 0 6-10 9-26 9-14 0-24-3-24-10z" class="sk"/>')

for x in (287, 294, 301):
    a(f'<path d="M{x} 398v16" class="ft"/>')
for x in (479, 486, 493):
    a(f'<path d="M{x} 398v16" class="ft"/>')

# ---- torso ---------------------------------------------------------------
a('<path d="M334 186q2-30 22-38 14-6 34-6t34 6q20 8 22 38l-8 86q-4 32-12 62H354q-8-30-12-62z" class="sk"/>')
a('<circle cx="390" cy="288" r="3.5" fill="none" stroke="#b9b0a4" stroke-width="2"/>')

# ---- neck and head -------------------------------------------------------
a('<rect x="374" y="116" width="32" height="34" rx="10" class="sk"/>')
a('<ellipse cx="390" cy="84" rx="37" ry="45" class="sk"/>')
a('<ellipse cx="352" cy="86" rx="8" ry="12" class="sk"/>')
a('<ellipse cx="428" cy="86" rx="8" ry="12" class="sk"/>')
a('<path d="M353 62q6-30 37-30t37 30q2-16-8-28-12-14-29-14t-29 14q-10 12-8 28z" class="hair"/>')
a('<path d="M370 80q6-7 12 0-6 6-12 0z" fill="#fff" stroke="#4a5159" stroke-width="1.6" stroke-linejoin="round"/>')
a('<path d="M398 80q6-7 12 0-6 6-12 0z" fill="#fff" stroke="#4a5159" stroke-width="1.6" stroke-linejoin="round"/>')
a('<circle cx="376" cy="80" r="2.3" fill="#3a4047"/>')
a('<circle cx="404" cy="80" r="2.3" fill="#3a4047"/>')
a('<path d="M367 69q8-5 16-2M397 67q8-3 16 2" fill="none" stroke="#5d5148" stroke-width="2.2" stroke-linecap="round"/>')
a('<path d="M389 86v11q0 5-6 6" fill="none" stroke="#b9b0a4" stroke-width="2.2" stroke-linecap="round"/>')
a('<path d="M379 110q6 6 11 6t11-6" fill="none" stroke="#a8998c" stroke-width="2.4" stroke-linecap="round"/>')

# ---- small back view, for la espalda -------------------------------------
a('<g transform="translate(546,352) scale(0.34)">'
  '<path d="M336 168 306 262 294 372" class="limbs" stroke-width="40"/>'
  '<path d="M444 168 474 262 486 372" class="limbs" stroke-width="40"/>'
  '<path d="M362 330 352 466 348 560" class="limbs" stroke-width="52"/>'
  '<path d="M418 330 428 466 432 560" class="limbs" stroke-width="52"/>'
  '<path d="M336 168 306 262 294 372" class="limbf" stroke-width="34"/>'
  '<path d="M444 168 474 262 486 372" class="limbf" stroke-width="34"/>'
  '<path d="M362 330 352 466 348 560" class="limbf" stroke-width="46"/>'
  '<path d="M418 330 428 466 432 560" class="limbf" stroke-width="46"/>'
  '<rect x="374" y="116" width="32" height="34" rx="10" class="sk"/>'
  '<path d="M330 172q0-24 26-28h68q26 4 26 28l-8 100q-4 32-12 62H350q-8-30-12-62z" class="sk"/>'
  '<path d="M390 168v150" stroke="#b6aea4" stroke-width="4" fill="none"/>'
  '<ellipse cx="390" cy="84" rx="37" ry="45" class="sk"/>'
  '<path d="M353 84q0-52 37-52t37 52q0 16-6 22H359q-6-6-6-22z" class="hair"/>'
  '</g>')
a('<text x="678" y="586" class="cap lab">de espaldas · from behind</text>')

# ---- callouts ------------------------------------------------------------
# Face parts sit in a short stack beside the head; the body parts keep the
# outer column. Both sequences run top-down so no leader crosses another.
FACE_L = [(2, 52, 368, 44), (7, 88, 350, 88), (3, 124, 362, 100)]
FACE_R = [(1, 52, 414, 50), (4, 88, 406, 80), (5, 124, 392, 96),
          (6, 160, 392, 112), (8, 196, 400, 134)]
LEFT = [(9, 180, 338, 158), (10, 236, 314, 240), (11, 296, 300, 296),
        (12, 380, 292, 386), (13, 428, 294, 412)]
RIGHT = [(14, 250, 416, 186), (20, 290, 404, 210), (16, 330, 400, 280),
         (17, 418, 430, 420), (18, 466, 430, 466), (19, 566, 440, 588)]

def callout(n, bx, by, ax, ay):
    return (f'<line x1="{bx + (16 if bx < 390 else -16)}" y1="{by}" x2="{ax}" y2="{ay}" class="ld"/>'
            f'<circle cx="{ax}" cy="{ay}" r="3" class="dot"/>'
            f'<circle cx="{bx}" cy="{by}" r="13" class="bn"/>'
            f'<text x="{bx}" y="{by + 5}" class="bt">{n}</text>')

for n, by, ax, ay in LEFT:
    a(callout(n, 206, by, ax, ay))
for n, by, ax, ay in RIGHT:
    a(callout(n, 574, by, ax, ay))
for n, by, ax, ay in FACE_L:
    a(callout(n, 280, by, ax, ay))
for n, by, ax, ay in FACE_R:
    a(callout(n, 500, by, ax, ay))
a('<circle cx="606" cy="516" r="13" class="bn"/><text x="606" y="521" class="bt">15</text>')
a('<line x1="619" y1="516" x2="652" y2="500" class="ld"/><circle cx="652" cy="500" r="3" class="dot"/>')

svg = ' '.join((f'<svg viewBox="0 0 780 640" xmlns="http://www.w3.org/2000/svg">'
                f'{STYLE}{"".join(P)}</svg>').split())

items = [
    (1, "la cabeza", "head"), (2, "el pelo", "hair"), (3, "la cara", "face"),
    (4, "el ojo", "eye"), (5, "la nariz", "nose"), (6, "la boca", "mouth"),
    (7, "la oreja", "ear"), (8, "el cuello", "neck"), (9, "el hombro", "shoulder"),
    (10, "el brazo", "arm"), (11, "el codo", "elbow"), (12, "la mano", "hand"),
    (13, "el dedo", "finger"), (14, "el pecho", "chest"), (15, "la espalda", "back"),
    (16, "el estómago", "stomach"), (17, "la pierna", "leg"), (18, "la rodilla", "knee"),
    (19, "el pie", "foot"), (20, "el corazón", "heart"),
]

out = {
    "id": "p03",
    "title": "El cuerpo · the body",
    "intro": ("Twenty words on one drawing. Two of them break the gender rules you have "
              "learned so far: la mano ends in -o and is feminine, el pie is masculine "
              "and short. The small figure at the right exists for la espalda, which a "
              "front view cannot show."),
    "svg": svg,
    "items": [{"n": n, "es": es, "en": en} for n, es, en in items],
}
path = pathlib.Path(__file__).parent.parent / 'data/plates/p03.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("p03 svg:", len(svg), "chars")
