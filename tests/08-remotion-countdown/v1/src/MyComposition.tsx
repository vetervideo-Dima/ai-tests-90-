import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const NUMBERS = [5, 4, 3, 2, 1];

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Each number gets exactly one second on screen
  const segment = fps;
  const index = Math.min(Math.floor(frame / segment), NUMBERS.length - 1);
  const localFrame = frame - index * segment;
  const value = NUMBERS[index];

  // Enter: scale up + fade in; Exit: scale down + fade out
  const enterDuration = Math.round(segment * 0.35);
  const exitStart = Math.round(segment * 0.7);

  const scale = interpolate(
    localFrame,
    [0, enterDuration, exitStart, segment],
    [0.4, 1, 1, 1.6],
    {
      easing: Easing.inOut(Easing.cubic),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const opacity = interpolate(
    localFrame,
    [0, enterDuration, exitStart, segment],
    [0, 1, 1, 0],
    {
      easing: Easing.inOut(Easing.quad),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const translateY = interpolate(localFrame, [0, enterDuration], [40, 0], {
    easing: Easing.out(Easing.exp),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Progress ring that drains over each second
  const ringProgress = interpolate(localFrame, [0, segment], [1, 0], {
    easing: Easing.linear,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const radius = Math.min(width, height) * 0.3;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - ringProgress);

  // Background hue shifts smoothly across the full countdown
  const hue = interpolate(
    frame,
    [0, segment * NUMBERS.length],
    [220, 340],
    {
      easing: Easing.inOut(Easing.sin),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        background: `radial-gradient(circle at center, hsl(${hue}, 60%, 22%) 0%, hsl(${hue}, 70%, 8%) 100%)`,
        fontFamily: "Inter, Helvetica, Arial, sans-serif",
      }}
    >
      <svg
        width={width}
        height={height}
        style={{ position: "absolute", top: 0, left: 0 }}
      >
        <circle
          cx={width / 2}
          cy={height / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.12)"
          strokeWidth={12}
        />
        <circle
          cx={width / 2}
          cy={height / 2}
          r={radius}
          fill="none"
          stroke={`hsl(${hue}, 90%, 65%)`}
          strokeWidth={12}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          transform={`rotate(-90 ${width / 2} ${height / 2})`}
        />
      </svg>
      <div
        style={{
          fontSize: radius * 1.2,
          fontWeight: 800,
          color: "white",
          opacity,
          transform: `translateY(${translateY}px) scale(${scale})`,
          textShadow: `0 0 40px hsla(${hue}, 90%, 65%, 0.8)`,
          lineHeight: 1,
        }}
      >
        {value}
      </div>
    </AbsoluteFill>
  );
};
