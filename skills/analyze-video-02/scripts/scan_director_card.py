#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Director License Card (QR Code) Scanner
Tự động phát hiện và bóc tách dữ liệu từ Thẻ Kích Hoạt AI Đạo Diễn khi học viên ném ảnh vào chat.
"""

import os
import sys
import json

def scan_image_qr(image_path):
    if not os.path.exists(image_path):
        return {"success": False, "error": f"File không tồn tại: {image_path}"}

    try:
        import cv2
        img = cv2.imread(image_path)
        if img is not None:
            detector = cv2.QRCodeDetector()
            val, pts, qrcode = detector.detectAndDecode(img)
            if val:
                return parse_payload(val)
            
            # Thử tăng tương phản grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            val, pts, qrcode = detector.detectAndDecode(gray)
            if val:
                return parse_payload(val)
    except Exception as e:
        pass

    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
        decoded = decode(Image.open(image_path))
        if decoded:
            val = decoded[0].data.decode('utf-8')
            return parse_payload(val)
    except Exception:
        pass

    return {"success": False, "error": "Không tìm thấy mã QR trên ảnh Thẻ Kích Hoạt."}

def parse_payload(payload_str):
    try:
        data = json.loads(payload_str)
        return {
            "success": True,
            "data": data,
            "skill": data.get("skill", "analyze-video-02"),
            "name": data.get("name", "Học Viên FEDU"),
            "product": data.get("product", "Director Shot Notebook Pro"),
            "default_pass": data.get("default_pass", "")
        }
    except Exception:
        return {"success": True, "raw_payload": payload_str}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Thiếu đường dẫn ảnh thẻ"}))
        sys.exit(1)
        
    res = scan_image_qr(sys.argv[1])
    print(json.dumps(res, ensure_ascii=False, indent=2))
