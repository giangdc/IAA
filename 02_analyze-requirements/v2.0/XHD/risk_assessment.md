---
id: v2.0/XHD/risk_assessment
title: Risk Assessment — Module XHD
type: risk_assessment
version: v2.0
module: { code: XHD, dir: XHD, name: "Đồng bộ đơn hàng & xuất hóa đơn tự động" }
counts:                 # 🔑 CANONICAL — CL/RISK của module XHD
  cl: 31
  cl_open: 31
  cl_blocking: 4        # CL chặn sinh TC / execute (đánh dấu ⛔ BLOCKING)
  risk: 10
  risk_high: 6
status: ANALYZED
updated: 2026-10-16
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
| RISK-XHD-02 | XHD / phát hành trùng | Worker và realtime chạy song song có khoảng trống giữa kiểm BillNumber và ghi BillNumber ⇒ 2 HĐ thật cho 1 dòng, nợ khách tính gấp đôi, GN trừ Paid 2 lần | High | DOC-v2.0-01 §D#2 (L662-665); DOC-v2.0-02 BR-XHD-09 (L370-378) | Tín hiệu đến sát giờ chốt cuối; bản tin lặp; SC-XHD-055, 056, 077 | Chờ phương án PM + SA (CL-XHD-23); exploratory R1 sát giờ chốt; HĐ dư xử lý ngoài phạm vi | Open | SC-XHD-055, SC-XHD-056, SC-XHD-077 · REQ-XHD-027 |
| RISK-XHD-03 | XHD / bản tin trễ qua ngày | Dòng có mốc nghiệp vụ ngày N nhưng bản tin về ngày N+1 rơi vào khoảng trống — không luồng nào phát hành; mail cảnh báo "bắt buộc" chưa có đặc tả | High | DOC-v2.0-01 §D#3 (L666-669); DOC-v2.0-02 RISK-01 (L428-440) | SC-XHD-045 (ghi nhận hiện trạng) | Chờ CL-XHD-22; mail cảnh báo chưa sinh SC — nợ CHANGELOG §3 | Open | SC-XHD-045 · REQ-XHD-015, REQ-XHD-042 |
| RISK-XHD-04 | XHD / khóa chống trùng | Khóa 2.2 (dịch vụ hóa đơn + gói) khác 2.1 (ServiceCode + SubserviceType) nhưng ghi "Giữ nguyên"; SubServiceType 31 trùng ở 2 DV ⇒ dev và QC có thể dùng 2 khóa khác nhau, chặn nhầm hoặc phát hành trùng | High | DOC-v2.0-01 BR-XHD-08 (L419) ↔ §C#3 (L649-651) ↔ BR-DB-07 (L374) | SC-XHD-076..079, SC-XHD-028 | Hỏi BA khóa chốt (CL-XHD-11, 12) trước generate-tc cho nhóm chống trùng | Open | SC-XHD-076, SC-XHD-077, SC-XHD-078, SC-XHD-079 · REQ-XHD-027 |
| RISK-XHD-05 | XHD / kênh FPL | Lịch 2h, mốc 22:05, delay 2h, realtime sau 22h, thông tin KH 2 giờ đều mới ở 2.2 và thiếu mốc cụ thể ⇒ dễ lệch giữa dev / QC; vùng 18:00–22:00 khác kênh khác | High | DOC-v2.0-01 BR-XHD-01 (L386-388), BR-XHD-03 (L399), BR-XHD-06 (L414), BR-DB-03 (L356-358) | SC-XHD-031..034, SC-XHD-047..053 | Resolve CL-XHD-02..05 trước generate-tc; chỉnh lịch trên STG để chạy được nhiều mốc trong ngày | Open | SC-XHD-031..034, SC-XHD-047..053 · REQ-XHD-007, REQ-XHD-017, REQ-XHD-021, REQ-XHD-026 |
| RISK-XHD-06 | XHD / điều kiện PĐK + hợp đồng con | Rule mới; chưa biết trường nhận diện HĐ tổ chức, nguồn trạng thái PĐK, cách tính "2 ngày cuối tháng", đầu ra khi chặn ⇒ có thể chặn nhầm (không ra HĐ) hoặc bỏ lọt | High | DOC-v2.0-01 BR-XHD-03 (L400-401) | SC-XHD-061..068 (biên cuối tháng 28/30/31 ngày) | Resolve CL-XHD-07, 08, 09; chuẩn bị HĐ tổ chức / cá nhân / hợp đồng con trên STG | Open | SC-XHD-061..068 · REQ-XHD-022, REQ-XHD-023 |
| RISK-XHD-07 | XHD / thời gian | Nhiều SC phụ thuộc giờ chốt, cuối tháng, qua nửa đêm ⇒ khó tái hiện trên STG nếu không chỉnh được giờ hệ thống / tham số lịch | Medium | DOC-v2.0-01 BR-XHD-01 (L381-385); TP §3.2 | SC-XHD-041..046, 054..056, 063, 064 | Xác nhận với dev cách chỉnh tham số lịch + giờ hệ thống STG trước R1 | Open | SC-XHD-041..046, SC-XHD-054..056, SC-XHD-063, SC-XHD-064 · REQ-XHD-014..016 |
| RISK-XHD-08 | XHD / ma trận kênh × DV | 17 kênh × 20 nhóm × 2 loại đơn = 680 tổ hợp, không có ma trận kênh nào bán nhóm nào; mỗi kênh cần tài khoản / cách tạo đơn trên STG | Medium | DOC-v2.0-01 §A.2, §A.3; TP §2.3 GAP-62 | SC-XHD-001..017 | Xin ma trận thực bán (CL-XHD-26); ưu tiên Shopee/Tiktok (hồi quy) + FPL | Open | SC-XHD-001..017 · REQ-XHD-001, REQ-XHD-002 |
| RISK-XHD-09 | XHD / hồi quy Phase 1 | Chưa nhận URD v1.0 ⇒ không biết hành vi TMĐT nào giữ / đổi; "Có điều chỉnh ver2.0" không liệt kê điều chỉnh | Medium | DOC-v2.0-01 §A.2 (L133, L137), §A.4 #2 | SC-XHD-016, 017, 029, 060 | Xin URD v1.0 (CL-XHD-31); tạm dùng 2.1 BR-DB-02 làm hành vi Phase 1 | Open | SC-XHD-016, SC-XHD-017, SC-XHD-029, SC-XHD-060 · REQ-XHD-005, REQ-XHD-020 |
| RISK-XHD-10 | XHD / cutover v1 → v2 | Đơn dở dang lúc go-live có thể bị bỏ sót phần TB (hệ quả đã biết của kiểm tra chéo mức đơn) hoặc phát hành lại; scope test trên STG chưa chốt | Medium | DOC-v2.0-02 BR-DB-08 (L297-305); DOC-v2.0-01 §D#1 | SC-XHD-107, 108 | PM xác nhận scope (CL-XHD-24); nếu Out-scope ⇒ Status → Closed | Open | SC-XHD-107, SC-XHD-108 · REQ-XHD-041 |

