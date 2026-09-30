#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./uninstall.sh [skill-name]"
    exit 1
fi
SKILL_DIR="$HOME/.gemini/config/skills/$1"
if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    echo "✅ Đã gỡ bỏ skill: $1"
else
    echo "❌ Không tìm thấy skill: $1"
fi
