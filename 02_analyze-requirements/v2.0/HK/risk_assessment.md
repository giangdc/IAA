---
id: v2.0/HK/risk_assessment
title: Risk Assessment — Module HK
type: risk_assessment
version: v2.0
module: { code: HK, dir: HK, name: "Đẩy hậu kỳ qua dịch vụ – tiền trả trước" }
counts:                 # 🔑 CANONICAL — CL/RISK của module HK
  cl: 9
  cl_open: 9
  cl_blocking: 2
  risk: 5
  risk_high: 2
status: ANALYZED
updated: 2026-10-16
---

# Risk Assessment — v2.0 · Module HK

> Tạo bởi: analyze-requirements. Đánh giá rủi ro per module + định hướng test focus cho generate-tc/vibe-test.
>
> **Structure-lock:** dùng DUY NHẤT 1 dạng bảng chi tiết hợp nhất bên dưới cho MỌI module (KHÔNG dùng nhiều dạng bảng khác nhau giữa các module). KHÔNG đổi cột. Bảng gồm 9 cột (thêm `Solution` + `Status` để track vòng đời rủi ro).
>
> **Governance (layout v2):** file này là **nguồn PRIMARY duy nhất** cho risk + **Clarification** của module HK. Thiếu API spec HĐĐT / Dịch vụ thuộc risk xuyên suốt RISK-XHD-01 / CL-XHD-29 (home ở `XHD/`).
> Mã `GAP-NN` trỏ về `01_test-plans/DOC-READINESS-InvoiceIssuance-v2.0.md` / TP §2.4.

## Tổng quan
| Module | Risk Level | Rủi ro chính |
|--------|-----------|--------------|
| HK | High | Ký hiệu HĐĐT "cần chốt" — test trên bảng map 2.1 là giả định, mà sai đầu số là sai kê khai thuế; dòng EVC / chiết khấu / thông tin theo mẫu chưa có đặc tả nên chưa test được |

## Chi tiết rủi ro (bảng hợp nhất — 1 dạng cho mọi module)
| Risk ID | Module/Area | Rủi ro | Severity | Why (Source) | Test Focus | Solution | Status | REQ/SC |
|---------|-------------|--------|----------|--------------|------------|---------------------|--------|--------|
| RISK-HK-01 | HK / ký hiệu + ID HĐĐT | Bảng map vùng × loại đầu chưa chốt (DVKH HO ↔ FAF); loại HĐ nào dùng đầu M/U/A chưa có ⇒ TC theo 2.1 có thể sai toàn bộ; sai đầu số = sai kê khai thuế | High | DOC-v2.0-01 BR-HK-03 (L581-585), §C#1; GAP-17 | SC-HK-008..011, 020 — phủ đủ 7 vùng × 3 đầu + FPL | Xin bản chốt ký hiệu (CL-HK-01) trước generate-tc; TC đánh dấu "giả định bảng 2.1" | Open | SC-HK-008, SC-HK-009, SC-HK-010, SC-HK-011, SC-HK-020 · REQ-HK-005, REQ-HK-006 |
| RISK-HK-02 | HK / dòng EVC + chiết khấu + thông tin mẫu | BR-HK-02 bắt chuẩn bị "dòng EVC" và "thông tin theo mẫu" nhưng không có rule ⇒ chưa có SC; nếu thiếu thì HĐĐT không được đẩy (BR-HK-02) — chặn cả luồng | High | DOC-v2.0-01 BR-HK-02 (L575), §D#6; GAP-04 (Blocker), GAP-35 | SC-HK-006, 007 (gián tiếp) | PM chốt Out-scope hoặc đặc tả (CL-HK-03, 04); TP đề xuất Out-scope | Open | SC-HK-006, SC-HK-007 · REQ-HK-004, REQ-HK-010 |
| RISK-HK-03 | HK / tiền trả trước | "Một lần mỗi đơn" nhưng không rõ đợt nào, số tiền nào, TB có add không; 2.1 nói per dịch vụ ⇒ add sai số tiền hoặc thiếu tiền DV phát hành sau | Medium | DOC-v2.0-01 BR-HK-09 (L596) ↔ DOC-v2.0-02 L753; GAP-59 | SC-HK-015, 016, 021 | Resolve CL-HK-07; đơn DV + TB phát hành nhiều đợt | Open | SC-HK-015, SC-HK-016, SC-HK-021 · REQ-HK-009 |
| RISK-HK-04 | HK / hệ thống ngoài | HĐĐT, hệ thống Dịch vụ không sẵn trên STG; không có hành vi lỗi ⇒ không verify được "đã gen HĐĐT" / "đã add tiền" | Medium | TP §2.1b #24, #25; GAP-18, GAP-20 | SC-HK-006, 015, 018, 019 | Mock/stub + xác nhận hành vi lỗi (CL-HK-05, 06) | Open | SC-HK-006, SC-HK-015, SC-HK-018, SC-HK-019 · REQ-HK-001, REQ-HK-004, REQ-HK-009 |
| RISK-HK-05 | HK / đơn vị có đầu số riêng | FPL, FMC có đầu số / dãy số / mẫu riêng (2.1 BR-HK-10) — scope chưa rõ ⇒ HĐ của các đơn vị này có thể ra ký hiệu chung sai | Medium | DOC-v2.0-01 BR-HK-03 (L583), §D#5; GAP-34 | SC-HK-009 | PM xác nhận in/out scope (CL-HK-02) | Open | SC-HK-009 · REQ-HK-005 |

