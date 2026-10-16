# DOC READINESS — Invoice Issuance Architecture v2.0

> Skill: `create-test-plan-huyennhk` (DOC READINESS GATE). Quy trình gốc: `~/git-fpt/Issuse_DOC/`.
> **Nội bộ QC ↔ PM/BA — KHÔNG đưa vào Test Plan Excel / Email khi export.**

| Hạng mục | Giá trị |
|---|---|
| Lần rà | **2** — nhận tài liệu bổ sung URD rev 2.2 (`--update "nhận tài liệu bổ sung"`) |
| Ngày nhận tài liệu | Lần 1: 05/10/2026 (URD rev 2.1) · Lần 2: 13/10/2026 (URD rev 2.2, ngày trên tài liệu 08/10/2026) |
| Ngày rà | Lần 1: 07/10/2026 · Lần 2: 13/10/2026 |
| Người rà | HuyenNHK |
| Kết luận | ⚠️ **CONDITIONAL — plan có điều kiện** (xem §D) |
| D_clear (QC bắt đầu Clear nghiệp vụ) | **19/10/2026** (thứ Hai) |
| D_confirm (hạn PM xác nhận) | **16/10/2026** (thứ Sáu) — áp cho cả GAP còn mở lẫn GAP mới; PM có 3 ngày LV (14–16/10) |

> **Hệ thống không có UI.** URD không có màn hình hay Figma, nên bảng B1–B4 được hiểu theo backend:
> B1 = luồng/chức năng · B2 = action xử lý (sự kiện, job, lời gọi hệ thống) · B3 = rule điều kiện ·
> B4 = đầu ra kiểm chứng được (log, cột Note, mail, bản tin Kafka, dữ liệu ghi bảng).
> Ngoại lệ có thể có UI: BR-XHD-18 "cho phép DVKH HO chủ động xử lý" — xem GAP-53.


> **14/10/2026 — mã chức năng:** Scope test dùng mã **FR01–FR11** (gom từ các mã phân tích F01–F29 trong file này; bảng map ở TP §2.1a).
---

## §0. Lần rà 2 — URD rev 2.2 so với rev 2.1

**Tài liệu có đổi thật:** md5 `33f5acb6…` ≠ `b0f9d080…`. Bản 2.2 rút gọn từ 86 KB text xuống 33 KB:
mỗi BR có tiêu đề, gộp BR, chuyển nội dung kỹ thuật sang **Phụ lục D**, và tự ghi "Chi tiết xem URD v2.1".
⇒ **URD 2.1 vẫn là tài liệu tham chiếu** cho phần kỹ thuật (giữ ở `00_input/v2.0/Doc/`). Khi 2 bản mâu thuẫn thì **2.2 thắng**.

**Nội dung mới/đổi ở 2.2 (theo Revision History + đối chiếu từng BR):**

| # | Thay đổi | Vị trí 2.2 | Ghi chú của QC |
|---|---|---|---|
| 1 | Danh sách 17 kênh bán (SaleChannelID) | §A.2 | Đóng GAP-08 |
| 2 | Danh sách 20 nhóm / 55 dịch vụ trong phạm vi; ServiceID 2 và 22 ngoài phạm vi | §A.3 | Đóng GAP-05 (cùng BR-TL-04) |
| 3 | Chi nhánh xuất HĐ = chi nhánh quản lý hợp đồng | BR-XHD-12 · D#7 | Đóng GAP-01, bỏ gate G8 |
| 4 | Chốt lịch 12:00/12:05 và 18:00/18:05, đánh giá lại sau pilot | BR-XHD-01 | Đóng GAP-10 |
| 5 | **Kênh FPL:** lịch riêng 2h/lần + mốc 22:05, delay 2h, realtime sau 22h | BR-XHD-01, 03, 06 | Chức năng mới F28 — GAP-50, 51, 52 |
| 6 | **Thông tin khách xuất HĐ:** mặc định theo hợp đồng; FPL cho khách tự nhập trong 2 giờ | BR-DB-03 | Chức năng mới F27 — GAP-48, 49 |
| 7 | **Hợp đồng tổ chức phải duyệt PĐK** (trừ 2 ngày cuối tháng); **không phát hành trên hợp đồng con** | BR-XHD-03 | F04 mở rộng — GAP-44, 45, 46, 47 |
| 8 | **BR-XHD-18 Clear nội dung "thuê thiết bị đầu cuối"** | BR-XHD-18 | Chức năng mới F29 — GAP-53 |
| 9 | Gạch nợ EVC giao cho đội EVC; INVOICE chỉ chừa phần lock | BR-VC · Hình 2 · TN #9 | Đóng GAP-03, 33; còn GAP-16, 40 |
| 10 | Bỏ BR-XHD-04 (autobill TB theo phương thức) | D#9 | GAP-54 |
| 11 | BR-DB-01 chỉ còn 2 sự kiện (thanh toán, hủy đơn) | BR-DB-01 | GAP-42 |
| 12 | Khóa chống trùng đổi thành mã đơn + dịch vụ hóa đơn + gói dịch vụ — **cột "So với v2.1" ghi "Giữ nguyên"** | BR-XHD-08 | GAP-41, 56 |
| 13 | BR-XHD-11 gộp vào BR-XHD-10, mất câu "có bản tin đồng bộ mới thì xuất theo bản tin mới" | BR-XHD-10 | GAP-55 |
| 14 | Mục V (câu hỏi cũ) + OI-1…7 bỏ, thay bằng mục C (3 điểm cần xác nhận) | §C · D#8 | Đóng GAP-23; GAP-09 cập nhật |
| 15 | PO đổi: **Nguyễn Thị Ngọc Hoa (hoantn13) – DVKH** (2.1: Nguyễn Thị Nhung – Nhungnt3) | §A.1 #6 | Cập nhật Test Plan §1, §9 |
| 16 | *(Không từ URD)* Phạm vi test gồm **cả đơn bán mới và bán thêm** — PM xác nhận qua mail 13/10/2026; URD 2.2 không có từ "bán mới" / "bán thêm" | — | GAP-60, 61; +1 SC "bán thêm" cho 9 chức năng |
| 17 | *(Không từ URD)* Mail PM LeLTM 13/10/2026 10:56: "PO đã confirm URD" (gửi kèm bản PDF 2.2); "Danh sách kênh đơn hàng => URD"; "Nhóm sản phẩm => URD"; "Bán mới, Bán thêm => ok"; "EVC cần test => theo rule URD" | Mail PM | GAP-22 xuống Minor (chỉ còn điền Approver); GAP-60 xuống Major; xác nhận đóng GAP-05, 08; GAP-04, 40 chưa được trả lời |

**Trạng thái 39 GAP lần 1:** 15 Đóng · 24 Còn thiếu. **GAP mới lần 2:** 22 (GAP-40 … GAP-61), trong đó
18 gắn `doc-regression` (lỗi nằm trong nội dung mới/sửa ở 2.2), 4 không gắn: GAP-43 (lỗi có từ 2.1, lần 1 chưa bắt), GAP-57 (thiếu email căn cứ), GAP-60, 61 (phạm vi bán mới + bán thêm, URD không đề cập).

---

## §A. Danh mục tài liệu nhận được (R1)

| # | Loại | Tên file / link | Version | Ngày | Trạng thái ghi trên tài liệu | Đọc được? | md5 |
|---|---|---|---|---|---|---|---|
| 1 | Nghiệp vụ — **bản chính** | `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx` | Header `Phiên bản 2.2` · tên file `v2_2` · Revision History mới nhất **2.2** | 08/10/2026 | Không ghi trạng thái; cột Approver trống ở cả 4 bản | Có (text + 4 lưu đồ nhúng Hình I–IV) | `33f5acb6c27fa0f4feaa59c3197b2512` |
| 2 | Nghiệp vụ — tham chiếu kỹ thuật | `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_0_URD_v1_0.docx` (URD rev 2.1) | Header `2.0` · Revision **2.1** | 26/08/2026 | Bị 2.2 thay phần chính; Phụ lục D của 2.2 trỏ về bản này | Có | `b0f9d0800b248864a70fc2d4f9790f74` |
| 3 | Nghiệp vụ (tham chiếu) | URD v1.0 — Phase 1 (rule kênh TMĐT) — 2.2 §A.4 #2 | 1.0 | 25/02/2026 | — | **Không — chưa nhận** (GAP-24) | — |
| 4 | Mail chốt nghiệp vụ | Email ISC 24/09/2026 · email FTQ 30/09/2026 — 2.2 §A.4 #3 | — | 24/09, 30/09/2026 | — | **Không — chưa nhận** (GAP-57) | — |
| 5 | Lưu đồ draw.io | 2.2 §A.4 #4: "[Bổ sung link … cho từng chức năng]" | — | — | Placeholder | **Không — chưa có link** (GAP-58). Rà theo 4 hình nhúng trong #1 | — |
| 6 | Tích hợp | Kafka Order/Invoice Event, Kafka Out, schema bảng, API kênh thanh toán / đội EVC / Billing / HĐĐT / Dịch vụ | — | — | — | **Không — chưa nhận** (GAP-07) | — |
| 7 | Thiết kế UI | — | — | — | — | ➖ N/A (backend) — trừ BR-XHD-18 nếu có màn hình (GAP-53) | — |
| 8 | Mail PM (scope + duyệt) | `00_input/v2.0/Doc/Mail_PM-LeLTM_2026-10-13_PO-confirm-URD-v2.2.png` — LeLTM gửi 13/10/2026 10:56: "PO đã confirm URD" · "Danh sách kênh đơn hàng => URD" · "Nhóm sản phẩm => URD" · "Bán mới, Bán thêm => ok" · "EVC cần test => theo rule URD" | — | 13/10/2026 | PO đã confirm URD 2.2 | Có (ảnh chụp mail) | — |
| 9 | Nghiệp vụ — bản PDF đính kèm mail #8 (**bản PO confirm**) | `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.pdf` (16 trang, xuất từ Word 08/10/2026 16:09) | 2.2 | 13/10/2026 | Bản PO đã confirm | Có. **Đã đối chiếu 13/10/2026: nội dung = #1** — không có từ nào khác (chỉ thêm header bảng lặp khi sang trang + số thứ tự danh sách); 4 lưu đồ trùng từng pixel. QC tiếp tục trích dẫn theo #1 (.docx) | `44eb00ce36190a08673afcccb3c76551` |

