# -*- coding: utf-8 -*-
"""Arte 1:1 da roda de campo harmonico (A4). COR=0 gera a versao P&B."""
import math, os, sys, colorsys

COR  = int(os.environ.get("COR","1"))
LADO = os.environ.get("LADO","maior")     # "maior" ou "menor"

# ---------------- conteudo musical ----------------------------------------
CIRC=["C","G","D","A","E","B","Gb/F#","Db","Ab","Eb","Bb","F"]
MEN =["Am","Em","Bm","F#m","C#m","G#m","Ebm","Bbm","Fm","Cm","Gm","Dm"]
DIM =["B","F#","C#","G#","D#","A#","F","C","G","D","A","E"]
# por coluna da janela (-30, 0, +30): romano, extensao (tetrade + nona), funcao
# algarismos romanos SEMPRE em maiuscula (notacao brasileira); a qualidade do
# acorde vem do sufixo ao lado e do nome que aparece na janela
# Cada face traz um modo so. O acorde e o mesmo nos dois -- muda o grau e a funcao.
# A pastilha ESCURA marca a tonica do tom relativo (menor no lado maior, e vice-versa).
# pastilha BRANCA = grau no tom maior | PRETA = grau no tom menor relativo.
# O acorde e o mesmo nos dois -- muda o grau e, em 3 casos, a funcao.
TIT="CAMPO HARMONICO"
L1=[("IV","VI","7M(9)","S","T"), ("I","III","7M(9)","T","T"), ("V","VII","7(9)","D","D")]
L2=[("II","IV","m7(9)","S","S"), ("VI","I","m7(9)","T","T"), ("III","V","m7(b9)","T","D")]
L3=("VII","II","m7(b5b9)","D","S")     # so o IIIm e o VII tem b9 -- os graus mais tensos

# ---------------- geometria (casa com regua.scad) -------------------------
R_PAP_BASE=52.0 ; R_FURO_BASE=5.5
R_PAP_TOPO=54.0 ; R_FURO_TOPO=9.5
W1=(40.5,49.0,13) ; W2=(25.5,34.5,13) ; W3=(10.5,20.0,13)     # aberturas
CEL1=(40.0,54.0,15) ; CEL2=(24.5,39.0,15) ; CEL3=(9.5,24.0,34) # area colorida
A1=(37.5,51.6) ; A2=(22.8,36.8) ; A3=(8.2,22.2)                # aneis da base (folga p/ erro de escala)
RT1,RT2,RT3 = 44.75, 30.0, 15.25   # centro exato de cada janela
FX1,FX2,FX3 = 51.4, 36.75, 22.0                                # linha do rotulo
SR1,SR2,SR3 = 3.2, 2.7, 2.7                                    # tam. do romano
SE1,SE2,SE3 = 2.7, 2.1, 2.2                                    # tam. da extensao

def hsl(h,s_,l_):
    r,g,b=colorsys.hls_to_rgb((h%360)/360.0,l_,s_)
    return "#%02X%02X%02X"%(int(r*255),int(g*255),int(b*255))
def cor_pos(p,anel): return hsl(p*30,0.72,{1:0.885,2:0.815,3:0.735}[anel])
C_T="#2E7D32"; C_S="#E36A0B"; C_D="#C62828"
FUN={"T":C_T,"S":C_S,"D":C_D}

W,H=210,297
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="#fff"/>',
   '<style>text{font-family:"DejaVu Sans",Arial,sans-serif;font-weight:700;'
   'text-anchor:middle;dominant-baseline:central}'
   '.cut{fill:none;stroke:#C9CDD2;stroke-width:.35}'
   '.rib{stroke:#222;stroke-width:.5}.ring{fill:none;stroke:#222;stroke-width:.5}</style>']

LARG={"Ô":.60,"i":.30,"l":.30,".":.30,"°":.36,"I":.36," ":.34,"(":.38,")":.38,",":.30,
      "m":.88,"M":.88,"W":.88,"D":.70,"7":.60,"5":.60,"9":.60,"b":.62,"V":.66,"v":.58}
