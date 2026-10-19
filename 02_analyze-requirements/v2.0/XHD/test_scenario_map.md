---
id: v2.0/XHD/test_scenario_map
title: Test Scenario Map — Module XHD
type: test_scenario_map
version: v2.0
module: { code: XHD, dir: XHD, name: "Đồng bộ đơn hàng & xuất hóa đơn tự động" }
counts:                 # 🔑 CANONICAL — REQ/SC/lifecycle/priority của module XHD
  req: 43
  sc: 109
  new: 109
  modified: 0
  carried: 0
  deprecated: 2
  p1: 84
  p2: 24
  p3: 1
  blocked_by_cl: 9      # SC có Then phụ thuộc CL chưa trả lời (vẫn gán Priority)
status: ANALYZED
updated: 2026-10-19
---

# Test Scenario Map — v2.0 · Module XHD

> **Home của SC quote** (1 quote = 1 nơi): Source Quote per SC ở §"Source Detail per Scenario" file này. REQ quote → `requirement_traceability.md §2`; Clarification quote → `risk_assessment.md` §Clarifications.

## Quy tắc đủ scenario (Scenario Sufficiency Rule)

> Nguyên tắc: **1 SC = 1 hành vi nguyên tử** (KHÔNG gộp nhiều hành vi vào 1 SC, KHÔNG đặt số N cứng cho mọi REQ).
>
> **Sàn tối thiểu / REQ:** ≥1 positive (happy path) + ≥1 negative (nếu REQ có validation/rule) + boundary (nếu có input range).
>
> **Fan-out theo chiều** — mỗi cái sau = 1 SC riêng: mỗi **role/quyền** · mỗi **state-transition** · mỗi **lớp EP** · mỗi **giá trị boundary** · mỗi **nhánh lỗi/MSG**. (Vd REQ 6-state → ~6 SC; REQ 2-role → ≥2-3 SC.)
>
> **Trần (KHÔNG sinh SC):** display-only / Phase-2 / duplicate — ghi vào `CHANGELOG.md §3` như gap có chủ đích, không tạo SC rác.

**Áp dụng cho XHD:**
- **Ma trận kênh × nhóm DV × loại đơn (TP F01):** fan-out theo **kênh** (17 SC — SC-XHD-001..017, mỗi kênh 1 lớp EP). Chiều 20 nhóm DV × {bán mới, bán thêm} là **dữ liệu** của từng SC (xem `test_data_catalog.md` field `ServiceID / SubServiceType`), generate-tc nhân ra TC.
- **BR-XHD-10:** mỗi trường bắt buộc = 1 SC (14 SC — SC-XHD-082..095), biên `> 0` nằm trong SC của trường đó.
- **SC phụ thuộc CL chưa trả lời** vẫn được sinh khi URD có hành vi một phần; cột `Then` ghi rõ `⛔ chờ CL-…` hoặc `(giả định TP)`. REQ không đủ để viết Then (REQ-XHD-039, REQ-XHD-042) **không** sinh SC.
- **Thời gian** viết theo "giờ chốt đợt 1 / đợt cuối" — giá trị 12:00/18:00 chỉ là giá trị đang cấu hình (⛔ không hardcode trong TC).

## Tổng quan
- Tổng số scenarios: 109 (NEW: 109, MODIFIED: 0, CARRIED: 0) — số canonical ở frontmatter `counts:`.
- Phân bổ priority: xem frontmatter `counts:` (p1 / p2 / p3).

> ℹ️ **19/10/2026 — QC không có quyền xem log** (CL-XHD-15, CL-XHD-19): mọi Then "ghi log" / "ghi Note" chỉ verify phần hành vi (không phát hành / không ghi nhận) qua tool ở `07_environments/environments.md §Tool tra cứu`; phần log không verify.

## Scenarios — NEW & MODIFIED (chi tiết đầy đủ)

### XHD — Đồng bộ đơn hàng & xuất hóa đơn tự động

