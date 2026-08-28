# -*- coding: utf-8 -*-
"""1:1 art for the harmonic field wheel (A4).
   COLOR=0 renders the black-and-white version.
   ART_LANG=en|pt|es picks the language of every printed label.
   (the variable is ART_LANG and not LANG on purpose: LANG is the shell locale)"""
import math, os, sys, colorsys

COLOR = int(os.environ.get("COLOR","1"))
LANG  = os.environ.get("ART_LANG","en")

# ---------------- printed strings, one table per language -----------------
STR={
 "en":{"title":"HARMONIC FIELD",
       "major_key":"MAJOR KEY", "minor_key":"MINOR KEY", "rel_minor":"RELATIVE MINOR",
       "rest":"REST", "transition":"TRANSITION", "tension":"TENSION",
       "key_qual":"M = major · m = minor · ° = diminished",
       "key_step":"T = tone · S = semitone",
       "base_note":"BASE (D104) — glue into the recess with C on the arrow, facing the tab",
       "top_note":"TOP DISC (D108) — cut out the circle, the hole and the 7 white windows",
       "ruler":"MEASURE THIS BAR WITH A RULER: it has to be exactly 100 mm.",
       "ruler2":"Shorter than that and the PDF was scaled down — print again at 100% scale / "
                "actual size (uncheck “Fit to page”).",
       "ruler3":"Got X mm? Reprint at scale = 100 × 100 ÷ X. Check: base disc = 104 mm, top disc = 108 mm.",
       "footer":"Dashed = cut line.  |  Only IIIm and VII carry a b9 — that is why they are the tensest degrees."},
 "pt":{"title":"CAMPO HARMÔNICO",
       "major_key":"TOM MAIOR", "minor_key":"TOM MENOR", "rel_minor":"RELATIVA MENOR",
       "rest":"REPOUSO", "transition":"TRANSIÇÃO", "tension":"TENSÃO",
       "key_qual":"M = maior · m = menor · ° = diminuto",
       "key_step":"T = tom · S = semitom",
       "base_note":"BASE (D104) — colar no rebaixo com o C na seta, virado para a aba",
       "top_note":"DISCO DE CIMA (D108) — recortar o círculo, o furo e as 7 janelas brancas",
       "ruler":"MEÇA ESTA BARRA COM UMA RÉGUA: tem de dar 100 mm exatos.",
       "ruler2":"Se deu menos, o PDF saiu reduzido — imprima de novo com Escala 100% / "
                "Tamanho real (desmarque “Ajustar à página”).",
       "ruler3":"Deu X mm? Reimprima com escala = 100 × 100 ÷ X. Conferência: disco da base = 104 mm, disco de cima = 108 mm.",
       "footer":"Tracejado = linha de corte.  |  Só o IIIm e o VII têm b9 — por isso são os graus mais tensos."},
 "es":{"title":"CAMPO ARMÓNICO",
       "major_key":"TONO MAYOR", "minor_key":"TONO MENOR", "rel_minor":"RELATIVO MENOR",
       "rest":"REPOSO", "transition":"TRANSICIÓN", "tension":"TENSIÓN",
       "key_qual":"M = mayor · m = menor · ° = disminuido",
       "key_step":"T = tono · S = semitono",
       "base_note":"BASE (D104) — pegar en el rebaje con la C en la flecha, hacia la pestaña",
       "top_note":"DISCO SUPERIOR (D108) — recortar el círculo, el agujero y las 7 ventanas blancas",
       "ruler":"MIDE ESTA BARRA CON UNA REGLA: tiene que dar 100 mm exactos.",
       "ruler2":"Si salió menos, el PDF se redujo — imprime de nuevo con Escala 100% / "
                "Tamaño real (desmarca “Ajustar a la página”).",
       "ruler3":"¿Dio X mm? Reimprime con escala = 100 × 100 ÷ X. Control: disco base = 104 mm, disco superior = 108 mm.",
       "footer":"Discontinuo = línea de corte.  |  Solo IIIm y VII llevan b9 — por eso son los grados más tensos."},
}
if LANG not in STR: raise SystemExit("ART_LANG must be one of: "+", ".join(STR))
S=STR[LANG]

