#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Render & Prompt Generator for AI Face Clone
Tạo và xuất các kịch bản Prompt chuẩn điện ảnh theo 4 phong cách kinh điển.
"""

import os
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_CATALOG = SKILL_DIR / "assets" / "face_catalog.json"

STYLES = {
    "1": {
        "key": "studio_expert",
        "title": "1. Avatar Chuyên Gia / Studio Executive",
        "aspect": "1:1",
        "prompt": "{anchor}, {attire_formal}, looking confidently into the camera, gentle warm smile, clean minimalist studio lighting with soft rim light, 85mm f/1.4 lens bokeh, ultra-detailed skin texture, Hasselblad medium format quality"
    },
    "2": {
        "key": "deep_work",
        "title": "2. Bàn Gỗ Tự Nhiên / Deep Work Tech",
        "aspect": "16:9",
        "prompt": "{anchor}, {attire_deepwork}, focused working in front of a sleek setup at a solid rustic walnut wooden desk, soft warm golden hour sunlight streaming through tall modern window, lush green houseplants in background, cozy minimalist tech aesthetic"
    },
    "3": {
        "key": "outdoor_sport",
        "title": "3. Thể Thao / Runner Marathon Đón Bình Minh",
        "aspect": "9:16",
        "prompt": "{anchor}, {attire_athletic}, dynamic running stride at sunrise in a modern urban park, golden morning mist, glistening light sweat on skin, energetic powerful athletic physique, motion-freeze cinematic shutter"
    },
    "4": {
        "key": "nature_zen",
        "title": "4. Thiền Định / Zen Áo Đũi Thiên Nhiên",
        "aspect": "16:9",
        "prompt": "{anchor}, {attire_zen}, standing calmly on a rustic wooden bridge over a serene misty mountain lake, soft diffused morning overcast light, peaceful contemplative gaze, cinematic 35mm film mood, earthy color palette"
    }
}

def load_catalog(path=None):
    cat_file = Path(path or DEFAULT_CATALOG)
    if not cat_file.exists():
        return None
    with open(cat_file, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Sinh Prompt kiểm thử cho AI Face Clone")
    parser.add_argument("--catalog", type=str, default=str(DEFAULT_CATALOG), help="Đường dẫn face_catalog.json")
    args = parser.parse_args()

    data = load_catalog(args.catalog)
    # Detect uninitialized catalog (is_activated == false or empty subject_name)
    if not data or (data.get("is_activated") == False and not data.get("subject_name")):
        print("⚠️ Chưa tìm thấy face_catalog.json hoặc hồ sơ chưa được kích hoạt!")
        print("👉 Vui lòng kích hoạt kỹ năng AI Face Clone trước (ném Thẻ Kích Hoạt vào chat hoặc chạy setup).")
        anchor = "a person, authentic facial features, natural confident expression, clean professional attire"
        attire_formal = "wearing a tailored executive suit with open-collar shirt"
        attire_deepwork = "wearing a tailored dark charcoal blazer over crisp white crewneck tee"
        attire_athletic = "wearing a high-performance running singlet and sports smartwatch"
        attire_zen = "wearing a light gray breathable linen collarless shirt"
        photos = []
    elif "profile" in data:
        # Nested schema (from setup_face_profile.py)
        prof = data["profile"]
        anchor = prof.get("prompt_anchor_snippet", "")
        attires = prof.get("standard_attires", {})
        attire_formal = attires.get("formal_expert", "wearing a tailored executive suit")
        attire_deepwork = attires.get("deep_work_tech", "wearing a tailored charcoal blazer over white tee")
        attire_athletic = attires.get("athletic_runner", "wearing athletic runner apparel")
        attire_zen = attires.get("nature_eco_zen", "wearing a light gray linen collarless shirt")
        photos = data.get("dataset_metadata", {}).get("reference_photos", [])
    else:
        # Flat schema (from install_from_qr.py)
        anchor = data.get("prompt_anchor_snippet", "")
        anchors = data.get("anchors", {})
        photos = [v for v in anchors.values() if v]
        attire_formal = "wearing a tailored executive suit with open-collar shirt"
        attire_deepwork = "wearing a tailored dark charcoal blazer over crisp white crewneck tee"
        attire_athletic = "wearing a high-performance running singlet and sports smartwatch"
        attire_zen = "wearing a light gray breathable linen collarless shirt"

    print("\n" + "=" * 70)
    print("🎨 BỘ 4 PROMPT TEST THỰC CHIẾN - AI FACE CLONE PRO")
    print("=" * 70)
    print(f"👤 Mỏ neo nhân dạng: {anchor}")
    print(f"📸 Ảnh tham chiếu mỏ neo ({len(photos)} ảnh): {photos}")
    print("=" * 70 + "\n")

    for idx, s in STYLES.items():
        formatted_prompt = s["prompt"].format(
            anchor=anchor,
            attire_formal=attire_formal,
            attire_deepwork=attire_deepwork,
            attire_athletic=attire_athletic,
            attire_zen=attire_zen
        )
        print(f"✨ {s['title']} (Tỉ lệ: {s['aspect']})")
        print(f"   Prompt: \"{formatted_prompt}\"")
        print("-" * 70)

if __name__ == "__main__":
    main()
