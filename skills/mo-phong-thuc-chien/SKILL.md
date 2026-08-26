---
name: mo-phong-thuc-chien
description: Kích hoạt khi người dùng nhắc đến "mô phỏng", "MÔ PHỎNG", "test thực chiến", "chạy thực tế", "vòng lặp phản hồi", "kiểm thử toàn diện", "tự test và nghiệm thu", "tự chạy thử", "mô phỏng hoạt động thật". Kỹ năng buộc AI kích hoạt Vòng Lặp Phản Hồi Thực Tế (Empirical Verification & Self-Correction Loop), tự chạy kiểm thử chuỗi mắt xích từ đầu đến cuối, tự đọc log sửa lỗi ngầm và trình bày báo cáo nghiệm thu bằng dữ liệu đo lường thật.
---

# KỸ NĂNG MÔ PHỎNG NGHIỆM THU THỰC CHIẾN (SIMULATION & EMPIRICAL VERIFICATION PROTOCOL)

Khi người dùng kích hoạt từ khóa (VD: *"mô phỏng lại..."*, *"tự test thực chiến..."*, *"chạy thử luồng thực tế..."*), AI **TUYỆT ĐỐI KHÔNG DỪNG LẠI Ở VIỆC VIẾT CODE LÝ THUYẾT**, mà BẮT BUỘC thực hiện quy trình kiểm thử 4 bước sau:

## 1. PHÂN TÍCH CHUỖI MẮT XÍCH ĐẦU - CUỐI (END-TO-END CHAIN MAPPING)
- Liệt kê toàn bộ các mắt xích trong chuỗi quy trình mà tính năng đi qua:
  - Input (Trigger / Lệnh / File / Webhook / Telegram).
  - Background Processing (Worker / Daemon / Script / Thuật toán).
  - Integration & Storage (Database / Cloudflare R2 / Google Drive / GitHub Pages).
  - Output & Notification (UI Responsive / Modal / Lightbox / Tin nhắn thông báo).

## 2. KÍCH HOẠT THỰC THI & TẠO DỮ LIỆU THỬ NGHIỆM THẬT (LIVE EXECUTION)
- Tự động chuẩn bị dữ liệu mẫu (hoặc trigger lệnh thật qua CLI/API/Background Queue).
- Trực tiếp chạy lệnh thực tế trên hệ thống máy Mac qua `run_command`.
- BẮT BUỘC kiểm tra trạng thái tiến trình nền (`ps`, `lsof`, `launchctl`, log file) để xác nhận hệ thống đã thực sự tiếp nhận và xử lý.

## 3. VÒNG LẶP ĐỌC LOG & TỰ SỬA LỖI NGẦM (SELF-CORRECTION LOOP)
- Đọc chi tiết `stdout`, `stderr`, và file log hệ thống.
- **Nếu phát hiện bất kỳ lỗi nào** (lỗi thiếu biến môi trường, cắt cụt chuỗi lệnh, lỗi cú pháp JS ngầm, lỗi kết nối port, file 404):
  - **TỰ ĐỘNG SỬA CODE NGAY LẬP TỨC**.
  - Khởi động lại dịch vụ liên quan (nếu là daemon/service).
  - Chạy lại kiểm thử cho đến khi toàn bộ quy trình đạt **100% Exit Code 0**.

## 4. BÁO CÁO NGHIỆM THU DỮ LIỆU THẬT & MÔ PHỎNG TRẢI NGHIỆM ĐẦU RA
Trình bày kết quả bàn giao cho anh Việt theo cấu trúc chuẩn 3 phần:
1. **Dữ liệu Đo lường Thực tế (Empirical Metrics)**:
   - ID phiên làm việc / PID tiến trình thực tế.
   - Dung lượng file (KB/MB) sau khi tối ưu.
   - Trạng thái HTTP status, phản hồi API thực tế.
2. **Nội dung Thông báo Đầu ra (Real Output Dispatch)**:
   - Hiển thị chính xác nguyên văn thông báo/tin nhắn đã được gửi đi (Telegram, Email, Terminal).
   - Kèm các đường link truy cập trực tiếp có thể click mở ngay.
3. **Mô phỏng Trải nghiệm Người Dùng Cuối (User Experience Simulation)**:
   - Mô phỏng chi tiết người dùng trên **Điện thoại (Mobile)**: Cảm giác lướt, bố cục responsive, các nút bấm thao tác ngón tay cái, tốc độ hiển thị.
   - Mô phỏng chi tiết người dùng trên **Máy tính (Desktop)**: Giao diện chia đôi, phím tắt điều khiển, trải nghiệm đa nhiệm.

## QUY TẮC CỐT LÕI VỀ GIAO TIẾP
- Xưng hô chuẩn mực: **"em - anh Việt"**.
- Tuyệt đối **KHÔNG dùng đường kẻ ngang (`---`)**.
- Luôn giữ độ thoáng và nhịp thở thị giác (`\n\n`) giữa các đoạn văn.
