import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const TEXT = "Hello World";
const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  const framesPerChar = Math.round(fps / 8); // ~8 characters per second
  const startDelay = Math.round(fps * 0.4);
  const typingEnd = startDelay + framesPerChar * TEXT.length;

  const charsShown = Math.floor(
    interpolate(frame, [startDelay, typingEnd], [0, TEXT.length], clamp)
  );

  // Cursor: solid while typing, smooth blink (strictly increasing input range) otherwise
  const typing = frame >= startDelay && frame < typingEnd + framesPerChar;
  const cursorPhase = (frame % fps) / fps;
  const blink = interpolate(cursorPhase, [0, 0.4, 0.5, 0.9, 1], [1, 1, 0, 0, 1], {
    easing: Easing.inOut(Easing.ease),
  });
  const cursorOpacity = typing ? 1 : blink;

  const fontSize = Math.min(width, height) * 0.13;

  // Gentle camera push and fade-out at the end
  const push = interpolate(frame, [0, durationInFrames], [1, 1.06], clamp);
  const fadeOut = interpolate(frame, [durationInFrames - 10, durationInFrames - 1], [1, 0], clamp);
  const underline = interpolate(frame, [typingEnd, typingEnd + fps * 0.5], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(ellipse at 50% 45%, #1b2030 0%, #0d0f16 55%, #06070a 100%)",
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeOut,
      }}
    >
      <div
        style={{
          position: "relative",
          transform: `scale(${push})`,
          fontFamily:
            "'Fira Code', 'JetBrains Mono', 'DejaVu Sans Mono', 'Liberation Mono', 'Courier New', monospace",
          fontSize,
          fontWeight: 600,
          color: "#f5f7fa",
          whiteSpace: "pre",
          display: "flex",
          alignItems: "center",
          textShadow: "0 0 24px rgba(74, 222, 128, 0.25)",
        }}
      >
        {/* All letters are laid out from the start, so the line never re-centres while typing */}
        {TEXT.split("").map((char, i) => {
          const charStart = startDelay + i * framesPerChar;
          const p = interpolate(frame, [charStart, charStart + framesPerChar * 1.5], [0, 1], {
            ...clamp,
            easing: Easing.out(Easing.cubic),
          });
          const visible = i < charsShown;
          return (
            <React.Fragment key={i}>
              <span
                style={{
                  display: "inline-block",
                  opacity: visible ? p : 0,
                  transform: `translateY(${(1 - p) * fontSize * 0.18}px)`,
                  filter: `blur(${((1 - p) * 6).toFixed(2)}px)`,
                  color: i >= 6 ? "#4ade80" : undefined,
                }}
              >
                {char}
              </span>
              {i === charsShown - 1 ? <Cursor opacity={cursorOpacity} size={fontSize} /> : null}
            </React.Fragment>
          );
        })}
        {charsShown === 0 ? (
          <span style={{ position: "absolute", left: 0, top: 0, bottom: 0, display: "flex", alignItems: "center" }}>
            <Cursor opacity={cursorOpacity} size={fontSize} />
          </span>
        ) : null}
        <div
          style={{
            position: "absolute",
            left: 0,
            bottom: -fontSize * 0.18,
            height: Math.max(3, fontSize * 0.03),
            width: `${underline * 100}%`,
            background: "linear-gradient(90deg, #4ade80, #22d3ee)",
            borderRadius: 4,
            boxShadow: "0 0 18px rgba(74,222,128,0.6)",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

// Zero-width anchor so the cursor never pushes the text around
const Cursor: React.FC<{ opacity: number; size: number }> = ({ opacity, size }) => (
  <span style={{ position: "relative", display: "inline-block", width: 0, height: size }}>
    <span
      style={{
        position: "absolute",
        left: size * 0.06,
        top: size * 0.04,
        width: Math.max(6, size * 0.07),
        height: size * 0.95,
        backgroundColor: "#4ade80",
        borderRadius: 3,
        boxShadow: "0 0 16px rgba(74,222,128,0.8)",
        opacity,
      }}
    />
  </span>
);
