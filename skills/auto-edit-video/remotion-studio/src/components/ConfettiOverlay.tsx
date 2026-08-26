import React, { useMemo } from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export interface ConfettiOverlayProps {
  startFrame?: number;
  durationFrames?: number;
  count?: number;
  theme?: 'gold' | 'celebration';
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  color: string;
  rotationSpeed: number;
  shape: 'rect' | 'circle';
}

export const ConfettiOverlay: React.FC<ConfettiOverlayProps> = ({
  startFrame = 0,
  durationFrames = 60,
  count = 60,
  theme = 'gold',
}) => {
  const frame = useCurrentFrame();
  const localFrame = Math.max(0, frame - startFrame);

  if (frame < startFrame || localFrame > durationFrames) {
    return null;
  }

  const colors =
    theme === 'gold'
      ? ['#FFDE00', '#FFA500', '#FFFFFF', '#FFE873', '#D4AF37']
      : ['#FFDE00', '#00FFCC', '#FF007F', '#FFFFFF', '#7928CA'];

  // Generate deterministic particles using pseudo-random seed
  const particles: Particle[] = useMemo(() => {
    const list: Particle[] = [];
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2 + (Math.sin(i * 99) * 0.5);
      const speed = 12 + (Math.sin(i * 33) * 6);
      list.push({
        x: 540,
        y: 960,
        vx: Math.cos(angle) * speed * 1.6,
        vy: (Math.sin(angle) * speed - 16) * 1.4,
        size: 14 + (Math.sin(i * 77) * 8),
        color: colors[i % colors.length],
        rotationSpeed: (Math.sin(i * 123) * 15),
        shape: i % 3 === 0 ? 'circle' : 'rect',
      });
    }
    return list;
  }, [count, theme]);

  const gravity = 0.95;
  const opacity = interpolate(localFrame, [0, 8, durationFrames - 12, durationFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 60, opacity }}>
      {particles.map((p, idx) => {
        const posX = p.x + p.vx * localFrame;
        const posY = p.y + p.vy * localFrame + 0.5 * gravity * localFrame * localFrame;
        const rot = localFrame * p.rotationSpeed;

        return (
          <div
            key={idx}
            style={{
              position: 'absolute',
              left: `${posX}px`,
              top: `${posY}px`,
              width: `${p.size}px`,
              height: p.shape === 'rect' ? `${p.size * 1.6}px` : `${p.size}px`,
              backgroundColor: p.color,
              borderRadius: p.shape === 'circle' ? '50%' : '2px',
              transform: `rotate(${rot}deg)`,
              boxShadow: `0 0 10px ${p.color}`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
