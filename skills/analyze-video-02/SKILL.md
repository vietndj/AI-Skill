---
name: analyze-video-02
description: >-
  Kỹ năng Phân Tích Video & Bóc Tách Phân Cảnh Chuẩn Đạo Diễn (Director's Shot Notebook Edition).
  Dành cho người dùng mới Antigravity: Tích hợp bảo vệ bản quyền bằng Mật Khẩu Kích Hoạt 1 Lần,
  tự động cài thư viện 100%, bóc tách OpenCV, trích xuất Keyframes & Color Palette,
  phân tích 3 khối chuyên sâu (Điểm sáng, Hạn chế, Bài học), xuất bản Báo Cáo PDF A4 Dark-Mode sang xịn
  sử dụng chuẩn font SVN-Integral CF & SVN-Poppins, tự động mở trên máy và đồng bộ chia sẻ qua Google Drive.
---

# PHÂN TÍCH VIDEO 02 - DIRECTOR'S SHOT NOTEBOOK PRO

Kỹ năng này biến Antigravity thành một **Đạo Diễn Phân Tích Video Cá Nhân Hóa** cho học viên / người dùng mới. Bất kỳ khi nào người dùng gửi một đường link video ngắn (Instagram Reels, TikTok, YouTube Shorts, Facebook Video) hoặc kéo thả tệp `.mp4` cục bộ vào khung chat, AI sẽ tự động thực hiện quy trình phân tích và xuất bản báo cáo PDF khép kín trong 1 câu lệnh (1-Shot).

---

## 🔒 QUY TRÌNH XÁC THỰC MẬT KHẨU KÍCH HOẠT 1 LẦN (ONBOARDING PROTOCOL)

Khi người dùng gửi link/video hoặc yêu cầu phân tích video lần đầu tiên:

1. **Kiểm tra trạng thái kích hoạt**:
   - Chạy lệnh: `python3 ~/.gemini/config/skills/analyze-video-02/scripts/verify_license.py`
2. **Nếu CHƯA KÍCH HOẠT (`is_activated: false`)**:
   - AI **BẮT BUỘC DỪNG LẠI** và gửi thông báo yêu cầu mật khẩu kích hoạt:
     ```text
     🎬 CHÀO MỪNG BẠN ĐẾN VỚI PHÂN TÍCH VIDEO 02 (DIRECTOR'S SHOT NOTEBOOK PRO)
     
     🔒 Kỹ năng này được bảo vệ bản quyền bằng Mật Khẩu Kích Hoạt 1 Lần.
     👉 Vui lòng nhập Mật Khẩu (hoặc Mã Đơn Hàng bạn nhận được từ anh Việt / FEDU) để kích hoạt trọn đời:
     ```
3. **Khi người dùng nhập mật khẩu / mã kích hoạt**:
   - Chạy lệnh: `python3 ~/.gemini/config/skills/analyze-video-02/scripts/verify_license.py "<MẬT_KHẨU>" "<TÊN_NGƯỜI_DÙNG>"`
   - Nếu SAI: Báo lỗi và cho phép nhập lại.
   - Nếu ĐÚNG: Ghi nhận kích hoạt vĩnh viễn và **TỰ ĐỘNG CHẠY NGAY TIẾN TRÌNH PHÂN TÍCH VIDEO** mà không bắt người dùng phải paste lại link!

---

## 📌 QUY TRÌNH THỰC THI TỰ ĐỘNG 5 BƯỚC (ZERO-FRICTION PIPELINE)

### BƯỚC 1: TỰ ĐỘNG KIỂM TRA & CÀI ĐẶT THƯ VIỆN (AUTO SELF-HEALING)
- Trước khi xử lý, AI tự động chạy script kiểm tra:
  ```bash
  python3 ~/.gemini/config/skills/analyze-video-02/scripts/setup_deps.py
  ```
- Nếu máy học viên thiếu `yt-dlp`, `opencv-python`, `Pillow`, script sẽ tự động cài ngầm trong 3 giây mà không làm gián đoạn trải nghiệm của học viên.

### BƯỚC 2: TẢI VIDEO & BÓC TÁCH PHÂN CẢNH OPENCV
- Chạy script trích xuất:
  ```bash
  python3 ~/.gemini/config/skills/analyze-video-02/scripts/extract_shots.py "<URL_HOẶC_ĐƯỜNG_DẪN_VIDEO>" --output "./Video_Analysis/[Tên_Kênh]_[Mã_Video]"
  ```
- Script sẽ tự động:
  1. Tải video `.mp4` gốc chất lượng cao nhất (tự làm sạch rác URL tracking).
  2. Bóc tách toàn bộ Scene Cuts bằng thuật toán OpenCV HSV Histogram.
  3. Trích xuất 3 ảnh Keyframe cho mỗi Shot (`shot_XX_start.jpg`, `shot_XX_mid.jpg`, `shot_XX_end.jpg`).
  4. Trích xuất bảng 4 mã màu chủ đạo (Dominant Color Palette) cho từng phân cảnh.
  5. Xuất file dữ liệu `shot_data.json`.

### BƯỚC 3: PHÂN TÍCH CHUYÊN SÂU CHUẨN ĐẠO DIỄN (SHOT BREAKDOWN LOGIC)
AI đọc file `shot_data.json` và bóc tách từng phân cảnh theo quy chuẩn 4 phần đắt giá (TUYỆT ĐỐI KHÔNG DÙNG VĂN MẪU SÁO RỖNG):

1. **Tiêu Đề Phân Cảnh (Key Visual Logic)**:
   - Đặt trực tiếp **Điểm hiệu quả nhất / Logic thị giác đắt giá nhất + Lý do vì sao** làm tiêu đề (Font SVN-Integral CF).
   - *Ví dụ*: *"Hook thị giác: Tách lớp chủ thể qua ly cà phê và ánh sáng ven tóc"*.
2. **Mô Tả Đối Tượng & Diễn Biến (Subject & Action)**:
   - Mô tả cụ thể chủ thể là ai/cái gì và hành động diễn ra như thế nào trong shot đó.
3. **Đánh Giá Bố Cục 2 Chiều (Composition Critique)**:
   - `✅ Điểm sáng thị giác`: Phân tích tỷ lệ khung hình, điểm nhấn mắt, ánh sáng, tiêu cự mang lại hiệu ứng gì.
   - `⚠️ Hạn chế / Lưu ý`: Phê bình khách quan thẳng thắn (bố cục chật, ánh sáng bết, chuyển động giật...).
4. **Bài Học Thực Chiến (Actionable Takeaway)**:
   - 1-2 câu súc tích để người làm video áp dụng ngay vào video của mình.

### BƯỚC 4: XUẤT BẢN BÁO CÁO PDF ĐẠO DIỄN (CHROME HEADLESS + BRAND FONTS)
- Cập nhật các nội dung phân tích vào `shot_data.json` và chạy script render PDF:
  ```bash
  python3 ~/.gemini/config/skills/analyze-video-02/scripts/build_pdf_report.py "./Video_Analysis/[Tên_Kênh]_[Mã_Video]/shot_data.json"
  ```
- **Chuẩn Typography bắt buộc**:
  - Tiêu đề ngắn ($\le 8$ từ): **`SVN-Integral CF` (Regular - font-weight: 400, tuyệt đối không dùng Bold/Heavy)**.
  - Tiêu đề dài ($> 8$ từ / câu diễn giải): **BẮT BUỘC dùng `SVN-Poppins` (SemiBold 600)** để đảm bảo đọc lướt êm mắt, chống ngộp thị giác.
  - Nội dung & Thân bài: **`SVN-Poppins`** (Regular 400).
  - Layout A4 Dark Editorial chống cắt đôi phân cảnh (`page-break-inside: avoid;`).
  - Dung lượng file tối ưu siêu nhẹ (< 6MB).
  - **Tự động mở file PDF trên máy** để học viên thưởng thức ngay lập tức!

### BƯỚC 5: ĐỒNG BỘ GOOGLE DRIVE & TRÌNH BÀY KẾT QUẢ
- Chạy script đồng bộ:
  ```bash
  python3 ~/.gemini/config/skills/analyze-video-02/scripts/drive_share.py "./Video_Analysis/[Tên_Kênh]_[Mã_Video]/Director_Shot_Notebook.pdf"
  ```
- Script tự động đưa file vào Google Drive Desktop nếu máy có cài đặt.
- **Trình bày phản hồi cho người dùng trong chat**:
  - Tóm tắt 3 Insight điện ảnh đắt giá nhất của video.
  - Kèm **Kịch Bản Chuyển Thể 1-1 (Remake Shooting Script)** để học viên có thể vác máy đi quay luôn.
  - Đính kèm các nút liên kết mở nhanh file PDF và thư mục dự án.

---

## 🎯 CÁC MẪU CÂU LỆNH KÍCH HOẠT TỰ NHIÊN (TRIGGER PATTERNS)
1. Gửi đường link Reels / TikTok / Shorts / Facebook Video trực tiếp vào chat.
2. Kéo thả file video `.mp4` vào khung chat.
3. *"Phân tích video này cho tôi [link]"*.
4. *"Bóc tách phân cảnh và xuất file PDF video này"*.
5. *"Mổ xẻ góc quay video này và xuất báo cáo đạo diễn"*.
