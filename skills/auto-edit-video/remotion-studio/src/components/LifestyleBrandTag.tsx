import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface LifestyleBrandTagProps {
  badgeText?: string;
  timeText?: string;
  locationText?: string;
  enabled?: boolean;
}

export const LifestyleBrandTag: React.FC<LifestyleBrandTagProps> = ({
  badgeText = '✨ Daily Moments',
  timeText,
  locationText,
  enabled = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!enabled) return null;

  const spr = spring({
    frame,
    fps,
    config: {
      damping: 14,
      mass: 0.5,
    },
  });

  const opacity = interpolate(spr, [0, 1], [0, 1]);
  const translateY = interpolate(spr, [0, 1], [-20, 0]);

  return (
    <div
      style={{
        position: 'absolute',
        top: '60px',
        left: '48px',
        right: '48px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        opacity,
        transform: `translateY(${translateY}px)`,
        zIndex: 60,
        pointerEvents: 'none',
      }}
    >
      {/* Left Badge */}
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 18px',
          background: 'rgba(0, 0, 0, 0.35)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          borderRadius: '20px',
          border: '1px solid rgba(255, 255, 255, 0.25)',
          color: '#FFFFFF',
          fontFamily: "'Be Vietnam Pro', sans-serif",
          fontSize: '22px',
          fontWeight: 600,
          boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
        }}
      >
        <span>{badgeText}</span>
      </div>

      {/* Right Time / Location (Optional) */}
      {(timeText || locationText) && (
        <div
          style={{
            padding: '8px 16px',
            background: 'rgba(0, 0, 0, 0.3)',
            backdropFilter: 'blur(10px)',
            borderRadius: '16px',
            color: 'rgba(255, 255, 255, 0.9)',
            fontFamily: "'Be Vietnam Pro', sans-serif",
            fontSize: '20px',
            fontWeight: 500,
          }}
        >
          {locationText ? `${locationText} ` : ''}{timeText || ''}
        </div>
      )}
    </div>
  );
};
