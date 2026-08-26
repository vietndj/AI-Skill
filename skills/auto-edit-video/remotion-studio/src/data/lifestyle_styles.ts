export interface LifestyleStyle {
  id: number;
  name: string;
  fontFamily: string;
  fontWeight: string;
  fontStyle?: string;
  textColor: string;
  bgColor?: string;
  borderColor?: string;
  borderWidth?: number;
  borderRadius?: number;
  boxShadow?: string;
  textShadow?: string;
  padding?: string;
  backdropBlur?: string;
  line1Transform?: 'none' | 'uppercase' | 'capitalize';
}

export const LIFESTYLE_STYLES_DB: LifestyleStyle[] = [
  {
    id: 1,
    name: '01. Vàng Nắng Vui Vẻ (Fun Sunshine)',
    fontFamily: "'Baloo 2', 'Be Vietnam Pro', sans-serif",
    fontWeight: '800',
    textColor: '#1A1A24',
    bgColor: '#FFDE59',
    borderColor: '#FFFFFF',
    borderWidth: 3,
    borderRadius: 36,
    boxShadow: '0 10px 30px rgba(0,0,0,0.22), 0 4px 10px rgba(255,222,89,0.4)',
    textShadow: 'none',
    padding: '14px 34px',
    line1Transform: 'none',
  },
  {
    id: 2,
    name: '02. Hồng Dâu Xinh Gái (Cute Strawberry)',
    fontFamily: "'Nunito', 'Be Vietnam Pro', sans-serif",
    fontWeight: '900',
    textColor: '#FFFFFF',
    bgColor: '#FF6B8B',
    borderColor: '#FFFFFF',
    borderWidth: 3,
    borderRadius: 36,
    boxShadow: '0 10px 30px rgba(255,107,139,0.35), 0 4px 12px rgba(0,0,0,0.15)',
    textShadow: '0 2px 4px rgba(0,0,0,0.2)',
    padding: '14px 34px',
    line1Transform: 'none',
  },
  {
    id: 3,
    name: '03. Xanh Mint Tươi Trẻ (Mint Fresh)',
    fontFamily: "'Baloo 2', 'Be Vietnam Pro', sans-serif",
    fontWeight: '800',
    textColor: '#0B3954',
    bgColor: '#70D6FF',
    borderColor: '#FFFFFF',
    borderWidth: 3,
    borderRadius: 36,
    boxShadow: '0 10px 30px rgba(112,214,255,0.35), 0 4px 10px rgba(0,0,0,0.15)',
    textShadow: 'none',
    padding: '14px 34px',
    line1Transform: 'none',
  },
  {
    id: 4,
    name: '04. Kem Kính Mờ Chữa Lành (Cozy Milk Glass)',
    fontFamily: "'Be Vietnam Pro', sans-serif",
    fontWeight: '700',
    textColor: '#1E2022',
    bgColor: 'rgba(255, 255, 255, 0.92)',
    borderColor: 'rgba(255, 255, 255, 0.6)',
    borderWidth: 2,
    borderRadius: 30,
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
    backdropBlur: '16px',
    textShadow: 'none',
    padding: '12px 30px',
    line1Transform: 'none',
  },
  {
    id: 5,
    name: '05. Hoạt Hình Vui Nhộn (Comic Pop)',
    fontFamily: "'Baloo 2', 'Be Vietnam Pro', sans-serif",
    fontWeight: '800',
    textColor: '#FFFFFF',
    bgColor: '#FF9F1C',
    borderColor: '#231F20',
    borderWidth: 4,
    borderRadius: 24,
    boxShadow: '6px 6px 0px #231F20',
    textShadow: '0 2px 4px rgba(0,0,0,0.3)',
    padding: '14px 32px',
    line1Transform: 'none',
  },
  {
    id: 6,
    name: '06. Xanh Chuối Tinh Nghịch (Neon Lime)',
    fontFamily: "'Nunito', sans-serif",
    fontWeight: '900',
    textColor: '#0F1B07',
    bgColor: '#D9F99D',
    borderColor: '#FFFFFF',
    borderWidth: 3,
    borderRadius: 36,
    boxShadow: '0 10px 25px rgba(217,249,157,0.4)',
    textShadow: 'none',
    padding: '14px 34px',
    line1Transform: 'none',
  },
  {
    id: 7,
    name: '07. Tím Mộng Mơ (Lavender Pastel)',
    fontFamily: "'Quicksand', 'Be Vietnam Pro', sans-serif",
    fontWeight: '700',
    textColor: '#381D2A',
    bgColor: '#E2C4FF',
    borderColor: '#FFFFFF',
    borderWidth: 3,
    borderRadius: 36,
    boxShadow: '0 10px 25px rgba(226,196,255,0.4)',
    textShadow: 'none',
    padding: '14px 34px',
    line1Transform: 'none',
  },
  {
    id: 8,
    name: '08. Thơ Mộng Điện Ảnh (Aesthetic Film Serif)',
    fontFamily: "'Playfair Display', serif",
    fontWeight: '700',
    fontStyle: 'italic',
    textColor: '#FFFDF9',
    bgColor: 'rgba(0, 0, 0, 0.45)',
    borderColor: 'rgba(255, 255, 255, 0.25)',
    borderWidth: 1,
    borderRadius: 24,
    backdropBlur: '12px',
    boxShadow: '0 8px 24px rgba(0,0,0,0.3)',
    textShadow: '0 2px 10px rgba(0,0,0,0.8)',
    padding: '12px 28px',
    line1Transform: 'none',
  }
];

export function findLifestyleStyleById(id: number | string): LifestyleStyle {
  const numId = typeof id === 'string' ? parseInt(id, 10) : id;
  return LIFESTYLE_STYLES_DB.find(s => s.id === numId) || LIFESTYLE_STYLES_DB[0];
}
