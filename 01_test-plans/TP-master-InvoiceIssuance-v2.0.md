# Test Plan: Invoice Issuance Architecture — v2.0

## 1. Giới thiệu
- **Dự án:** Invoice Issuance Architecture — Phase 2 (PO: Nguyễn Thị Ngọc Hoa — hoantn13, DVKH · PM: Lê Thị Mỹ Lệ — Leltm)
- **Version:** v2.0
- **Loại:** Master
- **Loại dự án:** INT — backend tích hợp event-driven (SPF → Kafka → INVOICE → Billing / HĐĐT / Dịch vụ / FHR), không có UI
- **Mô hình:** Waterfall
- **Mục tiêu:** Kiểm chứng các yêu cầu của URD Phase 2 (Revision 2.2, 08/10/2026 — phần kỹ thuật tham chiếu Revision 2.1): xuất hóa đơn tự động cho 17 kênh bán và 55 dịch vụ trong phạm vi, cả đơn bán mới và đơn bán thêm, 1 đơn 1..n hóa đơn; gạch nợ Paid / Cọc gồm gạch nợ tạm; đẩy hậu kỳ (HĐĐT + tiền trả trước) theo cấu trúc mới (tính lương FPT Play SA ngoài phạm vi). Đồng thời bảo đảm luồng TMĐT của Phase 1 vẫn đúng sau khi chuyển sang rule chung.
- **Ngày tạo:** 07/10/2026 · **Cập nhật:** 14/10/2026 (thêm Round 3 recheck bug 12–13/11; mã chức năng FR01–FR11; FR01 gồm ma trận kênh × nhóm DV × bán mới / bán thêm; TL tính lương FPT Play SA ra ngoài phạm vi; Scope test gom 11 chức năng; lịch QC lead chốt 19/10–10/11/2026; bản xuất không có DatDGD)

## 2. Phạm vi (Scope)

### 2.0. Version Context
- **Version:** v2.0
- **Parent version:** v1.0 (Phase 1 — kênh TMĐT Shopee, Tiktok; chưa có test plan / TC trong workspace này)
- **Delta:** Bỏ chia rule theo kênh và ngày thường / cuối tháng, dùng một lịch worker có tham số (12:05, 18:05) + nhánh realtime; riêng kênh FPL có lịch 2h/lần, delay 2h và realtime sau 22h. Một đơn hàng ra 1..n hóa đơn (DV theo thanh toán, TB theo phương thức triển khai). Thêm điều kiện hợp đồng tổ chức phải duyệt PĐK, không phát hành trên hợp đồng con; thông tin khách xuất HĐ theo hợp đồng (FPL cho khách tự nhập); chi nhánh xuất HĐ = chi nhánh quản lý hợp đồng. Gạch nợ mở rộng sang Paid (có gạch nợ tạm cho kênh sàn) và Cọc; gạch EVC do đội EVC thực hiện. Hậu kỳ tách theo đơn hàng. Tính lương FPT Play SA xét thêm bảng tồn mới.

### 2.1. Trong phạm vi (In Scope)

| # | Module | Mô tả | Test Approach |
|---|--------|-------|--------------|
| 1 | XHD — Đồng bộ đơn hàng & xuất hóa đơn tự động (URD §I) | Đồng bộ sự kiện SPF + tín hiệu giao hàng 3 nguồn; thông tin khách xuất HĐ; lịch worker / realtime (gồm lịch riêng FPL); điều kiện phát hành DV / TB, duyệt PĐK, hợp đồng con; gộp / tách hóa đơn; chống trùng; điều kiện hợp lệ; chi nhánh theo hợp đồng; phát hành qua Billing; cutover v1 → v2 *(chờ PM xác nhận)* | Manual — E2E qua log Kafka + dữ liệu bảng |
| 2 | GN — Gạch nợ hóa đơn (URD §II) | Đồng bộ Paid; 3 điểm chạm; xác định phương thức Paid / Cọc; gạch nợ tạm / gỡ gạch nợ tạm; gạch nợ thật bằng Paid (chừa phần EVC bị lock); gạch nợ bằng Cọc | Manual — E2E + mock/stub API kênh thanh toán / đội EVC khi STG chưa sẵn |
| 3 | HK — Đẩy hậu kỳ, tiền trả trước (URD §III) | Phạm vi đẩy theo đơn hàng; chuẩn bị ký hiệu / ID / nội dung / tổng tiền theo thuế suất / thông tin mẫu; đẩy HĐĐT; tiền trả trước một lần mỗi đơn | Manual — đối chiếu dữ liệu chuẩn bị + kết quả bên HĐĐT / Dịch vụ |

> Luồng xuyên module (đơn → hóa đơn → gạch nợ → hậu kỳ) là **cách test** (§3.2), không phải module riêng.
> TC của luồng gán về module đầu chuỗi và module chốt kết quả cuối.
> **Loại đơn:** cả **bán mới** và **bán thêm** (trên hợp đồng đang hoạt động) — PM xác nhận qua mail 13/10/2026 ("Bán mới, Bán thêm => ok"), áp cho cả 3 module trong phạm vi.
> URD không phân biệt loại đơn ⇒ test theo giả định rule áp chung (GAP-60).

#### 2.1a. Scope test theo chức năng ★

> Nguồn cho Excel `Tổng quan & Scope` mục D và Email Section A. **Mã chức năng FR01–FR11** (quy tắc `FRxx`, chốt 14/10/2026) gom từ 25 mã phân tích.
> Mã phân tích giữ `Fxx` (F01–F29) — dùng ở §2.3, §2.4, DOC-READINESS; cột cuối là bảng map.
> `*` = phần `Chờ bổ sung` (F11, F21, F29) — nằm trong chức năng nhưng chưa tính vào Est#TC.

| ID | Chức năng (In-scope) | Nhóm | Ưu tiên | HT phụ thuộc | Input cần có | Output kỳ vọng | Est#TC | Gồm mã phân tích |
|---|---|---|---|---|---|---|---:|---|
| FR01 | Đồng bộ đơn hàng SPF → INVOICE: tạo đơn từ 17 kênh bán × 20 nhóm dịch vụ × bán mới / bán thêm; tín hiệu giao hàng 3 nguồn; thông tin khách xuất hóa đơn | XHD | P1 | SPF | Đơn hàng tạo trên 17 kênh bán (§A.2) × 20 nhóm dịch vụ (§A.3) × bán mới / bán thêm; sự kiện đơn SPF (Kafka); tín hiệu phiếu thi công / Vendor / quầy; thông tin hợp đồng / khách FPL tự nhập | Ghi nhận đủ đơn của 17 kênh bán × 20 nhóm dịch vụ, cả bán mới và bán thêm (340 tổ hợp × 2 = 680 đơn); thiết bị map đúng tín hiệu giao hàng; thông tin khách đúng trên hóa đơn | 756 | F01, F02, F27 |
| FR02 | Lịch xuất hóa đơn + phân luồng worker / realtime (gồm kênh FPL) | XHD | P1 | FR01 | Lịch tham số 12:05 / 18:05, giờ chốt; lịch FPL 2h/lần, mốc 22:05, delay 2h | Dòng đi đúng luồng worker / realtime, đúng mốc FPL; xuất hóa đơn được đủ các dịch vụ, các kênh bán hàng, các đơn bán mới / bán thêm | 48 | F03, F28, F11* |
| FR03 | Điều kiện phát hành DV / TB (PĐK, hợp đồng con) + điều kiện hợp lệ | XHD | P1 | FR01 | Tín hiệu thanh toán / giao hàng; HĐ tổ chức, HĐ con; thông tin chung + chi tiết dịch vụ của đơn | Đơn đủ điều kiện được phát hành; không hợp lệ thì không phát hành + ghi log; xuất hóa đơn được đủ các dịch vụ, các kênh bán hàng, các đơn bán mới / bán thêm | 109 | F04, F07 |
| FR04 | Gộp / tách hóa đơn (1 đơn n hóa đơn) + chống phát hành trùng | XHD | P1 | FR02, FR03 | Các dòng DV / TB đủ điều kiện trong cùng đợt; dòng đã có BillNumber, log Kafka lặp | 1..n hóa đơn đúng cách gộp / tách; mỗi dòng chỉ xuất hóa đơn một lần; xuất hóa đơn được đủ các dịch vụ, các kênh bán hàng, các đơn bán mới / bán thêm | 53 | F05, F06 |
| FR05 | Phát hành hóa đơn qua Billing + Invoice Event + chi nhánh xuất hóa đơn | XHD | P1 | FR04 | Dòng đủ điều kiện; chi nhánh quản lý hợp đồng | BillNumber, BillDate, chi nhánh đúng; Invoice Event cho gạch nợ / hậu kỳ; xuất hóa đơn được đủ các dịch vụ, các kênh bán hàng, các đơn bán mới / bán thêm | 37 | F08, F09, F29* |
| FR06 | Cutover v1 → v2 + kiểm tra chéo | XHD | P2 | FR05 | Đơn luồng cũ / luồng mới | Không mất / trùng hóa đơn khi chuyển | 18 | F10 |
| FR07 | Đồng bộ Paid + điểm chạm + xác định phương thức Paid / Cọc | GN | P1 | FR05 | Paid từ kênh thanh toán; 3 điểm chạm; trường Paid / Cọc | Paid ghi nhận vào INVOICE; rẽ đúng luồng gạch nợ | 48 | F12, F13 |
| FR08 | Gạch nợ bằng Paid: gạch nợ tạm (kênh sàn), gạch nợ thật, chừa phần EVC bị lock | GN | P1 | FR07 | Đơn kênh Shopee, Tiktok; Paid hoàn tất, hóa đơn còn nợ; tổng tiền EVC + lock | Gạch nợ tạm / gỡ đúng; Payment, trừ Paid, Kafka Out; phần EVC không bị gạch bằng tiền khách | 66 | F14, F15, F16 |
| FR09 | Gạch nợ bằng Cọc | GN | P1 | FR07 | Tồn cọc theo loại, đơn bán mới / bán thêm | Trừ cọc + gạch nợ đúng | 40 | F17 |
| FR10 | Đẩy hậu kỳ theo đơn: ký hiệu + ID, nội dung + tổng tiền theo thuế suất, thông tin mẫu, đẩy HĐĐT | HK | P1 | FR05 | Hóa đơn đã phát hành theo đơn; loại hóa đơn, vùng; dòng hóa đơn, thuế suất | Đúng tập hóa đơn được đẩy; ký hiệu / ID, nội dung, tổng tiền theo từng thuế suất đúng; HĐĐT được gen | 71 | F18, F19, F20, F22, F21* |
| FR11 | Tiền trả trước một lần mỗi đơn | HK | P1 | FR10 | Đơn nhiều đợt hóa đơn | Add tiền trả trước đúng 1 lần / đơn; đủ các dịch vụ, các kênh bán hàng, các đơn bán mới / bán thêm | 18 | F23 |
| | **Tổng Est#TC** | | | | | | **1.264** | |

