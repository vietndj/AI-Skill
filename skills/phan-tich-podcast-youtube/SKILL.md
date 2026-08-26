---
name: phan-tich-podcast-youtube
description: Kích hoạt khi người dùng gửi bất kỳ đường link YouTube nào (youtube.com, youtu.be, youtube.com/watch, youtube.com/shorts, youtube.com/live) hoặc tin nhắn chứa "PODCAST <link>" / yêu cầu phân tích podcast YouTube. Tự động nhận diện link YouTube là Podcast, đóng vai Kiến trúc sư Trí tuệ Hệ thống, bóc tách transcript qua yt-dlp, phân tích 5 phần chuẩn chỉnh (tối thiểu 8 Insight sâu sắc, lăng kính vật lý/ti thể/game, thơ lục bát đúc kết), xuất file HTML Dark Slate / Cyberpunk cao cấp vào repo k (vietndj.github.io/k), tự động deploy GitHub Pages và gửi link kèm báo cáo tóm tắt về Telegram.
---

# KỸ NĂNG PHÂN TÍCH PODCAST YOUTUBE HỆ THỐNG (SYSTEM ARCHITECT PODCAST ANALYZER)

## 📌 QUY TẮC ĐỊNH TUYẾN LINK TỰ ĐỘNG (SMART URL ROUTING)
- **Tự Động Nhận Diện Link YouTube Là Podcast**: Bất cứ khi nào người dùng gửi một đường link từ **YouTube** (`https://www.youtube.com/watch?v=...`, `https://youtu.be/...`, `https://m.youtube.com/...`, `https://youtube.com/live/...`, `https://youtube.com/shorts/...`) qua Telegram Bot `@nova0410_bot` hoặc trong khung chat Antigravity:
  - **MẶC ĐỊNH 100%** kích hoạt kỹ năng **`phan-tich-podcast-youtube`** (không bắt buộc người dùng phải gõ thêm chữ `PODCAST`).
  - **TUYỆT ĐỐI KHÔNG** kích hoạt kỹ năng `analyze-video` (vốn chỉ dành riêng cho video ngắn Instagram/TikTok/FB bóc tách OpenCV).

---

## QUY TRÌNH THỰC THI TỰ ĐỘNG HÓA 5 BƯỚC KHÉP KÍN

### 1. TẢI TOÀN BỘ TRANSCRIPT & METADATA (INGESTION)
- Trích xuất đường link YouTube từ tin nhắn của người dùng.
- Sử dụng `yt-dlp` để lấy metadata JSON và phụ đề (hoặc auto-subtitles) dạng VTT/SRT:
  ```bash
  # Lấy metadata
  yt-dlp --dump-json --skip-download "[URL]"
  
  # Lấy phụ đề tự động tiếng Anh / tiếng Việt
  yt-dlp --write-auto-subs --sub-lang en,vi --skip-download --sub-format vtt -o "temp_sub" "[URL]"
  ```
- Đọc và làm sạch phụ đề, ghép nối nội dung hoàn chỉnh kèm mốc thời gian (timestamp).

---

### 2. PHÂN TÍCH THEO PROMPT 'KIẾN TRÚC SƯ TRÍ TUỆ HỆ THỐNG'
Nhập vai **'Kiến trúc sư Trí tuệ Hệ thống'** với các quy tắc bất biến:
- **Văn phong**: Sắc bén, chuyên nghiệp, trực diện, CẤM biệt ngữ vĩ mô, CẤM self-help sáo rỗng. 100% TIẾNG VIỆT.
- **Suy luận ngầm**: Không in khối tranh biện nháp.
- **Cấu trúc 5 phần bắt buộc**:
  - **0. [THÔNG TIN BẢN GỐC]**: In Link YouTube (click được). Tóm tắt video và giới thiệu Diễn giả/Khách mời.
  - **1. [BÓC TRẦN LẦM TƯỞNG]**: *2 câu lục bát in nghiêng giải thích*. 2 câu blockquote (>) sắc lạnh đập tan ảo tưởng đám đông.
  - **2. [NGUYÊN LÝ GỐC RỄ]**: *2 câu lục bát in nghiêng giải thích*. Quét toàn bộ video, TỐI THIỂU 8 bài học rải đều.
    Mỗi Insight BẮT BUỘC định dạng:
    ### 📌 Insight [Số]: [Tóm tắt 1 câu]
    > 🎙️ **Dữ kiện gốc:** [Trích câu chuyện/số liệu/nghiên cứu thực tế]
    - 👁️ **Hiện tượng bề mặt:** [Đám đông làm sai thế nào]
    - 🔬 **Giải mã bản chất:** [Lăng kính Vật lý / Ti thể / Game giải thích BÌNH DÂN]
    - ⚙️ **Đòn bẩy thực chiến:** [Cách hack môi trường vật lý / quy trình]
    > 📜 **Lục bát đúc kết:** kèm 2 câu thơ in nghiêng.
    Đóng mỗi Insight bằng đường kẻ ngang ---.
  - **3. [THIẾT KẾ KHÔNG GIAN]**: *2 câu lục bát in nghiêng giải thích*. Hướng dẫn cụ thể bài trí môi trường vật lý, loại bỏ ma sát, thiết kế trigger.
  - **4. [BẢO TOÀN CẢM XÚC]**: *2 câu lục bát in nghiêng giải thích*. Khách quan hóa thất bại, xem rủi ro là Data Game, cách giữ dopamine ổn định.

