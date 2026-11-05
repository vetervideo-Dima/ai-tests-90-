// src/GrooveBasement.tsx
// "Groove Basement" — 15s vertical promo (1080x1920 @ 30fps).
// Fully deterministic: no external assets, no Math.random(), every value derived from the frame.
import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  random,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {CameraMotionBlur} from '@remotion/motion-blur';

const CLAMP = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const C = {
  ink: '#120b08',
  brown: '#2a1a12',
  cream: '#f6e8cc',
  orange: '#ff6a2b',
  mustard: '#f5b83d',
  teal: '#2a9d8f',
  plum: '#6d2e5a',
  red: '#d62839',
  blue: '#2b59c3',
};

const DISPLAY = '"Arial Black", "Archivo Black", "Helvetica Neue", Impact, sans-serif';
const BODY = '"Helvetica Neue", Helvetica, Arial, sans-serif';
const SERIF = 'Georgia, "Times New Roman", serif';

// ---------------------------------------------------------------------------
// Timeline (frames @ 30fps, total 450)
// ---------------------------------------------------------------------------
const T = {
  intro: {from: 0, dur: 240},
  tag: {from: 95, dur: 141}, // 3 taglines x 47 frames
  grid: {from: 228, dur: 140},
  stamp: {from: 292, dur: 76},
  outro: {from: 362, dur: 88},
};
const TAG_LEN = 47;
const STAMP_IMPACT = T.stamp.from + 7;

// ---------------------------------------------------------------------------
// Vinyl record (pure SVG)
// ---------------------------------------------------------------------------
const Vinyl: React.FC<{
  size: number;
  rotation: number;
  uid: string;
  label?: string;
}> = ({size, rotation, uid, label = C.orange}) => {
  const grooves = Array.from({length: 26}, (_, i) => 38 + i * 2.3);
  return (
    <svg width={size} height={size} viewBox="-100 -100 200 200" style={{overflow: 'visible'}}>
      <defs>
        <radialGradient id={`${uid}-body`} cx="0" cy="0" r="100" gradientUnits="userSpaceOnUse">
          <stop offset="0.3" stopColor="#1d1d1f" />
          <stop offset="0.96" stopColor="#0b0b0c" />
          <stop offset="1" stopColor="#2c2c2e" />
        </radialGradient>
        <clipPath id={`${uid}-clip`}>
          <circle r="99" />
        </clipPath>
      </defs>
      <circle r="99" fill={`url(#${uid}-body)`} />
      {/* grooves rotate with the record */}
      <g transform={`rotate(${rotation})`}>
        {grooves.map((r, i) => (
          <circle
            key={i}
            r={r}
            fill="none"
            stroke={i % 4 === 0 ? '#36363a' : '#1f1f22'}
            strokeWidth={i % 4 === 0 ? 0.7 : 0.45}
          />
        ))}
      </g>
      {/* light sheen stays fixed (light source does not spin) */}
      <g clipPath={`url(#${uid}-clip)`}>
        <path d="M0 0 L -40 -110 L 40 -110 Z" fill="rgba(255,255,255,0.10)" />
        <path d="M0 0 L 40 110 L -40 110 Z" fill="rgba(255,255,255,0.06)" />
      </g>
      {/* label rotates */}
      <g transform={`rotate(${rotation})`}>
        <circle r="34" fill={label} />
        <circle r="33" fill="none" stroke="rgba(0,0,0,0.25)" strokeWidth="1.5" />
        <path id={`${uid}-arc`} d="M -24 0 A 24 24 0 0 1 24 0" fill="none" />
        <text fontFamily={BODY} fontWeight={800} fontSize="7" fill={C.ink} letterSpacing="0.8">
          <textPath href={`#${uid}-arc`} startOffset="50%" textAnchor="middle">
            GROOVE BASEMENT
          </textPath>
        </text>
        <text y="17" textAnchor="middle" fontFamily={BODY} fontSize="4.6" fill={C.ink} letterSpacing="0.6">
          33⅓ RPM · SIDE A
        </text>
        <rect x="-0.8" y="-31" width="1.6" height="6" fill={C.ink} opacity={0.6} />
      </g>
      <circle r="3.2" fill={C.ink} />
    </svg>
  );
};

