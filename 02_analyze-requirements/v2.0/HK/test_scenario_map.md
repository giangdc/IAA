---
id: v2.0/HK/test_scenario_map
title: Test Scenario Map — Module HK
type: test_scenario_map
version: v2.0
module: { code: HK, dir: HK, name: "Đẩy hậu kỳ qua dịch vụ – tiền trả trước" }
counts:                 # 🔑 CANONICAL — REQ/SC/lifecycle/priority của module HK
  req: 10
  sc: 20
  new: 20
  modified: 0
  carried: 0
  deprecated: 1
  p1: 12
  p2: 8
  p3: 0
  blocked_by_cl: 7
status: ANALYZED
updated: 2026-10-19
---

# Test Scenario Map — v2.0 · Module HK

> **Home của SC quote** (1 quote = 1 nơi): Source Quote per SC ở §"Source Detail per Scenario" file này. REQ quote → `requirement_traceability.md §2`; Clarification quote → `risk_assessment.md` §Clarifications.

## Quy tắc đủ scenario (Scenario Sufficiency Rule)

> Nguyên tắc: **1 SC = 1 hành vi nguyên tử** (KHÔNG gộp nhiều hành vi vào 1 SC, KHÔNG đặt số N cứng cho mọi REQ).
>
> **Sàn tối thiểu / REQ:** ≥1 positive (happy path) + ≥1 negative (nếu REQ có validation/rule) + boundary (nếu có input range).
>
> **Fan-out theo chiều** — mỗi cái sau = 1 SC riêng: mỗi **role/quyền** · mỗi **state-transition** · mỗi **lớp EP** · mỗi **giá trị boundary** · mỗi **nhánh lỗi/MSG**. (Vd REQ 6-state → ~6 SC; REQ 2-role → ≥2-3 SC.)
>
> **Trần (KHÔNG sinh SC):** display-only / Phase-2 / duplicate — ghi vào `CHANGELOG.md §3` như gap có chủ đích, không tạo SC rác.

**Áp dụng cho HK:** fan-out theo **thành phần hóa đơn** (DV / TB) · **số lần phát hành** của đơn · **vùng × đầu U** ký hiệu (bảng map URD 2.1; chỉ test đầu U — CL-HK-01) · **mức thuế suất** (5 lớp). REQ-HK-010 không sinh SC.

## Tổng quan
- Tổng số scenarios: 20 (NEW: 20, MODIFIED: 0, CARRIED: 0) — số canonical ở frontmatter `counts:`.
- Phân bổ priority: xem frontmatter `counts:`.

## Scenarios — NEW & MODIFIED (chi tiết đầy đủ)

### HK — Đẩy hậu kỳ qua dịch vụ – tiền trả trước

