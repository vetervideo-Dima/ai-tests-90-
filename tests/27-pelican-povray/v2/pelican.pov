// Pelican riding a bicycle — v2
// POV-Ray 3.7
// Still:     povray +Ipelican.pov +Orender.png +W1280 +H720 +A0.2 +AM2 +R3
// Animation: povray +Ipelican.pov +Oframe.png +W640 +H360 +A0.3 +KFI1 +KFF24 +KC
//            (clock 0..1 = one full pedal revolution; frames loop seamlessly)

#version 3.7;

#ifndef (Quality) #declare Quality = 1; #end   // 0 = fast preview (no radiosity, hard shadows)

global_settings {
  assumed_gamma 1.0
  max_trace_level 12
  #if (Quality > 0)
  radiosity {
    pretrace_start 0.08 pretrace_end 0.01
    count 80 error_bound 0.8 recursion_limit 1
    nearest_count 6 low_error_factor 0.6
    gray_threshold 0.0 brightness 1.0
    adc_bailout 0.01
  }
  #end
}

#include "colors.inc"
#include "metals.inc"

// ---------------------------------------------------------------- animation
#declare T          = clock;               // 0..1
#declare CrankAngle = 35 + T*360;          // pedal crank angle (deg)
#declare WheelSpin  = -T*360*1.6;          // wheels turn faster than cranks (gear)

// ---------------------------------------------------------------- camera
camera {
  location <1.55, 1.25, -5.0>
  look_at  <0.20, 1.05, 0>
  angle 44
}

// ---------------------------------------------------------------- lights
// warm late-afternoon sun
light_source {
  <-9, 9, -6>
  color rgb <1.0, 0.88, 0.70> * 1.4
  #if (Quality > 0)
  area_light <1.2,0,0>, <0,0,1.2>, 6, 6 adaptive 1 jitter circular orient
  #end
}
// cool sky fill (no shadow)
light_source { <6, 6, -9> color rgb <0.35, 0.45, 0.65> * 0.55 shadowless }
// rim light from behind to separate white feathers from the sky
light_source { <3, 4, 8> color rgb <1.0, 0.85, 0.7> * 0.5 shadowless }

// ---------------------------------------------------------------- sky
sky_sphere {
  pigment {
    gradient y
    color_map {
      [0.00 color rgb <1.00, 0.80, 0.58>]
      [0.10 color rgb <0.92, 0.82, 0.74>]
      [0.30 color rgb <0.52, 0.70, 0.92>]
      [0.70 color rgb <0.22, 0.45, 0.82>]
      [1.00 color rgb <0.12, 0.28, 0.66>]
    }
  }
  // soft clouds
  pigment {
    bozo
    turbulence 0.65 octaves 6 omega 0.55 lambda 2.2
    color_map {
      [0.00 color rgbt <1, 1, 1, 1>]
      [0.50 color rgbt <1, 1, 1, 1>]
      [0.68 color rgbt <1.0, 0.95, 0.90, 0.35>]
      [1.00 color rgbt <0.95, 0.92, 0.90, 0.05>]
    }
    scale <0.35, 0.08, 0.35>
    translate <0.3, 0.05, 0>
  }
}

// ---------------------------------------------------------------- ground
plane { y, 0
  texture {
    pigment {
      granite turbulence 0.3
      color_map {
        [0.0 color rgb <0.26, 0.46, 0.15>]
        [0.6 color rgb <0.36, 0.56, 0.20>]
        [1.0 color rgb <0.50, 0.62, 0.25>]
      }
      scale 0.6
    }
    normal { bumps 0.5 scale 0.03 }
    finish { diffuse 0.8 ambient 0 }
  }
}

// asphalt road with kerb lines
union {
  box { <-60, 0.0, -0.7>, <60, 0.008, 0.9>
    texture {
      pigment { granite color_map { [0 color rgb 0.20][0.7 color rgb 0.27][1 color rgb 0.36] } scale 0.08 }
      normal  { granite 0.35 scale 0.02 }
      finish  { diffuse 0.85 specular 0.05 roughness 0.1 }
    }
  }
  box { <-60, 0.0, -0.74>, <60, 0.012, -0.70> pigment { color rgb 0.85 } }
  box { <-60, 0.0,  0.90>, <60, 0.012,  0.94> pigment { color rgb 0.85 } }
}
#declare I = -60;
#while (I < 60)
  box { <I, 0.009, 0.08>, <I+0.7, 0.010, 0.13> pigment { color rgb <0.98,0.88,0.45> } finish { diffuse 0.9 } }
  #declare I = I + 1.4;
