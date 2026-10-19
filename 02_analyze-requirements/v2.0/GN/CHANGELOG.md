---
id: v2.0/GN/changelog
title: Changelog — Module GN
type: changelog
version: v2.0
sprint: —
module:
  code: GN
  dir: GN
  name: Gạch nợ hóa đơn
doc_source:
  - id: DOC-v2.0-01
    section: "§A.5 #6–#9 · §B.II"
  - id: DOC-v2.0-FIG-04
    section: "flow §B.II.b"
id_range:
  req: REQ-GN-001..020
  sc: "SC-GN-001..050 (NEW; 049 deprecated)"
  cl: CL-GN-01..10
  risk: RISK-GN-01..06
status: ANALYZED
updated: 2026-10-19
---

# Changelog — Module GN (`GN`)

> Tạo bởi: analyze-requirements (**layout v2** — 1 file / module, ở cùng thư mục với 5 deliverable còn lại).
> **Đây là đích write-back của LỊCH SỬ.** Mọi lượt `--init` / `--sweep` / `--update` / `--delta` chạm module này ghi **1 dòng bảng ở §1**.
> ⛔ **KHÔNG nối banner *"Cập nhật lần cuối"* vào đầu các file deliverable khác.**

> 🔴 **`id_range` là trường BẮT BUỘC.** ⛔ KHÔNG suy sprint từ số ID — quy chiếu bằng đường dẫn `v2.0/GN/`.

## 1. Lịch sử thay đổi

| Ngày | Loại | Thay đổi | Nguồn / Lý do | Ảnh hưởng |
|---|---|---|---|---|
| 2026-10-16 | INIT | Phân tích lần đầu §B.II — 20 REQ (`001..020`), 50 SC (P1 42 · P2 7 · P3 1), 9 CL (1 BLOCKING), 6 RISK. Điểm nghiệp vụ đáng chú ý nhất: ranh giới INVOICE ↔ đội EVC (Paid voucher, thứ tự gạch EVC / tiền khách) chưa rõ — nguy cơ gạch trùng | `DOC-v2.0-01` §B.II + URD 2.1 §II | Dựng đủ 5 deliverable + CHANGELOG |
| 2026-10-16 | UPDATE | Đối chiếu flow §B.II.b (`DOC-v2.0-FIG-04` (ảnh: FLOW GẠCH NỢ HÓA ĐƠN – ĐỒNG BỘ PAID.png)): mọi ghi chú trong ảnh khớp BR đã phân tích (BR-DP-01, BR-XL-01/03, BR-NT, BR-GN, BR-GC) — **không đổi** REQ / SC / CL | Flow URD 2.2 người dùng bổ sung | Không |
| 2026-10-16 | UPDATE | **Bỏ URD 2.1 — không sử dụng, xoá nội dung 2.1 khỏi analyze:** xoá mọi trích dẫn / ghi chú 2.1; kênh sàn {20, 21} chuyển căn cứ sang URD 2.2 §A.1 L59; test data PaidType / loại cọc / bảng tồn cọc bỏ phần lấy từ 2.1; +CL-GN-10 (D#4 + đối tượng dữ liệu trỏ về 2.1). Không đổi SC | QC owner yêu cầu 16/10/2026 | CL 9→10 |
| 2026-10-19 | UPDATE | Bổ sung tool verify vào `test_data_catalog.md` §Ghi chú chung (đường dẫn menu ở `07_environments/environments.md`). Không đổi REQ / SC / CL | QC owner cung cấp 19/10/2026 | Không |
| 2026-10-19 | UPDATE | QC trả lời CL vòng 2: **đóng** CL-GN-02, 03 · **làm rõ một phần** CL-GN-01 (hết BLOCKING: Paid voucher được dùng gạch nợ), 05, 07, 09. SC-GN-048 đổi Then (Negative→Functional, hết chờ CL); **deprecated SC-GN-049** (STG không test API EVC lỗi / timeout); SC-GN-030, 050 cập nhật ghi chú | QC trả lời 19/10/2026 (file câu hỏi vòng 2) | SC 50→49 (deprecated 1) · P2 7→6 · cl_open 10→8 · cl_blocking 1→0 · blocked_by_cl 5→3 |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⛔ **Gạch nợ bằng EVC ngoài phạm vi** — chỉ test phần INVOICE: không ghi Payment EVC (SC-GN-045) và chừa tiền lock (SC-GN-046, 047) | BR-VC L545; TP §2.2 #5; mail PM "EVC cần test => theo rule URD" | Viết TC kiểm trần 50% / Config EVC (D#4) ⇒ test hệ thống của đội EVC, FAIL không thuộc INVOICE |
| 2 | ⚠️ **Kênh sàn = {20 Shopee, 21 Tiktok}** là giả định (CL-GN-03) | 2.2 không đánh dấu kênh sàn; 2.1 L125 | BA thêm kênh ⇒ SC-GN-011, 012, 019, 020 thiếu lớp EP; gạch tạm sai kênh không bị phát hiện |
| 3 | ⚠️ **Tài liệu tích hợp / payload Kafka Out / enum** dùng chung CL-XHD-29, RISK-XHD-01 — home ở `XHD/` | Layout v2 không có `_global/` | Mở CL trùng ở GN ⇒ 2 home, drift trạng thái |
| 4 | ⚠️ Thuật ngữ thống nhất "**gỡ gạch nợ tạm**" (2.2) — không dùng "hất nợ tạm" / "xóa gạch nợ tạm" của 2.1 | BR-NT-04 L501 | TC / bug dùng 3 tên ⇒ khó trace, review-tc báo không nhất quán |
| 5 | ⛔ **URD 2.1 KHÔNG SỬ DỤNG từ 16/10/2026** (QC owner: tài liệu đã out) — chỉ URD 2.2 (`DOC-v2.0-01`) là căn cứ; mọi trích dẫn / ghi chú / dữ liệu lấy từ 2.1 **đã xoá** khỏi file module (bản cũ: `git show ec53583:<path>`). Thay ràng buộc cũ "2.2 thắng 2.1; 2.1 dùng cho phụ lục D" | Yêu cầu QC owner 16/10/2026 | Dựng expected / dữ liệu test theo 2.1 ⇒ TC kiểm theo tài liệu đã out, bug bị bác; phần 2.2 trỏ về 2.1 phải hỏi PO (CL-XHD-33, CL-GN-10, CL-HK-10) |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 CL-GN-01 Paid voucher có bị loại khỏi gạch nợ — chặn TC nhánh Paid có voucher (SC-GN-048) | GAP-40, đã đưa vào rủi ro TP #7 | Hỏi BA trước generate-tc 21/10/2026 |
| 2 | 🔴 CL-GN-08 thứ tự đội EVC ↔ INVOICE ở nhánh Paid — mới phát hiện, chưa có GAP | Câu "gạch EVC trước" của 2.1 không còn ở 2.2 | QC owner thêm vào danh sách gửi PM |
| 3 | 🟡 5 SC có Then `⛔ chờ CL-…` | Theo giả định TP | Khi CL resolved: `--update` |
| 4 | 🟡 Mock API kênh thanh toán / đội EVC / consumer Kafka Out chưa có | TP Entry Criteria | Chuẩn bị trước R1 (26/10/2026) |
