// ==========================================================================
//  SCALE RULER v3 -- track + slider + two shutters
//  Retention by a 45-degree DOVETAIL: no bridge in mid-air, so it prints
//  without supports and without vertical slop. Two stacked levels:
//    level 1 (bottom) -> the two shutters, between paper and slider
//    level 2 (top)    -> the sliding ruler
//  A shutter covers the paper: through the slider holes you see its blank face.
//  part = "track" | "slider" | "shutter" | "assembled"
// ==========================================================================
part="assembled"; $fn=48;

CW = 10.2;                  // fret width
NF = 13;                    // frets covered by the slider
RS = 11.2;                  // string spacing
BW = 280; BH = 108; BT = 3.0;
PAP = 0.35;                 // paper recess

// ---- profile of the two channels (dovetail) ------------------------------
C1 = 49.0;  V1 = 0.8;  H1 = 2.3;   // level 1: half-width, straight run, height
C2 = 48.4;  V2 = 0.8;  H2 = 2.1;   // level 2
// level 1 is 0.2 taller than the plate needs: that headroom is what keeps a
// lifted shutter from ever touching the slider running above it.
T1 = C1-(H1-V1);            // level 1 opening = 47.7
T2 = C2-(H2-V2);            // level 2 opening = 47.1
Z1 = BT;                    // level 1 floor
Z2 = BT+H1;                 // level 2 floor
ZT = BT+H1+H2;              // top of the walls = 7.2

ST = 1.8;  CHF = 1.0;       // plate thickness and 45-degree top chamfer

// ---- fit -----------------------------------------------------------------
// FIT is the side clearance between a plate and its channel, per side. Every
// plate width is DERIVED from it, so the dovetail grip can never end up
// smaller than the sideways play again -- which is what made the v3 plates
// slide off their ledge and fall out.
FIT = 0.25;                 // per side; raise it if a plate binds on your printer
PAPW = 2*C1;                // the paper recess spans the WHOLE channel floor, so a
                            // shutter is supported edge to edge whatever the paper
                            // thickness -- a narrower recess leaves two thin ledges
                            // for it to balance on and tip off of
PAPR = 2.0;                 // ramp at each end of the recess, so nothing catches
KH = 2*(C1-FIT);            // shutter, level 1 -> 97.7
SH = 2*(C2-FIT);            // slider,  level 2 -> 96.5
GRIP1 = KH/2-T1;            // dovetail grip per side, level 1 -> 1.15
GRIP2 = SH/2-T2;            // level 2 -> 1.15
// A plate can only rise until its shoulder meets the 45-degree wall: FIT mm.
// It therefore never reaches the floor of the level above (ST+FIT < H).
assert(GRIP1 >= 4*FIT, "level 1: dovetail grip too small for the side play");
assert(GRIP2 >= 4*FIT, "level 2: dovetail grip too small for the side play");
assert(ST+FIT <= H1, "shutter can lift into the slider channel");
assert(ST+FIT <= H2, "slider can lift out over the walls");
assert(ST-CHF == V1, "plate chamfer no longer matches the channel profile");
assert(PAPW >= KH, "shutter wider than the paper recess: it would ride on the ledges");
echo(str("fit: play ",FIT," mm/side  grip ",GRIP1," mm/side  lift ",FIT,
         " mm  gap to the level above ",H1-ST-FIT," mm"));

TUNING=[4,9,2,7,11,4];
DIAT=[0,2,4,5,7,9,11]; PENT=[0,2,4,7,9];
OFF=8;
SHAPES=[0,2,4,7,9,12];
SX0=-80.2; SX1=74.2;
JW=10.2; JH=10.6; JX=-71.4; JYc=39.2;
FW=8.8; FH=7.4; FYc=-38.5;
RX0=-65.0; RX1=65.0; RY0=32.6; RY1=45.2; RPAP=0.35;   // shape-label recess

function degree(i,f) = (TUNING[i]+f+OFF)%12;
function has(v,g) = len([for(a=v) if(a==g) 1])>0;
function xc(f) = -((NF-1)/2)*CW + f*CW;
function yc(i) = -((6-1)/2)*RS + i*RS;

// plate with a 45-degree chamfer on both long top edges
module plate(x0,x1,half,th,chf){
  hull(){
    translate([(x0+x1)/2,0,th/2-0.005]) cube([x1-x0, 2*(half-chf), 0.01], center=true);
    translate([(x0+x1)/2,0,-th/2+0.005]) cube([x1-x0, 2*half, 0.01], center=true);
  }
}
// channel cutter: Y-Z profile extruded along X
module channel(base,half,straight,height,top){
  translate([-BW/2-1,0,0]) rotate([90,0,90]) linear_extrude(BW+2)
    polygon([[-half,base-0.01],[half,base-0.01],[half,base+straight],
             [top,base+height],[-top,base+height],[-half,base+straight]]);
}

