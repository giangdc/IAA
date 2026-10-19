---
id: v2.0/HK/risk_assessment
title: Risk Assessment — Module HK
type: risk_assessment
version: v2.0
module: { code: HK, dir: HK, name: "Đẩy hậu kỳ qua dịch vụ – tiền trả trước" }
counts:                 # 🔑 CANONICAL — CL/RISK của module HK
  cl: 11
  cl_open: 5
  cl_blocking: 1
  risk: 5
  risk_high: 2
status: ANALYZED
updated: 2026-10-19
---

# Risk Assessment — v2.0 · Module HK

> Tạo bởi: analyze-requirements. Đánh giá rủi ro per module + định hướng test focus cho generate-tc/vibe-test.
>
> **Structure-lock:** dùng DUY NHẤT 1 dạng bảng chi tiết hợp nhất bên dưới cho MỌI module (KHÔNG dùng nhiều dạng bảng khác nhau giữa các module). KHÔNG đổi cột. Bảng gồm 9 cột (thêm `Solution` + `Status` để track vòng đời rủi ro).
>
> **Governance (layout v2):** file này là **nguồn PRIMARY duy nhất** cho risk + **Clarification** của module HK. Thiếu API spec hóa đơn điện tử / Dịch vụ thuộc risk xuyên suốt RISK-XHD-01 / CL-XHD-29 (home ở `XHD/`).
> Mã `GAP-NN` trỏ về `01_test-plans/DOC-READINESS-InvoiceIssuance-v2.0.md` / TP §2.4.

## Tổng quan
| Module | Risk Level | Rủi ro chính |
|--------|-----------|--------------|
| HK | High | Ký hiệu hóa đơn điện tử: bảng map theo URD 2.1, chỉ test đầu U (hóa đơn bán mới + bán thêm) — nhưng **chưa có chỗ kiểm ký hiệu** trên STG (CL-HK-11), mà sai đầu số là sai kê khai thuế; dòng EVC / thông tin theo mẫu chưa có đặc tả (CL-HK-03, 04) |

## Chi tiết rủi ro (bảng hợp nhất — 1 dạng cho mọi module)
| Risk ID | Module/Area | Rủi ro | Severity | Why (Source) | Test Focus | Solution | Status | REQ/SC |
|---------|-------------|--------|----------|--------------|------------|---------------------|--------|--------|
| RISK-HK-01 | HK / ký hiệu + ID hóa đơn điện tử | Bảng map vùng × loại đầu lấy theo URD 2.1 BR-HK-03; phạm vi chỉ đầu U (hóa đơn bán mới + bán thêm — CL-HK-01). Rủi ro còn lại: tool Liệt kê cước chỉ hiển thị ID hóa đơn ⇒ **chưa có chỗ kiểm ký hiệu** (2 ký tự cuối theo vùng); sai đầu số = sai kê khai thuế | High | DOC-v2.0-01 BR-HK-03 (L581-585), §C#1; DOC-v2.0-02 BR-HK-03, 04; GAP-17 | SC-HK-008, 009, 010, 011, 020 — 7 vùng × đầu U + FPL | Hỏi BA điểm verify ký hiệu (CL-HK-11); ID hóa đơn (SC-HK-011) verify trên Liệt kê cước | Open | SC-HK-008, SC-HK-009, SC-HK-010, SC-HK-011, SC-HK-020 · REQ-HK-005, REQ-HK-006 |
| RISK-HK-02 | HK / dòng EVC + chiết khấu + thông tin mẫu | BR-HK-02 bắt chuẩn bị "dòng EVC" và "thông tin theo mẫu" nhưng không có rule ⇒ chưa có SC; nếu thiếu thì hóa đơn điện tử không được đẩy (BR-HK-02) — chặn cả luồng | High | DOC-v2.0-01 BR-HK-02 (L575), §D#6; GAP-04 (Blocker), GAP-35 | SC-HK-006, 007 (gián tiếp) | PM chốt Out-scope hoặc đặc tả (CL-HK-03, 04); TP đề xuất Out-scope | Open | SC-HK-006, SC-HK-007 · REQ-HK-004, REQ-HK-010 |
| RISK-HK-03 | HK / tiền trả trước | "Một lần mỗi đơn" nhưng không rõ đợt nào, số tiền nào, TB có add không⇒ add sai số tiền hoặc thiếu tiền DV phát hành sau | Medium | DOC-v2.0-01 BR-HK-09 (L596); GAP-59 | SC-HK-015, 016, 021 | Resolve CL-HK-07; đơn DV + TB phát hành nhiều đợt | Open | SC-HK-015, SC-HK-016, SC-HK-021 · REQ-HK-009 |
| RISK-HK-04 | HK / hệ thống ngoài | Hóa đơn điện tử, hệ thống Dịch vụ không sẵn trên STG; không có hành vi lỗi ⇒ không verify được "đã gen hóa đơn điện tử" / "đã add tiền" | Medium | TP §2.1b #24, #25; GAP-18, GAP-20 | SC-HK-006, 015, 018 | Mock/stub + xác nhận hành vi lỗi hóa đơn điện tử (CL-HK-05). Lỗi / timeout hệ thống Dịch vụ: **không test trên STG** — retry thủ công (CL-HK-06, SC-HK-019 deprecated 19/10/2026) | Open | SC-HK-006, SC-HK-015, SC-HK-018 · REQ-HK-001, REQ-HK-004, REQ-HK-009 |
| RISK-HK-05 | HK / đơn vị có đầu số riêng | Đơn vị có đầu số / dãy số / mẫu riêng (vd FPL, FMC) *"thuộc luồng nghiệp vụ cũ"* (URD 2.1 BR-HK-10) ⇒ **ngoài scope test** (CL-HK-02, QC owner 19/10/2026). Riêng dòng FPL trong bảng map ký hiệu vẫn test (SC-HK-009) | Low | DOC-v2.0-01 BR-HK-03 (L583), §D#5; DOC-v2.0-02 BR-HK-10 (L810-812); GAP-34 | — | Không test đơn vị đầu số riêng | Out-scope | REQ-HK-005 |

