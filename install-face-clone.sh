#!/bin/bash
# ==============================================================================
# AI FACE CLONE PRO - 1-CLICK DEDICATED INSTALLER (macOS / Linux)
# ==============================================================================

set -e

REPO_URL="https://github.com/vietndj/AI-Skill.git"
TARGET_SKILLS_DIR="$HOME/.gemini/config/skills"
TARGET_SKILL_DIR="$TARGET_SKILLS_DIR/ai-face-clone"
TEMP_CLONE_DIR="$HOME/.gemini/.ai-skill-temp"
AVATAR_DIR="$HOME/.gemini/avatar_photos"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

echo ""
echo -e "${CYAN}======================================================================${NC}"
echo -e "${MAGENTA} 👤 CÀI ĐẶT SKILL: AI FACE CLONE PRO CHO ANTIGRAVITY${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""

# 1. Tạo thư mục cấu hình và thư mục ảnh
mkdir -p "$TARGET_SKILLS_DIR"
mkdir -p "$AVATAR_DIR"

# 2. Tải hoặc cập nhật từ GitHub
if [ -d "$TEMP_CLONE_DIR/.git" ]; then
    echo -e "${BLUE}🔄 Đang đồng bộ cập nhật từ GitHub repo...${NC}"
    cd "$TEMP_CLONE_DIR"
    git fetch --all --quiet
    git reset --hard origin/main --quiet || git pull --quiet
else
    echo -e "${BLUE}📥 Đang tải gói kỹ năng AI Face Clone...${NC}"
    rm -rf "$TEMP_CLONE_DIR"
    git clone --depth 1 "$REPO_URL" "$TEMP_CLONE_DIR" --quiet
fi

# 3. Đồng bộ skill ai-face-clone
echo -e "${BLUE}📂 Đang thiết lập cấu hình skill vào Antigravity...${NC}"
mkdir -p "$TARGET_SKILL_DIR"
cp -rf "$TEMP_CLONE_DIR"/skills/ai-face-clone/* "$TARGET_SKILL_DIR"/

# 4. Kiểm tra quyền thực thi script
chmod +x "$TARGET_SKILL_DIR"/scripts/*.py 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ CÀI ĐẶT THÀNH CÔNG SKILL AI FACE CLONE PRO!${NC}"
echo -e "${YELLOW}👉 Thư mục ảnh chân dung mỏ neo của bạn:${NC} ${AVATAR_DIR}"
echo ""
echo -e "${CYAN}----------------------------------------------------------------------${NC}"
echo -e "${GREEN}🎯 HƯỚNG DẪN 3 BƯỚC SỬ DỤNG NGAY:${NC}"
echo -e " 1. Copy 3-5 ảnh chân dung rõ mặt của bạn vào thư mục: ${YELLOW}${AVATAR_DIR}${NC}"
echo -e " 2. Khởi động lại hoặc mở Antigravity IDE."
echo -e " 3. Mở khung chat Antigravity và gõ bất kỳ câu lệnh nào:"
echo -e "    - ${MAGENTA}'Setup hồ sơ khuôn mặt của tôi'${NC}"
echo -e "    - ${MAGENTA}'Tạo cho tôi ảnh đang ngồi làm việc bàn gỗ'${NC}"
echo -e "    - ${MAGENTA}'Làm avatar chuyên gia phong cách studio'${NC}"
echo -e "    - ${MAGENTA}'Sinh ảnh storyboard cho kịch bản sau, nhân vật là tôi'${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""
