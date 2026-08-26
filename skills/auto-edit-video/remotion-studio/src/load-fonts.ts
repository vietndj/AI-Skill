/**
 * Font loader for Remotion — loads custom fonts using staticFile() + FontFace API
 * Must be called at MODULE SCOPE (not inside useEffect) to ensure fonts are loaded
 * before any frame is captured.
 */
import { staticFile, delayRender, continueRender } from 'remotion';

interface FontDef {
  family: string;
  file: string;
  weight: string;
  style: string;
}

const FONT_DEFS: FontDef[] = [
  // SVN-Integral
  { family: 'SVN-Integral', file: 'fonts/SVN-IntegralCF-Heavy.ttf', weight: '900', style: 'normal' },
  { family: 'SVN-Integral', file: 'fonts/SVN-IntegralCF-Bold.ttf', weight: '700', style: 'normal' },
  // SVN-Aeonik
  { family: 'SVN-Aeonik', file: 'fonts/SVN-AEONIK-BLACK.TTF', weight: '900', style: 'normal' },
  { family: 'SVN-Aeonik', file: 'fonts/SVN-AEONIK-BOLD.TTF', weight: '700', style: 'normal' },
  { family: 'SVN-Aeonik', file: 'fonts/SVN-AEONIK-REGULAR.TTF', weight: '400', style: 'normal' },
  // GT-America
  { family: 'GT-America', file: 'fonts/GT-America-LCGV-Standard-Black.ttf', weight: '900', style: 'normal' },
  { family: 'GT-America', file: 'fonts/GT-America-LCGV-Standard-Bold.ttf', weight: '700', style: 'normal' },
  { family: 'GT-America', file: 'fonts/GT-America-LCGV-Standard-Bold-Italic.ttf', weight: '700', style: 'italic' },
  { family: 'GT-America', file: 'fonts/GT-America-LCGV-Standard-Medium.ttf', weight: '500', style: 'normal' },
  // SVN-FreightDisplay
  { family: 'SVN-FreightDisplay', file: 'fonts/SVN-FreightDisplay-BlackItalic.ttf', weight: '900', style: 'italic' },
  { family: 'SVN-FreightDisplay', file: 'fonts/SVN-FreightDisplay-BoldItalic.ttf', weight: '700', style: 'italic' },
  { family: 'SVN-FreightDisplay', file: 'fonts/SVN-FreightDisplay-MediumItalic.ttf', weight: '500', style: 'italic' },
  // SVN-Flatline
  { family: 'SVN-Flatline', file: 'fonts/SVN-Flatline Bold Italic.ttf', weight: '700', style: 'italic' },
  { family: 'SVN-Flatline', file: 'fonts/SVN-Flatline SemiBold Italic.ttf', weight: '600', style: 'italic' },
  { family: 'SVN-Flatline', file: 'fonts/SVN-Flatline Regular Italic.ttf', weight: '400', style: 'italic' },
  // GT-Sectra
  { family: 'GT-Sectra', file: 'fonts/GT-Sectra-LCGV-Display-Bold.otf', weight: '700', style: 'normal' },
  { family: 'GT-Sectra', file: 'fonts/GT-Sectra-LCGV-Display-Bold-Italic.otf', weight: '700', style: 'italic' },
  { family: 'GT-Sectra', file: 'fonts/GT-Sectra-LCGV-Display-Super.otf', weight: '900', style: 'normal' },
  { family: 'GT-Sectra', file: 'fonts/GT-Sectra-LCGV-Display-Regular-Italic.otf', weight: '400', style: 'italic' },
  // SVN-Acta
  { family: 'SVN-Acta', file: 'fonts/SVN-Acta-BoldItalic.ttf', weight: '700', style: 'italic' },
  { family: 'SVN-Acta', file: 'fonts/SVN-Acta-MediumItalic.ttf', weight: '500', style: 'italic' },
];

// Load all fonts at module scope — Remotion will delay rendering until all fonts are ready
const fontHandles: number[] = [];

for (const def of FONT_DEFS) {
  const handle = delayRender(`Loading font: ${def.family} ${def.weight} ${def.style}`);
  fontHandles.push(handle);

  const fontUrl = staticFile(def.file);
  const font = new FontFace(def.family, `url('${fontUrl}')`, {
    weight: def.weight,
    style: def.style,
  });

  font
    .load()
    .then((loadedFont) => {
      document.fonts.add(loadedFont);
      continueRender(handle);
    })
    .catch((err) => {
      console.error(`Failed to load font ${def.family} ${def.weight}: ${err}`);
      continueRender(handle); // Continue anyway to not block render
    });
}

export { FONT_DEFS };
