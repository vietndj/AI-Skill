#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UGC Classifier (Phân loại video UGC tự động)
Dành riêng cho luồng UGC của anh Việt.
Phân loại video vào 4 catalogs: DAILY_LIFE, NATURE_AMBIENT, EVENT, LIVE_TALK.
"""

import os
import sys
import json
import argparse
import subprocess
import cv2
import numpy as np

def get_video_duration(video_path: str) -> float:
    """Lấy thời lượng video qua ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def count_scene_changes_in_first_30s(video_path: str) -> int:
    """Đếm số lần chuyển cảnh trong 30s đầu sử dụng OpenCV (so sánh Histogram HSV)"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    
    max_frames = int(fps * 30)
    
    scene_changes = 0
    prev_hist = None
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= max_frames:
            break
            
        # Tính toán histogram cho mỗi 10 frame để tối ưu tốc độ
        if frame_count % 10 == 0:
            # Thu nhỏ ảnh để tính toán nhanh hơn
            small = cv2.resize(frame, (160, 120))
            hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            cv2.normalize(hist, hist)
            
            if prev_hist is not None:
                # So sánh độ tương đồng
                score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                if score < 0.6:  # Ngưỡng phát hiện chuyển cảnh
                    scene_changes += 1
            prev_hist = hist
            
        frame_count += 1
        
    cap.release()
    return scene_changes

def analyze_speech(video_path: str, duration: float) -> dict:
    """Dùng faster-whisper để lấy tỷ lệ giọng nói, số đoạn và độ dài TB"""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return {"speech_ratio": 0, "segments_count": 0, "avg_segment_length": 0}
        
    model = WhisperModel("base", device="cpu", compute_type="int8")
    try:
        segments, _ = model.transcribe(
            video_path,
            language="vi",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=400)
        )
    except Exception:
        return {"speech_ratio": 0, "segments_count": 0, "avg_segment_length": 0}
    
    total_speech_time = 0.0
    seg_count = 0
    
    for seg in segments:
        seg_dur = seg.end - seg.start
        total_speech_time += seg_dur
        seg_count += 1
        
    if duration <= 0:
        duration = 1.0
        
    ratio = (total_speech_time / duration) * 100
    avg_len = (total_speech_time / seg_count) if seg_count > 0 else 0
    
    return {
        "speech_ratio": round(ratio, 2),
        "segments_count": seg_count,
        "avg_segment_length": round(avg_len, 2)
    }

def classify_video(video_path: str) -> dict:
    """Tiến hành phân loại thành 4 catalogs"""
    duration = get_video_duration(video_path)
    scenes = count_scene_changes_in_first_30s(video_path)
    speech_data = analyze_speech(video_path, duration)
    
    speech_ratio = speech_data["speech_ratio"]
    seg_count = speech_data["segments_count"]
    avg_len = speech_data["avg_segment_length"]
    
    catalog = "UNKNOWN"
    confidence = 0.0
    
    # Logic phân loại theo yêu cầu của anh Việt
    if speech_ratio > 70 and avg_len > 3.0:
        catalog = "LIVE_TALK"
        confidence = 0.90
    elif scenes > 5:
        catalog = "EVENT"
        confidence = 0.85
    elif speech_ratio > 15 and seg_count >= 3:
        catalog = "DAILY_LIFE"
        confidence = 0.88
    elif speech_ratio < 15:
        catalog = "NATURE_AMBIENT"
        confidence = 0.92
    else:
        # Fallback 
        catalog = "DAILY_LIFE"
        confidence = 0.60
        
    return {
        "catalog": catalog,
        "confidence": confidence,
        "speech_ratio": speech_ratio,
        "scene_count": scenes,
        "segments_count": seg_count,
        "avg_segment_length": avg_len,
        "duration": round(duration, 2)
    }

def main():
    parser = argparse.ArgumentParser(description="UGC Video Classifier")
    parser.add_argument("--video", required=True, help="Đường dẫn video đầu vào")
    args = parser.parse_args()
    
    if not os.path.exists(args.video):
        print(json.dumps({"error": "Video không tồn tại"}))
        sys.exit(1)
        
    result = classify_video(args.video)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
