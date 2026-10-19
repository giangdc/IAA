---
id: v2.0/GN/risk_assessment
title: Risk Assessment — Module GN
type: risk_assessment
version: v2.0
module: { code: GN, dir: GN, name: "Gạch nợ hóa đơn" }
counts:                 # 🔑 CANONICAL — CL/RISK của module GN
  cl: 10
  cl_open: 8
  cl_blocking: 0
  risk: 6
  risk_high: 3
status: ANALYZED
updated: 2026-10-19
---

# Risk Assessment — v2.0 · Module GN

> Tạo bởi: analyze-requirements. Đánh giá rủi ro per module + định hướng test focus cho generate-tc/vibe-test.
>
> **Structure-lock:** dùng DUY NHẤT 1 dạng bảng chi tiết hợp nhất bên dưới cho MỌI module (KHÔNG dùng nhiều dạng bảng khác nhau giữa các module). KHÔNG đổi cột. Bảng gồm 9 cột (thêm `Solution` + `Status` để track vòng đời rủi ro).
>
> **Governance (layout v2):** file này là **nguồn PRIMARY duy nhất** cho risk + **Clarification** của module GN. Thiếu tài liệu tích hợp (Kafka Out, API kênh thanh toán / EVC, enum) là risk xuyên suốt — home ở `XHD/risk_assessment.md` RISK-XHD-01 / CL-XHD-29, ở đây chỉ trỏ tới.
> Mã `GAP-NN` trỏ về `01_test-plans/DOC-READINESS-InvoiceIssuance-v2.0.md` / TP §2.4.

## Tổng quan
| Module | Risk Level | Rủi ro chính |
|--------|-----------|--------------|
| GN | High | Ranh giới INVOICE ↔ đội EVC chưa rõ (Paid voucher, thứ tự gạch, nguồn tiền lock) có thể dẫn tới gạch trùng hoặc gạch sai số; phụ thuộc mock API kênh thanh toán / EVC trên STG |

## Chi tiết rủi ro (bảng hợp nhất — 1 dạng cho mọi module)
| Risk ID | Module/Area | Rủi ro | Severity | Why (Source) | Test Focus | Solution | Status | REQ/SC |
|---------|-------------|--------|----------|--------------|------------|---------------------|--------|--------|
| RISK-GN-01 | GN / EVC ↔ Paid voucher | Paid đồng bộ "gồm cả voucher"; INVOICE gạch nợ dùng cả Paid voucher (CL-GN-01 vòng 2) trong khi EVC do đội EVC gạch ⇒ nếu hai bên cùng gạch một khoản thì nợ khách bị trừ 2 lần | High | DOC-v2.0-01 BR-DP-01 (L474) ↔ BR-VC (L545) ↔ BR-GN-01 (L508); TP rủi ro #7 | SC-GN-045, 048 | Gạch nợ EVC / voucher **vẫn test** (QC owner 19/10/2026 — khác TP §2.2 #5); chờ BA liệt kê loại EVC / voucher và bên gạch (CL-GN-01, 08, 10) | Open | SC-GN-045, SC-GN-048 · REQ-GN-012, REQ-GN-019 |
| RISK-GN-02 | GN / EVC lock | Nguồn tổng EVC + tiền lock không nêu ở 2.2, không có hành vi lỗi ⇒ công thức min(nợ − lock, Paid) và kiểm đủ tiền nhánh Cọc không tái hiện được nếu không có mock | High | DOC-v2.0-01 BR-VC (L546), BR-GC-01 (L529); GAP-16 | SC-GN-037, 038, 046, 047 | Dựng mock trả {tổng EVC, lock}. API EVC lỗi / timeout: **không test trên STG** — retry thủ công, lỗi ⇒ log bug (CL-GN-02, SC-GN-049 deprecated 19/10/2026) | Open | SC-GN-037, SC-GN-038, SC-GN-046, SC-GN-047 · REQ-GN-016, REQ-GN-020 |
| RISK-GN-03 | GN / gạch nợ tạm kênh sàn | Gạch tạm → gỡ tạm → gạch thật đổi trạng thái HĐ 2 lần; sai thứ tự (gạch thật trước khi gỡ) ⇒ Σ Payment > tổng HĐ; sàn quyết toán thiếu ⇒ HĐ quay về "còn nợ" | High | DOC-v2.0-01 BR-NT-01..04 (L491-505) | SC-GN-019, 022, 023, 024 | Test đủ chuỗi trạng thái trên Shopee + Tiktok; hỏi CL-GN-06 cho ca thiếu | Open | SC-GN-019, SC-GN-022, SC-GN-023, SC-GN-024 · REQ-GN-009..011 |
| RISK-GN-04 | GN / tích hợp | Cần mock API kênh thanh toán (trường Paid/Cọc), Kafka Out, đội EVC trên STG; payload chưa có | Medium | TP §2.1b #23; CL-XHD-29 | SC-GN-016, 017, 034 | Chuẩn bị mock/stub trước R1 (TP Entry Criteria); lỗi / timeout API ngoài không test trên STG (CL-GN-02) | Open | SC-GN-016, SC-GN-017, SC-GN-034 · REQ-GN-007, REQ-GN-014 |
| RISK-GN-05 | GN / thứ tự bill + gạch từng phần | Đơn 1..n bill; sai thứ tự hoặc sai min() ⇒ gạch sai bill, Paid dư sai | Medium | DOC-v2.0-01 BR-GN-03, BR-GN-04 (L511-521) | SC-GN-028..033 | BVA đủ 3 biên Paid vs nợ; đơn ≥3 bill khác tiền | Resolved | SC-GN-028..033 · REQ-GN-013, REQ-GN-014 |
| RISK-GN-06 | GN / cọc theo loại | Thiếu danh sách loại cọc ↔ dịch vụ ⇒ không dựng được dữ liệu "thiếu 1 loại"; gom Payment sai loại | Medium | DOC-v2.0-01 BR-GC-02, BR-GC-03 (L532-542) | SC-GN-039..043 | Xin danh mục loại cọc (CL-GN-07) | Open | SC-GN-039..043 · REQ-GN-017, REQ-GN-018 |

