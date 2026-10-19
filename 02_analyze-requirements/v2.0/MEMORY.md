---
id: v2.0/router
title: Router — Analyze v2.0
type: router
version: v2.0
sprint: —
modules: 3
doc_source:
  - id: DOC-v2.0-01
    file: Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx
    revision: "URD rev 2.2 · 08/10/2026 · Vuongnd17 (Reviewer Leltm) · PO confirm qua mail PM 13/10/2026"
    md5: 33f5acb6c27fa0f4feaa59c3197b2512
    kind: URD — bản chính
    modules: [XHD, GN, HK]
    sections: "§A.1 Thông tin chung · §A.2 Kênh bán (L79-137) · §A.3 Nhóm DV (L138-260) · §A.5 Thuật ngữ (L277-320) · §B.I XHD (L323-452) · §B.II GN (L453-548) · §B.III HK (L549-597) · §B.IV TL — ngoài phạm vi (L598-634) · §C Điểm cần xác nhận (L635-651) · §D Phụ lục (L652-693)"
  - id: DOC-v2.0-02
    file: Doc/out-of-date/Invoice_Issuance_Architecture_v2_0_URD_v1_0.docx
    revision: "URD rev 2.1 · 26/08/2026 · Vuongnd17 · bị 2.2 thay phần chính"
    md5: b0f9d0800b248864a70fc2d4f9790f74
    kind: "URD — chỉ dùng cho Phụ lục D của 2.2 (D#1, 2, 3, 4, 5, 6; KHÔNG D#7, 8, 9) — QC owner chốt 19/10/2026"
    modules: [XHD, HK]
  - id: DOC-v2.0-03
    file: Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.pdf
    revision: "URD rev 2.2 bản PDF đính kèm mail PM 13/10/2026"
    md5: 44eb00ce36190a08673afcccb3c76551
    kind: "KHÔNG trích dẫn — nội dung = DOC-v2.0-01 (đã đối chiếu 13/10/2026, DOC-READINESS §A #9)"
    modules: [XHD, GN, HK]
  - id: DOC-v2.0-04
    file: Doc/Mail_PM-LeLTM_2026-10-13_PO-confirm-URD-v2.2.png
    revision: "mail LeLTM 13/10/2026 10:56"
    md5: 6ea4fc1da95015e8554999513f16f0ea
    kind: "KHÔNG PHẢI URD — mail PM xác nhận phạm vi (bán mới + bán thêm, kênh, nhóm SP, EVC)"
    modules: [XHD, GN, HK]
  - id: DOC-v2.0-05
    file: Doc/AnhNQ75-List HT Triển khai.xlsx
    revision: "không version / ngày — người soạn AnhNQ75"
    md5: 7760bc736ea8ac5f4c8ce8193fd575af
    kind: "KHÔNG PHẢI URD — danh mục hình thức triển khai (bổ sung); URD thắng khi mâu thuẫn"
    modules: [XHD]
  - id: DOC-v2.0-06
    file: Doc/U26SG00002067.pdf
    revision: "bản in hóa đơn chuyển đổi từ hóa đơn điện tử U26SG00002067, ngày 06/08/2026, in 19/10/2026"
    md5: 55f9b2eee3953ca06cc1bcf003afa9de
    kind: "KHÔNG PHẢI URD — mẫu hóa đơn điện tử (trường theo mẫu, phần tổng theo thuế suất) — QC owner cung cấp"
    modules: [HK]
  - id: DOC-v2.0-FIG-01
    file: Design/Chi tiết hóa đơn.png
    revision: "ảnh chụp màn Hệ thống Thông tin — hóa đơn U25SG00002918 (2025)"
    md5: 7b01d992073d03f1ed5913fdadf11ff6
    kind: "KHÔNG PHẢI prototype — màn hiện hữu tab \"Chi tiết của Hóa đơn\""
    modules: [XHD, GN, HK]
  - id: DOC-v2.0-FIG-02
    file: Design/Danh sách hóa đơn của Hợp đồng.png
    revision: "ảnh chụp màn Hệ thống Thông tin — Liệt kê cước của thuê bao SGFDL-250409-5459 (2025)"
    md5: 837b08b547cd55c16efdc1ff73e98c69
    kind: "KHÔNG PHẢI prototype — màn hiện hữu tab \"Báo cáo tổng hợp\""
    modules: [XHD]
  - id: DOC-v2.0-FIG-03
    file: "Doc/Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png"
    revision: "ảnh flow §B.I.b nhúng trong DOC-v2.0-01 (sau L337) — trùng pixel"
    md5: 3e2e9b4b5600e32eb9f5949a4eb281a9
    kind: "Flow URD 2.2 (một phần DOC-v2.0-01)"
    modules: [XHD]
  - id: DOC-v2.0-FIG-04
    file: "Doc/FLOW GẠCH NỢ HÓA ĐƠN – ĐỒNG BỘ PAID.png"
    revision: "ảnh flow §B.II.b nhúng trong DOC-v2.0-01 (sau L466) — trùng pixel"
    md5: 3419b484f15bbb13e6aee6f42db71664
    kind: "Flow URD 2.2 (một phần DOC-v2.0-01)"
    modules: [GN]
  - id: DOC-v2.0-FIG-05
    file: "Doc/Workflow ĐẨY HẬU KỲ – TIỀN TRẢ TRƯỚC (URD 2.2 §III.b).png"
    revision: "ảnh flow §B.III.b trích từ DOC-v2.0-01 (sau L562) ngày 16/10/2026"
    md5: 4cea9e3d9acb990361da91d25e0698ed
    kind: "Flow URD 2.2 (một phần DOC-v2.0-01)"
    modules: [HK]