// ---------------------------------------------------------------------------
// Scene 1 — vinyl spins in (with real multi-sample motion blur)
// ---------------------------------------------------------------------------
const VinylIntro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const enter = spring({frame, fps, config: {damping: 14, stiffness: 70, mass: 1.1}});
  const x = interpolate(enter, [0, 1], [-1500, 0]);
  const yIn = interpolate(enter, [0, 1], [-500, 0]);

  // pan the record up out of the way of the typography
  const pan = interpolate(frame, [72, 108], [0, 1], {...CLAMP, easing: Easing.inOut(Easing.cubic)});
  const exit = interpolate(frame, [212, 238], [0, 1], {...CLAMP, easing: Easing.in(Easing.cubic)});

  const y = yIn - pan * 520;
  const scale = 1 - pan * 0.38;
  const rotation = frame * 9 - (1 - enter) * 600;

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          transform: `translate(${x + exit * 1500}px, ${y}px) scale(${scale})`,
          filter: 'drop-shadow(0 40px 60px rgba(0,0,0,0.6))',
        }}
      >
        <Vinyl size={860} rotation={rotation} uid="intro" />
      </div>
    </AbsoluteFill>
  );
};

const IntroAccents: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const ring = interpolate(frame, [20, 50], [0, 1], CLAMP);
  const textIn = spring({frame: frame - 26, fps, config: {damping: 12, stiffness: 140}});
  const textOut = interpolate(frame, [66, 80], [0, 1], {...CLAMP, easing: Easing.in(Easing.quad)});

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      {ring > 0 && ring < 1 ? (
        <div
          style={{
            position: 'absolute',
            width: 860,
            height: 860,
            borderRadius: '50%',
            border: `${interpolate(ring, [0, 1], [18, 1])}px solid ${C.orange}`,
            transform: `scale(${interpolate(ring, [0, 1], [1, 1.6])})`,
            opacity: 1 - ring,
          }}
        />
      ) : null}
      <div
        style={{
          position: 'absolute',
          top: 1450,
          width: '100%',
          textAlign: 'center',
          color: C.cream,
          opacity: interpolate(textIn, [0, 1], [0, 1], CLAMP) * (1 - textOut),
          transform: `translateY(${(1 - textIn) * 80 + textOut * -60}px)`,
        }}
      >
        <div style={{fontFamily: BODY, fontSize: 36, letterSpacing: 14, opacity: 0.75}}>NOW SPINNING AT</div>
        <div style={{fontFamily: DISPLAY, fontSize: 96, letterSpacing: 2, color: C.mustard, marginTop: 10}}>
          GROOVE BASEMENT
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Scene 2 — kinetic typography, three taglines
// ---------------------------------------------------------------------------
const TAGLINES = [
  {words: ['DIG', 'DEEPER.'], color: C.mustard, kicker: 'crates on crates'},
  {words: ['DROP', 'THE', 'NEEDLE.'], color: C.orange, kicker: 'listening booths open'},
  {words: ['FEEL', 'THE', 'WAX.'], color: C.teal, kicker: 'new · used · rare'},
];

const Tagline: React.FC<{words: string[]; color: string; kicker: string; index: number}> = ({
  words,
  color,
  kicker,
  index,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const pan = interpolate(frame, [0, TAG_LEN], [60, -60]);
  const exit = interpolate(frame, [38, TAG_LEN], [0, 1], {...CLAMP, easing: Easing.in(Easing.quad)});
  const bar = spring({frame: frame - 10, fps, config: {damping: 200}});

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingTop: 620}}>
      <div
        style={{
          transform: `translateX(${pan - exit * 1300}px) skewX(${-exit * 18}deg)`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            fontFamily: BODY,
            fontSize: 32,
            letterSpacing: 8,
            color: C.cream,
            opacity: 0.7 * interpolate(frame, [0, 6], [0, 1], CLAMP),
            marginBottom: 18,
          }}
        >
          {`0${index + 1} / 03 — ${kicker.toUpperCase()}`}
        </div>
        {words.map((w, i) => {
          const s = spring({frame: frame - i * 5, fps, config: {damping: 10, stiffness: 170, mass: 0.7}});
          const size = w.length <= 4 ? 200 : 150;
          return (
            <div
              key={w + i}
              style={{
                fontFamily: DISPLAY,
                fontWeight: 900,
                fontSize: size,
                lineHeight: 0.95,
                color: i === words.length - 1 ? color : C.cream,
                transform: `translateY(${(1 - s) * 140}px) scale(${interpolate(s, [0, 1], [2.2, 1])}) rotate(${
                  (1 - s) * (i % 2 ? 8 : -8)
                }deg)`,
                opacity: interpolate(frame - i * 5, [0, 3], [0, 1], CLAMP),
                textShadow: '0 12px 0 rgba(0,0,0,0.35)',
              }}
            >
              {w}
            </div>
          );
        })}
        <div style={{height: 14, width: 600 * bar, background: color, marginTop: 24, borderRadius: 7}} />
      </div>
    </AbsoluteFill>
  );
};

