#!/usr/bin/env python3
"""
get_latest_image.py: Tự động tìm kiếm file ảnh/screenshot mới nhất trên máy Mac.
Ưu tiên hàng đầu thư mục: ~/Documents/anhchup và các biến thể anhchup.
"""

import os
import sys
import time
import json
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def find_latest_image():
    home = os.path.expanduser('~')
    
    # Danh sách các thư mục quét (ưu tiên thư mục anhchup lên hàng đầu)
    target_dirs = [
        os.path.join(home, 'Documents', 'anhchup'),
        os.path.join(home, 'anhchup'),
        os.path.join(home, 'Desktop', 'anhchup'),
        os.path.join(home, 'Pictures', 'anhchup'),
        os.path.join(home, 'Downloads', 'anhchup'),
        os.path.join(home, 'Screenshots'),
        os.path.join(home, 'Desktop'),
        os.path.join(home, 'Downloads'),
        os.path.join(home, 'Pictures'),
        '/Users/vietmac/Documents/CODE/Quản gia'
    ]
    
    valid_exts = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif'}
    found_images = []
    
    for cdir in target_dirs:
        if not os.path.exists(cdir):
            continue
        try:
            for entry in os.scandir(cdir):
                if entry.name.startswith('.'):
                    continue
                if entry.is_file():
                    ext = os.path.splitext(entry.name)[1].lower()
                    if ext in valid_exts:
                        try:
                            st = entry.stat()
                            if st.st_size > 0:
                                found_images.append((st.st_mtime, entry.path, st.st_size))
                        except Exception:
                            pass
                elif entry.is_dir() and entry.name not in ('node_modules', '.git', 'dist', 'build', '.next', 'Library'):
                    try:
                        for sub_entry in os.scandir(entry.path):
                            if sub_entry.name.startswith('.'):
                                continue
                            if sub_entry.is_file():
                                ext = os.path.splitext(sub_entry.name)[1].lower()
                                if ext in valid_exts:
                                    try:
                                        st = sub_entry.stat()
                                        if st.st_size > 0:
                                            found_images.append((st.st_mtime, sub_entry.path, st.st_size))
                                    except Exception:
                                        pass
                    except Exception:
                        pass
        except Exception:
            pass

    if not found_images:
        return None

    # Sắp xếp theo thời gian sửa đổi mới nhất
    found_images.sort(key=lambda x: x[0], reverse=True)
    latest_mtime, latest_path, latest_size = found_images[0]
    
    now = time.time()
    seconds_ago = int(now - latest_mtime)
    
    # Lấy thông tin kích thước ảnh
    width, height = 0, 0
    preview_path = latest_path
    
    if HAS_PIL:
        try:
            with Image.open(latest_path) as img:
                width, height = img.size
                
                # Nếu ảnh quá lớn (>1.5MB hoặc chiều rộng > 1920px), tạo bản nén preview để view nhanh & nhẹ
                if latest_size > 1024 * 1024 or width > 1920:
                    max_dim = 1600
                    scale = min(max_dim / width, max_dim / height) if (width > max_dim or height > max_dim) else 1.0
                    new_w = int(width * scale)
                    new_h = int(height * scale)
                    
                    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    if resized_img.mode in ('RGBA', 'P'):
                        resized_img = resized_img.convert('RGB')
                    
                    tmp_preview = '/tmp/agy_latest_screenshot_preview.jpg'
                    resized_img.save(tmp_preview, 'JPEG', quality=85, optimize=True)
                    preview_path = tmp_preview
        except Exception:
            pass

    # Định dạng thời gian
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest_mtime))
    
    human_ago = (
        f"{seconds_ago} giây trước" if seconds_ago < 60
        else f"{seconds_ago // 60} phút trước" if seconds_ago < 3600
        else f"{seconds_ago // 3600} giờ trước"
    )

    return {
        "success": True,
        "path": latest_path,
        "preview_path": preview_path,
        "filename": os.path.basename(latest_path),
        "size_kb": round(latest_size / 1024, 1),
        "dimensions": f"{width}x{height}" if width and height else "Unknown",
        "modified_time": time_str,
        "human_ago": human_ago,
        "seconds_ago": seconds_ago
    }

if __name__ == "__main__":
    res = find_latest_image()
    if res:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"success": False, "message": "Không tìm thấy file ảnh nào trên hệ thống."}, ensure_ascii=False))
