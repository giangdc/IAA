---
id: v2.0/XHD/test_data_catalog
title: Test Data Catalog — Module XHD
type: test_data_catalog
version: v2.0
module: { code: XHD, dir: XHD, name: "Đồng bộ đơn hàng & xuất hóa đơn tự động" }
status: ANALYZED
updated: 2026-10-19
---

# Test Data Catalog — v2.0 · Module XHD

> Tạo bởi: analyze-requirements (**stage: analyze** — sinh sớm để generate-tc dùng cho EP/BVA). Dữ liệu test (valid / invalid / boundary) per module, trích từ tài liệu gốc **theo đúng ký hiệu của DOC dự án** (`req_notation: BR` — cột `Nguồn` ghi `BR-…`; bảng phạm vi / phụ lục ghi `DOC-ID §section`).
>
> **Structure-lock:** giữ nguyên 6 cột `| Field | Loại data | Valid | Invalid | Boundary | Nguồn |` cho mọi module. KHÔNG đổi cột.

## Module XHD — Đồng bộ đơn hàng & xuất hóa đơn tự động (DOC-v2.0-01)

| Field | Loại data | Valid | Invalid | Boundary | Nguồn |
|-------|-----------|-------|---------|----------|-------|
| SaleChannelID (kênh bán) | Master | `{1=Mobile, 2=Desktop, 4=DKOL, 7=API, 9=W-Sale, 10=FPL, 11=VNTT, 12=MBBank, 13=CRM, 14=TGDD, 15=F-Retail, 16=CMR-App, 17=Momo, 18=SR-KPDV, 19=HiFPT, 20=Shopee, 21=Tiktok}` (17 kênh) | kênh ngoài danh sách, vd `3`, `5` (→ hành vi chưa đặc tả, CL-XHD-30) | — | DOC-v2.0-01 §A.2 |
| Nhóm kênh theo rule | Master | `FPL = {10}` (lịch / delay / KH riêng) · `kênh sàn TMĐT = {20, 21}` (hồi quy Phase 1, gạch nợ tạm) · `kênh thường = 15 kênh còn lại` | — | — | BR-XHD-01, BR-XHD-03, BR-DB-02 |
| ServiceID / SubServiceType (nhóm DV – dịch vụ) | Master | 20 nhóm: `1 Internet {1,2,3,4,25,28}` · `3 FPT Camera Only {10,11,12,13}` · `4 FPT Camera Combo {14,15,16,404}` · `5 FPT Play Stands Alone {17,18}` · `6 Sản phẩm khác {19}` · `7 FPT Play {20,21,22,23,24,42,43}` · `8 Tổng đài Oncall {29,30,31,31}` · `9 FPT Smart Home {32,33}` · `10 Ultra Fast Stand Alone {34}` · `11 FPro {35,36,37,38}` · `12 FSafe Go {39}` · `13 VioEdu Stand Alone {40}` · `15 VIP 247 {1501}` · `16 SIM data {1601..1604}` · `17 Pay Wifi {1701}` · `18 Ultra Fast {1801}` · `19 FPT Camera B2B {1901..1906}` · `21 HyperFast {2101}` · `23 FPT AI Wi-Fi {2301,2302,2303}` · `25 Prepaid 3 {2501}` (55 dịch vụ) | `ServiceID 2` (SubServiceType 5..9) · `ServiceID 22` GSafe (→ ngoài phạm vi, CL-XHD-30) | **SubServiceType 31 xuất hiện 2 lần trong nhóm 8 (Thiết bị Oncall / Thiết bị IP phone) — ca biên của khóa chống trùng** | DOC-v2.0-01 §A.3 · §C#3 |
| Type dịch vụ (1–4) | Master | `{1, 2, 3, 4}` — nghĩa chưa định nghĩa (suy diễn: 1 Basic, 2 Thiết bị, 3 Extra, 4 Triển khai; QC rà 16/10: không có bảng mô tả, chờ PO) | — | — | DOC-v2.0-01 §A.3 · §C#2 (CL-XHD-13) |
| ProductType (dòng chi tiết) | Fixture | `DV` · `TB` (SPF gắn) | rỗng / giá trị khác (→ chưa đặc tả) | — | BR-DB-04 |
| Loại đơn | Fixture | `bán mới` · `bán thêm` (trên hợp đồng đang hoạt động) | — | — | DOC-v2.0-04 (mail PM) |
| Sự kiện SPF | Runtime | `thanh toán` · `hủy đơn` (BR-DB-01) (SPF chỉ gửi 2 sự kiện này — CL-XHD-01 resolved 19/10/2026; thông tin khách lấy từ hợp đồng) | bản tin lỗi giải mã / thiếu trường (→ chưa đặc tả, CL-XHD-20) · bản tin lặp (→ không phát hành lại) | — | BR-DB-01 · BR-DB-05 |
| Nguồn tín hiệu giao hàng | Runtime | `phiếu thi công` ("Đã xử lý hoàn tất") · `Vendor` · `phiếu giao tại quầy` | phiếu thi công chưa "Đã xử lý hoàn tất" (→ không có tín hiệu) | — | BR-DB-02 |
| Phương thức / HT triển khai (DeployType) | Master | `TIN/PNC` · `TIN/PNC giao hàng` · `FTI` (→ phiếu thi công) · `NCC-Samsung` · `NCC-Sony` · `NCC-Casper` (→ Vendor) · `Quầy` · `Sale` (→ quầy) — map là suy diễn | `Không` / None (→ không có tín hiệu, CL-XHD-27) | **đơn mix TIN/PNC + Quầy/Sale → gộp luồng TINPNC** | DOC-v2.0-05 · BR-DB-02 |
| Khóa map tín hiệu giao hàng | Fixture | mã đơn + ServiceCode + SubserviceType + phương thức khớp TB chưa xuất | không khớp (→ không ghi nhận, log cột Note) · TB đã có BillNumber (→ log Note) | **khớp 3/4 (sai phương thức) → không khớp** | BR-DB-07 |
| Khóa chống trùng | Fixture | DV: mã đơn + dịch vụ hóa đơn + gói dịch vụ · TB: + phương thức (2.2 — QC chốt 16/10; field dữ liệu chờ schema CL-XHD-29) | dòng đã có BillNumber (→ bỏ qua) | **2 TB cùng khóa DV, khác phương thức → 2 lần phát hành hợp lệ** | BR-XHD-08 (CL-XHD-11) |
| Thông tin KH xuất HĐ — mặc định | Master | theo hợp đồng (tên, địa chỉ, MST…) | — | — | BR-DB-03 |
| Thông tin KH FPL tự nhập | Fixture | tên, email, số điện thoại, mã số thuế, mã định danh, mã quan hệ ngân sách, số hộ chiếu — bắt buộc: công ty = tên công ty, địa chỉ, MST, email; cá nhân = họ tên, địa chỉ, email; mã quan hệ ngân sách, số hộ chiếu, mã định danh không bắt buộc (CL-XHD-03) | khách không bấm Xuất hóa đơn / không nhập trong 2 giờ (→ không phát hành hóa đơn, CL-XHD-02) · kênh khác FPL (→ không có lựa chọn này) | **nhập lúc 2:00 (hợp lệ), 2:01 (chặn) kể từ thời điểm ghi nhận trên kênh** | BR-DB-03 (CL-XHD-03) |
| Lịch worker chung (tham số) | Master | `số đợt = 2` · đợt 1 `chốt 12:00 / chạy 12:05` · đợt 2 `chốt 18:00 / chạy 18:05` — ⛔ TC ghi "giờ chốt đợt N" | — | **mốc nghiệp vụ ngay trước giờ chốt (vào đợt) · đúng giờ chốt / sau (sang đợt sau)** | BR-XHD-01 |
| Mốc nghiệp vụ dòng | Runtime | DV = thời điểm hoàn tất thanh toán · TB = thời điểm giao hàng (— URD 2.2 chưa định nghĩa, CL-XHD-33) | mốc thuộc ngày trước, bản tin về hôm sau (→ không luồng nào lấy, RISK-XHD-03) | **ngày cuối tháng sau giờ chốt cuối (→ không phát hành trong tháng, sang tháng sau; đợt phát hành CL-XHD-32)** | BR-XHD-01 |
| Thời điểm nhận tín hiệu | Runtime | trước giờ chốt (→ worker) · giữa các đợt (→ worker đợt kế) · sau giờ chốt cuối (→ realtime) | — | **đúng giờ chốt cuối** | BR-XHD-02 · BR-DB-05 |
| Lịch FPL | Master | `2h/lần` (tham số; mốc giả định 0:05, 2:05 … 20:05) + `mốc 22:05 chốt 0h–22h` + `sau 22h chỉ realtime` | — | **tín hiệu FPL 21:59 (worker) / 22:01 (realtime)** | BR-XHD-01 · BR-XHD-06 (CL-XHD-05) |
| Delay FPL | Runtime | thời gian tạo đơn + ≥ 2h | < 2h (→ chưa phát hành ở mốc đó) | **1:59 (chưa), 2:00 (đủ), 2:01 (đủ)** | BR-XHD-03 (CL-XHD-04) |
| Loại hợp đồng | Master | `cá nhân` · `tổ chức` = loại hình KH cấp 1 "Tổ chức" (QC chốt 16/10) | — | — | BR-XHD-03 (CL-XHD-07) |
| Trạng thái PĐK (HĐ tổ chức) | Fixture | `đã duyệt` (trạng thái lấy từ SPF) | `chưa duyệt` (→ không autobill, trừ 2 ngày lịch cuối tháng) | **ngày cuối −2 (chặn) · cuối −1 và ngày cuối (không xét PĐK) — tháng 28/30/31 ngày** | BR-XHD-03 |
| Hợp đồng cha / con | Fixture | hợp đồng không gắn hợp đồng cha | hợp đồng có gắn hợp đồng cha — kiểm bằng tool tình trạng (→ không phát hành DV + TB) | — | BR-XHD-03 |
| Trạng thái đơn | Master | `Bình thường` | `Đã hủy` · `Đang cập nhật` = chưa có thông tin hợp đồng (→ không phát hành + log) | — | BR-XHD-10 (CL-XHD-14) |
| Trạng thái hợp đồng | Master | `Bình thường` | `Tạm ngưng` · `Đã chấm dứt` · `Ngưng vì lý do thanh toán` (→ không phát hành + log) | — | BR-XHD-10 (CL-XHD-14) |
| Sale Team · Sale Channel · Tên KH · Loại hình KH cấp 1 · cấp 2 · Địa chỉ xuất HĐ | Master | có giá trị | rỗng (→ không phát hành + log) | — | BR-XHD-10 |
| LocationID | Master | `≥ 1` | `0`, âm (→ không phát hành + log) | **0 (chặn), 1 (hợp lệ)** | BR-XHD-10 |
| ID dịch vụ · ID nhóm DV · ID gói DV · ID chính sách · ID câu lệnh giá · ID CTKM | Master | `≥ 1` | `0`, âm (→ không phát hành + log) | **0 (chặn), 1 (hợp lệ)** — riêng ID CTKM: đơn không có khuyến mãi vẫn phát hành (CL-XHD-15) | BR-XHD-10 |
| Chi nhánh xuất HĐ | Master | chi nhánh quản lý hợp đồng tại thời điểm phát hành | — | **đổi chi nhánh quản lý giữa 2 lần phát hành** | BR-XHD-12 |
| BillNumber | Runtime | Billing trả về, ghi vào `OB_OrderBill` | Billing lỗi / timeout (→ không phát hành, dev retry tay, CL-XHD-18) | — | BR-XHD-13 |
| BillDate | Runtime | ngày phát hành thực tế | ngày = mốc nghiệp vụ khi khác ngày phát hành (→ sai) | **realtime qua nửa đêm: BillDate = ngày mới** | BR-XHD-13 |
| Nội dung dòng HĐ | Runtime | tên dịch vụ + số tháng sử dụng (SPF) | có kỳ hạn "từ ngày – đến ngày" (→ sai) | — | BR-XHD-13 (CL-XHD-28) |
| Số tháng sử dụng | Master | lấy từ SPF | — | — | BR-XHD-13 |

