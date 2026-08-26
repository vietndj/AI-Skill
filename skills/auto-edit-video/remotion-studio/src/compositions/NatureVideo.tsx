import React from 'react';
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig } from 'remotion';
import { NatureVideoProps } from '../types';
import { KenBurnsEffect } from '../components/KenBurnsEffect';
import { TypewriterText } from '../components/TypewriterText';
import { ParallaxText } from '../components/ParallaxText';
import { SurpriseEffect } from '../components/SurpriseEffect';
import { findNatureStyleById } from '../data/nature_styles';

export const NatureVideo: React.FC<NatureVideoProps> = ({ videoSrc, scenes = [], filter }) => {
  const { fps } = useVideoConfig();
  const filterStyle = `brightness(${filter?.brightness ?? 1.0}) contrast(${filter?.contrast ?? 1.0}) saturate(${filter?.saturate ?? 0.95})`;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <KenBurnsEffect durationFrames={Math.round((scenes.length ? scenes[scenes.length-1].end : 10) * fps)} scale={1.08} direction="zoom_in">
        <OffthreadVideo src={staticFile(videoSrc)} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: filterStyle }} />
      </KenBurnsEffect>

      {scenes.map(scene => {
        const startFrame = Math.round(scene.start * fps);
        const endFrame = Math.round(scene.end * fps);
        const duration = Math.max(1, endFrame - startFrame);
        const style = scene.text ? findNatureStyleById(scene.text.styleId) : null;

        return (
          <Sequence key={`nature-scene-${scene.scene}`} from={startFrame} durationInFrames={duration}>
            {scene.text && scene.text.type === 'typewriter' && (
              <div style={{ position: 'absolute', top: `${scene.text.posY ?? 80}%`, width: '100%', display: 'flex', justifyContent: 'center' }}>
                <TypewriterText text={scene.text.content} fontFamily={style?.fontFamily} color={style?.textColor} fontSize={scene.text.fontSize ?? 40} />
              </div>
            )}
            {scene.text && scene.text.type === 'parallax' && (
              <div style={{ position: 'absolute', top: `${scene.text.posY ?? 80}%`, width: '100%', display: 'flex', justifyContent: 'center' }}>
                <ParallaxText text={scene.text.content} fontFamily={style?.fontFamily} color={style?.textColor} fontSize={scene.text.fontSize ?? 40} durationFrames={duration} />
              </div>
            )}
            {scene.wowEffect?.enabled && scene.wowEffect.presetId && (
              <SurpriseEffect effectType={scene.wowEffect.presetId as any} startFrame={0} durationFrames={duration} intensity={scene.wowEffect.intensity} />
            )}
          </Sequence>
        );
      })}
      
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 15%, rgba(0,0,0,0) 85%, rgba(0,0,0,0.4) 100%)', pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
