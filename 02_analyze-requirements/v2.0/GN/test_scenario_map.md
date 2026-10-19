---
id: v2.0/GN/test_scenario_map
title: Test Scenario Map — Module GN
type: test_scenario_map
version: v2.0
module: { code: GN, dir: GN, name: "Gạch nợ hóa đơn" }
counts:                 # 🔑 CANONICAL — REQ/SC/lifecycle/priority của module GN
  req: 20
  sc: 48
  new: 48
  modified: 0
  carried: 0
  deprecated: 2
  p1: 41
  p2: 6
  p3: 1
  blocked_by_cl: 3
status: ANALYZED
updated: 2026-10-19
---

# Test Scenario Map — v2.0 · Module GN

> **Home của SC quote** (1 quote = 1 nơi): Source Quote per SC ở §"Source Detail per Scenario" file này. REQ quote → `requirement_traceability.md §2`; Clarification quote → `risk_assessment.md` §Clarifications.

## Quy tắc đủ scenario (Scenario Sufficiency Rule)

> Nguyên tắc: **1 SC = 1 hành vi nguyên tử** (KHÔNG gộp nhiều hành vi vào 1 SC, KHÔNG đặt số N cứng cho mọi REQ).
>
> **Sàn tối thiểu / REQ:** ≥1 positive (happy path) + ≥1 negative (nếu REQ có validation/rule) + boundary (nếu có input range).
>
> **Fan-out theo chiều** — mỗi cái sau = 1 SC riêng: mỗi **role/quyền** · mỗi **state-transition** · mỗi **lớp EP** · mỗi **giá trị boundary** · mỗi **nhánh lỗi/MSG**. (Vd REQ 6-state → ~6 SC; REQ 2-role → ≥2-3 SC.)
>
> **Trần (KHÔNG sinh SC):** display-only / Phase-2 / duplicate — ghi vào `CHANGELOG.md §3` như gap có chủ đích, không tạo SC rác.

**Áp dụng cho GN:** fan-out theo **3 điểm chạm** · **paymentstatus** (tạm / hoàn tất) × **kênh** (sàn / không sàn) · **luồng** (Paid / Cọc) · biên **Paid vs nợ** (<, =, >) · biên **cọc vs nợ**. Dữ liệu kênh sàn = Shopee (20), Tiktok (21) theo giả định CL-GN-03.

## Tổng quan
- Tổng số scenarios: 48 (NEW: 48, MODIFIED: 0, CARRIED: 0) — số canonical ở frontmatter `counts:`.
- Phân bổ priority: xem frontmatter `counts:`.

## Scenarios — NEW & MODIFIED (chi tiết đầy đủ)

### GN — Gạch nợ hóa đơn

