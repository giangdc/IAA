---
id: v2.0/GN/test_scenario_map
title: Test Scenario Map — Module GN
type: test_scenario_map
version: v2.0
module: { code: GN, dir: GN, name: "Gạch nợ hóa đơn" }
counts:                 # 🔑 CANONICAL — REQ/SC/lifecycle/priority của module GN
  req: 20
  sc: 54
  new: 54
  modified: 0
  carried: 0
  deprecated: 21
  p1: 34
  p2: 19
  p3: 1
  blocked_by_cl: 0
status: ANALYZED
updated: 2026-10-21
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
- Tổng số scenarios: 54 active (NEW: 54, MODIFIED: 0, CARRIED: 0) · 21 deprecated — số canonical ở frontmatter `counts:`.
- Phân bổ priority: xem frontmatter `counts:`.

## Scenarios — NEW & MODIFIED (chi tiết đầy đủ)

### GN — Gạch nợ hóa đơn

| Scenario ID | Feature | Req ID | DOC Source | Given | When | Then | Priority | Test Type | Lifecycle |
|-------------|---------|--------|-----------|-------|------|------|----------|-----------|-----------|
| SC-GN-003 | Chống trùng Paid | REQ-GN-002 | DOC-v2.0-01 BR-DP-01 (L475) | Đơn sàn đã có Paid tạm, hóa đơn đã gạch nợ tạm | Sàn quyết toán ⇒ Paid **trùng đủ 4 trường**, paymentstatus = hoàn tất | Hóa đơn có đúng 1 Payment gạch thật bằng tổng nợ, không gạch 2 lần (dòng Paid không bị nhân đôi). QC kiểm qua hóa đơn — bảng Paid QC không check (dev tự kiểm, QC owner 21/10/2026) | P1 | Functional | NEW |
| SC-GN-007 | Đồng bộ Paid | REQ-GN-003 | DOC-v2.0-01 BR-DP-01 (L476) | Đơn **chưa có hóa đơn** | Paid đồng bộ về trước khi hóa đơn phát hành | Khi hóa đơn phát hành, điểm chạm (b) dùng Paid đã ghi để gạch (có Payment). Bản thân dòng Paid QC không check (dev tự kiểm) | P1 | Integration | NEW |
| SC-GN-008 | Điểm chạm | REQ-GN-004 | DOC-v2.0-01 BR-XL-01 (L480) | Hóa đơn còn nợ, luồng Paid | Paid hoàn tất **đồng bộ xong** — điểm chạm (a) | Xử lý gạch nợ được kích hoạt ngay | P1 | Functional | NEW |
| SC-GN-009 | Điểm chạm | REQ-GN-004 | DOC-v2.0-01 BR-XL-01 (L480) | Paid hoàn tất đã có từ trước | Hóa đơn **vừa phát hành** (Invoice Event) — điểm chạm (b) | Xử lý gạch nợ được kích hoạt sau khi xuất hóa đơn | P1 | Integration | NEW |
| SC-GN-010 | Điểm chạm | REQ-GN-004 | DOC-v2.0-01 BR-XL-01 (L480) | Hóa đơn còn nợ, Paid đủ điều kiện nhưng lần xét trước bị dừng (vd API lỗi) | **Worker 30 phút** chạy — điểm chạm (c) | Gạch nợ được xử lý ở lần quét kế tiếp; chu kỳ 30 phút | P1 | Functional | NEW |
| SC-GN-011 | Lọc điểm chạm (a) | REQ-GN-005 | DOC-v2.0-01 BR-XL-01 (L482) | Đơn kênh **sàn** | Paid **tạm** đồng bộ xong | Đi tiếp xử lý nợ (dẫn tới gạch nợ tạm) | P1 | Functional | NEW |
| SC-GN-013 | Lọc điểm chạm (a) | REQ-GN-005 | DOC-v2.0-01 BR-XL-01 (L482) | Đơn kênh **sàn** (Paid chỉ có ở luồng sàn — QC owner 21/10/2026) | Paid **hoàn tất** đồng bộ xong | Đi tiếp xử lý nợ (gạch nợ thật) | P1 | Functional | NEW |
| SC-GN-014 | Lấy nợ | REQ-GN-006 | DOC-v2.0-01 BR-XL-03 (L486) | Hóa đơn **đã hết nợ** | Một điểm chạm kích hoạt | Dừng, không ghi Payment, chờ điểm chạm sau | P1 | Negative | NEW |
| SC-GN-015 | Phương thức gạch | REQ-GN-007 | DOC-v2.0-01 BR-XL-03 (L487) | Trường Paid/Cọc trên OrderBill **đã có** giá trị | Điểm chạm kích hoạt | Dùng giá trị có sẵn; **không** gọi API kênh thanh toán | P1 | Functional | NEW |
| SC-GN-016 | Phương thức gạch | REQ-GN-007 | DOC-v2.0-01 BR-XL-03 (L487) | Trường Paid/Cọc **chưa có** | Điểm chạm kích hoạt | Gọi API kênh thanh toán; giá trị lưu vào OrderBill; lần sau không gọi lại | P1 | Integration | NEW |
| SC-GN-017 | Phương thức gạch | REQ-GN-007 | DOC-v2.0-01 BR-XL-03 (L488) | Trường chưa có; API kênh thanh toán **lỗi / timeout** (mock) | Điểm chạm kích hoạt | Dừng, không gạch, **không retry** trong lần đó; điểm chạm sau gọi lại | P1 | Negative | NEW |
| SC-GN-018 | Phân luồng Paid / Cọc | REQ-GN-008 | DOC-v2.0-01 BR-XL-03 (L489) | 2 hóa đơn: trường = "Paid" và trường = "Cọc" | Điểm chạm kích hoạt | Hóa đơn "Paid" đi luồng Paid; hóa đơn "Cọc" đi luồng Cọc; mỗi đơn chỉ một luồng | P1 | Functional | NEW |
| SC-GN-019 | Gạch nợ tạm | REQ-GN-009, REQ-GN-010 | DOC-v2.0-01 BR-NT-01 (L493), BR-NT-02 (L498-499) | Đơn kênh sàn (Shopee/Tiktok), hóa đơn còn nợ N, luồng Paid | Paid ở trạng thái **tạm** | Ghi 1 Payment phương thức **"gạch nợ tạm"** = N (toàn bộ nợ còn lại — đơn không có EVC); hóa đơn chuyển "Đã gạch nợ" | P1 | Functional | NEW |
| SC-GN-022 | Gỡ gạch nợ tạm | REQ-GN-011 | DOC-v2.0-01 BR-NT-04 (L503) | Hóa đơn đã gạch nợ tạm (Payment đặc biệt) | Paid chuyển **hoàn tất** | Payment tạm bị gỡ trước (hóa đơn trở lại còn nợ), sau đó gạch nợ thật bằng Paid | P1 | Functional | NEW |
| SC-GN-023 | Gỡ gạch nợ tạm | REQ-GN-011 | DOC-v2.0-01 BR-NT-04 (L504) | Hóa đơn **chưa** gạch nợ tạm | Paid hoàn tất | Gạch nợ thật luôn, không có bước gỡ | P1 | Functional | NEW |
| SC-GN-026 | Điều kiện Paid | REQ-GN-012 | DOC-v2.0-01 BR-GN-01 (L508) | Hóa đơn của OrderCode X; Paid thuộc OrderCode **Y** | Gạch nợ chạy | Paid của Y không được dùng cho hóa đơn của X | P1 | Negative | NEW |
| SC-GN-027 | Điều kiện Paid | REQ-GN-012 | DOC-v2.0-01 BR-GN-01 (L509) | Hóa đơn **đã gạch đủ** | Điểm chạm kích hoạt lại (worker 30 phút) | Không gạch lần nữa; không có Payment trùng | P1 | Negative | NEW |
| SC-GN-028 | Thứ tự bill | REQ-GN-013 | DOC-v2.0-01 BR-GN-03 (L513) | Đơn sàn TMĐT có 3 bill 300k / 500k / 100k, luồng Paid, **Paid 900k = tổng tiền đơn** | Gạch nợ chạy | Gạch lần lượt **bill 500k → bill 300k → bill 100k** (từ cao xuống thấp), mỗi bill gạch đủ nợ 1 lần; cả 3 bill "Đã gạch nợ"; Paid còn 0 (CL-GN-05 resolved 20/10/2026) | P1 | Functional | NEW |
| SC-GN-029 | Thứ tự bill | REQ-GN-013 | DOC-v2.0-01 BR-GN-03 (L514) | Đơn có ≥2 bill, luồng **Cọc** | Gạch nợ chạy | Bill được xét từ cao xuống thấp | P1 | Functional | NEW |
| SC-GN-030 | Thứ tự bill | REQ-GN-013 | DOC-v2.0-01 BR-GN-03 (L513) | Đơn sàn TMĐT có 2 bill **bằng tiền nhau** (vd 300k / 300k), luồng Paid, Paid 600k = tổng tiền đơn | Gạch nợ chạy | Cả 2 bill được gạch đủ nợ, "Đã gạch nợ"; Paid còn 0. **Bill nào gạch trước cũng được** — không kiểm thứ tự giữa 2 bill (CL-GN-09 resolved 20/10/2026) | P3 | Boundary | NEW |
| SC-GN-033 | Gạch từng phần | REQ-GN-014, REQ-GN-015 | DOC-v2.0-01 BR-GN-04 (L518) | Hóa đơn nợ 500k; Paid 500k | Gạch nợ chạy | Gạch 500k; hóa đơn "Đã gạch nợ"; Paid còn 0 | P1 | Boundary | NEW |
| SC-GN-034 | Gạch từng phần | REQ-GN-014 | DOC-v2.0-01 BR-GN-04 (L518) | Luồng Paid, hóa đơn còn nợ | Một lần gạch thực hiện | QC kiểm dòng Payment ghi đúng số tiền. Paid bị trừ: QC không check (không có màn tra Paid luồng sàn — dev tự kiểm, QC owner 21/10/2026). Kafka Out: QC không check (CL-XHD-29) | P1 | Integration | NEW |
| SC-GN-037 | Cọc — đủ tiền | REQ-GN-016 | DOC-v2.0-01 BR-GC-01 (L529) | Bill nợ 1.000k; cọc hóa đơn 700k + EVC đơn 300k (gồm lock 100k) | Gạch cọc xét bill | Tổng = nợ ⇒ **đủ tiền** (biên "không nhỏ hơn"), bill được gạch bằng cọc (không kiểm theo loại cọc — nháp #12) | P1 | Boundary | NEW |
| SC-GN-042 | Cọc — cách trừ | REQ-GN-017, REQ-GN-018 | DOC-v2.0-01 BR-GC-02 (L534) ↔ BR-GC-03 (L539) | Đơn ngoài sàn, luồng Cọc, bill có nhiều dịch vụ (dùng nhiều loại cọc) | Gạch cọc | Có sinh Payment cọc; Σ Payment cọc = nợ bill; cọc bị trừ đúng tổng tiền; hóa đơn "Đã gạch nợ", nợ còn lại = 0. **Không kiểm theo từng loại cọc** / số dòng Payment theo loại (QC owner 21/10/2026, nháp #12 — gộp SC-GN-039, 035) | P1 | Functional | NEW |
| SC-GN-043 | Cọc — cách trừ | REQ-GN-018 | DOC-v2.0-01 BR-GC-03 (L540) | Bill nợ 1.000k, đội EVC đã gạch 200k | Gạch cọc | Trừ cọc trên **800k** còn lại; Payment + trừ cọc ghi theo BillNumber + số hợp đồng | P1 | Functional | NEW |
| SC-GN-045 | EVC | REQ-GN-019 | DOC-v2.0-01 BR-VC (L545) | Đơn có EVC (không lock), luồng Paid | Chạy hết các điểm chạm | **Nợ còn lại của hóa đơn = 0**, hóa đơn "Đã gạch nợ"; Σ Payment (tiền khách + EVC) = tổng hóa đơn — **không vượt** (không gạch trùng). **Không kiểm bên nào gạch** phần EVC. Nợ ≠ 0 ⇒ liên hệ owner EVC (CL-GN-01 21/10/2026) | P1 | Functional | NEW |
| SC-GN-046 | EVC lock | REQ-GN-020 | DOC-v2.0-01 BR-VC (L546) | Bill nợ 1.000k; EVC lock 300k; Paid khách **700k** (= phần khách trả) | Gạch tiền khách | Gạch = min(1.000k − 300k, 700k) = **700k**; phần lock 300k **chừa ra**, hóa đơn còn nợ 300k chờ khách ký (đội EVC add) | P1 | Functional | NEW |
| SC-GN-047 | EVC lock | REQ-GN-020 | DOC-v2.0-01 BR-VC (L546) | Bill nợ 1.000k; lock **0**; Paid khách 1.000k | Gạch tiền khách | **Lock 0 ⇒ gạch như thường: 1.000k**; hóa đơn "Đã gạch nợ" | P2 | Boundary | NEW |
| SC-GN-048 | Paid voucher | REQ-GN-012, REQ-GN-019 | DOC-v2.0-01 BR-DP-01 (L474) ↔ BR-VC (L545) | Đơn có Paid PaidType **voucher** Amount > 0 cùng OrderCode | Chạy hết các điểm chạm, luồng Paid | **Nợ còn lại = 0**, hóa đơn "Đã gạch nợ"; Σ Payment = tổng hóa đơn (không vượt). **Không kiểm bên nào gạch** khoản voucher (CL-GN-01 21/10/2026) | P1 | Functional | NEW |
| SC-GN-050 | Bán thêm | REQ-GN-016, REQ-GN-018 | DOC-v2.0-04 mail PM ↔ DOC-v2.0-01 BR-GC-01 (L529) | Hợp đồng **đã có từ trước** (có thể tạo từ rất lâu), đơn hàng trước đã gạch xong (dòng cọc đã clear); khách mua **bán thêm** trên hợp đồng này, thanh toán ngoài Paid, luồng Cọc | Gạch cọc | Đơn bán thêm **có sinh dòng cọc** riêng cho bill bán thêm; gạch ⇒ clear đúng dòng cọc của bill bán thêm, dòng cọc của đơn trước không đổi; hóa đơn bán thêm "Đã gạch nợ". Loại cọc không test (CL-GN-07); QC owner xác nhận nháp #15 | P2 | Functional | NEW |
| SC-GN-051 | Gạch nợ tạm | REQ-GN-010, REQ-GN-019 | DOC-v2.0-01 BR-NT-02 (L498) ↔ BR-VC (L545) | Đơn kênh sàn, hóa đơn tổng T, có EVC / voucher E, luồng Paid | Paid ở trạng thái **tạm** | Payment "gạch nợ tạm" = **T − E** (luôn trừ phần EVC — BA 21/10/2026); sau khi phần EVC được gạch: nợ còn lại = 0, hóa đơn "Đã gạch nợ" | P1 | Functional | NEW |
| SC-GN-053 | Cọc — clear đúng dòng | REQ-GN-018 | DOC-v2.0-01 BR-GC-03 (L540-541) | Hợp đồng có 2 bill A, B ⇒ thông tin cọc có 2 dòng (dòng A, dòng B); khách thanh toán bill A | Gạch cọc bill A | Chỉ **dòng cọc A** được clear; dòng cọc B giữ nguyên; Payment ghi theo BillNumber A + số hợp đồng; bill B chưa gạch (QC owner 21/10/2026, nháp #11) | P1 | Functional | NEW |
| SC-GN-054 | Bán thêm — gạch kèm đơn hàng trước | REQ-GN-016, REQ-GN-018 | DOC-v2.0-04 mail PM ↔ DOC-v2.0-01 BR-GC-01 (L529), BR-GC-03 (L540) | Hợp đồng đã có **đơn hàng trước chưa thanh toán** (chưa thỏa điều kiện gạch); khách mua **bán thêm** trên cùng hợp đồng, luồng Cọc | Khách thanh toán đơn hàng trước; gạch nợ đơn bán thêm chạy, lúc này đơn hàng trước **đã thỏa điều kiện** | **Gạch luôn cả 2 đơn hàng**: hóa đơn của đơn hàng trước và hóa đơn bán thêm đều "Đã gạch nợ"; mỗi bill clear đúng dòng cọc của nó (QC owner 21/10/2026, nháp #15, #16) | P2 | Integration | NEW |
| SC-GN-055 | Cọc — hóa đơn DV + TB khác thời điểm | REQ-GN-004, REQ-GN-018 | DOC-v2.0-01 BR-XL-01 (L480) ↔ BR-GC-03 (L540) | Đơn **ngoài sàn** có dịch vụ + thiết bị, khách thanh toán toàn bộ đơn ngoài Paid ⇒ mỗi bill (DV, TB) có dòng cọc riêng; hóa đơn DV phát hành khi có tín hiệu "đã thanh toán", hóa đơn TB **chưa** phát hành (chưa giao hàng) | Gạch nợ chạy cho hóa đơn DV; sau đó giao hàng hoàn tất ⇒ hóa đơn TB phát hành — điểm chạm (b) | Lần 1: chỉ hóa đơn DV "Đã gạch nợ", chỉ dòng cọc bill DV được clear, dòng cọc bill TB giữ nguyên. Lần 2: hóa đơn TB "Đã gạch nợ" bằng dòng cọc của bill TB; dòng cọc bill DV không bị trừ lại | P1 | Integration | NEW |
| SC-GN-056 | Nhóm DV — Internet | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh Mobile (1) gồm dịch vụ thuộc nhóm **Internet (ServiceID 1)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P1 | Integration | NEW |
| SC-GN-057 | Nhóm DV — FPT Camera Only | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh CMR-App (16) gồm dịch vụ thuộc nhóm **FPT Camera Only (ServiceID 3)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P1 | Integration | NEW |
| SC-GN-058 | Nhóm DV — FPT Camera Combo | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh Desktop (2) gồm dịch vụ thuộc nhóm **FPT Camera Combo (ServiceID 4)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P1 | Integration | NEW |
| SC-GN-059 | Nhóm DV — FPT Play Stands Alone | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh FPL (10) gồm dịch vụ thuộc nhóm **FPT Play Stands Alone (ServiceID 5)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-060 | Nhóm DV — Sản phẩm khác | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh F-Retail (15) gồm dịch vụ thuộc nhóm **Sản phẩm khác (ServiceID 6)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-061 | Nhóm DV — FPT Play | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh HiFPT (19) gồm dịch vụ thuộc nhóm **FPT Play (ServiceID 7)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P1 | Integration | NEW |
| SC-GN-062 | Nhóm DV — Tổng đài Oncall | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh CRM (13) gồm dịch vụ thuộc nhóm **Tổng đài Oncall (ServiceID 8)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-063 | Nhóm DV — FPT Smart Home | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh DKOL (4) gồm dịch vụ thuộc nhóm **FPT Smart Home (ServiceID 9)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-064 | Nhóm DV — Ultra Fast Stand Alone | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh W-Sale (9) gồm dịch vụ thuộc nhóm **Ultra Fast Stand Alone (ServiceID 10)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-065 | Nhóm DV — FPro | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh VNTT (11) gồm dịch vụ thuộc nhóm **FPro (ServiceID 11)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-066 | Nhóm DV — FSafe Go | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh MBBank (12) gồm dịch vụ thuộc nhóm **FSafe Go (ServiceID 12)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-067 | Nhóm DV — VioEdu Stand Alone | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh Momo (17) gồm dịch vụ thuộc nhóm **VioEdu Stand Alone (ServiceID 13)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-068 | Nhóm DV — VIP 247 | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh TGDD (14) gồm dịch vụ thuộc nhóm **VIP 247 (ServiceID 15)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-069 | Nhóm DV — SIM data | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh API (7) gồm dịch vụ thuộc nhóm **SIM data (ServiceID 16)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-070 | Nhóm DV — Pay Wifi | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh Mobile (1) gồm dịch vụ thuộc nhóm **Pay Wifi (ServiceID 17)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-071 | Nhóm DV — Ultra Fast | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh Desktop (2) gồm dịch vụ thuộc nhóm **Ultra Fast (ServiceID 18)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-072 | Nhóm DV — FPT Camera B2B | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh CRM (13) gồm dịch vụ thuộc nhóm **FPT Camera B2B (ServiceID 19)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-073 | Nhóm DV — HyperFast | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh HiFPT (19) gồm dịch vụ thuộc nhóm **HyperFast (ServiceID 21)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-074 | Nhóm DV — FPT AI Wi-Fi | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh Mobile (1) gồm dịch vụ thuộc nhóm **FPT AI Wi-Fi (ServiceID 23)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |
| SC-GN-075 | Nhóm DV — Prepaid 3 | REQ-GN-016, REQ-GN-018 | DOC-v2.0-01 §A.3 ↔ BR-GC-01 (L529), BR-GC-03 (L540) | Đơn ngoài sàn kênh DKOL (4) gồm dịch vụ thuộc nhóm **Prepaid 3 (ServiceID 25)** — dịch vụ bất kỳ của nhóm; khách thanh toán toàn bộ ngoài Paid | Mọi hóa đơn của đơn phát hành (gồm hóa đơn thiết bị sau giao hàng, nếu có); chạy hết điểm chạm | Mọi hóa đơn "Đã gạch nợ", nợ còn lại = 0; Σ Payment = tổng tiền đơn; cọc từng bill clear đúng số tiền. Không kiểm loại cọc / SubServiceType | P2 | Integration | NEW |

#### Source Detail per Scenario (verbatim quotes — `references/quoting-guide.md`)

> Given/When/Then đã ở bảng trên — block dưới không lặp, chỉ giữ quote justify + ghi chú dẫn xuất. Số tiền trong G/W/T là dữ liệu minh họa của analyst.

##### SC-GN-003 · Trùng đủ 4 trường
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L475`

> Trùng khi giống cả 4 trường OrderCode + RefTransactionId + PaidType + Amount: trùng thì cập nhật paymentstatus

↳ **Ghi chú:** Đây cũng là đường Paid "tạm → hoàn tất" của kênh sàn.

---

##### SC-GN-007 · Paid về trước hóa đơn
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

↳ **Ghi chú:** Chạy với dữ liệu Shopee và Tiktok. Nửa XHD ở SC-XHD-029. Đơn có EVC: Payment tạm = nợ − EVC (SC-GN-051).

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

↳ **Ghi chú:** Luồng Paid áp cho sàn TMĐT: tiền khách thanh toán về công ty rồi mới gạch ⇒ Paid luôn = tổng tiền đơn; thứ tự kiểm qua thứ tự ghi Payment của từng bill (CL-GN-05 resolved 20/10/2026).

---

##### SC-GN-029 · Thứ tự cao → thấp (Cọc)
📍 `DOC-v2.0-01 §II.c BR-GN-03 · L514`

> Áp dụng cho cả nhánh Paid và nhánh Cọc.

↳ **Ghi chú:** Cọc luôn đủ (cọc = phần khách trả) ⇒ thứ tự kiểm qua thứ tự ghi Payment của từng bill, như SC-GN-028. Mỗi bill clear dòng cọc của chính bill đó (QC owner 21/10/2026, nháp #11).

---

##### SC-GN-030 · Bill bằng tiền nhau
📍 `DOC-v2.0-01 §II.c BR-GN-03 · L513`

> theo số tiền từ cao xuống thấp.

↳ **Ghi chú:** 2 bill bằng tiền nhau ⇒ gạch bill nào trước cũng được, tùy logic code; TC chỉ kiểm cả 2 bill được gạch đúng số tiền (CL-GN-09 resolved 20/10/2026) — P3.

---

##### SC-GN-033 · Paid = nợ
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L518`

> Mỗi lần gạch = nhỏ nhất của số dư Paid và nợ còn lại

↳ **Ghi chú:** Biên bằng.

---

##### SC-GN-034 · Đầu ra của một lần gạch Paid
📍 `DOC-v2.0-01 §II.c BR-GN-04 · L518`

> ghi Payment, trừ Paid, đẩy Kafka Out về kênh thanh toán.

↳ **Ghi chú:** QC chỉ kiểm Payment + Paid bị trừ. Kafka Out: QC không check Kafka (BA: phần dành cho dev — CL-XHD-29, 21/10/2026) — không là điều kiện PASS.

---

##### SC-GN-037 · Đủ tiền — biên bằng
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529`

> Tổng cọc còn lại của hợp đồng (mọi loại cọc) cộng tổng tiền EVC của đơn (tính cả phần bị lock) phải không nhỏ hơn nợ của bill đang xét.

↳ **Ghi chú:** Lock tính vào điều kiện đủ tiền nhưng không được gạch.

---

##### SC-GN-042 · Gạch cọc bill nhiều dịch vụ
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L539`

> Mỗi dịch vụ trừ đúng loại cọc của nó; nhiều dịch vụ cùng loại cọc gom thành một dòng Payment.

↳ **Ghi chú:** QC owner 21/10/2026 (nháp #12 — chọn a): không kiểm map dịch vụ ↔ loại cọc, không kiểm số dòng Payment theo loại; chỉ kiểm có sinh Payment cọc, tổng tiền đúng, nợ = 0. Gộp ý của SC-GN-039 (đủ cọc mọi loại) và SC-GN-035 (đầu ra một lần gạch Cọc: Payment + cọc bị trừ).

---

##### SC-GN-043 · Trừ cọc sau EVC
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L540`

> Tính trên nợ còn lại sau khi EVC đã gạch; ghi Payment và trừ cọc theo BillNumber + số hợp đồng.

↳ **Ghi chú:** Cần đội EVC (hoặc mock) gạch trước.

---

##### SC-GN-045 · INVOICE không gạch EVC
📍 `DOC-v2.0-01 §II.c BR-VC · L545`

> Phần gạch nợ bằng EVC do đội EVC thực hiện; ISC tự quyết phương thức quản trị và xử lý voucher.

↳ **Ghi chú:** BA 21/10/2026 (CL-GN-01): QC **không cần quan tâm bên nào gạch**; gạch EVC chỉ là gạch nợ trên hóa đơn ⇒ kiểm **nợ còn lại = 0** sau khi chạy các điểm chạm, nợ ≠ 0 ⇒ liên hệ owner check. Thêm điều kiện Σ Payment không vượt tổng hóa đơn để bắt gạch trùng (RISK-GN-01). Bối cảnh CL-GN-08: 2 hệ thống chạy song song.

---

##### SC-GN-046 · Chừa phần lock
📍 `DOC-v2.0-01 §II.c BR-VC · L546`

> số gạch = nhỏ nhất của (nợ bill trừ tiền lock) và Paid khách thanh toán.

↳ **Ghi chú:** Hiện chỉ EVC Loyalty FTEL có lock. Paid khách = phần khách trả (BA 21/10/2026) ⇒ không có Paid dư.

---

##### SC-GN-047 · Lock = 0
📍 `DOC-v2.0-01 §II.c BR-VC · L546`

> Với EVC bị lock (khách chưa ký hợp đồng), INVOICE chừa phần lock khi gạch tiền khách

↳ **Ghi chú:** Biên 0 — công thức suy biến về BR-GN-04.

---

##### SC-GN-048 · Paid voucher dùng gạch nợ
📍 `DOC-v2.0-01 §II.c BR-DP-01 · L474` ↔ `BR-VC · L545`

> gồm cả voucher và tiền khách thanh toán
> Phần gạch nợ bằng EVC do đội EVC thực hiện

↳ **Ghi chú:** Gạch nợ EVC / voucher vẫn test (QC owner 19/10/2026, khác TP §2.2 #5). BA 21/10/2026 (CL-GN-01): không kiểm bên nào gạch — kiểm nợ còn lại = 0. Dữ liệu: dùng loại voucher có sẵn trên STG.

---

##### SC-GN-050 · Đơn bán thêm dùng cọc hợp đồng
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529` + `DOC-v2.0-04 mail PM`

> Tổng cọc còn lại của hợp đồng (mọi loại cọc)
> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** QC owner 21/10/2026 (nháp #11): 1 hợp đồng có nhiều dòng trong thông tin cọc, mỗi bill clear đúng dòng của nó, mỗi dòng clear 1 lần ⇒ không có cọc dư dùng chung. Đơn bán thêm có bill riêng ⇒ có dòng cọc riêng — **QC owner xác nhận 21/10/2026 (nháp #15)**. Bán mới = phát sinh hợp đồng mới; bán thêm = bán trên hợp đồng đã có (có thể từ rất lâu); hai luồng xử lý gạch nợ cơ bản như nhau. Thay suy diễn cũ "dùng chung cọc dư của hợp đồng" (hết hiệu lực).

---

##### SC-GN-051 · Gạch tạm luôn trừ phần EVC
📍 `DOC-v2.0-01 §II.c BR-NT-02 · L498` ↔ `BR-VC · L545`

> Ghi Payment bằng phương thức thanh toán đặc biệt, số tiền bằng toàn bộ nợ còn lại.
> Phần gạch nợ bằng EVC do đội EVC thực hiện

↳ **Ghi chú:** BA 21/10/2026: luồng gạch tạm luôn trừ phần EVC trước ⇒ "toàn bộ nợ còn lại" = nợ sau khi trừ EVC. Không kiểm bên nào gạch phần EVC; điểm kiểm cuối: nợ còn lại = 0 (CL-GN-01).

---

##### SC-GN-053 · Mỗi bill clear đúng dòng cọc của nó
📍 `DOC-v2.0-01 §II.c BR-GC-03 · L540-541`

> ghi Payment và trừ cọc theo BillNumber + số hợp đồng.
> Dư cọc không xử lý; không gạch lại hóa đơn đã gạch.

↳ **Ghi chú:** QC owner 21/10/2026 (nháp #11): 1 hợp đồng có nhiều dòng trong thông tin cọc (vd bill A, bill B); thanh toán A thì chỉ clear dòng A; mỗi dòng cọc clear 1 lần ⇒ không có case một dòng cọc clear 2–3 lần, không có cọc dư. Thay SC-GN-044 (deprecated). Verify: Tiền đặt cọc › Tra cứu.

---

##### SC-GN-054 · Gạch đơn bán thêm kéo theo đơn hàng trước
📍 `DOC-v2.0-01 §II.c BR-GC-01 · L529` + `DOC-v2.0-04 mail PM`

> Tổng cọc còn lại của hợp đồng (mọi loại cọc)
> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** QC owner 21/10/2026 (nháp #15): nếu đơn hàng trước trên cùng hợp đồng chưa thỏa điều kiện gạch, mà lúc gạch đơn bán thêm thì đơn hàng trước đã thỏa ⇒ gạch luôn 2 đơn. Nháp #16: "chưa thỏa điều kiện" = **đơn hàng trước chưa thanh toán**; "đơn" ở đây là **đơn hàng**, không phải hóa đơn. URD 2.2 không nêu rõ — căn cứ là câu trả lời QC owner. Dữ liệu: hợp đồng có đơn hàng chưa thanh toán + tạo đơn bán thêm trên cùng hợp đồng.

---

##### SC-GN-055 · Hóa đơn DV và TB phát hành khác thời điểm, mỗi hóa đơn gạch đúng dòng cọc
📍 `DOC-v2.0-01 §II.c BR-XL-01 · L480` ↔ `BR-GC-03 · L540`

> 3 điểm chạm: (a) đồng bộ Paid xong; (b) sau khi xuất hóa đơn; (c) worker quét 30 phút một lần.
> ghi Payment và trừ cọc theo BillNumber + số hợp đồng.

↳ **Ghi chú:** Ghép từ flow E2E QC owner (`07_environments/environments.md` — xuất hóa đơn dịch vụ trước, hóa đơn thiết bị sau khi giao hàng; BR-XHD-03 L396 xét độc lập) + nháp #11 (mỗi bill 1 dòng cọc, clear 1 lần). Đề xuất QC 21/10/2026 khi rà phủ kênh / nhóm dịch vụ — tình huống thực tế phổ biến nhất của luồng Cọc. Kênh ngoài sàn: dùng đại diện (EP — 14 kênh ngoài sàn cùng 1 lớp, BR-NT-01 L494).

---

##### SC-GN-056 · Gạch nợ đúng cho nhóm Internet (ServiceID 1)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh Mobile (1) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-057 · Gạch nợ đúng cho nhóm FPT Camera Only (ServiceID 3)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh CMR-App (16) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-058 · Gạch nợ đúng cho nhóm FPT Camera Combo (ServiceID 4)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh Desktop (2) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-059 · Gạch nợ đúng cho nhóm FPT Play Stands Alone (ServiceID 5)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh FPL (10) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-060 · Gạch nợ đúng cho nhóm Sản phẩm khác (ServiceID 6)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh F-Retail (15) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-061 · Gạch nợ đúng cho nhóm FPT Play (ServiceID 7)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh HiFPT (19) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-062 · Gạch nợ đúng cho nhóm Tổng đài Oncall (ServiceID 8)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh CRM (13) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-063 · Gạch nợ đúng cho nhóm FPT Smart Home (ServiceID 9)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh DKOL (4) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-064 · Gạch nợ đúng cho nhóm Ultra Fast Stand Alone (ServiceID 10)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh W-Sale (9) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-065 · Gạch nợ đúng cho nhóm FPro (ServiceID 11)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh VNTT (11) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-066 · Gạch nợ đúng cho nhóm FSafe Go (ServiceID 12)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh MBBank (12) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-067 · Gạch nợ đúng cho nhóm VioEdu Stand Alone (ServiceID 13)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh Momo (17) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-068 · Gạch nợ đúng cho nhóm VIP 247 (ServiceID 15)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh TGDD (14) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-069 · Gạch nợ đúng cho nhóm SIM data (ServiceID 16)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh API (7) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-070 · Gạch nợ đúng cho nhóm Pay Wifi (ServiceID 17)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh Mobile (1) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-071 · Gạch nợ đúng cho nhóm Ultra Fast (ServiceID 18)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh Desktop (2) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-072 · Gạch nợ đúng cho nhóm FPT Camera B2B (ServiceID 19)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh CRM (13) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-073 · Gạch nợ đúng cho nhóm HyperFast (ServiceID 21)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh HiFPT (19) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-074 · Gạch nợ đúng cho nhóm FPT AI Wi-Fi (ServiceID 23)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh Mobile (1) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

##### SC-GN-075 · Gạch nợ đúng cho nhóm Prepaid 3 (ServiceID 25)
📍 `DOC-v2.0-01 §A.3` ↔ `§II.c BR-GC-03 · L540`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ).

↳ **Ghi chú:** QC owner 21/10/2026: mỗi nhóm dịch vụ có ≥1 TC riêng, không quan tâm SubServiceType. Kênh DKOL (4) gán xoay vòng để phủ 14 kênh ngoài sàn (EP — cùng quy tắc BR-NT-01 L494); kênh không bán nhóm này ⇒ đổi kênh ngoài sàn khác, ghi kênh thực tế.

---

## Scenarios — CARRIED (reference only)

| Scenario ID | Tên ngắn | Module | Origin Version | Priority | Reference |
|-------------|----------|--------|---------------|----------|-----------|
| — | *(v2.0 là version đầu tiên trong workspace — chưa có CARRIED)* | — | — | — | — |

## Scenarios — DEPRECATED

| Scenario ID | Tên ngắn | Module | Deprecated ở | Lý do |
|-------------|----------|--------|-------------|-------|
| SC-GN-049 | API EVC lỗi / timeout | GN | v2.0 (19/10/2026) | CL-GN-02: STG không test timeout; thực tế đội dự án retry thủ công, API lỗi ⇒ log bug |
| SC-GN-024 | Paid hoàn tất nhỏ hơn nợ đã gạch tạm | GN | v2.0 (19/10/2026) | CL-GN-06: phí sàn TMĐT đã tính vào tiền khách trả ⇒ không có trường hợp Paid quyết toán của sàn nhỏ hơn nợ |
| SC-GN-012 | Lọc (a) — Paid tạm + kênh không sàn | GN | v2.0 (21/10/2026) | BA 21/10/2026: Paid trạng thái tạm chỉ có ở đơn sàn ⇒ đơn ngoài sàn không có Paid tạm, case không xảy ra |
| SC-GN-020 | Không gạch tạm kênh không sàn | GN | v2.0 (21/10/2026) | Cùng lý do SC-GN-012 — đơn ngoài sàn không có Paid tạm; đơn ngoài sàn đi luồng Cọc |
| SC-GN-021 | Nhánh Cọc không gạch tạm (đơn sàn) | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: đơn sàn luôn đi luồng Paid, đơn ngoài sàn đi luồng Cọc ⇒ không có đơn sàn đi Cọc; "Cọc không gạch tạm" kiểm qua các SC luồng Cọc (vd SC-GN-042, 055 — Payment bằng cọc, không có Payment tạm) |
| SC-GN-032 | Paid > nợ, Paid dư giữ lại | GN | v2.0 (21/10/2026) | BA 21/10/2026: luồng thực tế không dựng được Paid dư (dư = dev đẩy data sai) |
| SC-GN-038 | Cọc — không đủ tiền (cọc + EVC < nợ bill) | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: khách thanh toán ngoài Paid đều đẩy vào cọc, cọc luôn bằng tiền đơn ⇒ thực tế không có case thiếu tiền (lệch chỉ khi dev đẩy dữ liệu sai) |
| SC-GN-040 | Cọc — thiếu một loại cọc ⇒ không gạch cả bill | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: cọc luôn bằng tiền đơn ⇒ không có case thiếu cọc theo loại; map dịch vụ ↔ loại cọc không test (CL-GN-07) |
| SC-GN-041 | Cọc — bill thiếu cọc không chặn bill khác | GN | v2.0 (21/10/2026) | Phụ thuộc SC-GN-040 (cần một bill thiếu cọc) — không xảy ra, cùng lý do |
| SC-GN-031 | Paid < nợ (gạch từng phần hóa đơn) | GN | v2.0 (20/10/2026) | CL-GN-05: luồng Paid áp cho sàn TMĐT, khách thanh toán full ⇒ Paid = tổng tiền đơn, không có trường hợp Paid nhỏ hơn nợ; "gạch từng phần" (BR-GN-04) là chia Paid cho từng bill, không phải gạch một phần hóa đơn |
| SC-GN-025 | Biên Paid Amount 0 / 1 | GN | v2.0 (21/10/2026) | QC owner 21/10/2026 (nháp #13): đơn 0đ không thanh toán, không có khoản thu / cọc / gạch nợ; Paid 1đ không dựng được data ⇒ biên không cần |
| SC-GN-036 | Biên Σ Payment T − 1 / T | GN | v2.0 (21/10/2026) | QC owner 21/10/2026 (nháp #13): biên không cần — Paid / cọc luôn bằng phần khách trả, không dựng được T − 1; Σ Payment = T đã kiểm ở SC-GN-033, trạng thái còn nợ ở SC-GN-046 |
| SC-GN-035 | Đầu ra của một lần gạch Cọc | GN | v2.0 (21/10/2026) | QC owner 21/10/2026 (nháp #14): gộp vào SC-GN-042, 043 (Payment + cọc bị trừ); ý "không Kafka Out" đã bỏ (CL-XHD-29) |
| SC-GN-039 | Cọc — đủ cọc mọi loại | GN | v2.0 (21/10/2026) | QC owner 21/10/2026 (nháp #12): không kiểm theo loại cọc ⇒ gộp vào SC-GN-042 |
| SC-GN-044 | Dư cọc, không gạch lại | GN | v2.0 (21/10/2026) | QC owner 21/10/2026 (nháp #11): mỗi bill có dòng cọc riêng, clear 1 lần ⇒ không có cọc dư; thay bằng SC-GN-053; không gạch lại hóa đơn đã gạch kiểm ở SC-GN-027 |
| SC-GN-052 | Điểm chạm (a) — luồng Cọc (Paid hoàn tất kích hoạt gạch cọc) | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: **Paid chỉ có ở luồng sàn**, luồng ngoài sàn là Cọc ⇒ đơn Cọc không có Paid, không kích hoạt ở điểm chạm (a); gạch cọc ở điểm chạm (b) sau khi xuất hóa đơn và worker (c) — đã kiểm qua SC-GN-029, 042, 055, 056..075 (khác câu trả lời BA nháp #8, #10 — theo QC owner) |
| SC-GN-001 | Paid 1:1 theo OrderCode (2 dòng tiền khách) | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: luồng sàn không có data trên Foxpay › Đối soát khoản thu online, không có màn tra bảng Paid ⇒ đồng bộ Paid **dev tự kiểm, QC không check** |
| SC-GN-002 | Paid voucher + tiền khách, PaidType theo nguồn tiền | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: luồng sàn không có data trên Foxpay › Đối soát khoản thu online, không có màn tra bảng Paid ⇒ đồng bộ Paid **dev tự kiểm, QC không check** |
| SC-GN-004 | Chống trùng — khác RefTransactionId thêm mới | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: luồng sàn không có data trên Foxpay › Đối soát khoản thu online, không có màn tra bảng Paid ⇒ đồng bộ Paid **dev tự kiểm, QC không check** |
| SC-GN-005 | Chống trùng — khác PaidType thêm mới | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: luồng sàn không có data trên Foxpay › Đối soát khoản thu online, không có màn tra bảng Paid ⇒ đồng bộ Paid **dev tự kiểm, QC không check** |
| SC-GN-006 | Chống trùng — khác Amount thêm mới | GN | v2.0 (21/10/2026) | QC owner 21/10/2026: luồng sàn không có data trên Foxpay › Đối soát khoản thu online, không có màn tra bảng Paid ⇒ đồng bộ Paid **dev tự kiểm, QC không check** |