> Risk ID format: `RISK-<MODULE>-<NN>` (vd `RISK-PV-01`). Severity = High / Medium / Low (có thể Medium-High).
> **Solution:** biện pháp giảm thiểu hoặc hướng xử lý cụ thể (vd "resolve C-XXX trước generate-tc", "thêm negative TC cho MSG", "defer tới khi có env"). Chưa có → `—` (nhưng High/Medium nên có).
> **Status** — trạng thái xử lý rủi ro. Enum THUẦN (không kèm ghi chú trong ô — lý do để ở cột `Solution`):
> - `Open` = chưa xử lý / **đang bị chặn** (env/API/BA/backend chưa sẵn → chưa cover được).
> - `Pending` = **chấp nhận + defer có chủ đích** (không xử ở version này; vd NFR chờ môi trường thật / tải lớn).
> - `Resolved` = **đã xử lý và thêm test case cover** rủi ro (có `Solution` + TC/SC khả thi).
> - `Closed` = **bỏ khỏi scope** (feature loại khỏi version → rủi ro không còn áp dụng).
> KHÔNG để trống. Vòng đời: `Open` → `Resolved` (khi đã cover) · `Open` → `Pending` (defer) · `→ Closed` (bỏ scope).

## Khuyến nghị tổng thể
1. **Resolve blocker clarifications trước generate-tc** các scenario liên quan: CL-XHD-21 (BR-XHD-18), CL-XHD-22 (mail cảnh báo), CL-XHD-29 (tài liệu tích hợp), CL-XHD-11 (khóa chống trùng) — và nhóm FPL CL-XHD-02..05, nhóm PĐK CL-XHD-07, 08.
2. **Ưu tiên test P1 high-risk:** SC-XHD-041..043, 054..059, 061..063, 066, 067, 069..071, 073, 074, 076..078, 101..103, 105 (+ ma trận Shopee/Tiktok SC-XHD-016, 017).
3. **Performance / cần môi trường:** không có NFR; các SC thời gian (SC-XHD-041..046, 063, 064) cần chỉnh lịch / giờ STG — RISK-XHD-07.
4. **ID/text cleanup (non-blocking, cần trước automation):** cột "So với v2.1" ghi "Giữ nguyên" ở BR-XHD-01, 06, 08, 10 dù đã đổi (GAP-56); typo URD "SFP" (L326), "bên đưới" (L63), "thự hiện" (L452) — giữ nguyên trong quote.

## Clarifications (home CL — layout v2)

> 1 CL = 1 heading `### CL-XHD-NN · <câu hỏi ngắn>`. Dòng META mang `Status` (+ `⛔ BLOCKING` nếu chặn sinh TC / execute) và mã GAP tương ứng. Khi resolved: **thêm** đoạn `✅ RESOLVED <ngày> — <kết luận>`, giữ nguyên phần phân tích cũ.

### CL-XHD-01 · BR-DB-01 chỉ còn 2 sự kiện, nhưng BR khác vẫn cần "tạo đơn" và "cập nhật thông tin khách"
📍 `DOC-v2.0-01 BR-DB-01 (L345)` ↔ `BR-DB-03 (L359)` ↔ `BR-XHD-03 (L399)`  ·  Status: **Open** · GAP-42 (Critical)

**BR-DB-01** — `DOC-v2.0-01 §I.c · L345`
> Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng.

**BR-DB-03 — dùng sự kiện không còn trong danh sách** — `L359`
> Cập nhật thông tin khách không kích hoạt phát hành hóa đơn; lần phát hành tiếp theo dùng thông tin mới nhất.

**BR-XHD-03 — mốc cần dữ liệu tạo đơn** — `L399`
> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

↳ **Ghi chú:** Doc tự mâu thuẫn. 2.1 (L256-262) có đủ 4 sự kiện. SC-XHD-020 đang theo giả định TP "đủ 4 sự kiện như 2.1".

