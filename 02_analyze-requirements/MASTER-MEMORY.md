# MASTER-MEMORY — Cross-Version Registry

> Cập nhật lần cuối: 2026-10-16
> Active version: v2.0
>
> **⚠️ Tầng 1 (project) — ROUTER cross-version.** Chứa registry (version/DOC/TC-file/downstream path), current-state canonical (§0 nếu có), quyết định cross-version. **KHÔNG chứa chi tiết SC/data/risk per-module** (sống ở tầng 3 module fragment). **KHÔNG lặp** cùng 1 bảng ở version `MEMORY.md`: §2 DOC Registry (Loại/Modules) là **nguồn duy nhất** ở đây; §3 giữ **lifecycle cross-version** (version MEMORY §3 giữ **count trong version**, không trùng).
> Layout analyze: **module-first v2** (`v2.0/<MODULE>/CHANGELOG.md` tồn tại). Số current canonical ở frontmatter `counts:` của file module — bảng ở đây là bản dẫn xuất.

## 1. Version Registry
| Version | Release Date | Input Folder | Analyze Folder | Status | Tổng DOC | Tổng SC (all) | Tổng SC (new+mod) | Parent |
|---------|-------------|-------------|----------------|--------|----------|--------------|-------------------|--------|
| v2.0 | TBD (R3 kết thúc 13/11/2026) | `00_input/v2.0/` | `02_analyze-requirements/v2.0/` | ANALYZED | 9 | 178 | 178 | v1.0 (Phase 1 — chưa có trong workspace) |

## 2. DOC ID Registry (Global)
> **`Status`** — trạng thái của FILE, không phải của yêu cầu:
> `Active` = file có trên disk trong `00_input/`, là bản latest · `Superseded` = còn file nhưng đã có bản mới thay (giữ để tham chiếu) · `Removed <ngày>` = file đã xoá khỏi working tree khi package version — **DOC-ID vẫn giữ nguyên** để citation lịch sử còn đọc được.
> **`Superseded by`** — DOC-ID của bản thay thế, hoặc `—` khi không có bản thay (vd tính năng bị loại khỏi scope). Đây là thứ giúp reader lần từ citation cũ ra bản latest.
>
> ⚠️ **KHÔNG BAO GIỜ xoá dòng khỏi registry này.** Xoá dòng = mọi citation `DOC-...` trong artifact/TC/bug/report đã ký thành mồ côi. Đổi `Status` + điền `Superseded by`, và ghi lệnh truy hồi (`git show <hash>:'<path>'`) vào ghi chú dưới bảng. Chi tiết: `SKILL.md §Input retention`.
> ⚠️ **Đổi tên / gộp / xoá file input phải cập nhật cột `File` NGAY.** Path chết ở đây làm mọi quote trỏ vào nó không verify được — `health-check` **F-07** kiểm điều này.

| DOC ID | Version | File | Loại | Status | Superseded by | Modules |
|--------|---------|------|------|--------|---------------|---------|
| DOC-v2.0-01 | v2.0 | `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx` | URD rev 2.2 — **bản chính** | Active | — | XHD, GN, HK |
| DOC-v2.0-03 | v2.0 | `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.pdf` | URD rev 2.2 bản PDF PO confirm — nội dung = DOC-v2.0-01, không trích dẫn | Active | — | XHD, GN, HK |
| DOC-v2.0-04 | v2.0 | `00_input/v2.0/Doc/Mail_PM-LeLTM_2026-10-13_PO-confirm-URD-v2.2.png` | Mail PM — xác nhận phạm vi (bổ sung) | Active | — | XHD, GN, HK |
| DOC-v2.0-05 | v2.0 | `00_input/v2.0/Doc/AnhNQ75-List HT Triển khai.xlsx` | Danh mục hình thức triển khai (bổ sung — URD thắng khi mâu thuẫn) | Active | — | XHD |
| DOC-v2.0-FIG-01 | v2.0 | `00_input/v2.0/Design/Chi tiết hóa đơn.png` | Ảnh màn hiện hữu "Chi tiết của Hóa đơn" (không phải prototype) | Active | — | XHD, GN, HK |
| DOC-v2.0-FIG-02 | v2.0 | `00_input/v2.0/Design/Danh sách hóa đơn của Hợp đồng.png` | Ảnh màn hiện hữu "Liệt kê cước của thuê bao" (không phải prototype) | Active | — | XHD |
| DOC-v2.0-FIG-03 | v2.0 | `00_input/v2.0/Doc/Workflow ĐỒNG BỘ & XUẤT HÓA ĐƠN TỰ ĐỘNG (v2.0).png` | Flow §B.I.b (XHD) — ảnh nhúng trong DOC-v2.0-01 sau L337, trùng pixel | Active | — | XHD |
| DOC-v2.0-FIG-04 | v2.0 | `00_input/v2.0/Doc/FLOW GẠCH NỢ HÓA ĐƠN – ĐỒNG BỘ PAID.png` | Flow §B.II.b (GN) — ảnh nhúng trong DOC-v2.0-01 sau L466, trùng pixel | Active | — | GN |
| DOC-v2.0-FIG-05 | v2.0 | `00_input/v2.0/Doc/Workflow ĐẨY HẬU KỲ – TIỀN TRẢ TRƯỚC (URD 2.2 §III.b).png` | Flow §B.III.b (HK) — trích từ DOC-v2.0-01 sau L562 | Active | — | HK |

