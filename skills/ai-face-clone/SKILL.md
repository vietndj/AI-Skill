---
name: ai-face-clone
description: >-
  Kích hoạt khi người dùng yêu cầu tạo ảnh, avatar, poster, mockup, storyboard, hoặc ảnh đời thường/lifestyle có khuôn mặt của chính họ,
  hoặc khi người dùng yêu cầu "setup khuôn mặt", "tạo hồ sơ khuôn mặt", "cài đặt nhận dạng khuôn mặt", "làm ảnh giống tôi".
  Tự động nạp dữ liệu nhận dạng khuôn mặt (Face Catalog), gắn ảnh mỏ neo (Visual Anchor) vào ImagePaths của generate_image,
  tự động chèn Face DNA Prompt và duy trì đồng nhất trang phục (Wardrobe Continuity) 100% tự nhiên.
---

# AI Face Clone Pro — Kỹ Năng Nhân Bản Khuôn Mặt AI Cho Antigravity

Kỹ năng này biến Antigravity thành Studio Sáng Tạo Hình Ảnh Cá Nhân Hóa. Bất kỳ khi nào người dùng yêu cầu vẽ ảnh/poster/storyboard có nhân vật đại diện, AI sẽ **tự động lấy đúng khuôn mặt của người dùng** mà không cần phải mô tả lại từ đầu.

---

## 1. Cơ Chế Hoạt Động (How It Works)

1. **Nhận diện Ý Định (Intent Detection)**:
   - Khi người dùng chat các câu lệnh tự nhiên:
     - *"Tạo cho anh/tôi ảnh đang ngồi làm việc..."*
     - *"Làm avatar phong cách chuyên gia..."*
     - *"Tạo poster chủ đề AI có tôi trong đó..."*
     - *"Sinh ảnh storyboard minh họa kịch bản này (nhân vật là tôi)..."*
     - *"Tạo ảnh tôi chạy bộ / đứng ngắm cảnh thiên nhiên..."*
   - Hoặc khi có nhân vật chính trong kịch bản mà không chỉ định ai khác.

2. **Kiểm Tra Trạng Thái Kích Hoạt**:
   - Đọc file `~/.gemini/config/skills/ai-face-clone/assets/face_catalog.json`.
   - Nếu `is_activated` là `false` hoặc file chưa tồn tại → **DỪNG LẠI**, hướng dẫn người dùng kích hoạt (xem Mục 2 bên dưới).
   - Nếu đã kích hoạt → tiếp tục nạp dữ liệu.

3. **Nạp Dữ Liệu Hồ Sơ Nhân Dạng (Face Catalog)**:
   - Đọc hồ sơ tại `~/.gemini/config/skills/ai-face-clone/assets/face_catalog.json`.
   - Trích xuất:
     - `prompt_anchor_snippet`: Đoạn mô tả nhân trắc học chuẩn hóa cho chủ nhân hồ sơ.
     - `anchors.primary`: Đường dẫn ảnh chân dung chất lượng cao làm mỏ neo thị giác (`ImagePaths`).
     - Phong cách trang phục tương ứng với bối cảnh (nếu có).

4. **Thực Thi Sinh Ảnh & Vòng Lặp Phản Hồi Khép Kín (Closed-Loop Protocol)**:
   - **Bước 1: Nạp mỏ neo & Face DNA**:
     - Đọc đường dẫn ảnh mỏ neo từ `face_catalog.json → anchors.primary` và nạp vào tham số `ImagePaths` của `generate_image`.
     - Đọc `prompt_anchor_snippet` từ catalog và ghép vào prompt theo công thức:
       `[Subject Face Anchor] + [Attire/Wardrobe] + [Action/Pose] + [Setting/Lighting] + [Aspect Ratio]`.
   - **Bước 2: Sinh ảnh (`generate_image`)**.
   - **Bước 3: TỰ ĐỘNG SOI ẢNH BẰNG `view_file` (BẮT BUỘC 100%)**:
     - Ngay sau khi tool trả về ảnh, AI **BẮT BUỘC dùng `view_file` mở ảnh vừa sinh lên xem trực quan ngay lập tức**.
     - Tự động soi xét và chấm điểm 3 tiêu chí nhân dạng cốt lõi:
       1. *Cấu trúc xương mặt*: Dáng mặt, đường viền hàm, gò má cân đối.
       2. *Đôi mắt & Thần thái*: Kiểu mắt, ánh mắt sáng có catchlight sống động.
       3. *Nụ cười & Khuôn miệng*: Nụ cười tự nhiên hoặc khuôn miệng đĩnh đạc.
   - **Bước 4: TỰ ĐỘNG TINH CHỈNH & SINH LẠI (Auto Self-Correction)**:
     - Nếu độ giống **< 95%**, AI tự động bóc tách lỗi sai, nạp ảnh vừa sinh cùng ảnh mỏ neo gốc, viết lại prompt sắc nét hơn và sinh lại ngay lập tức (tối đa 3 vòng lặp) cho đến khi đạt độ giống >95% mới bàn giao cho người dùng.

