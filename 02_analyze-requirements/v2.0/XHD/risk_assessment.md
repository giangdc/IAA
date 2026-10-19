---
id: v2.0/XHD/risk_assessment
title: Risk Assessment — Module XHD
type: risk_assessment
version: v2.0
module: { code: XHD, dir: XHD, name: "Đồng bộ đơn hàng & xuất hóa đơn tự động" }
counts:                 # 🔑 CANONICAL — CL/RISK của module XHD
  cl: 34
  cl_open: 17
  cl_blocking: 3        # CL chặn sinh TC / execute (đánh dấu ⛔ BLOCKING)
  risk: 10
  risk_high: 6
status: ANALYZED
updated: 2026-10-19
---

# Risk Assessment — v2.0 · Module XHD

> Tạo bởi: analyze-requirements. Đánh giá rủi ro per module + định hướng test focus cho generate-tc/vibe-test.
>
> **Structure-lock:** dùng DUY NHẤT 1 dạng bảng chi tiết hợp nhất bên dưới cho MỌI module (KHÔNG dùng nhiều dạng bảng khác nhau giữa các module). KHÔNG đổi cột. Bảng gồm 9 cột (thêm `Solution` + `Status` để track vòng đời rủi ro).
>
> **Governance (layout v2):** file này là **nguồn PRIMARY duy nhất** cho risk + **Clarification** của module XHD. Risk xuyên suốt cả 3 module (thiếu tài liệu tích hợp, cutover, URD v1.0) đặt ở đây vì XHD là module đầu chuỗi — module bị ảnh hưởng ghi ở `CHANGELOG.md §2`. Bảng roll-up toàn dự án là **DERIVED**, sinh on-demand, ⛔ không lưu file.
> Mã `GAP-NN` trỏ về `01_test-plans/DOC-READINESS-InvoiceIssuance-v2.0.md` / TP §2.4 (nơi PM xác nhận) — CL ở đây là bản phân tích có quote, không thay thế danh sách GAP.

## Tổng quan
| Module | Risk Level | Rủi ro chính |
|--------|-----------|--------------|
| XHD | High | Thiếu tài liệu tích hợp (payload Kafka, schema, enum) và nhiều mâu thuẫn nội bộ sau khi rút gọn URD 2.2 (sự kiện đồng bộ, khóa chống trùng, cuối tháng ↔ realtime, lịch FPL) — expected của nhiều SC phải giữ dạng giả định |