#### 2.1b. Hệ thống liên kết ★

> 17 kênh bán (URD 2.2 §A.2) là nơi QC tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ (§A.3) — đầu vào của FR01.
> FHR không liệt kê vì đối soát FHR ngoài phạm vi (§2.2).

| # | Hệ thống | Vai trò | Loại kết nối | Chức năng phụ thuộc | Mức | Rủi ro thời gian |
|---|---|---|---|---|---|---|
| 1 | Kênh bán Mobile — SaleChannelID 1 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 2 | Kênh bán Desktop — SaleChannelID 2 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 3 | Kênh bán DKOL — SaleChannelID 4 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 4 | Kênh bán API (partner ngoài FTEL) — SaleChannelID 7 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 5 | Kênh bán W-Sale — SaleChannelID 9 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 6 | Kênh bán FPL (FPT Play) — SaleChannelID 10 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01, FR02 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 7 | Kênh bán VNTT — SaleChannelID 11 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 8 | Kênh bán MBBank — SaleChannelID 12 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 9 | Kênh bán CRM — SaleChannelID 13 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 10 | Kênh bán TGDD — SaleChannelID 14 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 11 | Kênh bán F-Retail (FPT Shop) — SaleChannelID 15 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 12 | Kênh bán CMR-App (FSS) — SaleChannelID 16 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 13 | Kênh bán Momo — SaleChannelID 17 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 14 | Kênh bán SR-KPDV — SaleChannelID 18 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 15 | Kênh bán HiFPT — SaleChannelID 19 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 16 | Kênh bán Shopee — SaleChannelID 20 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01, FR08 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 17 | Kênh bán Tiktok — SaleChannelID 21 | Tạo đơn hàng bán mới / bán thêm cho 20 nhóm dịch vụ | SPF đồng bộ | FR01, FR08 | Cao | Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh |
| 18 | SPF | Nguồn sự kiện đơn hàng | Kafka (Order Event) | XHD | Cao | Log Kafka trùng / đảo thứ tự / trễ |
| 19 | Billing System | Phát hành hóa đơn | API | XHD | Cao | Không sẵn sàng trên STG |
| 20 | Phiếu thi công | Tín hiệu giao hàng hoàn tất khi phiếu ở tình trạng "Đã xử lý hoàn tất" | Tín hiệu đẩy về INVOICE | FR01 | Cao | Cần cách phát tín hiệu trên STG |
| 21 | Vendor | Tín hiệu giao hàng hoàn tất khi đối tác giao xong | Tín hiệu đẩy về INVOICE | FR01 | Cao | Cần cách phát tín hiệu trên STG |
| 22 | Quầy (phiếu giao tại quầy) | Tín hiệu giao hàng hoàn tất khi giao tại quầy | Tín hiệu đẩy về INVOICE | FR01 | Cao | Cần cách phát tín hiệu trên STG |
| 23 | Kênh thanh toán / đội EVC | Paid, Cọc, tiền EVC + lock | API, Kafka Out | GN | Cao | Cần hệ thống giả lập khi STG chưa sẵn sàng |
| 24 | Hóa đơn điện tử (HĐĐT) | Nhận HĐĐT hậu kỳ | API | HK | Cao | Không sẵn sàng trên STG |
| 25 | Hệ thống Dịch vụ | Nhận tiền trả trước | API | HK | TB | Không sẵn sàng trên STG |

### 2.2. Ngoài phạm vi (Out of Scope)

| # | Module / Feature | Lý do |
|---|-----------------|-------|
| 1 | Xuất hóa đơn tay | URD 2.2 §A.1 #4: "Chưa bao gồm xuất hóa đơn tay." |
| 2 | Điều chỉnh / hủy hóa đơn khi hủy đơn đã có hóa đơn | BR-XHD-10: "Hủy đơn khi đã có hóa đơn: hệ thống không tự hủy hay điều chỉnh hóa đơn, xử lý theo quy trình riêng." |
| 3 | Điều chỉnh hóa đơn đã phát hành khi chi nhánh đổi giữa các lần phát hành | URD 2.1 BR-XHD-12: nghiệp vụ Điều chỉnh, ngoài phạm vi. 2.2 không nhắc lại — chi nhánh xác định tại thời điểm phát hành |
| 4 | Thuộc tính chi nhánh nào được bán sản phẩm / dịch vụ nào | BR-XHD-12: "do bên quản lý sản phẩm bổ sung thuộc tính, nằm ngoài URD này" |
| 5 | Gạch nợ bằng EVC / voucher | BR-VC: "Phần gạch nợ bằng EVC do đội EVC thực hiện". INVOICE chỉ chừa phần EVC bị lock khi gạch tiền khách — phần này trong scope (GN) |
| 6 | ServiceID 2 (SubServiceType 5–9) và ServiceID 22 (GSafe) | URD 2.2 §A.3: "Không có trong danh sách phạm vi" |
| 7 | Xử lý hóa đơn dư khi phát hành trùng | Phụ lục D#2 (URD 2.1 BR-XHD-09: xử lý theo quy trình điều chỉnh / thay thế riêng) |
| 8 | Quét tay bổ sung đơn bị bỏ sót trong giai đoạn giao thoa cutover | Phụ lục D#1 (URD 2.1 BR-DB-08: "QUÉT TAY BỔ SUNG, không xây cơ chế tự động") |
| 9 | Xuất hóa đơn bổ sung case-by-case cho log Kafka trễ qua ngày | Phụ lục D#3 (URD 2.1 RISK-01: không nằm trong luồng tự động) |
| 10 | Performance / Security testing | URD không có SLA tải hay yêu cầu bảo mật |
| 11 | Điều chỉnh tính lương FPT Play SA (URD §IV — F24 gộp 2 nguồn + khử trùng + tính hoa hồng, F25 lọc FPT Play SA, F26 đối soát FHR) | QC lead chốt 14/10/2026: ngoài phạm vi test v2.0. Riêng đối soát FHR theo BR-TL-04 do FHR nghiệm thu ở UAT |

### 2.3. Đánh giá tài liệu đầu vào (Doc Readiness) ★

> Chỉ có trong Markdown — **không** render ra Excel / Email khi export.
> Bản đầy đủ (diff 2.1 → 2.2, B1–B4, checklist có trích dẫn, mail PM): `01_test-plans/DOC-READINESS-InvoiceIssuance-v2.0.md`.

- **Kết luận:** ⚠️ CONDITIONAL — 23/26 chức năng trong phạm vi estimate được (8 Đủ, 15 Giả định), 3 chức năng Chờ bổ sung (F11, F21, F29). TL (F24–F26) chuyển Ngoài phạm vi 14/10/2026; ma trận kênh × nhóm dịch vụ × bán mới / bán thêm nằm trong F01
- **Lần rà:** 2 — Lần 1: 07/10/2026 trên URD rev 2.1 · Lần 2: 13/10/2026 trên URD rev 2.2 · **Người rà:** HuyenNHK
- **Đếm từ tài liệu:** 29 luồng/chức năng · 27 action xử lý · 26 rule điều kiện · 7 đầu ra kiểm chứng · 17 kênh bán · 20 nhóm / 55 dịch vụ
- **Checklist Gate 1:** 12 Pass · 14 Fail · 4 N/A (lần 1: 9 · 15 · 4)
- **DOC-GAP:** 15/39 GAP lần 1 đã đóng · 24 còn thiếu · 22 GAP mới (18 phát sinh trong nội dung mới/sửa của 2.2, 2 về phạm vi bán mới + bán thêm)

