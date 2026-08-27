// ==========================================================================
//  REGUA DE ESCALAS v3 -- trilho + regua + duas cortinas
//  Retencao por RABO DE ANDORINHA a 45 graus: nenhuma ponte no ar, imprime
//  sem suporte e sem folga vertical. Dois niveis empilhados:
//    nivel 1 (embaixo) -> duas cortinas, entre o papel e a regua
//    nivel 2 (em cima) -> regua deslizante
//  A cortina tapa o papel: pelos furos da regua voce ve a chapa lisa dela.
//  part = "trilho" | "regua" | "cortina" | "montada"
// ==========================================================================
part="montada"; $fn=48;

CW = 10.2;                  // largura da casa
NC = 13;                    // casas cobertas pela regua
RS = 11.2;                  // espacamento entre cordas
BW = 280; BH = 108; BT = 3.0;
PAP = 0.35;                 // rebaixo do papel

// ---- perfil dos dois canais (rabo de andorinha) --------------------------
C1 = 49.0;  V1 = 0.8;  H1 = 2.1;   // nivel 1: meia-largura, trecho reto, altura
C2 = 48.4;  V2 = 0.8;  H2 = 2.1;   // nivel 2
T1 = C1-(H1-V1);            // abertura do nivel 1 = 47.7
T2 = C2-(H2-V2);            // abertura do nivel 2 = 47.1
Z1 = BT;                    // piso do nivel 1
Z2 = BT+H1;                 // piso do nivel 2
ZT = BT+H1+H2;              // topo das paredes = 7.2

ST = 1.8;  CHF = 1.0;       // espessura das chapas e chanfro de 45 no topo
KH = 96.4;                  // cortina, nivel 1 (meia 48.2 > T1=47.7 -> nao sai)
SH = 95.2;                  // regua,   nivel 2 (meia 47.6 > T2=47.1 -> nao sai)

AFIN=[4,9,2,7,11,4];
DIA=[0,2,4,5,7,9,11]; PEN=[0,2,4,7,9];
OFF=8;
FORMAS=[0,2,4,7,9,12];
SX0=-80.2; SX1=74.2;
JW=10.2; JH=10.6; JX=-71.4; JYc=39.2;
FW=8.8; FH=7.4; FYc=-38.5;
RX0=-65.0; RX1=65.0; RY0=32.6; RY1=45.2; RPAP=0.35;   // etiqueta das formas

function grau(i,c) = (AFIN[i]+c+OFF)%12;
function tem(v,g) = len([for(a=v) if(a==g) 1])>0;
function xc(c) = -((NC-1)/2)*CW + c*CW;
function yc(i) = -((6-1)/2)*RS + i*RS;

// chapa com chanfro de 45 nas duas bordas longas do topo
module chapa(x0,x1,meia,esp,chf){
  hull(){
    translate([(x0+x1)/2,0,esp/2-0.005]) cube([x1-x0, 2*(meia-chf), 0.01], center=true);
    translate([(x0+x1)/2,0,-esp/2+0.005]) cube([x1-x0, 2*meia, 0.01], center=true);
  }
}
// cortador do canal: perfil em Y-Z estendido no eixo X
module canal(base,meia,reto,alt,topo){
  translate([-BW/2-1,0,0]) rotate([90,0,90]) linear_extrude(BW+2)
    polygon([[-meia,base-0.01],[meia,base-0.01],[meia,base+reto],
             [topo,base+alt],[-topo,base+alt],[-meia,base+reto]]);
}

module trilho(){
  difference(){
    translate([-BW/2,-BH/2,0]) cube([BW,BH,ZT]);
    canal(Z1,C1,V1,H1,T1);
    canal(Z2,C2,V2,H2,T2);
    translate([-(BW-8)/2,-C1+0.5,BT-PAP]) cube([BW-8, 2*C1-1, PAP+0.01]);   // papel
  }
}

module regua(){
  difference(){
    union(){
      chapa(SX0,SX1,SH/2,ST,CHF);
      translate([SX1-9,0,ST/2]) cube([7,SH-26,1.2], center=true);           // pega
    }
    for(i=[0:5]) for(c=[0:NC-1]){
      g=grau(i,c);
      if(g==0)      translate([xc(c),yc(i),0]) cube([8.6,8.6,ST+2], center=true);
      else if(g==9) translate([xc(c),yc(i),0]) rotate([0,0,45]) cube([6.9,6.9,ST+2], center=true);
      else if(tem(PEN,g)) translate([xc(c),yc(i),-ST]) cylinder(h=ST*3, d=8.3);
      else if(tem(DIA,g)) translate([xc(c),yc(i),-ST]) rotate([0,0,90])
                            cylinder(h=ST*3, d=8.8, $fn=3);   // triangulo: graus 4 e 7
    }
    // rebaixo para a etiqueta das formas (papel colado, nada gravado)
    translate([RX0, RY0, ST/2-RPAP]) cube([RX1-RX0, RY1-RY0, RPAP+0.01]);
    translate([JX,JYc,0]) cube([JW,JH,ST+2], center=true);                    // janela TOM
    for(c=[0:NC-1]) translate([xc(c),FYc,0]) cube([FW,FH,ST+2], center=true); // janelas das casas
  }
}

// cortina: tapa a faixa das cordas e deixa ver a tabela das formas e as casas
KL = 112;                   // comprimento
KS_T = [32.6, 45.2];        // rasgo de cima  (tabela das formas / janela TOM)
KS_B = [-45.2, -33.0];      // rasgo de baixo (numero das casas)
module cortina(){
  // sem pega saliente: a regua corre por cima. Empurra-se pelos rasgos.
  difference(){
    union(){
      chapa(0,KL,KH/2,ST,CHF);
    }
    for(s=[KS_T,KS_B]) difference(){
      translate([3,s[0],-1]) cube([KL-6, s[1]-s[0], ST+2]);
      for(x=[KL*0.32, KL*0.66])                                               // travessas
        translate([x-1.2,s[0]-1,-2]) cube([2.4, s[1]-s[0]+2, ST+4]);
    }
  }
}

if(part=="trilho") trilho();
else if(part=="regua") regua();
else if(part=="cortina") cortina();
else { trilho();
       translate([-BW/2+6,0,Z1+ST/2+0.15]) cortina();
       translate([BW/2-6-KL,0,Z1+ST/2+0.15]) cortina();
       translate([0,0,Z2+ST/2+0.15]) regua(); }
