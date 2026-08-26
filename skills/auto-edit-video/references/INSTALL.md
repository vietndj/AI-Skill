# Hướng Dẫn Cài Đặt: Auto Edit Video Skill

## Yêu Cầu Hệ Thống

| Thành phần | Phiên bản tối thiểu | Kiểm tra bằng lệnh |
|:-----------|:--------------------|:--------------------|
| macOS | 12+ (Monterey) | `sw_vers` |
| Google Antigravity | Bản mới nhất | `agy --version` |
| Python 3 | 3.9+ | `python3 --version` |
| FFmpeg | 5.0+ | `ffmpeg -version` |
| Node.js | 18+ | `node --version` |
| Google Chrome | Bản mới nhất | Kiểm tra trong `/Applications/` |

## Cài Đặt Nhanh (3 Bước)

### Bước 1: Copy thư mục skill

```bash
# Giải nén hoặc copy thư mục auto-edit-video vào đúng vị trí:
cp -r auto-edit-video/ ~/.gemini/config/skills/auto-edit-video/
```

### Bước 2: Cài dependencies (nếu chưa có)

```bash
# Kiểm tra và cài nếu thiếu
brew install ffmpeg python3 node
npm install -g puppeteer
```

### Bước 3: Kiểm tra cài đặt

```bash
# Kiểm tra file đã đúng vị trí
ls ~/.gemini/config/skills/auto-edit-video/SKILL.md
# Nếu thấy file → đã cài đúng

# Kiểm tra script hoạt động
python3 ~/.gemini/config/skills/auto-edit-video/scripts/generate_studio.py --help
```

## Cấu Trúc Thư Mục

```
~/.gemini/config/skills/auto-edit-video/
├── SKILL.md                          ← Hướng dẫn cho AI agent
├── scripts/
│   ├── generate_studio.py            ← Tạo Studio HTML cho mỗi video
│   └── auto_edit_pipeline.py         ← Pipeline phân tích + render
├── resources/
│   ├── studio_template.html          ← Template giao diện Studio
│   ├── styles_db.json                ← 35 kiểu chữ Typography
│   ├── presets_db.json               ← 8 preset ảnh minh họa
│   └── fonts/                        ← 21 file font (7 họ font Vietnamese)
│       ├── SVN-IntegralCF-Heavy.ttf
│       ├── GT-America-LCGV-*.ttf
│       ├── GT-Sectra-LCGV-*.otf
│       └── ... (21 files, ~5MB)
└── references/
    ├── INSTALL.md                    ← File bạn đang đọc
    └── troubleshooting.md            ← Xử lý sự cố
```

## Cách Sử Dụng

Sau khi cài đặt xong, mở Antigravity và gõ:

- **Edit tự động:** `edit video [tên_file].mp4 tự động`
- **Edit chi tiết (có chọn kiểu):** `edit video [tên_file].mp4 chi tiết`

Agent sẽ tự động nhận diện kỹ năng và hướng dẫn bạn qua từng bước.

## Tùy Chỉnh Brand Tag

Mặc định Brand Tag hiển thị:
- Trái: `Viral Video COURSE`
- Giữa: `↗ 0934.68.86.32 (imess)`
- Phải: `2026`

Để đổi, gõ trong chat: *"Đổi Brand Tag: Trái = Tên Kênh, Giữa = SĐT mới, Phải = 2026"*
Hoặc sửa trực tiếp trong Studio HTML khi chọn chi tiết.

## Lưu Ý Quan Trọng

- **Font bản quyền:** Gói bao gồm font thương mại (GT-America, GT-Sectra). Đảm bảo bạn có giấy phép sử dụng.
- **File Studio HTML:** Mỗi lần edit video chi tiết sẽ tạo 1 file HTML riêng (~7-10MB do nhúng font base64). File này hoàn toàn self-contained, mở trên bất kỳ trình duyệt nào đều đúng.
- **Render video:** Cần Google Chrome cài đặt tại đường dẫn chuẩn macOS (`/Applications/Google Chrome.app/`). Nếu Chrome ở vị trí khác, đặt biến môi trường: `export CHROME_PATH=/path/to/chrome`
