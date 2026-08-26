import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { findLifestyleStyleById, LifestyleStyle } from '../data/lifestyle_styles';

interface LifestyleSubtitlesProps {
  line1: string;
  line2?: string;
  styleId?: number | string;
  fontSize1?: number;
  fontSize2?: number;
  posY?: number; // 0-100% from top, default ~78% (safe-zone above TikTok caption)
  motion?: 'pop' | 'bounce' | 'slide_up' | 'fade';
  enterFrame?: number;
}

export const LifestyleSubtitles: React.FC<LifestyleSubtitlesProps> = ({
  line1,
  line2,
  styleId = 1,
  fontSize1 = 44,
  fontSize2 = 32,
  posY = 78,
  motion = 'bounce',
  enterFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!line1 && !line2) return null;

  const style: LifestyleStyle = findLifestyleStyleById(styleId);
  const relFrame = Math.max(0, frame - enterFrame);

  // Entrance spring
  const spr = spring({
    frame: relFrame,
    fps,
    config: {
      damping: motion === 'bounce' ? 10 : 14,
      mass: 0.5,
      stiffness: 160,
    },
  });

  // Calculate motion transform
  let transform = '';
  let opacity = 1;

  if (motion === 'pop' || motion === 'bounce') {
    const scale = interpolate(spr, [0, 1], [0.8, 1.0]);
    transform = `scale(${scale})`;
    opacity = interpolate(spr, [0, 0.4], [0, 1]);
  } else if (motion === 'slide_up') {
    const translateY = interpolate(spr, [0, 1], [40, 0]);
    transform = `translateY(${translateY}px)`;
    opacity = interpolate(spr, [0, 0.5], [0, 1]);
  } else {
    opacity = interpolate(spr, [0, 1], [0, 1]);
  }

  return (
    <div
      style={{
        position: 'absolute',
        top: `${posY}%`,
        left: 0,
        right: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '0 40px',
        zIndex: 40,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          display: 'inline-flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: line2 ? '6px' : '0px',
          maxWidth: '92%',
          background: style.bgColor || 'rgba(0,0,0,0.6)',
          border: style.borderColor ? `${style.borderWidth || 2}px solid ${style.borderColor}` : 'none',
          borderRadius: `${style.borderRadius || 28}px`,
          padding: style.padding || '12px 28px',
          boxShadow: style.boxShadow || '0 8px 24px rgba(0,0,0,0.2)',
          backdropFilter: style.backdropBlur ? `blur(${style.backdropBlur})` : undefined,
          WebkitBackdropFilter: style.backdropBlur ? `blur(${style.backdropBlur})` : undefined,
          transform,
          opacity,
          transition: 'all 0.15s ease-out',
        }}
      >
        {/* Main Line */}
        {line1 && (
          <div
            style={{
              fontFamily: style.fontFamily,
              fontWeight: style.fontWeight,
              fontStyle: style.fontStyle || 'normal',
              fontSize: `${fontSize1}px`,
              color: style.textColor,
              textAlign: 'center',
              lineHeight: 1.25,
              letterSpacing: '-0.01em',
              textShadow: style.textShadow,
              textTransform: style.line1Transform || 'none',
            }}
          >
            {line1}
          </div>
        )}

        {/* Secondary Line (if present) */}
        {line2 && (
          <div
            style={{
              fontFamily: style.fontFamily,
              fontWeight: '600',
              fontSize: `${fontSize2}px`,
              color: style.textColor,
              opacity: 0.88,
              textAlign: 'center',
              lineHeight: 1.2,
            }}
          >
            {line2}
          </div>
        )}
      </div>
    </div>
  );
};
