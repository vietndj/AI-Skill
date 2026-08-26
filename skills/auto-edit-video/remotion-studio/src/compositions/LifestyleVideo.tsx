import React from 'react';
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig } from 'remotion';
import { LifestyleVideoProps } from '../types';
import { PunchZoom } from '../components/PunchZoom';
import { LifestyleSubtitles } from '../components/LifestyleSubtitles';
import { FloatingEmojis } from '../components/FloatingEmojis';
import { LifestyleBrandTag } from '../components/LifestyleBrandTag';

export const LifestyleVideo: React.FC<LifestyleVideoProps> = ({
  videoSrc,
  scenes = [],
  filter = {
    brightness: 1.04,
    contrast: 1.03,
    saturate: 1.12,
  },
  headerTag = {
    enabled: true,
    badgeText: '✨ Daily Moments',
  },
}) => {
  const { fps } = useVideoConfig();

  const filterStyle = `brightness(${filter.brightness ?? 1.04}) contrast(${filter.contrast ?? 1.03}) saturate(${filter.saturate ?? 1.12})`;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      {/* Background Video Layer with Dynamic Punch-Zoom per scene */}
      <PunchZoom scenes={scenes}>
        <OffthreadVideo
          src={staticFile(videoSrc)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: filterStyle,
          }}
        />
      </PunchZoom>

      {/* Overlay layers per scene */}
      {scenes.map((scene) => {
        const startFrame = Math.round(scene.start * fps);
        const endFrame = Math.round(scene.end * fps);
        const durationFrames = Math.max(1, endFrame - startFrame);

        return (
          <Sequence
            key={`scene-seq-${scene.scene}`}
            from={startFrame}
            durationInFrames={durationFrames}
          >
            {/* Floating Emojis Overlay */}
            {scene.floatingEmoji && scene.floatingEmoji.emojis.length > 0 && (
              <FloatingEmojis
                emojis={scene.floatingEmoji.emojis}
                position={scene.floatingEmoji.position || 'top-right'}
                motion={scene.floatingEmoji.motion || 'float_up'}
                enterFrame={0}
                durationFrames={durationFrames}
              />
            )}

            {/* Cute / Rounded Subtitles Overlay */}
            {scene.subtitles && (
              <LifestyleSubtitles
                line1={scene.subtitles.line1}
                line2={scene.subtitles.line2}
                styleId={scene.subtitles.styleId || 1}
                fontSize1={scene.subtitles.fontSize1 || 44}
                fontSize2={scene.subtitles.fontSize2 || 32}
                posY={scene.subtitles.posY || 78}
                motion={scene.subtitles.motion || 'bounce'}
                enterFrame={0}
              />
            )}
          </Sequence>
        );
      })}

      {/* Subtle Warm Tone Gradient for Natural Glow (Top & Bottom subtle contrast) */}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0) 25%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.3) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* Header Tag / Vlog Badge */}
      <LifestyleBrandTag
        enabled={headerTag?.enabled ?? true}
        badgeText={headerTag?.badgeText || '✨ Daily Moments'}
        timeText={headerTag?.timeText}
        locationText={headerTag?.locationText}
      />
    </AbsoluteFill>
  );
};
