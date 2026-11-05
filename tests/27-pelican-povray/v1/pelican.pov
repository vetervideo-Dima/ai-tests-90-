// Pelican riding a bicycle
// POV-Ray 3.7
// Render: povray +Ipelican.pov +Orender.png +W1280 +H720 +A0.3 +AM2

#version 3.7;
global_settings { assumed_gamma 1.0 max_trace_level 10 }

#include "colors.inc"
#include "textures.inc"
#include "metals.inc"

// ---------------------------------------------------------------- camera & lights
camera {
  location <0.6, 1.45, -4.6>
  look_at  <0.1, 1.0, 0>
  angle 42
}

light_source {
  <-6, 10, -8>
  color rgb <1.0, 0.97, 0.9> * 1.3
  area_light <1.5,0,0>, <0,0,1.5>, 5, 5 adaptive 1 jitter circular orient
}
light_source { <5, 4, -6> color rgb <0.45, 0.55, 0.7> shadowless }

sky_sphere {
  pigment {
    gradient y
    color_map {
      [0.00 color rgb <0.95, 0.85, 0.70>]
      [0.15 color rgb <0.60, 0.78, 0.95>]
      [0.60 color rgb <0.25, 0.50, 0.85>]
      [1.00 color rgb <0.15, 0.30, 0.70>]
    }
  }
}

// ---------------------------------------------------------------- ground
plane { y, 0
  texture {
    pigment { color rgb <0.35, 0.55, 0.22> }
    normal  { bumps 0.3 scale 0.05 }
    finish  { diffuse 0.8 ambient 0.05 }
  }
}
// road
box { <-20, 0.0, -0.6>, <20, 0.005, 0.8>
  texture {
    pigment { granite color_map { [0 color rgb 0.22][1 color rgb 0.32] } scale 0.2 }
    normal  { granite 0.3 scale 0.05 }
    finish  { diffuse 0.8 }
  }
}
// dashed centre line
#declare I = -20;
#while (I < 20)
  box { <I, 0.006, 0.08>, <I+0.6, 0.007, 0.13> pigment { color rgb <0.95,0.9,0.6> } }
  #declare I = I + 1.2;
#end

// ---------------------------------------------------------------- materials
#declare FrameTex = texture {
  pigment { color rgb <0.80, 0.08, 0.10> }
  finish  { ambient 0.05 diffuse 0.6 specular 0.8 roughness 0.005 reflection 0.08 }
}
#declare Chrome = texture { T_Chrome_3C }
#declare Rubber = texture {
  pigment { color rgb 0.04 }
  finish  { diffuse 0.6 specular 0.1 roughness 0.1 }
}
#declare Feather = texture {
  pigment { color rgb <0.97, 0.96, 0.92> }
  normal  { wrinkles 0.15 scale 0.03 }
  finish  { ambient 0.06 diffuse 0.85 specular 0.05 }
}
#declare FeatherGrey = texture {
  pigment { color rgb <0.72, 0.72, 0.74> }
  finish  { ambient 0.05 diffuse 0.8 }
}
#declare BlackFeather = texture {
  pigment { color rgb 0.06 }
  finish  { diffuse 0.7 specular 0.15 }
}
#declare BeakTex = texture {
  pigment { color rgb <1.0, 0.62, 0.15> }
  finish  { ambient 0.06 diffuse 0.75 specular 0.4 roughness 0.02 }
}
#declare PouchTex = texture {
  pigment { color rgb <0.98, 0.50, 0.30> }
  finish  { ambient 0.06 diffuse 0.7 specular 0.3 roughness 0.03 }
}
#declare LegTex = texture {
  pigment { color rgb <1.0, 0.55, 0.12> }
  finish  { ambient 0.05 diffuse 0.75 specular 0.2 }
}
#declare SeatTex = texture {
  pigment { color rgb 0.08 }
  finish  { diffuse 0.6 specular 0.4 roughness 0.02 }
}

