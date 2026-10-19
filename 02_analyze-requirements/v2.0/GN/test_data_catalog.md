---
id: v2.0/GN/test_data_catalog
title: Test Data Catalog — Module GN
type: test_data_catalog
version: v2.0
module: { code: GN, dir: GN, name: "Gạch nợ hóa đơn" }
status: ANALYZED
updated: 2026-10-19
---

# Test Data Catalog — v2.0 · Module GN

> Tạo bởi: analyze-requirements (**stage: analyze** — sinh sớm để generate-tc dùng cho EP/BVA). Dữ liệu test (valid / invalid / boundary) per module, trích từ tài liệu gốc **theo đúng ký hiệu của DOC dự án** (`req_notation: BR`).
>
> **Structure-lock:** giữ nguyên 6 cột `| Field | Loại data | Valid | Invalid | Boundary | Nguồn |` cho mọi module. KHÔNG đổi cột.

## Module GN — Gạch nợ hóa đơn (DOC-v2.0-01)

| Field | Loại data | Valid | Invalid | Boundary | Nguồn |
|-------|-----------|-------|---------|----------|-------|
| Orderpaid → Paid (OrderCode) | Fixture | 1 Orderpaid / OrderCode, nhiều dòng detail = nhiều đợt thanh toán | — | — | BR-DP-01 (CL-GN-01) |
| PaidType | Master | tiền khách · các loại voucher (BR-DP-01 L474) — enum + danh sách loại EVC / voucher chờ BA (CL-GN-01, CL-GN-10); Paid voucher được dùng gạch nợ (CL-GN-01 vòng 2) | — | — | BR-DP-01 (CL-GN-01, CL-GN-10) |
| Khóa trùng Paid | Fixture | trùng đủ `OrderCode + RefTransactionId + PaidType + Amount` (→ cập nhật paymentstatus) | khác 1 trong 3 trường RefTransactionId / PaidType / Amount (→ thêm mới) | — | BR-DP-01 |
| paymentstatus | Master | `gạch nợ tạm` · `thanh toán hoàn tất` (giá trị enum chưa có) | trạng thái khác (→ dừng ở điểm chạm a, CL-GN-04) | — | BR-XL-01 · §A.5 #6 |
| Điểm chạm | Runtime | `(a) đồng bộ Paid xong` · `(b) sau khi xuất HĐ` · `(c) worker 30 phút` | — | **chu kỳ worker = 30 phút** | BR-XL-01 |
| Kênh sàn | Master | `{20 Shopee, 21 Tiktok}` (giả định — URD 2.2 §A.1 L59 "kênh TMĐT (Shopee, TikTok Shop)") | kênh khác, vd quầy / nơi triển khai (→ không gạch tạm) | — | BR-NT-01 (CL-GN-03) |
| Trường gạch nợ Paid/Cọc (OrderBill) | Runtime | `Paid` · `Cọc` · rỗng (→ gọi API kênh thanh toán) | API lỗi / timeout (→ dừng, không retry) | — | BR-XL-03 |
| Phương thức thanh toán đặc biệt (Payment tạm) | Master | mã PT đặc biệt (chưa có), số tiền = toàn bộ nợ còn lại | — | — | BR-NT-02 (CL-GN-04) |
| Paid Amount | Fixture | `≥ 1`, cùng OrderCode với HĐ | `0`, âm (→ không dùng) · khác OrderCode (→ không dùng) | **0 (không dùng), 1 (dùng)** | BR-GN-01 |
| Danh sách bill của đơn | Fixture | 1..n bill, số tiền khác nhau (vd 500k / 300k / 100k) | — | **2 bill bằng tiền (→ CL-GN-09)** | BR-GN-03 |
| Paid so với nợ bill | Fixture | Paid < nợ · Paid = nợ · Paid > nợ | — | **Paid = nợ − 1 / = nợ / = nợ + 1** | BR-GN-04 |
| Σ Payment so với tổng HĐ | Runtime | Σ Payment = tổng HĐ (→ "Đã gạch nợ") | Σ Payment < tổng HĐ (→ còn nợ) | **T − 1 (còn nợ), T (Đã gạch nợ)** | BR-GN-05 |
| Kafka Out | Runtime | 1 bản tin / lần gạch nhánh Paid (payload chưa có) | có Kafka Out ở nhánh Cọc (→ sai) | — | BR-GN-04 (CL-XHD-29) |
| Cọc còn lại của hợp đồng (theo loại) | Fixture | tổng mọi loại + EVC (gồm lock) ≥ nợ bill; từng loại ≥ tiền DV dùng loại đó | tổng < nợ bill (→ không gạch) · thiếu 1 loại (→ không gạch cả bill) | **cọc + EVC = nợ bill (đủ), = nợ − 1 (không đủ)** | BR-GC-01 · BR-GC-02 |
| Loại cọc của dịch vụ | Master | mỗi dịch vụ dùng một loại cọc (BR-GC-03 L539) — **map dịch vụ ↔ loại cọc không test**, chỉ check có sinh đặt cọc (CL-GN-07, 19/10/2026) | — | — | BR-GC-03 (CL-GN-07) |
| Payment nhánh Cọc | Runtime | 1 dòng / (BillNumber × loại cọc), trừ cọc theo BillNumber + số hợp đồng | — | — | BR-GC-03 (CL-GN-07) |
| Tổng EVC + tiền lock của đơn | Fixture | từ API đội EVC (mock): `{tổng EVC, lock}` | API lỗi / timeout (→ chưa đặc tả, CL-GN-02) | **lock = 0 (gạch như thường)** | BR-VC · BR-GC-01 |
| Số gạch tiền khách khi có lock | Runtime | `min(nợ bill − lock, Paid khách)` — vd nợ 1.000k, lock 300k, Paid 900k → 700k | — | **Paid khách = nợ − lock − 1 / = nợ − lock / = nợ − lock + 1** | BR-VC |
| Loại đơn | Fixture | `bán mới` · `bán thêm` (cọc theo hợp đồng dùng chung) | — | — | DOC-v2.0-04 · BR-GC-01 |

