import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const PullQuoteCard: React.FC<{
  quote: string;
  speaker: string;
  fontSize?: number;
  bgColor?: string;
  textColor?: string;
  enterFrame?: number;
  durationFrames?: number;
}> = ({ quote, speaker, fontSize = 64, bgColor = 'rgba(0,0,0,0.7)', textColor = '#fff', enterFrame = 0, durationFrames = 90 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const relFrame = Math.max(0, frame - enterFrame);

  const spr = spring({
    frame: relFrame,
    fps,
    config: { damping: 14, stiffness: 150 }
  });

  const scale = interpolate(spr, [0, 1], [0.8, 1]);
  const bgOpacity = interpolate(spr, [0, 1], [0, 1]);
  const opacity = interpolate(
    relFrame,
    [0, 10, durationFrames - 15, durationFrames],
    [0, 1, 1, 0],
    { extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{
      backgroundColor: bgColor,
      opacity: bgOpacity,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '40px',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)'
    }}>
      <div style={{
        transform: `scale(${scale})`,
        opacity,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '24px'
      }}>
        <div style={{
          fontFamily: "'Be Vietnam Pro', sans-serif",
          fontSize: `${fontSize}px`,
          fontWeight: 700,
          color: textColor,
          textAlign: 'center',
          lineHeight: 1.3
        }}>
          "{quote}"
        </div>
        <div style={{
          fontFamily: "'Be Vietnam Pro', sans-serif",
          fontSize: `${fontSize * 0.5}px`,
          fontWeight: 500,
          color: textColor,
          opacity: 0.8
        }}>
          — {speaker}
        </div>
      </div>
    </AbsoluteFill>
  );
};
