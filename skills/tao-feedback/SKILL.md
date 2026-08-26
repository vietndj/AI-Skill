---
name: tao-feedback
description: >-
  Kích hoạt khi người dùng nhắc đến "TẠO FEEDBACK", "TAO FEEDBACK", "tạo feedback",
  "TẠO FORM FEEDBACK", "TRÀ ĐÁ FEEDBACK", "tạo khảo sát", "tạo form khảo sát",
  "form phản hồi", "feedback học viên", "khảo sát học viên".
  Tự động hóa 100% trong 1 câu lệnh duy nhất (1-Shot): Tự tạo Google Sheet (Service Account),
  tự tạo GitHub Repo, tự deploy Vercel + gắn subdomain fedu.vn, tự chạy Health Check,
  bắn kết quả qua Telegram.
---

# KỸ NĂNG: TẠO FEEDBACK (CỖ MÁY TẠO FORM KHẢO SÁT HỌC VIÊN 1-SHOT)

> **QUY TẮC BẤT DI BẤT DỊCH**:
> 1. **TUYỆT ĐỐI KHÔNG HỎI LẠI / KHÔNG DỪNG CHỜ CHỌN A/B/C**.
> 2. Người dùng chỉ cần gửi **1 CÂU LỆNH DUY NHẤT** (VD: `TẠO FEEDBACK: Khóa Offline K13 HN`).
> 3. AI **TỰ ĐỘNG LÀM HẾT TỪ A-Z** trong 1 lượt chạy và trả về link web live + Google Sheet + Health Check.

## THẦN CHÚ KÍCH HOẠT CHUẨN (CỰC KỲ DỄ NHỚ)
* `TẠO FEEDBACK: [Tên khóa học]`
* `TAO FEEDBACK: [Tên khóa học]`
* `TẠO FORM FEEDBACK: [Tên khóa học]`
* `TRÀ ĐÁ FEEDBACK: [Tên khóa học]`

## CẤU HÌNH MẶC ĐỊNH CỦA ANH VIỆT

### Google Service Account (KHÔNG CẦN APPS SCRIPT!)
- **SA JSON File**: `/Users/vietmac/Documents/CODE/vietndj-git-cms-7cd725b38083.json`
- **SA Email**: `form-feedback-offline@vietndj-git-cms.iam.gserviceaccount.com`
- **Project**: `vietndj-git-cms`
- **API đã bật**: Google Sheets API ✅, Google Drive API ✅

### Telegram Bot NOVA-CORE
- **Token**: `8964853536:AAHuRNm_hY-YQtveBD1HlmthN4I5xpVzM8U`
- **Chat ID**: `2050406425`

### Cloudflare R2 CDN (Ảnh)
- **Account ID**: `2dae0527b790faa880c1cfb57247640a`
- **Access Key**: `ef3e4fbcd874fb204ed9c291608f9d75`
- **Secret Key**: `2426f986845501c6d30416a312a69e4be6cc478dc6a861c3aa7dad5dce9a436a`
- **Bucket**: `vietndjmedia`
- **Public Base**: `https://pub-447bd44dfdac4938912655c855b8631c.r2.dev`

### Vercel
- **Scope**: `viet-s-projects1`
- **Domain pattern**: `[slug].fedu.vn`

### Người bán / Chủ form
- **Email**: `vietndj@gmail.com`
- **SĐT**: `0934688632`

## QUY TRÌNH THỰC THI TỰ ĐỘNG 1-SHOT (7 BƯỚC KHÔNG DỪNG)

### BƯỚC 1: BÓC TÁCH THÔNG TIN TỪ LỆNH
1. **Tên khóa học**: Trích xuất từ lệnh (VD: "Khóa Offline K13 HN")
2. **Slug**: Tự tạo slug không dấu (VD: `tra-da-k13-hn`)
3. **Subdomain**: `[slug].fedu.vn`

### BƯỚC 2: NHÂN BẢN TEMPLATE
1. Copy thư mục nguồn:
   ```bash
   cp -R "/Users/vietmac/Documents/CODE/tra-da-khao-sat-hoc-vien" "/Users/vietmac/Documents/CODE/[slug]"
   cd "/Users/vietmac/Documents/CODE/[slug]"
   rm -rf .git .vercel
   ```
2. Cập nhật tên khóa học trong `index.html` nếu cần.

