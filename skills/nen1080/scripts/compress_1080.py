#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nen1080: Script nén video chuẩn Instagram 1080p True CDN (Siêu nhẹ ~3MB-6MB, cực nét trên điện thoại)
"""

import sys
import os
import subprocess
import argparse
import unicodedata

def find_file(query):
    if os.path.exists(query):
        return os.path.abspath(query)
    
    # Chuẩn hóa Unicode NFD/NFC để tìm kiếm tiếng Việt trên macOS
    norm_query = unicodedata.normalize('NFD', os.path.basename(query).lower())
    search_dirs = [
        os.getcwd(),
        os.path.expanduser("~/Documents/RENDER THANG 7"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Movies")
    ]
    
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for root, _, files in os.walk(sdir):
            for f in files:
                norm_f = unicodedata.normalize('NFD', f.lower())
                if norm_query in norm_f and f.lower().endswith(('.mp4', '.mov', '.mkv', '.m4v')):
                    return os.path.join(root, f)
    return None

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def compress_video_1080(input_path, output_path=None):
    real_input = find_file(input_path)
    if not real_input or not os.path.exists(real_input):
        print(f"❌ Không tìm thấy video: {input_path}")
        return False, None
    
    if not output_path:
        dir_name = os.path.dirname(real_input)
        base_name = os.path.splitext(os.path.basename(real_input))[0]
        output_path = os.path.join(dir_name, f"{base_name}_1080p_insta.mp4")
    
    orig_size = get_file_size_mb(real_input)
    print(f"🎬 Bắt đầu nén video:")
    print(f"   • Đầu vào: {real_input}")
    print(f"   • Dung lượng gốc: {orig_size:.2f} MB")
    print(f"   • Cấu hình: Instagram 1080p True CDN (H.264 CRF 28, Maxrate 1000k, Audio AAC 64k, Faststart)")
    
    # Cấu hình chuẩn Instagram 1080p True CDN
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", real_input,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "28",
        "-maxrate", "1000k",
        "-bufsize", "2000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "64k",
        "-movflags", "+faststart",
        output_path
    ]
    
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if process.returncode != 0:
        print(f"❌ Lỗi khi nén video:")
        print(process.stderr[-500:])
        return False, None
    
    new_size = get_file_size_mb(output_path)
    reduction = ((orig_size - new_size) / orig_size) * 100
    
    print("\n✅ Nén hoàn tất thành công!")
    print(f"   • File xuất ra: {output_path}")
    print(f"   • Dung lượng mới: {new_size:.2f} MB")
    print(f"   • Tiết kiệm: {reduction:.1f}% dung lượng")
    
    return True, output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="nen1080 - Nén video chuẩn Instagram 1080p nét cao siêu nhẹ")
    parser.add_argument("input", help="Đường dẫn hoặc tên file video cần nén")
    parser.add_argument("-o", "--output", help="Đường dẫn file đầu ra (tùy chọn)", default=None)
    
    args = parser.parse_args()
    compress_video_1080(args.input, args.output)
