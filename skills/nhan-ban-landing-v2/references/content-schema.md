## Bổ sung các trường mới (từ template ci.fedu.vn)

Các trường sau được bổ sung hoặc mở rộng so với schema cũ. Hầu hết là không bắt buộc (OPTIONAL) trừ khi được ghi rõ.
- **bridgeHeading, bridgeLabel**: Heading và nhãn cho phần bridge.
- **bridgeSteps**: Mảng các bước (array of `{n, title, lead, items}`).
- **bridgeCompareHeading, bridgeCompareSubtitle, bridgeCompareOldTitle, bridgeCompareOldItems, bridgeCompareNewTitle, bridgeCompareNewItems**: Các trường dùng cho phần so sánh cách cũ/cách mới.
- **showcaseLabel, showcaseHeading, showcaseSub**: Các thông tin cho phần showcase.
- **showcaseVideos**: Danh sách video showcase.
- **philosophyAssets**: Mảng các triết lý/phương pháp, gồm `{icon, tag, desc, n, title, input, output, kpi}`.
- **quoteText, quoteAuthor, quoteRole**: Thông tin trích dẫn chứng thực.
- **instructorHighlights, instructorInsight**: Bổ sung thông tin cho người hướng dẫn/tác giả.
- **bonusItems (mở rộng)**: Thêm các trường `tag, speedBadge, summary, highlights, mockupType, audioDemo, youtubeDemo, gifDemo`.
- **LANTAN_FAQS**: Dữ liệu FAQ hardcode trong Checkout.tsx giờ phải được thêm vào `content.ts`.

*Lưu ý:* Mảng `blocksMeta.hidden` dùng để ẩn các section. Trong ci.fedu.vn, nhiều section bị ẩn `["rule", "cycle", "discovery", "solution", "skills", "midCta", "before-after"]`. Đối với một sản phẩm chung chung, TẤT CẢ các section nên được hiển thị (`hidden=[]`).

---

# Content Schema — Danh Sách Mọi Trường Cần Viết Trong `content.ts`

Khi viết lại `DEFAULT_CONTENT` trong `src/content.ts`, AI **BẮT BUỘC** phải viết lại **TẤT CẢ** các trường bên dưới cho phù hợp với sản phẩm/dịch vụ mà người dùng yêu cầu.

> **NGUYÊN TẮC**: Mọi nội dung phải viết bằng tiếng Việt, giọng bán hàng chuyên nghiệp, tạo cảm giác cấp bách và tin cậy. Không để lại BẤT KỲ nội dung mẫu cũ nào.

---

## 1. HERO SECTION (Phần đầu trang — gây ấn tượng mạnh)

| Trường | Kiểu | Mô tả | Ví dụ (ngành xăm) |
|---|---|---|---|
| `heroBadge` | string | Badge nhỏ phía trên headline, IN HOA | `"DỊCH VỤ XĂM THẨM MỸ CAO CẤP 2026"` |
| `heroHeadline1` | string | Headline chính, IN HOA, gây chú ý mạnh | `"NGHỆ THUẬT XĂM THẨM MỸ — PHONG CÁCH RIÊNG TRÊN TỪNG ĐƯỜNG NÉT"` |
| `heroHeadline2` | string | Subheadline, bổ trợ headline 1 | `"Dịch vụ xăm trọn gói từ tư vấn đến chăm sóc sau xăm"` |
| `heroPoem` | string[] | 3 dòng bullet point USP nổi bật, mỗi dòng bắt đầu bằng emoji | `["🎨 Thiết Kế Bản Phác Thảo Cá Nhân Hóa 100%", "🛡️ Mực Organic Chuẩn FDA — An Toàn Tuyệt Đối", "⚡ Kỹ Thuật Fine Line & Watercolor Đỉnh Cao"]` |
| `heroAccentLine` | string | Câu nhấn mạnh cảm xúc, italic | `"Mỗi hình xăm là một câu chuyện — hãy để chúng tôi kể câu chuyện của bạn!"` |
| `heroSub` | string | Đoạn mô tả 2-3 câu về sản phẩm/dịch vụ | `"Không cần lo lắng về đau hay nhiễm trùng..."` |
| `heroCta` | string | Text nút CTA chính, IN HOA, chứa giá | `"ĐẶT LỊCH XĂM NGAY (2.000.000đ)"` |
| `heroVideoYoutubeId` | string | ID video YouTube (để trống nếu không có) | `""` |
| `heroSubPrice` | string | Dòng giá gốc so sánh | `"Giá niêm yết: 5.000.000 VNĐ — Tiết kiệm 60% chỉ hôm nay"` |
| `products` | array | 2 sản phẩm/gói dịch vụ chính | `[{name: "Xăm Fine Line Art", desc: "Nét mảnh tinh tế..."}, ...]` |

