# CHANGELOG — Test Cases v2.0

> Ghi bởi `generate-tc`. Trạng thái TC từng SC do TC-MASTER sở hữu; file này chỉ giữ lịch sử generate.

## TC Gen Log

| Ngày | Action | DOC ID | Module | Tổng TC | File output | Priority | Mode | Techniques | Review Status |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-21 | GENERATE | DOC-v2.0-01, DOC-v2.0-04 | GN | 39 | fragments/TC-GN-v2.0.md | P1:33, P2:5, P3:1 | standard | N/A | ⏳ |
| 2026-10-21 | REGENERATE | DOC-v2.0-01, DOC-v2.0-04 | GN | 40 | fragments/TC-GN-v2.0.md | P1:34, P2:5, P3:1 | standard | N/A | ⏳ |
| 2026-10-21 | REGENERATE | DOC-v2.0-01, DOC-v2.0-04 | GN | 60 | fragments/TC-GN-v2.0.md | P1:38, P2:21, P3:1 | standard | N/A | ⏳ |
| 2026-10-21 | REGENERATE | DOC-v2.0-01, DOC-v2.0-04 | GN | 59 | fragments/TC-GN-v2.0.md | P1:37, P2:21, P3:1 | standard | N/A | ⏳ |
| 2026-10-21 | REGENERATE | DOC-v2.0-01, DOC-v2.0-04 | GN | 54 | fragments/TC-GN-v2.0.md | P1:34, P2:19, P3:1 | standard | N/A | ⏳ |

## Ghi chú

- 2026-10-21 · GN: 39 TC = 39 SC active (1 SC = 1 TC). 15 SC deprecated không có TC. TC ID theo `Project_rule.md §Naming Conventions` (`TC-[MODULE]-[NNN]-[short-title]`), đánh số liên tục 001–039 theo thứ tự SC ID — không có lỗ ID. Expected viết theo trạng thái dữ liệu trên tool tra cứu (inside.fpt.net), không theo khuôn HTTP (QC owner 21/10/2026).
- 2026-10-21 · GN regenerate: +TC-GN-040 (SC-GN-055 — hóa đơn DV + TB phát hành khác thời điểm). TC 001–039 giữ nguyên ID. Không tách TC theo kênh / nhóm dịch vụ (lý do: analyze GN CHANGELOG §3 #9).
- 2026-10-21 · GN regenerate: +TC-GN-041..060 (SC-GN-056..075 — 1 TC / nhóm dịch vụ, kênh ngoài sàn xoay vòng). TC 001–040 giữ nguyên ID.
- 2026-10-21 · GN: fragment chia 2 group theo luồng — `### 01 Luồng Paid — đơn sàn TMĐT` (31 TC) · `### 02 Luồng Cọc — đơn ngoài sàn` (29 TC). ID giữ nguyên, không đổi nội dung TC.
- 2026-10-21 · GN: đánh lại số liền trong từng group — 01 Luồng Paid TC-GN-001..031 · 02 Luồng Cọc TC-GN-032..060 (chiến lược renumber §A.2 (b): `ID cũ:` ở Notes + `TC-GN-v2.0-ID-MAPPING.md`).
- 2026-10-21 · GN regenerate (Paid chỉ có ở luồng sàn — QC owner): group 02 Luồng Cọc bỏ mọi bước "Gửi Orderpaid" + Pre-condition mock Orderpaid, thay bằng khách thanh toán (tiền vào cọc); gỡ TC của SC-GN-052 (deprecated); group 02 đánh lại liền TC-GN-032..059. Group 01 chưa đổi. Mapping: `TC-GN-v2.0-ID-MAPPING.md` (cột ID cũ = ID lần generate đầu).
- 2026-10-21 · GN: sửa theo health-check — Notes TC-GN-012 bỏ tham chiếu SC-GN-052; TC-GN-017 bỏ Orderpaid cho đơn B (ngoài sàn). Không đổi số TC / ID.
- 2026-10-21 · GN group 01 (Luồng Paid) viết lại: bỏ mọi bước "Gửi Orderpaid"; đơn sàn = "Nhờ dev cung cấp …" (setup); sàn quyết toán = 3 bước SPF Web Admin › Queue › Push custom task (Refer ID = OrderID, tick 1 task bất kỳ — bùa data); TC chống trùng 004–006 dùng dòng Orderpaid dev giả lập. Không đổi số TC / ID. Còn ⚠️: TC-GN-010, 014, 015, 016 (mock API kênh thanh toán + Ob_OrderBill), 026 (số dư Paid trên Foxpay).
- 2026-10-21 · GN group 01: gộp 3 bước Push custom task thành 1 step "Giả lập sàn quyết toán: …" (QC owner). Không đổi số TC / ID.
- 2026-10-21 · GN: QC không check dữ liệu Paid (dev tự kiểm; luồng sàn không có data trên Foxpay Đối soát khoản thu online) — gỡ TC của SC-GN-001, 002, 004, 005, 006; TC của SC-GN-003, 007, 011, 034 bỏ bước Foxpay, kiểm qua hóa đơn. Đánh lại số: group 01 TC-GN-001..026 · group 02 TC-GN-027..054 (mapping cập nhật).
