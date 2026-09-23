# Español para lectura

A printable A4 vocabulary booklet for a Hebrew/English speaker learning Spanish.
Latin American usage.

## Build

```sh
python3 build.py             # -> out/spanish-vocab.pdf     110 pages
python3 build.py --compact   # -> out/spanish-compact.pdf     25 pages
python3 build.py --html      # -> HTML only, for fast layout iteration
```

## Folios, running heads and the contents

Chrome does not support CSS margin boxes, so page numbers cannot be printed in
the same pass as the text. `stamp_folios` prints a second, numbers-only PDF and
merges it onto every body page with pypdf. The same pass reads back which page
each section begins on, which is what lets the contents carry real page
references: build once, learn the pagination, rebuild the contents with it,
reprint, then stamp. The title page and contents carry no folio.

## Two editions

The full edition teaches; the compact one reviews. Measured shares of the full
book's text: headwords and glosses 18%, example sentences 47%, usage notes 30%.
So the compact edition keeps all 1003 headwords, glosses, Hebrew, the irregular
`yo` form and one example per entry (two where an entry has several senses), and
drops the 753 usage notes, the surplus sentences and the plates. It also lets the
units flow continuously instead of starting each of the fifty on a fresh page,
which alone was worth a large share of the saving.

Warnings (`warn`) are kept in both editions in full. They are safety
information — `coger`, `concha`, `picante` — and compressing them would be the
wrong economy.

Requires Google Chrome, used headless to print the PDF. Chrome handles Hebrew
RTL and Spanish diacritics with system fonts; the pure-Python PDF libraries do
not. Chrome writes the file but does not reliably exit, so `build.py` waits for
the PDF to stop growing and then kills it — without that the build hangs for
minutes after the PDF is already done.

## Structure

```
data/meta.json        cover text
data/grammar.json     section G — function words, explained rather than glossed
data/units/uNN.json   themed units of ~20 words
data/plates/pNN.json  diagram plates (see below)
data/cognates.json    appendix A — words already transparent from English
```

Frequency decides *which* words are in the book. Theme decides the page order.

Two columns throughout. The build does a **measuring pass** first: it lays each
unit out in a real column width in headless Chrome, reads back the rendered
height, and solves for the type size that fills one page (clamped to 7.6–8.9pt).
Dense units get smaller type rather than an extra half-empty page.

## Diagram plates

A plate is a numbered drawing plus a key. They exist for themes with spatial
structure — a house plan, the prepositions of place — where a picture teaches
the word better than a gloss does, and links the Spanish to the thing without
routing through English.

Each plate renders **twice**: once labeled, then again with every name hidden
and the numbers left in place, as a self-test. That second page is the reason
the plates are worth their space — retrieval, not re-reading.

Plate SVG is hand-authored in the JSON. The only rule the build depends on:
**every text element naming something must carry `class="lab"`**, because the
test copy hides exactly those. `lint_plates` in `build.py` enforces this — a
missing `lab` leaks the answer onto the self-test page, which is silent and
easy to miss by eye.

Plates are for concrete, spatial vocabulary only. Do not add one for abstract
words or verbs — a vague picture next to `todavía` teaches a blur.

## Entry rules

These are conventions the content must follow; the first is enforced by a lint
in `build.py` that runs on every build.

- **One sentence per sense.** Senses are separated by `;` in the `en` field.
  Every sense needs its own example carrying a `tag` naming it. The build prints
  a warning for any entry that violates this.
- **Nouns carry their article** — `la mesa`, not `mesa`.
- **Hebrew only where English is not enough**: the gloss needs two distinct
  English senses, or English collapses a distinction Hebrew keeps
  (`esperar` = wait/hope, `saber` vs `conocer`).
- **Conjugation strips only on verbs whose forms you cannot guess.** Regular
  verbs get none. Order is yo / tú / él-ella / nosotros / ellos-ustedes.
- **Vary sentence structure** across entries — statements, questions, negatives,
  imperatives, subordinate clauses. Not twenty declaratives in a row.
- **Flag anything vulgar or regionally loaded** with the `warn` field, which
  renders as a red-ruled box. `coger` in u02 is the worked example: neutral in
  Spain, obscene across most of Latin America. Also applies to `concha`,
  `pico`, `chucha`. The rule is to say so plainly, never to quietly omit the
  word — these are common and you will meet them.

## Entry schema

```json
{
  "es": "poner",
  "pos": "v. irr.",
  "en": "to put, to place; to turn on; (ponerse) to put on, to become",
  "he": "optional Hebrew gloss",
  "note": "optional usage note, no examples inside it",
  "conj": {"label": "pres.", "forms": ["pongo", "pones", "pone", "ponemos", "ponen"]},
  "ex": [{"tag": "place", "es": "Pon el plato en la mesa.", "en": "Put the plate on the table."}]
}
```

