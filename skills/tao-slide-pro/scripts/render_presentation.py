#!/usr/bin/env python3
"""
Slide Presentation Render Engine (Standard Master Deck)
Standardized 100% based on slide mau.pptx specifications:
- 10.0 x 5.625 inches (16:9 Widescreen)
- SVN Font System (SVN-Integral CF, SVN-Anguita Sans, SVN-Freight Display, SVN-Walsheim Pro, SVN-Aeonik, SVN-Monument Extended)
- Signature Chrome: Top Year (2026) + Contact, Bottom Mentor Avatar + Name + Phone + Page Number
- Clean Charcoal Theme (#0A0C10, #14171E, #222834, #FFFFFF, #CFCFCF)
- Auto upload to Google Drive folder 'SLIDE 08.2026'
"""

import os
import sys
import json
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

# Core Design System Palette
C_CANVAS_BG = hex_to_rgb('0A0C10')      # Deep Charcoal Black
C_CARD_BG = hex_to_rgb('14171E')        # Container Card
C_CARD_BORDER = hex_to_rgb('222834')    # Card subtle border
C_CARD_ALT_BG = hex_to_rgb('181D26')    # Highlight Card
C_CODE_BG = hex_to_rgb('0B0E14')        # Pure Code Dark
C_HAIRLINE = hex_to_rgb('202632')       # Hairline separator
C_WATERMARK = hex_to_rgb('161B24')      # Backdrop Big Numbers

C_TEXT_HERO = hex_to_rgb('FFFFFF')      # Pure Crisp White
C_TEXT_BODY = hex_to_rgb('CFCFCF')      # Readable Light Gray / Silver
C_TEXT_SUB = hex_to_rgb('94A3B8')       # Soft Subtitle / Gray
C_TEXT_MUTED = hex_to_rgb('64748B')     # Muted

C_ACCENT_CYAN = hex_to_rgb('38BDF8')    # Primary Tech Accent
C_ACCENT_EMERALD = hex_to_rgb('34D399') # Success Accent
C_ACCENT_AMBER = hex_to_rgb('FBBF24')   # Amber Accent
C_ACCENT_ROSE = hex_to_rgb('F43F5E')    # Rose Accent
C_ACCENT_PURPLE = hex_to_rgb('A78BFA')  # Purple Accent
C_ACCENT_ICE = hex_to_rgb('E5E9FF')     # Ice Blue

# Typography (SVN Hierarchy)
FONT_HERO = 'SVN-Integral CF'
FONT_TITLE = 'SVN-Anguita Sans'
FONT_SERIF = 'SVN-Freight Display'
FONT_LABEL = 'SVN-Walsheim Pro'
FONT_BODY = 'SVN-Aeonik'
FONT_CODE = 'Space Grotesk'
FONT_NUM = 'SVN-Monument Extended'

AVATAR_PATH = '/Users/vietmac/.gemini/config/skills/tao-slide-pro/templates/media/image-1-1.png'
if not os.path.exists(AVATAR_PATH):
    AVATAR_PATH = '/Users/vietmac/.gemini/config/skills/tao-slide-pro/templates/media/image-8-1.png'

