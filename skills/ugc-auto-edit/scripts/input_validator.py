#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Validator (Kiểm tra chất lượng video đầu vào)
Kiểm tra độ phân giải, framerate, VFR, thời lượng, định dạng, và dung lượng.
"""

import os
import sys
import json
import argparse
import subprocess

def get_video_info(video_path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,avg_frame_rate:format=duration,size,format_name",
        "-of", "json",
        video_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        return {}

def check_vfr(video_path: str) -> bool:
    """Phát hiện Variable Frame Rate qua ffprobe vfrdet (nếu hỗ trợ)"""
    cmd = [
        "ffmpeg", "-v", "error", "-i", video_path,
        "-vf", "vfrdet", "-f", "null", "-"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return "VFR:" in res.stderr
    except Exception:
        return False

def validate_video(video_path: str) -> dict:
    report = {
        "resolution": {"status": "fail", "msg": ""},
        "framerate": {"status": "fail", "msg": ""},
        "duration": {"status": "fail", "msg": ""},
        "format": {"status": "fail", "msg": ""},
        "filesize": {"status": "fail", "msg": ""}
    }
    
    if not os.path.exists(video_path):
        return report

    info = get_video_info(video_path)
    if not info:
        return report

    streams = info.get("streams", [{}])[0]
    formats = info.get("format", {})
    
    # 1. Resolution
    width = streams.get("width", 0)
    height = streams.get("height", 0)
    min_dim = min(width, height)
    
    if min_dim >= 1080:
        report["resolution"] = {"status": "pass", "msg": f"Độ phân giải tốt ({width}x{height})"}
    elif min_dim >= 720:
        report["resolution"] = {"status": "warn", "msg": f"Độ phân giải hơi thấp ({width}x{height})"}
    else:
        report["resolution"] = {"status": "fail", "msg": f"Độ phân giải quá thấp ({width}x{height})"}
        
    # 2. Framerate / VFR
    is_vfr = check_vfr(video_path)
    if is_vfr:
        report["framerate"] = {"status": "warn", "msg": "Phát hiện Variable Frame Rate (VFR), có thể lỗi đồng bộ audio"}
    else:
        report["framerate"] = {"status": "pass", "msg": "Framerate ổn định (CFR)"}
        
    # 3. Duration
    try:
        duration = float(formats.get("duration", 0))
    except ValueError:
        duration = 0
        
    if 15 <= duration <= 45:
        report["duration"] = {"status": "pass", "msg": f"Thời lượng tối ưu ({duration:.1f}s)"}
    elif 5 <= duration <= 120:
        report["duration"] = {"status": "warn", "msg": f"Thời lượng hơi ngắn/dài ({duration:.1f}s)"}
    else:
        report["duration"] = {"status": "fail", "msg": f"Thời lượng không hợp lệ ({duration:.1f}s)"}
        
    # 4. Format
    ext = os.path.splitext(video_path)[1].lower()
    if ext in [".mp4", ".mov", ".mkv"]:
        report["format"] = {"status": "pass", "msg": f"Định dạng hỗ trợ ({ext})"}
    else:
        report["format"] = {"status": "fail", "msg": f"Định dạng không khuyến khích ({ext})"}
        
    # 5. File size
    try:
        size_bytes = int(formats.get("size", os.path.getsize(video_path)))
        size_mb = size_bytes / (1024 * 1024)
        if size_mb <= 500:
            report["filesize"] = {"status": "pass", "msg": f"Dung lượng nhẹ ({size_mb:.1f}MB)"}
        else:
            report["filesize"] = {"status": "warn", "msg": f"Dung lượng lớn ({size_mb:.1f}MB)"}
    except Exception:
        pass
        
    return report

def main():
    parser = argparse.ArgumentParser(description="UGC Input Validator")
    parser.add_argument("--video", required=True, help="Đường dẫn video đầu vào")
    args = parser.parse_args()
    
    report = validate_video(args.video)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
