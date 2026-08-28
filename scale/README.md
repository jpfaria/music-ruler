# Scale ruler — track + slider + shutters

Same logic as the wheel: one fixed layer carrying all the information, moving layers
that crop it.

## Printing
| Part | Size | Weight | Quantity |
|---|---|---|---|
| `scale_1-TRACK.stl` | 280 × 108 × 7.2 mm | ~54 g | 1 |
| `scale_2-SLIDER.stl` | 154 × 96.5 × 2.4 mm | ~12 g | 1 |
| `scale_3-SHUTTER.stl` | 112 × 97.7 × 1.8 mm | ~8 g | **2** |
| `scale_0-FIT-COUPON.stl` | 144 × 108 × 7.2 mm | ~9 g | 1, first |

**Print the fit coupon first.** `scale_0-FIT-COUPON.stl` is a 40 mm stub of the track
plus a 40 mm section of each plate — ten minutes. Slide each plate into the stub: it has
to run freely end to end and not lift out. Only then print the real parts. Too tight?
Raise `FIT` in the `.scad` by 0.05 and print the coupon again.

No supports on any part. 0.4 nozzle · 0.16 layer · 3 perimeters · 20 %. **PETG.**
The track is 280 mm long — use a **5 mm brim**, bed at 80 °C and a closed chamber,
otherwise the ends lift.

`pdf/art-track-<lang>.pdf` (`en`, `pt`, `es`) — **A4 LANDSCAPE**, 100 % / actual size.
Page 1 carries the two panels, page 2 the legend. Cut out one of the two rectangles
(the other is a spare) and glue it into the track recess.

### Assembly
Glue the **shape label** into the recess on top of the slider before assembling (page 2
of the PDF). The track has **two stacked channels**, each with a dovetail profile:

1. **bottom channel** — the two shutters go in, sliding from one of the ends
2. **top channel** — the slider goes in the same way

Nothing comes out through the top: the channel closes at 45° and each plate is wider at
its base than at the mouth. Nothing is bridged in mid-air — that is exactly what came
out badly in the previous version, a 1.5 mm bridge printed over thin air.

## How it works
The track carries the **24-fret note map**. The slider has holes at the notes of the
scale. You slide until the tonic lands in the right hole — and the 5 shapes place
themselves.

**Square = MAJOR tonic. Diamond = relative MINOR tonic.**

- Line a **square** up over G → G major scale.
- Line a **diamond** up over E → E minor scale.

### Which key am I in — the KEY window
The top left corner of the slider has a **window marked KEY**. The track paper carries a
strip of keys along the top, and the window frames exactly one of them: you read `C` on
top and `Am` underneath, and that is it — the major key and the relative minor of that
position. Nothing to count.

Slide the ruler one fret to the right and the window turns into `C#` / `A#m`, and so on.
The 12 useful positions are frets 1 to 12; from 13 on it repeats one octave up.

### Where each shape starts and ends
The top of the slider has a **table of 5 boxes**. Each box is one shape: where the box
starts the shape starts, where it ends the shape ends. **Top number = major key**,
**bottom = relative minor**.

The vertical lines fall on the **boundary frets**, which belong to both neighboring
shapes — that is why the shapes join up instead of floating apart.

### Which fret am I on
Along the bottom edge of the slider there is **one window per column**. Each one shows a
square split on the diagonal with **two** frets: on top, blue, the fret from 1 to 12;
below, orange, its twin from 13 to 24. Same shape, 12 frets apart.

This settles the most common confusion with the piece: the ruler shows **one octave of
the major key**, so in `C / Am` it covers frets 8 to 20. The Am tonic sits 3 frets before
the C, on fret 5 — outside the window. That is why **shape 1 of Am shows up on fret 17**
and not on 5. It is not another shape: 17 − 12 = 5.

On the 6th string the **two squares** sit 12 frets apart: from one to the other is an
octave — that is where the scale closes and starts over.

### Seeing one shape only — the shutters
The two shutters run in the bottom channel, **between the paper and the slider**. They
cover the paper, so through the slider holes you see their blank face instead of the note.

Push one in from each side until they meet around the shape you want to study: only that
box stays alive, the rest of the neck goes dark. To see everything again, push both back
out to the ends.

Each shutter has a slot on top and another at the bottom, so the **shape table and the
fret numbers stay visible** the whole time — and the slots are where you put your finger
to push (there is no raised grip, it would hit the slider).

None of this is engraved into the plastic: the full legend is on page 2 of the A4 sheet.

It is a single piece because the natural minor uses the same notes as its relative major
— the same reason the wheel shows both fields at once.

## The holes
| Hole | What it is |
|---|---|
| Big square | major tonic |
| Diamond | relative minor tonic |
| Circle | pentatonic note |
| **Triangle** | degrees 4 and 7 — the full scale only |

Ignore the triangles and you are playing the pentatonic; use every hole and you get the
full scale.

## The 5 shapes
The table on top of the slider is a **paper label** (130 × 13 mm) glued into a recess —
it comes out in color, one color per shape, instead of engraved into the plastic. It is
on page 2 of `art-track-<lang>.pdf`, with a spare copy.

It is a grid of 5 boxes. **Top row = numbering for the major key, bottom row = for the
relative minor** — the shapes are the same, only where you start counting changes:

| major | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **minor** | 2 | 3 | 4 | 5 | 1 |

The vertical lines fall on the boundary frets, which belong to **both** neighboring
shapes — that is where you join one to the next without stopping the phrase.

## Why it works in all 12 keys
Because the fret spacing is **uniform** — this is not a model of a real neck. Sliding
1 fret = going up 1 semitone, and the drawing still lines up. On a real neck, where the
spacing is logarithmic, this would not work.

## Tuning it (`.scad`)
- Anything stuck or rattling → **`FIT`**, the side clearance per side (0.15 mm). Both plate
  widths are derived from it, so the dovetail grip follows automatically: 1.15 mm per
  side, almost 8× the play. In v3 they were hand-typed at 0.8 mm of play against 0.5 mm
  of grip — a plate could slide off its own ledge, which is why everything fell apart.
  `assert()`s at the top now refuse to build that geometry.
- A plate can only rise by `FIT` before its shoulder wedges under the 45° wall, so the
  shutter never reaches the slider above it: they always clear each other by 0.15 mm.
- Dovetail deeper → increase the difference `C1-T1` (1.3 mm of ramp per side today)
- Bigger/smaller piece → change `CW` and `RS` in the `.scad` **and** in `art_scale.py` (they have to match)
- Thicker paper → `PAP` from 0.35 to your paper thickness
- Another tuning → `TUNING` (pitch class, from the lowest string to the highest) in the `.scad` **and** in `art_scale.py`
