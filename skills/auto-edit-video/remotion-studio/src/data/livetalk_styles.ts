export interface LiveTalkStyle {
  id: number;
  name: string;
  textColor: string;
  bgColor: string;
  fontFamily: string;
}

export const LIVETALK_STYLES_DB: LiveTalkStyle[] = [
  { id: 1, name: 'Classic Clean', textColor: '#000', bgColor: '#FFF', fontFamily: "'Be Vietnam Pro', sans-serif" },
  { id: 2, name: 'Warm Neutral', textColor: '#333', bgColor: '#F5F5F0', fontFamily: "'Nunito', sans-serif" },
  { id: 3, name: 'Cool Professional', textColor: '#E0E7FF', bgColor: '#1E293B', fontFamily: "'Be Vietnam Pro', sans-serif" },
  { id: 4, name: 'Cozy Cream', textColor: '#4A3F35', bgColor: '#FFF8E7', fontFamily: "'Quicksand', sans-serif" }
];

export function findLiveTalkStyleById(id: number | string): LiveTalkStyle {
  const numId = typeof id === 'string' ? parseInt(id, 10) : id;
  return LIVETALK_STYLES_DB.find(s => s.id === numId) || LIVETALK_STYLES_DB[0];
}