status: ANALYZED
updated: 2026-10-19
---

# Router — Analyze v2.0

> **File này là BẢN ĐỒ, không phải kho nội dung.** Nội dung thật nằm ở **6 file / module**; router chỉ trả lời 2 câu: *"chức năng này ở module nào"* và *"module này lớn cỡ nào, rủi ro ra sao"*.
> 📜 **Lịch sử từng lượt UPDATE của mỗi module** → `<module>/CHANGELOG.md §1`. **Lịch sử router bản cũ** → `git show <commit>:<path>`.
> 🔑 **Nguồn canonical của số đếm là FILE MODULE** — xem §Luật `counts` canonical dưới. Bảng §2 là **bản dẫn xuất**: sửa số ở file module trước, rồi mới đồng bộ về đây.
> 📍 Đường dẫn `file:` ở frontmatter tính từ `00_input/v2.0/`. `L<n>` trong Source Location = số dòng bản trích text của `scripts/doc/search-doc.sh`. Status / Superseded by của DOC-ID: `MASTER-MEMORY.md §2`.

## 1. Function Register

| Module | Dir | Chức năng | DOC Source | Dải REQ | Dải SC |
|---|---|---|---|---|---|
| **XHD** | [`XHD/`](XHD/) | Đồng bộ đơn SPF → INVOICE (17 kênh × 20 nhóm DV, bán mới / bán thêm), tín hiệu giao hàng 3 nguồn, thông tin KH, lịch worker / realtime (gồm FPL), điều kiện phát hành (PĐK, hợp đồng con), gộp / tách hóa đơn, chống trùng, điều kiện hợp lệ, chi nhánh, phát hành Billing + Invoice Event, cutover — **FR01–FR06** | `DOC-v2.0-01` §A.2, §A.3, §B.I, §C, §D (+ `-02`, `-04`, `-05`, `-FIG-01`, `-FIG-02`) | `REQ-XHD-001..043` | `SC-XHD-001..109` |
| **GN** | [`GN/`](GN/) | Đồng bộ Paid, 3 điểm chạm, chọn Paid / Cọc, gạch nợ tạm / gỡ tạm (kênh sàn), gạch nợ thật bằng Paid (chừa EVC lock), gạch nợ bằng Cọc — **FR07–FR09** | `DOC-v2.0-01` §B.II (+ `-02`) | `REQ-GN-001..020` | `SC-GN-001..050` |
| **HK** | [`HK/`](HK/) | Đẩy hậu kỳ theo đơn sau Invoice Event: ký hiệu + ID hóa đơn điện tử, nội dung, tổng tiền theo thuế suất, đẩy hóa đơn điện tử, tiền trả trước một lần mỗi đơn — **FR10–FR11** | `DOC-v2.0-01` §B.III, §C#1, §D#5–6 (+ `-02`) | `REQ-HK-001..010` | `SC-HK-001..021` |