| Scenario ID | Feature | Req ID | DOC Source | Given | When | Then | Priority | Test Type | Lifecycle |
|-------------|---------|--------|-----------|-------|------|------|----------|-----------|-----------|
| SC-XHD-001 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L85-87) | Kênh **Mobile (1)**; đơn bán mới / bán thêm cho từng nhóm DV §A.3 | Tạo đơn trên kênh, SPF đồng bộ sang INVOICE | Đơn ghi nhận đủ vào `OB_OrderRaw`/`_Detail` với SaleChannelID = 1; kết quả xuất hóa đơn kiểm ở các SC điều kiện phát hành | P1 | Integration | NEW |
| SC-XHD-002 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L88-90) | Kênh **Desktop (2)**; như SC-XHD-001 | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 2 | P1 | Integration | NEW |
| SC-XHD-003 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L91-93) | Kênh **DKOL (4)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 4 | P1 | Integration | NEW |
| SC-XHD-004 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L94-96) | Kênh **API (7)** — partner ngoài FTEL | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 7 | P1 | Integration | NEW |
| SC-XHD-005 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L97-99) | Kênh **W-Sale (9)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 9 | P1 | Integration | NEW |
| SC-XHD-006 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L100-102) | Kênh **FPL (10)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 10; luồng phát hành theo lịch FPL (SC-XHD-047..053) | P1 | Integration | NEW |
| SC-XHD-007 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L103-105) | Kênh **VNTT (11)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 11 | P1 | Integration | NEW |
| SC-XHD-008 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L106-108) | Kênh **MBBank (12)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 12 | P1 | Integration | NEW |
| SC-XHD-009 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L109-111) | Kênh **CRM (13)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 13 | P1 | Integration | NEW |
| SC-XHD-010 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L112-114) | Kênh **TGDD (14)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 14 | P1 | Integration | NEW |
| SC-XHD-011 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L115-117) | Kênh **F-Retail (15)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 15 | P1 | Integration | NEW |
| SC-XHD-012 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L118-120) | Kênh **CMR-App (16)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 16 | P1 | Integration | NEW |
| SC-XHD-013 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L121-123) | Kênh **Momo (17)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 17 | P1 | Integration | NEW |
| SC-XHD-014 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L124-126) | Kênh **SR-KPDV (18)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 18 | P1 | Integration | NEW |
| SC-XHD-015 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L127-129) | Kênh **HiFPT (19)** | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 19 | P1 | Integration | NEW |
| SC-XHD-016 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L130-133) | Kênh **Shopee (20)** — đã có Phase 1 | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 20; luồng Phase 1 không hỏng | P1 | Regression | NEW |
| SC-XHD-017 | Ma trận kênh | REQ-XHD-001, REQ-XHD-002, REQ-XHD-040 | DOC-v2.0-01 §A.2 (L134-137) | Kênh **Tiktok (21)** — đã có Phase 1 | Như SC-XHD-001 | Đơn ghi nhận đủ với SaleChannelID = 21; luồng Phase 1 không hỏng | P1 | Regression | NEW |
| SC-XHD-018 | Sự kiện SPF | REQ-XHD-003 | DOC-v2.0-01 BR-DB-01 (L345) | Đơn đã đồng bộ, DV chưa thanh toán | SPF phát sự kiện **thanh toán** | INVOICE nhận bản tin, cập nhật đơn; dòng DV đủ điều kiện phát hành ĐK DV | P1 | Functional | NEW |
| SC-XHD-019 | Sự kiện SPF | REQ-XHD-003, REQ-XHD-028 | DOC-v2.0-01 BR-DB-01 (L345) | Đơn đã đồng bộ, chưa có hóa đơn | SPF phát sự kiện **hủy đơn** | INVOICE ghi nhận trạng thái hủy; đơn không được phát hành ở đợt kế tiếp | P1 | Functional | NEW |
| SC-XHD-020 | Sự kiện SPF | REQ-XHD-003, REQ-XHD-008 | DOC-v2.0-01 BR-DB-01 (L345) ↔ BR-DB-03 (L359) | Khách hàng cập nhật thông tin trên **hợp đồng** trước khi hóa đơn phát hành | Worker phát hành hóa đơn | Hóa đơn dùng thông tin khách hàng **mới nhất trên hợp đồng**; SPF chỉ gửi sự kiện thanh toán, hủy đơn — không có sự kiện tạo đơn / cập nhật thông tin khách (CL-XHD-01, 19/10/2026) | P2 | Functional | NEW |
| SC-XHD-021 | Tín hiệu giao hàng | REQ-XHD-004, REQ-XHD-012 | DOC-v2.0-01 BR-DB-02 (L349) | Đơn có TB chưa xuất hóa đơn, phương thức TIN/PNC | **Phiếu thi công** chuyển "Đã xử lý hoàn tất" → tín hiệu về INVOICE | Tín hiệu map đúng dòng TB theo khóa 4 thành phần; TB đủ điều kiện phát hành | P1 | Integration | NEW |
| SC-XHD-022 | Tín hiệu giao hàng | REQ-XHD-004 | DOC-v2.0-01 BR-DB-02 (L349) | Đơn có TB chưa xuất hóa đơn, phương thức NCC (Vendor) | **Vendor** báo đối tác giao xong | Tín hiệu ghi nhận cho đúng TB của phương thức; TB đủ điều kiện | P1 | Integration | NEW |
| SC-XHD-023 | Tín hiệu giao hàng | REQ-XHD-004 | DOC-v2.0-01 BR-DB-02 (L349) | Đơn có TB chưa xuất hóa đơn, phương thức Quầy | **Phiếu giao tại quầy** hoàn tất | Tín hiệu ghi nhận cho đúng TB; TB đủ điều kiện | P1 | Integration | NEW |
| SC-XHD-024 | Tín hiệu giao hàng | REQ-XHD-004 | DOC-v2.0-01 BR-DB-02 (L350) | Đơn có TB chưa xuất hóa đơn | Nhận 1 tín hiệu giao hàng hoàn tất | Dữ liệu ghi nhận đủ 6 trường: mã đơn, ServiceCode, SubserviceType, phương thức triển khai, nguồn gửi, thời gian hoàn tất | P2 | Functional | NEW |
| SC-XHD-025 | Tín hiệu giao hàng | REQ-XHD-013 | DOC-v2.0-01 BR-DB-07 (L376) | TB phương thức Quầy chưa xuất hóa đơn | Tín hiệu đến từ **nguồn khác** (vd Vendor) nhưng khóa khớp | Vẫn ghi nhận (không ràng buộc nguồn); nguồn gửi được lưu = Vendor | P2 | Functional | NEW |
| SC-XHD-026 | Tín hiệu giao hàng | REQ-XHD-013 | DOC-v2.0-01 BR-DB-07 (L375) | Đơn không có TB nào khớp khóa của tín hiệu | Nhận tín hiệu giao hàng | Không ghi nhận vào dữ liệu phát hành; nội dung tín hiệu ghi vào cột Note | P1 | Negative | NEW |
| SC-XHD-027 | Tín hiệu giao hàng | REQ-XHD-013 | DOC-v2.0-01 BR-DB-07 (L375) | TB của phương thức đã có BillNumber | Nhận lại tín hiệu giao hàng cho phương thức đó | Không ghi nhận, không phát hành lại; log nội dung tín hiệu vào cột Note | P1 | Negative | NEW |
| SC-XHD-028 | Tín hiệu giao hàng | REQ-XHD-012 | DOC-v2.0-01 BR-DB-07 (L374) | TB có mã đơn + ServiceCode + SubserviceType khớp nhưng phương thức khác | Nhận tín hiệu sai phương thức triển khai | Coi là không khớp khóa (khớp 3/4 không đủ) → không ghi nhận, log Note | P2 | Negative | NEW |
| SC-XHD-029 | Đơn TMĐT | REQ-XHD-005 | DOC-v2.0-01 BR-DB-02 (L351) | Đơn Shopee/Tiktok có DV | SPF đánh dấu đơn "đã thanh toán" | DV đủ điều kiện phát hành; đồng thời Paid ghi nhận paymentstatus = gạch nợ tạm (đối chiếu GN SC-GN-019) | P1 | Regression | NEW |
| SC-XHD-030 | Thông tin KH | REQ-XHD-006 | DOC-v2.0-01 BR-DB-03 (L355) | Đơn kênh khác FPL đủ điều kiện | Worker phát hành hóa đơn | Tên, địa chỉ, MST… trên hóa đơn lấy theo **hợp đồng** | P1 | Functional | NEW |
| SC-XHD-031 | Thông tin KH | REQ-XHD-007 | DOC-v2.0-01 BR-DB-03 (L356-358) | Đơn FPL, khách chọn **lấy hóa đơn** | Khách nhập đủ 7 trường trong 2 giờ, sau đó hóa đơn được phát hành | Hóa đơn dùng thông tin khách tự nhập (tên, email, SĐT, MST, mã định danh, mã QHNS, số hộ chiếu), không dùng thông tin hợp đồng | P1 | Functional | NEW |
| SC-XHD-032 | Thông tin KH | REQ-XHD-007 | DOC-v2.0-01 BR-DB-03 (L358) | Đơn FPL đã thanh toán; khách vào web FPL › Quản lý thanh toán và gói › Xuất hóa đơn | Khách mở form ở mốc **đúng 2:00** và **2:01** kể từ thời gian tạo đơn | **2:00: nút Xuất hóa đơn còn, khách nhập được; 2:01: nút Xuất hóa đơn bị ẩn** (CL-XHD-02, 19/10/2026) | P2 | Boundary | NEW |
| SC-XHD-033 | Thông tin KH | REQ-XHD-007 | DOC-v2.0-01 BR-DB-03 (L356) | Đơn FPL đã thanh toán | Khách **không bấm** Xuất hóa đơn trong 2 giờ | **Không phát hành hóa đơn** (CL-XHD-02, 19/10/2026) | P2 | Functional | NEW |
| SC-XHD-034 | Thông tin KH | REQ-XHD-007 | DOC-v2.0-01 BR-DB-03 (L358) | Đơn FPL, khách đã bấm Xuất hóa đơn (form mở) | Quá 2 giờ khách không gửi thông tin | Nút Xuất hóa đơn bị ẩn; **không phát hành hóa đơn** (CL-XHD-02, 19/10/2026) | P2 | Negative | NEW |
| SC-XHD-035 | Thông tin KH | REQ-XHD-008 | DOC-v2.0-01 BR-DB-03 (L359) | Đơn đủ điều kiện, chưa tới giờ chạy worker | Thông tin khách được cập nhật | Không phát sinh hóa đơn tại thời điểm cập nhật | P1 | Functional | NEW |
| SC-XHD-036 | Thông tin KH | REQ-XHD-008 | DOC-v2.0-01 BR-DB-03 (L359) | Đơn đã cập nhật thông tin khách sau lần phát hành trước | Lần phát hành tiếp theo (TB / DV còn lại) chạy | Hóa đơn mới dùng thông tin khách mới nhất; hóa đơn cũ giữ nguyên | P1 | Functional | NEW |
| SC-XHD-037 | ProductType | REQ-XHD-009 | DOC-v2.0-01 BR-DB-04 (L363-364) | Đơn có dòng ProductType = DV và dòng ProductType = TB | Có tín hiệu thanh toán, chưa có tín hiệu giao hàng | Chỉ dòng DV phát hành; dòng TB chờ tín hiệu giao hàng — INVOICE không suy diễn từ SubServiceType/Type | P1 | Functional | NEW |
| SC-XHD-038 | Lần đẩy cuối | REQ-XHD-010 | DOC-v2.0-01 BR-DB-05 (L368) | Đơn chưa xuất hóa đơn | SPF đẩy bản tin lần 1 rồi lần 2 (khác thông tin) trước giờ chạy | Hóa đơn phát hành theo thông tin **lần 2** | P1 | Functional | NEW |
| SC-XHD-039 | Lần đẩy cuối | REQ-XHD-010 | DOC-v2.0-01 BR-DB-05 (L369) | Đơn đã xuất hóa đơn phần DV, TB chưa xuất | SPF đẩy bản tin mới cho đơn | Phần DV đã xuất không bị ghi đè / xóa / phát hành lại; chỉ phần TB được xử lý theo bản tin mới | P1 | Functional | NEW |
| SC-XHD-040 | Lần đẩy cuối | REQ-XHD-011 | DOC-v2.0-01 BR-DB-05 (L370) | — | INVOICE nhận mỗi bản tin đồng bộ | Thời điểm nhận được lưu cho từng bản tin (tên cột ⛔ chờ CL-XHD-29) | P2 | Functional | NEW |
| SC-XHD-041 | Lịch worker | REQ-XHD-014 | DOC-v2.0-01 BR-XHD-01 (L382) | Dòng đủ điều kiện, mốc nghiệp vụ trước giờ chốt đợt 1 | Tới giờ chạy đợt 1 | Dòng được phát hành ở đợt 1; BillDate = ngày chạy | P1 | Functional | NEW |
| SC-XHD-042 | Lịch worker | REQ-XHD-014, REQ-XHD-015 | DOC-v2.0-01 BR-XHD-01 (L382, L384) | Dòng A mốc sau chốt đợt 1 trước chốt đợt 2; dòng B mốc trước chốt đợt 1 nhưng đợt 1 chưa đủ điều kiện | Tới giờ chạy đợt 2 | Cả A và B được đợt 2 phát hành (đợt sau quét lại từ đầu ngày) | P1 | Functional | NEW |
| SC-XHD-043 | Lịch worker | REQ-XHD-014 | DOC-v2.0-01 BR-XHD-01 (L382, L384) | Dòng có mốc nghiệp vụ **ngay trước / đúng / ngay sau** giờ chốt đợt 1 | Tới giờ chạy đợt 1 | **Trước giờ chốt: vào đợt 1; đúng giờ chốt và sau: sang đợt sau** (biên "trước giờ chốt") | P1 | Boundary | NEW |
| SC-XHD-044 | Lịch worker | REQ-XHD-014 | DOC-v2.0-01 BR-XHD-01 (L381, L383) | Cấu hình hiện 2 đợt | Đổi tham số (thêm 1 đợt / đổi giờ chốt) | Worker chạy theo cấu hình mới, không cần sửa code; dòng phân đợt theo giờ chốt mới | P2 | Functional | NEW |
| SC-XHD-045 | Lịch worker | REQ-XHD-015 | DOC-v2.0-01 BR-XHD-01 (L384) | Dòng có mốc nghiệp vụ **ngày N**, bản tin về INVOICE ngày N+1 | Các đợt worker + realtime ngày N+1 chạy | Không đợt nào lấy dòng (hiện trạng có chủ đích — RISK-XHD-03); cảnh báo ⛔ chờ CL-XHD-22 | P2 | Negative | NEW |
| SC-XHD-046 | Lịch worker | REQ-XHD-016 | DOC-v2.0-01 BR-XHD-01 (L385) | **Ngày cuối tháng**, dòng đủ điều kiện sau giờ chốt cuối | Hệ thống xử lý dòng | **Không** phát hành trong ngày cuối tháng (realtime cũng không xuất); dòng giữ BillNumber rỗng, hóa đơn thuộc tháng sau — phát hành ngày 1 tháng sau, BillDate = ngày phát hành (QC, chờ PM confirm) — đợt cụ thể ⛔ chờ CL-XHD-32 | P1 | Boundary | NEW |
| SC-XHD-047 | Lịch FPL | REQ-XHD-017 | DOC-v2.0-01 BR-XHD-01 (L387) | Đơn FPL đã qua delay 2h, đủ điều kiện | Tới mốc worker FPL kế tiếp (2h/lần) | Đơn được phát hành ở mốc đó (chu kỳ 2 giờ, đợt cuối 22:05 — BR-XHD-01; giờ các đợt trước 22:05 ⛔ chờ CL-XHD-05, giả định TP 0:05, 2:05 …) | P1 | Functional | NEW |
| SC-XHD-048 | Lịch FPL | REQ-XHD-017 | DOC-v2.0-01 BR-XHD-01 (L388) | Đơn FPL tạo trong ngày bị lỡ 2 mốc trước do delay | Tới mốc 22:05 | Mốc 22:05 quét toàn bộ 0h–22h, phát hành các đơn còn sót | P1 | Functional | NEW |
| SC-XHD-049 | Delay FPL | REQ-XHD-021 | DOC-v2.0-01 BR-XHD-03 (L399) | Đơn FPL đủ điều kiện nhưng mới tạo < 2 giờ | Worker FPL chạy | Đơn **chưa** phát hành ở mốc này; chờ mốc sau | P1 | Negative | NEW |
| SC-XHD-050 | Delay FPL | REQ-XHD-021 | DOC-v2.0-01 BR-XHD-03 (L399) | Đơn FPL, khách đã bấm Xuất hóa đơn và nhập thông tin; thời gian tạo đơn (Web admin) cách mốc chạy **1:59 / 2:00 / 2:01** | Worker FPL chạy | **1:59 chưa phát hành hóa đơn; 2:00 và 2:01 phát hành** (mốc = thời gian tạo đơn, trùng thời điểm ghi nhận của kênh ; áp **cả dòng dịch vụ và dòng thiết bị** — CL-XHD-04, 19/10/2026) | P2 | Boundary | NEW |
| SC-XHD-051 | Realtime FPL | REQ-XHD-026 | DOC-v2.0-01 BR-XHD-06 (L414) | Đơn FPL | Tín hiệu đến **sau 22h** | Xử lý ngay ở realtime | P1 | Functional | NEW |
| SC-XHD-052 | Realtime FPL | REQ-XHD-026 | DOC-v2.0-01 BR-XHD-06 (L414) | Đơn FPL | Tín hiệu đến **sau giờ chốt cuối chung nhưng trước 22h** | **Không** đi realtime; đi worker FPL (mốc kế tiếp / 22:05) | P1 | Negative | NEW |
| SC-XHD-053 | Delay FPL | REQ-XHD-014, REQ-XHD-021 | DOC-v2.0-01 BR-XHD-01 (L380) | Đơn kênh **khác FPL** mới tạo < 2 giờ, đủ điều kiện | Worker đợt chung chạy | Đơn phát hành bình thường — delay 2h và lịch 2h/lần chỉ áp FPL | P2 | Negative | NEW |
| SC-XHD-054 | Phân luồng | REQ-XHD-018 | DOC-v2.0-01 BR-XHD-02 (L392) | Kênh khác FPL | Tín hiệu đến **trước** giờ chốt đợt 1 | Xử lý ở worker đợt 1, không qua realtime | P1 | Functional | NEW |
| SC-XHD-055 | Phân luồng | REQ-XHD-018 | DOC-v2.0-01 BR-XHD-02 (L392) | Kênh khác FPL | Tín hiệu đến **sau** giờ chốt cuối trong ngày | Xử lý ngay ở realtime, lọc theo thời điểm nhận tín hiệu | P1 | Functional | NEW |
| SC-XHD-056 | Phân luồng | REQ-XHD-018 | DOC-v2.0-01 BR-XHD-02 (L392-393) | Kênh khác FPL | Tín hiệu đến **giữa** giờ chốt đợt 1 và đợt cuối | Không đi realtime; phát hành ở đợt worker kế tiếp; không phát hành 2 lần | P1 | Functional | NEW |
| SC-XHD-057 | Điều kiện phát hành | REQ-XHD-019 | DOC-v2.0-01 BR-XHD-03 (L397) | Đơn có DV | SPF gửi tín hiệu "đã thanh toán" | DV đủ điều kiện, được phát hành ở đợt / luồng tương ứng | P1 | Functional | NEW |
| SC-XHD-058 | Điều kiện phát hành | REQ-XHD-019 | DOC-v2.0-01 BR-XHD-03 (L397) | Đơn có DV **chưa thanh toán**, TB đã giao hoàn tất | Worker chạy | Chỉ TB phát hành; DV **không** phát hành | P1 | Negative | NEW |
| SC-XHD-059 | Điều kiện phát hành | REQ-XHD-019 | DOC-v2.0-01 BR-XHD-03 (L397) | Đơn có TB ở 2 phương thức A, B | Chỉ phương thức A có tín hiệu giao hàng hoàn tất | Chỉ TB phương thức A phát hành; TB phương thức B chờ tín hiệu riêng | P1 | Functional | NEW |
| SC-XHD-060 | Đơn TMĐT | REQ-XHD-020 | DOC-v2.0-01 BR-XHD-03 (L398) | Đơn Shopee/Tiktok có TB | TB giao hàng thành công | TB đủ điều kiện, phát hành (hồi quy Phase 1) | P1 | Regression | NEW |
| SC-XHD-061 | PĐK | REQ-XHD-022 | DOC-v2.0-01 BR-XHD-03 (L400) | Hợp đồng **tổ chức**, PĐK **đã duyệt**, ngày thường | Dòng đủ điều kiện, worker chạy | Hóa đơn được phát hành | P1 | Functional | NEW |
| SC-XHD-062 | PĐK | REQ-XHD-022 | DOC-v2.0-01 BR-XHD-03 (L400) | Hợp đồng tổ chức, PĐK **chưa duyệt**, ngày thường | Worker chạy | **Không** autobill; dòng giữ BillNumber rỗng | P1 | Negative | NEW |
| SC-XHD-063 | PĐK | REQ-XHD-022 | DOC-v2.0-01 BR-XHD-03 (L400) | Hợp đồng tổ chức, PĐK chưa duyệt, ngày thuộc **2 ngày cuối tháng** | Worker chạy | Hóa đơn **vẫn** phát hành (không xét PĐK) | P1 | Functional | NEW |
| SC-XHD-064 | PĐK | REQ-XHD-022 | DOC-v2.0-01 BR-XHD-03 (L400) | Hợp đồng tổ chức chưa duyệt PĐK; tháng 28 / 30 / 31 ngày | Worker chạy vào **ngày cuối −2**, **cuối −1**, **ngày cuối** | **Cuối −2: chặn; cuối −1 và ngày cuối: phát hành** (2 ngày lịch — CL-XHD-07 đã chốt) | P2 | Boundary | NEW |
| SC-XHD-065 | PĐK | REQ-XHD-022 | DOC-v2.0-01 BR-XHD-03 (L400) | **Hợp đồng** tổ chức chưa duyệt PĐK, hóa đơn bị chặn ở đợt trước | PĐK được duyệt, đợt worker sau chạy | **Không tự phát hành** ở đợt sau — "không autobill" = phải xuất hóa đơn tay (ngoài phạm vi); QC verify không phát hành (CL-XHD-07, 19/10/2026) | P2 | Functional | NEW |
| SC-XHD-066 | Hợp đồng con | REQ-XHD-023 | DOC-v2.0-01 BR-XHD-03 (L401) | Hợp đồng có gắn hợp đồng cha; DV đã thanh toán | Worker / realtime chạy | **Không** phát hành DV | P1 | Negative | NEW |
| SC-XHD-067 | Hợp đồng con | REQ-XHD-023 | DOC-v2.0-01 BR-XHD-03 (L401) | Hợp đồng con; TB đã giao hoàn tất | Worker / realtime chạy | **Không** phát hành TB | P1 | Negative | NEW |
| SC-XHD-068 | PĐK | REQ-XHD-022 | DOC-v2.0-01 BR-XHD-03 (L400) | Hợp đồng **cá nhân**, không có PĐK duyệt | Dòng đủ điều kiện, worker chạy | Hóa đơn phát hành bình thường — điều kiện PĐK chỉ áp hợp đồng tổ chức | P2 | Functional | NEW |
| SC-XHD-069 | Gộp worker | REQ-XHD-024 | DOC-v2.0-01 BR-XHD-05 (L406) | Đơn có ≥2 dòng DV cùng đủ điều kiện trong một đợt | Worker chạy | Các dòng gộp **1 hóa đơn** (1 BillNumber) | P1 | Functional | NEW |
| SC-XHD-070 | Gộp worker | REQ-XHD-024 | DOC-v2.0-01 BR-XHD-05 (L406) | Đơn có DV và TB cùng đủ điều kiện trong một đợt | Worker chạy | DV + TB gộp **1 hóa đơn** | P1 | Functional | NEW |
| SC-XHD-071 | Gộp worker | REQ-XHD-024 | DOC-v2.0-01 BR-XHD-05 (L407) | Đơn có DV đủ điều kiện, TB chưa giao | Worker chạy | Xuất hóa đơn cho DV; TB chờ đợt sau, ra hóa đơn riêng khi đủ điều kiện | P1 | Functional | NEW |
| SC-XHD-072 | Gộp worker | REQ-XHD-024 | DOC-v2.0-01 BR-XHD-05 (L406) | 2 đơn khác nhau cùng hợp đồng, cùng đủ điều kiện một đợt | Worker chạy | Ra **2 hóa đơn** — phạm vi gộp là đơn hàng | P2 | Negative | NEW |
| SC-XHD-073 | Realtime | REQ-XHD-025 | DOC-v2.0-01 BR-XHD-06 (L412-413) | Sau giờ chốt cuối; đơn có TB đã đủ điều kiện từ trước nhưng chưa xuất | Tín hiệu **thanh toán** đến | Realtime xuất ngay hóa đơn **chỉ gồm DV**; TB không được gộp | P1 | Functional | NEW |
| SC-XHD-074 | Realtime | REQ-XHD-025 | DOC-v2.0-01 BR-XHD-06 (L412) | Sau giờ chốt cuối; đơn có TB phương thức A, B và DV đã thanh toán chưa xuất | Tín hiệu giao hàng phương thức **A** đến | Hóa đơn chỉ gồm TB phương thức A | P1 | Functional | NEW |
| SC-XHD-075 | Realtime | REQ-XHD-025 | DOC-v2.0-01 BR-XHD-06 (L412-413) | Sau giờ chốt cuối | 2 tín hiệu của cùng đơn đến liên tiếp (thanh toán rồi giao hàng) | Ra **2 hóa đơn riêng**, mỗi hóa đơn đúng thành phần của tín hiệu | P2 | Functional | NEW |
| SC-XHD-076 | Chống trùng | REQ-XHD-027 | DOC-v2.0-01 BR-XHD-08 (L420) | Dòng DV đã có BillNumber | Đợt worker sau chạy | Dòng bị bỏ qua, không phát hành lại | P1 | Negative | NEW |
| SC-XHD-077 | Chống trùng | REQ-XHD-027 | DOC-v2.0-01 BR-XHD-08 (L418) | Đơn đã phát hành toàn bộ | Bản tin Kafka **lặp** cùng nội dung về lại | Không phát sinh hóa đơn mới | P1 | Negative | NEW |
| SC-XHD-078 | Chống trùng | REQ-XHD-027 | DOC-v2.0-01 BR-XHD-08 (L419) | 2 dòng TB cùng mã đơn + dịch vụ hóa đơn + gói, **khác phương thức triển khai** | Mỗi phương thức có tín hiệu giao hàng ở thời điểm khác | 2 lần phát hành hợp lệ, không bị coi là trùng | P1 | Functional | NEW |
| SC-XHD-079 | Chống trùng | REQ-XHD-027, REQ-XHD-002 | DOC-v2.0-01 BR-XHD-08 (L419) ↔ §C#3 (L649-651) | Đơn nhóm Tổng đài Oncall có cả "Thiết bị Oncall" và "Thiết bị IP phone" (cùng SubServiceType 31) | Cả 2 đủ điều kiện | Cả 2 dòng được phát hành, không bị coi là trùng (khóa chống trùng 2.2 không chứa SubServiceType — CL-XHD-11); tín hiệu giao map đúng dòng TB của mình ⛔ chờ CL-XHD-12 | P2 | Negative | NEW |
| SC-XHD-080 | Hợp lệ | REQ-XHD-028, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L425) | Đơn ở trạng thái **Đã hủy** | Worker chạy | Không phát hành hóa đơn; ghi log (CL-XHD-14) | P1 | Negative | NEW |
| SC-XHD-081 | Hợp lệ | REQ-XHD-028, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L425) | Đơn ở trạng thái **Đang cập nhật** (đơn chưa có thông tin hợp đồng) | Worker chạy | Không phát hành hóa đơn (trạng thái hợp lệ = "Bình thường" — CL-XHD-14, QC owner giữ case 19/10/2026) | P1 | Negative | NEW |
| SC-XHD-082 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | **Hợp đồng** ở trạng thái **Tạm ngưng** / **Đã chấm dứt** / **Ngưng vì lý do thanh toán** | Worker chạy | Không phát hành hóa đơn; ghi log (CL-XHD-14) | P1 | Negative | NEW |
| SC-XHD-083 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | Đơn thiếu **Sale Team** | Worker chạy | Không phát hành; ghi log | P1 | Negative | NEW |
| SC-XHD-084 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | Đơn thiếu **Sale Channel** | Worker chạy | Không phát hành; ghi log | P1 | Negative | NEW |
| SC-XHD-085 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | **Tên khách hàng** rỗng | Worker chạy | Không phát hành; ghi log | P1 | Negative | NEW |
| SC-XHD-086 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | **Loại hình KH cấp 1** rỗng | Worker chạy | Không phát hành; ghi log | P1 | Negative | NEW |
| SC-XHD-087 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | **Loại hình KH cấp 2** rỗng | Worker chạy | Không phát hành; ghi log | P1 | Negative | NEW |
| SC-XHD-088 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | **Địa chỉ xuất hóa đơn** rỗng | Worker chạy | Không phát hành; ghi log | P1 | Negative | NEW |
| SC-XHD-089 | Hợp lệ | REQ-XHD-029, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L426) | **LocationID = 0** / **= 1** | Worker chạy | **0: không phát hành + log; 1: phát hành** | P1 | Boundary | NEW |
| SC-XHD-090 | Hợp lệ | REQ-XHD-030, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L427) | **ID dịch vụ = 0** / **= 1** | Worker chạy | **0: không phát hành + log; 1: phát hành** | P1 | Boundary | NEW |
| SC-XHD-091 | Hợp lệ | REQ-XHD-030, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L427) | **ID nhóm dịch vụ = 0** / **= 1** | Worker chạy | **0: không phát hành + log; 1: phát hành** | P1 | Boundary | NEW |
| SC-XHD-092 | Hợp lệ | REQ-XHD-030, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L427) | **ID gói dịch vụ = 0** / **= 1** | Worker chạy | **0: không phát hành + log; 1: phát hành** | P1 | Boundary | NEW |
| SC-XHD-093 | Hợp lệ | REQ-XHD-030, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L427) | **ID chính sách = 0** / **= 1** | Worker chạy | **0: không phát hành + log; 1: phát hành** | P1 | Boundary | NEW |
| SC-XHD-094 | Hợp lệ | REQ-XHD-030, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L427) | **ID câu lệnh giá = 0** / **= 1** | Worker chạy | **0: không phát hành + log; 1: phát hành** | P1 | Boundary | NEW |
| SC-XHD-095 | Hợp lệ | REQ-XHD-030, REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L427) | Đơn **không có chương trình khuyến mãi** (ID = 0 / rỗng) / ID chương trình khuyến mãi **= 1** | Worker chạy | **Cả hai đều phát hành hóa đơn** — đơn không có khuyến mãi vẫn phát hành (CL-XHD-15, 19/10/2026) | P1 | Boundary | NEW |
| SC-XHD-096 | Hợp lệ | REQ-XHD-031 | DOC-v2.0-01 BR-XHD-10 (L428) | Dòng bị chặn ở đợt 1 vì thiếu thông tin | Thông tin được bổ sung trước giờ chốt đợt 2 | Đợt 2 cùng ngày phát hành dòng (worker quét dòng chưa xuất có mốc nghiệp vụ trong ngày — L384); không có hàng chờ phát hành lại | P2 | Functional | NEW |
| SC-XHD-097 | Job cảnh báo | REQ-XHD-032 | DOC-v2.0-01 BR-XHD-10 (L429) | Có đơn thiếu thông tin trước giờ chốt | Job cảnh báo chạy | Job chạy chu kỳ 15 phút; đầu ra cảnh báo ⛔ chờ CL-XHD-16 | P3 | Functional | NEW |
| SC-XHD-099 | Chi nhánh | REQ-XHD-034 | DOC-v2.0-01 BR-XHD-12 (L434) | Hợp đồng do chi nhánh X quản lý | Hóa đơn được phát hành | Chi nhánh xuất hóa đơn = X, lưu trên tồn xuất hóa đơn (`OB_OrderBill`) | P1 | Functional | NEW |
| SC-XHD-101 | Phát hành Billing | REQ-XHD-035 | DOC-v2.0-01 BR-XHD-13 (L439-440) | Dòng đủ điều kiện, mốc nghiệp vụ ngày N | Phát hành vào ngày N (hoặc N+1 với realtime qua nửa đêm) | Billing trả BillNumber; ghi BillNumber + BillDate = **ngày phát hành thực tế** vào tồn xuất hóa đơn | P1 | Integration | NEW |
| SC-XHD-102 | Nội dung hóa đơn | REQ-XHD-036 | DOC-v2.0-01 BR-XHD-13 (L441) | Dòng DV có số tháng sử dụng trên SPF | Hóa đơn được phát hành | Nội dung dòng = tên dịch vụ + số tháng; **không** có kỳ hạn từ ngày – đến ngày | P1 | Functional | NEW |
| SC-XHD-103 | Invoice Event | REQ-XHD-037 | DOC-v2.0-01 BR-XHD-13 (L442) | Hóa đơn vừa phát hành thành công | Sau khi ghi BillNumber | Invoice Event được gửi lên Kafka (kích hoạt điểm chạm b của GN và hậu kỳ HK) | P1 | Integration | NEW |
| SC-XHD-104 | Phát hành Billing | REQ-XHD-035 | DOC-v2.0-01 BR-XHD-13 (L439) | Billing lỗi / timeout (mock) | Worker gọi phát hành | **Không phát hành** (BillNumber rỗng); hệ thống ghi lỗi, dev retry bằng tay — không retry tự động (CL-XHD-18, 19/10/2026) | P2 | Negative | NEW |
| SC-XHD-105 | 1 đơn n hóa đơn | REQ-XHD-038 | DOC-v2.0-01 BR-XHD-14 (L446-447) | Đơn có DV + TB ở 2 phương thức, đủ điều kiện ở 3 thời điểm khác đợt | Lần lượt các đợt / realtime chạy | Đơn có **3 BillNumber**; `OB_OrderBill` liên kết đủ 3; mỗi hóa đơn có thể nhiều dòng | P1 | Functional | NEW |
| SC-XHD-106 | Bán thêm | REQ-XHD-040 | DOC-v2.0-04 mail PM | Hợp đồng đang hoạt động có đơn **bán thêm** (DV / TB) | Đơn đi qua các điều kiện phát hành như đơn bán mới | Xuất hóa đơn theo cùng rule đơn bán mới; hóa đơn gắn đúng đơn bán thêm (CL-XHD-25, 19/10/2026) | P1 | Functional | NEW |
| SC-XHD-107 | Cutover | REQ-XHD-041 | DOC-v2.0-02 BR-DB-08 (L302) | Đơn đã ra hóa đơn ở luồng cũ (v1), kiểm tra chéo đang bật | Bản tin của đơn về luồng mới | Luồng mới **không** xử lý đơn — ⛔ chờ CL-XHD-24 (STG có luồng cũ không) | P2 | Regression | NEW |
| SC-XHD-108 | Cutover | REQ-XHD-041 | DOC-v2.0-02 BR-DB-08 (L300) | Cả 2 luồng cùng đọc Kafka | 1 bản tin được luồng mới ghi | Luồng cũ không ghi bản tin đó (và ngược lại) — ⛔ chờ CL-XHD-24 | P2 | Regression | NEW |
| SC-XHD-109 | HT triển khai | REQ-XHD-043 | DOC-v2.0-05 dòng 8 | Đơn có TB DeployType = "Không" (và đơn mix "Không" + TIN/PNC) | Không có / có phiếu thi công TINPNC | QC: xuất hóa đơn khi đơn hoàn tất — chưa có căn cứ URD ⛔ chờ CL-XHD-27, CL-XHD-34 | P2 | Functional | NEW |
| SC-XHD-110 | Điều kiện phát hành | REQ-XHD-019, REQ-XHD-025 | DOC-v2.0-01 BR-XHD-06 (L412) ↔ BR-DB-07 (L374) | Đơn có **2 TB cùng phương thức** triển khai A; DV đã phát hành | Tín hiệu giao hàng hoàn tất của A chỉ mang **TB1** (giao thiếu TB2) | Chỉ TB1 phát hành; TB2 giữ BillNumber rỗng, chờ tín hiệu riêng (CL-XHD-10) | P1 | Functional | NEW |
| SC-XHD-111 | Hợp lệ | REQ-XHD-031, REQ-XHD-015 | DOC-v2.0-01 BR-XHD-10 (L428) ↔ BR-XHD-01 (L384) | Dòng bị chặn trong ngày N vì thiếu thông tin | Thông tin được bổ sung **sau giờ chốt cuối ngày N** (hoặc ngày N+1) | Hệ thống **không** tự phát hành lại dòng ở các đợt sau (không giữ chờ — CL-XHD-17); dòng giữ BillNumber rỗng | P2 | Negative | NEW |

