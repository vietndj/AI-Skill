#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wow Engine (Bộ máy gán hiệu ứng bất ngờ Wow Moments)
Dành cho UGC pipeline của anh Việt.
"""

import json
import argparse
import random

PRESETS_DB = {
    "DAILY_LIFE": [
        {"id": "emoji_burst", "name": "Emoji explosion at laugh", "effect": "emoji_burst", "intensity": 0.8},
        {"id": "freeze_zoom", "name": "Freeze frame + slow zoom", "effect": "freeze_zoom", "intensity": 0.7},
        {"id": "color_flash", "name": "Brief warm color flash", "effect": "color_flash", "intensity": 0.6},
        {"id": "shake_zoom", "name": "Quick camera shake + zoom", "effect": "shake_zoom", "intensity": 0.9},
        {"id": "sparkle_trail", "name": "Sparkle particles", "effect": "sparkle_trail", "intensity": 0.5}
    ],
    "NATURE_AMBIENT": [
        {"id": "parallax_drift", "name": "Text floating opposite", "effect": "parallax_drift", "intensity": 0.4},
        {"id": "light_leak", "name": "Film light leak overlay", "effect": "light_leak", "intensity": 0.6},
        {"id": "golden_bloom", "name": "Warm bloom/glow", "effect": "golden_bloom", "intensity": 0.5},
        {"id": "slow_reveal", "name": "Cinematic letterbox open", "effect": "slow_reveal", "intensity": 0.7},
        {"id": "mist_overlay", "name": "Subtle fog/mist layer", "effect": "mist_overlay", "intensity": 0.4}
    ],
    "EVENT": [
        {"id": "beat_flash", "name": "Flash cut synced to peaks", "effect": "beat_flash", "intensity": 0.9},
        {"id": "speed_ramp", "name": "Slow-mo highlight", "effect": "speed_ramp", "intensity": 0.8},
        {"id": "glitch_cut", "name": "Digital glitch transition", "effect": "glitch_cut", "intensity": 0.7},
        {"id": "freeze_burst", "name": "Freeze + particle burst", "effect": "freeze_burst", "intensity": 0.9},
        {"id": "split_screen", "name": "Brief split-screen montage", "effect": "split_screen", "intensity": 0.8}
    ],
    "LIVE_TALK": [
        {"id": "pull_quote", "name": "Full screen quote card", "effect": "pull_quote", "intensity": 0.8},
        {"id": "focus_blur", "name": "Background blur", "effect": "focus_blur", "intensity": 0.6},
        {"id": "zoom_reaction", "name": "Subtle zoom on reaction", "effect": "zoom_reaction", "intensity": 0.5},
        {"id": "highlight_glow", "name": "Glow highlight words", "effect": "highlight_glow", "intensity": 0.7},
        {"id": "lower_third_pop", "name": "Animated speaker name tag", "effect": "lower_third_pop", "intensity": 0.8}
    ]
}

def get_wow_preset(catalog: str) -> dict:
    catalog = catalog.upper()
    if catalog not in PRESETS_DB:
        catalog = "DAILY_LIFE"
        
    presets = PRESETS_DB[catalog]
    selected = random.choice(presets)
    
    # Timing logic will be applied in Remotion
    selected["timing_mode"] = "peak_audio" if catalog in ["DAILY_LIFE", "EVENT"] else "random_interval"
    
    return {
        "catalog": catalog,
        "wow_preset": selected
    }

def main():
    parser = argparse.ArgumentParser(description="Wow Engine cho UGC")
    parser.add_argument("--catalog", required=True, help="Tên Catalog (DAILY_LIFE, NATURE_AMBIENT, ...)")
    args = parser.parse_args()
    
    result = get_wow_preset(args.catalog)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