(lặp bảng cho mỗi module — file này chỉ module XHD)

## Ghi chú chung
- **Cột `Loại data`** (trả lời "data nào mặc định / tự tạo"):
  - **Master** = có sẵn từ hệ thống (danh mục kênh, dịch vụ, hợp đồng, chi nhánh…). KHÔNG cần seed; **giá trị thực xác nhận lại ở vibe-test** (môi trường-phụ thuộc).
  - **Fixture** = test **tự tạo** (đơn hàng SPF, PĐK, hợp đồng con, thông tin KH FPL…). Test chịu trách nhiệm tạo + dọn.
  - **Runtime** = sinh khi chạy (BillNumber, BillDate, thời điểm nhận bản tin, sự kiện Kafka) — không cố định trước.
- Boundary values (in **đậm**) là ứng viên chính cho BVA ở generate-tc.
- ⛔ Giờ chốt / giờ chạy là **tham số cấu hình** — TC ghi theo "giờ chốt của đợt", không hardcode 12:00/18:00 (Project_rule §Test Data Rules). Ngày `dd/MM/yyyy`, tiền VND không phần thập phân.
- Bảng verify chính: `OB_OrderRaw` / `OB_OrderRaw_Detail` (đơn đồng bộ) · `OB_OrderBill` / `OB_OrderBill_Detail` (BillNumber, BillDate, chi nhánh). Tên cột chi tiết chờ CL-XHD-29.
- Tool verify (QC không xem được DB/log — `07_environments/environments.md §Tool tra cứu`): đơn hàng → **Web admin**; hóa đơn → **Quản lý kế toán › Liệt kê cước**.

