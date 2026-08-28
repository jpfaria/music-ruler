// ==========================================================================
//  SCALE RULER v4 -- track + cassette + blade + slider
//
//  Three stacked dovetail channels, each with its own retention, so the
//  moving parts never fight for room and can cross each other:
//    channel 1 (bottom) -> cassette: two masks rigidly joined, with a
//                          4-fret window between them. One move selects
//                          which CAGED shape stays visible.
//    channel 2 (middle) -> blade: covers the one extra fret when the shape
//                          is 3 frets wide instead of 4. It lives under the
//                          slider, so it is worked by two tails that always
//                          reach past it. PULL a tail, never push.
//    channel 3 (top)    -> the sliding ruler.
//
//  part = "track" | "slider" | "cassette" | "blade" | "coupon" | "assembled"
// ==========================================================================
part="assembled"; $fn=48;

CW = 10.2;                  // fret width
NF = 13;                    // frets covered by the slider
RS = 11.2;                  // string spacing
BW = 280; BH = 108; BT = 3.0;
PAP = 0.35;                 // paper recess

// ---- the three channels --------------------------------------------------
// Every level is the one below stepped inwards by LSTEP, which leaves a
// LSTEP+... ledge for the plate above to rest on.
C0 = 49.0;                  // half-width of the bottom channel floor
LSTEP = 0.6;                // each level is this much narrower per side
V = 0.8;                    // straight run before the 45-degree undercut
H = 2.6;                    // channel height: the ramp is H-V = 1.8 mm long,
                            // which is what buys a loose fit AND a deep grip
function CH(k) = C0 - k*LSTEP;              // floor half-width of level k
function TH(k) = CH(k) - (H-V);             // mouth half-width of level k
function ZH(k) = BT + k*H;                  // floor height of level k
ZT = BT + 3*H;              // top of the walls = 10.8

ST = 1.8;  CHF = 1.0;       // plate thickness and 45-degree top chamfer
BCHF = 0.4;                 // relief on the bottom edge for the squished
                            // first layer (elephant's foot)

// ---- fit -----------------------------------------------------------------
// A PETG plate leaves the bed wider than the model and the channel comes out
// narrower, so 0.15 and 0.25 per side both printed too tight to slide.
FIT = 0.50;                 // per side; drop to 0.4 if your printer runs small
function PLATE(k) = CH(k) - FIT;            // plate half-width for level k
function GRIP(k)  = PLATE(k) - TH(k);       // dovetail grip per side = 1.3

PAPW = 2*C0;                // the paper recess spans the WHOLE channel floor,
                            // so a plate is supported edge to edge whatever
                            // the paper thickness -- a narrower recess leaves
                            // two thin ledges for it to balance on and tip off
PAPR = 2.0;                 // ramp at each end of the recess

// The real invariant: shove a plate as far to one side as the play allows and
// the far side must STILL be well engaged. That leftover is GRIP-FIT.
assert(GRIP(0)-FIT >= 0.5, "level 1: plate can slide off its own ledge");
assert(GRIP(1)-FIT >= 0.5, "level 2: plate can slide off its own ledge");
assert(GRIP(2)-FIT >= 0.5, "level 3: plate can slide off its own ledge");
assert(ST+FIT <= H, "a lifted plate reaches the channel above it");
assert(ST-CHF == V, "plate chamfer no longer matches the channel profile");
assert(PAPW >= 2*PLATE(0), "cassette wider than the paper recess");
echo(str("fit: play ",FIT," mm/side  grip ",GRIP(0)," mm/side  gap to the level above ",H-ST-FIT," mm"));

TUNING=[4,9,2,7,11,4];
DIAT=[0,2,4,5,7,9,11]; PENT=[0,2,4,7,9];
OFF=8;
SX0=-80.2; SX1=74.2;
JW=10.2; JH=10.6; JX=-71.4; JYc=39.2;       // KEY window on the slider
FW=8.8; FH=7.4; FYc=-38.5;                  // fret windows
RX0=-65.0; RX1=65.0; RY0=32.6; RY1=45.2; RPAP=0.35;   // shape-label recess

