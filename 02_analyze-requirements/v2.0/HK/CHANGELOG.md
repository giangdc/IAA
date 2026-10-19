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
  cl: CL-HK-01..11
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
| 2026-10-19 | UPDATE | **Dùng lại URD 2.1 cho Phụ lục D#5, D#6:** đóng CL-HK-02 (đơn vị đầu số riêng ngoài phạm vi) + CL-HK-10 (ký hiệu `1K<yy>T<xx>`, ID HĐ năm 2 số + mã tỉnh + số Invoice No); CL-HK-03 làm rõ một phần (chiết khấu không test; vẫn BLOCKING cho dòng EVC). **SC-HK-009, 010 dùng lại**; SC-HK-008 có bảng map (loại HĐ → đầu vẫn chờ CL-HK-01); SC-HK-011 hết chờ CL; test data ký hiệu / ID / mã tỉnh điền theo 2.1 | QC owner chốt 19/10/2026 | SC 18→20 · deprecated 3→1 · P2 6→8 · cl_open 8→6 · blocked_by_cl 7 (011 −1, 009 +1) |
| 2026-10-19 | SCOPE↓ | **Ký hiệu HĐĐT: chỉ test HĐ bán mới đầu U, không test đầu M** (và A). CL-HK-01 làm rõ một phần, **hết BLOCKING**; SC-HK-008, 009 (đổi thành "FPL đầu U", Negative→Functional), 010 hết chờ CL; SC-HK-020 còn chờ (bán thêm có dùng đầu U?) | QC owner 19/10/2026 | cl_blocking 2→1 · blocked_by_cl 7→5 |
| 2026-10-19 | UPDATE | **Đóng CL-HK-01:** HĐ đơn bán thêm cũng dùng đầu U ⇒ SC-HK-020 hết chờ CL | QC owner 19/10/2026 | cl_open 6→5 · blocked_by_cl 5→4 |
| 2026-10-19 | UPDATE | +CL-HK-11 (Open): ký hiệu HĐĐT verify ở đâu — tool Liệt kê cước chỉ hiển thị ID hóa đơn. SC-HK-008, 009, 010, 020 chờ điểm verify | QC owner 19/10/2026 | CL 10→11 · cl_open 5→6 · blocked_by_cl 4→8 |
| 2026-10-19 | UPDATE | Dọn chữ cũ theo câu trả lời QC owner: Tổng quan + RISK-HK-01 (bảng map theo URD 2.1, chỉ đầu U, còn chờ CL-HK-11), RISK-HK-04 (bỏ SC-HK-019 — không test lỗi trên STG), RISK-HK-05 → Out-scope (CL-HK-02), REQ-HK-005 ghi chú, quy tắc đủ scenario + ghi chú SC-HK-020, §3 Nợ #4. Không đổi REQ / SC / CL | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | QC trả lời CL vòng 3: **đóng** CL-HK-09 (1 hóa đơn chỉ thuộc 1 đơn hàng; 1 hợp đồng có nhiều đơn hàng — SC-HK-005 giữ, viết lại Given / Then) · **làm rõ thêm** CL-HK-07 (mỗi đơn chỉ add tiền trả trước 1 lần; còn hỏi add ở hóa đơn nào) | QC trả lời 19/10/2026 (file câu hỏi vòng 3) | cl_open 6→5 · blocked_by_cl 8→7 |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⚠️ **URD 2.1 (`DOC-v2.0-02`) chỉ dùng cho các mục Phụ lục D của URD 2.2 trỏ về** (QC owner chốt 19/10/2026 — thay ràng buộc 16/10 "2.1 không sử dụng"): dùng D#1 cutover, D#2 chống phát hành trùng, D#3 RISK-01, D#4 cấu hình EVC (từ vòng 3 19/10/2026 — 2.2 ghi "Giữ nguyên (gộp nhóm BR-VC)"; bỏ bước 2.1 đánh dấu `[Bỏ]`), D#5 ký hiệu / ID / đơn vị đầu số riêng, D#6 dòng chiết khấu / thông tin theo mẫu. ⛔ **Không dùng:** D#7 mapping chi nhánh, D#8 câu hỏi mục V, D#9 autobill TB theo phương thức (2.2 ghi không còn áp dụng / đã bỏ). Phần chính 2.2 thắng khi mâu thuẫn. Chỉ cập nhật các CL QC owner chỉ định (CL-XHD-22, 23, 24 · CL-HK-02, 03, 10) | QC owner 19/10/2026 | Dùng 2.1 ngoài các mục trên ⇒ TC kiểm theo nội dung đã bỏ, bug bị bác |
| 2 | ⚠️ **Tiền trả trước: "mỗi đơn một lần" (2.2) thắng "một lần với 1 dịch vụ" (2.1)** | Quy tắc 2.2 thắng | Viết TC per dịch vụ ⇒ expected add nhiều lần, FAIL oan |
| 3 | ⚠️ **API spec HĐĐT / hệ thống Dịch vụ** dùng chung CL-XHD-29 / RISK-XHD-01 — home ở `XHD/` | Layout v2 không có `_global/` | Mở CL trùng ở HK ⇒ 2 home, drift |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 REQ-HK-010 (dòng EVC, chiết khấu, thông tin theo mẫu) **chưa có SC** | Chỉ có tên, đặc tả chuyển D#6 — CL-HK-03 ⛔ (GAP-04 Blocker, TP đề xuất Out-scope) | PM chốt Out-scope ⇒ ghi `SCOPE↓` ở §1; nếu in-scope ⇒ `--update` thêm SC |
| 2 | ✅ CL-HK-01, CL-HK-10 đã đóng 19/10/2026 — ký hiệu / ID theo URD 2.1, chỉ đầu U (bán mới + bán thêm) | — | — |
| 3 | 🟡 8 SC có Then `⛔ chờ CL-…` | Theo giả định TP | Khi CL resolved: `--update` |
| 4 | ✅ CL-HK-09 đã đóng 19/10/2026 vòng 3 (1 hóa đơn chỉ thuộc 1 đơn hàng) · ✅ CL-HK-08 đã đóng 19/10/2026 (mã tỉnh theo địa chỉ hợp đồng) | — | — |
