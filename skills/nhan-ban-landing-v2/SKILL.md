---
name: nhan-ban-landing-v2
description: >-
  Kích hoạt khi người dùng nhắc đến "MISS BÁN HÀNG", "MISSBANHANG", "CỖ MÁY BÁN HÀNG",
  "tạo web bán hàng", "landing page bán hàng", "trang bán sản phẩm", "nhân bản landing",
  "tạo trang bán", "bán hàng online", "web thanh toán tự động", "lên web bán hàng".
  Tự động hóa 100% trong 1 câu lệnh duy nhất (1-Shot): Tự viết nội dung marketing chuẩn ci.fedu.vn,
  tự tạo GitHub Repo, tự cấu hình VietQR tài khoản anh Việt, tự deploy Vercel và bắn link qua Telegram.
---

# KỸ NĂNG: MISS BÁN HÀNG (CỖ MÁY TẠO LANDING PAGE TỰ ĐỘNG 1-SHOT)

> **QUY TẮC BẤT DI BẤT DỊCH CHO DEMO TRÊN LỚP**:
> 1. **TUYỆT ĐỐI KHÔNG HỎI LẠI / KHÔNG PHỎNG VẤN 4 BƯỚC / KHÔNG DỪNG CHỜ CHỌN A/B/C**.
> 2. Người dùng chỉ cần gửi **1 CÂU LỆNH DUY NHẤT** (VD: `MISS BÁN HÀNG: Gói Chăm sóc da Y Khoa giá 600k`).
> 3. AI **TỰ ĐỘNG LÀM HẾT TỪ A-Z** trong 1 lượt chạy và trả về link web Vercel live + repo GitHub + QR thanh toán nhận tiền thật!

---

## THẦN CHÚ KÍCH HOẠT CHUẨN
* `MISS BÁN HÀNG: [Tên sản phẩm/dịch vụ], giá [giá bán], nhận qua [ngân hàng nếu có]`
* `CỖ MÁY BÁN HÀNG: [Tên sản phẩm/dịch vụ], giá [giá bán]`
* `LÊN WEB BÁN HÀNG: [Tên sản phẩm/dịch vụ], giá [giá bán]`

---

## QUY TRÌNH THỰC THI TỰ ĐỘNG 1-SHOT (AUTOMATED PIPELINE)

Ngay khi nhận lệnh, AI thực hiện liên tục không dừng các bước sau:

### BƯỚC 1: BÓC TÁCH & TỰ SUY LUẬN TOÀN BỘ DỮ LIỆU
1. **Thông tin cơ bản**:
   - **Tên sản phẩm**: Trích xuất từ lệnh (VD: "Gói Chăm Sóc & Phục Hồi Da Chuẩn Y Khoa").
   - **Giá bán**: Trích xuất số tiền (VD: `600000`, format: `600.000`).
   - **Giá gốc (Anchor Price)**: Tự tính = Giá bán x 2.5 đến 3 (VD: `1.500.000`).
   - **Mã chuyển khoản (Transfer Prefix)**: Tự tạo mã viết tắt IN HOA không dấu 4-8 ký tự (VD: `DALIEUYKHOA`, `EBOOKPROMPT`).
   - **Slug / Tên thư mục**: Tự tạo slug tiếng Việt không dấu (VD: `cham-soc-da-y-khoa-600k`).
2. **Cấu hình thanh toán mặc định của anh Việt**:
   - Chủ tài khoản: `NGUYEN DUC VIET`
   - Ngân hàng: `TPBank` (Mã `TPB`, STK `88804101986`) — Nếu người dùng nói MBBank thì dùng `MBBank` (Mã `MB`, STK `88804101986`).
   - Người bán: `Nguyễn Đức Việt`, SĐT: `0934688632`, Email: `vietndj@gmail.com`, Zalo: `0934688632`.
   - Telegram Bot: `NOVA-CORE` (`Token: 8964853536:AAHuRNm_hY-YQtveBD1HlmthN4I5xpVzM8U`, `Chat ID: 2050406425`).

---

### BƯỚC 2: AI TỰ SINH 100% NỘI DUNG MARKETING THỰC CHIẾN (COPYWRITING)
Dựa vào sản phẩm và giá, AI tự đóng vai chuyên gia marketing viết toàn bộ 70+ trường cho `src/content.ts` theo cấu trúc của `ci.fedu.vn`:
- **Hero**: Headline bùng nổ, 3 gạch đầu dòng USP, câu nhấn mạnh cảm xúc, CTA giá.
- **Pain Points**: 4 nỗi đau nhức nhối thực tế của khách hàng trong ngành (dấu `❌`).
- **Attention & Solutions**: 3 trụ cột giải pháp đối chiếu "Cách cũ thủ công/sai lầm" vs "Cách mới chuẩn chỉnh".
- **Skills/Modules/Roadmap**: Lộ trình 4 giai đoạn rõ ràng.
- **Instructor**: Profile chuyên gia uy tín.
- **Bonus Value Stack**: 3-5 quà tặng đắt giá nâng tổng giá trị lên gấp 5-10 lần giá bán.
- **FAQ**: 5 câu hỏi giải tỏa do dự thực chiến.
- **Live Social Proof**: 15 dòng popup mua hàng nhảy thời gian thực trong `src/LiveSocialProof.tsx`.

