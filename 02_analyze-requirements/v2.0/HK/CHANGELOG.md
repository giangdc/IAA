---
id: v2.0/HK/changelog
title: Changelog — Module HK
type: changelog
version: v2.0
sprint: —
module:
  code: HK
  dir: HK
  name: Đẩy hậu kỳ qua dịch vụ – tiền trả trước
doc_source:
  - id: DOC-v2.0-01
    section: "§A.5 #12 · §B.III · §C#1 · §D#5, #6"
  - id: DOC-v2.0-FIG-05
    section: "flow §B.III.b"
id_range:
  req: REQ-HK-001..010
  sc: "SC-HK-001..021 (NEW)"
  cl: CL-HK-01..10
  risk: RISK-HK-01..05
status: ANALYZED
updated: 2026-10-19
---

# Changelog — Module HK (`HK`)

> Tạo bởi: analyze-requirements (**layout v2** — 1 file / module, ở cùng thư mục với 5 deliverable còn lại).
> **Đây là đích write-back của LỊCH SỬ.** Mọi lượt `--init` / `--sweep` / `--update` / `--delta` chạm module này ghi **1 dòng bảng ở §1**.
> ⛔ **KHÔNG nối banner *"Cập nhật lần cuối"* vào đầu các file deliverable khác.**

> 🔴 **`id_range` là trường BẮT BUỘC.** ⛔ KHÔNG suy sprint từ số ID — quy chiếu bằng đường dẫn `v2.0/HK/`.

## 1. Lịch sử thay đổi

| Ngày | Loại | Thay đổi | Nguồn / Lý do | Ảnh hưởng |
|---|---|---|---|---|
| 2026-10-16 | INIT | Phân tích lần đầu §B.III — 10 REQ (`001..010`), 21 SC (P1 12 · P2 9), 9 CL (2 BLOCKING), 5 RISK. Điểm nghiệp vụ đáng chú ý nhất: ký hiệu HĐĐT "cần chốt" — SC ký hiệu / ID đang dựa trên bảng map của URD 2.1 (sidecar `quotes/REQ-HK-005.md`) | `DOC-v2.0-01` §B.III + URD 2.1 §III | Dựng đủ 5 deliverable + CHANGELOG + 1 sidecar quote |
| 2026-10-16 | UPDATE | Đối chiếu flow §B.III.b (`DOC-v2.0-FIG-05` (ảnh: Workflow ĐẨY HẬU KỲ – TIỀN TRẢ TRƯỚC (URD 2.2 §III.b).png), trích từ URD): ghi chú khớp BR-HK-01, 02, 03, 05, 07, 09; nhánh A (HĐĐT) được tô "cần xác nhận" — củng cố CL-HK-01, 03, 04. **Không đổi** REQ / SC / CL | Flow URD 2.2 người dùng bổ sung | Không |
| 2026-10-16 | UPDATE | **Bỏ URD 2.1 — không sử dụng, xoá nội dung 2.1 khỏi analyze:** xoá mọi trích dẫn 2.1 và sidecar `quotes/REQ-HK-005.md` (bảng map 2.1); **deprecated SC-HK-009, 010** (FPL đầu số, Vùng 5 — chỉ có ở bảng 2.1); SC-HK-008, 011, 020 bỏ dữ liệu 2.1, chờ bảng chốt; test data ký hiệu / ID / mã tỉnh thành chờ; +CL-HK-10 | QC owner yêu cầu 16/10/2026 | SC active 21→19 (deprecated 2) · CL 9→10 · blocked_by_cl 8→9 |
| 2026-10-19 | UPDATE | CL-HK-04 làm rõ một phần (QC trả lời vòng 2): mức thuế suất không phát sinh thì không in dòng ⇒ SC-HK-014 hết chờ CL, Then chốt "chỉ dòng 10% + tổng cộng"; REQ-HK-008 ghi chú cập nhật. CL-HK-04 vẫn Open (mẫu HĐĐT) | QC trả lời 19/10/2026 | blocked_by_cl 9→8 · CL open không đổi |
| 2026-10-19 | UPDATE | Bổ sung tool verify vào `test_data_catalog.md` §Ghi chú chung (đường dẫn menu ở `07_environments/environments.md`). Không đổi REQ / SC / CL | QC owner cung cấp 19/10/2026 | Không |
| 2026-10-19 | UPDATE | QC trả lời CL vòng 2: **đóng** CL-HK-06, 08 · **làm rõ một phần** CL-HK-07, 09. **Deprecated SC-HK-019** (STG không test lỗi hệ thống Dịch vụ); SC-HK-011 ghi mã tỉnh theo địa chỉ hợp đồng. Câu dính URD 2.1 (CL-HK-02, 03, 10) **chưa cập nhật** | QC trả lời 19/10/2026 (file câu hỏi vòng 2) | SC 19→18 (deprecated 3) · P2 7→6 · cl_open 10→8 · blocked_by_cl 8→7 |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⛔ **URD 2.1 KHÔNG SỬ DỤNG từ 16/10/2026** (QC owner: tài liệu đã out) — chỉ URD 2.2 (`DOC-v2.0-01`) là căn cứ; mọi trích dẫn / ghi chú / dữ liệu lấy từ 2.1 **đã xoá** khỏi file module (bản cũ: `git show ec53583:<path>`). Thay ràng buộc cũ "2.2 thắng 2.1; 2.1 dùng cho phụ lục D" | Yêu cầu QC owner 16/10/2026 | Dựng expected / dữ liệu test theo 2.1 ⇒ TC kiểm theo tài liệu đã out, bug bị bác; phần 2.2 trỏ về 2.1 phải hỏi PO (CL-XHD-33, CL-GN-10, CL-HK-10). Riêng HK: bảng map ký hiệu 2.1 (`quotes/REQ-HK-005.md`) không còn là giả định |
| 2 | ⚠️ **Tiền trả trước: "mỗi đơn một lần" (2.2) thắng "một lần với 1 dịch vụ" (2.1)** | Quy tắc 2.2 thắng | Viết TC per dịch vụ ⇒ expected add nhiều lần, FAIL oan |
| 3 | ⚠️ **API spec HĐĐT / hệ thống Dịch vụ** dùng chung CL-XHD-29 / RISK-XHD-01 — home ở `XHD/` | Layout v2 không có `_global/` | Mở CL trùng ở HK ⇒ 2 home, drift |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 REQ-HK-010 (dòng EVC, chiết khấu, thông tin theo mẫu) **chưa có SC** | Chỉ có tên, đặc tả chuyển D#6 — CL-HK-03 ⛔ (GAP-04 Blocker, TP đề xuất Out-scope) | PM chốt Out-scope ⇒ ghi `SCOPE↓` ở §1; nếu in-scope ⇒ `--update` thêm SC |
| 2 | 🔴 CL-HK-01 + CL-HK-10 ký hiệu / ID bản chốt — chặn TC chi tiết SC-HK-008, 011, 020 (SC-HK-009, 010 deprecated) | GAP-17 | Hỏi BA trước generate-tc 21/10/2026 |
| 3 | 🟡 8 SC có Then `⛔ chờ CL-…` | Theo giả định TP | Khi CL resolved: `--update` |
| 4 | 🟡 CL-HK-08 (mã tỉnh lấy theo đâu), CL-HK-09 (1 HĐ nhiều đơn) mới phát hiện, chưa có GAP | — | QC owner thêm vào danh sách gửi PM |
