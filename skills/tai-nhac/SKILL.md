---
name: tai-nhac
description: Kích hoạt khi người dùng nhắc đến "TAI NHAC :", "tải nhạc", "tai nhac", "lấy âm thanh", "tải audio", "tách nhạc", "tải bài hát", "link audio instagram", hoặc gửi đường link Instagram audio / reels / posts, YouTube, TikTok, Facebook, SoundCloud yêu cầu tìm file gốc, tải về máy, đồng bộ Google Drive và bắn thẳng file nhạc MP3 qua Telegram.
---

# KỸ NĂNG TỰ ĐỘNG TẢI NHẠC & ĐỒNG BỘ ĐA NỀN TẢNG (TAI NHAC SKILL)

Kỹ năng này thiết lập phản xạ tự động 100% khi anh Việt gửi yêu cầu tải bài hát, gửi link Instagram audio (`instagram.com/reels/audio/...`), trích xuất âm thanh từ video hoặc sử dụng cú pháp `TAI NHAC : <link/tên bài>`.

## 1. QUY TRÌNH THỰC THI 4 BƯỚC CỐT LÕI

Khi nhận được link audio Instagram hoặc yêu cầu tải nhạc, AI BẮT BUỘC thực thi chuỗi 4 mắt xích tự động không điều kiện:

1. **Bước 1: Tự động phân tích link & Tải bản gốc (Master Audio 320kbps)**:
   - Với **Link Instagram Audio** (`/reels/audio/<id>`, `/audio/<id>`): Tự động trích xuất thông tin Bài hát & Nghệ sĩ.
   - Tìm kiếm và đối soát bản phát hành gốc đầy đủ (Official Studio Master / Full Audio 320kbps) trên hệ thống, loại bỏ các clip cắt ngắn / rè / remix không mong muốn.
   - Chuyển đổi và lưu trữ file MP3 chuẩn cao nhất tại thư mục máy: `/Users/vietmac/Documents/Nhạc tai ve/`.

2. **Bước 2: Đồng bộ lên Google Drive (Cloud Storage)**:
   - Tự động kiểm tra và đồng bộ file MP3 hoàn chỉnh lên Google Drive remote của anh Việt: `gdrive:Nhạc tai ve`.

3. **Bước 3: Lấy đường dẫn chia sẻ (Google Drive Direct Link)**:
   - Dùng `rclone link` lấy link truy cập trực tiếp của file MP3 trên Google Drive.

4. **Bước 4: Bắn trực tiếp file MP3 qua Telegram (@nova0410_bot)**:
   - Gọi module Telegram Dispatcher gửi **FILE MP3 TRỰC TIẾP** (tích hợp Telegram Music Player để nghe ngay trong app) kèm thông tin chi tiết: Tên bài hát, Nghệ sĩ, Thời lượng, Dung lượng, Tên file cục bộ và Link Google Drive.

## 2. CÚ PHÁP THỰC THI CHUẨN TRONG 1 DÒNG LỆNH

Toàn bộ quy trình 4 bước đã được tự động hóa tối ưu trong script:

```bash
python3 "/Users/vietmac/.gemini/config/skills/tai-nhac/scripts/tai_nhac.py" "<URL_hoặc_Tên_Bài_Hát>"
```

### Các nguồn hỗ trợ:
- **Link Instagram Audio**: `https://www.instagram.com/reels/audio/<id>/` hoặc `https://www.instagram.com/audio/<id>/` (Tự động nhận diện tên bài và tải bản Studio Master Full).
- **Link Instagram Reel / Post**: `https://www.instagram.com/reel/<shortcode>/`
- **Link YouTube / YouTube Music**: `https://www.youtube.com/watch?v=...`
- **Link TikTok / Facebook / SoundCloud**.
- **Tìm kiếm theo tên bài hát**: `TAI NHAC : Deelite Siren`

## 3. THÔNG TIN BOT & TÀI NGUYÊN ĐÍCH
- **Thư mục trên máy**: `/Users/vietmac/Documents/Nhạc tai ve/`
- **Thư mục Google Drive**: `gdrive:Nhạc tai ve`
- **Bot Telegram**: `NOVA-CORE` (`@nova0410_bot` - Chat ID: `2050406425`)
- **Script Telegram Dispatcher**: `/Users/vietmac/Documents/CODE/Quản gia/telegram_notify.py`

## 4. QUY TẮC TRÌNH BÀY CHO ANH VIỆT
- Xưng hô chuẩn mực: **"em - anh Việt"**.
- Tuyệt đối **KHÔNG dùng đường kẻ ngang (`---`)**.
- Luôn giữ độ thoáng và nhịp thở thị giác (`\n\n`) giữa các đoạn văn.
- Cung cấp đầy đủ các liên kết có thể click trực tiếp:
  - Link mở file MP3 trong máy: `file:///Users/vietmac/Documents/Nhạc%20tai%20ve/<Tên_File>`
  - Link mở thư mục máy: `file:///Users/vietmac/Documents/Nhạc%20tai%20ve/`
  - Link truy cập Google Drive trực tuyến.