const Taglines: React.FC = () => (
  <AbsoluteFill>
    {TAGLINES.map((t, i) => (
      <Sequence key={i} from={i * TAG_LEN} durationInFrames={TAG_LEN} layout="none">
        <Tagline {...t} index={i} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

// ---------------------------------------------------------------------------
// Scene 3 — grid of 9 CSS/SVG album covers
// ---------------------------------------------------------------------------
const COVERS = [
  {title: 'Sunburst Sessions', artist: 'The Velvet Ohms'},
  {title: 'Midnight Static', artist: 'Lo Fidelity'},
  {title: 'Basement Hymns', artist: 'Cellar Door Choir'},
  {title: 'Checker Club', artist: 'DJ Parquet'},
  {title: 'Bass Cathedral', artist: 'Subwoofer Saints'},
  {title: 'Neon Tide', artist: 'Mara Lux'},
  {title: 'Polka Dot Panic', artist: 'The Halftones'},
  {title: 'Polar Funk', artist: 'Ice Cold Brass'},
  {title: 'Side B Forever', artist: 'Needle & Thread'},
];

const fill: React.CSSProperties = {position: 'absolute', inset: 0};

const CoverArt: React.FC<{i: number; t: number}> = ({i, t}) => {
  switch (i) {
    case 0:
      return (
        <div
          style={{
            ...fill,
            background: `repeating-conic-gradient(from ${t * 0.6}deg at 50% 72%, ${C.mustard} 0deg 10deg, ${C.orange} 10deg 20deg)`,
          }}
        >
          <div
            style={{
              position: 'absolute',
              left: 95,
              top: 156,
              width: 110,
              height: 110,
              borderRadius: '50%',
              background: C.red,
              boxShadow: '0 0 0 10px rgba(255,255,255,0.25)',
            }}
          />
        </div>
      );
    case 1:
      return (
        <svg style={fill} viewBox="0 0 100 100">
          <rect width="100" height="100" fill={C.ink} />
          {Array.from({length: 9}, (_, k) => (
            <circle
              key={k}
              cx={50 + Math.sin(t / 20 + k) * 3}
              cy={46}
              r={6 + k * 5}
              fill="none"
              stroke={k % 2 ? C.cream : C.teal}
              strokeWidth={1.2}
              opacity={1 - k * 0.08}
            />
          ))}
        </svg>
      );
    case 2:
      return (
        <div style={{...fill, background: `linear-gradient(160deg, ${C.plum} 0%, ${C.orange} 100%)`}}>
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: 18,
              textAlign: 'center',
              fontFamily: SERIF,
              fontStyle: 'italic',
              fontSize: 200,
              color: 'rgba(246,232,204,0.9)',
              lineHeight: 1,
            }}
          >
            ♪
          </div>
        </div>
      );
    case 3:
      return (
        <div
          style={{
            ...fill,
            background: `repeating-conic-gradient(${C.cream} 0 25%, ${C.ink} 0 50%) ${t * 0.8}px 0 / 60px 60px`,
          }}
        >
          <div
            style={{
              position: 'absolute',
              left: 60,
              top: 60,
              width: 180,
              height: 180,
              borderRadius: '50%',
              background: C.red,
              border: `8px solid ${C.cream}`,
            }}
          />
        </div>
      );
    case 4:
      return (
        <svg style={fill} viewBox="0 0 100 100">
          <rect width="100" height="100" fill={C.teal} />
          {Array.from({length: 5}, (_, k) => (
            <polygon
              key={k}
              points={`50,${8 + k * 10} ${90 - k * 4},${88} ${10 + k * 4},${88}`}
              fill={k % 2 ? C.ink : C.mustard}
            />
          ))}
        </svg>
      );
    case 5:
      return (
        <svg style={fill} viewBox="0 0 100 100">
          <rect width="100" height="100" fill="#0e1b3d" />
          {Array.from({length: 7}, (_, k) => {
            const y0 = 22 + k * 10;
            let d = `M 0 ${y0}`;
            for (let x = 0; x <= 100; x += 5) {
              d += ` L ${x} ${y0 + Math.sin(x / 9 + k * 0.8 + t / 8) * 4}`;
            }
            return <path key={k} d={d} fill="none" stroke={k % 2 ? '#ff4fd8' : '#4ff0ff'} strokeWidth={1.6} />;
          })}
        </svg>
      );
    case 6:
      return (
        <div
          style={{
            ...fill,
            background: `radial-gradient(circle, ${C.red} 30%, transparent 32%) 0 0 / 36px 36px, ${C.cream}`,
          }}
        />
      );
    case 7:
      return (
        <div
          style={{
            ...fill,
            background: `repeating-linear-gradient(45deg, ${C.blue} 0 22px, ${C.cream} 22px 44px)`,
          }}
        >
          <div
            style={{
              position: 'absolute',
              left: 70,
              top: 50,
              width: 160,
              height: 160,
              borderRadius: '50%',
              background: C.cream,
              border: `10px solid ${C.ink}`,
            }}
          />
        </div>
      );
    default:
      return (
        <div style={{...fill, background: C.mustard}}>
          <div
            style={{
              ...fill,
              background: `radial-gradient(circle, rgba(18,11,8,0.5) 22%, transparent 24%) 0 0 / 14px 14px`,
              maskImage: 'linear-gradient(135deg, transparent 20%, black 90%)',
              WebkitMaskImage: 'linear-gradient(135deg, transparent 20%, black 90%)',
            }}
          />
          <div
            style={{
              position: 'absolute',
              left: 24,
              top: -6,
              fontFamily: DISPLAY,
              fontSize: 240,
              color: C.ink,
              lineHeight: 1,
            }}
          >
            B
          </div>
        </div>
      );
  }
};

const AlbumGrid: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // camera pan across the crate
  const camScale = interpolate(frame, [0, T.grid.dur], [1.18, 0.98], {...CLAMP, easing: Easing.out(Easing.quad)});
  const camY = interpolate(frame, [0, T.grid.dur], [160, -30], CLAMP);
  const camX = interpolate(frame, [0, T.grid.dur], [-40, 40], CLAMP);
  const exit = interpolate(frame, [T.grid.dur - 16, T.grid.dur], [0, 1], CLAMP);
  const heading = spring({frame: frame - 4, fps, config: {damping: 14}});

  const SIZE = 300;
  const GAP = 30;

  return (
    <AbsoluteFill style={{opacity: 1 - exit}}>
      <div
        style={{
          position: 'absolute',
          top: 170,
          width: '100%',
          textAlign: 'center',
          transform: `translateY(${(1 - heading) * -200}px)`,
        }}
      >
        <div style={{fontFamily: BODY, fontSize: 34, letterSpacing: 12, color: C.cream, opacity: 0.7}}>
          FRESH PRESSINGS
        </div>
        <div style={{fontFamily: DISPLAY, fontSize: 104, color: C.mustard, lineHeight: 1.05}}>THIS WEEK'S CRATE</div>
      </div>
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          transform: `translate(${camX}px, ${camY}px) scale(${camScale * (1 - exit * 0.3)})`,
        }}
      >
        <div style={{display: 'grid', gridTemplateColumns: `repeat(3, ${SIZE}px)`, gap: GAP}}>
          {COVERS.map((c, i) => {
            const r = Math.floor(i / 3);
            const col = i % 3;
            const delay = (Math.abs(r - 1) + Math.abs(col - 1)) * 5 + random(`delay-${i}`) * 3;
            const s = spring({frame: frame - delay, fps, config: {damping: 12, stiffness: 120, mass: 0.9}});
            const tilt = (random(`tilt-${i}`) - 0.5) * 6;
            return (
              <div
                key={c.title}
                style={{
                  width: SIZE,
                  height: SIZE,
                  position: 'relative',
                  overflow: 'hidden',
                  borderRadius: 6,
                  boxShadow: '0 24px 40px rgba(0,0,0,0.55)',
                  transform: `translateY(${(1 - s) * 600}px) rotate(${tilt + (1 - s) * 25}deg) scale(${interpolate(
                    s,
                    [0, 1],
                    [0.4, 1]
                  )})`,
                  opacity: interpolate(frame - delay, [0, 4], [0, 1], CLAMP),
                }}
              >
                <CoverArt i={i} t={frame} />
                <div
                  style={{
                    position: 'absolute',
                    left: 0,
                    right: 0,
                    bottom: 0,
                    padding: '10px 14px',
                    background: 'linear-gradient(transparent, rgba(0,0,0,0.65))',
                    color: '#fff',
                    fontFamily: BODY,
                  }}
                >
                  <div style={{fontSize: 22, fontWeight: 800}}>{c.title}</div>
                  <div style={{fontSize: 17, opacity: 0.8}}>{c.artist}</div>
                </div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Scene 4 — price-tag stamp (spring impact + camera shake)
// ---------------------------------------------------------------------------
const PriceStamp: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const s = spring({frame, fps, config: {damping: 8, stiffness: 260, mass: 0.7}});
  const scale = interpolate(s, [0, 1], [3.4, 1]);
  const appear = interpolate(frame, [0, 3], [0, 1], CLAMP);
  const exit = interpolate(frame, [T.stamp.dur - 16, T.stamp.dur], [0, 1], CLAMP);
  const splat = interpolate(frame, [6, 12], [0, 1], {...CLAMP, easing: Easing.out(Easing.cubic)});

  const splats = Array.from({length: 14}, (_, i) => {
    const a = random(`splat-a-${i}`) * Math.PI * 2;
    const d = 250 + random(`splat-d-${i}`) * 110;
    return {
      x: Math.cos(a) * d,
      y: Math.sin(a) * d * 0.55,
      r: 5 + random(`splat-r-${i}`) * 14,
    };
  });

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          position: 'relative',
          transform: `translateY(250px) rotate(-12deg) scale(${scale * (1 - exit * 0.2)})`,
          opacity: appear * (1 - exit),
        }}
      >
        {splats.map((p, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 310 + p.x * splat - p.r,
              top: 170 + p.y * splat - p.r,
              width: p.r * 2,
              height: p.r * 2,
              borderRadius: '50%',
              background: C.red,
              opacity: splat,
            }}
          />
        ))}
        <svg width={620} height={340} viewBox="0 0 620 340" style={{overflow: 'visible'}}>
          <defs>
            <filter id="rough" x="-10%" y="-10%" width="120%" height="120%">
              <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" seed="7" />
              <feDisplacementMap in="SourceGraphic" scale="6" />
            </filter>
            <filter id="ink">
              <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="3" result="n" />
              <feColorMatrix
                in="n"
                type="matrix"
                values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.25"
                result="mask"
              />
              <feComposite in="SourceGraphic" in2="mask" operator="in" />
            </filter>
          </defs>
          {/* string */}
          <path d="M 95 170 C 40 120, 10 60, -40 20" stroke={C.cream} strokeWidth="4" fill="none" />
          {/* tag body */}
          <path
            d="M 130 20 H 585 Q 600 20 600 35 V 305 Q 600 320 585 320 H 130 L 20 170 Z"
            fill={C.cream}
            filter="url(#rough)"
            style={{filter: 'drop-shadow(0 20px 30px rgba(0,0,0,0.5))'}}
          />
          <circle cx="95" cy="170" r="18" fill={C.ink} />
          <g filter="url(#ink)">
            <path
              d="M 142 40 H 578 V 300 H 142 L 50 170 Z"
              fill="none"
              stroke={C.red}
              strokeWidth="6"
              strokeDasharray="18 10"
            />
            <text x="370" y="98" textAnchor="middle" fontFamily={DISPLAY} fontSize="54" fill={C.red} letterSpacing="4">
              ALL LPs
            </text>
            <text x="370" y="232" textAnchor="middle" fontFamily={DISPLAY} fontSize="150" fill={C.red}>
              $9.99
            </text>
            <text x="370" y="284" textAnchor="middle" fontFamily={BODY} fontWeight={800} fontSize="30" fill={C.red} letterSpacing="6">
              THIS WEEKEND ONLY
            </text>
          </g>
        </svg>
      </div>
    </AbsoluteFill>
  );
};