#end

// rolling hills in the distance (hazed by the fog)
#declare HillTex = texture {
  pigment { granite color_map { [0 color rgb <0.34,0.47,0.33>][1 color rgb <0.42,0.54,0.40>] } scale 3 }  // pale = aerial haze
  finish { diffuse 0.8 }
}
sphere { 0, 1 scale <22, 4.5, 8>  translate <-18, -1.5, 34> texture { HillTex } }
sphere { 0, 1 scale <26, 6.0, 9>  translate < 14, -2.8, 40> texture { HillTex } }
sphere { 0, 1 scale <18, 3.0, 7>  translate < -2, -1.2, 28> texture { HillTex } }

// trees
#declare R = seed(27);
#macro Tree(P, S)
  union {
    cone { <0,0,0>, 0.11, <0,1.3,0>, 0.06
      pigment { color rgb <0.33,0.21,0.12> } normal { wrinkles 0.6 scale <0.02,0.2,0.02> } }
    #local K = 0;
    #while (K < 7)
      sphere { <(rand(R)-0.5)*0.9, 1.45+rand(R)*0.6, (rand(R)-0.5)*0.9>, 0.38+rand(R)*0.25
        texture {
          pigment { color rgb <0.14+rand(R)*0.08, 0.36+rand(R)*0.12, 0.12> }
          normal  { bumps 0.9 scale 0.08 }
          finish  { diffuse 0.75 }
        }
      }
      #local K = K + 1;
    #end
    scale S
    translate P
  }
#end
Tree(<-5.2, 0,  5.5>, 1.35)
Tree(<-2.4, 0,  9.0>, 1.80)
Tree(< 3.8, 0,  6.5>, 1.45)
Tree(< 7.2, 0, 11.0>, 2.00)
Tree(<-9.0, 0, 12.0>, 2.20)
Tree(< 11., 0,  8.0>, 1.60)

// ---------------------------------------------------------------- materials
#declare FrameTex = texture {
  pigment { color rgb <0.78, 0.06, 0.08> }
  finish  { ambient 0 diffuse 0.55 specular 0.9 roughness 0.004 reflection { 0.04, 0.15 fresnel on } conserve_energy }
}
#declare Chrome = texture {
  pigment { color rgb <0.80, 0.80, 0.82> }
  finish  { ambient 0 diffuse 0.15 brilliance 4 specular 0.9 roughness 0.002 metallic reflection 0.6 }
}
#declare Rubber = texture {
  pigment { color rgb 0.035 }
  finish  { diffuse 0.6 specular 0.12 roughness 0.08 }
}
#declare Feather = texture {
  pigment { color rgb <0.97, 0.95, 0.90> }
  normal  { wrinkles 0.12 scale <0.06, 0.015, 0.03> }
  finish  { ambient 0 diffuse 0.85 specular 0.06 roughness 0.1 }
}
#declare FeatherGrey = texture {
  pigment { color rgb <0.78, 0.78, 0.80> }
  normal  { wrinkles 0.15 scale <0.05, 0.012, 0.02> }
  finish  { ambient 0 diffuse 0.8 }
}
#declare BlackFeather = texture {
  pigment { color rgb 0.05 }
  finish  { diffuse 0.7 specular 0.2 roughness 0.03 }
}
#declare BeakTex = texture {
  pigment {
    gradient x
    color_map {
      [0.0 color rgb <0.98, 0.70, 0.35>]
      [0.8 color rgb <1.00, 0.60, 0.18>]
      [1.0 color rgb <0.90, 0.38, 0.12>]
    }
    scale 0.7
  }
  finish  { ambient 0 diffuse 0.75 specular 0.45 roughness 0.015 }
}
#declare PouchTex = texture {
  pigment {
    gradient y
    color_map {
      [0.0 color rgb <0.95, 0.45, 0.26>]
      [1.0 color rgb <1.00, 0.70, 0.40>]
    }
    scale 0.2 translate -0.15*y
  }
  normal { wrinkles 0.25 scale <0.08, 0.01, 0.02> }
  finish { ambient 0 diffuse 0.7 specular 0.35 roughness 0.025 }
}
#declare LegTex = texture {
  pigment { color rgb <1.0, 0.52, 0.10> }
  normal  { bumps 0.25 scale 0.01 }
  finish  { ambient 0 diffuse 0.75 specular 0.25 roughness 0.04 }
}
#declare SeatTex = texture {
  pigment { color rgb <0.22, 0.12, 0.06> }
  finish  { diffuse 0.6 specular 0.45 roughness 0.02 }
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
#declare StemTop = < 0.62, 1.06, 0>;
#declare TubeR   = 0.022;
#declare CrankLen = 0.17;
#declare GripL   = StemTop + <0.0, 0.0, -0.21>;
#declare GripR   = StemTop + <0.0, 0.0,  0.21>;