def larg(t,s): return sum(LARG.get(c,.60) for c in t)*s
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
def faixa(R,a0,a1,w,cor):
    if not COR: return
    d=f"M {pol(a0,R)} A {R},{R} 0 {1 if a1-a0>180 else 0} 1 {pol(a1,R)}"
    o.append(f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{w}"/>')
def janela(ri,ro,half,ang=0):
    p=[pol(a+ang,ro) for a in [half-i*(2*half/48) for i in range(49)]]
    p+=[pol(a+ang,ri) for a in [-half+i*(2*half/48) for i in range(49)]]
    pts=" ".join(p)
    o.append(f'<polygon points="{pts}" style="fill:#fff;stroke:#fff;stroke-width:1.2"/>')
    o.append(f'<polygon points="{pts}" class="cut" style="fill:none"/>')
def arco(t,r,ac,s,fill="#111",x0=None):
    """texto ao longo do arco; x0 = deslocamento inicial em mm (senao centraliza)"""
    ws=[LARG.get(c,.60)*s for c in t]
    x=(-sum(ws)/2) if x0 is None else x0
    for c,w in zip(t,ws):
        cx=x+w/2; x+=w
        if c!=" ":
            o.append(f'<g transform="rotate({ac+math.degrees(cx/r)})">'
                     f'<text y="{-r}" font-size="{s}" fill="{fill}">{esc(c)}</text></g>')

erros=[]
def confere(nome,lo,hi,lim_i,lim_e):
    if lo<lim_i or hi>lim_e: erros.append(f"{nome}: {lo:.1f}..{hi:.1f} fora de {lim_i:.1f}..{lim_e:.1f}")
def confere_reto(nome,y,t,s,lim,x0=0.0,furo=0.0):
    """texto reto: confere a borda externa E o furo central"""
    ext=math.hypot(abs(y)+0.55*s, abs(x0)+larg(t,s)/2)
    if ext>lim: erros.append(f"{nome}: canto em {ext:.1f} > {lim:.1f}")
    if furo and abs(y)-0.55*s < furo+0.8:
        erros.append(f"{nome}: encosta no furo central ({abs(y)-0.55*s:.1f} < {furo+0.8:.1f})")

ESCURO="#17181A"
def pastilha(ang,r,txt,sz,cor,menor=False):
    """branca = grau no tom maior | preta = grau no tom menor relativo"""
    pw=larg(txt,sz)+2.4; ph=sz*1.30
    fundo_p = ESCURO if menor else "#fff"
    letra   = "#fff" if menor else (cor if COR else "#111")
    o.append(f'<g transform="rotate({ang})"><rect x="{-pw/2:.2f}" y="{-r-ph/2:.2f}" '
             f'width="{pw:.2f}" height="{ph:.2f}" rx="{ph*0.3:.2f}" fill="{fundo_p}" '
             f'stroke="#fff" stroke-width="{0.45 if menor else 0}"/></g>')
    o.append(f'<g transform="rotate({ang})"><text y="{-r}" font-size="{sz}" '
             f'fill="{letra}">{esc(txt)}</text></g>')
    return pw, ph

def celula(ang,r,gM,gm,ext,fM,fm,sr,se,lim_i,lim_e,meia=15):
    pwM=larg(gM,sr)+2.4; pwm=larg(gm,sr)+2.4; we=larg(ext,se); ph=sr*1.30
    tot=pwM+0.6+pwm+0.9+we; x=-tot/2
    pastilha(ang+math.degrees((x+pwM/2)/r), r, gM, sr, FUN[fM]);              x+=pwM+0.6
    pastilha(ang+math.degrees((x+pwm/2)/r), r, gm, sr, FUN[fm], menor=True);  x+=pwm+0.9
    arco(ext,r,ang,se,"#fff" if COR else "#111",x0=x)
    confere(f"celula {gM}/{gm}", r-ph/2, r+ph/2, lim_i, lim_e)
    confere(f"ext {gM}/{gm}",    r-0.55*se, r+0.55*se, lim_i, lim_e)
    disp=2*meia*math.pi*r/180.0
    if tot > disp-0.6: erros.append(f"rotulo {gM}/{gm}: {tot:.1f}mm nao cabe em {disp:.1f}mm")

def fundo(R,a,half,w,fM,fm):
    """se a funcao muda entre maior e menor, a celula sai bicolor"""
    if fM==fm: faixa(R,a-half,a+half,w,FUN[fM])
    else:      faixa(R,a-half,a,w,FUN[fM]); faixa(R,a,a+half,w,FUN[fm])

# ===================== 1. DISCO DA BASE (D104) ============================
g(W/2,58)
for p in range(12):
    for anel,(r0,r1) in ((1,A1),(2,A2),(3,A3)):
        faixa((r0+r1)/2,p*30-15,p*30+15,r1-r0,cor_pos(p,anel))
cut(R_PAP_BASE); cut(R_FURO_BASE)
for r in A1+A2+A3: ring(r)
for p in range(12):
    for (r0,r1) in (A1,A2,A3): rib(p*30+15,r0,r1)
    m=CIRC[p]
    txt(p*30,RT1,m,5.6 if len(m)>2 else 8.6)
    txt(p*30,RT2,MEN[p],5.6)
    txt(p*30,RT3,DIM[p]+"°",3.4)
o.append('<polygon points="0,-8.6 -1.6,-6.2 1.6,-6.2" fill="#8A9099"/>')
o.append('<text y="-56" font-size="3.2" fill="#8A9099">BASE (D104) — colar no rebaixo com o C na seta, virado para a aba</text>')
e()

# ============ 2. ETIQUETA DO DISCO DE CIMA (D108) =========================
g(W/2,196)
for i,a in enumerate((-30,0,30)):
    fundo((CEL1[0]+CEL1[1])/2,a,CEL1[2],CEL1[1]-CEL1[0],L1[i][3],L1[i][4])
    fundo((CEL2[0]+CEL2[1])/2,a,CEL2[2],CEL2[1]-CEL2[0],L2[i][3],L2[i][4])
fundo((CEL3[0]+CEL3[1])/2,0,CEL3[2],CEL3[1]-CEL3[0],L3[3],L3[4])
cut(R_PAP_TOPO); cut(R_FURO_TOPO)
for i,a in enumerate((-30,0,30)):
    janela(W1[0],W1[1],W1[2],a); janela(W2[0],W2[1],W2[2],a)
janela(W3[0],W3[1],W3[2])
for i,a in enumerate((-30,0,30)):
    celula(a,FX1,*L1[i],SR1,SE1,W1[1],CEL1[1])
    celula(a,FX2,*L2[i],SR2,SE2,W2[1],CEL2[1])
celula(0,FX3,*L3,SR3,SE3,W3[1],CEL3[1],meia=CEL3[2])

# ---------------- tabelas de intervalos e qualidade ------------------------
GRAUS=["I","II","III","IV","V","VI","VII"]
INT_MAI=["T","T","S","T","T","T","S"]
INT_MEN=["T","S","T","T","S","T","T"]
QUA_MAI=["M","m","m","M","M","m","\u00b0"]
QUA_MEN=["m","\u00b0","M","m","m","M","M"]
C_TOM="#3F4A57"; C_SEMI="#7C3AED"   # neutros: nao confundem com repouso/transicao/tensao

CAIXAS=[]
def _caixa(nome,x0,y0,x1,y1):
    CAIXAS.append((nome,min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)))
    for X in (x0,x1):
        for Y in (y0,y1): _livre(X,Y,nome)