> Risk ID format: `RISK-<MODULE>-<NN>` (vd `RISK-PV-01`). Severity = High / Medium / Low (có thể Medium-High).
> **Solution:** biện pháp giảm thiểu hoặc hướng xử lý cụ thể (vd "resolve C-XXX trước generate-tc", "thêm negative TC cho MSG", "defer tới khi có env"). Chưa có → `—` (nhưng High/Medium nên có).
> **Status** — trạng thái xử lý rủi ro. Enum THUẦN (không kèm ghi chú trong ô — lý do để ở cột `Solution`):
> - `Open` = chưa xử lý / **đang bị chặn** (env/API/BA/backend chưa sẵn → chưa cover được).
> - `Pending` = **chấp nhận + defer có chủ đích** (không xử ở version này; vd NFR chờ môi trường thật / tải lớn).
> - `Resolved` = **đã xử lý và thêm test case cover** rủi ro (có `Solution` + TC/SC khả thi).
> - `Closed` = **bỏ khỏi scope** (feature loại khỏi version → rủi ro không còn áp dụng).
> KHÔNG để trống. Vòng đời: `Open` → `Resolved` (khi đã cover) · `Open` → `Pending` (defer) · `→ Closed` (bỏ scope).

## Khuyến nghị tổng thể
1. **Resolve blocker clarifications trước generate-tc** các scenario liên quan: CL-HK-03 (⛔ dòng EVC / chiết khấu), CL-HK-07 (tiền trả trước).
2. **Ưu tiên test P1 high-risk:** SC-HK-004, 006..008, 011..013, 015, 016.
3. **Performance / cần môi trường:** không có NFR; cần mock hóa đơn điện tử + hệ thống Dịch vụ (RISK-HK-04).
4. **ID/text cleanup (non-blocking, cần trước automation):** không có.

## Clarifications (home CL — layout v2)

> 1 CL = 1 heading `### CL-HK-NN · <câu hỏi ngắn>`. Dòng META mang `Status` (+ `⛔ BLOCKING`) và mã GAP. Khi resolved: **thêm** `✅ RESOLVED <ngày> — <kết luận>`, giữ phần phân tích cũ.

### CL-HK-01 · Ký hiệu hóa đơn điện tử bản chốt + bảng map; loại hóa đơn nào dùng đầu M / U / A (kể cả bán thêm)?
📍 `DOC-v2.0-01 BR-HK-03 (L581, L585)` + `§C#1 (L640-643)`  ·  Status: **Resolved 19/10/2026** · GAP-17 (Critical)

> Ký hiệu hóa đơn xác định theo quy định thuế; DVKH HO chốt với FAF.
> (...)
> Giữ nguyên, cần chốt ký hiệu (gộp BR-HK-04, 10)