## Chi tiết rủi ro (bảng hợp nhất — 1 dạng cho mọi module)
| Risk ID | Module/Area | Rủi ro | Severity | Why (Source) | Test Focus | Solution | Status | REQ/SC |
|---------|-------------|--------|----------|--------------|------------|---------------------|--------|--------|
| RISK-XHD-01 | XHD / tích hợp (xuyên module) | Không có payload Kafka Order/Invoice Event, schema bảng, API Billing, enum trạng thái ⇒ không dựng được dữ liệu test và không định lượng được expected | High | DOC-v2.0-01 §D: "Chi tiết xem URD v2.1"; TP §2.3 GAP-07 | Mọi SC Integration; SC-XHD-024, 040, 101, 103 | Xin SDD / API spec / schema trước setup 23/10 (CL-XHD-29); chưa có thì verify định tính qua log + bảng `OB_*` | Open | SC-XHD-001..017, SC-XHD-040, SC-XHD-101, SC-XHD-103 · REQ-XHD-011, REQ-XHD-037 |
| RISK-XHD-02 | XHD / phát hành trùng | Worker và realtime chạy song song có khoảng trống giữa kiểm BillNumber và ghi BillNumber ⇒ 2 hóa đơn thật cho 1 dòng, nợ khách tính gấp đôi, GN trừ Paid 2 lần | High | DOC-v2.0-01 §D#2 (L662-665) | Tín hiệu đến sát giờ chốt cuối; bản tin lặp; SC-XHD-055, 056, 077 | Chờ phương án PM + SA (CL-XHD-23); exploratory R1 sát giờ chốt; hóa đơn dư xử lý ngoài phạm vi | Open | SC-XHD-055, SC-XHD-056, SC-XHD-077 · REQ-XHD-027 |
| RISK-XHD-03 | XHD / bản tin trễ qua ngày | Dòng có mốc nghiệp vụ ngày N nhưng bản tin về ngày N+1 rơi vào khoảng trống — không luồng nào phát hành; mail cảnh báo "bắt buộc" chưa có đặc tả | High | DOC-v2.0-01 §D#3 (L666-669) | SC-XHD-045 (ghi nhận hiện trạng) | Chờ CL-XHD-22; mail cảnh báo chưa sinh SC — nợ CHANGELOG §3 | Open | SC-XHD-045 · REQ-XHD-015, REQ-XHD-042 |
| RISK-XHD-04 | XHD / khóa chống trùng | Khóa chống trùng BR-XHD-08 (dịch vụ hóa đơn + gói) khác khóa map tín hiệu BR-DB-07 (ServiceCode + SubserviceType) và §C#3; SubServiceType 31 trùng ở 2 DV ⇒ dev và QC có thể dùng 2 khóa khác nhau, chặn nhầm hoặc phát hành trùng | High | DOC-v2.0-01 BR-XHD-08 (L419) ↔ §C#3 (L649-651) ↔ BR-DB-07 (L374) | SC-XHD-076..079, SC-XHD-028 | QC chốt khóa theo 2.2 (CL-XHD-11, 16/10/2026); còn field dữ liệu của khóa (CL-XHD-29) và SubServiceType 31 ở khóa map tín hiệu BR-DB-07 (CL-XHD-12) | Open | SC-XHD-076, SC-XHD-077, SC-XHD-078, SC-XHD-079 · REQ-XHD-027 |
| RISK-XHD-05 | XHD / kênh FPL | Lịch 2h, mốc 22:05, delay 2h, realtime sau 22h, thông tin KH 2 giờ đều mới ở 2.2 và thiếu mốc cụ thể ⇒ dễ lệch giữa dev / QC; vùng 18:00–22:00 khác kênh khác | High | DOC-v2.0-01 BR-XHD-01 (L386-388), BR-XHD-03 (L399), BR-XHD-06 (L414), BR-DB-03 (L356-358) | SC-XHD-031..034, SC-XHD-047..053 | Resolve CL-XHD-02..05 trước generate-tc; chỉnh lịch trên STG để chạy được nhiều mốc trong ngày | Open | SC-XHD-031..034, SC-XHD-047..053 · REQ-XHD-007, REQ-XHD-017, REQ-XHD-021, REQ-XHD-026 |
| RISK-XHD-06 | XHD / điều kiện PĐK + hợp đồng con | Rule mới; chưa biết trường nhận diện hợp đồng tổ chức, nguồn trạng thái PĐK, cách tính "2 ngày cuối tháng", đầu ra khi chặn ⇒ có thể chặn nhầm (không ra hóa đơn) hoặc bỏ lọt | High | DOC-v2.0-01 BR-XHD-03 (L400-401) | SC-XHD-061..068 (biên cuối tháng 28/30/31 ngày) | Resolve CL-XHD-07, 08, 09; chuẩn bị hợp đồng tổ chức / cá nhân / hợp đồng con trên STG | Open | SC-XHD-061..068 · REQ-XHD-022, REQ-XHD-023 |
| RISK-XHD-07 | XHD / thời gian | Nhiều SC phụ thuộc giờ chốt, cuối tháng, qua nửa đêm ⇒ khó tái hiện trên STG nếu không chỉnh được giờ hệ thống / tham số lịch | Medium | DOC-v2.0-01 BR-XHD-01 (L381-385); TP §3.2 | SC-XHD-041..046, 054..056, 063, 064 | Xác nhận với dev cách chỉnh tham số lịch + giờ hệ thống STG trước R1 | Open | SC-XHD-041..046, SC-XHD-054..056, SC-XHD-063, SC-XHD-064 · REQ-XHD-014..016 |
| RISK-XHD-08 | XHD / ma trận kênh × DV | 17 kênh × 20 nhóm × 2 loại đơn = 680 tổ hợp, không có ma trận kênh nào bán nhóm nào; mỗi kênh cần tài khoản / cách tạo đơn trên STG | Medium | DOC-v2.0-01 §A.2, §A.3; TP §2.3 GAP-62 | SC-XHD-001..017 | Xin ma trận thực bán (CL-XHD-26); ưu tiên Shopee/Tiktok (hồi quy) + FPL | Open | SC-XHD-001..017 · REQ-XHD-001, REQ-XHD-002 |
| RISK-XHD-09 | XHD / hồi quy Phase 1 | Chưa nhận URD v1.0 ⇒ không biết hành vi TMĐT nào giữ / đổi; "Có điều chỉnh ver2.0" không liệt kê điều chỉnh | Medium | DOC-v2.0-01 §A.2 (L133, L137), §A.4 #2 | SC-XHD-016, 017, 029, 060 | Xin URD v1.0 (CL-XHD-31); chưa có thì chỉ test theo URD 2.2 | Open | SC-XHD-016, SC-XHD-017, SC-XHD-029, SC-XHD-060 · REQ-XHD-005, REQ-XHD-020 |
| RISK-XHD-10 | XHD / cutover v1 → v2 | Đơn dở dang lúc go-live có thể bị bỏ sót hoặc phát hành lại; cơ chế theo URD 2.1 BR-DB-08 (kiểm tra chéo mức đơn hàng, mỗi bản tin một luồng); STG có luồng cũ để test chưa rõ. ⛔ Quét tay bổ sung đơn bị bỏ sót: ngoài scope test (TP §2.2 #8) | Medium | DOC-v2.0-01 §D#1 (L658-661) · DOC-v2.0-02 BR-DB-08 (L297-305) | SC-XHD-107, 108 | PM xác nhận STG có luồng cũ (CL-XHD-24); quét tay không test | Open | SC-XHD-107, SC-XHD-108 · REQ-XHD-041 |

> Risk ID format: `RISK-<MODULE>-<NN>` (vd `RISK-PV-01`). Severity = High / Medium / Low (có thể Medium-High).
> **Solution:** biện pháp giảm thiểu hoặc hướng xử lý cụ thể (vd "resolve C-XXX trước generate-tc", "thêm negative TC cho MSG", "defer tới khi có env"). Chưa có → `—` (nhưng High/Medium nên có).
> **Status** — trạng thái xử lý rủi ro. Enum THUẦN (không kèm ghi chú trong ô — lý do để ở cột `Solution`):
> - `Open` = chưa xử lý / **đang bị chặn** (env/API/BA/backend chưa sẵn → chưa cover được).
> - `Pending` = **chấp nhận + defer có chủ đích** (không xử ở version này; vd NFR chờ môi trường thật / tải lớn).
> - `Resolved` = **đã xử lý và thêm test case cover** rủi ro (có `Solution` + TC/SC khả thi).
> - `Closed` = **bỏ khỏi scope** (feature loại khỏi version → rủi ro không còn áp dụng).
> KHÔNG để trống. Vòng đời: `Open` → `Resolved` (khi đã cover) · `Open` → `Pending` (defer) · `→ Closed` (bỏ scope).

## Khuyến nghị tổng thể
1. **Resolve blocker clarifications trước generate-tc** các scenario liên quan: CL-XHD-21 (BR-XHD-18), CL-XHD-22 (mail cảnh báo), CL-XHD-29 (tài liệu tích hợp, gồm field khóa chống trùng của CL-XHD-11) — và nhóm FPL CL-XHD-02..05, nhóm PĐK CL-XHD-07, 08.
2. **Ưu tiên test P1 high-risk:** SC-XHD-041..043, 054..059, 061..063, 066, 067, 069..071, 073, 074, 076..078, 101..103, 105 (+ ma trận Shopee/Tiktok SC-XHD-016, 017).
3. **Performance / cần môi trường:** không có NFR; các SC thời gian (SC-XHD-041..046, 063, 064) cần chỉnh lịch / giờ STG — RISK-XHD-07.
4. **ID/text cleanup (non-blocking, cần trước automation):** cột "So với v2.1" ghi "Giữ nguyên" ở BR-XHD-01, 06, 08, 10 dù đã đổi (GAP-56); typo URD "SFP" (L326), "bên đưới" (L63), "thự hiện" (L452) — giữ nguyên trong quote.

## Clarifications (home CL — layout v2)

> 1 CL = 1 heading `### CL-XHD-NN · <câu hỏi ngắn>`. Dòng META mang `Status` (+ `⛔ BLOCKING` nếu chặn sinh TC / execute) và mã GAP tương ứng. Khi resolved: **thêm** đoạn `✅ RESOLVED <ngày> — <kết luận>`, giữ nguyên phần phân tích cũ.

### CL-XHD-01 · BR-DB-01 chỉ còn 2 sự kiện, nhưng BR khác vẫn cần "tạo đơn" và "cập nhật thông tin khách"
📍 `DOC-v2.0-01 BR-DB-01 (L345)` ↔ `BR-DB-03 (L359)` ↔ `BR-XHD-03 (L399)`  ·  Status: **Resolved 19/10/2026** · GAP-42 (Critical)

**BR-DB-01** — `DOC-v2.0-01 §I.c · L345`
> Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng.

**BR-DB-03 — dùng sự kiện không còn trong danh sách** — `L359`
> Cập nhật thông tin khách không kích hoạt phát hành hóa đơn; lần phát hành tiếp theo dùng thông tin mới nhất.

**BR-XHD-03 — mốc cần dữ liệu tạo đơn** — `L399`
> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

↳ **Ghi chú:** Doc tự mâu thuẫn. SC-XHD-020 giữ chỗ, Then chờ câu trả lời.

**Câu hỏi cho BA:** SPF còn đồng bộ sự kiện "tạo đơn" và "cập nhật thông tin khách hàng" sang INVOICE không? (Có / Không — nếu không thì dữ liệu tạo đơn và thông tin KH lấy từ đâu?)

🔎 **QC rà lại 16/10/2026:** QC đề nghị hỏi rõ hơn: SPF đồng bộ thông tin gì, vào lúc nào. Sau khi phát hành thì hóa đơn không cập nhật lại thông tin KH / đơn; nếu có đồng bộ trước khi phát hành thì đó chính là 2 sự kiện "tạo đơn" / "cập nhật thông tin KH". Flow §B.I.b (`DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png)) bước 1 chỉ ghi "Nhận đơn hàng và tín hiệu giao · BR-DB-01, 02" — không bổ sung sự kiện. ⇒ Vẫn Open. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** Trước khi phát hành hóa đơn, SPF có gửi sang INVOICE (a) bản tin khi đơn được **tạo** và (b) bản tin khi KH **sửa thông tin** (tên, MST, địa chỉ xuất hóa đơn…) không? Nếu không có (a): "thời gian tạo đơn" dùng cho delay 2h FPL (BR-XHD-03) lấy từ trường nào của bản tin thanh toán? Nếu không có (b): "thông tin mới nhất" của BR-DB-03 lấy từ đâu tại thời điểm phát hành?

✅ **RESOLVED 19/10/2026 (vòng 3)** — (a) SPF chỉ gửi 2 sự kiện **thanh toán** và **hủy đơn** (khác v2.1) — không có sự kiện tạo đơn / cập nhật thông tin khách. (b) Thông tin khách hàng trên hóa đơn lấy **từ hợp đồng** tại thời điểm phát hành (khách cập nhật thông tin thì hóa đơn phát hành sau dùng thông tin mới trên hợp đồng). (c) "Thời gian tạo đơn" (mốc delay 2h FPL) QC kiểm tra ở **Web admin** (thời gian tạo đơn hàng). SC-XHD-020 viết lại theo kết luận này. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-02 · FPL: khách không lấy hóa đơn, hoặc quá 2 giờ không nhập thì sao? "(ví dụ FPL)" có kênh khác không?
📍 `DOC-v2.0-01 BR-DB-03 · L356-358`  ·  Status: **Resolved 19/10/2026** · GAP-48 (Critical)

> Ngoại lệ: kênh bán FPL cho khách chọn có lấy hóa đơn hay không (ví dụ FPL).
> (...)
> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** 2 nhánh không có đầu ra. Theo quy định hóa đơn điện tử vẫn phải lập hóa đơn dù khách không lấy — suy diễn của analyst, cần xác nhận. Ảnh hưởng SC-XHD-032..034.

**Câu hỏi cho BA:** (1) Khách FPL chọn "không lấy hóa đơn" ⇒ INVOICE vẫn phát hành với thông tin hợp đồng hay không phát hành? (2) Quá 2 giờ không nhập ⇒ dùng thông tin hợp đồng? (3) Ngoại lệ chỉ áp FPL (10) hay còn kênh nào?

🟡 **Làm rõ một phần 16/10/2026** — Đã chốt (3): ngoại lệ chọn lấy / không lấy hóa đơn **chỉ áp kênh FPL (10)**; flow `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png) ghi "Kênh FPL: khách chọn lấy hóa đơn thì tự nhập thông tin trong tối đa 2 giờ" (không còn chữ "ví dụ"). Còn mở (1), (2); QC đề nghị hỏi rõ thao tác. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** Trên kênh FPL, khách chọn lấy / không lấy hóa đơn và nhập thông tin ở bước nào (lúc đặt đơn hay sau khi đặt), INVOICE nhận lựa chọn này qua trường nào? Với 2 tình huống: (1) khách chọn **không** lấy hóa đơn — INVOICE vẫn phát hành hóa đơn với thông tin hợp đồng, hay không phát hành? (2) khách chọn lấy hóa đơn nhưng **hết 2 giờ** vẫn chưa nhập — phát hành với thông tin hợp đồng, hay không phát hành?

✅ **RESOLVED 19/10/2026 (vòng 3)** — Thao tác FPL: sau khi tạo đơn và thanh toán thành công, khách vào web FPL › *Thông tin cá nhân › Quản lý thanh toán và gói › Xuất hóa đơn* › bấm **Xuất hóa đơn** ⇒ form nhập thông tin (có validate). Quá 2 giờ nút **Xuất hóa đơn bị ẩn**. Trong 2 giờ khách **không bấm** xuất hóa đơn ⇒ **không phát hành hóa đơn**. SC-XHD-032, 033, 034 hết chờ CL. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-03 · 7 trường khách FPL tự nhập: bắt buộc, định dạng, ai kiểm tra?
📍 `DOC-v2.0-01 BR-DB-03 · L357`  ·  Status: **Resolved 19/10/2026** · GAP-49 (Major)

> Nếu khách chọn lấy hóa đơn thì dùng thông tin khách tự nhập: tên, email, số điện thoại, mã số thuế, mã định danh, mã quan hệ ngân sách, số hộ chiếu.

↳ **Ghi chú:** Không có rule validate ⇒ `test_data_catalog.md` chỉ ghi được "có / rỗng". Nếu kênh FPL tự kiểm thì INVOICE chỉ nhận dữ liệu đã sạch.

**Câu hỏi cho BA:** Trường nào bắt buộc, định dạng (MST 10/13 số? email?), và INVOICE có validate lại hay tin dữ liệu kênh FPL gửi?

🔎 **QC rà lại 16/10/2026:** Theo logic, kênh FPL phải tự kiểm tra dữ liệu khách nhập; cần đội dự án hướng dẫn thao tác thực tế rồi mới chốt. ⇒ Vẫn Open. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** Xác nhận kênh FPL kiểm tra dữ liệu khách nhập và INVOICE không kiểm lại? Nếu đúng, cho QC quy tắc kiểm tra của kênh FPL (trường bắt buộc, định dạng MST / email / SĐT) và nhờ đội dự án FPL hướng dẫn thao tác nhập trên STG.

✅ **RESOLVED 19/10/2026 (vòng 3)** — Kênh FPL kiểm tra dữ liệu khách nhập. Hóa đơn **công ty**: bắt buộc tên công ty, địa chỉ, MST, email; mã đơn vị quan hệ ngân sách không bắt buộc. Hóa đơn **cá nhân**: bắt buộc họ và tên, địa chỉ, email; số hộ chiếu và mã định danh cá nhân **không bắt buộc**. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-04 · Mốc delay 2h của FPL: "thời gian tạo đơn" hay "thời điểm ghi nhận trên hệ thống của kênh"? Áp cho DV hay cả TB?
📍 `DOC-v2.0-01 BR-XHD-03 (L399)` ↔ `BR-DB-03 (L358)`  ·  Status: **Resolved 19/10/2026** · GAP-51 (Major)

**BR-XHD-03** — `L399`
> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

**BR-DB-03** — `L358`
> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** Hai mốc 2 giờ dùng 2 cách gọi khác nhau; nếu khác thời điểm thì có thể phát hành trước khi khách hết hạn nhập.

**Câu hỏi cho BA:** Hai mốc là một? Delay 2h áp cho dòng DV, TB hay cả hai?

🟡 **Làm rõ một phần 16/10/2026** — Đã chốt: **hai mốc 2 giờ là hai việc khác nhau.** BR-DB-03 (L358) = thời hạn khách nhập thông tin, tính từ thời điểm ghi nhận trên hệ thống của kênh. BR-XHD-03 (L399) = delay xét xuất hóa đơn, tính từ thời gian tạo đơn. Còn mở: delay áp DV, TB hay cả hai; và nếu 2 mốc gốc lệch nhau thì hóa đơn có thể ra trước khi khách hết hạn nhập. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** (1) Delay 2h xét xuất hóa đơn kênh FPL áp cho dòng DV, dòng TB hay cả hai? (2) "Thời điểm ghi nhận trên hệ thống của kênh" (mốc bắt đầu 2 giờ nhập thông tin) có trùng "thời gian tạo đơn" (mốc delay 2h) không? Nếu khác nhau, hóa đơn có thể phát hành khi khách vẫn còn thời gian nhập — khi đó dùng thông tin nào?

🟡 **Làm rõ thêm 19/10/2026 (vòng 3)** — "Thời điểm ghi nhận trên hệ thống của kênh" (mốc 2 giờ khách nhập thông tin) **trùng** "thời gian tạo đơn" (mốc delay 2h xét xuất hóa đơn) ⇒ hai mốc cùng gốc, không có trường hợp hóa đơn ra trước khi khách hết hạn nhập. Mốc kiểm tra ở Web admin (CL-XHD-01). SC-XHD-050 hết chờ mốc tính. Còn mở: delay 2h áp cho dòng **dịch vụ**, dòng **thiết bị** hay cả hai — câu trả lời vòng 3 chỉ chép lại câu hỏi. Nguồn: QC trả lời 19/10/2026 vòng 3.

✅ **RESOLVED 19/10/2026 (sau vòng 3)** — Delay 2 giờ xét xuất hóa đơn kênh FPL áp cho **cả dòng dịch vụ và dòng thiết bị**. Mốc = thời gian tạo đơn (Web admin), trùng thời điểm ghi nhận của kênh. SC-XHD-050 áp cả 2 loại dòng. Nguồn: QC owner 19/10/2026.

---

### CL-XHD-05 · Lịch FPL "2h quét 1 lần": các mốc chạy và giờ chốt cụ thể? Có là tham số?
📍 `DOC-v2.0-01 BR-XHD-01 · L386-388` ↔ `§A.1 #3 · L63`  ·  Status: **Open — đã rõ một phần 16/10/2026** · GAP-50 (Critical), GAP-52 (Minor)

> Xét riêng cho kênh bán FPL:
> 2h quét 1 lần
> Mốc 22:05 chốt từ 0h đến 22 giờ (Do FPL có rule delay 2h nên phải bổ sung khung giờ để quét hết những case không quét được do delay ở hai khung giờ trước)

**§A.1 #3 — mục tiêu nói lịch chung** — `L63`
> Xuất hóa đơn cho tất cả kênh bán liệt kê bên đưới và có đơn hàng SPF, dùng một lịch chung (giờ chốt và giờ chạy là tham số cấu hình) thay vì chia theo kênh và theo ngày thường / cuối tháng.

↳ **Ghi chú:** Không biết đợt đầu chạy lúc mấy giờ, mỗi đợt chốt tới đâu, "hai khung giờ trước" là khung nào. Mục tiêu §A.1 "không chia theo kênh" mâu thuẫn với lịch riêng FPL (GAP-52).

**Câu hỏi cho BA:** Liệt kê mốc chạy + giờ chốt của lịch FPL trong ngày; có cấu hình được như lịch chung không?

🟡 **Làm rõ một phần 16/10/2026** — QC nhờ rà lại BR-XHD-01. URD đã nói được:

**BR-XHD-01 — tiêu đề + phạm vi lịch chung** — `L379-380`
> Lịch xuất hóa đơn (tham số cấu hình)
> Dùng chung một lịch cho mọi ngày và mọi kênh bán khác FPL

**BR-XHD-06 — FPL** — `L414`
> Đối với Kênh bán FPL chỉ realtime từ sau mốc 22h

**Flow §B.I.b** — `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png) (ghi chú bước "Luồng worker / realtime")
> Giờ chốt, giờ chạy là tham số cấu hình (BR-XHD-01, 02, 06).

⇒ Đã rõ: FPL quét 2 giờ/lần; đợt cuối 22:05 chốt từ 0h–22h; sau 22h FPL chỉ realtime; giờ chốt / giờ chạy là tham số cấu hình. "Không chia theo kênh" ở §A.1 được L380 giới hạn lại ("kênh bán khác FPL") ⇒ GAP-52 không còn mâu thuẫn. **Còn mở:** giờ chạy các đợt trước 22:05, mỗi đợt chốt tới giờ nào, "hai khung giờ trước" là khung nào. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** BR-XHD-01 cho biết FPL quét 2 giờ/lần và đợt 22:05 chốt từ 0h–22h. Cần thêm: (1) các đợt trước 22:05 chạy lúc mấy giờ (vd 00:05, 02:05 … 20:05?) và mỗi đợt chốt dữ liệu tới giờ nào; (2) "hai khung giờ trước" trong câu L388 là 2 đợt nào; (3) ngoài phạm vi quét 0h–22h, đợt 22:05 còn khác các đợt 2 giờ thường ở điểm nào?

---

### CL-XHD-06 · Ngày cuối tháng, đủ điều kiện sau giờ chốt cuối: realtime phát hành ngay hay để sang tháng sau?
📍 `DOC-v2.0-01 BR-XHD-01 (L385)` ↔ `BR-XHD-06 (L413)`  ·  Status: **Resolved 16/10/2026** · GAP-43 (Critical)

**BR-XHD-01** — `L385`
> Đơn đủ điều kiện sau giờ chốt cuối của ngày cuối tháng sẽ phát hành sang tháng sau, ảnh hưởng kỳ ghi nhận doanh thu.

**BR-XHD-06** — `L413`
> Xử lý ngay khi nhận, không chờ đợt worker kế tiếp.

↳ **Ghi chú:** Nếu realtime chạy cả ngày cuối tháng thì câu L385 chỉ đúng cho dòng có tín hiệu về trước giờ chốt cuối nhưng chưa đủ điều kiện. TP đang giả định realtime vẫn chạy (SC-XHD-046).

**Câu hỏi cho BA:** Ngày cuối tháng, tín hiệu về sau giờ chốt cuối ⇒ realtime phát hành trong ngày (tháng này) hay dòng chờ sang tháng sau?

✅ **RESOLVED 16/10/2026** — Ngày cuối tháng, dòng đủ điều kiện **sau giờ chốt cuối** ⇒ **không phát hành trong tháng**, phát hành sang tháng sau — đúng câu BR-XHD-01 L385. Đây là ngoại lệ của realtime "xử lý ngay khi nhận" (BR-XHD-06 L413) cho ngày cuối tháng. QC lấy ví dụ: ngày cuối tháng, tới sau giờ chốt cuối mới đủ điều kiện ⇒ hóa đơn thuộc tháng sau. Nguồn: QC trả lời 16/10/2026 vòng 1. Phát sinh câu hỏi mới về đợt phát hành ở tháng sau → **CL-XHD-32**. SC-XHD-046 đổi Then.

---

### CL-XHD-07 · PĐK: nhận diện hợp đồng tổ chức, nguồn trạng thái PĐK, cách tính "2 ngày cuối tháng", duyệt muộn
📍 `DOC-v2.0-01 BR-XHD-03 · L400`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-44 (Critical), GAP-45 (Major), GAP-61 (Major)

> Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK; hai ngày cuối tháng không xét điều kiện này. Quên duyệt PĐK thì không autobill. Khi có thay đổi hoặc dịch chuyển luồng duyệt PĐK/hợp đồng thì phải hiệu chỉnh lại điều kiện này.

↳ **Ghi chú:** 4 điểm mở: (1) trường nào đánh dấu hợp đồng tổ chức (loại hình KH cấp 1?); (2) trạng thái PĐK lấy từ hệ thống nào; (3) "2 ngày cuối tháng" = 2 ngày lịch hay 2 ngày làm việc; (4) PĐK duyệt sau khi bị chặn thì đợt sau có phát hành. Thêm đơn **bán thêm** trên hợp đồng tổ chức đã duyệt PĐK: xét PĐK của lần nào (GAP-61). Ảnh hưởng SC-XHD-061..065, 068.

**Câu hỏi cho BA:** Trả lời 4 điểm trên + PĐK của đơn bán thêm.

🟡 **Làm rõ một phần 16/10/2026** — Đã chốt: (1) hợp đồng tổ chức = hợp đồng có **loại hình KH cấp 1 = Tổ chức**; (2) trạng thái PĐK **lấy từ SPF**; (3) "2 ngày cuối tháng" = **2 ngày lịch** cuối cùng của tháng. Còn mở: (4) duyệt PĐK muộn; PĐK của đơn bán thêm (GAP-61); trường SPF trả trạng thái PĐK. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** (1) hợp đồng tổ chức bị chặn vì chưa duyệt PĐK, sau đó PĐK được duyệt: đợt worker sau có phát hành không, hay "không autobill" nghĩa là phải xuất tay? (2) Đơn bán thêm trên hợp đồng tổ chức: xét PĐK của hợp đồng (đã duyệt từ lần bán mới) hay cần PĐK mới cho đơn bán thêm? (3) Trạng thái PĐK nằm ở trường nào trong dữ liệu SPF gửi sang?

🟡 **Làm rõ thêm 19/10/2026 (vòng 3)** — Hợp đồng tổ chức chưa duyệt PĐK ⇒ hệ thống **chặn** và ghi lỗi vào log; "không autobill" = **phải xuất hóa đơn tay** (xuất tay ngoài phạm vi TP) ⇒ hóa đơn bị chặn không tự phát hành ở đợt worker sau (SC-XHD-065, QC chỉ verify không phát hành). Quy tắc áp cho **cả đơn bán mới và đơn bán thêm**. Còn mở: đơn bán thêm xét PĐK của hợp đồng (đã duyệt từ lần bán mới) hay cần PĐK mới; trường trạng thái PĐK. Nguồn: QC trả lời 19/10/2026 vòng 3.

🟡 **Làm rõ thêm 19/10/2026 (sau vòng 3)** — Chuẩn bị dữ liệu PĐK: cập nhật tình trạng PĐK ở menu *Báo cáo phiếu đăng ký › Duyệt HD › Chuyển tình trạng PDK*; kiểm tra trạng thái PĐK ở *Web admin › Chi tiết đơn hàng › Thông tin khác › Thông tin duyệt đơn*. Phạm vi: **mỗi kênh bán test 1 hợp đồng doanh nghiệp** (tổ chức). Tool ghi ở `07_environments/environments.md`. Còn mở (duy nhất): đơn bán thêm trên hợp đồng tổ chức xét PĐK của hợp đồng (đã duyệt từ lần bán mới) hay cần PĐK mới. Nguồn: QC owner 19/10/2026.

---

### CL-XHD-08 · Hợp đồng con không phát hành: ghi nhận ra sao? Hợp đồng cha có phát hành hóa đơn thay?
📍 `DOC-v2.0-01 BR-XHD-03 · L401`  ·  Status: **Resolved 19/10/2026** · GAP-46 (Major)

> Hợp đồng con: nhận diện hợp đồng con khi hợp đồng có gắn hợp đồng cha (hợp đồng dự án). Không phát hành hóa đơn trên hợp đồng con, cả thiết bị và dịch vụ.

↳ **Ghi chú:** SC-XHD-066, 067 chỉ kiểm được "không phát hành". Không rõ có log, có cờ, hay dòng nằm tồn mãi.

**Câu hỏi cho BA:** Dòng của hợp đồng con được đánh dấu / log thế nào; hợp đồng cha có xuất hóa đơn thay không?

🟡 **Làm rõ một phần 16/10/2026** — Đã chốt cách nhận diện khi chuẩn bị dữ liệu: vào tool tình trạng kiểm tra hợp đồng; có thông tin hợp đồng cha ⇒ là hợp đồng con. Còn mở: dòng bị chặn được ghi nhận thế nào, hợp đồng cha có xuất hóa đơn thay không. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** Dòng DV / TB trên hợp đồng con bị chặn thì hệ thống ghi nhận thế nào (ghi log ở đâu, đánh cờ, hay để tồn)? Phần này có được xuất trên hóa đơn của hợp đồng cha (dự án) không, hay xuất theo quy trình khác?

✅ **RESOLVED 19/10/2026 (vòng 3)** — Sau khi tạo đơn, SPF gửi thông tin hợp đồng cho INVOICE; ở bước xét điều kiện phát hành, dòng thuộc **hợp đồng con của dự án bị chặn** và ghi lỗi vào log. QC không xem log ⇒ chỉ verify **không phát hành hóa đơn**. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-09 · Revision 2.2 ghi thêm "KH Chuỗi/Dự án" vào BR-XHD-03 nhưng BR không có nội dung
📍 `DOC-v2.0-01 Revision History 2.2 · L36` ↔ `BR-XHD-03 · L395-403`  ·  Status: **Resolved 16/10/2026** · GAP-47 (Major)

> [A]: Điều kiện duyệt PĐK, hợp đồng con, KH Chuỗi/Dự án (gộp vào BR-XHD-03); BR-XHD-18 (clear thuê thiết bị đầu cuối) theo email 24/09 và 30/09.

↳ **Ghi chú:** BR-XHD-03 chỉ có "hợp đồng dự án" trong câu hợp đồng con; không có gì về KH Chuỗi ⇒ có thể thiếu rule.

**Câu hỏi cho BA:** KH Chuỗi có rule phát hành riêng không? Nếu có, nội dung là gì?

✅ **RESOLVED 16/10/2026** — **KH Chuỗi không có rule phát hành riêng**: URD không mô tả nội dung nào. "Dự án" trong Revision History ứng với câu hợp đồng con / hợp đồng dự án đã có ở BR-XHD-03 L401. Không sinh SC. Nguồn: QC trả lời 16/10/2026 vòng 1. Nếu PO bổ sung rule cho KH Chuỗi ⇒ mở lại CL này.

---

### CL-XHD-10 · BR-XHD-04 (autobill TB theo phương thức) đã bỏ — bỏ hành vi hay chỉ bỏ câu chữ?
📍 `DOC-v2.0-01 §D#9 (L690-693)` ↔ `§A.5 #3 (L288-290)` ↔ `BR-XHD-03 (L397)`  ·  Status: **Resolved 16/10/2026** · GAP-54 (Major)

**Phụ lục D#9** — `L691-693`
> Autobill thiết bị theo phương thức triển khai (gom một lượt theo từng phương thức).
> BR-XHD-04
> Đã bỏ khỏi tài liệu.

**Thuật ngữ #3 — vẫn dùng** — `L290`
> Mỗi phương thức tương ứng một phiếu triển khai hoặc giao hàng và là đơn vị autobill của thiết bị.

↳ **Ghi chú:** D#9 ghi BR-XHD-04 "đã bỏ" nhưng thuật ngữ #3 vẫn gọi phương thức là "đơn vị autobill của thiết bị" ⇒ không rõ phát hành toàn bộ TB của phương thức hay chỉ TB có trong tín hiệu (SC-XHD-059).

**Câu hỏi cho BA:** Khi nhận tín hiệu giao hàng của một phương thức, INVOICE phát hành toàn bộ TB thuộc phương thức đó hay chỉ TB có trong tín hiệu?

✅ **RESOLVED 16/10/2026** — Khi nhận tín hiệu giao hàng của một phương thức, INVOICE **chỉ phát hành TB có trong tín hiệu**, không phát hành toàn bộ TB của phương thức. Căn cứ: BR-XHD-06 L412; tín hiệu map vào từng TB theo khóa có SubserviceType + phương thức (BR-DB-07 L374); flow `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png) ghi "realtime tách theo tín hiệu". Nguồn: QC trả lời 16/10/2026 vòng 1. Thêm **SC-XHD-110**.

---

### CL-XHD-11 · Khóa chống trùng chốt theo bản nào, gồm field nào?
📍 `DOC-v2.0-01 BR-XHD-08 (L419)` ↔ `§C#3 (L649-651)` ↔ `BR-DB-07 (L374)`  ·  Status: **Open — đã rõ một phần 16/10/2026, hết BLOCKING** · GAP-41 (Critical), GAP-56 (Major)

**URD 2.2 BR-XHD-08** — `L419, L422`
> Khóa xác định dòng: dịch vụ = mã đơn hàng + dịch vụ hóa đơn + Gói dịch vụ; thiết bị thêm phương thức triển khai.
> (...)
> Giữ nguyên

**URD 2.2 §C#3 — vẫn nói khóa dùng SubServiceType** — `L651`
> Khóa chống trùng có dùng SubServiceType nên có thể làm hai dòng bị coi là trùng.

↳ **Ghi chú:** 2.2 đổi khóa nhưng ghi "Giữ nguyên"; §C#3 và BR-DB-07 vẫn theo khóa cũ. "Dịch vụ hóa đơn" và "Gói dịch vụ" ứng với field nào trong dữ liệu chưa rõ. Theo quy tắc 2.2 thắng, TP giả định theo text 2.2. ⛔ Không sinh TC chi tiết dữ liệu khóa cho SC-XHD-076..079 tới khi trả lời.

**Câu hỏi cho BA:** Khóa chống trùng chốt theo BR-XHD-08 (mã đơn + dịch vụ hóa đơn + gói dịch vụ [+ phương thức]) hay có dùng SubServiceType như §C#3? Field tương ứng là gì?

🟡 **Làm rõ một phần 16/10/2026** — Đã chốt **theo URD 2.2** (L419): DV = mã đơn hàng + dịch vụ hóa đơn + gói dịch vụ; TB thêm phương thức triển khai. Câu §C#3 L651 ("khóa chống trùng có dùng SubServiceType") hết hiệu lực với chống trùng. Khóa **map tín hiệu** BR-DB-07 L374 (có SubserviceType) là khóa khác, giữ nguyên. Còn mở: field dữ liệu của "dịch vụ hóa đơn" và "gói dịch vụ" — cần schema (CL-XHD-29). Hết BLOCKING: SC-XHD-076..078 viết được TC theo khóa 2.2, chỉ phần field cụ thể của dữ liệu test chờ schema. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** "Dịch vụ hóa đơn" và "Gói dịch vụ" trong khóa chống trùng BR-XHD-08 ứng với cột nào trong dữ liệu đơn (bảng chi tiết đơn: ServiceCode? mã gói? SubServiceType?)

---

### CL-XHD-12 · SubServiceType 31 trùng ở 2 dịch vụ Tổng đài Oncall
📍 `DOC-v2.0-01 §A.3 (L191-192, L259)` + `§C#3 (L649-651)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · §C#3 của URD

> 31 – Thiết bị Oncall (Type 2)
> 31 – Thiết bị IP phone (Type 2)
> (...)
> Ô màu vàng: SubServiceType 31 trùng ở hai dịch vụ (Thiết bị Oncall, Thiết bị IP phone) của nhóm Tổng đài Oncall.

↳ **Ghi chú:** Doc tự đưa vào điểm cần xác nhận. Nếu khóa còn dùng SubServiceType (CL-XHD-11) thì đơn có cả 2 TB này sẽ chỉ ra hóa đơn cho 1 dòng (SC-XHD-079).

**Câu hỏi cho BA:** SubServiceType của "Thiết bị IP phone" có phải 31 thật không, hay danh mục nhập sai?

🔎 **QC rà lại 16/10/2026:** QC xác nhận có dịch vụ "Thiết bị IP phone", nhưng chưa ai xác nhận SubServiceType 31 có đúng không. Vì khóa chống trùng đã chốt theo 2.2 (CL-XHD-11), rủi ro chuyển sang **khóa map tín hiệu BR-DB-07** (vẫn có SubserviceType): tín hiệu giao của Thiết bị Oncall có thể khớp nhầm dòng Thiết bị IP phone. ⇒ Vẫn Open. Nguồn: QC trả lời 16/10/2026 vòng 1

**Câu hỏi cho BA (vòng 2):** SubServiceType của "Thiết bị IP phone" đúng là 31 (trùng "Thiết bị Oncall") không? Nếu đúng, tín hiệu giao hàng map theo mã đơn + ServiceCode + SubserviceType + phương thức (BR-DB-07) phân biệt 2 thiết bị này bằng gì?

🟡 **Làm rõ một phần 19/10/2026 (vòng 3)** — SubServiceType của "Thiết bị IP phone" **đúng là 31**, trùng "Thiết bị Oncall". Còn mở: tín hiệu giao hàng map theo mã đơn + ServiceCode + SubserviceType + phương thức (BR-DB-07) phân biệt 2 thiết bị bằng gì — QC hỏi lại BA. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-13 · Ý nghĩa cột Type 1–4 và quan hệ với ProductType DV/TB
📍 `DOC-v2.0-01 §C#2 · L644-647`  ·  Status: **Open** · §C#2 của URD

> Ý nghĩa cột Type (1 đến 4) của dịch vụ và cách map với ProductType (DV/TB).
> Mục A.3, BR-DB-04
> Danh sách dịch vụ ghi Type từ 1 đến 4, chưa có mô tả ý nghĩa.

↳ **Ghi chú:** Suy diễn của analyst từ tên dịch vụ: Type 1 = Basic/cước chính, Type 2 = thiết bị, Type 3 = Extra/dịch vụ cộng thêm, Type 4 = triển khai. Nếu đúng thì Type 2 ⇔ TB, còn lại DV — nhưng "Đặt cọc thuê bao (Type 3)" và "Triển khai (Type 4)" là DV hay TB thì không suy được. INVOICE không suy diễn (BR-DB-04) nên ảnh hưởng chủ yếu là **dữ liệu test**.

**Câu hỏi cho BA:** Xác nhận nghĩa Type 1–4 và với mỗi Type thì SPF gắn ProductType gì.

🔎 **QC rà lại 16/10/2026:** Ghi chú của QC: danh sách dịch vụ được map theo ServiceID giữa bảng dịch vụ và bảng nhóm dịch vụ (55 dòng, 20 nhóm); đã loại ServiceID 2 và 22; SubServiceType 31 trùng ở 2 dịch vụ nhóm Tổng đài Oncall; **cột Type (1–4) chưa có bảng mô tả ý nghĩa, cần PO xác nhận.** ⇒ Vẫn Open, chuyển PO. Nguồn: QC trả lời 16/10/2026 vòng 1

---

### CL-XHD-14 · "Hợp đồng có hiệu lực" và "đang cập nhật" là những giá trị trạng thái nào?
📍 `DOC-v2.0-01 BR-XHD-10 · L425-426`  ·  Status: **Resolved 19/10/2026** · GAP-13 (Critical)

> Đơn không ở trạng thái hủy hoặc đang cập nhật.
> Thông tin chung phải đủ: hợp đồng có hiệu lực, Sale Team, Sale Channel, tên khách hàng, loại hình khách hàng cấp 1 và cấp 2, địa chỉ xuất hóa đơn, LocationID > 0.

↳ **Ghi chú:** Cần enum trạng thái đơn + hợp đồng để dựng SC-XHD-081, 082 (TP giả định theo v1.0).

**Câu hỏi cho BA:** Liệt kê trạng thái đơn = "đang cập nhật" và trạng thái hợp đồng = "có hiệu lực".

🔎 **QC rà lại 16/10/2026:** Không tìm thấy mô tả trong tài liệu nào (URD 2.2, flow `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png)) ⇒ gap tài liệu, vẫn Open, chuyển PO. Nguồn: QC trả lời 16/10/2026 vòng 1

🟡 **Làm rõ một phần 19/10/2026** — Trạng thái hợp lệ: **đơn hàng = "Bình thường"** và **hợp đồng = "Bình thường"** (= "có hiệu lực"). Còn mở: danh sách giá trị trạng thái **bị chặn** (hủy, đang cập nhật, …) để dựng case âm SC-XHD-080..082. Nguồn: QC trả lời 19/10/2026 vòng 2.

✅ **RESOLVED 19/10/2026 (vòng 3)** — Case âm cần có: trạng thái **hợp đồng** không hợp lệ: **Tạm ngưng**, **Đã chấm dứt**, **Ngưng vì lý do thanh toán**… (SC-XHD-082); trạng thái **đơn hàng** không hợp lệ: **Đã hủy** (SC-XHD-080) và **Đang cập nhật** = đơn chưa có thông tin hợp đồng (SC-XHD-081, QC owner giữ). Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-15 · Log khi không hợp lệ: ghi ở đâu, nội dung gì, thứ tự validate, nhiều lỗi cùng lúc? Đơn không có khuyến mãi?
📍 `DOC-v2.0-01 BR-XHD-10 · L427-428`  ·  Status: **Resolved 19/10/2026** · GAP-29 (Major), GAP-30 (Major)

> Chi tiết từng dịch vụ phải có các ID dịch vụ, nhóm dịch vụ, gói dịch vụ, chính sách, câu lệnh giá, chương trình khuyến mãi > 0.
> Không hợp lệ thì không phát hành và ghi log; hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

↳ **Ghi chú:** 14 SC negative (SC-XHD-080..095) chỉ kiểm được "có log". Đơn không có chương trình khuyến mãi thì ID KM = 0? ⇒ theo chữ URD sẽ bị chặn.

**Câu hỏi cho BA:** (1) Log ghi bảng / cột nào, format? (2) Thứ tự kiểm, có log tất cả lỗi hay dừng ở lỗi đầu? (3) Đơn không có KM thì ID KM mang giá trị gì và có bị chặn không?

🔎 **QC rà lại 16/10/2026:** Không tìm thấy mô tả trong tài liệu nào (URD 2.2, flow `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png)) ⇒ gap tài liệu, vẫn Open, chuyển PO. Nguồn: QC trả lời 16/10/2026 vòng 1