def _colisoes():
    for i in range(len(CAIXAS)):
        for j in range(i+1,len(CAIXAS)):
            n1,a0,b0,a1,b1=CAIXAS[i]; n2,c0,d0,c1,d1=CAIXAS[j]
            if a1>c0+0.01 and c1>a0+0.01 and b1>d0+0.01 and d1>b0+0.01:
                erros.append(f"sobreposicao: {n1} x {n2}")

def _livre(x,y,nome):
    """canto tem de caber no papel e ficar fora do leque de janelas"""
    r=math.hypot(x,y)
    if r>R_PAP_TOPO-1.0: erros.append(f"{nome}: canto a {r:.1f} > {R_PAP_TOPO-1.0:.1f}")
    if r>W3[0]-1.0 and r<W1[1]+1.0:
        a=math.degrees(math.atan2(x,-y))
        if abs(a)<46.0: erros.append(f"{nome}: canto invade o leque (ang {a:.0f}, r {r:.1f})")

SG=2.6; SQ=2.3; SI=2.3          # tamanhos: grau / qualidade / intervalo
BH=8.0; CW_=2.9; CH_=3.9; GAP=0.4
def _larg_tab():
    w=sum(larg(g,SG)+1.7 for g in GRAUS)+7*CW_+13*GAP
    return w