> Risk ID format: `RISK-<MODULE>-<NN>` (vd `RISK-PV-01`). Severity = High / Medium / Low (có thể Medium-High).
> **Solution:** biện pháp giảm thiểu hoặc hướng xử lý cụ thể (vd "resolve C-XXX trước generate-tc", "thêm negative TC cho MSG", "defer tới khi có env"). Chưa có → `—` (nhưng High/Medium nên có).
> **Status** — trạng thái xử lý rủi ro. Enum THUẦN (không kèm ghi chú trong ô — lý do để ở cột `Solution`):
> - `Open` = chưa xử lý / **đang bị chặn** (env/API/BA/backend chưa sẵn → chưa cover được).
> - `Pending` = **chấp nhận + defer có chủ đích** (không xử ở version này; vd NFR chờ môi trường thật / tải lớn).
> - `Resolved` = **đã xử lý và thêm test case cover** rủi ro (có `Solution` + TC/SC khả thi).
> - `Closed` = **bỏ khỏi scope** (feature loại khỏi version → rủi ro không còn áp dụng).
> KHÔNG để trống. Vòng đời: `Open` → `Resolved` (khi đã cover) · `Open` → `Pending` (defer) · `→ Closed` (bỏ scope).

## Khuyến nghị tổng thể
1. **Resolve blocker clarifications trước generate-tc** các scenario liên quan: CL-GN-01 (⛔ Paid voucher), CL-GN-02, CL-GN-08 (ranh giới EVC), CL-GN-03 (kênh sàn).
2. **Ưu tiên test P1 high-risk:** SC-GN-011..013, 017, 019, 022, 023, 031..034, 040, 046 (+ hồi quy Shopee/Tiktok qua SC-GN-019, 022).
3. **Performance / cần môi trường:** không có NFR; mock API kênh thanh toán + đội EVC + consumer Kafka Out là điều kiện chạy (RISK-GN-04).
4. **ID/text cleanup (non-blocking, cần trước automation):** TC dùng thống nhất thuật ngữ "gỡ gạch nợ tạm" của URD 2.2.

## Clarifications (home CL — layout v2)

> 1 CL = 1 heading `### CL-GN-NN · <câu hỏi ngắn>`. Dòng META mang `Status` (+ `⛔ BLOCKING`) và mã GAP. Khi resolved: **thêm** `✅ RESOLVED <ngày> — <kết luận>`, giữ phần phân tích cũ.

### CL-GN-01 · Paid voucher có bị loại khỏi gạch nợ của INVOICE không?
📍 `DOC-v2.0-01 BR-DP-01 (L474)` ↔ `BR-GN-01 (L508)` ↔ `BR-VC (L545)`  ·  Status: **Open — mở lại 19/10/2026** (nhánh Paid có voucher) · GAP-40 (Critical)

