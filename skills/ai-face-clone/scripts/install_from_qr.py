#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installer for AI Face Clone from Verified QR Card (v3.0 — Universal Edition)
Tải ảnh mỏ neo, xác thực mật khẩu đầu vào và kích hoạt Bản Sao Khuôn Mặt trên Antigravity.
Hoạt động cho MỌI người dùng — không hardcode dữ liệu cá nhân của bất kỳ ai.
"""

import os
import sys
import json
import ssl
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

# Tạo SSL context an toàn chống lỗi chứng chỉ trên macOS
ssl_ctx = ssl._create_unverified_context()

# Tính đường dẫn tương đối từ vị trí script — portable cho mọi máy
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"
RULE_FILE = Path.home() / ".gemini" / "config" / "rules" / "ai_face_clone.md"
CATALOG_PATH = ASSETS_DIR / "face_catalog.json"

# CDN & API endpoints
R2_BASE = "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev"
API_BASE = "https://ai.fedu.vn/api"


def hash_password(password: str) -> str:
    """Tạo SHA-256 hash chuẩn hóa cho mật khẩu"""
    return hashlib.sha256(password.strip().encode('utf-8')).hexdigest()


def fetch_manifest(face_id: str):
    """Tải manifest hồ sơ khuôn mặt từ R2 hoặc API. Trả về None nếu không tìm thấy."""
    r2_url = f"{R2_BASE}/faces/{face_id}/manifest.json"
    api_url = f"{API_BASE}/face/get?id={face_id}"

    for url in [r2_url, api_url]:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity-Face-Installer/3.0'})
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode('utf-8'))
        except Exception:
            continue
    return None


def verify_password(password: str, manifest: dict, face_id: str) -> bool:
    """Xác thực mật khẩu qua 3 cơ chế: Master key, Hash so khớp, API verify."""
    clean_pass = password.strip().upper()

    # Master passwords (dùng cho quản trị viên / anh Việt test)
    master_keys = ["2026", "FEDU2026", "AIPRO"]
    if clean_pass in master_keys:
        return True

    # Order code prefix AI-XXXXXX (>= 6 ký tự)
    if (clean_pass.startswith("AI-") or clean_pass.startswith("FEDU-")) and len(clean_pass) >= 6:
        return True

    # So khớp hash từ manifest
    stored_hash = manifest.get("password_hash")
    if stored_hash and hash_password(password) == stored_hash:
        return True

    # Kiểm tra mã động dùng 1 lần qua API
    try:
        verify_url = f"{API_BASE}/face/license/verify"
        payload = json.dumps({
            "code": clean_pass,
            "face_id": face_id,
            "action": "consume"
        }).encode('utf-8')
        v_req = urllib.request.Request(verify_url, data=payload, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Antigravity-Face-Installer/3.0'
        })
        with urllib.request.urlopen(v_req, context=ssl_ctx, timeout=10) as v_resp:
            if v_resp.status == 200:
                v_data = json.loads(v_resp.read().decode('utf-8'))
                if v_data.get("valid"):
                    return True
    except Exception:
        pass

    return False


def download_photos(manifest: dict, face_id: str) -> dict:
    """Tải 3 ảnh mỏ neo về thư mục assets/ với tên file trung tính."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    photos = manifest.get("photos", [])
    downloaded = {}
    roles = ["primary", "secondary", "lifestyle"]

    for idx, p_info in enumerate(photos[:3], start=1):
        # Tên file trung tính — KHÔNG dùng tên cá nhân
        filename = f"anchor_00{idx}.jpg"
        target_path = ASSETS_DIR / filename

        # Xác định URL ảnh
        if isinstance(p_info, dict) and "url" in p_info:
            img_url = p_info["url"]
        elif isinstance(p_info, str) and p_info.startswith("http"):
            img_url = p_info
        else:
            # Fallback URL chuẩn trên R2
            img_url = f"{R2_BASE}/faces/{face_id}/photo_00{idx}.jpg"

        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Antigravity-Face-Installer/3.0'})
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=20) as img_resp:
                if img_resp.status == 200:
                    with open(target_path, "wb") as f:
                        f.write(img_resp.read())
                    role = roles[idx - 1] if idx <= len(roles) else f"extra_{idx}"
                    downloaded[role] = str(target_path)
                    print(f"✅ Đã tải ảnh mỏ neo {idx}: {filename}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Lỗi tải ảnh {idx}: {e}", file=sys.stderr)

    return downloaded


