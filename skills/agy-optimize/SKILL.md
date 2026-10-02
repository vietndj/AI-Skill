---
name: agy-optimize
description: Quét, chẩn đoán và tối ưu hệ thống Hệ Thống AI. Giảm lag, tiết kiệm token, dọn rác context.
---

# 🚀 KỸ NĂNG: TỐI ƯU HỆ THỐNG HỆ THỐNG AI (AGY-OPTIMIZE)

**Mantra Triggers:** `OPTIMIZE`, `TỐI ƯU`, `DỌN RÁC AGY`

Kỹ năng này giúp Agent tự động quét, phân tích và đề xuất các hành động tối ưu hóa để dọn dẹp hệ thống Hệ Thống AI của User, giảm thiểu tình trạng phình to context (context bloat), tiết kiệm token và giảm lag.

## 📋 HƯỚNG DẪN THỰC THI CHO AGENT
Khi kích hoạt kỹ năng này, bạn **PHẢI** thực hiện theo đúng thứ tự 5 Phase sau đây. Tuân thủ nghiêm ngặt các mốc giới hạn (threshold).

---

### PHASE 1: AUDIT (TỰ ĐỘNG - KHÔNG HỎI USER)
Kiểm tra xem có file `context_audit.py` trong `~/.gemini/config/skills/agy-optimize/scripts/` không.
- Nếu **CÓ** → chạy `python3 ~/.gemini/config/skills/agy-optimize/scripts/context_audit.py --json` để lấy report tự động.
- Nếu **KHÔNG** → báo lỗi hoặc quét thủ công bằng các lệnh shell.

Quét thủ công hoặc sử dụng công cụ `run_command` để thu thập các thông tin sau:
1. **Quét Workspace Rules:** Kiểm tra dung lượng và nội dung các file `AGENTS.md`, `GEMINI.md` trong thư mục gốc của workspace.
2. **Quét Skills (`skills/`):** Dùng `ls -la` và `du -sh` để liệt kê tất cả các kỹ năng đã cài đặt và dung lượng của từng cái (thường ở `~/.gemini/config/skills/`).
3. **Quét Rules (`rules/`):** Liệt kê tất cả rule, kiểm tra dung lượng từng rule và tính TỔNG dung lượng thư mục `rules/`.
4. **Quét MCP và Hooks:** Đọc file `mcp_config.json` (liệt kê danh sách server/tool) và `hooks.json` (nếu có).
5. **Kiểm tra trạng thái tạm dừng:** Tìm kiếm các thư mục `skills-paused/`, `rules-paused/` hoặc các thư mục lưu trữ (archive).
6. **Đánh giá Context Footprint:** Tính tổng số bytes của tất cả file `SKILL.md` đang bật + toàn bộ dung lượng `rules/` + workspace rules.
7. **Kiểm tra Threshold:** Ghi nhận xem tổng dung lượng các rule có vượt qua mức cảnh báo không.

---

### PHASE 2: DIAGNOSE (TỰ ĐỘNG PHÂN TÍCH)
Tiến hành phân tích sâu các dữ liệu từ Phase 1:

- **Đánh giá Health Score cho từng Skill:**
  - *Dung lượng:* Cảnh báo BÉO PHÌ (Bloated) nếu 1 skill > 20KB.
  - *Trùng lặp:* Kiểm tra nhanh nội dung xem có 2 skill nào tương tự chức năng không.
  - *Tính chất công cụ:* Kỹ năng nào chỉ là script/công cụ đơn giản có thể được gợi ý chuyển thành MCP Tool.
- **Đánh giá Rule (Workspace & Global):**
  - **Pattern phát hiện 'Rules nhồi Workflows':** Rule file mà có:
    - Heading `##` với > 3 sub-heading `###`
    - Code blocks hướng dẫn chi tiết
    - Numbered lists > 5 items
    - Dung lượng > 4KB
    → **Đó là WORKFLOW BỊ NHỒI SAI CHỖ, cần tách ra thành Skill.**
  - **Pattern phát hiện 'Workspace Rules béo phì':** File `GEMINI.md` hoặc `AGENTS.md` > 5KB → Cảnh báo nghiêm trọng.
  - Xem có rule nào trùng lặp với nội dung đã có trong skill không.
  - Tổng rule hệ thống có vượt quá **12KB** không.