🟡 **Làm rõ một phần 19/10/2026** — (1) QC **không có quyền xem log** ⇒ không verify nội dung / vị trí log, chỉ verify không phát hành. Điều kiện chi tiết dịch vụ xem trên **Web admin** (ID dịch vụ, nhóm DV, gói DV, chính sách, câu lệnh giá, CTKM > 0). Còn mở: (2) thứ tự validate; (3) đơn **không có KM** — theo chữ "chương trình khuyến mãi > 0" sẽ bị chặn, cần BA xác nhận (SC-XHD-095). Nguồn: QC trả lời 19/10/2026 vòng 2.

✅ **RESOLVED 19/10/2026 (vòng 3)** — (2) Kiểm tra điều kiện **dừng ở lỗi đầu tiên**. (3) Đơn **không có chương trình khuyến mãi vẫn phát hành** hóa đơn ⇒ điều kiện "CTKM > 0" chỉ xét khi đơn có CTKM; SC-XHD-095 sửa Then. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-16 · Job cảnh báo 15 phút: điều kiện, kênh gửi, người nhận, nội dung?
📍 `DOC-v2.0-01 BR-XHD-10 · L429`  ·  Status: **Open** · GAP-31 (Critical)

> Job cảnh báo chạy 15 phút một lần để bổ sung thông tin kịp trước giờ chốt.