**BR-DP-01 — đồng bộ cả voucher** — `L474`
> Paid đồng bộ 1:1 từ Orderpaid theo OrderCode, gồm cả voucher và tiền khách thanh toán; mỗi Paid gán PaidType theo nguồn tiền.

**BR-GN-01 — không loại PaidType nào** — `L508`
> Chỉ lấy dòng Paid có Amount > 0 và cùng OrderCode với hóa đơn.

**BR-VC — EVC do đội EVC gạch** — `L545`
> Phần gạch nợ bằng EVC do đội EVC thực hiện; ISC tự quyết phương thức quản trị và xử lý voucher.

**Màn hiện hữu — Payment gồm cả voucher** — `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png) bảng "Liệt kê các khoản đã thanh toán"
> 1 | Cuoc K+ | U25SG00002918 | 155,000 | System1 | (17/11/2025)
> 2 | Cuoc K+ | U25SG00002918 | 10,000 | phieumuahang4 | Voucher(17/11/2025)

↳ **Ghi chú:** Đọc đúng chữ thì INVOICE dùng mọi Paid Amount > 0, kể cả voucher ⇒ gạch trùng với đội EVC. Màn hiện hữu (HĐ 2025, trước Phase 2) cho thấy khoản voucher được ghi thành 1 dòng thanh toán riêng trên HĐ — không cho biết bên nào ghi. Cấu hình EVC (PaidType, Owner gạch) 2.2 chuyển D#4 — chưa có đặc tả (CL-GN-10). Mail PM "EVC cần test => theo rule URD" không trả lời điểm này. TP giả định loại Paid voucher (SC-GN-048).

**Câu hỏi cho BA:** Khi gạch nợ nhánh Paid, INVOICE dùng (a) chỉ Paid tiền khách hay (b) cả Paid voucher? Nếu (b): voucher nhóm nào (Payment Hub?) và đội EVC có bỏ qua khoản đó không?

🟡 **Làm rõ một phần 19/10/2026** — Gạch nợ của INVOICE dùng **cả Paid voucher và các loại voucher giảm tiền** (không loại voucher) — bỏ giả định TP; SC-GN-048 đổi Then. Hết BLOCKING. Còn mở: đội EVC có bỏ qua khoản voucher này không (tránh gạch 2 lần). Nguồn: QC trả lời 19/10/2026 vòng 2.

⛔ **OUT-SCOPE 19/10/2026** — TP §2.2 #5 *"Gạch nợ bằng EVC / voucher"* ngoài phạm vi (BR-VC L545 *"Phần gạch nợ bằng EVC do đội EVC thực hiện"*); chỉ giữ phần INVOICE chừa EVC bị lock. QC owner 19/10/2026: phần gạch nợ EVC không test. Gạch nợ bằng Paid voucher thuộc phần này ⇒ SC-GN-048 deprecated, phần còn hỏi (đội EVC có bỏ qua voucher không) không hỏi BA. Đồng bộ Paid gồm dòng voucher (SC-GN-002) vẫn test.

🔄 **MỞ LẠI 19/10/2026** — QC owner: phần **gạch nợ EVC / voucher VẪN TEST**, chờ BA liệt kê các loại EVC / voucher. Ghi nhận ⛔ OUT-SCOPE / thu hẹp phía trên **bị hủy**. ⚠️ Khác TP §2.2 #5 (TP chưa cập nhật — QC owner xử lý TP, analyze không sửa TP). Đã rõ (vòng 2): INVOICE gạch nợ dùng cả Paid voucher và các loại voucher giảm tiền ⇒ SC-GN-048 dùng lại. Còn hỏi: danh sách loại EVC / voucher; với mỗi loại INVOICE gạch hay đội EVC gạch; đội EVC có bỏ qua khoản INVOICE đã gạch không (tránh gạch 2 lần).

---

### CL-GN-02 · Nguồn tổng tiền EVC + tiền lock; API lỗi / timeout xử lý ra sao?
📍 `DOC-v2.0-01 BR-VC (L546)` + `BR-GC-01 (L529)`  ·  Status: **Resolved 19/10/2026** · GAP-16 (Critical)

**URD 2.2** — `L546`
> Với EVC bị lock (khách chưa ký hợp đồng), INVOICE chừa phần lock khi gạch tiền khách: số gạch = nhỏ nhất của (nợ bill trừ tiền lock) và Paid khách thanh toán.

↳ **Ghi chú:** URD 2.2 không nói nguồn và không có hành vi lỗi. TP giả định lỗi xử lý như BR-XL-03 (dừng, không retry) — SC-GN-049.

**Câu hỏi cho BA:** Xác nhận nguồn = API đội EVC (spec?) và hành vi khi API lỗi / timeout.

✅ **RESOLVED 19/10/2026** — Thực tế đội dự án **retry thủ công**; STG **không test** timeout; API EVC lỗi ⇒ log bug. SC-GN-049 deprecated. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-GN-03 · "Kênh sàn" gồm những SaleChannelID nào?
📍 `DOC-v2.0-01 BR-NT-01 (L493)` ↔ `§A.2 (L79-137)`  ·  Status: **Resolved 19/10/2026** · *mới — 16/10/2026*

**URD 2.2** — `L493`
> Chỉ gạch nợ tạm khi Paid ở trạng thái gạch nợ tạm và đơn thuộc kênh bán qua sàn (khách thanh toán với sàn nên tiền chưa chắc về công ty).

↳ **Ghi chú:** §A.2 không có cột đánh dấu kênh sàn. Momo (17), MBBank (12), TGDD (14), API (7) cũng là kênh khách thanh toán qua bên thứ ba — không rõ có tính là sàn. Giả định {20, 21} theo URD 2.2 §A.1 L59 ("kênh TMĐT (Shopee, TikTok Shop)").

**Câu hỏi cho BA:** Kênh sàn (được gạch nợ tạm) = chỉ Shopee (20) + Tiktok (21)? Có kênh nào khác?

✅ **RESOLVED 19/10/2026** — Kênh sàn (được gạch nợ tạm) = **chỉ Shopee (20) và TikTok Shop (21)**. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-GN-04 · Enum `paymentstatus` và mã "phương thức thanh toán đặc biệt"
📍 `DOC-v2.0-01 §A.5 #6 (L300)` + `BR-NT-02 (L498)`  ·  Status: **Open** · thuộc GAP-07 (Critical)