> **Đổi tên 16/10/2026:** `Design/Pasted image.png` → `Design/Chi tiết hóa đơn.png` (cùng nội dung, đổi trước khi đăng ký) — DOC-v2.0-FIG-01 trỏ tên mới.
> **Flow 16/10/2026:** FIG-03..05 là ảnh nhúng sẵn trong DOC-v2.0-01 (mục `b. Flow` không có text nên bản trích `.docx` không có L-number) — đối chiếu pixel 16/10/2026: trùng 100%. Ghi chú trong ảnh chủ yếu tóm tắt lại BR; ô tô màu = "Nội dung mới, đã sửa hoặc cần xác nhận". FIG-05 do analyze trích từ URD.
> Chưa nhận (không cấp DOC-ID): URD v1.0 Phase 1 (GAP-24) · email ISC 24/09 + FTQ 30/09/2026 (GAP-57) · tài liệu tích hợp Kafka / schema / API (GAP-07) · link lưu đồ draw.io (GAP-58).

## 3. Scenario Lifecycle (Cross-Version)
> Canonical = per-SC (theo dõi lifecycle từng SC qua các version). Version ĐẦU (tất cả NEW) có thể dùng roll-up gọn `| Module | Origin | Lifecycle | Count |`; từ delta version trở đi, liệt kê per-SC cho MODIFIED/CARRIED/DEPRECATED.

| Module | Origin | Lifecycle | Count |
|--------|--------|-----------|-------|
| XHD | v2.0 | NEW | 109 |
| GN | v2.0 | NEW | 50 |
| HK | v2.0 | NEW | 21 |

> v2.0 là version đầu tiên trong workspace (Phase 1 v1.0 chưa có analyze/TC) ⇒ toàn bộ NEW. Số đếm dẫn xuất từ `v2.0/<MODULE>/test_scenario_map.md` `counts:`.

## 4. Regression Scope
### v2.0
**Phải test (new + modified):**
| SC ID | Type | Lý do |
|-------|------|-------|
| Toàn bộ `SC-XHD-*`, `SC-GN-*`, `SC-HK-*` (178 active · 4 deprecated) | NEW | Version đầu — xem `v2.0/<MODULE>/test_scenario_map.md` |

**Nên regression (carried — high risk):**
| SC ID | Type | Lý do |
|-------|------|-------|
| SC-XHD-016, SC-XHD-017, SC-XHD-029, SC-XHD-060 · SC-GN-019, SC-GN-022 | Regression (Phase 1 TMĐT) | Kênh Shopee / Tiktok đã chạy Phase 1, "có điều chỉnh v2.0" — chưa có URD v1.0 (CL-XHD-31); gắn R2 theo TP §3.2 |

**Không cần test (carried — low risk, stable):**
| SC ID | Type | Lý do |
|-------|------|-------|
| — | — | Chưa có SC carried |

## 5. Version Comparison
(Từ v2 trở đi) — chưa áp dụng: workspace chưa có analyze v1.0.

## 6. TC Files Registry
| Version | TC-MASTER File | Tổng TC | Ngày consolidate | Status |
|---------|---------------|---------|-------------------|--------|
| v2.0 | — | — | — | Chưa generate |

## 7. Downstream Path Registry
| Skill | Active Version Path |
|-------|-------------------|
| analyze-requirements | `02_analyze-requirements/v2.0/` (router `MEMORY.md` + `XHD/`, `GN/`, `HK/`) |
| generate-tc | `03_test-cases/v2.0/` |
| review-tc | `11_tc-review/` |
| vibe-test | `08_test-runs/vibe/` |
| log-bug | `05_bug-reports/` |
| test-report | `09_reports/` |

## 8. Pipeline Status — v2.0
> Thứ tự + tên skill khớp `PIPELINE.md §2 Skill Registry` (toolkit qc-claude-v1: 12 bước chính + health-check + 4 skill kề `0.5`/`4b`/`4c`/`11b` = **17 dòng**). Status ∈ NOT_STARTED / IN_PROGRESS / PARTIAL / COMPLETED / SKIPPED / FAILED.
>
> **CURRENT-STATE, OVERWRITE — đúng 1 dòng / skill.** Mỗi lần chạy **ghi đè** dòng của skill đó (cập nhật Status/Last Run/Notes). **KHÔNG append** thêm dòng cho mỗi lần chạy lại (không tạo 7 dòng health-check, 3 dòng review-src-tc trùng). **KHÔNG chèn blockquote giữa các dòng bảng** (làm vỡ bảng). Cần lịch sử run → tách file log riêng, không nhét vào bảng này.

