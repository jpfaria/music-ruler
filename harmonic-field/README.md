# Harmonic field wheel

One piece. 3D mechanics (plain) + colored paper art glued into the recesses.

## Printing
| Part | Size | Weight |
|---|---|---|
| `field_1-BASE-DISC.stl` | Ø117.9 × 13.0 mm | ~37 g |
| `field_2-TOP-DISC.stl` | Ø110 (+tab, 120.5) × 8.0 mm | ~19 g |

No supports. 0.4 nozzle · 0.2 layer · **3 perimeters** · 20 %. PETG preferably.

`pdf/art-color-<lang>.pdf` (`en`, `pt`, `es`) — A4, 100 % / actual size.
- **Base (Ø104):** cut out the circle and the hole. C on the red arrow, facing the tab.
- **Top disc (Ø108):** cut out the circle, the hole and the 7 white windows.

## Reading it
Each window carries two chips:

- **white = degree in the MAJOR key**
- **black = degree in the relative MINOR key**

The key to the symbols is on the disc itself.

Cell color: 🟩 rest · 🟧 transition · 🟥 tension. Three chords change function between
the two modes and come out two-toned:

| Chord | Major | Minor |
|---|---|---|
| F | transition (IV) | rest (VI) |
| Em | rest (III) | tension (V) |
| B° | tension (VII) | transition (II) |

## Editing
`COLOR=0 python3 art_field.py` renders the black-and-white version, and `ART_LANG=pt`
(or `es`, or `en`) picks the language. The script stops if any text crosses a cut line
or overflows its cell.

## Before cutting the paper — CHECK THE SCALE
The footer of the sheet has a **100 mm bar**. Measure it with a ruler.
If it is not exactly 100 mm the PDF came out reduced: print again at **100 % scale /
actual size**, with "fit to page" UNCHECKED. Got X mm? Reprint at scale
`100 × 100 ÷ X`. The discs have to come out at **104 mm** (base) and **108 mm** (top).

That was what made the chords near the rim miss their window.

## The hub (snap fit)
The snap-fit shaft was redone: the ledge is now **0.90 mm** wide (it was 0.45) and it
starts **0.5 mm above the hub**, so it always clears the hole — the previous version got
stuck inside the hole and did not hold the top down. Reprint both parts.

To assemble: put the top disc over the shaft and **press until it clicks**.

## The two reference tables
On both sides of the center, the top disc carries the rules everybody forgets:

- **MAJOR KEY** — `I(M) T II(m) T III(m) S IV(M) T V(M) T VI(m) T VII(°) S`
- **MINOR KEY** — `I(m) T II(°) S III(M) T IV(m) T V(m) S VI(M) T VII(M) T`

Each box is a degree, with the chord quality inside it. The chip between two boxes is the
interval separating them — gray = tone, purple = semitone. The last chip closes the
octave, back to I.

`T` = tone, `S` = semitone, `M` = major, `m` = minor, `°` = diminished.
