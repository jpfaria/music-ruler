# -*- coding: utf-8 -*-
"""Track paper for the scale ruler -- LARGE version (280 x 95 mm).
   A4 LANDSCAPE, 1:1. Page 1 = two panels (one is a spare). Page 2 = legend.
   COLOR=0 renders the black-and-white version.
   ART_LANG=en|pt|es picks the language of every printed label.
   (the variable is ART_LANG and not LANG on purpose: LANG is the shell locale)"""
import colorsys, os, sys
COLOR=int(os.environ.get("COLOR","1"))
LANG =os.environ.get("ART_LANG","en")

# ---------------- printed strings, one table per language -----------------
STR={
 "en":{"open":"open",
       "p1_head":"TRACK PAPER — A4 LANDSCAPE, print at 100% / actual size. "
                 "Dashed = cut line. The lower one is a spare.",
       "p2_title":"HOW TO READ THE RULER",
       "leg":["square — major tonic","diamond — relative minor tonic",
              "circle — pentatonic note","triangle — degrees 4 and 7",
              "KEY window — the key you are in","lower windows — fret + octave twin"],
       "oct1":"the fret: on top (blue) frets 1 to 12, below (orange) frets 13 to 24.",
       "oct2":"It is the same shape in both — one octave apart.",
       "tips":["Top table: each box is a shape. TOP number = major key, BOTTOM = relative minor.",
               "The vertical lines fall on the frets two neighboring shapes share.",
               "On the 6th string the two squares sit 12 frets apart: one to the other is an octave.",
               "Every note has its own color — the same one as on the harmonic field wheel.",
               "Lowest string = bottom line. Glue the paper into the track recess."],
       "lab_title":"SHAPE LABEL — glue into the slider recess",
       "lab_note":"{w:.0f} × {h:.0f} mm · cut along the gray line · the second one is a spare",
       "lab_major":"major","lab_minor":"minor"},
 "pt":{"open":"solta",
       "p1_head":"PAPEL DO TRILHO — A4 DEITADO, imprimir em 100% / tamanho real. "
                 "Tracejado = corte. O de baixo é reserva.",
       "p2_title":"COMO LER A RÉGUA",
       "leg":["quadrado — tônica maior","losango — tônica da relativa menor",
              "círculo — nota da pentatônica","triângulo — graus 4 e 7",
              "janela TOM — a tonalidade","janelas de baixo — casa + gêmea"],
       "oct1":"a casa: em cima (azul) as casas 1 a 12, embaixo (laranja) as 13 a 24.",
       "oct2":"É a mesma forma nas duas — uma oitava de distância.",
       "tips":["Tabela do topo: cada caixa é uma forma. Número de CIMA = tom maior, de BAIXO = relativa menor.",
               "Os traços verticais caem nas casas que duas formas vizinhas dividem.",
               "Na 6ª corda os dois quadrados ficam a 12 casas: de um ao outro é uma oitava.",
               "Cada nota tem sua cor — a mesma da roda de campo harmônico.",
               "Corda mais grave = linha de baixo. Colar o papel no rebaixo do trilho."],
       "lab_title":"ETIQUETA DAS FORMAS — colar no rebaixo da régua",
       "lab_note":"{w:.0f} × {h:.0f} mm · recorte pela linha cinza · a segunda é reserva",
       "lab_major":"maior","lab_minor":"menor"},
 "es":{"open":"suelta",
       "p1_head":"PAPEL DEL RIEL — A4 HORIZONTAL, imprimir al 100% / tamaño real. "
                 "Discontinuo = corte. El de abajo es de repuesto.",
       "p2_title":"CÓMO LEER LA REGLA",
       "leg":["cuadrado — tónica mayor","rombo — tónica de la relativa menor",
              "círculo — nota de la pentatónica","triángulo — grados 4 y 7",
              "ventana TONO — la tonalidad","ventanas de abajo — traste + gemela"],
       "oct1":"el traste: arriba (azul) los trastes 1 a 12, abajo (naranja) los 13 a 24.",
       "oct2":"Es la misma forma en ambos — a una octava de distancia.",
       "tips":["Tabla de arriba: cada caja es una forma. Número de ARRIBA = tono mayor, de ABAJO = relativa menor.",
               "Las líneas verticales caen en los trastes que comparten dos formas vecinas.",
               "En la 6ª cuerda los dos cuadrados quedan a 12 trastes: de uno a otro hay una octava.",
               "Cada nota tiene su color — el mismo de la rueda de campo armónico.",
               "Cuerda más grave = línea de abajo. Pegar el papel en el rebaje del riel."],
       "lab_title":"ETIQUETA DE LAS FORMAS — pegar en el rebaje de la regla",
       "lab_note":"{w:.0f} × {h:.0f} mm · recorta por la línea gris · la segunda es de repuesto",
       "lab_major":"mayor","lab_minor":"menor"},
}
if LANG not in STR: raise SystemExit("ART_LANG must be one of: "+", ".join(STR))
S=STR[LANG]

