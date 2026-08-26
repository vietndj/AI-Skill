import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export interface FullscreenTextCardProps {
  badge?: string;
  tier1: string;
  tier2?: string;
  tier1Color?: string;
  tier2Color?: string;
  theme?: 'dark' | 'gold' | 'outro';
  durationInFrames: number;
  hasArrow?: boolean;
}

export const FullscreenTextCard: React.FC<FullscreenTextCardProps> = ({
  badge,
  tier1,
  tier2,
  tier1Color = '#FFDE00',
  tier2Color = '#FFFFFF',
  theme = 'dark',
  durationInFrames,
  hasArrow = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animation (Frames 0 -> 12)
  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 110 },
  });

  const cardScaleEnter = interpolate(enterSpring, [0, 1], [0.88, 1.0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const cardOpacityEnter = interpolate(frame, [0, 6], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Exit animation (Last 8 frames: J-Cut fade & zoom out)
  const exitFrames = 8;
  const exitStartFrame = Math.max(0, durationInFrames - exitFrames);
  
  const exitProgress = interpolate(frame, [exitStartFrame, durationInFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const cardScale = interpolate(exitProgress, [0, 1], [cardScaleEnter, 1.08]);
  const cardOpacity = interpolate(exitProgress, [0, 1], [cardOpacityEnter, 0]);

  // Background gradient per theme
  let background = 'radial-gradient(circle at 50% 50%, #161b26 0%, #080a10 65%, #000000 100%)';
  if (theme === 'gold') {
    background = 'radial-gradient(circle at 50% 45%, #2a2205 0%, #120e02 60%, #000000 100%)';
  } else if (theme === 'outro') {
    background = 'radial-gradient(circle at 50% 55%, #1f1b0c 0%, #0d0c07 70%, #000000 100%)';
  }

  // Dynamic font sizing for Tier 1
  let tier1Size = 92;
  if (tier1.length > 18) tier1Size = 72;
  else if (tier1.length > 12) tier1Size = 82;

  // Arrow bounce animation
  const arrowBounce = Math.sin(frame * 0.25) * 16;

  return (
    <AbsoluteFill
      style={{
        background,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '0 64px',
        textAlign: 'center',
        opacity: cardOpacity,
        transform: `scale(${cardScale})`,
        zIndex: 50,
      }}
    >
      {badge && (
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '10px',
            padding: '12px 32px',
            borderRadius: '999px',
            background: 'rgba(255, 222, 0, 0.14)',
            border: '2px solid rgba(255, 222, 0, 0.5)',
            color: '#FFDE00',
            fontFamily: "'SVN-Aeonik', sans-serif",
            fontSize: '24px',
            fontWeight: 800,
            letterSpacing: '2px',
            marginBottom: '36px',
            textTransform: 'uppercase',
            boxShadow: '0 4px 25px rgba(255, 222, 0, 0.25)',
          }}
        >
          {badge}
        </div>
      )}

      <div
        style={{
          fontFamily: "'SVN-Integral', sans-serif",
          fontWeight: 900,
          fontSize: `${tier1Size}px`,
          lineHeight: 1.05,
          color: tier1Color,
          textTransform: 'uppercase',
          letterSpacing: '-0.02em',
          textShadow:
            tier1Color === '#FFDE00'
              ? '0 0 35px rgba(255, 222, 0, 0.95), 0 0 75px rgba(255, 180, 0, 0.7), 0 8px 25px rgba(0, 0, 0, 0.98)'
              : '0 0 35px rgba(255, 255, 255, 0.95), 0 0 70px rgba(255, 255, 255, 0.6), 0 8px 25px rgba(0, 0, 0, 0.98)',
          maxWidth: '960px',
        }}
      >
        {tier1}
      </div>

      {tier2 && (
        <div
          style={{
            fontFamily: "'SVN-Acta', 'SVN-FreightDisplay', serif",
            fontStyle: 'italic',
            fontWeight: 700,
            fontSize: '64px',
            lineHeight: 1.15,
            color: tier2Color,
            marginTop: '22px',
            maxWidth: '880px',
            textShadow:
              tier2Color === '#FFDE00'
                ? '0 0 30px rgba(255, 222, 0, 0.95), 0 0 60px rgba(255, 180, 0, 0.65), 0 8px 25px rgba(0, 0, 0, 0.98)'
                : '0 0 30px rgba(255, 255, 255, 0.95), 0 0 60px rgba(255, 220, 150, 0.7), 0 8px 25px rgba(0, 0, 0, 0.98)',
          }}
        >
          {tier2}
        </div>
      )}

      {hasArrow && (
        <div
          style={{
            marginTop: '40px',
            fontSize: '76px',
            color: '#FFDE00',
            filter: 'drop-shadow(0 0 35px rgba(255, 222, 0, 0.95))',
            transform: `translateY(${arrowBounce}px)`,
          }}
        >
          ↓
        </div>
      )}
    </AbsoluteFill>
  );
};