↳ **Ghi chú:** Nằm trong BR in-scope nhưng không có đặc tả — SC-XHD-097 để P3.

**Câu hỏi cho BA:** Job cảnh báo những dòng nào, gửi qua kênh nào (mail?), cho ai, nội dung gì? Có thuộc v2.0 không?

🔎 **QC rà lại 16/10/2026:** Không tìm thấy mô tả trong tài liệu nào (URD 2.2, flow `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png)) ⇒ gap tài liệu, vẫn Open, chuyển PO. Nguồn: QC trả lời 16/10/2026 vòng 1

---

### CL-XHD-17 · Dòng không hợp lệ được bổ sung thông tin: đợt sau có phát hành?
📍 `DOC-v2.0-01 BR-XHD-10 (L428)`  ·  Status: **Resolved 16/10/2026** · GAP-55 (Major)

**URD 2.2** — `L428`
> Không hợp lệ thì không phát hành và ghi log; hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

↳ **Ghi chú:** "Không giữ chờ" không nói rõ dòng bị chặn còn được phát hành ở đợt sau không (SC-XHD-096).

**Câu hỏi cho BA:** Dòng bị chặn vì thiếu thông tin, sau đó được bổ sung: đợt sau có phát hành không?

✅ **RESOLVED 16/10/2026** — **Theo URD 2.2**: dòng bị chặn chỉ còn cơ hội phát hành **trong cùng ngày**. Đợt worker sau quét "dòng chưa xuất hóa đơn có mốc nghiệp vụ trong ngày" (L384), và job cảnh báo 15 phút tồn tại để "bổ sung thông tin kịp trước giờ chốt" (L429). Qua ngày thì hệ thống không tự phát hành lại (L428). Nguồn: QC trả lời 16/10/2026 vòng 1. SC-XHD-096 đổi Then; thêm **SC-XHD-111**.

---

### CL-XHD-18 · Billing lỗi / timeout: hệ thống làm gì?
📍 `DOC-v2.0-01 BR-XHD-13 · L439`  ·  Status: **Resolved 19/10/2026** · GAP-14 (Critical)

> Phát hành qua Billing System, ghi BillNumber và BillDate vào giỏ tồn xuất hóa đơn

↳ **Ghi chú:** Không có nhánh lỗi. TP giả định giữ BillNumber rỗng + log (SC-XHD-104).

**Câu hỏi cho BA:** Retry? Giữ rỗng chờ đợt sau? Cảnh báo?

🔎 **QC rà lại 16/10/2026:** Không tìm thấy mô tả trong tài liệu nào (URD 2.2, flow `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png)) ⇒ gap tài liệu, vẫn Open, chuyển PO. Nguồn: QC trả lời 16/10/2026 vòng 1