| Scenario ID | Feature | Req ID | DOC Source | Given | When | Then | Priority | Test Type | Lifecycle |
|-------------|---------|--------|-----------|-------|------|------|----------|-----------|-----------|
| SC-GN-001 | Đồng bộ Paid | REQ-GN-001 | DOC-v2.0-01 BR-DP-01 (L474) | Orderpaid của OrderCode X có 2 dòng thanh toán tiền khách | Kênh thanh toán đồng bộ sang INVOICE | 2 dòng Paid 1:1 theo OrderCode X, PaidType = tiền khách | P1 | Integration | NEW |
| SC-GN-002 | Đồng bộ Paid | REQ-GN-001 | DOC-v2.0-01 BR-DP-01 (L474) | Orderpaid có 1 dòng voucher + 1 dòng tiền khách | Đồng bộ | Cả 2 dòng được ghi Paid; mỗi dòng PaidType đúng nguồn tiền | P1 | Integration | NEW |
| SC-GN-003 | Chống trùng Paid | REQ-GN-002 | DOC-v2.0-01 BR-DP-01 (L475) | Đã có Paid (OrderCode, RefTransactionId, PaidType, Amount) với paymentstatus = tạm | Đồng bộ lại dòng **trùng đủ 4 trường**, paymentstatus = hoàn tất | Không thêm dòng; paymentstatus của dòng cũ cập nhật = hoàn tất | P1 | Functional | NEW |
| SC-GN-004 | Chống trùng Paid | REQ-GN-002 | DOC-v2.0-01 BR-DP-01 (L475) | Đã có Paid A | Đồng bộ dòng giống A nhưng **khác RefTransactionId** | Thêm Paid mới | P1 | Functional | NEW |
| SC-GN-005 | Chống trùng Paid | REQ-GN-002 | DOC-v2.0-01 BR-DP-01 (L475) | Đã có Paid A | Đồng bộ dòng giống A nhưng **khác PaidType** | Thêm Paid mới | P2 | Functional | NEW |
| SC-GN-006 | Chống trùng Paid | REQ-GN-002 | DOC-v2.0-01 BR-DP-01 (L475) | Đã có Paid A | Đồng bộ dòng giống A nhưng **khác Amount** | Thêm Paid mới | P2 | Functional | NEW |
| SC-GN-007 | Đồng bộ Paid | REQ-GN-003 | DOC-v2.0-01 BR-DP-01 (L476) | Đơn **chưa có HĐ** | Paid hoàn tất đồng bộ về | Paid vẫn được ghi; không gạch (không có nợ); khi HĐ phát hành, điểm chạm (b) nhặt Paid lên gạch | P1 | Integration | NEW |
| SC-GN-008 | Điểm chạm | REQ-GN-004 | DOC-v2.0-01 BR-XL-01 (L480) | HĐ còn nợ, luồng Paid | Paid hoàn tất **đồng bộ xong** — điểm chạm (a) | Xử lý gạch nợ được kích hoạt ngay | P1 | Functional | NEW |
| SC-GN-009 | Điểm chạm | REQ-GN-004 | DOC-v2.0-01 BR-XL-01 (L480) | Paid hoàn tất đã có từ trước | HĐ **vừa phát hành** (Invoice Event) — điểm chạm (b) | Xử lý gạch nợ được kích hoạt sau khi xuất HĐ | P1 | Integration | NEW |
| SC-GN-010 | Điểm chạm | REQ-GN-004 | DOC-v2.0-01 BR-XL-01 (L480) | HĐ còn nợ, Paid đủ điều kiện nhưng lần xét trước bị dừng (vd API lỗi) | **Worker 30 phút** chạy — điểm chạm (c) | Gạch nợ được xử lý ở lần quét kế tiếp; chu kỳ 30 phút | P1 | Functional | NEW |
| SC-GN-011 | Lọc điểm chạm (a) | REQ-GN-005 | DOC-v2.0-01 BR-XL-01 (L482) | Đơn kênh **sàn** | Paid **tạm** đồng bộ xong | Đi tiếp xử lý nợ (dẫn tới gạch nợ tạm) | P1 | Functional | NEW |
| SC-GN-012 | Lọc điểm chạm (a) | REQ-GN-005 | DOC-v2.0-01 BR-XL-01 (L482) | Đơn kênh **không sàn** (vd quầy) | Paid **tạm** đồng bộ xong | **Dừng** ngay, không lấy nợ, không gọi API | P1 | Negative | NEW |
| SC-GN-013 | Lọc điểm chạm (a) | REQ-GN-005 | DOC-v2.0-01 BR-XL-01 (L482) | Đơn kênh bất kỳ | Paid **hoàn tất** đồng bộ xong | Đi tiếp xử lý nợ (gạch nợ thật) | P1 | Functional | NEW |
| SC-GN-014 | Lấy nợ | REQ-GN-006 | DOC-v2.0-01 BR-XL-03 (L486) | HĐ **đã hết nợ** | Một điểm chạm kích hoạt | Dừng, không ghi Payment, chờ điểm chạm sau | P1 | Negative | NEW |
| SC-GN-015 | Phương thức gạch | REQ-GN-007 | DOC-v2.0-01 BR-XL-03 (L487) | Trường Paid/Cọc trên OrderBill **đã có** giá trị | Điểm chạm kích hoạt | Dùng giá trị có sẵn; **không** gọi API kênh thanh toán | P1 | Functional | NEW |
| SC-GN-016 | Phương thức gạch | REQ-GN-007 | DOC-v2.0-01 BR-XL-03 (L487) | Trường Paid/Cọc **chưa có** | Điểm chạm kích hoạt | Gọi API kênh thanh toán; giá trị lưu vào OrderBill; lần sau không gọi lại | P1 | Integration | NEW |
| SC-GN-017 | Phương thức gạch | REQ-GN-007 | DOC-v2.0-01 BR-XL-03 (L488) | Trường chưa có; API kênh thanh toán **lỗi / timeout** (mock) | Điểm chạm kích hoạt | Dừng, không gạch, **không retry** trong lần đó; điểm chạm sau gọi lại | P1 | Negative | NEW |
| SC-GN-018 | Phân luồng Paid / Cọc | REQ-GN-008 | DOC-v2.0-01 BR-XL-03 (L489) | 2 HĐ: trường = "Paid" và trường = "Cọc" | Điểm chạm kích hoạt | HĐ "Paid" đi luồng Paid; HĐ "Cọc" đi luồng Cọc; mỗi đơn chỉ một luồng | P1 | Functional | NEW |
| SC-GN-019 | Gạch nợ tạm | REQ-GN-009, REQ-GN-010 | DOC-v2.0-01 BR-NT-01 (L493), BR-NT-02 (L498-499) | Đơn kênh sàn (Shopee/Tiktok), HĐ còn nợ N, luồng Paid | Paid ở trạng thái **tạm** | Ghi 1 Payment phương thức **đặc biệt** = N (toàn bộ nợ còn lại); HĐ chuyển "Đã gạch nợ" | P1 | Functional | NEW |
| SC-GN-020 | Gạch nợ tạm | REQ-GN-009 | DOC-v2.0-01 BR-NT-01 (L494) | Đơn kênh **không sàn**, HĐ còn nợ, Paid tạm | Điểm chạm (b) hoặc (c) kích hoạt (không qua bộ lọc a) | **Không** gạch nợ tạm; HĐ vẫn còn nợ, chờ Paid hoàn tất | P1 | Negative | NEW |
| SC-GN-021 | Gạch nợ tạm | REQ-GN-008 | DOC-v2.0-01 BR-XL-03 (L489) | HĐ luồng **Cọc**, đơn kênh sàn, Paid tạm | Điểm chạm kích hoạt | Không có gạch nợ tạm ở nhánh Cọc | P1 | Negative | NEW |
| SC-GN-022 | Gỡ gạch nợ tạm | REQ-GN-011 | DOC-v2.0-01 BR-NT-04 (L503) | HĐ đã gạch nợ tạm (Payment đặc biệt) | Paid chuyển **hoàn tất** | Payment tạm bị gỡ trước (HĐ trở lại còn nợ), sau đó gạch nợ thật bằng Paid | P1 | Functional | NEW |
| SC-GN-023 | Gỡ gạch nợ tạm | REQ-GN-011 | DOC-v2.0-01 BR-NT-04 (L504) | HĐ **chưa** gạch nợ tạm | Paid hoàn tất | Gạch nợ thật luôn, không có bước gỡ | P1 | Functional | NEW |
| SC-GN-024 | Gỡ gạch nợ tạm | REQ-GN-011 | DOC-v2.0-01 BR-NT-04 (L503) | HĐ đã gạch tạm nợ N | Paid hoàn tất với Amount **< N** | Gỡ tạm; gạch thật = Amount; HĐ kết thúc ở "còn nợ" (N − Amount) — hệ quả ⛔ chờ CL-GN-06 | P2 | Boundary | NEW |
| SC-GN-025 | Điều kiện Paid | REQ-GN-012 | DOC-v2.0-01 BR-GN-01 (L508) | HĐ còn nợ; Paid cùng OrderCode Amount = **0** và Paid Amount = **1** | Gạch nợ chạy | **Amount 0 không được dùng; Amount 1 được dùng** | P1 | Boundary | NEW |
| SC-GN-026 | Điều kiện Paid | REQ-GN-012 | DOC-v2.0-01 BR-GN-01 (L508) | HĐ của OrderCode X; Paid thuộc OrderCode **Y** | Gạch nợ chạy | Paid của Y không được dùng cho HĐ của X | P1 | Negative | NEW |
| SC-GN-027 | Điều kiện Paid | REQ-GN-012 | DOC-v2.0-01 BR-GN-01 (L509) | HĐ **đã gạch đủ** | Điểm chạm kích hoạt lại (worker 30 phút) | Không gạch lần nữa; không có Payment trùng | P1 | Negative | NEW |
| SC-GN-028 | Thứ tự bill | REQ-GN-013 | DOC-v2.0-01 BR-GN-03 (L513) | Đơn có 3 bill 300k / 500k / 100k, luồng Paid, Paid 600k | Gạch nợ chạy | Thứ tự gạch 500k → 300k (gạch 100k) → 100k (chưa gạch); bill 500k hết nợ | P1 | Functional | NEW |
| SC-GN-029 | Thứ tự bill | REQ-GN-013 | DOC-v2.0-01 BR-GN-03 (L514) | Đơn có ≥2 bill, luồng **Cọc** | Gạch nợ chạy | Bill được xét từ cao xuống thấp | P1 | Functional | NEW |
| SC-GN-030 | Thứ tự bill | REQ-GN-013 | DOC-v2.0-01 BR-GN-03 (L513) | 2 bill **bằng tiền nhau**, Paid chỉ đủ 1 bill | Gạch nợ chạy | Thứ tự — QC: ưu tiên BillNumber cao nhất ⛔ chờ BA xác nhận chỉ là tie-break (CL-GN-09) | P3 | Boundary | NEW |
| SC-GN-031 | Gạch từng phần | REQ-GN-014 | DOC-v2.0-01 BR-GN-04 (L518-519) | HĐ nợ 500k; Paid 300k | Gạch nợ chạy | Gạch 300k; HĐ còn nợ 200k; Paid còn 0; dừng vì hết Paid | P1 | Boundary | NEW |
| SC-GN-032 | Gạch từng phần | REQ-GN-014 | DOC-v2.0-01 BR-GN-04 (L518-519) | HĐ nợ 300k; Paid 500k | Gạch nợ chạy | Gạch 300k; HĐ hết nợ; **Paid dư 200k được giữ** | P1 | Boundary | NEW |
| SC-GN-033 | Gạch từng phần | REQ-GN-014, REQ-GN-015 | DOC-v2.0-01 BR-GN-04 (L518) | HĐ nợ 500k; Paid 500k | Gạch nợ chạy | Gạch 500k; HĐ "Đã gạch nợ"; Paid còn 0 | P1 | Boundary | NEW |
| SC-GN-034 | Gạch từng phần | REQ-GN-014 | DOC-v2.0-01 BR-GN-04 (L518) | Luồng Paid, HĐ còn nợ | Một lần gạch thực hiện | 3 đầu ra: dòng Payment ghi nhận · Paid bị trừ đúng số tiền · Kafka Out đẩy về kênh thanh toán | P1 | Integration | NEW |
| SC-GN-035 | Gạch từng phần | REQ-GN-014 | DOC-v2.0-01 BR-GN-04 (L520) | Luồng **Cọc**, HĐ còn nợ, đủ cọc | Gạch cọc thực hiện | Payment ghi; cọc bị trừ; **không** có Kafka Out | P1 | Negative | NEW |
| SC-GN-036 | Trạng thái | REQ-GN-015 | DOC-v2.0-01 BR-GN-05 (L524) | HĐ tổng T | Σ Payment = **T − 1** rồi = **T** | **T − 1: chưa "Đã gạch nợ"; T: "Đã gạch nợ"** | P1 | Boundary | NEW |
| SC-GN-037 | Cọc — đủ tiền | REQ-GN-016 | DOC-v2.0-01 BR-GC-01 (L529) | Bill nợ 1.000k; cọc HĐ 700k + EVC đơn 300k (gồm lock 100k) | Gạch cọc xét bill | Tổng = nợ ⇒ **đủ tiền** (biên "không nhỏ hơn"), đi tiếp kiểm cọc theo loại | P1 | Boundary | NEW |
| SC-GN-038 | Cọc — đủ tiền | REQ-GN-016 | DOC-v2.0-01 BR-GC-01 (L529) | Bill nợ 1.000k; cọc + EVC = 999k | Gạch cọc xét bill | **Không** gạch bill | P1 | Negative | NEW |
| SC-GN-039 | Cọc — theo loại | REQ-GN-017 | DOC-v2.0-01 BR-GC-02 (L534) | Bill có DV dùng loại cọc A và B; cọc HĐ đủ cả A và B | Gạch cọc | Bill được gạch | P1 | Functional | NEW |
| SC-GN-040 | Cọc — theo loại | REQ-GN-017 | DOC-v2.0-01 BR-GC-02 (L535) | Bill dùng loại A và B; cọc loại B **thiếu** (dù tổng cọc đủ) | Gạch cọc | **Không gạch cả bill**, không gạch một phần loại A | P1 | Negative | NEW |
| SC-GN-041 | Cọc — theo loại | REQ-GN-017 | DOC-v2.0-01 BR-GC-02 (L535) | Đơn 2 bill: bill 1 thiếu cọc loại B, bill 2 chỉ dùng loại A đủ | Gạch cọc | Bill 1 không gạch; bill 2 **vẫn** được gạch | P1 | Functional | NEW |
| SC-GN-042 | Cọc — cách trừ | REQ-GN-018 | DOC-v2.0-01 BR-GC-03 (L539) | Bill có 2 DV cùng loại cọc A + 1 DV loại cọc B | Gạch cọc | 2 dòng Payment (1 cho loại A gom 2 DV, 1 cho loại B); mỗi DV trừ đúng loại cọc | P1 | Functional | NEW |
| SC-GN-043 | Cọc — cách trừ | REQ-GN-018 | DOC-v2.0-01 BR-GC-03 (L540) | Bill nợ 1.000k, đội EVC đã gạch 200k | Gạch cọc | Trừ cọc trên **800k** còn lại; Payment + trừ cọc ghi theo BillNumber + số hợp đồng | P1 | Functional | NEW |
| SC-GN-044 | Cọc — cách trừ | REQ-GN-018 | DOC-v2.0-01 BR-GC-03 (L541) | Cọc HĐ dư sau khi gạch; HĐ đã gạch bằng cọc | Điểm chạm kích hoạt lại | Cọc dư giữ nguyên, không xử lý; HĐ không bị gạch lại | P2 | Negative | NEW |
| SC-GN-045 | EVC | REQ-GN-019 | DOC-v2.0-01 BR-VC (L545) | Đơn có EVC (không lock), luồng Paid | Gạch nợ chạy | INVOICE **không** ghi Payment cho phần EVC; chỉ gạch tiền khách trên phần nợ còn lại | P1 | Negative | NEW |
| SC-GN-046 | EVC lock | REQ-GN-020 | DOC-v2.0-01 BR-VC (L546) | Bill nợ 1.000k; EVC lock 300k; Paid khách 900k | Gạch tiền khách | Gạch = min(1.000k − 300k, 900k) = **700k**; Paid khách dư 200k giữ lại; phần 300k chừa ra | P1 | Functional | NEW |
| SC-GN-047 | EVC lock | REQ-GN-020 | DOC-v2.0-01 BR-VC (L546) | Bill nợ 1.000k; lock **0**; Paid khách 500k / 1.000k | Gạch tiền khách | **Lock 0 ⇒ gạch như thường: 500k / 1.000k** | P2 | Boundary | NEW |
| SC-GN-050 | Bán thêm | REQ-GN-016, REQ-GN-018 | DOC-v2.0-04 mail PM ↔ DOC-v2.0-01 BR-GC-01 (L529) | Đơn **bán thêm** trên hợp đồng đang có cọc dư từ đơn trước, luồng Cọc | Gạch cọc | Dùng cọc còn lại của **hợp đồng** (không theo OrderCode) — điểm khác (nếu có) ⛔ chờ CL-GN-07 (CL-XHD-25 đã chốt: rule chung) | P2 | Functional | NEW |