| # | Tài liệu | Version | Ngày | Trạng thái | Ghi chú |
|---|----------|---------|------|-----------|---------|
| 1 | URD Invoice Issuance Architecture — **bản chính** | Revision 2.2 | 08/10/2026 | PO đã confirm (mail PM 13/10/2026); Approver trên tài liệu trống | Header = Revision = tên file |
| 2 | URD Invoice Issuance Architecture — tham chiếu kỹ thuật | Revision 2.1 | 26/08/2026 | Bị 2.2 thay phần chính | Phụ lục D của 2.2 trỏ về bản này |
| 3 | Lưu đồ Hình I–IV (nhúng trong URD 2.2) | — | — | — | Link draw.io: placeholder (GAP-58) |
| 4 | URD v1.0 — Phase 1 | 1.0 | 25/02/2026 | — | Chưa nhận (GAP-24) |
| 5 | Email ISC 24/09 + email FTQ 30/09/2026 | — | — | — | Chưa nhận (GAP-57) |
| 6 | Tài liệu tích hợp (Kafka, schema, API) | — | — | — | Chưa nhận (GAP-07) |
| 7 | Mail PM LeLTM | — | 13/10/2026 | PO đã confirm URD 2.2 | Kênh + nhóm sản phẩm theo URD; bán mới + bán thêm OK; EVC theo rule URD. Bản PDF đính kèm (bản PO confirm) đã đối chiếu: nội dung = bản .docx đang dùng |

| # | Chức năng | Trạng thái tài liệu | Est#TC | QC | GAP liên quan |
|---|-----------|--------------------|-------:|----|---------------|
| F01 | Đồng bộ đơn hàng SPF → INVOICE — tạo đơn từ 17 kênh bán × 20 nhóm dịch vụ × bán mới / bán thêm | Giả định | 29 (+20%) + 680 ma trận = 709 | GiangDC2 (ma trận chia 4 QC theo kênh, §6) | GAP-42, 60; 26, 62 (Major) |
| F02 | Tín hiệu giao hàng hoàn tất 3 nguồn | Đủ | 21 | GiangDC2 | GAP-27 (Major) |
| F03 | Lịch worker + phân luồng worker / realtime | Giả định | 26 (+20%) | HuyenNHK | GAP-11, 43 |
| F04 | Điều kiện phát hành DV / TB + PĐK + hợp đồng con | Giả định | 51 (+20%) | HuyenNHK | GAP-44, 60; 45, 46, 47, 54, 61 (Major) |
| F05 | Gộp / tách hóa đơn, 1 đơn n HĐ | Đủ | 24 | HuyenNHK | GAP-54 (Major) |
| F06 | Chống phát hành trùng | Giả định | 29 (+20%) | HuyenNHK | GAP-12, 41, 60 |
| F07 | Điều kiện hợp lệ + xử lý không hợp lệ + job cảnh báo | Giả định | 58 (+20%) | GiangDC2 | GAP-13, 31; 29, 30, 55 (Major) |
| F08 | Chi nhánh xuất hóa đơn (theo hợp đồng) | Đủ | 15 | GiangDC2 | — |
| F09 | Phát hành qua Billing + Invoice Event | Giả định | 22 (+20%) | GiangDC2 | GAP-14 |
| F10 | Cutover v1 → v2 + kiểm tra chéo | Giả định | 18 (+20%) | GiangDC2 | GAP-32 (đề xuất PM xác nhận scope) |
| F11 | Mail cảnh báo bản tin trễ qua ngày | Chờ bổ sung | *chưa estimate (tham khảo 9)* | — | GAP-02 |
| F12 | Đồng bộ Paid | Đủ | 21 | AnhPTM17 | — |
| F13 | Điểm chạm + phương thức Paid / Cọc | Đủ | 27 | AnhPTM17 | — |
| F14 | Gạch nợ tạm / gỡ gạch nợ tạm | Đủ | 18 | AnhPTM17 | — |
| F15 | Gạch nợ thật bằng Paid | Giả định | 33 (+20%) | AnhPTM17 | GAP-40 |
| F16 | Chừa phần EVC bị lock khi gạch tiền khách | Giả định | 15 (+20%) | AnhPTM17 | GAP-16, 40 |
| F17 | Gạch nợ bằng Cọc | Giả định | 40 (+20%) | AnhPTM17 | GAP-16, 60 |
| F18 | Phạm vi đẩy hậu kỳ theo đơn | Đủ | 12 | DatDGD | — |
| F19 | Ký hiệu + ID hóa đơn điện tử | Giả định | 33 (+20%) | DatDGD | GAP-17, 60; 34 (Major) |
| F20 | Nội dung hiển thị + tổng tiền theo thuế suất | Đủ | 15 | DatDGD | — |
| F21 | Dòng EVC + chiết khấu trên HĐĐT | Chờ bổ sung | *chưa estimate (tham khảo 9)* | — | GAP-04 |
| F22 | Thông tin theo mẫu + đẩy HĐĐT | Giả định | 11 (+20%) | DatDGD | GAP-18; 35 (Major) |
| F23 | Tiền trả trước một lần mỗi đơn | Giả định | 18 (+20%) | DatDGD | GAP-20, 60; 59 (Major) |
| ~~F24~~ | ~~Gộp 2 nguồn + khử trùng + tính hoa hồng~~ | **Ngoài phạm vi** (14/10/2026) | — | — | GAP-36 (đóng) |
| ~~F25~~ | ~~Lọc FPT Play SA trên bảng tồn mới~~ | **Ngoài phạm vi** (14/10/2026) | — | — | — |
| ~~F26~~ | ~~Đối soát FHR (UAT)~~ | **Ngoài phạm vi** (14/10/2026) | — | — | GAP-06 (QC lead chốt Out-scope) |
| F27 | Thông tin khách xuất hóa đơn (FPL khách tự nhập) | Giả định | 26 (+20%) | DatDGD | GAP-48, 60; 49 (Major) |
| F28 | Kênh FPL: delay 2h, lịch 2h/lần, mốc 22:05, realtime sau 22h | Giả định | 22 (+20%) | HuyenNHK | GAP-50; 51, 52 |
| F29 | Clear "thuê thiết bị đầu cuối" (BR-XHD-18) | Chờ bổ sung | *chưa estimate (tham khảo 9)* | — | GAP-53 |
| | **Tổng commit** | | **1.264** | | *Tham khảo Chờ bổ sung: 27* |

> **Ma trận trong F01 (thêm 14/10/2026 dưới tên ma trận F01, gộp vào F01 cùng ngày):** mỗi TC = 1 kênh × 1 nhóm DV × 1 loại đơn:
> tạo đơn trên kênh → đồng bộ về INVOICE → ghi nhận đủ đơn; kết quả xuất hóa đơn của từng tổ hợp kiểm ở output các chức năng hóa đơn
> (F03–F06, F08, F09, F27, F28). 17 × 20 × 2 = 680 TC. Không cộng 20% — 680 là trần; khi PM chốt những cặp kênh ↔ nhóm DV
> không bán (GAP-62), mỗi cặp bỏ ra giảm 2 TC.

### 2.4. Danh sách cần bổ sung — PM xác nhận trước 16/10/2026 ★

> `D_confirm` = **16/10/2026** — ngày làm việc liền trước ngày QC bắt đầu Clear nghiệp vụ (**19/10/2026**).
> PM chọn cho **từng dòng**: `Bổ sung trước [ngày]` · `Out-scope` · `Giữ giả định của QC`.
> "OK" chung cho cả file không tính là xác nhận.
> "Đưa vào rủi ro?" = `Chưa chốt` cho tới khi trao đổi xong; chỉ dòng chốt `Có` mới thêm vào §7.
> Chỉ có trong Markdown — **không** render ra Excel / Email khi export. Trích dẫn đầy đủ: DOC-READINESS §E.
> **Đã đóng ở lần rà 2 (URD 2.2):** GAP-01, 03, 05, 08, 10, 15, 19, 21, 23, 25, 28, 33, 37, 38, 39 — căn cứ ở DOC-READINESS §E.2.