NOTES=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def _lum(r,g,b):
    f=lambda c:(c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4)
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
SAT,VAL=0.90,0.97
def _rgb(pc):
    return colorsys.hsv_to_rgb(((((pc*7)%12)*30))/360.0, SAT, VAL)
def note_color(pc):
    r,g,b=_rgb(pc); return "#%02X%02X%02X"%(int(r*255+.5),int(g*255+.5),int(b*255+.5))
def note_ink(pc):
    return "#FFFFFF" if _lum(*_rgb(pc))<0.34 else "#141414"

TUNING=[4,9,2,7,11,4]
NF=24
CW=10.2                      # fret width
RS=11.2                      # string spacing
PW,PH=272.0,98.0
XN=21.0                      # nut
Y0=21.0                      # 1st string (highest); strings 21.0 .. 77.0
YT=9.8                       # center of the KEY strip
YN=87.5                      # center of the fret-number chip
MARKERS={3,5,7,9,12,15,17,19,21,24}
def xf(f): return XN+(f-0.5)*CW if f>0 else XN-10.0
def yi(i): return Y0+(5-i)*RS
def xs(f): return XN+(f-1.5)*CW
def key(f):
    pc=(TUNING[0]+f)%12
    return NOTES[pc], NOTES[(pc+9)%12]+"m", pc

# octave color: frets 1-12 blue, frets 13-24 orange
OCT1="#1552D8"; OCT2="#C25E00"

