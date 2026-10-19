---
id: v2.0/GN/requirement_traceability
title: Requirement Traceability — Module GN
type: requirement_traceability
version: v2.0
module: { code: GN, dir: GN, name: "Gạch nợ hóa đơn" }
doc_source:
  - id: DOC-v2.0-01
    section: "§A.5 #6–#9 · §B.II"
status: ANALYZED
updated: 2026-10-16
---

# Requirement Traceability — v2.0 · Module GN

> Tạo bởi: analyze-requirements. Ma trận truy vết REQ ↔ DOC ↔ Scenario ↔ Clarification.
> **Layout v2** — quote REQ ở **§2** file này; quote SC ở `test_scenario_map.md`; CL ở `risk_assessment.md`.
> `req_notation: BR` ⇒ **Schema A**. `L<n>` = số dòng bản trích text `.docx` (`scripts/doc/search-doc.sh`).

## 1. Traceability Matrix (REQ → DOC → SC)

### Schema A — Module GN — DOC-v2.0-01

| REQ ID | Maps (Ref DOC) | DOC §section | Scenarios | Clarification |
|--------|----------------|--------------|-----------|---------------|
| REQ-GN-001 | BR-DP-01 | DOC-v2.0-01 §II.c (L474) | SC-GN-001, SC-GN-002 | CL-GN-01 |
| REQ-GN-002 | BR-DP-01 | DOC-v2.0-01 §II.c (L475) | SC-GN-003, SC-GN-004, SC-GN-005, SC-GN-006 | — |
| REQ-GN-003 | BR-DP-01 | DOC-v2.0-01 §II.c (L476) | SC-GN-007 | — |
| REQ-GN-004 | BR-XL-01 | DOC-v2.0-01 §II.c (L480-481) | SC-GN-008, SC-GN-009, SC-GN-010 | — |
| REQ-GN-005 | BR-XL-01 | DOC-v2.0-01 §II.c (L482) | SC-GN-011, SC-GN-012, SC-GN-013 | CL-GN-03, CL-GN-04 |
| REQ-GN-006 | BR-XL-03 | DOC-v2.0-01 §II.c (L486) | SC-GN-014 | — |
| REQ-GN-007 | BR-XL-03 | DOC-v2.0-01 §II.c (L487-488) | SC-GN-015, SC-GN-016, SC-GN-017 | — |
| REQ-GN-008 | BR-XL-03 | DOC-v2.0-01 §II.c (L489) | SC-GN-018, SC-GN-021 | — |
| REQ-GN-009 | BR-NT-01 | DOC-v2.0-01 §II.c (L493-494) | SC-GN-019, SC-GN-020 | CL-GN-03 |
| REQ-GN-010 | BR-NT-02 | DOC-v2.0-01 §II.c (L498-499) | SC-GN-019 | CL-GN-04 |
| REQ-GN-011 | BR-NT-04 | DOC-v2.0-01 §II.c (L503-504) | SC-GN-022, SC-GN-023, SC-GN-024 | CL-GN-04, CL-GN-06 |
| REQ-GN-012 | BR-GN-01 | DOC-v2.0-01 §II.c (L508-509) | SC-GN-025, SC-GN-026, SC-GN-027 *(SC-GN-048 deprecated 19/10/2026 — out-scope)* | CL-GN-05 |
| REQ-GN-013 | BR-GN-03 | DOC-v2.0-01 §II.c (L513-514) | SC-GN-028, SC-GN-029, SC-GN-030 | CL-GN-09 |
| REQ-GN-014 | BR-GN-04 | DOC-v2.0-01 §II.c (L518-520) | SC-GN-031, SC-GN-032, SC-GN-033, SC-GN-034, SC-GN-035 | CL-GN-05 |
| REQ-GN-015 | BR-GN-05 | DOC-v2.0-01 §II.c (L524-525) | SC-GN-036 | — |
| REQ-GN-016 | BR-GC-01 | DOC-v2.0-01 §II.c (L529-530) | SC-GN-037, SC-GN-038 | CL-GN-02 |
| REQ-GN-017 | BR-GC-02 | DOC-v2.0-01 §II.c (L534-535) | SC-GN-039, SC-GN-040, SC-GN-041 | CL-GN-07 |
| REQ-GN-018 | BR-GC-03 | DOC-v2.0-01 §II.c (L539-541) | SC-GN-042, SC-GN-043, SC-GN-044, SC-GN-050 | CL-GN-07 |
| REQ-GN-019 | BR-VC | DOC-v2.0-01 §II.c (L545) | SC-GN-045 | — *(CL-GN-01, 08 out-scope 19/10/2026)* |
| REQ-GN-020 | BR-VC | DOC-v2.0-01 §II.c (L546) | SC-GN-046, SC-GN-047 *(SC-GN-049 deprecated 19/10/2026)* | CL-GN-02 |

