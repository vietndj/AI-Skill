export interface VideoConfig {
  fps: number;
  width: number;
  height: number;
}

export const VIDEO_DEFAULTS: VideoConfig = {
  fps: 30,
  width: 1080,
  height: 1920, // 9:16 vertical
};

export interface SceneConfig {
  scene: number;
  type: 'hook' | 'insight' | 'cta' | 'lower';
  start: number;  // seconds
  end: number;     // seconds
  typography: {
    style_id: string; // '01' to '35'
    line1: string;
    line2: string;
    size1: number;
    size2: number;
    posY: number;
    motion: 1 | 2 | 3 | 4;
    shadowOp: number;
    glowInt: number;
  };
  visual: {
    type: 'image' | 'broll' | 'none';
    preset?: string;
    scale?: number;
    position?: string;
    motion?: number;
    file?: string;
    insert?: string;
    trim?: string;
  };
  srt_text?: string;
}

export interface AutoEditProps {
  videoSrc: string;
  scenes: SceneConfig[];
  brand: {
    left: string;
    center: string;
    right: string;
  };
}

export interface LifestyleSceneConfig {
  scene: number;
  start: number; // seconds
  end: number;   // seconds
  subtitles: {
    line1: string;
    line2?: string;
    styleId: number | string; // 1 to 10
    fontSize1?: number;
    fontSize2?: number;
    posY?: number; // percentage from top, default 78
    motion?: 'pop' | 'bounce' | 'slide_up' | 'fade';
    highlightWords?: string[];
  };
  punchZoom?: {
    enabled: boolean;
    scale?: number; // e.g. 1.18
    originX?: number; // default 50
    originY?: number; // default 38
  };
  floatingEmoji?: {
    emojis: string[]; // e.g. ['😂', '✨']
    position?: 'top-right' | 'top-left' | 'center-right' | 'center-left' | 'bottom-right';
    motion?: 'float_up' | 'bounce' | 'pulse';
  };
  tag?: {
    show?: boolean;
    text?: string;
    time?: string;
  };
}

export interface LifestyleVideoProps {
  videoSrc: string;
  preset?: 'fun' | 'cozy' | 'dynamic' | 'cute';
  scenes: LifestyleSceneConfig[];
  filter?: {
    brightness?: number; // default 1.05
    contrast?: number;   // default 1.05
    saturate?: number;   // default 1.12
    warmth?: number;     // default 1.03
  };
  headerTag?: {
    enabled: boolean;
    badgeText?: string;
    timeText?: string;
    locationText?: string;
  };
}

export type UGCCatalog = 'DAILY_LIFE' | 'NATURE_AMBIENT' | 'EVENT' | 'LIVE_TALK';

export interface WowPreset {
  id: string;
  name: string;
  catalog: UGCCatalog;
  effectType: 'emoji_burst' | 'freeze_zoom' | 'color_flash' | 'sparkle_trail' | 'light_leak' | 'golden_bloom' | 'glitch_cut' | 'beat_flash';
  timing: 'start' | 'middle' | 'climax' | 'end';
  intensity: number;
  params: Record<string, any>;
}

export interface NatureSceneConfig {
  scene: number;
  start: number;
  end: number;
  text?: {
    content: string;
    type: 'typewriter' | 'parallax';
    styleId: number;
    fontSize?: number;
    posY?: number;
  };
  wowEffect?: {
    enabled: boolean;
    presetId?: string;
    intensity?: number;
  };
}

export interface NatureVideoProps {
  videoSrc: string;
  scenes: NatureSceneConfig[];
  filter?: {
    brightness?: number;
    contrast?: number;
    saturate?: number;
  };
}

export interface EventSceneConfig {
  scene: number;
  start: number;
  end: number;
  subtitles?: {
    text: string;
    styleId: number;
  };
  flashTransition?: boolean;
  speedRamp?: {
    enabled: boolean;
    slowRate?: number;
    fastRate?: number;
  };
  freezeFrame?: {
    enabled: boolean;
    duration?: number;
    zoomScale?: number;
  };
  wowEffect?: {
    enabled: boolean;
    presetId?: string;
  };
}

export interface EventVideoProps {
  videoSrc: string;
  scenes: EventSceneConfig[];
  filter?: {
    brightness?: number;
    contrast?: number;
    saturate?: number;
  };
}

export interface LiveTalkSceneConfig {
  scene: number;
  start: number;
  end: number;
  subtitles?: {
    text: string;
    speakerId: number;
    styleId?: number;
  };
  pullQuote?: {
    enabled: boolean;
    quote: string;
    speaker: string;
  };
  wowEffect?: {
    enabled: boolean;
    presetId?: string;
  };
}

export interface LiveTalkVideoProps {
  videoSrc: string;
  scenes: LiveTalkSceneConfig[];
}