| Scenario ID | Feature | Req ID | DOC Source | Given | When | Then | Priority | Test Type | Lifecycle |
|-------------|---------|--------|-----------|-------|------|------|----------|-----------|-----------|
| SC-HK-001 | Kích hoạt hậu kỳ | REQ-HK-001 | DOC-v2.0-01 §III.a (L553) | Hóa đơn có DV vừa phát hành thành công | INVOICE nhận Invoice Event | Cả 2 nhánh chạy: chuẩn bị + đẩy hóa đơn điện tử **và** đẩy tiền trả trước sang hệ thống Dịch vụ | P1 | Integration | NEW |
| SC-HK-002 | Phạm vi đẩy | REQ-HK-002 | DOC-v2.0-01 BR-HK-01 (L570) | Hóa đơn chỉ gồm dòng **DV** | Hậu kỳ chạy | Dữ liệu đẩy hóa đơn điện tử gồm đúng các dòng DV của hóa đơn | P1 | Functional | NEW |
| SC-HK-003 | Phạm vi đẩy | REQ-HK-002 | DOC-v2.0-01 BR-HK-01 (L570) | Hóa đơn chỉ gồm dòng **TB** | Hậu kỳ chạy | Dữ liệu đẩy hóa đơn điện tử gồm đúng các dòng TB (không bỏ TB) | P1 | Functional | NEW |
| SC-HK-004 | Phạm vi đẩy | REQ-HK-003 | DOC-v2.0-01 BR-HK-01 (L571) | Đơn đã phát hành hóa đơn 1 (DV) và đã đẩy hậu kỳ | Hóa đơn 2 (TB) phát hành | Hậu kỳ của hóa đơn 2 **chỉ** gồm phần TB vừa xuất; phần DV không bị đẩy lại | P1 | Functional | NEW |
| SC-HK-005 | Phạm vi đẩy | REQ-HK-003 | DOC-v2.0-01 BR-HK-01 (L571) | **Hợp đồng** có ≥2 đơn hàng, mỗi đơn có **hóa đơn** riêng (1 hóa đơn chỉ thuộc 1 đơn hàng — CL-HK-09) | Hậu kỳ chạy | Thông tin đẩy hậu kỳ của mỗi hóa đơn chỉ gồm dữ liệu của **đơn hàng cấu thành hóa đơn đó**, không lẫn đơn khác cùng hợp đồng (CL-HK-09, 19/10/2026) | P2 | Functional | NEW |
| SC-HK-006 | Đẩy hóa đơn điện tử | REQ-HK-004 | DOC-v2.0-01 BR-HK-02 (L575) | Hóa đơn đủ thông tin (ký hiệu, ID, nội dung, tổng tiền theo thuế suất, …) | Hậu kỳ chạy | Dữ liệu được đẩy sang hệ thống hóa đơn điện tử; hóa đơn điện tử được gen | P1 | Integration | NEW |
| SC-HK-007 | Đẩy hóa đơn điện tử | REQ-HK-004 | DOC-v2.0-01 BR-HK-02 (L576) | Hóa đơn **thiếu** 1 thông tin (vd vùng của tỉnh không có trong bảng map ⇒ không ra ký hiệu) | Hậu kỳ chạy | **Chưa** đẩy sang hóa đơn điện tử; thời điểm đẩy lại ⛔ chờ CL-HK-05 | P1 | Negative | NEW |
| SC-HK-008 | Ký hiệu hóa đơn | REQ-HK-005 | DOC-v2.0-01 BR-HK-03 (L581) ↔ DOC-v2.0-02 BR-HK-03 (L767-785) | Hóa đơn **bán mới** (đầu U) thuộc vùng V | Chuẩn bị ký hiệu | Ký hiệu 7 ký tự `1K<yy>T<xx>`, `<xx>` theo đầu U: V1 `QA` · V2 `EA` · V3 `GA` · V4 `MA` · V6 `OA` · V7 `YA` (vd `1K26TQA`) — chỉ test đầu U (CL-HK-01) — điểm verify ký hiệu ⛔ chờ CL-HK-11 | P1 | Functional | NEW |
| SC-HK-009 | Ký hiệu hóa đơn | REQ-HK-005 | DOC-v2.0-02 BR-HK-03 (L784) | Hóa đơn bán mới (đầu U) đơn vị **FPL** | Chuẩn bị ký hiệu | Hai ký tự cuối = `PA` (đầu U của FPL) — điểm verify ký hiệu ⛔ chờ CL-HK-11 | P2 | Functional | NEW |
| SC-HK-010 | Ký hiệu hóa đơn | REQ-HK-005 | DOC-v2.0-02 BR-HK-03 (L781) | Hóa đơn bán mới (đầu U) thuộc **Vùng 5** | Chuẩn bị ký hiệu | Dùng chung Vùng 1: hai ký tự cuối = `QA` — điểm verify ký hiệu ⛔ chờ CL-HK-11 | P2 | Functional | NEW |
| SC-HK-011 | ID hóa đơn | REQ-HK-006 | DOC-v2.0-01 BR-HK-03 (L582) ↔ DOC-v2.0-02 BR-HK-04 (L787-792) | Hóa đơn loại đầu U, năm 2026, hợp đồng địa chỉ Hà Nội, số hóa đơn 01053692 | Chuẩn bị ID | ID = `U26HN01053692` (loại đầu + năm 2 số + mã tỉnh theo **địa chỉ hợp đồng** + số hóa đơn); số hóa đơn trùng trường Số (Invoice No) trên hóa đơn điện tử | P1 | Functional | NEW |
| SC-HK-012 | Nội dung hiển thị | REQ-HK-007 | DOC-v2.0-01 BR-HK-05 (L588) | Dòng DV có số tháng sử dụng trên SPF | Chuẩn bị nội dung | Nội dung = tên dịch vụ + số tháng; không có "từ ngày – đến ngày"; không lấy nguyên tên gốc trên đơn | P1 | Functional | NEW |
| SC-HK-013 | Tổng tiền theo thuế suất | REQ-HK-008 | DOC-v2.0-01 BR-HK-07 (L592) | Hóa đơn có dòng ở đủ 5 mức: KCT, 0%, 5%, 8%, 10% | Chuẩn bị tổng tiền | 5 dòng (thành tiền, thuế GTGT, tổng cộng mỗi mức) + 1 dòng tổng cộng chung = tổng các mức | P1 | Functional | NEW |
| SC-HK-014 | Tổng tiền theo thuế suất | REQ-HK-008 | DOC-v2.0-01 BR-HK-07 (L592) | Hóa đơn chỉ có dòng **một** mức (10%) | Chuẩn bị tổng tiền | Chỉ in 1 dòng mức 10% + dòng tổng cộng chung; **không** in dòng KCT / 0% / 5% / 8% (CL-HK-04, 19/10/2026) | P2 | Boundary | NEW |
| SC-HK-015 | Tiền trả trước | REQ-HK-009 | DOC-v2.0-01 BR-HK-09 (L596) | Đơn phát hành hóa đơn lần đầu | Nhánh tiền trả trước chạy | Hệ thống Dịch vụ nhận lệnh add tiền trả trước cho đơn; đơn được đánh dấu đã add | P1 | Integration | NEW |
| SC-HK-016 | Tiền trả trước | REQ-HK-009 | DOC-v2.0-01 BR-HK-09 (L596) | Đơn đã add tiền trả trước ở hóa đơn 1 | Hóa đơn 2 của cùng đơn phát hành | **Không** add tiền trả trước lần 2 | P1 | Negative | NEW |
| SC-HK-017 | Tiền trả trước | REQ-HK-009 | DOC-v2.0-01 BR-HK-09 (L596) | Đơn đã add tiền trả trước | Invoice Event của cùng hóa đơn bị gửi lặp | Không add lại (idempotent) | P2 | Negative | NEW |
| SC-HK-018 | Đẩy hóa đơn điện tử | REQ-HK-004 | DOC-v2.0-01 BR-HK-02 (L575) | Hệ thống hóa đơn điện tử lỗi / timeout (mock) | Đẩy hóa đơn điện tử | (giả định TP: đẩy lại lần sau) — ⛔ chờ CL-HK-05 | P2 | Negative | NEW |
| SC-HK-020 | Ký hiệu hóa đơn | REQ-HK-005 | DOC-v2.0-01 BR-HK-03 (L581) ↔ DOC-v2.0-04 | Hóa đơn của đơn **bán thêm** | Chuẩn bị ký hiệu | Dùng **đầu U** như hóa đơn bán mới — hai ký tự cuối theo vùng (vd Vùng 1 `QA`) (CL-HK-01, 19/10/2026) — điểm verify ký hiệu ⛔ chờ CL-HK-11 | P2 | Functional | NEW |
| SC-HK-021 | Tiền trả trước | REQ-HK-009 | DOC-v2.0-01 BR-HK-09 (L596) | Đơn có **hóa đơn** đầu tiên chỉ gồm thiết bị (hóa đơn dịch vụ phát hành sau) | Hóa đơn TB phát hành | Tiền trả trước chỉ add **1 lần cho mỗi đơn hàng** (CL-HK-07); add ở hóa đơn thiết bị này hay hóa đơn dịch vụ sau ⛔ chờ CL-HK-07 | P2 | Functional | NEW |