### BƯỚC 3: TẠO GOOGLE SHEET TỰ ĐỘNG (SERVICE ACCOUNT)
Dùng Python script để:
1. Dùng OAuth token từ rclone (`~/.config/rclone/rclone.conf` → `gdrive` section) refresh token rồi share Sheet cho SA.
2. Hoặc: Dùng Sheet có sẵn `1J9ZrjLxTba9R-wuet1n_J_hKcL0PVtQDD_ag65Ewx04` và tạo tab mới theo tên khóa.
3. Service Account ghi header 12 cột + format.
4. Test ghi 1 dòng xác nhận.

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_FILE = '/Users/vietmac/Documents/CODE/vietndj-git-cms-7cd725b38083.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)
sheets = build('sheets', 'v4', credentials=creds)
# ... tạo tab, ghi header, test row
```

### BƯỚC 4: TẠO GITHUB REPO + PUSH
```bash
cd "/Users/vietmac/Documents/CODE/[slug]"
git init
git add .
git commit -m "feat: init feedback form [tên khóa]"
gh repo create "[slug]" --public --source=. --remote=origin --push
```

### BƯỚC 5: SET ENV VARS + DEPLOY VERCEL
```bash
cd "/Users/vietmac/Documents/CODE/[slug]"
npx vercel link --yes --scope viet-s-projects1

# Đọc private key từ SA JSON
PRIVATE_KEY=$(python3 -c "import json; print(json.load(open('/Users/vietmac/Documents/CODE/vietndj-git-cms-7cd725b38083.json'))['private_key'])")

for env in production preview development; do
  echo "form-feedback-offline@vietndj-git-cms.iam.gserviceaccount.com" | npx vercel env add GOOGLE_CLIENT_EMAIL $env --scope viet-s-projects1 --yes
  echo "$PRIVATE_KEY" | npx vercel env add GOOGLE_PRIVATE_KEY $env --scope viet-s-projects1 --yes
  echo "[SPREADSHEET_ID]" | npx vercel env add GOOGLE_SPREADSHEET_ID $env --scope viet-s-projects1 --yes
  echo "[SHEET_NAME]" | npx vercel env add GOOGLE_SHEET_NAME $env --scope viet-s-projects1 --yes
done

npx vercel --prod --yes --scope viet-s-projects1
```

### BƯỚC 6: GẮN SUBDOMAIN + HEALTH CHECK
1. Gắn subdomain Cloudflare:
   ```bash
   python3 /Users/vietmac/Documents/CODE/tra-da-khao-sat-hoc-vien/cf_subdomain.py [slug]
   ```
2. Chạy Health Check:
   ```bash
   curl https://[slug].fedu.vn/api/health
   ```
   Xác nhận: `google_sheet: ✅`, `github_db: ✅`, `cloudflare_r2: ✅`, `telegram_bot: ✅`

### BƯỚC 7: BẮN TELEGRAM + TRẢ KẾT QUẢ
1. Gửi Telegram:
   ```bash
   python3 /Users/vietmac/Documents/CODE/Quản\ gia/telegram_notify.py --msg "🎉 FORM FEEDBACK ĐÃ LÊN SÀN!\n📋 Khóa: [Tên khóa]\n🔗 Form: https://[slug].fedu.vn\n📊 Sheet: https://docs.google.com/spreadsheets/d/[ID]/edit\n🏥 Health: https://[slug].fedu.vn/api/health\n🐙 GitHub: https://github.com/vietndj/[slug]"
   ```
2. Trả kết quả trực tiếp trên chat.

## KIẾN TRÚC HỆ THỐNG (KHÔNG CẦN APPS SCRIPT!)

```
Học viên bấm Gửi
    │
    ▼
POST /api/submit (Vercel Serverless + googleapis SDK)
    │
    ├─► Google Sheets API (Service Account) → Ghi dòng mới
    ├─► Cloudflare R2 CDN → Upload ảnh HD
    ├─► GitHub API → Lưu JSON vĩnh cửu
    └─► Telegram NOVA → Bắn tin (CHỈ 1 LẦN từ server)
```

## ĐIỂM KHÁC BIỆT SO VỚI PHIÊN BẢN CŨ
| Cũ (Apps Script) | Mới (Service Account) |
|:--|:--|
| Anh phải dán code + deploy thủ công | Tự động 100% |
| Webhook chết không ai biết | Health Check `/api/health` |
| Telegram bắn trùng 2 lần | Chỉ 1 lần từ server |
| Token lộ trên frontend F12 | Token chỉ ở server |
| Race condition mất dữ liệu | Google Sheets append an toàn |