**§C#1** — `L641-643`
> Ký hiệu hóa đơn điện tử.
> BR-HK-03
> Chốt theo quy định thuế; bảng map chuyển sang phụ lục.

↳ **Ghi chú:** SC-HK-008, 011, 020 chờ bảng chốt; SC-HK-009, 010 deprecated 16/10/2026. Chưa có bảng loại hóa đơn → loại đầu.

**Câu hỏi cho BA:** Gửi bản chốt ký hiệu + bảng map vùng × đầu; liệt kê loại hóa đơn (cước, bán mới, bán thêm, thiết bị…) dùng đầu nào.

🟡 **Làm rõ một phần 19/10/2026** — Phạm vi test v2.0: **chỉ loại hóa đơn bán mới, đầu U**; **không test đầu M** (và đầu A). Bảng map lấy theo URD 2.1 BR-HK-03 (CL-HK-10) ⇒ ký hiệu đầu U: V1 `QA` · V2 `EA` · V3 `GA` · V4 `MA` · V5 `QA` · V6 `OA` · V7 `YA` · FPL `PA`. Hết BLOCKING; SC-HK-008, 009, 010 hết chờ CL. Còn mở: hóa đơn của đơn **bán thêm** có tính là hóa đơn bán mới (đầu U) không (SC-HK-020). Nguồn: QC owner 19/10/2026.

✅ **RESOLVED 19/10/2026** — hóa đơn của đơn **bán thêm cũng dùng đầu U** (như bán mới) ⇒ SC-HK-020 hết chờ CL. Nguồn: QC owner 19/10/2026.

---

### CL-HK-02 · Đơn vị có đầu số / dãy số / mẫu riêng: trong hay ngoài phạm vi test?
📍 `DOC-v2.0-01 BR-HK-03 (L583)` + `§D#5 (L674-677)`  ·  Status: **Resolved 19/10/2026** · GAP-34 (Major)

> Bảng map vùng miền và các đơn vị có đầu số riêng xem tài liệu kỹ thuật.
> (...)
> Bảng map ký hiệu hóa đơn theo vùng miền; đơn vị có đầu số, dãy số, mẫu riêng.
> BR-HK-03, 04, 10
> DVKH HO chốt với FAF.

↳ **Ghi chú:** URD 2.2 chỉ nêu "đơn vị có đầu số, dãy số, mẫu riêng" ở D#5, không liệt kê đơn vị nào (CL-HK-10).

**Câu hỏi cho BA:** Đơn vị có đầu số riêng có thuộc phạm vi v2.0 không; nếu có thì danh sách + quy tắc.

✅ **RESOLVED 19/10/2026** — Theo `DOC-v2.0-02` BR-HK-10 (L810-812): đơn vị có đầu số / dãy số / mẫu riêng (vd FPL, FMC) *"thuộc luồng nghiệp vụ cũ"*, danh sách *"[NỢ]… PO không cần chốt nội dung này"* ⇒ **ngoài phạm vi test v2.0**. Riêng dòng **FPL** trong bảng map ký hiệu (BR-HK-03 L784) vẫn test — SC-HK-009. Nguồn: QC trả lời 19/10/2026 vòng 2 (dùng URD 2.1 cho Phụ lục D, QC owner chốt 19/10/2026).

---

### CL-HK-03 · Dòng EVC và dòng chiết khấu trên hóa đơn điện tử: Out-scope hay có đặc tả? ⛔ BLOCKING
📍 `DOC-v2.0-01 BR-HK-02 (L575)` + `§D#6 (L678-681)`  ·  Status: **Open — đã rõ một phần 19/10/2026** (đẩy hóa đơn điện tử) · GAP-04 (Blocker)

> INVOICE chuẩn bị đầy đủ các thông tin cần để tạo hóa đơn điện tử (ký hiệu, ID hóa đơn, nội dung hiển thị, dòng EVC, tổng tiền theo thuế suất, thông tin theo mẫu) rồi mới đẩy sang hệ thống HĐĐT.

