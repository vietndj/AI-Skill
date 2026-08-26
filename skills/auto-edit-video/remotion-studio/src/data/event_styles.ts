export interface EventStyle {
  id: number;
  name: string;
  textColor: string;
  bgColor?: string;
  fontFamily: string;
  textShadow?: string;
}

export const EVENT_STYLES_DB: EventStyle[] = [
  { id: 1, name: 'Neon Pop', textColor: '#FFF', bgColor: '#FF00FF', fontFamily: "'Baloo 2', 'Be Vietnam Pro', sans-serif" },
  { id: 2, name: 'Urban Dark', textColor: '#FFF', bgColor: '#111', fontFamily: "'Oswald', sans-serif" },
  { id: 3, name: 'Festival Warm', textColor: '#FFD700', bgColor: '#FF4500', fontFamily: "'Nunito', sans-serif" },
  { id: 4, name: 'Electric Blue', textColor: '#00FFFF', bgColor: '#00008B', fontFamily: "'Be Vietnam Pro', sans-serif" },
  { id: 5, name: 'Fire Red', textColor: '#FFF', bgColor: '#FF0000', fontFamily: "'Baloo 2', sans-serif" }
];

export function findEventStyleById(id: number | string): EventStyle {
  const numId = typeof id === 'string' ? parseInt(id, 10) : id;
  return EVENT_STYLES_DB.find(s => s.id === numId) || EVENT_STYLES_DB[0];
}