// ---------------------------------------------------------------- bicycle geometry
#declare WR      = 0.34;                 // wheel radius
#declare RearHub = <-0.95, WR, 0>;
#declare FrontHub= < 0.95, WR, 0>;
#declare BB      = <-0.12, 0.30, 0>;     // bottom bracket
#declare SeatTop = <-0.36, 0.88, 0>;
#declare SeatPost= <-0.40, 0.98, 0>;
#declare HeadTop = < 0.68, 0.90, 0>;
#declare HeadBot = < 0.74, 0.72, 0>;
#declare StemTop = < 0.64, 1.05, 0>;
#declare TubeR   = 0.022;

#declare CrankLen   = 0.17;
#declare CrankAngle = 35;   // degrees

#macro Wheel(C)
  union {
    torus { WR-0.025, 0.025 rotate x*90 texture { Rubber } }
    torus { WR-0.055, 0.012 rotate x*90 texture { Chrome } }
    cylinder { <0,0,-0.05>, <0,0,0.05>, 0.03 texture { Chrome } }
    #local S = 0;
    #while (S < 24)
      #local A = S * 15;
      #local Zs = (mod(S,2)=0 ? 0.04 : -0.04);
      cylinder { <0,0,Zs>, <(WR-0.055)*cos(radians(A)), (WR-0.055)*sin(radians(A)), 0>, 0.0035
        texture { Chrome } }
      #local S = S + 1;
    #end
    translate C
  }
#end

#declare Bicycle = union {
  Wheel(RearHub)
  Wheel(FrontHub)

  // main frame
  union {
    cylinder { BB, SeatTop, TubeR }                 // seat tube
    cylinder { SeatTop, HeadTop, TubeR }            // top tube
    cylinder { BB, HeadBot, TubeR*1.15 }            // down tube
    cylinder { HeadTop, HeadBot, TubeR*1.3 }        // head tube
    cylinder { BB + <0,0, 0.05>, RearHub + <0,0, 0.05>, TubeR*0.7 }  // chain stays
    cylinder { BB + <0,0,-0.05>, RearHub + <0,0,-0.05>, TubeR*0.7 }
    cylinder { SeatTop + <0,0, 0.02>, RearHub + <0,0, 0.05>, TubeR*0.7 } // seat stays
    cylinder { SeatTop + <0,0,-0.02>, RearHub + <0,0,-0.05>, TubeR*0.7 }
    cylinder { HeadBot + <0,0, 0.03>, FrontHub + <0,0, 0.05>, TubeR*0.8 } // fork
    cylinder { HeadBot + <0,0,-0.03>, FrontHub + <0,0,-0.05>, TubeR*0.8 }
    sphere { BB, TubeR*1.5 }
    sphere { SeatTop, TubeR }
    sphere { HeadTop, TubeR*1.3 }
    sphere { HeadBot, TubeR*1.3 }
    texture { FrameTex }
  }

  // seat post, saddle
  cylinder { SeatTop, SeatPost, 0.014 texture { Chrome } }
  union {
    sphere { 0, 1 scale <0.13, 0.03, 0.07> translate SeatPost + <0.0, 0.02, 0> }
    sphere { 0, 1 scale <0.09, 0.025, 0.035> translate SeatPost + <0.10, 0.02, 0> }
    texture { SeatTex }
  }

  // stem and handlebar
  cylinder { HeadTop, StemTop, 0.016 texture { Chrome } }
  cylinder { StemTop + <0,0,-0.24>, StemTop + <0,0,0.24>, 0.013 texture { Chrome } }
  cylinder { StemTop + <0,0,-0.26>, StemTop + <0,0,-0.16>, 0.02 texture { Rubber } }
  cylinder { StemTop + <0,0, 0.16>, StemTop + <0,0, 0.26>, 0.02 texture { Rubber } }

  // chainring + chain + cranks
  torus { 0.09, 0.008 rotate x*90 translate BB + <0,0,-0.06> texture { Chrome } }
  cylinder { BB + <0,0,-0.065>, BB + <0,0,-0.055>, 0.085 texture { Chrome } }
  torus { 0.04, 0.006 rotate x*90 translate RearHub + <0,0,-0.06> texture { Chrome } }
  cylinder { BB + <0, 0.09,-0.06>, RearHub + <0, 0.04,-0.06>, 0.005 texture { pigment { color rgb 0.25 } finish { specular 0.5 metallic } } }
  cylinder { BB + <0,-0.09,-0.06>, RearHub + <0,-0.04,-0.06>, 0.005 texture { pigment { color rgb 0.25 } finish { specular 0.5 metallic } } }

  #declare PedalL = BB + <CrankLen*cos(radians(CrankAngle)),      CrankLen*sin(radians(CrankAngle)),      -0.12>;
  #declare PedalR = BB + <CrankLen*cos(radians(CrankAngle+180)),  CrankLen*sin(radians(CrankAngle+180)),   0.12>;
  cylinder { BB + <0,0,-0.08>, PedalL + <0,0,0.03>, 0.012 texture { Chrome } }
  cylinder { BB + <0,0, 0.08>, PedalR - <0,0,0.03>, 0.012 texture { Chrome } }
  cylinder { BB + <0,0,-0.08>, BB + <0,0,0.08>, 0.015 texture { Chrome } }
  box { <-0.045,-0.01,-0.04>, <0.045,0.01,0.04> translate PedalL texture { Rubber } }
  box { <-0.045,-0.01,-0.04>, <0.045,0.01,0.04> translate PedalR texture { Rubber } }
}