**Tạo Báo Cáo:** Sử dụng file artifact (định dạng HTML - INKDOC theo thiết kế Dark Glassmorphic Obsidian điểm nhấn Emerald) hoặc Markdown để hiển thị chi tiết chẩn đoán này, kèm theo **Health Score 0-100**.

---

### PHASE 3: RECOMMEND (TƯƠNG TÁC VỚI USER)
Trình bày kết quả phân tích cho User dưới dạng một Bảng Markdown gồm các nhóm hành động:

| Trạng thái | Thể loại | Mô tả & Đề xuất |
|---|---|---|
| 🔴 **CRITICAL** | Context bloat nghiêm trọng | - Cảnh báo workspace rules (`GEMINI.md`, `AGENTS.md`) quá lớn.<br>- Yêu cầu dọn dẹp hoặc tách thành skill. |
| 🟢 **AUTO-FIX** | Tự động xử lý ngay | - Chuyển rule trùng lặp/dư thừa thành rule định tuyến 1 dòng.<br>- Xóa các thư mục skill trống/lỗi. |
| 🟡 **RECOMMEND MERGE/SPLIT** | Đề xuất gộp/tách | - Liệt kê skill trùng lắp cần gộp.<br>- Đề xuất tách các rule chứa workflow sang skill riêng.<br>- *Ước tính token tiết kiệm: `saved_bytes * 0.35`*. |
| 🔴 **USER DECISION** | Chờ quyết định | - Danh sách skill ít dùng nên chuyển sang `skills-paused/`.<br>- Các rule có thể tạm tắt. |
| 🔵 **MCP PACKAGING** | Đóng gói thành MCP | - Danh sách skill nên chuyển sang dạng MCP để gọi On-demand. |

*Lúc này, hãy DỪNG LẠI và hỏi User xem họ muốn áp dụng những đề xuất nào (nhóm 🟢 sẽ tự chạy nếu user đồng ý "Tiến hành sửa").*

---

### PHASE 4: EXECUTE (CHỜ USER XÁC NHẬN)
Sau khi có lệnh duyệt từ User:
1. **Backup:** 
   - Backup skills: `cp -r ~/.gemini/config/skills/ ~/.gemini/config/skills-backup-$(date +%Y%m%d)/`
   - Backup workspace rules: `cp GEMINI.md GEMINI.md.bak-$(date +%Y%m%d)` (và tương tự với `AGENTS.md` nếu có).
2. **Thực thi:** Lần lượt thực hiện các hành động đã được duyệt (gộp, di chuyển vào paused, xóa, sửa nội dung).
3. **Tách workflow ra skill:** Nếu được yêu cầu, tạo skill mới trong `~/.gemini/config/skills/`, ghi file `SKILL.md` với frontmatter chuẩn YAML ở đầu.
4. **Xác minh:** Kiểm tra lại file sau mỗi bước.

---

### PHASE 5: REPORT & MAINTENANCE (BÁO CÁO & BẢO TRÌ)
Kết thúc phiên, hãy thực hiện báo cáo:
- **Tạo Artifact:** Tạo một artifact (HTML hoặc Markdown) trình bày bảng **Before/After** so sánh dung lượng trước và sau tối ưu.
- **Health Score:** Hiển thị điểm số sức khỏe mới (0-100) của hệ thống.
- **Lịch trình bảo trì:**
  - 📅 **Hàng Tuần:** Kiểm tra tổng dung lượng context (đặc biệt thư mục Rules).
  - 🧩 **Khi thêm Skill mới:** Chạy lại `OPTIMIZE` để kiểm tra độ tương thích.
  - 🐌 **Khi hệ thống giật, lag hoặc quên context:** Hô Mantra `DỌN RÁC AGY`.
  - 📆 **Hàng Tháng:** Audit toàn diện.