> ⚠️ **Bẫy tra cứu:** ID (`SC-XHD-NNN`) **không** suy ra được tên thư mục, và thư mục thường **dùng lại qua nhiều sprint** ⇒ phân biệt **BẮT BUỘC bằng dải ID** ở bảng trên (khớp `id_range` trong frontmatter `CHANGELOG.md`).
> ⛔ **TL (URD §B.IV — điều chỉnh tính lương FPT Play SA) ngoài phạm vi** (QC lead chốt 14/10/2026) — **không có thư mục `TL/`**, đừng dựng. Module Codes ghi `Out-of-scope`.
> Thứ tự luồng: XHD (Invoice Event) → GN (điểm chạm b) + HK. Risk / CL xuyên module đặt ở `XHD/risk_assessment.md` (RISK-XHD-01, 02, 10 · CL-XHD-25, 29, 31).

## 2. Module Summary

> 📐 **Bảng dẫn xuất** — sinh lại / đối chiếu bằng cách đọc `counts:` ở frontmatter từng file module:
> ```bash
> for m in 02_analyze-requirements/v2.0/*/; do
>   [ -f "$m/test_scenario_map.md" ] || continue
>   echo "== $(basename $m)"
>   sed -n '/^counts:/,/^[a-z_]*:/p' "$m/test_scenario_map.md"
>   sed -n '/^counts:/,/^[a-z_]*:/p' "$m/risk_assessment.md"
> done
> ```

| Module | Req | SC | NEW | MOD | CARRIED | DEPR | P1 | P2 | P3 | CL | RISK | Risk Level |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| XHD | 43 | 109 | 109 | 0 | 0 | 2 | 84 | 24 | 1 | 34 | 10 | High |
| GN | 20 | 48 | 48 | 0 | 0 | 2 | 42 | 5 | 1 | 10 | 6 | High |
| HK | 10 | 20 | 20 | 0 | 0 | 1 | 12 | 8 | 0 | 11 | 5 | High |
| **Tổng** | **73** | **177** | **177** | **0** | **0** | **5** | **138** | **37** | **2** | **55** | **21** | — |