#macro Wheel(C)
  union {
    // tyre with tread
    torus { WR-0.025, 0.026 rotate x*90
      texture { Rubber normal { gradient x 0.4 frequency 1 scale 0.008 } } }
    // rim
    difference {
      cylinder { <0,0,-0.014>, <0,0,0.014>, WR-0.045 }
      cylinder { <0,0,-0.02>,  <0,0,0.02>,  WR-0.065 }
      texture { Chrome }
    }
    // hub
    cylinder { <0,0,-0.055>, <0,0,0.055>, 0.022 texture { Chrome } }
    cylinder { <0,0,-0.045>, <0,0,-0.035>, 0.04 texture { Chrome } }
    cylinder { <0,0, 0.035>, <0,0, 0.045>, 0.04 texture { Chrome } }
    // tangentially laced spokes
    #local S = 0;
    #while (S < 32)
      #local A  = S * 360/32;
      #local Zs = (mod(S,2)=0 ? 0.04 : -0.04);
      #local Ah = A + (mod(floor(S/2),2)=0 ? 1 : -1) * 40;
      cylinder { <0.035*cos(radians(Ah)), 0.035*sin(radians(Ah)), Zs>,
                 <(WR-0.06)*cos(radians(A)), (WR-0.06)*sin(radians(A)), 0>, 0.0028
        texture { Chrome } }
      #local S = S + 1;
    #end
    // valve
    cylinder { <0, -(WR-0.06), 0>, <0, -(WR-0.08), 0>, 0.005 texture { Chrome } }
    rotate z*WheelSpin
    translate C
  }
#end

// chain: links distributed along the loop around chainring and sprocket
#macro Chain(C1, R1, C2, R2, Z)
  #local D    = vlength(C2 - C1);
  #local Ang  = degrees(asin((R1 - R2)/D));
  #local Base = degrees(atan2(C2.y - C1.y, C2.x - C1.x));
  // upper and lower tangent points
  #local N1u = <cos(radians(Base+90+Ang)), sin(radians(Base+90+Ang)), 0>;
  #local N1d = <cos(radians(Base-90-Ang)), sin(radians(Base-90-Ang)), 0>;
  #local P1u = C1 + N1u*R1;  #local P2u = C2 + N1u*R2;
  #local P1d = C1 + N1d*R1;  #local P2d = C2 + N1d*R2;
  union {
    #local Step = 0.018;
    // straight runs
    #local L = vlength(P2u - P1u); #local K = 0;
    #while (K*Step < L)
      #local P = P1u + (P2u - P1u)*(K*Step/L);
      box { <-0.007,-0.004,-0.006>, <0.007,0.004,0.006>
        rotate z*Base translate P + <0,0,Z> }
      #local K = K + 1;
    #end
    #local L = vlength(P2d - P1d); #local K = 0;
    #while (K*Step < L)
      #local P = P1d + (P2d - P1d)*(K*Step/L);
      box { <-0.007,-0.004,-0.006>, <0.007,0.004,0.006>
        rotate z*Base translate P + <0,0,Z> }
      #local K = K + 1;
    #end
    texture { pigment { color rgb 0.22 } finish { metallic specular 0.6 roughness 0.02 diffuse 0.5 } }
  }
