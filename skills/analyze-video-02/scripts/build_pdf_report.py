#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Director's Shot Notebook PDF Builder (Optimized Edition)
Render Báo Cáo Đạo Diễn HTML sang PDF chuyên nghiệp (Khổ A4 Dark Editorial) với font SVN-Integral & SVN-Poppins.
Tự động nén tối ưu ảnh Base64 để file PDF dưới 5MB-8MB.
"""

import sys
import os
import json
import base64
import io
import argparse
import subprocess
import platform
from PIL import Image

def get_font_base64(font_path):
    """Đọc font và chuyển sang base64 data URI để nhúng trực tiếp vào CSS."""
    if not os.path.exists(font_path):
        return ""
    with open(font_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:font/truetype;charset=utf-8;base64,{encoded}"

def img_to_base64_optimized(img_path, max_width=640, quality=75):
    """Đọc ảnh, nén resize tối ưu và chuyển sang base64 data URI."""
    if not os.path.exists(img_path):
        return ""
    try:
        with Image.open(img_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            # Resize thông minh
            if img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(float(img.height) * float(ratio))
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=quality, optimize=True)
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded}"
    except Exception as e:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

def find_chrome_executable():
    """Tìm Chrome / Chromium trên hệ thống."""
    system = platform.system()
    candidates = []
    if system == "Darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    elif system == "Windows":
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        ]
    else:
        candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def generate_html_report(data_json_path, output_html_path, skill_dir=None):
    """Tạo file HTML hoàn chỉnh với font và hình ảnh nhúng trực tiếp."""
    if skill_dir is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    fonts_dir = os.path.join(skill_dir, "assets", "fonts")
    font_integral_reg = get_font_base64(os.path.join(fonts_dir, "SVN-IntegralCF-Regular.ttf"))
    font_poppins_reg = get_font_base64(os.path.join(fonts_dir, "SVN-Poppins-Regular.ttf"))
    font_poppins_med = get_font_base64(os.path.join(fonts_dir, "SVN-Poppins-Medium.ttf"))
    font_poppins_bold = get_font_base64(os.path.join(fonts_dir, "SVN-Poppins-Bold.ttf"))
    
    with open(data_json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    title = meta.get("title", "BÁO CÁO PHÂN TÍCH ĐIỆN ẢNH & SHOT BREAKDOWN")
    author = meta.get("author", "Director's Cut")
    duration = meta.get("total_duration", 0)
    resolution = f"{meta.get('width', 1080)}x{meta.get('height', 1920)}"
    fps = meta.get("fps", 30)
    shots = meta.get("shots", [])
    
    def get_title_style(text, base_class=""):
        words = len(text.strip().split())
        if words > 8:
            return f"{base_class} title-long-poppins"
        return f"{base_class} title-short-integral"
    
    # Render từng phân cảnh
    shots_html = ""
    for shot in shots:
        shot_num = shot.get("shot_number", 1)
        headline = shot.get("headline", f"Phân cảnh {shot_num:02d}")
        headline_cls = get_title_style(headline, "shot-headline")
        subject_action = shot.get("subject_action", "Mô tả đối tượng và diễn biến.")
        good_points = shot.get("good_points", "Điểm sáng thị giác nổi bật.")
        bad_points = shot.get("bad_points", "Hạn chế hoặc điểm cần cải thiện.")
        takeaway = shot.get("takeaway", "Bài học thực chiến áp dụng.")
        time_range = shot.get("time_range", f"{shot.get('start_time', 0)}s - {shot.get('end_time', 0)}s")
        camera_specs = shot.get("camera_specs", "Góc máy & Tiêu cự")
        lighting_color = shot.get("lighting_color", "Ánh sáng & Tone màu")
        transition = shot.get("transition", "Cut trực tiếp")
        
        # Ảnh Keyframes tối ưu
        kfs = shot.get("keyframes", {})
        start_img = img_to_base64_optimized(kfs.get("start", ""), max_width=480, quality=75)
        mid_img = img_to_base64_optimized(kfs.get("mid", ""), max_width=640, quality=80)
        end_img = img_to_base64_optimized(kfs.get("end", ""), max_width=480, quality=75)
        
        # Dominant Colors
        colors_html = "".join([f'<span class="color-dot" style="background:{c};" title="{c}"></span>' for c in shot.get("dominant_colors", [])])
        
        shots_html += f"""
        <div class="shot-card">
            <div class="shot-header">
                <div class="shot-badge">SHOT {shot_num:02d}</div>
                <div class="shot-time">{time_range}</div>
                <div class="shot-colors">{colors_html}</div>
            </div>
            
            <h2 class="{headline_cls}">{headline}</h2>
            
            <div class="keyframe-grid">
                <div class="kf-col">
                    <span class="kf-label">START ({shot.get('start_time', 0):.2f}s)</span>
                    <img src="{start_img}" class="kf-img" />
                </div>
                <div class="kf-col kf-main">
                    <span class="kf-label kf-badge">MID KEYFRAME (ĐẮT GIÁ NHẤT)</span>
                    <img src="{mid_img}" class="kf-img" />
                </div>
                <div class="kf-col">
                    <span class="kf-label">END ({shot.get('end_time', 0):.2f}s)</span>
                    <img src="{end_img}" class="kf-img" />
                </div>
            </div>
            
            <div class="critique-grid">
                <div class="critique-box box-subject">
                    <div class="box-title">🎬 ĐỐI TƯỢNG & DIỄN BIẾN</div>
                    <p>{subject_action}</p>
                </div>
                
                <div class="critique-box box-good">
                    <div class="box-title">✅ ĐIỂM SÁNG THỊ GIÁC</div>
                    <p>{good_points}</p>
                </div>
                
                <div class="critique-box box-bad">
                    <div class="box-title">⚠️ HẠN CHẾ / LƯU Ý</div>
                    <p>{bad_points}</p>
                </div>
                
                <div class="critique-box box-takeaway">
                    <div class="box-title">💡 BÀI HỌC THỰC CHIẾN</div>
                    <p>{takeaway}</p>
                </div>
            </div>
            
            <div class="shot-specs-bar">
                <span>📐 <b>Góc máy:</b> {camera_specs}</span>
                <span>💡 <b>Ánh sáng:</b> {lighting_color}</span>
                <span>⚡ <b>Chuyển tiếp:</b> {transition}</span>
            </div>
        </div>
        """
        
    main_title_cls = get_title_style(title, "main-title")
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>{title} - Director's Report</title>
<style>
@font-face {{
    font-family: 'SVN-Integral';
    src: url('{{font_integral_reg}}') format('truetype');
    font-weight: 400;
    font-style: normal;
}}
@font-face {{
    font-family: 'SVN-Poppins';
    src: url('{{font_poppins_reg}}') format('truetype');
    font-weight: 400;
    font-style: normal;
}}
@font-face {{
    font-family: 'SVN-Poppins';
    src: url('{{font_poppins_med}}') format('truetype');
    font-weight: 500;
    font-style: normal;
}}
@font-face {{
    font-family: 'SVN-Poppins';
    src: url('{{font_poppins_bold}}') format('truetype');
    font-weight: 700;
    font-style: normal;
}}

:root {{
    --bg-dark: #090B0E;
    --card-bg: #12161F;
    --card-border: #1E2638;
    --accent: #E50914;
    --accent-gold: #F59E0B;
    --text-main: #E2E8F0;
    --text-muted: #94A3B8;
    --green-bg: rgba(16, 185, 129, 0.12);
    --green-border: rgba(16, 185, 129, 0.4);
    --yellow-bg: rgba(245, 158, 11, 0.12);
    --yellow-border: rgba(245, 158, 11, 0.4);
    --blue-bg: rgba(59, 130, 246, 0.12);
    --blue-border: rgba(59, 130, 246, 0.4);
    --purple-bg: rgba(168, 85, 247, 0.12);
    --purple-border: rgba(168, 85, 247, 0.4);
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'SVN-Poppins', -apple-system, sans-serif;
    font-size: 13.5px;
    line-height: 1.55;
    padding: 24px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

.report-container {{
    max-width: 1000px;
    margin: 0 auto;
}}

/* COVER / HEADER */
.cover-header {{
    background: linear-gradient(135deg, #161B26 0%, #0F131C 100%);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
    page-break-inside: avoid;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}}

.doc-tag {{
    font-family: 'SVN-Integral', sans-serif;
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.main-title {{
    margin-bottom: 12px;
    color: #FFFFFF;
}}
.main-title.title-short-integral {{
    font-family: 'SVN-Integral', sans-serif;
    font-weight: 400;
    font-size: 22px;
    line-height: 1.35;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.main-title.title-long-poppins {{
    font-family: 'SVN-Poppins', sans-serif;
    font-weight: 600;
    font-size: 20px;
    line-height: 1.4;
    letter-spacing: normal;
}}

.meta-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 12.5px;
    color: var(--text-muted);
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 12px;
    margin-top: 12px;
}}
.meta-item b {{
    color: #FFFFFF;
}}

/* SHOT CARD */
.shot-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    page-break-inside: avoid;
    break-inside: avoid;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}}

.shot-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}}

.shot-badge {{
    font-family: 'SVN-Integral', sans-serif;
    font-weight: 400;
    font-size: 14px;
    color: #FFFFFF;
    background: var(--accent);
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: 1px;
}}

.shot-time {{
    font-family: 'SVN-Poppins', sans-serif;
    font-weight: 700;
    font-size: 12px;
    color: var(--accent-gold);
    background: rgba(245, 158, 11, 0.1);
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(245, 158, 11, 0.3);
}}

.shot-colors {{
    display: flex;
    gap: 6px;
}}
.color-dot {{
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: inline-block;
    border: 1px solid rgba(255,255,255,0.3);
}}

.shot-headline {{
    margin-bottom: 14px;
    color: #FFFFFF;
}}
.shot-headline.title-short-integral {{
    font-family: 'SVN-Integral', sans-serif;
    font-weight: 400;
    font-size: 14px;
    line-height: 1.4;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}}
.shot-headline.title-long-poppins {{
    font-family: 'SVN-Poppins', sans-serif;
    font-weight: 600;
    font-size: 14.5px;
    line-height: 1.45;
    letter-spacing: normal;
}}

/* KEYFRAME GRID */
.keyframe-grid {{
    display: grid;
    grid-template-columns: 1fr 1.3fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}}

.kf-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.kf-label {{
    font-size: 10.5px;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 4px;
    text-transform: uppercase;
}}

.kf-badge {{
    color: #38BDF8;
}}

.kf-img {{
    width: 100%;
    height: 165px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    background: #000;
}}

.kf-main .kf-img {{
    height: 185px;
    border: 2px solid #38BDF8;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.25);
}}

/* CRITIQUE GRID */
.critique-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 12px;
}}

.critique-box {{
    padding: 12px 14px;
    border-radius: 8px;
    font-size: 12.5px;
}}
.critique-box p {{
    color: var(--text-main);
}}

.box-title {{
    font-family: 'SVN-Integral', sans-serif;
    font-size: 11px;
    margin-bottom: 4px;
    letter-spacing: 0.5px;
}}

.box-subject {{
    background: var(--blue-bg);
    border: 1px solid var(--blue-border);
}}
.box-subject .box-title {{ color: #60A5FA; }}

.box-good {{
    background: var(--green-bg);
    border: 1px solid var(--green-border);
}}
.box-good .box-title {{ color: #34D399; }}

.box-bad {{
    background: var(--yellow-bg);
    border: 1px solid var(--yellow-border);
}}
.box-bad .box-title {{ color: #FBBF24; }}

.box-takeaway {{
    background: var(--purple-bg);
    border: 1px solid var(--purple-border);
}}
.box-takeaway .box-title {{ color: #C084FC; }}

.shot-specs-bar {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 11.5px;
    color: var(--text-muted);
}}
.shot-specs-bar b {{
    color: #CBD5E1;
}}

/* REMAKE SCRIPT & CTA MATRIX STYLES */
.remake-section {{
    page-break-before: always;
    margin-top: 30px;
    padding: 30px;
    background: #111520;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}}
.remake-header {{
    border-bottom: 1px solid rgba(245, 158, 11, 0.2);
    padding-bottom: 18px;
    margin-bottom: 24px;
}}
.remake-badge {{
    display: inline-block;
    background: rgba(245, 158, 11, 0.15);
    color: #F59E0B;
    border: 1px solid rgba(245, 158, 11, 0.4);
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}
.remake-title {{
    font-family: 'SVN-Integral', sans-serif;
    font-size: 20px;
    font-weight: 400;
    color: #FFFFFF;
    letter-spacing: 0.5px;
    line-height: 1.3;
}}
.remake-desc {{
    color: var(--text-muted);
    font-size: 13px;
    margin-top: 6px;
}}

.script-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 30px;
}}
.script-table th {{
    background: rgba(255,255,255,0.05);
    color: #F8FAFC;
    font-family: 'SVN-Integral', sans-serif;
    font-weight: 400;
    font-size: 12px;
    text-align: left;
    padding: 12px 14px;
    border: 1px solid rgba(255,255,255,0.1);
}}
.script-table td {{
    padding: 12px 14px;
    border: 1px solid rgba(255,255,255,0.06);
    vertical-align: top;
    font-size: 13px;
}}
.script-table tr:nth-child(even) {{
    background: rgba(255,255,255,0.02);
}}
.script-time {{
    font-weight: 700;
    color: #E50914;
    font-family: monospace;
    white-space: nowrap;
    width: 15%;
}}
.script-shot {{
    color: #94A3B8;
    width: 35%;
}}
.script-voice {{
    color: #F1F5F9;
    font-weight: 500;
    width: 50%;
}}
.script-voice b {{
    color: #F59E0B;
}}

.cta-section-title {{
    font-family: 'SVN-Integral', sans-serif;
    font-size: 16px;
    font-weight: 400;
    color: #F59E0B;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.cta-grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
}}
.cta-card {{
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 16px 20px;
}}
.cta-card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}}
.cta-hook-label {{
    color: #E2E8F0;
    font-size: 13px;
    font-weight: 700;
}}
.cta-badge {{
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
}}
.badge-direct {{
    background: rgba(239, 68, 68, 0.2);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
}}
.badge-lead {{
    background: rgba(59, 130, 246, 0.2);
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.4);
}}
.badge-engage {{
    background: rgba(16, 185, 129, 0.2);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.4);
}}
.cta-text {{
    color: #FFFFFF;
    font-size: 13.5px;
    line-height: 1.5;
    background: rgba(255,255,255,0.03);
    padding: 10px 14px;
    border-radius: 6px;
    border-left: 3px solid #F59E0B;
}}
.cta-why {{
    color: var(--text-muted);
    font-size: 11.5px;
    margin-top: 6px;
    border-radius: 0 6px 6px 0;
}}

/* PRINT OPTIMIZATION */
@page {{
    size: A4 portrait;
    margin: 10mm;
}}
@media print {{
    body {{
        background: #090B0E !important;
        padding: 0;
    }}
    .shot-card {{
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-bottom: 20px;
    }}
    .remake-section {{
        page-break-before: always !important;
        break-before: page !important;
    }}
}}
</style>
</head>
<body>
<div class="report-container">
    <div class="cover-header">
        <div class="doc-tag">DIRECTOR'S SHOT NOTEBOOK • PERSONAL AI STUDIO</div>
        <h1 class="{main_title_cls}">{title}</h1>
        <div class="meta-row">
            <div class="meta-item">👤 <b>Kênh / Tác giả:</b> {author}</div>
            <div class="meta-item">⏱ <b>Thời lượng:</b> {duration:.2f}s</div>
            <div class="meta-item">📐 <b>Độ phân giải:</b> {resolution} ({fps} FPS)</div>
            <div class="meta-item">✂️ <b>Tổng phân cảnh:</b> {len(shots)} Shots</div>
        </div>
    </div>
    
    {shots_html}

    <!-- KHỐI KỊCH BẢN TIẾNG VIỆT ĂN THEO & 3 MẪU CTA CHỐT HẠ -->
    <div class="remake-section">
        <div class="remake-header">
            <span class="remake-badge">🎬 KỊCH BẢN THỰC THI (REMAKE SCRIPT)</span>
            <h2 class="remake-title">KỊCH BẢN LỜI THOẠI TIẾNG VIỆT ĂN THEO (SẴN SÀNG QUAY NGAY)</h2>
            <p class="remake-desc">Lời thoại mẫu được băm khớp 1-1 theo từng mốc thời gian và hành động của 39 phân cảnh phía trên.</p>
        </div>

        <table class="script-table">
            <thead>
                <tr>
                    <th>MỐC THỜI GIAN</th>
                    <th>CẢNH QUAY & HÀNH ĐỘNG</th>
                    <th>LỜI THOẠI TIẾNG VIỆT (VOICEOVER)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="script-time">0.00s - 2.88s<br><small>(Shot 01 - 02)</small></td>
                    <td class="script-shot"><b>Hook Mở Màn:</b> Góc máy trên cao chúc xuống, tay gạt che camera ➔ POV trực diện đồng bộ chữ lớn.</td>
                    <td class="script-voice">"<b>Đừng bao giờ quay video mà không biết cảnh tiếp theo mình sẽ làm gì...</b> Xem cách mình lên kịch bản 60 giây trong 5 bước."</td>
                </tr>
                <tr>
                    <td class="script-time">2.88s - 13.05s<br><small>(Shot 03 - 08)</small></td>
                    <td class="script-shot"><b>B-Roll Thực Chiến:</b> Cận cảnh nắm tay đòn tạ, toàn cảnh kéo xà đối xứng, nhịp cắt theo tiếng trống nhạc nền.</td>
                    <td class="script-voice">"<b>Bước 1 & 2:</b> Quay lại chính việc bạn làm hàng ngày. Đừng diễn. Một góc toàn định vị không gian và một góc cận tả thực áp lực công việc."</td>
                </tr>
                <tr>
                    <td class="script-time">13.05s - 45.20s<br><small>(Shot 09 - 30)</small></td>
                    <td class="script-shot"><b>Quy Trình & Chi Tiết:</b> Góc quay nghiêng màn hình dựng phim, chuyển cảnh động, chia sẻ bài học xương máu.</td>
                    <td class="script-voice">"<b>Bước 3 & 4:</b> Đưa người xem vào hậu trường làm việc thật. Cắt cảnh đúng vào nhịp nhạc, chữ tiêu đề đặt ở 1/3 trên để không bị che khuất."</td>
                </tr>
                <tr>
                    <td class="script-time">45.20s - 65.36s<br><small>(Shot 31 - 39)</small></td>
                    <td class="script-shot"><b>Đỉnh Điểm & Đoạn Kết:</b> Ngồi trước bàn làm việc, ánh mắt trực diện tự tin, đưa tay tương tác camera để kêu gọi hành động.</td>
                    <td class="script-voice">"<b>Bước 5:</b> Chốt hạ bằng một lời kêu gọi hành động rõ ràng... <i>(Chọn 1 trong 3 mẫu CTA bên dưới tùy mục tiêu)</i>"</td>
                </tr>
            </tbody>
        </table>

        <div class="cta-section-title">
            <span>🎯 3 PHƯƠNG ÁN LỜI THOẠI CTA ĐOẠN CUỐI (TÙY CHỌN THEO MỤC TIÊU)</span>
        </div>

        <div class="cta-grid">
            <div class="cta-card">
                <div class="cta-card-header">
                    <span class="cta-type-badge badge-lead">MẪU 1: KÉO LEAD & BÌNH LUẬN (COMMENT-TO-DM)</span>
                    <small style="color: #94A3B8;">Tăng tỷ lệ tương tác & gửi tài liệu tự động</small>
                </div>
                <div class="cta-voice-quote">
                    "Nếu bạn muốn có trọn bộ kịch bản bóc tách từng giây của video này cùng file PDF 39 trang để tự làm theo: <b>Bình luận [BÓC TÁCH] ngay bên dưới</b>, mình gửi trọn bộ tài liệu vào tin nhắn cho bạn trong 3 giây!"
                </div>
            </div>

            <div class="cta-card">
                <div class="cta-card-header">
                    <span class="cta-type-badge badge-sale">MẪU 2: BÁN HÀNG & CHUYỂN ĐỔI (DIRECT LINK BIO)</span>
                    <small style="color: #94A3B8;">Đẩy traffic vào trang bán hàng / đăng ký khóa học</small>
                </div>
                <div class="cta-voice-quote">
                    "Đừng tự mò góc quay mất thời gian nữa. <b>Bấm ngay vào link ở đầu trang cá nhân</b> để nhận công cụ tự động bóc tách video trong 1 câu lệnh!"
                </div>
            </div>

            <div class="cta-card">
                <div class="cta-card-header">
                    <span class="cta-type-badge badge-viral">MẪU 3: TĂNG LƯỢT LƯU & ĐẨY THUẬT TOÁN (SAVE & SHARE)</span>
                    <small style="color: #94A3B8;">Giúp video ăn đề xuất triệu view</small>
                </div>
                <div class="cta-voice-quote">
                    "<b>Lưu video này lại ngay</b> để lần tới khi bí ý tưởng quay video ngắn, bạn chỉ cần mở ra và làm đúng 3 bước này là có clip triệu view!"
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Đã tạo file HTML Báo Cáo: {output_html_path}")
    return output_html_path

def convert_html_to_pdf(html_path, pdf_path):
    """Dùng Chrome Headless chuyển HTML thành PDF sang xịn mịn."""
    chrome_path = find_chrome_executable()
    if not chrome_path:
        raise FileNotFoundError("Không tìm thấy Google Chrome hoặc Chromium để xuất PDF!")
        
    print(f"🖨 Đang in PDF bằng Chrome Headless ({chrome_path})...")
    file_url = f"file://{os.path.abspath(html_path)}"
    
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        file_url
    ]
    subprocess.check_call(cmd)
    
    if os.path.exists(pdf_path):
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"🎉 Xuất bản PDF thành công: {pdf_path} ({size_mb:.2f} MB)")
        return pdf_path
    raise RuntimeError("Lỗi không tạo được file PDF!")

def auto_open_file(file_path):
    """Tự động mở file trên máy."""
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.Popen(["open", file_path])
        elif system == "Windows":
            os.startfile(file_path)
        else:
            subprocess.Popen(["xdg-open", file_path])
    except Exception as e:
        print(f"⚠️ Không thể tự mở file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Director Report PDF")
    parser.add_argument("data_json", help="Path to shot_data.json")
    parser.add_argument("--output-pdf", "-o", default=None, help="Output PDF path")
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open PDF")
    
    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(args.data_json))
    html_file = os.path.join(base_dir, "director_report.html")
    pdf_file = args.output_pdf or os.path.join(base_dir, "Director_Shot_Notebook.pdf")
    
    generate_html_report(args.data_json, html_file)
    convert_html_to_pdf(html_file, pdf_file)
    
    if not args.no_open:
        auto_open_file(pdf_file)
