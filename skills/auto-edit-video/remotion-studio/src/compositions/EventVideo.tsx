import React from 'react';
import {
  AbsoluteFill,
  OffthreadVideo,
  Sequence,
  staticFile,
  useVideoConfig,
  useCurrentFrame,
  spring,
  interpolate,
} from 'remotion';
import { EventVideoProps } from '../types';
import { SurpriseEffect } from '../components/SurpriseEffect';

/**
 * EventVideo — Composition cho catalog EVENT (sự kiện).
 * 
 * Hiệu ứng chính:
 * 1. Video gốc chạy full timeline liên tục (KHÔNG bị cắt)
 * 2. Subtitle bold uppercase với backdrop blur + gradient
 * 3. Flash transition trắng giữa các scene
 * 4. Subtle zoom pulse theo nhịp scene
 * 5. Bottom gradient cinematic
 * 6. Wow SurpriseEffect overlay
 */

const FlashTransition: React.FC<{ durationFrames: number }> = ({ durationFrames }) => {
  const frame = useCurrentFrame();
  // Flash trắng 6 frames (~0.2s) ở đầu scene
  const flashDuration = Math.min(6, durationFrames);
  const opacity = interpolate(frame, [0, flashDuration], [0.85, 0], {
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'white',
        opacity,
        pointerEvents: 'none',
        zIndex: 200,
      }}
    />
  );
};

const EventSubtitle: React.FC<{
  text: string;
  styleId: number;
  durationFrames: number;
}> = ({ text, styleId, durationFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Bảng màu luân phiên theo styleId
  const colorPalette = [
    { bg: 'rgba(0,0,0,0.75)', text: '#FFFFFF', accent: '#FFD700' },        // 1: Trắng trên đen
    { bg: 'rgba(255,69,0,0.85)', text: '#FFFFFF', accent: '#FFD700' },      // 2: Cam lửa
    { bg: 'rgba(0,0,139,0.85)', text: '#00FFFF', accent: '#00BFFF' },       // 3: Xanh điện
    { bg: 'rgba(139,0,139,0.85)', text: '#FFFFFF', accent: '#FF69B4' },     // 4: Tím neon
    { bg: 'rgba(0,100,0,0.85)', text: '#7CFC00', accent: '#00FF7F' },       // 5: Xanh lá neon
  ];
  const palette = colorPalette[(styleId - 1) % colorPalette.length];

  // Pop-in animation
  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 150, mass: 0.6 },
  });

  // Slide up from bottom
  const translateY = interpolate(frame, [0, 8], [40, 0], {
    extrapolateRight: 'clamp',
  });

  // Fade out cuối scene
  const fadeOut = interpolate(
    frame,
    [durationFrames - 8, durationFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        position: 'absolute',
        bottom: '18%',
        width: '100%',
        display: 'flex',
        justifyContent: 'center',
        zIndex: 50,
        transform: `translateY(${translateY}px) scale(${Math.min(scale, 1)})`,
        opacity: fadeOut,
      }}
    >
      <div
        style={{
          backgroundColor: palette.bg,
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          borderRadius: '8px',
          padding: '14px 28px',
          maxWidth: '90%',
          border: `2px solid ${palette.accent}40`,
          boxShadow: `0 4px 20px rgba(0,0,0,0.5), 0 0 30px ${palette.accent}30`,
        }}
      >
        <div
          style={{
            fontFamily: "'SVN-Acta', 'GT America', 'Be Vietnam Pro', sans-serif",
            fontSize: '42px',
            fontWeight: 900,
            color: palette.text,
            textTransform: 'uppercase',
            letterSpacing: '1.5px',
            textAlign: 'center',
            textShadow: `0 2px 8px rgba(0,0,0,0.6), 0 0 20px ${palette.accent}50`,
            lineHeight: 1.3,
          }}
        >
          {text}
        </div>
      </div>
    </div>
  );
};

export const EventVideo: React.FC<EventVideoProps> = ({
  videoSrc,
  scenes = [],
  filter,
}) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  const filterStyle = `brightness(${filter?.brightness ?? 1.05}) contrast(${filter?.contrast ?? 1.08}) saturate(${filter?.saturate ?? 1.15})`;

  // Subtle zoom pulse — nhịp thở nhẹ cho toàn video
  const breathScale = interpolate(
    frame % (fps * 4),
    [0, fps * 2, fps * 4],
    [1.0, 1.03, 1.0]
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* VIDEO GỐC — chạy liên tục full timeline, không wrap trong Sequence */}
      <AbsoluteFill
        style={{
          transform: `scale(${breathScale})`,
          transformOrigin: 'center center',
        }}
      >
        <OffthreadVideo
          src={staticFile(videoSrc)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: filterStyle,
          }}
        />
      </AbsoluteFill>

      {/* CINEMATIC GRADIENT — top & bottom */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0) 20%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.5) 100%)',
          pointerEvents: 'none',
          zIndex: 10,
        }}
      />

      {/* SCENE OVERLAYS — subtitles, flash, wow effects */}
      {scenes.map((scene) => {
        const startFrame = Math.round(scene.start * fps);
        const endFrame = Math.round(scene.end * fps);
        const duration = Math.max(1, endFrame - startFrame);

        return (
          <Sequence
            key={`event-${scene.scene}`}
            from={startFrame}
            durationInFrames={duration}
          >
            {/* Flash transition trắng ở đầu scene (trừ scene 1) */}
            {scene.flashTransition && scene.scene > 1 && (
              <FlashTransition durationFrames={duration} />
            )}

            {/* Subtitle nếu có */}
            {scene.subtitles && scene.subtitles.text && (
              <EventSubtitle
                text={scene.subtitles.text}
                styleId={scene.subtitles.styleId || 1}
                durationFrames={duration}
              />
            )}

            {/* Wow Effect */}
            {scene.wowEffect?.enabled && scene.wowEffect.presetId && (
              <SurpriseEffect
                effectType={scene.wowEffect.presetId as any}
                startFrame={0}
                durationFrames={duration}
                intensity={0.8}
              />
            )}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