**Câu hỏi cho BA:** SPF còn đồng bộ sự kiện "tạo đơn" và "cập nhật thông tin khách hàng" sang INVOICE không? (Có — giữ như 2.1 / Không — dữ liệu tạo đơn và thông tin KH lấy từ đâu?)

---

### CL-XHD-02 · FPL: khách không lấy HĐ, hoặc quá 2 giờ không nhập thì sao? "(ví dụ FPL)" có kênh khác không?
📍 `DOC-v2.0-01 BR-DB-03 · L356-358`  ·  Status: **Open** · GAP-48 (Critical)

> Ngoại lệ: kênh bán FPL cho khách chọn có lấy hóa đơn hay không (ví dụ FPL).
> (...)
> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** 2 nhánh không có đầu ra. Theo quy định HĐĐT vẫn phải lập HĐ dù khách không lấy — suy diễn của analyst, cần xác nhận. Ảnh hưởng SC-XHD-032..034.

**Câu hỏi cho BA:** (1) Khách FPL chọn "không lấy HĐ" ⇒ INVOICE vẫn phát hành với thông tin hợp đồng hay không phát hành? (2) Quá 2 giờ không nhập ⇒ dùng thông tin hợp đồng? (3) Ngoại lệ chỉ áp FPL (10) hay còn kênh nào?

---

### CL-XHD-03 · 7 trường khách FPL tự nhập: bắt buộc, định dạng, ai kiểm tra?
📍 `DOC-v2.0-01 BR-DB-03 · L357`  ·  Status: **Open** · GAP-49 (Major)

> Nếu khách chọn lấy hóa đơn thì dùng thông tin khách tự nhập: tên, email, số điện thoại, mã số thuế, mã định danh, mã quan hệ ngân sách, số hộ chiếu.

↳ **Ghi chú:** Không có rule validate ⇒ `test_data_catalog.md` chỉ ghi được "có / rỗng". Nếu kênh FPL tự kiểm thì INVOICE chỉ nhận dữ liệu đã sạch.

**Câu hỏi cho BA:** Trường nào bắt buộc, định dạng (MST 10/13 số? email?), và INVOICE có validate lại hay tin dữ liệu kênh FPL gửi?

---

### CL-XHD-04 · Mốc delay 2h của FPL: "thời gian tạo đơn" hay "thời điểm ghi nhận trên hệ thống của kênh"? Áp cho DV hay cả TB?
📍 `DOC-v2.0-01 BR-XHD-03 (L399)` ↔ `BR-DB-03 (L358)`  ·  Status: **Open** · GAP-51 (Major)

**BR-XHD-03** — `L399`
> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

**BR-DB-03** — `L358`
> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** Hai mốc 2 giờ dùng 2 cách gọi khác nhau; nếu khác thời điểm thì có thể phát hành trước khi khách hết hạn nhập.

**Câu hỏi cho BA:** Hai mốc là một? Delay 2h áp cho dòng DV, TB hay cả hai?

---

### CL-XHD-05 · Lịch FPL "2h quét 1 lần": các mốc chạy và giờ chốt cụ thể? Có là tham số?
📍 `DOC-v2.0-01 BR-XHD-01 · L386-388` ↔ `§A.1 #3 · L63`  ·  Status: **Open** · GAP-50 (Critical), GAP-52 (Minor)

> Xét riêng cho kênh bán FPL:
> 2h quét 1 lần
> Mốc 22:05 chốt từ 0h đến 22 giờ (Do FPL có rule delay 2h nên phải bổ sung khung giờ để quét hết những case không quét được do delay ở hai khung giờ trước)

**§A.1 #3 — mục tiêu nói lịch chung** — `L63`
> Xuất hóa đơn cho tất cả kênh bán liệt kê bên đưới và có đơn hàng SPF, dùng một lịch chung (giờ chốt và giờ chạy là tham số cấu hình) thay vì chia theo kênh và theo ngày thường / cuối tháng.

↳ **Ghi chú:** Không biết đợt đầu chạy lúc mấy giờ, mỗi đợt chốt tới đâu, "hai khung giờ trước" là khung nào. Mục tiêu §A.1 "không chia theo kênh" mâu thuẫn với lịch riêng FPL (GAP-52).

**Câu hỏi cho BA:** Liệt kê mốc chạy + giờ chốt của lịch FPL trong ngày; có cấu hình được như lịch chung không?

---

### CL-XHD-06 · Ngày cuối tháng, đủ điều kiện sau giờ chốt cuối: realtime phát hành ngay hay để sang tháng sau?
📍 `DOC-v2.0-01 BR-XHD-01 (L385)` ↔ `BR-XHD-06 (L413)`  ·  Status: **Open** · GAP-43 (Critical)

**BR-XHD-01** — `L385`
> Đơn đủ điều kiện sau giờ chốt cuối của ngày cuối tháng sẽ phát hành sang tháng sau, ảnh hưởng kỳ ghi nhận doanh thu.

**BR-XHD-06** — `L413`
> Xử lý ngay khi nhận, không chờ đợt worker kế tiếp.

↳ **Ghi chú:** Nếu realtime chạy cả ngày cuối tháng thì câu L385 chỉ đúng cho dòng có tín hiệu về trước giờ chốt cuối nhưng chưa đủ điều kiện. TP đang giả định realtime vẫn chạy (SC-XHD-046).

