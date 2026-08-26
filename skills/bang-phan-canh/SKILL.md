---
name: bang-phan-canh
description: >-
  Kích hoạt khi người dùng nhắc đến "bảng phân cảnh", "phân cảnh", "storyboard",
  "lên phân cảnh", "tạo phân cảnh", "bóc phân cảnh kịch bản", "băm nhỏ kịch bản",
  "visual script", hoặc gửi kịch bản nói + ảnh bối cảnh. Tự động hóa quy trình băm
  nhỏ kịch bản thành các micro-beats (Đầu cảnh, Cao trào chi tiết, Mồi chuyển cảnh),
  upload ảnh lên Cloudflare R2, và xuất bản trang HTML Studio tương tác trực tuyến
  lên GitHub Pages.
---

# Kỹ Năng: Tạo Bảng Phân Cảnh Điện Ảnh Tự Động (AI Storyboard Studio)

Kỹ năng này tự động hóa 100% quy trình chuyển đổi **Kịch bản nói (lời thoại + mô tả cảnh)** và **Ảnh bối cảnh gốc** thành **Bảng Phân Cảnh Điện Ảnh 9:16** tương tác đa tầng chuẩn Studio.

---

## 🎯 1. NGUYÊN TẮC CỐT LÕI & CHUẨN ĐẦU RA

1. **Cơ chế phân cảnh 3 nhịp (3-Beat Rhythm):** Mỗi cảnh BẮT BUỘC được băm nhỏ thành 3 khung hình:
   - 🔰 **Đầu cảnh (In-point):** Thiết lập không gian, vị thế nhân vật và điểm chạm mở màn.
   - 🔥 **Chi tiết / Cao trào (Main Action):** Hành động trọng tâm, biểu cảm và cận cảnh nội dung.
   - 🔄 **Cuối cảnh / Mồi chuyển (Out-point Lead):** Động tác kết thúc / ngắt nhịp làm mồi nối mượt sang cảnh kế tiếp (*Match-cut*).
2. **Nhân Vật Mặc Định Tuyệt Đối Là Anh Việt:** Mọi khung hình visual storyboard có nhân vật nam đều MẶC ĐỊNH lấy theo nhân diện anh Việt (khai thác bộ mỏ neo tại `/Users/vietmac/Documents/CODE/Quản gia/assets/ava` và `anh_viet_face_catalog.json`).
3. **Đồng Nhất 100% Trang Phục (Wardrobe Continuity):** Toàn bộ 15 micro-beats trong cùng một bảng phân cảnh BẮT BUỘC phải mặc CÙNG MỘT BỘ TRANG PHỤC duy nhất (khóa mã Wardrobe Anchor Prompt cố định, ví dụ: `wearing a tailored dark charcoal blazer over a crisp plain white crewneck t-shirt`). Tuyệt đối không để AI tự đổi trang phục giữa các cảnh làm gãy nhịp raccord điện ảnh.
4. **Khối Tin Nhắn Gốc (Original Input Context):** Hiển thị nổi bật ở trên cùng file HTML (gồm text kịch bản gốc và ảnh bối cảnh nhận được qua Telegram hoặc Chat).
5. **Giao Diện Sạch (No AI Prompt Box):** Loại bỏ hoàn toàn các box prompt AI lý thuyết, tập trung 100% vào thông số đạo diễn (Cỡ cảnh, Góc máy, Động tác máy, Bố cục, Ghi chú đạo diễn và Lời thoại).
6. **Lưu trữ Cloudflare R2:** Mọi hình ảnh phân cảnh và bối cảnh tham chiếu được lưu trữ vĩnh viễn trên Cloudflare R2 CDN (`https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/storyboards/`).
7. **Xuất bản GitHub Pages:** Tự động đồng bộ và xuất bản web HTML tương tác trực tuyến tại `https://vietndj.github.io/offline02/` (và cổng tra cứu `https://fedu.vn/offline02/`).
8. **Định Dạng Tin Nhắn Telegram Siêu Tinh Gọn:** Khi gửi kết quả qua Telegram cho anh Việt (@nova0410_bot), BẮT BUỘC chỉ gửi **Tiêu đề kịch bản** và **Link HTML online**, ngắn gọn nhất có thể, tuyệt đối không chèn dài dòng.
   * *Mẫu chuẩn:*
     ```text
     🎬 Bảng Phân Cảnh: [Tiêu đề kịch bản]
     🔗 https://vietndj.github.io/offline02/[ten_file].html
     ```

---

## 🗣️ 2. CÁCH GỌI TỰ NHIÊN

### A. 5 Cách Gọi Trong Chat Antigravity / AGY IDE:
1. *"Lên bảng phân cảnh cho kịch bản này giúp tôi, kèm ảnh bối cảnh..."*
2. *"Tạo storyboard 5 cảnh cho video bán hàng này..."*
3. *"Băm nhỏ kịch bản này thành các phân cảnh 3 nhịp (đầu, chi tiết, mồi chuyển)..."*
4. *"Lập visual storyboard 9:16 và xuất ra web html..."*
5. *"Phân cảnh kịch bản này và đẩy ảnh lên R2 + GitHub Pages..."*

### B. 5 Cách Gọi Khi Nhắn Qua Nova Telegram Bot (@nova0410_bot):
1. **Gửi 1-3 ảnh bối cảnh** kèm Caption là nội dung kịch bản thoại.
2. **Gõ lệnh nhanh:** `/storyboard [dán nội dung kịch bản hoặc link online]`
3. **Nhắn tự nhiên:** `Phân cảnh kịch bản này giúp tôi: Cảnh 1... Cảnh 2...`
4. **Nhắn theo tiền tố:** `Bảng phân cảnh: [dán kịch bản 5 cảnh]`
5. **Nhắn yêu cầu:** `Lên phân cảnh video 30s từ kịch bản này...`

---

## ⚙️ 3. QUY TRÌNH THỰC THI

1. **Bóc tách kịch bản (Text / Link Online):** Tự động đọc text hoặc cào ngầm nội dung từ URL (Google Docs, Google Sheets, Web) không cần cấp quyền browser.
2. **Khớp bối cảnh tham chiếu:** Sử dụng ảnh người dùng gửi hoặc ảnh mẫu AI làm seed gốc.
3. **Sinh & Đồng bộ ảnh lên R2:** Lưu trữ ảnh vào `r2:vietndjmedia/storyboards/[slug]/assets/`.
4. **Render HTML Studio & Cập nhật Master Hub:**
   - Biên dịch file HTML kịch bản chi tiết (gồm khối tin nhắn gốc, 15 beats, dải filmstrip, không box AI prompt).
   - Tự động cập nhật thẻ kịch bản mới vào Master Hub `index.html`.
5. **Deploy GitHub Pages & Gửi Tin Nhắn Telegram:**
   - Push lên repo `vietndj/offline02`.
   - Gửi tin nhắn siêu ngắn gọn về Telegram cho anh Việt gồm Tiêu đề và Link trực tuyến.

---

## 📁 4. VỊ TRÍ MÃ NGUỒN & TÀI NGUYÊN MASTER

* **Thư mục Repo GitHub:** `/Users/vietmac/Documents/CODE/offline02`
* **Script Pipeline Chính:** `/Users/vietmac/Documents/CODE/offline02/storyboard_generator.py`
* **Master Hub Index Builder:** `/Users/vietmac/Documents/CODE/offline02/build_master_index.py`
* **Link Master Hub:** `https://vietndj.github.io/offline02/`
* **Cloudflare R2 Base:** `https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/storyboards/`