#end

#declare PedalL = BB + <CrankLen*cos(radians(CrankAngle)),     CrankLen*sin(radians(CrankAngle)),     -0.13>;
#declare PedalR = BB + <CrankLen*cos(radians(CrankAngle+180)), CrankLen*sin(radians(CrankAngle+180)),  0.13>;

#declare Bicycle = union {
  Wheel(RearHub)
  Wheel(FrontHub)

  // main frame
  union {
    cylinder { BB, SeatTop, TubeR }
    cylinder { SeatTop, HeadTop, TubeR }
    cylinder { BB, HeadBot, TubeR*1.2 }
    cylinder { HeadTop + <0.0,0.02,0>, HeadBot - <0.0,0.02,0>, TubeR*1.35 }
    cylinder { BB + <0,0, 0.05>, RearHub + <0,0, 0.05>, TubeR*0.65 }
    cylinder { BB + <0,0,-0.05>, RearHub + <0,0,-0.05>, TubeR*0.65 }
    cylinder { SeatTop + <0,0, 0.015>, RearHub + <0,0, 0.05>, TubeR*0.6 }
    cylinder { SeatTop + <0,0,-0.015>, RearHub + <0,0,-0.05>, TubeR*0.6 }
    // fork with a slight forward rake
    sphere_sweep { cubic_spline 4, HeadBot + <-0.03,0.05, 0.035>, 0.018, HeadBot + <0,0, 0.035>, 0.018,
                   FrontHub + <0,0, 0.05>, 0.012, FrontHub + <0.06,-0.06, 0.05>, 0.012 }
    sphere_sweep { cubic_spline 4, HeadBot + <-0.03,0.05,-0.035>, 0.018, HeadBot + <0,0,-0.035>, 0.018,
                   FrontHub + <0,0,-0.05>, 0.012, FrontHub + <0.06,-0.06,-0.05>, 0.012 }
    box { <-0.03,-0.012,-0.05>, <0.03,0.012,0.05> rotate z*-18 translate HeadBot }   // fork crown
    sphere { BB, TubeR*1.6 }
    sphere { SeatTop, TubeR*1.1 }
    texture { FrameTex }
  }
  // headset rings
  cylinder { HeadTop + <0,0.02,0>, HeadTop + <0,0.035,0>, 0.034 texture { Chrome } }
  cylinder { HeadBot - <0,0.02,0>, HeadBot - <0,0.035,0>, 0.034 texture { Chrome } }

  // mudguards
  intersection {
    difference { cylinder { <0,0,-0.03>,<0,0,0.03>, WR+0.03 } cylinder { <0,0,-0.04>,<0,0,0.04>, WR+0.02 } }
    plane { -x, 0 rotate z*-30 }
    plane { y, 0 rotate z*-80 inverse }
    translate RearHub
    texture { Chrome }
  }

  // seat post, sprung leather saddle
  cylinder { SeatTop, SeatPost, 0.014 texture { Chrome } }
  union {
    sphere { 0, 1 scale <0.13, 0.032, 0.075> translate SeatPost + <0.0, 0.025, 0> }
    sphere { 0, 1 scale <0.10, 0.025, 0.035> translate SeatPost + <0.10, 0.025, 0> }
    texture { SeatTex }
  }
  torus { 0.012, 0.004 rotate z*90 translate SeatPost + <-0.07, 0.0, -0.04> texture { Chrome } }
  torus { 0.012, 0.004 rotate z*90 translate SeatPost + <-0.07, 0.0,  0.04> texture { Chrome } }

  // stem, swept-back handlebar, grips, bell
  cylinder { HeadTop, StemTop, 0.016 texture { Chrome } }
  sphere_sweep {
    cubic_spline 6,
    StemTop + <-0.10,0,-0.30>, 0.012,
    GripL + <-0.08,0,-0.02>, 0.012,
    StemTop + <0.03,0,-0.10>, 0.012,
    StemTop + <0.03,0, 0.10>, 0.012,
    GripR + <-0.08,0, 0.02>, 0.012,
    StemTop + <-0.10,0, 0.30>, 0.012
    texture { Chrome }
  }
  cylinder { GripL + <-0.12,0,-0.025>, GripL + <-0.02,0,-0.01>, 0.021 texture { Rubber } }
  cylinder { GripR + <-0.12,0, 0.025>, GripR + <-0.02,0, 0.01>, 0.021 texture { Rubber } }
  union {
    sphere { 0, 0.03 scale <1, 0.6, 1> }
    cylinder { <0,-0.02,0>, <0,0,0>, 0.006 }
    translate StemTop + <0.03, 0.03, 0.10>
    texture { pigment { color rgb <0.95,0.78,0.25> } finish { metallic specular 0.9 roughness 0.003 reflection 0.3 } }
  }
  // headlamp
  union {
    cylinder { <0,0,0>, <0.04,0,0>, 0.025 texture { Chrome } }
    disc { <0.041,0,0>, x, 0.02 texture { pigment { color rgb <1,0.95,0.7> } finish { emission 0.9 } } }
    translate HeadTop + <0.04, -0.06, 0>
  }

  // drivetrain
  union {
    difference {
      cylinder { <0,0,-0.006>, <0,0,0.006>, 0.095 }
      #local K = 0;
      #while (K < 5)
        cylinder { <0,0,-0.01>, <0,0,0.01>, 0.028 translate <0.055,0,0> rotate z*(K*72) }
        #local K = K + 1;
      #end
      rotate z*CrankAngle
      translate BB + <0,0,-0.065>
    }
    cylinder { <0,0,-0.006>, <0,0,0.006>, 0.042 translate RearHub + <0,0,-0.065> }
    texture { Chrome }
  }
  Chain(BB, 0.098, RearHub, 0.045, -0.065)

  // cranks and pedals
  cylinder { BB + <0,0,-0.085>, PedalL + <0,0,0.035>, 0.012 texture { Chrome } }
  cylinder { BB + <0,0, 0.085>, PedalR - <0,0,0.035>, 0.012 texture { Chrome } }
  cylinder { BB + <0,0,-0.085>, BB + <0,0,0.085>, 0.016 texture { Chrome } }
  box { <-0.045,-0.012,-0.04>, <0.045,0.012,0.04> translate PedalL texture { Rubber } }
  box { <-0.045,-0.012,-0.04>, <0.045,0.012,0.04> translate PedalR texture { Rubber } }
}

