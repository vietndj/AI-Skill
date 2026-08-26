import React from 'react';
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig } from 'remotion';
import { LiveTalkVideoProps } from '../types';
import { SpeakerColorSub } from '../components/SpeakerColorSub';
import { PullQuoteCard } from '../components/PullQuoteCard';
import { SurpriseEffect } from '../components/SurpriseEffect';

export const LiveTalkVideo: React.FC<LiveTalkVideoProps> = ({ videoSrc, scenes = [] }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <OffthreadVideo src={staticFile(videoSrc)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />

      {scenes.map(scene => {
        const startFrame = Math.round(scene.start * fps);
        const endFrame = Math.round(scene.end * fps);
        const duration = Math.max(1, endFrame - startFrame);

        return (
          <Sequence key={`livetalk-scene-${scene.scene}`} from={startFrame} durationInFrames={duration}>
            {scene.subtitles && (
              <SpeakerColorSub text={scene.subtitles.text} speakerId={scene.subtitles.speakerId} />
            )}
            {scene.pullQuote?.enabled && (
              <PullQuoteCard quote={scene.pullQuote.quote} speaker={scene.pullQuote.speaker} durationFrames={duration} />
            )}
            {scene.wowEffect?.enabled && scene.wowEffect.presetId && (
              <SurpriseEffect effectType={scene.wowEffect.presetId as any} startFrame={0} durationFrames={duration} />
            )}
          </Sequence>
        );
      })}
      
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.6) 100%)', pointerEvents: 'none', zIndex: 10 }} />
    </AbsoluteFill>
  );
};
