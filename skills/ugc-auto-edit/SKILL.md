---
name: ugc-auto-edit
description: Kỹ năng biên tập video UGC (User Generated Content) tự quay với 2 chế độ AUTO (wow bất ngờ, gửi nhanh) và DETAILED (chi tiết kiểm soát). Tự động phân loại 4 Catalog (Daily Life, Nature Ambient, Event, Live Talk), kiểm soát font tiếng Việt, surprise wow effects. Render engine: Remotion. Kích hoạt khi: "edit video UGC", "auto edit video tự quay", "edit video đời thường", "edit video nhanh", "edit video wow", "ugc edit".
---

# Kỹ năng: UGC Auto-Edit 🚀

Chào anh Việt, đây là tài liệu hướng dẫn kỹ năng **UGC Auto-Edit** của hệ thống. Kỹ năng này giúp anh biến các đoạn video tự quay (UGC) thành các video hoàn chỉnh, chuyên nghiệp chỉ trong vài phút, với hai chế độ hoạt động linh hoạt.

## 1. NGUYÊN TẮC CỐT LÕI 🧠

Hệ thống UGC Auto-Edit hoạt động dựa trên các nguyên tắc thiết kế khắt khe để đảm bảo chất lượng video đầu ra:

- 🎬 **Render Engine**: Sử dụng **Remotion** làm engine render cốt lõi. Đảm bảo tính nhất quán (deterministic) và 0 drop frame, cho chất lượng video hoàn hảo tới từng pixel.
- 🛡️ **4 Gate kiểm soát lỗi**:
  1. **Input**: Kiểm tra định dạng, độ phân giải, thời lượng video gốc.
  2. **Font**: Đảm bảo font chữ hỗ trợ tiếng Việt đầy đủ, không lỗi dấu.
  3. **Duration**: Khớp thời lượng hiệu ứng và subtitle với video gốc.
  4. **Post-render**: Kiểm tra file đầu ra trước khi gửi.
- 🤖 **AI Classifier**: Tự động phân loại video của anh vào 1 trong 4 catalog để áp dụng phong cách edit tối ưu nhất.
- ✨ **Surprise Wow Engine**: Trái tim của chế độ AUTO, mang đến những hiệu ứng thị giác bất ngờ.
- 🎞️ **Single Video Processing**: Hệ thống hiện chỉ hỗ trợ xử lý 1 video gốc duy nhất (Không hỗ trợ Multi-clip ghép nhiều video). Hệ thống sẽ tập trung tạo ra các hiệu ứng (zoom in/out, text animation...) **trong chính video đó** để giữ chân người xem.
- 🎵 **Âm thanh (Music)**: Trong Phase 1, hệ thống sẽ giữ nguyên âm thanh gốc của video. Tính năng chèn nhạc nền miễn phí hoặc thư viện cá nhân sẽ được cập nhật sau.

## 2. HỆ THỐNG PHÂN LOẠI 4 CATALOG 📁

AI sẽ tự động phân tích video của anh Việt và xếp vào một trong các nhóm sau:

| Catalog | Icon | Mô tả | Ví dụ | Đặc điểm AI nhận diện |
| :--- | :---: | :--- | :--- | :--- |
| **DAILY LIFE** | 🎭 | Video quay khoảnh khắc đời thường, vui nhộn, năng động. | Chơi với thú cưng, unbox đồ, nấu ăn. | Chuyển động máy quay nhiều, khuôn mặt gần, âm thanh môi trường ồn ào. |
| **NATURE AMBIENT** | 🌿 | Khung cảnh thiên nhiên tĩnh lặng, thư giãn, slow-paced. | Cảnh mưa, pha cà phê, hoàng hôn. | Ít chuyển động, màu xanh/đất, âm thanh êm dịu hoặc không có thoại. |
| **EVENT** | 🎪 | Sự kiện, đông người, không khí sôi động. | Khai trương, tiệc tùng, du lịch đông người. | Nhiều góc quay, thay đổi cảnh liên tục, âm thanh náo nhiệt. |
| **LIVE TALK** | 💬 | Video tập trung vào người nói, chia sẻ kiến thức. | Review sản phẩm, kể chuyện, Q&A. | Cố định máy, mặt người ở giữa khung hình, có giọng nói rõ ràng (Voice/Speech). |

## 3. CHẾ ĐỘ AUTO (⚡ GỬI NHANH, WOW BẤT NGỜ)

Đây là chế độ mặc định khi anh Việt muốn có video nhanh gọn lẹ mà vẫn "chất".

- **Lệnh thực thi**:
  ```bash
  python3 <skill_dir>/scripts/ugc_auto_pipeline.py --video /path/to/video.mp4 --mode auto
  ```
- **Quy trình hoạt động**:
  1. Validate ➔ 2. Classify ➔ 3. Transcribe ➔ 4. Wow Select ➔ 5. Render ➔ 6. Upload ➔ 7. Notify
- 🎁 **Surprise Factor**: Ở chế độ này, hệ thống sẽ random chọn 1 "wow effect" (như *PunchZoom*, *FreezeFrame*). Anh Việt sẽ không bao giờ biết trước hệ thống sẽ chọn hiệu ứng nào cho đến khi xem video hoàn chỉnh!

## 4. CHẾ ĐỘ DETAILED (🎬 CHI TIẾT, KIỂM SOÁT)

Chế độ dành cho những lúc anh Việt muốn kiểm soát hoàn toàn kịch bản, hiệu ứng và subtitle.

- **Lệnh thực thi**:
  ```bash
  python3 <skill_dir>/scripts/ugc_auto_pipeline.py --video /path/to/video.mp4 --mode detailed
  ```
- **Quy trình hoạt động**:
  Hệ thống sẽ tạo ra một file config định dạng JSON. Để preview và chỉnh sửa, anh Việt sử dụng **Remotion Studio** bằng cách chạy lệnh `npx remotion studio`. Giao diện Studio cho phép anh review timeline, sửa text và thay đổi hiệu ứng trực tiếp. Khi đã chốt kịch bản, hệ thống sẽ tiến hành render.

## 5. BỘ CÔNG CỤ & TÀI NGUYÊN 🛠️

- **Scripts**:
  - `ugc_classifier.py`: Nhận diện catalog.
  - `input_validator.py`: Kiểm tra đầu vào.
  - `font_validator.py`: Check lỗi font tiếng Việt.
  - `wow_engine.py`: Xử lý logic random effect.
  - `ugc_auto_pipeline.py`: Main script điều phối.
- **Remotion Compositions**: `LifestyleVideo`, `NatureVideo`, `EventVideo`, `LiveTalkVideo`.
- **Remotion Components**: `PunchZoom`, `KenBurns`, `TypewriterText`, `ParallaxText`, `SpeedRamp`, `FreezeFrame`, `PullQuoteCard`, `SpeakerColorSub`, `SurpriseEffect`.

## 6. TIÊU CHUẨN ĐẦU VÀO VIDEO 🎥

Để hệ thống hoạt động mượt mà và cho ra video đẹp nhất, đầu vào cần đạt một số tiêu chuẩn cơ bản.

- 📖 **Xem chi tiết tại**: [Tiêu chuẩn đầu vào Video](references/input_standards.md)
- **Tóm tắt nhanh**:
  - Độ phân giải: 1080p hoặc 4K (Dọc 9:16).
  - FPS: 30 hoặc 60fps.
  - Ánh sáng: Đủ sáng, rõ mặt (đối với Daily/Talk).
