---
name: sua-phu-de-capcut
description: Kỹ năng tự động tìm dự án CapCut PC mới nhất, lọc từ đệm thừa ("ấy", "ý", "một cái", "để mà"...), ngắt 2 dòng cân đối chống xé chữ trên video dọc 9:16, sửa chính tả thương hiệu và cập nhật trực tiếp vào dự án CapCut PC. Kích hoạt khi người dùng yêu cầu: "sửa phụ đề video capcut mới tạo", "sửa phụ đề capcut", "sửa phụ đề", "lọc phụ đề capcut".
---

# KỸ NĂNG SỬA & LỌC PHỤ ĐỀ CAPCUT TỰ ĐỘNG (CAPCUT SUBTITLE FIXER & PUNCHY FILTER V5)

Khi người dùng yêu cầu "sửa phụ đề", "lọc phụ đề", "sửa phụ đề video capcut", AI **BẮT BUỘC** tự động quét dự án CapCut mới nhất, lọc sạch từ thừa và ngắt dòng chuẩn theo quy trình bên dưới:

---

## 🎯 3 PHƯƠNG ÁN LỌC PHỤ ĐỀ (3-TIER FILTERING PARADIGM)

| Cấp Độ | Tên Chế Độ | Mục Đích & Nguyên Tắc | Khi Nào Dùng? |
| :--- | :--- | :--- | :--- |
| **Level 1** | **Clean Raw**<br>*(Lọc đệm cơ bản)* | - Giữ nguyên 90-95% câu nói gốc.<br>- Chỉ xóa ậm ờ, từ đệm đuôi (`ờ, à, ừm, ấy, ý, nhé, nè, nhỉ, nha, luôn ấy`), xóa từ lặp (`tôi tôi`, `là là`). | Podcast, Talkshow, Phỏng vấn sâu cần giữ nguyên ngữ điệu tự nhiên. |
| **Level 2** ⭐<br>*(Mặc định)* | **Punchy Short-form**<br>*(Cô đọng sắc bén)* | - **Gọt sạch 100% từ đệm + từ nối rườm rà**: `một cái`, `những cái`, `các cái`, `để mà`, `sau khi mà`, `cho nên là`, `bởi vì là`, `thế là`, `rất là`, `xong rồi`, `nói chung là`, `tức là`.<br>- Giữ trọn 100% ý nghĩa cốt lõi nhưng câu ngắn hơn 30-40%, đọc lướt 0.5s là hiểu ngay.<br>- Cân đối 2 dòng (mỗi dòng <= 22-26 ký tự). | **Mặc định cho Video ngắn Reels / TikTok / Shorts** (Times City, Bàn gỗ, Review...). |
| **Level 3** | **Action-Driven Hook**<br>*(Mệnh lệnh thực chiến)* | - Biến câu nói thành các câu hành động ngắn, đập thẳng vào mắt (3-5 từ/beat).<br>- Áp dụng triệt để bộ lọc Sổ Đen & văn phong thực chiến của kỹ năng `loc`. | Video bán hàng (Miss Sale), Ads chuyển đổi cao, Hook 3 giây đầu. |

---

## 🛠️ QUY TRÌNH THỰC THI 4 BƯỚC

### 1. Tự Động Quét Dự Án & Chạy Bộ Lọc
- Chạy script Python tự động tìm dự án mới nhất và áp dụng bộ lọc:
  ```bash
  python3 ~/.gemini/config/skills/sua-phu-de-capcut/scripts/fix_capcut_subtitles.py --level 2
  ```
- Hoặc chỉ định dự án cụ thể:
  ```bash
  python3 ~/.gemini/config/skills/sua-phu-de-capcut/scripts/fix_capcut_subtitles.py "tên_project" --level 2
  ```

### 2. Thuật Toán Ngắt 2 Dòng Chống Xé Chữ (Smart Balanced Break)
- **Giới hạn dòng đơn**: Nếu câu ngắn (<= 20 ký tự, <= 4 từ) $ightarrow$ Giữ nguyên 1 dòng.
- **Nếu câu dài (> 20 ký tự)**: Tự động ngắt thành 2 dòng cân đối (`
`), ưu tiên ngắt sau dấu phẩy hoặc trước liên từ (`mà`, `nhưng`, `để`, `là`, `thì`...).
- **Giới hạn an toàn**: Mỗi dòng **tối đa <= 24-26 ký tự**, tuyệt đối không để rớt 1 chữ đơn lẻ (orphan word) hay xé đôi từ có dấu (vd: `cà` và `ng`, `l` và `à`).
- **Đồng bộ Token 1-to-1**: Cập nhật chính xác `words['text']`, `words['start_time']`, `words['end_time']` và `styles[0]['range']` khớp với ký tự `
`.
- Tắt ép cuộn dòng tự động của CapCut (`force_apply_line_max_width = False`).

### 3. Chuẩn Hóa Thương Hiệu & Viết Hoa
- Chuẩn hóa tên thương hiệu: `ChatGPT`, `CapCut`, `TikTok`, `YouTube`, `Facebook`, `App Store`, `Play Store`, `B-roll`, `Cutaway`, `Talking Head`, `Video Ads`, `Video Marketing`, `Đế Chế`...
- Khắc phục lỗi viết hoa tùy tiện giữa câu của CapCut Auto-Caption.

### 4. Báo Cáo & Bắn Thông Báo Telegram
- Báo cáo rõ: Tên dự án CapCut, số lượng câu phụ đề đã xử lý, bảng so sánh Before vs After.
- Bắn thông báo hoàn tất qua Telegram bot NOVA-CORE (`telegram_notify.py`).
- Nhắc anh Việt nhấn `Cmd + Q` thoát hẳn CapCut và mở lại để cập nhật thay đổi.
