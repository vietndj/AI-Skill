#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO LIFESTYLE VIDEO EDITING PIPELINE (DAILY LIFE & FUN MOMENTS)
Tự động hậu kỳ video Đời Sống Hằng Ngày:
- Nhận diện giọng nói Faster-Whisper
- Phân tích cảm xúc & trêu đùa đời thường
- Tự động gán hiệu ứng Punch-Zoom biểu cảm, Floating Emojis, Subtitle bo tròn tươi sáng
- Nâng tone sáng ấm áp tự nhiên (khử hoàn toàn vignette đen tối tăm)
- Render qua Remotion Engine (Composition: LifestyleVideo)
- Đồng bộ Google Drive & Báo cáo Telegram trực tiếp cho anh Việt.
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

SKILL_DIR = Path.home() / ".gemini" / "config" / "skills" / "auto-edit-video"
SCRIPTS_DIR = SKILL_DIR / "scripts"
REMOTION_DIR = SKILL_DIR / "remotion-studio"
TELEGRAM_NOTIFY_PATH = "/Users/vietmac/Documents/CODE/Quản gia/telegram_notify.py"

def get_video_duration(video_path: str) -> float:
    """Lấy thời lượng video bằng ffprobe"""
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

def transcribe_with_whisper(video_path: str, output_srt: str = None) -> list:
    """Sử dụng faster-whisper để nhận diện giọng nói tiếng Việt và timestamps"""
    print(f"🎙️ [Faster-Whisper] Đang bóc tách giọng nói hội thoại tiếng Việt...")
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

    if output_srt:
        with open(output_srt, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))
        print(f"✅ Đã nhận diện {len(results)} câu phụ đề. Lưu SRT tại: {output_srt}")

    return results

def clean_lifestyle_text(text: str) -> str:
    """Lọc bớt các từ lặp vấp nhưng giữ nguyên chất hội thoại tự nhiên"""
    cleaned = text
    # Chuẩn hóa khoảng trắng
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Loại bỏ lặp 3 từ liên tiếp (ví dụ: 'cái cái cái' -> 'cái')
    cleaned = re.sub(r'\b(\w+)(?:\s+\1){2,}\b', r'\1', cleaned, flags=re.IGNORECASE)
    # Viết hoa chữ cái đầu câu
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned

def map_emojis_for_phrase(text: str) -> list:
    """Gán emoji vui nhộn dựa trên từ khóa ngữ nghĩa câu nói"""
    lower = text.lower()
    emojis = []
    
    if any(k in lower for k in ["xinh", "đẹp", "gái", "dễ thương", "cute"]):
        emojis.extend(["🌸", "✨", "💖"])
    elif any(k in lower for k in ["cười", "hài", "vui", "linh tinh", "trêu", "đùa", "ngáo", "ngơ"]):
        emojis.extend(["😂", "🤪", "✨"])
    elif any(k in lower for k in ["lớn", "nhìn", "mặt", "mắt", "trông"]):
        emojis.extend(["👀", "✨"])
    elif any(k in lower for k in ["đồng hồ", "đồ", "mua", "mới", "khoe"]):
        emojis.extend(["⌚", "✨", "🤩"])
    elif any(k in lower for k in ["ăn", "uống", "cafe", "trà", "ngon"]):
        emojis.extend(["☕", "🍰", "😋"])
    elif any(k in lower for k in ["yêu", "thương", "ôm"]):
        emojis.extend(["🥰", "💕"])
    else:
        emojis.extend(["✨", "🌿"])
        
    return emojis[:2]

