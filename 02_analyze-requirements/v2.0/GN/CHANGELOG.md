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
  sc: "SC-GN-001..075 (NEW; 001, 002, 004, 005, 006, 012, 020, 021, 024, 025, 031, 032, 035, 036, 038, 039, 040, 041, 044, 049, 052 deprecated)"
  cl: CL-GN-01..10
  risk: RISK-GN-01..06
status: ANALYZED
updated: 2026-10-21
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
| 2026-10-21 | UPDATE | **Kafka Out — QC không check** (BA: phần dành cho dev, theo CL-XHD-29): SC-GN-034 bỏ Kafka khỏi Then (QC kiểm Payment + Paid bị trừ), SC-GN-035 bỏ "không có Kafka Out" khỏi Then (QC kiểm Payment + cọc bị trừ), đổi tiêu đề chi tiết 2 SC; ghi chú REQ-GN-014, test_data_catalog dòng Kafka Out, RISK-GN-04, §2 #3, §3 #4. Không đổi số REQ / SC / CL | BA note + QC owner 21/10/2026 | Không |
| 2026-10-21 | UPDATE | **Luồng Cọc (QC owner trả lời 3 câu nháp):** (1) đơn ngoài sàn (gồm thanh toán tại quầy / tại nơi triển khai) đi luồng Cọc, luồng Paid chỉ gồm đơn sàn; (2) khách thanh toán ngoài Paid đều đẩy vào cọc — đơn Cọc kích hoạt ở điểm chạm (b), (c); (3) cọc luôn bằng tiền đơn ⇒ không có case thiếu cọc. **Deprecated SC-GN-038, 040, 041**; SC-GN-012, 020 đổi ví dụ "quầy" → kênh ngoài sàn (Mobile 1) + ghi chú; CL-GN-03, 07 thêm ghi nhận; RISK-GN-06 → Resolved; RISK-GN-02 bỏ SC-GN-038; ghi chú REQ-GN-016, 017; test_data_catalog dòng Kênh sàn, Cọc | QC owner 21/10/2026 | SC 47→44 · deprecated 3→6 · P1 41→38 |
| 2026-10-21 | UPDATE | **BA trả lời toàn bộ câu nháp (#1, 3, 4, 7, 8, 9, 10):** đóng **CL-GN-01** — điểm kiểm EVC / voucher = nợ còn lại = 0, không kiểm bên gạch ⇒ SC-GN-045, 048 viết lại Then (hết mâu thuẫn 045 ↔ 048; 048 hết chờ CL); gạch tạm luôn trừ EVC ⇒ **+SC-GN-051**, SC-GN-019 làm rõ Then; Paid có ở mọi luồng, đơn Cọc kích hoạt ở điểm chạm (a) ⇒ **+SC-GN-052**; Paid tạm chỉ đơn sàn ⇒ **deprecated SC-GN-012, 020**; đơn sàn luôn đi Paid ⇒ **deprecated SC-GN-021**; Paid dư không dựng được ⇒ **deprecated SC-GN-032**; SC-GN-046, 047 sửa dữ liệu (Paid = phần khách trả); cọc = phần khách trả (sau EVC). CL-GN-07 đính chính, CL-GN-08 ghi nhận; RISK-GN-01 → Resolved; test_data_catalog dòng PaidType, Payment tạm, Paid so với nợ, lock, Cọc | BA trả lời 21/10/2026 (file InvoiceIssuance_v2.0_GN_Tong-hop-cau-hoi-tra-loi_2026-10-21.xlsx, sheet nháp) | SC 44→42 · deprecated 6→10 · P1 38→36 · cl_open 1→0 · blocked_by_cl 1→0 |
| 2026-10-21 | UPDATE | **QC owner trả lời nháp #11–14 (rà test design):** (#11) thông tin cọc nhiều dòng, mỗi bill clear đúng dòng của nó, clear 1 lần ⇒ không có cọc dư — **deprecated SC-GN-044**, **+SC-GN-053**, SC-GN-050 viết lại (bill bán thêm có dòng cọc riêng — chờ #15), SC-GN-029 sửa ghi chú; (#12) không kiểm theo loại cọc ⇒ SC-GN-042 viết lại, **deprecated SC-GN-039** (gộp); (#13) biên Paid 0 / 1 và T − 1 không cần ⇒ **deprecated SC-GN-025, 036**; (#14) **deprecated SC-GN-035** (gộp vào 042, 043). Ghi chú REQ-GN-015, 017, 018; CL-GN-07 bổ sung; RISK-GN-06; test_data_catalog dòng Paid Amount, Σ Payment, Cọc, Payment nhánh Cọc, Loại đơn. +nháp #15 | QC owner 21/10/2026 (file InvoiceIssuance_v2.0_GN_Tong-hop-cau-hoi-tra-loi_2026-10-21.xlsx, sheet nháp #11–14) | SC 42→38 · deprecated 10→15 · P1 36→33 · P2 5→4 |
| 2026-10-21 | UPDATE | **QC owner trả lời nháp #15:** đơn bán thêm có dòng cọc riêng (SC-GN-050 bỏ cờ chờ, Given ghi rõ hợp đồng có thể từ rất lâu); đơn trước cùng hợp đồng chưa thỏa điều kiện mà lúc gạch bán thêm đã thỏa ⇒ gạch luôn 2 đơn — **+SC-GN-054**; bán mới = hợp đồng mới, bán thêm = hợp đồng đã có, 2 luồng cơ bản như nhau. CL-GN-07 bổ sung; ghi chú REQ-GN-016, 018; test_data_catalog dòng Loại đơn. +nháp #16 | QC owner 21/10/2026 (sheet nháp #15) | SC 38→39 · P2 4→5 |
| 2026-10-21 | UPDATE | **QC owner trả lời nháp #16:** "đơn trước chưa thỏa điều kiện" = **đơn hàng trước chưa thanh toán** ("đơn" là đơn hàng, không phải hóa đơn) ⇒ SC-GN-054 viết lại Given / When / Then theo đơn hàng; CL-GN-07 bổ sung; test_data_catalog dòng Loại đơn. Không đổi số SC | QC owner 21/10/2026 (sheet nháp #16) | Không |
| 2026-10-21 | UPDATE | **+SC-GN-055** (đơn ngoài sàn có hóa đơn DV + TB phát hành khác thời điểm, mỗi hóa đơn gạch đúng dòng cọc của bill) — QC đề xuất khi rà phủ kênh / nhóm dịch vụ, QC owner đồng ý. Kết luận rà: GN **không tách TC theo kênh / nhóm dịch vụ** — quy tắc chỉ đổi theo sàn (20, 21) / ngoài sàn (BR-XL-01 L482, BR-NT-01 L493-494); dịch vụ chỉ ảnh hưởng loại cọc (không test, CL-GN-07). Ghi chú REQ-GN-004, 018 (cột SC); test_data_catalog dòng Danh sách bill | QC owner 21/10/2026 | SC 39→40 · P1 33→34 |
| 2026-10-21 | UPDATE | **+SC-GN-056..075** — 1 SC / nhóm dịch vụ (20 nhóm §A.3, bỏ ServiceID 2, 22): luồng Cọc, kênh ngoài sàn xoay vòng phủ đủ 14 kênh; kiểm mọi hóa đơn "Đã gạch nợ", nợ = 0, cọc từng bill clear; không quan tâm SubServiceType, không kiểm loại cọc. P1: Internet, FPT Camera Only, FPT Camera Combo, FPT Play; còn lại P2. Ghi chú REQ-GN-016, 018 (cột SC); test_data_catalog +dòng Nhóm dịch vụ; §3 #9 sửa | QC owner 21/10/2026 | SC 40→60 · P1 34→38 · P2 5→21 |
| 2026-10-21 | UPDATE | **Paid chỉ có ở luồng sàn, luồng ngoài sàn là Cọc** (QC owner): **deprecated SC-GN-052** (đơn Cọc kích hoạt ở điểm chạm (a) bằng Paid hoàn tất); SC-GN-013 Given đổi "kênh bất kỳ" → kênh sàn; ghi chú REQ-GN-005; REQ-GN-005, 008 bỏ SC-GN-052; CL-GN-07 đính chính lần 2; §2 #6 (a) đảo lại. test_data_catalog dòng Orderpaid (chỉ đơn sàn). ⚠️ Khác câu trả lời BA nháp #8, #10 | QC owner 21/10/2026 | SC 60→59 · deprecated 15→16 · P1 38→37 |
| 2026-10-21 | UPDATE | Sửa theo health-check GN: Khuyến nghị #2 (risk_assessment) thay SC-GN-052 (deprecated) bằng SC-GN-055; §3 #5 bỏ câu cũ "cọc luôn bằng tiền đơn" → cọc = phần khách trả. Không đổi số | health-check 21/10/2026 | Không |
| 2026-10-21 | UPDATE | **Đồng bộ Paid: dev tự kiểm, QC không check** (QC owner): luồng sàn không có data trên Foxpay › Đối soát khoản thu online, QC không có màn tra bảng Paid ⇒ **deprecated SC-GN-001, 002, 004, 005, 006**; SC-GN-003, 007, 034 viết lại Then — kiểm gián tiếp qua hóa đơn (Payment / không gạch 2 lần), bỏ ý kiểm dòng Paid / Paid bị trừ. REQ-GN-001 không còn SC QC (gap có chủ đích §3 #10). Ghi chú REQ-GN-001..003; test_data_catalog dòng Orderpaid, PaidType, Khóa trùng; §2 +#7 | QC owner 21/10/2026 | SC 59→54 · deprecated 16→21 · P1 37→34 · P2 21→19 |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⚠️ **Gạch nợ EVC / voucher VẪN TEST** (QC owner 19/10/2026) — **khác TP §2.2 #5** (TP ghi ngoài phạm vi; QC owner xử lý TP, analyze không sửa TP). **Điểm kiểm EVC / voucher = nợ còn lại = 0** (+ Σ Payment không vượt tổng hóa đơn) — **không kiểm bên nào gạch** (BA 21/10/2026, CL-GN-01) | QC owner 19/10/2026 | Bỏ case EVC / voucher ⇒ hở phạm vi QC owner yêu cầu |
| 2 | ⚠️ **Kênh sàn = {20 Shopee, 21 Tiktok}** (CL-GN-03) · **đơn sàn đi luồng Paid, đơn ngoài sàn đi luồng Cọc**; **Paid chỉ có ở luồng sàn** — đơn ngoài sàn không có Paid, không dựng bước Paid / Orderpaid cho TC luồng Cọc (QC owner 21/10/2026) | CL-GN-03, CL-GN-07 | Dựng đơn ngoài sàn đi luồng Paid / Paid tạm ngoài sàn ⇒ case không có thật, TC sai expected |
| 3 | ⚠️ **Tài liệu tích hợp / payload Kafka Out / enum** dùng chung CL-XHD-29, RISK-XHD-01 — home ở `XHD/`. ⛔ **QC không check Kafka Out** (BA: phần dành cho dev, 21/10/2026) — Kafka không là điều kiện PASS của SC / TC | Layout v2 không có `_global/` | Mở CL trùng ở GN ⇒ 2 home, drift trạng thái |
| 4 | ⚠️ Thuật ngữ thống nhất "**gỡ gạch nợ tạm**" (2.2) — không dùng "hất nợ tạm" / "xóa gạch nợ tạm" của 2.1 | BR-NT-04 L501 | TC / bug dùng 3 tên ⇒ khó trace, review-tc báo không nhất quán |
| 5 | ⚠️ **URD 2.1 (`DOC-v2.0-02`) chỉ dùng cho Phụ lục D của URD 2.2** (QC owner 19/10/2026 — thay ràng buộc 16/10 "không sử dụng"), trừ D#7, 8, 9. Với GN: **D#4 cấu hình EVC lấy từ URD 2.1 BR-VC-01..07, BR-GC-04..07** (từ vòng 3 19/10/2026 — 2.2 D#4 ghi "Giữ nguyên (gộp nhóm BR-VC)"), bỏ các bước 2.1 đánh dấu `[Bỏ]`; danh sách loại EVC / voucher vẫn hỏi BA (CL-GN-10) | QC owner 19/10/2026 | Dùng bước 2.1 đã đánh dấu `[Bỏ]` ⇒ TC kiểm theo nội dung đã bỏ |
| 6 | ⛔ **Kết luận HẾT HIỆU LỰC — đừng trích lại:** (a) CL-GN-07 ý BA "Paid có ở mọi luồng, đơn Cọc kích hoạt ở điểm chạm (a)" (bản 21/10/2026 chiều, SC-GN-052) — hiện hành (QC owner 21/10/2026): **Paid chỉ có ở luồng sàn**, đơn Cọc gạch ở điểm chạm (b), (c), SC-GN-052 deprecated; (b) CL-GN-01 vòng 2 "Paid voucher được dùng gạch như tiền khách" và CL-GN-08 20/10 "INVOICE chừa phần voucher / EVC" **không dùng làm điểm kiểm** — hiện hành: nợ còn lại = 0, không kiểm bên gạch; (c) "cọc luôn bằng tiền đơn" — hiện hành: cọc = phần khách trả (sau voucher / EVC); (d) "đơn bán thêm dùng chung cọc dư của hợp đồng" và "Payment cọc = 1 dòng / loại cọc là điểm kiểm" — hiện hành: mỗi bill 1 dòng cọc, clear 1 lần; không kiểm theo loại (nháp #11, 12) | BA 21/10/2026 | Viết expected theo bản cũ ⇒ TC sai / mâu thuẫn nhau |
| 7 | ⛔ **QC không check dữ liệu Paid** (bảng Paid / dòng Paid / Paid bị trừ / PaidType) — dev tự kiểm. Luồng sàn không có data trên Foxpay › Đối soát khoản thu online. QC chỉ kiểm kết quả gạch nợ trên hóa đơn (Liệt kê cước / bảng kê thanh toán) | QC owner 21/10/2026 | Viết TC tra Paid ⇒ TC không chạy được |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | ✅ CL-GN-01 Resolved 21/10/2026 — điểm kiểm nợ còn lại = 0. 2 quy tắc EVC theo SPDV (BA vòng 4) **không có SC riêng có chủ đích**: phân bổ EVC là phía EVC, QC kiểm kết quả cuối qua SC-GN-045, 048 | Đóng | — |
| 2 | ✅ CL-GN-08 thứ tự đội EVC ↔ INVOICE ở nhánh Paid | Resolved 20/10/2026 — chạy song song, INVOICE chừa phần voucher / EVC | — |
| 3 | ✅ 0 SC chờ CL (SC-GN-048 hết chờ 21/10/2026) | Đóng | — |
| 4 | 🟡 Mock API kênh thanh toán / đội EVC chưa có (Kafka Out QC không check) | TP Entry Criteria | Chuẩn bị trước R1 (26/10/2026) |
| 5 | ℹ️ BR-GC-01 nhánh thiếu tiền, BR-GC-02 nhánh thiếu một loại cọc **không có SC** (có chủ đích) — cọc = phần khách trả, cọc + EVC = nợ ⇒ không có case thiếu cọc (QC owner + BA 21/10/2026) | Gap có chủ đích | — |
| 6 | ✅ Nháp 21/10/2026 — BA trả lời hết (#1–#10); QC owner trả lời #11–14 | Đóng 21/10/2026 | — |
| 7 | ✅ Nháp #15, #16 — đã trả lời 21/10/2026 (SC-GN-050, 054) | Đóng 21/10/2026 | — |
| 8 | ℹ️ Biên Paid Amount 0 / 1 (BR-GN-01) và Σ Payment T − 1 (BR-GN-05) **không có SC** (có chủ đích — không dựng được data, QC owner 21/10/2026) | Gap có chủ đích | — |
| 9 | ℹ️ **Không tách TC theo kênh** (có chủ đích): 14 kênh ngoài sàn cùng 1 lớp EP — phủ kênh bằng cách xoay vòng kênh trong SC-GN-056..075; sàn phủ cả Shopee + TikTok. **Nhóm dịch vụ: mỗi nhóm 1 TC** (SC-GN-056..075), không quan tâm SubServiceType | Gap có chủ đích | — |
| 10 | ℹ️ **REQ-GN-001 (đồng bộ Paid 1:1, PaidType) và nhánh "thêm mới" của REQ-GN-002 không có SC QC** (có chủ đích) — dev tự kiểm (QC owner 21/10/2026) | Gap có chủ đích | — |
