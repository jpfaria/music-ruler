#!/usr/bin/env bash
# Regera STLs e PDFs a partir das fontes.
# Precisa de: openscad, python3 (colorsys/math), cairosvg, pypdf
set -euo pipefail
cd "$(dirname "$0")"
SCAD=${SCAD:-openscad}

echo "== roda: mecanica"
$SCAD -o roda/stl/roda_1-DISCO-BASE.stl      -D 'part="base"' roda/roda.scad
$SCAD -o roda/stl/roda_2-DISCO-GIRATORIO.stl -D 'part="top"'  roda/roda.scad

echo "== roda: arte"
( cd roda && COR=1 python3 arte.py && mv arte_roda.svg /tmp/roda_cor.svg \
           && COR=0 python3 arte.py && mv arte_roda.svg /tmp/roda_pb.svg )
python3 - <<'PY'
import cairosvg
cairosvg.svg2pdf(url="/tmp/roda_cor.svg", write_to="roda/pdf/arte-colorida.pdf")
cairosvg.svg2pdf(url="/tmp/roda_pb.svg",  write_to="roda/pdf/arte-preto-e-branco.pdf")
PY

echo "== regua: mecanica"
$SCAD -o regua/stl/regua_1-TRILHO.stl            -D 'part="trilho"' regua/regua.scad
$SCAD -o regua/stl/regua_2-REGUA-DESLIZANTE.stl  -D 'part="regua"'   regua/regua.scad
$SCAD -o regua/stl/regua_3-CORTINA.stl           -D 'part="cortina"' regua/regua.scad

echo "== regua: arte"
( cd regua && python3 arte_regua.py )
python3 - <<'PY'
import cairosvg
from pypdf import PdfWriter
cairosvg.svg2pdf(url="regua/arte_regua.svg",    write_to="/tmp/p1.pdf")
cairosvg.svg2pdf(url="regua/arte_regua_p2.svg", write_to="/tmp/p2.pdf")
w=PdfWriter()
for f in ("/tmp/p1.pdf","/tmp/p2.pdf"): w.append(f)
w.write("regua/pdf/arte-trilho.pdf"); w.close()
PY

echo "pronto."
