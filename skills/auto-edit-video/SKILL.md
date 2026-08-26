---
name: auto-edit-video
description: Kỹ năng tự động hóa biên tập video Talking Head chuyên gia (Editorial Motion Graphics) và Video Đời Sống Hằng Ngày (Daily Life / Lifestyle / Fun & Cozy Vlog). Render engine: Remotion (React, deterministic frame-by-frame, 0 drop frame). Typography phong phú, Punch-Zoom biểu cảm, Floating Emojis, Safe-Zone TikTok/Reels, AI Mood Classifier. Kích hoạt khi người dùng yêu cầu: "edit video tự quay", "edit video tự động", "dựng video talking head", "edit video đời sống", "edit vlog", "auto edit video", hoặc gửi video qua Telegram bot.
---

# KỸ NĂNG BIÊN TẬP VIDEO TỰ ĐỘNG (REMOTION ENGINE)

## 1. NGUYÊN TẮC CỐT LÕI
* **Render Engine: Remotion** — Frame-by-frame deterministic, 0 drop frame, khớp audio tuyệt đối.
* **Đa Phong Cách & Nhận Diện AI (AI Mood Classifier):** Tự động phân loại nội dung để chọn đúng phong cách phù hợp (Editorial Chuyên gia vs Đời Sống Vui Tươi).
* **Safe-Zone Chuẩn TikTok/Reels:** Tránh che mặt, tránh đè lên UI thanh điều hướng và caption mạng xã hội.

---

## 2. CÁC PHONG CÁCH HẬU KỲ

### 🌸 PHONG CÁCH 1: ĐỜI SỐNG HẰNG NGÀY (LIFESTYLE / VLOG / FUN MOMENTS)
* **Dành cho:** Video gia đình, bạn bè, người yêu, trêu đùa, ăn uống, cafe, dạo phố, du lịch.
* **Điểm nhấn:**
  - **Punch-Zoom (1.15x - 1.25x):** Giật nhẹ vào biểu cảm khuôn mặt khi có câu nói đùa/cười.
  - **Chữ bo tròn tươi sáng:** Font *Baloo 2, Nunito, Quicksand, Be Vietnam Pro Rounded* với màu pastel (Vàng tươi, Hồng dâu, Xanh mint, Kem kính mờ).
  - **Floating Emojis:** Icon động (😂, 🌸, ✨, 💖, ⌚) bay lên tự nhiên theo ngữ cảnh thoại.
  - **Khử Vignette đen:** Tự động nâng sáng ấm áp tự nhiên (+4% Brightness, +12% Saturation).
  - **Header Tag tinh tế:** `✨ Daily Moments • 10:30 AM` hoặc ẩn hoàn toàn (không chèn số điện thoại bán hàng).
* **Lệnh chạy:**
  ```bash
  python3 <skill_dir>/scripts/auto_lifestyle_pipeline.py --video /path/to/video.mp4 --preset [fun|cozy|dynamic|cute]
  ```

### 💼 PHONG CÁCH 2: TALKING HEAD / EDITORIAL TECH (CHUYÊN GIA / KHÓA HỌC)
* **Dành cho:** Chia sẻ kiến thức, kinh doanh, bài học, podcast, review công nghệ.
* **Điểm nhấn:** Kinetic Typography 35 kiểu, ảnh AI 3D Glassmorphism, B-Roll fullscreen, Brand Tag thương hiệu.
* **Lệnh chạy:**
  ```bash
  python3 <skill_dir>/scripts/auto_transcribe_and_edit.py --video /path/to/video.mp4 --preset editorial
  ```

---

## 3. CHẾ ĐỘ TỰ ĐỘNG HOÀN TOÀN (AUTO-PILOT)
* **Lệnh thông minh (AI tự động chọn phong cách phù hợp nhất):**
  ```bash
  python3 <skill_dir>/scripts/auto_transcribe_and_edit.py --video /path/to/video.mp4 --preset auto
  ```
* **Quy trình trọn gói:** Faster-Whisper nhận diện tiếng Việt → AI Classifier chọn Style → Render Remotion → Tải lên Google Drive → Gửi Link xem trực tiếp về Telegram cho anh Việt (@nova0410_bot).

---

## 4. BỘ CÔNG CỤ & TÀI NGUYÊN

### Remotion Project (Render Engine)
- **Project dir:** `<skill_dir>/remotion-studio/`
- **Compositions:** 
  - `AutoEditVideo` (Editorial Talking Head)
  - `LifestyleVideo` (Daily Life & Vlog)
- **Components:** `PunchZoom.tsx`, `LifestyleSubtitles.tsx`, `FloatingEmojis.tsx`, `LifestyleBrandTag.tsx`, `KineticText.tsx`, `ImageOverlay.tsx`, `BRollScene.tsx`
- **Data:** `src/data/lifestyle_styles.ts` (8 lifestyle styles), `src/data/styles.ts` (35 editorial styles)

### Scripts Điều Phối
- **Lifestyle Pipeline:** `<skill_dir>/scripts/auto_lifestyle_pipeline.py`
- **Multi-Style Master:** `<skill_dir>/scripts/auto_transcribe_and_edit.py`
- **Studio Generator:** `<skill_dir>/scripts/generate_studio.py`
- **Remotion Bridge:** `<skill_dir>/scripts/render_with_remotion.py`