---

### BƯỚC 3: NHÂN BẢN TEMPLATE & GHI CẤU HÌNH
1. Thư mục nguồn template: `/Users/vietmac/Documents/CODE/mau-ban-hang-v2`
2. Thư mục đích: `/Users/vietmac/Documents/CODE/[slug]`
3. Thực hiện lệnh:
   ```bash
   cp -R "/Users/vietmac/Documents/CODE/mau-ban-hang-v2" "/Users/vietmac/Documents/CODE/[slug]"
   cd "/Users/vietmac/Documents/CODE/[slug]"
   rm -rf .git .vercel dist
   ```
4. Ghi file `src/site.config.ts` với thông tin sản phẩm và ngân hàng `NGUYEN DUC VIET`.
5. Ghi file `src/content.ts` với toàn bộ nội dung marketing vừa sinh.
6. Ghi file `.env` với `COURSE_AMOUNT=[giá số]` và các biến bot Telegram NOVA-CORE.

---

### BƯỚC 4: TỰ ĐỘNG TẠO GITHUB REPOSITORY
Khởi tạo git và tạo repo GitHub qua GitHub CLI `gh`:
```bash
cd "/Users/vietmac/Documents/CODE/[slug]"
git init
git add .
git commit -m "feat: init sales landing page for [slug]"
gh repo create "[slug]" --public --source=. --remote=origin --push
```

---

### BƯỚC 5: TỰ ĐỘNG CẤU HÌNH BIẾN MÔI TRƯỜNG & DEPLOY LÊN VERCEL
1. **Tự động set toàn bộ biến môi trường lên Vercel** (Đảm bảo thanh toán tự động, SePay, Make webhook gửi mail, Telegram chạy 100%):
```bash
cd "/Users/vietmac/Documents/CODE/[slug]"
# Link project trước
npx vercel link --yes --scope viet-s-projects1

# Set đủ các biến môi trường cho cả 3 môi trường (production, preview, development)
for env in production preview development; do
  echo "[giá số]" | npx vercel env add COURSE_AMOUNT $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "[TÊN SP]" | npx vercel env add PRODUCT_NAME $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "ZXDNXUIW6N2IQROARNGKEZTI0YFCV2JSBU41RTMEPA1QIMJYKG9PHG35WD5O90QY" | npx vercel env add SEPAY_API_KEY $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "https://script.google.com/macros/s/AKfycbz3s4V-cItvUcM3g-oZy0mAWsxGXr9UhLhz_qPgXWZgFNTT9KgKZxu391m-aRv8rz8U/exec" | npx vercel env add GOOGLE_SCRIPT_URL $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "re_YOUR_RESEND_API_KEY_HERE" | npx vercel env add RESEND_API_KEY $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "[TÊN SP] · Việt <viet@fedu.vn>" | npx vercel env add RESEND_FROM_EMAIL $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "8964853536:AAHuRNm_hY-YQtveBD1HlmthN4I5xpVzM8U" | npx vercel env add TELEGRAM_BOT_TOKEN $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "2050406425" | npx vercel env add TELEGRAM_CHAT_ID $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "Nguyễn Đức Việt" | npx vercel env add SELLER_NAME $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "0934688632" | npx vercel env add SELLER_PHONE $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "0934688632" | npx vercel env add SELLER_ZALO $env --scope viet-s-projects1 --yes 2>/dev/null
  echo "vietndj@gmail.com" | npx vercel env add SELLER_EMAIL $env --scope viet-s-projects1 --yes 2>/dev/null
done
```

2. **Chạy build và deploy production**:
```bash
npm run build
npx vercel --prod --yes --scope viet-s-projects1
```
*(Lấy URL trả về từ output của lệnh Vercel)*

---

### BƯỚC 6: BẮN THÔNG BÁO TELEGRAM & TRẢ KẾT QUẢ TRỰC DIỆN
1. **Gửi Telegram cho anh Việt**:
   ```bash
   python3 /Users/vietmac/Documents/CODE/Quản\ gia/telegram_notify.py --msg "🎉 CỖ MÁY BÁN HÀNG ĐÃ LÊN SÀN!\n📦 Sản phẩm: [Tên SP]\n💰 Giá: [Giá] VNĐ\n💳 VietQR: TPBank - 88804101986 (NGUYEN DUC VIET)\n🔗 Web Live: [Vercel URL]\n🐙 GitHub: https://github.com/vietndj/[slug]"
   ```
2. **Trả kết quả trực tiếp trên khung chat**:
   - Link Vercel Live (bấm vào xem ngay)
   - Link GitHub Repo
   - Tên sản phẩm, Giá bán, Mã VietQR
   - Xác nhận hệ thống quét QR chuyển khoản thẳng vào tài khoản anh Việt đã sẵn sàng 100%!

