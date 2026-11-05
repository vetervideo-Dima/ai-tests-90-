import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from 'remotion';

// Quarterly sales data (in $K)
const DATA = [
  {label: 'Q1', value: 420},
  {label: 'Q2', value: 580},
  {label: 'Q3', value: 910},
  {label: 'Q4', value: 760},
];

const MAX_VALUE = 1000;
const COLORS = ['#4F8CFF', '#7B61FF', '#FF5FA2', '#2DD4BF'];

// Chart layout (in px, for a 1920x1080 canvas)
const CHART = {
  left: 260,
  right: 1700,
  top: 220,
  bottom: 880,
};
const CHART_W = CHART.right - CHART.left;
const CHART_H = CHART.bottom - CHART.top;

const BAR_W = 200;
const SLOT_W = CHART_W / DATA.length;

const formatMoney = (n: number) =>
  `$${Math.round(n).toLocaleString('en-US')}K`;

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const bestIndex = DATA.reduce(
    (best, d, i) => (d.value > DATA[best].value ? i : best),
    0
  );

  // ---- Title ----
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const titleY = interpolate(frame, [0, 20], [-30, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // ---- Axis draw-in ----
  const yAxisProgress = interpolate(frame, [10, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  const xAxisProgress = interpolate(frame, [25, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });

  // Gridlines & tick labels
  const ticks = [0, 250, 500, 750, 1000];

  // ---- Bars ----
  const barsStart = 50;
  const stagger = 12;

  // ---- Glow on best quarter (after all bars landed) ----
  const glowStart = barsStart + stagger * DATA.length + 40;
  const glowIn = interpolate(frame, [glowStart, glowStart + 25], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const pulse = 0.75 + 0.25 * Math.sin((frame - glowStart) / 8);
  const glowStrength = glowIn * pulse;

  // ---- Outro fade ----
  const outro = interpolate(
    frame,
    [durationInFrames - 15, durationInFrames],
    [1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  return (
    <AbsoluteFill
      style={{
        background:
          'radial-gradient(ellipse at 50% 30%, #1b1f3b 0%, #0b0d1a 70%)',
        fontFamily:
          'Inter, "Helvetica Neue", Helvetica, Arial, sans-serif',
        color: 'white',
        opacity: outro,
      }}
    >
      {/* Title */}
      <div
        style={{
          position: 'absolute',
          top: 70,
          width: '100%',
          textAlign: 'center',
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
        }}
      >
        <div style={{fontSize: 64, fontWeight: 800, letterSpacing: -1}}>
          Quarterly Sales 2024
        </div>
        <div style={{fontSize: 28, opacity: 0.6, marginTop: 8}}>
          Revenue in thousands of USD
        </div>
      </div>

      <svg
        width={1920}
        height={1080}
        style={{position: 'absolute', top: 0, left: 0}}
      >
        <defs>
          {DATA.map((d, i) => (
            <linearGradient
              key={d.label}
              id={`grad-${i}`}
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >
              <stop offset="0%" stopColor={COLORS[i]} stopOpacity={1} />
              <stop offset="100%" stopColor={COLORS[i]} stopOpacity={0.55} />
            </linearGradient>
          ))}
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="18" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Gridlines + Y tick labels */}
        {ticks.map((t, i) => {
          const y = CHART.bottom - (t / MAX_VALUE) * CHART_H;
          const tickOpacity = interpolate(
            frame,
            [20 + i * 4, 35 + i * 4],
            [0, 1],
            {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
          );
          const lineLen = CHART_W * xAxisProgress;
          return (
            <g key={t} opacity={tickOpacity}>
              {t !== 0 && (
                <line
                  x1={CHART.left}
                  x2={CHART.left + lineLen}
                  y1={y}
                  y2={y}
                  stroke="white"
                  strokeOpacity={0.08}
                  strokeWidth={2}
                  strokeDasharray="8 10"
                />
              )}
              <text
                x={CHART.left - 24}
                y={y + 9}
                fill="white"
                fillOpacity={0.55}
                fontSize={26}
                textAnchor="end"
              >
                {`$${t}K`}
              </text>
            </g>
          );
        })}

        {/* Y axis */}
        <line
          x1={CHART.left}
          x2={CHART.left}
          y1={CHART.bottom}
          y2={CHART.bottom - CHART_H * yAxisProgress}
          stroke="white"
          strokeOpacity={0.7}
          strokeWidth={4}
          strokeLinecap="round"
        />
        {/* X axis */}
        <line
          x1={CHART.left}
          x2={CHART.left + CHART_W * xAxisProgress}
          y1={CHART.bottom}
          y2={CHART.bottom}
          stroke="white"
          strokeOpacity={0.7}
          strokeWidth={4}
          strokeLinecap="round"
        />

        {/* Bars */}
        {DATA.map((d, i) => {
          const delay = barsStart + i * stagger;
          const s = spring({
            frame: frame - delay,
            fps,
            config: {damping: 9, stiffness: 110, mass: 0.9},
          });
          // Bouncy height (spring may overshoot > 1)
          const h = (d.value / MAX_VALUE) * CHART_H * s;
          const x = CHART.left + SLOT_W * i + (SLOT_W - BAR_W) / 2;
          const y = CHART.bottom - Math.max(0, h);

          // Counting number uses a smoother, non-overshooting progress
          const countProgress = interpolate(
            frame,
            [delay, delay + 35],
            [0, 1],
            {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
              easing: Easing.out(Easing.cubic),
            }
          );
          const shown = d.value * countProgress;

          const labelOpacity = interpolate(
            frame,
            [delay, delay + 10],
            [0, 1],
            {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
          );

          const isBest = i === bestIndex;
          const glow = isBest ? glowStrength : 0;

          return (
            <g key={d.label}>
              {/* Glow halo for best quarter */}
              {isBest && glow > 0 && (
                <rect
                  x={x - 10}
                  y={y - 10}
                  width={BAR_W + 20}
                  height={Math.max(0, h) + 10}
                  rx={22}
                  fill={COLORS[i]}
                  opacity={0.55 * glow}
                  filter="url(#glow)"
                />
              )}
              <rect
                x={x}
                y={y}
                width={BAR_W}
                height={Math.max(0, h)}
                rx={14}
                fill={`url(#grad-${i})`}
                stroke={isBest ? 'white' : 'none'}
                strokeOpacity={isBest ? 0.8 * glow : 0}
                strokeWidth={3}
              />
              {/* Value label */}
              <text
                x={x + BAR_W / 2}
                y={y - 24}
                fill="white"
                fontSize={isBest ? 44 + 6 * glow : 40}
                fontWeight={800}
                textAnchor="middle"
                opacity={labelOpacity}
                style={{
                  fontVariantNumeric: 'tabular-nums',
                  filter: isBest && glow > 0
                    ? `drop-shadow(0 0 ${12 * glow}px ${COLORS[i]})`
                    : undefined,
                }}
              >
                {formatMoney(shown)}
              </text>
              {/* Quarter label */}
              <text
                x={x + BAR_W / 2}
                y={CHART.bottom + 56}
                fill="white"
                fillOpacity={0.8 * xAxisProgress}
                fontSize={34}
                fontWeight={600}
                textAnchor="middle"
              >
                {d.label}
              </text>
              {/* Best badge */}
              {isBest && glow > 0 && (
                <text
                  x={x + BAR_W / 2}
                  y={y - 90}
                  fill={COLORS[i]}
                  fontSize={26}
                  fontWeight={700}
                  textAnchor="middle"
                  opacity={glowIn}
                  letterSpacing={3}
                >
                  ★ BEST QUARTER
                </text>
              )}
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