> `§II.c` = mục B.II "Gạch nợ hóa đơn" → c. Business rules. Mọi REQ đều có ≥1 SC.
> Đơn **bán thêm** (REQ-XHD-040, phạm vi chung từ mail PM) có SC riêng ở module này: SC-GN-050 (nhánh Cọc dùng cọc của hợp đồng đang hoạt động).

## 2. Requirement Source Detail (verbatim quotes — home của REQ quote)

### REQ-GN-001 · Đồng bộ Paid 1:1 từ Orderpaid theo OrderCode, gồm voucher và tiền khách, gán PaidType
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L474`  ·  Clarif: `CL-GN-01`

> Paid đồng bộ 1:1 từ Orderpaid theo OrderCode, gồm cả voucher và tiền khách thanh toán; mỗi Paid gán PaidType theo nguồn tiền.

↳ **Ghi chú:** Nhiều đợt thanh toán là các dòng detail trong cùng 1 Orderpaid. PaidType phân loại tiền khách / voucher / phí TMĐT. Paid voucher được đồng bộ nhưng việc gạch EVC thuộc đội EVC ⇒ Paid voucher có bị INVOICE dùng để gạch không là CL-GN-01.

---

### REQ-GN-002 · Chống trùng Paid theo 4 trường: trùng → cập nhật paymentstatus, không trùng → thêm mới
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L475`  ·  Clarif: —

> Trùng khi giống cả 4 trường OrderCode + RefTransactionId + PaidType + Amount: trùng thì cập nhật paymentstatus, không trùng thì thêm mới.

↳ **Ghi chú:** EP theo từng trường khác nhau ⇒ 1 SC trùng đủ 4 + 3 SC khác 1 trường (OrderCode khác đã ra đơn khác nên bỏ). Trường hợp trùng chỉ cập nhật `paymentstatus`, không đổi Amount.

---

### REQ-GN-003 · Đồng bộ Paid độc lập, luôn ghi nhận kể cả khi HĐ chưa phát hành
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L476`  ·  Clarif: —

> Đồng bộ Paid là luồng độc lập với gạch nợ và luôn ghi nhận Paid kể cả khi hóa đơn chưa phát hành.

↳ **Ghi chú:** Paid về trước HĐ ⇒ nằm chờ, điểm chạm (b) "sau khi xuất hóa đơn" hoặc (c) worker 30 phút sẽ nhặt lên.

---

### REQ-GN-004 · 3 điểm chạm xét gạch nợ; điểm chạm chỉ là thời điểm kích hoạt
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L480-481`  ·  Clarif: —

> 3 điểm chạm: (a) đồng bộ Paid xong; (b) sau khi xuất hóa đơn; (c) worker quét 30 phút một lần.
> Điểm chạm chỉ là thời điểm kích hoạt; loại gạch nợ do paymentstatus của Paid quyết định.

↳ **Ghi chú:** 3 lớp EP trigger. Điểm chạm (b) nối từ Invoice Event của XHD (REQ-XHD-037).

---