✅ **RESOLVED 19/10/2026 (vòng 3)** — Billing lỗi / timeout: hệ thống **ghi lỗi**, **dev retry bằng tay** (không có retry tự động). QC không xem log ⇒ SC-XHD-104 verify hóa đơn **không phát hành** (BillNumber rỗng). Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-19 · Cột Note: thuộc bảng nào, format log tín hiệu giao hàng?
📍 `DOC-v2.0-01 BR-DB-07 · L375`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-27 (Major)

> Nếu thiết bị đã có hóa đơn hoặc không khớp khóa thì không ghi nhận, chỉ ghi log nội dung tín hiệu vào cột Note.

↳ **Ghi chú:** SC-XHD-026..028 chỉ kiểm định tính.

**Câu hỏi cho BA:** Cột Note ở bảng nào, ghi những trường gì của tín hiệu, có ghi lý do (đã có hóa đơn / không khớp) không?

🟡 **Làm rõ một phần 19/10/2026** — QC **không có quyền xem log** ⇒ không verify cột Note; SC-XHD-026..028 chỉ verify hành vi (không ghi nhận / không phát hành). Còn mở: chỉ để thông tin, không chặn TC. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-XHD-20 · Bản tin Order Event lỗi giải mã / thiếu trường
📍 `DOC-v2.0-01 §I.a Trigger · L332` *(derived from omission — URD không nói)*  ·  Status: **Resolved 19/10/2026** · GAP-26 (Major)

> Sự kiện đơn hàng từ SPF; tín hiệu giao hàng hoàn tất; worker chạy theo lịch (BR-XHD-01).

↳ **Ghi chú:** URD 2.2 không có nhánh lỗi khi nhận / giải mã bản tin. Chưa sinh SC.

**Câu hỏi cho BA:** Bản tin không giải mã được / thiếu trường bắt buộc thì bỏ qua + log, hay dừng consumer?

🔎 **QC rà lại 16/10/2026:** URD 2.2 không mô tả ⇒ gap tài liệu, vẫn Open, chuyển PO. Nguồn: QC trả lời 16/10/2026 vòng 1

