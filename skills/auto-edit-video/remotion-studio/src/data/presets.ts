export interface VisualPreset {
  id: string;
  name: string;
  icon: string;
  defaultPos: string;
  defaultPosY: number;
  defaultScale: number;
  defaultMotion: number;
  width: number;
  height: number;
  badge: string;
  prompt: string;
  imgSrc: string;
}

export const PRESETS_DB: VisualPreset[] = 
[
  {
    "id": "IMG-01",
    "name": "Thẻ Nổi 3D",
    "icon": "✨",
    "defaultPos": "tr",
    "defaultPosY": 85,
    "defaultScale": 100,
    "defaultMotion": 1,
    "width": 155,
    "height": 155,
    "badge": "⚡ AI AUTOMATION",
    "prompt": "High-end futuristic gold glowing AI microchip floating on dark minimalist desk, cinematic lighting, 8k --ar 1:1",
    "imgSrc": "./assets/ai_leverage_core_1786841955183.jpg"
  },
  {
    "id": "IMG-02",
    "name": "Nửa Màn Trên",
    "icon": "🎬",
    "defaultPos": "top",
    "defaultPosY": 0,
    "defaultScale": 100,
    "defaultMotion": 2,
    "width": 350,
    "height": 298,
    "badge": "B-ROLL",
    "prompt": "Cinematic moody workstation with multiple monitors, ambient warm lighting, professional creator studio --ar 16:9",
    "imgSrc": "./assets/chill_creator_desk_1786841919746.jpg"
  },
  {
    "id": "IMG-03",
    "name": "Toàn Màn 9:16",
    "icon": "📱",
    "defaultPos": "center",
    "defaultPosY": 0,
    "defaultScale": 100,
    "defaultMotion": 3,
    "width": 350,
    "height": 622,
    "badge": "J-CUT HERO",
    "prompt": "Viral growth dashboard on luxury dark titanium phone mockup, neon golden metrics exploding --ar 9:16",
    "imgSrc": "./assets/viral_creator_card_1786841900103.jpg"
  },
  {
    "id": "IMG-04",
    "name": "Ghim Polaroid",
    "icon": "📌",
    "defaultPos": "tr",
    "defaultPosY": 90,
    "defaultScale": 100,
    "defaultMotion": 4,
    "width": 150,
    "height": 180,
    "badge": "LIFESTYLE",
    "prompt": "Vintage gold studio microphone close-up, warm film grain, nostalgic bokeh aesthetic --ar 1:1",
    "imgSrc": "./assets/studio_mic_gold_1786841885528.jpg"
  },
  {
    "id": "IMG-05",
    "name": "Khung iPhone",
    "icon": "📲",
    "defaultPos": "tr",
    "defaultPosY": 80,
    "defaultScale": 100,
    "defaultMotion": 1,
    "width": 145,
    "height": 195,
    "badge": "APP WORKFLOW",
    "prompt": "Modern video editing timeline software on sleek black smartphone screen, 8k UI details --ar 4:5",
    "imgSrc": "./assets/ai_timeline_edit_1786841970084.jpg"
  },
  {
    "id": "IMG-06",
    "name": "Điện Ảnh 16:9",
    "icon": "🎥",
    "defaultPos": "tr",
    "defaultPosY": 95,
    "defaultScale": 100,
    "defaultMotion": 2,
    "width": 190,
    "height": 107,
    "badge": "CINEMA 4K",
    "prompt": "Ultra wide cinematic shot of high-tech studio editing bay, dramatic anamorphic flare --ar 16:9",
    "imgSrc": "./assets/chill_creator_desk_1786841919746.jpg"
  },
  {
    "id": "IMG-07",
    "name": "So Sánh Kép",
    "icon": "⚖️",
    "defaultPos": "center",
    "defaultPosY": 160,
    "defaultScale": 100,
    "defaultMotion": 2,
    "width": 220,
    "height": 145,
    "badge": "BEFORE / AFTER",
    "prompt": "Comparison of messy manual video editing vs ultra-clean automated AI pipeline workflow --ar 4:5",
    "imgSrc": "./assets/ai_timeline_edit_1786841970084.jpg"
  },
  {
    "id": "IMG-08",
    "name": "Ảnh Tròn Stamp",
    "icon": "🎖️",
    "defaultPos": "tr",
    "defaultPosY": 90,
    "defaultScale": 100,
    "defaultMotion": 1,
    "width": 135,
    "height": 135,
    "badge": "VERIFIED",
    "prompt": "Glowing golden circular badge with AI neural network hologram core inside, 3d medal --ar 1:1",
    "imgSrc": "./assets/ai_leverage_core_1786841955183.jpg"
  }
];