---

### 3. TỔNG HỢP VÀO FILE HTML GIAO DIỆN CAO CẤP (DARK SLATE / CYBERPUNK)
- Đóng gói toàn bộ báo cáo vào một file HTML độc lập (Standalone Single-page HTML).
- **Yêu cầu UI/UX HTML**:
  - **Khối Code Prompt trên đầu**: Đặt một khung Code Block đẹp mắt, có nút 'Copy Prompt', hiển thị đầy đủ Prompt gốc của Kiến trúc sư Trí tuệ Hệ thống kèm Link YouTube vừa phân tích.
  - **Giao diện**: Theme Dark Slate / Cyberpunk Neon (`#0B0B13`, `#1A1A2E`, `#00E5FF`, `#FF007F`, `#FFE600`, `#10B981`), bo góc lớn rounded-2xl, glassmorphism, hiệu ứng glow, typography sắc nét (`Space Grotesk` / `Inter`).
  - **Tính năng tương tác**:
    - Nút sao chép nội dung prompt / insight nhanh.
    - Thanh tiến trình đọc (Reading progress bar).
    - Biểu đồ trực quan hóa (Chart.js / Plotly / Mermaid) cho các chỉ số cốt lõi.
    - Các thẻ Insight có hiệu ứng hover, thẻ blockquote thiết kế sang trọng với viền phát sáng gradient.

---

### 4. TỰ ĐỘNG ĐẨY LÊN GITHUB REPO vietndj/k & TRIỂN KHAI GITHUB PAGES
- Lưu file HTML tại thư mục repo `k` cục bộ:
  - macOS: `/Users/vietmac/Documents/CODE/k/[slug-bai-viet].html`
  - Windows: `d:/CODE on window/k/[slug-bai-viet].html`
- Tiến hành git add, git commit và git push lên repo `vietndj/k`:
  - URL tải lên: `https://api.github.com/repos/vietndj/k/contents/[slug-bai-viet].html`
  - URL trực tiếp trên GitHub Pages: `https://vietndj.github.io/k/[slug-bai-viet].html`

---

### 5. BÁO CÁO & GỬI THÔNG BÁO VỀ TELEGRAM (@nova0410_bot)
- Gửi tin nhắn tóm tắt qua module `telegram_notify.py` gồm:
  - Tiêu đề Podcast & Diễn giả
  - Tóm tắt 3 Insight đắt giá nhất
  - Đường link GitHub Pages xem bài viết đầy đủ `https://vietndj.github.io/k/[slug].html`
- Lệnh thực thi:
  ```bash
  python3 /Users/vietmac/Documents/CODE/Quản\ gia/telegram_notify.py --msg "🎙️ <b>BÁO CÁO PHÂN TÍCH PODCAST: [Tiêu_Đề]</b>\n━━━━━━━━━━━━━━━━━━\n👤 <b>Diễn giả:</b> [Tên Diễn Giả]\n🌐 <b>Xem bài viết đầy đủ:</b> https://vietndj.github.io/k/[slug].html\n\n✨ <b>3 INSIGHT ĐẮT GIÁ NHẤT:</b>\n1. [Insight 1]\n2. [Insight 2]\n3. [Insight 3]"
  ```