module track(){
  difference(){
    translate([-BW/2,-BH/2,0]) cube([BW,BH,ZT]);
    channel(Z1,C1,V1,H1,T1);
    channel(Z2,C2,V2,H2,T2);
    paper();
  }
}

// Paper recess: full channel width, ramped at both ends so a plate slides out of
// it onto the bare floor without catching on a 0.35 mm step.
module paper(){
  translate([0,PAPW/2,BT]) rotate([90,0,0]) linear_extrude(PAPW)
    polygon([[-(BW-8)/2-PAPR, 0.01], [-(BW-8)/2, -PAP], [(BW-8)/2, -PAP],
             [(BW-8)/2+PAPR, 0.01]]);
}

module slider(){
  difference(){
    union(){
      plate(SX0,SX1,SH/2,ST,CHF);
      translate([SX1-9,0,ST/2]) cube([7,SH-26,1.2], center=true);           // grip
    }
    for(i=[0:5]) for(f=[0:NF-1]){
      g=degree(i,f);
      if(g==0)      translate([xc(f),yc(i),0]) cube([8.6,8.6,ST+2], center=true);
      else if(g==9) translate([xc(f),yc(i),0]) rotate([0,0,45]) cube([6.9,6.9,ST+2], center=true);
      else if(has(PENT,g)) translate([xc(f),yc(i),-ST]) cylinder(h=ST*3, d=8.3);
      else if(has(DIAT,g)) translate([xc(f),yc(i),-ST]) rotate([0,0,90])
                            cylinder(h=ST*3, d=8.8, $fn=3);   // triangle: degrees 4 and 7
    }
    // recess for the shape label (glued paper, nothing engraved)
    translate([RX0, RY0, ST/2-RPAP]) cube([RX1-RX0, RY1-RY0, RPAP+0.01]);
    translate([JX,JYc,0]) cube([JW,JH,ST+2], center=true);                    // KEY window
    for(f=[0:NF-1]) translate([xc(f),FYc,0]) cube([FW,FH,ST+2], center=true); // fret windows
  }
}

// shutter: hides the string area while leaving the shape table and frets visible
KL = 112;                   // length
KS_T = [32.6, 45.2];        // top slot    (shape table / KEY window)
KS_B = [-45.2, -33.0];      // bottom slot (fret numbers)
module shutter(){
  // no raised grip: the slider runs on top. You push it by the slots.
  difference(){
    union(){
      plate(0,KL,KH/2,ST,CHF);
    }
    for(s=[KS_T,KS_B]) difference(){
      translate([3,s[0],-1]) cube([KL-6, s[1]-s[0], ST+2]);
      for(x=[KL*0.32, KL*0.66])                                               // cross bars
        translate([x-1.2,s[0]-1,-2]) cube([2.4, s[1]-s[0]+2, ST+4]);
    }
  }
}

// Test coupon: a short slice of the channel plus a section of each plate. Slide
// them together and you know the fit before committing hours to the real track.
// The wider plate is the shutter (level 1), the narrower one the slider.
// The floor under the recess is shaved down to CFLOOR: the 3 mm of base in the
// real track is most of its mass and none of the fit, so printing it here only
// costs time.
CL = 20;                    // coupon length
CFLOOR = 1.0;               // material left under the paper recess
CTRIM = BT-PAP-CFLOOR;      // how much of the base is cut away
CRAIL = 14;                 // edge rail kept on a coupon plate
CRIB  = 8;                  // central rib kept on a coupon plate
// A coupon plate keeps its two edges (where the dovetail works) and a central
// rib, and is hollow in between -- the real plates are full of slots anyway.
module coupon_plate(half){
  difference(){
    plate(-CL/2,CL/2,half,ST,CHF);
    for(sy=[-1,1]) translate([0, sy*(CRIB/2+(half-CRAIL-CRIB/2)/2), 0])
      cube([CL-6, half-CRAIL-CRIB/2, ST+2], center=true);
  }
}
module coupon(){
  translate([0,0,-CTRIM]) difference(){
    intersection(){ track(); translate([-CL/2,-BH/2,-1]) cube([CL,BH,ZT+2]); }
    translate([-BW,-BH,-1]) cube([2*BW,2*BH,CTRIM+1]);
  }
  translate([CL+15,0,ST/2])   coupon_plate(KH/2);
  translate([2*CL+30,0,ST/2]) coupon_plate(SH/2);
}

if(part=="track") track();
else if(part=="coupon") coupon();
else if(part=="slider") slider();
else if(part=="shutter") shutter();
else { track();
       translate([-BW/2+6,0,Z1+ST/2+0.15]) shutter();
       translate([BW/2-6-KL,0,Z1+ST/2+0.15]) shutter();
       translate([0,0,Z2+ST/2+0.15]) slider(); }
