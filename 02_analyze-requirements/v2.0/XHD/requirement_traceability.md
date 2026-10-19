---
id: v2.0/XHD/requirement_traceability
title: Requirement Traceability — Module XHD
type: requirement_traceability
version: v2.0
module: { code: XHD, dir: XHD, name: "Đồng bộ đơn hàng & xuất hóa đơn tự động" }
doc_source:
  - id: DOC-v2.0-01
    section: "§A.1 · §A.2 · §A.3 · §A.5 · §B.I · §C · §D"
  - id: DOC-v2.0-04
    section: "mail PM 13/10/2026"
  - id: DOC-v2.0-05
    section: "sheet \"1. HT Triển khai\""
status: ANALYZED
updated: 2026-10-16
---

# Requirement Traceability — v2.0 · Module XHD

> Tạo bởi: analyze-requirements. Ma trận truy vết REQ ↔ DOC ↔ Scenario ↔ Clarification.
> **Layout v2** — quote REQ ở **§2** file này; quote SC ở `test_scenario_map.md`; CL ở `risk_assessment.md`.
> `req_notation: BR` ⇒ **Schema A**, cột `Maps (Ref DOC)` dùng nguyên văn ID `BR-…` của URD. Requirement không có BR (bảng phạm vi §A, phụ lục §D, mail PM) ghi `—` ở cột này và neo bằng `DOC §section`.
> 📍 `L<n>` = số dòng trong bản trích text của `.docx` do `scripts/doc/search-doc.sh` sinh ra — tra lại bằng
> `DOC_DIR=00_input/v2.0/Doc DOC_DEFAULT="Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx" scripts/doc/search-doc.sh "<từ khoá>"`.

## 1. Traceability Matrix (REQ → DOC → SC)

### Schema A — Module XHD — DOC-v2.0-01

