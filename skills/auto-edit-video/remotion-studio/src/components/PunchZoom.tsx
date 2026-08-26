import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { LifestyleSceneConfig } from '../types';

interface PunchZoomProps {
  scenes: LifestyleSceneConfig[];
  children: React.ReactNode;
}

export const PunchZoom: React.FC<PunchZoomProps> = ({ scenes, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Find the currently active scene
  const activeScene = scenes.find(s => {
    const startF = Math.round(s.start * fps);
    const endF = Math.round(s.end * fps);
    return frame >= startF && frame < endF;
  });

  const isZoom = activeScene?.punchZoom?.enabled ?? false;
  const targetScale = isZoom ? (activeScene?.punchZoom?.scale ?? 1.18) : 1.0;
  const originX = activeScene?.punchZoom?.originX ?? 50;
  const originY = activeScene?.punchZoom?.originY ?? 38;

  const startF = activeScene ? Math.round(activeScene.start * fps) : 0;
  const relFrame = Math.max(0, frame - startF);

  // If not zooming, just return normal scale
  // We use spring to smoothly zoom in when a zoom scene starts
  const spr = spring({
    frame: relFrame,
    fps,
    config: {
      damping: 12,
      mass: 0.5,
      stiffness: 180,
    },
  });

  // Calculate current scale. If it's a zoom scene, interpolate from 1 to targetScale.
  // If it's not a zoom scene, smoothly zoom back to 1.0 using another spring? 
  // Actually, a simpler way is to just let spring handle the transition from 1.0 to targetScale.
  // If the scene suddenly changes to no-zoom, the component re-evaluates.
  // To make transitions perfectly smooth across scene boundaries, it's better to calculate
  // the exact scale based on the previous frame, but Remotion requires pure functions.
  // A simple spring from 1.0 to targetScale works well for cut-in zooms.
  const currentScale = isZoom ? interpolate(spr, [0, 1], [1.0, targetScale]) : 1.0;

  return (
    <AbsoluteFill
      style={{
        transformOrigin: `${originX}% ${originY}%`,
        transform: `scale(${currentScale})`,
        willChange: 'transform',
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

