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
  - id: DOC-v2.0-02
    section: "§I (BR-DB-08, BR-XHD-04, 09, 11, RISK-01) — tham chiếu"
  - id: DOC-v2.0-04
    section: "mail PM 13/10/2026"
  - id: DOC-v2.0-05
    section: "sheet \"1. HT Triển khai\""
  - id: DOC-v2.0-FIG-01
    section: "màn \"Chi tiết của hóa đơn\""
  - id: DOC-v2.0-FIG-02
    section: "màn \"Liệt kê cước của thuê bao\""
id_range:
  req: REQ-XHD-001..043
  sc: "SC-XHD-001..109 (NEW)"
  cl: CL-XHD-01..31
  risk: RISK-XHD-01..10
status: ANALYZED
updated: 2026-10-16
---

# Changelog — Module XHD (`XHD`)

> Tạo bởi: analyze-requirements (**layout v2** — 1 file / module, ở cùng thư mục với 5 deliverable còn lại).
> **Đây là đích write-back của LỊCH SỬ.** Mọi lượt `--init` / `--sweep` / `--update` / `--delta` chạm module này ghi **1 dòng bảng ở §1**.
> ⛔ **KHÔNG nối banner *"Cập nhật lần cuối"* vào đầu các file deliverable khác** — banner đó là lịch sử, thuộc về §1 file này dưới dạng 1 dòng bảng.

> 🔴 **`id_range` là trường BẮT BUỘC.** ⛔ KHÔNG suy sprint từ số ID — quy chiếu bằng đường dẫn `v2.0/XHD/`.

## 1. Lịch sử thay đổi

| Ngày | Loại | Thay đổi | Nguồn / Lý do | Ảnh hưởng |
|---|---|---|---|---|
| 2026-10-16 | INIT | Phân tích lần đầu §A.2, §A.3, §B.I, §C, §D — 43 REQ (`001..043`), 109 SC (P1 84 · P2 24 · P3 1), 31 CL (4 BLOCKING), 10 RISK. Điểm nghiệp vụ đáng chú ý nhất: URD 2.2 rút gọn làm nảy sinh nhiều mâu thuẫn nội bộ (sự kiện đồng bộ, khóa chống trùng, cuối tháng ↔ realtime) — 21 SC có Then phụ thuộc CL | `DOC-v2.0-01` (URD 2.2) + `DOC-v2.0-02` (2.1, tham chiếu) + `DOC-v2.0-04`, `-05`, `-FIG-01` | Dựng đủ 5 deliverable + CHANGELOG |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⛔ **URD 2.2 (`DOC-v2.0-01`) thắng 2.1 (`DOC-v2.0-02`)** khi mâu thuẫn; 2.1 chỉ dùng cho nội dung 2.2 chuyển sang phụ lục D | Project_rule §Project Info; DOC-READINESS §0 | Quote/expected theo 2.1 ở BR đã đổi (vd khóa chống trùng BR-XHD-08) ⇒ TC kiểm sai khóa, FAIL oan hoặc bỏ lọt trùng |
| 2 | ⛔ **Giờ chốt / giờ chạy / số đợt / lịch FPL là tham số** — SC và TC viết "giờ chốt đợt N", không hardcode 12:00/18:00 | BR-XHD-01 L381, L383; Project_rule §Test Data Rules | Pilot đổi tham số ⇒ toàn bộ TC thời gian sai expected, phải viết lại |
| 3 | ⚠️ **Số dòng `L<n>` trong Source Location** là số dòng của bản trích text do `scripts/doc/search-doc.sh` sinh từ `.docx` (mỗi đoạn / ô bảng = 1 dòng). Đổi file `.docx` ⇒ L-number lệch | Cách trích ở `scripts/doc/search-doc.sh` | Reviewer mở sai vị trí; health-check F-05 báo quote không khớp — phải chạy lại verify quote (đã verify 100% quote URD ngày 2026-10-16) |
| 4 | ⚠️ **Risk xuyên suốt đặt ở XHD** (RISK-XHD-01 tài liệu tích hợp · RISK-XHD-02 phát hành trùng · RISK-XHD-10 cutover; CL-XHD-25 bán thêm · CL-XHD-29 tích hợp · CL-XHD-31 URD v1.0) — ảnh hưởng cả **GN** và **HK** | Layout v2 không có `_global/`; XHD là module đầu chuỗi | Sửa / đóng ở module khác ⇒ 2 home cho cùng nội dung, drift; GN/HK chỉ được **trỏ** về đây |
| 5 | ⛔ **TL (URD §IV — tính lương FPT Play SA) ngoài phạm vi** — không dựng thư mục `v2.0/TL/`, 0 REQ/SC là đúng | QC lead chốt 14/10/2026 (TP §2.2 #11) | Dựng TL ⇒ health-check báo module thiếu TC; effort ngoài kế hoạch |
| 6 | ⚠️ **`DOC-v2.0-05` (HT Triển khai) và `DOC-v2.0-FIG-01`, `-FIG-02` (ảnh màn Hệ thống Thông tin, HĐ 2025) không phải URD** — chỉ dùng làm dữ liệu / câu hỏi; không sinh rule mới từ chúng khi chưa có BA xác nhận | Tài liệu bổ sung, không version, chưa có người duyệt | Sinh expected theo file bổ sung ⇒ TC mâu thuẫn URD, bug sai căn cứ |
| 7 | ⚠️ **SC-XHD-001..017** fan-out theo **kênh**; chiều nhóm DV × loại đơn là **dữ liệu** — không tách thêm SC theo nhóm DV | Sufficiency Rule (1 lớp EP / SC); TP F01 680 TC | Tách SC theo nhóm ⇒ 340 SC trùng hành vi, vượt trần 200 SC/version |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 REQ-XHD-039 (BR-XHD-18 clear "thuê thiết bị đầu cuối") **chưa có SC** | URD 1 câu, "kịp plan" — CL-XHD-21 ⛔ | PM trả lời GAP-53 → `/analyze-requirements --update` thêm SC hoặc đánh dấu Out-scope |
| 2 | 🔴 REQ-XHD-042 (mail cảnh báo bản tin trễ qua ngày) **chưa có SC** | "Bắt buộc" nhưng không đặc tả — CL-XHD-22 ⛔ | PM trả lời GAP-02/11 → `--update` |
| 3 | 🔴 CL-XHD-29 tài liệu tích hợp (payload / schema / enum) chặn setup data + execute | GAP-07 chưa trả lời | Xin SDD trước setup 23/10/2026; chưa có ⇒ verify định tính |
| 4 | 🔴 CL-XHD-11 khóa chống trùng — chặn TC chi tiết SC-XHD-076..079 | GAP-41 | Hỏi BA trước generate-tc 21/10/2026 |
| 5 | 🟡 21 SC có Then `⛔ chờ CL-…` / `(giả định TP)` (đếm ở `counts.blocked_by_cl`) | Theo giả định của TP §2.4 | Khi CL resolved: `--update` sửa Then, ghi 1 dòng UPDATE ở §1 |
| 6 | 🟡 CL-XHD-30 (đơn ngoài 17 kênh / ServiceID 2, 22) — chưa có SC negative | Chờ BA: bỏ qua hay vẫn xuất | Nếu "bỏ qua" ⇒ thêm SC negative qua `--update` |
| 7 | 🟡 CL-XHD-27, CL-XHD-28 mới phát hiện khi analyze (chưa có GAP-ID) | Chưa đưa vào DOC-READINESS / TP §2.4 | QC owner thêm vào danh sách gửi PM (create-test-plan `--update`) |