def panel(o,ox,oy):
    o.append(f'<g transform="translate({ox},{oy})">')
    o.append(f'<rect x="0" y="0" width="{PW}" height="{PH}" fill="#fff" stroke="#bbb" stroke-width=".3"/>')
    # KEY strip
    for f in range(1,13):
        maj,men,pc=key(f); x=xs(f)
        o.append(f'<rect x="{x-4.9:.2f}" y="{YT-4.9:.2f}" width="9.8" height="9.8" rx="2.0" '
                 f'fill="{note_color(pc) if COLOR else "#fff"}" stroke="#111" stroke-width=".4"/>')
        o.append(f'<text x="{x:.2f}" y="{YT-2.3:.2f}" font-size="4.6" fill="{note_ink(pc) if COLOR else "#111"}">{maj}</text>')
        o.append(f'<text x="{x:.2f}" y="{YT+3.0:.2f}" font-size="3.5" fill="{note_ink(pc) if COLOR else "#444"}" opacity=".85">{men}</text>')
    # neck
    for i in range(6):
        y=yi(i)
        o.append(f'<line x1="{XN}" y1="{y}" x2="{XN+NF*CW}" y2="{y}" stroke="#444" stroke-width="{0.7-0.05*i:.2f}"/>')
    for f in range(1,NF+1):
        x=XN+f*CW
        o.append(f'<line x1="{x}" y1="{Y0}" x2="{x}" y2="{Y0+5*RS}" stroke="#c4c4c4" stroke-width=".4"/>')
    o.append(f'<line x1="{XN}" y1="{Y0-2.0}" x2="{XN}" y2="{Y0+5*RS+2.0}" stroke="#222" stroke-width="2.6"/>')
    for i in range(6):
        for f in range(NF+1):
            pc=(TUNING[i]+f)%12; n=NOTES[pc]; nat=len(n)==1
            x,y=xf(f),yi(i)
            if COLOR:
                w,hh=(9.2,9.4) if f>0 else (12.2,9.4)
                o.append(f'<rect x="{x-w/2:.2f}" y="{y-hh/2:.2f}" width="{w}" height="{hh}" rx="2.4" fill="{note_color(pc)}"/>')
            o.append(f'<text x="{x}" y="{y}" font-size="{5.0 if nat else 4.1}" '
                     f'fill="{note_ink(pc) if COLOR else ("#17181A" if nat else "#969CA2")}">{n}</text>')
    # fret number (shows through the slider windows)
    for f in range(1,NF+1):
        m=f in MARKERS
        low  = f if f<=12 else f-12              # number in the 1st octave
        high = low+12                            # same shape, 12 frets up
        w,h=8.8,7.4
        x0,y0=xf(f)-w/2, YN-h/2; x1,y1=x0+w, y0+h
        # square split on the diagonal: top corner = 1st octave, bottom = 2nd
        o.append(f'<polygon points="{x0:.2f},{y0:.2f} {x1:.2f},{y0:.2f} {x0:.2f},{y1:.2f}" fill="{OCT1}"/>')
        o.append(f'<polygon points="{x1:.2f},{y0:.2f} {x1:.2f},{y1:.2f} {x0:.2f},{y1:.2f}" fill="{OCT2}"/>')
        o.append(f'<line x1="{x1:.2f}" y1="{y0:.2f}" x2="{x0:.2f}" y2="{y1:.2f}" stroke="#fff" stroke-width=".45"/>')
        o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w}" height="{h}" fill="none" '
                 f'stroke="{"#17181A" if m else "#FFFFFF"}" stroke-width="{0.8 if m else 0.35}"/>')
        o.append(f'<text x="{x0+0.29*w:.2f}" y="{y0+0.29*h:.2f}" font-size="3.0" fill="#fff">{low}</text>')
        o.append(f'<text x="{x0+0.71*w:.2f}" y="{y0+0.71*h:.2f}" font-size="3.0" fill="#fff">{high}</text>')
    o.append(f'<text x="{XN-10.0}" y="{YN}" font-size="3.4" fill="#888">{S["open"]}</text>')
    o.append('</g>')

# ---------------- shape label (glued into the slider recess) ---------------
SHAPES=[0,2,4,7,9,12]
EX0,EX1,EY0,EY1 = -65.0, 65.0, 32.6, 45.2      # same measurements as the recess in the .scad
EW,EH = EX1-EX0, EY1-EY0
SHAPE_COLORS=["#C62828","#E0670B","#1B7F3B","#1552D8","#6A2FB0"]
def _dark(c):    # deeper tone for the bottom row
    import colorsys as _c
    r,g,b=int(c[1:3],16)/255,int(c[3:5],16)/255,int(c[5:7],16)/255
    h,l,s=_c.rgb_to_hls(r,g,b); r,g,b=_c.hls_to_rgb(h,max(0,l*0.62),s)
    return "#%02X%02X%02X"%(int(r*255+.5),int(g*255+.5),int(b*255+.5))