| REQ ID | Maps (Ref DOC) | DOC §section | Scenarios | Clarification |
|--------|----------------|--------------|-----------|---------------|
| REQ-XHD-001 | — | DOC-v2.0-01 §A.2 (L79-137) | SC-XHD-001..017 | CL-XHD-26 |
| REQ-XHD-002 | — | DOC-v2.0-01 §A.3 (L138-260) | SC-XHD-001..017 (chiều dữ liệu nhóm DV) | CL-XHD-12, CL-XHD-13, CL-XHD-26, CL-XHD-30 |
| REQ-XHD-003 | BR-DB-01 | DOC-v2.0-01 §I.c (L343-346) | SC-XHD-018, SC-XHD-019, SC-XHD-020 | CL-XHD-01 |
| REQ-XHD-004 | BR-DB-02 | DOC-v2.0-01 §I.c (L347-350) | SC-XHD-021, SC-XHD-022, SC-XHD-023, SC-XHD-024 | CL-XHD-27 |
| REQ-XHD-005 | BR-DB-02 | DOC-v2.0-01 §I.c (L351) | SC-XHD-029 | CL-XHD-31 |
| REQ-XHD-006 | BR-DB-03 | DOC-v2.0-01 §I.c (L355) | SC-XHD-030 | — |
| REQ-XHD-007 | BR-DB-03 | DOC-v2.0-01 §I.c (L356-358) | SC-XHD-031, SC-XHD-032, SC-XHD-033, SC-XHD-034 | CL-XHD-02, CL-XHD-03 |
| REQ-XHD-008 | BR-DB-03 | DOC-v2.0-01 §I.c (L359) | SC-XHD-035, SC-XHD-036 | CL-XHD-01 |
| REQ-XHD-009 | BR-DB-04 | DOC-v2.0-01 §I.c (L361-364) | SC-XHD-037 | CL-XHD-13 |
| REQ-XHD-010 | BR-DB-05 | DOC-v2.0-01 §I.c (L366-369) | SC-XHD-038, SC-XHD-039 | — |
| REQ-XHD-011 | BR-DB-05 | DOC-v2.0-01 §I.c (L370) | SC-XHD-040 | CL-XHD-29 |
| REQ-XHD-012 | BR-DB-07 | DOC-v2.0-01 §I.c (L372-374) | SC-XHD-021, SC-XHD-028 | CL-XHD-11 |
| REQ-XHD-013 | BR-DB-07 | DOC-v2.0-01 §I.c (L375-376) | SC-XHD-025, SC-XHD-026, SC-XHD-027 | CL-XHD-19 |
| REQ-XHD-014 | BR-XHD-01 | DOC-v2.0-01 §I.c (L378-383) | SC-XHD-041, SC-XHD-042, SC-XHD-043, SC-XHD-044 | — |
| REQ-XHD-015 | BR-XHD-01 | DOC-v2.0-01 §I.c (L384) | SC-XHD-042, SC-XHD-045, SC-XHD-111 | CL-XHD-22, CL-XHD-32 |
| REQ-XHD-016 | BR-XHD-01 | DOC-v2.0-01 §I.c (L385) | SC-XHD-046 | CL-XHD-06 ✅, CL-XHD-32 |
| REQ-XHD-017 | BR-XHD-01 | DOC-v2.0-01 §I.c (L386-388) | SC-XHD-047, SC-XHD-048 | CL-XHD-05 |
| REQ-XHD-018 | BR-XHD-02 | DOC-v2.0-01 §I.c (L390-393) | SC-XHD-054, SC-XHD-055, SC-XHD-056 | — |
| REQ-XHD-019 | BR-XHD-03 | DOC-v2.0-01 §I.c (L397) | SC-XHD-057, SC-XHD-058, SC-XHD-059, SC-XHD-110 | CL-XHD-10 ✅ |
| REQ-XHD-020 | BR-XHD-03 | DOC-v2.0-01 §I.c (L398) | SC-XHD-060 | CL-XHD-31 |
| REQ-XHD-021 | BR-XHD-03 | DOC-v2.0-01 §I.c (L399) | SC-XHD-049, SC-XHD-050, SC-XHD-053 | CL-XHD-04 |
| REQ-XHD-022 | BR-XHD-03 | DOC-v2.0-01 §I.c (L400) | SC-XHD-061, SC-XHD-062, SC-XHD-063, SC-XHD-064, SC-XHD-065, SC-XHD-068 | CL-XHD-07, CL-XHD-09 ✅ |
| REQ-XHD-023 | BR-XHD-03 | DOC-v2.0-01 §I.c (L401) | SC-XHD-066, SC-XHD-067 | CL-XHD-08 |
| REQ-XHD-024 | BR-XHD-05 | DOC-v2.0-01 §I.c (L404-408) | SC-XHD-069, SC-XHD-070, SC-XHD-071, SC-XHD-072 | — |
| REQ-XHD-025 | BR-XHD-06 | DOC-v2.0-01 §I.c (L410-413) | SC-XHD-073, SC-XHD-074, SC-XHD-075, SC-XHD-110 | CL-XHD-10 ✅ |
| REQ-XHD-026 | BR-XHD-06 | DOC-v2.0-01 §I.c (L414) | SC-XHD-051, SC-XHD-052 | CL-XHD-05 |
| REQ-XHD-027 | BR-XHD-08 | DOC-v2.0-01 §I.c (L416-421) | SC-XHD-076, SC-XHD-077, SC-XHD-078, SC-XHD-079 | CL-XHD-11, CL-XHD-12, CL-XHD-23 |
| REQ-XHD-028 | BR-XHD-10 | DOC-v2.0-01 §I.c (L425) | SC-XHD-019, SC-XHD-080, SC-XHD-081 | CL-XHD-14 |
| REQ-XHD-029 | BR-XHD-10 | DOC-v2.0-01 §I.c (L426) | SC-XHD-082..089 | CL-XHD-14, CL-XHD-15 |
| REQ-XHD-030 | BR-XHD-10 | DOC-v2.0-01 §I.c (L427) | SC-XHD-090..095 | CL-XHD-15 |
| REQ-XHD-031 | BR-XHD-10 | DOC-v2.0-01 §I.c (L428) | SC-XHD-080..096, SC-XHD-111 | CL-XHD-15, CL-XHD-17 ✅ |
| REQ-XHD-032 | BR-XHD-10 | DOC-v2.0-01 §I.c (L429) | SC-XHD-097 | CL-XHD-16 |
| REQ-XHD-033 | BR-XHD-10 | DOC-v2.0-01 §I.c (L430) | — *(⛔ ngoài scope test — TP §2.2 #2; SC-XHD-098 deprecated 19/10/2026)* | — |
| REQ-XHD-034 | BR-XHD-12 | DOC-v2.0-01 §I.c (L432-435) | SC-XHD-099 *(SC-XHD-100 ⛔ ngoài scope test — TP §2.2 #3, deprecated 19/10/2026)* | — |
| REQ-XHD-035 | BR-XHD-13 | DOC-v2.0-01 §I.c (L437-440) | SC-XHD-101, SC-XHD-104 | CL-XHD-18 |
| REQ-XHD-036 | BR-XHD-13 | DOC-v2.0-01 §I.c (L441) | SC-XHD-102 | CL-XHD-28 |
| REQ-XHD-037 | BR-XHD-13 | DOC-v2.0-01 §I.c (L442) | SC-XHD-103 | CL-XHD-29 |
| REQ-XHD-038 | BR-XHD-14 | DOC-v2.0-01 §I.c (L444-447) | SC-XHD-105 | — |
| REQ-XHD-039 | BR-XHD-18 | DOC-v2.0-01 §I.c (L449-452) | — *(chờ đặc tả — CHANGELOG §3)* | CL-XHD-21 |
| REQ-XHD-040 | — | DOC-v2.0-04 (mail PM) | SC-XHD-106 | CL-XHD-25 |
| REQ-XHD-041 | — | DOC-v2.0-01 §D#1 (L658-661) | SC-XHD-107, SC-XHD-108 *(dùng lại 19/10/2026 — URD 2.1 BR-DB-08)* | CL-XHD-24, CL-XHD-33 |
| REQ-XHD-042 | — | DOC-v2.0-01 §D#3 (L666-669) | — *(chờ đặc tả — CHANGELOG §3)* | CL-XHD-22, CL-XHD-33 |
| REQ-XHD-043 | — | DOC-v2.0-05 sheet "1. HT Triển khai" · dòng 1–8 | SC-XHD-109 | CL-XHD-27 |

> **Cột `DOC §section` = neo audit chính.** `§I.c` = mục B.I "Đồng bộ đơn hàng và xuất hóa đơn tự động" → c. Business rules.
> REQ-XHD-039 và REQ-XHD-042 **chưa có SC có chủ đích**: URD chỉ có 1 câu / chỉ nêu "bắt buộc", không đủ để viết Given/When/Then — ghi ở `CHANGELOG.md §3`.

## 2. Requirement Source Detail (verbatim quotes — home của REQ quote)

### REQ-XHD-001 · Phạm vi 17 kênh bán (SaleChannelID)
📍 `DOC-v2.0-01 §A.2 "Phạm vi kênh bán" · L79-137 · bảng SaleChannelID`  ·  Clarif: `CL-XHD-26`

> Tất cả kênh bán trong danh sách dưới đây thuộc phạm vi. Phase 1 đã triển khai Shopee và Tiktok.
> (...)
> | SaleChannelID | Tên kênh | Mô tả | Ghi chú |
> |---|---|---|---|
> | 1 | Mobile | Mobile | |
> | 2 | Desktop | Desktop | |
> | 4 | DKOL | DKOL | |
> | 7 | API | Dùng cho các partner ngoài FTEL (TGDD,..) | |
> | 9 | W-Sale | W-Sale | |
> | 10 | FPL | FPT Play | |
> | 11 | VNTT | VNTT | |
> | 12 | MBBank | MB Bank | |
> | 13 | CRM | CRM | |
> | 14 | TGDD | Thế Giới Di Động | |
> | 15 | F-Retail | FPT Shop | |
> | 16 | CMR-App | FSS | |
> | 17 | Momo | Momo | |
> | 18 | SR-KPDV | SR KPDV | |
> | 19 | HiFPT | HiFPT | |
> | 20 | Shopee | Shopee | Đã triển khai ver1.0Có điều chinh ver2.0 |
> | 21 | Tiktok | Tiktok | Đã triển khai v1.0Có điều chỉnh v2.0 |

↳ **Ghi chú:** 17 kênh có đơn SPF đều phải xuất HĐ tự động. Kênh 20, 21 là luồng Phase 1 ⇒ vừa là test mới vừa là **hồi quy**. URD chỉ liệt kê kênh và nhóm DV riêng rẽ, **không có ma trận kênh nào bán nhóm DV nào** (CL-XHD-26 / GAP-62) ⇒ test plan đang giả định đủ 17 × 20 × 2 loại đơn. Implicit: SaleChannelID ngoài 17 giá trị trên (vd 3, 5, 6, 8) không thuộc phạm vi — URD không nói hệ thống xử lý chúng ra sao.

---

### REQ-XHD-002 · Phạm vi 20 nhóm / 55 dịch vụ; loại ServiceID 2 và 22
📍 `DOC-v2.0-01 §A.3 "Phạm vi nhóm dịch vụ và dịch vụ" · L138-260 · bảng ServiceID`  ·  Clarif: `CL-XHD-12`, `CL-XHD-13`, `CL-XHD-26`, `CL-XHD-30`

> Các nhóm dịch vụ và dịch vụ trong danh sách dưới đây thuộc phạm vi (20 nhóm, 55 dịch vụ). Mỗi dịch vụ ghi theo dạng SubServiceType – Tên dịch vụ (Type).
> (...)
> Ô màu vàng: SubServiceType 31 trùng ở hai dịch vụ (Thiết bị Oncall, Thiết bị IP phone) của nhóm Tổng đài Oncall.
> Không có trong danh sách phạm vi: ServiceID 2 (SubServiceType 5 đến 9) vì không có trong bảng nhóm dịch vụ; ServiceID 22 (GSafe) vì chưa có dịch vụ nào.

↳ **Ghi chú:** Bảng đầy đủ 20 nhóm × SubServiceType nằm ở `test_data_catalog.md` (field `ServiceID / SubServiceType`) — không chép lại ở đây. Mỗi dịch vụ có cột `Type 1..4`; URD **chưa định nghĩa** Type và cách map sang ProductType DV/TB (§C#2 → CL-XHD-13). SubServiceType 31 trùng ở 2 dịch vụ ảnh hưởng khóa chống trùng (§C#3 → CL-XHD-12). Hai cột "Loại nhóm" `Billing` / `SubScription` chưa được BR nào dùng — **suy diễn của analyst:** chỉ mang tính mô tả.

---

### REQ-XHD-003 · Sự kiện đồng bộ từ SPF: thanh toán, hủy đơn
📍 `DOC-v2.0-01 §I.c BR-DB-01 · L343-346`  ·  Clarif: `CL-XHD-01`

> Áp dụng chung cho mọi kênh bán: thanh toán, hủy đơn hàng.

↳ **Ghi chú:** 2.2 chỉ còn **2 sự kiện**. Nhưng BR-DB-03 vẫn nói "Cập nhật thông tin khách" và BR-XHD-03 lấy mốc "thời gian tạo đơn" ⇒ doc tự mâu thuẫn (CL-XHD-01 / GAP-42). Test chắc chắn được 2 sự kiện ghi trong BR; 2 sự kiện còn lại chờ CL-XHD-01.

---

### REQ-XHD-004 · Tín hiệu giao hàng hoàn tất từ 3 nguồn độc lập
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L347-350`  ·  Clarif: `CL-XHD-27`

> Tín hiệu đi thẳng về INVOICE từ 3 nguồn độc lập: phiếu thi công (tình trạng "Đã xử lý hoàn tất"), Vendor (khi đối tác giao xong), phiếu giao tại quầy.
> Tín hiệu gồm mã đơn, ServiceCode, SubserviceType, phương thức triển khai, nguồn gửi và thời gian hoàn tất.

↳ **Ghi chú:** 3 nguồn = 3 lớp EP. Tín hiệu **không đi qua đơn hàng SPF**. 6 trường của tín hiệu là căn cứ verify dữ liệu ghi nhận. `DOC-v2.0-05` (file HT Triển khai) liệt kê 8 hình thức (TIN/PNC, TIN/PNC giao hàng, Quầy, Sale, NCC Samsung/Sony/Casper, FTI, Không) — **suy diễn của analyst** về map sang 3 nguồn: TIN/PNC + FTI → phiếu thi công · NCC → Vendor · Quầy + Sale → phiếu giao tại quầy · "Không" → không có tín hiệu (CL-XHD-27).

---

### REQ-XHD-005 · Đơn TMĐT: tín hiệu thanh toán = SPF đánh dấu "đã thanh toán", Paid ở trạng thái gạch nợ tạm
📍 `DOC-v2.0-01 §I.c BR-DB-02 · L351`  ·  Clarif: `CL-XHD-31`

> Với đơn TMĐT, tín hiệu hoàn tất thanh toán là lúc SPF đánh dấu đơn "đã thanh toán"; cùng lúc đó Paid được ghi nhận ở trạng thái gạch nợ tạm.

↳ **Ghi chú:** Điểm nối XHD ↔ GN cho kênh sàn (20, 21): cùng một mốc vừa kích hoạt xuất HĐ phần DV vừa sinh Paid tạm (gạch nợ tạm ở `GN/` REQ-GN-009). Hành vi Phase 1 giữ hay đổi chưa có căn cứ vì chưa nhận URD v1.0 (CL-XHD-31 / GAP-24).

---

### REQ-XHD-006 · Thông tin khách xuất HĐ mặc định theo hợp đồng
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L355`  ·  Clarif: —

> Mặc định lấy theo thông tin trên hợp đồng.

↳ **Ghi chú:** Mọi kênh trừ ngoại lệ FPL (REQ-XHD-007): tên, địa chỉ, MST… in trên HĐ lấy từ hợp đồng, không lấy từ đơn hàng.

---

### REQ-XHD-007 · FPL: khách chọn lấy HĐ và tự nhập thông tin trong tối đa 2 giờ
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L356-358`  ·  Clarif: `CL-XHD-02`, `CL-XHD-03`

> Ngoại lệ: kênh bán FPL cho khách chọn có lấy hóa đơn hay không (ví dụ FPL).
> Nếu khách chọn lấy hóa đơn thì dùng thông tin khách tự nhập: tên, email, số điện thoại, mã số thuế, mã định danh, mã quan hệ ngân sách, số hộ chiếu.
> Khách được nhập thông tin trong tối đa 2 giờ, tính từ thời điểm ghi nhận trên hệ thống của kênh.

↳ **Ghi chú:** 7 trường khách nhập. Câu "(ví dụ FPL)" để ngỏ khả năng có kênh khác. Nhánh "khách **không** lấy HĐ" và "quá 2 giờ không nhập" **không có đầu ra** (CL-XHD-02 / GAP-48). Trường nào bắt buộc, định dạng ra sao, ai kiểm tra: chưa đặc tả (CL-XHD-03 / GAP-49). Mốc 2 giờ "từ thời điểm ghi nhận trên hệ thống của kênh" khác mốc delay 2h "theo thời gian tạo đơn" của BR-XHD-03 (CL-XHD-04). **Cập nhật 16/10/2026:** ngoại lệ chỉ áp kênh FPL (CL-XHD-02); 2 mốc 2 giờ là 2 việc khác nhau — hạn nhập thông tin ≠ delay xuất HĐ (CL-XHD-04).

---

### REQ-XHD-008 · Cập nhật thông tin khách không kích hoạt phát hành; lần sau dùng thông tin mới nhất
📍 `DOC-v2.0-01 §I.c BR-DB-03 · L359`  ·  Clarif: `CL-XHD-01`

> Cập nhật thông tin khách không kích hoạt phát hành hóa đơn; lần phát hành tiếp theo dùng thông tin mới nhất.

↳ **Ghi chú:** 2 hành vi: (1) không phát sinh HĐ ngay khi cập nhật; (2) HĐ của đợt kế tiếp in thông tin mới. Nguồn của sự kiện "cập nhật thông tin khách" không còn trong BR-DB-01 (CL-XHD-01).

---

### REQ-XHD-009 · Phân loại DV/TB theo ProductType do SPF gắn
📍 `DOC-v2.0-01 §I.c BR-DB-04 · L361-364`  ·  Clarif: `CL-XHD-13`

> SPF gắn sẵn ProductType (DV/TB) trên từng dòng chi tiết khi đồng bộ đơn.
> INVOICE dùng trường này, không tự suy diễn.

↳ **Ghi chú:** INVOICE không được suy DV/TB từ ServiceID/SubServiceType/Type. Test: dòng mang ProductType nào thì đi đúng điều kiện phát hành của loại đó. Quan hệ giữa cột `Type 1..4` (§A.3) và ProductType chưa rõ (CL-XHD-13).

---

### REQ-XHD-010 · Ghi nhận theo lần đẩy cuối; chỉ xuất phần chưa có HĐ
📍 `DOC-v2.0-01 §I.c BR-DB-05 · L366-369`  ·  Clarif: —

> Một đơn có thể được đồng bộ nhiều lần; lần đẩy cuối là thông tin mới nhất.
> Chỉ xuất hóa đơn cho phần chưa có hóa đơn; phần đã xuất không bị ghi đè, xóa hay phát hành lại.

↳ **Ghi chú:** Bản tin sau ghi đè thông tin **phần chưa xuất**; phần đã có BillNumber bất biến. Liên quan chống trùng REQ-XHD-027.

---

### REQ-XHD-011 · Ghi thời điểm nhận mỗi bản tin để phân luồng
📍 `DOC-v2.0-01 §I.c BR-DB-05 · L370`  ·  Clarif: `CL-XHD-29`

> INVOICE ghi lại thời điểm nhận mỗi bản tin để phân luồng worker hoặc realtime.

↳ **Ghi chú:** Mốc này là căn cứ của realtime (REQ-XHD-018). Tên cột lưu chưa có vì thiếu schema (CL-XHD-29 / GAP-07).

---

### REQ-XHD-012 · Map tín hiệu giao hàng vào thiết bị theo bộ khóa 4 thành phần
📍 `DOC-v2.0-01 §I.c BR-DB-07 · L372-374`  ·  Clarif: `CL-XHD-11`

> Map theo bộ khóa mã đơn + ServiceCode + SubserviceType + phương thức triển khai, cho phần thiết bị chưa xuất hóa đơn.

↳ **Ghi chú:** Phải khớp đủ 4 thành phần. Khóa map tín hiệu vẫn dùng SubserviceType trong khi khóa chống trùng BR-XHD-08 đã đổi sang "dịch vụ hóa đơn + Gói dịch vụ" (CL-XHD-11).

---

### REQ-XHD-013 · Tín hiệu không khớp / TB đã có HĐ: không ghi nhận, log vào cột Note; không ràng buộc nguồn
📍 `DOC-v2.0-01 §I.c BR-DB-07 · L375-376`  ·  Clarif: `CL-XHD-19`

> Nếu thiết bị đã có hóa đơn hoặc không khớp khóa thì không ghi nhận, chỉ ghi log nội dung tín hiệu vào cột Note.
> Nguồn gửi được lưu lại để đối soát; không ràng buộc nguồn nào được báo cho phương thức triển khai nào.

↳ **Ghi chú:** 2 nhánh negative (đã có HĐ · không khớp khóa) cùng đầu ra "log cột Note". Cột Note thuộc bảng nào, format ra sao: chưa đặc tả (CL-XHD-19 / GAP-27) ⇒ expected chỉ kiểm được "có log chứa nội dung tín hiệu". Nguồn bất kỳ báo cho phương thức bất kỳ đều hợp lệ.

---

### REQ-XHD-014 · Lịch xuất HĐ dạng tham số: 2 đợt 12:00/12:05 và 18:00/18:05 cho mọi kênh khác FPL
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L378-383`  ·  Clarif: —

> Dùng chung một lịch cho mọi ngày và mọi kênh bán khác FPL
> Mỗi đợt gồm giờ chốt và giờ chạy worker; số đợt cũng là tham số.
> Giá trị áp dụng: chia 2 đợt, đợt 1 chốt 12:00 chạy 12:05; đợt 2 chốt 18:00 chạy 18:05
> Sau giai đoạn pilot sẽ đánh giá lại; nếu cần thì cấu hình lại tham số worker.

↳ **Ghi chú:** Số đợt, giờ chốt, giờ chạy đều là **tham số** — TC ghi theo "giờ chốt của đợt", ⛔ không hardcode giá trị (Project_rule §Test Data Rules). Bỏ phân biệt ngày thường / cuối tháng của Phase 1.

---

### REQ-XHD-015 · Mỗi đợt quét dòng chưa xuất có mốc nghiệp vụ trong ngày, trước giờ chốt
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L384`  ·  Clarif: `CL-XHD-22`

> Mỗi đợt quét các dòng chưa xuất hóa đơn có mốc nghiệp vụ trong ngày, trước giờ chốt của đợt.

↳ **Ghi chú:** Không có chặn dưới giữa các đợt trong ngày. Dòng có mốc nghiệp vụ **ngày trước** không được đợt nào lấy — khoảng trống D#3 (CL-XHD-22).

---

### REQ-XHD-016 · Đủ điều kiện sau giờ chốt cuối của ngày cuối tháng → phát hành sang tháng sau
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L385`  ·  Clarif: `CL-XHD-06`

> Đơn đủ điều kiện sau giờ chốt cuối của ngày cuối tháng sẽ phát hành sang tháng sau, ảnh hưởng kỳ ghi nhận doanh thu.

↳ **Ghi chú:** Câu này mâu thuẫn với realtime "xử lý ngay khi nhận" (BR-XHD-06): sau giờ chốt cuối thì realtime chạy ngay trong ngày ⇒ HĐ vẫn thuộc tháng này? (CL-XHD-06 / GAP-43). Test plan giả định realtime vẫn chạy. **Cập nhật 16/10/2026:** CL-XHD-06 chốt theo đúng câu này — sau giờ chốt cuối ngày cuối tháng không phát hành trong tháng; đợt phát hành ở tháng sau: CL-XHD-32.

---

### REQ-XHD-017 · Kênh FPL: worker 2 giờ/lần + mốc 22:05 chốt 0h–22h
📍 `DOC-v2.0-01 §I.c BR-XHD-01 · L386-388`  ·  Clarif: `CL-XHD-05`

> Xét riêng cho kênh bán FPL:
> 2h quét 1 lần
> Mốc 22:05 chốt từ 0h đến 22 giờ (Do FPL có rule delay 2h nên phải bổ sung khung giờ để quét hết những case không quét được do delay ở hai khung giờ trước)

↳ **Ghi chú:** Không nêu giờ bắt đầu, giờ chốt từng đợt 2h, có phải tham số không (CL-XHD-05 / GAP-50). "Hai khung giờ trước" có thể hiểu là 2 đợt chung 12:05/18:05 hoặc 2 đợt FPL liền trước — suy diễn của analyst, chưa chắc. Test plan giả định các mốc 0:05, 2:05 … 22:05. **Cập nhật 16/10/2026:** lịch FPL thuộc BR "Lịch xuất hóa đơn (tham số cấu hình)" (L379) và flow FIG-03 (ảnh: Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png) ghi giờ chốt / giờ chạy là tham số; còn mở giờ các đợt trước 22:05 (CL-XHD-05).

---

### REQ-XHD-018 · Phân luồng worker / realtime theo giờ chốt
📍 `DOC-v2.0-01 §I.c BR-XHD-02 · L390-393`  ·  Clarif: —

> Tín hiệu về trước giờ chốt của đợt thì xử lý ở worker; về sau giờ chốt cuối trong ngày thì xử lý ở realtime.
> Worker lọc theo mốc nghiệp vụ, realtime lọc theo thời điểm nhận tín hiệu, hai luồng không trùng nhau.

↳ **Ghi chú:** 3 vùng thời gian: trước giờ chốt đợt 1 · giữa các đợt (vẫn worker, đợt kế) · sau giờ chốt cuối (realtime). Với FPL ranh giới realtime là 22h (REQ-XHD-026).

---

### REQ-XHD-019 · Điều kiện phát hành: DV khi đã thanh toán; TB khi giao hàng hoàn tất theo phương thức
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L397`  ·  Clarif: `CL-XHD-10`

> Dịch vụ: khi có tín hiệu "đã thanh toán" từ SPF. Thiết bị: khi có tín hiệu giao hàng hoàn tất của phương thức triển khai tương ứng (phiếu thi công, Vendor, quầy). Hai điều kiện xét độc lập và dùng chung cho mọi kênh bán.

↳ **Ghi chú:** DV và TB có đường ra HĐ riêng. Hệ quả có chủ đích: DV chưa thanh toán thì không phát hành dù TB đã giao. 2.2 bỏ BR-XHD-04 (autobill TB theo phương thức, D#9) nhưng thuật ngữ #3 và câu này vẫn dùng "phương thức triển khai tương ứng" (CL-XHD-10 / GAP-54). **Cập nhật 16/10/2026:** CL-XHD-10 chốt — chỉ phát hành TB có trong tín hiệu (SC-XHD-110).

---

### REQ-XHD-020 · Đơn TMĐT: DV khi SPF đánh dấu "đã thanh toán"; TB khi giao hàng thành công
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L398`  ·  Clarif: `CL-XHD-31`

> Đơn TMĐT: dịch vụ khi SPF đánh dấu đơn "đã thanh toán"; thiết bị khi giao hàng thành công.

↳ **Ghi chú:** Hồi quy Phase 1 cho kênh 20, 21. "Giao hàng thành công" của đơn TMĐT đi qua nguồn tín hiệu nào trong 3 nguồn BR-DB-02: URD không nói.

---

### REQ-XHD-021 · Kênh FPL: xét delay 2 giờ theo thời gian tạo đơn
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L399`  ·  Clarif: `CL-XHD-04`

> Kênh bán FPL: Xét delay 2h (lấy chuẩn theo thời gian tạo đơn)

↳ **Ghi chú:** Đơn FPL chỉ đủ điều kiện phát hành khi đã qua 2 giờ kể từ tạo đơn — **suy diễn của analyst:** delay để chờ khách nhập thông tin HĐ (REQ-XHD-007). Áp cho DV hay cả TB, và mốc "tạo đơn" có trùng "thời điểm ghi nhận trên hệ thống của kênh" không: CL-XHD-04 / GAP-51.

---

### REQ-XHD-022 · Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK, trừ 2 ngày cuối tháng
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L400`  ·  Clarif: `CL-XHD-07`, `CL-XHD-09`

> Hợp đồng tổ chức: chỉ phát hành khi đã duyệt PĐK; hai ngày cuối tháng không xét điều kiện này. Quên duyệt PĐK thì không autobill. Khi có thay đổi hoặc dịch chuyển luồng duyệt PĐK/hợp đồng thì phải hiệu chỉnh lại điều kiện này.

↳ **Ghi chú:** 3 lớp: HĐ tổ chức đã duyệt · chưa duyệt ngày thường · chưa duyệt trong 2 ngày cuối tháng; HĐ cá nhân không xét. Chưa rõ: nhận diện HĐ tổ chức bằng trường nào, trạng thái PĐK lấy ở đâu, "2 ngày cuối tháng" tính theo lịch nào, duyệt muộn thì đợt sau có phát hành không (CL-XHD-07 / GAP-44, 45). Revision 2.2 nhắc "KH Chuỗi/Dự án (gộp vào BR-XHD-03)" nhưng không có nội dung (CL-XHD-09 / GAP-47). **Cập nhật 16/10/2026:** HĐ tổ chức = loại hình KH cấp 1 "Tổ chức", PĐK lấy từ SPF, 2 ngày lịch (CL-XHD-07 một phần); KH Chuỗi không có rule riêng (CL-XHD-09 ✅).

---

### REQ-XHD-023 · Hợp đồng con: không phát hành DV lẫn TB
📍 `DOC-v2.0-01 §I.c BR-XHD-03 · L401`  ·  Clarif: `CL-XHD-08`

> Hợp đồng con: nhận diện hợp đồng con khi hợp đồng có gắn hợp đồng cha (hợp đồng dự án). Không phát hành hóa đơn trên hợp đồng con, cả thiết bị và dịch vụ.

↳ **Ghi chú:** Negative 2 nhánh (DV, TB). Không phát hành rồi ghi nhận ra sao, HĐ cha có phát hành thay không: chưa đặc tả (CL-XHD-08 / GAP-46). **Cập nhật 16/10/2026:** nhận diện hợp đồng con qua tool tình trạng (có thông tin hợp đồng cha).

---

### REQ-XHD-024 · Gộp HĐ ở luồng worker theo đơn trong cùng đợt
📍 `DOC-v2.0-01 §I.c BR-XHD-05 · L404-408`  ·  Clarif: —

> Trong cùng một đợt, các dòng DV/TB đủ điều kiện của cùng một đơn gộp vào một hóa đơn.
> Chỉ một thành phần đủ điều kiện thì xuất thành phần đó, phần còn lại chờ đợt sau.
> Chi nhánh không phải tiêu chí tách hóa đơn.

↳ **Ghi chú:** Phạm vi gộp = **đơn hàng** (không gộp khác đơn). Chi nhánh nay theo hợp đồng (REQ-XHD-034) nên một đơn luôn 1 chi nhánh — câu cuối gần như mặc định đúng.

---

### REQ-XHD-025 · Luồng realtime: không gộp, phát hành đúng thành phần của tín hiệu, xử lý ngay
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L410-413`  ·  Clarif: —

> Mỗi tín hiệu chỉ phát hành đúng thành phần gắn với tín hiệu đó: tín hiệu thanh toán chỉ phát hành dịch vụ; tín hiệu giao hàng chỉ phát hành thiết bị của phương thức triển khai đó.
> Xử lý ngay khi nhận, không chờ đợt worker kế tiếp.

↳ **Ghi chú:** Ở realtime một đơn có thể ra nhiều HĐ nhỏ (mỗi tín hiệu 1 HĐ). Thành phần khác đã đủ điều kiện trước đó **không** được gộp kèm.

---

### REQ-XHD-026 · Kênh FPL chỉ realtime từ sau mốc 22h
📍 `DOC-v2.0-01 §I.c BR-XHD-06 · L414`  ·  Clarif: `CL-XHD-05`

> Đối với Kênh bán FPL chỉ realtime từ sau mốc 22h

↳ **Ghi chú:** Ranh giới realtime của FPL = 22h (kênh khác = giờ chốt cuối 18:00). Tín hiệu FPL 18:00–22:00 đi worker FPL. Cột "So với v2.1" ghi "Giữ nguyên" dù đây là nội dung mới (GAP-56).

---

### REQ-XHD-027 · Chống xuất trùng: mỗi dòng DV/TB chỉ xuất HĐ một lần
📍 `DOC-v2.0-01 §I.c BR-XHD-08 · L416-421`  ·  Clarif: `CL-XHD-11`, `CL-XHD-12`, `CL-XHD-23`

> Mỗi dòng DV/TB trên một đơn chỉ xuất hóa đơn một lần.
> Khóa xác định dòng: dịch vụ = mã đơn hàng + dịch vụ hóa đơn + Gói dịch vụ; thiết bị thêm phương thức triển khai.
> Dòng đã có BillNumber thì bỏ qua.
> Một hóa đơn vẫn có thể chứa nhiều dòng.

↳ **Ghi chú:** Khóa 2.2 khác 2.1 (`OrderCode + ServiceCode + SubserviceType`) nhưng cột "So với v2.1" ghi "Giữ nguyên"; §C#3 vẫn nói khóa "có dùng SubServiceType" (CL-XHD-11 / GAP-41). Race worker ↔ realtime (D#2) chưa có phương án (CL-XHD-23). **Cập nhật 16/10/2026:** QC chốt khóa theo 2.2; field dữ liệu chờ schema (CL-XHD-11 một phần → CL-XHD-29).

---

### REQ-XHD-028 · Điều kiện hợp lệ: đơn không ở trạng thái hủy / đang cập nhật
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L425`  ·  Clarif: `CL-XHD-14`

> Đơn không ở trạng thái hủy hoặc đang cập nhật.

↳ **Ghi chú:** Giá trị trạng thái "đang cập nhật" cụ thể là gì: chưa định nghĩa (CL-XHD-14 / GAP-13).

---

### REQ-XHD-029 · Điều kiện hợp lệ: đủ 8 trường thông tin chung
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L426`  ·  Clarif: `CL-XHD-14`, `CL-XHD-15`

> Thông tin chung phải đủ: hợp đồng có hiệu lực, Sale Team, Sale Channel, tên khách hàng, loại hình khách hàng cấp 1 và cấp 2, địa chỉ xuất hóa đơn, LocationID > 0.

↳ **Ghi chú:** 8 rule, mỗi rule 1 SC (EP). LocationID có biên `> 0`. "Hợp đồng có hiệu lực" chưa có danh sách trạng thái (CL-XHD-14).

---

### REQ-XHD-030 · Điều kiện hợp lệ: 6 ID chi tiết dịch vụ > 0
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L427`  ·  Clarif: `CL-XHD-15`

> Chi tiết từng dịch vụ phải có các ID dịch vụ, nhóm dịch vụ, gói dịch vụ, chính sách, câu lệnh giá, chương trình khuyến mãi > 0.

↳ **Ghi chú:** 6 rule biên `> 0` (0 chặn, 1 hợp lệ). **Suy diễn của analyst:** "chương trình khuyến mãi > 0" bắt buộc cả đơn không có khuyến mãi — đúng như chữ của URD nhưng dễ chặn nhầm đơn không KM; nêu ở CL-XHD-15.

---

### REQ-XHD-031 · Không hợp lệ → không phát hành + ghi log; không giữ chờ phát hành lại
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L428`  ·  Clarif: `CL-XHD-15`, `CL-XHD-17`

> Không hợp lệ thì không phát hành và ghi log; hệ thống không giữ chờ phát hành lại vì hóa đơn phải lập trong ngày.

↳ **Ghi chú:** Log ở đâu, nội dung gì, thứ tự validate và cách log nhiều lỗi: chưa đặc tả (CL-XHD-15 / GAP-29, 30). Dòng bị chặn chỉ được phát hành trong cùng ngày, qua ngày không phát hành lại (CL-XHD-17 ✅ — SC-XHD-096, SC-XHD-111).

---

### REQ-XHD-032 · Job cảnh báo chạy 15 phút/lần để bổ sung thông tin trước giờ chốt
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L429`  ·  Clarif: `CL-XHD-16`

> Job cảnh báo chạy 15 phút một lần để bổ sung thông tin kịp trước giờ chốt.

↳ **Ghi chú:** Không có điều kiện, kênh gửi, người nhận, nội dung (CL-XHD-16 / GAP-31). Chỉ kiểm được tần suất chạy.

---

### REQ-XHD-033 · Hủy đơn khi đã có HĐ: hệ thống không tự hủy / điều chỉnh HĐ
📍 `DOC-v2.0-01 §I.c BR-XHD-10 · L430`  ·  Clarif: —

> Hủy đơn khi đã có hóa đơn: hệ thống không tự hủy hay điều chỉnh hóa đơn, xử lý theo quy trình riêng.

↳ **Ghi chú:** Trong phạm vi test chỉ là kiểm **hệ thống không làm gì** với HĐ đã có (BillNumber giữ nguyên, không sinh HĐ điều chỉnh). Quy trình điều chỉnh/hủy riêng: ngoài phạm vi (TP §2.2 #2).

⛔ **Ngoài scope test 19/10/2026** — TP §2.2 #2 *"Điều chỉnh / hủy hóa đơn khi hủy đơn đã có hóa đơn"*. Không sinh SC (SC-XHD-098 deprecated). QC owner 19/10/2026.

---

### REQ-XHD-034 · Chi nhánh xuất HĐ = chi nhánh quản lý hợp đồng tại thời điểm phát hành
📍 `DOC-v2.0-01 §I.c BR-XHD-12 · L432-435`  ·  Clarif: —

> Chi nhánh xuất hóa đơn là chi nhánh quản lý hợp đồng, xác định tại thời điểm phát hành và lưu trên tồn xuất hóa đơn
> Chi nhánh nào được bán sản phẩm dịch vụ nào do bên quản lý sản phẩm bổ sung thuộc tính, nằm ngoài URD này.

↳ **Ghi chú:** Bảng mapping chi nhánh theo (loại DV, kênh bán) không còn áp dụng (D#7) — gate G8 bỏ ngày 13/10/2026. Đổi chi nhánh quản lý HĐ giữa 2 lần phát hành ⇒ lần sau dùng chi nhánh mới; sửa HĐ cũ là nghiệp vụ Điều chỉnh, ngoài phạm vi.

⛔ **Một phần ngoài scope test 19/10/2026** — TP §2.2 #3 *"Điều chỉnh hóa đơn đã phát hành khi chi nhánh đổi giữa các lần phát hành"* ⇒ SC-XHD-100 deprecated; giữ SC-XHD-099 (chi nhánh = chi nhánh quản lý hợp đồng). QC owner 19/10/2026.

---

### REQ-XHD-035 · Phát hành qua Billing System; ghi BillNumber, BillDate = ngày phát hành thực tế
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L437-440`  ·  Clarif: `CL-XHD-18`

> Phát hành qua Billing System, ghi BillNumber và BillDate vào giỏ tồn xuất hóa đơn
> BillDate là ngày phát hành thực tế.

↳ **Ghi chú:** BillDate không lùi về mốc nghiệp vụ. Billing lỗi / timeout: không có hành vi (CL-XHD-18 / GAP-14).

---

### REQ-XHD-036 · Nội dung HĐ = tên dịch vụ + số tháng sử dụng (từ SPF), không hiển thị từ ngày – đến ngày
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L441`  ·  Clarif: `CL-XHD-28`

> Nội dung hiển thị trên hóa đơn là tên dịch vụ + số tháng sử dụng (lấy từ SPF), không hiển thị kỳ hạn từ ngày – đến ngày.

↳ **Ghi chú:** Cùng nội dung với BR-HK-05 (`HK/` REQ-HK-005) — ở XHD kiểm trên HĐ Billing, ở HK kiểm trên dữ liệu đẩy HĐĐT. Ảnh `DOC-v2.0-FIG-01` (ảnh: Chi tiết hóa đơn.png) (màn "Chi tiết của hóa đơn" hiện hữu) vẫn hiện "Cước phí từ ngày / Đến ngày" (CL-XHD-28).

---

### REQ-XHD-037 · Sau phát hành gửi Invoice Event để gạch nợ và hậu kỳ
📍 `DOC-v2.0-01 §I.c BR-XHD-13 · L442`  ·  Clarif: `CL-XHD-29`

> Sau đó gửi Invoice Event để gạch nợ và xử lý hậu kỳ.

↳ **Ghi chú:** Điểm nối XHD → GN (điểm chạm b) và XHD → HK. Payload chưa có (CL-XHD-29 / GAP-07).

---

### REQ-XHD-038 · Một đơn hàng, nhiều hóa đơn
📍 `DOC-v2.0-01 §I.c BR-XHD-14 · L444-447`  ·  Clarif: —

> Một đơn có thể có nhiều BillNumber; một hóa đơn có thể chứa nhiều dòng DV/TB.
> Nguyên nhân: đơn được xuất ở nhiều đợt (dịch vụ khi thanh toán, thiết bị theo từng phương thức triển khai).

↳ **Ghi chú:** Verify qua `OB_OrderBill` (glossary §A.5 #10, L312-313): 1 OrderCode ↔ n BillNumber.

---

### REQ-XHD-039 · Clear nội dung "thuê thiết bị đầu cuối" trên HĐ (DVKH HO)
📍 `DOC-v2.0-01 §I.c BR-XHD-18 · L449-452`  ·  Clarif: `CL-XHD-21`

> Bổ sung chức năng cho phép DVKH HO chủ động xử lý với hợp đồng có yêu cầu clear nội dung "thuê thiết bị đầu cuối" trên hóa đơn.
> Mới (kịp plan các chức năng chính sẽ thự hiện)

↳ **Ghi chú:** Chỉ 1 câu: không rõ thao tác, có UI không, kết quả trên HĐ; "kịp plan" ⇒ chưa chắc thuộc v2.0 (CL-XHD-21 / GAP-53, Blocker). **Chưa sinh SC** — ghi nợ ở `CHANGELOG.md §3`.

---

### REQ-XHD-040 · Phạm vi gồm cả đơn bán mới và bán thêm
📍 `DOC-v2.0-04 mail PM LeLTM 13/10/2026 10:56 · dòng 3 danh sách`  ·  Clarif: `CL-XHD-25`

> - Bán mới, Bán thêm => ok

↳ **Ghi chú:** Không đến từ URD — URD 2.2 không có từ "bán mới" / "bán thêm", mọi BR viết chung cho "đơn hàng". PM xác nhận phạm vi gồm cả 2 loại ⇒ áp chung mọi BR của XHD, GN, HK (giả định rule áp chung — CL-XHD-25 / GAP-60, 61). Đơn bán thêm = đơn trên hợp đồng đang hoạt động (TP §2.1).

---

### REQ-XHD-041 · Cutover v1 → v2: kiểm tra chéo ở mức đơn hàng, mỗi bản tin chỉ một luồng xử lý
📍 `DOC-v2.0-01 §D#1 · L658-661`  ·  Clarif: `CL-XHD-24`

**URD 2.2 — phụ lục D** — `DOC-v2.0-01 §D#1`
> Chuyển đổi hệ thống v1 sang v2 (cutover, giai đoạn giao thoa, quét tay bổ sung).

↳ **Ghi chú:** URD 2.2 chỉ có tên mục §D#1, không đủ viết Then; SC-XHD-107, 108 deprecated 16/10/2026 (CL-XHD-33). Test plan giữ in-scope (FR06, P2) nhưng chờ PM xác nhận có test trên STG không (CL-XHD-24 / GAP-32). Quét tay bổ sung đơn bị miss: ngoài phạm vi (TP §2.2 #8).

---

### REQ-XHD-042 · Mail cảnh báo bản tin đồng bộ về chậm qua ngày
📍 `DOC-v2.0-01 §D#3 · L666-669`  ·  Clarif: `CL-XHD-22`

**URD 2.2 — phụ lục D** — `DOC-v2.0-01 §D#3`
> Bản tin đồng bộ về chậm qua ngày, dòng không được luồng nào xử lý.
> RISK-01
> PM và SA xử lý; mail cảnh báo là yêu cầu bắt buộc đã thống nhất.

↳ **Ghi chú:** "Bắt buộc" nhưng không có điều kiện, lịch, người nhận, nội dung (CL-XHD-22 / GAP-02, 11 — Blocker). **Chưa sinh SC** — ghi nợ ở `CHANGELOG.md §3`. Xuất HĐ bổ sung case-by-case: ngoài phạm vi (TP §2.2 #9).

---

### REQ-XHD-043 · Danh mục hình thức triển khai (HT triển khai) và nguồn tín hiệu giao hàng
📍 `DOC-v2.0-05 sheet "1. HT Triển khai" · dòng STT 1–8 · cột B "HT TRIỂN KHAI", D "PHƯƠNG THỨC TK-GH", E "TRIGGER"`  ·  Clarif: `CL-XHD-27`

> | STT | HT TRIỂN KHAI | … | TRIGGER | … | GHI CHÚ |
> |---|---|---|---|---|---|
> | 1 | TIN/PNC | … | Đơn hàng SPF: - DeployType = TIN/PNC | … | Đơn hàng có ít nhất 1 SPDV có mix HT Triển khai TIN/PNC và Quầy/ Sales --> auto xử lý theo luồng triển khai TINPNC |
> | | TIN/PNC giao hàng | … | Đơn hàng SPF: - DeployType = TIN/PNC giao hàng | … | Chỉ áp dụng cho Dịch vụ Camera Offnet, Thiết bị lẻ |
> | 2 | Quầy | … | Đơn hàng SPF: - DeployType = Quầy - Đã ký BBDT - Tình trạng "Đã thanh toán" | … | Chỉ áp dụng cho Dịch vụ Camera Offnet, Thiết bị lẻ |
> | 3 | Sale | … | Đơn hàng SPF: - DeployType = Sale - Đã ký BBDT - Tình trạng "Đã thanh toán" | … | Chỉ áp dụng cho Thiết bị lẻ (quản lý MAC) |
> | 4–6 | NCC - Samsung / NCC - Sony / NCC - Casper | … | Đơn hàng SPF: - DeployType = NCC-… - Đã ký BBDT - Tình trạng "Đã thanh toán" | … | 1 Đơn hàng SPF = 1/N HT Triển khai NCC |
> | 7 | FTI | … | Đơn hàng SPF: - DeployType = FTI | … | |
> | 8 | Không/ None | … | Đơn hàng SPF - DeployType = Không | … | |

↳ **Ghi chú:** Tài liệu **bổ sung** (không phải URD, người soạn AnhNQ75, chưa có ngày/version) — dùng làm dữ liệu cho chiều "phương thức triển khai" của khóa BR-DB-07 / BR-XHD-08. Bảng rút gọn: cột C, D, F lược bằng "…" (chi tiết ở file). Câu hỏi mở: TB có DeployType = "Không" không có tín hiệu giao hàng thì phát hành theo đường nào; "mix" TIN/PNC + Quầy/Sale gộp về TINPNC thì phương thức trong khóa là gì (CL-XHD-27). **URD 2.2 thắng** khi mâu thuẫn.

---

> **Quy ước:** Implicit REQ → thay quote bằng *(Implicit — không có quote trực tiếp)* + derivation ở Ghi chú. Quote >500 ký tự → sidecar `v2.0/quotes/REQ-XXX-NNN.md`.
> **Clarification quote KHÔNG ở đây** — `XHD/risk_assessment.md` §Clarifications. **SC quote** ở `test_scenario_map.md`.