#### Source Detail per Scenario (verbatim quotes — `references/quoting-guide.md`)

> Given/When/Then đã ở bảng trên — block dưới **không lặp** lại, chỉ giữ quote justify + ghi chú dẫn xuất.
> SC-XHD-001..017 dùng chung khung; quote riêng là dòng kênh trong bảng §A.2.

##### SC-XHD-001 · Ma trận — kênh Mobile (1)
📍 `DOC-v2.0-01 §A.2 · L85-87`

> 1 | Mobile | Mobile

↳ **Ghi chú:** 1 lớp EP kênh. Dữ liệu nhân ra TC: 20 nhóm DV §A.3 × {bán mới, bán thêm}.

---

##### SC-XHD-002 · Ma trận — kênh Desktop (2)
📍 `DOC-v2.0-01 §A.2 · L88-90`

> 2 | Desktop | Desktop

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-003 · Ma trận — kênh DKOL (4)
📍 `DOC-v2.0-01 §A.2 · L91-93`

> 4 | DKOL | DKOL

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-004 · Ma trận — kênh API (7)
📍 `DOC-v2.0-01 §A.2 · L94-96`

> 7 | API | Dùng cho các partner ngoài FTEL (TGDD,..)

↳ **Ghi chú:** Kênh partner — mô tả nhắc TGDD trong khi TGDD (14) là kênh riêng; cách tạo đơn trên STG cần hỏi (TP §2.1b).