**Câu hỏi cho BA:** Ngày cuối tháng, tín hiệu về sau giờ chốt cuối ⇒ realtime phát hành trong ngày (tháng này) hay dòng chờ sang tháng sau?

---

### CL-XHD-07 · PĐK: nhận diện HĐ tổ chức, nguồn trạng thái PĐK, cách tính "2 ngày cuối tháng", duyệt muộn
📍 `DOC-v2.0-01 BR-XHD-03 · L400`  ·  Status: **Open** · GAP-44 (Critical), GAP-45 (Major), GAP-61 (Major)

> Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK; hai ngày cuối tháng không xét điều kiện này. Quên duyệt PĐK thì không autobill. Khi có thay đổi hoặc dịch chuyển luồng duyệt PĐK/hợp đồng thì phải hiệu chỉnh lại điều kiện này.

↳ **Ghi chú:** 4 điểm mở: (1) trường nào đánh dấu HĐ tổ chức (loại hình KH cấp 1?); (2) trạng thái PĐK lấy từ hệ thống nào; (3) "2 ngày cuối tháng" = 2 ngày lịch hay 2 ngày làm việc; (4) PĐK duyệt sau khi bị chặn thì đợt sau có phát hành. Thêm đơn **bán thêm** trên HĐ tổ chức đã duyệt PĐK: xét PĐK của lần nào (GAP-61). Ảnh hưởng SC-XHD-061..065, 068.

**Câu hỏi cho BA:** Trả lời 4 điểm trên + PĐK của đơn bán thêm.

---

### CL-XHD-08 · Hợp đồng con không phát hành: ghi nhận ra sao? HĐ cha có phát hành thay?
📍 `DOC-v2.0-01 BR-XHD-03 · L401`  ·  Status: **Open** · GAP-46 (Major)

> Hợp đồng con: nhận diện hợp đồng con khi hợp đồng có gắn hợp đồng cha (hợp đồng dự án). Không phát hành hóa đơn trên hợp đồng con, cả thiết bị và dịch vụ.

↳ **Ghi chú:** SC-XHD-066, 067 chỉ kiểm được "không phát hành". Không rõ có log, có cờ, hay dòng nằm tồn mãi.

**Câu hỏi cho BA:** Dòng của hợp đồng con được đánh dấu / log thế nào; HĐ cha có xuất thay không?

---

### CL-XHD-09 · Revision 2.2 ghi thêm "KH Chuỗi/Dự án" vào BR-XHD-03 nhưng BR không có nội dung
📍 `DOC-v2.0-01 Revision History 2.2 · L36` ↔ `BR-XHD-03 · L395-403`  ·  Status: **Open** · GAP-47 (Major)

> [A]: Điều kiện duyệt PĐK, hợp đồng con, KH Chuỗi/Dự án (gộp vào BR-XHD-03); BR-XHD-18 (clear thuê thiết bị đầu cuối) theo email 24/09 và 30/09.

↳ **Ghi chú:** BR-XHD-03 chỉ có "hợp đồng dự án" trong câu hợp đồng con; không có gì về KH Chuỗi ⇒ có thể thiếu rule.

**Câu hỏi cho BA:** KH Chuỗi có rule phát hành riêng không? Nếu có, nội dung là gì?

---

### CL-XHD-10 · BR-XHD-04 (autobill TB theo phương thức) đã bỏ — bỏ hành vi hay chỉ bỏ câu chữ?
📍 `DOC-v2.0-01 §D#9 (L690-693)` ↔ `§A.5 #3 (L288-290)` ↔ `BR-XHD-03 (L397)`  ·  Status: **Open** · GAP-54 (Major)

**Phụ lục D#9** — `L691-693`
> Autobill thiết bị theo phương thức triển khai (gom một lượt theo từng phương thức).
> BR-XHD-04
> Đã bỏ khỏi tài liệu.

**Thuật ngữ #3 — vẫn dùng** — `L290`
> Mỗi phương thức tương ứng một phiếu triển khai hoặc giao hàng và là đơn vị autobill của thiết bị.

↳ **Ghi chú:** 2.1 BR-XHD-04 (L334-341): nhận tín hiệu của một phương thức ⇒ phát hành **toàn bộ** TB của phương thức đó (kể cả giao thiếu). TP giả định hành vi như 2.1 (SC-XHD-059).

**Câu hỏi cho BA:** Khi nhận tín hiệu giao hàng của một phương thức, INVOICE phát hành toàn bộ TB thuộc phương thức đó (như 2.1) hay chỉ TB có trong tín hiệu?

---

### CL-XHD-11 · Khóa chống trùng chốt theo bản nào, gồm field nào? ⛔ BLOCKING
📍 `DOC-v2.0-01 BR-XHD-08 (L419)` ↔ `§C#3 (L649-651)` ↔ `BR-DB-07 (L374)` ↔ `DOC-v2.0-02 BR-XHD-08 (L361-363)`  ·  Status: **Open — ⛔ BLOCKING** (nhóm chống trùng) · GAP-41 (Critical), GAP-56 (Major)

**URD 2.2 BR-XHD-08** — `L419, L422`
> Khóa xác định dòng: dịch vụ = mã đơn hàng + dịch vụ hóa đơn + Gói dịch vụ; thiết bị thêm phương thức triển khai.
> (...)
> Giữ nguyên

**URD 2.2 §C#3 — vẫn nói khóa dùng SubServiceType** — `L651`
> Khóa chống trùng có dùng SubServiceType nên có thể làm hai dòng bị coi là trùng.

