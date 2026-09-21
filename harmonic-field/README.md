# Harmonic field wheel

Three printed parts. 3D mechanics (plain) + colored paper art glued into the recesses.

## Printing
| Part | Size | Weight |
|---|---|---|
| `field_1-BASE-DISC.stl` | Ø117.9 × 19.0 mm | ~38 g |
| `field_2-TOP-DISC.stl` | Ø110 (+tab, 120.5) × 8.0 mm | ~19 g |
| `field_3-CAP.stl` | Ø18.7 × 9.1 mm | ~2 g |

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

## The hub (threaded shaft + cap)
The snap-fit shaft is gone: its hooks were the weak point. The base now carries a **solid
Ø9.4 mm shaft** — a smooth axle as tall as the top disc, then a coarse printed thread
(3 mm pitch, 1 mm deep, flanks at ~46°, no supports). A knurled **cap nut** screws onto it.

The cap bottoms out on the **end of the shaft**, not on the disc, so it cannot be
overtightened: the disc always keeps **0.5 mm** of lift, which it needs to climb the
0.40 mm detent bumps. Radial play in the thread is 0.35 mm (`thr_c`); cap too tight on
your printer? Raise it by 0.05 and reprint only the cap (~5 min).

The top disc did not change — only the base needs reprinting. The cap is exported
roof-down, which is how it prints.

To assemble: put the top disc over the shaft and **screw the cap on, clockwise, until it
stops**.

## The two reference tables
On both sides of the center, the top disc carries the rules everybody forgets:

- **MAJOR KEY** — `I(M) T II(m) T III(m) S IV(M) T V(M) T VI(m) T VII(°) S`
- **MINOR KEY** — `I(m) T II(°) S III(M) T IV(m) T V(m) S VI(M) T VII(M) T`

Each box is a degree, with the chord quality inside it. The chip between two boxes is the
interval separating them — gray = tone, purple = semitone. The last chip closes the
octave, back to I.

`T` = tone, `S` = semitone, `M` = major, `m` = minor, `°` = diminished.
