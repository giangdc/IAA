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
  - id: DOC-v2.0-02
    section: "§II (luồng A–D, đối tượng dữ liệu, BR-VC-07, BR-GC-04/05) — tham chiếu"
id_range:
  req: REQ-GN-001..020
  sc: "SC-GN-001..050 (NEW)"
  cl: CL-GN-01..09
  risk: RISK-GN-01..06
status: ANALYZED
updated: 2026-10-16
---

# Changelog — Module GN (`GN`)

> Tạo bởi: analyze-requirements (**layout v2** — 1 file / module, ở cùng thư mục với 5 deliverable còn lại).
> **Đây là đích write-back của LỊCH SỬ.** Mọi lượt `--init` / `--sweep` / `--update` / `--delta` chạm module này ghi **1 dòng bảng ở §1**.
> ⛔ **KHÔNG nối banner *"Cập nhật lần cuối"* vào đầu các file deliverable khác.**

> 🔴 **`id_range` là trường BẮT BUỘC.** ⛔ KHÔNG suy sprint từ số ID — quy chiếu bằng đường dẫn `v2.0/GN/`.

## 1. Lịch sử thay đổi

| Ngày | Loại | Thay đổi | Nguồn / Lý do | Ảnh hưởng |
|---|---|---|---|---|
| 2026-10-16 | INIT | Phân tích lần đầu §B.II — 20 REQ (`001..020`), 50 SC (P1 42 · P2 7 · P3 1), 9 CL (1 BLOCKING), 6 RISK. Điểm nghiệp vụ đáng chú ý nhất: ranh giới INVOICE ↔ đội EVC (Paid voucher, thứ tự gạch EVC / tiền khách) chưa rõ — nguy cơ gạch trùng | `DOC-v2.0-01` §B.II + `DOC-v2.0-02` §II | Dựng đủ 5 deliverable + CHANGELOG |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⛔ **Gạch nợ bằng EVC ngoài phạm vi** — chỉ test phần INVOICE: không ghi Payment EVC (SC-GN-045) và chừa tiền lock (SC-GN-046, 047) | BR-VC L545; TP §2.2 #5; mail PM "EVC cần test => theo rule URD" | Viết TC kiểm trần 50% / Config EVC (D#4) ⇒ test hệ thống của đội EVC, FAIL không thuộc INVOICE |
| 2 | ⚠️ **Kênh sàn = {20 Shopee, 21 Tiktok}** là giả định (CL-GN-03) | 2.2 không đánh dấu kênh sàn; 2.1 L125 | BA thêm kênh ⇒ SC-GN-011, 012, 019, 020 thiếu lớp EP; gạch tạm sai kênh không bị phát hiện |
| 3 | ⚠️ **Tài liệu tích hợp / payload Kafka Out / enum** dùng chung CL-XHD-29, RISK-XHD-01 — home ở `XHD/` | Layout v2 không có `_global/` | Mở CL trùng ở GN ⇒ 2 home, drift trạng thái |
| 4 | ⚠️ Thuật ngữ thống nhất "**gỡ gạch nợ tạm**" (2.2) — không dùng "hất nợ tạm" / "xóa gạch nợ tạm" của 2.1 | BR-NT-04 L501 | TC / bug dùng 3 tên ⇒ khó trace, review-tc báo không nhất quán |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 CL-GN-01 Paid voucher có bị loại khỏi gạch nợ — chặn TC nhánh Paid có voucher (SC-GN-048) | GAP-40, đã đưa vào rủi ro TP #7 | Hỏi BA trước generate-tc 21/10/2026 |
| 2 | 🔴 CL-GN-08 thứ tự đội EVC ↔ INVOICE ở nhánh Paid — mới phát hiện, chưa có GAP | Câu "gạch EVC trước" của 2.1 không còn ở 2.2 | QC owner thêm vào danh sách gửi PM |
| 3 | 🟡 5 SC có Then `⛔ chờ CL-…` | Theo giả định TP | Khi CL resolved: `--update` |
| 4 | 🟡 Mock API kênh thanh toán / đội EVC / consumer Kafka Out chưa có | TP Entry Criteria | Chuẩn bị trước R1 (26/10/2026) |
