# -*- coding: utf-8 -*-
"""Papel do trilho da regua de escalas -- versao GRANDE (280 x 95 mm).
   A4 DEITADO, 1:1. Pagina 1 = dois paineis (um de reserva). Pagina 2 = legenda."""
import colorsys, os
COR=int(os.environ.get("COR","1"))
NOTAS=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def _lum(r,g,b):
    f=lambda c:(c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4)
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
SAT,VAL=0.90,0.97
def _rgb(pc):
    return colorsys.hsv_to_rgb(((((pc*7)%12)*30))/360.0, SAT, VAL)
def cor_nota(pc):
    r,g,b=_rgb(pc); return "#%02X%02X%02X"%(int(r*255+.5),int(g*255+.5),int(b*255+.5))
def txt_nota(pc):
    return "#FFFFFF" if _lum(*_rgb(pc))<0.34 else "#141414"

AFIN=[4,9,2,7,11,4]
NF=24
CW=10.2                      # largura da casa
RS=11.2                      # espacamento entre cordas
PW,PH=272.0,98.0
XN=21.0                      # pestana
Y0=21.0                      # 1a corda (aguda); cordas 21.0 .. 77.0
YT=9.8                       # centro da faixa TOM
YN=87.5                      # centro da pastilha do numero da casa
MARC={3,5,7,9,12,15,17,19,21,24}
def xf(f): return XN+(f-0.5)*CW if f>0 else XN-10.0
def yi(i): return Y0+(5-i)*RS
def xs(f): return XN+(f-1.5)*CW
def tom(f):
    pc=(AFIN[0]+f)%12
    return NOTAS[pc], NOTAS[(pc+9)%12]+"m", pc

def painel(o,ox,oy):
    o.append(f'<g transform="translate({ox},{oy})">')
    o.append(f'<rect x="0" y="0" width="{PW}" height="{PH}" fill="#fff" stroke="#bbb" stroke-width=".3"/>')
    # faixa TOM
    for f in range(1,13):
        maj,men,pc=tom(f); x=xs(f)
        o.append(f'<rect x="{x-4.9:.2f}" y="{YT-4.9:.2f}" width="9.8" height="9.8" rx="2.0" '
                 f'fill="{cor_nota(pc) if COR else "#fff"}" stroke="#111" stroke-width=".4"/>')
        o.append(f'<text x="{x:.2f}" y="{YT-2.3:.2f}" font-size="4.6" fill="{txt_nota(pc) if COR else "#111"}">{maj}</text>')
        o.append(f'<text x="{x:.2f}" y="{YT+3.0:.2f}" font-size="3.5" fill="{txt_nota(pc) if COR else "#444"}" opacity=".85">{men}</text>')
    # braco
    for i in range(6):
        y=yi(i)
        o.append(f'<line x1="{XN}" y1="{y}" x2="{XN+NF*CW}" y2="{y}" stroke="#444" stroke-width="{0.7-0.05*i:.2f}"/>')
    for f in range(1,NF+1):
        x=XN+f*CW
        o.append(f'<line x1="{x}" y1="{Y0}" x2="{x}" y2="{Y0+5*RS}" stroke="#c4c4c4" stroke-width=".4"/>')
    o.append(f'<line x1="{XN}" y1="{Y0-2.0}" x2="{XN}" y2="{Y0+5*RS+2.0}" stroke="#222" stroke-width="2.6"/>')
    for i in range(6):
        for f in range(NF+1):
            pc=(AFIN[i]+f)%12; n=NOTAS[pc]; nat=len(n)==1
            x,y=xf(f),yi(i)
            if COR:
                w,hh=(9.2,9.4) if f>0 else (12.2,9.4)
                o.append(f'<rect x="{x-w/2:.2f}" y="{y-hh/2:.2f}" width="{w}" height="{hh}" rx="2.4" fill="{cor_nota(pc)}"/>')
            o.append(f'<text x="{x}" y="{y}" font-size="{5.0 if nat else 4.1}" '
                     f'fill="{txt_nota(pc) if COR else ("#17181A" if nat else "#969CA2")}">{n}</text>')
    # numero da casa (aparece nas janelas da regua)
    for f in range(1,NF+1):
        m=f in MARC
        gemea = f+12 if f<=12 else f-12          # mesma forma, uma oitava de distancia
        o.append(f'<rect x="{xf(f)-4.4:.2f}" y="{YN-3.5:.2f}" width="8.8" height="7.0" rx="1.6" '
                 f'fill="{"#17181A" if m else "#E4E7EA"}"/>')
        o.append(f'<text x="{xf(f)}" y="{YN-1.6:.2f}" font-size="3.6" '
                 f'fill="{"#fff" if m else "#222"}">{f}</text>')
        o.append(f'<text x="{xf(f)}" y="{YN+2.3:.2f}" font-size="2.3" '
                 f'fill="{"#9aa2ab" if m else "#8A9099"}">{gemea}</text>')
    o.append(f'<text x="{XN-10.0}" y="{YN}" font-size="3.4" fill="#888">solta</text>')
    o.append('</g>')