#### Source Detail per Scenario (verbatim quotes — `references/quoting-guide.md`)

> Given/When/Then đã ở bảng trên — block dưới không lặp, chỉ giữ quote justify + ghi chú dẫn xuất.

##### SC-HK-001 · Hai nhánh song song
📍 `DOC-v2.0-01 §III.a · L553`

> Sau khi nhận Invoice Event, hai nhánh chạy song song.

↳ **Ghi chú:** Nối từ SC-XHD-103.

---

##### SC-HK-002 · Hóa đơn chỉ DV
📍 `DOC-v2.0-01 §III.c BR-HK-01 · L570`

> Phần nào trên đơn đã xuất hóa đơn thì đẩy hậu kỳ đúng phần đó

↳ **Ghi chú:** Lớp EP DV.

---

##### SC-HK-003 · Hóa đơn chỉ TB
📍 `DOC-v2.0-01 §III.c BR-HK-01 · L570`

> không phân biệt dịch vụ hay thiết bị.

↳ **Ghi chú:** Lớp EP TB.

---

##### SC-HK-004 · Lần phát hành sau chỉ đẩy phần mới
📍 `DOC-v2.0-01 §III.c BR-HK-01 · L571`

> Mỗi lần phát hành chỉ đẩy phần vừa xuất

