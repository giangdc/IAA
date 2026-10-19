---
id: v2.0/XHD/changelog
title: Changelog — Module XHD
type: changelog
version: v2.0
sprint: —
module:
  code: XHD
  dir: XHD
  name: Đồng bộ đơn hàng & xuất hóa đơn tự động
doc_source:
  - id: DOC-v2.0-01
    section: "§A.1 · §A.2 · §A.3 · §A.5 · §B.I · §C · §D"
  - id: DOC-v2.0-04
    section: "mail PM 13/10/2026"
  - id: DOC-v2.0-05
    section: "sheet \"1. HT Triển khai\""
  - id: DOC-v2.0-FIG-01
    section: "màn \"Chi tiết của hóa đơn\""
  - id: DOC-v2.0-FIG-02
    section: "màn \"Liệt kê cước của thuê bao\""
  - id: DOC-v2.0-FIG-03
    section: "flow §B.I.b"
id_range:
  req: REQ-XHD-001..043
  sc: "SC-XHD-001..111 (NEW)"
  cl: CL-XHD-01..34
  risk: RISK-XHD-01..10
status: ANALYZED
updated: 2026-10-19
---

# Changelog — Module XHD (`XHD`)

> Tạo bởi: analyze-requirements (**layout v2** — 1 file / module, ở cùng thư mục với 5 deliverable còn lại).
> **Đây là đích write-back của LỊCH SỬ.** Mọi lượt `--init` / `--sweep` / `--update` / `--delta` chạm module này ghi **1 dòng bảng ở §1**.
> ⛔ **KHÔNG nối banner *"Cập nhật lần cuối"* vào đầu các file deliverable khác** — banner đó là lịch sử, thuộc về §1 file này dưới dạng 1 dòng bảng.

> 🔴 **`id_range` là trường BẮT BUỘC.** ⛔ KHÔNG suy sprint từ số ID — quy chiếu bằng đường dẫn `v2.0/XHD/`.

## 1. Lịch sử thay đổi

