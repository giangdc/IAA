---
id: v2.0/HK/test_data_catalog
title: Test Data Catalog — Module HK
type: test_data_catalog
version: v2.0
module: { code: HK, dir: HK, name: "Đẩy hậu kỳ qua dịch vụ – tiền trả trước" }
status: ANALYZED
updated: 2026-10-16
---

# Test Data Catalog — v2.0 · Module HK

> Tạo bởi: analyze-requirements (**stage: analyze** — sinh sớm để generate-tc dùng cho EP/BVA). Dữ liệu test (valid / invalid / boundary) per module, trích từ tài liệu gốc **theo đúng ký hiệu của DOC dự án** (`req_notation: BR`).
>
> **Structure-lock:** giữ nguyên 6 cột `| Field | Loại data | Valid | Invalid | Boundary | Nguồn |` cho mọi module. KHÔNG đổi cột.

## Module HK — Đẩy hậu kỳ qua dịch vụ – tiền trả trước (DOC-v2.0-01)

| Field | Loại data | Valid | Invalid | Boundary | Nguồn |
|-------|-----------|-------|---------|----------|-------|
| Invoice Event | Runtime | 1 event / hóa đơn phát hành thành công (payload chưa có) | event lặp (→ không đẩy / add lại) | — | §III.a · BR-HK-09 (CL-XHD-29) |
| Thành phần hóa đơn | Fixture | chỉ DV · chỉ TB · DV + TB | — | — | BR-HK-01 |
| Số lần phát hành của đơn | Fixture | 1 · ≥2 (DV và TB khác đợt) | — | **lần 2 chỉ đẩy phần vừa xuất** | BR-HK-01 · BR-XHD-14 |
| Ký hiệu hóa đơn điện tử | Runtime | `1K<yy>T<xx>` — hóa đơn bán mới đầu U, vd `1K26TQA` (Vùng 1) | ký hiệu sai bảng map (→ sai kê khai) | — | BR-HK-03 L581 · DOC-v2.0-02 BR-HK-03 (CL-HK-01, CL-HK-10) |
| Vùng × loại đầu → 2 ký tự cuối | Master | V1: M=`HT` U=`QA` A=`HH` · V2: `ET`/`EA`/`EH` · V3: `GT`/`GA`/`GH` · V4: `MT`/`MA`/`MH` · V5 = V1 · V6: `OT`/`OA`/`OH` · V7: `YT`/`YA`/`YH` · FPL: U=`PA` A=`PH` (không có M) | đầu số sai bảng (→ sai kê khai thuế) | **Vùng 5 (dùng chung V1) · FPL đầu M (không có)** | DOC-v2.0-02 BR-HK-03 L776-784 (CL-HK-10) |
| Loại đầu | Master | **`U` — hóa đơn bán mới và bán thêm** (phạm vi test v2.0); `M`, `A` không test | — | — | BR-HK-03 (CL-HK-01, QC owner 19/10/2026) |
| ID hóa đơn | Runtime | loại đầu + năm 2 số + mã tỉnh + số hóa đơn — vd `U26HN01053692` | mã chi nhánh thay mã tỉnh (→ sai) | — | BR-HK-03 L582 · DOC-v2.0-02 BR-HK-04 L787-792 (CL-HK-08, CL-HK-10) |
| Mã tỉnh | Master | theo danh mục tỉnh thành, lấy theo **địa chỉ hợp đồng** (vd `HN` = Hà Nội) — QC tự backup danh mục | mã chi nhánh (→ sai) | — | BR-HK-03 L582 · DOC-v2.0-02 BR-HK-04 L791 (CL-HK-08) |
| Nội dung dòng hàng | Runtime | tên dịch vụ + số tháng (SPF) | có "từ ngày – đến ngày" · tên gốc trên đơn (→ sai) | — | BR-HK-05 |
| Mức thuế suất | Master | `{KCT, 0%, 5%, 8%, 10%}` | — | **Hóa đơn chỉ 1 mức · hóa đơn đủ 5 mức** | BR-HK-07 |
| Dòng tổng theo thuế suất | Runtime | mỗi mức: thành tiền + thuế GTGT + tổng cộng; dòng tổng cộng chung = Σ các mức | — | — | BR-HK-07 |
| Dòng EVC / chiết khấu / thông tin theo mẫu | Master | *(chưa đặc tả — REQ-HK-010)* | — | — | BR-HK-02 · §D#6 (CL-HK-03, CL-HK-04) |
| Cờ đã add tiền trả trước (theo đơn) | Runtime | chưa add (→ add) · đã add (→ bỏ qua) | — | **Hóa đơn 2 cùng đơn → không add · hóa đơn chỉ thiết bị → không add (add theo hóa đơn có dịch vụ trả trước)** | BR-HK-09 (CL-HK-07) |
| Hệ thống hóa đơn điện tử / Dịch vụ (mock) | Fixture | phản hồi thành công | lỗi / timeout (→ chưa đặc tả, CL-HK-05, CL-HK-06) | — | §III.a |

(lặp bảng cho mỗi module — file này chỉ module HK)

## Ghi chú chung
- **Cột `Loại data`** (trả lời "data nào mặc định / tự tạo"):
  - **Master** = có sẵn từ hệ thống (danh mục tỉnh – vùng, bảng map ký hiệu, mức thuế suất…). KHÔNG cần seed; **giá trị thực xác nhận lại ở vibe-test** (môi trường-phụ thuộc).
  - **Fixture** = test **tự tạo** (đơn / hóa đơn có thành phần cần thiết, mock hóa đơn điện tử / Dịch vụ). Test chịu trách nhiệm tạo + dọn.
  - **Runtime** = sinh khi chạy (ký hiệu, ID hóa đơn, payload đẩy, cờ đã add) — không cố định trước.
- Boundary values (in **đậm**) là ứng viên chính cho BVA ở generate-tc.
- Bảng map ký hiệu lấy theo URD 2.1 BR-HK-03 (dùng cho Phụ lục D#5 từ 19/10/2026). Phạm vi test chỉ hóa đơn bán mới đầu U (CL-HK-01) — cột M, A của bảng map chỉ để tham chiếu. Dòng chiết khấu không test (CL-HK-03).
- Tool verify (`07_environments/environments.md §Tool tra cứu`): tiền trả trước → **Quản lý kế toán › Cước trả trước › Tra cứu new**; hóa đơn → **Quản lý kế toán › Liệt kê cước**.

### Quy ước cell (giữ nhất quán)
- **Loại data:** đúng 1 trong `Master` / `Fixture` / `Runtime` (xem Ghi chú chung). Field lấy từ danh mục hệ thống → `Master`; field test nhập/tạo → `Fixture`; field hệ thống tự sinh → `Runtime`.
- **Valid:** `value (mô tả)` — vd `ABC1234567 (10 ký tự)`, `hôm nay (default)`.
- **Invalid:** `value (→ hệ quả/MSG)` — vd `rỗng (→MSG-001)`, `"abc" (→MSG-E-002)`. Dự án không có mã MSG → ghi mô tả hệ quả (vd `rỗng (→ báo lỗi bắt buộc nhập)`).
- **Boundary:** **bold** giá trị biên + (hợp lệ/chặn) — vd `**500 ký tự (hợp lệ), 501 (chặn)**`.
- **Nguồn:** dùng **đúng ký hiệu của DOC dự án** theo `req_notation` — ở đây là `BR-…`. **KHÔNG tự bịa ID**.
- Set literal `{0=…, 1=…}`; `→` = hệ quả; `⟷` = quan hệ 2 chiều; `[…]` = ID pattern.