### REQ-GN-005 · Lọc sớm ở điểm chạm (a): chỉ đi tiếp khi Paid tạm + kênh sàn, hoặc Paid hoàn tất
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L482`  ·  Clarif: `CL-GN-03`, `CL-GN-04`

> Ở điểm chạm (a), chỉ xử lý tiếp khi Paid ở trạng thái gạch nợ tạm và đơn thuộc kênh sàn, hoặc Paid đã thanh toán hoàn tất.

↳ **Ghi chú:** Bộ lọc chỉ áp điểm chạm (a); điểm chạm (b), (c) vẫn xét kênh trong luồng gạch Paid. Giá trị enum `paymentstatus` ngoài "tạm" / "hoàn tất" (nếu có) dừng ngay — enum chưa có (CL-GN-04).

---

### REQ-GN-006 · Lấy nợ HĐ kèm trường gạch nợ Paid/Cọc; không có nợ thì dừng
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L486`  ·  Clarif: —

> Lấy nợ hóa đơn kèm trường gạch nợ Paid/Cọc; không có nợ thì dừng, chờ điểm chạm sau.

↳ **Ghi chú:** "Không có nợ" gồm HĐ đã gạch đủ và HĐ chưa phát hành.

---

### REQ-GN-007 · Trường Paid/Cọc: có thì dùng; chưa có thì gọi API kênh thanh toán và lưu OrderBill; API lỗi/timeout thì dừng
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L487-488`  ·  Clarif: —

> Trường đã có giá trị thì dùng luôn; chưa có thì gọi API kênh thanh toán rồi lưu vào OrderBill.
> API lỗi hoặc timeout thì dừng, không retry trong cùng lần.

↳ **Ghi chú:** Verify bằng số lần gọi API (mock): lần 2 không gọi lại vì đã lưu. Lỗi ⇒ không gạch, chờ điểm chạm sau gọi lại.

---

### REQ-GN-008 · Một đơn chỉ đi một luồng: Paid (có gạch nợ tạm) hoặc Cọc (không có gạch nợ tạm)
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L489`  ·  Clarif: —

> Một đơn chỉ đi một luồng: Paid (có gạch nợ tạm) hoặc Cọc (không có gạch nợ tạm).

↳ **Ghi chú:** Không trộn Paid + Cọc trên cùng đơn. Nhánh Cọc không bao giờ gạch tạm.

---

### REQ-GN-009 · Điều kiện gạch nợ tạm: Paid ở trạng thái tạm VÀ đơn kênh sàn; kênh khác chờ Paid hoàn tất
📍 `DOC-v2.0-01 §II.c BR-NT-01 · L493-494`  ·  Clarif: `CL-GN-03`

> Chỉ gạch nợ tạm khi Paid ở trạng thái gạch nợ tạm và đơn thuộc kênh bán qua sàn (khách thanh toán với sàn nên tiền chưa chắc về công ty).
> Kênh khác như tại quầy, tại nơi triển khai: không gạch nợ tạm, chờ Paid thanh toán hoàn tất rồi gạch nợ thật.

↳ **Ghi chú:** "Kênh sàn" — §A.2 không đánh dấu kênh nào là sàn; giả định {20, 21} theo §A.1 L59 "kênh TMĐT (Shopee, TikTok Shop)" của 2.2 () (CL-GN-03).

---

### REQ-GN-010 · Cách ghi gạch nợ tạm: Payment phương thức đặc biệt = toàn bộ nợ còn lại; HĐ chuyển "Đã gạch nợ"
📍 `DOC-v2.0-01 §II.c BR-NT-02 · L498-499`  ·  Clarif: `CL-GN-04`

> Ghi Payment bằng phương thức thanh toán đặc biệt, số tiền bằng toàn bộ nợ còn lại.
> Khoản này tính vào tổng Payment nên hóa đơn chuyển sang "Đã gạch nợ" ngay.

↳ **Ghi chú:** Mã "phương thức thanh toán đặc biệt" chưa có (CL-GN-04). Số tiền = nợ **còn lại** (không phải tổng HĐ).

---

