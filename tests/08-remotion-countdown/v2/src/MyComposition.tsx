import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const NUMBERS = [5, 4, 3, 2, 1];
const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

// Hue per number: cool blue -> violet -> magenta -> warm red
const hueAt = (t: number) =>
  interpolate(t, [0, 1], [215, 350], {
    ...clamp,
    easing: Easing.inOut(Easing.sin),
  });

type DigitProps = {
  value: number;
  local: number; // frames since this digit's slot started (may be negative / > segment)
  segment: number;
  size: number;
  hue: number;
  isLast: boolean;
};

const Digit: React.FC<DigitProps> = ({
  value,
  local,
  segment,
  size,
  hue,
  isLast,
}) => {
  const enter = Math.round(segment * 0.4);
  const exitLen = Math.round(segment * 0.35);

  // Enter (overlaps the previous digit's exit for a real crossfade)
  const inP = interpolate(local, [0, enter], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  // Exit: starts a little before the next digit arrives
  const outP = isLast
    ? 0
    : interpolate(local, [segment - exitLen * 0.5, segment + exitLen * 0.5], [0, 1], {
        ...clamp,
        easing: Easing.in(Easing.cubic),
      });

  if (inP <= 0 || outP >= 1) return null;

  const scale = interpolate(inP, [0, 1], [0.55, 1]) * interpolate(outP, [0, 1], [1, 1.7]);
  const opacity = inP * (1 - outP);
  const blur = (1 - inP) * 18 + outP * 22;
  const y = (1 - inP) * size * 0.12;
  const rotX = (1 - inP) * 35 - outP * 20;

  // Subtle "breathing" while the digit is held
  const hold = interpolate(local, [enter, segment], [0, 1], clamp);
  const breathe = 1 + Math.sin(hold * Math.PI) * 0.025;

  return (
    <div
      style={{
        position: "absolute",
        fontSize: size,
        fontWeight: 900,
        lineHeight: 1,
        color: "white",
        fontVariantNumeric: "tabular-nums",
        letterSpacing: "-0.04em",
        opacity,
        filter: `blur(${blur.toFixed(2)}px)`,
        transform: `perspective(1200px) translateY(${y}px) rotateX(${rotX}deg) scale(${(
          scale * breathe
        ).toFixed(4)})`,
        textShadow: `0 0 ${size * 0.08}px hsla(${hue}, 95%, 65%, 0.85), 0 0 ${
          size * 0.25
        }px hsla(${hue}, 95%, 55%, 0.45), 0 ${size * 0.02}px 0 hsla(${hue}, 60%, 30%, 0.6)`,
        willChange: "transform, opacity, filter",
      }}
    >
      {value}
    </div>
  );
};

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  const segment = fps; // one second per number
  const total = segment * NUMBERS.length;
  const minSide = Math.min(width, height);
  const cx = width / 2;
  const cy = height / 2;

  const progress = interpolate(frame, [0, total], [0, 1], clamp);
  const hue = hueAt(progress);

  const index = Math.min(Math.floor(frame / segment), NUMBERS.length - 1);
  const local = frame - index * segment;

  // --- Rings -----------------------------------------------------------
  const outerR = minSide * 0.34;
  const innerR = minSide * 0.3;
  const outerC = 2 * Math.PI * outerR;
  const innerC = 2 * Math.PI * innerR;

  // Outer ring: whole countdown, drains continuously
  const outerRemaining = 1 - progress;
  // Inner ring: per second, eased so the refill at each tick is a smooth sweep
  const refill = interpolate(local, [0, segment * 0.25], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const drain = interpolate(local, [segment * 0.25, segment], [1, 0], {
    ...clamp,
    easing: Easing.inOut(Easing.quad),
  });
  const innerRemaining = frame >= total ? 0 : local < segment * 0.25 ? refill : drain;

  // Pulse on every tick
  const pulseP = interpolate(local, [0, segment * 0.6], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.quad),
  });
  const pulseR = innerR * (1 + pulseP * 0.45);
  const pulseOpacity = frame >= total ? 0 : (1 - pulseP) * 0.55;

  // Outro: flash and fade after "1"
  const outroP = interpolate(frame, [total - segment * 0.2, durationInFrames], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const flash = interpolate(frame, [total - 4, total + 2, total + 14], [0, 0.55, 0], clamp);
  const sceneOpacity = interpolate(frame, [durationInFrames - 12, durationInFrames - 1], [1, 0], clamp);
  const ringScale = 1 + outroP * 0.35;
  const ringOpacity = 1 - outroP;

  // Final "1" exits in the outro
  const lastExit = interpolate(frame, [total - 2, total + 12], [0, 1], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });

  // Tick marks around the outer ring
  const ticks = Array.from({ length: 60 }, (_, i) => i);

  // Background glow drifts slowly
  const glowX = 50 + Math.sin(frame / (fps * 2.2)) * 6;
  const glowY = 48 + Math.cos(frame / (fps * 2.7)) * 5;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at ${glowX}% ${glowY}%, hsl(${hue}, 65%, 24%) 0%, hsl(${hue}, 70%, 11%) 45%, hsl(${hue + 20}, 60%, 4%) 100%)`,
        fontFamily:
          "'Inter', 'Helvetica Neue', 'Liberation Sans', Helvetica, Arial, sans-serif",
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
        opacity: sceneOpacity,
      }}
    >
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        style={{ position: "absolute", inset: 0 }}
      >
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={minSide * 0.008} result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor={`hsl(${hue - 25}, 95%, 70%)`} />
            <stop offset="100%" stopColor={`hsl(${hue + 25}, 95%, 62%)`} />
          </linearGradient>
        </defs>

        <g
          opacity={ringOpacity}
          transform={`translate(${cx} ${cy}) scale(${ringScale}) translate(${-cx} ${-cy})`}
        >
          {/* Tick marks */}
          {ticks.map((i) => {
            const a = (i / ticks.length) * Math.PI * 2 - Math.PI / 2;
            const major = i % 12 === 0;
            const r1 = outerR + minSide * 0.025;
            const r2 = r1 + (major ? minSide * 0.028 : minSide * 0.012);
            const lit = i / ticks.length < outerRemaining;
            return (
              <line
                key={i}
                x1={cx + Math.cos(a) * r1}
                y1={cy + Math.sin(a) * r1}
                x2={cx + Math.cos(a) * r2}
                y2={cy + Math.sin(a) * r2}
                stroke={lit ? `hsla(${hue}, 90%, 75%, ${major ? 0.9 : 0.5})` : "rgba(255,255,255,0.08)"}
                strokeWidth={major ? 4 : 2}
                strokeLinecap="round"
              />
            );
          })}

          {/* Outer ring (whole countdown) */}
          <circle cx={cx} cy={cy} r={outerR} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth={4} />
          <circle
            cx={cx}
            cy={cy}
            r={outerR}
            fill="none"
            stroke={`hsla(${hue}, 90%, 75%, 0.75)`}
            strokeWidth={4}
            strokeLinecap="round"
            strokeDasharray={outerC}
            strokeDashoffset={outerC * (1 - outerRemaining)}
            transform={`rotate(-90 ${cx} ${cy})`}
          />

          {/* Inner ring (per second) */}
          <circle cx={cx} cy={cy} r={innerR} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={14} />
          <circle
            cx={cx}
            cy={cy}
            r={innerR}
            fill="none"
            stroke="url(#ringGrad)"
            strokeWidth={14}
            strokeLinecap="round"
            strokeDasharray={innerC}
            strokeDashoffset={innerC * (1 - innerRemaining)}
            transform={`rotate(-90 ${cx} ${cy})`}
            filter="url(#glow)"
          />

          {/* Tick pulse */}
          <circle
            cx={cx}
            cy={cy}
            r={pulseR}
            fill="none"
            stroke={`hsl(${hue}, 95%, 72%)`}
            strokeWidth={6 * (1 - pulseP) + 1}
            opacity={pulseOpacity}
          />
        </g>
      </svg>

      {/* Digits: previous and current rendered together for a real crossfade */}
      {NUMBERS.map((n, i) => {
        const l = frame - i * segment;
        if (l < -2 || l > segment * 1.5) return null;
        const isLast = i === NUMBERS.length - 1;
        return (
          <div
            key={n}
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              opacity: isLast ? 1 - lastExit : 1,
              transform: isLast ? `scale(${1 + lastExit * 0.8})` : undefined,
              filter: isLast && lastExit > 0 ? `blur(${lastExit * 20}px)` : undefined,
            }}
          >
            <Digit
              value={n}
              local={l}
              segment={segment}
              size={innerR * 1.25}
              hue={hueAt(i / NUMBERS.length + 0.1)}
              isLast={isLast}
            />
          </div>
        );
      })}

      {/* Flash on zero */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle, hsla(${hue}, 100%, 85%, 1) 0%, hsla(${hue}, 100%, 60%, 0) 60%)`,
          opacity: flash,
          mixBlendMode: "screen",
        }}
      />

      {/* Vignette */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Film grain: breaks up gradient banding in the h264 encode */}
      <svg
        width={width}
        height={height}
        style={{ position: "absolute", inset: 0, opacity: 0.07, mixBlendMode: "overlay" }}
      >
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 8} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