✅ **RESOLVED 19/10/2026** — Đơn hàng luôn có đủ thông tin bắt buộc ⇒ **không dựng case** bản tin lỗi giải mã / thiếu trường; nếu xảy ra trên STG thì log bug. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-XHD-21 · BR-XHD-18 "clear thuê thiết bị đầu cuối": có thuộc v2.0? Đặc tả? ⛔ BLOCKING
📍 `DOC-v2.0-01 BR-XHD-18 · L449-452`  ·  Status: **Open — ⛔ BLOCKING** · GAP-53 (Blocker)

> Bổ sung chức năng cho phép DVKH HO chủ động xử lý với hợp đồng có yêu cầu clear nội dung "thuê thiết bị đầu cuối" trên hóa đơn.
> Mới (kịp plan các chức năng chính sẽ thự hiện)

**Ảnh màn hình hiện hữu — có sẵn cột cùng tên** — `DOC-v2.0-FIG-02` (ảnh: Danh sách hóa đơn của Hợp đồng.png) màn "LIỆT KÊ CƯỚC CỦA THUÊ BAO" · tiêu đề cột cuối bảng
> Clear thiết bị đầu cuối

↳ **Ghi chú:** Có thể có UI (duy nhất trong URD). Màn "Liệt kê cước" của Hệ thống Thông tin (FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png)) **đã có cột "Clear thiết bị đầu cuối"** cạnh "Hóa đơn điều chỉnh giảm", "Hóa đơn thay thế", "Gen hóa đơn" ⇒ **suy diễn của analyst:** BR-XHD-18 có thể là thao tác trên màn này, nhưng URD không nói. REQ-XHD-039 chưa có SC.

**Câu hỏi cho BA:** Chức năng này thuộc v2.0 không? Nếu có: có phải cột "Clear thiết bị đầu cuối" trên màn Liệt kê cước (FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png)) không; input, kết quả trên hóa đơn (hóa đơn mới / điều chỉnh / chỉ đổi nội dung dòng?).

🔎 **Bổ sung 16/10/2026 từ flow §B.I.b** — `DOC-v2.0-FIG-03` (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png), bước "Phát hành hóa đơn · BR-XHD-13, 14, 18" (ô tô màu = "Nội dung mới, đã sửa hoặc cần xác nhận"):
> DVKH HO clear được "thuê TB đầu cuối".

↳ Flow v2.0 đã đặt BR-XHD-18 trong luồng phát hành và ghi rõ đây là nội dung cần xác nhận ⇒ phần "thuộc v2.0" coi như có, nhưng vẫn chưa có đặc tả ⇒ giữ ⛔ BLOCKING cho REQ-XHD-039.

**Câu hỏi cho BA (vòng 2):** Flow v2.0 đã đưa BR-XHD-18 vào bước phát hành. Cần đặc tả: DVKH HO thao tác ở đâu (màn / tool nào; có phải cột "Clear thiết bị đầu cuối" trên màn Liệt kê cước — FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png) không), trước hay sau khi phát hành, và kết quả trên hóa đơn (bỏ dòng "thuê thiết bị đầu cuối" / đổi nội dung / lập hóa đơn điều chỉnh)?

---

### CL-XHD-22 · Mail cảnh báo bản tin trễ qua ngày + phương án xử lý: thuộc v2.0? Đặc tả? ⛔ BLOCKING
📍 `DOC-v2.0-01 §D#3 · L666-669`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-02 (Blocker), GAP-11 (Critical)

> Bản tin đồng bộ về chậm qua ngày, dòng không được luồng nào xử lý.
> RISK-01
> PM và SA xử lý; mail cảnh báo là yêu cầu bắt buộc đã thống nhất.

↳ **Ghi chú:** Phụ lục ghi "không cần PO confirm" nhưng là "yêu cầu bắt buộc". REQ-XHD-042 chưa có SC; SC-XHD-045 chỉ ghi nhận hiện trạng.

**Câu hỏi cho BA:** Mail cảnh báo có trong v2.0? Điều kiện phát hiện, lịch gửi, người nhận, nội dung? Phương án xử lý dòng trễ đã chốt chưa?

🟡 **Làm rõ một phần 19/10/2026** — Theo `DOC-v2.0-02` RISK-01 (L428-442): dòng có mốc nghiệp vụ ngày N nhưng bản tin về ngày N+1 **không được worker lẫn realtime xử lý** (SC-XHD-045 giữ nguyên); xuất bổ sung là case-by-case (ngoài phạm vi TP); **mail cảnh báo là yêu cầu bắt buộc** — L436 *"Cần có hệ thống MAIL CẢNH BÁO để phát hiện các dòng rơi vào tình huống này. Đây là yêu cầu bắt buộc, không phụ thuộc phương án kỹ thuật được chọn."* ⇒ mail thuộc phạm vi v2.0. Còn mở (**vẫn BLOCKING** cho REQ-XHD-042): điều kiện phát hiện, lịch gửi, người nhận, nội dung mail; phương án kỹ thuật (mở rộng phạm vi quét / xuất bổ sung có kiểm soát) PM + SA chưa chốt. Nguồn: QC trả lời 19/10/2026 vòng 2 (dùng URD 2.1 cho Phụ lục D, QC owner chốt 19/10/2026).

---

### CL-XHD-23 · Phương án chặn phát hành trùng worker ↔ realtime
📍 `DOC-v2.0-01 §D#2 · L662-665`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-12 (Critical)

> Rủi ro phát hành hóa đơn trùng khi worker và realtime chạy song song.
> BR-XHD-09
> PM và SA chốt phương án kỹ thuật.

↳ **Ghi chú:** RISK-XHD-02. Không có phương án ⇒ không biết expected khi 2 luồng tranh nhau.

**Câu hỏi cho BA:** Phương án đã chốt? Ngày có trên STG?

🟡 **Làm rõ một phần 19/10/2026** — Theo `DOC-v2.0-02` BR-XHD-09 (L370-378): race worker ↔ realtime là rủi ro đã biết (khoảng trống giữa kiểm `BillNumber IS NULL` và ghi BillNumber); ràng buộc L377 *"ưu tiên bảo đảm hóa đơn luôn được phát hành — cơ chế chặn trùng không được dẫn tới tình huống không ra được hóa đơn."* Còn mở: 2.1 vẫn ghi L378 *"[NỢ] Chờ PM và SA thống nhất phương án kỹ thuật"* ⇒ chưa có phương án / ngày lên STG — hỏi PM, SA. Hóa đơn dư khi trùng: ngoài phạm vi (TP). Nguồn: QC trả lời 19/10/2026 vòng 2 (dùng URD 2.1 cho Phụ lục D, QC owner chốt 19/10/2026).

🟡 **Ghi nhận 19/10/2026 (vòng 3)** — QC nhắc lại: xử lý hóa đơn dư khi trùng **không test** (quy trình điều chỉnh / thay thế riêng, ngoài phạm vi TP). Chưa trả lời: PM / SA đã chốt phương án chặn trùng worker ↔ realtime chưa; có test worker và realtime chạy song song không. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-24 · Cutover v1 → v2: có test trên STG không? Dữ liệu luồng cũ?
📍 `DOC-v2.0-01 §D#1 · L658-661`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-32 (Major)

> Chuyển đổi hệ thống v1 sang v2 (cutover, giai đoạn giao thoa, quét tay bổ sung).
> BR-DB-08
> PM, SA

↳ **Ghi chú:** TP giữ FR06 (P2, 18 TC). Out-scope ⇒ SC-XHD-107, 108 chuyển DEPRECATED và RISK-XHD-10 → Closed.

**Câu hỏi cho BA:** Cutover có nằm trong phạm vi QC v2.0? Nếu có: STG có dữ liệu + service luồng cũ không?

🟡 **Làm rõ một phần 19/10/2026** — Theo `DOC-v2.0-02` BR-DB-08 (L297-305): v2.0 ghi hoàn toàn vào bảng mới, tắt service cũ khi go-live; mỗi bản tin Kafka chỉ một luồng xử lý (L300); giai đoạn giao thoa luồng mới kiểm tra chéo dữ liệu cũ **mức đơn hàng** — đơn đã ra hóa đơn ở luồng cũ thì luồng mới bỏ qua (L302); kiểm tra chéo là cấu hình bật / tắt. ⇒ **SC-XHD-107, 108 dùng lại** (bỏ deprecated). Quét tay bổ sung: ngoài phạm vi (TP). Còn mở: STG có dữ liệu + service luồng cũ để test không. Nguồn: QC trả lời 19/10/2026 vòng 2 (dùng URD 2.1 cho Phụ lục D, QC owner chốt 19/10/2026).

🟡 **Ghi nhận 19/10/2026 (vòng 3)** — QC nhắc lại: quét tay bổ sung đơn bỏ sót giai đoạn giao thoa cutover **không test** (thao tác tay, ngoài phạm vi TP). Chưa trả lời: STG có dữ liệu + service luồng cũ để test kiểm tra chéo (SC-XHD-107, 108) không; ai bật cấu hình. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-25 · Đơn bán thêm: rule áp chung, hay có điểm khác?
📍 `DOC-v2.0-04 mail PM · dòng 3` ↔ `DOC-v2.0-01 (toàn bộ BR — không có từ "bán thêm")`  ·  Status: **Resolved 19/10/2026** · GAP-60 (Major)

> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** Ảnh hưởng ≥7 chức năng (XHD F01, F04, F06; GN F17; HK F19, F23; F27). Điểm có thể khác: PĐK (CL-XHD-07), cọc (CL-GN-07), ký hiệu hóa đơn (CL-HK-01), tiền trả trước (CL-HK-07).

**Câu hỏi cho BA:** Mọi BR áp chung cho đơn bán thêm? Nếu không, liệt kê điểm khác.

✅ **RESOLVED 19/10/2026** — Mọi BR **áp dụng chung cho bán mới và bán thêm**, không có điểm khác. SC-XHD-106 đổi Then. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-XHD-26 · Ma trận kênh × nhóm DV × loại đơn thực bán
📍 `DOC-v2.0-01 §A.2 (L80)` + `§A.3 (L139)` + `BR-XHD-12 (L435)`  ·  Status: **Resolved 19/10/2026** · GAP-62 (Major)

> Tất cả kênh bán trong danh sách dưới đây thuộc phạm vi. Phase 1 đã triển khai Shopee và Tiktok.
> (...)
> Chi nhánh nào được bán sản phẩm dịch vụ nào do bên quản lý sản phẩm bổ sung thuộc tính, nằm ngoài URD này.