> Risk ID format: `RISK-<MODULE>-<NN>` (vd `RISK-PV-01`). Severity = High / Medium / Low (có thể Medium-High).
> **Solution:** biện pháp giảm thiểu hoặc hướng xử lý cụ thể (vd "resolve C-XXX trước generate-tc", "thêm negative TC cho MSG", "defer tới khi có env"). Chưa có → `—` (nhưng High/Medium nên có).
> **Status** — trạng thái xử lý rủi ro. Enum THUẦN (không kèm ghi chú trong ô — lý do để ở cột `Solution`):
> - `Open` = chưa xử lý / **đang bị chặn** (env/API/BA/backend chưa sẵn → chưa cover được).
> - `Pending` = **chấp nhận + defer có chủ đích** (không xử ở version này; vd NFR chờ môi trường thật / tải lớn).
> - `Resolved` = **đã xử lý và thêm test case cover** rủi ro (có `Solution` + TC/SC khả thi).
> - `Closed` = **bỏ khỏi scope** (feature loại khỏi version → rủi ro không còn áp dụng).
> KHÔNG để trống. Vòng đời: `Open` → `Resolved` (khi đã cover) · `Open` → `Pending` (defer) · `→ Closed` (bỏ scope).

## Khuyến nghị tổng thể
1. **Resolve blocker clarifications trước generate-tc** các scenario liên quan: CL-HK-01 (⛔ ký hiệu), CL-HK-03 (⛔ dòng EVC / chiết khấu), CL-HK-07 (tiền trả trước).
2. **Ưu tiên test P1 high-risk:** SC-HK-004, 006..008, 011..013, 015, 016.
3. **Performance / cần môi trường:** không có NFR; cần mock HĐĐT + hệ thống Dịch vụ (RISK-HK-04).
4. **ID/text cleanup (non-blocking, cần trước automation):** 2.1 BR-HK-06 có câu cụt ("…hiện đi từ luồng đơn hàng không có") — chỉ ghi nhận.

## Clarifications (home CL — layout v2)

> 1 CL = 1 heading `### CL-HK-NN · <câu hỏi ngắn>`. Dòng META mang `Status` (+ `⛔ BLOCKING`) và mã GAP. Khi resolved: **thêm** `✅ RESOLVED <ngày> — <kết luận>`, giữ phần phân tích cũ.

### CL-HK-01 · Ký hiệu HĐĐT bản chốt + bảng map; loại HĐ nào dùng đầu M / U / A (kể cả bán thêm)? ⛔ BLOCKING
📍 `DOC-v2.0-01 BR-HK-03 (L581, L585)` + `§C#1 (L640-643)`  ·  Status: **Open — ⛔ BLOCKING** (ký hiệu + ID) · GAP-17 (Critical)

> Ký hiệu hóa đơn xác định theo quy định thuế; DVKH HO chốt với FAF.
> (...)
> Giữ nguyên, cần chốt ký hiệu (gộp BR-HK-04, 10)

**§C#1** — `L641-643`
> Ký hiệu hóa đơn điện tử.
> BR-HK-03
> Chốt theo quy định thuế; bảng map chuyển sang phụ lục.

↳ **Ghi chú:** SC-HK-008..011, 020 đang dùng bảng 2.1 (`quotes/REQ-HK-005.md`). 2.1 chỉ nói "hóa đơn cước và hóa đơn bán mới dùng đầu khác nhau" — không có bảng loại HĐ → đầu.

