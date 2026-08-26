import React from 'react';
import { AbsoluteFill, OffthreadVideo, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface BRollSceneProps {
  videoSrc: string;
  enterFrame: number;
  durationFrames: number;
  trimStartSec: number;
}

export const BRollScene: React.FC<BRollSceneProps> = ({
  videoSrc,
  enterFrame,
  durationFrames,
  trimStartSec
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - enterFrame;

  if (localFrame < 0 || localFrame >= durationFrames) return null;

  const startFrom = Math.round(trimStartSec * fps);
  
  const opacity = interpolate(
    localFrame,
    [0, 10, durationFrames - 10, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ opacity }}>
      <OffthreadVideo 
        src={videoSrc} 
        startFrom={startFrom}
        endAt={startFrom + durationFrames}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
    </AbsoluteFill>
  );
};