---

## 2. PAIN SECTION (Nỗi đau khách hàng)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `painLabel` | string | Label section, IN HOA |
| `painHeading` | string | Câu hỏi đánh vào nỗi đau |
| `painQuote` | string | Trích dẫn/phát biểu gây đồng cảm |
| `painSub` | string | Đoạn giải thích nỗi đau sâu hơn |
| `pains` | string[] | 4 bullet nỗi đau, mỗi item bắt đầu bằng `❌` |

---

## 3. ATTENTION SECTION (3 yếu tố thu hút)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `attentionLabel` | string | Label IN HOA |
| `attentionHeading` | string | Tiêu đề section |
| `attentionPara` | string | Đoạn dẫn nhập |
| `attentionItems` | array[3] | Mỗi item: `{icon: "emoji", title: string, desc: string}` |

---

## 4. RULE SECTION (Quy tắc/Nguyên lý)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `ruleLabel` | string | Label IN HOA |
| `ruleHeading` | string | Tên quy tắc |
| `rulePara` | string | Giải thích quy tắc |
| `ruleItems` | array[3] | Mỗi item: `{fail: string, why: string}` — sai lầm & hậu quả |
| `ruleConclusion` | string | Kết luận, nhắc tên sản phẩm là giải pháp |

---

## 5. CYCLE SECTION (Giải pháp toàn diện)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `cycleLabel` | string | Label IN HOA |
| `cycleHeading` | string | Tiêu đề, chứa giá |
| `cyclePara` | string | Mô tả ngắn |
| `cycleItems` | array[4] | Mỗi item: `{fail: string, why: string}` — tên gói & mô tả |

---

## 6. DISCOVERY SECTION (Chi tiết tính năng)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `discoveryLabel` | string | Label IN HOA |
| `discoveryHeading` | string | Tiêu đề |
| `discoverySub` | string | Mô tả phụ |
| `discoveryItems` | array[4] | Mỗi item: `{title: string, desc: string}` — đánh số 1,2,3,4 |

---

## 7. SOLUTION SECTION (Lợi ích)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `solutionLabel` | string | Label IN HOA |
| `solutionHeading` | string | "Bạn sẽ nhận được gì..." |
| `solutionSub` | string | Tóm tắt lợi ích chính |
| `solutionItems` | string[5] | 5 bullet lợi ích, mỗi item bắt đầu bằng `✅` |

---

## 8. SKILLS SECTION (Danh mục sản phẩm/kỹ năng)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `skillsLabel` | string | Label IN HOA |
| `skillsHeading` | string | Tiêu đề |
| `skillCards` | array[4] | `{n: "01", title: string, desc: string}` |

---

## 9. MID CTA (Nút kêu gọi hành động giữa trang)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `midCtaHeading` | string | Tiêu đề IN HOA |
| `midCtaSub` | string | Mô tả kèm giá |
| `midCtaBtn` | string | Text nút, chứa giá |

---