↳ **Ghi chú:** SC-XHD-001..017 giả định mọi kênh bán mọi nhóm. Mỗi cặp không bán bớt 2 TC (TP §2.3).

**Câu hỏi cho BA:** Gửi ma trận kênh × nhóm DV × {bán mới, bán thêm} thực bán; cặp nào không bán thì bỏ khỏi phạm vi test.

⛔ **Ngoài scope test 19/10/2026** — câu *"Chi nhánh nào được bán sản phẩm dịch vụ nào do bên quản lý sản phẩm bổ sung thuộc tính"* thuộc **TP §2.2 #4** *"Thuộc tính chi nhánh nào được bán sản phẩm / dịch vụ nào"* ⇒ không sinh SC, không kiểm thuộc tính này. QC owner 19/10/2026. Câu hỏi ma trận kênh × nhóm DV vẫn giữ (phạm vi FR01).

✅ **RESOLVED 19/10/2026 (vòng 3)** — QC lead chốt: viết TC **bán mới và bán thêm cho từng nhóm dịch vụ, cho từng kênh bán** (không cắt cặp nào khỏi phạm vi). Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-27 · Danh mục HT triển khai (DOC-v2.0-05): map sang 3 nguồn tín hiệu; TB "Không" phát hành thế nào?
📍 `DOC-v2.0-05 sheet "1. HT Triển khai" · STT 1, 8` ↔ `DOC-v2.0-01 BR-DB-02 (L349)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · *mới — phát hiện khi analyze 16/10/2026, chưa có GAP*

**DOC-v2.0-05 — STT 8** — cột D
> - Phiếu thi công: triển khai bởi TINPNC nếu hàng hóa có mix HT "Không" và "TIN/PNC"
> - None: không đẩy triển khai, giao hàng nếu hàng hóa, dịch vụ trên đơn hàng chỉ có "Không"

**DOC-v2.0-05 — STT 1** — cột G
> Đơn hàng có ít nhất 1 SPDV có mix HT Triển khai TIN/PNC và Quầy/ Sales --> auto xử lý theo luồng triển khai TINPNC

**URD 2.2 BR-DB-02** — `L349`
> Tín hiệu đi thẳng về INVOICE từ 3 nguồn độc lập: phiếu thi công (tình trạng "Đã xử lý hoàn tất"), Vendor (khi đối tác giao xong), phiếu giao tại quầy.

↳ **Ghi chú:** File bổ sung có 8 hình thức, URD chỉ nói 3 nguồn. (1) TB DeployType "Không" ⇒ không có phiếu ⇒ không có tín hiệu ⇒ theo BR-XHD-03 không bao giờ phát hành. (2) Đơn mix TIN/PNC + Quầy gộp sang TINPNC ⇒ phương thức trong khóa (BR-DB-07, BR-XHD-08) là gì. (3) File chưa có version/ngày, chưa rõ là tài liệu chính thức hay tham khảo.

**Câu hỏi cho BA:** (1) TB "Không" xuất hóa đơn theo đường nào? (2) Đơn mix: tín hiệu mang phương thức nào? (3) File này có phải danh mục chính thức của v2.0 không?

🟡 **Làm rõ một phần 19/10/2026** — (1) TB / DV hình thức triển khai **"Không"** vẫn xuất hóa đơn **khi đơn hàng hoàn tất** — chưa có căn cứ URD, tách câu hỏi sang **CL-XHD-34**. Còn mở: (2) câu trả lời đơn mix bị cắt dở ("…hình thức Phiếu thi công:"); (3) file HT triển khai có phải danh mục chính thức không. Nguồn: QC trả lời 19/10/2026 vòng 2.

🟡 **Làm rõ thêm 19/10/2026 (vòng 3)** — File "List HT Triển khai" (AnhNQ75, DOC-v2.0-05) là **danh mục chính thức của PO** (QC ghi "File List HT Triển khai (AnhNQ75) có phải danh mục chính thức của PO" — analyst hiểu là khẳng định). Còn mở (duy nhất): đơn mix hình thức triển khai — tín hiệu giao hàng mang phương thức nào trong khóa map (BR-DB-07). Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-28 · Ảnh màn Hệ thống Thông tin (DOC-v2.0-FIG-01 (ảnh: Chi tiết hóa đơn.png), FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png)) vẫn hiện "Từ ngày / Đến ngày" — 2 màn này dùng để verify?
📍 `DOC-v2.0-FIG-01 (ảnh: Chi tiết hóa đơn.png) màn "CHI TIẾT CỦA HÓA ĐƠN U25SG00002918" · ô "Cước phí từ ngày (From)" / "Đến ngày (To)" · dòng Chi tiết #1` ↔ `DOC-v2.0-01 BR-XHD-13 (L441)`  ·  Status: **Resolved 19/10/2026** · *mới — 16/10/2026*

**Ảnh màn hình hiện hữu** — `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png)
> Cước phí từ ngày (From) 17/11/2025 · Đến ngày (To) 16/12/2025
> Khoan thu tu 17/11/2025 den 16/12/2025

**URD 2.2** — `L441`
> Nội dung hiển thị trên hóa đơn là tên dịch vụ + số tháng sử dụng (lấy từ SPF), không hiển thị kỳ hạn từ ngày – đến ngày.

↳ **Ghi chú:** Hai ảnh là cùng hóa đơn `U25SG00002918` năm 2025 (trước Phase 2) trên "Hệ thống Thông tin": FIG-01 (ảnh: Chi tiết hóa đơn.png) tab "Chi tiết của Hóa đơn", FIG-02 (ảnh: Danh sách hóa đơn của Hợp đồng.png) tab "Báo cáo tổng hợp" → "Liệt kê cước của thuê bao" (cột Hóa đơn, Ngày Phát Hành, CN, Loại hóa đơn, Số tiền, Đã TT, Gen hóa đơn…). Nhiều khả năng đây là **điểm verify** BillNumber / BillDate / chi nhánh / Payment của QC — nhưng chưa ai xác nhận. Nếu dùng để verify hóa đơn v2.0 thì cần biết ô From/To sẽ hiển thị gì.

**Câu hỏi cho BA:** Hai màn này có phải điểm verify hóa đơn v2.0 không (QC có quyền truy cập STG)? Với hóa đơn v2.0, ô From/To và dòng "Khoản" hiển thị gì; cột "CN" là chi nhánh xuất hóa đơn của BR-XHD-12?

✅ **RESOLVED 19/10/2026** — Màn **Quản lý kế toán › Liệt kê cước** là điểm verify. Check: số tháng, thông tin KH, số tiền, tình trạng thanh toán, thông tin dịch vụ. From/To trên đầu hóa đơn lấy giá trị nào cũng được miễn nằm trong detail; dòng "Khoản" hiển thị "Khoản thu từ <fromdate> đến <todate>"; cột CN = chi nhánh hợp đồng (BR-XHD-12). Nội dung trên hóa đơn = tên dịch vụ (theo thông tin chi tiết loại dịch vụ) + số tháng tính ra kỳ hạn (khớp BR-XHD-13). Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-XHD-29 · Tài liệu tích hợp: payload Kafka, schema bảng, API, enum ⛔ BLOCKING
📍 `DOC-v2.0-01 §D · L653`  ·  Status: **Open — ⛔ BLOCKING** (setup data + execute) · GAP-07 (Critical), GAP-09 (Critical)

> Các nội dung dưới đây không cần PO confirm và không còn nằm trong phần chính. Chi tiết xem URD v2.1.

↳ **Ghi chú:** Ảnh hưởng cả GN (Kafka Out, API kênh thanh toán, API EVC, enum paymentstatus) và HK (API hóa đơn điện tử, Dịch vụ). §C của 2.2 không có owner / ngày chốt (GAP-09).

**Câu hỏi cho BA:** Gửi SDD / API spec / schema các bảng `OB_OrderRaw*`, `OB_OrderBill*`, `Paid`, `Payment`, cọc + enum trạng thái; điền owner + ngày chốt cho §C.

---

### CL-XHD-30 · Đơn ngoài 17 kênh / dịch vụ ngoài danh sách (ServiceID 2, 22) đi vào INVOICE thì xử lý thế nào?
📍 `DOC-v2.0-01 §A.3 · L260`  ·  Status: **Resolved 19/10/2026** · *mới — 16/10/2026*

> Không có trong danh sách phạm vi: ServiceID 2 (SubServiceType 5 đến 9) vì không có trong bảng nhóm dịch vụ; ServiceID 22 (GSafe) vì chưa có dịch vụ nào.

↳ **Ghi chú:** URD chỉ nói "không thuộc phạm vi", không nói hệ thống bỏ qua, log hay vẫn xuất. TP ghi ServiceID 2, 22 ngoài phạm vi test ⇒ chưa sinh SC; hỏi để biết có cần negative test chặn không.

**Câu hỏi cho BA:** Đơn có SaleChannelID / ServiceID ngoài danh sách thì INVOICE bỏ qua (không xuất) hay vẫn xuất?

✅ **RESOLVED 19/10/2026** — Đơn ngoài danh sách kênh / dịch vụ (ServiceID 2, 22): **không test** — khớp TP Scope OUT. Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-XHD-31 · URD v1.0 (Phase 1) và các "điều chỉnh v2.0" của Shopee / Tiktok
📍 `DOC-v2.0-01 §A.4 #2 (L269-270)` + `§A.2 (L133, L137)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · GAP-24 (Major)

> URD v1.0
> v1.0 (nền tảng, rule kênh TMĐT).
> (...)
> Đã triển khai ver1.0Có điều chinh ver2.0

↳ **Ghi chú:** Không có URD v1.0 ⇒ hồi quy TMĐT (SC-XHD-016, 017, 029, 060) theo giả định.

**Câu hỏi cho BA:** Gửi URD v1.0 + liệt kê hành vi Phase 1 của Shopee/Tiktok giữ / đổi ở v2.0.

🟡 **Làm rõ một phần 19/10/2026** — QC owner: hành vi Phase 1 của Shopee / TikTok Shop **vẫn test**. Còn mở: chưa có URD v1.0 / danh sách hành vi giữ – đổi ⇒ chưa có căn cứ viết expected. Nguồn: QC trả lời 19/10/2026 vòng 2.

🟡 **Ghi nhận 19/10/2026 (vòng 3)** — QC dán phần Hiện trạng / Mục tiêu của URD: sau Phase 1 đã xuất hóa đơn tự động kênh TMĐT (Shopee, TikTok Shop), **1 đơn 1 hóa đơn**, gạch nợ **chỉ bằng tiền đặt cọc**; Phase 2 mở cho mọi kênh, lịch chung, thêm gạch nợ tạm cho TMĐT. Còn mở: danh sách hành vi Phase 1 được giữ / đổi để viết expected. Nguồn: QC trả lời 19/10/2026 vòng 3.

