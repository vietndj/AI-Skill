---
name: tao-slide-pro
description: Kích hoạt khi người dùng nhắc đến "bật figma slide", "tạo slide figma", "slide figma", "kết nối figma", "sửa figma", "vẽ sơ đồ figma", "mindmap figma", "figjam", "figma live sync", "tắt figma", hoặc yêu cầu tạo/sửa slide bài giảng chuyên nghiệp phong cách anh Việt (Charcoal Slate #282928, Typography SVN, Signature Header/Footer, Avatar Mentor). Hỗ trợ 3 môi trường Figma Design, Figma Slides & FigJam qua Live Sync On-Demand hoặc xuất bản PowerPoint PPTX đồng bộ Google Drive.
---

# Kỹ Năng Thiết Kế Slide, Sơ Đồ & Biên Tập Figma/FigJam (Tao-Slide-Pro) - On-Demand Mode

Kỹ năng này biến AI thành một Co-pilot thiết kế & biên tập thực chiến của **anh Việt**, giao tiếp 2 chiều theo thời gian thực với **Figma Design, Figma Slides và FigJam** theo cơ chế **On-Demand (Zero-Resource khi không sử dụng)** hoặc xuất bản file **PowerPoint (.pptx)** đồng bộ Google Drive.

---

## 5 Cách Gọi / Ra Lệnh Chắc Chắn Kích Hoạt Kỹ Năng

| STT | Mục đích sử dụng | Câu lệnh gọi chắc chắn kích hoạt | Hành vi AI thực hiện tự động |
| :--- | :--- | :--- | :--- |
| **1** | **Tạo slide bài giảng / chia sẻ theo chủ đề** | **"Tạo slide figma về [chủ đề]"** *(hoặc "Lên slide figma đối chiếu...")* | Tự động phân tích nội dung, áp dụng đúng chuẩn **Cover Kiểu 01 (Slide 85)** cho slide đầu và **Kiểu 03 (2 Cột Đối Chiếu)** / **Kiểu 02 (3 Cột)** cho các slide sau, đẩy trực tiếp lên Figma. |
| **2** | **Bật kết nối & Kiểm tra trạng thái** | **"Bật figma slide"** *(hoặc "Kết nối figma")* | Đánh thức Bridge Server On-Demand (`0.2s`), kiểm tra kết nối với Plugin Figma Slides và báo cáo trạng thái sẵn sàng. |
| **3** | **Nhân bản slide siêu tốc theo mẫu đang chọn** | **"Clone slide figma với nội dung [text/JSON]"** | Đọc slide đang chọn trên Figma, nhân bản và thay thế số thứ tự, tiêu đề, nội dung tức thì chỉ trong `0.3s/slide`. |
| **4** | **Sửa văn bản / Tối ưu slide trực tiếp** | **"Sửa figma slide đang chọn"** *(hoặc "Sửa text đang chọn cho hay hơn")* | Lấy vùng chọn trên Figma, viết lại theo văn phong thực chiến ngắn gọn và cập nhật ngược lại trực tiếp vào layer. |
| **5** | **Vẽ Sơ đồ tư duy / Flowchart quy trình** | **"Vẽ mindmap figma về [chủ đề]"** *(hoặc "Tạo flowchart trên figjam")* | Tự dựng sơ đồ phân nhánh hoặc biểu đồ hình khối có mũi tên liên kết trực tiếp trên FigJam / Figma. |

---

## 1. Cơ Chế Hoạt Động On-Demand (Tối Ưu Tài Nguyên Tuyệt Đối)

* **Khi bình thường:** Tiến trình tắt hoàn toàn (`0 MB RAM, 0% CPU`).
* **Khi người dùng yêu cầu làm việc:** AI tự động đánh thức server trong `0.2 giây` ngầm để giao tiếp với Figma / FigJam.
* **Khi người dùng bảo dừng/tắt:** AI tự động giải phóng tiến trình (`helper.py stop`).

### 🔹 Các lệnh AI tự động gọi:
1. **Đọc Selection trực tiếp từ Figma / FigJam (Tự đánh thức server):**
   ```bash
   python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py get
   ```
2. **⚡ TẠO SLIDE SIÊU TỐC THEO THIẾT KẾ ĐANG CHỌN (Clone & Smart Fill - 0.3s/slide) [ƯU TIÊN SỐ 1]:**
   > [!TIP]
   > Khi người dùng đang chọn 1 Slide mẫu trên Figma và muốn tạo slide mới theo thiết kế đó, **LUÔN DÙNG LỆNH CLONE**. Không dựng lại từ đầu để tiết kiệm 10x thời gian và bảo toàn 100% layout chuẩn:
   > ```bash
   > # 1 slide:
   > python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py clone '{"number": "04", "title": "TIÊU ĐỀ MỚI", "subtitle": "phụ đề mới", "questionText": "...", "poemText": "..."}'
   > 
   > # Hàng loạt N slide từ file JSON:
   > python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py clone /tmp/batch_slides.json
   > ```

3. **Tạo Bộ Slide Mới từ đầu (Khi chưa có slide mẫu):**
   > [!IMPORTANT]
   > Khi tạo từ **2 slide trở lên**, BẮT BUỘC lưu danh sách slide thành file JSON tạm (VD: `/tmp/deck.json`) rồi gọi 1 lệnh duy nhất:
   > ```bash
   > python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py create /tmp/deck.json
   > ```
   > **TUYỆT ĐỐI KHÔNG** gọi lệnh tạo từng slide đơn lẻ liên tiếp vì sẽ làm đè vùng chọn hoặc đảo lộn thứ tự!

4. **Cấu trúc JSON Chuẩn Cho Bộ Slide:**
   ```json
   [
     {
       "layout": "cover",
       "number": "0",
       "title_part1": "Làm thế nào",
       "title_part2": "Video đẹp ?",
       "subtitle": "Khi đã biết cách dùng capcut & quay bằng đt rất nét rồi"
     },
     {
       "layout": "2_columns",
       "section": "ĐỐI CHIẾU 01 • MỤC TIÊU & TÂM LÝ",
       "title": "CHUYỂN HOÁ NHẬN THỨC VS THÚC ÉP MUA HÀNG",
       "subtitle": "sự khác biệt gốc rễ giữa nuôi dưỡng niềm tin và săn bắt doanh số tức thì",
       "cards": [
         {
           "badge": "❌ 01 • VIDEO ADS (QUẢNG CÁO CHUYỂN ĐỔI)",
           "title": "SĂN BẮT DOANH SỐ & BẬT KHIÊN ĐỀ PHÒNG",
           "desc": "• Mục tiêu cốt lõi: Bán hàng ngay lập tức (Hard Sell), gom data nóng, ép khách bấm mua trên từng đồng chi phí.\n\n• Tâm lý người xem: Cảm thấy đang bị chào bán. Bật khiên đề phòng, phán xét và lướt qua ngay nếu chưa có nhu cầu cấp bách.",
           "takeaway": "Ads giải quyết dòng tiền ngắn hạn nhưng khiến tệp khách hàng cảnh giác."
         },
         {
           "badge": "✅ 02 • VIDEO MARKETING (ĐÓNG GÓI GIÁ TRỊ)",
           "title": "GIEO HẠT NHẬN THỨC & TỰ NGUYỆN TÌM MUA",
           "desc": "• Mục tiêu cốt lõi: Xây dựng uy tín, niềm tin (Trust), định vị chuyên gia đầu ngành và chuyển hoá nhận thức lâu dài.\n\n• Tâm lý người xem: Cảm thấy được nhận giá trị, mở mang tư duy. Người xem biết ơn, tự nguyện follow và chủ động tìm mua.",
           "takeaway": "Marketing nuôi dưỡng lòng tin để khách hàng tự chốt đơn mà không cần ép mua."
         }
       ]
     },
     {
       "layout": "3_columns",
       "section": "KỊCH BẢN THỰC CHIẾN",
       "title": "3 TẦNG ĐÀO SÂU TỰ SỰ VIRAL",
       "subtitle": "công thức bóc trần sự thật ngượng miệng",
       "cards": [
         {
           "badge": "TẦNG 1 • SAFE",
           "title": "Bề nổi ai cũng thấy",
           "desc": "Nêu đúng nỗi đau hoặc sự thật đời thường quen thuộc. Mở khoá sự chú ý ngay 3 giây đầu.",
           "takeaway": "Mở khoá chú ý"
         },
         {
           "badge": "TẦNG 2 • REAL",
           "title": "Lý do thực sự bên trong",
           "desc": "Ép não bộ hỏi 'Tại sao' 2 lần. Bóc trần sự thật ngượng miệng mà số đông né tránh.",
           "takeaway": "Chạm đúng nỗi đau"
         },
         {
           "badge": "TẦNG 3 • RAW",
           "title": "Đóng gói giải pháp cốt lõi",
           "desc": "Đưa ra công thức dứt điểm vấn đề. Biến chiêm nghiệm thành hành động cụ thể.",
           "takeaway": "Tạo niềm tin tuyệt đối"
         }
       ]
     },
     {
       "layout": "quote",
       "section": "BÀI HỌC ĐÚC KẾT",
       "title": "CÔNG THỨC KẾT HỢP MARKETING & ADS",
       "subtitle": "marketing đi trước tạo niềm tin, ads tiếp sức bùng nổ",
       "quote": "Đừng bao giờ chạy Ads khi kênh chưa có Video Marketing tạo dựng niềm tin. Hãy dùng Video Marketing để xây 'đập giữ nước' trước, rồi mới dùng Ads để 'mở van xả nước' mang doanh thu bùng nổ.",
       "takeaway": "🎯 80% Năng lượng đóng gói giá trị (Organic) + 20% Ngân sách vít Ads bài có chuyển đổi cao nhất."
     }
   ]
   ```

5. **Sửa văn bản đang chọn (Hỗ trợ Text, Slide, Sticky Notes, Shapes, Code Block):**
   ```bash
   python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py replace "Nội dung văn bản mới"
   ```
6. **Sửa Tiêu đề / Phụ đề slide:**
   ```bash
   python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py update --title "TIÊU ĐỀ MỚI" --subtitle "phụ đề mới"
   ```
7. **Tạo Sơ đồ tư duy (Mindmap phân nhánh) trên FigJam:**
   ```bash
   python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py mindmap '{
     "topic": "Chủ đề chính",
     "branches": [
       {"title": "Ý tưởng 1", "sub": ["Ý con 1.1", "Ý con 1.2"]},
       {"title": "Ý tưởng 2", "sub": ["Ý con 2.1"]},
       {"title": "Ý tưởng 3"}
     ]
   }'
   ```
8. **Tạo cụm Sticky Notes trên FigJam:**
   ```bash
   python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py stickies '[
     {"text": "Ý tưởng 1...", "color": "YELLOW"},
     {"text": "Ý tưởng 2...", "color": "BLUE"},
     {"text": "Ý tưởng 3...", "color": "GREEN"}
   ]'
   ```
9. **Tạo Sơ đồ quy trình / Flowchart trên FigJam:**
   ```bash
   python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py flow '[
     {"title": "Bước 1", "desc": "Thu thập yêu cầu", "shape": "ROUNDED_RECTANGLE"},
     {"title": "Bước 2", "desc": "Xử lý logic", "shape": "ROUNDED_RECTANGLE"},
     {"title": "Bước 3", "desc": "Triển khai kết quả", "shape": "ROUNDED_RECTANGLE"}
   ]'
   ```
10. **Tắt Bridge Server khi kết thúc:**
    ```bash
    python3 ~/.gemini/config/skills/tao-slide-pro/scripts/helper.py stop
    ```

---

## 2. Bảng Menu 6 Kiểu Layout Chuẩn Hóa Slide (Design Presets)

| Mã Kiểu | Tên Layout | Thuộc tính JSON nhận diện | Bố cục & Tiêu chuẩn chi tiết |
| :--- | :--- | :--- | :--- |
| **Kiểu 01** | **Editorial Giant Anchor Number (Slide 85 Master Standard)** | `layout: "cover"`, `number: "0"`, `watermark: "0"` | **Slide Mở Đầu (Bắt buộc cho slide 1):** Số khổng lồ `1636px` (`#3C3C3C`, opacity 0.99) tràn mép trái (`x = -178, y = -401`) + Cụm tiêu đề song tấu tại `x = 899, y = 418` (Vế 1 Serif Nghiêng `SVN-Freight Display Medium Italic` 89px & Vế 2 Sans `SVN-Aeonik Medium` 77px) + Subtitle 28px (`x = 899, y = 540`) + Top Header `2026` & `imess/zalo : 0934688632` + Hairline đáy `y = 955` + Mentor Footer Signature (`x = 1590, y = 1000`). |
| **Kiểu 02** | **3-Column Breakdown (3 Tầng)** | `layout: "3_columns"` hoặc `cards: [3 phần tử]` | 3 Cột lớn song song (`w = 570px`): Header badge cyan + Tiêu đề thẻ `28px` + Hairline phân tách + Body text `22px` (`lineHeight 160%`) + Hộp Takeaway xanh ngọc ở đáy. |
| **Kiểu 03** | **Luxury Comparison 2 Columns (Slide 10 Master Standard)** | `layout: "2_columns"` hoặc `cards: [2 phần tử]` | **2 Khối Đối Chiếu Sang Trọng (`w = 868px`):**<br>• Cột Trái (Cảnh báo/Ads): Viền đỏ `#FCA5A5` 1.5px, Badge `❌ 01 • ...` (`SVN-Aeonik Bold 20px`, đỏ `#DC2626`), Tiêu đề thẻ `32px` (`SVN-Integral CF Bold`), Hairline phân cách 1px `#E2E8F0`, Body `25px` (`lineHeight 155%`) phân đoạn `\n\n`, Hộp Takeaway bo góc 10px.<br>• Cột Phải (Chuẩn chỉ/Marketing): Viền xanh ngọc `#6EE7B7` 1.5px, Badge `✅ 02 • ...` (`SVN-Aeonik Bold 20px`, xanh `#059669`), Tiêu đề thẻ `32px`, Hairline phân cách 1px, Body `25px`, Hộp Takeaway bo góc 10px. |
| **Kiểu 04** | **Prompt & Code Jet Dark** | `layout: "code"` hoặc `code_lines: [...]` | Cột trái giải thích logic; Cột phải là hộp IDE Dark Jet `#0F172A` có 3 nút tròn Mac OS đỏ-vàng-xanh chứa code/prompt XML chuẩn chỉ. |
| **Kiểu 05** | **4-Grid Matrix** | `layout: "4_grid"` hoặc `cards: [4 phần tử]` | 4 cột song song / ma trận với badge số `01, 02, 03, 04`. |
| **Kiểu 06** | **Big Quote / Takeaway** | `layout: "quote"` hoặc `quote: "..."` | 1 Câu khẩu quyết cốt lõi cỡ lớn `40px` (`SVN-Freight Display Medium Italic`) ở giữa màn hình + Thẻ đúc kết hành động thực chiến ở đáy. |

---

## 3. Hệ Thống Tiêu Chuẩn Thiết Kế Slide Mới (Design System 2.0)

> [!IMPORTANT]
> **3 NGUYÊN TẮC BẤT DI BẤT DỊCH CỦA ANH VIỆT:**
> 1. **SLIDE TIÊU ĐỀ ĐẦU TIÊN (COVER) LUÔN DÙNG KIỂU 01 (GIANT ANCHOR NUMBER 0):**
>    - Số khổng lồ `1636px` (`SVN-Aeonik Black`, màu `#3C3C3C`, tràn viền mép trái `x = -178px, y = -401px`) để neo giữ thị giác trong 0.2s đầu tiên.
>    - Mặc định đánh số `0` (người dùng sẽ đổi số 1, 2, 3... sau tùy ý).
>    - Cụm tiêu đề song tấu: Serif nghiêng (`SVN-Freight Display Medium Italic` 89px) + Sans dứt khoát (`SVN-Aeonik Medium` 77px) + Subtag 28px (`SVN-Aeonik Regular`).
>    - Nền trắng tinh khiết `#FFFFFF`, Top Header `2026` & `imess/zalo : 0934688632`, Hairline đáy `y = 955px`, Mentor Footer Signature `x = 1590, y = 1000`.
> 2. **TẤT CẢ SLIDE NỘI DUNG TIẾP THEO (SLIDES 2+):**
>    - Dùng chuẩn **NỀN TRẮNG TINH KHIẾT `#FFFFFF`** với chữ than chì đậm `#0F172A` / `#334155` sắc nét, thẻ Container `#F8FAFC`, Viền `#E2E8F0`, Takeaway trắng/xanh ngọc.
>    - Header Top dàn đều 2 đầu (`SPACE_BETWEEN`): `2026  •  TÊN CHUYÊN MỤC` ở trái và `imess/zalo : 0934688632` ở phải.
>    - Footer Bar dàn đều 2 đầu: Mentor Profile (Avatar + `Mentor : Nguyễn Đức Việt` / `0934.688.632`) ở trái và `vietndj@gmail.com` ở phải.
> 3. **CẤU TRÚC THẺ ĐỐI CHIẾU 2 CỘT (KIỂU 03):**
>    - **BẮT BUỘC** có Cụm Header Thẻ riêng: Badge phân loại màu + Tiêu đề thẻ lớn `32px` (`SVN-Integral CF Bold`).
>    - **BẮT BUỘC** có đường kẻ Hairline 1px `#E2E8F0` ngăn cách tiêu đề và nội dung bên dưới.
>    - Nội dung body phải có khoảng cách dòng thông thoáng (`lineHeight: 155%`) và ngắt đoạn `\n\n`.

