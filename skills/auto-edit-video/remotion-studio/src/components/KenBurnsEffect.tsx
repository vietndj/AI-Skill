import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const KenBurnsEffect: React.FC<{
  scale?: number;
  direction?: 'zoom_in' | 'zoom_out' | 'pan_left' | 'pan_right';
  durationFrames: number;
  children: React.ReactNode;
}> = ({ scale = 1.08, direction = 'zoom_in', durationFrames, children }) => {
  const frame = useCurrentFrame();

  let transform = '';
  if (direction === 'zoom_in') {
    const s = interpolate(frame, [0, durationFrames], [1, scale], { extrapolateRight: 'clamp' });
    transform = `scale(${s})`;
  } else if (direction === 'zoom_out') {
    const s = interpolate(frame, [0, durationFrames], [scale, 1], { extrapolateRight: 'clamp' });
    transform = `scale(${s})`;
  } else if (direction === 'pan_left') {
    const x = interpolate(frame, [0, durationFrames], [0, -5], { extrapolateRight: 'clamp' });
    transform = `scale(${scale}) translateX(${x}%)`;
  } else if (direction === 'pan_right') {
    const x = interpolate(frame, [0, durationFrames], [0, 5], { extrapolateRight: 'clamp' });
    transform = `scale(${scale}) translateX(${x}%)`;
  }

  return (
    <AbsoluteFill style={{ transform, transformOrigin: 'center center', willChange: 'transform' }}>
      {children}
    </AbsoluteFill>
  );
};
