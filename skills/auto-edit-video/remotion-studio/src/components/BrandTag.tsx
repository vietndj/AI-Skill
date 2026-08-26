import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

export interface BrandTagProps {
  left?: string;
  center?: string;
  right?: string;
}

export const BrandTag: React.FC<BrandTagProps> = ({
  left = 'Viral Video COURSE',
  center = '↗ 0934.68.86.32 (imess)',
  right = '2026',
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        top: '52px',
        left: '56px',
        right: '56px',
        zIndex: 100,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'rgba(10, 14, 22, 0.72)',
        backdropFilter: 'blur(16px)',
        border: '1.5px solid rgba(255, 255, 255, 0.15)',
        padding: '14px 32px',
        borderRadius: '999px',
        boxShadow: '0 8px 30px rgba(0, 0, 0, 0.75)',
        opacity,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          fontFamily: "'SVN-Aeonik', sans-serif",
          fontSize: '20px',
          fontWeight: 700,
          color: '#FFFFFF',
          letterSpacing: '0.8px',
          textTransform: 'uppercase',
          textShadow: '0 2px 8px rgba(0, 0, 0, 0.95)',
        }}
      >
        {left}
      </div>

      <div
        style={{
          fontFamily: "'SVN-Aeonik', 'SF Mono', monospace",
          fontSize: '19px',
          fontWeight: 600,
          color: '#FFDE00',
          letterSpacing: '0.6px',
          textShadow: '0 0 15px rgba(255, 222, 0, 0.6), 0 2px 8px rgba(0, 0, 0, 0.95)',
        }}
      >
        {center}
      </div>

      <div
        style={{
          fontFamily: "'SVN-Integral', sans-serif",
          fontSize: '22px',
          fontWeight: 900,
          color: '#FFFFFF',
          letterSpacing: '1px',
          textShadow: '0 2px 8px rgba(0, 0, 0, 0.95)',
        }}
      >
        {right}
      </div>
    </div>
  );
};
