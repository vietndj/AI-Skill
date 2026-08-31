#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Face Card (QR Code / AI Passport) Scanner
Quét và bóc tách dữ liệu từ Thẻ Căn Cước AI Face hoặc mã QR do học viên ném vào Antigravity.
"""

import os
import sys
import json
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path

def scan_image_qr(image_path):
    """Quét mã QR từ file ảnh sử dụng OpenCV QRCodeDetector hoặc fallback"""
    if not os.path.exists(image_path):
        return {"success": False, "error": f"File không tồn tại: {image_path}"}

    # Thử quét bằng OpenCV nếu có
    try:
        import cv2
        img = cv2.imread(image_path)
        if img is not None:
            detector = cv2.QRCodeDetector()
            val, pts, qrcode = detector.detectAndDecode(img)
            if val:
                return parse_qr_payload(val)
            
            # Thử lại với ảnh grayscale hoặc tăng tương phản
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            val, pts, qrcode = detector.detectAndDecode(gray)
            if val:
                return parse_qr_payload(val)
    except Exception as e:
        pass

    # Thử quét bằng pyzbar nếu có
    try:
        from pyzbar.pyzbar import decode
        from PIL import Image
        decoded = decode(Image.open(image_path))
        if decoded:
            val = decoded[0].data.decode('utf-8')
            return parse_qr_payload(val)
    except Exception as e:
        pass

    return {"success": False, "error": "Không tìm thấy mã QR trên ảnh. Vui lòng kiểm tra lại ảnh Thẻ Căn Cước AI."}

def parse_qr_payload(payload_str):
    """Phân tích nội dung mã QR (URL, JSON hoặc chuỗi nhận diện FEDU-FACE)"""
    payload_str = payload_str.strip()
    
    # Dạng 1: URL trực tiếp https://ai.fedu.vn/face?id=... hoặc https://...
    if payload_str.startswith("http://") or payload_str.startswith("https://"):
        parsed = urllib.parse.urlparse(payload_str)
        params = urllib.parse.parse_qs(parsed.query)
        face_id = params.get('id', [None])[0]
        if not face_id:
            # Lấy phần path cuối cùng làm ID nếu dạng /face/ID
            face_id = parsed.path.strip('/').split('/')[-1]
            
        return fetch_face_metadata(face_id, original_url=payload_str)

    # Dạng 2: Prefix FEDU-FACE:ID
    if payload_str.startswith("FEDU-FACE:"):
        face_id = payload_str.replace("FEDU-FACE:", "").strip()
        return fetch_face_metadata(face_id)

    # Dạng 3: JSON trực tiếp
    try:
        data = json.loads(payload_str)
        if "id" in data or "subject_name" in data:
            return {"success": True, "data": data}
    except Exception:
        pass

    return {"success": False, "error": f"Nội dung QR không hợp lệ: {payload_str}"}

def fetch_face_metadata(face_id, original_url=None):
    """Truy vấn metadata của bản sao từ Cloudflare R2 / Vercel API"""
    # 1. Thử lấy từ Cloudflare R2 public base
    r2_url = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/faces/{face_id}/manifest.json"
    api_url = f"https://ai.fedu.vn/api/face/get?id={face_id}"
    
    for target_url in [r2_url, api_url]:
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Antigravity-Face-Scanner/2.4'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return {
                        "success": True,
                        "face_id": face_id,
                        "data": data,
                        "requires_password": bool(data.get("password_hash") or data.get("is_locked", True))
                    }
        except Exception:
            continue

    return {
        "success": False,
        "face_id": face_id,
        "error": f"Không thể tải hồ sơ #{face_id} từ máy chủ. Vui lòng kiểm tra lại kết nối mạng."
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Thiếu đường dẫn file ảnh thẻ QR"}))
        sys.exit(1)
        
    img_path = sys.argv[1]
    result = scan_image_qr(img_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
