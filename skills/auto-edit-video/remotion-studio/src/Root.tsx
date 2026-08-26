import { CalculateMetadataFunction, Composition } from 'remotion';
import './index.css';
import './load-fonts'; // Module-scope font loading (must be before any component)
import { AutoEditVideo } from './compositions/AutoEditVideo';
import { LifestyleVideo } from './compositions/LifestyleVideo';
import { NatureVideo } from './compositions/NatureVideo';
import { EventVideo } from './compositions/EventVideo';
import { LiveTalkVideo } from './compositions/LiveTalkVideo';
import type { AutoEditProps, LifestyleVideoProps, NatureVideoProps, EventVideoProps, LiveTalkVideoProps } from './types';

const defaultProps: AutoEditProps = {
  videoSrc: 'test.mp4',
  scenes: [
    {
      scene: 1, type: 'hook', start: 0, end: 3,
      typography: { style_id: '06', line1: 'EDIT = AI', line2: 'Nhàn lắm sao?', size1: 56, size2: 44, posY: 260, motion: 1, shadowOp: 45, glowInt: 65 },
      visual: { type: 'none' }
    }
  ],
  brand: { left: 'Viral Video COURSE', center: '↗ 0934.68.86.32', right: '2026' }
};

const defaultLifestyleProps: LifestyleVideoProps = {
  videoSrc: 'test.mp4',
  preset: 'fun',
  scenes: [
    {
      scene: 1,
      start: 0,
      end: 4,
      subtitles: {
        line1: 'Trông xinh gái đấy nhỉ? ✨',
        styleId: 1,
        fontSize1: 44,
        posY: 78,
        motion: 'bounce',
      },
      punchZoom: {
        enabled: true,
        scale: 1.18,
      },
      floatingEmoji: {
        emojis: ['😂', '✨'],
        position: 'top-right',
      }
    }
  ],
  filter: {
    brightness: 1.04,
    contrast: 1.03,
    saturate: 1.12,
  },
  headerTag: {
    enabled: true,
    badgeText: '✨ Daily Moments',
  }
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateAutoEditMetadata: CalculateMetadataFunction<any> = async ({ props }) => {
  const fps = 30;
  if (!props.scenes || props.scenes.length === 0) {
    return { durationInFrames: 300, fps, width: 1080, height: 1920 };
  }
  const maxEnd = Math.max(...props.scenes.map((s: any) => s.end));
  const durationInFrames = Math.max(30, Math.ceil((maxEnd + 0.5) * fps));
  return { durationInFrames, fps, width: 1080, height: 1920 };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateLifestyleMetadata: CalculateMetadataFunction<any> = async ({ props }) => {
  const fps = 30;
  if (!props.scenes || props.scenes.length === 0) {
    return { durationInFrames: 300, fps, width: 1080, height: 1920 };
  }
  const maxEnd = Math.max(...props.scenes.map((s: any) => s.end));
  const durationInFrames = Math.max(30, Math.ceil((maxEnd + 0.5) * fps));
  return { durationInFrames, fps, width: 1080, height: 1920 };
};

const defaultNatureProps: NatureVideoProps = {
  videoSrc: 'test.mp4',
  scenes: [
    { scene: 1, start: 0, end: 5, text: { content: 'Misty morning vibes...', type: 'typewriter', styleId: 5, posY: 80 } }
  ]
};

const defaultEventProps: EventVideoProps = {
  videoSrc: 'test.mp4',
  scenes: [
    { scene: 1, start: 0, end: 4, subtitles: { text: 'GET READY!', styleId: 1 }, flashTransition: true }
  ]
};

const defaultLiveTalkProps: LiveTalkVideoProps = {
  videoSrc: 'test.mp4',
  scenes: [
    { scene: 1, start: 0, end: 6, subtitles: { text: 'The secret is out.', speakerId: 0 } }
  ]
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateNatureMetadata: CalculateMetadataFunction<any> = async ({ props }) => {
  const fps = 30;
  if (!props.scenes || props.scenes.length === 0) return { durationInFrames: 300, fps, width: 1080, height: 1920 };
  const maxEnd = Math.max(...props.scenes.map((s: any) => s.end));
  return { durationInFrames: Math.max(30, Math.ceil((maxEnd + 0.5) * fps)), fps, width: 1080, height: 1920 };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateEventMetadata: CalculateMetadataFunction<any> = async ({ props }) => {
  const fps = 30;
  if (!props.scenes || props.scenes.length === 0) return { durationInFrames: 300, fps, width: 1080, height: 1920 };
  const maxEnd = Math.max(...props.scenes.map((s: any) => s.end));
  return { durationInFrames: Math.max(30, Math.ceil((maxEnd + 0.5) * fps)), fps, width: 1080, height: 1920 };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateLiveTalkMetadata: CalculateMetadataFunction<any> = async ({ props }) => {
  const fps = 30;
  if (!props.scenes || props.scenes.length === 0) return { durationInFrames: 300, fps, width: 1080, height: 1920 };
  const maxEnd = Math.max(...props.scenes.map((s: any) => s.end));
  return { durationInFrames: Math.max(30, Math.ceil((maxEnd + 0.5) * fps)), fps, width: 1080, height: 1920 };
};

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="AutoEditVideo"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        component={AutoEditVideo as any}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={calculateAutoEditMetadata as any}
        defaultProps={defaultProps as unknown as Record<string, unknown>}
      />
      <Composition
        id="LifestyleVideo"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        component={LifestyleVideo as any}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={calculateLifestyleMetadata as any}
        defaultProps={defaultLifestyleProps as unknown as Record<string, unknown>}
      />
      <Composition
        id="NatureVideo"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        component={NatureVideo as any}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={calculateNatureMetadata as any}
        defaultProps={defaultNatureProps as unknown as Record<string, unknown>}
      />
      <Composition
        id="EventVideo"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        component={EventVideo as any}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={calculateEventMetadata as any}
        defaultProps={defaultEventProps as unknown as Record<string, unknown>}
      />
      <Composition
        id="LiveTalkVideo"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        component={LiveTalkVideo as any}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={calculateLiveTalkMetadata as any}
        defaultProps={defaultLiveTalkProps as unknown as Record<string, unknown>}
      />
    </>
  );
};
