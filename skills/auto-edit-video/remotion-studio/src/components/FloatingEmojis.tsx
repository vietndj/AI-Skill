import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface FloatingEmojisProps {
  emojis: string[];
  position?: 'top-right' | 'top-left' | 'center-right' | 'center-left' | 'bottom-right';
  motion?: 'float_up' | 'bounce' | 'pulse';
  enterFrame?: number;
  durationFrames?: number;
}

export const FloatingEmojis: React.FC<FloatingEmojisProps> = ({
  emojis = [],
  position = 'top-right',
  motion = 'float_up',
  enterFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!emojis || emojis.length === 0) return null;

  const relFrame = Math.max(0, frame - enterFrame);

  // Positional coordinates
  const positionStyles: Record<string, React.CSSProperties> = {
    'top-right': { top: '16%', right: '8%' },
    'top-left': { top: '16%', left: '8%' },
    'center-right': { top: '42%', right: '7%' },
    'center-left': { top: '42%', left: '7%' },
    'bottom-right': { bottom: '26%', right: '8%' },
  };

  return (
    <div
      style={{
        position: 'absolute',
        ...positionStyles[position],
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        pointerEvents: 'none',
        zIndex: 50,
      }}
    >
      {emojis.map((emoji, index) => {
        const delay = index * 4;
        const itemFrame = Math.max(0, relFrame - delay);

        const spr = spring({
          frame: itemFrame,
          fps,
          config: {
            damping: 10,
            mass: 0.5,
            stiffness: 150,
          },
        });

        // Scale pop in
        const scale = interpolate(spr, [0, 1], [0, 1.25]);
        
        // Gentle float up / oscillation
        const translateY = motion === 'float_up'
          ? interpolate(itemFrame, [0, 60], [10, -35], { extrapolateRight: 'clamp' })
          : Math.sin((itemFrame + index * 10) / 8) * 8;

        const rotate = (index % 2 === 0 ? 1 : -1) * (12 + Math.sin(itemFrame / 10) * 8);

        return (
          <div
            key={index}
            style={{
              fontSize: '64px',
              lineHeight: '1',
              transform: `translateY(${translateY}px) scale(${scale}) rotate(${rotate}deg)`,
              filter: 'drop-shadow(0 8px 16px rgba(0,0,0,0.25))',
              display: 'inline-block',
            }}
          >
            {emoji}
          </div>
        );
      })}
    </div>
  );
};