> Trường paymentstatus quyết định gạch nợ tạm hay gạch nợ thật.
> (...)
> Ghi Payment bằng phương thức thanh toán đặc biệt, số tiền bằng toàn bộ nợ còn lại.

↳ **Ghi chú:** Cần giá trị cụ thể để dựng dữ liệu SC-GN-011..013, 019 và phân biệt Payment tạm với Payment thật khi verify gỡ tạm. Có trạng thái nào khác "tạm" / "hoàn tất" (vd hủy, hoàn tiền) không?

**Câu hỏi cho BA:** Liệt kê enum `paymentstatus` và mã phương thức thanh toán đặc biệt dùng cho gạch nợ tạm.

---

### CL-GN-05 · "Mỗi bill chỉ gạch một lần" vs gạch từng phần — bill gạch thiếu có được gạch tiếp khi có Paid mới?
📍 `DOC-v2.0-01 BR-GN-01 (L509)` ↔ `BR-GN-04 (L518-519)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · *mới — 16/10/2026*

**BR-GN-01** — `L509`
> Chỉ gạch bill còn nợ; mỗi bill chỉ gạch một lần.

**BR-GN-04** — `L518-519`
> Mỗi lần gạch = nhỏ nhất của số dư Paid và nợ còn lại; ghi Payment, trừ Paid, đẩy Kafka Out về kênh thanh toán.
> Dừng khi hết nợ hoặc hết Paid; Paid dư được giữ lại.

↳ **Ghi chú:** Đọc đúng chữ thì bill gạch thiếu ở SC-GN-031 sẽ không bao giờ được gạch tiếp. Suy diễn của analyst: "một lần" nghĩa là không gạch lại cùng khoản Paid, còn Paid mới vẫn gạch tiếp được — cần xác nhận.

**Câu hỏi cho BA:** Bill đã gạch một phần, khi Paid mới về (đợt thanh toán sau) có được gạch tiếp không?

🟡 **Làm rõ một phần 19/10/2026** — QC: số tiền gạch phải bằng số tiền cần thanh toán; gạch xong bill chuyển "Đã thanh toán" ⇒ không gạch nữa. Còn mở: câu trả lời chưa nói bill **mới gạch một phần** (BR-GN-04 "Gạch từng phần… nhỏ nhất của số dư Paid và nợ còn lại") có được gạch tiếp khi có Paid mới không. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-GN-06 · Gỡ gạch tạm rồi Paid hoàn tất nhỏ hơn nợ: HĐ quay về "còn nợ" — có hệ quả / cảnh báo?
📍 `DOC-v2.0-01 BR-NT-04 · L503`  ·  Status: **Open** · *mới — 16/10/2026*

> Khi Paid chuyển sang thanh toán hoàn tất, nếu hóa đơn đã gạch nợ tạm thì gỡ Payment tạm trước (hóa đơn trở lại còn nợ) rồi mới gạch nợ thật.

↳ **Ghi chú:** Sàn quyết toán có thể trừ phí ⇒ Paid hoàn tất < nợ. HĐ từ "Đã gạch nợ" về "còn nợ" — downstream (hậu kỳ, báo cáo) có bị ảnh hưởng? Phí TMĐT là một PaidType — có được dùng để gạch phần chênh không?

**Câu hỏi cho BA:** Khi Paid quyết toán của sàn nhỏ hơn nợ, phần chênh xử lý thế nào (Paid phí TMĐT? để còn nợ?)

---

### CL-GN-07 · Danh mục loại cọc ↔ dịch vụ; đơn bán thêm dùng cọc nào?
📍 `DOC-v2.0-01 BR-GC-02 (L534)` + `BR-GC-03 (L539)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-60 (Major) cho phần bán thêm