#### Source Detail per Scenario (verbatim quotes — `references/quoting-guide.md`)

> Given/When/Then đã ở bảng trên — block dưới không lặp, chỉ giữ quote justify + ghi chú dẫn xuất. Số tiền trong G/W/T là dữ liệu minh họa của analyst.

##### SC-GN-001 · Paid 1:1 theo OrderCode
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L474`

> Paid đồng bộ 1:1 từ Orderpaid theo OrderCode

↳ **Ghi chú:** Nhiều đợt thanh toán = nhiều dòng detail trong 1 Orderpaid.

---

##### SC-GN-002 · Đồng bộ cả voucher
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L474`

> gồm cả voucher và tiền khách thanh toán; mỗi Paid gán PaidType theo nguồn tiền.

↳ **Ghi chú:** Enum PaidType chưa có (CL-XHD-29).

---

##### SC-GN-003 · Trùng đủ 4 trường
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L475`

> Trùng khi giống cả 4 trường OrderCode + RefTransactionId + PaidType + Amount: trùng thì cập nhật paymentstatus

↳ **Ghi chú:** Đây cũng là đường Paid "tạm → hoàn tất" của kênh sàn.

---

##### SC-GN-004 · Khác RefTransactionId
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L475`

> không trùng thì thêm mới.

