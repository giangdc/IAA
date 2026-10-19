---
id: v2.0/HK/requirement_traceability
title: Requirement Traceability — Module HK
type: requirement_traceability
version: v2.0
module: { code: HK, dir: HK, name: "Đẩy hậu kỳ qua dịch vụ – tiền trả trước" }
doc_source:
  - id: DOC-v2.0-01
    section: "§A.5 #12 · §B.III · §C#1 · §D#5, #6"
status: ANALYZED
updated: 2026-10-19
---

# Requirement Traceability — v2.0 · Module HK

> Tạo bởi: analyze-requirements. Ma trận truy vết REQ ↔ DOC ↔ Scenario ↔ Clarification.
> **Layout v2** — quote REQ ở **§2** file này; quote SC ở `test_scenario_map.md`; CL ở `risk_assessment.md`.
> `req_notation: BR` ⇒ **Schema A**. `L<n>` = số dòng bản trích text `.docx` (`scripts/doc/search-doc.sh`).

## 1. Traceability Matrix (REQ → DOC → SC)

### Schema A — Module HK — DOC-v2.0-01

| REQ ID | Maps (Ref DOC) | DOC §section | Scenarios | Clarification |
|--------|----------------|--------------|-----------|---------------|
| REQ-HK-001 | — | DOC-v2.0-01 §III.a (L552-561) | SC-HK-001 | CL-HK-05, CL-HK-06 |
| REQ-HK-002 | BR-HK-01 | DOC-v2.0-01 §III.c (L570) | SC-HK-002, SC-HK-003 | — |
| REQ-HK-003 | BR-HK-01 | DOC-v2.0-01 §III.c (L571) | SC-HK-004, SC-HK-005 | CL-HK-09 |
| REQ-HK-004 | BR-HK-02 | DOC-v2.0-01 §III.c (L575-577) | SC-HK-006, SC-HK-007, SC-HK-018 | CL-HK-03, CL-HK-04, CL-HK-05 |
| REQ-HK-005 | BR-HK-03 | DOC-v2.0-01 §III.c (L581, L583-584) | SC-HK-008, SC-HK-009, SC-HK-010, SC-HK-020 | CL-HK-01, CL-HK-02, CL-HK-10 |
| REQ-HK-006 | BR-HK-03 | DOC-v2.0-01 §III.c (L582) | SC-HK-011 | CL-HK-08 |
| REQ-HK-007 | BR-HK-05 | DOC-v2.0-01 §III.c (L588) | SC-HK-012 | — |
| REQ-HK-008 | BR-HK-07 | DOC-v2.0-01 §III.c (L592) | SC-HK-013, SC-HK-014 | — |
| REQ-HK-009 | BR-HK-09 | DOC-v2.0-01 §III.c (L596) | SC-HK-015, SC-HK-016, SC-HK-017, SC-HK-021 | CL-HK-06, CL-HK-07 |
| REQ-HK-010 | BR-HK-02 | DOC-v2.0-01 §III.c (L575) + §D#6 (L678-681) | — *(chờ đặc tả — CHANGELOG §3)* | CL-HK-03, CL-HK-04 |

> `§III.c` = mục B.III "Đẩy hậu kỳ qua dịch vụ – tiền trả trước" → c. Business rules.
> REQ-HK-010 (dòng EVC, dòng chiết khấu, thông tin theo mẫu) **chưa có SC có chủ đích**: chỉ được nhắc tên, đặc tả chuyển phụ lục D#6 — nợ ở `CHANGELOG.md §3`.

## 2. Requirement Source Detail (verbatim quotes — home của REQ quote)

### REQ-HK-001 · Sau Invoice Event, hai nhánh hậu kỳ chạy song song: HĐĐT và tiền trả trước
📍 `DOC-v2.0-01 §III.a "Mô tả" · L552-561`  ·  Clarif: `CL-HK-05`, `CL-HK-06`

> Điều chỉnh cách đẩy thông tin hậu kỳ (tạo hóa đơn điện tử, add tiền trả trước) khi một đơn có thể có nhiều hóa đơn.
> Sau khi nhận Invoice Event, hai nhánh chạy song song.
> (...)
> Thông tin dịch vụ và tiền dịch vụ được đẩy đúng theo từng đơn hàng cấu thành hóa đơn; đã add tiền trả trước cho khách.

