---
name: ai-face-clone
description: >-
  Kích hoạt khi người dùng yêu cầu tạo ảnh, avatar, poster, mockup, storyboard, hoặc ảnh đời thường/lifestyle có khuôn mặt của chính họ,
  hoặc khi người dùng yêu cầu "setup khuôn mặt", "tạo hồ sơ khuôn mặt", "cài đặt nhận dạng khuôn mặt", "làm ảnh giống tôi".
  Tự động nạp dữ liệu nhận dạng khuôn mặt (Face Catalog), gắn ảnh mỏ neo (Visual Anchor) vào ImagePaths của generate_image,
  tự động chèn Face DNA Prompt và duy trì đồng nhất trang phục (Wardrobe Continuity) 100% tự nhiên.
---

# AI Face Clone Pro - Kỹ Năng Nhân Bản Khuôn Mặt AI Cho Antigravity

Kỹ năng này biến Antigravity thành Studio Sáng Tạo Hình Ảnh Cá Nhân Hóa tối thượng. Bất kỳ khi nào người dùng yêu cầu vẽ ảnh/poster/storyboard có nhân vật đại diện, AI sẽ **tự động lấy đúng khuôn mặt của người dùng** mà không cần phải mô tả lại từ đầu.

---

## 1. Cơ Chế Hoạt Động (How It Works)

1. **Nhận diện Ý Định (Intent Detection)**:
   - Khi người dùng chat các câu lệnh tự nhiên:
     - *"Tạo cho anh/tôi ảnh đang ngồi làm việc..."*
     - *"Làm avatar phong cách chuyên gia..."*
     - *"Tạo poster chủ đề AI có tôi trong đó..."*
     - *"Sinh ảnh storyboard minh họa kịch bản này (nhân vật là tôi)..."*
     - *"Tạo ảnh tôi chạy bộ / đứng ngắm cảnh thiên nhiên..."*
   - Hoặc khi có nhân vật nam/nữ chính trong kịch bản mà không chỉ định ai khác.

2. **Nạp Dữ Liệu Hồ Sơ Nhân Dạng (Face Catalog)**:
   - Đọc hồ sơ tại `~/.gemini/avatar_photos/face_catalog.json` (hoặc trong thư mục cấu hình của dự án).
   - Trích xuất:
     - `prompt_anchor_snippet`: Đoạn mô tả nhân trắc học chuẩn (tuổi, dáng người, mắt, mũi, nụ cười, tóc, làn da).
     - `reference_images`: 1-3 đường dẫn ảnh chân dung thực tế chất lượng cao làm mỏ neo thị giác (`ImagePaths`).
     - `wardrobe_styles`: Phong cách trang phục tương ứng với bối cảnh (Studio, Bàn gỗ, Outdoor, Zen, Thể thao).

3. **Thực Thi Sinh Ảnh Chuẩn Điện Ảnh**:
   - Gọi tool `generate_image`:
     - Tham số `ImagePaths`: Nạp danh sách 1-3 ảnh chân dung mẫu từ `~/.gemini/avatar_photos/` hoặc thư mục ảnh đã quét.
     - Tham số `Prompt`: Ghép theo công thức chuẩn:
       `[Subject Face Anchor] + [Attire/Wardrobe Anchor] + [Action/Pose] + [Setting/Lighting/Cinematography] + [Aspect Ratio / Camera Specs]`
     - Tham số `AspectRatio`: '1:1' cho Avatar/Square, '9:16' cho Story/Reel, '16:9' cho Banner/Thumbnail, '4:3' cho Phân cảnh.

4. **Nguyên Tắc Đồng Nhất Trang Phục (Wardrobe Continuity)**:
   - Khi sinh chuỗi ảnh liên hoàn (Storyboard 5-15 beats), **BẮT BUỘC giữ nguyên 100% một bộ trang phục** xuyên suốt tất cả các phân cảnh, không tự ý đổi đồ giữa chừng.

---

## 2. Quy Trình Onboarding Tự Động Trong Chat (Interactive Chat Setup)

Khi người dùng nói: *"Setup khuôn mặt của tôi"* hoặc *"Cài đặt hồ sơ khuôn mặt"*:
1. **Quét ảnh tự động**: Chạy ngay lệnh `python3 ~/.gemini/config/skills/ai-face-clone/scripts/setup_face_profile.py`.
2. **Khởi tạo hồ sơ**: Nếu tìm thấy ảnh trong máy, tự động tạo `face_catalog.json`.
3. **Sinh ảnh Chào Mừng (Welcome Render)**: Tự động gọi `generate_image` tạo 1 ảnh Avatar Studio hoặc Bàn Gỗ đầu tiên để người dùng thấy ngay hiệu quả trong 30 giây đầu tiên.

---

## 3. Cấu Trúc Hồ Sơ Nhân Dạng Chuẩn (`face_catalog.json`)

Hồ sơ được lưu trữ tại `~/.gemini/avatar_photos/face_catalog.json`:
- Chứa thông số nhân trắc học, độ tuổi, vóc dáng, màu tóc, dáng mắt, sống mũi, nụ cười.
- Chứa danh sách ảnh mỏ neo thực tế.
- Chứa bộ mã trang phục chuẩn theo từng bối cảnh.