↳ **Ghi chú:** EP — khác 1/4 trường.

---

##### SC-GN-005 · Khác PaidType
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L475`

> Trùng khi giống cả 4 trường OrderCode + RefTransactionId + PaidType + Amount

↳ **Ghi chú:** EP — khác 1/4 trường.

---

##### SC-GN-006 · Khác Amount
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L475`

> Trùng khi giống cả 4 trường OrderCode + RefTransactionId + PaidType + Amount

↳ **Ghi chú:** EP — khác 1/4 trường.

---

##### SC-GN-007 · Paid về trước HĐ
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L476`

> Đồng bộ Paid là luồng độc lập với gạch nợ và luôn ghi nhận Paid kể cả khi hóa đơn chưa phát hành.

↳ **Ghi chú:** SC E2E nối với SC-GN-009.

---

##### SC-GN-008 · Điểm chạm (a)
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L480`

> (a) đồng bộ Paid xong

↳ **Ghi chú:** Trigger 1/3.

---

##### SC-GN-009 · Điểm chạm (b)
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L480`

> (b) sau khi xuất hóa đơn

↳ **Ghi chú:** Trigger 2/3 — nối từ SC-XHD-103.

---

##### SC-GN-010 · Điểm chạm (c)
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L480`

> (c) worker quét 30 phút một lần.

