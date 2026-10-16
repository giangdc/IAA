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
| Invoice Event | Runtime | 1 event / HĐ phát hành thành công (payload chưa có) | event lặp (→ không đẩy / add lại) | — | §III.a · BR-HK-09 (CL-XHD-29) |
| Thành phần HĐ | Fixture | chỉ DV · chỉ TB · DV + TB | — | — | BR-HK-01 |
| Số lần phát hành của đơn | Fixture | 1 · ≥2 (DV và TB khác đợt) | — | **lần 2 chỉ đẩy phần vừa xuất** | BR-HK-01 · BR-XHD-14 |
| Ký hiệu HĐĐT (7 ký tự) | Runtime | `1K<yy>T<xx>` — vd `1K26TQA` (giả định bảng 2.1) | `<xx>` sai bảng map (→ sai kê khai) | — | BR-HK-03 · DOC-v2.0-02 L769-774 (CL-HK-01) |
| Vùng × loại đầu → 2 ký tự cuối | Master | Vùng 1 `M=HT U=QA A=HH` · Vùng 2 `ET EA EH` · Vùng 3 `GT GA GH` · Vùng 4 `MT MA MH` · Vùng 5 = Vùng 1 · Vùng 6 `OT OA OH` · Vùng 7 `YT YA YH` · FPL `U=PA A=PH` (giả định 2.1) | tỉnh không thuộc vùng nào (→ thiếu thông tin, chưa đẩy) | **Vùng 5 dùng chung Vùng 1 · FPL không có đầu M** | DOC-v2.0-02 L776-784 (CL-HK-01, CL-HK-02) |
| Loại đầu | Master | `M` · `U` · `A` — theo loại HĐ (map loại HĐ → đầu chưa có) | — | — | DOC-v2.0-02 L775 (CL-HK-01) |
| ID HĐ | Runtime | `<đầu><yy><mã tỉnh><số HĐ>` — vd `U26HN01053692` | mã chi nhánh thay mã tỉnh (→ sai) | — | BR-HK-03 · DOC-v2.0-02 L788-792 (CL-HK-08) |
| Mã tỉnh | Master | theo danh mục tỉnh thành (vd `HN`) | — | — | DOC-v2.0-02 L791 (CL-HK-08) |
| Nội dung dòng hàng | Runtime | tên dịch vụ + số tháng (SPF) | có "từ ngày – đến ngày" · tên gốc trên đơn (→ sai) | — | BR-HK-05 |
| Mức thuế suất | Master | `{KCT, 0%, 5%, 8%, 10%}` | — | **HĐ chỉ 1 mức · HĐ đủ 5 mức** | BR-HK-07 |
| Dòng tổng theo thuế suất | Runtime | mỗi mức: thành tiền + thuế GTGT + tổng cộng; dòng tổng cộng chung = Σ các mức | — | — | BR-HK-07 |
| Dòng EVC / chiết khấu / thông tin theo mẫu | Master | *(chưa đặc tả — REQ-HK-010)* | — | — | BR-HK-02 · §D#6 (CL-HK-03, CL-HK-04) |
| Cờ đã add tiền trả trước (theo đơn) | Runtime | chưa add (→ add) · đã add (→ bỏ qua) | — | **HĐ2 cùng đơn → không add** | BR-HK-09 (CL-HK-07) |
| Hệ thống HĐĐT / Dịch vụ (mock) | Fixture | phản hồi thành công | lỗi / timeout (→ chưa đặc tả, CL-HK-05, CL-HK-06) | — | §III.a |

(lặp bảng cho mỗi module — file này chỉ module HK)

## Ghi chú chung
- **Cột `Loại data`** (trả lời "data nào mặc định / tự tạo"):
  - **Master** = có sẵn từ hệ thống (danh mục tỉnh – vùng, bảng map ký hiệu, mức thuế suất…). KHÔNG cần seed; **giá trị thực xác nhận lại ở vibe-test** (môi trường-phụ thuộc).
  - **Fixture** = test **tự tạo** (đơn / HĐ có thành phần cần thiết, mock HĐĐT / Dịch vụ). Test chịu trách nhiệm tạo + dọn.
  - **Runtime** = sinh khi chạy (ký hiệu, ID HĐ, payload đẩy, cờ đã add) — không cố định trước.
- Boundary values (in **đậm**) là ứng viên chính cho BVA ở generate-tc.
- ⚠️ Bảng map ký hiệu là của **URD 2.1** — giả định tới khi CL-HK-01 trả lời. Full quote: `../quotes/REQ-HK-005.md`.

### Quy ước cell (giữ nhất quán)
- **Loại data:** đúng 1 trong `Master` / `Fixture` / `Runtime` (xem Ghi chú chung). Field lấy từ danh mục hệ thống → `Master`; field test nhập/tạo → `Fixture`; field hệ thống tự sinh → `Runtime`.
- **Valid:** `value (mô tả)` — vd `ABC1234567 (10 ký tự)`, `hôm nay (default)`.
- **Invalid:** `value (→ hệ quả/MSG)` — vd `rỗng (→MSG-001)`, `"abc" (→MSG-E-002)`. Dự án không có mã MSG → ghi mô tả hệ quả (vd `rỗng (→ báo lỗi bắt buộc nhập)`).
- **Boundary:** **bold** giá trị biên + (hợp lệ/chặn) — vd `**500 ký tự (hợp lệ), 501 (chặn)**`.
- **Nguồn:** dùng **đúng ký hiệu của DOC dự án** theo `req_notation` — ở đây là `BR-…`; nội dung chỉ có ở 2.1 ghi `DOC-v2.0-02 L…`. **KHÔNG tự bịa ID**.
- Set literal `{0=…, 1=…}`; `→` = hệ quả; `⟷` = quan hệ 2 chiều; `[…]` = ID pattern.