| Ngày | Loại | Thay đổi | Nguồn / Lý do | Ảnh hưởng |
|---|---|---|---|---|
| 2026-10-16 | INIT | Phân tích lần đầu §A.2, §A.3, §B.I, §C, §D — 43 REQ (`001..043`), 109 SC (P1 84 · P2 24 · P3 1), 31 CL (4 BLOCKING), 10 RISK. Điểm nghiệp vụ đáng chú ý nhất: URD 2.2 rút gọn làm nảy sinh nhiều mâu thuẫn nội bộ (sự kiện đồng bộ, khóa chống trùng, cuối tháng ↔ realtime) — 21 SC có Then phụ thuộc CL | `DOC-v2.0-01` (URD 2.2) + URD 2.1 (đã bỏ) + `DOC-v2.0-04`, `-05`, `-FIG-01` (ảnh: Chi tiết hóa đơn.png) | Dựng đủ 5 deliverable + CHANGELOG |
| 2026-10-16 | UPDATE | **Đóng** CL-XHD-06 (cuối tháng sau giờ chốt cuối ⇒ sang tháng sau), 09 (KH Chuỗi không có rule riêng), 10 (chỉ phát hành TB có trong tín hiệu), 17 (theo 2.2, câu 2.1 hết hiệu lực). **Rõ một phần** CL-XHD-02, 04, 05, 07, 08, 11 (khóa chống trùng theo 2.2 ⇒ hết BLOCKING). +CL-XHD-32 (đợt phát hành dòng cuối tháng ở tháng sau). +SC-XHD-110, 111; sửa Then SC-XHD-046, 047, 064, 079, 096. Ghi chú QC cho CL-XHD-01, 03, 12–16, 18, 20; bằng chứng flow cho CL-XHD-21 | QC trả lời 20/49 CL vòng 1 (file Excel câu hỏi) + flow URD §B.I.b (`DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png)) | SC 109→111 · CL 31→32 (28 Open · 3 BLOCKING) · blocked_by_cl 21→19 |
| 2026-10-16 | UPDATE | **Bỏ URD 2.1 — không sử dụng, xoá nội dung 2.1 khỏi analyze:** xoá mọi trích dẫn / ghi chú 2.1; SC-XHD-020 bỏ giả định "4 sự kiện như 2.1"; **deprecated SC-XHD-107, 108** (cutover — căn cứ chỉ có ở 2.1); REQ-XHD-041, 042 bỏ nguồn 2.1; mốc nghiệp vụ DV/TB thành chưa định nghĩa; +CL-XHD-33 (Phụ lục D trỏ về 2.1). Ràng buộc §2 #1 thay mới | QC owner yêu cầu 16/10/2026 (URD 2.1 đã out) | SC active 111→109 (deprecated 2) · CL 32→33 (29 Open) · blocked_by_cl 19→17 |
| 2026-10-19 | UPDATE | Bổ sung tool verify vào `test_data_catalog.md` §Ghi chú chung (đường dẫn menu ở `07_environments/environments.md`). Không đổi REQ / SC / CL | QC owner cung cấp 19/10/2026 | Không |
| 2026-10-19 | UPDATE | +CL-XHD-34 (Open): đơn DV kèm TB — DV phát hành khi thanh toán (BR-XHD-03) hay chờ đơn hoàn tất (flow QC test); TB triển khai "Không" lấy tín hiệu nào. Không đổi SC — chờ BA | QC owner yêu cầu hỏi BA 19/10/2026 | CL 33→34 · cl_open 29→30 |
| 2026-10-19 | UPDATE | QC trả lời CL vòng 2: **đóng** CL-XHD-20, 25, 28, 30 · **làm rõ một phần** CL-XHD-14, 15, 19, 27, 31, 32. SC-XHD-106 hết chờ CL (bán thêm = rule chung); SC-XHD-081, 095, 109, 046 cập nhật Then (vẫn chờ CL). Ghi chú chung: QC không xem được log ⇒ Then "ghi log" chỉ verify hành vi. Câu dính URD 2.1 (CL-XHD-22, 23, 24) **chưa cập nhật** — chờ QC owner chốt dùng 2.1 cho Phụ lục D | QC trả lời 19/10/2026 (file câu hỏi vòng 2) | cl_open 30→26 · blocked_by_cl 17→16 |
| 2026-10-19 | UPDATE | **Dùng lại URD 2.1 cho Phụ lục D** (trừ D#4, 7, 8, 9): CL-XHD-22, 23, 24 làm rõ một phần theo RISK-01, BR-XHD-09, BR-DB-08 của 2.1 (CL-XHD-22 vẫn BLOCKING — mail chưa đặc tả); **SC-XHD-107, 108 dùng lại** (bỏ deprecated, vẫn chờ CL-XHD-24 về luồng cũ trên STG) | QC owner chốt 19/10/2026 | SC 109→111 · deprecated 2→0 · P2 23→25 · blocked_by_cl 16→18 |
| 2026-10-19 | SCOPE↓ | Đánh dấu **ngoài scope test** theo TP §2.2 (chỉ đọc TP): **SC-XHD-098** (hủy đơn đã có HĐ — #2), **SC-XHD-100** (đổi chi nhánh, HĐ cũ không tự điều chỉnh — #3) → deprecated; REQ-XHD-033 không còn SC; REQ-XHD-034 giữ SC-XHD-099 | QC owner 19/10/2026 + TP §2.2 #2, #3 | SC 111→109 · deprecated 0→2 · P1 85→84 · P2 25→24 |
| 2026-10-19 | UPDATE | Gắn nhãn **ngoài scope test** (TP §2.2 #4 — thuộc tính chi nhánh được bán SP / DV) tại REQ-XHD-034 và CL-XHD-26; vốn không có SC nào cho phần này. Không đổi REQ / SC / CL | QC owner 19/10/2026 + TP §2.2 #4 | Không |
| 2026-10-19 | UPDATE | Dọn chữ cũ theo TP §2.2 (chỉ đọc TP): REQ-XHD-041 + RISK-XHD-10 ghi kiểm tra chéo cutover trong scope (URD 2.1 BR-DB-08, SC-XHD-107, 108), **quét tay bổ sung ngoài scope test (TP #8)**; §3 Nợ #6 CL-XHD-30 → ngoài scope (TP #6). Không đổi REQ / SC / CL | QC owner 19/10/2026 | Không |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⚠️ **URD 2.1 (`DOC-v2.0-02`) chỉ dùng cho các mục Phụ lục D của URD 2.2 trỏ về** (QC owner chốt 19/10/2026 — thay ràng buộc 16/10 "2.1 không sử dụng"): dùng D#1 cutover, D#2 chống phát hành trùng, D#3 RISK-01, D#5 ký hiệu / ID / đơn vị đầu số riêng, D#6 dòng chiết khấu / thông tin theo mẫu. ⛔ **Không dùng:** D#4 cấu hình EVC (QC owner: không đụng tới), D#7 mapping chi nhánh, D#8 câu hỏi mục V, D#9 autobill TB theo phương thức (2.2 ghi không còn áp dụng / đã bỏ). Phần chính 2.2 thắng khi mâu thuẫn. Chỉ cập nhật các CL QC owner chỉ định (CL-XHD-22, 23, 24 · CL-HK-02, 03, 10) | QC owner 19/10/2026 | Dùng 2.1 ngoài các mục trên (hoặc cho D#4) ⇒ TC kiểm theo nội dung đã bỏ, bug bị bác |
| 2 | ⛔ **Giờ chốt / giờ chạy / số đợt / lịch FPL là tham số** — SC và TC viết "giờ chốt đợt N", không hardcode 12:00/18:00 | BR-XHD-01 L381, L383; Project_rule §Test Data Rules | Pilot đổi tham số ⇒ toàn bộ TC thời gian sai expected, phải viết lại |
| 3 | ⚠️ **Số dòng `L<n>` trong Source Location** là số dòng của bản trích text do `scripts/doc/search-doc.sh` sinh từ `.docx` (mỗi đoạn / ô bảng = 1 dòng). Đổi file `.docx` ⇒ L-number lệch | Cách trích ở `scripts/doc/search-doc.sh` | Reviewer mở sai vị trí; health-check F-05 báo quote không khớp — phải chạy lại verify quote (đã verify 100% quote URD ngày 2026-10-16) |
| 4 | ⚠️ **Risk xuyên suốt đặt ở XHD** (RISK-XHD-01 tài liệu tích hợp · RISK-XHD-02 phát hành trùng · RISK-XHD-10 cutover; CL-XHD-25 bán thêm · CL-XHD-29 tích hợp · CL-XHD-31 URD v1.0) — ảnh hưởng cả **GN** và **HK** | Layout v2 không có `_global/`; XHD là module đầu chuỗi | Sửa / đóng ở module khác ⇒ 2 home cho cùng nội dung, drift; GN/HK chỉ được **trỏ** về đây |
| 5 | ⛔ **TL (URD §IV — tính lương FPT Play SA) ngoài phạm vi** — không dựng thư mục `v2.0/TL/`, 0 REQ/SC là đúng | QC lead chốt 14/10/2026 (TP §2.2 #11) | Dựng TL ⇒ health-check báo module thiếu TC; effort ngoài kế hoạch |
| 6 | ⚠️ **`DOC-v2.0-05` (HT Triển khai) và `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png), `-FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png)` (ảnh màn Hệ thống Thông tin, HĐ 2025) không phải URD** — chỉ dùng làm dữ liệu / câu hỏi; không sinh rule mới từ chúng khi chưa có BA xác nhận | Tài liệu bổ sung, không version, chưa có người duyệt | Sinh expected theo file bổ sung ⇒ TC mâu thuẫn URD, bug sai căn cứ |
| 7 | ⚠️ **SC-XHD-001..017** fan-out theo **kênh**; chiều nhóm DV × loại đơn là **dữ liệu** — không tách thêm SC theo nhóm DV | Sufficiency Rule (1 lớp EP / SC); TP F01 680 TC | Tách SC theo nhóm ⇒ 340 SC trùng hành vi, vượt trần 200 SC/version |
| 8 | ⛔ **Câu trả lời vòng 1 của QC không phải xác nhận PO** — chỉ đóng CL khi chốt được bằng chữ URD 2.2; còn lại ghi `🔎 QC rà lại` và giữ Open | Người trả lời là QC owner, cột "Người trả lời" trống | Đóng CL theo ý kiến QC chưa có căn cứ ⇒ TC sai expected, bug bị dev bác |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 REQ-XHD-039 (BR-XHD-18 clear "thuê thiết bị đầu cuối") **chưa có SC** | URD 1 câu, "kịp plan" — CL-XHD-21 ⛔ | PM trả lời GAP-53 → `/analyze-requirements --update` thêm SC hoặc đánh dấu Out-scope |
| 2 | 🔴 REQ-XHD-042 (mail cảnh báo bản tin trễ qua ngày) **chưa có SC** | "Bắt buộc" nhưng không đặc tả — CL-XHD-22 ⛔ | PM trả lời GAP-02/11 → `--update` |
| 3 | 🔴 CL-XHD-29 tài liệu tích hợp (payload / schema / enum) chặn setup data + execute | GAP-07 chưa trả lời | Xin SDD trước setup 23/10/2026; chưa có ⇒ verify định tính |
| 4 | 🟡 CL-XHD-11 khóa chống trùng — đã chốt theo 2.2 (16/10/2026), còn field dữ liệu | Hết BLOCKING; field chờ schema CL-XHD-29 | Có schema ⇒ điền field vào `test_data_catalog` |
| 5 | 🟡 17 SC có Then `⛔ chờ CL-…` / `(giả định TP)` (đếm ở `counts.blocked_by_cl`) | Theo giả định của TP §2.4 | Khi CL resolved: `--update` sửa Then, ghi 1 dòng UPDATE ở §1 |
| 6 | ✅ CL-XHD-30 đơn ngoài 17 kênh / ServiceID 2, 22 — **ngoài scope test** (TP §2.2 #6 + QC trả lời vòng 2 "bỏ qua không test") ⇒ không thêm SC negative | Đóng 19/10/2026 | — |
| 7 | 🟡 CL-XHD-27, CL-XHD-28 mới phát hiện khi analyze (chưa có GAP-ID) | Chưa đưa vào DOC-READINESS / TP §2.4 | QC owner thêm vào danh sách gửi PM (create-test-plan `--update`) |