---

##### SC-XHD-005 · Ma trận — kênh W-Sale (9)
📍 `DOC-v2.0-01 §A.2 · L97-99`

> 9 | W-Sale | W-Sale

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-006 · Ma trận — kênh FPL (10)
📍 `DOC-v2.0-01 §A.2 · L100-102`

> 10 | FPL | FPT Play

↳ **Ghi chú:** Kênh duy nhất có lịch, delay, thông tin KH riêng — các SC FPL (SC-XHD-031..034, 047..053) dựa trên đơn tạo ở SC này.

---

##### SC-XHD-007 · Ma trận — kênh VNTT (11)
📍 `DOC-v2.0-01 §A.2 · L103-105`

> 11 | VNTT | VNTT

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-008 · Ma trận — kênh MBBank (12)
📍 `DOC-v2.0-01 §A.2 · L106-108`

> 12 | MBBank | MB Bank

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-009 · Ma trận — kênh CRM (13)
📍 `DOC-v2.0-01 §A.2 · L109-111`

> 13 | CRM | CRM

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-010 · Ma trận — kênh TGDD (14)
📍 `DOC-v2.0-01 §A.2 · L112-114`

> 14 | TGDD | Thế Giới Di Động

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-011 · Ma trận — kênh F-Retail (15)
📍 `DOC-v2.0-01 §A.2 · L115-117`