| GAP-ID | Lần 2 | Mã | Severity | Chức năng | Thiếu gì | Câu hỏi cho BA | Ảnh hưởng plan | Hạn PM xác nhận | Ticket | PM xác nhận | Đưa vào rủi ro? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-02 | Còn thiếu | L3 | Blocker | F11 | Mail cảnh báo "bắt buộc" (D#3) nhưng không có điều kiện / lịch / người nhận / nội dung | Có thuộc v2.0 không? Ai cung cấp đặc tả? | Chờ bổ sung (~9 TC) | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-04 | Còn thiếu | L3 | Blocker | F21 | BR-HK-02 nhắc "dòng EVC"; dòng EVC / chiết khấu chuyển D#6, chưa định nghĩa | Theo mail PM "EVC theo rule URD": dòng EVC / chiết khấu (chỉ ở phụ lục) có ngoài phạm vi test? Nếu không: loại EVC nào + format | Chờ bổ sung (~9 TC); đề xuất Out-scope | 16/10/2026 | chưa log | | **Có** — rủi ro #7 (14/10/2026) |
| GAP-06 | **Đóng 14/10 — Out-scope** (QC lead chốt) | L2 | Blocker | F26 | Đối soát FHR thuộc UAT, FHR nghiệm thu (BR-TL-04); plan QC không có UAT | Xác nhận out-scope của QC? Nếu QC hỗ trợ: phần nào | Chờ bổ sung (~6 TC); đề xuất Out-scope | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-53 | Mới | L3 | Blocker | F29 | BR-XHD-18 chỉ 1 câu; "(kịp plan …)"; không rõ thao tác, UI, kết quả trên HĐ | Có thuộc v2.0? Nếu có: đặc tả + thiết kế nếu có UI | Chờ bổ sung (~9 TC) | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-07 | Còn thiếu | L1 | Critical | Toàn bộ | Không có payload Kafka, schema bảng, API, bảng enum (D chỉ trỏ "xem URD v2.1") | Gửi SDD / API spec / schema + enum | Chặn Setup data + Execute | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-09 | Còn thiếu | L9 | Critical | Toàn bộ | §C 3 điểm cần xác nhận không có owner + ngày chốt | Điền owner + ngày (≤ 19/10) | Quyết định GAP-17, 41 có kịp lịch không | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-11 | Còn thiếu | L9 | Critical | F03 | Xử lý bản tin trễ qua ngày chưa quyết (D#3) | Chọn phương án, có trong v2.0? | Giả định hiện trạng | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-12 | Còn thiếu | L9 | Critical | F06 | Phương án chặn trùng worker ↔ realtime (D#2) | Phương án + ngày có | Case song song test sau | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-13 | Còn thiếu | L5 | Critical | F07 | "Hợp đồng có hiệu lực", "đang cập nhật" chưa định nghĩa | Liệt kê giá trị trạng thái | Giả định theo v1.0 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-14 | Còn thiếu | L4 | Critical | F09 | Billing lỗi / timeout không có hành vi | Retry / giữ rỗng / cảnh báo? | Giả định giữ rỗng + log | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-16 | Còn thiếu | L4 | Critical | F16, F17 | Nguồn tổng tiền EVC + lock không nêu ở 2.2; lỗi / timeout không có hành vi | API đội EVC? Lỗi áp như BR-XL-03? | Giả định như BR-XL-03 | 16/10/2026 | chưa log | | **Có** — rủi ro #7 (14/10/2026) |
| GAP-17 | Còn thiếu | L6 | Critical | F19 | Ký hiệu HĐĐT "cần chốt" (DVKH HO ↔ FAF); bảng map ở tài liệu kỹ thuật | Gửi bản chốt ký hiệu + bảng map; HĐ bán mới / bán thêm dùng đầu nào? | Giả định trên bảng map 2.1 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-18 | Còn thiếu | L4 | Critical | F22 | Đẩy HĐĐT lỗi không có hành vi | Retry / đánh dấu? | Giả định đẩy lại lần sau | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-20 | Còn thiếu | L4 | Critical | F23 | Đẩy hệ thống Dịch vụ lỗi không có hành vi | Đánh dấu / retry? | Giả định đẩy lại lần sau | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-31 | Còn thiếu ↑ | L3 | Critical | F07 | Job cảnh báo 15 phút nay nằm trong BR-XHD-10 (in-scope) nhưng không có đặc tả | Điều kiện, kênh, người nhận, nội dung | Chưa tính TC (+~9 nếu in-scope) | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-40 | Mới | L7 | Critical | F15, F16 | Paid "gồm cả voucher" ↔ EVC do đội EVC gạch; BR-GN-01 không loại Paid voucher | Paid voucher có bị loại khỏi gạch nợ? Thứ tự với đội EVC? | Giả định loại Paid voucher | 16/10/2026 | chưa log | | **Có** — rủi ro #7 (14/10/2026) |
| GAP-41 | Mới | L7 | Critical | F06 | BR-XHD-08 đổi khóa chống trùng nhưng ghi "Giữ nguyên"; mâu thuẫn §C#3, BR-DB-07 | Khóa chốt theo bản nào, field nào? | Giả định theo text 2.2 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-42 | Mới | L7 | Critical | F01 | BR-DB-01 bỏ sự kiện tạo đơn + cập nhật thông tin KH, nhưng BR-DB-03 / BR-XHD-03 vẫn cần | Hai sự kiện còn đồng bộ không? | Giả định đủ 4 sự kiện như 2.1 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-43 | Mới | L7 | Critical | F03 | "Cuối tháng sau giờ chốt cuối → phát hành sang tháng sau" ↔ realtime "xử lý ngay" | Realtime có chạy ngày cuối tháng? | Giả định realtime vẫn chạy | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-44 | Mới | L4 | Critical | F04 | "Quên duyệt PĐK thì không autobill" — duyệt muộn thì đợt sau có phát hành? | Duyệt muộn xử lý ra sao? | Giả định đợt kế tiếp phát hành | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-48 | Mới | L4 | Critical | F27 | FPL: "(ví dụ FPL)"; khách không lấy HĐ / quá 2 giờ không nhập: không đặc tả | Chỉ FPL? Không lấy HĐ / quá 2 giờ → ? | Giả định dùng thông tin hợp đồng | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-50 | Mới | L5 | Critical | F28 | Lịch FPL "2h quét 1 lần" + "Mốc 22:05" không đủ để biết từng đợt | Liệt kê mốc chạy / giờ chốt; có tham số? | Giả định 0:05 … 22:05 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-60 | Mới | L2 | Major | F01, F04, F06, F17, F19, F23, F27 | Phạm vi gồm bán mới + bán thêm nhưng URD không phân biệt loại đơn | Xác nhận BR áp chung; nêu điểm khác cho đơn bán thêm (nếu có) | Giả định áp chung; +31 TC | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-24 | Còn thiếu | L1 | Major | Toàn bộ | Chưa nhận URD v1.0 | Gửi URD v1.0 + hành vi Phase 1 giữ / đổi | Regression TMĐT theo giả định | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-26 | Còn thiếu | L4 | Major | F01 | Bản tin lỗi giải mã / thiếu trường | Hành vi? | Giả định bỏ qua + log | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-27 | Còn thiếu | L6 | Major | F02 | Cột Note: bảng + format | Đặc tả | Expected không định lượng | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-29 | Còn thiếu | L6 | Major | F07 | Log không hợp lệ: nơi ghi + nội dung | Đặc tả | Như trên | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-30 | Còn thiếu | L5 | Major | F04, F07 | Thứ tự validate, cách log nhiều lỗi | Đặc tả | +TC tổ hợp | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-32 | Còn thiếu | L2 | Major | F10 | Cutover chuyển phụ lục kỹ thuật (PM, SA) — có test trên STG không | Xác nhận scope + data luồng cũ | Giả định in-scope; Out-scope −18 TC | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-34 | Còn thiếu | L2 | Major | F19 | Đơn vị có đầu số / mẫu riêng: in / out scope? | Xác nhận scope | Chưa tính TC | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-35 | Còn thiếu | L3 | Major | F22 | Danh sách trường theo từng mẫu HĐĐT (D#6) | Đặc tả | Expected thiếu trường | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-36 | **Đóng 14/10 — TL ngoài phạm vi** | L3 | Major | F24 | Công thức hoa hồng | Gửi công thức hiện hành | Giả định giữ công thức cũ | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-45 | Mới | L6 | Major | F04 | Nhận diện HĐ tổ chức, nguồn trạng thái PĐK, cách tính 2 ngày cuối tháng | Field + giá trị + cách tính | Giả định theo loại hình KH cấp 1 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-46 | Mới | L4 | Major | F04 | HĐ con không phát hành — ghi nhận ra sao, HĐ cha có phát hành thay? | Đặc tả đầu ra | Giả định chỉ không phát hành | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-47 | Mới | L10 | Major | F04 | Revision 2.2 ghi "KH Chuỗi/Dự án" nhưng BR-XHD-03 không có nội dung | KH Chuỗi có rule riêng? | Có thể thiếu TC | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-49 | Mới | L6 | Major | F27 | 7 trường khách tự nhập: bắt buộc / định dạng / ai kiểm tra | Đặc tả | Giả định kênh FPL kiểm tra | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-51 | Mới | L7 | Major | F28 | Mốc delay: "thời gian tạo đơn" ↔ "thời điểm ghi nhận trên hệ thống của kênh" | Cùng mốc? Áp cho DV hay cả TB? | Giả định cùng mốc, áp DV | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-54 | Mới | L7 | Major | F04, F05 | D#9 bỏ autobill TB theo phương thức ↔ thuật ngữ #3 + BR-XHD-03 vẫn dùng | Bỏ hành vi hay chỉ bỏ câu chữ? | Giả định hành vi như 2.1 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-55 | Mới | L4 | Major | F07 | Mất câu "có bản tin mới thì xuất theo bản tin mới" khi gộp BR-XHD-11 | Bổ sung thông tin xong thì đợt sau có phát hành? | Giả định theo 2.1 | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-56 | Mới | L10 | Major | Toàn bộ | Cột "So với v2.1" ghi "Giữ nguyên" ở 4 BR đã đổi | Rà lại cột này | QC phải diff toàn bộ | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-57 | Mới | L1 | Major | F04, F08, F29 | Chưa nhận email ISC 24/09 + email FTQ 30/09 (căn cứ của 2.2) | Forward 2 email | Thiếu căn cứ khi BR mơ hồ | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-59 | Mới | L4 | Major | F23 | Add tiền trả trước 1 lần / đơn nhiều đợt: đợt nào, số tiền nào, TB có add? | Đặc tả | Giả định đợt đầu, toàn bộ tiền DV | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-61 | Mới | L5 | Major | F04 | Bán thêm trên HĐ tổ chức đã duyệt PĐK: có cần duyệt PĐK mới? | Xét PĐK của lần nào? | Giả định PĐK riêng mỗi đơn | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-62 | Mới (14/10) | L2 | Major | F01 | §A.2 + §A.3 chỉ liệt kê kênh và nhóm DV riêng rẽ; không có ma trận kênh nào bán nhóm DV nào, bán mới hay bán thêm (BR-XHD-12: thuộc tính bán do bên quản lý sản phẩm, ngoài URD) | Gửi ma trận kênh × nhóm DV × loại đơn thực bán; cặp nào không bán thì bỏ khỏi phạm vi test | Giả định đủ 340 cặp × 2 = 680 TC; mỗi cặp bỏ −2 TC | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-22 | Còn thiếu ↓ | L10 | Minor | Toàn bộ | PO đã confirm qua mail PM 13/10 nhưng cột Approver vẫn trống | Điền Approver + trạng thái | — | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-52 | Mới | L7 | Minor | F03, F28 | §A.1 #3 "lịch chung thay vì chia theo kênh" ↔ lịch riêng FPL | Sửa mục tiêu | — | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-58 | Mới | L3 | Minor | Toàn bộ | §A.4 #4 "[Bổ sung link … cho từng chức năng]" | Điền link lưu đồ | — | 16/10/2026 | chưa log | | Chưa chốt |

**Tổng còn mở:** 45 GAP — 3 Blocker · 18 Critical · 21 Major · 3 Minor (GAP-06, GAP-36 đóng 14/10/2026: TL ngoài phạm vi).

## 3. Test Strategy

### 3.1 Hướng / Loại Test

| # | Loại test | Áp dụng | Round áp dụng | Mô tả |
|---|-----------|:-------:|:-------------:|-------|
| 1 | Functional Testing | Yes | 1, 2, 3 | R1: kiểm thử toàn bộ scope 3 module (FR01–FR11) theo URD Phase 2 (Revision 2.2) trên STG, E2E qua log Kafka + dữ liệu bảng. R2: retest TC fail + recheck bug + hồi quy luồng TMĐT Phase 1. R3: recheck bug |
| 2 | Exploratory Testing | Yes | 1 | Edge case tích hợp: log Kafka trùng / đảo thứ tự, tín hiệu sát giờ chốt, đơn FPL sát mốc delay 2h / 22h, đơn nhiều phương thức triển khai, nhiều bill + nhiều loại cọc |
| 3 | Smoke Testing | Yes | 1, 2 | Đầu mỗi round: kết nối Kafka, worker chạy đúng lịch cấu hình, Billing / API liên kết phản hồi |
| 4 | UAT | No | — | Đối soát FHR (BR-TL-04) do FHR nghiệm thu ở UAT — ngoài phạm vi QC |
| 5 | Performance Testing | No | — | URD không có SLA |
| 6 | Security Testing | No | — | Không có yêu cầu |

### 3.2 Approach per Module

| Module | Approach | Priority | Ghi chú |
|--------|---------|----------|---------|
| XHD | Manual E2E: đẩy sự kiện đơn / tín hiệu giao hàng → chạy worker theo lịch cấu hình (chỉnh lịch trên STG để không phải chờ 12:05 / 18:05, các mốc FPL) → đối chiếu dữ liệu tồn xuất HĐ + Billing | P1 | Case thời gian (sát giờ chốt, sau giờ chốt cuối, qua ngày, 2 ngày cuối tháng, delay 2h FPL) cần chỉnh cấu hình / thời gian hệ thống STG. Chiều kênh × nhóm DV phủ đủ ở FR01 (F01): mỗi kênh (§A.2) tạo đơn bán mới và đơn bán thêm cho từng nhóm dịch vụ (§A.3) — 680 TC, chia 4 QC theo kênh |
| GN | Manual E2E: tạo Paid theo từng paymentstatus × kênh → kích hoạt từng điểm chạm → đối chiếu Payment, trừ Paid / cọc, Kafka Out | P1 | Mock/stub API kênh TT + nguồn EVC nếu STG chưa có; gạch EVC do đội EVC — chỉ kiểm phần chừa lock và việc không gạch trùng Paid voucher |
| HK | Manual: đối chiếu dữ liệu chuẩn bị (ký hiệu, ID, nội dung, tổng tiền theo thuế suất) + kết quả gen HĐĐT, tiền trả trước | P1 | Sai đầu số là sai kê khai thuế — phủ đủ tổ hợp vùng × đầu theo bảng map bản chốt |
| Hồi quy Phase 1 (TMĐT) | Gắn vào R2 trên các TC kênh sàn Shopee (20), Tiktok (21) của XHD + GN, gồm 80 TC ma trận F01 của 2 kênh này | P1 | Chưa có TC Phase 1 — dựng từ URD v1.0 khi nhận |

## 4. Entry & Exit Criteria

### Entry Criteria
- Build v2.0 đã deploy lên STG
- Test data đã chuẩn bị xong (đơn bán mới + đơn bán thêm trên hợp đồng đang hoạt động, theo các nhóm kênh §A.2, dịch vụ theo §A.3, DV + TB nhiều phương thức triển khai, HĐ tổ chức / HĐ con, Paid các trạng thái, tồn cọc theo loại)
- Tài liệu yêu cầu (URD) đã có phiên bản để test
- Hệ thống giả lập cho hệ thống ngoài (Billing, kênh thanh toán, đội EVC, HĐĐT, Dịch vụ) sẵn sàng hoặc hệ thống thật trên STG đã được xác nhận
- QC có cách phát sự kiện đơn hàng / tín hiệu giao hàng / Paid lên STG, có quyền đọc DB INVOICE và chỉnh được cấu hình lịch worker trên STG

### Exit Criteria / Quality Gates
*(Đã điều chỉnh từ default G1–G7 theo project type INT, manual only: G7 N/A. G8 "Bảng mapping chi nhánh" bỏ ngày 13/10/2026 — URD 2.2 BR-XHD-12 xác định chi nhánh theo hợp đồng, không còn bảng mapping)*

| # | Gate | Criteria | Source |
|---|------|----------|--------|
| G1 | TC Review | Score ≥ 70 | review-tc |
| G2 | P1 Pass | 100% | execute-maintain |
| G3 | Overall Pass | ≥ 80% | execute-maintain |
| G4 | P1 Bugs | 0 open | log-bug |
| G5 | Bug Fix Rate | ≥ 80% | log-bug |
| G6 | Blocked | ≤ 0 | execute-maintain |
| G7 | SRC-TC Match | N/A — không có automation | review-src-tc |

## 5. Test Environment

| Environment | URL | Purpose |
|------------|-----|---------|
| STG | TBD | Môi trường test duy nhất — R1, R2. Cập nhật URL / endpoint / quyền DB ở `07_environments/environments.md` |

## 6. Resources & Schedule

> ★ **Hai bản Resources / Schedule / Effort (chốt 14/10/2026):** DatDGD là **thực tập sinh** ⇒ file export Excel và Email Test Plan
> **không có tên DatDGD và không tính effort của DatDGD**.
> - **Bản nội bộ (có DatDGD):** các mục Resources, Schedule, Effort & Estimate ngay dưới đây — dùng để điều phối team.
> - **Bản xuất (không có DatDGD):** mục **6B** cuối §6 — `--export` (Excel + Email) chỉ lấy từ 6B.
> - **File xuất nội bộ (có DatDGD, 15/10/2026):** `ISC_InvoiceIssuance_v2.0_TestPlan_NoiBo.xlsx` + `EMAIL_InvoiceIssuance_v2.0_TestPlan_NoiBo.docx` render từ các mục bản nội bộ (4 QC · 65 md) — chỉ dùng trong team, ⛔ không gửi PM / khách.
>   DatDGD vẫn làm thật phần HK + F27 + ma trận F01 5 kênh; bản xuất ghi PIC là HuyenNHK (QC Lead chịu trách nhiệm phần việc của thực tập sinh) và không cộng effort phần này.

### Resources (Team mode)

| Thành viên | Vai trò | Chức năng phụ trách (mã Scope test §2.1a · mã phân tích) | Est#TC | Ngày công khả dụng |
|-----------|---------|---------------------|-------:|----------------:|
| HuyenNHK | QC Lead | FR02 lịch + kênh FPL, FR03 điều kiện phát hành, FR04 gộp / tách + chống trùng (F03–F06, F28) · ma trận FR01 kênh FPL, Mobile, Desktop, DKOL | 152 + 160 = 312 | 20 |
| GiangDC2 | QC | FR01 đồng bộ đơn + tín hiệu giao hàng, FR03 điều kiện hợp lệ, FR05 Billing + chi nhánh, FR06 cutover (F01, F02, F07–F10) · ma trận FR01 kênh API, W-Sale, VNTT, CRM | 163 + 160 = 323 | 20 |
| AnhPTM17 | QC | FR07, FR08, FR09 gạch nợ (F12–F17) · ma trận FR01 kênh Shopee, Tiktok, MBBank, Momo | 154 + 160 = 314 | 20 |
| DatDGD | QC (thực tập sinh) | FR10, FR11 hậu kỳ + tiền trả trước, thông tin khách xuất HĐ trong FR01 (F18–F20, F22, F23, F27) · ma trận FR01 kênh TGDD, F-Retail, CMR-App, SR-KPDV, HiFPT | 115 + 200 = 315 | 20 |

> Cả 4 QC làm 100% thời gian cho dự án (QC lead chốt 13/10/2026). Phần `Chờ bổ sung` (F11, F21, F29) chưa giao — giao khi PM xác nhận GAP.
> Ma trận FR01 chia theo kênh: mỗi kênh = 20 nhóm DV × 2 loại đơn = 40 TC. TL (F24, F25) ra ngoài phạm vi 14/10/2026 ⇒ DatDGD giảm 27 TC.

### Schedule — bản nội bộ (có DatDGD)

> **Chốt 14/10/2026 (QC lead HuyenNHK):** clear nghiệp vụ, Round 1, Round 2, Round 3 chạy đủ 4 QC; **Review và gen testcase, Update TC + Setup data không có HuyenNHK**.

| # | Giai đoạn / Task | Loại test | Bắt đầu | Kết thúc | Ngày LV | Owner | Effort (md) |
|---|-----------------|-----------|---------|----------|--------:|-------|------------:|
| 1 | Đọc và clear nghiệp vụ | — | 19/10/2026 | 20/10/2026 | 2 | HuyenNHK, GiangDC2, AnhPTM17, DatDGD | 8 |
| 2 | Review và gen testcase | — | 21/10/2026 | 22/10/2026 | 2 | GiangDC2, AnhPTM17, DatDGD | 6 |
| 3 | Update TC + Setup data | — | 23/10/2026 | 23/10/2026 | 1 | GiangDC2, AnhPTM17, DatDGD | 3 |
| 4 | Test Execution - Round 1 (Smoke + Functional + Exploratory) | Functional | 26/10/2026 | 30/10/2026 | 5 | HuyenNHK, GiangDC2, AnhPTM17, DatDGD | 20 |
| 5 | Buffer Dev-fix | — | 02/11/2026 | 03/11/2026 | 2 | Dev | — |
| 6 | Test Execution - Round 2 (Smoke + Retest + Recheck bug + Regression TMĐT) | Functional | 04/11/2026 | 10/11/2026 | 5 | HuyenNHK, GiangDC2, AnhPTM17, DatDGD | 20 |
| 7 | Buffer Dev-fix | — | 11/11/2026 | 11/11/2026 | 1 | Dev | — |
| 8 | Test Execution - Round 3 (Recheck bug) | Functional | 12/11/2026 | 13/11/2026 | 2 | HuyenNHK, GiangDC2, AnhPTM17, DatDGD | 8 |
| | **Tổng** | | 19/10/2026 | 13/11/2026 | 20 | | **65** |

> Effort theo người: HuyenNHK 14 md · GiangDC2 17 · AnhPTM17 17 · DatDGD 17.
> TC thuộc phần của HuyenNHK do 3 QC còn lại gen; Review TC là task của QA Lead, không nằm trong effort QC.
> Lịch không có ngày nghỉ lễ trong khoảng 19/10–13/11/2026.

### Effort & Estimate — Chiến lược Test

> Từ 14/10/2026 effort **cam kết** = theo lịch QC lead chốt (bảng "Effort cam kết theo lịch" dưới đây, map 1:1 sheet Plan).
> Bảng "Estimate theo công thức" giữ làm tham chiếu để thấy chênh lệch với lịch.
> Dòng không AI: `eff_md = manual_md`. Công thức: `references/formulas.md`.
> Không có version trước trong workspace ⇒ dùng STABLE_PARAMS mặc định INT.

#### Estimate theo công thức (tham chiếu — không phải effort cam kết)

| # | Giai đoạn / Task | Est#TC | manual_md | AI? | %AI | eff_md | Theo QC |
|---|-----------------|-------:|----------:|:---:|----:|-------:|-------------|
| 1 | Phân tích nghiệp vụ | — | 4.00 | ❌ FIXED | 0% | 4 | 1 md × 4 QC |
| 2 | Viết TC (review + gen TC) | 1.264 | 142.20 | ✅ | 80% | 28 | HuyenNHK 7 · GiangDC2 7 · AnhPTM17 7 · DatDGD 7 |
| 3 | Update TC + Setup data | — | 4.00 | ❌ FIXED | 0% | 4 | 1 md × 4 QC |
| 4 | Execute - Functional R1 (+ Smoke 0.5 + Exploratory 1) | 1.264 | 67.86 | ✅ | 10% (Functional) | 61 | 15 · 16 · 15 · 15 |
| 5 | Execute - Functional R2 (Smoke 0.5 + Retest ~632 TC + Recheck ~253 bug) | ~632 | 52.64 | ✅ | 10% (trừ Smoke) | 48 | 12 · 12 · 12 · 12 |
| — | **Tổng** | | **270.70** | | | **145** | Effort cần theo STABLE_PARAMS cho 1.264 TC (AI gen TC 80%) |

> ★ Chưa estimate (không nằm trong tổng): F11 Mail cảnh báo (GAP-02, tham khảo *9*) · F21 Dòng EVC / chiết khấu (GAP-04, *9*) ·
> F29 Clear "thuê thiết bị đầu cuối" (GAP-53, *9*) — tổng tham khảo *27 TC*. TL (F24–F26) đã chuyển Ngoài phạm vi.
> F10 Cutover (18 TC) đang tính theo giả định in-scope — PM xác nhận Out-scope (GAP-32) thì giảm khoảng 2.3 md.
> Hồi quy TMĐT Phase 1 chưa có TC cũ (TC_existing = 0) ⇒ chưa cộng effort riêng, chạy trong R2 trên TC kênh sàn.

#### Tham số estimate (nguồn tính manual_md)

| Module | Est#TC | avg_tc_h | avg_exec_h | buffer% | Nguồn Est#TC |
|--------|-------:|---------:|----------:|--------:|-------------|
| XHD — chức năng | 341 | 0.75h | 0.35h | 20% | Quick scan BR × 3 (+20% Giả định) |
| XHD — ma trận FR01 | 680 | 0.75h | 0.35h | 20% | 17 kênh × 20 nhóm DV × 2 loại đơn (không +20%, đã là trần) |
| GN | 154 | 0.75h | 0.35h | 20% | Quick scan BR × 3 (+20% Giả định) |
| HK | 89 | 0.75h | 0.35h | 20% | Như trên |
| **Tổng** | **1.264** | | | | ⭐⭐ sơ bộ — chạy analyze-requirements xong thì đối chiếu lại |

- Est#bug = 1.264 × 20% (bug_rate INT) ≈ 253 · retest 0.5h/bug. Loại đơn bán thêm: +1 SC cho 9 chức năng = +31 TC (rule riêng),
  cộng phần bán thêm trong ma trận FR01 (340 TC).
- Ma trận dùng chung avg_tc_h / avg_exec_h / bug_rate với phần còn lại. TC ma trận cùng khuôn nên thực tế có thể viết nhanh hơn và ít bug hơn — đối chiếu lại sau R1.
- Làm tròn theo từng QC (HuyenNHK 312 · GiangDC2 323 · AnhPTM17 314 · DatDGD 315 TC): Viết TC (AI 80%) 7.02 → 7 · 7.27 → 7 · 7.07 → 7 · 7.09 → 7;
  R1 15.49 → 15 · 15.51 → 16 · 15.09 → 15 · 15.13 → 15; R2 12.08 → 12 · 11.99 → 12 · 11.66 → 12 · 11.69 → 12. Smoke R1 + R2 tính cho HuyenNHK; Exploratory 1 md chia đều 4 QC.

#### Effort cam kết theo lịch (14/10/2026)

| # | Giai đoạn / Task | Est#TC | manual_md | AI? | %AI | eff_md | → Plan task |
|---|-----------------|-------:|----------:|:---:|----:|-------:|-------------|
| 1 | Đọc và clear nghiệp vụ | — | 8.00 | ❌ FIXED | 0% | 8 | 2 ngày × 4 QC |
| 2 | Review và gen testcase | 1.264 | 30.00 | ✅ | 80% | 6 | 2 ngày × 3 QC (không HuyenNHK) |
| 3 | Update TC + Setup data | — | 3.00 | ❌ FIXED | 0% | 3 | 1 ngày × 3 QC (không HuyenNHK) |
| 4 | Test Execution - Round 1 | 1.264 | 22.22 | ✅ | 10% | 20 | 5 ngày × 4 QC |
| 5 | Test Execution - Round 2 | ~632 | 22.22 | ✅ | 10% | 20 | 5 ngày × 4 QC |
| 6 | Test Execution - Round 3 (Recheck bug) | — | 8.89 | ✅ | 10% | 8 | 2 ngày × 4 QC |
| — | **Tổng** | | **94.33** | | | **65** | **= Total Plan effort** |

> `manual_md` back-solve từ `eff_md` (`eff_md ÷ (1 − %AI)`) để tổng Test Strategy §C = tổng sheet Plan.

#### Kết luận Feasibility

```
Effort cần (công thức)  : 145 md cho 1.264 TC (HuyenNHK 36 · GiangDC2 37 · AnhPTM17 36 · DatDGD 36) — AI gen TC 80%
Effort theo lịch        : 65 md  — Available 4 QC × 20 ngày LV (19/10 → 13/11/2026) = 80 md
Ratio (cần ÷ available) : 145 ÷ 80 = 1.81
→ KHÔNG ĐÁP ỨNG theo tham số estimate — effort lịch (65 md) bằng khoảng 45% effort công thức tính ra
```

Lịch do QC lead chốt. Để chạy được trong lịch này, nhịp làm việc thực tế phải đạt:

| Giai đoạn | Theo lịch | Theo tham số estimate |
|---|---|---|
| Review và gen testcase | 1.264 TC / 6 md ≈ **2.3 phút / TC** (AI gen, 3 QC review) | 0.75h viết / TC (×20% sau AI 80% ≈ 9 phút) |
| Round 1 | 1.264 TC / 20 md ≈ **7.6 phút / TC** | 0.35h chạy / TC (≈ 21 phút, +20% buffer) |
| Round 2 | ~632 TC retest + ~253 bug recheck / 20 md | ≈ 48 md |

- **Điều kiện để lịch khả thi:** AI gen TC nháp đầy đủ; dữ liệu và cách phát sự kiện trên STG sẵn từ 23/10; TC ma trận FR01 chạy theo lô (cùng khuôn); đặc tả tích hợp có trước 23/10.
- **Nếu không đạt nhịp:** thu hẹp ma trận FR01 theo ma trận kênh ↔ nhóm DV thực bán (GAP-62), ưu tiên P1 trong R1, hoặc bổ sung QC.
- **Automation:** không áp dụng.

### 6B. Bản xuất Excel / Email — không có DatDGD ★

> Nguồn **duy nhất** cho `--export` (sheet Plan, Test Strategy §C, Tổng quan; Email Section B). ⛔ Không đưa tên DatDGD vào bất kỳ ô / dòng nào.
> Cùng lịch với bản nội bộ; effort của DatDGD (15 md) không cộng. Phần việc của DatDGD ghi dưới HuyenNHK ở Resources;
> task Review và gen testcase, Update TC + Setup data chỉ có GiangDC2, AnhPTM17.

#### Resources (bản xuất)

| Thành viên | Vai trò | Chức năng phụ trách | Est#TC | Ngày công khả dụng |
|-----------|---------|---------------------|-------:|----------------:|
| HuyenNHK | QC Lead | FR02, FR03 (điều kiện phát hành), FR04 · FR10, FR11 · thông tin khách xuất HĐ trong FR01 · ma trận FR01 kênh FPL, Mobile, Desktop, DKOL, TGDD, F-Retail, CMR-App, SR-KPDV, HiFPT | 627 | 20 |
| GiangDC2 | QC | FR01 (đồng bộ đơn, tín hiệu giao hàng), FR03 (điều kiện hợp lệ), FR05, FR06 · ma trận FR01 kênh API, W-Sale, VNTT, CRM | 323 | 20 |
| AnhPTM17 | QC | FR07, FR08, FR09 · ma trận FR01 kênh Shopee, Tiktok, MBBank, Momo | 314 | 20 |

#### Schedule (bản xuất)

| # | Giai đoạn / Task | Loại test | Bắt đầu | Kết thúc | Owner | Effort (md) |
|---|-----------------|-----------|---------|----------|-------|------------:|
| 1 | Đọc và clear nghiệp vụ | — | 19/10/2026 | 20/10/2026 | HuyenNHK, GiangDC2, AnhPTM17 | 5 |
| 2 | Review và gen testcase | — | 21/10/2026 | 22/10/2026 | GiangDC2, AnhPTM17 | 4 |
| 3 | Update TC + Setup data | — | 23/10/2026 | 23/10/2026 | GiangDC2, AnhPTM17 | 2 |
| 4 | Test Execution - Round 1 (Smoke + Functional + Exploratory) | Functional | 26/10/2026 | 30/10/2026 | HuyenNHK, GiangDC2, AnhPTM17 | 15 |
| 5 | Buffer Dev-fix | — | 02/11/2026 | 03/11/2026 | Dev | — |
| 6 | Test Execution - Round 2 (Smoke + Retest + Recheck bug + Regression TMĐT) | Functional | 04/11/2026 | 10/11/2026 | HuyenNHK, GiangDC2, AnhPTM17 | 15 |
| 7 | Buffer Dev-fix | — | 11/11/2026 | 11/11/2026 | Dev | — |
| 8 | Test Execution - Round 3 (Recheck bug) | Functional | 12/11/2026 | 13/11/2026 | HuyenNHK, GiangDC2, AnhPTM17 | 6 |
| | **Tổng** | | 19/10/2026 | 13/11/2026 | | **47** |

#### Effort & Estimate (bản xuất)

| # | Giai đoạn / Task | Est#TC | manual_md | AI? | %AI | eff_md | → Plan task |
|---|-----------------|-------:|----------:|:---:|----:|-------:|-------------|
| 1 | Đọc và clear nghiệp vụ | — | 5.00 | ❌ FIXED | 0% | 5 | QC lead chốt 5 md |
| 2 | Review và gen testcase | 1.264 | 20.00 | ✅ | 80% | 4 | 2 ngày × 2 QC |
| 3 | Update TC + Setup data | — | 2.00 | ❌ FIXED | 0% | 2 | 1 ngày × 2 QC |
| 4 | Test Execution - Round 1 | 1.264 | 16.67 | ✅ | 10% | 15 | 5 ngày × 3 QC |
| 5 | Test Execution - Round 2 | ~632 | 16.67 | ✅ | 10% | 15 | 5 ngày × 3 QC |
| 6 | Test Execution - Round 3 (Recheck bug) | — | 6.67 | ✅ | 10% | 6 | 2 ngày × 3 QC |
| — | **Tổng** | | **67.01** | | | **47** | **= Total Plan effort (bản xuất)** |

> `manual_md` back-solve từ `eff_md` để tổng Test Strategy §C = tổng sheet Plan = 47 md. Cột Est#TC không render ra Excel.

## 7. Risk Assessment

> Cập nhật 14/10/2026: bỏ 4 rủi ro (tài liệu yêu cầu chưa đầy đủ · đặc tả tích hợp chưa có · round liên tục không chừa ngày fix ·
> nhiều QC cùng làm liên module); #1 viết lại theo dữ liệu đơn hàng từ các kênh; #2 gộp ý "hệ thống liên kết sẵn sàng, support kịp thời";
> #4 biện pháp theo AI gen TC + tạo data; thêm #6 về bug; thêm #7 về các loại EVC chưa chốt (hạn 16/10/2026). **Người phụ trách ghi theo vai trò** (QC Lead / PM / Dev / BA), không ghi account.

| # | Rủi ro | Mức ảnh hưởng | Xác suất | Biện pháp | Người phụ trách |
|---|--------|-------------|----------|-----------|-----------------|
| 1 | Data đơn hàng từ các kênh bán không sẵn sàng hoặc support chậm (R01) | Cao | Cao | Cần PM và các kênh bán hỗ trợ tạo / cung cấp đơn hàng bán mới, bán thêm trên STG; book lịch sớm với từng kênh và chốt qua email | PM |
| 2 | Hệ thống liên kết (SPF, Billing, phiếu thi công / Vendor / quầy, kênh thanh toán, đội EVC, HĐĐT, Dịch vụ) không sẵn sàng, không ổn định trên STG hoặc support không kịp thời, làm gián đoạn và ảnh hưởng thời gian test (R04 / I01) | Cao | Cao | PM thông báo trước lịch test cho các đầu mối hệ thống liên kết và điều phối support trong suốt các round; QC kiểm tra trạng thái hệ thống trước mỗi round, dùng hệ thống giả lập khi hệ thống thật chưa sẵn sàng | PM |
| 3 | Log Kafka về trùng, sai thứ tự hoặc chậm làm sai kết quả phát hành / gạch nợ hóa đơn (I03) | Cao | TB | Test các chuỗi log Kafka gửi theo thứ tự khác nhau và gửi lặp; kiểm tra hệ thống lấy đúng lần gửi cuối cùng và không xử lý trùng | QC Lead |
| 4 | Effort theo lịch (19/10–13/11/2026) thấp hơn effort estimate (145 md) cho 1.264 TC, phần lớn do ma trận kênh × nhóm dịch vụ × bán mới / bán thêm (R07) | Cao | Cao | Áp dụng AI vào gen testcase và phần tạo data; QC Lead theo dõi tiến độ hằng ngày | QC Lead |
| 5 | Job xuất hóa đơn chạy theo lịch chưa chạy xong khi QC kiểm tra kết quả (A05) | TB | Cao | Chỉnh lịch chạy job trên STG theo giờ test; ghi rõ thời gian cần chờ trong TC; kiểm tra lại kết quả định kỳ cho tới khi job chạy xong | QC Lead |
| 6 | Phát sinh nhiều bug, bug fix chậm, bug thuộc hệ thống liên kết (R02) | Cao | Cao | PM / Dev fix bug kịp timeline và kiểm soát chất lượng fix bug; bug của hệ thống liên kết do PM chuyển đầu mối hệ thống đó | PM / Dev |
| 7 | Các loại EVC chưa chốt (EVC bị lock khi gạch nợ bằng tiền khách, Paid voucher, dòng EVC / chiết khấu trên HĐĐT) — chậm chốt thì TC gạch nợ và hậu kỳ phải viết lại, ảnh hưởng lịch test | Cao | Cao | PM / BA chốt danh sách loại EVC trong phạm vi test **trước 16/10/2026**; chưa chốt thì QC viết TC theo giả định và cập nhật lại khi có xác nhận | PM / BA |

> ★ GAP ở §2.4 **không** tự vào bảng này. Chỉ thêm khi đã trao đổi xong và chốt "Đưa vào rủi ro? = Có"
> (`--update "chốt GAP"`); viết theo ngôn ngữ rủi ro dự án, không ghi mã GAP.

## 8. Deliverables

| # | Deliverable | Folder | Status |
|---|------------|--------|--------|
| 1 | Test Plan | 01_test-plans/TP-master-InvoiceIssuance-v2.0.md | ✅ |
| 1a | ★ Doc Readiness + DOC-GAP | 01_test-plans/DOC-READINESS-InvoiceIssuance-v2.0.md | ✅ |
| 1b | Test Plan Excel + Email (bản xuất §6B, không có DatDGD) | 01_test-plans/ISC_InvoiceIssuance_v2.0_TestPlan.xlsx · EMAIL_InvoiceIssuance_v2.0_TestPlan.docx | ✅ 14/10/2026 |
| 2 | Requirement Analysis | 02_analyze-requirements/v2.0/ | ⏳ |
| 3 | TC-MASTER | 03_test-cases/v2.0/TC-MASTER-v2.0.xlsx | ⏳ |
| 4 | TC Review Report | 11_tc-review/ | ⏳ |
| 5 | Vibe Test Report | 08_test-runs/vibe/ | ⏳ |
| 6 | SRC-TC Review Report | 11_tc-review/ | N/A |
| 7 | Test Run Log | 08_test-runs/ | ⏳ |
| 8 | Summary Report | 09_reports/ | ⏳ |

## 9. Approval

| Vai trò | Tên | Ngày | Chữ ký |
|---------|-----|------|--------|
| PM | Lê Thị Mỹ Lệ (Leltm) | | |
| PO | Nguyễn Thị Ngọc Hoa (hoantn13) — DVKH | | |
| QC Lead | HuyenNHK | | |

## 10. Revision History

| Version | Date | Changed By | Changes |
|---------|------|-----------|---------|
| 1.0 | 07/10/2026 | HuyenNHK | Initial creation |
| 1.1 | 13/10/2026 | HuyenNHK | Nhận URD rev 2.2: rà lại tài liệu (15 GAP đóng, 24 còn thiếu, 20 GAP mới); thêm F27–F29; F08, F25 lên Đủ; Est#TC 465 → 580. Team 2 → 4 QC (GiangDC2, AnhPTM17, DatDGD), lịch rút từ 07/12 → 20/11/2026. Bỏ gate G8. Cập nhật PO, Out of Scope, Risk #6–7 |
| 1.2 | 13/10/2026 | HuyenNHK | Phạm vi gồm cả đơn bán mới và bán thêm (PM xác nhận qua mail 13/10): thêm GAP-60, 61; +1 SC bán thêm cho 9 chức năng; Est#TC 580 → 611, effort 86 → 89 md, giữ mốc 20/11/2026 |
| 1.3 | 13/10/2026 | HuyenNHK | Nhận mail PM LeLTM 13/10/2026: PO đã confirm URD 2.2; kênh + nhóm sản phẩm theo URD; bán mới + bán thêm OK; EVC theo rule URD. GAP-22 Major → Minor, GAP-60 Critical → Major; nguồn phạm vi bán thêm = mail PM. Không đổi estimate |
| 1.4 | 14/10/2026 | HuyenNHK | Estimate lại TC: mỗi kênh bán tạo đơn bán mới + bán thêm cho từng nhóm dịch vụ — thêm F30 (17 kênh × 20 nhóm DV × 2 loại đơn = 680 TC), chia 4 QC theo kênh. Thêm GAP-62 (ma trận kênh ↔ nhóm DV thực bán). Est#TC 611 → 1.291, effort 89 → 177 md ⇒ Feasibility KHÔNG ĐÁP ỨNG, chờ PM chọn phương án A / B / C. Chưa đổi ngày trong Schedule |
| 1.5 | 14/10/2026 | HuyenNHK | DatDGD là thực tập sinh: tách 2 bản — bản nội bộ (có DatDGD) giữ ở §6; thêm §6B bản xuất Excel / Email không có tên DatDGD, không tính effort DatDGD (phần HK + TL + F27 ghi PIC HuyenNHK). Cả 2 dựng trên 611 TC · lịch hiện tại; bản xuất 3 QC · 69 md · ratio 0.92 |
| 1.6 | 14/10/2026 | HuyenNHK | Export Excel + Email: dựng lại 2 bản lịch trên 1.291 TC (gồm F30) theo phương án A — nội bộ 4 QC · 177 md · 19/10–23/12/2026 (ratio 0.92); bản xuất 3 QC · 131 md (ratio 0.91). Thêm rủi ro #8 (R07 nguồn lực), #9 (A01 đặc tả tích hợp); rủi ro #7 bỏ chữ "4 QC" |
| 1.7 | 14/10/2026 | HuyenNHK | Bỏ F30, gộp ma trận 17 kênh × 20 nhóm DV × bán mới / bán thêm vào F01 (Est#TC 29 → 709; tổng giữ 1.291). Thêm §2.1a Scope test theo chức năng: output các chức năng xuất hóa đơn (F03–F06, F08, F09, F27, F28) bổ sung "xuất hóa đơn đủ dịch vụ, kênh bán, đơn bán mới / bán thêm". Thêm §2.1b Hệ thống liên kết, liệt kê 17 kênh bán tạo đơn. F26 đối soát FHR chuyển Ngoài phạm vi (GAP-06 đóng) |
| 1.8 | 14/10/2026 | HuyenNHK | Lịch mới QC lead chốt, mỗi giai đoạn đủ 4 QC: clear nghiệp vụ 19–20/10 · review + gen TC 21–22/10 · update TC + setup data 23/10 · R1 26–30/10 · buffer 02–03/11 · R2 04–10/11/2026. Effort cam kết 60 md (bản xuất 3 QC · 45 md) so với estimate công thức 177 md ⇒ Feasibility KHÔNG ĐÁP ỨNG theo tham số; ghi nhịp cần đạt + điều kiện. Rủi ro #6, #8 cập nhật |
| 1.9 | 14/10/2026 | HuyenNHK | Gate G3 Overall Pass ≥ 90% → ≥ 80% (đồng bộ Project_rule). Excel: Gantt sheet Plan nới đủ 19/10–10/11/2026 (trước bị cắt ở 05/11, Round 2 thiếu ngày) |
| 1.10 | 14/10/2026 | HuyenNHK | TL — Điều chỉnh tính lương FPT Play SA (F24, F25; F26 đã ra trước) chuyển Ngoài phạm vi: −27 TC ⇒ 1.264 TC; GAP-36 đóng. Scope test gom 25 mã F thành 11 chức năng XHD-01..06, GN-01..03, HK-01..02 (§2.1a, có bảng map). Review và gen testcase + Update TC + Setup data bỏ HuyenNHK ⇒ effort lịch 57 md (bản xuất 42 md) |
| 1.11 | 14/10/2026 | HuyenNHK | Output HK-02 (tiền trả trước) bổ sung "đủ các dịch vụ, các kênh bán hàng, các đơn bán mới / bán thêm" |
| 1.12 | 14/10/2026 | HuyenNHK | Mã chức năng Scope test đánh lại F01–F11 (mã phân tích cũ Fxx → Axx, có bảng map §2.1a). F01: HT phụ thuộc = SPF. Hệ thống liên kết: kênh bán loại kết nối "SPF đồng bộ"; tách Phiếu thi công / Vendor / Quầy thành 3 dòng (25 hệ thống). Thêm Round 3 recheck bug 12–13/11/2026 + buffer 11/11; bản xuất Update TC + Setup data = 4 md ⇒ effort lịch nội bộ 65 md, bản xuất 50 md. §7: viết lại rủi ro #1 (data đơn hàng từ các kênh), bỏ 4 rủi ro (tài liệu, đặc tả tích hợp, round liên tục, nhiều QC), thêm cột Người phụ trách |
| 1.13 | 14/10/2026 | HuyenNHK | Mã chức năng Scope test theo quy tắc **FRxx**: F01–F11 → FR01–FR11. Mã phân tích trả về Fxx như ban đầu (bản 1.12 tạm đổi sang Axx) |
| 1.14 | 14/10/2026 | HuyenNHK | AI hỗ trợ Review và gen testcase 60% → 80% (effort lịch giữ nguyên; estimate công thức 174 → 145 md). §7: người phụ trách ghi theo vai trò; #2 gộp ý hệ thống liên kết sẵn sàng + support kịp thời, PM thông báo đầu mối; #4 biện pháp = AI gen TC + tạo data, QC Lead theo dõi tiến độ hằng ngày; thêm #6 nhiều bug / fix chậm / bug hệ thống liên kết |
| 1.15 | 14/10/2026 | HuyenNHK | Bản xuất: Update TC + Setup data 4 → 2 md (1 ngày × 2 QC) ⇒ 48 md. "Bản tin Kafka" → "log Kafka"; rủi ro #2, #3, #5 viết lại bằng tiếng Việt (bỏ polling, idempotent, mock / stub) |
| 1.16 | 14/10/2026 | HuyenNHK | Hệ thống liên kết (17 kênh bán): rủi ro thời gian đổi thành "Cần tài khoản / cách tạo đơn / chính sách bán trên STG cho kênh" |
| 1.17 | 14/10/2026 | HuyenNHK | Thêm rủi ro #7: các loại EVC chưa chốt, PM / BA chốt trước 16/10/2026. GAP-04, 16, 40: "Đưa vào rủi ro?" = Có |
| 1.18 | 14/10/2026 | HuyenNHK | Bản xuất: Đọc và clear nghiệp vụ 6 → 5 md (QC lead chốt) ⇒ tổng 47 md |
| 1.19 | 15/10/2026 | HuyenNHK | Xuất thêm bộ file nội bộ có DatDGD (`*_NoiBo.xlsx` / `*_NoiBo.docx`) từ §6 bản nội bộ: 4 QC · 65 md. Bộ file gửi PM giữ nguyên (3 QC · 47 md, §6B) |