> Cọc của hợp đồng theo từng loại phải đủ cho các dịch vụ dùng loại cọc đó trên bill.
> (...)
> Mỗi dịch vụ trừ đúng loại cọc của nó; nhiều dịch vụ cùng loại cọc gom thành một dòng Payment.

↳ **Ghi chú:** URD 2.2 không nói loại cọc của dịch vụ lưu ở đâu. Cần danh mục để dựng SC-GN-039..042. SubServiceType 25 "Đặt cọc thuê bao" (§A.3) có liên quan không?

**Câu hỏi cho BA:** Danh mục loại cọc + dịch vụ dùng loại nào; đơn bán thêm có dùng chung cọc của hợp đồng không?

🟡 **Làm rõ một phần 19/10/2026** — Đơn bán mới và bán thêm đều có cọc; loại cọc: **đặt cọc trừ dần, đặt cọc hợp đồng, đặt cọc thiết bị**. Tra cứu: Quản lý kế toán › Tiền đặt cọc › Tra cứu. Còn mở: map dịch vụ ↔ loại cọc; đơn bán thêm dùng chung cọc còn lại của hợp đồng không. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-GN-08 · Nhánh Paid: thứ tự giữa đội EVC gạch EVC và INVOICE gạch tiền khách?
📍 `DOC-v2.0-01 BR-VC (L545-546)`  ·  Status: **Open — mở lại 19/10/2026** · *mới — 16/10/2026*

**URD 2.2** — `L545-546`
> Phần gạch nợ bằng EVC do đội EVC thực hiện; ISC tự quyết phương thức quản trị và xử lý voucher.
> Với EVC bị lock (khách chưa ký hợp đồng), INVOICE chừa phần lock khi gạch tiền khách

↳ **Ghi chú:** 2.2 không giữ câu "gạch EVC trước". Nếu INVOICE gạch tiền khách trước khi đội EVC gạch (EVC không lock) ⇒ tiền khách cover luôn phần EVC, Paid khách bị dùng thừa, đội EVC không còn nợ để gạch. Chỉ phần **lock** được chừa ra theo 2.2.

**Câu hỏi cho BA:** Ở nhánh Paid, INVOICE có phải chờ đội EVC gạch phần EVC (không lock) xong mới gạch tiền khách không? Nếu không, INVOICE có chừa phần EVC không lock không?

⛔ **OUT-SCOPE 19/10/2026** — TP §2.2 #5 *"Gạch nợ bằng EVC / voucher"* ngoài phạm vi (BR-VC L545 *"Phần gạch nợ bằng EVC do đội EVC thực hiện"*); chỉ giữ phần INVOICE chừa EVC bị lock. QC owner 19/10/2026: phần gạch nợ EVC không test. Thứ tự đội EVC gạch EVC ↔ INVOICE gạch tiền khách thuộc phần đội EVC ⇒ không hỏi. SC-GN-045 (INVOICE không ghi Payment cho phần EVC) giữ làm kiểm ranh giới.