> 15 | F-Retail | FPT Shop

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-012 · Ma trận — kênh CMR-App (16)
📍 `DOC-v2.0-01 §A.2 · L118-120`

> 16 | CMR-App | FSS

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-013 · Ma trận — kênh Momo (17)
📍 `DOC-v2.0-01 §A.2 · L121-123`

> 17 | Momo | Momo

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-014 · Ma trận — kênh SR-KPDV (18)
📍 `DOC-v2.0-01 §A.2 · L124-126`

> 18 | SR-KPDV | SR KPDV

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-015 · Ma trận — kênh HiFPT (19)
📍 `DOC-v2.0-01 §A.2 · L127-129`

> 19 | HiFPT | HiFPT

↳ **Ghi chú:** Như SC-XHD-001.

---

##### SC-XHD-016 · Ma trận — kênh Shopee (20)
📍 `DOC-v2.0-01 §A.2 · L130-133`

> 20 | Shopee | Shopee | Đã triển khai ver1.0Có điều chinh ver2.0

↳ **Ghi chú:** "Có điều chỉnh ver2.0" ⇒ vừa test mới vừa hồi quy Phase 1 (TP §3.2: gắn R2). Điều chỉnh cụ thể là gì URD không liệt kê (CL-XHD-31).

---

##### SC-XHD-017 · Ma trận — kênh Tiktok (21)
📍 `DOC-v2.0-01 §A.2 · L134-137`

> 21 | Tiktok | Tiktok | Đã triển khai v1.0Có điều chỉnh v2.0

↳ **Ghi chú:** Như SC-XHD-016.

---

##### SC-XHD-018 · Sự kiện thanh toán từ SPF
📍 `DOC-v2.0-01 §I.c BR-DB-01 · L345`

> Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng.

↳ **Ghi chú:** Positive cho sự kiện "thanh toán"; kết quả cuối cùng (phát hành DV) kiểm ở SC-XHD-057.

---

##### SC-XHD-019 · Sự kiện hủy đơn chưa có hóa đơn
📍 `DOC-v2.0-01 §I.c BR-DB-01 · L345` + `BR-XHD-10 · L425`

> Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng.
> Đơn không ở trạng thái hủy hoặc đang cập nhật.

↳ **Ghi chú:** Hủy đơn khi **chưa** có hóa đơn ⇒ trạng thái hủy chặn phát hành. Hủy khi **đã** có hóa đơn: ngoài scope test (TP §2.2 #2 — SC-XHD-098 deprecated 19/10/2026).

---

##### SC-XHD-020 · Sự kiện tạo đơn / cập nhật thông tin KH
📍 `DOC-v2.0-01 §I.c BR-DB-01 · L345` ↔ `BR-DB-03 · L359`

> Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng.

↳ **Ghi chú:** SPF chỉ gửi thanh toán, hủy đơn; thông tin khách lấy từ hợp đồng lúc phát hành (CL-XHD-01 resolved 19/10/2026) ⇒ SC verify hóa đơn in thông tin mới nhất của hợp đồng.

---

##### SC-XHD-021 · Tín hiệu từ phiếu thi công
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L349`

> phiếu thi công (tình trạng "Đã xử lý hoàn tất")

↳ **Ghi chú:** Nguồn 1/3. Theo `DOC-v2.0-05`, phương thức TIN/PNC và FTI dùng phiếu thi công.

---

##### SC-XHD-022 · Tín hiệu từ Vendor
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L349`

> Vendor (khi đối tác giao xong)

↳ **Ghi chú:** Nguồn 2/3. Theo `DOC-v2.0-05`, phương thức NCC (Samsung / Sony / Casper) đi qua đơn đặt hàng Vendor.

---

##### SC-XHD-023 · Tín hiệu từ phiếu giao tại quầy
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L349`

> phiếu giao tại quầy.

↳ **Ghi chú:** Nguồn 3/3. Theo `DOC-v2.0-05`, phương thức Quầy và Sale dùng phiếu giao dịch thiết bị tại quầy.

---

##### SC-XHD-024 · Đủ 6 trường của tín hiệu
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L350`

> Tín hiệu gồm mã đơn, ServiceCode, SubserviceType, phương thức triển khai, nguồn gửi và thời gian hoàn tất.

↳ **Ghi chú:** Verify dữ liệu ghi nhận có đủ 6 trường; tên cột chờ schema (CL-XHD-29).

---

##### SC-XHD-025 · Không ràng buộc nguồn ↔ phương thức
📍 `DOC-v2.0-01 §I.c BR-DB-07 · L376`

> Nguồn gửi được lưu lại để đối soát; không ràng buộc nguồn nào được báo cho phương thức triển khai nào.

↳ **Ghi chú:** Nguồn "lệch" vẫn được chấp nhận; nguồn thực tế được lưu.

---

##### SC-XHD-026 · Tín hiệu không khớp khóa
📍 `DOC-v2.0-01 §I.c BR-DB-07 · L375`

> Nếu thiết bị đã có hóa đơn hoặc không khớp khóa thì không ghi nhận, chỉ ghi log nội dung tín hiệu vào cột Note.

↳ **Ghi chú:** Nhánh "không khớp khóa". Expected chỉ định tính được tới khi có format cột Note (CL-XHD-19).

---

##### SC-XHD-027 · Tín hiệu cho TB đã có hóa đơn
📍 `DOC-v2.0-01 §I.c BR-DB-07 · L375`

> Nếu thiết bị đã có hóa đơn hoặc không khớp khóa thì không ghi nhận, chỉ ghi log nội dung tín hiệu vào cột Note.

↳ **Ghi chú:** Nhánh "đã có hóa đơn" — cũng là ca giao bù trong cùng phương thức.

---

##### SC-XHD-028 · Khớp 3/4 thành phần khóa
📍 `DOC-v2.0-01 §I.c BR-DB-07 · L374`

> Map theo bộ khóa mã đơn + ServiceCode + SubserviceType + phương thức triển khai, cho phần thiết bị chưa xuất hóa đơn.

↳ **Ghi chú:** Lớp EP "sai đúng 1 thành phần" — chọn phương thức vì đó là thành phần phân biệt các lần phát hành TB.

---

##### SC-XHD-029 · Đơn TMĐT — mốc đã thanh toán + Paid tạm
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L351`

> Với đơn TMĐT, tín hiệu hoàn tất thanh toán là lúc SPF đánh dấu đơn "đã thanh toán"; cùng lúc đó Paid được ghi nhận ở trạng thái gạch nợ tạm.

↳ **Ghi chú:** SC tích hợp XHD ↔ GN; nửa gạch nợ tạm kiểm ở SC-GN-019.

---

##### SC-XHD-030 · Thông tin KH theo hợp đồng
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L355`

> Mặc định lấy theo thông tin trên hợp đồng.

↳ **Ghi chú:** Verify bằng cách cho thông tin trên đơn khác hợp đồng — hóa đơn phải in thông tin hợp đồng.

---

##### SC-XHD-031 · FPL — khách lấy hóa đơn, nhập đủ trong 2 giờ
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L357`

> Nếu khách chọn lấy hóa đơn thì dùng thông tin khách tự nhập: tên, email, số điện thoại, mã số thuế, mã định danh, mã quan hệ ngân sách, số hộ chiếu.

↳ **Ghi chú:** Positive FPL. 7 trường đối chiếu với các ô "Mã số thuế KH", "Mã định danh", "Mã QHNS", "Số hộ chiếu" của màn `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png).

