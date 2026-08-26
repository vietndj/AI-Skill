#!/bin/bash
# ==============================================================================
# AI SKILL - ONE-CLICK INSTALLER (macOS / Linux)
# ==============================================================================

set -e

REPO_URL="https://github.com/vietndj/AI-Skill.git"
TARGET_SKILLS_DIR="$HOME/.gemini/config/skills"
TEMP_CLONE_DIR="$HOME/.gemini/.ai-skill-temp"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}======================================================${NC}"
echo -e "${GREEN} 🚀 CÀI ĐẶT BỘ KỸ NĂNG ANTIGRAVITY AI - AI SKILL${NC}"
echo -e "${CYAN}======================================================${NC}"
echo ""

# 1. Tạo thư mục cấu hình nếu chưa có
mkdir -p "$TARGET_SKILLS_DIR"

# 2. Tải hoặc cập nhật từ GitHub
if [ -d "$TEMP_CLONE_DIR/.git" ]; then
    echo -e "${BLUE}🔄 Đang đồng bộ cập nhật phiên bản mới nhất từ GitHub...${NC}"
    cd "$TEMP_CLONE_DIR"
    git fetch --all --quiet
    git reset --hard origin/main --quiet || git pull --quiet
else
    echo -e "${BLUE}📥 Đang tải bộ kỹ năng về máy...${NC}"
    rm -rf "$TEMP_CLONE_DIR"
    git clone --depth 1 "$REPO_URL" "$TEMP_CLONE_DIR" --quiet
fi

# 3. Đồng bộ các thư mục kỹ năng vào Antigravity
echo -e "${BLUE}📂 Đang sao chép các kỹ năng vào thư mục Antigravity...${NC}"
cp -rf "$TEMP_CLONE_DIR"/skills/* "$TARGET_SKILLS_DIR"/

# 4. Kiểm tra số lượng kỹ năng đã cài
COUNT=$(ls -d "$TARGET_SKILLS_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo -e "${GREEN}✅ CÀI ĐẶT THÀNH CÔNG! ĐÃ ĐỒNG BỘ ${COUNT} KỸ NĂNG VÀO HỆ THỐNG.${NC}"
echo -e "${YELLOW}👉 Vị trí lưu trữ: ${TARGET_SKILLS_DIR}${NC}"
echo ""
echo -e "${CYAN}------------------------------------------------------${NC}"
echo -e "${GREEN}💡 CÁCH SỬ DỤNG TRÊN ANTIGRAVITY:${NC}"
echo "1. Khởi động lại hoặc mở Antigravity IDE."
echo "2. Gửi link video hoặc chat các câu lệnh thực chiến:"
echo "   - Phân tích video: 'Phân tích video này giúp tôi: <link instagram/tiktok>'"
echo "   - Phân tích podcast: 'PODCAST <link youtube>'"
echo "   - Tải nhạc: 'TAI NHAC : <link>' hoặc 'Tải nhạc bài này <link>'"
echo "   - Nén video 1080p: 'nen1080 <đường dẫn file video>'"
echo "   - Bảng phân cảnh: 'BẢNG PHÂN CẢNH cho kịch bản sau: ...'"
echo "   - Lọc văn mẫu: 'LỌC văn mẫu đoạn văn này: ...'"
echo -e "${CYAN}------------------------------------------------------${NC}"
echo ""