// ---- what a mask has to cover, and what it must never cover --------------
MB = 33.5;                  // mask half-height: covers every note hole ...
RAIL_I = 45.0;              // ... and stops short of the KEY window (44.5) and
                            // the fret windows (34.8..42.2), which stay
                            // readable. Beyond RAIL_I is the edge rail that
                            // the dovetail grabs.

function degree(i,f) = (TUNING[i]+f+OFF)%12;
function has(v,g) = len([for(a=v) if(a==g) 1])>0;
function xc(f) = -((NF-1)/2)*CW + f*CW;
function yc(i) = -((6-1)/2)*RS + i*RS;

// Plate: 45-degree chamfer on both long top edges (that is the dovetail face)
// and a small relief on the bottom edges for the first-layer squish.
module plate(x0,x1,half,th=ST,chf=CHF){
  hull(){
    translate([(x0+x1)/2,0,th/2-0.005])  cube([x1-x0, 2*(half-chf), 0.01], center=true);
    translate([(x0+x1)/2,0,-th/2+BCHF])  cube([x1-x0, 2*half, 0.01], center=true);
    translate([(x0+x1)/2,0,-th/2+0.005]) cube([x1-x0, 2*(half-BCHF), 0.01], center=true);
  }
}
// channel cutter: Y-Z profile extruded along X
module channel(k){
  base=ZH(k); half=CH(k); top=TH(k);
  translate([-BW/2-1,0,0]) rotate([90,0,90]) linear_extrude(BW+2)
    polygon([[-half,base-0.01],[half,base-0.01],[half,base+V],
             [top,base+H],[-top,base+H],[-half,base+V]]);
}
// Paper recess: full channel width, ramped at both ends so a plate slides out
// of it onto the bare floor without catching on a 0.35 mm step.
module paper(){
  translate([0,PAPW/2,BT]) rotate([90,0,0]) linear_extrude(PAPW)
    polygon([[-(BW-8)/2-PAPR, 0.01], [-(BW-8)/2, -PAP], [(BW-8)/2, -PAP],
             [(BW-8)/2+PAPR, 0.01]]);
}

module track(){
  difference(){
    translate([-BW/2,-BH/2,0]) cube([BW,BH,ZT]);
    for(k=[0:2]) channel(k);
    paper();
  }
}

// The two long openings of a masking plate: they keep the KEY window and the
// fret numbers readable, and they are where a finger pushes the cassette.
module mask_slots(x0,x1,bars=2){
  for(s=[[MB,RAIL_I],[-RAIL_I,-MB]]) difference(){
    translate([x0+3,s[0],-1]) cube([x1-x0-6, s[1]-s[0], ST+2]);
    for(i=[1:bars]) translate([x0+(x1-x0)*i/(bars+1)-1.2, s[0]-1, -2])
      cube([2.4, s[1]-s[0]+2, ST+4]);
  }
}

// ------------------------------- CASSETTE ---------------------------------
AP    = 4*CW;               // window = the widest CAGED box, 4 frets
MASKL = NF*CW - AP;         // 91.8: what one mask covers when the box sits at
                            // the very end of the slider window
CASL  = 2*MASKL + AP;       // 224.4 overall
module cassette(){
  half=PLATE(0);
  difference(){
    union(){
      plate(-CASL/2, -AP/2, half);
      plate( AP/2,    CASL/2, half);
      // the window: only the two edge rails carry across
      for(sy=[-1,1]) intersection(){
        plate(-AP/2, AP/2, half);
        translate([0, sy*(half+RAIL_I)/2, 0]) cube([AP, half-RAIL_I, ST+2], center=true);
      }
    }
    mask_slots(-CASL/2, -AP/2, 2);
    mask_slots( AP/2,    CASL/2, 2);
  }
}