↳ **Ghi chú:** Nối với SC-XHD-105 (1 đơn n hóa đơn).

---

##### SC-HK-005 · Tách theo từng đơn
📍 `DOC-v2.0-01 §III.c BR-HK-01 · L571`

> tách theo từng đơn hàng cấu thành hóa đơn.

↳ **Ghi chú:** 1 hóa đơn chỉ thuộc 1 đơn hàng; 1 hợp đồng có nhiều đơn hàng (CL-HK-09 resolved 19/10/2026) ⇒ verify thông tin đẩy của mỗi hóa đơn không lẫn đơn khác cùng hợp đồng.

---

##### SC-HK-006 · Đủ thông tin → đẩy
📍 `DOC-v2.0-01 §III.c BR-HK-02 · L575`

> INVOICE chuẩn bị đầy đủ các thông tin cần để tạo hóa đơn điện tử (ký hiệu, ID hóa đơn, nội dung hiển thị, dòng EVC, tổng tiền theo thuế suất, thông tin theo mẫu) rồi mới đẩy sang hệ thống HĐĐT.

↳ **Ghi chú:** Positive E2E.

---

##### SC-HK-007 · Thiếu thông tin → chưa đẩy
📍 `DOC-v2.0-01 §III.c BR-HK-02 · L576`

> Chưa đủ thì chưa đẩy.

↳ **Ghi chú:** Cách làm thiếu thông tin trên STG là suy diễn của analyst (tỉnh không có vùng).

---

##### SC-HK-008 · Ký hiệu theo vùng × loại đầu
📍 `DOC-v2.0-02 §III.c BR-HK-03 · L767-785`

> QA — hai ký tự do người bán tự xác định, LẤY TỪ BẢNG MAP VÙNG MIỀN theo tổ hợp (vùng, loại đầu).