// ---------------------------------------------------------------- pelican
#declare BodyC  = <-0.28, 1.28, 0>;
#declare HipL   = <-0.22, 1.08, -0.12>;
#declare HipR   = <-0.22, 1.08,  0.12>;
#declare HeadC  = <0.10, 2.02, 0>;

// two-bone IK: knee pushed forward (+x)
#macro Leg(H, P, L1, L2)
  #local D  = vlength(P - H);
  #local Dc = min(D, L1 + L2 - 0.001);
  #local Dir = (P - H) / D;
  #local A  = (L1*L1 - L2*L2 + Dc*Dc) / (2*Dc);
  #local Hh = sqrt(max(L1*L1 - A*A, 0));
  #local Perp = vnormalize(<-Dir.y, Dir.x, 0>);
  #if (Perp.x < 0) #local Perp = -Perp; #end
  #local K  = H + Dir*A + Perp*Hh;
  #local Pc = H + Dir*Dc;
  union {
    // feathered thigh
    sphere_sweep { linear_spline 2, H, 0.075, K, 0.045 texture { Feather } }
    // bare orange shin
    cylinder { K, Pc, 0.022 texture { LegTex } }
    sphere   { K, 0.03 texture { LegTex } }
    // webbed foot resting on pedal
    union {
      sphere { 0, 1 scale <0.10, 0.012, 0.055> translate <0.04, 0, 0> }
      sphere { 0, 0.025 }
      texture { LegTex }
      translate Pc + <0, 0.02, 0>
    }
  }
#end

