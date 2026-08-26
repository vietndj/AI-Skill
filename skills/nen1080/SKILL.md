---
name: nen1080
description: Kích hoạt khi người dùng nhắc đến "nen1080", "nén 1080", "nén video 1080", "nén chuẩn instagram", "nén video siêu nhẹ", "ép dung lượng video", "nén 1080p", hoặc yêu cầu tối ưu kích thước video về chuẩn Instagram CDN nét cao (~3MB - 5MB cho 30-45s).
---

# KỸ NĂNG NÉN VIDEO 1080P CHUẨN INSTAGRAM TRUE CDN (NEN1080)

Kỹ năng này tự động nén các video gốc nặng hàng trăm MB (từ iPhone, máy quay chuyên nghiệp) về chuẩn **1080p True CDN của Instagram**. Video sau khi nén có dung lượng siêu nhỏ (**chỉ từ 3MB – 5MB cho 30–45 giây**) nhưng vẫn giữ độ nét cực cao và phát tức thì trên mọi thiết bị di động.

---

## 1. 3 CÁCH GỌI TỰ NHIÊN (3 TRIGGER PATTERNS)

| STT | Dạng yêu cầu | Mẫu câu khẩu ngữ của anh Việt | Phản xạ của AI |
| :---: | :--- | :--- | :--- |
| **1** | **Chuẩn Instagram / Mạng xã hội** | • *"Nén video này chuẩn Instagram 1080 cho anh"*<br>• *"Nén video [tên video] theo chuẩn IG nét cao"*<br>• *"Chuyển video này về chuẩn kích thước Instagram"* | Tự động quét file và áp dụng profile 1080p True CDN |
| **2** | **Ép dung lượng / Siêu nhẹ** | • *"Ép video này xuống dưới 5MB mà vẫn nét"*<br>• *"Nén video này nhẹ nhất có thể ở độ phân giải 1080"*<br>• *"Làm cho video này nhẹ như video tải trên mạng về"* | Khống chế bitrate ~1000k, audio 64k, giữ chuẩn 1080p |
| **3** | **Gọi trực tiếp tên Skill / Mã lệnh** | • *"nen1080 [tên video]"*<br>• *"chạy nen1080 file này"*<br>• *"dùng skill nen1080"* | Kích hoạt ngay lập tức script xử lý `compress_1080.py` |

---

## 2. THÔNG SỐ KỸ THUẬT NÉN CHUẨN (SPECIFICATIONS)

* **Resolution**: `1080 × 1920` (hoặc scale giữ đúng tỷ lệ góc, pad viền chuẩn).
* **Video Codec**: `H.264 (libx264)` High Profile, `yuv420p`.
* **Rate Control**: `CRF 28` + `Maxrate 1000k` + `Bufsize 2000k` (VBR tối ưu cảnh chuyển động).
* **Audio Codec**: `AAC` Mono/Stereo `64 kbps` (Đủ chuẩn cho loa di động, giảm tải triệt để).
* **Faststart**: Bật cờ `+faststart` (đưa moov atom lên đầu file để bấm là xem ngay không cần chờ tải hết).

---

## 3. CÁCH THỨC THỰC THI

Khi kỹ năng được kích hoạt:
1. **Chạy script nén tự động**:
   ```bash
   python3 ~/.gemini/config/skills/nen1080/scripts/compress_1080.py "<đường dẫn hoặc tên video>"
   ```
2. **Hiển thị báo cáo kết quả**:
   - Tên file gốc & dung lượng ban đầu (MB).
   - Tên file sau khi nén & dung lượng mới (MB).
   - Tỷ lệ dung lượng tiết kiệm được (% giảm).
   - Clickable link trỏ trực tiếp đến file video đã nén trên máy.
