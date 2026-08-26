import React from 'react';
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig } from 'remotion';
import { AutoEditProps } from '../types';
import { FullscreenTextCard } from '../components/FullscreenTextCard';
import { ConfettiOverlay } from '../components/ConfettiOverlay';
import { BrandTag } from '../components/BrandTag';
import { KineticText } from '../components/KineticText';
import { STYLES_DB } from '../data/styles';

function findStyleById(id: number) {
  return STYLES_DB.find((s) => s.id === id) || STYLES_DB[0];
}

export const AutoEditVideo: React.FC<AutoEditProps> = ({ videoSrc, scenes = [], brand }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      {/* Layer 1: Main speaker video footage */}
      <OffthreadVideo
        src={staticFile(videoSrc)}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />

      {/* Layer 2: Fullscreen Interstitial Cards / Lower-Thirds */}
      {scenes.map((scene) => {
        const startFrame = Math.round(scene.start * fps);
        const endFrame = Math.round(scene.end * fps);
        const durationFrames = Math.max(1, endFrame - startFrame);

        // 1. FULLSCREEN INTERSTITIAL TEXT CARD (MÀN HÌNH ĐEN CHỮ TO ĐÙNG Ở GIỮA)
        const isFullscreen =
          scene.type === 'hook' ||
          scene.type === 'insight' ||
          scene.type === 'cta' ||
          (scene as any).type === 'fullscreen';

        if (isFullscreen) {
          const theme =
            scene.type === 'insight' ? 'gold' : scene.type === 'cta' ? 'outro' : 'dark';
          const hasArrow = scene.type === 'cta';
          const hasConfetti = (scene as any).hasConfetti || scene.type === 'insight' || scene.type === 'cta';

          return (
            <Sequence
              key={`fs-scene-${scene.scene}`}
              from={startFrame}
              durationInFrames={durationFrames}
            >
              <FullscreenTextCard
                badge={(scene as any).badge}
                tier1={scene.typography?.line1 || ''}
                tier2={scene.typography?.line2 || ''}
                tier1Color={(scene as any).tier1Color || '#FFDE00'}
                tier2Color={(scene as any).tier2Color || '#FFFFFF'}
                theme={theme}
                durationInFrames={durationFrames}
                hasArrow={hasArrow}
              />
              {hasConfetti && (
                <ConfettiOverlay
                  startFrame={0}
                  durationFrames={durationFrames}
                  theme={scene.type === 'cta' ? 'celebration' : 'gold'}
                />
              )}
            </Sequence>
          );
        }

        // 2. LOWER-THIRD OVERLAY (Only if explicitly type === 'lower')
        if (scene.type === 'lower' && scene.typography) {
          return (
            <Sequence
              key={`lower-scene-${scene.scene}`}
              from={startFrame}
              durationInFrames={durationFrames}
            >
              <KineticText
                line1={scene.typography.line1}
                line2={scene.typography.line2}
                style={findStyleById(parseInt(String(scene.typography.style_id || 1)))}
                size1={scene.typography.size1 || 84}
                size2={scene.typography.size2 || 60}
                posY={scene.typography.posY || 340}
                motionType={scene.typography.motion || 1}
                shadowOp={scene.typography.shadowOp || 80}
                glowInt={scene.typography.glowInt || 60}
                enterFrame={0}
              />
            </Sequence>
          );
        }

        // Otherwise: Speaker video plays CLEAN with NO text overlay!
        return null;
      })}

      {/* Layer 3: Top Brand Tag Header */}
      <BrandTag left={brand?.left} center={brand?.center} right={brand?.right} />
    </AbsoluteFill>
  );
};
