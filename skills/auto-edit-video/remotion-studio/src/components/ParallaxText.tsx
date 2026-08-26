import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

export const ParallaxText: React.FC<{
  text: string;
  fontSize?: number;
  fontFamily?: string;
  color?: string;
  direction?: 'left' | 'right' | 'up' | 'down';
  speed?: number;
  startFrame?: number;
  durationFrames?: number;
}> = ({ text, fontSize = 48, fontFamily = 'sans-serif', color = '#fff', direction = 'left', speed = 50, startFrame = 0, durationFrames = 90 }) => {
  const frame = useCurrentFrame();
  const relFrame = Math.max(0, frame - startFrame);

  const drift = interpolate(relFrame, [0, durationFrames], [0, speed]);
  
  let transform = '';
  if (direction === 'left') transform = `translateX(${-drift}px)`;
  if (direction === 'right') transform = `translateX(${drift}px)`;
  if (direction === 'up') transform = `translateY(${-drift}px)`;
  if (direction === 'down') transform = `translateY(${drift}px)`;

  const opacity = interpolate(
    relFrame,
    [0, 15, durationFrames - 15, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div style={{
      fontFamily,
      fontSize: `${fontSize}px`,
      color,
      transform,
      opacity,
      textShadow: '0 2px 8px rgba(0,0,0,0.5)',
      textAlign: 'center'
    }}>
      {text}
    </div>
  );
};