def build_lifestyle_scenes(segments: list, total_duration: float, preset: str = "fun") -> list:
    """Xây dựng danh sách phân cảnh Lifestyle (PunchZoom, Subtitle, Emojis)"""
    scenes = []
    
    # Bảng luân phiên style cho phong cách Đời Sống
    style_sequence = [1, 2, 3, 5, 6, 7] if preset == "fun" else [4, 8, 3, 7]
    
    if not segments:
        scenes.append({
            "scene": 1,
            "start": 0.0,
            "end": total_duration,
            "subtitles": {
                "line1": "✨ Daily Moments ✨",
                "styleId": 1 if preset == "fun" else 4,
                "fontSize1": 46,
                "posY": 78,
                "motion": "bounce" if preset == "fun" else "fade"
            },
            "punchZoom": {
                "enabled": preset == "fun",
                "scale": 1.15
            },
            "floatingEmoji": {
                "emojis": ["✨", "🌿"],
                "position": "top-right"
            }
        })
        return scenes

    scene_idx = 1
    for i, seg in enumerate(segments):
        raw_text = seg["text"]
        cleaned = clean_lifestyle_text(raw_text)
        if not cleaned:
            continue

        # Thêm dấu chấm hỏi hoặc cảm thán nếu là câu hỏi/trêu
        if any(cleaned.lower().endswith(w) for w in ["nhỉ", "nhở", "hả", "sao", "đấy nhỉ"]):
            if not cleaned.endswith("?"):
                cleaned += "?"

        start_t = max(0.0, seg["start"])
        end_t = min(total_duration, seg["end"] + 0.25)
        
        # Chọn style luân phiên tươi sáng
        style_id = style_sequence[(scene_idx - 1) % len(style_sequence)]
        
        # Quyết định Punch-Zoom: Bật cho các câu có tính trêu đùa / cao trào
        is_punch_zoom = (scene_idx % 2 == 1) or any(k in cleaned.lower() for k in ["xinh", "lớn", "linh tinh", "nhìn", "đồng hồ"])
        
        # Chọn emoji phù hợp
        emojis = map_emojis_for_phrase(cleaned)
        emoji_pos = "top-right" if scene_idx % 2 == 1 else "center-right"
        
        # Tách dòng nếu câu dài
        words = cleaned.split()
        if len(words) > 7:
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
        else:
            line1 = cleaned
            line2 = ""

        scenes.append({
            "scene": scene_idx,
            "start": start_t,
            "end": end_t,
            "subtitles": {
                "line1": line1,
                "line2": line2 if line2 else undefined_to_empty(line2),
                "styleId": style_id,
                "fontSize1": 44 if len(line1) < 22 else 38,
                "fontSize2": 32,
                "posY": 78,
                "motion": "bounce" if preset == "fun" else "pop"
            },
            "punchZoom": {
                "enabled": is_punch_zoom,
                "scale": 1.18 if is_punch_zoom else 1.0,
                "originX": 50,
                "originY": 38
            },
            "floatingEmoji": {
                "emojis": emojis,
                "position": emoji_pos,
                "motion": "float_up"
            }
        })
        scene_idx += 1

    if scenes:
        scenes[-1]["end"] = max(scenes[-1]["end"], total_duration)

    return scenes


def undefined_to_empty(val):
    return val if val else ""