# ---------------- musical content -----------------------------------------
CIRC=["C","G","D","A","E","B","Gb/F#","Db","Ab","Eb","Bb","F"]
MIN =["Am","Em","Bm","F#m","C#m","G#m","Ebm","Bbm","Fm","Cm","Gm","Dm"]
DIM =["B","F#","C#","G#","D#","A#","F","C","G","D","A","E"]
# per window column (-30, 0, +30): roman numeral, extension (7th chord + 9th), function
# roman numerals are ALWAYS uppercase (Brazilian notation); the chord quality comes
# from the suffix next to it and from the chord name showing in the window
# Each face carries one mode only. The chord is the same in both -- what changes
# is the degree and the function.
# WHITE chip = degree in the major key | BLACK chip = degree in the relative minor.
TITLE=S["title"]
L1=[("IV","VI","7M(9)","S","T"), ("I","III","7M(9)","T","T"), ("V","VII","7(9)","D","D")]
L2=[("II","IV","m7(9)","S","S"), ("VI","I","m7(9)","T","T"), ("III","V","m7(b9)","T","D")]
L3=("VII","II","m7(b5b9)","D","S")     # only IIIm and VII take a b9 -- the tensest degrees

# ---------------- geometry (matches scale.scad) ---------------------------
R_PAP_BASE=52.0 ; R_HOLE_BASE=5.5
R_PAP_TOP =54.0 ; R_HOLE_TOP =9.5
W1=(40.5,49.0,13) ; W2=(25.5,34.5,13) ; W3=(10.5,20.0,13)     # openings
CEL1=(40.0,54.0,15) ; CEL2=(24.5,39.0,15) ; CEL3=(9.5,24.0,34) # colored area
A1=(37.5,51.6) ; A2=(22.8,36.8) ; A3=(8.2,22.2)                # base rings (slack for scale error)
RT1,RT2,RT3 = 44.75, 30.0, 15.25   # exact center of each window
FX1,FX2,FX3 = 51.4, 36.75, 22.0                                # label line
SR1,SR2,SR3 = 3.2, 2.7, 2.7                                    # roman numeral size
SE1,SE2,SE3 = 2.7, 2.1, 2.2                                    # extension size

def hsl(h,s_,l_):
    r,g,b=colorsys.hls_to_rgb((h%360)/360.0,l_,s_)
    return "#%02X%02X%02X"%(int(r*255),int(g*255),int(b*255))
def pos_color(p,ring_n): return hsl(p*30,0.72,{1:0.885,2:0.815,3:0.735}[ring_n])
C_T="#2E7D32"; C_S="#E36A0B"; C_D="#C62828"
FUN={"T":C_T,"S":C_S,"D":C_D}

W,H=210,297
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="#fff"/>',
   '<style>text{font-family:"DejaVu Sans",Arial,sans-serif;font-weight:700;'
   'text-anchor:middle;dominant-baseline:central}'
   '.cut{fill:none;stroke:#C9CDD2;stroke-width:.35}'
   '.rib{stroke:#222;stroke-width:.5}.ring{fill:none;stroke:#222;stroke-width:.5}</style>']

WID={"Ô":.60,"i":.30,"l":.30,".":.30,"°":.36,"I":.36," ":.34,"(":.38,")":.38,",":.30,
     "m":.88,"M":.88,"W":.88,"D":.70,"7":.60,"5":.60,"9":.60,"b":.62,"V":.66,"v":.58}
def wid(t,s): return sum(WID.get(c,.60) for c in t)*s
def esc(t): return t.replace("&","&amp;").replace("<","&lt;")
def g(cx,cy): o.append(f'<g transform="translate({cx},{cy})">')
def e(): o.append('</g>')
def txt(a,r,t,s,fill="#111"):
    o.append(f'<g transform="rotate({a})"><text y="{-r}" font-size="{s}" fill="{fill}">{esc(t)}</text></g>')
