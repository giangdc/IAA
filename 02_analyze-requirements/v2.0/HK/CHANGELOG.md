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
  - id: DOC-v2.0-02
    section: "§III (BR-HK-03 bảng map vùng, BR-HK-04, 06, 08, 10) — tham chiếu"
id_range:
  req: REQ-HK-001..010
  sc: "SC-HK-001..021 (NEW)"
  cl: CL-HK-01..09
  risk: RISK-HK-01..05
status: ANALYZED
updated: 2026-10-16
---

# Changelog — Module HK (`HK`)

> Tạo bởi: analyze-requirements (**layout v2** — 1 file / module, ở cùng thư mục với 5 deliverable còn lại).
> **Đây là đích write-back của LỊCH SỬ.** Mọi lượt `--init` / `--sweep` / `--update` / `--delta` chạm module này ghi **1 dòng bảng ở §1**.
> ⛔ **KHÔNG nối banner *"Cập nhật lần cuối"* vào đầu các file deliverable khác.**

> 🔴 **`id_range` là trường BẮT BUỘC.** ⛔ KHÔNG suy sprint từ số ID — quy chiếu bằng đường dẫn `v2.0/HK/`.

## 1. Lịch sử thay đổi

| Ngày | Loại | Thay đổi | Nguồn / Lý do | Ảnh hưởng |
|---|---|---|---|---|
| 2026-10-16 | INIT | Phân tích lần đầu §B.III — 10 REQ (`001..010`), 21 SC (P1 12 · P2 9), 9 CL (2 BLOCKING), 5 RISK. Điểm nghiệp vụ đáng chú ý nhất: ký hiệu HĐĐT "cần chốt" — SC ký hiệu / ID đang dựa trên bảng map của URD 2.1 (sidecar `quotes/REQ-HK-005.md`) | `DOC-v2.0-01` §B.III + `DOC-v2.0-02` §III | Dựng đủ 5 deliverable + CHANGELOG + 1 sidecar quote |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⚠️ **Bảng map ký hiệu vùng × loại đầu là của URD 2.1** — mọi TC ký hiệu / ID ghi rõ "giả định bảng 2.1" tới khi CL-HK-01 trả lời | 2.2 ghi "cần chốt ký hiệu" (L585), §C#1 | Bảng chốt khác 2.1 ⇒ TC ký hiệu sai hàng loạt; bug sai căn cứ. Sai đầu số = sai kê khai thuế, không được bỏ qua |
| 2 | ⚠️ **Tiền trả trước: "mỗi đơn một lần" (2.2) thắng "một lần với 1 dịch vụ" (2.1)** | Quy tắc 2.2 thắng | Viết TC per dịch vụ ⇒ expected add nhiều lần, FAIL oan |
| 3 | ⚠️ **API spec HĐĐT / hệ thống Dịch vụ** dùng chung CL-XHD-29 / RISK-XHD-01 — home ở `XHD/` | Layout v2 không có `_global/` | Mở CL trùng ở HK ⇒ 2 home, drift |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 REQ-HK-010 (dòng EVC, chiết khấu, thông tin theo mẫu) **chưa có SC** | Chỉ có tên, đặc tả chuyển D#6 — CL-HK-03 ⛔ (GAP-04 Blocker, TP đề xuất Out-scope) | PM chốt Out-scope ⇒ ghi `SCOPE↓` ở §1; nếu in-scope ⇒ `--update` thêm SC |
| 2 | 🔴 CL-HK-01 ký hiệu bản chốt — chặn TC chi tiết SC-HK-008..011, 020 | GAP-17 | Hỏi BA trước generate-tc 21/10/2026 |
| 3 | 🟡 8 SC có Then `⛔ chờ CL-…` | Theo giả định TP | Khi CL resolved: `--update` |
| 4 | 🟡 CL-HK-08 (mã tỉnh lấy theo đâu), CL-HK-09 (1 HĐ nhiều đơn) mới phát hiện, chưa có GAP | — | QC owner thêm vào danh sách gửi PM |