↳ **Ghi chú:** Trigger 3/3 — cũng là đường phục hồi sau API lỗi (SC-GN-017).

---

##### SC-GN-011 · Lọc (a) — Paid tạm + kênh sàn
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L482`

> Ở điểm chạm (a), chỉ xử lý tiếp khi Paid ở trạng thái gạch nợ tạm và đơn thuộc kênh sàn

↳ **Ghi chú:** Lớp đi tiếp 1/2.

---

##### SC-GN-012 · Lọc (a) — Paid tạm + kênh không sàn
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L482`

> Ở điểm chạm (a), chỉ xử lý tiếp khi Paid ở trạng thái gạch nợ tạm và đơn thuộc kênh sàn, hoặc Paid đã thanh toán hoàn tất.

↳ **Ghi chú:** Lớp dừng — kiểm không gọi API (mock đếm số lần gọi).

---

##### SC-GN-013 · Lọc (a) — Paid hoàn tất
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L482`

> hoặc Paid đã thanh toán hoàn tất.

↳ **Ghi chú:** Lớp đi tiếp 2/2.

---

##### SC-GN-014 · Không có nợ
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L486`

> không có nợ thì dừng, chờ điểm chạm sau.

↳ **Ghi chú:** Negative.

---

##### SC-GN-015 · Trường Paid/Cọc có sẵn
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L487`

> Trường đã có giá trị thì dùng luôn

↳ **Ghi chú:** Verify bằng log/mock: 0 lần gọi API.

---

##### SC-GN-016 · Trường Paid/Cọc chưa có
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L487`