def ring(r): o.append(f'<circle r="{r}" class="ring"/>')
def cut(r):  o.append(f'<circle r="{r}" class="cut"/>')
def rib(a,r0,r1): o.append(f'<g transform="rotate({a})"><line y1="{-r0}" y2="{-r1}" class="rib"/></g>')
def pol(a,r):
    return f"{r*math.sin(math.radians(a)):.2f},{-r*math.cos(math.radians(a)):.2f}"
def band(R,a0,a1,w,color):
    if not COLOR: return
    d=f"M {pol(a0,R)} A {R},{R} 0 {1 if a1-a0>180 else 0} 1 {pol(a1,R)}"
    o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"/>')
def window(ri,ro,half,ang=0):
    p=[pol(a+ang,ro) for a in [half-i*(2*half/48) for i in range(49)]]
    p+=[pol(a+ang,ri) for a in [-half+i*(2*half/48) for i in range(49)]]
    pts=" ".join(p)
    o.append(f'<polygon points="{pts}" style="fill:#fff;stroke:#fff;stroke-width:1.2"/>')
    o.append(f'<polygon points="{pts}" class="cut" style="fill:none"/>')
def arc(t,r,ac,s,fill="#111",x0=None):
    """text along the arc; x0 = starting offset in mm (otherwise centered)"""
    ws=[WID.get(c,.60)*s for c in t]
    x=(-sum(ws)/2) if x0 is None else x0
    for c,w in zip(t,ws):
        cx=x+w/2; x+=w
        if c!=" ":
            o.append(f'<g transform="rotate({ac+math.degrees(cx/r)})">'
                     f'<text y="{-r}" font-size="{s}" fill="{fill}">{esc(c)}</text></g>')

errors=[]
def check(name,lo,hi,lim_i,lim_e):
    if lo<lim_i or hi>lim_e: errors.append(f"{name}: {lo:.1f}..{hi:.1f} outside {lim_i:.1f}..{lim_e:.1f}")
def check_flat(name,y,t,s,lim,x0=0.0,hole=0.0):
    """flat text: checks the outer edge AND the center hole"""
    ext=math.hypot(abs(y)+0.55*s, abs(x0)+wid(t,s)/2)
    if ext>lim: errors.append(f"{name}: corner at {ext:.1f} > {lim:.1f}")
    if hole and abs(y)-0.55*s < hole+0.8:
        errors.append(f"{name}: touches the center hole ({abs(y)-0.55*s:.1f} < {hole+0.8:.1f})")

DARK="#17181A"
def chip(ang,r,text,sz,color,minor=False):
    """white = degree in the major key | black = degree in the relative minor key"""
    pw=wid(text,sz)+2.4; ph=sz*1.30
    bg   = DARK if minor else "#fff"
    ink  = "#fff" if minor else (color if COLOR else "#111")
    o.append(f'<g transform="rotate({ang})"><rect x="{-pw/2:.2f}" y="{-r-ph/2:.2f}" '
             f'width="{pw:.2f}" height="{ph:.2f}" rx="{ph*0.3:.2f}" fill="{bg}" '
             f'stroke="#fff" stroke-width="{0.45 if minor else 0}"/></g>')
    o.append(f'<g transform="rotate({ang})"><text y="{-r}" font-size="{sz}" '
             f'fill="{ink}">{esc(text)}</text></g>')
    return pw, ph

