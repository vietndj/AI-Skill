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

3. **Thực Thi Sinh Ảnh Chuẩn Điện Ảnh & Vòng Lặp Phản Hồi Khép Kín (Closed-Loop Protocol)**:
   - **Bước 1: Nạp mỏ neo & Face DNA**:
     - Luôn nạp ảnh chân dung sắc nét nhất (`viet_avatar_002.jpg` hoặc ảnh mỏ neo phù hợp) vào tham số `ImagePaths` của `generate_image`.
     - Ghép prompt theo công thức: `[Subject Face Anchor] + [Attire/Wardrobe Anchor] + [Action/Pose] + [Setting/Lighting/Cinematography] + [Aspect Ratio / Camera Specs]`.
   - **Bước 2: Sinh ảnh (`generate_image`)**:
     - Sinh ảnh theo tỷ lệ yêu cầu ('1:1', '3:4', '16:9', '9:16').
   - **Bước 3: TỰ ĐỘNG SOI ẢNH BẰNG `view_file` (BẮT BUỘC 100%)**:
     - Ngay sau khi tool trả về ảnh, AI **BẮT BUỘC dùng `view_file` mở ảnh vừa sinh lên xem trực quan ngay lập tức**.
     - Tự động soi xét và chấm điểm 3 tiêu chí nhân dạng cốt lõi:
       1. *Cấu trúc xương mặt*: Dáng mặt Oval thon gọn, đường viền hàm sắc cạnh (defined jawline), gò má cân đối (không để mặt dài oblong hoặc cằm thụt).
       2. *Đôi mắt & Thần thái*: Mắt mí lót sâu Á Đông, ánh mắt sáng có catchlight sống động (không để mắt 1 mí mờ dẹt vô hồn).
       3. *Nụ cười & Khuôn miệng*: Nụ cười sáng rạng rỡ hở cung răng trên đều đặn / khuôn miệng đĩnh đạc tự nhiên (không để miệng há hốc đơ cứng).
   - **Bước 4: TỰ ĐỘNG TINH CHỈNH & SINH LẠI (Auto Self-Correction)**:
     - Nếu độ giống **< 95%**, AI tự động bóc tách lỗi sai, nạp ảnh vừa sinh cùng ảnh mỏ neo gốc, viết lại prompt sắc nét hơn và sinh lại ngay lập tức (tối đa 3 vòng lặp) cho đến khi đạt độ giống >95% mới bàn giao cho anh Việt.

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
