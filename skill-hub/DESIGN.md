# Thiết Kế Kiến Trúc Trang Skill Hub

## 4A. PHÂN LOẠI SKILL

**PUBLIC** (dành cho học viên — từ GitHub repo `AI-Skill`):
1. analyze-video
2. phan-tich-podcast-youtube
3. tai-nhac
4. nen1080
5. bang-phan-canh
6. 3-tang
7. loc
8. tao-slide-pro
9. sua-phu-de-capcut
10. nhan-ban-web
11. miss-sale-page
12. create-landing-page
13. toi-uu-prompt
14. mo-phong-thuc-chien
15. vietmac-voice
16. ugc-auto-edit
17. xem-anh-moi-nhat
18. telegram-dispatcher

**PRIVATE** (chỉ admin anh Việt — từ `~/.gemini/config/skills/`):
1. architect
2. team
3. re-nhanh
4. nghiem-thu
5. master-vault
6. agy-cleanup
7. codegraph
8. ghi-web
9. html
10. nguyen-viet-voice

## 4B. CƠ CHẾ "CÀI → CHẠY → QUÊN" (Ephemeral Skill)
- Khi user bấm "Cài & Chạy" trên web → copy lệnh curl/bash vào clipboard.
- Lệnh đó sẽ: clone skill → copy vào `~/.gemini/config/skills/` → thông báo xong.
- Sau khi dùng xong, user gõ "Gỡ skill [tên]" → AI xóa folder skill đó (hoặc thông qua script `uninstall.sh`).
- Mục đích: không chiếm bộ nhớ context khi không cần.

## 4C. TRANG WEB fedu.vn/skill/
- **Loại trang**: Single-page HTML/CSS/JS (static, deploy Cloudflare Pages).
- **Thiết kế**: Responsive mobile-first.
- **Layout**:
  - Hero: "🚀 Kho Kỹ Năng AI — FEDU Ecosystem"
  - Grid cards: mỗi skill 1 card (icon, tên, mô tả ngắn, nút CÀI).
  - Nút CÀI mỗi skill: copy lệnh curl install riêng lẻ vào clipboard.
  - Nút "CÀI TẤT CẢ": copy lệnh curl install.sh tổng.
  - Filter: Tất cả | Video | Marketing | Developer
- **Login**: Nhập password `0070` → hiện thêm các skill PRIVATE + nút "Cài & Chạy ngay" (chạy thẳng lệnh).
- **Style**:
  - Font: system font stack (không load Google Fonts nặng).
  - Chữ: Vietnamese Sentence case (KHÔNG Title Case).
  - Màu sắc: Charcoal Slate palette (dark theme).