🔄 **MỞ LẠI 19/10/2026** — QC owner: phần **gạch nợ EVC / voucher VẪN TEST**, chờ BA liệt kê các loại EVC / voucher. Ghi nhận ⛔ OUT-SCOPE / thu hẹp phía trên **bị hủy**. ⚠️ Khác TP §2.2 #5 (TP chưa cập nhật — QC owner xử lý TP, analyze không sửa TP). Câu hỏi gốc giữ nguyên (thứ tự đội EVC gạch EVC ↔ INVOICE gạch tiền khách).

---

### CL-GN-09 · Hai bill bằng tiền nhau: thứ tự gạch?
📍 `DOC-v2.0-01 BR-GN-03 · L513`  ·  Status: **Open — đã rõ một phần 19/10/2026** · *mới — 16/10/2026* (Low)

> Một đơn có 1..n bill; gạch từng bill, theo số tiền từ cao xuống thấp.

↳ **Ghi chú:** Chỉ ảnh hưởng khi Paid / cọc không đủ cho cả 2 bill. SC-GN-030 để P3.

**Câu hỏi cho BA:** Bill bằng tiền thì ưu tiên theo BillDate / BillNumber?

🟡 **Làm rõ một phần 19/10/2026** — QC: 1 đơn nhiều bill ⇒ ưu tiên bill có **BillNumber cao nhất**. Còn mở: xác nhận đây **chỉ là tie-break khi 2 bill bằng tiền** — nếu là quy tắc chung thì trái BR-GN-03 ("theo số tiền từ cao xuống thấp"). Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-GN-10 · Chi tiết gạch nợ URD 2.2 chuyển sang Phụ lục D#4 — chưa có đặc tả
📍 `DOC-v2.0-01 §D#4 · L671-673`  ·  Status: **Open — mở lại 19/10/2026** · *mới — 16/10/2026*

> Cấu hình EVC: PaidType, Owner gạch, trần 50%, EVC bị lock chi tiết.
> BR-VC-01 đến 07, BR-GC-04 đến 07
> Đội EVC thực hiện; một số bước đã đánh dấu bỏ.

↳ **Ghi chú:** Phụ lục D của URD 2.2 trỏ chi tiết về tài liệu không còn sử dụng ⇒ chưa có: danh mục PaidType; nguồn tổng EVC + tiền lock và loại EVC nào có lock (CL-GN-02); bảng tồn cọc và nơi ghi loại cọc của dịch vụ (CL-GN-07); nghĩa của "mỗi bill chỉ gạch một lần" (CL-GN-05); thứ tự đội EVC gạch (CL-GN-08). Phần URD 2.2 tự đủ, vẫn dùng: cọc theo hợp đồng (L529, L534), mỗi dịch vụ trừ đúng loại cọc, gom dòng Payment theo loại cọc (L539).

**Câu hỏi cho BA:** Phụ lục D#4 của URD 2.2 chưa có đặc tả. PO / đội EVC cung cấp: (1) danh mục PaidType và mã voucher; (2) nguồn / API lấy tổng EVC và tiền lock, loại EVC nào có lock; (3) bảng / trường lưu tồn cọc và loại cọc của từng dịch vụ?

🟡 **Thu hẹp 19/10/2026** — TP §2.2 #5 *"Gạch nợ bằng EVC / voucher"* ngoài phạm vi (BR-VC L545 *"Phần gạch nợ bằng EVC do đội EVC thực hiện"*); chỉ giữ phần INVOICE chừa EVC bị lock. QC owner 19/10/2026: phần gạch nợ EVC không test. Phụ lục D#4 (cấu hình EVC) không dùng (QC owner). Bỏ ý (2) nguồn / API EVC + loại EVC lock. Còn hỏi: (1) danh mục PaidType (để phân biệt Paid tiền khách / voucher khi đồng bộ — SC-GN-002); (3) bảng / trường lưu tồn cọc và loại cọc của từng dịch vụ.

🔄 **MỞ LẠI 19/10/2026** — QC owner: phần **gạch nợ EVC / voucher VẪN TEST**, chờ BA liệt kê các loại EVC / voucher. Ghi nhận ⛔ OUT-SCOPE / thu hẹp phía trên **bị hủy**. ⚠️ Khác TP §2.2 #5 (TP chưa cập nhật — QC owner xử lý TP, analyze không sửa TP). Hỏi lại đủ 3 ý (Phụ lục D#4 vẫn **không** lấy từ URD 2.1 — hỏi BA): (1) danh mục loại EVC / voucher (PaidType, mã voucher); (2) loại EVC nào có lock + nguồn tổng EVC và tiền lock; (3) bảng / trường lưu tồn cọc và loại cọc của dịch vụ.
