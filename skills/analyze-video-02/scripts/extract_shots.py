#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Scene Ingestion & Shot Extraction Engine (OpenCV + yt-dlp)
Bóc tách phân cảnh, trích xuất 3 Keyframes (Start, Mid, End) & Bảng màu Color Palette.
"""

import sys
import os
import json
import re
import argparse
import subprocess
from urllib.parse import urlparse, urlunparse

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:
    # Auto install if missing
    import setup_deps
    setup_deps.check_and_install_all()
    import cv2
    import numpy as np
    from PIL import Image

def clean_url(url):
    """Làm sạch URL, loại bỏ query string rác."""
    if not url.startswith("http"):
        return url
    parsed = urlparse(url)
    # Giữ lại id trên youtube nếu có, bỏ query thừa trên insta/tiktok
    if "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:
        return url
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def download_video(url_or_path, output_dir):
    """Tải video từ link mạng hoặc sao chép file cục bộ."""
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.exists(url_or_path):
        video_path = os.path.join(output_dir, "source_video.mp4")
        if os.path.abspath(url_or_path) != os.path.abspath(video_path):
            import shutil
            shutil.copy2(url_or_path, video_path)
        return video_path, "local_video"
    
    clean = clean_url(url_or_path)
    output_template = os.path.join(output_dir, "source_video.%(ext)s")
    
    print(f"📥 Đang tải video từ URL: {clean}...")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", output_template,
        clean
    ]
    subprocess.check_call(cmd)
    
    # Tìm file mp4 đã tải
    for f in os.listdir(output_dir):
        if f.startswith("source_video.") and not f.endswith(".part"):
            actual_path = os.path.join(output_dir, f)
            # Chuẩn hóa về mp4 nếu cần
            mp4_path = os.path.join(output_dir, "source_video.mp4")
            if actual_path != mp4_path:
                os.rename(actual_path, mp4_path)
            return mp4_path, os.path.splitext(f)[0]
            
    raise FileNotFoundError("Không tìm thấy video sau khi tải về!")

def get_dominant_colors(image_bgr, k=4):
    """Trích xuất k màu chủ đạo dưới dạng HEX code từ ảnh BGR."""
    try:
        # Resize nhỏ để tính toán nhanh
        small_img = cv2.resize(image_bgr, (64, 64), interpolation=cv2.INTER_AREA)
        rgb_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
        pixels = rgb_img.reshape(-1, 3).astype(np.float32)
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, _, centers = cv2.kmeans(pixels, k, None, criteria, 10, flags)
        
        hex_colors = []
        for center in centers:
            r, g, b = [int(c) for c in center]
            hex_colors.append(f"#{r:02x}{g:02x}{b:02x}".upper())
        return hex_colors
    except Exception:
        return ["#1A1A1A", "#333333", "#E50914", "#FFFFFF"]

def extract_scenes(video_path, output_dir, threshold=30.0, min_shot_duration=0.6):
    """
    Phát hiện cắt cảnh bằng HSV Histogram và trích xuất Keyframes.
    """
    shots_dir = os.path.join(output_dir, "extracted_shots")
    os.makedirs(shots_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Không thể mở file video: {video_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_duration = total_frames / fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"🎬 Thông số video: {width}x{height} | {fps:.2f} FPS | {total_duration:.2f}s ({total_frames} frames)")
    
    prev_hist = None
    shot_boundaries = [0] # Frame index
    min_frame_gap = int(fps * min_shot_duration)
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [30, 32], [0, 180, 0, 256])
        cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        
        if prev_hist is not None:
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR)
            if diff > threshold and (frame_idx - shot_boundaries[-1]) >= min_frame_gap:
                shot_boundaries.append(frame_idx)
                
        prev_hist = hist
        frame_idx += 1
        
    if shot_boundaries[-1] != total_frames - 1:
        shot_boundaries.append(total_frames - 1)
        
    # Tạo danh sách các Shots
    shots_data = []
    print(f"✂️ Đã phát hiện {len(shot_boundaries)-1} phân cảnh (Shots). Đang trích xuất Keyframes...")
    
    for i in range(len(shot_boundaries) - 1):
        start_frame = shot_boundaries[i]
        end_frame = shot_boundaries[i+1]
        mid_frame = start_frame + (end_frame - start_frame) // 2
        
        shot_num = i + 1
        shot_id = f"shot_{shot_num:02d}"
        
        start_sec = start_frame / fps
        end_sec = end_frame / fps
        duration_sec = end_sec - start_sec
        
        # Đọc 3 frame đại diện
        keyframes = {}
        dominant_colors = []
        for name, f_pos in [("start", start_frame), ("mid", mid_frame), ("end", max(start_frame, end_frame - 1))]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_pos)
            ret, frame = cap.read()
            if ret:
                img_name = f"{shot_id}_{name}.jpg"
                img_path = os.path.join(shots_dir, img_name)
                # Lưu ảnh chất lượng cao 88%
                cv2.imwrite(img_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
                keyframes[name] = img_path
                if name == "mid":
                    dominant_colors = get_dominant_colors(frame, k=4)
                    
        shots_data.append({
            "shot_number": shot_num,
            "shot_id": shot_id,
            "start_time": round(start_sec, 2),
            "end_time": round(end_sec, 2),
            "duration": round(duration_sec, 2),
            "time_range": f"{start_sec:.2f}s - {end_sec:.2f}s ({duration_sec:.2f}s)",
            "start_frame": start_frame,
            "mid_frame": mid_frame,
            "end_frame": end_frame,
            "keyframes": keyframes,
            "dominant_colors": dominant_colors
        })
        
    cap.release()
    
    metadata = {
        "video_path": video_path,
        "width": width,
        "height": height,
        "fps": round(fps, 2),
        "total_duration": round(total_duration, 2),
        "total_frames": total_frames,
        "shots_count": len(shots_data),
        "shots": shots_data
    }
    
    json_path = os.path.join(output_dir, "shot_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Bóc tách hoàn tất! Dữ liệu lưu tại: {json_path}")
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract video shots and keyframes")
    parser.add_argument("input", help="Video URL or local MP4 path")
    parser.add_argument("--output", "-o", default="./analysis_output", help="Output directory")
    parser.add_argument("--threshold", "-t", type=float, default=28.0, help="Scene cut sensitivity threshold")
    
    args = parser.parse_args()
    video_file, _ = download_video(args.input, args.output)
    extract_scenes(video_file, args.output, threshold=args.threshold)
