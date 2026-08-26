import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const SurpriseEffect: React.FC<{
  effectType: 'emoji_burst' | 'freeze_zoom' | 'color_flash' | 'sparkle_trail' | 'light_leak' | 'golden_bloom' | 'glitch_cut' | 'beat_flash';
  startFrame: number;
  durationFrames: number;
  intensity?: number;
}> = ({ effectType, startFrame, durationFrames, intensity = 1.0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const relFrame = frame - startFrame;

  if (frame < startFrame || frame >= startFrame + durationFrames) {
    return null;
  }

  if (effectType === 'color_flash' || effectType === 'beat_flash') {
    const opacity = interpolate(relFrame, [0, 10], [intensity * 0.8, 0], { extrapolateRight: 'clamp' });
    return <AbsoluteFill style={{ backgroundColor: '#FF8C00', opacity, pointerEvents: 'none', zIndex: 100 }} />;
  }
  
  if (effectType === 'light_leak') {
    const opacity = Math.sin((relFrame / durationFrames) * Math.PI) * intensity * 0.6;
    return (
      <AbsoluteFill style={{
        background: 'radial-gradient(circle at top right, #FF7F50, transparent)',
        opacity, pointerEvents: 'none', zIndex: 100
      }} />
    );
  }

  if (effectType === 'golden_bloom') {
    const opacity = Math.sin((relFrame / durationFrames) * Math.PI) * intensity * 0.4;
    return <AbsoluteFill style={{ boxShadow: 'inset 0 0 100px 50px rgba(255,215,0,0.5)', opacity, pointerEvents: 'none', zIndex: 100 }} />;
  }

  if (effectType === 'emoji_burst') {
    const emojis = ['✨', '🔥', '🎉', '🌟', '💖', '🚀', '💥', '🎈'];
    return (
      <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 100 }}>
        {emojis.map((emoji, i) => {
          const spr = spring({ frame: relFrame, fps, config: { damping: 10, mass: 0.5, stiffness: 150 } });
          const angle = (i / emojis.length) * Math.PI * 2;
          const dist = interpolate(spr, [0, 1], [0, 300 * intensity]);
          const x = Math.cos(angle) * dist;
          const y = Math.sin(angle) * dist;
          const scale = interpolate(spr, [0, 0.5, 1], [0, 1.5, 1]);
          const opacity = interpolate(relFrame, [durationFrames - 15, durationFrames], [1, 0], { extrapolateLeft: 'clamp' });
          return (
            <div key={i} style={{
              position: 'absolute', top: '50%', left: '50%',
              transform: `translate(-50%, -50%) translate(${x}px, ${y}px) scale(${scale})`,
              fontSize: '48px', opacity
            }}>
              {emoji}
            </div>
          );
        })}
      </AbsoluteFill>
    );
  }

  if (effectType === 'glitch_cut') {
    const offset = (Math.random() - 0.5) * 40 * intensity;
    const isGlitch = relFrame % 5 < 2;
    if (!isGlitch) return null;
    return (
      <AbsoluteFill style={{
        transform: `translateX(${offset}px)`,
        boxShadow: `10px 0 0 red, -10px 0 0 blue`,
        opacity: 0.3,
        pointerEvents: 'none', zIndex: 100
      }} />
    );
  }

  if (effectType === 'sparkle_trail') {
    const sparkles = Array.from({ length: 20 });
    return (
      <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 100 }}>
        {sparkles.map((_, i) => {
          const x = (Math.sin(relFrame / 10 + i) * 50) + 50;
          const y = (Math.cos(relFrame / 10 + i) * 50) + 50;
          const opacity = Math.random() > 0.5 ? intensity : 0;
          return <div key={i} style={{ position: 'absolute', left: `${x}%`, top: `${y}%`, fontSize: '24px', opacity }}>✨</div>;
        })}
      </AbsoluteFill>
    );
  }

  return null;
};
