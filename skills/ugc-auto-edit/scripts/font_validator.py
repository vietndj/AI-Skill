#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Validator (Kiểm tra lỗi hiển thị font chữ tiếng Việt)
Kiểm tra xem font có kết xuất đủ các ký tự tiếng Việt khó không.
"""

import os
import sys
import json
import argparse
from pathlib import Path

def check_font_vietnamese_support(font_path: str, test_string: str = 'Ướt sũng ễnh ương đỏ ối ẵm ặn ẫm ẩn') -> dict:
    """Kiểm tra render tiếng Việt sử dụng PIL. Phân tích các glyph bị thiếu (tofu)."""
    try:
        from PIL import ImageFont
    except ImportError:
        return {"status": "error", "msg": "Cần cài đặt Pillow (pip install Pillow) để kiểm tra font"}

    if not os.path.exists(font_path):
        return {"status": "fail", "msg": f"Không tìm thấy font tại {font_path}", "valid": False}

    try:
        # Load font chữ ở size 40
        font = ImageFont.truetype(font_path, 40)
        
        # Kiểm tra mask của font. Nếu glyph = 0 hoặc missing (tofu) thì báo lỗi
        # Pillow font.getmask() cho một ký tự sẽ rỗng nếu không có glyph hoặc là space
        missing_chars = []
        for char in test_string:
            if char == ' ':
                continue
            
            # Một số font thay thế ký tự thiếu bằng ô vuông (tofu) hoặc trống
            # Ở cấp độ cơ bản, ta kiểm tra độ dài và bound của mask
            mask = font.getmask(char)
            bbox = mask.getbbox()
            
            if not bbox:
                missing_chars.append(char)
                
        if missing_chars:
            unique_missing = list(set(missing_chars))
            return {
                "status": "fail", 
                "valid": False, 
                "msg": f"Font thiếu hỗ trợ ký tự tiếng Việt: {', '.join(unique_missing)}"
            }
            
        return {"status": "pass", "valid": True, "msg": "Font hỗ trợ tiếng Việt tốt"}
    except Exception as e:
        return {"status": "error", "valid": False, "msg": f"Lỗi kiểm tra font: {e}"}

def check_scenes_text(font_path: str, scenes_json: str) -> dict:
    """Kiểm tra toàn bộ text trong scenes JSON (mở rộng)"""
    with open(scenes_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    full_text = ""
    for scene in data:
        subs = scene.get('subtitles', {})
        full_text += subs.get('line1', '') + " " + subs.get('line2', '') + " "
        
    return check_font_vietnamese_support(font_path, full_text.strip())

def main():
    parser = argparse.ArgumentParser(description="Font Validator cho Tiếng Việt")
    parser.add_argument("--font", required=True, help="Đường dẫn file font (.ttf, .otf)")
    parser.add_argument("--text", default="Ướt sũng ễnh ương đỏ ối ẵm ặn ẫm ẩn", help="Chuỗi kiểm tra")
    parser.add_argument("--scenes", help="File JSON chứa phân cảnh để test toàn bộ chữ")
    
    args = parser.parse_args()
    
    if args.scenes and os.path.exists(args.scenes):
        res = check_scenes_text(args.font, args.scenes)
    else:
        res = check_font_vietnamese_support(args.font, args.text)
        
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