**URD 2.1 BR-XHD-08** — `DOC-v2.0-02 L362-363`
> •  Dòng Dịch vụ: OrderCode + ServiceCode + SubserviceType. Dòng dịch vụ không xét hình thức triển khai.
> •  Dòng Thiết bị: OrderCode + ServiceCode + SubserviceType + hình thức triển khai.

↳ **Ghi chú:** 2.2 đổi khóa nhưng ghi "Giữ nguyên"; §C#3 và BR-DB-07 vẫn theo khóa cũ. "Dịch vụ hóa đơn" và "Gói dịch vụ" ứng với field nào trong dữ liệu chưa rõ. Theo quy tắc 2.2 thắng, TP giả định theo text 2.2. ⛔ Không sinh TC chi tiết dữ liệu khóa cho SC-XHD-076..079 tới khi trả lời.

**Câu hỏi cho BA:** Khóa chống trùng chốt là (a) mã đơn + dịch vụ hóa đơn + gói dịch vụ [+ phương thức] (2.2) hay (b) OrderCode + ServiceCode + SubserviceType [+ phương thức] (2.1)? Field tương ứng là gì?

---

### CL-XHD-12 · SubServiceType 31 trùng ở 2 dịch vụ Tổng đài Oncall
📍 `DOC-v2.0-01 §A.3 (L191-192, L259)` + `§C#3 (L649-651)`  ·  Status: **Open** · §C#3 của URD

> 31 – Thiết bị Oncall (Type 2)
> 31 – Thiết bị IP phone (Type 2)
> (...)
> Ô màu vàng: SubServiceType 31 trùng ở hai dịch vụ (Thiết bị Oncall, Thiết bị IP phone) của nhóm Tổng đài Oncall.

↳ **Ghi chú:** Doc tự đưa vào điểm cần xác nhận. Nếu khóa còn dùng SubServiceType (CL-XHD-11) thì đơn có cả 2 TB này sẽ chỉ ra HĐ cho 1 dòng (SC-XHD-079).

**Câu hỏi cho BA:** SubServiceType của "Thiết bị IP phone" có phải 31 thật không, hay danh mục nhập sai?

---

### CL-XHD-13 · Ý nghĩa cột Type 1–4 và quan hệ với ProductType DV/TB
📍 `DOC-v2.0-01 §C#2 · L644-647`  ·  Status: **Open** · §C#2 của URD

> Ý nghĩa cột Type (1 đến 4) của dịch vụ và cách map với ProductType (DV/TB).
> Mục A.3, BR-DB-04
> Danh sách dịch vụ ghi Type từ 1 đến 4, chưa có mô tả ý nghĩa.

↳ **Ghi chú:** Suy diễn của analyst từ tên dịch vụ: Type 1 = Basic/cước chính, Type 2 = thiết bị, Type 3 = Extra/dịch vụ cộng thêm, Type 4 = triển khai. Nếu đúng thì Type 2 ⇔ TB, còn lại DV — nhưng "Đặt cọc thuê bao (Type 3)" và "Triển khai (Type 4)" là DV hay TB thì không suy được. INVOICE không suy diễn (BR-DB-04) nên ảnh hưởng chủ yếu là **dữ liệu test**.

**Câu hỏi cho BA:** Xác nhận nghĩa Type 1–4 và với mỗi Type thì SPF gắn ProductType gì.

---

### CL-XHD-14 · "Hợp đồng có hiệu lực" và "đang cập nhật" là những giá trị trạng thái nào?
📍 `DOC-v2.0-01 BR-XHD-10 · L425-426`  ·  Status: **Open** · GAP-13 (Critical)

> Đơn không ở trạng thái hủy hoặc đang cập nhật.
> Thông tin chung phải đủ: hợp đồng có hiệu lực, Sale Team, Sale Channel, tên khách hàng, loại hình khách hàng cấp 1 và cấp 2, địa chỉ xuất hóa đơn, LocationID > 0.

↳ **Ghi chú:** Cần enum trạng thái đơn + hợp đồng để dựng SC-XHD-081, 082 (TP giả định theo v1.0). 2.1 L381 có chữ "hủy TSD".

**Câu hỏi cho BA:** Liệt kê trạng thái đơn = "đang cập nhật" và trạng thái hợp đồng = "có hiệu lực".

---

### CL-XHD-15 · Log khi không hợp lệ: ghi ở đâu, nội dung gì, thứ tự validate, nhiều lỗi cùng lúc? Đơn không có khuyến mãi?
📍 `DOC-v2.0-01 BR-XHD-10 · L427-428`  ·  Status: **Open** · GAP-29 (Major), GAP-30 (Major)

> Chi tiết từng dịch vụ phải có các ID dịch vụ, nhóm dịch vụ, gói dịch vụ, chính sách, câu lệnh giá, chương trình khuyến mãi > 0.
> Không hợp lệ thì không phát hành và ghi log; hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

↳ **Ghi chú:** 14 SC negative (SC-XHD-080..095) chỉ kiểm được "có log". Đơn không có chương trình khuyến mãi thì ID KM = 0? ⇒ theo chữ URD sẽ bị chặn.

**Câu hỏi cho BA:** (1) Log ghi bảng / cột nào, format? (2) Thứ tự kiểm, có log tất cả lỗi hay dừng ở lỗi đầu? (3) Đơn không có KM thì ID KM mang giá trị gì và có bị chặn không?

---