// ---------------------------------------------------------------- pelican
#declare BodyC  = <-0.24, 1.30, 0>;
#declare HipL   = <-0.24, 1.10, -0.13>;
#declare HipR   = <-0.24, 1.10,  0.13>;
#declare Bob    = 0.012*sin(radians(CrankAngle*2));    // tiny body bob while pedalling
#declare HeadC  = <0.16, 2.00 + Bob, 0>;

// two-bone IK, knee pushed forward (+x)
#macro Leg(H, P, L1, L2)
  #local D   = vlength(P - H);
  #local Dc  = min(D, L1 + L2 - 0.001);
  #local Dir = (P - H) / D;
  #local A   = (L1*L1 - L2*L2 + Dc*Dc) / (2*Dc);
  #local Hh  = sqrt(max(L1*L1 - A*A, 0));
  #local Perp = vnormalize(<-Dir.y, Dir.x, 0>);
  #if (Perp.x < 0) #local Perp = -Perp; #end
  #local K   = H + Dir*A + Perp*Hh;
  #local Pc  = H + Dir*Dc;
  #local Ka  = K + (Pc - K)*0.22;      // feathers stop a bit below the knee
  union {
    // feathered thigh, tapering
    sphere_sweep { linear_spline 3, H, 0.085, K, 0.05, Ka, 0.032 texture { Feather } }
    // scaly orange shank
    cylinder { K, Pc + <0,0.02,0>, 0.02 texture { LegTex } }
    sphere   { K, 0.028 texture { LegTex } }
    // webbed foot on the pedal: three toes + web
    union {
      sphere { 0, 0.026 }
      cylinder { 0, < 0.13, 0, 0.000>, 0.009 }
      cylinder { 0, < 0.11, 0,-0.050>, 0.009 }
      cylinder { 0, < 0.11, 0, 0.050>, 0.009 }
      sphere { < 0.13, 0, 0.000>, 0.012 }
      sphere { < 0.11, 0,-0.050>, 0.012 }
      sphere { < 0.11, 0, 0.050>, 0.012 }
      prism { linear_sweep linear_spline -0.004, 0.004, 5,
              <0,0>, <0.11,-0.05>, <0.12,0.0>, <0.11,0.05>, <0,0> }
      texture { LegTex }
      translate Pc + <-0.02, 0.022, 0>
    }
  }