> Lần 1 có "Link tài liệu FTQ mô tả" (2.1 §A.2 #3). Bản 2.2 không còn tham chiếu tài liệu này ⇒ đóng GAP-25.

---

## §B. Bảng B1–B4 (R2 — nháp của QC, cập nhật theo 2.2)

### B1 — Luồng / chức năng (29 dòng)

| ID | Chức năng / luồng | Mục URD 2.2 | BR | Trong scope? | Trạng thái tài liệu | Đổi so với lần 1 |
|---|---|---|---|---|---|---|
| F01 | Đồng bộ đơn hàng SPF → INVOICE (sự kiện, ProductType, lần đẩy cuối, mốc nhận bản tin) | I · Hình I bước 1–2 | DB-01, 04, 05 | Có | Giả định | Đủ → Giả định (GAP-42) |
| F02 | Tín hiệu giao hàng hoàn tất 3 nguồn + map bộ khóa | I | DB-02, DB-07 | Có | Đủ | — |
| F03 | Lịch worker (tham số) + phân luồng worker / realtime | I · Hình I | XHD-01, 02, 06 | Có | Giả định | GAP-10 đóng; thêm GAP-43 |
| F04 | Điều kiện phát hành DV / TB + HĐ tổ chức duyệt PĐK + hợp đồng con | I · Hình I | XHD-03 | Có | Giả định | Đủ → Giả định (GAP-44); thêm PĐK, HĐ con |
| F05 | Gộp HĐ ở worker · tách theo tín hiệu ở realtime · 1 đơn n HĐ | I | XHD-05, 06, 14 | Có | Đủ | — |
| F06 | Chống xuất trùng (+ rủi ro race worker/realtime) | I · D#2 | XHD-08 | Có | Giả định | Thêm GAP-41 (khóa đổi) |
| F07 | Điều kiện hợp lệ + xử lý không hợp lệ + job cảnh báo 15 phút | I | XHD-10 | Có | Giả định | — |
| F08 | Chi nhánh xuất hóa đơn = chi nhánh quản lý hợp đồng | I | XHD-12 | Có | **Đủ** | Chờ bổ sung → Đủ (GAP-01 đóng) |
| F09 | Phát hành qua Billing + nội dung HĐ + Invoice Event | I | XHD-13 | Có | Giả định | — |
| F10 | Cutover v1 → v2 + kiểm tra chéo luồng cũ | D#1 (2.1 BR-DB-08) | — | *Cần xác nhận* | Giả định | 2.2 chuyển sang phụ lục kỹ thuật |
| F11 | Mail cảnh báo bản tin đồng bộ trễ qua ngày | D#3 (2.1 RISK-01) | — | Có *("yêu cầu bắt buộc đã thống nhất")* | **Chờ bổ sung** | — |
| F12 | Đồng bộ Paid (Orderpaid → Paid, check trùng 4 trường) | II · Hình II | DP-01 | Có | Đủ | — |
| F13 | 3 điểm chạm + lọc sớm + chọn Paid / Cọc | II | XL-01, 03 | Có | Đủ | — |
| F14 | Gạch nợ tạm / gỡ gạch nợ tạm (kênh sàn: Shopee 20, Tiktok 21) | II | NT-01, 02, 04 | Có | Đủ | — |
| F15 | Gạch nợ thật bằng Paid (Amount > 0, thứ tự bill, từng phần, Kafka Out) | II | GN-01, 03, 04, 05 | Có | Giả định | GAP-15 đóng; thêm GAP-40 |
| F16 | Phần EVC ở nhánh Paid: INVOICE chừa tiền lock khi gạch tiền khách (gạch EVC do đội EVC) | II · Hình II | BR-VC | Có | Giả định | Chờ bổ sung → Giả định (GAP-03 đóng) |
| F17 | Gạch nợ bằng Cọc (đủ tiền, đủ cọc theo loại, trừ cọc) | II | GC-01, 02, 03 | Có | Giả định | GAP-33 đóng |
| F18 | Phạm vi đẩy hậu kỳ theo từng đơn hàng | III · Hình III | HK-01 | Có | Đủ | — |
| F19 | Ký hiệu + ID hóa đơn điện tử | III · §C#1 · D#5 | HK-03 | Có | Giả định | — |
| F20 | Nội dung hiển thị + tổng tiền theo thuế suất | III | HK-05, HK-07 | Có | Đủ | — |
| F21 | Dòng EVC + dòng chiết khấu trên HĐĐT | HK-02 · D#6 | HK-02 | Có | **Chờ bổ sung** | — |
| F22 | Thông tin theo mẫu + đẩy HĐĐT khi đủ thông tin | III · D#6 | HK-02 | Có | Giả định | — |
| F23 | Tiền trả trước sang hệ thống Dịch vụ, một lần mỗi đơn | III · Hình III | HK-09 | Có | Giả định | GAP-19 đóng; thêm GAP-59 |
| F24 | Gộp 2 bảng tồn + khử trùng SĐT + tính hoa hồng FPT Play SA | IV · Hình IV | TL-01, TL-03 | Có | **Ngoài phạm vi** (14/10/2026) | TL ra ngoài phạm vi |
| F25 | Lọc FPT Play SA trên bảng tồn mới (kênh §A.2 + ServiceID 5 / SubServiceType 17, 18) | IV · §A.2 · §A.3 | TL-02 | Có | **Ngoài phạm vi** (14/10/2026) | Chờ bổ sung → Đủ (GAP-05 đóng) |
| F26 | Đối soát kết quả hoa hồng với FHR (giai đoạn UAT) | IV | TL-04 | *Cần xác nhận vai trò QC* | **Ngoài phạm vi** (14/10/2026) | Rõ hơn: thuộc UAT, FHR nghiệm thu |
| F27 | **[Mới]** Thông tin khách xuất HĐ: mặc định theo hợp đồng; FPL cho khách chọn lấy HĐ và tự nhập trong 2 giờ | I · Hình I | DB-03 | Có | Giả định | Mới ở 2.2 |
| F28 | **[Mới]** Kênh FPL: delay 2h theo thời gian tạo đơn · worker 2h/lần · mốc 22:05 · realtime sau 22h | I | XHD-01, 03, 06 | Có | Giả định | Mới ở 2.2 |
| F29 | **[Mới]** Clear nội dung "thuê thiết bị đầu cuối" trên HĐ theo yêu cầu (DVKH HO xử lý) | I · Hình I | XHD-18 | *Cần xác nhận ("kịp plan")* | **Chờ bổ sung** | Mới ở 2.2 |

**Loại đơn:** mọi chức năng áp cho cả **đơn bán mới** và **đơn bán thêm** (trên hợp đồng đang hoạt động) — PM xác nhận qua mail 13/10/2026.
URD không phân biệt loại đơn ⇒ test theo giả định rule áp chung (GAP-60).

Ngoài phạm vi (URD 2.2 ghi rõ): xuất hóa đơn tay (§A.1 #4) · ServiceID 2 và 22 (§A.3) · hủy / điều chỉnh HĐ khi hủy đơn
đã có hóa đơn (BR-XHD-10) · thuộc tính chi nhánh được bán SPDV nào (BR-XHD-12) · gạch nợ bằng EVC (đội EVC thực hiện — BR-VC) ·
xử lý HĐ dư khi phát hành trùng, quét tay giai đoạn giao thoa, xuất bổ sung case-by-case cho bản tin trễ (Phụ lục D#1–3, chi tiết ở 2.1).

### B2 — Action xử lý (27)

| ACT | F | Action | Kết quả thành công | Kết quả thất bại | Đủ? |
|---|---|---|---|---|---|
| ACT-01 | F01 | Invoice Consumer nhận + giải mã Order Event | Ghi đơn theo lần đẩy cuối, lưu thời điểm nhận | **Không đặc tả** (bản tin lỗi / thiếu trường) | ❌ GAP-26 |
| ACT-02 | F02 | Nhận tín hiệu giao hàng hoàn tất | Ghi nhận cho TB khớp khóa, lưu nguồn | Đã có HĐ / không khớp → không ghi, log vào Note *(format chưa rõ)* | ⚠️ GAP-27 |
| ACT-03 | F03–F05 | Worker chạy theo đợt (12:05, 18:05) | Gộp 1 HĐ/đơn/đợt | Dòng không đủ ĐK → chờ đợt sau | ✅ |
| ACT-04 | F03, F05 | Xử lý realtime sau giờ chốt cuối | Phát hành đúng thành phần của tín hiệu | — | ⚠️ GAP-43 (cuối tháng) |
| ACT-05 | F04, F06, F07 | Kiểm tra trước khi phát hành (trùng, hợp lệ, PĐK, HĐ con) | Đi tiếp xác định chi nhánh | Không hợp lệ → không phát hành, ghi log *(nội dung chưa rõ)*; PĐK chưa duyệt / HĐ con → *không đặc tả đầu ra* | ⚠️ GAP-29, 44, 46 |
| ACT-06 | F08 | Xác định chi nhánh | Chi nhánh quản lý hợp đồng tại thời điểm phát hành, lưu trên tồn xuất HĐ | — | ✅ |
| ACT-07 | F09 | Gọi Billing System phát hành | Ghi BillNumber, BillDate = ngày thực tế | **Không đặc tả** (Billing lỗi / timeout) | ❌ GAP-14 |
| ACT-08 | F09 | Gửi Kafka Invoice Event | Kích hoạt gạch nợ + hậu kỳ | **Không đặc tả** | ⚠️ GAP-07 |
| ACT-09 | F10 | Kiểm tra chéo dữ liệu luồng cũ | Đơn đã ra HĐ ở luồng cũ → luồng mới bỏ qua *(chỉ có ở 2.1)* | — | ⚠️ GAP-32 |
| ACT-10 | F11 | Mail cảnh báo dòng trễ qua ngày | **Không đặc tả** | **Không đặc tả** | ❌ GAP-02 |
| ACT-11 | F07 | Job cảnh báo thiếu thông tin (15 phút) | **Không đặc tả** | — | ❌ GAP-31 |
| ACT-12 | F12 | Đồng bộ Paid | Thêm mới / cập nhật paymentstatus | — | ✅ |
| ACT-13 | F13 | Nhận điểm chạm + lấy nợ | Lấy nợ + trường Paid/Cọc | Không có nợ → dừng | ✅ |
| ACT-14 | F13 | Gọi API kênh TT lấy trường Paid/Cọc | Lưu vào OrderBill, rẽ luồng | Lỗi/timeout → dừng, không retry | ✅ |
| ACT-15 | F14 | Gạch nợ tạm | Payment phương thức đặc biệt = toàn bộ nợ còn lại; HĐ "Đã gạch nợ" | Kênh không qua sàn → không gạch | ✅ |
| ACT-16 | F14 | Gỡ gạch nợ tạm | Gỡ Payment tạm, HĐ còn nợ, gạch thật | — | ✅ |
| ACT-17 | F15 | Gạch nợ thật Paid từng bill | Payment, trừ Paid, Kafka Out; dư Paid giữ | Hết Paid → dừng | ⚠️ GAP-40 |
| ACT-18 | F16 | Chừa phần EVC lock khi gạch tiền khách | Số gạch = min(nợ bill − lock, Paid khách) | — | ⚠️ GAP-40 |
| ACT-19 | F16, F17 | Lấy tổng tiền EVC + phần lock của đơn | Dùng cho kiểm tra đủ tiền / chừa lock | **Nguồn + lỗi không đặc tả ở 2.2** | ❌ GAP-16 |
| ACT-20 | F17 | Gạch nợ Cọc từng bill | Gom Payment theo loại cọc, trừ cọc, không Kafka Out | Thiếu tiền / thiếu cọc 1 loại → không gạch cả bill | ✅ |
| ACT-21 | F19–F22 | Chuẩn bị + đẩy hệ thống HĐĐT | Gen HĐĐT | Chưa đủ thông tin → chưa đẩy; **đẩy lỗi: không đặc tả** | ❌ GAP-18 |
| ACT-22 | F23 | Đẩy tiền trả trước sang hệ thống Dịch vụ | Add tiền trả trước, đánh dấu đã đẩy | **Không đặc tả** | ❌ GAP-20 |
| ACT-23 | F24, F25 | Job tính lương FPT Play SA | Hoa hồng trên dữ liệu đã gộp + khử trùng | — *(công thức chưa có)* | ⚠️ GAP-36 |
| ACT-24 | F26 | Đối soát FHR (UAT) | "FHR kiểm tra và nghiệm thu" | — | ❌ GAP-06 |
| ACT-25 | F27 | Xác định thông tin khách xuất HĐ | Theo hợp đồng; FPL khách chọn lấy HĐ → thông tin khách nhập | **Khách FPL không lấy HĐ / quá 2 giờ không nhập: không đặc tả** | ❌ GAP-48 |
| ACT-26 | F28 | Worker FPL quét 2h/lần + mốc 22:05 | Phát hành đơn FPL đã qua delay 2h | — *(mốc bắt đầu, giờ chốt từng đợt chưa rõ)* | ❌ GAP-50 |
| ACT-27 | F29 | DVKH HO clear "thuê thiết bị đầu cuối" | **Không đặc tả** | **Không đặc tả** | ❌ GAP-53 |

### B3 — Rule điều kiện (26)

| VAL | ACT | Rule (bị chặn khi) | Ngưỡng | Đầu ra khi chặn | Ghi chú |
|---|---|---|---|---|---|
| VAL-01 | ACT-05 | Đơn ở trạng thái hủy | — | MSG-01 | |
| VAL-02 | ACT-05 | Đơn "đang cập nhật" | — | MSG-01 | Giá trị trạng thái chưa rõ — GAP-13 |
| VAL-03 | ACT-05 | Hợp đồng không có hiệu lực | — | MSG-01 | "Có hiệu lực" chưa định nghĩa — GAP-13 |
| VAL-04 | ACT-05 | Thiếu Sale Team | — | MSG-01 | |
| VAL-05 | ACT-05 | Thiếu Sale Channel | — | MSG-01 | |
| VAL-06 | ACT-05 | Tên KH rỗng | — | MSG-01 | |
| VAL-07 | ACT-05 | Loại hình KH cấp 1 rỗng | — | MSG-01 | |
| VAL-08 | ACT-05 | Loại hình KH cấp 2 rỗng | — | MSG-01 | |
| VAL-09 | ACT-05 | Địa chỉ xuất HĐ rỗng | — | MSG-01 | |
| VAL-10 | ACT-05 | LocationID ≤ 0 | > 0 | MSG-01 | |
| VAL-11 | ACT-05 | ID dịch vụ ≤ 0 | > 0 | MSG-01 | |
| VAL-12 | ACT-05 | ID nhóm dịch vụ ≤ 0 | > 0 | MSG-01 | |
| VAL-13 | ACT-05 | ID gói dịch vụ ≤ 0 | > 0 | MSG-01 | |
| VAL-14 | ACT-05 | ID chính sách ≤ 0 | > 0 | MSG-01 | |
| VAL-15 | ACT-05 | ID câu lệnh giá ≤ 0 | > 0 | MSG-01 | |
| VAL-16 | ACT-05 | ID chương trình khuyến mãi ≤ 0 | > 0 | MSG-01 | |
| VAL-17 | ACT-05 | Dòng đã có BillNumber (theo khóa BR-XHD-08) | — | Bỏ qua | Khóa đổi ở 2.2 — GAP-41 |
| VAL-18 | ACT-02 | Tín hiệu giao hàng không khớp khóa / TB đã có HĐ | — | MSG-02 | |
| VAL-19 | ACT-13 | Lọc sớm điểm chạm (a): Paid tạm + kênh sàn, hoặc Paid hoàn tất | — | Dừng | |
| VAL-20 | ACT-15 | Kênh bán không qua sàn | — | Không gạch tạm | Kênh sàn = Shopee (20), Tiktok (21) theo §A.2 |
| VAL-21 | ACT-17 | Paid Amount ≤ 0 / khác OrderCode | > 0 | Không dùng dòng Paid | Paid voucher? — GAP-40 |
| VAL-22 | ACT-20 | Σ cọc + Σ EVC (gồm lock) < nợ bill | so sánh | Không gạch bill | |
| VAL-23 | ACT-20 | Σ cọc theo loại < tiền cần trừ loại đó | so sánh | Không gạch cả bill | |
| VAL-24 | ACT-05 | **[Mới]** HĐ tổ chức chưa duyệt PĐK (trừ 2 ngày cuối tháng) | ngày cuối tháng | "không autobill" | GAP-44, 45 |
| VAL-25 | ACT-05 | **[Mới]** Hợp đồng con (có gắn hợp đồng cha) | — | Không phát hành DV + TB | GAP-46 |
| VAL-26 | ACT-26 | **[Mới]** Đơn FPL chưa đủ 2h kể từ tạo đơn | 2h | Chưa phát hành | GAP-50, 51 |

> Bỏ so với lần 1: VAL-24 cũ "trần 50% EVC" — 2.2 chuyển cấu hình EVC sang Phụ lục D#4 (đội EVC thực hiện).
> Thứ tự kiểm tra VAL-01..16, VAL-24, VAL-25 và cách log khi nhiều lỗi cùng lúc: **không đặc tả** (GAP-30).

### B4 — Đầu ra kiểm chứng được (7)

| MSG | Đầu ra | Ở đâu | Điều kiện | Nội dung / format đặc tả? |
|---|---|---|---|---|
| MSG-01 | Log không phát hành | ? | VAL-01..16 | ❌ GAP-29 |
| MSG-02 | Log nội dung tín hiệu giao hàng | Cột Note | VAL-18 | ❌ GAP-27 |
| MSG-04 | Mail cảnh báo bản tin trễ qua ngày | ? | D#3 | ❌ GAP-02 |
| MSG-05 | Cảnh báo thiếu thông tin (job 15 phút) | ? | BR-XHD-10 | ❌ GAP-31 |
| MSG-06 | Kafka Invoice Event | Kafka | Sau phát hành | ❌ payload — GAP-07 |
| MSG-07 | Kafka Out báo Paid đã dùng | Kafka → kênh TT | Sau gạch Paid | ❌ payload — GAP-07 |
| MSG-08 | Lưu thời điểm nhận mỗi bản tin | Dữ liệu đơn | BR-DB-05 | ⚠️ tên trường chưa rõ — GAP-07 |

> Bỏ so với lần 1: MSG-03 "log 2 dòng cùng khóa" — BR-XHD-08 ở 2.2 không còn câu này (đóng GAP-28).

---

## §C. Checklist Gate 1 (R3 — rà lại trên URD 2.2)

| # | Kiểm tra | KQ | Dẫn chứng (vị trí · trích nguyên văn) | GAP |
|---|---|---|---|---|
| 1A-01 | Có tài liệu nghiệp vụ | ✅ | URD 2.2 đủ 4 chức năng I–IV, mỗi chức năng có Mô tả / Flow / Business rules | — |
| 1A-02 | Có thiết kế UI | ➖ | Backend. Riêng BR-XHD-18 "cho phép DVKH HO chủ động xử lý" chưa rõ có màn hình không | GAP-53 |
| 1A-03 | Có danh sách chức năng trong scope | ✅ | Mục lục I–IV; §A.2 "Tất cả kênh bán trong danh sách dưới đây thuộc phạm vi"; §A.3 "(20 nhóm, 55 dịch vụ)" | — |
| 1A-04 | Có tài liệu tích hợp | ❌ | I · Actor: "SPF, phiếu thi công, Vendor, quầy, INVOICE, Billing System."; D: "Các nội dung dưới đây không cần PO confirm … Chi tiết xem URD v2.1." — không có payload, schema, API contract | GAP-07 |
| 1B-01 | In / Out scope rõ | ✅ | §A.1 #4: "Các kênh bán trong danh sách ở mục A.2 và các nhóm dịch vụ, dịch vụ trong danh sách ở mục A.3. ¶ Chưa bao gồm xuất hóa đơn tay."; §A.3: "Không có trong danh sách phạm vi: ServiceID 2 … ServiceID 22 (GSafe)". Còn mơ hồ in/out: BR-XHD-18, cutover, đối soát FHR | GAP-53, 32, 06 |
| 1B-02 | Các phần trong tài liệu khớp nhau | ❌ | (1) BR-XHD-08 "dịch vụ = mã đơn hàng + dịch vụ hóa đơn + Gói dịch vụ" ↔ §C#3 "Khóa chống trùng có dùng SubServiceType". (2) BR-DB-01 "thanh toán, hủy đơn hàng" ↔ BR-DB-03 "Cập nhật thông tin khách …" và BR-XHD-03 "lấy chuẩn theo thời gian tạo đơn". (3) BR-XHD-01 "phát hành sang tháng sau" ↔ BR-XHD-06 "Xử lý ngay khi nhận". (4) BR-DP-01 Paid "gồm cả voucher" ↔ BR-VC "gạch nợ bằng EVC do đội EVC thực hiện". (5) TN #3 "là đơn vị autobill của thiết bị" ↔ D#9 "Đã bỏ khỏi tài liệu". (6) Mốc delay FPL: BR-XHD-03 "thời gian tạo đơn" ↔ BR-DB-03 "thời điểm ghi nhận trên hệ thống của kênh". (7) §A.1 #3 "thay vì chia theo kênh" ↔ BR-XHD-01 lịch riêng FPL | GAP-41, 42, 43, 40, 54, 51, 52 |
| 1B-03 | Scope giữa các nguồn khớp nhau | ❌ | PM xác nhận qua mail 13/10/2026 phạm vi gồm đơn bán mới + bán thêm; URD 2.2 không có từ "bán mới" / "bán thêm", mọi BR viết chung cho "đơn hàng" (2.1 chỉ nhắc "hóa đơn bán mới" ở BR-HK-04). Hình I–IV khớp text 2.2. **Hạ Blocker → Major:** phạm vi đã có PM xác nhận bằng văn bản; bán thêm không mâu thuẫn BR nào, không thêm luồng / chức năng — chỉ còn xác nhận điểm khác biệt | GAP-60, 61, 17 |
| 1B-04 | US ↔ FR ↔ AC | ➖ | URD dùng BR, không có US/AC | — |
| 1C-01 | Không có luồng chính rỗng | ❌ | BR-XHD-18 chỉ có 1 câu: "Bổ sung chức năng cho phép DVKH HO chủ động xử lý với hợp đồng có yêu cầu clear nội dung "thuê thiết bị đầu cuối" trên hóa đơn." | GAP-53 |
| 1C-02 | Bảng US đủ As a / I want / So that | ➖ | Không có US | — |
| 1C-03 | Không còn placeholder | ❌ | §A.4 #4: "[Bổ sung link … cho từng chức năng]". (Câu cụt "napas", `[?]`, `[NỢ]` của 2.1 đã hết) | GAP-58 |
| 1C-04 | TBD có owner + hạn | ❌ | §C có 3 "Các điểm cần xác nhận" — bảng chỉ có cột "Nội dung / Liên quan / Hiện trạng", không có owner và ngày chốt | GAP-09 |
| 1C-05 | Trạng thái Approved đúng thực tế | ✅ | Mail PM 13/10/2026: "PO đã confirm URD" (bản 2.2). Cột Approver trên tài liệu vẫn trống — ghi ở 1D-02 | — |
| 1D-01 | Version header = Revision History = tên file | ✅ | Header "Phiên bản 2.2" = Revision "08/10/2026 \| 2.2" = tên file "v2_2". "URD_v2_0" trong tên file và "V2.0" ở tiêu đề là version sản phẩm | — |
| 1D-01b | *(bổ sung lần 2)* Ghi chú thay đổi khớp nội dung | ❌ | Cột "So với v2.1" ghi "Giữ nguyên" ở BR-XHD-01 (thêm lịch FPL), BR-XHD-06 (thêm FPL), BR-XHD-08 (đổi khóa), BR-XHD-10 (mất câu bản tin mới). Revision 2.2 ghi "[A] … KH Chuỗi/Dự án (gộp vào BR-XHD-03)" nhưng BR-XHD-03 không có nội dung KH Chuỗi | GAP-56, 47 |
| 1D-02 | Revision History có Author / Reviewer / Approver | ❌ | Approver trống ở cả 4 bản dù PO đã confirm qua mail | GAP-22 |
| 1D-03 | Thứ tự thời gian hợp lý | ✅ | 25/02 → 10/07 → 26/08 → 08/10/2026 | — |
| 1D-04 | ID liên tục, không trùng | ✅ | "ID của BR giữ theo URD v2.1 để dễ đối chiếu; các BR đã gộp hoặc chuyển sang phụ lục không còn xuất hiện ở đây" — số nhảy có chủ đích, có giải thích | — |
| 1E-01 | Không có tên dự án khác | ✅ | Không thấy tên dự án lạ | — |
| 1E-02 | PO / Glossary đúng sản phẩm | ✅ | PO Nguyễn Thị Ngọc Hoa (hoantn13) – DVKH; PM Leltm; glossary đúng domain | — |
| 1E-03 | Đã xóa hướng dẫn template | ✅ | Không còn mục "HƯỚNG DẪN SỬ DỤNG TEMPLATE"; glossary hết track change | — |
| 1E-04 | Tham chiếu trỏ đúng | ✅ | Mọi BR được nhắc trong Hình I–IV, §C, BR-XHD-03 đều có trong bảng BR; tham chiếu Phụ lục D dùng ID của 2.1 | — |
| 1E-05 | N/A có lý do | ➖ | Không có câu N/A | — |
| 1F-01 | Mọi dòng B1 có mục đặc tả | ❌ | F11: D#3 "mail cảnh báo là yêu cầu bắt buộc đã thống nhất" — không đặc tả; F29: BR-XHD-18 một câu | GAP-02, 53 |
| 1F-02 | Mọi luồng được nhắc đều có đặc tả | ❌ | BR-XHD-10 "Job cảnh báo chạy 15 phút một lần …" không có đặc tả; BR-HK-02 nhắc "dòng EVC" nhưng không có rule (BR-HK-06 chuyển D#6) | GAP-31, 04 |
| 1F-03 | Mọi action có kết quả thành công + thất bại | ❌ | B2: ACT-01, 07, 19, 21, 22 không có kết quả thất bại; ACT-05 (PĐK chưa duyệt, HĐ con) và ACT-25 (khách FPL không lấy HĐ) không có đầu ra | GAP-26, 14, 16, 18, 20, 44, 46, 48 |
| 1F-04 | Validate có danh sách rule | ✅ | BR-XHD-10 liệt kê 8 rule chung + 6 rule chi tiết; BR-XHD-03 thêm PĐK, hợp đồng con | — |
| 1F-05 | Thứ tự validate / báo nhiều lỗi | ❌ | BR-XHD-10: "Không hợp lệ thì không phát hành và ghi log" — không có thứ tự, cách log nhiều lỗi | GAP-30 |
| 1F-06 | Đầu ra có nội dung + điều kiện | ❌ | B4: MSG-01, 02, 04, 05 không có nội dung / nơi ghi | GAP-29, 27, 02, 31 |
| 1F-07 | Không còn câu mơ hồ ở luồng chính | ❌ | "hợp đồng có hiệu lực" (BR-XHD-10); "cho khách chọn có lấy hóa đơn hay không (ví dụ FPL)" (BR-DB-03); "2h quét 1 lần" (BR-XHD-01) | GAP-13, 48, 50 |

**Tổng:** 12 ✅ · 14 ❌ · 4 ➖ (gồm 1 mục bổ sung 1D-01b). Lần 1: 9 ✅ · 15 ❌ · 4 ➖.

---

## §D. Kết luận (R4)

**⚠️ CONDITIONAL — plan có điều kiện** (giữ nguyên kết luận lần 1).

- Không rơi vào điều kiện REJECT: 1A-01, 1B-01 Pass; 1B-03 Fail nhưng hạ Major (lý do ở §C); 1A-02 N/A; số chức năng bị Blocker 3/28 = 11% (< 50%).
- Fail Critical ở cấp tài liệu: tài liệu tích hợp (1A-04), mâu thuẫn nội bộ (1B-02 — 7 cặp, đa số phát sinh khi rút gọn),
  điểm cần xác nhận không có hạn (1C-04), action thiếu kết quả thất bại (1F-03), câu mơ hồ (1F-07).

| Trạng thái | Số chức năng | Chức năng | So với lần 1 |
|---|---:|---|---|
| Đủ | 8 | F02, F05, F08, F12, F13, F14, F18, F20 | F08 lên Đủ; F01, F04 xuống Giả định; F25 → Ngoài phạm vi (14/10/2026) |
| Giả định | 15 | F01, F03, F04, F06, F07, F09, F10, F15, F16, F17, F19, F22, F23, F27, F28 | +F01, F04, F16, F27, F28; F01 gồm ma trận kênh × nhóm DV (14/10/2026, GAP-62) |
| Chờ bổ sung | 3 | F11, F21, F29 | F08, F16, F25 ra; F29 vào; F26 → Ngoài phạm vi (14/10/2026) |
| Ngoài phạm vi | 3 | F24, F25, F26 | TL — Điều chỉnh tính lương FPT Play SA, QC lead chốt 14/10/2026 |

**Est#TC (PATH B — chưa chạy analyze-requirements).** Profile INT, `tc_per_sc = 3` (QC lead chốt 07/10/2026). 16 rule validate
của F07 tính kiểu BVA (1 TC, hoặc 3 TC khi rule có ngưỡng). Phần Giả định cộng +20%, làm tròn lên theo từng chức năng.
Phân công theo QC lead chốt 13/10/2026 (4 QC).

| Module | F | SC | Est#TC gốc | Est#TC dùng | QC | Ghi chú |
|---|---|---:|---:|---:|---|---|
| XHD | F01 | 8 + ma trận | 24 + 680 | 29 + 680 = 709 | GiangDC2 (ma trận: 4 QC theo kênh) | +1 SC bán thêm; Giả định (lần 1: 21). **14/10/2026:** gộp ma trận tạo đơn 17 kênh × 20 nhóm DV × bán mới / bán thêm (680 TC, trước là F30; không +20%, GAP-62) — output: ghi nhận đủ đơn mọi kênh × nhóm DV × loại đơn |
| XHD | F02 | 7 | 21 | 21 | GiangDC2 | |
| XHD | F03 | 7 | 21 | 26 | HuyenNHK | Giả định |
| XHD | F04 | 14 | 42 | 51 | HuyenNHK | +7 SC: HĐ tổ chức đã/chưa duyệt PĐK, chưa duyệt rơi vào 2 ngày cuối tháng, HĐ không phải tổ chức, HĐ con (DV, TB), bán thêm trên HĐ tổ chức; Giả định (lần 1: 21) |
| XHD | F05 | 8 | 24 | 24 | HuyenNHK | +1 SC: đơn bán thêm cùng hợp đồng không gộp với đơn trước |
| XHD | F06 | 8 | 24 | 29 | HuyenNHK | +1 SC SubServiceType 31 trùng (§C#3), +1 SC bán thêm cùng dịch vụ khác mã đơn; Giả định (lần 1: 22) |
| XHD | F07 | 6 + 16 VAL | 48 | 58 | GiangDC2 | 18 TC luồng + 30 TC validate (7 × 3 + 9 × 1); Giả định |
| XHD | F08 | 5 | 15 | 15 | GiangDC2 | Chi nhánh HĐ cho DV, TB, HĐ gộp nhiều dòng, HĐ đổi chi nhánh giữa 2 lần phát hành, đơn bán thêm (lần 1: chưa estimate) |
| XHD | F09 | 6 | 18 | 22 | GiangDC2 | Giả định |
| XHD | F10 | 5 | 15 | 18 | GiangDC2 | Giả định |
| XHD | F27 | 7 | 21 | 26 | DatDGD | Mới — theo HĐ; bán thêm theo HĐ hiện hữu; FPL lấy HĐ nhập trong / quá 2 giờ; FPL không lấy HĐ; cập nhật không kích hoạt; lần sau dùng thông tin mới nhất; Giả định |
| XHD | F28 | 6 | 18 | 22 | HuyenNHK | Mới — chưa đủ / đủ 2h; chu kỳ 2h; mốc 22:05; realtime sau 22h; không theo lịch 12h/18h; Giả định |
| GN | F12 | 7 | 21 | 21 | AnhPTM17 | |
| GN | F13 | 9 | 27 | 27 | AnhPTM17 | |
| GN | F14 | 6 | 18 | 18 | AnhPTM17 | |
| GN | F15 | 9 | 27 | 33 | AnhPTM17 | Giả định |
| GN | F16 | 4 | 12 | 15 | AnhPTM17 | Chừa lock (2 nhánh của min), không lock, Paid voucher; Giả định (lần 1: chưa estimate) |
| GN | F17 | 11 | 33 | 40 | AnhPTM17 | +1 SC: đơn bán thêm dùng cọc còn lại của hợp đồng; Giả định |
| HK | F18 | 4 | 12 | 12 | DatDGD | |
| HK | F19 | 9 | 27 | 33 | DatDGD | +1 SC: loại đầu HĐ bán thêm; Giả định (bảng map ở 2.1) |
| HK | F20 | 5 | 15 | 15 | DatDGD | KCT / 0 / 5 / 8 / 10% + tổng cộng |
| HK | F22 | 3 | 9 | 11 | DatDGD | Giả định |
| HK | F23 | 5 | 15 | 18 | DatDGD | +1 SC: đơn bán thêm add tiền trả trước riêng; Giả định |
| TL | ~~F24~~ | | | | | **Ngoài phạm vi** 14/10/2026 |
| TL | ~~F25~~ | | | | | **Ngoài phạm vi** 14/10/2026 |
| | **Tổng commit** | | **1.187** | **1.264** | | Đủ 153 + Giả định 1.111 · XHD 1.021 (gồm ma trận FR01 680) · GN 154 · HK 89 · TL 0 (ngoài phạm vi) |
| XHD | *F11* | *3* | | *9* | | *Chờ GAP-02 — ngoài tổng* |
| HK | *F21* | *3* | | *9* | | *Chờ GAP-04 — ngoài tổng* |
| TL | ~~F26~~ | | | | | **Ngoài phạm vi** — QC lead chốt 14/10/2026 (GAP-06 đóng) |
| XHD | *F29* | *3* | | *9* | | *Chờ GAP-53 — ngoài tổng* |
| | *Tham khảo Chờ bổ sung* | | | *27* | | |

Theo QC: HuyenNHK 152 + 160 ma trận FR01 = 312 (F03–F06, F28) · GiangDC2 163 + 160 = 323 (F01, F02, F07–F10) · AnhPTM17 154 + 160 = 314 (F12–F17) · DatDGD 115 + 200 = 315 (F18–F20, F22, F23, F27). Scope test gom 11 chức năng FR01–FR11 (map ở TP §2.1a).

> TC_min theo B1–B4 (ACT 27 × ~2.5 + VAL 8 × 3 + 18 × 1 ≈ 110) vẫn thấp hơn nhiều so với Est#TC theo rule.
> Đó là do hệ thống backend không có tầng UI/popup, không phải dấu hiệu thiếu tầng action ⇒ dùng Est#TC theo rule.
> ~~Chiều biến thể kênh × dịch vụ chọn đại diện theo nhóm~~ → **14/10/2026 estimate lại:** phủ đủ trong F01 (lúc đầu tách là F30, gộp vào F01 cùng ngày), mỗi kênh (17 kênh §A.2)
> tạo đơn bán mới và bán thêm cho từng nhóm dịch vụ (20 nhóm §A.3) = 680 TC. Mức phủ theo nhóm DV, không theo 55 dịch vụ.
> Khi PM gửi ma trận kênh ↔ nhóm DV thực bán (GAP-62), cặp không bán thì bỏ (−2 TC / cặp).
> Loại đơn bán mới / bán thêm: +1 SC "bán thêm" cho 9 chức năng có rule phụ thuộc hợp đồng hoặc đơn trước (F01, F04, F05, F06,
> F08, F17, F19, F23, F27) = +31 TC; các chức năng còn lại phủ bán thêm bằng dữ liệu test, không thêm SC.

---

## §E. Danh sách cần bổ sung — DOC-GAP (R5, cập nhật lần 2)

> Hạn PM xác nhận = `D_confirm` **16/10/2026** (ngày LV liền trước ngày Clear nghiệp vụ 19/10/2026 — áp cho mọi chức năng).
> PM chọn cho **từng dòng còn mở**: `Bổ sung trước [ngày]` · `Out-scope` · `Giữ giả định của QC`. "OK" chung không tính.
> "Đưa vào rủi ro?" = `Chưa chốt` cho tới khi trao đổi xong.
> Cột **Lần 2**: `Đóng` (2.2 đã trả lời) · `Còn thiếu` · `Mới` (+ `doc-regression` nếu lỗi nằm trong nội dung mới/sửa ở 2.2).

### E.1 — GAP còn mở (45)

| GAP-ID | Lần 2 | Mã | Severity | Chức năng | Vị trí (URD 2.2) | Thiếu gì (cụ thể) | Câu hỏi / đề xuất cho BA | Ảnh hưởng plan | Người bổ sung | Hạn PM xác nhận | Ticket | PM xác nhận | Đưa vào rủi ro? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-02 | Còn thiếu | L3 | Blocker | F11 · ACT-10 · MSG-04 | Phụ lục D#3 | D#3: "mail cảnh báo là yêu cầu bắt buộc đã thống nhất", giao "PM và SA xử lý" — vẫn không có điều kiện phát hiện, lịch chạy, người nhận, nội dung mail | Mail cảnh báo có thuộc release v2.0 không? Nếu có: ai cung cấp đặc tả (URD hay tài liệu kỹ thuật), gồm điều kiện quét, tần suất, người nhận, mẫu nội dung | Chờ bổ sung (tham khảo ~9 TC) | PM + SA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-04 | Còn thiếu | L3 | Blocker | F21 | BR-HK-02 · D#6 | BR-HK-02 vẫn liệt kê "dòng EVC" trong thông tin phải chuẩn bị; BR-HK-06 (dòng EVC, dòng chiết khấu) chuyển D#6 "Kỹ thuật", mà bản 2.1 cũng chưa định nghĩa "nhóm EVC được thể hiện". Mail PM 13/10/2026: "EVC cần test => theo rule URD" — phần chính URD 2.2 không có rule dòng EVC | Theo mail PM, dòng EVC / chiết khấu (chỉ có ở phụ lục kỹ thuật) có nằm ngoài phạm vi test không? Nếu trong phạm vi: loại EVC nào thành dòng riêng, format dòng (dấu tiền, thuế suất); dòng chiết khấu áp cho đơn nào? | Chờ bổ sung (tham khảo ~9 TC); QC đề xuất Out-scope theo mail PM | SA / Dev | 16/10/2026 | chưa log | | **Có** — rủi ro #7 (14/10/2026) |
| GAP-06 | **Đóng 14/10/2026 — Out-scope (QC lead chốt)** | L2 | Blocker | F26 · ACT-24 | BR-TL-04 | Đã rõ hơn: "Trong giai đoạn UAT, trước go-live … FHR kiểm tra và nghiệm thu." Plan QC chỉ có R1, R2 trên STG, không có UAT | Xác nhận đối soát FHR **ngoài phạm vi test của QC** (do FHR nghiệm thu ở UAT)? Nếu QC phải hỗ trợ: tạo đơn ở kênh nào, chạy job lúc nào | Chờ bổ sung (tham khảo ~6 TC) — QC đề xuất Out-scope | PM + FHR | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-53 | Mới · doc-regression | L3 | Blocker | F29 · ACT-27 | BR-XHD-18 | Cả chức năng chỉ có 1 câu: "Bổ sung chức năng cho phép DVKH HO chủ động xử lý với hợp đồng có yêu cầu clear nội dung "thuê thiết bị đầu cuối" trên hóa đơn." Cột ghi chú: "Mới (kịp plan các chức năng chính sẽ thự hiện)". Không có: DVKH HO thao tác ở đâu (có màn hình không), "clear" là bỏ dòng hay bỏ chữ, áp từ lần phát hành nào, HĐ đã phát hành thì sao | BR-XHD-18 có thuộc release v2.0 không ("kịp plan" nghĩa là gì)? Nếu có: đặc tả luồng thao tác + kết quả trên HĐ + điều kiện áp dụng; có UI thì gửi thiết kế | Chờ bổ sung (tham khảo ~9 TC); có UI thì estimate thêm | PO + BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-07 | Còn thiếu | L1 | Critical | Toàn bộ · MSG-06/07/08 | I Actor · II · III · Phụ lục D | Không có tài liệu tích hợp: payload Kafka Order Event / Invoice Event / Kafka Out; schema OB_OrderRaw*, OB_OrderBill*, Paid, Payment; API kênh TT, nguồn tiền EVC + lock, Billing, HĐĐT, hệ thống Dịch vụ; format tín hiệu giao hàng 3 nguồn; giá trị enum (paymentstatus, PaidType, ProductType, trạng thái đơn, mã "phương thức thanh toán đặc biệt"). 2.2 Phụ lục D chỉ trỏ "Chi tiết xem URD v2.1" | Cung cấp SDD / API spec / schema (hoặc link Confluence) + bảng giá trị enum | Không chặn viết TC nghiệp vụ; **chặn Setup data + Execute** | Dev Lead / SA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-09 | Còn thiếu | L9 | Critical | Toàn bộ | §C | OI-1…OI-7 đã bỏ (D#8). Thay bằng §C 3 điểm (ký hiệu HĐĐT; ý nghĩa Type 1–4 và map ProductType; SubServiceType 31 trùng) — bảng không có người chốt và ngày chốt | Điền owner + ngày chốt cho từng điểm §C (ngày ≤ 19/10/2026) | Quyết định GAP-17, 41 có kịp lịch không | PM | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-11 | Còn thiếu | L9 | Critical | F03 | Phụ lục D#3 | Cơ chế xử lý bản tin về trễ qua ngày vẫn chưa quyết, nay giao "PM và SA xử lý" | Chọn phương án nào, có trong v2.0 không? | Giả định: test hiện trạng (dòng không được phát hành); TC phương án làm sau | PM + SA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-12 | Còn thiếu | L9 | Critical | F06 | Phụ lục D#2 | D#2: "Rủi ro phát hành hóa đơn trùng khi worker và realtime chạy song song. … PM và SA chốt phương án kỹ thuật." — chưa có expected cho case race | Phương án kỹ thuật + ngày có? | Giả định: test chống trùng tuần tự; case song song test sau | PM + SA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-13 | Còn thiếu | L5 | Critical | F07 · VAL-02, VAL-03 | BR-XHD-10 | "Đơn không ở trạng thái hủy hoặc đang cập nhật" và "hợp đồng có hiệu lực" — không nêu field / giá trị trạng thái | Liệt kê trạng thái hợp đồng được coi là có hiệu lực + giá trị trạng thái đơn "đang cập nhật" | Giả định theo URD v1.0 (chưa nhận — GAP-24) | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-14 | Còn thiếu | L4 | Critical | F09 · ACT-07 | BR-XHD-13 | Chỉ có kết quả thành công khi gọi Billing System; Billing lỗi / timeout / đã sinh số mà INVOICE không nhận được phản hồi: không đặc tả | Billing lỗi thì giữ BillNumber rỗng chờ đợt sau, retry hay cảnh báo? Billing đã sinh số mà INVOICE không nhận được thì xử lý ra sao? | Giả định: giữ rỗng, ghi log, đợt sau xử lý lại | BA + Dev | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-16 | Còn thiếu | L4 | Critical | F16, F17 · ACT-19 | BR-GC-01 · BR-VC | BR-GC-01 cần "tổng tiền EVC của đơn (tính cả phần bị lock)", BR-VC cần tiền lock — 2.2 không nói lấy từ đâu (2.1 BR-VC-07: API đội EVC) và không có hành vi khi nguồn này lỗi / timeout | Nguồn tổng tiền EVC + lock là API đội EVC đúng không? Lỗi / timeout thì áp như BR-XL-03 (dừng, chờ điểm chạm sau)? | Giả định: API đội EVC, lỗi thì giống BR-XL-03 | BA + đội EVC | 16/10/2026 | chưa log | | **Có** — rủi ro #7 (14/10/2026) |
| GAP-17 | Còn thiếu | L6 | Critical | F19 | BR-HK-03 · §C#1 · D#5 | BR-HK-03: "Ký hiệu hóa đơn xác định theo quy định thuế; DVKH HO chốt với FAF … Bảng map vùng miền và các đơn vị có đầu số riêng xem tài liệu kỹ thuật"; cột ghi chú "cần chốt ký hiệu". Chưa có bảng loại HĐ → đầu, tỉnh → vùng bản chốt | Gửi bản chốt ký hiệu + bảng loại hóa đơn → đầu, danh mục tỉnh → vùng; ngày DVKH HO chốt với FAF? HĐ bán mới và HĐ bán thêm dùng đầu nào (2.1 BR-HK-04: "hóa đơn cước và hóa đơn bán mới dùng đầu khác nhau")? | Giả định trên bảng map của 2.1; chưa test được tỉnh → vùng | DVKH HO + FAF | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-18 | Còn thiếu | L4 | Critical | F22 · ACT-21 | BR-HK-02 | "Chưa đủ thì chưa đẩy" — có; đẩy sang hệ thống HĐĐT thất bại: không đặc tả (retry, đánh dấu, cảnh báo) | Đẩy lỗi thì xử lý ra sao, có retry không? | Giả định: không đánh dấu đã đẩy, lần sau đẩy lại | BA + Dev | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-20 | Còn thiếu | L4 | Critical | F23 · ACT-22 | Hình III nhánh B | Đẩy sang hệ thống Dịch vụ thất bại: không đặc tả | Đẩy lỗi thì có đánh dấu không, retry ra sao? | Giả định: không đánh dấu, đẩy lại lần sau | BA + Dev | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-31 | Còn thiếu · ↑ Major → Critical | L3 | Critical | F07 · ACT-11 · MSG-05 | BR-XHD-10 | 2.2 đưa job vào thân BR: "Job cảnh báo chạy 15 phút một lần để bổ sung thông tin kịp trước giờ chốt." và bỏ câu "chạy độc lập ngoài luồng này" của 2.1 ⇒ thành in-scope, nhưng không có điều kiện, người nhận, nội dung cảnh báo | Xác nhận job thuộc v2.0; đặc tả điều kiện quét, kênh cảnh báo, người nhận, nội dung | Chưa tính TC; nếu in-scope +~9 TC | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-40 | Mới · doc-regression | L7 | Critical | F15, F16 · VAL-21 | BR-DP-01 · BR-GN-01 · BR-VC · BR-GC-03 | BR-DP-01: Paid đồng bộ "gồm cả voucher và tiền khách thanh toán"; BR-VC: "Phần gạch nợ bằng EVC do đội EVC thực hiện"; nhưng BR-GN-01 chỉ lọc "Amount > 0 và cùng OrderCode", không loại dòng Paid voucher ⇒ INVOICE có thể gạch trùng phần đội EVC đã gạch. Thứ tự cũng chưa rõ: BR-GC-03 "Tính trên nợ còn lại sau khi EVC đã gạch" — INVOICE biết EVC đã gạch bằng cách nào? Mail PM 13/10/2026 "EVC cần test => theo rule URD" chưa trả lời điểm này | Dòng Paid có PaidType voucher/EVC có bị loại khỏi gạch nợ ở INVOICE không? INVOICE gạch tiền khách trước hay phải chờ đội EVC gạch xong, nhận biết qua đâu? | Giả định: loại Paid voucher; không phụ thuộc thứ tự | BA + đội EVC | 16/10/2026 | chưa log | | **Có** — rủi ro #7 (14/10/2026) |
| GAP-41 | Mới · doc-regression | L7 | Critical | F06 · VAL-17 | BR-XHD-08 · §C#3 · BR-DB-07 | BR-XHD-08 2.2: "dịch vụ = mã đơn hàng + dịch vụ hóa đơn + Gói dịch vụ; thiết bị thêm phương thức triển khai" (cột "So với v2.1": "Giữ nguyên"); 2.1: "OrderCode + ServiceCode + SubserviceType". §C#3 lại nói "Khóa chống trùng có dùng SubServiceType"; BR-DB-07 map tín hiệu vẫn dùng "ServiceCode + SubserviceType". Yêu cầu "hai dòng cùng khóa thì ghi log" của 2.1 cũng bị bỏ | Khóa chống trùng chốt theo bản nào? "dịch vụ hóa đơn" / "Gói dịch vụ" là field nào? Map tín hiệu (BR-DB-07) và chống trùng có dùng chung một khóa không? SubServiceType 31 trùng thì xử lý sao? | Giả định theo text 2.2; expected chống trùng có thể đổi cả nhóm TC | BA + SA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-42 | Mới · doc-regression | L7 | Critical | F01 | BR-DB-01 · BR-DB-03 · BR-XHD-03 | BR-DB-01 2.2: "Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng." (2.1 có thêm "tạo Đơn hàng" và "cập nhật thông tin khách hàng"). Nhưng BR-DB-03 vẫn nói "Cập nhật thông tin khách không kích hoạt phát hành" và BR-XHD-03 tính delay FPL "theo thời gian tạo đơn" ⇒ cần 2 sự kiện đã bỏ | Sự kiện tạo đơn và cập nhật thông tin khách còn được đồng bộ về INVOICE không? Nếu bỏ thì INVOICE lấy thời gian tạo đơn và thông tin khách cập nhật từ đâu? | Giả định: vẫn đủ 4 sự kiện như 2.1 | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-43 | Mới | L7 | Critical | F03 · ACT-04 | BR-XHD-01 · BR-XHD-06 | BR-XHD-01: "Đơn đủ điều kiện sau giờ chốt cuối của ngày cuối tháng sẽ phát hành sang tháng sau"; BR-XHD-06 (realtime): "Xử lý ngay khi nhận, không chờ đợt worker kế tiếp" ⇒ tín hiệu về 19:00 ngày cuối tháng phát hành ngay trong tháng hay sang tháng sau? *(Có từ 2.1, lần 1 chưa bắt)* | Ngày cuối tháng, sau giờ chốt cuối thì realtime có chạy không? Câu "phát hành sang tháng sau" áp cho trường hợp nào? | Giả định: realtime vẫn chạy; câu cuối tháng chỉ áp cho dòng realtime không xử lý được | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-44 | Mới · doc-regression | L4 | Critical | F04 · VAL-24 | BR-XHD-03 | "Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK; hai ngày cuối tháng không xét điều kiện này. Quên duyệt PĐK thì không autobill." — không nói khi PĐK được duyệt muộn thì đợt sau có tự phát hành không, hay chuyển xuất tay (ngoài phạm vi) | PĐK duyệt sau giờ chốt / sang ngày khác thì dòng đó có được worker đợt sau nhặt không? "Không autobill" có nghĩa phải xuất tay? | Giả định: duyệt xong thì đợt kế tiếp phát hành | BA + PO | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-48 | Mới · doc-regression | L4 | Critical | F27 · ACT-25 | BR-DB-03 | "Ngoại lệ: kênh bán FPL cho khách chọn có lấy hóa đơn hay không (ví dụ FPL)." — (1) chỉ FPL hay FPL chỉ là ví dụ? (2) khách chọn **không** lấy hóa đơn thì xuất theo thông tin gì? (3) hết 2 giờ mà khách không nhập thì xử lý sao? | Trả lời 3 ý; nếu có kênh khác ngoài FPL thì liệt kê theo SaleChannelID §A.2 | Giả định: chỉ FPL; không lấy HĐ hoặc quá 2 giờ → dùng thông tin hợp đồng | BA + PO | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-50 | Mới · doc-regression | L5 | Critical | F28 · ACT-26 · VAL-26 | BR-XHD-01 · BR-XHD-06 | "Xét riêng cho kênh bán FPL: 2h quét 1 lần / Mốc 22:05 chốt từ 0h đến 22 giờ" — không nói chu kỳ 2h bắt đầu lúc mấy giờ, giờ chốt mỗi đợt, đợt 22:05 có phải đợt cuối không, lịch FPL có là tham số cấu hình như lịch chung không. BR-XHD-06: "Đối với Kênh bán FPL chỉ realtime từ sau mốc 22h" | Liệt kê các mốc chạy / giờ chốt của worker FPL trong ngày; lịch FPL có cấu hình được không? | Giả định: 0:05, 2:05 … 22:05, chốt đúng giờ chẵn; có tham số | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-60 | Mới | L2 | Major | F01, F04, F06, F17, F19, F23, F27 | Toàn bộ URD 2.2 · 2.1 BR-HK-04 | Phạm vi test gồm cả đơn **bán mới** và **bán thêm** (PM xác nhận qua mail 13/10/2026), nhưng URD 2.2 không có từ "bán mới" / "bán thêm" — mọi BR viết chung cho "đơn hàng". Bản 2.1 chỉ nhắc ở BR-HK-04: "hóa đơn cước và hóa đơn bán mới dùng đầu khác nhau". Severity hạ từ Blocker (1B-03) xuống Major: phạm vi đã có PM xác nhận bằng văn bản, không mâu thuẫn BR nào, không thêm luồng — chỉ còn xác nhận điểm khác biệt | Xác nhận mọi BR áp chung cho bán mới và bán thêm; nếu có điểm khác thì nêu rõ. Với đơn bán thêm QC đang hiểu: chống trùng theo mã đơn mới (BR-XHD-08) · gạch nợ Cọc dùng cọc còn lại của hợp đồng (BR-GC-01) · add tiền trả trước riêng cho đơn bán thêm (BR-HK-09) · thông tin khách theo hợp đồng hiện hữu (BR-DB-03) — đúng không? | Giả định: rule áp chung; +1 SC "bán thêm" cho 9 chức năng (+31 TC) | BA + PO | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-24 | Còn thiếu | L1 | Major | Toàn bộ | §A.4 #2 | Chưa nhận URD v1.0 (Phase 1) trong khi §A.4 dùng làm nền tảng và kênh TMĐT Phase 1 cần test hồi quy | Gửi URD v1.0 + chỉ rõ hành vi Phase 1 nào giữ / đổi | Regression TMĐT dựng theo giả định | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-26 | Còn thiếu | L4 | Major | F01 · ACT-01 | BR-DB-05 | Bản tin Order Event lỗi giải mã / thiếu trường: không đặc tả | Hành vi khi bản tin lỗi (bỏ qua + log? dead-letter?) | Giả định: bỏ qua + log | BA + Dev | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-27 | Còn thiếu | L6 | Major | F02 · MSG-02 | BR-DB-07 | "chỉ ghi log nội dung tín hiệu vào cột Note" — cột Note thuộc bảng nào, format ra sao | Bảng + format nội dung Note | Expected TC không định lượng được | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-29 | Còn thiếu | L6 | Major | F07 · MSG-01 | BR-XHD-10 | "Không hợp lệ thì không phát hành và ghi log" — log ở đâu, nội dung gì | Nơi ghi + nội dung log (có ghi lý do từng rule không) | Như trên | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-30 | Còn thiếu | L5 | Major | F04, F07 · VAL-01..16, 24, 25 | BR-XHD-03 · BR-XHD-10 | Không có thứ tự kiểm tra; nhiều rule sai cùng lúc thì log tất cả hay rule đầu | Thứ tự validate + cách log nhiều lỗi | +TC tổ hợp lỗi | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-32 | Còn thiếu | L2 | Major | F10 · ACT-09 | Phụ lục D#1 | 2.2 chuyển cutover sang phụ lục kỹ thuật ("PM, SA") — chưa rõ có test trên STG không, dữ liệu luồng cũ lấy đâu, tên cờ bật/tắt | Cutover có thuộc phạm vi test của QC không? Nếu có: cách chuẩn bị dữ liệu luồng cũ | Giả định in-scope (18 TC); Out-scope thì giảm 18 TC | PM + SA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-34 | Còn thiếu | L2 | Major | F19 | BR-HK-03 · D#5 | Đơn vị có đầu số / dãy số / mẫu riêng chuyển D#5 "DVKH HO chốt với FAF" — chưa nói in hay out scope test | In-scope v2.0 không? Nếu in: danh sách đơn vị + quy tắc | Chưa tính TC | PM | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-35 | Còn thiếu | L3 | Major | F22 | BR-HK-02 · D#6 | BR-HK-02 cần "thông tin theo mẫu"; BR-HK-08 chuyển D#6 "Kỹ thuật" — không có danh sách trường theo từng mẫu | Danh sách trường theo từng mẫu | Expected TC thiếu trường | SA / Dev | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-36 | **Đóng 14/10/2026 — TL ngoài phạm vi** | L3 | Major | F24 · ACT-23 | IV · Hình IV | Bước "Tính hoa hồng" chỉ ghi "Tính trên dữ liệu đã gộp và khử trùng" — không có công thức / tham chiếu | Công thức hiện hành (làm baseline) + cách nhận diện bản ghi nguồn mới | Giả định: công thức giữ nguyên luồng cũ | BA + FHR | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-45 | Mới · doc-regression | L6 | Major | F04 · VAL-24 | BR-XHD-03 | "Hợp đồng tổ chức", "đã duyệt PĐK", "hai ngày cuối tháng" — không nêu field / giá trị nhận diện HĐ tổ chức, trạng thái duyệt PĐK lấy từ đâu, 2 ngày cuối tính theo ngày chạy worker hay mốc nghiệp vụ | Field + giá trị nhận diện HĐ tổ chức; nguồn trạng thái PĐK; cách tính 2 ngày cuối tháng (tháng 30 / 31 / tháng 2) | Giả định: theo loại hình KH cấp 1; ngày chạy worker | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-46 | Mới · doc-regression | L4 | Major | F04 · VAL-25 | BR-XHD-03 | "Không phát hành hóa đơn trên hợp đồng con, cả thiết bị và dịch vụ." — dòng của HĐ con được ghi nhận thế nào (log? trạng thái?), có phát hành trên HĐ cha thay không | Đơn của HĐ con: ai xuất HĐ, ở đâu; INVOICE có ghi log / đánh dấu không? | Giả định: chỉ không phát hành, không có đầu ra khác | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-47 | Mới · doc-regression | L10 | Major | F04 | Revision History 2.2 · BR-XHD-03 | Revision 2.2: "[A]: Điều kiện duyệt PĐK, hợp đồng con, KH Chuỗi/Dự án (gộp vào BR-XHD-03)" — BR-XHD-03 không có nội dung nào về KH Chuỗi | KH Chuỗi có rule riêng không? Nếu có thì bổ sung vào BR-XHD-03 | Có thể thiếu TC | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-49 | Mới · doc-regression | L6 | Major | F27 | BR-DB-03 | 7 trường khách tự nhập (tên, email, SĐT, MST, mã định danh, mã quan hệ ngân sách, số hộ chiếu) — trường nào bắt buộc, khác nhau giữa cá nhân / tổ chức không, INVOICE có kiểm tra định dạng không | Liệt kê trường bắt buộc theo loại khách + bên kiểm tra định dạng | Giả định: kênh FPL kiểm tra, INVOICE chỉ dùng | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-51 | Mới · doc-regression | L7 | Major | F28 · VAL-26 | BR-XHD-03 · BR-DB-03 | Mốc delay FPL: BR-XHD-03 "lấy chuẩn theo thời gian tạo đơn" ↔ BR-DB-03 "tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh". Delay áp cho cả DV và TB? | Hai mốc này là một không? Delay 2h áp cho thành phần nào? | Giả định: cùng mốc tạo đơn, áp cho DV | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-54 | Mới · doc-regression | L7 | Major | F04, F05 | Phụ lục D#9 · TN #3 · BR-XHD-03 | D#9: "Autobill thiết bị theo phương thức triển khai (gom một lượt theo từng phương thức). \| BR-XHD-04 \| Đã bỏ khỏi tài liệu." nhưng TN #3 vẫn ghi "là đơn vị autobill của thiết bị" và BR-XHD-03 vẫn phát hành TB theo tín hiệu của phương thức | Bỏ hành vi hay chỉ bỏ câu chữ? Trường hợp giao thiếu trong cùng phương thức (2.1: PO đã chấp nhận phát hành cả lô) còn đúng không? | Giả định: hành vi giữ như 2.1 | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-55 | Mới · doc-regression | L4 | Major | F07 | BR-XHD-10 | Gộp BR-XHD-11 nhưng mất câu 2.1: "Dòng không phát hành được vẫn giữ trạng thái BillNumber IS NULL. Nếu về sau có bản tin đồng bộ mới cho đơn đó thì dòng được xuất hóa đơn theo bản tin mới". 2.2 còn lại: "hệ thống không giữ chờ phát hành lại" + "Job cảnh báo … để bổ sung thông tin kịp trước giờ chốt" ⇒ bổ sung xong thì đợt sau có phát hành không? | Sau khi bổ sung thông tin thiếu, dòng có được phát hành ở đợt kế tiếp không, cần bản tin mới không? | Giả định: theo 2.1 (cần bản tin mới) | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-56 | Mới · doc-regression | L10 | Major | Toàn bộ | Cột "So với v2.1" | Ghi "Giữ nguyên" ở BR đã đổi nội dung: BR-XHD-01 (thêm lịch FPL), BR-XHD-06 (thêm FPL realtime), BR-XHD-08 (đổi khóa), BR-XHD-10 (mất câu bản tin mới) ⇒ không dùng cột này để khoanh vùng thay đổi được | Rà lại cột "So với v2.1" cho toàn bộ BR | QC phải tự diff toàn bộ mỗi bản mới | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-57 | Mới | L1 | Major | F04, F08, F29 | §A.4 #3 | "Email ISC ngày 24/09/2026; email FTQ ngày 30/09/2026" — căn cứ của BR-XHD-18, điều kiện PĐK, chi nhánh theo HĐ — QC chưa nhận | Forward 2 email cho QC | Thiếu căn cứ khi BR mơ hồ | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-59 | Mới · doc-regression | L4 | Major | F23 | BR-HK-09 · BR-HK-01 · Hình III | "Mỗi đơn chỉ add tiền trả trước một lần, kể cả khi đơn phát hành ở nhiều đợt hóa đơn." — add ở đợt nào, số tiền gồm phần của các đợt sau không? Hình III nhánh B "đẩy dịch vụ" ↔ BR-HK-01 "không phân biệt dịch vụ hay thiết bị" | Đơn xuất 2 đợt: add tiền trả trước ở đợt 1 với toàn bộ tiền đơn hay chỉ phần đã xuất? TB có add không? | Giả định: đợt đầu, toàn bộ tiền DV của đơn | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-61 | Mới | L5 | Major | F04 · VAL-24 | BR-XHD-03 | "Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK" — đơn **bán thêm** trên hợp đồng tổ chức đã duyệt PĐK từ lần bán mới: có cần duyệt PĐK mới cho đơn bán thêm không? | Bán thêm trên HĐ tổ chức xét PĐK của lần nào? | Giả định: mỗi đơn bán thêm có PĐK riêng, phải duyệt | BA + PO | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-62 | Mới (14/10/2026) | L2 | Major | F01 | §A.2 · §A.3 · BR-XHD-12 | §A.2: "Tất cả kênh bán trong danh sách dưới đây thuộc phạm vi."; §A.3: "Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ)." — hai danh sách riêng rẽ, không có ma trận kênh nào bán nhóm DV nào, bán mới hay bán thêm. BR-XHD-12: "Chi nhánh nào được bán sản phẩm dịch vụ nào do bên quản lý sản phẩm bổ sung thuộc tính, nằm ngoài URD này" | Gửi ma trận kênh × nhóm DV × loại đơn (bán mới / bán thêm) mà từng kênh thực bán; cặp không bán thì QC bỏ khỏi phạm vi test | Giả định: đủ 17 × 20 = 340 cặp × 2 loại đơn = 680 TC; mỗi cặp bỏ −2 TC. Effort ma trận F01 ≈ 88 md làm Feasibility không đáp ứng (TP §6) | PM + bên quản lý sản phẩm | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-22 | Còn thiếu · ↓ Major → Minor | L10 | Minor | Toàn bộ | Revision History | PO đã confirm URD 2.2 (mail PM 13/10/2026) nhưng cột Approver vẫn trống ở cả 4 bản, tài liệu không ghi trạng thái | Điền Approver + trạng thái Approved cho bản 2.2 để tài liệu tự chứng minh được | — | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-52 | Mới · doc-regression | L7 | Minor | F03, F28 | §A.1 #3 · BR-XHD-01 | §A.1 #3: "dùng một lịch chung … thay vì chia theo kênh" ↔ BR-XHD-01: "Dùng chung một lịch cho mọi ngày và mọi kênh bán khác FPL" + lịch riêng FPL | Sửa mục tiêu §A.1 #3 cho khớp | — | BA | 16/10/2026 | chưa log | | Chưa chốt |
| GAP-58 | Mới · doc-regression | L3 | Minor | Toàn bộ | §A.4 #4 | "[Bổ sung link … cho từng chức năng]" — link draw.io của 2.1 bị bỏ, chưa điền link mới | Điền link lưu đồ | — | BA | 16/10/2026 | chưa log | | Chưa chốt |

**Tổng còn mở:** 45 GAP — 3 Blocker · 18 Critical · 21 Major · 3 Minor (24 còn từ lần 1 · 22 mới lần 2, 18 `doc-regression` · GAP-62 thêm 14/10/2026).
Ticket Jira: chưa tạo (project_key TBD; tạo khi user đồng ý).

### E.2 — GAP đã đóng ở lần 2 (15)

| GAP-ID | Mã | Severity cũ | Chức năng | Nội dung lần 1 (tóm tắt) | Căn cứ đóng (URD 2.2) |
|---|---|---|---|---|---|
| GAP-01 | L9 | Blocker | F08 | Thiếu bảng mapping (loại DV, kênh bán) → chi nhánh | BR-XHD-12: "Chi nhánh xuất hóa đơn là chi nhánh quản lý hợp đồng, xác định tại thời điểm phát hành và lưu trên tồn xuất hóa đơn"; D#7: "Không còn áp dụng vì chi nhánh theo hợp đồng." |
| GAP-03 | L7 | Blocker | F16 | Text bỏ bước EVC nhưng Hình 2 + BR-GN-03 + BR-VC-02..05 còn logic Config EVC / trần 50% | BR-VC: "Phần gạch nợ bằng EVC do đội EVC thực hiện"; Hình II: "Phần EVC do đội EVC gạch."; BR-GN-03 không còn "gạch EVC TRƯỚC"; cấu hình EVC chuyển D#4. Phần còn lại → GAP-40 |
| GAP-05 | L9 | Blocker | F25 | `[?]` kênh bán + loại dịch vụ để lọc FPT Play SA | §A.2 (17 kênh) + §A.3 "5 \| FPT Play Stands Alone \| SubScription \| 17 – Thiết bị (Type 2) ¶ 18 – Giải trí đa nền tảng (Type 1)"; BR-TL-04: "lên đơn bán FPT Play SA từ tất cả kênh bán … Phủ mọi kênh để bước lọc theo kênh nhận đúng dữ liệu." QC hiểu: lọc theo kênh thuộc §A.2 + ServiceID 5; mail PM 13/10/2026: "Nhóm sản phẩm => URD" |
| GAP-08 | L2 | Critical | Toàn bộ | Không liệt kê kênh bán trong phạm vi | §A.2: bảng 17 kênh (SaleChannelID 1 … 21); kênh sàn TMĐT = Shopee (20), Tiktok (21) "Đã triển khai ver1.0"; mail PM 13/10/2026: "Danh sách kênh đơn hàng => URD" |
| GAP-10 | L9 | Critical | F03 | Đề xuất lịch của DVKH chưa đồng thuận | BR-XHD-01: "Giá trị áp dụng: chia 2 đợt, đợt 1 chốt 12:00 chạy 12:05; đợt 2 chốt 18:00 chạy 18:05 ¶ Sau giai đoạn pilot sẽ đánh giá lại" |
| GAP-15 | L3 | Critical | F15 | Câu cụt "p/s: Hiện tại trừ napas thì" | Câu không còn trong 2.2 (BR-GN-04 viết lại) — QC hiểu không có ngoại lệ Napas |
| GAP-19 | L7 | Critical | F23 | Idempotent theo đơn ↔ theo (đơn × dịch vụ) | BR-HK-09 + Hình III: "Mỗi đơn chỉ add tiền trả trước một lần" — chốt mức đơn. Phần còn lại → GAP-59 |
| GAP-21 | L10 | Major | Toàn bộ | Header 2.0 ≠ Revision 2.1 ≠ tên file | Header 2.2 = Revision 2.2 = tên file v2_2 |
| GAP-23 | L8 | Major | Toàn bộ | §V chưa cập nhật, tham chiếu sai | D#8: "Các câu hỏi cũ ở mục V của v2.1 … Đã gộp vào mục C hoặc không còn áp dụng." |
| GAP-25 | L1 | Major | Toàn bộ | Link tài liệu FTQ là "…" | §A.4 không còn tham chiếu tài liệu FTQ, thay bằng email FTQ 30/09 (→ GAP-57) |
| GAP-28 | L6 | Major | F06 | Log 2 dòng cùng khóa: nơi ghi + nội dung | BR-XHD-08 2.2 không còn yêu cầu ghi log này (đã nêu trong GAP-41) |
| GAP-33 | L9 | Major | F17 | EVC loại mới trong nhánh Cọc chưa chốt | D#4: "Cấu hình EVC … BR-GC-04 đến 07 \| Đội EVC thực hiện" |
| GAP-37 | L8 | Minor | F16, F17 | Tham chiếu sai BR-GC-05, Hình 2 | BR-GC-05 đã gộp; Hình II vẽ lại, tham chiếu đúng |
| GAP-38 | L8 | Minor | Toàn bộ | Còn hướng dẫn template + track change | Không còn mục hướng dẫn template; glossary sạch |
| GAP-39 | L7 | Minor | F02, F04, F06 | Dùng lẫn "Phương thức" / "Hình thức" triển khai | 2.2 chỉ dùng "phương thức triển khai" (0 lần "Hình thức triển khai") |

---

## §F. Mail yêu cầu PM xác nhận (R6 — hiển thị để copy, KHÔNG tự gửi)

```
Tiêu đề: [Invoice Issuance Architecture v2.0] QC cần PM xác nhận 45 mục tài liệu (URD 2.2) trước 16/10/2026

Chào chị Lệ (Leltm),
Cảm ơn chị đã xác nhận ở mail 13/10/2026: PO đã confirm URD 2.2; kênh bán và nhóm sản phẩm theo URD;
phạm vi gồm bán mới + bán thêm; EVC test theo rule URD.
QC đã rà URD Invoice Issuance Architecture bản 2.2 (08/10/2026) so với bản 2.1 để cập nhật Test Plan v2.0.
Kết luận: CONDITIONAL — 23/26 chức năng đủ đặc tả để estimate (8 đủ, 15 theo giả định của QC),
3 chức năng chưa estimate được; đối soát FHR (F26) QC chốt ngoài phạm vi.

Bản 2.2 đã trả lời 15/39 mục QC hỏi lần trước (chi nhánh theo hợp đồng, danh sách kênh bán
và dịch vụ, gạch EVC do đội EVC, lịch 12h/18h…). Còn 24 mục cũ chưa trả lời và 22 mục mới phát sinh,
phần lớn ở nội dung bổ sung (kênh FPL, duyệt PĐK, hợp đồng con, BR-XHD-18) và ở các BR bị đổi
khi rút gọn nhưng vẫn ghi "Giữ nguyên" (khóa chống trùng BR-XHD-08, sự kiện đồng bộ BR-DB-01).
Ngoài ra phạm vi test gồm cả đơn bán mới và bán thêm, nhưng URD chưa nói rule nào áp riêng
cho đơn bán thêm (GAP-60, 61).
Về EVC: phần chính URD không có rule cho dòng EVC trên HĐĐT (chỉ ở phụ lục kỹ thuật) và chưa nói
Paid voucher có bị loại khỏi gạch nợ không — QC hỏi lại ở GAP-04, GAP-40.

Cần anh/chị xác nhận TỪNG DÒNG trong bảng đính kèm trước 16/10/2026
(ngày QC bắt đầu Clear nghiệp vụ: 19/10/2026), mỗi dòng chọn 1 trong 3:
  (1) Bổ sung trước <ngày>   (2) Out-scope   (3) Giữ giả định của QC

- Blocker: 3 mục — Mail cảnh báo bản tin trễ, Dòng EVC/chiết khấu trên HĐĐT,
  Clear "thuê thiết bị đầu cuối" (BR-XHD-18) chưa được estimate, chưa tính vào effort.
  Đối soát FHR: QC để ngoài phạm vi (FHR nghiệm thu ở UAT).
- Critical: 18 mục — QC đang plan theo giả định, buffer +20% phần chức năng tương ứng.
  Riêng tài liệu tích hợp (payload Kafka, schema bảng, API) cần có trước khi Setup data.
- Major/Minor: 24 mục — không chặn plan, cần bổ sung trước khi viết TC.
  Riêng GAP-62 (kênh nào bán nhóm dịch vụ nào): QC đang test đủ 17 kênh × 20 nhóm DV × bán mới / bán thêm
  = 680 TC (tổng 1.264 TC). Lịch QC chốt 19/10–13/11/2026 có 65 md, thấp hơn estimate
  145 md (đã tính AI gen TC 80%) ⇒ cần chị gửi ma trận kênh ↔ nhóm DV thực bán để QC thu hẹp phần không bán.

Dòng chưa được xác nhận tới 16/10/2026: phần chức năng tương ứng sẽ dời mốc viết TC,
và QC sẽ trao đổi lại để chốt có đưa vào mục Rủi ro của Test Plan hay không.

Trân trọng,
HuyenNHK
```
