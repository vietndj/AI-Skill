import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export interface SceneTransitionProps {
  transitionFrame: number;
  durationFrames: number;
}

export const SceneTransition: React.FC<SceneTransitionProps> = ({
  transitionFrame,
  durationFrames = 12
}) => {
  const frame = useCurrentFrame();
  
  const halfDuration = Math.round(durationFrames / 2);
  const startFrame = transitionFrame - halfDuration;
  const endFrame = transitionFrame + halfDuration;

  if (frame < startFrame || frame > endFrame) return null;

  const opacity = interpolate(
    frame,
    [startFrame, transitionFrame, endFrame],
    [0, 0.6, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: 'black', opacity }} />
  );
};
