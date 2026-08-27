// ==========================================================================
//  RODA DE CAMPO HARMONICO -- versao "regua": so a mecanica.
//  A arte (acordes / graus) vai em papel colado nos rebaixos.
//  part = "base" | "top" | "all"
// ==========================================================================
part="all"; viz=0; $fn=110;

R_base=59.0; R_top=55.0; t_base=3.0; t_top=2.0;
pap_d = 0.35;              // profundidade do rebaixo do papel
pap_o = 52.0; pap_i = 5.5; // rebaixo da base  -> disco de papel D104
tpp_o = 54.0; tpp_i = 9.5; // rebaixo do disco de cima -> etiqueta D108

// janela escalonada: 3 celulas maiores, 3 menores, 1 diminuto
w1_o=49.0; w1_i=40.5;
w2_o=34.5; w2_i=25.5;
w3_o=20.0; w3_i=10.5;
cel_h=13;      // meia-abertura de cada celula (deixa 4 graus de moldura)
col=[-30,0,30];

// eixo snap-fit (mecanismo ja verificado em corte)
post_od=9.4; post_wall=1.0; hook_od=11.6;
hub_od=17.0; hub_h=6.0; bore_d=9.8;
folga_z=0.5;                       // o gancho sai 0.5 acima do cubo, sempre
post_h=t_top+hub_h+folga_z; hook_land=1.2; post_top=post_h+hook_land+2.6;
slot_w=1.6; slot_z0=0.5;
// ressalto radial = (hook_od-bore_d)/2 = 0.90 mm
// deformacao: e = 3*t*d/(2*L^2) = 3*1.0*0.90/(2*8.0^2) = 2.1% -> ok em PETG
r_det=53.5; bump_r=2.0; bump_h=0.40; dimp_r=2.2; dimp_h=0.55;

module at(a,r){ rotate([0,0,-a]) translate([0,r,0]) children(); }
module setor2d(ri,ro,half,rd=1.2){
    offset(r=rd) offset(r=-rd)
    intersection(){
        difference(){ circle(ro); circle(ri); }
        polygon(concat([[0,0]],[for(i=[-half:1:half]) [(ro+5)*sin(i),(ro+5)*cos(i)]]));
    }
}
module janela2d(){
  union(){
    for(a=col) rotate([0,0,-a]) union(){
        setor2d(w1_i,w1_o,cel_h);      // acordes maiores  (IV I V)
        setor2d(w2_i,w2_o,cel_h);      // acordes menores  (ii vi iii)
    }
    setor2d(w3_i,w3_o,cel_h);          // diminuto (vii)
  }
}

// ------------------------------- BASE -------------------------------------
module disco_base(){
  difference(){
    union(){
      difference(){                                   // prato + serrilha de pega
        cylinder(h=t_base, r=R_base);
        for(i=[0:43]) at(i*8.18,R_base) cylinder(h=3*t_base,r=1.6,center=true);
      }
      for(a=[0,180]) at(a,r_det)                      // ressaltos dos detentes
        translate([0,0,t_base-(bump_r-bump_h)]) sphere(r=bump_r,$fn=40);
      translate([0,0,t_base]) difference(){           // eixo snap-fit
        union(){
          cylinder(h=post_h,r=post_od/2);
          translate([0,0,post_h]) cylinder(h=hook_land,r=hook_od/2);
          translate([0,0,post_h+hook_land])
            cylinder(h=post_top-post_h-hook_land,r1=hook_od/2,r2=post_od/2-0.4);
          rotate_extrude() translate([post_od/2,0,0])
            difference(){ square([1.4,1.4]); translate([1.4,1.4]) circle(r=1.4,$fn=32); }
        }
        translate([0,0,0.6]) cylinder(h=post_top,r=post_od/2-post_wall);
        for(a=[0,90,180,270]) rotate([0,0,a])
          translate([-slot_w/2,-post_od,slot_z0]) cube([slot_w,2*post_od,post_top]);
      }
    }
    // rebaixo anelar para o disco de papel
    difference(){
      translate([0,0,t_base-pap_d]) cylinder(h=pap_d+1,r=pap_o);
      translate([0,0,t_base-pap_d-1]) cylinder(h=pap_d+3,r=pap_i);
    }
    translate([-200,-200,-60]) cube([400,400,60]);    // apara abaixo de z=0
  }
}

// --------------------------- DISCO DE CIMA --------------------------------
module aba2d(){ hull(){ translate([0,49]) circle(r=6.4); translate([0,58]) circle(r=7.5); } }

module disco_top(){
  difference(){
    union(){
      linear_extrude(t_top) union(){ circle(R_top); aba2d(); }
      translate([0,0,t_top]) union(){                 // botao serrilhado
        cylinder(h=hub_h,r=hub_od/2);
        for(i=[0:13]) at(i*25.7,hub_od/2) cylinder(h=hub_h,r=0.85);
      }
    }
    // rebaixo para a etiqueta de papel
    difference(){
      translate([0,0,t_top-pap_d]) cylinder(h=pap_d+1,r=tpp_o);
      translate([0,0,t_top-pap_d-1]) cylinder(h=pap_d+3,r=tpp_i);
    }
    translate([0,0,-1]) linear_extrude(t_top+2) janela2d();   // janela escalonada
    translate([0,0,-1]) cylinder(h=t_top+hub_h+2,r=bore_d/2);
    translate([0,0,-0.01]) cylinder(h=0.7,r1=bore_d/2+0.7,r2=bore_d/2);
    for(i=[0:11]) at(i*30,r_det) translate([0,0,dimp_h-dimp_r]) sphere(r=dimp_r,$fn=40);
  }
}

if(part=="base") disco_base();
else if(part=="top") disco_top();
else if(part=="all"){ disco_base(); translate([0,0,t_base]) disco_top(); }