def label(o,ox,oy,rot=True):
    xc=lambda c: -61.2+c*10.2
    o.append(f'<rect x="{ox}" y="{oy}" width="{EW}" height="{EH}" fill="#fff" '
             f'stroke="#C9CDD2" stroke-width=".35"/>')
    for n in range(5):
        a,b = ox+xc(SHAPES[n])-EX0, ox+xc(SHAPES[n+1])-EX0
        c = SHAPE_COLORS[n] if COLOR else "#fff"; c2 = _dark(SHAPE_COLORS[n]) if COLOR else "#fff"
        tx = "#fff" if COLOR else "#111"
        o.append(f'<rect x="{a:.2f}" y="{oy}" width="{b-a:.2f}" height="{EH*0.56:.2f}" fill="{c}"/>')
        o.append(f'<rect x="{a:.2f}" y="{oy+EH*0.56:.2f}" width="{b-a:.2f}" height="{EH*0.44:.2f}" fill="{c2}"/>')
        if not COLOR:
            o.append(f'<rect x="{a:.2f}" y="{oy}" width="{b-a:.2f}" height="{EH}" fill="none" stroke="#111" stroke-width=".4"/>')
            o.append(f'<line x1="{a:.2f}" y1="{oy+EH*0.56:.2f}" x2="{b:.2f}" y2="{oy+EH*0.56:.2f}" stroke="#111" stroke-width=".3"/>')
        o.append(f'<text x="{(a+b)/2:.2f}" y="{oy+EH*0.28:.2f}" font-size="5.2" fill="{tx}">{n+1}</text>')
        o.append(f'<text x="{(a+b)/2:.2f}" y="{oy+EH*0.78:.2f}" font-size="4.0" fill="{tx}">{((n+1)%5)+1}</text>')
    for n in range(6):
        x = ox+xc(SHAPES[n])-EX0
        o.append(f'<line x1="{x:.2f}" y1="{oy}" x2="{x:.2f}" y2="{oy+EH}" stroke="#fff" stroke-width=".7"/>')
    if rot:
        o.append(f'<text x="{ox-2.5:.2f}" y="{oy+EH*0.28:.2f}" font-size="3.2" fill="#666" style="text-anchor:end">{S["lab_major"]}</text>')
        o.append(f'<text x="{ox-2.5:.2f}" y="{oy+EH*0.78:.2f}" font-size="3.2" fill="#666" style="text-anchor:end">{S["lab_minor"]}</text>')

# ---------------- checks ----------------
JW,JH,JX,JYc=10.2,10.6,-71.4,39.2      # KEY window on the slider (.scad coordinates)
FW,FH,FYc=8.8,7.4,-38.5                # fret-number windows
err=[]
if abs((Y0+2.5*RS)-PH/2)>0.01: err.append('strings off the paper center -> they miss the slider holes')
if YT+4.9 > Y0-4.7-0.2: err.append("KEY strip touches the 1st string")
if YN+3.5 > PH-1.0: err.append("fret-number chip runs off the paper")
if Y0+5*RS+4.7 > YN-3.5: err.append("fret-number chip hits the 6th string")
p0,p1=PH/2-(JYc+JH/2), PH/2-(JYc-JH/2)
if not (p0<=YT-4.9 and p1>=YT+4.9): err.append(f"KEY window does not cover the cell ({p0:.2f}..{p1:.2f})")
if JW/2 >= CW-4.9: err.append("KEY window shows the neighboring cell")
q0,q1=PH/2-(FYc+FH/2), PH/2-(FYc-FH/2)
if not (q0<=YN-3.5 and q1>=YN+3.5): err.append(f"fret window does not cover the chip ({q0:.2f}..{q1:.2f})")
if xs(1)-4.9 < 0: err.append("KEY cell of fret 1 runs off the paper")
if XN+NF*CW+5 > PW: err.append("frets run past the paper width")

W,H=297.0,210.0
TXT_W=0.55                # rough character width factor, in font-size units
def _wide(t,size,x,anchor="middle"):
    """left/right edge of a text run, so a long translation cannot leave the page"""
    w=len(t)*size*TXT_W
    return (x-w/2, x+w/2) if anchor=="middle" else (x, x+w)
def check_text(name,t,size,x,anchor="middle",margin=6.0):
    a,b=_wide(t,size,x,anchor)
    if a<margin or b>W-margin: err.append(f"{name}: text spans {a:.0f}..{b:.0f} mm, outside {margin:.0f}..{W-margin:.0f}")

def page1():
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" fill="#fff"/>',
       '<style>text{font-family:"DejaVu Sans",Arial,sans-serif;font-weight:700;'
       'text-anchor:middle;dominant-baseline:central}'
       '.cut{fill:none;stroke:#e11;stroke-width:.35;stroke-dasharray:2.5 2}</style>',
       f'<text x="{W/2}" y="7" font-size="4.2" fill="#444">{S["p1_head"]}</text>']
    check_text("page 1 header",S["p1_head"],4.2,W/2)
    for oy in (12.0, 110.0):
        o.append(f'<rect x="{(W-PW)/2}" y="{oy}" width="{PW}" height="{PH}" class="cut"/>')
        panel(o,(W-PW)/2,oy)
    o.append('</svg>'); return "\n".join(o)

