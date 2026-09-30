#!/bin/bash
# ==============================================================================
# AI SKILL - 1-CLICK DEDICATED INSTALLER (macOS / Linux)
# ==============================================================================

set -e

REPO_URL="https://github.com/vietndj/AI-Skill.git"
TARGET_SKILLS_DIR="$HOME/.gemini/config/skills"
TARGET_SKILL_DIR="$TARGET_SKILLS_DIR/ai-face-clone"
TEMP_CLONE_DIR="$HOME/.gemini/.ai-skill-temp"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

echo ""
echo -e "${CYAN}======================================================================${NC}"
echo -e "${MAGENTA} 🚀 CÀI ĐẶT SKILL: ai-face-clone CHO ANTIGRAVITY${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""

# 1. Tạo thư mục cấu hình
mkdir -p "$TARGET_SKILLS_DIR"

# 2. Tải hoặc cập nhật từ GitHub
if [ -d "$TEMP_CLONE_DIR/.git" ]; then
    echo -e "${BLUE}🔄 Đang đồng bộ cập nhật từ GitHub repo...${NC}"
    cd "$TEMP_CLONE_DIR"
    git fetch --all --quiet
    git reset --hard origin/main --quiet || git pull --quiet
else
    echo -e "${BLUE}📥 Đang tải gói kỹ năng...${NC}"
    rm -rf "$TEMP_CLONE_DIR"
    git clone --depth 1 "$REPO_URL" "$TEMP_CLONE_DIR" --quiet
fi

# 3. Đồng bộ skill
echo -e "${BLUE}📂 Đang thiết lập cấu hình skill vào Antigravity...${NC}"
mkdir -p "$TARGET_SKILL_DIR"
cp -rf "$TEMP_CLONE_DIR"/skills/ai-face-clone/* "$TARGET_SKILL_DIR"/

# 4. Kiểm tra quyền thực thi script
chmod +x "$TARGET_SKILL_DIR"/scripts/*.py 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ CÀI ĐẶT THÀNH CÔNG SKILL ai-face-clone!${NC}"
echo ""