def cell(ang,r,gM,gm,ext,fM,fm,sr,se,lim_i,lim_e,half=15):
    pwM=wid(gM,sr)+2.4; pwm=wid(gm,sr)+2.4; we=wid(ext,se); ph=sr*1.30
    tot=pwM+0.6+pwm+0.9+we; x=-tot/2
    chip(ang+math.degrees((x+pwM/2)/r), r, gM, sr, FUN[fM]);              x+=pwM+0.6
    chip(ang+math.degrees((x+pwm/2)/r), r, gm, sr, FUN[fm], minor=True);  x+=pwm+0.9
    arc(ext,r,ang,se,"#fff" if COLOR else "#111",x0=x)
    check(f"cell {gM}/{gm}", r-ph/2, r+ph/2, lim_i, lim_e)
    check(f"ext {gM}/{gm}",  r-0.55*se, r+0.55*se, lim_i, lim_e)
    room=2*half*math.pi*r/180.0
    if tot > room-0.6: errors.append(f"label {gM}/{gm}: {tot:.1f}mm does not fit in {room:.1f}mm")

def cell_bg(R,a,half,w,fM,fm):
    """if the function changes between major and minor, the cell comes out two-toned"""
    if fM==fm: band(R,a-half,a+half,w,FUN[fM])
    else:      band(R,a-half,a,w,FUN[fM]); band(R,a,a+half,w,FUN[fm])

# ===================== 1. BASE DISC (D104) ================================
g(W/2,58)
for p in range(12):
    for ring_n,(r0,r1) in ((1,A1),(2,A2),(3,A3)):
        band((r0+r1)/2,p*30-15,p*30+15,r1-r0,pos_color(p,ring_n))
cut(R_PAP_BASE); cut(R_HOLE_BASE)
for r in A1+A2+A3: ring(r)
for p in range(12):
    for (r0,r1) in (A1,A2,A3): rib(p*30+15,r0,r1)
    m=CIRC[p]
    txt(p*30,RT1,m,5.6 if len(m)>2 else 8.6)
    txt(p*30,RT2,MIN[p],5.6)
    txt(p*30,RT3,DIM[p]+"°",3.4)
o.append('<polygon points="0,-8.6 -1.6,-6.2 1.6,-6.2" fill="#8A9099"/>')
o.append(f'<text y="-56" font-size="3.2" fill="#8A9099">{esc(S["base_note"])}</text>')
e()

# ============ 2. TOP DISC LABEL (D108) ====================================
g(W/2,196)
for i,a in enumerate((-30,0,30)):
    cell_bg((CEL1[0]+CEL1[1])/2,a,CEL1[2],CEL1[1]-CEL1[0],L1[i][3],L1[i][4])
    cell_bg((CEL2[0]+CEL2[1])/2,a,CEL2[2],CEL2[1]-CEL2[0],L2[i][3],L2[i][4])
cell_bg((CEL3[0]+CEL3[1])/2,0,CEL3[2],CEL3[1]-CEL3[0],L3[3],L3[4])
cut(R_PAP_TOP); cut(R_HOLE_TOP)
for i,a in enumerate((-30,0,30)):
    window(W1[0],W1[1],W1[2],a); window(W2[0],W2[1],W2[2],a)
window(W3[0],W3[1],W3[2])
for i,a in enumerate((-30,0,30)):
    cell(a,FX1,*L1[i],SR1,SE1,W1[1],CEL1[1])
    cell(a,FX2,*L2[i],SR2,SE2,W2[1],CEL2[1])
cell(0,FX3,*L3,SR3,SE3,W3[1],CEL3[1],half=CEL3[2])

# ---------------- interval and quality tables ------------------------------
DEGREES=["I","II","III","IV","V","VI","VII"]
STEP_MAJ=["T","T","S","T","T","T","S"]
STEP_MIN=["T","S","T","T","S","T","T"]
QUAL_MAJ=["M","m","m","M","M","m","°"]
QUAL_MIN=["m","°","M","m","m","M","M"]
C_TONE="#3F4A57"; C_SEMI="#7C3AED"   # neutral: never confused with rest/transition/tension

BOXES=[]
def _box(name,x0,y0,x1,y1):
    BOXES.append((name,min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)))
    for X in (x0,x1):
        for Y in (y0,y1): _fits(X,Y,name)