def page2():
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" fill="#fff"/>',
       '<style>text{font-family:"DejaVu Sans",Arial,sans-serif;font-weight:700;'
       'text-anchor:middle;dominant-baseline:central}</style>',
       f'<text x="{W/2}" y="18" font-size="8">{S["p2_title"]}</text>']
    check_text("page 2 title",S["p2_title"],8,W/2)
    def item(x,y,kind,t):
        if kind=="q": o.append(f'<rect x="{x-4.3}" y="{y-4.3}" width="8.6" height="8.6" fill="#17181A"/>')
        if kind=="l": o.append(f'<rect x="{x-3.4}" y="{y-3.4}" width="6.9" height="6.9" fill="#17181A" transform="rotate(45 {x} {y})"/>')
        if kind=="g": o.append(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#17181A"/>')
        if kind=="p": o.append(f'<polygon points="{x},{y-4.4} {x+3.8},{y+2.2} {x-3.8},{y+2.2}" fill="#17181A"/>')
        if kind=="j": o.append(f'<rect x="{x-5.3}" y="{y-5.3}" width="10.6" height="10.6" fill="none" stroke="#17181A" stroke-width="1.1"/>')
        if kind=="n": o.append(f'<rect x="{x-4.4}" y="{y-3.4}" width="8.8" height="6.8" rx="1.6" fill="none" stroke="#17181A" stroke-width="1.1"/>')
        o.append(f'<text x="{x+9}" y="{y}" font-size="5.2" fill="#222" style="text-anchor:start">{t}</text>')
        check_text(f"legend {t[:12]}",t,5.2,x+9,anchor="start")
    for k,(kd,tx) in enumerate(zip(["q","l","g","p","j","n"],S["leg"])):
        item(18 if k<3 else 168, 36+(k%3)*16, kd, tx)
    cw,ch,cx,cy=17.6,14.8,20,92
    o.append(f'<polygon points="{cx},{cy} {cx+cw},{cy} {cx},{cy+ch}" fill="{OCT1}"/>')
    o.append(f'<polygon points="{cx+cw},{cy} {cx+cw},{cy+ch} {cx},{cy+ch}" fill="{OCT2}"/>')
    o.append(f'<line x1="{cx+cw}" y1="{cy}" x2="{cx}" y2="{cy+ch}" stroke="#fff" stroke-width=".9"/>')
    o.append(f'<text x="{cx+0.29*cw}" y="{cy+0.29*ch}" font-size="6.0" fill="#fff">5</text>')
    o.append(f'<text x="{cx+0.71*cw}" y="{cy+0.71*ch}" font-size="6.0" fill="#fff">17</text>')
    for k,t in enumerate((S["oct1"],S["oct2"])):
        o.append(f'<text x="{cx+cw+6}" y="{cy+ch/2-3+7*k}" font-size="5.2" fill="#222" style="text-anchor:start">{t}</text>')
        check_text(f"octave note {k}",t,5.2,cx+cw+6,anchor="start")
    for k,t in enumerate(S["tips"]):
        o.append(f'<text x="{W/2}" y="{120+k*10}" font-size="5.0" fill="#333">{t}</text>')
        check_text(f"tip {k}",t,5.0,W/2)
    o.append(f'<text x="{W/2}" y="176" font-size="6">{S["lab_title"]}</text>')
    check_text("label title",S["lab_title"],6,W/2)
    note=S["lab_note"].format(w=EW,h=EH)
    o.append(f'<text x="{W/2}" y="183" font-size="4.2" fill="#666">{note}</text>')
    check_text("label note",note,4.2,W/2)
    label(o, 24.0, 190.0, True)
    label(o, 162.0, 190.0, False)
    o.append('</svg>'); return "\n".join(o)

svg1,svg2=page1(),page2()
if err: raise SystemExit("ERROR: "+" | ".join(err))
open("art_scale.svg","w",encoding="utf-8").write(svg1)
open("art_scale_p2.svg","w",encoding="utf-8").write(svg2)
print(f"ok ({LANG}, color={COLOR})  KEY window sees {p0:.1f}..{p1:.1f} | "
      f"fret window sees {q0:.1f}..{q1:.1f} | panel {PW:.0f} x {PH:.0f} mm")