> chưa có thì gọi API kênh thanh toán rồi lưu vào OrderBill.

↳ **Ghi chú:** Lần xét sau rơi vào SC-GN-015.

---

##### SC-GN-017 · API lỗi / timeout
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L488`

> API lỗi hoặc timeout thì dừng, không retry trong cùng lần.

↳ **Ghi chú:** Cần mock API kênh thanh toán (TP §2.1b #23).

---

##### SC-GN-018 · Một đơn một luồng
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L489`

> Một đơn chỉ đi một luồng: Paid (có gạch nợ tạm) hoặc Cọc (không có gạch nợ tạm).

↳ **Ghi chú:** 2 lớp EP luồng.

---

##### SC-GN-019 · Gạch nợ tạm kênh sàn
📍 `DOC-v2.0-01 §II.c BR-NT-02 · L498-499`

> Ghi Payment bằng phương thức thanh toán đặc biệt, số tiền bằng toàn bộ nợ còn lại.
> Khoản này tính vào tổng Payment nên hóa đơn chuyển sang "Đã gạch nợ" ngay.

↳ **Ghi chú:** Chạy với dữ liệu Shopee và Tiktok. Nửa XHD ở SC-XHD-029.

---

##### SC-GN-020 · Không gạch tạm kênh khác
📍 `DOC-v2.0-01 §II.c BR-NT-01 · L494`

> Kênh khác như tại quầy, tại nơi triển khai: không gạch nợ tạm, chờ Paid thanh toán hoàn tất rồi gạch nợ thật.

↳ **Ghi chú:** Đi qua điểm chạm (b)/(c) để chứng minh kênh vẫn được xét trong luồng.

---

##### SC-GN-021 · Nhánh Cọc không gạch tạm
📍 `DOC-v2.0-01 §II.c BR-XL-03 · L489`

> Cọc (không có gạch nợ tạm).

↳ **Ghi chú:** Negative.

---

##### SC-GN-022 · Gỡ tạm rồi gạch thật
📍 `DOC-v2.0-01 §II.c BR-NT-04 · L503`