// -------------------------------- BLADE -----------------------------------
BLW  = CW+0.8;              // covers one fret column of holes
TAIL_L = 85;                // reaches past the slider from any position
TAIL_I = 43.0;              // inner edge of the tail
// The tails are not loose strips: each one keeps the dovetail edge profile, so
// it rides in the channel like the plate does. A bare 85 mm strip hanging off
// an 11 mm mask would pitch down into the channel below and jam. They run
// under the solid bottom rail of the slider, so they are never visible.
module blade(){
  half=PLATE(1);
  plate(-BLW/2, BLW/2, half);
  for(sx=[-1,1]) intersection(){
    plate(min(sx*BLW/2, sx*(BLW/2+TAIL_L)), max(sx*BLW/2, sx*(BLW/2+TAIL_L)), half);
    translate([sx*(BLW/2+TAIL_L/2), -(half+TAIL_I)/2, 0])
      cube([TAIL_L+1, half-TAIL_I, ST+2], center=true);
  }
}

// -------------------------------- SLIDER ----------------------------------
module slider(){
  half=PLATE(2);
  difference(){
    union(){
      plate(SX0,SX1,half);
      translate([SX1-9,0,ST/2]) cube([7,2*half-26,1.2], center=true);        // grip
    }
    for(i=[0:5]) for(f=[0:NF-1]){
      g=degree(i,f);
      if(g==0)      translate([xc(f),yc(i),0]) cube([8.6,8.6,ST+2], center=true);
      else if(g==9) translate([xc(f),yc(i),0]) rotate([0,0,45]) cube([6.9,6.9,ST+2], center=true);
      else if(has(PENT,g)) translate([xc(f),yc(i),-ST]) cylinder(h=ST*3, d=8.3);
      else if(has(DIAT,g)) translate([xc(f),yc(i),-ST]) rotate([0,0,90])
                            cylinder(h=ST*3, d=8.8, $fn=3);   // triangle: degrees 4 and 7
    }
    translate([RX0, RY0, ST/2-RPAP]) cube([RX1-RX0, RY1-RY0, RPAP+0.01]);     // label recess
    translate([JX,JYc,0]) cube([JW,JH,ST+2], center=true);                    // KEY window
    for(f=[0:NF-1]) translate([xc(f),FYc,0]) cube([FW,FH,ST+2], center=true); // fret windows
  }
}

// -------------------------------- COUPON ----------------------------------
// A short slice of the channel plus a section of each plate: ten minutes to
// print, and it answers the only question that matters before the big print.
CL = 20; CFLOOR = 1.0; CTRIM = BT-PAP-CFLOOR;
CRAIL = 14; CRIB = 8;
module coupon_plate(half){
  difference(){
    plate(-CL/2,CL/2,half);
    for(sy=[-1,1]) translate([0, sy*(CRIB/2+(half-CRAIL-CRIB/2)/2), 0])
      cube([CL-6, half-CRAIL-CRIB/2, ST+2], center=true);
  }
}
module coupon(){
  translate([0,0,-CTRIM]) difference(){
    intersection(){ track(); translate([-CL/2,-BH/2,-1]) cube([CL,BH,ZT+2]); }
    translate([-BW,-BH,-1]) cube([2*BW,2*BH,CTRIM+1]);
  }
  for(k=[0:2]) translate([(k+1)*(CL+15),0,ST/2]) coupon_plate(PLATE(k));
}

if(part=="track") track();
else if(part=="slider") slider();
else if(part=="cassette") cassette();
else if(part=="blade") blade();
else if(part=="coupon") coupon();
else if(part=="assembled"){
  track();
  translate([-30,0,ZH(0)+ST/2+0.1]) cassette();
  translate([ 40,0,ZH(1)+ST/2+0.1]) blade();
  translate([  0,0,ZH(2)+ST/2+0.1]) slider();
}