def tabela(cy,rotulo,ints,quas):
    """faixa alinhada: caixa do grau (com a qualidade dentro) + pastilha do intervalo"""
    tot=_larg_tab(); x=-tot/2
    o.append(f'<text y="{cy-BH/2-2.6}" font-size="2.8">{rotulo}</text>')
    for k,gr in enumerate(GRAUS):
        bw=larg(gr,SG)+1.7
        o.append(f'<rect x="{x:.2f}" y="{cy-BH/2:.2f}" width="{bw:.2f}" height="{BH}" rx="1.5" '
                 f'fill="#fff" stroke="#17181A" stroke-width=".45"/>')
        o.append(f'<text x="{x+bw/2:.2f}" y="{cy-1.6:.2f}" font-size="{SG}">{gr}</text>')
        o.append(f'<text x="{x+bw/2:.2f}" y="{cy+2.4:.2f}" font-size="{SQ}" fill="#17181A">{quas[k]}</text>')
        x+=bw+GAP
        it=ints[k]; c=(C_SEMI if it=="S" else C_TOM) if COR else "#111"
        st = "" if COR else ' stroke="#111" stroke-width=".4"'
        o.append(f'<rect x="{x:.2f}" y="{cy-CH_/2:.2f}" width="{CW_}" height="{CH_}" rx="1.2" '
                 f'fill="{c}"{st}/>')
        o.append(f'<text x="{x+CW_/2:.2f}" y="{cy:.2f}" font-size="{SI}" '
                 f'fill="{"#fff" if COR else "#111"}">{it}</text>')
        x+=CW_+GAP
    _caixa(rotulo, -tot/2, cy-BH/2-4.2, tot/2, cy+BH/2)

# --- centro: titulo + as duas tabelas ---
TY=13.0
o.append(f'<text y="{TY}" font-size="3.8">{TIT}</text>')
confere_reto("titulo", TY, TIT, 3.8, R_PAP_TOPO, furo=R_FURO_TOPO)
_caixa("titulo", -larg(TIT,3.8)/2, TY-2.1, larg(TIT,3.8)/2, TY+2.1)
tabela(25,"TOM MAIOR",INT_MAI,QUA_MAI)
tabela(41,"TOM MENOR",INT_MEN,QUA_MEN)

# --- setor da esquerda: o que a cor do fundo quer dizer ---
for i,(cor,nome) in enumerate([(C_T,"REPOUSO"),(C_S,"TRANSICAO"),(C_D,"TENSAO")]):
    cx,y=-33.0,-13.0+i*8.6
    if COR:
        o.append(f'<rect x="{cx-13}" y="{y-3.5}" width="26" height="7.0" rx="1.8" fill="{cor}"/>')
        o.append(f'<text x="{cx}" y="{y}" font-size="3.4" fill="#fff">{nome}</text>')
    else:
        o.append(f'<rect x="{cx-13}" y="{y-3.5}" width="26" height="7.0" rx="1.8" '
                 f'fill="none" stroke="#111" stroke-width=".5"/>')
        o.append(f'<text x="{cx}" y="{y}" font-size="3.4">{nome}</text>')
    _caixa(f"chip {nome}", cx-13, y-3.5, cx+13, y+3.5)

