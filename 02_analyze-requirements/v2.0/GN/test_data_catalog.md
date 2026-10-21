---
id: v2.0/GN/test_data_catalog
title: Test Data Catalog — Module GN
type: test_data_catalog
version: v2.0
module: { code: GN, dir: GN, name: "Gạch nợ hóa đơn" }
status: ANALYZED
updated: 2026-10-21
---

# Test Data Catalog — v2.0 · Module GN

> Tạo bởi: analyze-requirements (**stage: analyze** — sinh sớm để generate-tc dùng cho EP/BVA). Dữ liệu test (valid / invalid / boundary) per module, trích từ tài liệu gốc **theo đúng ký hiệu của DOC dự án** (`req_notation: BR`).
>
> **Structure-lock:** giữ nguyên 6 cột `| Field | Loại data | Valid | Invalid | Boundary | Nguồn |` cho mọi module. KHÔNG đổi cột.

## Module GN — Gạch nợ hóa đơn (DOC-v2.0-01)

| Field | Loại data | Valid | Invalid | Boundary | Nguồn |
|-------|-----------|-------|---------|----------|-------|
| Orderpaid → Paid (OrderCode) | Fixture | ⛔ QC không check bảng Paid — dev tự kiểm (QC owner 21/10/2026); **chỉ đơn sàn** (Paid chỉ có ở luồng sàn — QC owner 21/10/2026); 1 Orderpaid / OrderCode | — | — | BR-DP-01 (CL-GN-01) |
| PaidType | Master | ⛔ QC không check bảng Paid — dev tự kiểm (QC owner 21/10/2026); tiền khách · các loại voucher (BR-DP-01 L474) — dùng loại voucher có sẵn trên STG; không kiểm bên nào gạch, kiểm nợ còn lại = 0 (CL-GN-01, 21/10/2026) | — | — | BR-DP-01 (CL-GN-01, CL-GN-10) |
| Khóa trùng Paid | Fixture | ⛔ QC không check bảng Paid — dev tự kiểm (QC owner 21/10/2026); trùng đủ `OrderCode + RefTransactionId + PaidType + Amount` (→ cập nhật paymentstatus) | khác 1 trong 3 trường RefTransactionId / PaidType / Amount (→ thêm mới) | — | BR-DP-01 |
| paymentstatus | Master | `gạch nợ tạm` · `thanh toán hoàn tất` (verify trên bảng kê thanh toán — CL-GN-04) | trạng thái khác (→ dừng ở điểm chạm a, CL-GN-04) | — | BR-XL-01 · §A.5 #6 |
| Điểm chạm | Runtime | `(a) đồng bộ Paid xong` · `(b) sau khi xuất hóa đơn` · `(c) worker 30 phút` | — | **chu kỳ worker = 30 phút** | BR-XL-01 |
| Kênh sàn | Master | `{20 Shopee, 21 Tiktok}` (giả định — URD 2.2 §A.1 L59 "kênh TMĐT (Shopee, TikTok Shop)") | kênh ngoài sàn, vd Mobile (1) (→ không gạch tạm; đơn ngoài sàn đi luồng Cọc — QC owner 21/10/2026) | — | BR-NT-01 (CL-GN-03) |
| Trường gạch nợ Paid/Cọc (OrderBill) | Runtime | `Paid` · `Cọc` · rỗng (→ gọi API kênh thanh toán) | API lỗi / timeout (→ dừng, không retry) | — | BR-XL-03 |
| Phương thức thanh toán đặc biệt (Payment tạm) | Master | Phương thức thanh toán = "gạch nợ tạm" trên bảng kê thanh toán, số tiền = nợ còn lại **sau khi trừ EVC** (BA 21/10/2026) | — | — | BR-NT-02 (CL-GN-04) |
| Paid Amount | Fixture | `> 0` (= phần khách trả), cùng OrderCode với hóa đơn | khác OrderCode (→ không dùng) | — (biên 0 / 1 không test: đơn 0đ không có khoản thu / gạch nợ, 1đ không dựng được — QC owner 21/10/2026, nháp #13) | BR-GN-01 |
| Danh sách bill của đơn | Fixture | 1..n bill, số tiền khác nhau (vd 500k / 300k / 100k) · đơn ngoài sàn có bill DV + bill TB, hóa đơn TB phát hành sau khi giao hàng (SC-GN-055) | — | **2 bill bằng tiền (→ bill nào gạch trước cũng được, CL-GN-09)** | BR-GN-03 |
| Paid so với nợ bill | Fixture | **Paid = phần khách trả = tổng tiền đơn − EVC** (chia lần lượt cho từng bill) | Paid < nợ, Paid > nợ — không dựng được trên luồng thực tế (CL-GN-05; BA 21/10/2026: lệch = dev đẩy data sai) | **Paid = nợ** | BR-GN-04 |
| Σ Payment so với tổng hóa đơn | Runtime | Σ Payment = tổng hóa đơn (→ "Đã gạch nợ") | Σ Payment < tổng hóa đơn (→ còn nợ — vd còn phần lock EVC, SC-GN-046) | — (T − 1 không dựng được — nháp #13) | BR-GN-05 |
| Kafka Out | Runtime | ⛔ QC không check — phần dành cho dev (BA, CL-XHD-29, 21/10/2026) | — | — | BR-GN-04 (CL-XHD-29) |
| Cọc còn lại của hợp đồng | Runtime | thông tin cọc có **nhiều dòng, mỗi dòng gắn 1 bill**, mỗi dòng clear 1 lần (nháp #11); khách thanh toán ngoài Paid ⇒ tiền đẩy vào cọc, **cọc = phần khách trả** (tổng tiền đơn − voucher / EVC — BA 21/10/2026); verify tồn cọc tăng khi thanh toán, giảm đúng số tiền khi gạch | — (thiếu cọc không xảy ra thực tế; SC-GN-038, 040, 041 deprecated) | **cọc + EVC = nợ bill (đủ)** | BR-GC-01 · BR-GC-02 |
| Loại cọc của dịch vụ | Master | mỗi dịch vụ dùng một loại cọc (BR-GC-03 L539) — **map dịch vụ ↔ loại cọc không test**, chỉ check có sinh đặt cọc (CL-GN-07, 19/10/2026) | — | — | BR-GC-03 (CL-GN-07) |
| Payment nhánh Cọc | Runtime | trừ cọc theo BillNumber + số hợp đồng; kiểm Σ Payment cọc = nợ bill — **không kiểm số dòng theo loại cọc** (nháp #12) | — | — | BR-GC-03 (CL-GN-07) |
| Tổng EVC + tiền lock của đơn | Fixture | từ API đội EVC (mock): `{tổng EVC, lock}` | API lỗi / timeout (→ chưa đặc tả, CL-GN-02) | **lock = 0 (gạch như thường)** | BR-VC · BR-GC-01 |
| Số gạch tiền khách khi có lock | Runtime | `min(nợ bill − lock, Paid khách)` — vd nợ 1.000k, lock 300k, Paid 700k → 700k | — | **Paid khách = nợ − lock**; lock = 0 ⇒ Paid = nợ | BR-VC |
| Nhóm dịch vụ (ServiceID) | Master | 20 nhóm trong phạm vi: 1 Internet · 3 FPT Camera Only · 4 FPT Camera Combo · 5 FPT Play Stands Alone · 6 Sản phẩm khác · 7 FPT Play · 8 Tổng đài Oncall · 9 FPT Smart Home · 10 Ultra Fast Stand Alone · 11 FPro · 12 FSafe Go · 13 VioEdu Stand Alone · 15 VIP 247 · 16 SIM data · 17 Pay Wifi · 18 Ultra Fast · 19 FPT Camera B2B · 21 HyperFast · 23 FPT AI Wi-Fi · 25 Prepaid 3 — mỗi nhóm 1 TC, dịch vụ bất kỳ của nhóm (**không quan tâm SubServiceType** — QC owner 21/10/2026); danh sách SubServiceType ở `XHD/test_data_catalog.md` | ServiceID 2, 22 (→ ngoài phạm vi) | — | DOC-v2.0-01 §A.3 |
| Loại đơn | Fixture | `bán mới` (phát sinh hợp đồng mới) · `bán thêm` (bán trên hợp đồng đã có, có thể từ rất lâu; bill bán thêm có dòng cọc riêng) — 2 luồng cơ bản như nhau; hợp đồng bán thêm có **đơn hàng trước chưa thanh toán** ⇒ khi đã thanh toán, gạch luôn cùng đơn bán thêm (nháp #15, #16) | — | — | DOC-v2.0-04 · BR-GC-01 |

(lặp bảng cho mỗi module — file này chỉ module GN)

## Ghi chú chung
- **Cột `Loại data`** (trả lời "data nào mặc định / tự tạo"):
  - **Master** = có sẵn từ hệ thống (enum paymentstatus, PaidType, danh mục loại cọc…). KHÔNG cần seed; **giá trị thực xác nhận lại ở vibe-test** (môi trường-phụ thuộc).
  - **Fixture** = test **tự tạo** (Orderpaid/Paid, tồn cọc, mock EVC…). Test chịu trách nhiệm tạo + dọn.
  - **Runtime** = sinh khi chạy (Payment, trạng thái hóa đơn) — không cố định trước.
- Boundary values (in **đậm**) là ứng viên chính cho BVA ở generate-tc.
- Bảng verify chính: `Paid` / `Orderpaid` · `Payment` · `Ob_OrderBill` (trường Paid/Cọc) · bảng tồn cọc (tên bảng là phần của dev — CL-GN-10). Tiền VND không phần thập phân.
- Tool verify (`07_environments/environments.md §Tool tra cứu`): khoản thu → **Foxpay › Thanh toán online › Đối soát khoản thu online**; cọc → **Quản lý kế toán › Tiền đặt cọc › Tra cứu**; trạng thái nợ hóa đơn → **Quản lý kế toán › Liệt kê cước**. Gạch nợ tay (**Gạch nợ bổ sung TT online**) chỉ dùng chuẩn bị / khôi phục data, không thay luồng tự động.
- Số tiền trong cột Valid / Boundary là **dữ liệu minh họa của analyst**, không phải giá trị của URD.

### Quy ước cell (giữ nhất quán)
- **Loại data:** đúng 1 trong `Master` / `Fixture` / `Runtime` (xem Ghi chú chung). Field lấy từ danh mục hệ thống → `Master`; field test nhập/tạo → `Fixture`; field hệ thống tự sinh → `Runtime`.
- **Valid:** `value (mô tả)` — vd `ABC1234567 (10 ký tự)`, `hôm nay (default)`.
- **Invalid:** `value (→ hệ quả/MSG)` — vd `rỗng (→MSG-001)`, `"abc" (→MSG-E-002)`. Dự án không có mã MSG → ghi mô tả hệ quả (vd `rỗng (→ báo lỗi bắt buộc nhập)`).
- **Boundary:** **bold** giá trị biên + (hợp lệ/chặn) — vd `**500 ký tự (hợp lệ), 501 (chặn)**`.
- **Nguồn:** dùng **đúng ký hiệu của DOC dự án** theo `req_notation` — ở đây là `BR-…`. **KHÔNG tự bịa ID**.
- Set literal `{0=…, 1=…}`; `→` = hệ quả; `⟷` = quan hệ 2 chiều; `[…]` = ID pattern.