5. **Nguyên Tắc Đồng Nhất Trang Phục (Wardrobe Continuity)**:
   - Khi sinh chuỗi ảnh liên hoàn (Storyboard 5-15 beats), **BẮT BUỘC giữ nguyên 100% một bộ trang phục** xuyên suốt tất cả các phân cảnh, không tự ý đổi đồ giữa chừng.

---

## 2. Quy Trình Kích Hoạt (2 Cách)

### Cách A: Nạp Thẻ Căn Cước AI (Mã QR) — Zero Friction Onboarding

Khi người dùng **kéo thả file ảnh Thẻ Căn Cước AI** vào khung chat Antigravity:

1. **Tự động quét và nhận diện mã QR**:
   - Chạy script: `python3 <SKILL_DIR>/scripts/scan_face_card.py "<đường_dẫn_ảnh_thẻ>"`
   - Lấy thông tin `subject_name`, `face_id`, `requires_password`.

2. **DỪNG LẠI VÀ YÊU CẦU MẬT KHẨU KÍCH HOẠT (BẮT BUỘC)**:
   ```text
   🪪 ĐÃ NHẬN DIỆN THẺ CĂN CƯỚC AI: [Tên Chủ Nhân] (Mã #{face_id})
   
   🔒 Hồ sơ Bản Sao Khuôn Mặt này được bảo vệ bản quyền bằng Mật Khẩu Kích Hoạt.
   👉 Vui lòng nhập Mật Khẩu (hoặc Mã Đơn Hàng bạn nhận được khi mua gói) để mở khóa:
   ```

3. **Xác thực và cài đặt khi nhận được mật khẩu**:
   - Chạy script: `python3 <SKILL_DIR>/scripts/install_from_qr.py "<face_id>" "<password>"`
   - Nếu SAI: Báo lỗi và cho phép nhập lại.
   - Nếu ĐÚNG:
     - Tải toàn bộ 3 ảnh mỏ neo về `<SKILL_DIR>/assets/` (tên file: `anchor_001.jpg`, `anchor_002.jpg`, `anchor_003.jpg`).
     - Tạo `face_catalog.json` với đầy đủ prompt mô tả lấy từ server.
     - Tạo rule kích hoạt tự động tại `~/.gemini/config/rules/ai_face_clone.md`.

4. **Sinh ảnh Quà Tặng Chào Mừng (Welcome Render)**:
   - Tự động gọi `generate_image` tạo 1 bức ảnh Avatar Studio đầu tiên mang khuôn mặt của người dùng.
   - BẮT BUỘC dùng `view_file` soi ảnh và gửi ngay trong khung chat!

### Cách B: Tự Setup Từ Ảnh Trên Máy — Interactive Onboarding

Khi người dùng yêu cầu "setup khuôn mặt", "cài đặt nhận dạng khuôn mặt", hoặc gửi 3 ảnh chân dung trực tiếp:

1. **Hỏi thông tin cơ bản** (tên, giới tính).
2. **Chạy setup**: `python3 <SKILL_DIR>/scripts/setup_face_profile.py --name "<Tên>" --gender "<male/female>" --photos-dir "<thư_mục_ảnh>"`
3. Hoặc nếu người dùng gửi ảnh trực tiếp vào chat → AI lưu ảnh vào `<SKILL_DIR>/assets/` rồi chạy setup.

---

## 3. Cấu Trúc Hồ Sơ Nhân Dạng Chuẩn (`face_catalog.json`)

Hồ sơ được lưu trữ **DUY NHẤT** tại `~/.gemini/config/skills/ai-face-clone/assets/face_catalog.json`:
- `subject_name`: Tên chủ nhân hồ sơ.
- `is_activated`: Trạng thái kích hoạt (`true` / `false`).
- `anchors.primary`: Đường dẫn ảnh mỏ neo chính (dùng cho `ImagePaths`).
- `prompt_anchor_snippet`: Đoạn mô tả nhân trắc học chuẩn hóa.
- `face_id`: Mã định danh hồ sơ.

> ⚠️ **LƯU Ý**: Tuyệt đối KHÔNG hardcode bất kỳ đường dẫn tuyệt đối, tên file cụ thể, hay mô tả ngoại hình cố định nào trong SKILL.md hoặc Rule. Luôn đọc ĐỘNG từ `face_catalog.json`.
