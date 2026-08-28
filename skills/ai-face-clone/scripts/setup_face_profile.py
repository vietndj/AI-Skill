#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Face Profile Generator for Antigravity AI Face Clone
Tự động quét ảnh chân dung, trích xuất cấu hình và tạo face_catalog.json chuẩn hóa.
"""

import os
import sys
import json
import glob
import argparse
from pathlib import Path

DEFAULT_PHOTO_DIR = Path.home() / ".gemini" / "avatar_photos"
DEFAULT_CATALOG_PATH = DEFAULT_PHOTO_DIR / "face_catalog.json"
DEFAULT_RULE_PATH = Path.home() / ".gemini" / "config" / "rules" / "ai_face_clone.md"

def ensure_dirs():
    DEFAULT_PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_RULE_PATH.parent.mkdir(parents=True, exist_ok=True)

def find_photos(photo_dir):
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.JPG", "*.JPEG", "*.PNG", "*.WEBP")
    photos = []
    for ext in valid_exts:
        photos.extend(glob.glob(str(Path(photo_dir) / ext)))
    return sorted(list(set(photos)))

def generate_catalog(name="Chủ Nhân", gender="male", age_range="28-36", ethnicity="Vietnamese / East Asian", 
                     build="Athletic, lean runner build, upright posture", hair="Short modern textured crop, dark black hair",
                     photo_dir=None, custom_anchor=None):
    photo_dir = Path(photo_dir or DEFAULT_PHOTO_DIR).resolve()
    photos = find_photos(photo_dir)
    
    gender_word = "man" if gender.lower() in ("male", "nam", "m") else "woman"
    handsome_pretty = "handsome" if gender_word == "man" else "beautiful"
    
    if not custom_anchor:
        anchor_snippet = (
            f"a {handsome_pretty} {age_range.split('-')[0]}s {ethnicity.split('/')[0].strip()} {gender_word} "
            f"with {hair}, defined jawline, {build}, expressive dark eyes, authentic Asian facial features, clean smart attire"
        )
    else:
        anchor_snippet = custom_anchor

    attires = {
        "smart_casual_studio": "Tailored dark blazer over crisp white or black crewneck tee, minimalist aesthetic",
        "deep_work_tech": "Modern tech professional attire, premium minimalist black crewneck tee, clean smartwatch",
        "nature_eco_zen": "Light gray or ivory breathable linen collarless shirt, earthy relaxed organic aesthetic",
        "athletic_runner": "High-performance athletic running apparel, technical sportswear, lean fit gear",
        "formal_expert": "Crisp tailored executive suit with open-collar dress shirt, authoritative professional look"
    }

    catalog = {
        "profile": {
            "name": name,
            "gender": gender,
            "age_range": age_range,
            "ethnicity": ethnicity,
            "build": build,
            "hair": hair,
            "facial_features": {
                "face_shape": "Oval / defined jawline with natural contour",
                "eyes": "Expressive dark brown Asian eyes, authentic confident gaze",
                "nose": "Straight proportionate bridge",
                "mouth_smile": "Genuine warm confident smile",
                "skin": "Healthy fair-to-medium skin tone with natural micro-texture"
            },
            "standard_attires": attires,
            "prompt_anchor_snippet": anchor_snippet
        },
        "dataset_metadata": {
            "storage_dir": str(photo_dir),
            "total_images_found": len(photos),
            "reference_photos": photos[:5] if photos else []
        }
    }
    
    return catalog

def save_catalog(catalog, out_path=None):
    out_file = Path(out_path or DEFAULT_CATALOG_PATH)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    return out_file

def generate_rule_file(catalog, rule_path=None):
    rule_file = Path(rule_path or DEFAULT_RULE_PATH)
    name = catalog["profile"]["name"]
    anchor = catalog["profile"]["prompt_anchor_snippet"]
    photos = catalog["dataset_metadata"]["reference_photos"]
    photos_str = json.dumps(photos, ensure_ascii=False)
    
    rule_content = f"""# Quy Tắc Tự Động Nhân Bản Khuôn Mặt AI ({name})
- **Quy tắc tuyệt đối**: Khi sinh ảnh minh họa / avatar / mockup / poster / storyboard bằng công cụ `generate_image`, Midjourney, Flux, SDXL,... nếu kịch bản có nhân vật đại diện (hoặc nhân vật chính) -> **MẶC ĐỊNH 100% nhân vật đó chính là {name}**.
- **Hồ sơ nhân dạng (Visual Anchor)**:
  - Anchor Prompt: `{anchor}`
  - Kho ảnh tham chiếu: `{catalog["dataset_metadata"]["storage_dir"]}`
  - Ảnh mỏ neo ưu tiên (ImagePaths): `{photos_str}`
- **Quy tắc đồng nhất trang phục (Wardrobe Continuity)**:
  - Trong cùng một kịch bản/storyboard, nhân vật **BẮT BUỘC mặc CÙNG MỘT LOẠI QUẦN ÁO** xuyên suốt tất cả các cảnh.
"""
    with open(rule_file, "w", encoding="utf-8") as f:
        f.write(rule_content)
    return rule_file

def main():
    parser = argparse.ArgumentParser(description="Thiết lập hồ sơ khuôn mặt AI cho Antigravity")
    parser.add_argument("--name", type=str, default="Chủ Nhân", help="Tên chủ nhân hồ sơ")
    parser.add_argument("--gender", type=str, default="male", choices=["male", "female", "nam", "nu"], help="Giới tính")
    parser.add_argument("--age", type=str, default="28-36", help="Độ tuổi (ví dụ: 30-35)")
    parser.add_argument("--photos-dir", type=str, default=str(DEFAULT_PHOTO_DIR), help="Thư mục chứa ảnh chân dung mẫu")
    parser.add_argument("--anchor", type=str, default=None, help="Prompt anchor tùy biến")
    parser.add_argument("--out", type=str, default=str(DEFAULT_CATALOG_PATH), help="Đường dẫn lưu catalog JSON")
    
    args = parser.parse_args()
    ensure_dirs()
    
    print("=" * 60)
    print("🚀 ĐANG THIẾT LẬP HỒ SƠ KHUÔN MẶT AI CHO ANTIGRAVITY")
    print("=" * 60)
    
    photo_dir = Path(args.photos_dir).resolve()
    photos = find_photos(photo_dir)
    print(f"📂 Thư mục ảnh: {photo_dir}")
    print(f"📸 Tìm thấy {len(photos)} ảnh chân dung mỏ neo.")
    
    if len(photos) == 0:
        print("⚠️ CẢNH BÁO: Chưa tìm thấy ảnh nào trong thư mục.")
        print(f"👉 Vui lòng copy 3-5 ảnh chân dung rõ mặt của bạn vào: {photo_dir}")
    
    catalog = generate_catalog(
        name=args.name,
        gender=args.gender,
        age_range=args.age,
        photo_dir=photo_dir,
        custom_anchor=args.anchor
    )
    
    cat_file = save_catalog(catalog, args.out)
    rule_file = generate_rule_file(catalog)
    
    print(f"✅ Đã lưu Face Catalog tại: {cat_file}")
    print(f"✅ Đã tạo Rule tự động kích hoạt tại: {rule_file}")
    print(f"🎯 Prompt Anchor mặc định: {catalog['profile']['prompt_anchor_snippet']}")
    print("=" * 60)
    print("🎉 HOÀN TẤT! Antigravity đã sẵn sàng tạo ảnh chuẩn khuôn mặt của bạn.")

if __name__ == "__main__":
    main()