### Quy ước cell (giữ nhất quán)
- **Loại data:** đúng 1 trong `Master` / `Fixture` / `Runtime` (xem Ghi chú chung). Field lấy từ danh mục hệ thống → `Master`; field test nhập/tạo → `Fixture`; field hệ thống tự sinh → `Runtime`.
- **Valid:** `value (mô tả)` — vd `ABC1234567 (10 ký tự)`, `hôm nay (default)`.
- **Invalid:** `value (→ hệ quả/MSG)` — vd `rỗng (→MSG-001)`, `"abc" (→MSG-E-002)`. Dự án không có mã MSG → ghi mô tả hệ quả (vd `rỗng (→ báo lỗi bắt buộc nhập)`).
- **Boundary:** **bold** giá trị biên + (hợp lệ/chặn) — vd `**500 ký tự (hợp lệ), 501 (chặn)**`.
- **Nguồn:** dùng **đúng ký hiệu của DOC dự án** theo `req_notation` trong block `## DOC Notation` của `Project_rule.md` — ở đây là `BR-…`; bảng phạm vi / phụ lục / tài liệu bổ sung dùng `DOC-ID §section`. **KHÔNG tự bịa ID**.
- Set literal `{0=…, 1=…}`; `→` = hệ quả; `⟷` = quan hệ 2 chiều; `[…]` = ID pattern.