### CL-XHD-16 · Job cảnh báo 15 phút: điều kiện, kênh gửi, người nhận, nội dung?
📍 `DOC-v2.0-01 BR-XHD-10 · L429`  ·  Status: **Open** · GAP-31 (Critical)

> Job cảnh báo chạy 15 phút một lần để bổ sung thông tin kịp trước giờ chốt.

↳ **Ghi chú:** Nằm trong BR in-scope nhưng không có đặc tả — SC-XHD-097 để P3.

**Câu hỏi cho BA:** Job cảnh báo những dòng nào, gửi qua kênh nào (mail?), cho ai, nội dung gì? Có thuộc v2.0 không?

---

### CL-XHD-17 · Dòng không hợp lệ được bổ sung thông tin: đợt sau có phát hành?
📍 `DOC-v2.0-01 BR-XHD-10 (L428)` ↔ `DOC-v2.0-02 BR-XHD-11 (L402)`  ·  Status: **Open** · GAP-55 (Major)

**URD 2.2** — `L428`
> Không hợp lệ thì không phát hành và ghi log; hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

**URD 2.1 — câu bị mất khi gộp BR-XHD-11** — `DOC-v2.0-02 L402`
> Dòng không phát hành được vẫn giữ trạng thái BillNumber IS NULL. Nếu về sau có bản tin đồng bộ mới cho đơn đó thì dòng được xuất hóa đơn theo bản tin mới, với ngày phát hành tại thời điểm đó.

↳ **Ghi chú:** Bản mới sửa BR-XHD-10 nhưng không nói câu 2.1 hết hiệu lực. TP giả định theo 2.1 (SC-XHD-096).

**Câu hỏi cho BA:** Câu "có bản tin mới thì xuất theo bản tin mới" của 2.1 còn hiệu lực không?

---

### CL-XHD-18 · Billing lỗi / timeout: hệ thống làm gì?
📍 `DOC-v2.0-01 BR-XHD-13 · L439`  ·  Status: **Open** · GAP-14 (Critical)

> Phát hành qua Billing System, ghi BillNumber và BillDate vào giỏ tồn xuất hóa đơn

↳ **Ghi chú:** Không có nhánh lỗi. TP giả định giữ BillNumber rỗng + log (SC-XHD-104).

**Câu hỏi cho BA:** Retry? Giữ rỗng chờ đợt sau? Cảnh báo?

---

### CL-XHD-19 · Cột Note: thuộc bảng nào, format log tín hiệu giao hàng?
📍 `DOC-v2.0-01 BR-DB-07 · L375`  ·  Status: **Open** · GAP-27 (Major)

> Nếu thiết bị đã có hóa đơn hoặc không khớp khóa thì không ghi nhận, chỉ ghi log nội dung tín hiệu vào cột Note.

↳ **Ghi chú:** SC-XHD-026..028 chỉ kiểm định tính.

**Câu hỏi cho BA:** Cột Note ở bảng nào, ghi những trường gì của tín hiệu, có ghi lý do (đã có HĐ / không khớp) không?

---

### CL-XHD-20 · Bản tin Order Event lỗi giải mã / thiếu trường
📍 `DOC-v2.0-01 §I.a Trigger · L332` *(derived from omission — URD không nói)*  ·  Status: **Open** · GAP-26 (Major)

> Sự kiện đơn hàng từ SPF; tín hiệu giao hàng hoàn tất; worker chạy theo lịch (BR-XHD-01).

↳ **Ghi chú:** 2.1 có bước "Invoice Consumer nhận và giải mã bản tin" (L183) nhưng cả 2 bản không có nhánh lỗi. Chưa sinh SC.

**Câu hỏi cho BA:** Bản tin không giải mã được / thiếu trường bắt buộc thì bỏ qua + log, hay dừng consumer?

---

### CL-XHD-21 · BR-XHD-18 "clear thuê thiết bị đầu cuối": có thuộc v2.0? Đặc tả? ⛔ BLOCKING
📍 `DOC-v2.0-01 BR-XHD-18 · L449-452`  ·  Status: **Open — ⛔ BLOCKING** · GAP-53 (Blocker)

> Bổ sung chức năng cho phép DVKH HO chủ động xử lý với hợp đồng có yêu cầu clear nội dung "thuê thiết bị đầu cuối" trên hóa đơn.
> Mới (kịp plan các chức năng chính sẽ thự hiện)

**Ảnh màn hình hiện hữu — có sẵn cột cùng tên** — `DOC-v2.0-FIG-02` màn "LIỆT KÊ CƯỚC CỦA THUÊ BAO" · tiêu đề cột cuối bảng
> Clear thiết bị đầu cuối

↳ **Ghi chú:** Có thể có UI (duy nhất trong URD). Màn "Liệt kê cước" của Hệ thống Thông tin (FIG-02) **đã có cột "Clear thiết bị đầu cuối"** cạnh "Hóa đơn điều chỉnh giảm", "Hóa đơn thay thế", "Gen hóa đơn" ⇒ **suy diễn của analyst:** BR-XHD-18 có thể là thao tác trên màn này, nhưng URD không nói. REQ-XHD-039 chưa có SC.

**Câu hỏi cho BA:** Chức năng này thuộc v2.0 không? Nếu có: có phải cột "Clear thiết bị đầu cuối" trên màn Liệt kê cước (FIG-02) không; input, kết quả trên HĐ (HĐ mới / điều chỉnh / chỉ đổi nội dung dòng?).

---

