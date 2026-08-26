import React from 'react';
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const FreezeFrame: React.FC<{
  freezeAtFrame: number;
  freezeDuration: number;
  zoomScale?: number;
  children: React.ReactNode;
}> = ({ freezeAtFrame, freezeDuration, zoomScale = 1.1, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const isFrozen = frame >= freezeAtFrame && frame < freezeAtFrame + freezeDuration;
  const relFrame = isFrozen ? frame - freezeAtFrame : 0;

  const spr = spring({
    frame: relFrame,
    fps,
    config: { damping: 12, stiffness: 180 }
  });
  
  const scale = isFrozen ? 1 + (zoomScale - 1) * spr : 1;

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})`, transformOrigin: 'center center' }}>
      {children}
    </AbsoluteFill>
  );
};