> Khi Paid chuyển sang thanh toán hoàn tất, nếu hóa đơn đã gạch nợ tạm thì gỡ Payment tạm trước (hóa đơn trở lại còn nợ) rồi mới gạch nợ thật.

↳ **Ghi chú:** State transition Đã gạch nợ (tạm) → còn nợ → Đã gạch nợ (thật).

---

##### SC-GN-023 · Chưa gạch tạm → gạch thật luôn
📍 `DOC-v2.0-01 §II.c BR-NT-04 · L504`

> Chưa gạch tạm thì gạch thật luôn.

↳ **Ghi chú:** Không phát sinh thao tác gỡ.

---

##### SC-GN-024 · Paid hoàn tất nhỏ hơn nợ đã gạch tạm
📍 `DOC-v2.0-01 §II.c BR-NT-04 · L503`

> (hóa đơn trở lại còn nợ) rồi mới gạch nợ thật.

↳ **Ghi chú:** Ca sàn quyết toán thiếu (phí sàn?) — kết quả cuối "còn nợ" có hệ quả gì: CL-GN-06.

---

##### SC-GN-025 · Biên Amount > 0
📍 `DOC-v2.0-01 §II.c BR-GN-01 · L508`

> Chỉ lấy dòng Paid có Amount > 0

↳ **Ghi chú:** BVA 0 / 1 (Amount âm cùng lớp với 0).

---

##### SC-GN-026 · Khác OrderCode
📍 `DOC-v2.0-01 §II.c BR-GN-01 · L508`

> và cùng OrderCode với hóa đơn.

↳ **Ghi chú:** Negative.

---

##### SC-GN-027 · Không gạch lại bill đã hết nợ
📍 `DOC-v2.0-01 §II.c BR-GN-01 · L509`

> Chỉ gạch bill còn nợ; mỗi bill chỉ gạch một lần.

↳ **Ghi chú:** Idempotent qua điểm chạm (c) lặp.

---

##### SC-GN-028 · Thứ tự cao → thấp (Paid)
📍 `DOC-v2.0-01 §II.c BR-GN-03 · L513`

> Một đơn có 1..n bill; gạch từng bill, theo số tiền từ cao xuống thấp.

↳ **Ghi chú:** Paid không đủ cho tất cả bill để thấy rõ thứ tự.

---

##### SC-GN-029 · Thứ tự cao → thấp (Cọc)
📍 `DOC-v2.0-01 §II.c BR-GN-03 · L514`

> Áp dụng cho cả nhánh Paid và nhánh Cọc.

↳ **Ghi chú:** Cọc chỉ đủ cho bill lớn để thấy thứ tự.

---

##### SC-GN-030 · Bill bằng tiền nhau
📍 `DOC-v2.0-01 §II.c BR-GN-03 · L513`

> theo số tiền từ cao xuống thấp.

↳ **Ghi chú:** Tie-break không định nghĩa (CL-GN-09) — P3.

---

##### SC-GN-031 · Paid < nợ
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L518-519`

> Mỗi lần gạch = nhỏ nhất của số dư Paid và nợ còn lại
> Dừng khi hết nợ hoặc hết Paid

↳ **Ghi chú:** Biên dưới.

---

##### SC-GN-032 · Paid > nợ
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L519`

> Paid dư được giữ lại.

↳ **Ghi chú:** Biên trên.

---

##### SC-GN-033 · Paid = nợ
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L518`

> Mỗi lần gạch = nhỏ nhất của số dư Paid và nợ còn lại

↳ **Ghi chú:** Biên bằng.

---

##### SC-GN-034 · 3 đầu ra của một lần gạch Paid
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L518`

> ghi Payment, trừ Paid, đẩy Kafka Out về kênh thanh toán.

↳ **Ghi chú:** Payload Kafka Out chờ CL-XHD-29.

---

##### SC-GN-035 · Nhánh Cọc không Kafka Out
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L520`

> Nhánh Cọc không đẩy Kafka Out.

↳ **Ghi chú:** Negative.

---

##### SC-GN-036 · Biên "Đã gạch nợ"
📍 `DOC-v2.0-01 §II.c BR-GN-05 · L524`

> Khi tổng Payment bằng tổng tiền hóa đơn thì hóa đơn chuyển sang "Đã gạch nợ".

↳ **Ghi chú:** BVA T − 1 / T.

---

##### SC-GN-037 · Đủ tiền — biên bằng
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529`