---

##### SC-XHD-032 · FPL — biên 2 giờ nhập thông tin
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L358`

> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** "Tối đa 2 giờ" ⇒ 2:00 hợp lệ, quá 2:00 chặn. Kênh FPL chặn: quá 2 giờ nút Xuất hóa đơn bị ẩn (CL-XHD-02, CL-XHD-03 resolved 19/10/2026).

---

##### SC-XHD-033 · FPL — khách không lấy hóa đơn
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L356`

> Ngoại lệ: kênh bán FPL cho khách chọn có lấy hóa đơn hay không (ví dụ FPL).

↳ **Ghi chú:** Khách không bấm Xuất hóa đơn trong 2 giờ ⇒ không phát hành hóa đơn (CL-XHD-02 resolved 19/10/2026).

---

##### SC-XHD-034 · FPL — quá 2 giờ không nhập
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L358`

> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** Nhánh hết hạn — nút bị ẩn, không phát hành hóa đơn (CL-XHD-02 resolved 19/10/2026).

---

##### SC-XHD-035 · Cập nhật thông tin KH không kích hoạt phát hành
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L359`

> Cập nhật thông tin khách không kích hoạt phát hành hóa đơn

↳ **Ghi chú:** Kiểm không có hóa đơn / Invoice Event sinh ra ngay sau cập nhật.

---

##### SC-XHD-036 · Lần phát hành sau dùng thông tin mới nhất
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L359`

> lần phát hành tiếp theo dùng thông tin mới nhất.

↳ **Ghi chú:** Cần đơn có ≥2 lần phát hành (DV trước, TB sau) để thấy khác biệt.

---

##### SC-XHD-037 · ProductType quyết định DV/TB
📍 `DOC-v2.0-01 §I.c BR-DB-04 · L363-364`

> SPF gắn sẵn ProductType (DV/TB) trên từng dòng chi tiết khi đồng bộ đơn.
> INVOICE dùng trường này, không tự suy diễn.

↳ **Ghi chú:** Có thể dùng dòng có `Type` §A.3 "lệch" với ProductType để chứng minh INVOICE không suy diễn (chờ CL-XHD-13 xác nhận có ca này).

---

##### SC-XHD-038 · Phát hành theo bản tin cuối
📍 `DOC-v2.0-01 §I.c BR-DB-05 · L368`

> Một đơn có thể được đồng bộ nhiều lần; lần đẩy cuối là thông tin mới nhất.

↳ **Ghi chú:** Thay đổi chỉ cho phép ở thông tin KH sau khi thanh toán — dữ liệu khác nhau nên ở thông tin KH.

---

##### SC-XHD-039 · Phần đã xuất bất biến
📍 `DOC-v2.0-01 §I.c BR-DB-05 · L369`

> Chỉ xuất hóa đơn cho phần chưa có hóa đơn; phần đã xuất không bị ghi đè, xóa hay phát hành lại.

↳ **Ghi chú:** So sánh dữ liệu dòng đã có BillNumber trước/sau bản tin mới.

---

##### SC-XHD-040 · Lưu thời điểm nhận bản tin
📍 `DOC-v2.0-01 §I.c BR-DB-05 · L370`

> INVOICE ghi lại thời điểm nhận mỗi bản tin để phân luồng worker hoặc realtime.

↳ **Ghi chú:** Tiền đề của SC-XHD-055 (realtime lọc theo thời điểm nhận).

---

##### SC-XHD-041 · Đợt 1
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L382`

> Giá trị áp dụng: chia 2 đợt, đợt 1 chốt 12:00 chạy 12:05; đợt 2 chốt 18:00 chạy 18:05

↳ **Ghi chú:** Positive đợt 1. TP §3.2: chỉnh lịch trên STG để không phải chờ giờ thật.

---

##### SC-XHD-042 · Đợt 2 quét lại phần còn sót
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L384`

> Mỗi đợt quét các dòng chưa xuất hóa đơn có mốc nghiệp vụ trong ngày, trước giờ chốt của đợt.

↳ **Ghi chú:** "Trong ngày, trước giờ chốt" ⇒ không có chặn dưới giữa các đợt.

---

##### SC-XHD-043 · Biên giờ chốt
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L384`

> Mỗi đợt quét các dòng chưa xuất hóa đơn có mốc nghiệp vụ trong ngày, trước giờ chốt của đợt.

↳ **Ghi chú:** "Trước giờ chốt" ⇒ đúng giờ chốt **không** thuộc đợt (suy diễn theo chữ "trước", cần dev xác nhận phép so sánh `<` hay `<=`).

---

##### SC-XHD-044 · Lịch là tham số
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L381, L383`

> Mỗi đợt gồm giờ chốt và giờ chạy worker; số đợt cũng là tham số.
> Sau giai đoạn pilot sẽ đánh giá lại; nếu cần thì cấu hình lại tham số worker.

↳ **Ghi chú:** Kiểm cấu hình được trên STG — cũng là cách test các SC thời gian.

---

##### SC-XHD-045 · Bản tin trễ qua ngày không được xử lý
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L384`

> Mỗi đợt quét các dòng chưa xuất hóa đơn có mốc nghiệp vụ trong ngày, trước giờ chốt của đợt.

↳ **Ghi chú:** Ghi nhận hiện trạng có chủ đích; mail cảnh báo là REQ-XHD-042 chưa có SC.

---

##### SC-XHD-046 · Cuối tháng sau giờ chốt cuối
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L385`

> Đơn đủ điều kiện sau giờ chốt cuối của ngày cuối tháng sẽ phát hành sang tháng sau, ảnh hưởng kỳ ghi nhận doanh thu.

↳ **Ghi chú:** CL-XHD-06 đã chốt (16/10/2026): không phát hành trong tháng, sang tháng sau — ngoại lệ của realtime ngày cuối tháng. Đợt nào của tháng sau phát hành: CL-XHD-32.

---

##### SC-XHD-047 · FPL worker 2h/lần
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L387`

> 2h quét 1 lần

↳ **Ghi chú:** Mốc cụ thể chưa có (CL-XHD-05).

---

##### SC-XHD-048 · FPL mốc 22:05
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L388`

> Mốc 22:05 chốt từ 0h đến 22 giờ (Do FPL có rule delay 2h nên phải bổ sung khung giờ để quét hết những case không quét được do delay ở hai khung giờ trước)

↳ **Ghi chú:** Mốc vét — phạm vi quét 0h–22h.

---

##### SC-XHD-049 · FPL chưa đủ delay 2h
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L399`

> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

↳ **Ghi chú:** Negative: đơn chưa đủ 2h không phát hành.

---

##### SC-XHD-050 · Biên delay 2h
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L399`

> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

↳ **Ghi chú:** Biên 1:59 / 2:00 / 2:01 — "đủ 2h" được hiểu là ≥ 2h (suy diễn). Mốc = thời gian tạo đơn xem trên Web admin, trùng thời điểm ghi nhận của kênh; áp cả dòng dịch vụ và dòng thiết bị (CL-XHD-04, 19/10/2026). Khách không bấm Xuất hóa đơn trong 2 giờ ⇒ không phát hành (CL-XHD-02).

---

##### SC-XHD-051 · FPL realtime sau 22h
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L414`

> Đối với Kênh bán FPL chỉ realtime từ sau mốc 22h

↳ **Ghi chú:** Positive realtime FPL.

---