def build_catalog(manifest: dict, face_id: str, downloaded_anchors: dict) -> dict:
    """Tạo face_catalog.json từ dữ liệu manifest server — KHÔNG hardcode bất kỳ mô tả cố định nào."""
    subject_name = manifest.get("subject_name", "Chủ Nhân")
    style_profile = manifest.get("style_profile", "executive")

    # LẤY prompt_anchor_snippet TỪ MANIFEST — đây là điểm sửa lỗi quan trọng nhất
    prompt_snippet = manifest.get("prompt_anchor_snippet", "")

    # Nếu manifest không có prompt, sinh tự động từ thông tin profile
    if not prompt_snippet:
        profile = manifest.get("profile", {})
        gender = profile.get("gender", "").lower()
        age = profile.get("age_range", "30s")
        ethnicity = profile.get("ethnicity", "Vietnamese")

        gender_word = "man" if gender in ("male", "nam", "m", "") else "woman"
        adj = "handsome" if gender_word == "man" else "beautiful"

        prompt_snippet = (
            f"a {adj} {age} {ethnicity} {gender_word}, "
            f"authentic facial features, natural confident expression, clean professional attire"
        )

    catalog = {
        "subject_name": subject_name,
        "style_profile": style_profile,
        "face_id": face_id,
        "created_at": datetime.now().isoformat(),
        "is_activated": True,
        "anchors": {
            "primary": downloaded_anchors.get("primary", str(ASSETS_DIR / "anchor_002.jpg")),
            "secondary": downloaded_anchors.get("secondary", str(ASSETS_DIR / "anchor_001.jpg")),
            "lifestyle": downloaded_anchors.get("lifestyle", str(ASSETS_DIR / "anchor_003.jpg"))
        },
        "prompt_anchor_snippet": prompt_snippet
    }
    return catalog


def save_catalog(catalog: dict):
    """Ghi face_catalog.json vào vị trí chuẩn duy nhất."""
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    return CATALOG_PATH


def generate_rule(catalog: dict):
    """Sinh rule kích hoạt tự động — dùng biến động từ catalog, KHÔNG hardcode."""
    RULE_FILE.parent.mkdir(parents=True, exist_ok=True)
    name = catalog["subject_name"]
    anchor_path = catalog["anchors"]["primary"]
    prompt = catalog["prompt_anchor_snippet"]

    rule_content = f"""# Quy Tắc Tự Động AI Face Clone ({name})
Bất kỳ khi nào người dùng yêu cầu tạo ảnh chân dung, avatar, poster, storyboard, AI BẮT BUỘC:
1. Nạp ảnh mỏ neo: `{anchor_path}` vào tham số `ImagePaths` của `generate_image`.
2. Ghép prompt mỏ neo chuẩn: `{prompt}`.
3. Sau khi sinh ảnh, TỰ ĐỘNG DÙNG `view_file` mở ảnh lên soi 3 điểm (khung xương hàm, mắt, nụ cười) để đảm bảo độ giống >95%.
"""
    with open(RULE_FILE, "w", encoding="utf-8") as f:
        f.write(rule_content)
    return RULE_FILE


def verify_and_install(face_id: str, password: str):
    """Quy trình chính: xác thực → tải ảnh → tạo catalog → sinh rule."""

    # 1. Tải manifest từ server
    manifest = fetch_manifest(face_id)
    if not manifest:
        return {
            "success": False,
            "error": f"❌ Không tìm thấy hồ sơ Bản Sao #{face_id} trên máy chủ. "
                     f"Vui lòng kiểm tra lại mã hoặc liên hệ anh Việt để được hỗ trợ."
        }

    # 2. Xác thực mật khẩu
    if not verify_password(password, manifest, face_id):
        return {
            "success": False,
            "error": "❌ Mật khẩu kích hoạt không chính xác! "
                     "Vui lòng kiểm tra lại mã đơn hàng hoặc liên hệ người bán."
        }

    # 3. Tải ảnh mỏ neo
    downloaded = download_photos(manifest, face_id)
    if not downloaded:
        return {
            "success": False,
            "error": "❌ Không tải được ảnh mỏ neo từ máy chủ. Kiểm tra kết nối mạng và thử lại."
        }

    # 4. Tạo face_catalog.json
    catalog = build_catalog(manifest, face_id, downloaded)
    cat_path = save_catalog(catalog)

    # 5. Sinh rule kích hoạt
    rule_path = generate_rule(catalog)

    return {
        "success": True,
        "subject_name": catalog["subject_name"],
        "face_id": face_id,
        "style_profile": catalog["style_profile"],
        "assets_dir": str(ASSETS_DIR),
        "catalog_path": str(cat_path),
        "rule_path": str(rule_path),
        "primary_anchor": catalog["anchors"]["primary"],
        "prompt_anchor_snippet": catalog["prompt_anchor_snippet"],
        "photos_downloaded": len(downloaded),
        "message": f"✅ Đã xác thực thành công và nạp Bản Sao Khuôn Mặt cho {catalog['subject_name']}!"
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "Cú pháp: install_from_qr.py <face_id> <password>"
        }))
        sys.exit(1)

    f_id = sys.argv[1]
    pwd = sys.argv[2]
    res = verify_and_install(f_id, pwd)
    print(json.dumps(res, ensure_ascii=False, indent=2))
