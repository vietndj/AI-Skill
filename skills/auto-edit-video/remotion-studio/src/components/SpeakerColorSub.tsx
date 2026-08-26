import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

const SPEAKER_COLORS = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF'];

export const SpeakerColorSub: React.FC<{
  text: string;
  speakerId?: number;
  fontSize?: number;
  posY?: number;
  enterFrame?: number;
}> = ({ text, speakerId = 0, fontSize = 44, posY = 78, enterFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const color = SPEAKER_COLORS[speakerId % SPEAKER_COLORS.length];

  const relFrame = Math.max(0, frame - enterFrame);
  const spr = spring({
    frame: relFrame,
    fps,
    config: { damping: 12, stiffness: 160 }
  });
  
  const opacity = interpolate(spr, [0, 1], [0, 1]);
  const translateY = interpolate(spr, [0, 1], [20, 0]);

  const hex = color.replace('#', '');
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  const bgColor = `rgba(${r}, ${g}, ${b}, 0.2)`;

  return (
    <div style={{
      position: 'absolute',
      top: `${posY}%`,
      width: '100%',
      display: 'flex',
      justifyContent: 'center',
      pointerEvents: 'none',
      zIndex: 40
    }}>
      <div style={{
        fontFamily: "'Nunito', sans-serif",
        fontSize: `${fontSize}px`,
        fontWeight: 800,
        color: '#fff',
        backgroundColor: bgColor,
        padding: '12px 32px',
        borderRadius: '36px',
        border: `2px solid ${color}`,
        transform: `translateY(${translateY}px)`,
        opacity,
        textAlign: 'center',
        textShadow: '0 2px 4px rgba(0,0,0,0.5)'
      }}>
        {text}
      </div>
    </div>
  );
};
