#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO TRANSCRIBE & EDIT VIDEO (MULTI-STYLE AUTO-PILOT PIPELINE)
Hỗ trợ cả 2 trường phái:
1. TALKING HEAD / EDITORIAL (Chuyên gia, khóa học, marketing, tri thức)
2. LIFESTYLE & DAILY LIFE (Đời sống hằng ngày, vui nhộn, vlog, kỷ niệm, trêu đùa)
Tự động phân loại (AI Mood Classifier) hoặc chọn preset qua cờ --preset [auto|fun|cozy|dynamic|cute|editorial]
"""

import os
import sys
import json
import re
import shutil
import subprocess
import argparse
import time
from pathlib import Path

# Thư mục gốc kỹ năng
SKILL_DIR = Path.home() / ".gemini" / "config" / "skills" / "auto-edit-video"
SCRIPTS_DIR = SKILL_DIR / "scripts"
REMOTION_DIR = SKILL_DIR / "remotion-studio"
TELEGRAM_NOTIFY_PATH = "/Users/vietmac/Documents/CODE/Quản gia/telegram_notify.py"

UNIFIED_SPECS = {
    "tier1_base_font_size": 56,
    "tier2_base_font_size": 44,
    "max_tier1_chars": 16,
    "max_tier2_chars": 28,
    "brand_meta": {
        "left": "Viral Video COURSE",
        "center": "↗ 0934.68.86.32 (imess)",
        "right": "2026"
    }
}

CURATED_STYLES = [1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 19, 21, 23, 25, 28, 30]

def get_video_duration(video_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        print(f"⚠️ Không đọc được thời lượng video qua ffprobe: {e}")
        return 10.0

def transcribe_with_whisper(video_path: str, output_srt: str) -> list:
    print(f"🎙️ Đang nhận diện giọng nói tiếng Việt bằng Faster-Whisper...")
    from faster_whisper import WhisperModel

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        video_path,
        language="vi",
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=400)
    )

    results = []
    srt_lines = []
    
    def sec_to_srt(s):
        hrs = int(s // 3600)
        mins = int((s % 3600) // 60)
        secs = int(s % 60)
        millis = int((s - int(s)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    for i, seg in enumerate(segments, 1):
        text = seg.text.strip()
        if not text:
            continue
        results.append({
            "index": i,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": text
        })
        srt_lines.append(f"{i}\n{sec_to_srt(seg.start)} --> {sec_to_srt(seg.end)}\n{text}\n")

    with open(output_srt, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    print(f"✅ Đã nhận diện được {len(results)} câu phụ đề. Lưu tại: {output_srt}")
    return results

def classify_video_genre(segments: list) -> str:
    """Tự động phân loại thể loại video dựa trên từ khóa và ngữ điệu câu nói"""
    full_text = " ".join(seg["text"] for seg in segments).lower()
    
    lifestyle_keywords = [
        "xinh", "gái", "nhìn", "mặt", "cười", "trêu", "đùa", "vui", "linh tinh",
        "đi chơi", "ăn", "uống", "cafe", "đồng hồ", "mua", "em bé", "chó", "mèo",
        "yêu", "nhở", "nhỉ", "đấy nhỉ", "hôm nay", "dạo", "cuối tuần"
    ]
    editorial_keywords = [
        "khóa học", "doanh thu", "chiến lược", "viral", "chuyển đổi", "marketing",
        "content creator", "lập trình", "ai video", "prompt", "kinh doanh", "bài học", "bí quyết"
    ]
    
    lifestyle_score = sum(1 for kw in lifestyle_keywords if kw in full_text)
    editorial_score = sum(1 for kw in editorial_keywords if kw in full_text)
    
    print(f"🔍 [AI Classifier] Điểm Đời Sống: {lifestyle_score} | Điểm Chuyên Gia/Khóa Học: {editorial_score}")
    if lifestyle_score > editorial_score:
        return "fun"
    elif editorial_score > 0:
        return "editorial"
    return "fun" if lifestyle_score > 0 else "editorial"

def clean_subtitles(raw_text: str) -> str:
    filler_words = [
        r'\b(ờ|à|ừm|ừ|hả|hở|nhỉ)\b',
        r'\b(kiểu như|ý là|thì là|nói chung là|thật ra thì|đấy tức là)\b'
    ]
    cleaned = raw_text
    for pattern in filler_words:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    cleaned = re.sub(r'\b(\w+)\s+\1\b', r'\1', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    brand_map = {
        r'\bai\b': 'AI',
        r'\bchatgpt\b': 'ChatGPT',
        r'\btiktok\b': 'TikTok',
        r'\bcapcut\b': 'CapCut',
        r'\byoutube\b': 'YouTube',
        r'\bremotion\b': 'Remotion',
        r'\bgoogle\b': 'Google'
    }
    for pat, rep in brand_map.items():
        cleaned = re.sub(pat, rep, cleaned, flags=re.IGNORECASE)
        
    return cleaned

def split_into_scenes(segments: list, total_duration: float) -> list:
    scenes = []
    if not segments:
        scenes.append({
            "scene": 1,
            "start": 0.0,
            "end": min(total_duration, 4.0),
            "typography": {
                "line1": "TALKING HEAD",
                "line2": "Auto Edit by Antigravity",
                "style_id": 1,
                "size1": UNIFIED_SPECS["tier1_base_font_size"],
                "size2": UNIFIED_SPECS["tier2_base_font_size"],
                "posY": 50,
                "motion": 1,
                "shadowOp": 0.8,
                "glowInt": 0.3
            },
            "visual": {"type": "none"}
        })
        return scenes

    scene_idx = 1
    for i, seg in enumerate(segments):
        cleaned = clean_subtitles(seg["text"])
        if not cleaned:
            continue
            
        words = cleaned.split()
        if not words:
            continue
            
        if len(words) <= 3:
            l1 = " ".join(words).upper()
            l2 = ""
        else:
            l1 = " ".join(words[:2]).upper()
            l2 = " ".join(words[2:6])
            
        if len(l1) > UNIFIED_SPECS["max_tier1_chars"]:
            l1 = l1[:UNIFIED_SPECS["max_tier1_chars"]].strip()
        if len(l2) > UNIFIED_SPECS["max_tier2_chars"]:
            l2 = l2[:UNIFIED_SPECS["max_tier2_chars"]].strip()

        start_t = max(0.0, seg["start"])
        end_t = min(total_duration, seg["end"] + 0.3)
        
        style_id = CURATED_STYLES[(scene_idx - 1) % len(CURATED_STYLES)]
        pos_y = 50 if scene_idx == 1 else 70
        motion = (scene_idx % 4) + 1
        
        scenes.append({
            "scene": scene_idx,
            "start": start_t,
            "end": end_t,
            "typography": {
                "line1": l1,
                "line2": l2,
                "style_id": style_id,
                "size1": UNIFIED_SPECS["tier1_base_font_size"],
                "size2": UNIFIED_SPECS["tier2_base_font_size"],
                "posY": pos_y,
                "motion": motion,
                "shadowOp": 0.8,
                "glowInt": 0.3
            },
            "visual": {"type": "none"}
        })
        scene_idx += 1

    if scenes:
        scenes[-1]["end"] = max(scenes[-1]["end"], total_duration)

    return scenes

def build_remotion_props(video_path: str, scenes: list) -> dict:
    return {
        "videoSrc": os.path.basename(video_path),
        "brand": UNIFIED_SPECS["brand_meta"],
        "scenes": scenes
    }

def render_with_remotion_cli(config_data: dict, video_path: str, output_path: str) -> bool:
    render_script = SCRIPTS_DIR / "render_with_remotion.py"
    temp_config = f"/tmp/remotion_config_{int(time.time())}.json"
    
    with open(temp_config, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    cmd = [
        "python3", str(render_script),
        "--config", temp_config,
        "--video", video_path,
        "--output", output_path,
        "--concurrency", "4"
    ]
    
    print(f"🎬 Đang render video qua Remotion Engine (Composition: AutoEditVideo)...")
    res = subprocess.run(cmd, text=True)
    if os.path.exists(temp_config):
        os.remove(temp_config)
    return res.returncode == 0 and os.path.exists(output_path)

def upload_to_drive(video_path: str) -> str:
    filename = os.path.basename(video_path)
    remote_folder = "gdrive:Work/Auto_Edit_Videos"
    remote_file = f"{remote_folder}/{filename}"
    
    print(f"📤 Đang đồng bộ video lên Google Drive ({remote_folder})...")
    res_copy = subprocess.run(["rclone", "copy", video_path, remote_folder], capture_output=True, text=True)
    if res_copy.returncode != 0:
        print(f"❌ Lỗi rclone copy: {res_copy.stderr}")
        return ""

    print(f"🔗 Đang tạo Link chia sẻ công khai...")
    res_link = subprocess.run(["rclone", "link", remote_file], capture_output=True, text=True)
    if res_link.returncode == 0 and res_link.stdout.strip():
        public_url = res_link.stdout.strip()
        print(f"✅ Google Drive Public Link: {public_url}")
        return public_url
    
    return "https://drive.google.com"

def notify_telegram(message: str):
    if os.path.exists(TELEGRAM_NOTIFY_PATH):
        subprocess.run(["python3", TELEGRAM_NOTIFY_PATH, "--msg", message])

def run_auto_edit_pipeline(video_path: str, output_path: str = None, preset: str = "auto", upload_drive: bool = True, send_telegram: bool = True):
    video_path = os.path.abspath(video_path)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Không tìm thấy file video: {video_path}")

    base_dir = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    srt_path = os.path.join(base_dir, f"{base_name}_subs.srt")
    total_dur = get_video_duration(video_path)

    # Nhận diện giọng nói sơ bộ
    segments = transcribe_with_whisper(video_path, srt_path)
    
    # Xác định preset
    chosen_preset = preset
    if preset == "auto":
        chosen_preset = classify_video_genre(segments)
        print(f"🤖 [AI Decision] Tự động chọn phong cách: {chosen_preset.upper()}")

    # Nếu là phong cách Đời Sống (Lifestyle)
    if chosen_preset in ["fun", "cozy", "dynamic", "cute", "lifestyle", "lifestyle_fun"]:
        actual_lifestyle_preset = "fun" if chosen_preset in ["lifestyle", "lifestyle_fun"] else chosen_preset
        from auto_lifestyle_pipeline import run_lifestyle_pipeline
        return run_lifestyle_pipeline(
            video_path=video_path,
            output_path=output_path,
            preset=actual_lifestyle_preset,
            upload_drive=upload_drive,
            send_telegram=send_telegram
        )

    # Nếu là phong cách Chuyên gia / Editorial Tech
    print(f"🚀 BẮT ĐẦU TỰ ĐỘNG BIÊN TẬP TALKING HEAD / EDITORIAL: {base_name}")
    if not output_path:
        output_path = os.path.join(base_dir, f"{base_name}_editorial_final.mp4")
    output_path = os.path.abspath(output_path)

    scenes = split_into_scenes(segments, total_dur)
    remotion_props = build_remotion_props(video_path, scenes)
    ok = render_with_remotion_cli(remotion_props, video_path, output_path)
    if not ok:
        print("❌ Lỗi trong quá trình render video Remotion!")
        if send_telegram:
            notify_telegram(f"❌ <b>Lỗi Render Video:</b> Không thể xuất video <code>{base_name}</code>.")
        return False
        
    final_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"🎉 RENDER HOÀN TẤT: {output_path} ({final_size_mb:.1f}MB)")
    
    drive_link = ""
    if upload_drive:
        drive_link = upload_to_drive(output_path)
        
    if send_telegram:
        msg = (
            f"🎬 <b>AUTO-EDIT VIDEO: HOÀN TẤT THÀNH PHẨM!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📹 <b>Tệp gốc:</b> <code>{os.path.basename(video_path)}</code>\n"
            f"⏱️ <b>Thời lượng:</b> <code>{total_dur:.1f}s</code>\n"
            f"🎨 <b>Phân cảnh Kinetic:</b> <code>{len(scenes)} cảnh</code>\n"
            f"📦 <b>Dung lượng xuất:</b> <code>{final_size_mb:.1f}MB</code> (1080x1920 30fps)\n"
            f"━━━━━━━━━━━━━━━━━━\n"
        )
        if drive_link:
            msg += f"☁️ <b>Link xem & tải Google Drive:</b>\n👉 <a href=\"{drive_link}\">{drive_link}</a>\n\n"
        msg += f"✨ <i>Biên tập tự động bởi AI Remotion Engine cho anh Việt.</i>"
        notify_telegram(msg)
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Auto Transcribe & Multi-Style Video Editor")
    parser.add_argument("--video", required=True, help="Đường dẫn file video đầu vào")
    parser.add_argument("--output", help="Đường dẫn file video thành phẩm")
    parser.add_argument("--preset", default="auto", choices=["auto", "fun", "cozy", "dynamic", "cute", "editorial"], help="Phong cách biên tập")
    parser.add_argument("--no-upload", action="store_true", help="Không upload Google Drive")
    parser.add_argument("--no-notify", action="store_true", help="Không gửi tin nhắn Telegram")
    
    args = parser.parse_args()
    run_auto_edit_pipeline(
        video_path=args.video,
        output_path=args.output,
        preset=args.preset,
        upload_drive=not args.no_upload,
        send_telegram=not args.no_notify
    )

if __name__ == "__main__":
    main()