#declare Pelican = union {
  // body
  sphere { 0, 1 scale <0.46, 0.28, 0.27> rotate z*-12 translate BodyC texture { Feather } }
  // tail
  sphere { 0, 1 scale <0.18, 0.06, 0.15> rotate z*18 translate BodyC + <-0.48, 0.08, 0> texture { FeatherGrey } }

  // folded wings along the body
  #macro WingFold(Zs)
    union {
      sphere { 0, 1 scale <0.40, 0.17, 0.05> rotate z*-10 translate <0,0,0> texture { FeatherGrey } }
      sphere { 0, 1 scale <0.22, 0.08, 0.04> rotate z*8 translate <-0.38, 0.03, 0> texture { BlackFeather } }
      translate BodyC + <-0.05, 0.03, Zs*0.26>
    }
  #end
  WingFold(-1)
  WingFold(1)

  // wing "arms" reaching the handlebar grips
  sphere_sweep {
    cubic_spline 5,
    BodyC + <-0.2, 0.15, -0.30>, 0.06,
    BodyC + < 0.15, 0.08, -0.29>, 0.06,
    BodyC + < 0.55, -0.05, -0.27>, 0.045,
    StemTop + <0.02, 0.02, -0.21>, 0.03,
    StemTop + <0.10, 0.00, -0.21>, 0.03
    texture { FeatherGrey }
  }
  sphere_sweep {
    cubic_spline 5,
    BodyC + <-0.2, 0.15, 0.30>, 0.06,
    BodyC + < 0.15, 0.08, 0.29>, 0.06,
    BodyC + < 0.55, -0.05, 0.27>, 0.045,
    StemTop + <0.02, 0.02, 0.21>, 0.03,
    StemTop + <0.10, 0.00, 0.21>, 0.03
    texture { FeatherGrey }
  }
  // wing-tip "fingers" around the grips
  sphere { 0, 1 scale <0.06, 0.035, 0.04> translate StemTop + <0.0, 0.01, -0.21> texture { BlackFeather } }
  sphere { 0, 1 scale <0.06, 0.035, 0.04> translate StemTop + <0.0, 0.01,  0.21> texture { BlackFeather } }

  // S-curved neck
  sphere_sweep {
    cubic_spline 6,
    BodyC + <0.10, -0.05, 0>, 0.13,
    BodyC + <0.30,  0.10, 0>, 0.12,
    <0.12, 1.62, 0>, 0.085,
    <0.02, 1.85, 0>, 0.075,
    HeadC + <0.0, 0.0, 0>, 0.08,
    HeadC + <0.1, 0.05, 0>, 0.08
    texture { Feather }
  }

  // head
  sphere { 0, 1 scale <0.13, 0.11, 0.10> translate HeadC texture { Feather } }
  // pale yellow crown
  sphere { 0, 1 scale <0.09, 0.05, 0.07> translate HeadC + <-0.02, 0.08, 0>
    texture { pigment { color rgb <1.0, 0.92, 0.55> } finish { diffuse 0.8 } } }

  // eyes
  #macro Eye(Zs)
    union {
      sphere { 0, 0.022 texture { pigment { color rgb <1, 0.95, 0.85> } finish { specular 0.6 } } }
      sphere { <0.005, 0.0, Zs*0.016>, 0.012 texture { pigment { color rgb 0.02 } finish { specular 0.9 roughness 0.002 } } }
      translate HeadC + <0.05, 0.03, Zs*0.085>
    }
  #end
  Eye(-1)
  Eye(1)

  // beak: long upper mandible, hooked tip, pouch below
  union {
    cone { <0,0,0>, 0.055, <0.68,0,0>, 0.016 scale <1, 0.45, 1> texture { BeakTex } }
    sphere { <0.69, -0.012, 0>, 0.022 texture { pigment { color rgb <0.85, 0.30, 0.10> } finish { specular 0.4 } } }
    // pouch
    intersection {
      sphere { 0, 1 scale <0.34, 0.11, 0.055> translate <0.33, -0.035, 0> }
      plane  { y, -0.012 }
      texture { PouchTex }
    }
    rotate z*-16
    translate HeadC + <0.09, -0.02, 0>
  }

  // legs to the pedals
  Leg(HipL, PedalL, 0.48, 0.50)
  Leg(HipR, PedalR, 0.48, 0.50)
}

// ---------------------------------------------------------------- scene
union {
  object { Bicycle }
  object { Pelican }
  rotate y*-18
}

// a few background trees
#macro Tree(P, S)
  union {
    cylinder { <0,0,0>, <0,1.2,0>, 0.08 pigment { color rgb <0.35,0.22,0.12> } }
    sphere { <0,1.6,0>, 0.7 pigment { color rgb <0.18,0.42,0.15> } normal { bumps 0.6 scale 0.15 } }
    sphere { <0.35,1.35,0.1>, 0.45 pigment { color rgb <0.2,0.45,0.17> } normal { bumps 0.6 scale 0.15 } }
    scale S
    translate P
  }
#end
Tree(<-4.5, 0, 6>, 1.4)
Tree(<-1.8, 0, 9>, 1.8)
Tree(< 3.5, 0, 7>, 1.5)
Tree(< 6.5, 0, 11>, 2.0)