> Tổng cọc còn lại của hợp đồng (mọi loại cọc) cộng tổng tiền EVC của đơn (tính cả phần bị lock) phải không nhỏ hơn nợ của bill đang xét.

↳ **Ghi chú:** Lock tính vào điều kiện đủ tiền nhưng không được gạch.

---

##### SC-GN-038 · Không đủ tiền
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529`

> phải không nhỏ hơn nợ của bill đang xét.

↳ **Ghi chú:** Biên −1.

---

##### SC-GN-039 · Đủ cọc mọi loại
📍 `DOC-v2.0-01 §II.c BR-GC-02 · L534`

> Cọc của hợp đồng theo từng loại phải đủ cho các dịch vụ dùng loại cọc đó trên bill.

↳ **Ghi chú:** Positive.

---

##### SC-GN-040 · Thiếu một loại cọc
📍 `DOC-v2.0-01 §II.c BR-GC-02 · L535`

> Thiếu ở một loại thì không gạch cả bill đó, không gạch một phần

↳ **Ghi chú:** Tổng cọc đủ nhưng 1 loại thiếu — phân biệt với SC-GN-038.

---

##### SC-GN-041 · Bill khác vẫn xét
📍 `DOC-v2.0-01 §II.c BR-GC-02 · L535`

> các bill khác của đơn vẫn xét bình thường.

↳ **Ghi chú:** Bill lớn fail không chặn bill nhỏ.

---

##### SC-GN-042 · Gom Payment theo loại cọc
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L539`

> Mỗi dịch vụ trừ đúng loại cọc của nó; nhiều dịch vụ cùng loại cọc gom thành một dòng Payment.

↳ **Ghi chú:** Số dòng Payment = số loại cọc.

---

##### SC-GN-043 · Trừ cọc sau EVC
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L540`

> Tính trên nợ còn lại sau khi EVC đã gạch; ghi Payment và trừ cọc theo BillNumber + số hợp đồng.

↳ **Ghi chú:** Cần đội EVC (hoặc mock) gạch trước.

---

##### SC-GN-044 · Dư cọc, không gạch lại
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L541`

> Dư cọc không xử lý; không gạch lại hóa đơn đã gạch.

↳ **Ghi chú:** Negative.

---

##### SC-GN-045 · INVOICE không gạch EVC
📍 `DOC-v2.0-01 §II.c BR-VC · L545`

> Phần gạch nợ bằng EVC do đội EVC thực hiện; ISC tự quyết phương thức quản trị và xử lý voucher.

↳ **Ghi chú:** Ranh giới phạm vi (TP §2.2 #5).

---

##### SC-GN-046 · Chừa phần lock
📍 `DOC-v2.0-01 §II.c BR-VC · L546`

> số gạch = nhỏ nhất của (nợ bill trừ tiền lock) và Paid khách thanh toán.

↳ **Ghi chú:** Hiện chỉ EVC Loyalty FTEL có lock.

---

##### SC-GN-047 · Lock = 0
📍 `DOC-v2.0-01 §II.c BR-VC · L546`

> Với EVC bị lock (khách chưa ký hợp đồng), INVOICE chừa phần lock khi gạch tiền khách

↳ **Ghi chú:** Biên 0 — công thức suy biến về BR-GN-04.

---

##### SC-GN-050 · Đơn bán thêm dùng cọc hợp đồng
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529` + `DOC-v2.0-04 mail PM`

> Tổng cọc còn lại của hợp đồng (mọi loại cọc)
> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** Cọc tính theo hợp đồng nên đơn bán thêm dùng chung cọc với đơn trước — suy diễn từ chữ "của hợp đồng".

## Scenarios — CARRIED (reference only)

| Scenario ID | Tên ngắn | Module | Origin Version | Priority | Reference |
|-------------|----------|--------|---------------|----------|-----------|
| — | *(v2.0 là version đầu tiên trong workspace — chưa có CARRIED)* | — | — | — | — |

## Scenarios — DEPRECATED

| Scenario ID | Tên ngắn | Module | Deprecated ở | Lý do |
|-------------|----------|--------|-------------|-------|
| SC-GN-048 | Paid voucher dùng gạch nợ | GN | v2.0 (19/10/2026) | TP §2.2 #5: gạch nợ bằng EVC / voucher ngoài phạm vi (CL-GN-01 Out-scope) |
| SC-GN-049 | API EVC lỗi / timeout | GN | v2.0 (19/10/2026) | CL-GN-02: STG không test timeout; thực tế đội dự án retry thủ công, API lỗi ⇒ log bug |