**Câu hỏi cho BA:** Gửi bản chốt ký hiệu + bảng map vùng × đầu; liệt kê loại HĐ (cước, bán mới, bán thêm, thiết bị…) dùng đầu nào.

---

### CL-HK-02 · Đơn vị có đầu số / dãy số / mẫu riêng (FPL, FMC): trong hay ngoài phạm vi test?
📍 `DOC-v2.0-01 BR-HK-03 (L583)` + `§D#5 (L674-677)`  ·  Status: **Open** · GAP-34 (Major)

> Bảng map vùng miền và các đơn vị có đầu số riêng xem tài liệu kỹ thuật.
> (...)
> Bảng map ký hiệu hóa đơn theo vùng miền; đơn vị có đầu số, dãy số, mẫu riêng.
> BR-HK-03, 04, 10
> DVKH HO chốt với FAF.

↳ **Ghi chú:** 2.1 BR-HK-10 (L811): "ví dụ FPL, FMC. Phần này thuộc luồng nghiệp vụ cũ." "FPL" ở bảng map là đơn vị hay kênh bán 10? HĐ đầu M của FPL thì sao (SC-HK-009)?

**Câu hỏi cho BA:** Đơn vị có đầu số riêng có thuộc phạm vi v2.0 không; nếu có thì danh sách + quy tắc.

---

### CL-HK-03 · Dòng EVC và dòng chiết khấu trên HĐĐT: Out-scope hay có đặc tả? ⛔ BLOCKING
📍 `DOC-v2.0-01 BR-HK-02 (L575)` + `§D#6 (L678-681)`  ·  Status: **Open — ⛔ BLOCKING** (đẩy HĐĐT) · GAP-04 (Blocker)

> INVOICE chuẩn bị đầy đủ các thông tin cần để tạo hóa đơn điện tử (ký hiệu, ID hóa đơn, nội dung hiển thị, dòng EVC, tổng tiền theo thuế suất, thông tin theo mẫu) rồi mới đẩy sang hệ thống HĐĐT.