# --- setor da direita: pastilhas e chave dos simbolos ---
def _amostra(cx,y,t,menor,rot):
    pw=larg(t,3.4)+2.6; ph=4.6
    o.append(f'<rect x="{cx-pw/2:.2f}" y="{y-ph/2:.2f}" width="{pw:.2f}" height="{ph:.2f}" '
             f'rx="1.4" fill="{ESCURO if menor else "#fff"}" stroke="#17181A" stroke-width=".4"/>')
    o.append(f'<text x="{cx}" y="{y}" font-size="3.4" fill="{"#fff" if menor else "#17181A"}">{t}</text>')
    o.append(f'<text x="{cx+pw/2+1.6}" y="{y}" font-size="2.6" style="text-anchor:start">{rot}</text>')
    _caixa(f"amostra {rot}", cx-pw/2, y-ph/2, cx+pw/2+1.6+larg(rot,2.6), y+ph/2)
_amostra(22,-11.5,"I",False,"TOM MAIOR")
_amostra(22, -5.5,"I",True ,"RELATIVA MENOR")
for k,ln in enumerate(["M = maior \u00b7 m = menor \u00b7 \u00b0 = diminuto",
                       "T = tom \u00b7 S = semitom"]):
    yy=0.5+k*5.0
    o.append(f'<text x="32" y="{yy}" font-size="2.1">{ln}</text>')
    _caixa(f"chave {k}", 32-larg(ln,2.1)/2, yy-1.3, 32+larg(ln,2.1)/2, yy+1.3)

o.append('<text y="-58" font-size="3.2" fill="#8A9099">DISCO DE CIMA (D108) — recortar o circulo, o furo e as 7 janelas brancas</text>')
e()
# ---------------- regua de conferencia de escala --------------------------
RX0,RY=(W-100)/2,262.0
o.append(f'<rect x="{RX0}" y="{RY}" width="100" height="4.5" fill="none" stroke="#B9BEC4" stroke-width=".5"/>')
for k in range(11):
    x=RX0+k*10; h=4.5 if k%5==0 else 2.6
    o.append(f'<line x1="{x}" y1="{RY+4.5-h}" x2="{x}" y2="{RY+4.5}" stroke="#B9BEC4" stroke-width=".5"/>')
    if k%5==0: o.append(f'<text x="{x}" y="{RY-2.6}" font-size="2.8" fill="#8A9099">{k*10}</text>')
o.append(f'<text x="{W/2}" y="{RY+10.5}" font-size="3.6" fill="#8A9099">'
         'MEÇA ESTA BARRA COM UMA RÉGUA: tem de dar 100 mm exatos.</text>')
o.append(f'<text x="{W/2}" y="{RY+16.0}" font-size="3.1" fill="#444">'
         'Se deu menos, o PDF saiu reduzido — imprima de novo com Escala 100% / Tamanho real '
         '(desmarque “Ajustar à página”).</text>')
o.append(f'<text x="{W/2}" y="{RY+21.0}" font-size="3.1" fill="#444">'
         'Deu X mm? Reimprima com escala = 100 × 100 ÷ X. Conferência: disco da base = 104 mm, disco de cima = 108 mm.</text>')
o.append(f'<text x="{W/2}" y="290" font-size="3.3" fill="#666">Tracejado = linha de corte.  |  Só o IIIm e o VII têm b9 — por isso são os graus mais tensos.</text>')
o.append('</svg>')

_colisoes()
if erros:
    print("FALHOU:"); [print("  -",x) for x in erros]; sys.exit(1)
open("arte_roda.svg","w",encoding="utf-8").write("\n".join(o))
print("verificacao ok — nada invade linha de corte")