def _overlaps():
    for i in range(len(BOXES)):
        for j in range(i+1,len(BOXES)):
            n1,a0,b0,a1,b1=BOXES[i]; n2,c0,d0,c1,d1=BOXES[j]
            if a1>c0+0.01 and c1>a0+0.01 and b1>d0+0.01 and d1>b0+0.01:
                errors.append(f"overlap: {n1} x {n2}")

def _fits(x,y,name):
    """the corner has to stay on the paper and clear the fan of windows"""
    r=math.hypot(x,y)
    if r>R_PAP_TOP-1.0: errors.append(f"{name}: corner at {r:.1f} > {R_PAP_TOP-1.0:.1f}")
    if r>W3[0]-1.0 and r<W1[1]+1.0:
        a=math.degrees(math.atan2(x,-y))
        if abs(a)<46.0: errors.append(f"{name}: corner runs into the fan (angle {a:.0f}, r {r:.1f})")

SG=2.6; SQ=2.3; SI=2.3          # sizes: degree / quality / interval
BH=8.0; CW_=2.9; CH_=3.9; GAP=0.4
def _table_w():
    w=sum(wid(g,SG)+1.7 for g in DEGREES)+7*CW_+13*GAP
    return w
def table(cy,label,steps,quals):
    """aligned strip: degree box (quality inside it) + interval chip"""
    tot=_table_w(); x=-tot/2
    o.append(f'<text y="{cy-BH/2-2.6}" font-size="2.8">{esc(label)}</text>')
    for k,gr in enumerate(DEGREES):
        bw=wid(gr,SG)+1.7
        o.append(f'<rect x="{x:.2f}" y="{cy-BH/2:.2f}" width="{bw:.2f}" height="{BH}" rx="1.5" '
                 f'fill="#fff" stroke="#17181A" stroke-width=".45"/>')
        o.append(f'<text x="{x+bw/2:.2f}" y="{cy-1.6:.2f}" font-size="{SG}">{gr}</text>')
        o.append(f'<text x="{x+bw/2:.2f}" y="{cy+2.4:.2f}" font-size="{SQ}" fill="#17181A">{quals[k]}</text>')
        x+=bw+GAP
        it=steps[k]; c=(C_SEMI if it=="S" else C_TONE) if COLOR else "#111"
        st = "" if COLOR else ' stroke="#111" stroke-width=".4"'
        o.append(f'<rect x="{x:.2f}" y="{cy-CH_/2:.2f}" width="{CW_}" height="{CH_}" rx="1.2" '
                 f'fill="{c}"{st}/>')
        o.append(f'<text x="{x+CW_/2:.2f}" y="{cy:.2f}" font-size="{SI}" '
                 f'fill="{"#fff" if COLOR else "#111"}">{it}</text>')
        x+=CW_+GAP
    _box(label, -tot/2, cy-BH/2-4.2, tot/2, cy+BH/2)

# --- center: title plus the two tables ---
TY=13.0
o.append(f'<text y="{TY}" font-size="3.8">{esc(TITLE)}</text>')
check_flat("title", TY, TITLE, 3.8, R_PAP_TOP, hole=R_HOLE_TOP)
_box("title", -wid(TITLE,3.8)/2, TY-2.1, wid(TITLE,3.8)/2, TY+2.1)
table(25,S["major_key"],STEP_MAJ,QUAL_MAJ)
table(41,S["minor_key"],STEP_MIN,QUAL_MIN)

# --- left sector: what the background color means ---
for i,(color,name) in enumerate([(C_T,S["rest"]),(C_S,S["transition"]),(C_D,S["tension"])]):
    cx,y=-33.0,-13.0+i*8.6
    if COLOR:
        o.append(f'<rect x="{cx-13}" y="{y-3.5}" width="26" height="7.0" rx="1.8" fill="{color}"/>')
        o.append(f'<text x="{cx}" y="{y}" font-size="3.4" fill="#fff">{esc(name)}</text>')
    else:
        o.append(f'<rect x="{cx-13}" y="{y-3.5}" width="26" height="7.0" rx="1.8" '
                 f'fill="none" stroke="#111" stroke-width=".5"/>')
        o.append(f'<text x="{cx}" y="{y}" font-size="3.4">{esc(name)}</text>')
    _box(f"chip {name}", cx-13, y-3.5, cx+13, y+3.5)