### REQ-GN-011 · Gỡ gạch nợ tạm trước khi gạch nợ thật; chưa gạch tạm thì gạch thật luôn
📍 `DOC-v2.0-01 §II.c BR-NT-04 · L503-504`  ·  Clarif: `CL-GN-06`

> Khi Paid chuyển sang thanh toán hoàn tất, nếu hóa đơn đã gạch nợ tạm thì gỡ Payment tạm trước (hóa đơn trở lại còn nợ) rồi mới gạch nợ thật.
> Chưa gạch tạm thì gạch thật luôn.

↳ **Ghi chú:** Chuyển trạng thái "Đã gạch nợ" → "còn nợ" → (gạch thật) → "Đã gạch nợ" nếu đủ tiền. Paid hoàn tất < nợ ⇒ HĐ kết thúc ở "còn nợ" — URD không nói có hệ quả gì (CL-GN-06).

---

### REQ-GN-012 · Paid dùng để gạch: Amount > 0, cùng OrderCode; chỉ gạch bill còn nợ, mỗi bill một lần
📍 `DOC-v2.0-01 §II.c BR-GN-01 · L508-509`  ·  Clarif: `CL-GN-01`, `CL-GN-05`

> Chỉ lấy dòng Paid có Amount > 0 và cùng OrderCode với hóa đơn.
> Chỉ gạch bill còn nợ; mỗi bill chỉ gạch một lần.

↳ **Ghi chú:** Biên Amount `> 0`. "Mỗi bill chỉ gạch một lần" mâu thuẫn bề ngoài với gạch từng phần BR-GN-04 (bill gạch thiếu, Paid mới về thì gạch tiếp?) — chưa rõ (CL-GN-05).

---

### REQ-GN-013 · Gạch theo từng bill, số tiền từ cao xuống thấp — cả nhánh Paid và Cọc
📍 `DOC-v2.0-01 §II.c BR-GN-03 · L513-514`  ·  Clarif: `CL-GN-09`

> Một đơn có 1..n bill; gạch từng bill, theo số tiền từ cao xuống thấp.
> Áp dụng cho cả nhánh Paid và nhánh Cọc.

↳ **Ghi chú:** Hai bill bằng tiền nhau: thứ tự không định nghĩa (CL-GN-09). Thứ tự quan trọng khi Paid không đủ cho mọi bill.

---

### REQ-GN-014 · Gạch từng phần = min(số dư Paid, nợ còn lại); ghi Payment, trừ Paid, Kafka Out; dừng khi hết nợ / hết Paid
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L518-520`  ·  Clarif: `CL-GN-05`

> Mỗi lần gạch = nhỏ nhất của số dư Paid và nợ còn lại; ghi Payment, trừ Paid, đẩy Kafka Out về kênh thanh toán.
> Dừng khi hết nợ hoặc hết Paid; Paid dư được giữ lại.
> Nhánh Cọc không đẩy Kafka Out.

↳ **Ghi chú:** BVA Paid < nợ / = nợ / > nợ. 3 đầu ra mỗi lần gạch: Payment, Paid giảm, Kafka Out (payload chưa có — CL-XHD-29).

---

### REQ-GN-015 · Trạng thái "Đã gạch nợ" khi tổng Payment = tổng tiền HĐ (cả tạm và thật)
📍 `DOC-v2.0-01 §II.c BR-GN-05 · L524-525`  ·  Clarif: —

> Khi tổng Payment bằng tổng tiền hóa đơn thì hóa đơn chuyển sang "Đã gạch nợ".
> Áp dụng cho cả gạch nợ tạm và gạch nợ thật.

↳ **Ghi chú:** Cũng là "Kết quả" của chức năng II (L465). Biên Σ Payment = tổng HĐ − 1 / = tổng HĐ.

---

### REQ-GN-016 · Nhánh Cọc — đủ tiền: Σ cọc còn lại của hợp đồng + Σ EVC của đơn (gồm lock) ≥ nợ bill
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529-530`  ·  Clarif: `CL-GN-02`

