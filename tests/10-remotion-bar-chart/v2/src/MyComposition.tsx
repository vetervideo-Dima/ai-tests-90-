import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
  random,
  staticFile,
  delayRender,
  continueRender,
} from 'remotion';

// Inter (Google Fonts, variable 500–800, latin subset) bundled in public/ so the
// render works offline. Rendering waits for the font via delayRender.
const fontFamily = 'InterLocal';
if (typeof window !== 'undefined' && typeof FontFace !== 'undefined') {
  const handle = delayRender('Loading Inter');
  const face = new FontFace(fontFamily, `url(${staticFile('Inter-latin.woff2')}) format('woff2')`, {
    weight: '500 800',
  });
  face
    .load()
    .then((f) => {
      (document.fonts as unknown as {add: (f: FontFace) => void}).add(f);
      continueRender(handle);
    })
    .catch((err) => {
      console.warn('Inter failed to load, using fallback fonts', err);
      continueRender(handle);
    });
}

// Quarterly sales data (in $K)
const DATA = [
  {label: 'Q1', value: 420},
  {label: 'Q2', value: 580},
  {label: 'Q3', value: 910},
  {label: 'Q4', value: 760},
];

// Headroom so the best bar + badge never collide with the title
const MAX_VALUE = 1200;
const TICKS = [0, 300, 600, 900, 1200];
const COLORS = ['#4F8CFF', '#8B6CFF', '#FF5FA2', '#2DD4BF'];

// Chart layout (1920x1080), centred horizontally
const CHART = {left: 300, right: 1660, top: 250, bottom: 900};
const CHART_W = CHART.right - CHART.left;
const CHART_H = CHART.bottom - CHART.top;
const BAR_W = 190;
const SLOT_W = CHART_W / DATA.length;