# --- right sector: sample chips and the symbol key ---
def _sample(cx,y,t,minor,label):
    pw=wid(t,3.4)+2.6; ph=4.6
    o.append(f'<rect x="{cx-pw/2:.2f}" y="{y-ph/2:.2f}" width="{pw:.2f}" height="{ph:.2f}" '
             f'rx="1.4" fill="{DARK if minor else "#fff"}" stroke="#17181A" stroke-width=".4"/>')
    o.append(f'<text x="{cx}" y="{y}" font-size="3.4" fill="{"#fff" if minor else "#17181A"}">{t}</text>')
    o.append(f'<text x="{cx+pw/2+1.6}" y="{y}" font-size="2.6" style="text-anchor:start">{esc(label)}</text>')
    _box(f"sample {label}", cx-pw/2, y-ph/2, cx+pw/2+1.6+wid(label,2.6), y+ph/2)
_sample(22,-11.5,"I",False,S["major_key"])
_sample(22, -5.5,"I",True ,S["rel_minor"])
def _key_size(ln,cx,yy,s0=2.1):
    """shrinks the key line until its corners clear the cut circle -- the same
       sentence runs longer in English and Spanish than in Portuguese"""
    s=s0
    while s>1.5:
        w=wid(ln,s); hh=1.3*s/2.1
        if math.hypot(cx+w/2, abs(yy)+hh) <= R_PAP_TOP-1.0: break
        s-=0.05
    return s
for k,ln in enumerate([S["key_qual"], S["key_step"]]):
    yy=0.5+k*5.0
    s=_key_size(ln,32,yy); hh=1.3*s/2.1
    o.append(f'<text x="32" y="{yy}" font-size="{s:.2f}">{esc(ln)}</text>')
    _box(f"key {k}", 32-wid(ln,s)/2, yy-hh, 32+wid(ln,s)/2, yy+hh)

o.append(f'<text y="-58" font-size="3.2" fill="#8A9099">{esc(S["top_note"])}</text>')
e()
# ---------------- print-scale check bar -----------------------------------
RX0,RY=(W-100)/2,262.0
o.append(f'<rect x="{RX0}" y="{RY}" width="100" height="4.5" fill="none" stroke="#B9BEC4" stroke-width=".5"/>')
for k in range(11):
    x=RX0+k*10; h=4.5 if k%5==0 else 2.6
    o.append(f'<line x1="{x}" y1="{RY+4.5-h}" x2="{x}" y2="{RY+4.5}" stroke="#B9BEC4" stroke-width=".5"/>')
    if k%5==0: o.append(f'<text x="{x}" y="{RY-2.6}" font-size="2.8" fill="#8A9099">{k*10}</text>')
o.append(f'<text x="{W/2}" y="{RY+10.5}" font-size="3.6" fill="#8A9099">{esc(S["ruler"])}</text>')
o.append(f'<text x="{W/2}" y="{RY+16.0}" font-size="3.1" fill="#444">{esc(S["ruler2"])}</text>')
o.append(f'<text x="{W/2}" y="{RY+21.0}" font-size="3.1" fill="#444">{esc(S["ruler3"])}</text>')
o.append(f'<text x="{W/2}" y="290" font-size="3.3" fill="#666">{esc(S["footer"])}</text>')
o.append('</svg>')

_overlaps()
if errors:
    print("FAILED:"); [print("  -",x) for x in errors]; sys.exit(1)
open("art_field.svg","w",encoding="utf-8").write("\n".join(o))
print(f"check ok ({LANG}, color={COLOR}) — nothing crosses a cut line")