class SlideBuilder:
    def __init__(self, width=10.0, height=5.625):
        self.prs = Presentation()
        self.prs.slide_width = Inches(width)
        self.prs.slide_height = Inches(height)
        self.blank_layout = self.prs.slide_layouts[6]
        self.width = width
        self.height = height

    def add_base_chrome(self, slide, page_num=1, total_pages=5, breadcrumb="CHỦ ĐỀ BÀI GIẢNG", watermark_num=""):
        # Canvas Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(self.width), Inches(self.height))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_CANVAS_BG
        bg.line.fill.background()

        # Watermark Backdrop Number
        if watermark_num:
            wm = slide.shapes.add_textbox(Inches(7.2), Inches(0.8), Inches(2.6), Inches(4.0))
            tf_wm = wm.text_frame
            tf_wm.word_wrap = False
            tf_wm.margin_left = tf_wm.margin_right = tf_wm.margin_top = tf_wm.margin_bottom = 0
            p_wm = tf_wm.paragraphs[0]
            p_wm.alignment = PP_ALIGN.RIGHT
            r_wm = p_wm.add_run()
            r_wm.text = str(watermark_num)
            r_wm.font.name = FONT_NUM
            r_wm.font.size = Pt(130)
            r_wm.font.bold = True
            r_wm.font.color.rgb = C_WATERMARK

        # Top Bar: Year Left
        tb_yr = slide.shapes.add_textbox(Inches(0.42), Inches(0.30), Inches(1.5), Inches(0.25))
        tf_yr = tb_yr.text_frame
        tf_yr.margin_left = tf_yr.margin_right = tf_yr.margin_top = tf_yr.margin_bottom = 0
        p_yr = tf_yr.paragraphs[0]
        r_yr = p_yr.add_run()
        r_yr.text = "2026"
        r_yr.font.name = 'Inter'
        r_yr.font.size = Pt(6.5)
        r_yr.font.bold = True
        r_yr.font.color.rgb = C_TEXT_BODY

        # Top Bar: Contact Right
        tb_ct = slide.shapes.add_textbox(Inches(5.0), Inches(0.30), Inches(4.58), Inches(0.25))
        tf_ct = tb_ct.text_frame
        tf_ct.margin_left = tf_ct.margin_right = tf_ct.margin_top = tf_ct.margin_bottom = 0
        p_ct = tf_ct.paragraphs[0]
        p_ct.alignment = PP_ALIGN.RIGHT
        r_ct = p_ct.add_run()
        r_ct.text = "IMESS/ZALO : 0934688632"
        r_ct.font.name = FONT_BODY
        r_ct.font.size = Pt(6.5)
        r_ct.font.color.rgb = C_TEXT_BODY

        # Top Hairline
        line_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), Inches(0.88), Inches(9.16), Inches(0.012))
        line_top.fill.solid()
        line_top.fill.fore_color.rgb = C_HAIRLINE
        line_top.line.fill.background()

        # Breadcrumb Label
        if breadcrumb:
            tb_bc = slide.shapes.add_textbox(Inches(0.42), Inches(0.55), Inches(8.0), Inches(0.25))
            tf_bc = tb_bc.text_frame
            tf_bc.margin_left = tf_bc.margin_right = tf_bc.margin_top = tf_bc.margin_bottom = 0
            p_bc = tf_bc.paragraphs[0]
            r_bc = p_bc.add_run()
            r_bc.text = breadcrumb.upper()
            r_bc.font.name = FONT_LABEL
            r_bc.font.size = Pt(7.5)
            r_bc.font.bold = True
            r_bc.font.color.rgb = C_ACCENT_CYAN

        # Bottom Hairline
        line_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), Inches(4.85), Inches(9.16), Inches(0.012))
        line_bot.fill.solid()
        line_bot.fill.fore_color.rgb = C_HAIRLINE
        line_bot.line.fill.background()

        # Bottom Footer: Mentor Avatar & Info
        if os.path.exists(AVATAR_PATH):
            try:
                slide.shapes.add_picture(AVATAR_PATH, Inches(0.42), Inches(4.96), Inches(0.35), Inches(0.35))
            except:
                pass

        tb_mt = slide.shapes.add_textbox(Inches(0.88), Inches(4.96), Inches(4.0), Inches(0.38))
        tf_mt = tb_mt.text_frame
        tf_mt.margin_left = tf_mt.margin_right = tf_mt.margin_top = tf_mt.margin_bottom = 0
        p_m1 = tf_mt.paragraphs[0]
        rm1 = p_m1.add_run()
        rm1.text = "Mentor : Nguyễn Đức Việt"
        rm1.font.name = FONT_LABEL
        rm1.font.size = Pt(8.5)
        rm1.font.bold = True
        rm1.font.color.rgb = C_TEXT_HERO

        p_m2 = tf_mt.add_paragraph()
        rm2 = p_m2.add_run()
        rm2.text = "0934.688.632"
        rm2.font.name = FONT_LABEL
        rm2.font.size = Pt(7.5)
        rm2.font.color.rgb = C_ACCENT_ICE

        # Bottom Right Email
        tb_pg = slide.shapes.add_textbox(Inches(6.5), Inches(5.05), Inches(3.08), Inches(0.25))
        tf_pg = tb_pg.text_frame
        tf_pg.margin_left = tf_pg.margin_right = tf_pg.margin_top = tf_pg.margin_bottom = 0
        p_pg = tf_pg.paragraphs[0]
        p_pg.alignment = PP_ALIGN.RIGHT
        r_pg = p_pg.add_run()
        r_pg.text = "vietndj@gmail.com"
        r_pg.font.name = FONT_BODY
        r_pg.font.size = Pt(8.0)
        r_pg.font.bold = True
        r_pg.font.color.rgb = C_ACCENT_CYAN

    def add_header_titles(self, slide, headline, subline=""):
        tb = slide.shapes.add_textbox(Inches(0.42), Inches(1.02), Inches(9.16), Inches(0.45))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = headline.upper()
        r.font.name = FONT_HERO
        r.font.size = Pt(17.5)
        r.font.bold = True
        r.font.color.rgb = C_TEXT_HERO

        if subline:
            tb_s = slide.shapes.add_textbox(Inches(0.42), Inches(1.42), Inches(9.16), Inches(0.30))
            tf_s = tb_s.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
            ps = tf_s.paragraphs[0]
            rs = ps.add_run()
            rs.text = subline
            rs.font.name = FONT_SERIF
            rs.font.size = Pt(13.0)
            rs.font.italic = True
            rs.font.color.rgb = C_TEXT_BODY

    def render_slide(self, slide_data, page_num, total_pages):
        cat = slide_data.get("category", "CAT-01").upper()
        breadcrumb = slide_data.get("breadcrumb", slide_data.get("section", "BÀI GIẢNG CHUYÊN SÂU"))
        headline = slide_data.get("headline", "")
        subline = slide_data.get("subline", "")
        wm_num = f"{page_num:02d}"

        slide = self.prs.slides.add_slide(self.blank_layout)

        if cat == "CAT-01":
            self.add_base_chrome(slide, page_num, total_pages, breadcrumb=breadcrumb, watermark_num=wm_num)
            tb_title = slide.shapes.add_textbox(Inches(0.42), Inches(1.35), Inches(8.5), Inches(0.95))
            tf_t = tb_title.text_frame
            tf_t.word_wrap = True
            tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
            p_t = tf_t.paragraphs[0]
            r_t = p_t.add_run()
            r_t.text = headline.upper()
            r_t.font.name = FONT_HERO
            r_t.font.size = Pt(28.0)
            r_t.font.bold = True
            r_t.font.color.rgb = C_TEXT_HERO

            if subline:
                tb_sub = slide.shapes.add_textbox(Inches(0.42), Inches(2.45), Inches(8.5), Inches(0.45))
                tf_sub = tb_sub.text_frame
                tf_sub.word_wrap = True
                tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
                p_s = tf_sub.paragraphs[0]
                r_s = p_s.add_run()
                r_s.text = subline
                r_s.font.name = FONT_SERIF
                r_s.font.size = Pt(17.0)
                r_s.font.italic = True
                r_s.font.color.rgb = C_TEXT_BODY

            card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), Inches(3.15), Inches(9.16), Inches(1.45))
            card.fill.solid()
            card.fill.fore_color.rgb = C_CARD_BG
            card.line.color.rgb = C_CARD_BORDER
            card.line.width = Pt(1)

            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), Inches(3.15), Inches(0.06), Inches(1.45))
            bar.fill.solid()
            bar.fill.fore_color.rgb = C_ACCENT_CYAN
            bar.line.fill.background()

            tb_c = slide.shapes.add_textbox(Inches(0.65), Inches(3.28), Inches(8.75), Inches(1.20))
            tf_c = tb_c.text_frame
            tf_c.word_wrap = True
            tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
            
            p1 = tf_c.paragraphs[0]
            r1 = p1.add_run()
            r1.text = slide_data.get("takeaway_title", "KẾT LUẬN CỐT LÕI:")
            r1.font.name = FONT_LABEL
            r1.font.size = Pt(10.0)
            r1.font.bold = True
            r1.font.color.rgb = C_ACCENT_CYAN

            points = slide_data.get("takeaway_points", [])
            for pt_txt in points:
                p = tf_c.add_paragraph()
                p.space_before = Pt(4)
                r = p.add_run()
                r.text = f"• {pt_txt}"
                r.font.name = FONT_BODY
                r.font.size = Pt(10.5)
                r.font.color.rgb = C_TEXT_BODY

        elif cat == "CAT-03":
            self.add_base_chrome(slide, page_num, total_pages, breadcrumb=breadcrumb, watermark_num=wm_num)
            self.add_header_titles(slide, headline, subline)
            card_y = Inches(1.80)
            card_w = Inches(4.45)
            card_h = Inches(2.85)

            # Left Card
            c_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), card_y, card_w, card_h)
            c_left.fill.solid()
            c_left.fill.fore_color.rgb = hex_to_rgb('141113')
            c_left.line.color.rgb = hex_to_rgb('382025')
            c_left.line.width = Pt(1)

            b_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), card_y, Inches(0.06), card_h)
            b_left.fill.solid()
            b_left.fill.fore_color.rgb = C_ACCENT_ROSE
            b_left.line.fill.background()

            tb_l = slide.shapes.add_textbox(Inches(0.62), card_y + Inches(0.15), card_w - Inches(0.35), card_h - Inches(0.30))
            tf_l = tb_l.text_frame
            tf_l.word_wrap = True
            tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
            
            col_l = slide_data.get("col_left", {})
            pl0 = tf_l.paragraphs[0]
            rl0 = pl0.add_run()
            rl0.text = col_l.get("title", "TIÊU CỰC / CẢNH BÁO")
            rl0.font.name = FONT_LABEL
            rl0.font.size = Pt(10.0)
            rl0.font.bold = True
            rl0.font.color.rgb = C_ACCENT_ROSE

            for it in col_l.get("points", []):
                p = tf_l.add_paragraph()
                p.space_before = Pt(6)
                r = p.add_run()
                r.text = f"• {it}"
                r.font.name = FONT_BODY
                r.font.size = Pt(9.5)
                r.font.color.rgb = C_TEXT_BODY

            # Right Card
            c_right = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.13), card_y, card_w, card_h)
            c_right.fill.solid()
            c_right.fill.fore_color.rgb = hex_to_rgb('11161D')
            c_right.line.color.rgb = hex_to_rgb('1C2D42')
            c_right.line.width = Pt(1)

            b_right = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.13), card_y, Inches(0.06), card_h)
            b_right.fill.solid()
            b_right.fill.fore_color.rgb = C_ACCENT_CYAN
            b_right.line.fill.background()

            tb_r = slide.shapes.add_textbox(Inches(5.33), card_y + Inches(0.15), card_w - Inches(0.35), card_h - Inches(0.30))
            tf_r = tb_r.text_frame
            tf_r.word_wrap = True
            tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

            col_r = slide_data.get("col_right", {})
            pr0 = tf_r.paragraphs[0]
            rr0 = pr0.add_run()
            rr0.text = col_r.get("title", "TÍCH CỰC / GIẢI PHÁP")
            rr0.font.name = FONT_LABEL
            rr0.font.size = Pt(10.0)
            rr0.font.bold = True
            rr0.font.color.rgb = C_ACCENT_CYAN

            for it in col_r.get("points", []):
                p = tf_r.add_paragraph()
                p.space_before = Pt(6)
                r = p.add_run()
                r.text = f"• {it}"
                r.font.name = FONT_BODY
                r.font.size = Pt(9.5)
                r.font.color.rgb = C_TEXT_BODY

        elif cat == "CAT-06":
            self.add_base_chrome(slide, page_num, total_pages, breadcrumb=breadcrumb, watermark_num=wm_num)
            self.add_header_titles(slide, headline, subline)
            card_y = Inches(1.80)
            card_w = Inches(2.88)
            card_h = Inches(2.85)
            xs = [Inches(0.42), Inches(3.56), Inches(6.70)]
            colors = [C_ACCENT_CYAN, C_ACCENT_EMERALD, C_ACCENT_AMBER]

            cards = slide_data.get("cards", [])
            for i in range(min(3, len(cards))):
                cd = cards[i]
                c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, xs[i], card_y, card_w, card_h)
                c.fill.solid()
                c.fill.fore_color.rgb = C_CARD_BG
                c.line.color.rgb = C_CARD_BORDER
                c.line.width = Pt(1)

                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, xs[i], card_y, card_w, Inches(0.04))
                bar.fill.solid()
                bar.fill.fore_color.rgb = colors[i]
                bar.line.fill.background()

                tb = slide.shapes.add_textbox(xs[i] + Inches(0.18), card_y + Inches(0.18), card_w - Inches(0.36), card_h - Inches(0.36))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

                p_n = tf.paragraphs[0]
                rn = p_n.add_run()
                rn.text = cd.get("num", f"0{i+1}")
                rn.font.name = FONT_NUM
                rn.font.size = Pt(18.0)
                rn.font.bold = True
                rn.font.color.rgb = colors[i]

                p_tg = tf.add_paragraph()
                p_tg.space_before = Pt(2)
                rtg = p_tg.add_run()
                rtg.text = cd.get("tag", "").upper()
                rtg.font.name = FONT_LABEL
                rtg.font.size = Pt(8.5)
                rtg.font.bold = True
                rtg.font.color.rgb = colors[i]

                p_t = tf.add_paragraph()
                p_t.space_before = Pt(4)
                rt = p_t.add_run()
                rt.text = cd.get("title", "")
                rt.font.name = FONT_HERO
                rt.font.size = Pt(11.0)
                rt.font.bold = True
                rt.font.color.rgb = C_TEXT_HERO

                p_d = tf.add_paragraph()
                p_d.space_before = Pt(8)
                rd = p_d.add_run()
                rd.text = cd.get("desc", "")
                rd.font.name = FONT_BODY
                rd.font.size = Pt(9.5)
                rd.font.color.rgb = C_TEXT_BODY

        elif cat == "CAT-05":
            self.add_base_chrome(slide, page_num, total_pages, breadcrumb=breadcrumb, watermark_num=wm_num)
            self.add_header_titles(slide, headline, subline)
            card_y = Inches(1.80)
            card_h = Inches(2.85)

            c_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), card_y, Inches(4.0), card_h)
            c_left.fill.solid()
            c_left.fill.fore_color.rgb = C_CARD_BG
            c_left.line.color.rgb = C_CARD_BORDER
            c_left.line.width = Pt(1)

            b_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), card_y, Inches(0.06), card_h)
            b_left.fill.solid()
            b_left.fill.fore_color.rgb = C_ACCENT_AMBER
            b_left.line.fill.background()

            tb_l = slide.shapes.add_textbox(Inches(0.62), card_y + Inches(0.18), Inches(3.65), card_h - Inches(0.36))
            tf_l = tb_l.text_frame
            tf_l.word_wrap = True
            tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

            logic = slide_data.get("logic", {})
            pl0 = tf_l.paragraphs[0]
            rl0 = pl0.add_run()
            rl0.text = logic.get("title", "NGUYÊN LÝ LOGIC")
            rl0.font.name = FONT_LABEL
            rl0.font.size = Pt(10.0)
            rl0.font.bold = True
            rl0.font.color.rgb = C_ACCENT_AMBER

            for r in logic.get("rules", []):
                p = tf_l.add_paragraph()
                p.space_before = Pt(6)
                run = p.add_run()
                run.text = f"• {r}"
                run.font.name = FONT_BODY
                run.font.size = Pt(9.2)
                run.font.color.rgb = C_TEXT_BODY

            # IDE Code Box Right
            c_right = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.62), card_y, Inches(4.96), card_h)
            c_right.fill.solid()
            c_right.fill.fore_color.rgb = C_CODE_BG
            c_right.line.color.rgb = hex_to_rgb('1E232F')
            c_right.line.width = Pt(1)

            ide_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.62), card_y, Inches(4.96), Inches(0.32))
            ide_bar.fill.solid()
            ide_bar.fill.fore_color.rgb = hex_to_rgb('141822')
            ide_bar.line.fill.background()

            tb_it = slide.shapes.add_textbox(Inches(4.80), card_y + Inches(0.06), Inches(4.5), Inches(0.20))
            tf_it = tb_it.text_frame
            tf_it.margin_left = tf_it.margin_right = tf_it.margin_top = tf_it.margin_bottom = 0
            pi = tf_it.paragraphs[0]
            ri = pi.add_run()
            ri.text = slide_data.get("code_title", "CONFIG_BLUEPRINT.XML")
            ri.font.name = FONT_LABEL
            ri.font.size = Pt(7.5)
            ri.font.bold = True
            ri.font.color.rgb = C_ACCENT_CYAN

            tb_code = slide.shapes.add_textbox(Inches(4.80), card_y + Inches(0.42), Inches(4.65), card_h - Inches(0.50))
            tf_c = tb_code.text_frame
            tf_c.word_wrap = True
            tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

            code_lines = slide_data.get("code_lines", [])
            first = True
            for line in code_lines:
                p = tf_c.paragraphs[0] if first else tf_c.add_paragraph()
                first = False
                p.space_before = Pt(1.5)
                r = p.add_run()
                r.text = line
                r.font.name = FONT_CODE
                r.font.size = Pt(8.5)
                r.font.color.rgb = C_ACCENT_CYAN if '<' in line and '>' in line else C_TEXT_BODY

        elif cat == "CAT-07":
            self.add_base_chrome(slide, page_num, total_pages, breadcrumb=breadcrumb, watermark_num=wm_num)
            self.add_header_titles(slide, headline, subline)
            card_w = Inches(4.45)
            card_h = Inches(1.35)
            xs = [Inches(0.42), Inches(5.13), Inches(0.42), Inches(5.13)]
            ys = [Inches(1.80), Inches(1.80), Inches(3.30), Inches(3.30)]
            colors = [C_ACCENT_CYAN, C_ACCENT_EMERALD, C_ACCENT_AMBER, C_ACCENT_PURPLE]

            blocks = slide_data.get("blocks", [])
            for i in range(min(4, len(blocks))):
                b = blocks[i]
                c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, xs[i], ys[i], card_w, card_h)
                c.fill.solid()
                c.fill.fore_color.rgb = C_CARD_BG
                c.line.color.rgb = C_CARD_BORDER
                c.line.width = Pt(1)

                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, xs[i], ys[i], Inches(0.04), card_h)
                bar.fill.solid()
                bar.fill.fore_color.rgb = colors[i]
                bar.line.fill.background()

                tb = slide.shapes.add_textbox(xs[i] + Inches(0.15), ys[i] + Inches(0.10), card_w - Inches(0.28), card_h - Inches(0.20))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

                p_t = tf.paragraphs[0]
                rt = p_t.add_run()
                rt.text = f"{b.get('num', f'0{i+1}')}. {b.get('title', '')}"
                rt.font.name = FONT_LABEL
                rt.font.size = Pt(9.5)
                rt.font.bold = True
                rt.font.color.rgb = colors[i]

                p_d = tf.add_paragraph()
                p_d.space_before = Pt(3)
                rd = p_d.add_run()
                rd.text = b.get("desc", "")
                rd.font.name = FONT_BODY
                rd.font.size = Pt(8.8)
                rd.font.color.rgb = C_TEXT_BODY

    def save(self, output_path):
        self.prs.save(output_path)
        print(f"Presentation generated: {output_path}")

def render_from_json(json_path, output_pptx, upload=False):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    slides = data.get("slides", [])
    total_pages = len(slides)
    builder = SlideBuilder()

    for idx, slide_data in enumerate(slides):
        builder.render_slide(slide_data, idx + 1, total_pages)

    builder.save(output_pptx)

    if upload:
        remote_dest = "gdrive:SLIDE 08.2026/"
        cmd = f'rclone copy "{output_pptx}" "{remote_dest}"'
        print(f"Uploading to Google Drive: {cmd}")
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            link_cmd = f'rclone link "{remote_dest}{os.path.basename(output_pptx)}"'
            link_res = subprocess.run(link_cmd, shell=True, capture_output=True, text=True)
            print("Google Drive Link:", link_res.stdout.strip())
        else:
            print("Upload error:", res.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 render_presentation.py <deck.json> <output.pptx> [--upload]")
        sys.exit(1)

    json_file = sys.argv[1]
    out_pptx = sys.argv[2]
    do_upload = "--upload" in sys.argv
    render_from_json(json_file, out_pptx, upload=do_upload)
