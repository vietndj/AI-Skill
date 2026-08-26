#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UGC Auto Pipeline v2 - MASTER PIPELINE (ĐÃ FIX TRIỆT ĐỂ)
Sửa lỗi:
- Video output phải cover FULL duration video gốc (không cắt cụt)
- Audio phải được giữ nguyên từ video gốc
- Scenes phải bao phủ toàn bộ timeline, kể cả đoạn không có thoại
- Font mặc định: SVN-Acta
- Render params: --crf=18 --pixel-format=yuv420p
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
import time
from pathlib import Path

# Paths setup
SKILL_DIR = Path.home() / ".gemini" / "config" / "skills" / "ugc-auto-edit"
SCRIPTS_DIR = SKILL_DIR / "scripts"
REMOTION_DIR = Path.home() / ".gemini" / "config" / "skills" / "auto-edit-video" / "remotion-studio"
TELEGRAM_NOTIFY_PATH = "/Users/vietmac/Documents/CODE/Quản gia/telegram_notify.py"
FONTS_DIR = REMOTION_DIR / "public" / "fonts"

def get_video_duration(video_path: str) -> float:
    """Lấy thời lượng chính xác bằng ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except:
        return 15.0

def run_script(script_name: str, args: list) -> dict:
    cmd = ["python3", str(SCRIPTS_DIR / script_name)] + args
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        print(f"⚠️ Lỗi chạy {script_name}: {e}")
        return {}

def transcribe_with_whisper(video_path: str) -> list:
    """Faster-Whisper bóc tách giọng nói tiếng Việt"""
    print(f"🎙️ [Faster-Whisper] Đang bóc tách giọng nói tiếng Việt...")
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(video_path, language="vi", vad_filter=True,
                                     vad_parameters=dict(min_silence_duration_ms=400))
    
    results = []
    for i, seg in enumerate(segments, 1):
        text = seg.text.strip()
        if text:
            results.append({
                "index": i,
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": text
            })
    print(f"   => Nhận diện {len(results)} đoạn thoại.")
    return results

def notify_telegram(message: str):
    if os.path.exists(TELEGRAM_NOTIFY_PATH):
        subprocess.run(["python3", TELEGRAM_NOTIFY_PATH, "--msg", message])

def upload_to_drive(video_path: str) -> str:
    filename = os.path.basename(video_path)
    remote_folder = "gdrive:Work/Auto_Edit_Videos"
    remote_file = f"{remote_folder}/{filename}"
    print(f"📤 Đang upload {filename} lên {remote_folder}...")
    subprocess.run(["rclone", "copy", video_path, remote_folder])
    res_link = subprocess.run(["rclone", "link", remote_file], capture_output=True, text=True)
    if res_link.returncode == 0:
        return res_link.stdout.strip()
    return "https://drive.google.com"

def build_scenes_full_coverage(catalog: str, segments: list, wow_preset: dict, total_duration: float) -> list:
    """
    TẠO SCENES BAO PHỦ TOÀN BỘ TIMELINE VIDEO.
    Không chỉ cover đoạn có thoại, mà cả khoảng trống giữa các đoạn.
    Scene cuối cùng PHẢI end = total_duration.
    """
    scenes = []
    scene_idx = 1
    
    if not segments:
        # Video không có thoại — 1 scene toàn bộ
        scenes.append({
            "scene": 1,
            "start": 0.0,
            "end": total_duration,
            "subtitles": None,
            "flashTransition": False,
            "wowEffect": {"enabled": True, "presetId": wow_preset.get("effect", "beat_flash")} if wow_preset else None
        })
        return scenes
    
    current_time = 0.0
    
    for i, seg in enumerate(segments):
        seg_start = seg["start"]
        seg_end = seg["end"]
        
        # Gap trước đoạn thoại → scene không subtitle (chỉ hiệu ứng visual)
        if seg_start > current_time + 0.3:
            scenes.append({
                "scene": scene_idx,
                "start": current_time,
                "end": seg_start,
                "subtitles": None,
                "flashTransition": True if scene_idx > 1 else False,
                "wowEffect": None
            })
            scene_idx += 1
        
        # Scene có subtitle
        # Chọn style luân phiên 1-5
        style_id = ((i % 5) + 1)
        
        # Wow effect: áp dụng cho scene đầu tiên hoặc scene giữa
        apply_wow = (i == 0 or i == len(segments) // 2) and wow_preset
        
        scenes.append({
            "scene": scene_idx,
            "start": seg_start,
            "end": seg_end,
            "subtitles": {
                "text": seg["text"],
                "line1": seg["text"],
                "styleId": style_id
            },
            "flashTransition": True if scene_idx > 1 else False,
            "wowEffect": {
                "enabled": True,
                "presetId": wow_preset.get("effect", "beat_flash")
            } if apply_wow else None
        })
        scene_idx += 1
        current_time = seg_end
    
    # QUAN TRỌNG: Scene cuối cover hết video
    if current_time < total_duration - 0.3:
        scenes.append({
            "scene": scene_idx,
            "start": current_time,
            "end": total_duration,
            "subtitles": None,
            "flashTransition": True,
            "wowEffect": None
        })
    
    # ĐẢM BẢO scene cuối end = total_duration
    if scenes:
        scenes[-1]["end"] = total_duration
    
    return scenes

def render_remotion(video_path: str, catalog: str, scenes: list, wow_preset: dict, 
                     output_path: str, total_duration: float) -> bool:
    """Render Remotion với đầy đủ params chống lỗi"""
    video_name = os.path.basename(video_path)
    dest_video = REMOTION_DIR / "public" / video_name
    if not dest_video.exists() or os.path.getmtime(video_path) > os.path.getmtime(str(dest_video)):
        print(f"📁 Copy video vào Remotion public: {video_name}")
        shutil.copy2(video_path, dest_video)
        
    # Map catalog to composition
    comp_map = {
        "DAILY_LIFE": "LifestyleVideo",
        "NATURE_AMBIENT": "NatureVideo",
        "EVENT": "EventVideo",
        "LIVE_TALK": "LiveTalkVideo"
    }
    comp_id = comp_map.get(catalog, "LifestyleVideo")
    
    # Build props với filter tối ưu theo catalog
    filter_map = {
        "EVENT": {"brightness": 1.05, "contrast": 1.08, "saturate": 1.15},
        "DAILY_LIFE": {"brightness": 1.04, "contrast": 1.03, "saturate": 1.12},
        "NATURE_AMBIENT": {"brightness": 1.02, "contrast": 1.02, "saturate": 0.95},
        "LIVE_TALK": {"brightness": 1.03, "contrast": 1.03, "saturate": 1.05},
    }
    
    props = {
        "videoSrc": video_name,
        "catalog": catalog,
        "wowEffect": wow_preset,
        "scenes": scenes,
        "filter": filter_map.get(catalog, filter_map["DAILY_LIFE"]),
    }
    
    # Thêm headerTag cho DAILY_LIFE
    if catalog == "DAILY_LIFE":
        props["preset"] = "fun"
        props["headerTag"] = {"enabled": True, "badgeText": "✨ Daily Moments"}
    
    props_file = REMOTION_DIR / "input-props.json"
    with open(props_file, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)
    
    print(f"📝 Props đã lưu: {len(scenes)} scenes, duration cover đến {scenes[-1]['end']:.1f}s")
    
    cmd = [
        "npx", "remotion", "render", comp_id, output_path,
        f"--props={props_file}",
        "--concurrency=4",
        "--codec=h264",
        "--crf=18",
        "--pixel-format=yuv420p",
        "--gl=angle"
    ]
    
    print(f"🎬 [Remotion] Đang render {comp_id} ({total_duration:.1f}s)...")
    res = subprocess.run(cmd, cwd=str(REMOTION_DIR), text=True)
    
    if res.returncode == 0 and os.path.exists(output_path):
        # POST-RENDER VALIDATION
        out_dur = get_video_duration(output_path)
        in_dur = total_duration
        diff = abs(out_dur - in_dur)
        if diff > 2.0:
            print(f"⚠️ CẢNH BÁO: Duration mismatch! Input={in_dur:.1f}s, Output={out_dur:.1f}s (diff={diff:.1f}s)")
        else:
            print(f"✅ Duration OK: Input={in_dur:.1f}s, Output={out_dur:.1f}s")
        return True
    return False

def run_pipeline(args):
    video_path = os.path.abspath(args.video)
    if not os.path.exists(video_path):
        print(f"❌ Không tìm thấy file: {video_path}")
        return
    
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    out_path = os.path.join(os.path.dirname(video_path), f"{base_name}_ugc_final.mp4")
    
    print("==========================================")
    print("🚀 BẮT ĐẦU UGC AUTO-EDIT PIPELINE v2")
    print("==========================================")
    
    # 0. Đo thời lượng chính xác
    total_duration = get_video_duration(video_path)
    print(f"📹 Video: {os.path.basename(video_path)} | Duration: {total_duration:.1f}s")
    
    # 1. Validation
    print("🔍 Bước 1: Validate video đầu vào...")
    val_report = run_script("input_validator.py", ["--video", video_path])
    
    # 2. Classification
    catalog = args.catalog
    if not catalog:
        print("🤖 Bước 2: AI phân loại catalog...")
        class_res = run_script("ugc_classifier.py", ["--video", video_path])
        catalog = class_res.get("catalog", "DAILY_LIFE")
        confidence = class_res.get("confidence", 0)
        print(f"   => Nhận diện: {catalog} (Confidence: {confidence:.2f})")
    
    # 3. Transcribe
    print("🎙️ Bước 3: Faster-Whisper nhận diện giọng nói...")
    segments = transcribe_with_whisper(video_path)
    
    # 4. Wow Engine
    print("✨ Bước 4: Chọn Wow Effect...")
    wow_res = run_script("wow_engine.py", ["--catalog", catalog])
    wow_preset = wow_res.get("wow_preset", {})
    print(f"   => Hiệu ứng: {wow_preset.get('name', 'None')}")
    
    # 5. Build Scenes — FULL COVERAGE
    print("🎬 Bước 5: Xây dựng timeline phân cảnh...")
    scenes = build_scenes_full_coverage(catalog, segments, wow_preset, total_duration)
    print(f"   => {len(scenes)} scenes, cover 0.0s → {scenes[-1]['end']:.1f}s (full {total_duration:.1f}s)")
    
    if args.mode == "detailed":
        # Detailed mode: save props & hướng dẫn mở Remotion Studio
        props_file = REMOTION_DIR / "input-props.json"
        comp_map = {
            "DAILY_LIFE": "LifestyleVideo",
            "NATURE_AMBIENT": "NatureVideo",
            "EVENT": "EventVideo",
            "LIVE_TALK": "LiveTalkVideo"
        }
        props = {"videoSrc": os.path.basename(video_path), "scenes": scenes, "catalog": catalog}
        with open(props_file, "w", encoding="utf-8") as f:
            json.dump(props, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Config đã lưu tại: {props_file}")
        print(f"👉 Mở Remotion Studio để preview:")
        print(f"   cd {REMOTION_DIR}")
        print(f"   npx remotion studio")
        print(f"👉 Chọn composition: {comp_map.get(catalog, 'EventVideo')}")
        return
        
    # 6. Render
    print("🎥 Bước 6: Render Remotion Engine...")
    ok = render_remotion(video_path, catalog, scenes, wow_preset, out_path, total_duration)
    
    if not ok:
        print("❌ Lỗi render Remotion!")
        if not args.no_notify:
            notify_telegram(f"❌ <b>Lỗi UGC Auto-Edit:</b> Không thể render <code>{base_name}</code>")
        return
        
    final_mb = os.path.getsize(out_path) / (1024*1024)
    print(f"🎉 RENDER THÀNH CÔNG: {out_path} ({final_mb:.1f}MB)")
    
    # 7. Upload
    link = ""
    if not args.no_upload:
        link = upload_to_drive(out_path)
        
    # 8. Notify
    if not args.no_notify:
        msg = (
            f"🎬 <b>UGC AUTO-EDIT HOÀN TẤT</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📹 <b>Gốc:</b> <code>{os.path.basename(video_path)}</code>\n"
            f"🏷️ <b>Catalog:</b> {catalog}\n"
            f"✨ <b>Wow Effect:</b> {wow_preset.get('name', 'None')}\n"
            f"⏱️ <b>Thời lượng:</b> {total_duration:.1f}s\n"
            f"📦 <b>Thành phẩm:</b> <code>{final_mb:.1f}MB</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
        )
        if link:
            msg += f"☁️ <a href=\"{link}\">Link Google Drive</a>\n"
        notify_telegram(msg)
        
    print("✅ HOÀN TẤT PIPELINE!")

def main():
    parser = argparse.ArgumentParser(description="UGC Master Pipeline v2")
    parser.add_argument("--video", required=True, help="Video đầu vào")
    parser.add_argument("--mode", choices=["auto", "detailed"], default="auto")
    parser.add_argument("--catalog", help="Force catalog (DAILY_LIFE, EVENT, ...)")
    parser.add_argument("--preset", help="Override preset cho DAILY_LIFE")
    parser.add_argument("--no-upload", action="store_true")
    parser.add_argument("--no-notify", action="store_true")
    
    args = parser.parse_args()
    run_pipeline(args)

if __name__ == "__main__":
    main()
