# Scale ruler — track + cassette + blade + slider

Same logic as the wheel: one fixed layer carrying all the information, moving layers
that crop it.

## Printing
| Part | Size | Weight | Quantity |
|---|---|---|---|
| `scale_1-TRACK.stl` | 280 × 108 × 11.4 mm | ~60 g | 1 |
| `scale_2-SLIDER.stl` | 154 × 97.0 × 2.4 mm | ~26 g | 1 |
| `scale_3-CASSETTE.stl` | 224 × 97.0 × 1.8 mm | ~32 g | 1 |
| `scale_4-BLADE.stl` | 181 × 97.0 × 1.8 mm | ~4 g | 1 |
| `scale_0-FIT-COUPON.stl` | 125 × 108 × 9.8 mm | ~10 g | 1, first |

**Print the fit coupon first.** `scale_0-FIT-COUPON.stl` is a 20 mm stub of the track
plus a section of each of the three plates. Slide each one into its own channel: it has to
run freely, not lift out, and sit flat on the recessed floor. Only then print the real
parts. Too tight? Raise `FIT` in the `.scad` by 0.05 and print the coupon again.

The coupon carries only what the fit depends on — the three dovetail profiles, the
recessed floor and the full width of each plate. The 3 mm of base under the channel is
shaved to 1 mm and the plate sections are hollow between their edge rails.

No supports on any part. 0.4 nozzle · 0.16 layer · 3 perimeters · 20 %. **PETG.**
The track is 280 mm long — use a **5 mm brim**, bed at 80 °C and a closed chamber,
otherwise the ends lift.

`pdf/art-track-<lang>.pdf` (`en`, `pt`, `es`) — **A4 LANDSCAPE**, 100 % / actual size.
Page 1 carries the two panels, page 2 the legend. Cut out one of the two rectangles
(the other is a spare) and glue it into the track recess.

### Assembly
Glue the **shape label** into the recess on top of the slider before assembling (page 2
of the PDF). The track has **three stacked channels**, each with its own dovetail profile
all three with the same profile — the plates are interchangeable:

1. **bottom channel** — the cassette, sliding in from one of the ends
2. **middle channel** — the blade, tails first
3. **top channel** — the slider, the same way

Three channels instead of two is not decoration. With the masks sharing one channel they
could not cross each other, so each had to cover the worst case on its own and each one
disappeared under the slider when it did. One channel per part removes both limits.

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

### Seeing one shape only — the cassette and the blade
The cassette runs in the bottom channel, **between the paper and the slider**. It is two
masks rigidly joined, with a **4-fret window** between them: where a mask covers the paper
you see its blank face through the slider holes, and where the window is you see the
notes. Slide it until the window lands on the box you want — one move, and the rest of
the neck goes dark.

The five CAGED boxes are not all the same width. Because neighbouring shapes share their
boundary fret, three of them are 3 frets wide and two are 4:

| shape (major) | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| frets | 3 | 3 | **4** | 3 | **4** |

So the window is cut to the widest, and for the 3-fret shapes the **blade** — one fret
wide, in the middle channel — closes the leftover column. On the 4-fret shapes you park
it out at the end of the track.

The blade always ends up under the slider, where you cannot reach it, and there is no free
band on the slider to run a pin through: the note holes, the KEY window, the fret windows
and the dovetail rails use all of it. So the blade carries **two tails** instead, each one
keeping the dovetail edge profile so it rides in the channel rather than hanging off the
mask. They run under the solid bottom rail of the slider, invisible from above, and at
least one of them always sticks out past the slider. **Pull a tail; do not push it.**

Both masks are cut away above and below the note band, so the **shape table, the KEY
window and the fret numbers stay readable** the whole time — and those openings are where
you put your finger to move the cassette.

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
- Anything stuck or rattling → **`FIT`**, the side clearance per side (0.50 mm). All three
  plate widths are derived from it (`PLATE(k) = CH(k) - FIT`), and the dovetail grip
  follows: 1.5 mm per side on every level. Print the coupon before trusting a new value.
- **A plate does not rest on the channel floor — it rests on the ledge** between the mouth
  of the channel below and the floor of its own, and that ledge is `H-V` wide. Stepping
  each level inwards eats it: at 0.6 mm per level the ledge left only 0.25 mm under the
  plate's bottom face, and −0.25 mm once the plate was pushed sideways by `FIT`, so the
  blade and the slider simply dropped into the channel below. `LSTEP` is 0 and `BEAR(k)`
  is asserted for that reason.
- **Do not treat `FIT` as a CAD number.** A PETG plate leaves the bed wider than the model
  and the channel comes out narrower; 0.15 and 0.25 per side both printed too tight to
  slide. The bottom edge of every plate also carries a `BCHF` relief so the squished first
  layer has somewhere to go other than into the channel wall.
- In v3 the widths were hand-typed: 0.8 mm of play against 0.5 mm of grip, so a plate
  could slide off its own ledge. `assert()` now refuses any geometry where a plate shoved
  fully to one side has less than 0.5 mm of engagement left on the other.
- A plate can only rise by `FIT` before its shoulder wedges under the 45° wall, and each
  channel is 0.3 mm taller than the plate needs, so no plate ever touches the one running
  above it.
- The paper recess spans the **whole** channel floor (`PAPW = 2*C0`) and ramps up at both
  ends. A recess narrower than the cassette would leave two thin ledges for it to balance
  on: under the slider it stays flat, and the moment it slides out from under it, it tips
  and drops into the recess. An `assert()` refuses any geometry where the cassette is wider
  than the recess. Paper thickness no longer matters to the mechanism — thin paper just
  means every plate sits a fraction lower, still supported edge to edge.
- Dovetail deeper → increase the difference `C1-T1` (1.3 mm of ramp per side today)
- Bigger/smaller piece → change `CW` and `RS` in the `.scad` **and** in `art_scale.py` (they have to match)
- Thicker paper → `PAP` from 0.35 to your paper thickness
- Another tuning → `TUNING` (pitch class, from the lowest string to the highest) in the `.scad` **and** in `art_scale.py`