↳ **Ghi chú:** Trigger = Invoice Event của XHD (REQ-XHD-037). Actor: INVOICE, hệ thống HĐĐT, hệ thống Dịch vụ (L555). Hai nhánh độc lập ⇒ một nhánh lỗi không chặn nhánh kia — **suy diễn của analyst**, URD không có hành vi lỗi (CL-HK-05, 06).

---

### REQ-HK-002 · Đẩy hậu kỳ đúng phần đã xuất HĐ, không phân biệt DV hay TB
📍 `DOC-v2.0-01 §III.c BR-HK-01 · L570`  ·  Clarif: —

> Phần nào trên đơn đã xuất hóa đơn thì đẩy hậu kỳ đúng phần đó, không phân biệt dịch vụ hay thiết bị.

↳ **Ghi chú:** Lớp EP: HĐ chỉ DV · HĐ chỉ TB · HĐ DV + TB.

---

### REQ-HK-003 · Mỗi lần phát hành chỉ đẩy phần vừa xuất, tách theo từng đơn cấu thành HĐ
📍 `DOC-v2.0-01 §III.c BR-HK-01 · L571`  ·  Clarif: `CL-HK-09`

> Mỗi lần phát hành chỉ đẩy phần vừa xuất, tách theo từng đơn hàng cấu thành hóa đơn.

↳ **Ghi chú:** Với 1 đơn n HĐ (REQ-XHD-038) mỗi HĐ đẩy hậu kỳ riêng, không đẩy lại phần cũ. "Từng đơn hàng cấu thành hóa đơn": 1 hóa đơn chỉ thuộc 1 đơn hàng, 1 hợp đồng có nhiều đơn hàng (CL-HK-09 resolved 19/10/2026).

---

### REQ-HK-004 · Chuẩn bị đủ thông tin rồi mới đẩy HĐĐT; chưa đủ thì chưa đẩy
📍 `DOC-v2.0-01 §III.c BR-HK-02 · L575-577`  ·  Clarif: `CL-HK-03`, `CL-HK-04`, `CL-HK-05`

> INVOICE chuẩn bị đầy đủ các thông tin cần để tạo hóa đơn điện tử (ký hiệu, ID hóa đơn, nội dung hiển thị, dòng EVC, tổng tiền theo thuế suất, thông tin theo mẫu) rồi mới đẩy sang hệ thống HĐĐT.
> Chưa đủ thì chưa đẩy.
> Hệ thống HĐĐT không truy vấn ngược dữ liệu đơn hàng.

↳ **Ghi chú:** 6 nhóm thông tin; 3 nhóm có rule ở 2.2 (ký hiệu + ID — REQ-HK-005, 006; nội dung — REQ-HK-007; tổng tiền — REQ-HK-008), 2 nhóm (dòng EVC, thông tin theo mẫu) chỉ có tên (REQ-HK-010). "Chưa đủ thì chưa đẩy" ⇒ khi nào đẩy lại? URD không nói (CL-HK-05).

---

### REQ-HK-005 · Ký hiệu HĐ điện tử theo quy định thuế; đầu số sai là sai kê khai
📍 `DOC-v2.0-01 §III.c BR-HK-03 · L581, L583-584`  ·  Clarif: `CL-HK-01`, `CL-HK-02`

**URD 2.2** — `DOC-v2.0-01 L581, L583-584`
> Ký hiệu hóa đơn xác định theo quy định thuế; DVKH HO chốt với FAF.
> (...)
> Bảng map vùng miền và các đơn vị có đầu số riêng xem tài liệu kỹ thuật.
> Đầu số sai là sai kê khai thuế, không chỉ lỗi hiển thị.

↳ **Ghi chú:** 2.2 ghi "cần chốt ký hiệu" (cột So với v2.1, L585) + §C#1. Từ 19/10/2026: bảng map vùng × loại đầu lấy theo URD 2.1 BR-HK-03 (CL-HK-10); **chỉ test đầu U** cho HĐ bán mới và bán thêm, không test đầu M (CL-HK-01); đơn vị có đầu số riêng **ngoài scope test** (CL-HK-02), riêng dòng FPL của bảng map vẫn test. Điểm kiểm ký hiệu trên STG chờ CL-HK-11. Severity cao: sai là sai kê khai thuế.