↳ **Ghi chú:** BR-HK-02 bắt buộc có "dòng EVC" trước khi đẩy, nhưng không có rule. Mail PM "EVC cần test => theo rule URD" không làm rõ. TP đề xuất Out-scope (rủi ro TP #7). REQ-HK-010 chưa có SC.

**Câu hỏi cho BA:** Dòng EVC / chiết khấu trên hóa đơn điện tử có trong phạm vi test v2.0? Nếu có: loại EVC nào được thể hiện, format dòng.

🟡 **Làm rõ một phần 19/10/2026** — Theo `DOC-v2.0-02`: **dòng chiết khấu** chỉ có ở đơn đại lý FPT Play / Smart Home — BR-HK-06 L798 *"(hiện đi từ luồng đơn hàng không có)"* ⇒ **không test**. **Dòng EVC** (L725) *"Thêm DÒNG EVC trên hóa đơn nếu loại EVC đó thuộc nhóm được thể hiện"*; thông tin khác theo mẫu (BR-HK-08) chỉ có tên. Còn mở (**vẫn BLOCKING**, thu hẹp về dòng EVC): loại EVC nào thuộc nhóm được thể hiện + format dòng EVC. Nguồn: QC trả lời 19/10/2026 vòng 2 (dùng URD 2.1 cho Phụ lục D, QC owner chốt 19/10/2026).

---

### CL-HK-04 · Danh sách trường theo từng mẫu hóa đơn điện tử; mức thuế suất không phát sinh có in dòng 0?
📍 `DOC-v2.0-01 §D#6 (L679)` + `BR-HK-07 (L592)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-35 (Major)

> Dòng chiết khấu; thông tin khác theo mẫu hóa đơn.
> (...)
> Gom tổng tiền theo từng mức thuế suất (không chịu thuế, 0%, 5%, 8%, 10%), mỗi mức một dòng gồm thành tiền, thuế GTGT và tổng cộng; sau đó là dòng tổng cộng chung.

↳ **Ghi chú:** Không có mẫu ⇒ expected của SC-HK-006, 014 thiếu trường.

**Câu hỏi cho BA:** Gửi mẫu hóa đơn điện tử (trường bắt buộc); mức thuế không có dòng chi tiết thì có in không?

🟡 **Làm rõ một phần 19/10/2026** — Đã chốt: mức thuế suất không có dòng chi tiết thì **không in** — hóa đơn chỉ mua dịch vụ thuế 10% ⇒ chỉ in dòng 10% + dòng tổng cộng (không in dòng KCT / 0% / 5% / 8% giá trị 0). Còn mở: mẫu hóa đơn điện tử + danh sách trường bắt buộc theo mẫu (chặn expected SC-HK-006). Nguồn: QC trả lời 19/10/2026 vòng 2

---

### CL-HK-05 · Đẩy hóa đơn điện tử lỗi / chưa đủ thông tin: khi nào đẩy lại? Có đánh dấu / retry?
📍 `DOC-v2.0-01 BR-HK-02 · L576`  ·  Status: **Open** · GAP-18 (Critical)

> Chưa đủ thì chưa đẩy.

↳ **Ghi chú:** Không có trigger đẩy lại, không có hành vi lỗi. TP giả định "đẩy lại lần sau" (SC-HK-007, 018).

**Câu hỏi cho BA:** Khi chưa đủ thông tin hoặc hóa đơn điện tử lỗi: dòng được đánh dấu gì, ai / job nào đẩy lại, có cảnh báo?

---

### CL-HK-06 · Đẩy hệ thống Dịch vụ (tiền trả trước) lỗi: đánh dấu / retry?
📍 `DOC-v2.0-01 §III.a · L561`  ·  Status: **Resolved 19/10/2026** · GAP-20 (Critical)

> Thông tin dịch vụ và tiền dịch vụ được đẩy đúng theo từng đơn hàng cấu thành hóa đơn; đã add tiền trả trước cho khách.

↳ **Ghi chú:** Ảnh hưởng tính idempotent của BR-HK-09: lỗi rồi đẩy lại có bị tính là "đã add" không (SC-HK-019).

**Câu hỏi cho BA:** Lỗi thì đánh dấu gì, retry thế nào, bảo đảm vẫn chỉ add 1 lần ra sao?

✅ **RESOLVED 19/10/2026** — Lỗi đẩy hệ thống Dịch vụ: thực tế ghi log và **retry thủ công**; STG QC **không check log** ⇒ không dựng case lỗi / timeout. SC-HK-019 deprecated. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-HK-07 · Add tiền trả trước 1 lần / đơn nhiều đợt: đợt nào, số tiền nào, TB có add?
📍 `DOC-v2.0-01 BR-HK-09 (L596)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-59 (Major), GAP-60 (Major)

**URD 2.2** — `L596`
> Mỗi đơn chỉ add tiền trả trước một lần, kể cả khi đơn phát hành ở nhiều đợt hóa đơn.

↳ **Ghi chú:** "Mỗi đơn một lần" (per đơn), nhưng nếu DV phát hành ở 2 hóa đơn khác đợt thì DV thứ 2 có được add không? TP giả định: đợt đầu, toàn bộ tiền DV. Đơn bán thêm có add tiền trả trước như bán mới?

**Câu hỏi cho BA:** Tiền trả trước add ở hóa đơn nào, số tiền = tiền DV của hóa đơn đó hay của cả đơn; TB có add không; đơn bán thêm có khác không?

🟡 **Làm rõ một phần 19/10/2026** — hóa đơn mua dịch vụ trả trước được add tiền trả trước = **số tiền gói dịch vụ trả trước KH đã đăng ký**. Tra cứu: Quản lý kế toán › Cước trả trước › Tra cứu new. Còn mở: đơn phát hành nhiều đợt thì add ở hóa đơn nào (hóa đơn chỉ TB?), đơn bán thêm có khác không. Nguồn: QC trả lời 19/10/2026 vòng 2.

🟡 **Làm rõ thêm 19/10/2026 (vòng 3)** — **Mỗi đơn hàng chỉ add tiền trả trước 1 lần**, kể cả khi đơn phát hành nhiều đợt hóa đơn. Còn mở: add ở **hóa đơn** nào (hóa đơn đầu tiên của đơn — kể cả hóa đơn chỉ gồm thiết bị — hay hóa đơn có dịch vụ trả trước); đơn bán thêm có khác không. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-HK-08 · Mã tỉnh trong ID hóa đơn lấy theo đâu?
📍 `DOC-v2.0-01 BR-HK-03 (L582)`  ·  Status: **Resolved 19/10/2026** · *mới — 16/10/2026*

**URD 2.2** — `L582`
> ID hóa đơn ghép từ loại đầu + năm + mã tỉnh + số hóa đơn.

↳ **Ghi chú:** Không nói tỉnh của địa chỉ xuất hóa đơn, của hợp đồng, hay của chi nhánh quản lý hợp đồng (nay chi nhánh theo hợp đồng — BR-XHD-12 2.2). Vùng (để tra ký hiệu) cũng suy ra từ tỉnh nào?

**Câu hỏi cho BA:** Mã tỉnh (và vùng) lấy từ địa chỉ nào: địa chỉ xuất hóa đơn / địa chỉ hợp đồng / tỉnh của chi nhánh?

✅ **RESOLVED 19/10/2026** — Mã tỉnh lấy theo **địa chỉ hợp đồng**; QC tự backup danh mục mã để đối chiếu. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-HK-09 · Một hóa đơn có thể gồm nhiều đơn hàng không? ("tách theo từng đơn hàng cấu thành hóa đơn")
📍 `DOC-v2.0-01 BR-HK-01 (L571)` ↔ `BR-XHD-05 (L406)`  ·  Status: **Resolved 19/10/2026** · *mới — 16/10/2026*

**BR-HK-01** — `L571`
> Mỗi lần phát hành chỉ đẩy phần vừa xuất, tách theo từng đơn hàng cấu thành hóa đơn.

**BR-XHD-05** — `L406`
> Trong cùng một đợt, các dòng DV/TB đủ điều kiện của cùng một đơn gộp vào một hóa đơn.

↳ **Ghi chú:** XHD gộp theo đơn ⇒ 1 hóa đơn chỉ 1 đơn; HK lại nói "từng đơn hàng cấu thành hóa đơn". SC-HK-005 phụ thuộc câu trả lời.

**Câu hỏi cho BA:** Có trường hợp 1 hóa đơn gồm nhiều đơn ở v2.0 không? Nếu không, câu "tách theo từng đơn" chỉ áp cho hóa đơn luồng cũ?

🟡 **Làm rõ một phần 19/10/2026** — QC trả lời "1 **hợp đồng** có nhiều hóa đơn do có nhiều đơn hàng" — lệch câu hỏi. Còn mở: 1 **hóa đơn** có gồm nhiều **đơn hàng** không (SC-HK-005). Nguồn: QC trả lời 19/10/2026 vòng 2.

✅ **RESOLVED 19/10/2026 (vòng 3)** — **1 hóa đơn chỉ thuộc 1 đơn hàng** (không gồm nhiều đơn); 1 đơn hàng có 1 hoặc nhiều hóa đơn; 1 **hợp đồng** có nhiều đơn hàng. SC-HK-005 giữ (QC owner): hậu kỳ đẩy thông tin theo **đúng đơn hàng cấu thành hóa đơn**, không lẫn đơn khác cùng hợp đồng. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-HK-10 · Ký hiệu, ID hóa đơn điện tử, đơn vị đầu số riêng: URD 2.2 chuyển sang Phụ lục D#5, D#6 — chưa có đặc tả
📍 `DOC-v2.0-01 §D#5–#6 · L675-679`  ·  Status: **Resolved 19/10/2026** · *mới — 16/10/2026*

> Bảng map ký hiệu hóa đơn theo vùng miền; đơn vị có đầu số, dãy số, mẫu riêng.
> BR-HK-03, 04, 10
> DVKH HO chốt với FAF.
> (...)
> Dòng chiết khấu; thông tin khác theo mẫu hóa đơn.

↳ **Ghi chú:** Chưa có bảng map vùng × loại đầu, map loại hóa đơn → loại đầu, định dạng ID, quy ước mã tỉnh. SC-HK-009, 010 deprecated; SC-HK-008, 011, 020 chờ. Có thể trả lời chung với CL-HK-01 (BLOCKING) khi PO gửi bảng chốt.

**Câu hỏi cho BA:** Ngoài bảng map ký hiệu (CL-HK-01), cho QC định dạng ID hóa đơn điện tử: "năm" ghi 2 hay 4 chữ số, mã tỉnh theo danh mục nào, số hóa đơn có trùng số hóa đơn của Billing không; và danh sách đơn vị có đầu số / dãy số / mẫu riêng.

✅ **RESOLVED 19/10/2026** — Theo `DOC-v2.0-02` BR-HK-03 (L767-785) + BR-HK-04 (L787-792): ký hiệu 7 ký tự `1K<yy>T<xx>` (vd `1K26TQA`), `<xx>` tra **bảng map vùng × loại đầu** (7 vùng + FPL; Vùng 5 dùng chung Vùng 1; FPL không có đầu M). ID hóa đơn = loại đầu + **năm 2 chữ số** + **mã tỉnh theo danh mục tỉnh thành** (không phải mã chi nhánh; lấy theo địa chỉ hợp đồng — CL-HK-08) + số hóa đơn **trùng trường Số (Invoice No) trên hóa đơn điện tử** — vd `U26HN01053692`. Đơn vị đầu số riêng: ngoài phạm vi (CL-HK-02). Loại hóa đơn nào dùng đầu M / U / A vẫn ở **CL-HK-01**. Nguồn: QC trả lời 19/10/2026 vòng 2 (dùng URD 2.1 cho Phụ lục D, QC owner chốt 19/10/2026).

---

### CL-HK-11 · Ký hiệu hóa đơn điện tử verify ở đâu? Tool hóa đơn chỉ hiển thị ID hóa đơn
📍 `DOC-v2.0-01 BR-HK-03 (L581-582)` ↔ `07_environments/environments.md §Tool tra cứu`  ·  Status: **Open** · *mới — 19/10/2026, chưa có GAP*

> Ký hiệu hóa đơn xác định theo quy định thuế; DVKH HO chốt với FAF.
> ID hóa đơn ghép từ loại đầu + năm + mã tỉnh + số hóa đơn.

↳ **Ghi chú:** QC owner 19/10/2026: tool tra cứu hóa đơn (Quản lý kế toán › Liệt kê cước) **chỉ hiển thị ID hóa đơn**, không hiển thị ký hiệu hóa đơn điện tử (`1K<yy>T<xx>`) ⇒ SC-HK-008, 009, 010, 020 có expected nhưng **chưa có điểm verify**. ID hóa đơn (SC-HK-011) verify được trên tool này.

**Câu hỏi cho BA:** Ký hiệu hóa đơn điện tử (vd `1K26TQA`) QC kiểm tra ở đâu trên STG — màn / tool nào của hệ thống hóa đơn điện tử, file PDF / XML hóa đơn điện tử, portal tra cứu hóa đơn, hay dữ liệu đẩy sang hóa đơn điện tử? QC cần quyền gì để xem? Nếu STG không có hệ thống hóa đơn điện tử thật thì ký hiệu verify bằng cách nào?