## 10. BEFORE/AFTER SECTION (So sánh trước/sau)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `baLabel` | string | Label IN HOA |
| `baHeading` | string | Tiêu đề so sánh |
| `baSub` | string | Mô tả |
| `beforeLabel` | string | Label cột "trước", IN HOA |
| `afterLabel` | string | Label cột "sau", IN HOA |
| `beforeItems` | string[4] | 4 bullet bắt đầu bằng `❌` |
| `afterItems` | string[4] | 4 bullet bắt đầu bằng `✅` |

---

## 11. ROADMAP SECTION (Quy trình nhận sản phẩm)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `roadmapLabel` | string | Label IN HOA |
| `roadmapHeading` | string | "3 Bước đơn giản..." |
| `stages` | array[3] | `{n: "01", title: string, sub: string}` |

---

## 12. INSTRUCTOR SECTION (Tác giả/Đội ngũ)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `instructorLabel` | string | Label IN HOA |
| `instructorHeading` | string | Tiêu đề giới thiệu |
| `instructorInitials` | string | 2-3 chữ viết tắt (avatar) |
| `instructorName` | string | Tên đầy đủ |
| `instructorTitle` | string | Chức danh |
| `instructorBio` | string[2] | 2 đoạn tiểu sử |
| `instructorPhoto` | string | URL ảnh (Unsplash hoặc để trống) |
| `instructorBadge1` | string | Badge 1 (kinh nghiệm) |
| `instructorBadge2` | string | Badge 2 (cam kết) |
| `instructorSubtitle` | string | Dòng IN HOA bên dưới tên |

---

## 13. BONUS SECTION (Quà tặng kèm)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `bonusLabel` | string | Label IN HOA |
| `bonusHeading` | string | Tiêu đề |
| `bonusSub` | string | Mô tả tổng giá trị quà |
| `bonusItems` | array[3] | `{id: "b1", title: string, desc: string}` — bắt đầu bằng 🎁 |

---

## 14. CTA SECTION (Kêu gọi hành động cuối trang)

| Trường | Kiểu | Mô tả |
|---|---|---|
| `urgencyBar` | string | Dòng FOMO, bắt đầu bằng ⚡ |
| `ctaLabel` | string | Label IN HOA |
| `ctaHeading` | string | Tiêu đề CTA |
| `ctaSub` | string | Mô tả kèm giá & lợi ích |
| `countdownLabel` | string | Label đồng hồ đếm ngược |
| `valueStackTitle` | string | Tiêu đề bảng giá trị, IN HOA |
| `valueStack` | array[5] | `{label: string, price: string}` — liệt kê giá trị từng phần |
| `guarantee` | string | Cam kết bảo hành, bắt đầu bằng 🛡️ |

---

## 15. FOOTER

| Trường | Kiểu | Mô tả |
|---|---|---|
| `footerBrand` | string | Tên thương hiệu IN HOA (lấy từ siteConfig) |
| `footerDot` | string | Luôn là `"."` |
| `footerTagline` | string | Slogan ngắn |
| `footerLinks` | string[4] | 4 label menu |
| `footerCopyright` | string | Dòng copyright (lấy từ siteConfig) |

---

## 16. META

| Trường | Kiểu | Mô tả |
|---|---|---|
| `price` | string | Lấy từ `siteConfig.product.price` |
| `value` | string | Lấy từ `siteConfig.product.originalPrice` |
| `blocksMeta.order` | string[] | Giữ nguyên: `["hero","pain","attention","rule","cycle","discovery","solution","skills","midCta","before-after","roadmap","instructor","bonus","cta","footer"]` |
| `blocksMeta.hidden` | string[] | `[]` |
| `blocksMeta.media` | object | `{}` |
| `blocksMeta.custom` | object | `{}` |

---

## BONUS: LiveSocialProof.tsx

Ngoài `content.ts`, AI cũng phải viết lại array popup thông báo trong `LiveSocialProof.tsx`:
- 15 dòng thông báo giả lập, phù hợp sản phẩm
- Format: `"Anh/Chị [Tên] vừa [hành động] [sản phẩm]"`
- Ví dụ xăm: `"Chị Minh Anh vừa đặt lịch xăm Fine Line thành công"`