# ---------------- verificacao ----------------
JW,JH,JX,JYc=10.2,10.6,-71.4,39.2      # janela TOM na regua (coords do .scad)
FW,FH,FYc=8.8,7.4,-38.5                # janelas do numero da casa
err=[]
if abs((Y0+2.5*RS)-PH/2)>0.01: err.append('cordas fora do centro do papel -> desalinha com os furos')
if YT+4.9 > Y0-4.7-0.2: err.append("faixa TOM encosta na 1a corda")
if YN+3.5 > PH-1.0: err.append("pastilha do numero sai do papel")
if Y0+5*RS+4.7 > YN-3.5: err.append("pastilha do numero bate na 6a corda")
p0,p1=PH/2-(JYc+JH/2), PH/2-(JYc-JH/2)
if not (p0<=YT-4.9 and p1>=YT+4.9): err.append(f"janela TOM nao cobre a celula ({p0:.2f}..{p1:.2f})")
if JW/2 >= CW-4.9: err.append("janela TOM mostra celula vizinha")
q0,q1=PH/2-(FYc+FH/2), PH/2-(FYc-FH/2)
if not (q0<=YN-3.5 and q1>=YN+3.5): err.append(f"janela da casa nao cobre a pastilha ({q0:.2f}..{q1:.2f})")
if xs(1)-4.9 < 0: err.append("celula TOM da casa 1 sai do papel")
if XN+NF*CW+5 > PW: err.append("casas passam da largura do papel")
if err: raise SystemExit("ERRO: "+" | ".join(err))

W,H=297.0,210.0
def pag1():
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" fill="#fff"/>',
       '<style>text{font-family:"DejaVu Sans",Arial,sans-serif;font-weight:700;'
       'text-anchor:middle;dominant-baseline:central}'
       '.cut{fill:none;stroke:#e11;stroke-width:.35;stroke-dasharray:2.5 2}</style>',
       f'<text x="{W/2}" y="7" font-size="4.2" fill="#444">PAPEL DO TRILHO — A4 DEITADO, imprimir em 100% / tamanho real. '
       f'Tracejado = corte. O de baixo é reserva.</text>']
    for oy in (12.0, 110.0):
        o.append(f'<rect x="{(W-PW)/2}" y="{oy}" width="{PW}" height="{PH}" class="cut"/>')
        painel(o,(W-PW)/2,oy)
    o.append('</svg>'); return "\n".join(o)

def pag2():
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" fill="#fff"/>',
       '<style>text{font-family:"DejaVu Sans",Arial,sans-serif;font-weight:700;'
       'text-anchor:middle;dominant-baseline:central}</style>',
       f'<text x="{W/2}" y="18" font-size="8">COMO LER A RÉGUA</text>']
    def item(x,y,kind,txt):
        if kind=="q": o.append(f'<rect x="{x-4.3}" y="{y-4.3}" width="8.6" height="8.6" fill="#17181A"/>')
        if kind=="l": o.append(f'<rect x="{x-3.4}" y="{y-3.4}" width="6.9" height="6.9" fill="#17181A" transform="rotate(45 {x} {y})"/>')
        if kind=="g": o.append(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#17181A"/>')
        if kind=="p": o.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#17181A"/>')
        if kind=="j": o.append(f'<rect x="{x-5.3}" y="{y-5.3}" width="10.6" height="10.6" fill="none" stroke="#17181A" stroke-width="1.1"/>')
        if kind=="n": o.append(f'<rect x="{x-4.4}" y="{y-3.4}" width="8.8" height="6.8" rx="1.6" fill="none" stroke="#17181A" stroke-width="1.1"/>')
        o.append(f'<text x="{x+9}" y="{y}" font-size="6.0" fill="#222" style="text-anchor:start">{txt}</text>')
    L=[("q","tônica MAIOR"),("l","tônica da RELATIVA MENOR"),("g","nota da pentatônica"),
       ("p","só na escala completa (graus 4 e 7)"),("j","janela TOM — a tonalidade"),
       ("n","janelas de baixo — casa e sua gêmea (5 / 17)")]
    for k,(kd,tx) in enumerate(L): item(30, 42+k*15, kd, tx)
    txt=["Tabela do topo: cada caixa é uma forma. Número de CIMA = tom maior, de BAIXO = relativa menor.",
         "Os traços verticais caem nas casas que duas formas vizinhas dividem.",
         "Na 6ª corda os dois quadrados ficam a 12 casas: de um ao outro é uma oitava.",
         "Cada nota tem sua cor — a mesma da roda de campo harmônico.",
         "Corda mais grave = linha de baixo. Colar o papel no rebaixo do trilho."]
    for k,t in enumerate(txt):
        o.append(f'<text x="{W/2}" y="{146+k*11}" font-size="5.4" fill="#333">{t}</text>')
    o.append('</svg>'); return "\n".join(o)

open("arte_regua.svg","w",encoding="utf-8").write(pag1())
open("arte_regua_p2.svg","w",encoding="utf-8").write(pag2())
print("ok  janela TOM ve %.1f..%.1f | janela casa ve %.1f..%.1f"%(p0,p1,q0,q1))
print("   painel %.0f x %.0f mm"%(PW,PH))
