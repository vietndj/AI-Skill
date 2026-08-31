#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
License Verification & One-Time Password Manager for Video Analysis 02
Quản lý khóa bản quyền và kích hoạt 1 lần cho người dùng mới.
"""

import sys
import os
import json
import ssl
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

ssl_ctx = ssl._create_unverified_context()

SKILL_DIR = Path.home() / ".gemini" / "config" / "skills" / "analyze-video-02"
ASSETS_DIR = SKILL_DIR / "assets"
LICENSE_FILE = ASSETS_DIR / "license.json"

MASTER_PASSWORDS = [
    "FEDU2026",
    "DIRECTOR2026",
    "VIETMAC",
    "AIPRO",
    "2026",
    "FEDUVIDEO"
]

def hash_code(code: str) -> str:
    """Tạo SHA-256 hash chuẩn cho mật khẩu."""
    return hashlib.sha256(code.strip().upper().encode('utf-8')).hexdigest()

def check_license_status() -> dict:
    """Kiểm tra xem kỹ năng đã được kích hoạt trên máy hay chưa."""
    if not LICENSE_FILE.exists():
        return {"is_activated": False}
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception:
        return {"is_activated": False}

def activate_license(password_or_code: str, user_name: str = "Học Viên FEDU") -> dict:
    """Xác thực và kích hoạt bản quyền 1 lần."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    clean_code = password_or_code.strip().upper()
    
    is_valid = False
    activation_type = "offline_master"
    
    # 1. Kiểm tra Master Passwords
    if clean_code in MASTER_PASSWORDS:
        is_valid = True
        activation_type = "master_key"
    elif (clean_code.startswith("AI-") or clean_code.startswith("FEDU-")) and len(clean_code) >= 6:
        is_valid = True
        activation_type = "order_code"
    else:
        # 2. Kiểm tra API Online nếu có
        try:
            api_url = "https://ai.fedu.vn/api/video/license/verify"
            payload = json.dumps({"code": clean_code, "product": "analyze-video-02", "action": "consume"}).encode('utf-8')
            req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=5) as resp:
                if resp.status == 200:
                    res_data = json.loads(resp.read().decode('utf-8'))
                    if res_data.get("valid"):
                        is_valid = True
                        activation_type = "cloud_api"
        except Exception:
            pass

    if not is_valid:
        return {
            "success": False,
            "error": "❌ Mật khẩu kích hoạt không chính xác! Vui lòng kiểm tra lại mã đơn hàng hoặc liên hệ anh Việt (FEDU) để nhận mã mở khóa."
        }

    # Lưu trạng thái kích hoạt vĩnh viễn
    license_data = {
        "is_activated": True,
        "license_code": clean_code,
        "user_name": user_name,
        "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "activation_type": activation_type
    }
    
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(license_data, f, ensure_ascii=False, indent=2)
        
    return {
        "success": True,
        "user_name": user_name,
        "activated_at": license_data["activated_at"],
        "message": f"🎉 CHÚC MỪNG BẠN ĐÃ KÍCH HOẠT THÀNH CÔNG GÓI PHÂN TÍCH VIDEO 02 TRỌN ĐỜI!"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Kiểm tra trạng thái
        status = check_license_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
        sys.exit(0)
        
    code_input = sys.argv[1]
    name_input = sys.argv[2] if len(sys.argv) > 2 else "Học Viên FEDU"
    res = activate_license(code_input, name_input)
    print(json.dumps(res, ensure_ascii=False, indent=2))