---

### REQ-HK-006 · ID HĐ = loại đầu + năm + mã tỉnh + số HĐ
📍 `DOC-v2.0-01 §III.c BR-HK-03 · L582`  ·  Clarif: `CL-HK-08`

> ID hóa đơn ghép từ loại đầu + năm + mã tỉnh + số hóa đơn.

↳ **Ghi chú:** Định dạng theo URD 2.1 BR-HK-04 (CL-HK-10, 19/10/2026): năm 2 chữ số, mã tỉnh theo danh mục tỉnh thành, số HĐ = trường Số trên HĐĐT; mã tỉnh lấy theo địa chỉ hợp đồng (CL-HK-08).

---

### REQ-HK-007 · Nội dung hiển thị: tên dịch vụ + số tháng (SPF); không kỳ hạn từ – đến; không dùng bảng map
📍 `DOC-v2.0-01 §III.c BR-HK-05 · L588`  ·  Clarif: —

> Hiển thị tên dịch vụ + số tháng sử dụng (lấy từ SPF); không hiển thị kỳ hạn từ ngày – đến ngày và không dùng bảng map.

↳ **Ghi chú:** Kiểm trên dữ liệu đẩy sang HĐĐT (khác XHD REQ-XHD-036 kiểm trên HĐ Billing). "Không dùng bảng map" — nội dung dựng từ tên dịch vụ + số tháng.

---

### REQ-HK-008 · Gom tổng tiền theo từng mức thuế suất (KCT, 0%, 5%, 8%, 10%) + dòng tổng cộng chung
📍 `DOC-v2.0-01 §III.c BR-HK-07 · L592`  ·  Clarif: —

> Gom tổng tiền theo từng mức thuế suất (không chịu thuế, 0%, 5%, 8%, 10%), mỗi mức một dòng gồm thành tiền, thuế GTGT và tổng cộng; sau đó là dòng tổng cộng chung.

↳ **Ghi chú:** EP 5 mức thuế suất. Mức không có dòng chi tiết thì **không in** — QC trả lời CL-HK-04 19/10/2026 (khớp suy diễn trước đó).

---

### REQ-HK-009 · Mỗi đơn chỉ add tiền trả trước một lần, kể cả phát hành nhiều đợt
📍 `DOC-v2.0-01 §III.c BR-HK-09 · L596`  ·  Clarif: `CL-HK-06`, `CL-HK-07`

> Mỗi đơn chỉ add tiền trả trước một lần, kể cả khi đơn phát hành ở nhiều đợt hóa đơn.

↳ **Ghi chú:** "Mỗi đơn một lần" (per đơn), nhưng add ở đợt nào, số tiền nào, TB có add không: chưa rõ (CL-HK-07 / GAP-59). Đẩy Dịch vụ lỗi: CL-HK-06.

---

### REQ-HK-010 · Dòng EVC, dòng chiết khấu, thông tin theo mẫu trên HĐĐT
📍 `DOC-v2.0-01 §III.c BR-HK-02 · L575` + `§D#6 · L678-681`  ·  Clarif: `CL-HK-03`, `CL-HK-04`

**BR-HK-02 — chỉ nhắc tên** — `L575`
> (ký hiệu, ID hóa đơn, nội dung hiển thị, dòng EVC, tổng tiền theo thuế suất, thông tin theo mẫu)

**Phụ lục D#6** — `L679-681`
> Dòng chiết khấu; thông tin khác theo mẫu hóa đơn.
> BR-HK-06, 08
> Kỹ thuật.

↳ **Ghi chú:** Không có rule nào ở URD 2.2 (D#6 chuyển phụ lục). TP: F21 "Chờ bổ sung", đề xuất Out-scope (GAP-04, Blocker). **Chưa sinh SC.**

---

> **Quy ước:** Implicit REQ → *(Implicit — không có quote trực tiếp)* + derivation ở Ghi chú. Quote >500 ký tự → sidecar `v2.0/quotes/`.
> **Clarification quote KHÔNG ở đây** — `HK/risk_assessment.md` §Clarifications. **SC quote** ở `test_scenario_map.md`.