def render_lifestyle_video(video_path: str, scenes: list, output_path: str, preset: str = "fun", badge_title: str = "✨ Daily Moments") -> bool:
    """Chuẩn bị props và gọi Remotion CLI để render composition LifestyleVideo"""
    public_dir = REMOTION_DIR / "public"
    video_name = os.path.basename(video_path)
    dest_video = public_dir / video_name
    
    # Copy video vào thư mục public của Remotion nếu chưa có
    if not dest_video.exists() or os.path.getmtime(video_path) > os.path.getmtime(dest_video):
        print(f"📁 Đang chuẩn bị tệp vào Remotion public: {video_name}")
        shutil.copy2(video_path, dest_video)
        
    config = {
        "videoSrc": video_name,
        "preset": preset,
        "scenes": scenes,
        "filter": {
            "brightness": 1.05,
            "contrast": 1.03,
            "saturate": 1.14
        },
        "headerTag": {
            "enabled": True,
            "badgeText": badge_title
        }
    }
    
    props_file = REMOTION_DIR / "input-props.json"
    with open(props_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    total_frames = int((scenes[-1]["end"] + 0.5) * 30) if scenes else 300
    
    cmd = [
        "npx", "remotion", "render",
        "LifestyleVideo",
        output_path,
        f"--props={props_file}",
        "--concurrency=4",
        "--codec=h264",
        "--crf=18",
        "--pixel-format=yuv420p",
        "--gl=angle"
    ]
    
    print(f"🎬 [Remotion Engine] Đang render Video Đời Sống (Composition: LifestyleVideo)...")
    res = subprocess.run(cmd, cwd=str(REMOTION_DIR), text=True)
    return res.returncode == 0 and os.path.exists(output_path)

def upload_to_drive(video_path: str) -> str:
    """Tải video lên Google Drive và lấy Link chia sẻ Public"""
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
    """Gửi thông báo kết quả về Telegram cho anh Việt"""
    if os.path.exists(TELEGRAM_NOTIFY_PATH):
        subprocess.run(["python3", TELEGRAM_NOTIFY_PATH, "--msg", message])

def run_lifestyle_pipeline(video_path: str, output_path: str = None, preset: str = "fun", badge_title: str = "✨ Daily Moments", upload_drive: bool = True, send_telegram: bool = True):
    video_path = os.path.abspath(video_path)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Không tìm thấy file video: {video_path}")

    base_dir = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    if not output_path:
        output_path = os.path.join(base_dir, f"{base_name}_lifestyle_{preset}.mp4")
    output_path = os.path.abspath(output_path)
    srt_path = os.path.join(base_dir, f"{base_name}_lifestyle_subs.srt")
    
    total_dur = get_video_duration(video_path)
    print(f"🌸 BẮT ĐẦU HẬU KỲ TỰ ĐỘNG VIDEO ĐỜI SỐNG HẰNG NGÀY (LIFESTYLE PIPELINE)")
    print(f"📹 Tệp nguồn: {video_path} | Thời lượng: {total_dur:.1f}s | Preset: {preset.upper()}")
    
    # Bước 1: Whisper bóc transcript
    segments = transcribe_with_whisper(video_path, srt_path)
    
    # Bước 2: Phân tích kịch bản đời sống, gán Punch-Zoom & Floating Emojis
    scenes = build_lifestyle_scenes(segments, total_dur, preset=preset)
    print(f"✨ Đã thiết kế {len(scenes)} phân cảnh vui tươi (Punch-Zoom + Bo Tròn + Emojis).")
    
    # Bước 3: Render Remotion Lifestyle Video
    ok = render_lifestyle_video(video_path, scenes, output_path, preset=preset, badge_title=badge_title)
    if not ok:
        print("❌ Quá trình render video Remotion thất bại!")
        if send_telegram:
            notify_telegram(f"❌ <b>Lỗi Hậu Kỳ Video Đời Sống:</b> Không thể render <code>{base_name}</code>.")
        return False
        
    final_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"🎉 RENDER HOÀN TẤT THÀNH PHẨM ĐỜI SỐNG: {output_path} ({final_size_mb:.1f}MB)")
    
    # Bước 4: Upload Drive
    drive_link = ""
    if upload_drive:
        drive_link = upload_to_drive(output_path)
        
    # Bước 5: Gửi thông báo Telegram
    if send_telegram:
        msg = (
            f"🌸 <b>HẬU KỲ VIDEO ĐỜI SỐNG TỰ ĐỘNG HOÀN TẤT!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📹 <b>Tệp gốc:</b> <code>{os.path.basename(video_path)}</code>\n"
            f"🎨 <b>Phong cách:</b> <code>Đời Sống Hằng Ngày ({preset.capitalize()} & Playful)</code>\n"
            f"⏱️ <b>Thời lượng:</b> <code>{total_dur:.1f}s</code>\n"
            f"✨ <b>Điểm nhấn:</b> Punch-Zoom biểu cảm + Chữ bo tròn tươi sáng + Floating Emojis bay\n"
            f"📦 <b>Dung lượng:</b> <code>{final_size_mb:.1f}MB</code> (1080x1920 30fps)\n"
            f"━━━━━━━━━━━━━━━━━━\n"
        )
        if drive_link:
            msg += f"☁️ <b>Link xem & tải Google Drive:</b>\n👉 <a href=\"{drive_link}\">{drive_link}</a>\n\n"
        msg += f"✨ <i>Tự động hoàn toàn bởi AI Remotion Engine cho anh Việt.</i>"
        notify_telegram(msg)
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Auto Lifestyle & Daily Life Video Pipeline")
    parser.add_argument("--video", required=True, help="Đường dẫn file video đầu vào")
    parser.add_argument("--output", help="Đường dẫn file video thành phẩm")
    parser.add_argument("--preset", default="fun", choices=["fun", "cozy", "dynamic", "cute"], help="Preset phong cách đời sống")
    parser.add_argument("--badge", default="✨ Daily Moments", help="Tiêu đề badge ở góc trên")
    parser.add_argument("--no-upload", action="store_true", help="Không upload Google Drive")
    parser.add_argument("--no-notify", action="store_true", help="Không gửi tin nhắn Telegram")
    
    args = parser.parse_args()
    run_lifestyle_pipeline(
        video_path=args.video,
        output_path=args.output,
        preset=args.preset,
        badge_title=args.badge,
        upload_drive=not args.no_upload,
        send_telegram=not args.no_notify
    )

if __name__ == "__main__":
    main()