const ImpactShake: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const t = frame - STAMP_IMPACT;
  const amp = t < 0 ? 0 : interpolate(t, [0, 16], [26, 0], CLAMP);
  const dx = Math.sin(t * 2.7) * amp;
  const dy = Math.cos(t * 3.3) * amp * 0.7;
  const flash = t < 0 ? 0 : interpolate(t, [0, 1, 7], [0, 0.35, 0], CLAMP);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${dx}px, ${dy}px)`}}>{children}</AbsoluteFill>
      <AbsoluteFill style={{background: '#fff', opacity: flash}} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Scene 5 — logo outro
// ---------------------------------------------------------------------------
const LogoOutro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const wipe = interpolate(frame, [0, 18], [0, 1], {...CLAMP, easing: Easing.out(Easing.cubic)});
  const logo = spring({frame: frame - 8, fps, config: {damping: 11, stiffness: 120}});
  const sub = spring({frame: frame - 34, fps, config: {damping: 200}});
  const pulse = 1 + Math.sin(frame / 6) * 0.01;

  const letters = (word: string, start: number, size: number, color: string) => (
    <div style={{display: 'flex', justifyContent: 'center'}}>
      {word.split('').map((ch, i) => {
        const s = spring({frame: frame - start - i * 2, fps, config: {damping: 10, stiffness: 200, mass: 0.6}});
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              fontFamily: DISPLAY,
              fontSize: size,
              lineHeight: 1,
              color,
              transform: `translateY(${(1 - s) * 220}px) rotate(${(1 - s) * (i % 2 ? 20 : -20)}deg)`,
              opacity: interpolate(frame - start - i * 2, [0, 3], [0, 1], CLAMP),
            }}
          >
            {ch}
          </span>
        );
      })}
    </div>
  );

  return (
    <AbsoluteFill style={{clipPath: `circle(${wipe * 130}% at 50% 50%)`}}>
      <AbsoluteFill style={{background: `radial-gradient(90% 60% at 50% 40%, ${C.orange} 0%, #c8431a 100%)`}} />
      <AbsoluteFill
        style={{
          background: `repeating-conic-gradient(from ${frame * 0.4}deg at 50% 38%, rgba(255,255,255,0.07) 0deg 8deg, transparent 8deg 16deg)`,
        }}
      />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: `scale(${pulse})`}}>
        <div style={{transform: `scale(${logo}) rotate(${(1 - logo) * -180}deg)`, marginBottom: 40}}>
          <Vinyl size={420} rotation={frame * 6} uid="outro" label={C.mustard} />
        </div>
        {letters('GROOVE', 16, 170, C.ink)}
        {letters('BASEMENT', 24, 128, C.cream)}
        <div
          style={{
            marginTop: 36,
            textAlign: 'center',
            opacity: sub,
            transform: `translateY(${(1 - sub) * 40}px)`,
            color: C.ink,
            fontFamily: BODY,
          }}
        >
          <div style={{width: 520 * sub, height: 6, background: C.ink, margin: '0 auto 26px', borderRadius: 3}} />
          <div style={{fontSize: 40, fontWeight: 800, letterSpacing: 12}}>RECORDS · EST. 1979</div>
          <div style={{fontSize: 30, marginTop: 16, letterSpacing: 4}}>NEW · USED · RARE — OPEN TILL MIDNIGHT</div>
          <div style={{fontSize: 28, marginTop: 10, opacity: 0.75}}>B1, 42 Spindle Street · Downstairs, always</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Global backdrop & film grain