> Tổng cọc còn lại của hợp đồng (mọi loại cọc) cộng tổng tiền EVC của đơn (tính cả phần bị lock) phải không nhỏ hơn nợ của bill đang xét.
> Cọc chỉ gồm tiền thật khách trả, không gồm EVC.

↳ **Ghi chú:** Phạm vi cọc theo **hợp đồng**, không theo OrderCode. Tổng EVC + lock lấy qua API đội EVC — 2.2 không nêu nguồn (CL-GN-02). Biên "không nhỏ hơn" ⇒ bằng nhau là đủ.

---

### REQ-GN-017 · Nhánh Cọc — đủ cọc theo loại; thiếu một loại thì không gạch cả bill, bill khác vẫn xét
📍 `DOC-v2.0-01 §II.c BR-GC-02 · L534-535`  ·  Clarif: `CL-GN-07`

> Cọc của hợp đồng theo từng loại phải đủ cho các dịch vụ dùng loại cọc đó trên bill.
> Thiếu ở một loại thì không gạch cả bill đó, không gạch một phần; các bill khác của đơn vẫn xét bình thường.

↳ **Ghi chú:** Loại cọc tương ứng dịch vụ đã ghi sẵn trên dòng chi tiết HĐ. Danh sách loại cọc chưa có (CL-GN-07).

---

### REQ-GN-018 · Nhánh Cọc — cách trừ cọc
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L539-541`  ·  Clarif: `CL-GN-07`

> Mỗi dịch vụ trừ đúng loại cọc của nó; nhiều dịch vụ cùng loại cọc gom thành một dòng Payment.
> Tính trên nợ còn lại sau khi EVC đã gạch; ghi Payment và trừ cọc theo BillNumber + số hợp đồng.
> Dư cọc không xử lý; không gạch lại hóa đơn đã gạch.

↳ **Ghi chú:** Nhiều dịch vụ cùng loại cọc gom thành một dòng Payment (L539) ⇒ số dòng Payment = số loại cọc trên bill. "Sau khi EVC đã gạch" ⇒ phụ thuộc đội EVC gạch trước (CL-GN-08).

---

### REQ-GN-019 · Gạch nợ bằng EVC do đội EVC thực hiện — INVOICE không gạch EVC
📍 `DOC-v2.0-01 §II.c BR-VC · L545, L547`  ·  Clarif: `CL-GN-01`, `CL-GN-08`

> Phần gạch nợ bằng EVC do đội EVC thực hiện; ISC tự quyết phương thức quản trị và xử lý voucher.
> (...)
> Chi tiết cấu hình EVC xem phụ lục.

↳ **Ghi chú:** Ranh giới phạm vi: INVOICE **không** ghi Payment EVC. Gạch nợ EVC ngoài phạm vi test (TP §2.2 #5); mail PM "EVC cần test => theo rule URD" ⇒ chỉ test phần INVOICE (REQ-GN-019, 020). Cấu hình EVC (PaidType, Owner, trần 50%) ở phụ lục D#4 — đội EVC.

---

### REQ-GN-020 · EVC bị lock: INVOICE chừa phần lock — số gạch = min(nợ bill − tiền lock, Paid khách)
📍 `DOC-v2.0-01 §II.c BR-VC · L546`  ·  Clarif: `CL-GN-02`

> Với EVC bị lock (khách chưa ký hợp đồng), INVOICE chừa phần lock khi gạch tiền khách: số gạch = nhỏ nhất của (nợ bill trừ tiền lock) và Paid khách thanh toán.

↳ **Ghi chú:** Hiện chỉ EVC Loyalty FTEL có khoản lock. BVA: lock = 0 · Paid khách < / = / > (nợ − lock). Nguồn số tiền lock + lỗi API: CL-GN-02.

---

> **Quy ước:** Implicit REQ → *(Implicit — không có quote trực tiếp)* + derivation ở Ghi chú. Quote >500 ký tự → sidecar `v2.0/quotes/`.
> **Clarification quote KHÔNG ở đây** — `GN/risk_assessment.md` §Clarifications. **SC quote** ở `test_scenario_map.md`.
