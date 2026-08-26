---
name: miss-sale-page
description: >
  Được kích hoạt khi người dùng muốn tạo landing page bán hàng hoặc setup trang bán hàng tự động trong 1 lệnh (1-Shot).
---

# Hướng dẫn chi tiết tạo Landing Page Tự Động (1-Shot Autonomous)

Khi skill này được kích hoạt, AI **TUYỆT ĐỐI KHÔNG HỎI LẠI** mà thực hiện tự động toàn bộ pipeline:
1. **Tự suy luận thông tin**: Tên sản phẩm, giá bán, anchor price, mã chuyển khoản, ngân hàng mặc định của anh Việt (TPBank / MBBank - `NGUYEN DUC VIET` - `88804101986`).
2. **Tự sinh 100% nội dung marketing**: Viết theo chuẩn AIDA/PAS của `ci.fedu.vn`.
3. **Nhân bản từ template**: `/Users/vietmac/Documents/CODE/mau-ban-hang-v2` sang `/Users/vietmac/Documents/CODE/[slug]`.
4. **Tạo GitHub Repo**: `git init && git add . && git commit -m "feat: init" && gh repo create [slug] --public --source=. --remote=origin --push`.
5. **Deploy Vercel**: `npm run build && npx vercel --prod --yes`.
6. **Bắn Telegram & Bàn giao**: Gửi link live qua Telegram bot NOVA-CORE và trả link Vercel + VietQR ngay trên chat.

