---
name: telegram-dispatcher
description: Kích hoạt khi người dùng nhắc đến "gửi tin nhắn", "gửi link tin nhắn", "bắn tin", "bắn qua tele", "nhắn cho anh", "báo qua bot", "gửi file qua tele", "ping tin nhắn". Tự động nhận diện 5 cách gọi tự nhiên và gửi dữ liệu qua Bot Telegram NOVA-CORE.
---

# KỸ NĂNG ĐIỀU PHỐI TIN NHẮN BOT TELEGRAM NOVA-CORE (TELEGRAM DISPATCHER)

Kỹ năng này thiết lập **phản xạ tự động không điều kiện** cho AI: Bất cứ khi nào anh Việt đưa ra yêu cầu gửi tin nhắn, gửi link, gửi kết quả, hoặc chia sẻ tệp tin bằng các câu khẩu ngữ tự nhiên, AI **BẮT BUỘC** gọi module `telegram_notify.py` để đẩy dữ liệu thẳng vào tài khoản Telegram của anh Việt.

## 1. 5 CÁCH GỌI TỰ NHIÊN ĐƯỢC GHI NHỚ (5 TRIGGER PATTERNS)

| STT | Khẩu ngữ / Câu lệnh của anh Việt | Ý định (Intent) | Hành động tương ứng của AI |
| :--- | :--- | :--- | :--- |
| **1** | *"Gửi link tin nhắn cho tôi [link/nội dung]"* <br> *"Gửi tin nhắn cho tôi link html/báo cáo"* | Gửi đường link hoặc file HTML vừa tạo vào Telegram | Gọi `--msg` gửi link trực tiếp kèm tóm tắt nội dung để anh Việt bấm mở ngay trên điện thoại. |
| **2** | *"Bắn qua Telegram cho anh"* <br> *"Bắn tin qua Tele nhé"* <br> *"Bắn cái này qua bot"* | Yêu cầu gửi nhanh nội dung tóm tắt | Gọi `--msg` với nội dung cô đọng, định dạng HTML rõ ràng. |
| **3** | *"Nhắn cho tôi cái này"* <br> *"Nhắn cho anh qua bot"* <br> *"Gửi tin nhắn cho tôi"* | Giao việc chuyển tiếp văn bản/kết quả | Đóng gói toàn bộ kết quả cần báo và gọi `--msg` gửi ngay. |
| **4** | *"Gửi kết quả / file / ảnh này vào tin nhắn Telegram giúp anh"* <br> *"Gửi file này qua tele"* | Gửi file đính kèm hoặc ảnh chụp | Xác định đường dẫn file/ảnh và gọi `--file` hoặc `--photo` kèm caption. |
| **5** | *"Báo qua bot nhé"* <br> *"Xong thì ping/báo tin nhắn cho anh"* <br> *"Chạy xong nhắn anh"* | Kích hoạt chuông thông báo khi hoàn thành tác vụ dài | Tự động chèn lệnh gọi `telegram_notify.py` ở bước cuối cùng của tiến trình. |

## 2. THÔNG TIN BOT & CÚ PHÁP THỰC THI CHUẨN

* **Bot Telegram**: `NOVA-CORE` (`@nova0410_bot`)
* **Chat ID**: `2050406425`
* **Vị trí script**: `/Users/vietmac/Documents/CODE/Quản gia/telegram_notify.py`

### Cú pháp lệnh thực thi qua terminal:

1. **Gửi tin nhắn văn bản / Link URL**:
   ```bash
   python3 /Users/vietmac/Documents/CODE/Quản\ gia/telegram_notify.py --msg "<b>Tiêu đề thông báo</b>\nNội dung chi tiết hoặc link: https://..."
   ```

2. **Gửi file tài liệu (.html, .pdf, .zip, .py, .pptx, .srt, ...)**:
   ```bash
   python3 /Users/vietmac/Documents/CODE/Quản\ gia/telegram_notify.py --file "/đường/dẫn/tới/file" --caption "Mô tả ngắn gọn về file"
   ```

3. **Gửi hình ảnh (.png, .jpg, .webp, screenshot)**:
   ```bash
   python3 /Users/vietmac/Documents/CODE/Quản\ gia/telegram_notify.py --photo "/đường/dẫn/tới/anh.png" --caption "Mô tả hình ảnh"
   ```

## 3. NGUYÊN TẮC PHÂN PHỐI KÉP (DUAL-CHANNEL DELIVERY)

* **Không bao giờ chỉ in trên một kênh**: Vừa hiển thị phản hồi chỉn chu trên khung Chat IDE Antigravity, vừa chủ động chạy script bắn thông báo sang Telegram.
* **Định dạng tối ưu cho màn hình điện thoại**: Tin nhắn Telegram phải ngắn gọn, ngắt dòng thoáng đãng, dùng emoji điều hướng mắt (📍, 👉, 🔗, ✅, 🚀), tiêu đề in đậm `<b>...</b>`.
* **Trường hợp ngoại lệ (`analyze-video`)**: Theo quy tắc chung, tác vụ phân tích video chỉ gửi tin nhắn kèm link Drive/PDF online, không đính kèm file dung lượng lớn.