const SPRING_CFG = {damping: 9, stiffness: 120, mass: 0.85};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const money = (n: number) => `$${Math.round(n).toLocaleString('en-US')}K`;

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const bestIndex = DATA.reduce(
    (best, d, i) => (d.value > DATA[best].value ? i : best),
    0
  );

  // ---- Title ----
  const titleIn = spring({frame, fps, config: {damping: 14, stiffness: 120}});
  const titleY = interpolate(titleIn, [0, 1], [-40, 0]);

  // ---- Axis draw-in ----
  const yAxisP = interpolate(frame, [8, 36], [0, 1], {
    ...clamp,
    easing: Easing.inOut(Easing.cubic),
  });
  const xAxisP = interpolate(frame, [22, 52], [0, 1], {
    ...clamp,
    easing: Easing.inOut(Easing.cubic),
  });

  // ---- Bars ----
  const barsStart = 44;
  const stagger = 10;

  // ---- Glow on best quarter (right after the last bar settles) ----
  const glowStart = barsStart + stagger * DATA.length + 26;
  const glowIn = interpolate(frame, [glowStart, glowStart + 22], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const pulse = 0.78 + 0.22 * Math.sin((frame - glowStart) / 7);
  const glow = glowIn * pulse;

  // ---- Counting progress per bar (same timing as the bar spring, no overshoot) ----
  const counts = DATA.map((_, i) =>
    spring({
      frame: frame - (barsStart + i * stagger),
      fps,
      config: {...SPRING_CFG, overshootClamping: true},
    })
  );
  // Total (top-right) = sum of the bar counters, so it stays in sync
  const shownTotal = DATA.reduce((a, d, i) => a + d.value * counts[i], 0);

  // ---- Background light drift ----
  const lightX = 50 + 12 * Math.sin(frame / 60);

  // ---- Outro ----
  const outro = interpolate(
    frame,
    [durationInFrames - 14, durationInFrames - 1],
    [1, 0],
    clamp
  );

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 70% 60% at ${lightX}% 28%, #232a55 0%, #121633 45%, #070812 100%)`,
        fontFamily: `${fontFamily}, "Helvetica Neue", Helvetica, Arial, sans-serif`,
        color: 'white',
      }}
    >
      <AbsoluteFill style={{opacity: outro}}>
        {/* Title */}
        <div
          style={{
            position: 'absolute',
            top: 64,
            width: '100%',
            textAlign: 'center',
            opacity: titleIn,
            transform: `translateY(${titleY}px)`,
          }}
        >
          <div style={{fontSize: 66, fontWeight: 800, letterSpacing: -1.5}}>
            Quarterly Sales 2024
          </div>
          <div style={{fontSize: 28, fontWeight: 500, opacity: 0.55, marginTop: 6}}>
            Revenue in thousands of USD
          </div>
        </div>

        {/* Total pill */}
        <div
          style={{
            position: 'absolute',
            right: 120,
            top: 96,
            padding: '14px 26px',
            borderRadius: 999,
            background: 'rgba(255,255,255,0.06)',
            border: '1px solid rgba(255,255,255,0.12)',
            fontSize: 26,
            fontWeight: 600,
            opacity: interpolate(frame, [barsStart, barsStart + 12], [0, 1], clamp),
            fontVariantNumeric: 'tabular-nums',
          }}
        >
          <span style={{opacity: 0.55}}>Total&nbsp;&nbsp;</span>
          {money(shownTotal)}
        </div>

        <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
          <defs>
            {DATA.map((d, i) => (
              <linearGradient key={d.label} id={`grad-${i}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={COLORS[i]} stopOpacity={1} />
                <stop offset="100%" stopColor={COLORS[i]} stopOpacity={0.45} />
              </linearGradient>
            ))}
            <linearGradient id="gloss" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="white" stopOpacity={0.22} />
              <stop offset="35%" stopColor="white" stopOpacity={0.04} />
              <stop offset="100%" stopColor="white" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="white" stopOpacity={0} />
              <stop offset="50%" stopColor="white" stopOpacity={0.45} />
              <stop offset="100%" stopColor="white" stopOpacity={0} />
            </linearGradient>
            <radialGradient id="floor" cx="0.5" cy="0.5" r="0.5">
              <stop offset="0%" stopColor="#000" stopOpacity={0.55} />
              <stop offset="100%" stopColor="#000" stopOpacity={0} />
            </radialGradient>
            <filter id="glow" x="-60%" y="-40%" width="220%" height="180%">
              <feGaussianBlur stdDeviation="26" />
            </filter>
            <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="6" />
            </filter>
          </defs>

          {/* Gridlines + Y tick labels */}
          {TICKS.map((t, i) => {
            const y = CHART.bottom - (t / MAX_VALUE) * CHART_H;
            const tp = interpolate(frame, [18 + i * 4, 32 + i * 4], [0, 1], clamp);
            return (
              <g key={t} opacity={tp}>
                {t !== 0 && (
                  <line
                    x1={CHART.left}
                    x2={CHART.left + CHART_W * xAxisP}
                    y1={y}
                    y2={y}
                    stroke="white"
                    strokeOpacity={0.08}
                    strokeWidth={2}
                    strokeDasharray="8 10"
                  />
                )}
                <text
                  x={CHART.left - 26 + (1 - tp) * -14}
                  y={y + 9}
                  fill="white"
                  fillOpacity={0.5}
                  fontSize={26}
                  fontWeight={500}
                  textAnchor="end"
                >
                  {`$${t}K`}
                </text>
              </g>
            );
          })}

          {/* Axes */}
          <line
            x1={CHART.left}
            x2={CHART.left}
            y1={CHART.bottom}
            y2={CHART.bottom - CHART_H * yAxisP}
            stroke="white"
            strokeOpacity={0.65}
            strokeWidth={4}
            strokeLinecap="round"
          />
          <line
            x1={CHART.left}
            x2={CHART.left + CHART_W * xAxisP}
            y1={CHART.bottom}
            y2={CHART.bottom}
            stroke="white"
            strokeOpacity={0.65}
            strokeWidth={4}
            strokeLinecap="round"
          />
          {/* Drawing "pen" heads */}
          {yAxisP > 0 && yAxisP < 1 && (
            <circle cx={CHART.left} cy={CHART.bottom - CHART_H * yAxisP} r={7} fill="white" filter="url(#softGlow)" />
          )}
          {xAxisP > 0 && xAxisP < 1 && (
            <circle cx={CHART.left + CHART_W * xAxisP} cy={CHART.bottom} r={7} fill="white" filter="url(#softGlow)" />
          )}

          {/* Bars */}
          {DATA.map((d, i) => {
            const delay = barsStart + i * stagger;
            const s = spring({frame: frame - delay, fps, config: SPRING_CFG});
            // Same timing, no overshoot: drives the counter so it stays in sync with the bar
            const sCount = counts[i];
            const fullH = (d.value / MAX_VALUE) * CHART_H;
            const h = Math.max(0, fullH * s);
            // Squash & stretch: thinner while overshooting, wider while compressed
            const stretch = interpolate(s, [0, 1, 1.25], [0.88, 1, 0.9], clamp);
            const w = BAR_W * stretch;
            const cx = CHART.left + SLOT_W * i + SLOT_W / 2;
            const x = cx - w / 2;
            const y = CHART.bottom - h;

            const labelOpacity = interpolate(frame, [delay + 2, delay + 10], [0, 1], clamp);
            const isBest = i === bestIndex;
            const g = isBest ? glow : 0;

            // Light sweep across best bar
            const sweepT = ((frame - glowStart) % 70) / 70;
            const sweepY = CHART.bottom - (fullH + 160) * sweepT;

            // Delta vs previous quarter
            const delta = i > 0 ? ((d.value - DATA[i - 1].value) / DATA[i - 1].value) * 100 : null;

            return (
              <g key={d.label}>
                {/* Floor shadow */}
                <ellipse
                  cx={cx}
                  cy={CHART.bottom + 6}
                  rx={(w / 2 + 30) * Math.min(1, s)}
                  ry={14}
                  fill="url(#floor)"
                />
                {/* Glow halo for best quarter */}
                {isBest && g > 0 && (
                  <>
                    <rect x={x - 18} y={y - 18} width={w + 36} height={h + 18} rx={30} fill={COLORS[i]} opacity={0.75 * g} filter="url(#glow)" />
                    <ellipse cx={cx} cy={CHART.bottom} rx={180} ry={26} fill={COLORS[i]} opacity={0.35 * g} filter="url(#glow)" />
                  </>
                )}
                <rect x={x} y={y} width={w} height={h} rx={16} fill={`url(#grad-${i})`} />
                {/* Glossy highlight */}
                <rect x={x} y={y} width={w} height={h} rx={16} fill="url(#gloss)" />
                {/* Bright top cap */}
                {h > 8 && (
                  <rect x={x + 10} y={y + 4} width={w - 20} height={4} rx={2} fill="white" opacity={0.35} />
                )}
                {isBest && g > 0 && (
                  <>
                    <clipPath id="bestClip">
                      <rect x={x} y={y} width={w} height={h} rx={16} />
                    </clipPath>
                    <g clipPath="url(#bestClip)" opacity={glowIn}>
                      <rect
                        x={x - 40}
                        y={sweepY}
                        width={w + 80}
                        height={70}
                        fill="url(#sweep)"
                        transform={`skewY(-18) translate(0 ${Math.tan((18 * Math.PI) / 180) * cx})`}
                      />
                    </g>
                    <rect x={x} y={y} width={w} height={h} rx={16} fill="none" stroke="white" strokeOpacity={0.85 * g} strokeWidth={3} />
                  </>
                )}

                {/* Value label (counts in sync with the bar) */}
                <text
                  x={cx}
                  y={y - 26}
                  fill="white"
                  fontSize={42 + (isBest ? 8 * glowIn : 0)}
                  fontWeight={800}
                  textAnchor="middle"
                  opacity={labelOpacity}
                  style={{
                    fontVariantNumeric: 'tabular-nums',
                    filter: isBest && g > 0 ? `drop-shadow(0 0 ${14 * g}px ${COLORS[i]})` : undefined,
                  }}
                >
                  {money(d.value * sCount)}
                </text>

                {/* Quarter label */}
                <text
                  x={cx}
                  y={CHART.bottom + 58}
                  fill="white"
                  fillOpacity={0.85 * xAxisP}
                  fontSize={34}
                  fontWeight={600}
                  textAnchor="middle"
                >
                  {d.label}
                </text>
                {/* Delta vs previous */}
                {delta !== null && (
                  <text
                    x={cx}
                    y={CHART.bottom + 96}
                    fill={delta >= 0 ? '#4ADE80' : '#F87171'}
                    fontSize={24}
                    fontWeight={600}
                    textAnchor="middle"
                    opacity={interpolate(frame, [delay + 20, delay + 32], [0, 0.9], clamp)}
                  >
                    {`${delta >= 0 ? '▲' : '▼'} ${Math.abs(delta).toFixed(0)}%`}
                  </text>
                )}

                {/* Best badge (pill above the value) */}
                {isBest && glowIn > 0 && (
                  <g
                    opacity={glowIn}
                    transform={`translate(${cx} ${y - 112}) scale(${interpolate(
                      spring({frame: frame - glowStart, fps, config: {damping: 10, stiffness: 160}}),
                      [0, 1],
                      [0.6, 1]
                    )})`}
                  >
                    <rect x={-128} y={-24} width={256} height={46} rx={23} fill={COLORS[i]} opacity={0.18} stroke={COLORS[i]} strokeOpacity={0.8} strokeWidth={2} />
                    <text x={0} y={9} fill="#FFD1E6" fontSize={22} fontWeight={800} textAnchor="middle" letterSpacing={3}>
                      ★ BEST QUARTER
                    </text>
                  </g>
                )}

                {/* Sparkles around best bar */}
                {isBest &&
                  glowIn > 0 &&
                  new Array(14).fill(0).map((_, k) => {
                    const period = 50 + random(`p${k}`) * 40;
                    const t = ((frame - glowStart + random(`o${k}`) * period) % period) / period;
                    const px = x - 30 + random(`x${k}`) * (w + 60);
                    const py = CHART.bottom - random(`y${k}`) * (h + 40) - t * 60;
                    const a = Math.sin(t * Math.PI) * glowIn;
                    return <circle key={k} cx={px} cy={py} r={2 + random(`r${k}`) * 3} fill="white" opacity={a * 0.9} />;
                  })}
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
