# Idea: several interchangeable sliders

Status: idea, not built (2026-09-24).

Only the slider carries the pattern — its holes are the only geometry that depends on the
notes. The track, the paper, the cassette and the blade are the same for any pattern. So
one track can take a **set of sliders**, each one a different system, swapped by pulling
one out of the top channel and pushing another in.

Candidates:

- **pentatonic / diatonic** — the current slider.
- **CAGED arpeggios** — only the chord tones (1, 3, 5) of the major key, so each CAGED
  box shows the chord shape inside the scale shape.
- **blues** — the minor pentatonic plus the b5.
- **harmonic / melodic minor**, **modes** — same idea, other hole sets.

What has to hold for a new slider:

- same outline and plate as `slider()` in `scale/scale.scad` (it rides in channel 3, the
  fit asserts apply unchanged);
- the KEY window and the fret windows stay where they are, so the paper keeps working;
- the shape-label recess and label change per slider (the box boundaries depend on the
  pattern).

Implementation sketch: turn the hole choice in `slider()` into a table per pattern and
add a `pattern=` parameter; `build.sh` renders one `scale_2-SLIDER-<pattern>.stl` each.