### CL-XHD-22 · Mail cảnh báo bản tin trễ qua ngày + phương án xử lý: thuộc v2.0? Đặc tả? ⛔ BLOCKING
📍 `DOC-v2.0-01 §D#3 · L666-669`  ·  Status: **Open — ⛔ BLOCKING** · GAP-02 (Blocker), GAP-11 (Critical)

> Bản tin đồng bộ về chậm qua ngày, dòng không được luồng nào xử lý.
> RISK-01
> PM và SA xử lý; mail cảnh báo là yêu cầu bắt buộc đã thống nhất.

↳ **Ghi chú:** Phụ lục ghi "không cần PO confirm" nhưng là "yêu cầu bắt buộc". REQ-XHD-042 chưa có SC; SC-XHD-045 chỉ ghi nhận hiện trạng.

**Câu hỏi cho BA:** Mail cảnh báo có trong v2.0? Điều kiện phát hiện, lịch gửi, người nhận, nội dung? Phương án xử lý dòng trễ đã chốt chưa?

---

### CL-XHD-23 · Phương án chặn phát hành trùng worker ↔ realtime
📍 `DOC-v2.0-01 §D#2 · L662-665`  ·  Status: **Open** · GAP-12 (Critical)

> Rủi ro phát hành hóa đơn trùng khi worker và realtime chạy song song.
> BR-XHD-09
> PM và SA chốt phương án kỹ thuật.

↳ **Ghi chú:** RISK-XHD-02. Không có phương án ⇒ không biết expected khi 2 luồng tranh nhau.

**Câu hỏi cho BA:** Phương án đã chốt? Ngày có trên STG?

---

### CL-XHD-24 · Cutover v1 → v2: có test trên STG không? Dữ liệu luồng cũ?
📍 `DOC-v2.0-01 §D#1 · L658-661`  ·  Status: **Open** · GAP-32 (Major)

> Chuyển đổi hệ thống v1 sang v2 (cutover, giai đoạn giao thoa, quét tay bổ sung).
> BR-DB-08
> PM, SA

↳ **Ghi chú:** TP giữ FR06 (P2, 18 TC). Out-scope ⇒ SC-XHD-107, 108 chuyển DEPRECATED và RISK-XHD-10 → Closed.

**Câu hỏi cho BA:** Cutover có nằm trong phạm vi QC v2.0? Nếu có: STG có dữ liệu + service luồng cũ không?

---

### CL-XHD-25 · Đơn bán thêm: rule áp chung, hay có điểm khác?
📍 `DOC-v2.0-04 mail PM · dòng 3` ↔ `DOC-v2.0-01 (toàn bộ BR — không có từ "bán thêm")`  ·  Status: **Open** · GAP-60 (Major)

> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** Ảnh hưởng ≥7 chức năng (XHD F01, F04, F06; GN F17; HK F19, F23; F27). Điểm có thể khác: PĐK (CL-XHD-07), cọc (CL-GN-07), ký hiệu HĐ (CL-HK-01), tiền trả trước (CL-HK-07).

**Câu hỏi cho BA:** Mọi BR áp chung cho đơn bán thêm? Nếu không, liệt kê điểm khác.

---

### CL-XHD-26 · Ma trận kênh × nhóm DV × loại đơn thực bán
📍 `DOC-v2.0-01 §A.2 (L80)` + `§A.3 (L139)` + `BR-XHD-12 (L435)`  ·  Status: **Open** · GAP-62 (Major)

> Tất cả kênh bán trong danh sách dưới đây thuộc phạm vi. Phase 1 đã triển khai Shopee và Tiktok.
> (...)
> Chi nhánh nào được bán sản phẩm dịch vụ nào do bên quản lý sản phẩm bổ sung thuộc tính, nằm ngoài URD này.

↳ **Ghi chú:** SC-XHD-001..017 giả định mọi kênh bán mọi nhóm. Mỗi cặp không bán bớt 2 TC (TP §2.3).

**Câu hỏi cho BA:** Gửi ma trận kênh × nhóm DV × {bán mới, bán thêm} thực bán; cặp nào không bán thì bỏ khỏi phạm vi test.

---

### CL-XHD-27 · Danh mục HT triển khai (DOC-v2.0-05): map sang 3 nguồn tín hiệu; TB "Không" phát hành thế nào?
📍 `DOC-v2.0-05 sheet "1. HT Triển khai" · STT 1, 8` ↔ `DOC-v2.0-01 BR-DB-02 (L349)`  ·  Status: **Open** · *mới — phát hiện khi analyze 16/10/2026, chưa có GAP*

**DOC-v2.0-05 — STT 8** — cột D
> - Phiếu thi công: triển khai bởi TINPNC nếu hàng hóa có mix HT "Không" và "TIN/PNC"
> - None: không đẩy triển khai, giao hàng nếu hàng hóa, dịch vụ trên đơn hàng chỉ có "Không"

**DOC-v2.0-05 — STT 1** — cột G
> Đơn hàng có ít nhất 1 SPDV có mix HT Triển khai TIN/PNC và Quầy/ Sales --> auto xử lý theo luồng triển khai TINPNC

**URD 2.2 BR-DB-02** — `L349`
> Tín hiệu đi thẳng về INVOICE từ 3 nguồn độc lập: phiếu thi công (tình trạng "Đã xử lý hoàn tất"), Vendor (khi đối tác giao xong), phiếu giao tại quầy.

