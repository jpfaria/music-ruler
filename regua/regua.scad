// ==========================================================================
//  REGUA DE ESCALAS -- trilho + regua deslizante
//  O trilho leva o mapa de notas em papel. A regua corre por cima e mostra
//  a escala pelos furos. Como o espacamento e uniforme, deslizar 1 casa =
//  subir 1 semitom: a mesma peca serve os 12 tons.
//  Quadrado = tonica maior | Losango = tonica menor relativa.
//  part = "trilho" | "regua" | "montada"
// ==========================================================================
part="montada"; $fn=48;

CW   = 10.2;                // largura da casa
NC   = 13;                  // casas cobertas pela regua (0..12)
NB   = 24;                  // casas do trilho
RS   = 11.2;                // espacamento entre cordas

BW=280; BH=108; BT=3.0;     // trilho (cabe na mesa de 300)
CANAL=49.0;                 // meia-altura do canal
CH=2.6;                     // profundidade do canal (folga 0.8 sobre a regua)
LIP=47.1;                   // ate onde a aba avanca
LT=1.0;                     // espessura da aba (3-5 camadas, nao caida)
PAP=0.35;                   // rebaixo do papel

SH=96.4; ST=1.8;            // regua deslizante (0.8 de folga por lado)
SX0=-80.2; SX1=74.2;        // chapa da regua em x (assimetrica: sobra p/ a janela TOM)
JW=10.2; JH=10.6; JX=-71.4; JYc=39.2;   // janela TOM
FW=8.8; FH=7.4; FYc=-38.5;              // janelas do numero da casa

AFIN=[4,9,2,7,11,4];
DIA=[0,2,4,5,7,9,11]; PEN=[0,2,4,7,9];
OFF=8;                      // coluna 0 = tonica na 6a corda
FORMAS=[0,2,4,7,9,12];      // limites das 5 formas na 6a corda

function grau(i,c) = (AFIN[i]+c+OFF)%12;
function tem(v,g) = len([for(a=v) if(a==g) 1])>0;
function xc(c) = -((NC-1)/2)*CW + c*CW;
function yc(i) = -((6-1)/2)*RS + i*RS;

// ------------------------------ TRILHO ------------------------------------
module trilho(){
  difference(){
    union(){
      translate([-BW/2,-BH/2,0]) cube([BW,BH,BT]);                 // prato
      for(s=[-1,1]) translate([-BW/2, s>0?CANAL:-BH/2, 0])         // paredes
          cube([BW, BH/2-CANAL, BT+CH+LT]);
      for(s=[-1,1]) translate([-BW/2, s>0?LIP:-CANAL, BT+CH])      // abas de retencao
          cube([BW, CANAL-LIP, LT]);
    }
    translate([-BW/2-1,-CANAL,BT]) cube([BW+2, 2*CANAL, CH]);      // canal
    translate([-(BW-8)/2,-CANAL+0.5,BT-PAP])                        // rebaixo do papel
      cube([BW-8, 2*CANAL-1, PAP+0.01]);
  }
}

// --------------------------- REGUA DESLIZANTE ------------------------------
module regua(){
  difference(){
    union(){
      // chapa com chanfro de 45 nas duas bordas longas do topo
      hull(){
        translate([(SX0+SX1)/2,0,-ST/2]) cube([SX1-SX0,SH,0.01], center=true);
        translate([(SX0+SX1)/2,0, ST/2]) cube([SX1-SX0,SH-1.2,0.01], center=true);
      }
      translate([SX1-9,0,ST/2]) cube([7,SH-26,1.2], center=true);    // pega
    }
    for(i=[0:5]) for(c=[0:NC-1]){
      g=grau(i,c);
      if(g==0)                                                        // tonica maior
        translate([xc(c),yc(i),0]) cube([8.6,8.6,ST+2], center=true);
      else if(g==9)                                                   // tonica menor
        translate([xc(c),yc(i),0]) rotate([0,0,45]) cube([6.9,6.9,ST+2], center=true);
      else if(tem(PEN,g))
        translate([xc(c),yc(i),-ST]) cylinder(h=ST*3, d=8.3);
      else if(tem(DIA,g))
        translate([xc(c),yc(i),-ST]) cylinder(h=ST*3, d=5.0);
    }
    // ---- tabela das formas (topo): 5 caixas, linha de cima = tom maior,
    //      linha de baixo = relativa menor. Os tracos verticais caem nas
    //      casas-limite, que pertencem as duas formas vizinhas.
    LW=1.0; Y1=32.8; Y2=38.6; Y3=45.6;
    translate([0,0,ST/2-0.35]) linear_extrude(1){
      for(y=[Y1,Y2,Y3]) translate([xc(0)-LW/2, y-LW/2]) square([xc(12)-xc(0)+LW, LW]);
      for(k=[0:5]) translate([xc(FORMAS[k])-LW/2, Y1]) square([LW, Y3-Y1]);
      for(n=[0:4]){
        xm=(xc(FORMAS[n])+xc(FORMAS[n+1]))/2;
        translate([xm,(Y2+Y3)/2]) text(str(n+1), size=5.2, halign="center",
                  valign="center", font="DejaVu Sans:style=Bold");
        translate([xm,(Y1+Y2)/2]) text(str(((n+1)%5)+1), size=4.0, halign="center",
                  valign="center", font="DejaVu Sans:style=Bold");
      }
    }
    // ---- janelas das casas (base): mostram o numero da casa no papel
    for(c=[0:NC-1]) translate([xc(c),FYc,0]) cube([FW,FH,ST+2], center=true);
    // janela TOM: mostra a faixa de tonalidade impressa no papel
    translate([JX,JYc,0]) cube([JW,JH,ST+2], center=true);
  }
}

if(part=="trilho") trilho();
else if(part=="regua") regua();
else { trilho(); translate([0,0,BT+ST/2+0.15]) regua(); }
