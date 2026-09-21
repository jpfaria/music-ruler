// ==========================================================================
//  HARMONIC FIELD WHEEL -- "ruler" edition: mechanics only.
//  The art (chords / degrees) goes on paper glued into the recesses.
//  part = "base" | "top" | "cap" | "all"
// ==========================================================================
part="all"; viz=0; $fn=110;

R_base=59.0; R_top=55.0; t_base=3.0; t_top=2.0;
pap_d = 0.35;              // depth of the paper recess
pap_o = 52.0; pap_i = 5.5; // base recess     -> paper disc D104
tpp_o = 54.0; tpp_i = 9.5; // top disc recess -> label D108

// stepped window: 3 major cells, 3 minor, 1 diminished
w1_o=49.0; w1_i=40.5;
w2_o=34.5; w2_i=25.5;
w3_o=20.0; w3_i=10.5;
cel_h=13;      // half-opening of each cell (leaves a 4-degree frame)
col=[-30,0,30];

// threaded shaft + printed cap nut. The shaft is solid: a smooth axle as tall as the top
// disc, then a coarse thread. The cap bottoms out on the END of the shaft, never on the
// disc, so it cannot be overtightened and the disc keeps clear_z of lift.
post_od=9.4; hub_od=17.0; hub_h=6.0; bore_d=9.8;
clear_z=0.5;                       // lift left to the disc: it has to climb the detents
axle_h=t_top+hub_h+clear_z;
thr_p=3.0; thr_e=0.5;              // pitch / half depth: flanks at ~46 deg, no supports
thr_h=7.5;                         // 2.5 turns
thr_c=0.35;                        // radial play between shaft and cap
thr_r=post_od/2-thr_e;             // thread crest = axle diameter, so the disc slides over it
cap_roof=1.6; cap_h=thr_h+cap_roof;
r_det=53.5; bump_r=2.0; bump_h=0.40; dimp_r=2.2; dimp_h=0.55;

assert(clear_z>=bump_h, "the disc cannot climb the detent bumps under the cap");
assert(post_od<bore_d, "the thread crest does not pass through the top disc");
assert(atan(2*PI*thr_e/thr_p)<=50, "thread flank too flat to print without supports");
assert(thr_r-thr_e>=3.5, "thread core too thin");

// single-start right-hand thread: a circle of radius r swept off-centre by thr_e.
// Crest at r+thr_e, root at r-thr_e. Shaft and cap use the same sweep, so they mate.
module thread(r,h){
  linear_extrude(height=h,twist=-360*h/thr_p,slices=ceil(h/0.1),convexity=4)
    translate([thr_e,0]) circle(r);
}
module at(a,r){ rotate([0,0,-a]) translate([0,r,0]) children(); }
module sector2d(ri,ro,half,rd=1.2){
    offset(r=rd) offset(r=-rd)
    intersection(){
        difference(){ circle(ro); circle(ri); }
        polygon(concat([[0,0]],[for(i=[-half:1:half]) [(ro+5)*sin(i),(ro+5)*cos(i)]]));
    }
}
module window2d(){
  union(){
    for(a=col) rotate([0,0,-a]) union(){
        sector2d(w1_i,w1_o,cel_h);     // major chords      (IV I V)
        sector2d(w2_i,w2_o,cel_h);     // minor chords      (ii vi iii)
    }
    sector2d(w3_i,w3_o,cel_h);         // diminished (vii)
  }
}

// ------------------------------- BASE -------------------------------------
module base_disc(){
  difference(){
    union(){
      difference(){                                   // plate + knurled rim
        cylinder(h=t_base, r=R_base);
        for(i=[0:43]) at(i*8.18,R_base) cylinder(h=3*t_base,r=1.6,center=true);
      }
      for(a=[0,180]) at(a,r_det)                      // detent bumps
        translate([0,0,t_base-(bump_r-bump_h)]) sphere(r=bump_r,$fn=40);
      translate([0,0,t_base]){                        // threaded shaft
        cylinder(h=axle_h,r=post_od/2);
        translate([0,0,axle_h]) intersection(){
          thread(thr_r,thr_h);
          cylinder(h=thr_h,r1=post_od/2+thr_h-0.8,r2=post_od/2-0.8);   // lead-in chamfer
        }
        rotate_extrude() translate([post_od/2,0,0])
          difference(){ square([1.4,1.4]); translate([1.4,1.4]) circle(r=1.4,$fn=32); }
      }
    }
    // ring recess for the paper disc
    difference(){
      translate([0,0,t_base-pap_d]) cylinder(h=pap_d+1,r=pap_o);
      translate([0,0,t_base-pap_d-1]) cylinder(h=pap_d+3,r=pap_i);
    }
    translate([-200,-200,-60]) cube([400,400,60]);    // trim everything below z=0
  }
}

// ------------------------------ TOP DISC ----------------------------------
module tab2d(){ hull(){ translate([0,49]) circle(r=6.4); translate([0,58]) circle(r=7.5); } }

module top_disc(){
  difference(){
    union(){
      linear_extrude(t_top) union(){ circle(R_top); tab2d(); }
      translate([0,0,t_top]) union(){                 // knurled knob
        cylinder(h=hub_h,r=hub_od/2);
        for(i=[0:13]) at(i*25.7,hub_od/2) cylinder(h=hub_h,r=0.85);
      }
    }
    // recess for the paper label
    difference(){
      translate([0,0,t_top-pap_d]) cylinder(h=pap_d+1,r=tpp_o);
      translate([0,0,t_top-pap_d-1]) cylinder(h=pap_d+3,r=tpp_i);
    }
    translate([0,0,-1]) linear_extrude(t_top+2) window2d();   // stepped window
    translate([0,0,-1]) cylinder(h=t_top+hub_h+2,r=bore_d/2);
    translate([0,0,-0.01]) cylinder(h=0.7,r1=bore_d/2+0.7,r2=bore_d/2);
    for(i=[0:11]) at(i*30,r_det) translate([0,0,dimp_h-dimp_r]) sphere(r=dimp_r,$fn=40);
  }
}

// -------------------------------- CAP -------------------------------------
// Modelled as assembled (mouth down, z=0 at the top of the axle). Printed roof-down.
module cap(){
  difference(){
    union(){
      cylinder(h=cap_h,r=hub_od/2);
      for(i=[0:13]) at(i*25.7,hub_od/2) cylinder(h=cap_h,r=0.85);
    }
    translate([0,0,-0.01]) thread(thr_r+thr_c,thr_h+0.01);
    translate([0,0,-0.01]) cylinder(h=1.0,r1=post_od/2+thr_c+0.8,r2=post_od/2+thr_c-0.2);
  }
}

if(part=="base") base_disc();
else if(part=="top") top_disc();
else if(part=="cap") translate([0,0,cap_h]) rotate([180,0,0]) cap();
else if(part=="all"){ base_disc(); translate([0,0,t_base]) top_disc();
                      translate([0,0,t_base+axle_h]) cap(); }
else if(part=="probe") intersection(){ base_disc(); translate([0,0,t_base+axle_h]) cap(); }