↳ **Ghi chú:** File bổ sung có 8 hình thức, URD chỉ nói 3 nguồn. (1) TB DeployType "Không" ⇒ không có phiếu ⇒ không có tín hiệu ⇒ theo BR-XHD-03 không bao giờ phát hành. (2) Đơn mix TIN/PNC + Quầy gộp sang TINPNC ⇒ phương thức trong khóa (BR-DB-07, BR-XHD-08) là gì. (3) File chưa có version/ngày, chưa rõ là tài liệu chính thức hay tham khảo.

**Câu hỏi cho BA:** (1) TB "Không" xuất HĐ theo đường nào? (2) Đơn mix: tín hiệu mang phương thức nào? (3) File này có phải danh mục chính thức của v2.0 không?

---

### CL-XHD-28 · Ảnh màn Hệ thống Thông tin (DOC-v2.0-FIG-01, FIG-02) vẫn hiện "Từ ngày / Đến ngày" — 2 màn này dùng để verify?
📍 `DOC-v2.0-FIG-01 màn "CHI TIẾT CỦA HÓA ĐƠN U25SG00002918" · ô "Cước phí từ ngày (From)" / "Đến ngày (To)" · dòng Chi tiết #1` ↔ `DOC-v2.0-01 BR-XHD-13 (L441)`  ·  Status: **Open** · *mới — 16/10/2026*

**Ảnh màn hình hiện hữu** — `DOC-v2.0-FIG-01`
> Cước phí từ ngày (From) 17/11/2025 · Đến ngày (To) 16/12/2025
> Khoan thu tu 17/11/2025 den 16/12/2025

**URD 2.2** — `L441`
> Nội dung hiển thị trên hóa đơn là tên dịch vụ + số tháng sử dụng (lấy từ SPF), không hiển thị kỳ hạn từ ngày – đến ngày.

↳ **Ghi chú:** Hai ảnh là cùng HĐ `U25SG00002918` năm 2025 (trước Phase 2) trên "Hệ thống Thông tin": FIG-01 tab "Chi tiết của Hóa đơn", FIG-02 tab "Báo cáo tổng hợp" → "Liệt kê cước của thuê bao" (cột Hóa đơn, Ngày Phát Hành, CN, Loại hóa đơn, Số tiền, Đã TT, Gen hóa đơn…). Nhiều khả năng đây là **điểm verify** BillNumber / BillDate / chi nhánh / Payment của QC — nhưng chưa ai xác nhận. Nếu dùng để verify HĐ v2.0 thì cần biết ô From/To sẽ hiển thị gì.

**Câu hỏi cho BA:** Hai màn này có phải điểm verify HĐ v2.0 không (QC có quyền truy cập STG)? Với HĐ v2.0, ô From/To và dòng "Khoản" hiển thị gì; cột "CN" là chi nhánh xuất HĐ của BR-XHD-12?

---

### CL-XHD-29 · Tài liệu tích hợp: payload Kafka, schema bảng, API, enum ⛔ BLOCKING
📍 `DOC-v2.0-01 §D · L653`  ·  Status: **Open — ⛔ BLOCKING** (setup data + execute) · GAP-07 (Critical), GAP-09 (Critical)

> Các nội dung dưới đây không cần PO confirm và không còn nằm trong phần chính. Chi tiết xem URD v2.1.

↳ **Ghi chú:** 2.1 cũng không có payload / schema. Ảnh hưởng cả GN (Kafka Out, API kênh thanh toán, API EVC, enum paymentstatus) và HK (API HĐĐT, Dịch vụ). §C của 2.2 không có owner / ngày chốt (GAP-09).

**Câu hỏi cho BA:** Gửi SDD / API spec / schema các bảng `OB_OrderRaw*`, `OB_OrderBill*`, `Paid`, `Payment`, cọc + enum trạng thái; điền owner + ngày chốt cho §C.

---

### CL-XHD-30 · Đơn ngoài 17 kênh / dịch vụ ngoài danh sách (ServiceID 2, 22) đi vào INVOICE thì xử lý thế nào?
📍 `DOC-v2.0-01 §A.3 · L260`  ·  Status: **Open** · *mới — 16/10/2026*

> Không có trong danh sách phạm vi: ServiceID 2 (SubServiceType 5 đến 9) vì không có trong bảng nhóm dịch vụ; ServiceID 22 (GSafe) vì chưa có dịch vụ nào.

↳ **Ghi chú:** URD chỉ nói "không thuộc phạm vi", không nói hệ thống bỏ qua, log hay vẫn xuất. TP ghi ServiceID 2, 22 ngoài phạm vi test ⇒ chưa sinh SC; hỏi để biết có cần negative test chặn không.

**Câu hỏi cho BA:** Đơn có SaleChannelID / ServiceID ngoài danh sách thì INVOICE bỏ qua (không xuất) hay vẫn xuất?

---

### CL-XHD-31 · URD v1.0 (Phase 1) và các "điều chỉnh v2.0" của Shopee / Tiktok
📍 `DOC-v2.0-01 §A.4 #2 (L269-270)` + `§A.2 (L133, L137)`  ·  Status: **Open** · GAP-24 (Major)

> URD v1.0
> v1.0 (nền tảng, rule kênh TMĐT).
> (...)
> Đã triển khai ver1.0Có điều chinh ver2.0

↳ **Ghi chú:** Không có URD v1.0 ⇒ hồi quy TMĐT (SC-XHD-016, 017, 029, 060) theo giả định.

**Câu hỏi cho BA:** Gửi URD v1.0 + liệt kê hành vi Phase 1 của Shopee/Tiktok giữ / đổi ở v2.0.
