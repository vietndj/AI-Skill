import React from 'react';
import { useCurrentFrame } from 'remotion';

export const TypewriterText: React.FC<{
  text: string;
  fontSize?: number;
  fontFamily?: string;
  color?: string;
  startFrame?: number;
  speed?: number; // chars per frame
}> = ({ text, fontSize = 48, fontFamily = 'sans-serif', color = '#fff', startFrame = 0, speed = 0.5 }) => {
  const frame = useCurrentFrame();
  const relFrame = Math.max(0, frame - startFrame);
  
  const chars = [...text];
  const visibleCharsCount = Math.floor(relFrame * speed);
  const visibleText = chars.slice(0, visibleCharsCount).join('');
  const isComplete = visibleCharsCount >= chars.length;
  
  const showCursor = !isComplete || Math.floor(frame / 15) % 2 === 0;

  return (
    <div style={{
      fontFamily,
      fontSize: `${fontSize}px`,
      color,
      whiteSpace: 'pre-wrap',
      textShadow: '0 2px 8px rgba(0,0,0,0.5)',
      textAlign: 'center'
    }}>
      {visibleText}
      <span style={{ opacity: showCursor ? 1 : 0 }}>|</span>
    </div>
  );
};