#end

// a single covert / flight feather (pointing along +x, flat in xz)
#macro FeatherShape(Len, Wid)
  sphere { 0, 1 scale <Len/2, 0.012, Wid/2> translate <Len/2, 0, 0> }
#end

// wing held forward to the handlebar grip: shoulder -> wrist -> grip,
// with secondaries hanging below the arm
#macro WingArm(Sh, Wr, Gr)
  union {
    sphere_sweep { cubic_spline 5,
      Sh + <-0.15, 0.04, 0>, 0.07,
      Sh, 0.07,
      Wr, 0.045,
      Gr, 0.03,
      Gr + <0.1, 0, 0>, 0.03
      texture { FeatherGrey } }
    // secondaries along the arm, overlapping, getting darker toward the tip
    #local N = 9;
    #local K = 0;
    #while (K < N)
      #local Tt = K/(N-1);
      #if (Tt < 0.6)
        #local P = Sh + (Wr - Sh)*(Tt/0.6);
      #else
        #local P = Wr + (Gr - Wr)*((Tt-0.6)/0.4);
      #end
      object { FeatherShape(0.26 - 0.10*Tt, 0.085)
        rotate x*90                       // stand the feather up in the wing plane
        rotate z*(-150 + 15*Tt)           // trail backwards, a bit down
        translate P + <0, -0.01, 0>
        texture { #if (Tt > 0.8) BlackFeather #else FeatherGrey #end }
      }
      #local K = K + 1;
    #end
    // primaries wrapped around the grip like fingers
    #local K = 0;
    #while (K < 4)
      object { FeatherShape(0.11, 0.03)
        rotate x*90 rotate z*(-60 - K*20)
        translate Gr + <-0.01, 0.025, 0>
        texture { BlackFeather } }
      #local K = K + 1;
    #end
  }
#end

#declare Pelican = union {
  // tapered body: chest -> rump -> tail (scaled narrower in z)
  sphere_sweep {
    cubic_spline 7,
    BodyC + < 0.40, 0.18, 0>, 0.10,
    BodyC + < 0.22, 0.06, 0>, 0.21,
    BodyC + < 0.00, 0.00, 0>, 0.27,
    BodyC + <-0.28, 0.02, 0>, 0.24,
    BodyC + <-0.52, 0.06, 0>, 0.12,
    BodyC + <-0.70, 0.10, 0>, 0.03,
    BodyC + <-0.80, 0.12, 0>, 0.02
    scale <1, 1, 0.95>
    texture { Feather }
  }
  // fan of tail feathers
  #declare K = 0;
  #while (K < 7)
    object { FeatherShape(0.22, 0.06)
      rotate y*(180 + (K-3)*12) rotate z*-12
      translate BodyC + <-0.55, 0.08, 0>
      texture { FeatherGrey } }
    #declare K = K + 1;
  #end

  // folded wing panels on each side of the back, black primaries trailing
  #macro WingFold(Zs)
    union {
      sphere { 0, 1 scale <0.34, 0.14, 0.05> rotate z*-6 texture { FeatherGrey } }
      #local K = 0;
      #while (K < 5)
        object { FeatherShape(0.36 - K*0.03, 0.07)
          rotate y*180 rotate z*(-4 + K*3)
          translate <-0.12, 0.06 - K*0.035, Zs*0.01*K>
          texture { BlackFeather } }
        #local K = K + 1;
      #end
      translate BodyC + <-0.10, 0.06, Zs*0.235>
    }
  #end
  WingFold(-1)
  WingFold(1)

  // wings reaching forward to grip the handlebar
  WingArm(BodyC + <0.08, 0.12, -0.24>, BodyC + <0.42, 0.02, -0.26>, GripL + <-0.06, 0.03, 0>)
  WingArm(BodyC + <0.08, 0.12,  0.24>, BodyC + <0.42, 0.02,  0.26>, GripR + <-0.06, 0.03, 0>)

  // long S-curved neck
  sphere_sweep {
    cubic_spline 7,
    BodyC + <0.20, -0.05, 0>, 0.14,
    BodyC + <0.35,  0.10, 0>, 0.13,
    <0.18, 1.58, 0>, 0.085,
    <0.06, 1.74, 0>, 0.07,
    <0.08, 1.90 + Bob, 0>, 0.075,
    HeadC + <-0.02, 0.0, 0>, 0.085,
    HeadC + < 0.10, 0.05, 0>, 0.08
    texture { Feather }
  }

  // head
  sphere { 0, 1 scale <0.135, 0.11, 0.10> translate HeadC texture { Feather } }
  // pale yellow crown with a small crest
  union {
    sphere { 0, 1 scale <0.10, 0.05, 0.075> translate <-0.02, 0.075, 0> }
    sphere { 0, 1 scale <0.07, 0.025, 0.03> rotate z*25 translate <-0.10, 0.10, 0> }
    translate HeadC
    texture { pigment { color rgb <1.0, 0.90, 0.55> } finish { diffuse 0.8 } }
  }

  // eyes: pink skin ring, pale iris, dark pupil with highlight
  #macro Eye(Zs)
    union {
      sphere { 0, 1 scale <0.032, 0.026, 0.01> texture { pigment { color rgb <0.98, 0.65, 0.60> } finish { diffuse 0.8 } } }
      sphere { <0, 0, Zs*0.006>, 0.018 texture { pigment { color rgb <0.95, 0.92, 0.75> } finish { specular 0.6 } } }
      sphere { <0.004, 0.0, Zs*0.018>, 0.009 texture { pigment { color rgb 0.01 } finish { specular 1 roughness 0.001 reflection 0.1 } } }
      translate HeadC + <0.055, 0.025, Zs*0.088>
    }
  #end
  Eye(-1)
  Eye(1)

  // beak: long flat upper mandible with ridge, hooked tip, saggy pouch below
  union {
    cone { <0,0,0>, 0.058, <0.70,0,0>, 0.017 scale <1, 0.42, 1> texture { BeakTex } }
    cylinder { <0.02,0.018,0>, <0.66,0.006,0>, 0.006 texture { BeakTex } }       // culmen ridge
    sphere   { <0.71, -0.014, 0>, 0.022
      texture { pigment { color rgb <0.82, 0.25, 0.08> } finish { specular 0.5 roughness 0.01 } } }
    // lower mandible edges
    cylinder { <0.02,-0.018,-0.04>, <0.68,-0.02,-0.012>, 0.007 texture { BeakTex } }
    cylinder { <0.02,-0.018, 0.04>, <0.68,-0.02, 0.012>, 0.007 texture { BeakTex } }
    // pouch (half-ellipsoid hanging below the bill, deeper near the throat)
    intersection {
      sphere { 0, 1 scale <0.36, 0.13, 0.052> rotate z*6 translate <0.32, -0.03, 0> }
      plane  { y, -0.016 }
      texture { PouchTex }
    }
    rotate z*-14
    translate HeadC + <0.10, -0.02, 0>
  }

  // legs to the pedals
  Leg(HipL, PedalL, 0.48, 0.52)
  Leg(HipR, PedalR, 0.48, 0.52)
}

// ---------------------------------------------------------------- the rider
#declare Rider = union {
  object { Bicycle }
  object { Pelican }
}

object { Rider rotate y*20 }

// little dust puffs kicked up behind the rear wheel (suggest speed)
#declare RD = seed(5);
#declare K = 0;
#while (K < 9)
  #declare Px = -1.25 - K*0.16 - rand(RD)*0.1;
  sphere { 0, 1
    scale (0.06 + K*0.02) * <1.5, 0.8, 1.1>
    translate <Px, 0.05 + K*0.02 + rand(RD)*0.02, (rand(RD)-0.5)*0.25>
    rotate y*20
    hollow
    texture { pigment { color rgbt <0.92, 0.88, 0.80, 0.78 + K*0.02> } finish { diffuse 1.0 ambient 0.15 } }
    no_shadow
  }
  #declare K = K + 1;
#end