## Status

**1003 word entries across units 01–50** — target reached. Plus 13 function
words in section G, 96 words keyed to the seven plates, and 89 in the cognate
appendix: 1105 headwords in 106 pages.

Plates: the house plan, the prepositions of place, the body, the family tree,
the clock, the place setting, and the colour swatches.

Add a unit by dropping `data/units/uNN.json` in place, a plate by dropping
`data/plates/pNN.json`. Nothing else needs touching.

### Source note

The word list is built from proofed thematic vocabulary, not from the numbered
1–1000 table that circulates on vocabulary sites. That table is an English
frequency list run through machine translation word by word, and it is wrong in
ways that would teach bad Spanish: `lata` glossed as "can" (it is a tin can;
*able to* is **poder**), `sierra` as "saw" (the tool, not the past of *see*),
`satélite` as "sat", `ahora` as "far". It is not used here.

## Regenerating a plate

The house plate is generated, not hand-edited:

```sh
python3 tools/make_p01.py   # house
python3 tools/make_p03.py   # body
python3 tools/make_p04.py   # family tree
python3 tools/make_p05.py   # clock
python3 tools/make_p06.py   # place setting
python3 tools/make_p07.py   # colours
python3 build.py
```

Placing several hundred SVG coordinates by hand inside a JSON string is
unmaintainable. Edit the script, run it, rebuild. `p02` is still inline JSON
because it is mostly `<use>` references to four reusable `<defs>` shapes.

## House style

The book is set to print conventions, not screen ones. Worth preserving if you
edit the CSS:

- Section openers are a small-caps label over the title (`UNIT 28` / *Giving,
  taking and holding*), never an inline `U28` code. Cross-references in the data
  read "see unit 28", not "see U28".
- Sense labels are italic, with no border or background. Chips are a user
  interface pattern and look wrong in print.
- Warnings must survive a black-and-white laser printer, so they carry three
  independent cues: a solid dark tab with reversed `WATCH OUT` type, a heavy
  left rule, and a light neutral tint inside a thin box. The tab and the rules
  are line art and cannot be lost; the tint halftones to a clear light grey.
  A coloured panel alone would be unreliable — a pale colour tint can vanish
  in greyscale. Verify changes by rendering a page through a grey profile:

  ```sh
  sips -s format png --matchTo \
    "/System/Library/ColorSync/Profiles/Generic Gray Gamma 2.2 Profile.icc" \
    page.pdf --out page_grey.png
  ```
- Entries are not numbered in the full edition: reference books do not number
  their headwords, and a counter running to 1003 was the clearest sign the pages
  were generated. The compact edition *does* number them, deliberately — it is a
  word list rather than a teaching text, and published frequency lists number
  their entries.
- The appendix sets four columns at full page width. It must sit outside the
  entry column flow — nested multi-column containers collapse to one column.

## Mobile edition

```sh
python3 tools/make_mobile.py   # -> docs/index.html, one self-contained file (~370 KB)
```

Not a port of the book. The PDF is the reading artifact; the phone does what
paper cannot:

- **Search** across Spanish, English, Hebrew and all 1446 example sentences,
  diacritic-insensitive (`cancion` finds `canción`). Headword matches rank first.
- **Practice** — retrieval, not recognition, in either direction. Leitner boxes
  at 0/1/3/7/21 days. New words are released 15 a day in book order, so practice
  follows the units you have read instead of dumping all 1003 on day one.
- **Browse** with a *Hide meanings* toggle for self-testing a unit.
- **Plates** with a label toggle (reusing the same `.lab` class as the printed
  self-test pages) and tap-to-zoom, since plate labels are unreadable at 390pt.

Dark mode follows the system. Plates stay on a white card in dark mode — the
drawings are coloured for paper and inverting them would ruin them.

Progress lives in `localStorage`. **Copy backup** / **Restore** on the Practice
screen move it through the clipboard, as insurance against iOS clearing storage.

Audio is deliberately left out for now. `speechSynthesis` with `lang="es-MX"`
would slot into `entryHTML` without other changes.

### Testing it at phone size

Desktop Chrome enforces a minimum window width of about 500px, so a
`--window-size=390,...` screenshot is laid out too wide and then cropped — it
looks like an overflow bug that is not there. Render the page inside a
390px-wide `<iframe>` instead; `tools/shot.py` wraps the non-hanging Chrome call.

### Hosting

`docs/` is laid out for GitHub Pages (Settings → Pages → branch `main`, folder
`/docs`). Serve over HTTPS: *Add to Home Screen* only behaves like an app, and
`localStorage` is only dependable, on a real origin rather than `file://`.
