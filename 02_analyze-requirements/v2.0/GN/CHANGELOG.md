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
updated: 2026-10-20
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
| 2026-10-19 | UPDATE | Ràng buộc §2 #1 đổi: dùng URD 2.1 cho Phụ lục D trừ D#4 (cấu hình EVC — QC owner: không đụng), 7, 8, 9 ⇒ GN **không đổi** REQ / SC / CL | QC owner chốt 19/10/2026 | Không |
| 2026-10-19 | SCOPE↓ | Đối chiếu TP §2.2 (chỉ đọc, không sửa TP): **gạch nợ bằng EVC / voucher ngoài phạm vi** (#5). CL-GN-01, 08 → Out-scope; CL-GN-10 thu hẹp (bỏ ý nguồn / cấu hình EVC — D#4); **deprecated SC-GN-048** (Paid voucher dùng gạch nợ). Giữ SC-GN-045 (ranh giới), 046, 047 (chừa EVC lock — TP in-scope), nhánh Cọc 037, 038, 043 | QC owner 19/10/2026 + TP §2.2 #5 | SC 49→48 · deprecated 1→2 · P1 42→41 · cl_open 8→6 |
| 2026-10-19 | UPDATE | Dọn chữ cũ theo TP §2.2 #5 (chỉ đọc TP): RISK-GN-01 Status → Out-scope (bỏ SC-GN-048 khỏi cột SC); §3 Nợ #1, #2 (CL-GN-01, 08) → đóng Out-scope. Không đổi REQ / SC / CL | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | Dọn chữ cũ theo CL-GN-02: RISK-GN-02, 04 bỏ SC-GN-049 (không test lỗi / timeout trên STG); §3 Nợ #3 số SC chờ CL 5→3. Không đổi REQ / SC / CL | QC owner 19/10/2026 | Không |
| 2026-10-19 | SCOPE↑ | **Hoàn tác SCOPE↓ cùng ngày:** QC owner chốt gạch nợ EVC / voucher **vẫn test**, chờ BA liệt kê loại EVC / voucher. Mở lại CL-GN-01, 08; CL-GN-10 hỏi lại đủ 3 ý; **SC-GN-048 dùng lại** (chờ CL-GN-01, 10); RISK-GN-01 về Open. Ghi rõ khác TP §2.2 #5 (không sửa TP) | QC owner 19/10/2026 | SC 48→49 · deprecated 2→1 · P1 41→42 · cl_open 6→8 · blocked_by_cl 3→4 |
| 2026-10-19 | UPDATE | QC trả lời CL vòng 3: **đóng** CL-GN-06 (phí sàn đã tính vào tiền khách trả ⇒ Paid quyết toán không nhỏ hơn nợ — **deprecated SC-GN-024**), CL-GN-07 (không test map loại cọc; đơn bán thêm vẫn có cọc — SC-GN-050 hết chờ CL) · **làm rõ thêm** CL-GN-08 (INVOICE và đội EVC chạy cùng nhau), CL-GN-10 (**Phụ lục D#4 lấy từ URD 2.1** BR-VC-01..07, BR-GC-04..07, bỏ bước `[Bỏ]` — QC owner) · ghi nhận CL-GN-05 | QC trả lời 19/10/2026 (file câu hỏi vòng 3) + QC owner | SC 49→48 (deprecated 2) · P2 6→5 · cl_open 8→6 · blocked_by_cl 4→2 |
| 2026-10-19 | UPDATE | **Đóng CL-GN-05:** Bill chỉ gạch khi Paid đủ nợ còn lại; Paid thiếu ⇒ không gạch, chờ Paid đủ (khác cách đọc chữ BR-GN-04 "gạch từng phần" — theo QC owner). SC-GN-031 viết lại Then | QC owner 19/10/2026 | cl_open 6→5 |
| 2026-10-19 | UPDATE | CL-GN-05 bổ sung: đơn nhiều Bill — Bill thiếu tiền bị bỏ qua, xét tiếp Bill nhỏ hơn. SC-GN-028 viết lại Then (500k gạch · 300k không gạch · 100k gạch) | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | **Mở lại CL-GN-05:** quy tắc "chỉ gạch khi Paid đủ nợ còn lại" + bỏ qua Bill thiếu tiền là cách hiểu của QC owner, chờ BA xác nhận. SC-GN-028, 031 giữ Then, đánh dấu ⛔ chờ CL-GN-05 | QC owner 19/10/2026 | cl_open 5→6 · blocked_by_cl 2→4 |
| 2026-10-20 | UPDATE | **Đóng CL-GN-08:** INVOICE và hệ thống EVC chạy song song; INVOICE chừa phần tiền voucher / EVC khi gạch tiền khách; EVC gạch lỗi ⇒ báo đội EVC retry bằng tay hoặc tool hỗ trợ — SC-GN-045 viết lại Then; ghi chú REQ-GN-018, 019 | QC owner 20/10/2026 | cl_open 6→5 |
| 2026-10-20 | UPDATE | **Đóng CL-GN-05 (vòng 4):** gạch nợ Paid áp cho sàn TMĐT — tiền về công ty mới gạch ⇒ Paid = tổng tiền đơn; "gạch từng phần" (BR-GN-04) là chia Paid cho từng bill, không phải gạch một phần hóa đơn. SC-GN-028 viết lại (Paid 900k, gạch đủ 3 bill); **deprecated SC-GN-031** (Paid < nợ không xảy ra); ghi chú REQ-GN-012, 014; RISK-GN-05 bỏ SC-GN-031 | BA trả lời vòng 4 + QC owner 20/10/2026 | SC 48→47 (deprecated 3) · P1 42→41 · cl_open 5→4 · blocked_by_cl 4→2 |
| 2026-10-20 | UPDATE | **Đóng CL-GN-09 (vòng 4):** 2 bill bằng tiền nhau ⇒ gạch bill nào trước cũng được. SC-GN-030 viết lại (2 bill 300k, Paid 600k = tổng tiền đơn; không kiểm thứ tự, bỏ ⛔); ghi chú REQ-GN-013, test_data_catalog | BA trả lời vòng 4 + QC owner 20/10/2026 | cl_open 4→3 · blocked_by_cl 2→1 |
| 2026-10-20 | UPDATE | SC-GN-032 (Paid > nợ, Paid dư được giữ) **giữ nguyên Then**; thêm ghi chú: thực tế Paid = tổng tiền đơn nên case ít xảy ra, QC chưa rõ có ngoại lệ — data dựng được trên STG hay không sẽ xác định khi test | QC owner 20/10/2026 | Không |
| 2026-10-20 | UPDATE | **Vòng 4:** đóng CL-GN-04 (verify gạch nợ tạm trên bảng kê thanh toán, Phương thức thanh toán = "gạch nợ tạm") · đóng CL-GN-10 (cấu hình EVC D#4 là phần dành cho dev) · ghi nhận CL-GN-01: PO trả lời danh sách EVC sau; 2 quy tắc EVC không / có xác định SPDV; ghi chú REQ-GN-005, 010, test_data_catalog | BA trả lời vòng 4 + QC owner 20/10/2026 | cl_open 3→1 |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⚠️ **Gạch nợ EVC / voucher VẪN TEST** (QC owner 19/10/2026) — **khác TP §2.2 #5** (TP ghi ngoài phạm vi; QC owner xử lý TP, analyze không sửa TP). Loại EVC / voucher và bên gạch chờ BA (CL-GN-01, 08, 10). Phụ lục D#4 vẫn không lấy từ URD 2.1 | QC owner 19/10/2026 | Bỏ case EVC / voucher ⇒ hở phạm vi QC owner yêu cầu |
| 2 | ⚠️ **Kênh sàn = {20 Shopee, 21 Tiktok}** là giả định (CL-GN-03) | 2.2 không đánh dấu kênh sàn; 2.1 L125 | BA thêm kênh ⇒ SC-GN-011, 012, 019, 020 thiếu lớp EP; gạch tạm sai kênh không bị phát hiện |
| 3 | ⚠️ **Tài liệu tích hợp / payload Kafka Out / enum** dùng chung CL-XHD-29, RISK-XHD-01 — home ở `XHD/` | Layout v2 không có `_global/` | Mở CL trùng ở GN ⇒ 2 home, drift trạng thái |
| 4 | ⚠️ Thuật ngữ thống nhất "**gỡ gạch nợ tạm**" (2.2) — không dùng "hất nợ tạm" / "xóa gạch nợ tạm" của 2.1 | BR-NT-04 L501 | TC / bug dùng 3 tên ⇒ khó trace, review-tc báo không nhất quán |
| 5 | ⚠️ **URD 2.1 (`DOC-v2.0-02`) chỉ dùng cho Phụ lục D của URD 2.2** (QC owner 19/10/2026 — thay ràng buộc 16/10 "không sử dụng"), trừ D#7, 8, 9. Với GN: **D#4 cấu hình EVC lấy từ URD 2.1 BR-VC-01..07, BR-GC-04..07** (từ vòng 3 19/10/2026 — 2.2 D#4 ghi "Giữ nguyên (gộp nhóm BR-VC)"), bỏ các bước 2.1 đánh dấu `[Bỏ]`; danh sách loại EVC / voucher vẫn hỏi BA (CL-GN-10) | QC owner 19/10/2026 | Dùng bước 2.1 đã đánh dấu `[Bỏ]` ⇒ TC kiểm theo nội dung đã bỏ |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | 🔴 CL-GN-01: danh sách loại EVC / voucher — chặn expected SC-GN-048 (CL-GN-10 đóng 20/10/2026) | Vòng 4: BA hỏi PO, trả lời sau; đã có 2 quy tắc EVC theo SPDV | Chờ PO; cân nhắc thêm SC cho 2 quy tắc |
| 2 | ✅ CL-GN-08 thứ tự đội EVC ↔ INVOICE ở nhánh Paid | Resolved 20/10/2026 — chạy song song, INVOICE chừa phần voucher / EVC | — |
| 3 | 🟡 1 SC có Then `⛔ chờ CL-…` | Theo giả định TP | Khi CL resolved: `--update` |
| 4 | 🟡 Mock API kênh thanh toán / đội EVC / consumer Kafka Out chưa có | TP Entry Criteria | Chuẩn bị trước R1 (26/10/2026) |
