import React from 'react';
import { AbsoluteFill, Img, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export interface ImageOverlayProps {
  imageSrc: string;
  presetId: string;
  scale: number;
  position: string;
  motionType: number;
  enterFrame: number;
  durationFrames: number;
}

export const ImageOverlay: React.FC<ImageOverlayProps> = ({
  imageSrc,
  presetId,
  scale,
  position,
  motionType,
  enterFrame,
  durationFrames
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - enterFrame;

  if (localFrame < 0 || localFrame >= durationFrames) return null;

  // Motions
  const popSpring = spring({ frame: localFrame, fps, config: { damping: 10, mass: 1, stiffness: 100 } });
  const slideSpring = spring({ frame: localFrame, fps, config: { damping: 14, mass: 1, stiffness: 80 } });
  const fadeInterp = interpolate(localFrame, [0, 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const blurInterp = interpolate(localFrame, [0, 10], [12, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const scaleBlurInterp = interpolate(localFrame, [0, 10], [1.4, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  
  const flicker = localFrame < 5 ? (localFrame % 2 === 0 ? 0.3 : 0.8) : 1; // Deterministic flicker

  let style: React.CSSProperties = {
    position: 'absolute',
    width: '140px',
    height: '140px',
    objectFit: 'cover'
  };

  let containerStyle: React.CSSProperties = {
    position: 'absolute',
    transform: `scale(${scale / 100})`,
    transformOrigin: 'center'
  };

  // Preset Layouts
  switch (presetId) {
    case 'IMG-01':
    case 'IMG-07':
      style = { ...style, borderRadius: '12px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' };
      break;
    case 'IMG-02':
      style = { position: 'absolute', width: '100%', height: '50%', top: 0, left: 0, objectFit: 'cover', borderBottomLeftRadius: '16px', borderBottomRightRadius: '16px' };
      containerStyle = { ...containerStyle, width: '100%', height: '100%' };
      break;
    case 'IMG-03':
      style = { position: 'absolute', width: '100%', height: '100%', top: 0, left: 0, objectFit: 'cover' };
      containerStyle = { ...containerStyle, width: '100%', height: '100%' };
      break;
    case 'IMG-04':
      style = { ...style, border: '6px solid white', transform: 'rotate(-4deg)', boxShadow: '0 4px 15px rgba(0,0,0,0.3)' };
      break;
    case 'IMG-05':
      style = { ...style, borderRadius: '32px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)', width: '200px', height: '400px' };
      break;
    case 'IMG-06':
      style = { ...style, width: '80%', aspectRatio: '16/9', height: 'auto', boxShadow: '0 20px 40px rgba(0,0,0,0.6)' };
      break;
    case 'IMG-08':
      style = { ...style, borderRadius: '50%', border: '4px solid gold', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' };
      break;
  }

  // Positioning
  if (['IMG-01', 'IMG-04', 'IMG-05', 'IMG-07', 'IMG-08'].includes(presetId)) {
    if (position === 'tr') {
      containerStyle.top = '10%';
      containerStyle.right = '5%';
    } else if (position === 'tl') {
      containerStyle.top = '10%';
      containerStyle.left = '5%';
    } else if (position === 'center') {
      containerStyle.top = '50%';
      containerStyle.left = '50%';
      containerStyle.transform = `translate(-50%, -50%) scale(${scale / 100})`;
    } else if (position === 'half') {
      containerStyle.top = '25%';
      containerStyle.left = '50%';
      containerStyle.transform = `translate(-50%, -50%) scale(${scale / 100})`;
    }
  } else if (presetId === 'IMG-06') {
    containerStyle.top = '50%';
    containerStyle.left = '50%';
    containerStyle.transform = `translate(-50%, -50%) scale(${scale / 100})`;
  }

  // Motion Types
  switch (motionType) {
    case 1: // 3D Pop
      const scalePop = interpolate(popSpring, [0, 1], [0.5, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      const rotY = interpolate(popSpring, [0, 1], [30, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      containerStyle.transform = (containerStyle.transform || '') + ` scale(${scalePop}) perspective(1000px) rotateY(${rotY}deg)`;
      break;
    case 2: // Slide Drift
      const transX = interpolate(slideSpring, [0, 1], [-200, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      containerStyle.transform = (containerStyle.transform || '') + ` translateX(${transX}px)`;
      break;
    case 3: // Zoom Blur
      containerStyle.transform = (containerStyle.transform || '') + ` scale(${scaleBlurInterp})`;
      containerStyle.filter = `blur(${blurInterp}px)`;
      break;
    case 4: // Polaroid
      const transY = interpolate(slideSpring, [0, 1], [-200, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      const rot = interpolate(slideSpring, [0, 1], [-10, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      containerStyle.transform = (containerStyle.transform || '') + ` translateY(${transY}px) rotate(${rot}deg)`;
      break;
    case 5: // Hologram
      containerStyle.opacity = flicker;
      break;
    case 6: // Fade In
      containerStyle.opacity = fadeInterp;
      break;
  }

  return (
    <AbsoluteFill>
      <div style={containerStyle}>
        <Img src={imageSrc} style={style} />
      </div>
    </AbsoluteFill>
  );
};
