#!/usr/bin/env bash
# Regenerates the STLs and the PDFs from source.
# Needs: openscad, python3 (colorsys/math), cairosvg, pypdf
set -euo pipefail
cd "$(dirname "$0")"
SCAD=${SCAD:-openscad}
LANGS=${LANGS:-"en pt es"}          # printed art is generated in every language
mkdir -p scale/stl scale/pdf harmonic-field/stl harmonic-field/pdf

echo "== harmonic field: mechanics"
$SCAD -o harmonic-field/stl/field_1-BASE-DISC.stl -D 'part="base"' harmonic-field/harmonic_field.scad
$SCAD -o harmonic-field/stl/field_2-TOP-DISC.stl  -D 'part="top"'  harmonic-field/harmonic_field.scad

echo "== harmonic field: art"
for L in $LANGS; do
  ( cd harmonic-field && COLOR=1 ART_LANG=$L python3 art_field.py && mv art_field.svg /tmp/field_color.svg \
                      && COLOR=0 ART_LANG=$L python3 art_field.py && mv art_field.svg /tmp/field_bw.svg )
  python3 - "$L" <<'PY'
import sys, cairosvg
L=sys.argv[1]
cairosvg.svg2pdf(url="/tmp/field_color.svg", write_to=f"harmonic-field/pdf/art-color-{L}.pdf")
cairosvg.svg2pdf(url="/tmp/field_bw.svg",    write_to=f"harmonic-field/pdf/art-bw-{L}.pdf")
PY
done

echo "== scale ruler: mechanics"
$SCAD -o scale/stl/scale_1-TRACK.stl      -D 'part="track"'    scale/scale.scad
$SCAD -o scale/stl/scale_2-SLIDER.stl     -D 'part="slider"'   scale/scale.scad
$SCAD -o scale/stl/scale_3-CASSETTE.stl   -D 'part="cassette"' scale/scale.scad
$SCAD -o scale/stl/scale_4-BLADE.stl      -D 'part="blade"'    scale/scale.scad
$SCAD -o scale/stl/scale_0-FIT-COUPON.stl -D 'part="coupon"'   scale/scale.scad

echo "== scale ruler: art"
for L in $LANGS; do
  ( cd scale && ART_LANG=$L python3 art_scale.py )
  python3 - "$L" <<'PY'
import sys, cairosvg
from pypdf import PdfWriter
L=sys.argv[1]
cairosvg.svg2pdf(url="scale/art_scale.svg",    write_to="/tmp/p1.pdf")
cairosvg.svg2pdf(url="scale/art_scale_p2.svg", write_to="/tmp/p2.pdf")
w=PdfWriter()
for f in ("/tmp/p1.pdf","/tmp/p2.pdf"): w.append(f)
w.write(f"scale/pdf/art-track-{L}.pdf"); w.close()
PY
done

echo "done."