// ---------------------------------------------------------------------------
const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 80% at 50% 35%, #3a2216 0%, ${C.ink} 70%)`}}>
      <AbsoluteFill
        style={{
          background: `repeating-conic-gradient(from ${frame * 0.25}deg at 50% 40%, rgba(255,150,80,0.05) 0deg 6deg, transparent 6deg 12deg)`,
        }}
      />
    </AbsoluteFill>
  );
};

const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width="100%" height="100%" style={{mixBlendMode: 'overlay', opacity: 0.16}}>
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={frame % 12} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Main composition
// ---------------------------------------------------------------------------
export const GrooveBasement: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: C.ink, overflow: 'hidden'}}>
      <Backdrop />

      <Sequence from={T.intro.from} durationInFrames={T.intro.dur}>
        <CameraMotionBlur shutterAngle={200} samples={10}>
          <VinylIntro />
        </CameraMotionBlur>
      </Sequence>
      <Sequence from={T.intro.from} durationInFrames={90}>
        <IntroAccents />
      </Sequence>

      <Sequence from={T.tag.from} durationInFrames={T.tag.dur}>
        <Taglines />
      </Sequence>

      <ImpactShake>
        <Sequence from={T.grid.from} durationInFrames={T.grid.dur}>
          <AlbumGrid />
        </Sequence>
        <Sequence from={T.stamp.from} durationInFrames={T.stamp.dur}>
          <PriceStamp />
        </Sequence>
      </ImpactShake>

      <Sequence from={T.outro.from} durationInFrames={T.outro.dur}>
        <LogoOutro />
      </Sequence>

      <Grain />
    </AbsoluteFill>
  );
};