↳ **Ghi chú:** BR-HK-02 bắt buộc có "dòng EVC" trước khi đẩy, nhưng không có rule (2.1 L725: "nếu loại EVC đó thuộc nhóm được thể hiện"). Mail PM "EVC cần test => theo rule URD" không làm rõ. TP đề xuất Out-scope (rủi ro TP #7). REQ-HK-010 chưa có SC.

**Câu hỏi cho BA:** Dòng EVC / chiết khấu trên HĐĐT có trong phạm vi test v2.0? Nếu có: loại EVC nào được thể hiện, format dòng.

---

### CL-HK-04 · Danh sách trường theo từng mẫu HĐĐT; mức thuế suất không phát sinh có in dòng 0?
📍 `DOC-v2.0-01 §D#6 (L679)` + `BR-HK-07 (L592)`  ·  Status: **Open** · GAP-35 (Major)

> Dòng chiết khấu; thông tin khác theo mẫu hóa đơn.
> (...)
> Gom tổng tiền theo từng mức thuế suất (không chịu thuế, 0%, 5%, 8%, 10%), mỗi mức một dòng gồm thành tiền, thuế GTGT và tổng cộng; sau đó là dòng tổng cộng chung.

↳ **Ghi chú:** Không có mẫu ⇒ expected của SC-HK-006, 014 thiếu trường.

**Câu hỏi cho BA:** Gửi mẫu HĐĐT (trường bắt buộc); mức thuế không có dòng chi tiết thì có in không?

---

### CL-HK-05 · Đẩy HĐĐT lỗi / chưa đủ thông tin: khi nào đẩy lại? Có đánh dấu / retry?
📍 `DOC-v2.0-01 BR-HK-02 · L576`  ·  Status: **Open** · GAP-18 (Critical)

> Chưa đủ thì chưa đẩy.

↳ **Ghi chú:** Không có trigger đẩy lại, không có hành vi lỗi. TP giả định "đẩy lại lần sau" (SC-HK-007, 018).

**Câu hỏi cho BA:** Khi chưa đủ thông tin hoặc HĐĐT lỗi: dòng được đánh dấu gì, ai / job nào đẩy lại, có cảnh báo?

---

### CL-HK-06 · Đẩy hệ thống Dịch vụ (tiền trả trước) lỗi: đánh dấu / retry?
📍 `DOC-v2.0-01 §III.a · L561`  ·  Status: **Open** · GAP-20 (Critical)

> Thông tin dịch vụ và tiền dịch vụ được đẩy đúng theo từng đơn hàng cấu thành hóa đơn; đã add tiền trả trước cho khách.

↳ **Ghi chú:** Ảnh hưởng tính idempotent của BR-HK-09: lỗi rồi đẩy lại có bị tính là "đã add" không (SC-HK-019).

**Câu hỏi cho BA:** Lỗi thì đánh dấu gì, retry thế nào, bảo đảm vẫn chỉ add 1 lần ra sao?

---

### CL-HK-07 · Add tiền trả trước 1 lần / đơn nhiều đợt: đợt nào, số tiền nào, TB có add?
📍 `DOC-v2.0-01 BR-HK-09 (L596)` ↔ `DOC-v2.0-02 §III c.2 bước 2-3 (L750, L753)`  ·  Status: **Open** · GAP-59 (Major), GAP-60 (Major)

**URD 2.2** — `L596`
> Mỗi đơn chỉ add tiền trả trước một lần, kể cả khi đơn phát hành ở nhiều đợt hóa đơn.

**URD 2.1** — `DOC-v2.0-02 L750, L753`
> Đẩy sang hệ thống Dịch vụ để add tiền trả trước cho khách theo từng  Dịch vụ trên hóa đơn
> (...)
> Đánh dấu đã đẩy hậu kỳ, bảo đảm idempotent: một đơn hàng chỉ add tiền trả trước một lần với 1 dịch vụ, kể cả khi hóa đơn phát hành ở nhiều đợt.

↳ **Ghi chú:** 2.1 "một lần với 1 dịch vụ" (per DV) ≠ 2.2 "mỗi đơn một lần" (per đơn). 2.2 thắng, nhưng nếu DV phát hành ở 2 HĐ khác đợt thì DV thứ 2 có được add không? TP giả định: đợt đầu, toàn bộ tiền DV. Đơn bán thêm có add tiền trả trước như bán mới?

**Câu hỏi cho BA:** Tiền trả trước add ở HĐ nào, số tiền = tiền DV của HĐ đó hay của cả đơn; TB có add không; đơn bán thêm có khác không?

---

### CL-HK-08 · Mã tỉnh trong ID HĐ lấy theo đâu?
📍 `DOC-v2.0-01 BR-HK-03 (L582)` ↔ `DOC-v2.0-02 BR-HK-04 (L791)`  ·  Status: **Open** · *mới — 16/10/2026*

**URD 2.2** — `L582`
> ID hóa đơn ghép từ loại đầu + năm + mã tỉnh + số hóa đơn.

**URD 2.1** — `DOC-v2.0-02 L791`
> HN — MÃ TỈNH, lấy theo danh mục tỉnh thành. Ví dụ HN là Hà Nội. Đây là mã tỉnh, không phải mã chi nhánh xác định ở BR-XHD-12.

↳ **Ghi chú:** Không nói tỉnh của địa chỉ xuất HĐ, của hợp đồng, hay của chi nhánh quản lý hợp đồng (nay chi nhánh theo hợp đồng — BR-XHD-12 2.2). Vùng (để tra ký hiệu) cũng suy ra từ tỉnh nào?

**Câu hỏi cho BA:** Mã tỉnh (và vùng) lấy từ địa chỉ nào: địa chỉ xuất HĐ / địa chỉ hợp đồng / tỉnh của chi nhánh?

---

### CL-HK-09 · Một HĐ có thể gồm nhiều đơn hàng không? ("tách theo từng đơn hàng cấu thành hóa đơn")
📍 `DOC-v2.0-01 BR-HK-01 (L571)` ↔ `BR-XHD-05 (L406)`  ·  Status: **Open** · *mới — 16/10/2026*

**BR-HK-01** — `L571`
> Mỗi lần phát hành chỉ đẩy phần vừa xuất, tách theo từng đơn hàng cấu thành hóa đơn.

**BR-XHD-05** — `L406`
> Trong cùng một đợt, các dòng DV/TB đủ điều kiện của cùng một đơn gộp vào một hóa đơn.

↳ **Ghi chú:** XHD gộp theo đơn ⇒ 1 HĐ chỉ 1 đơn; HK lại nói "từng đơn hàng cấu thành hóa đơn" (2.1 L688 còn ghi "1 HĐ có thể gồm nhiều ĐH"). SC-HK-005 phụ thuộc câu trả lời.

**Câu hỏi cho BA:** Có trường hợp 1 HĐ gồm nhiều đơn ở v2.0 không? Nếu không, câu "tách theo từng đơn" chỉ áp cho HĐ luồng cũ?
