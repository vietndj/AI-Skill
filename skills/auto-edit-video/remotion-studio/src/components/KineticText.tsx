import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate, AbsoluteFill } from 'remotion';
import type { TypographyStyle } from '../data/styles';

export interface KineticTextProps {
  line1: string;
  line2: string;
  style: TypographyStyle;
  size1: number;
  size2: number;
  posY: number;
  motionType: 1 | 2 | 3 | 4;
  shadowOp: number;
  glowInt: number;
  enterFrame: number;
}

export const KineticText: React.FC<KineticTextProps> = ({
  line1,
  line2,
  style,
  size1,
  size2,
  posY,
  motionType,
  shadowOp,
  glowInt,
  enterFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Local frame relative to enterFrame
  const localFrame = Math.max(0, frame - enterFrame);

  if (frame < enterFrame) {
    return null;
  }

  // --- Common Shadow/Glow System ---
  const glow = glowInt / 100;
  const shadowOpacity = shadowOp / 100;
  const glowColor = style.glow || '255, 255, 255';
  
  const textShadow1 = glow > 0 
    ? `0 0 ${20*glow}px rgba(${glowColor}, ${0.85*glow}), 0 0 ${45*glow}px rgba(${glowColor}, ${0.5*glow}), 0 4px 8px rgba(0,0,0,0.9)`
    : `0 4px 8px rgba(0,0,0,0.9)`;
    
  const filter1 = shadowOpacity > 0 ? `drop-shadow(0 4px 10px rgba(0,0,0,${shadowOpacity}))` : undefined;

  const textShadow2 = shadowOpacity > 0
    ? `0 2px 4px rgba(0,0,0,${shadowOpacity}), 0 4px 10px rgba(0,0,0,${shadowOpacity})`
    : undefined;

  // --- Motion Values ---
  let l1Y = 0;
  let l1Scale = 1;
  let l1Blur = 0;
  let l1Opacity = 1;
  let l1LetterSpacing = 0;

  let l2Y = 0;
  let l2Scale = 1;
  let l2Blur = 0;
  let l2Opacity = 1;
  
  let globalScale = 1;
  let globalBlur = 0;
  let globalBrightness = 1;

  if (motionType === 1) {
    // Blur & Glow Pop
    const s1 = spring({ frame: localFrame, fps, config: { damping: 12 } });
    const s2 = spring({ frame: Math.max(0, localFrame - 8), fps, config: { damping: 12 } });

    l1Y = interpolate(s1, [0, 1], [22, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Scale = interpolate(s1, [0, 1], [0.88, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Blur = interpolate(s1, [0, 1], [14, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Opacity = interpolate(s1, [0, 0.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

    l2Y = interpolate(s2, [0, 1], [28, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l2Scale = interpolate(s2, [0, 1], [0.88, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l2Blur = interpolate(s2, [0, 1], [14, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l2Opacity = interpolate(s2, [0, 0.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  } else if (motionType === 2) {
    // Elastic Whip
    const s1 = spring({ frame: localFrame, fps, config: { damping: 8, stiffness: 100 } });
    const s2 = spring({ frame: Math.max(0, localFrame - 8), fps, config: { damping: 8, stiffness: 100 } });

    l1Y = interpolate(s1, [0, 1], [-20, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Scale = interpolate(s1, [0, 1], [0.78, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Opacity = interpolate(s1, [0, 0.2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

    l2Y = interpolate(s2, [0, 1], [35, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l2Opacity = interpolate(s2, [0, 0.2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  } else if (motionType === 3) {
    // Float & Drift
    l1Y = interpolate(localFrame, [0, 20], [16, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Opacity = interpolate(localFrame, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1LetterSpacing = interpolate(localFrame, [0, 30], [-0.04, -0.01], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l1Scale = interpolate(localFrame, [0, 50], [1, 1.025], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

    l2Y = interpolate(localFrame, [10, 30], [16, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l2Opacity = interpolate(localFrame, [10, 25], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  } else if (motionType === 4) {
    // Zoom Explosion
    const s1 = spring({ frame: localFrame, fps, config: { damping: 14 } });
    globalScale = interpolate(s1, [0, 1], [1.6, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    globalBlur = interpolate(localFrame, [0, 10], [18, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    globalBrightness = interpolate(localFrame, [0, 10], [2.5, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    
    l1Opacity = interpolate(localFrame, [0, 5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    l2Opacity = interpolate(localFrame, [0, 5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  }

  // --- Special Elements Animations ---
  // Strike Laser
  const strikeSpring = spring({ frame: Math.max(0, localFrame - 10), fps, config: { damping: 14 } });
  const strikeWidth = interpolate(strikeSpring, [0, 1], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Star Sparkle
  const starSpring = spring({ frame: Math.max(0, localFrame - 10), fps, config: { damping: 12 } });
  const starScale = interpolate(starSpring, [0, 1], [0, 1.2], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const starRotation = interpolate(starSpring, [0, 1], [-90, 45], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Circle Ring
  const circleSpring = spring({ frame: Math.max(0, localFrame - 5), fps, config: { damping: 12 } });
  const circleScale = interpolate(circleSpring, [0, 1], [0.8, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const circleOpacity = interpolate(circleSpring, [0, 1], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', paddingBottom: posY }}>
      <div 
        style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center',
          transform: `scale(${globalScale})`,
          filter: `blur(${globalBlur}px) brightness(${globalBrightness})`,
        }}
      >
        <div 
          style={{ 
            position: 'relative',
            opacity: l1Opacity,
            transform: `translateY(${l1Y}px) scale(${l1Scale})`,
            filter: `blur(${l1Blur}px) ${filter1 || ''}`.trim(),
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {style.isCircle && (
            <div 
              style={{
                position: 'absolute',
                width: '120%',
                height: '140%',
                border: '2.5px solid white',
                borderRadius: '50%',
                boxShadow: '0 0 10px rgba(255,255,255,0.8), inset 0 0 10px rgba(255,255,255,0.8)',
                transform: `scale(${circleScale})`,
                opacity: circleOpacity,
              }}
            />
          )}

          <div
            style={{
              fontFamily: style.f1,
              fontWeight: style.f1Weight,
              fontStyle: style.f1Style,
              color: style.c1,
              fontSize: size1,
              textShadow: textShadow1,
              letterSpacing: motionType === 3 ? `${l1LetterSpacing}em` : 'normal',
              textAlign: 'center',
              ...(style.isPill ? {
                border: '2px solid #00E5FF',
                borderRadius: '999px',
                padding: '9px 22px',
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                backdropFilter: 'blur(10px)',
              } : {})
            }}
          >
            {line1}
          </div>

          {style.isStrike && (
            <div 
              style={{
                position: 'absolute',
                height: '4px',
                width: `${strikeWidth}%`,
                backgroundColor: '#FF2E2E',
                boxShadow: '0 0 8px #FF2E2E, 0 0 16px #FF2E2E',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
              }}
            />
          )}

          {style.isStar && (
            <div
              style={{
                position: 'absolute',
                right: '-20px',
                top: '-10px',
                color: 'white',
                fontSize: size1 * 0.5,
                transform: `scale(${starScale}) rotate(${starRotation}deg)`,
                textShadow: '0 0 10px rgba(255,255,255,0.8)',
              }}
            >
              ✦
            </div>
          )}
        </div>

        {style.mid && (
          <div
            style={{
              fontFamily: style.fmid || style.f2,
              fontWeight: style.fmidWeight || style.f2Weight,
              fontSize: style.smid || (size2 * 0.8),
              color: style.c2,
              textAlign: 'center',
              marginTop: -(style.ov || 0) * 0.5,
              zIndex: 2,
              opacity: l2Opacity,
            }}
          >
            {style.mid}
          </div>
        )}

        <div
          style={{
            fontFamily: style.f2,
            fontWeight: style.f2Weight,
            fontStyle: style.f2Style,
            color: style.c2,
            fontSize: size2,
            textShadow: textShadow2,
            marginTop: -(style.ov || 0),
            opacity: l2Opacity,
            transform: `translateY(${l2Y}px) scale(${l2Scale})`,
            filter: `blur(${l2Blur}px)`,
            textAlign: 'center',
            zIndex: 1,
          }}
        >
          {line2}
        </div>
      </div>
    </AbsoluteFill>
  );
};