##### SC-XHD-052 · FPL không realtime trước 22h
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L414`

> Đối với Kênh bán FPL chỉ realtime từ sau mốc 22h

↳ **Ghi chú:** Khoảng 18:00–22:00 là vùng FPL khác kênh khác — lớp EP dễ sai nhất.

---

##### SC-XHD-053 · Kênh khác FPL không áp delay / lịch 2h
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L380`

> Dùng chung một lịch cho mọi ngày và mọi kênh bán khác FPL

↳ **Ghi chú:** Negative chứng minh rule FPL không lan sang kênh khác.

---

##### SC-XHD-054 · Trước giờ chốt → worker
📍 `DOC-v2.0-01 §I.c BR-XHD-02 · L392`

> Tín hiệu về trước giờ chốt của đợt thì xử lý ở worker; về sau giờ chốt cuối trong ngày thì xử lý ở realtime.

↳ **Ghi chú:** Lớp EP 1/3.

---

##### SC-XHD-055 · Sau giờ chốt cuối → realtime
📍 `DOC-v2.0-01 §I.c BR-XHD-02 · L392-393`

> về sau giờ chốt cuối trong ngày thì xử lý ở realtime.
> Worker lọc theo mốc nghiệp vụ, realtime lọc theo thời điểm nhận tín hiệu, hai luồng không trùng nhau.

↳ **Ghi chú:** Lớp EP 2/3.

---

##### SC-XHD-056 · Giữa các đợt → worker đợt kế tiếp
📍 `DOC-v2.0-01 §I.c BR-XHD-02 · L392-393`

> Worker lọc theo mốc nghiệp vụ, realtime lọc theo thời điểm nhận tín hiệu, hai luồng không trùng nhau.

↳ **Ghi chú:** Lớp EP 3/3 — chỉ "sau giờ chốt **cuối**" mới vào realtime.

---

##### SC-XHD-057 · DV phát hành khi đã thanh toán
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L397`

> Dịch vụ: khi có tín hiệu "đã thanh toán" từ SPF.

↳ **Ghi chú:** Positive ĐK DV.

---

##### SC-XHD-058 · DV chưa thanh toán không phát hành
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L397`

> Hai điều kiện xét độc lập và dùng chung cho mọi kênh bán.

↳ **Ghi chú:** Hệ quả trực tiếp của câu "hai điều kiện xét độc lập" (L397).

---

##### SC-XHD-059 · TB phát hành theo đúng phương thức
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L397`

> Thiết bị: khi có tín hiệu giao hàng hoàn tất của phương thức triển khai tương ứng (phiếu thi công, Vendor, quầy).

↳ **Ghi chú:** CL-XHD-10 đã chốt (16/10/2026): chỉ phát hành TB có trong tín hiệu — ca giao thiếu cùng phương thức ở SC-XHD-110.

---

##### SC-XHD-060 · Đơn TMĐT — TB khi giao hàng thành công
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L398`

> Đơn TMĐT: dịch vụ khi SPF đánh dấu đơn "đã thanh toán"; thiết bị khi giao hàng thành công.

↳ **Ghi chú:** Hồi quy Phase 1.

---

##### SC-XHD-061 · Hợp đồng tổ chức đã duyệt PĐK
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`

> Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK

↳ **Ghi chú:** Positive PĐK.

---

##### SC-XHD-062 · Hợp đồng tổ chức chưa duyệt PĐK
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`

> Quên duyệt PĐK thì không autobill.

↳ **Ghi chú:** Negative ngày thường. Đầu ra khi chặn (log?) chưa đặc tả.

---

##### SC-XHD-063 · 2 ngày cuối tháng bỏ qua PĐK
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`

> hai ngày cuối tháng không xét điều kiện này.

↳ **Ghi chú:** Ngoại lệ thời gian của rule PĐK.

---

##### SC-XHD-064 · Biên 2 ngày cuối tháng
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`

> hai ngày cuối tháng không xét điều kiện này.

↳ **Ghi chú:** Biên theo tháng 28/30/31 ngày; "2 ngày cuối" = 2 ngày lịch cuối cùng (CL-XHD-07 đã chốt 16/10/2026).

---

##### SC-XHD-065 · Duyệt PĐK muộn
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`

> Quên duyệt PĐK thì không autobill.

↳ **Ghi chú:** "Không autobill" = phải xuất hóa đơn tay (ngoài phạm vi) ⇒ không tự phát hành ở đợt sau (CL-XHD-07, 19/10/2026).

---

##### SC-XHD-066 · Hợp đồng con — DV
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L401`

> Không phát hành hóa đơn trên hợp đồng con, cả thiết bị và dịch vụ.

↳ **Ghi chú:** Nhánh DV.

---

##### SC-XHD-067 · Hợp đồng con — TB
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L401`

> Hợp đồng con: nhận diện hợp đồng con khi hợp đồng có gắn hợp đồng cha (hợp đồng dự án).

↳ **Ghi chú:** Nhánh TB; dữ liệu cần hợp đồng có trường "hợp đồng cha".

---

##### SC-XHD-068 · Hợp đồng cá nhân không xét PĐK
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`

> Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK

↳ **Ghi chú:** Lớp EP "không phải hợp đồng tổ chức" — chứng minh rule không chặn nhầm. Cách nhận diện tổ chức: CL-XHD-07.

---

##### SC-XHD-069 · Gộp nhiều dòng DV
📍 `DOC-v2.0-01 §I.c BR-XHD-05 · L406`

> Trong cùng một đợt, các dòng DV/TB đủ điều kiện của cùng một đơn gộp vào một hóa đơn.

↳ **Ghi chú:** DV + DV.

---

##### SC-XHD-070 · Gộp DV + TB
📍 `DOC-v2.0-01 §I.c BR-XHD-05 · L406`

> Trong cùng một đợt, các dòng DV/TB đủ điều kiện của cùng một đơn gộp vào một hóa đơn.

↳ **Ghi chú:** DV + TB.

---

##### SC-XHD-071 · Chỉ một thành phần đủ điều kiện
📍 `DOC-v2.0-01 §I.c BR-XHD-05 · L407`

> Chỉ một thành phần đủ điều kiện thì xuất thành phần đó, phần còn lại chờ đợt sau.

↳ **Ghi chú:** Tạo tiền đề cho 1 đơn n hóa đơn (SC-XHD-105).

---

##### SC-XHD-072 · Không gộp khác đơn
📍 `DOC-v2.0-01 §I.c BR-XHD-05 · L406`

> các dòng DV/TB đủ điều kiện của cùng một đơn gộp vào một hóa đơn.

↳ **Ghi chú:** "Của cùng một đơn" ⇒ 2 đơn cùng hợp đồng vẫn 2 hóa đơn.

---

##### SC-XHD-073 · Realtime — tín hiệu thanh toán chỉ ra DV
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L412`

> tín hiệu thanh toán chỉ phát hành dịch vụ

↳ **Ghi chú:** Phân biệt với worker (SC-XHD-070 gộp).

---

##### SC-XHD-074 · Realtime — tín hiệu giao hàng chỉ ra TB của phương thức
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L412`

> tín hiệu giao hàng chỉ phát hành thiết bị của phương thức triển khai đó.

↳ **Ghi chú:** DV đã thanh toán chưa xuất cũng không được gộp kèm.

---

##### SC-XHD-075 · Realtime — mỗi tín hiệu 1 hóa đơn
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L412-413`

> Mỗi tín hiệu chỉ phát hành đúng thành phần gắn với tín hiệu đó
> Xử lý ngay khi nhận, không chờ đợt worker kế tiếp.

↳ **Ghi chú:** Hai tín hiệu liên tiếp ⇒ hai hóa đơn.

---

##### SC-XHD-076 · Dòng đã có BillNumber bị bỏ qua
📍 `DOC-v2.0-01 §I.c BR-XHD-08 · L420`

> Dòng đã có BillNumber thì bỏ qua.

↳ **Ghi chú:** Negative cơ bản của chống trùng.

---

##### SC-XHD-077 · Bản tin Kafka lặp
📍 `DOC-v2.0-01 §I.c BR-XHD-08 · L418`

> Mỗi dòng DV/TB trên một đơn chỉ xuất hóa đơn một lần.

↳ **Ghi chú:** Case tích hợp: log Kafka trùng (TP §3.1 Exploratory).

---

##### SC-XHD-078 · Khác phương thức không phải trùng
📍 `DOC-v2.0-01 §I.c BR-XHD-08 · L419`

> thiết bị thêm phương thức triển khai.

↳ **Ghi chú:** Phương thức là thành phần khóa của TB.

---

##### SC-XHD-079 · SubServiceType 31 trùng
📍 `DOC-v2.0-01 §C#3 · L649-651`

> SubServiceType 31 trùng ở hai dịch vụ của nhóm Tổng đài Oncall (Thiết bị Oncall, Thiết bị IP phone).
> Mục A.3, BR-DB-07, BR-XHD-08
> Khóa chống trùng có dùng SubServiceType nên có thể làm hai dòng bị coi là trùng.

↳ **Ghi chú:** Khóa chống trùng chốt theo 2.2 (CL-XHD-11) nên không còn trùng ở bước phát hành; rủi ro còn lại ở bước map tín hiệu BR-DB-07 (CL-XHD-12).

---

##### SC-XHD-080 · Đơn hủy
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L425`

> Đơn không ở trạng thái hủy hoặc đang cập nhật.

↳ **Ghi chú:** Lớp trạng thái 1/2.

---

##### SC-XHD-081 · Đơn đang cập nhật
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L425`

> Đơn không ở trạng thái hủy hoặc đang cập nhật.

↳ **Ghi chú:** Lớp trạng thái 2/2.

---

##### SC-XHD-082 · Hợp đồng không có hiệu lực
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> Thông tin chung phải đủ: hợp đồng có hiệu lực