(lặp bảng cho mỗi module — file này chỉ module GN)

## Ghi chú chung
- **Cột `Loại data`** (trả lời "data nào mặc định / tự tạo"):
  - **Master** = có sẵn từ hệ thống (enum paymentstatus, PaidType, danh mục loại cọc…). KHÔNG cần seed; **giá trị thực xác nhận lại ở vibe-test** (môi trường-phụ thuộc).
  - **Fixture** = test **tự tạo** (Orderpaid/Paid, tồn cọc, mock EVC…). Test chịu trách nhiệm tạo + dọn.
  - **Runtime** = sinh khi chạy (Payment, Kafka Out, trạng thái HĐ) — không cố định trước.
- Boundary values (in **đậm**) là ứng viên chính cho BVA ở generate-tc.
- Bảng verify chính: `Paid` / `Orderpaid` · `Payment` · `Ob_OrderBill` (trường Paid/Cọc) · bảng tồn cọc (tên bảng chưa có — CL-GN-10). Tiền VND không phần thập phân.
- Tool verify (`07_environments/environments.md §Tool tra cứu`): khoản thu → **Foxpay › Thanh toán online › Đối soát khoản thu online**; cọc → **Quản lý kế toán › Tiền đặt cọc › Tra cứu**; trạng thái nợ HĐ → **Quản lý kế toán › Liệt kê cước**. Gạch nợ tay (**Gạch nợ bổ sung TT online**) chỉ dùng chuẩn bị / khôi phục data, không thay luồng tự động.
- Số tiền trong cột Valid / Boundary là **dữ liệu minh họa của analyst**, không phải giá trị của URD.

### Quy ước cell (giữ nhất quán)
- **Loại data:** đúng 1 trong `Master` / `Fixture` / `Runtime` (xem Ghi chú chung). Field lấy từ danh mục hệ thống → `Master`; field test nhập/tạo → `Fixture`; field hệ thống tự sinh → `Runtime`.
- **Valid:** `value (mô tả)` — vd `ABC1234567 (10 ký tự)`, `hôm nay (default)`.
- **Invalid:** `value (→ hệ quả/MSG)` — vd `rỗng (→MSG-001)`, `"abc" (→MSG-E-002)`. Dự án không có mã MSG → ghi mô tả hệ quả (vd `rỗng (→ báo lỗi bắt buộc nhập)`).
- **Boundary:** **bold** giá trị biên + (hợp lệ/chặn) — vd `**500 ký tự (hợp lệ), 501 (chặn)**`.
- **Nguồn:** dùng **đúng ký hiệu của DOC dự án** theo `req_notation` — ở đây là `BR-…`. **KHÔNG tự bịa ID**.
- Set literal `{0=…, 1=…}`; `→` = hệ quả; `⟷` = quan hệ 2 chiều; `[…]` = ID pattern.
