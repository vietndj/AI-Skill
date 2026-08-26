---
name: anh-xa-boi-canh
description: >-
  Kích hoạt khi người dùng nhắc đến "ánh xạ", "ánh xạ bối cảnh", "bối cảnh của tôi",
  "kho bối cảnh", "bối cảnh Times City", "bối cảnh nhà tôi", "quay theo bối cảnh thực tế",
  "kho R2 bối cảnh", "remake bối cảnh", "áp vào bối cảnh của tôi", hoặc yêu cầu chuyển thể/ráp
  video mẫu, kịch bản quay vào các địa điểm thực tế của người dùng (Times City & Home Studio).
---

# Kỹ Năng: Tự Động Ánh Xạ Bối Cảnh Thực Chiến (Times City & Home Studio)

Kỹ năng này cho phép AI tự động truy xuất và sử dụng **Kho dữ liệu 124 bối cảnh thực địa** đã được chuẩn hoá và lưu trữ trên **Cloudflare R2 CDN**, phục vụ việc chuyển thể kịch bản (Remake/Mapping) từ video mẫu sang các địa điểm quay thực tế của người dùng.

---

## 📂 1. Vị Trí Dữ Liệu & Nguồn Tham Chiếu Master

Khi người dùng kích hoạt kỹ năng này, AI **TỰ ĐỘNG** đọc và tham chiếu từ:
1. **Master Catalog JSON:** `/Users/vietmac/Documents/CODE/Video phan tich/location_master_catalog.json`
2. **Cloudflare R2 CDN Base:** `https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/locations/raw/loc_XX.jpg`
3. **Báo Cáo Trực Quan:** `https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/reports/Bao_Cao_Boi_Canh_Thuc_Chien_R2.html`

---

## 🏛️ 2. Hệ Thống 5 Nhóm Bối Cảnh Thực Địa

| Mã Nhóm | Tên Nhóm & Quy Mô | Đặc Điểm Nhận Diện Tuyệt Đối | Ứng Dụng Quay Tối Ưu |
| :--- | :--- | :--- | :--- |
| **`TimesCity_Outdoor`** | **Times City • Đường Chạy & Ngoại Cảnh** *(39+ ảnh)* | Đường chạy bộ lát đá cobble xám uốn lượn dưới tán cây cổ thụ; đại lộ đôi rộng lớn đón bình minh/hoàng hôn; thảm cỏ hoa ngũ sắc; giàn pergola cam. | Tracking shot chạy bộ, cảnh establishing đô thị, lướt qua hàng cây tạo visual speed. |
| **`TimesCity_Commercial`** | **Times City • Thương Mại & Cư Dân** *(25+ ảnh)* | Mặt tiền tiệm bánh Bread Talk kính trong suốt; siêu thị WinMart; Circle K; cụm tượng đài nấm kim loại & vòm gỗ; nhóm tập dưỡng sinh áo đỏ, cún Poodle. | B-roll nhịp sống, dừng chân nạp năng lượng, check-in sau tập, đời thường gần gũi. |
| **`TimesCity_GymCalifornia`** | **Times City • Phòng Gym California** *(22+ ảnh)* | Dàn máy chạy treadmill xếp hàng dài view kính trần công nghiệp; sảnh tiếp khách bàn ghế tròn đỏ rực; cầu thang bộ & thang cuốn tay vịn đỏ rực rỡ. | Cảnh chạy nước rút trên máy, bấm nút bắt đầu tập luyện cường độ cao, đếm ngược thời gian. |
| **`Home_OfficeDesk`** | **Nhà Riêng • Phòng Làm Việc Bàn Gỗ** *(23+ ảnh)* | Bàn gỗ tự nhiên dài nguyên khối đặt cạnh cửa sổ lớn mở rộng nhìn ra vòm cây xanh mát; góc setup máy tính làm việc; ánh sáng xiên tự nhiên. | Cảnh ngồi làm việc tập trung (Deep Work), review sản phẩm trên bàn gỗ mộc, shot Over-the-shoulder. |
| **`Home_ShootingRoom_Balcony`** | **Nhà Riêng • Phòng Quay & Ban Công** *(15+ ảnh)* | Sàn gỗ bóng ấm áp, chậu Monstera trầu bà Nam Mỹ xẻ lá khổng lồ; hệ 4 cánh cửa kính lùa nhôm đen đón vệt nắng xiên; dù tản sáng softbox; ban công sân gạch đỏ/sàn gốm chậu hoa lan. | Cảnh Jump-cut thay trang phục, khởi động ngày mới, video chia sẻ nói chuyện trước ống kính, B-roll ban công. |

---

## ⚙️ 3. Quy Trình Thực Thi Khi Người Dùng Gửi Yêu Cầu

1. **Phân tích Video mẫu / Yêu cầu:** Bóc tách nhịp điệu, góc máy, chuyển cảnh (cuts/wipes/transitions) và thông điệp.
2. **Khớp Bối Cảnh 1-to-1:** Tra cứu `location_master_catalog.json`, chọn chính xác mã `LOC_XXX` và Tên Semantic phù hợp nhất với hành động của từng shot.
3. **Soạn Kịch Bản Đạo Diễn:**
   - Số thứ tự phân cảnh & thời lượng (giây).
   - Tên bối cảnh & Mã `LOC_XXX`.
   - Mô tả hành động & Lời thoại/Voice-over.
   - Góc máy & Cỡ cảnh (Shot type).
   - Kỹ thuật chuyển cảnh (Match cut / Wipe / Pan / Cut on action).
4. **Nhúng Ảnh CDN R2:** Đính kèm trực tiếp đường dẫn ảnh Cloudflare R2 tương ứng `https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/locations/raw/loc_XX.jpg` vào báo cáo để người dùng xem trực quan.

---

## ⚡ 4. Danh Sách 5 Mantra Viết Hoa (Chuẩn Xác 100%)

Khi người dùng nhập các lệnh viết hoa dưới đây, AI thực thi ngay lập tức mà không cần hỏi lại:
1. `ÁNH XẠ BỐI CẢNH` (hoặc `ANHXABOICANH`): Tự động ráp kịch bản / video mẫu vào kho 124 bối cảnh thực tế của anh Việt. Gán mã `LOC_XXX`, cỡ cảnh, kỹ thuật chuyển cảnh và link ảnh CDN R2.
2. `CHECK BỐI CẢNH [ĐỊA ĐIỂM]` (hoặc `TRA BỐI CẢNH [ĐỊA ĐIỂM]`): Kiểm tra danh sách góc quay của khu vực cụ thể (`BÀN GỖ`, `TIMES CITY`, `GYM CALI`, `PHÒNG QUAY`, `BAN CÔNG`).
3. `KHO BỐI CẢNH` (hoặc `BẢN ĐỒ BỐI CẢNH`): Mở và xuất bản đồ tổng quan 124 bối cảnh + 5 phân khu + link báo cáo HTML online.
4. `REMAKE BỐI CẢNH`: Phân tích video mẫu và chuyển thể 1-1 sang kịch bản quay thực chiến tại bối cảnh anh Việt.
5. `STORYBOARD BỐI CẢNH`: Xuất bảng phân cảnh hoàn chỉnh gắn mã `LOC_XXX`, đồng nhất khuôn mặt anh Việt, đồng nhất trang phục và nhúng ảnh R2.

