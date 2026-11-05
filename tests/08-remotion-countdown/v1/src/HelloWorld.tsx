import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const TEXT = "Hello World";

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const framesPerChar = Math.round(fps / 8); // ~8 characters per second
  const startDelay = Math.round(fps * 0.3);

  const charsShown = Math.floor(
    interpolate(
      frame,
      [startDelay, startDelay + framesPerChar * TEXT.length],
      [0, TEXT.length],
      {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      }
    )
  );

  const typed = TEXT.slice(0, charsShown);

  // Cursor blinks with a smooth fade (period: 1 second)
  const cursorPhase = (frame % fps) / fps;
  const cursorOpacity = interpolate(
    cursorPhase,
    [0, 0.5, 0.5, 1],
    [1, 1, 0, 0],
    { easing: Easing.inOut(Easing.ease) }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0f0f14",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          fontFamily: "'Fira Code', 'Courier New', monospace",
          fontSize: 120,
          color: "#f5f5f5",
          whiteSpace: "pre",
          display: "flex",
          alignItems: "center",
        }}
      >
        {typed.split("").map((char, i) => {
          const charStart = startDelay + i * framesPerChar;
          const charOpacity = interpolate(
            frame,
            [charStart, charStart + framesPerChar],
            [0, 1],
            {
              easing: Easing.out(Easing.cubic),
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }
          );
          const charY = interpolate(
            frame,
            [charStart, charStart + framesPerChar],
            [20, 0],
            {
              easing: Easing.out(Easing.cubic),
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }
          );
          return (
            <span
              key={i}
              style={{
                opacity: charOpacity,
                display: "inline-block",
                transform: `translateY(${charY}px)`,
              }}
            >
              {char}
            </span>
          );
        })}
        <span
          style={{
            opacity: cursorOpacity,
            width: 8,
            height: 130,
            backgroundColor: "#4ade80",
            marginLeft: 8,
            display: "inline-block",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