| # | Skill | Status | Last Run | Scope | Output | Notes |
|---|-------|--------|----------|-------|--------|-------|
| 0.5 | init-source-code | SKIPPED | — | — | — | Không automation |
| 1 | init-project | COMPLETED | 2026-10-07 | — | CLAUDE.md/PIPELINE.md/COMMANDS.md | — |
| 2 | create-test-plan | COMPLETED | 2026-10-14 | v2.0 | `01_test-plans/TP-master-InvoiceIssuance-v2.0.md` (bản 1.3) + DOC-READINESS + Excel/Email | Doc readiness CONDITIONAL — 45 GAP mở |
| 3 | analyze-requirements | COMPLETED | 2026-10-16 | v2.0 · XHD, GN, HK (TL ngoài phạm vi) | `02_analyze-requirements/v2.0/` (router + 3 module × 6 file; `quotes/` đã xoá 16/10/2026 cùng URD 2.1) | INIT layout v2 — 73 REQ · 180 SC · 49 CL (7 BLOCKING) · 21 RISK; 100% quote URD đã verify với bản trích `.docx` · UPDATE 16/10/2026 (QC trả lời CL + flow URD; bỏ URD 2.1): 178 SC active (4 deprecated) · 53 CL (49 Open · 6 BLOCKING) · UPDATE 19/10/2026 (QC trả lời CL vòng 2 + tool verify): 176 SC active (6 deprecated) · 54 CL (42 Open · 5 BLOCKING) |
| 4 | generate-tc | NOT_STARTED | — | — | — | Nên resolve CL BLOCKING trước (router §2) |
| 4b | export-tc-rp | NOT_STARTED | — | — | — | renderer deliverable FPT — chạy sau consolidate |
| 4c | review-tc-ba | NOT_STARTED | — | — | — | vòng feedback BA trên sheet — chỉ khi project review TC online |
| 5 | review-tc | NOT_STARTED | — | — | — | — |
| 6 | scan-source-code | SKIPPED | — | — | — | Không automation |
| 7 | vibe-test | NOT_STARTED | — | — | — | — |
| 8 | implement-automation | SKIPPED | — | — | — | Không automation |
| 9 | review-src-tc | SKIPPED | — | — | — | Không automation |
| 10 | execute-maintain | SKIPPED | — | — | — | Không automation |
| 11 | log-bug | NOT_STARTED | — | — | — | — |
| 11b | sync-jira-bugs | NOT_STARTED | — | — | — | pull/mirror Jira → local — chỉ khi project dùng Jira (`project_key` TBD) |
| 12 | test-report | NOT_STARTED | — | — | — | — |
| 13 | health-check | NOT_STARTED | — | — | — | — |

## 9. Notes (quyết định cross-version — KHÔNG phải per-run count log)
- **2026-10-13** — URD rev 2.2 là bản chính (PO confirm qua mail PM — DOC-v2.0-04); rev 2.1 giữ làm tham chiếu kỹ thuật, **2.2 thắng khi mâu thuẫn**.
- **2026-10-16** — ⛔ **URD rev 2.1 không sử dụng** (QC owner: đã out) — thay quyết định 13/10. Chỉ URD 2.2 là căn cứ; SC dựng duy nhất trên 2.1 chuyển DEPRECATED (SC-XHD-107, 108 · SC-HK-009, 010).
- **2026-10-13** — Phạm vi gồm **đơn bán mới + bán thêm** (mail PM); URD không phân biệt loại đơn ⇒ analyze giả định rule áp chung (CL-XHD-25).
- **2026-10-14** — **TL (URD §B.IV) ngoài phạm vi** test v2.0 (QC lead chốt) ⇒ không có module `TL/` trong analyze.
- **2026-10-16** — Analyze dùng **layout module-first v2** (INIT trên thư mục trống). Module = XHD / GN / HK, map mã chức năng FR01–FR11 ở `Project_rule.md §Module Codes`.
- **2026-10-16** — File trả lời câu hỏi vòng 1 là câu trả lời của **QC**, không phải PO: CL chỉ đóng khi câu trả lời dựa được vào chữ URD 2.2; câu QC báo "không tìm thấy trong tài liệu" giữ Open và chuyển PO ở vòng 2.
- **2026-10-16** — Tài liệu bổ sung `DOC-v2.0-05` (HT triển khai) và ảnh `DOC-v2.0-FIG-01/02` (màn Hệ thống Thông tin, HĐ 2025) **không phải URD** — chỉ làm dữ liệu / câu hỏi, không sinh rule.

## 10. Version Cutover — Compaction Rule
> Khi mở version mới (v[N] → v[N+1]):
> 1. **Archive** append-log cũ (run-history nếu có) sang file lịch sử; §8 Pipeline Status **reset** về NOT_STARTED cho version mới.
> 2. **Không mang** số current của version cũ vào §0 — recompute cho version mới.
> 3. Số "đông cứng theo mốc" ở §9 giữ nguyên (có nhãn ngày), KHÔNG "sửa cho khớp" version mới.
> 4. Chạy `health-check` xác nhận: 0 drift count, 0 router-tier chứa nội dung leaf, 0 orphan reference.