↳ **Ghi chú:** Trạng thái đơn hàng không hợp lệ: Đã hủy, Đang cập nhật; trạng thái hợp đồng không hợp lệ: Tạm ngưng, Đã chấm dứt, Ngưng vì lý do thanh toán (CL-XHD-14 resolved 19/10/2026).

---

##### SC-XHD-083 · Thiếu Sale Team
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> Sale Team

↳ **Ghi chú:** Trích đoạn trong danh sách L426.

---

##### SC-XHD-084 · Thiếu Sale Channel
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> Sale Channel

↳ **Ghi chú:** Trích đoạn trong danh sách L426.

---

##### SC-XHD-085 · Tên KH rỗng
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> tên khách hàng

↳ **Ghi chú:** Trích đoạn trong danh sách L426.

---

##### SC-XHD-086 · Loại hình KH cấp 1 rỗng
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> loại hình khách hàng cấp 1 và cấp 2

↳ **Ghi chú:** Cấp 1.

---

##### SC-XHD-087 · Loại hình KH cấp 2 rỗng
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> loại hình khách hàng cấp 1 và cấp 2

↳ **Ghi chú:** Cấp 2.

---

##### SC-XHD-088 · Địa chỉ xuất hóa đơn rỗng
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> địa chỉ xuất hóa đơn

↳ **Ghi chú:** Trích đoạn trong danh sách L426.

---

##### SC-XHD-089 · LocationID biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`

> LocationID > 0.

↳ **Ghi chú:** BVA 0 / 1 (giá trị âm cùng lớp với 0).

---

##### SC-XHD-090 · ID dịch vụ biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`

> Chi tiết từng dịch vụ phải có các ID dịch vụ, nhóm dịch vụ, gói dịch vụ, chính sách, câu lệnh giá, chương trình khuyến mãi > 0.

↳ **Ghi chú:** BVA 0 / 1 cho ID dịch vụ.

---

##### SC-XHD-091 · ID nhóm dịch vụ biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`

> nhóm dịch vụ

↳ **Ghi chú:** BVA 0 / 1.

---

##### SC-XHD-092 · ID gói dịch vụ biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`

> gói dịch vụ

↳ **Ghi chú:** BVA 0 / 1.

---

##### SC-XHD-093 · ID chính sách biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`

> chính sách

↳ **Ghi chú:** BVA 0 / 1.

---

##### SC-XHD-094 · ID câu lệnh giá biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`

> câu lệnh giá

↳ **Ghi chú:** BVA 0 / 1.

---

##### SC-XHD-095 · ID chương trình khuyến mãi biên
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`

> chương trình khuyến mãi > 0.

↳ **Ghi chú:** Đơn không có chương trình khuyến mãi vẫn phát hành (CL-XHD-15 resolved 19/10/2026).

---

##### SC-XHD-096 · Bổ sung thông tin rồi đợt sau
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L428`

> hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

↳ **Ghi chú:** CL-XHD-17 đã chốt theo 2.2 (16/10/2026): còn trong ngày thì đợt sau vẫn lấy; qua ngày thì không phát hành lại (SC-XHD-111).

---

##### SC-XHD-097 · Job cảnh báo 15 phút
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L429`

> Job cảnh báo chạy 15 phút một lần để bổ sung thông tin kịp trước giờ chốt.

↳ **Ghi chú:** P3 — chỉ kiểm được chu kỳ chạy.

---

##### SC-XHD-099 · Chi nhánh theo hợp đồng
📍 `DOC-v2.0-01 §I.c BR-XHD-12 · L434`

> Chi nhánh xuất hóa đơn là chi nhánh quản lý hợp đồng, xác định tại thời điểm phát hành và lưu trên tồn xuất hóa đơn

↳ **Ghi chú:** Verify cột chi nhánh trên `OB_OrderBill` (glossary L313).

---

##### SC-XHD-101 · BillNumber + BillDate thực tế
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L439-440`

> Phát hành qua Billing System, ghi BillNumber và BillDate vào giỏ tồn xuất hóa đơn
> BillDate là ngày phát hành thực tế.

↳ **Ghi chú:** Ca realtime qua nửa đêm cho thấy rõ BillDate ≠ mốc nghiệp vụ.

---

##### SC-XHD-102 · Nội dung hóa đơn
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L441`

> Nội dung hiển thị trên hóa đơn là tên dịch vụ + số tháng sử dụng (lấy từ SPF), không hiển thị kỳ hạn từ ngày – đến ngày.

↳ **Ghi chú:** Ảnh FIG-01 (ảnh: Chi tiết hóa đơn.png) (màn hiện hữu) vẫn có "Từ ngày / Đến ngày" — CL-XHD-28.

---

##### SC-XHD-103 · Gửi Invoice Event
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L442`

> Sau đó gửi Invoice Event để gạch nợ và xử lý hậu kỳ.

↳ **Ghi chú:** Điểm nối GN SC-GN-009 và HK SC-HK-001.

---

##### SC-XHD-104 · Billing lỗi / timeout
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L439`

> Phát hành qua Billing System, ghi BillNumber và BillDate vào giỏ tồn xuất hóa đơn

↳ **Ghi chú:** Billing lỗi / timeout: ghi lỗi, dev retry bằng tay; QC verify không phát hành (CL-XHD-18 resolved 19/10/2026).

---

##### SC-XHD-105 · Một đơn ba hóa đơn
📍 `DOC-v2.0-01 §I.c BR-XHD-14 · L446-447`

> Một đơn có thể có nhiều BillNumber; một hóa đơn có thể chứa nhiều dòng DV/TB.
> Nguyên nhân: đơn được xuất ở nhiều đợt (dịch vụ khi thanh toán, thiết bị theo từng phương thức triển khai).

↳ **Ghi chú:** SC E2E gom kết quả của 057, 059, 071.

---

##### SC-XHD-106 · Đơn bán thêm
📍 `DOC-v2.0-04 mail PM · dòng 3 danh sách`

> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** Mỗi chức năng khác có SC bán thêm riêng ở GN/HK; ở XHD chiều bán thêm còn nằm trong dữ liệu ma trận SC-XHD-001..017.

---

##### SC-XHD-107 · Cutover — kiểm tra chéo luồng cũ
📍 `DOC-v2.0-02 §I.c BR-DB-08 · L302`

> Trong giai đoạn đầu sau khi go-live, luồng mới kiểm tra chéo trên dữ liệu cũ ở MỨC ĐƠN HÀNG: nếu Đơn hàng đã ra hóa đơn ở luồng cũ thì luồng mới không xử lý đơn đó nữa.

↳ **Ghi chú:** Nội dung từ URD 2.1 (2.2 chuyển Phụ lục D#1) — dùng lại 19/10/2026 (CL-XHD-24).

---

##### SC-XHD-108 · Cutover — một bản tin một luồng
📍 `DOC-v2.0-02 §I.c BR-DB-08 · L300`

> Kafka dùng chung một nguồn bản tin; mỗi bản tin chỉ được xử lý bởi một trong hai luồng — đã ghi qua luồng mới thì không ghi qua luồng cũ và ngược lại.

↳ **Ghi chú:** Như SC-XHD-107.

---

##### SC-XHD-109 · TB có HT triển khai "Không"
📍 `DOC-v2.0-05 sheet "1. HT Triển khai" · STT 8`

> - Phiếu thi công: triển khai bởi TINPNC nếu hàng hóa có mix HT "Không" và "TIN/PNC"
> - None: không đẩy triển khai, giao hàng nếu hàng hóa, dịch vụ trên đơn hàng chỉ có "Không"

↳ **Ghi chú:** TB "Không" không có tín hiệu giao hàng ⇒ theo BR-XHD-03 sẽ không bao giờ đủ điều kiện. Cần BA xác nhận (CL-XHD-27).

---

##### SC-XHD-110 · Giao thiếu TB cùng phương thức
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L412` ↔ `BR-DB-07 · L374`

> Mỗi tín hiệu chỉ phát hành đúng thành phần gắn với tín hiệu đó: tín hiệu thanh toán chỉ phát hành dịch vụ; tín hiệu giao hàng chỉ phát hành thiết bị của phương thức triển khai đó.

↳ **Ghi chú:** Tín hiệu map vào từng TB theo khóa (BR-DB-07) ⇒ TB không có trong tín hiệu thì chưa đủ điều kiện. Thêm 16/10/2026 sau khi CL-XHD-10 chốt.

---

##### SC-XHD-111 · Bổ sung thông tin sau khi qua ngày
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L428`

> Không hợp lệ thì không phát hành và ghi log; hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

↳ **Ghi chú:** Qua ngày thì không phát hành lại (CL-XHD-17). Thêm 16/10/2026.

## Scenarios — CARRIED (reference only)

| Scenario ID | Tên ngắn | Module | Origin Version | Priority | Reference |
|-------------|----------|--------|---------------|----------|-----------|
| — | *(v2.0 là version đầu tiên trong workspace — chưa có CARRIED)* | — | — | — | — |

## Scenarios — DEPRECATED

| Scenario ID | Tên ngắn | Module | Deprecated ở | Lý do |
|-------------|----------|--------|-------------|-------|
| SC-XHD-098 | Hủy đơn đã có hóa đơn — hóa đơn không tự hủy / điều chỉnh | XHD | v2.0 (19/10/2026) | ⛔ **Ngoài scope test — TP §2.2 #2** *"Điều chỉnh / hủy hóa đơn khi hủy đơn đã có hóa đơn"* (BR-XHD-10 L430: xử lý theo quy trình riêng). QC owner 19/10/2026 |
| SC-XHD-100 | Đổi chi nhánh giữa 2 lần phát hành — hóa đơn cũ không tự điều chỉnh | XHD | v2.0 (19/10/2026) | ⛔ **Ngoài scope test — TP §2.2 #3** *"Điều chỉnh hóa đơn đã phát hành khi chi nhánh đổi giữa các lần phát hành"*. QC owner 19/10/2026 |
