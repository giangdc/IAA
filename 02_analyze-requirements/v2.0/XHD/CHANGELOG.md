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
updated: 2026-10-20
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
| 2026-10-19 | SCOPE↓ | Đánh dấu **ngoài scope test** theo TP §2.2 (chỉ đọc TP): **SC-XHD-098** (hủy đơn đã có hóa đơn — #2), **SC-XHD-100** (đổi chi nhánh, hóa đơn cũ không tự điều chỉnh — #3) → deprecated; REQ-XHD-033 không còn SC; REQ-XHD-034 giữ SC-XHD-099 | QC owner 19/10/2026 + TP §2.2 #2, #3 | SC 111→109 · deprecated 0→2 · P1 85→84 · P2 25→24 |
| 2026-10-19 | UPDATE | Gắn nhãn **ngoài scope test** (TP §2.2 #4 — thuộc tính chi nhánh được bán SP / DV) tại REQ-XHD-034 và CL-XHD-26; vốn không có SC nào cho phần này. Không đổi REQ / SC / CL | QC owner 19/10/2026 + TP §2.2 #4 | Không |
| 2026-10-19 | UPDATE | Dọn chữ cũ theo TP §2.2 (chỉ đọc TP): REQ-XHD-041 + RISK-XHD-10 ghi kiểm tra chéo cutover trong scope (URD 2.1 BR-DB-08, SC-XHD-107, 108), **quét tay bổ sung ngoài scope test (TP #8)**; §3 Nợ #6 CL-XHD-30 → ngoài scope (TP #6). Không đổi REQ / SC / CL | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | Dọn chữ cũ: CL-XHD-33 viết lại theo quyết định dùng URD 2.1 cho Phụ lục D (Status → rõ một phần, câu hỏi khớp file vòng 3); §3 Nợ #5 số SC chờ CL 17→18. Không đổi REQ / SC / CL | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | CL-XHD-34 làm rõ một phần: QC owner cập nhật flow test — hóa đơn dịch vụ xuất ngay khi thanh toán, hóa đơn thiết bị sau giao hàng / triển khai thành công, 1 đơn nhiều hóa đơn (khớp BR-XHD-03, 14). Còn hỏi tín hiệu kích hoạt hóa đơn TB (tín hiệu giao hàng theo phương thức hay trạng thái đơn hoàn tất). Flow ở `07_environments/environments.md` cập nhật. Không đổi SC | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | CL-XHD-34 làm rõ thêm: hóa đơn thiết bị kích hoạt bởi tín hiệu giao hàng từng phương thức (phiếu thi công / Vendor / quầy) — khớp BR-DB-02, 06; SC-XHD-074, 105 giữ nguyên. Còn hỏi duy nhất: TB hình thức "Không" lấy tín hiệu nào | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | CL-XHD-34: QC owner xác nhận thiết bị nào có tín hiệu giao hàng thì xuất hóa đơn thiết bị đó (không chờ cả đơn hoàn tất). Không đổi SC | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | QC trả lời CL vòng 3: **đóng** CL-XHD-01 (SPF chỉ gửi thanh toán / hủy đơn; thông tin khách lấy từ hợp đồng; thời gian tạo đơn xem trên Web admin), 02 (khách không bấm Xuất hóa đơn trong 2 giờ ⇒ không phát hành), 03 (trường bắt buộc FPL), 08, 14 (trạng thái không hợp lệ), 15 (dừng ở lỗi đầu; đơn không có khuyến mãi vẫn phát hành), 18 (Billing lỗi ⇒ dev retry tay), 26 · **làm rõ thêm** CL-XHD-04 (2 mốc 2 giờ trùng nhau), 07 (chưa duyệt PĐK ⇒ xuất tay), 12, 27 (file HT Triển khai là danh mục chính thức) · ghi nhận CL-XHD-23, 24, 31. SC-XHD-020, 032, 033, 034, 050, 065, 080, 081 (QC owner giữ: đơn chưa có thông tin hợp đồng), 082, 095, 104 viết lại Then | QC trả lời 19/10/2026 (file câu hỏi vòng 3) | cl_open 26→18 · blocked_by_cl 18→9 |
| 2026-10-19 | UPDATE | **Đóng CL-XHD-04:** delay 2 giờ kênh FPL áp cả dòng dịch vụ và dòng thiết bị — SC-XHD-050 ghi rõ | QC owner 19/10/2026 | cl_open 18→17 |
| 2026-10-19 | UPDATE | CL-XHD-07 làm rõ thêm: tool cập nhật / kiểm tra trạng thái PĐK (thêm vào `07_environments/environments.md`); mỗi kênh bán test 1 hợp đồng doanh nghiệp. Còn mở: PĐK của đơn bán thêm | QC owner 19/10/2026 | Không |
| 2026-10-19 | UPDATE | **Đóng CL-XHD-24:** cutover có test — đơn luồng cũ / mới, không mất / trùng hóa đơn (URD 2.1 BR-DB-08). SC-XHD-107, 108 hết chờ CL. Hệ quả đã biết BR-DB-08 L304 (thiết bị bị bỏ sót, quét tay — ngoài phạm vi) ghi rõ trong CL | QC owner 19/10/2026 | cl_open 17→16 · blocked_by_cl 9→7 |
| 2026-10-19 | UPDATE | **Đóng CL-XHD-07:** đơn bán thêm trên hợp đồng tổ chức có PĐK mới riêng — phải duyệt PĐK mới mới xuất hóa đơn (hết GAP-61) | QC owner 19/10/2026 | cl_open 16→15 |
| 2026-10-19 | UPDATE | **Thêm SC-XHD-112, 113** (CL-XHD-07): đơn bán thêm trên hợp đồng doanh nghiệp — PĐK mới chưa duyệt ⇒ không xuất hóa đơn (P1 Negative); đã duyệt ⇒ phát hành (P2 Functional) | QC owner 19/10/2026 | SC 109→111 · P1 84→85 · P2 24→25 |
| 2026-10-20 | UPDATE | SC-XHD-030: màn Chi tiết hóa đơn — thông tin khách hàng đối chiếu theo hợp đồng, dòng dịch vụ / sản phẩm đối chiếu theo thông tin đơn hàng mua. SC-XHD-020: ghi rõ case cập nhật thông tin hợp đồng trong khi chờ phát hành hóa đơn ⇒ hệ thống ghi nhận thông tin hợp đồng mới (BR-DB-03 L359) | QC owner 20/10/2026 | Không |
| 2026-10-20 | UPDATE | Tool cập nhật thông tin hợp đồng: Inside › Quản lý hợp đồng › Cập nhật hợp đồng — thêm vào `07_environments/environments.md`, ghi vào SC-XHD-020 | QC owner 20/10/2026 | Không |
| 2026-10-20 | SCOPE↓ | **Kênh FPL (10) chỉ bán nhóm 5 FPT Play Stands Alone và 7 FPT Play** — SC-XHD-006 giới hạn 2 nhóm; ghi ngoại lệ ở CL-XHD-26, REQ-XHD-001 | QC owner 20/10/2026 | Không (SC giữ nguyên số) |
| 2026-10-20 | UPDATE | **Đóng CL-XHD-31:** hồi quy Shopee / TikTok chỉ test theo rule URD 2.2, không chờ URD v1.0 — SC-XHD-016, 017 viết lại Then; ghi chú SC-XHD-060, REQ-XHD-005, 020; RISK-XHD-09 → Mitigated | QC owner 20/10/2026 | cl_open 15→14 |
| 2026-10-20 | UPDATE | **Sửa kết luận CL-XHD-02 (vòng 4):** kênh FPL — khách không bấm Xuất hóa đơn / quá 2 giờ không nhập ⇒ hệ thống **vẫn phát hành hóa đơn với thông tin mặc định trên hợp đồng** (URD L355; BA trả lời tại CL-XHD-05), thay ý "không phát hành" của vòng 3. SC-XHD-032, 033, 034 viết lại Then; ghi chú SC-XHD-050, REQ-XHD-007, test_data_catalog | BA trả lời vòng 4 + QC owner 20/10/2026 | Không |
| 2026-10-20 | UPDATE | **Đóng CL-XHD-32 (vòng 4):** thanh toán 23:59 ngày cuối tháng, tín hiệu về 00:01 ngày 1 ⇒ phát hành ở đợt worker 12:05 ngày 1, BillDate = ngày phát hành — SC-XHD-046 viết lại theo ví dụ của BA, bỏ ⛔ · **Đóng CL-XHD-05 (vòng 4):** FPL quét 0h–2h chạy job 1 lần, 2h–4h chạy job 1 lần … — SC-XHD-047 viết lại, bỏ ⛔; ghi chú REQ-XHD-016, 017, test_data_catalog | BA trả lời vòng 4 + QC owner 20/10/2026 | cl_open 14→12 · blocked_by_cl 7→5 |
| 2026-10-20 | UPDATE | **Đóng CL-XHD-27, CL-XHD-34 (vòng 4):** TB hình thức "Không" gửi tín hiệu qua phiếu quầy — quầy gửi ⇒ xuất hóa đơn, **quầy không gửi ⇒ không xuất hóa đơn**; mix "Không" + TIN/PNC ⇒ theo phiếu thi công; ≥1 SPDV mix TIN/PNC ⇒ cả đơn đi luồng TINPNC. SC-XHD-109 viết lại (3 nhánh), bỏ ⛔; ghi chú REQ-XHD-004, 043, test_data_catalog | BA trả lời vòng 4 + QC owner 20/10/2026 | cl_open 12→10 · blocked_by_cl 5→4 |
| 2026-10-20 | SCOPE↓ | **Vòng 4 — QC không test / phần dành cho dev:** đóng CL-XHD-21 ⛔ (BR-XHD-18, REQ-XHD-039 ngoài phạm vi), CL-XHD-22 ⛔ (mail cảnh báo bản tin trễ, REQ-XHD-042 ngoài phạm vi), CL-XHD-29 ⛔ (tài liệu tích hợp — QC verify định tính), CL-XHD-13 (Type 1–4), CL-XHD-16 (job cảnh báo — **deprecated SC-XHD-097**), CL-XHD-19 (không xem log), CL-XHD-23 (race worker ↔ realtime — RISK-XHD-02 Closed), CL-XHD-33 (giữ URD 2.1 cho D#1–D#6, mốc nghiệp vụ theo giả định QC). SC-XHD-040, 045 bỏ ⛔. Ghi nhận vòng 4 cho CL-XHD-11, 12 (hỏi dev) | BA trả lời vòng 4 + QC owner 20/10/2026 | SC 111→110 (deprecated 3) · P3 1→0 · cl_open 10→2 · cl_blocking 3→0 · blocked_by_cl 4→1 |
| 2026-10-20 | UPDATE | **Đóng CL-XHD-11:** BA chốt khóa chống trùng theo BR-XHD-08 L419 (DV = mã đơn hàng + dịch vụ hóa đơn + gói dịch vụ; TB thêm phương thức triển khai), §C#3 L651 không áp dụng — SC-XHD-079, RISK-XHD-04, test_data_catalog. **SC-XHD-045 giữ rule:** mốc nghiệp vụ DV = ngày thanh toán, TB = ngày giao hàng (CL-XHD-33 bổ sung); ngày N không phải ngày cuối tháng — ngày cuối tháng → ngày 1 là ngoại lệ CL-XHD-32 / SC-XHD-046; RISK-XHD-03 cập nhật | BA chốt (QC owner chuyển lời) 20/10/2026 + QC owner | cl_open 2→1 |
| 2026-10-20 | UPDATE | **SC-XHD-046 viết lại:** đơn tạo 23:50, thanh toán 23:59 ngày 31/10, tín hiệu về 00:01 ngày 01/11 ⇒ mốc nghiệp vụ 00:01 ngày 01/11 ⇒ đợt worker 12:05 ngày 01/11 — đúng rule BR-XHD-01 L384, **không phải ngoại lệ**. **Mốc nghiệp vụ = thời điểm tín hiệu đẩy về hệ thống xuất hóa đơn** (CL-XHD-33 sửa định nghĩa). SC-XHD-045 bỏ điều kiện "không phải ngày cuối tháng"; RISK-XHD-03, test_data_catalog, REQ-XHD-016 cập nhật | QC owner 20/10/2026 | Không |
| 2026-10-20 | UPDATE | **CL-XHD-33 chốt lại:** worker xét theo mốc nghiệp vụ (thiết bị: ngày giao hàng · dịch vụ: ngày thanh toán); realtime phát hành theo thời điểm SPF đẩy về (thiết bị phải đã có ngày giao hàng, dịch vụ phải đã có ngày thanh toán) — thay định nghĩa "mốc = thời điểm tín hiệu về" của dòng trên; SC-XHD-045, RISK-XHD-03, test_data_catalog cập nhật | QC owner 20/10/2026 | Không |
| 2026-10-20 | UPDATE | SC-XHD-046: ngày thanh toán hệ thống ghi nhận = 00:01 ngày 01/11 (lúc SPF đẩy về), không phải 23:59 ngày 31/10 ⇒ worker 12:05 ngày 01/11 lấy dòng đúng rule; sửa chữ ở SC-XHD-046, CL-XHD-32, REQ-XHD-016, test_data_catalog | QC owner 20/10/2026 | Không |
| 2026-10-20 | SCOPE↓ | **Không test kênh SR-KPDV (SaleChannelID 18)** — **deprecated SC-XHD-014**; ghi ngoại lệ ở CL-XHD-26, REQ-XHD-001, 002, RISK-XHD-08, test_data_catalog | QC owner 20/10/2026 | SC 110→109 (deprecated 4) · P1 85→84 |

## 2. Ràng buộc còn hiệu lực

| # | Ràng buộc | Vì sao | Hệ quả nếu vi phạm |
|---|---|---|---|
| 1 | ⚠️ **URD 2.1 (`DOC-v2.0-02`) chỉ dùng cho các mục Phụ lục D của URD 2.2 trỏ về** (QC owner chốt 19/10/2026 — thay ràng buộc 16/10 "2.1 không sử dụng"): dùng D#1 cutover, D#2 chống phát hành trùng, D#3 RISK-01, D#4 cấu hình EVC (từ vòng 3 19/10/2026 — 2.2 ghi "Giữ nguyên (gộp nhóm BR-VC)"; bỏ bước 2.1 đánh dấu `[Bỏ]`), D#5 ký hiệu / ID / đơn vị đầu số riêng, D#6 dòng chiết khấu / thông tin theo mẫu. ⛔ **Không dùng:** D#7 mapping chi nhánh, D#8 câu hỏi mục V, D#9 autobill TB theo phương thức (2.2 ghi không còn áp dụng / đã bỏ). Phần chính 2.2 thắng khi mâu thuẫn. Chỉ cập nhật các CL QC owner chỉ định (CL-XHD-22, 23, 24 · CL-HK-02, 03, 10) | QC owner 19/10/2026 | Dùng 2.1 ngoài các mục trên ⇒ TC kiểm theo nội dung đã bỏ, bug bị bác |
| 2 | ⛔ **Giờ chốt / giờ chạy / số đợt / lịch FPL là tham số** — SC và TC viết "giờ chốt đợt N", không hardcode 12:00/18:00 | BR-XHD-01 L381, L383; Project_rule §Test Data Rules | Pilot đổi tham số ⇒ toàn bộ TC thời gian sai expected, phải viết lại |
| 3 | ⚠️ **Số dòng `L<n>` trong Source Location** là số dòng của bản trích text do `scripts/doc/search-doc.sh` sinh từ `.docx` (mỗi đoạn / ô bảng = 1 dòng). Đổi file `.docx` ⇒ L-number lệch | Cách trích ở `scripts/doc/search-doc.sh` | Reviewer mở sai vị trí; health-check F-05 báo quote không khớp — phải chạy lại verify quote (đã verify 100% quote URD ngày 2026-10-16) |
| 4 | ⚠️ **Risk xuyên suốt đặt ở XHD** (RISK-XHD-01 tài liệu tích hợp · RISK-XHD-02 phát hành trùng · RISK-XHD-10 cutover; CL-XHD-25 bán thêm · CL-XHD-29 tích hợp · CL-XHD-31 URD v1.0) — ảnh hưởng cả **GN** và **HK** | Layout v2 không có `_global/`; XHD là module đầu chuỗi | Sửa / đóng ở module khác ⇒ 2 home cho cùng nội dung, drift; GN/HK chỉ được **trỏ** về đây |
| 5 | ⛔ **TL (URD §IV — tính lương FPT Play SA) ngoài phạm vi** — không dựng thư mục `v2.0/TL/`, 0 REQ/SC là đúng | QC lead chốt 14/10/2026 (TP §2.2 #11) | Dựng TL ⇒ health-check báo module thiếu TC; effort ngoài kế hoạch |
| 6 | ⚠️ **`DOC-v2.0-05` (HT Triển khai) và `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png), `-FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png)` (ảnh màn Hệ thống Thông tin, hóa đơn 2025) không phải URD** — chỉ dùng làm dữ liệu / câu hỏi; không sinh rule mới từ chúng khi chưa có BA xác nhận | Tài liệu bổ sung, không version, chưa có người duyệt | Sinh expected theo file bổ sung ⇒ TC mâu thuẫn URD, bug sai căn cứ |
| 7 | ⚠️ **SC-XHD-001..017** fan-out theo **kênh**; chiều nhóm DV × loại đơn là **dữ liệu** — không tách thêm SC theo nhóm DV | Sufficiency Rule (1 lớp EP / SC); TP F01 680 TC | Tách SC theo nhóm ⇒ 340 SC trùng hành vi, vượt trần 200 SC/version |
| 8 | ⛔ **Câu trả lời vòng 1 của QC không phải xác nhận PO** — chỉ đóng CL khi chốt được bằng chữ URD 2.2; còn lại ghi `🔎 QC rà lại` và giữ Open | Người trả lời là QC owner, cột "Người trả lời" trống | Đóng CL theo ý kiến QC chưa có căn cứ ⇒ TC sai expected, bug bị dev bác |

## 3. Nợ đang mở

| # | Nợ | Trạng thái | Đích xử lý |
|---|---|---|---|
| 1 | ✅ REQ-XHD-039 (BR-XHD-18) — **ngoài phạm vi test** | Đóng 20/10/2026 (CL-XHD-21, BA vòng 4) | QC lead cập nhật Scope OUT của TP |
| 2 | ✅ REQ-XHD-042 (mail cảnh báo bản tin trễ) — **ngoài phạm vi test** | Đóng 20/10/2026 (CL-XHD-22, BA vòng 4) | QC lead cập nhật Scope OUT của TP |
| 3 | 🟡 CL-XHD-29 tài liệu tích hợp — BA: phần dành cho dev | Đóng 20/10/2026 | Verify định tính qua tool; RISK-XHD-01 còn mở |
| 4 | ✅ CL-XHD-11 khóa chống trùng — BA chốt theo BR-XHD-08 L419 | Đóng 20/10/2026 | — |
| 5 | 🟡 18 SC có Then `⛔ chờ CL-…` / `(giả định TP)` (đếm ở `counts.blocked_by_cl`) | Theo giả định của TP §2.4 | Khi CL resolved: `--update` sửa Then, ghi 1 dòng UPDATE ở §1 |
| 6 | ✅ CL-XHD-30 đơn ngoài 17 kênh / ServiceID 2, 22 — **ngoài scope test** (TP §2.2 #6 + QC trả lời vòng 2 "bỏ qua không test") ⇒ không thêm SC negative | Đóng 19/10/2026 | — |
| 7 | 🟡 CL-XHD-27, CL-XHD-28 mới phát hiện khi analyze (chưa có GAP-ID) | Chưa đưa vào DOC-READINESS / TP §2.4 | QC owner thêm vào danh sách gửi PM (create-test-plan `--update`) |