↳ **Ghi chú:** Bảng map lấy từ URD 2.1 (2.2 chuyển Phụ lục D#5) — dùng lại 19/10/2026 (CL-HK-10). Dữ liệu ở `test_data_catalog.md`. Phạm vi v2.0 chỉ hóa đơn bán mới đầu U (CL-HK-01, 19/10/2026).
---

##### SC-HK-009 · FPL đầu U
📍 `DOC-v2.0-02 §III.c BR-HK-03 · L784`

> FPL: Đầu U = PA · Đầu A = PH (không có Đầu M)

↳ **Ghi chú:** Dòng FPL của bảng map vẫn test (CL-HK-02: đơn vị đầu số riêng khác ngoài phạm vi). Chỉ test đầu U; "không có đầu M" không test (CL-HK-01, 19/10/2026).

---

##### SC-HK-010 · Vùng 5 dùng chung Vùng 1
📍 `DOC-v2.0-02 §III.c BR-HK-03 · L781`

> Vùng 5: Đầu M = HT · Đầu U = QA · Đầu A = HH (dùng chung đầu số với Vùng 1)

↳ **Ghi chú:** Ca đặc biệt của bảng map.

---

##### SC-HK-011 · ID hóa đơn
📍 `DOC-v2.0-01 §III.c BR-HK-03 · L582` + `DOC-v2.0-02 BR-HK-04 · L788`

> ID hóa đơn được ghép từ bốn thành phần. Ví dụ U26HN01053692:

↳ **Ghi chú:** Định dạng từ URD 2.1 BR-HK-04 (CL-HK-10); mã tỉnh theo địa chỉ hợp đồng (CL-HK-08).
---

##### SC-HK-012 · Nội dung hiển thị
📍 `DOC-v2.0-01 §III.c BR-HK-05 · L588`

> Hiển thị tên dịch vụ + số tháng sử dụng (lấy từ SPF); không hiển thị kỳ hạn từ ngày – đến ngày và không dùng bảng map.

↳ **Ghi chú:** Kiểm trên payload đẩy hóa đơn điện tử.

---

##### SC-HK-013 · Đủ 5 mức thuế suất
📍 `DOC-v2.0-01 §III.c BR-HK-07 · L592`

> Gom tổng tiền theo từng mức thuế suất (không chịu thuế, 0%, 5%, 8%, 10%), mỗi mức một dòng gồm thành tiền, thuế GTGT và tổng cộng; sau đó là dòng tổng cộng chung.

↳ **Ghi chú:** Đối chiếu khối "Cộng / Thuế suất GTGT / Tổng cộng" của màn `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png).

---

##### SC-HK-014 · Chỉ một mức thuế suất
📍 `DOC-v2.0-01 §III.c BR-HK-07 · L592`

> mỗi mức một dòng gồm thành tiền, thuế GTGT và tổng cộng

↳ **Ghi chú:** Biên tối thiểu. Mức không phát sinh thì không in dòng — QC trả lời CL-HK-04 19/10/2026 (URD không ghi).

---

##### SC-HK-015 · Add tiền trả trước lần đầu
📍 `DOC-v2.0-01 §III.c BR-HK-09 · L596`

> Mỗi đơn chỉ add tiền trả trước một lần

↳ **Ghi chú:** Positive.

---

##### SC-HK-016 · Không add lần 2 khi nhiều đợt
📍 `DOC-v2.0-01 §III.c BR-HK-09 · L596`

> kể cả khi đơn phát hành ở nhiều đợt hóa đơn.

↳ **Ghi chú:** Negative.

---

##### SC-HK-017 · Invoice Event lặp
📍 `DOC-v2.0-01 §III.c BR-HK-09 · L596`

> Mỗi đơn chỉ add tiền trả trước một lần

↳ **Ghi chú:** Idempotent khi bản tin lặp.

---

##### SC-HK-018 · Hóa đơn điện tử lỗi
📍 `DOC-v2.0-01 §III.c BR-HK-02 · L575`

> rồi mới đẩy sang hệ thống HĐĐT.

↳ **Ghi chú:** Không có nhánh lỗi (CL-HK-05).

---

##### SC-HK-020 · Ký hiệu hóa đơn bán thêm
📍 `DOC-v2.0-01 §III.c BR-HK-03 · L581`

> Ký hiệu hóa đơn xác định theo quy định thuế; DVKH HO chốt với FAF.

↳ **Ghi chú:** Phạm vi gồm đơn bán thêm (`DOC-v2.0-04`); hóa đơn bán thêm dùng **đầu U** như hóa đơn bán mới (CL-HK-01 đã đóng 19/10/2026).

---

##### SC-HK-021 · Hóa đơn đầu chỉ có TB
📍 `DOC-v2.0-01 §III.c BR-HK-09 · L596`

> Mỗi đơn chỉ add tiền trả trước một lần, kể cả khi đơn phát hành ở nhiều đợt hóa đơn.

↳ **Ghi chú:** Nếu add ở hóa đơn đầu (chỉ TB) thì số tiền DV chưa có — CL-HK-07.

## Scenarios — CARRIED (reference only)

| Scenario ID | Tên ngắn | Module | Origin Version | Priority | Reference |
|-------------|----------|--------|---------------|----------|-----------|
| — | *(v2.0 là version đầu tiên trong workspace — chưa có CARRIED)* | — | — | — | — |

## Scenarios — DEPRECATED

| Scenario ID | Tên ngắn | Module | Deprecated ở | Lý do |
|-------------|----------|--------|-------------|-------|
| SC-HK-019 | Hệ thống Dịch vụ lỗi / timeout | HK | v2.0 (19/10/2026) | CL-HK-06: thực tế retry thủ công, STG QC không check log ⇒ không dựng case lỗi |
