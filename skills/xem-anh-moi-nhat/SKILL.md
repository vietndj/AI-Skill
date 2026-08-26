---
name: xem-anh-moi-nhat
description: >-
  Kích hoạt khi người dùng yêu cầu xem ảnh mới nhất, check ảnh vừa chụp, xem screenshot,
  sửa theo ảnh, phân tích ảnh trên thư mục anhchup / Desktop / Screenshots / Downloads,
  hoặc nói "xem ảnh", "ảnh mới nhất", "vừa chụp ảnh xong". Hướng dẫn AI tự động quét file ảnh
  mới nhất trên máy (ưu tiên thư mục anhchup) và phân tích ngay lập tức mà người dùng không cần kéo thả ảnh vào chat.
---

# Kỹ năng: Tự Động Định Vị & Phân Tích Ảnh Mới Nhất

Kỹ năng này giúp AI tự động tìm bức ảnh/screenshot mới nhất trên máy tính của người dùng (ưu tiên thư mục `anhchup` tại `~/Documents/anhchup`, `~/anhchup`, cũng như Desktop, Screenshots, Downloads, Workspace), đọc trực tiếp và phân tích theo yêu cầu mà **không cần người dùng phải kéo thả ảnh vào khung chat**.

## 🚀 Các bước thực thi khi được kích hoạt:

1. **Chạy script quét ảnh mới nhất:**
   Thực thi lệnh sau bằng công cụ `run_command`:
   ```bash
   python3 ~/.gemini/config/skills/xem-anh-moi-nhat/scripts/get_latest_image.py
   ```

2. **Đọc kết quả JSON trả về:**
   Script sẽ trả về JSON gồm:
   - `path`: Đường dẫn file ảnh gốc (ưu tiên thư mục `anhchup`)
   - `preview_path`: Đường dẫn file preview (nếu ảnh gốc quá nặng, đã được nén tối ưu)
   - `filename`: Tên file
   - `human_ago`: Thời gian chụp (ví dụ "45 giây trước", "2 phút trước")
   - `dimensions`: Kích thước ảnh

3. **Xem và phân tích nội dung ảnh:**
   - Dùng công cụ `view_file` với `AbsolutePath: <preview_path hoặc path>`.
   - Trả lời người dùng:
     - Xác nhận đã thấy file ảnh: `Tên file: <filename> (chụp cách đây <human_ago>) tại <path>`.
     - Phân tích chi tiết giao diện / lỗi / nội dung trong ảnh.
     - Tiến hành sửa code hoặc đưa ra giải pháp theo đúng yêu cầu của người dùng.

## 💡 Ưu điểm:
- Tự động nhận diện thư mục `anhchup`.
- Không làm phình database hay tràn bộ nhớ chat (tránh triệt để giật lag).
- Người dùng chỉ cần chụp màn hình lưu vào `anhchup` ➔ Nhắn *"Xem ảnh mới nhất và sửa..."* là xong!