> ⚠️ **URD 2.1 (`DOC-v2.0-02`) chỉ dùng cho Phụ lục D của 2.2** — D#1, 2, 3, 4, 5, 6; **không** D#7, 8, 9 (QC owner chốt 19/10/2026, thay quyết định 16/10 "không sử dụng"). D#4 (EVC: BR-VC-01..07, BR-GC-04..07) dùng từ vòng 3 19/10/2026 vì 2.2 ghi "Giữ nguyên (gộp nhóm BR-VC)"; bỏ các bước 2.1 đánh dấu `[Bỏ]`. SC-XHD-107, 108 · SC-HK-009, 010 dùng lại.
> ⛔ **19/10/2026** — deprecated SC-XHD-098, 100 (ngoài scope test — TP §2.2 #2, #3: điều chỉnh / hủy hóa đơn) · SC-GN-049 (API EVC lỗi, CL-GN-02) · SC-HK-019 (hệ thống Dịch vụ lỗi, CL-HK-06): STG không test lỗi / timeout hệ thống ngoài, thực tế retry thủ công. · **vòng 3:** SC-GN-024 (Paid quyết toán sàn < nợ không xảy ra, CL-GN-06).
> ℹ️ REQ không có SC **có chủ đích** (URD chưa đủ để viết Then): REQ-XHD-039 (BR-XHD-18), REQ-XHD-042 (mail cảnh báo bản tin trễ), REQ-XHD-033 (ngoài scope test — TP §2.2 #2), REQ-HK-010 (dòng EVC / chiết khấu / mẫu hóa đơn điện tử) — nợ ở `CHANGELOG.md §3` từng module.
> ℹ️ 13 SC (XHD 9 · GN 4 · HK 0) có `Then` phụ thuộc CL chưa trả lời, vẫn gán Priority — đếm ở `counts.blocked_by_cl`.
> 🔴 CL còn **OPEN**: 24/55 (đóng CL-HK-04 theo mẫu DOC-v2.0-06 · đóng CL-HK-05: lỗi đẩy hóa đơn điện tử ⇒ dev retry thủ công · đóng CL-HK-11: ký hiệu kiểm trên biên bản điện tử · CL-GN-05 mở lại chờ BA xác nhận · **vòng 3 19/10/2026:** đóng CL-XHD-01, 02, 03, 04, 08, 14, 15, 18, 26 · CL-GN-06, 07 · CL-HK-07, 09 · làm rõ thêm CL-XHD-07, 12, 27 · CL-GN-08, 10 (URD 2.1 dùng cho D#4) · +CL-XHD-33, CL-GN-10, CL-HK-10 khi bỏ URD 2.1 · đã đóng CL-XHD-06, 09, 10, 17 · làm rõ một phần CL-XHD-02, 04, 05, 07, 08, 11 — 16/10/2026 · **vòng 2 19/10/2026:** +CL-XHD-34 · đóng CL-XHD-20, 25, 28, 30 · CL-GN-02, 03 · CL-HK-06, 08 · làm rõ một phần CL-XHD-14, 15, 19, 27, 31, 32 · CL-GN-01, 05, 07, 09 · CL-HK-04, 07, 09 · theo URD 2.1 Phụ lục D: đóng CL-HK-02, 10 · làm rõ một phần CL-XHD-22, 23, 24, CL-HK-03 · đóng CL-HK-01: chỉ test đầu U, cho hóa đơn bán mới và bán thêm · +CL-HK-11 điểm verify ký hiệu hóa đơn điện tử · gạch nợ EVC / voucher **vẫn test** (QC owner, khác TP §2.2 #5) — CL-GN-01, 08, 10 mở, chờ BA liệt kê loại EVC / voucher). **BLOCKING (4):** CL-XHD-21 (BR-XHD-18) · CL-XHD-22 (mail cảnh báo bản tin trễ) · CL-XHD-29 (tài liệu tích hợp — chặn setup + execute) · CL-HK-03 (dòng EVC / chiết khấu).

### 🔑 Luật `counts` canonical (v2)

Mỗi chỉ số có **đúng 1 nguồn canonical**; mọi nơi khác chỉ được **trỏ tới**, ⛔ không chép lại số:

| Chỉ số | Nguồn canonical |
|---|---|
| REQ · SC (+ NEW/MOD/CARRIED/DEPR · P1/P2/P3) | `<module>/test_scenario_map.md` — frontmatter `counts:` |
| CL · RISK | `<module>/risk_assessment.md` — frontmatter `counts:` |
| Dải ID (`id_range`) | `<module>/CHANGELOG.md` — frontmatter |

⛔ **Router §2 và MASTER-MEMORY là bản dẫn xuất** — khi lệch, **file module thắng**. Sửa số: sửa ở module trước, đồng bộ lên sau, và ghi 1 dòng `ĐÍNH CHÍNH` ở `<module>/CHANGELOG.md §1`.

### ⛔ Không thuộc router v2

Các section của v1 **đã có home riêng**, ⛔ không dựng lại ở router — `health-check` báo WARNING nếu thấy:

| Từng ở router v1 | Home ở v2 |
|---|---|
| §4 Scenario Index | `<module>/test_scenario_map.md` |
| §5 Test Data Summary | `<module>/test_data_catalog.md` |
| §6 Clarifications | `<module>/risk_assessment.md` (CL section) |
| §9 TC Generation Log | nơi `generate-tc` ghi (`MASTER-MEMORY §6` + log của generate-tc) |
| Lịch sử từng lượt UPDATE / banner *"Cập nhật lần cuối"* | `<module>/CHANGELOG.md §1` |
| Source Detail (quote REQ) | `<module>/requirement_traceability.md §2` |
