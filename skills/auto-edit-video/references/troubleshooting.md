# Xử Lý Sự Cố Auto Edit Video Skill

## ❌ "Template not found" khi chạy generate_studio.py

**Nguyên nhân:** Script không tìm thấy file `studio_template.html`
**Cách sửa:**
```bash
# Kiểm tra file template tồn tại
ls ~/.gemini/config/skills/auto-edit-video/resources/studio_template.html

# Nếu thiếu, copy lại từ gói gốc
```

## ❌ Font không hiển thị đúng trong Studio HTML

**Nguyên nhân:** File font bị thiếu hoặc tên file không khớp
**Cách sửa:**
```bash
# Kiểm tra đủ 21 font
ls ~/.gemini/config/skills/auto-edit-video/resources/fonts/ | wc -l
# Kết quả phải là 21
```

## ❌ FFmpeg not found

**Nguyên nhân:** FFmpeg chưa cài hoặc không trong PATH
**Cách sửa:**
```bash
brew install ffmpeg
# Kiểm tra
which ffmpeg
ffmpeg -version
```

## ❌ Video render bị lỗi / Chrome path sai

**Nguyên nhân:** Puppeteer không tìm thấy Google Chrome
**Cách sửa:**
```bash
# Kiểm tra Chrome đã cài
ls /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

# Nếu Chrome ở vị trí khác:
export CHROME_PATH="/path/to/your/Google Chrome"
```

## ❌ Studio HTML mở trắng / lỗi JS

**Nguyên nhân:** File bị hỏng khi generate hoặc trình duyệt chặn file local
**Cách sửa:**
1. Kiểm tra file HTML có nội dung: `wc -l studio_*.html` (phải > 2000 dòng)
2. Mở bằng Chrome (không phải Safari) vì Safari có thể chặn clipboard API
3. Thử generate lại: chạy lại lệnh `generate_studio.py`

## ❌ Copy JSON không hoạt động

**Nguyên nhân:** Trình duyệt chặn Clipboard API cho file local
**Cách sửa:**
- Mở Chrome, gõ `chrome://flags`, tìm "Async Clipboard API" và bật
- Hoặc: khi bấm Copy, nếu clipboard bị chặn sẽ hiện hộp thoại prompt() để copy thủ công

## ❌ Người dùng trên máy khác không thấy kỹ năng

**Nguyên nhân:** Thư mục skill chưa đúng vị trí
**Cách kiểm tra:**
```bash
# Phải nằm trong 1 trong 2 vị trí:
# Global (cho tất cả project):
ls ~/.gemini/config/skills/auto-edit-video/SKILL.md

# Hoặc Project-specific (cho 1 project):
ls .agents/skills/auto-edit-video/SKILL.md
```