---

### CL-XHD-32 · Dòng cuối tháng chuyển sang tháng sau: đợt nào phát hành, BillDate ngày nào?
📍 `DOC-v2.0-01 BR-XHD-01 (L384)` ↔ `BR-XHD-01 (L385)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · *mới — 16/10/2026* (phát sinh khi đóng CL-XHD-06)

**BR-XHD-01 — phạm vi quét của worker** — `L384`
> Mỗi đợt quét các dòng chưa xuất hóa đơn có mốc nghiệp vụ trong ngày, trước giờ chốt của đợt.

**BR-XHD-01 — dòng cuối tháng** — `L385`
> Đơn đủ điều kiện sau giờ chốt cuối của ngày cuối tháng sẽ phát hành sang tháng sau, ảnh hưởng kỳ ghi nhận doanh thu.

↳ **Ghi chú:** Dòng này có mốc nghiệp vụ ngày cuối tháng. Sang ngày 1 tháng sau, worker chỉ quét dòng có mốc **trong ngày** ⇒ theo chữ L384 thì không đợt nào lấy dòng này — cùng khoảng trống với RISK-XHD-03 (bản tin trễ qua ngày). SC-XHD-046 chỉ kiểm được "không phát hành trong tháng".

**Câu hỏi cho BA:** Dòng đủ điều kiện sau giờ chốt cuối ngày cuối tháng được phát hành ở đợt nào của tháng sau (đợt 1 ngày 1? realtime đầu ngày?), BillDate là ngày nào, và cơ chế nào đưa dòng này vào phạm vi quét khi mốc nghiệp vụ thuộc ngày trước?

🟡 **Làm rõ một phần 19/10/2026** — Dòng chuyển tháng phát hành **ngày 1 tháng sau**, **BillDate = ngày phát hành** (khớp BR-XHD-13 "BillDate là ngày phát hành thực tế") — QC ghi **cần PM confirm**. Còn mở: đợt nào của ngày 1, và cơ chế đưa dòng có mốc ngày trước vào phạm vi quét (BR-XHD-01 L384 chỉ quét mốc trong ngày). Nguồn: QC trả lời 19/10/2026 vòng 2.

---

### CL-XHD-33 · Phụ lục D của URD 2.2 trỏ chi tiết sang URD 2.1 — xác nhận hiệu lực + định nghĩa "mốc nghiệp vụ"
📍 `DOC-v2.0-01 §D · L653` + `§D#1–#3 (L658-669)`  ·  Status: **Open — đã rõ một phần 19/10/2026** · *mới — 16/10/2026*

> Các nội dung dưới đây không cần PO confirm và không còn nằm trong phần chính. Chi tiết xem URD v2.1.

↳ **Ghi chú:** Từ 16/10/2026 QC owner xác nhận URD 2.1 đã out, không dùng ⇒ các mục sau chưa có đặc tả: (1) D#1 cutover — cơ chế kiểm tra chéo luồng cũ / mới (SC-XHD-107, 108 đã deprecated; CL-XHD-24); (2) D#2 phương án chống phát hành trùng worker ↔ realtime (CL-XHD-23); (3) D#3 bản tin trễ qua ngày + mail cảnh báo (CL-XHD-22); (4) định nghĩa "mốc nghiệp vụ" của dòng DV / TB — BR-XHD-01 L384 và BR-XHD-02 L393 dùng nhưng 2.2 không định nghĩa. Phần GN (D#4) ở CL-GN-10; HK (D#5, D#6) ở CL-HK-10.

**Câu hỏi cho BA:** URD 2.2 Phụ lục D ghi "Chi tiết xem URD v2.1" — QC đã dùng URD 2.1 cho D#1 cutover, D#2 phát hành trùng, D#3 bản tin trễ (xem CL-XHD-22, 23, 24). Cần PO / SA: (1) xác nhận URD 2.1 còn hiệu lực cho các mục này; (2) định nghĩa "mốc nghiệp vụ" của dòng DV và dòng TB (thời điểm thanh toán / thời điểm giao hàng hoàn tất?) — BR-XHD-01, 02 dùng nhưng URD không định nghĩa.

🟡 **Làm rõ một phần 19/10/2026** — QC owner chốt dùng URD 2.1 (DOC-v2.0-02) cho Phụ lục D#1, 2, 3, 5, 6; **không** D#4, 7, 8, 9 ⇒ ghi chú gốc phía trên ("URD 2.1 đã out") không còn đúng. D#1–D#3 đã đối chiếu vào CL-XHD-22, 23, 24. Còn hỏi: PO / SA xác nhận hiệu lực của 2.1 cho các mục này + định nghĩa "mốc nghiệp vụ". Nguồn: QC owner 19/10/2026.

---

### CL-XHD-34 · Đơn DV kèm TB: DV phát hành ngay khi thanh toán hay chờ đơn hoàn tất? TB không triển khai lấy tín hiệu nào?
📍 `DOC-v2.0-01 BR-XHD-03 (L396)` ↔ `§I.a (L326)` ↔ flow QC test (`07_environments/environments.md §Flow QC test E2E`)  ·  Status: **Open — đã rõ một phần 19/10/2026** · *mới — 19/10/2026, chưa có GAP*

**URD 2.2 §I.a** — `L326`
> Dịch vụ phát hành khi hoàn tất thanh toán, thiết bị phát hành khi giao hàng hoàn tất.

**URD 2.2 BR-XHD-03** — `L396`
> Dịch vụ: khi có tín hiệu "đã thanh toán" từ SPF. Thiết bị: khi có tín hiệu giao hàng hoàn tất của phương thức triển khai tương ứng (phiếu thi công, Vendor, quầy). Hai điều kiện xét độc lập và dùng chung cho mọi kênh bán.

**Flow QC test (QC owner 19/10/2026)**
> KHÁCH HÀNG/ NHÂN VIÊN LÊN ĐON HÀNG THÀNH CÔNG -> KHÁCH HÀNG THANH TOÁN , KÝ BBDT > Triển khai (nếu có) > sau khi triển khai thành công -> cập nhật đơn hàng đã hoàn tất -> hệ thống mới gen hóa đơn

↳ **Ghi chú:** URD không có điều kiện "đơn hoàn tất": DV và TB xét độc lập ⇒ đơn DV + TB ra hóa đơn DV ngay khi thanh toán, hóa đơn TB khi có tín hiệu giao hàng (BR-XHD-05, 06, 14). Flow QC test và trả lời CL-XHD-27 vòng 2 ("xuất hóa đơn khi đơn hàng hoàn tất") lại cho hóa đơn chỉ gen sau khi đơn hoàn tất. Ngoài ra TB hình thức triển khai "Không" không có phiếu thi công / Vendor / quầy ⇒ không có nguồn tín hiệu theo BR-DB-02 (nối CL-XHD-27 ý 1). Nếu BA chốt "chờ đơn hoàn tất" ⇒ sửa Then của SC-XHD-037, 058, 071, 073, 105 và các SC phát hành DV / 1 đơn n hóa đơn.

**Câu hỏi cho BA:** (1) Đơn có dịch vụ kèm thiết bị: phần dịch vụ được phát hành hóa đơn ngay khi KH thanh toán xong (theo BR-XHD-03 — DV và TB xét độc lập), hay phải chờ triển khai xong và đơn chuyển "hoàn tất" mới phát hành? (2) Nếu chờ đơn hoàn tất: áp cho mọi đơn hay chỉ đơn có thiết bị / có triển khai; đơn chỉ có dịch vụ có phải chờ không? (3) Thiết bị có hình thức triển khai "Không" (không có phiếu thi công / Vendor / quầy): tín hiệu nào kích hoạt phát hành — có phải trạng thái "đơn hoàn tất" từ SPF, gửi qua bản tin nào?

🟡 **Làm rõ một phần 19/10/2026** — QC owner gửi flow cập nhật:
> KHÁCH HÀNG/ NHÂN VIÊN LÊN ĐON HÀNG THÀNH CÔNG -> KHÁCH HÀNG THANH TOÁN , KÝ BBDT > xuất hoá đơn cho dịch vụ truớc >Triển khai (nếu có) > sau khi giao hàng/ triển khai thành công -> cập nhật đơn hàng đã hoàn tất -> hệ thống mới gen tiếp hóa đơn cho thiết bị
> 1 ĐƠN HÀNG CÓ THỂ CÓ NHIỀU HÓA ĐƠN

⇒ Đã chốt (1): **DV phát hành hóa đơn ngay khi KH thanh toán**, không chờ triển khai — khớp BR-XHD-03 (DV / TB xét độc lập); SC-XHD-037, 058, 071, 073, 105 giữ nguyên. (2) Chỉ **hóa đơn thiết bị** chờ giao hàng / triển khai thành công; 1 đơn nhiều hóa đơn (BR-XHD-14). Còn hỏi: hóa đơn TB kích hoạt bởi **tín hiệu giao hàng của từng phương thức** (BR-DB-02, BR-XHD-06) hay bởi **trạng thái "đơn hàng hoàn tất"**? Đơn nhiều phương thức triển khai ra hóa đơn TB theo từng phương thức (SC-XHD-074, 105) hay một lần khi đơn hoàn tất? TB hình thức "Không" có dùng trạng thái "đơn hoàn tất" làm tín hiệu không (nối CL-XHD-27)? Nguồn: QC owner 19/10/2026.

🟡 **Làm rõ thêm 19/10/2026** — hóa đơn thiết bị được kích hoạt bởi **tín hiệu giao hàng của từng phương thức triển khai** (phiếu thi công / Vendor / quầy), **không** phải trạng thái "đơn hoàn tất" — khớp BR-DB-02, BR-XHD-06 ⇒ đơn nhiều phương thức ra hóa đơn thiết bị theo từng phương thức; SC-XHD-074, 105 giữ nguyên. Còn hỏi (duy nhất): thiết bị hình thức triển khai **"Không"** (không có phiếu thi công / Vendor / quầy) lấy tín hiệu nào để phát hành hóa đơn, gửi qua bản tin nào? (nối CL-XHD-27 — QC vòng 2 trả lời "xuất khi đơn hàng hoàn tất"). Nguồn: QC owner 19/10/2026.

✅ **Xác nhận 19/10/2026** — Đơn nhiều phương thức triển khai: **thiết bị nào có tín hiệu giao hàng thì xuất hóa đơn cho thiết bị đó**, không chờ cả đơn hoàn tất (QC owner). Khớp SC-XHD-074, 105. Câu còn hỏi giữ nguyên (TB hình thức "Không").
