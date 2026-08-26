export interface NatureStyle {
  id: number;
  name: string;
  textColor: string;
  bgOverlay?: string;
  fontFamily: string;
  fontSize?: number;
  textShadow?: string;
}

export const NATURE_STYLES_DB: NatureStyle[] = [
  { id: 1, name: 'Golden Hour', textColor: '#FFF8E7', fontFamily: "'Playfair Display', serif", textShadow: '0 2px 8px rgba(0,0,0,0.5)' },
  { id: 2, name: 'Ocean Mist', textColor: '#E0F7FA', fontFamily: "'Nunito', sans-serif", textShadow: '0 2px 4px rgba(0,0,0,0.3)' },
  { id: 3, name: 'Forest Green', textColor: '#F1F8E9', fontFamily: "'Lora', serif", textShadow: '0 2px 6px rgba(0,0,0,0.4)' },
  { id: 4, name: 'Sunset Glow', textColor: '#FFE0B2', fontFamily: "'Quicksand', sans-serif", textShadow: '0 2px 10px rgba(0,0,0,0.4)' },
  { id: 5, name: 'Misty Morning', textColor: '#F5F5F5', fontFamily: "'Be Vietnam Pro', sans-serif", textShadow: '0 1px 3px rgba(0,0,0,0.2)' }
];

export function findNatureStyleById(id: number | string): NatureStyle {
  const numId = typeof id === 'string' ? parseInt(id, 10) : id;
  return NATURE_STYLES_DB.find(s => s.id === numId) || NATURE_STYLES_DB[0];
}
