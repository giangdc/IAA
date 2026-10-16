# qc-invoice-issuance-architecture — Project Context

## Thông tin dự án (Project Info)
- **Tên dự án:** qc-invoice-issuance-architecture — Invoice Issuance Architecture (Phase 2)
- **App type:** API — backend event-driven (SPF → Kafka → INVOICE: Consumer / Rule Engine / Worker → Billing), không có UI
- **Loại kiểm thử:** Functional, Regression, Integration, Smoke
- **Môi trường:** STG
- **URL:** TBD (cập nhật ở `07_environments/environments.md`)
- **Team:** 4 QC theo Test Plan v2.0 — HuyenNHK (FR02, FR03, FR04) · GiangDC2 (FR01, FR03, FR05, FR06) · AnhPTM17 (FR07–FR09) · DatDGD (FR10, FR11 + thông tin khách trong FR01, **thực tập sinh** — không có tên / effort trong Excel + Email export, dùng `TP-master §6B`)
- **QC phụ trách:** HuyenNHK
- **Ngôn ngữ viết TC:** Tiếng Việt
- **Automation:** Không (manual + vibe-test)
- **Jira:** https://foxproject.atlassian.net — `project_key` TBD · `mcp_axis: connector` (bật Atlassian qua `/mcp`)
- **Tài liệu gốc:** `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx` (URD rev 2.2; phần kỹ thuật tham chiếu rev 2.1 `…v2_0_URD_v1_0.docx` cùng thư mục) — requirement đánh số `BR-<NHÓM>-<NN>` (`req_notation: BR`)

> **PIPELINE.md** và **COMMANDS.md** ở root — tester đọc `COMMANDS.md` để biết cách gọi skill.

## Version Info
- **Current version:** v2.0
- **Version history:** v2.0 (initial)
- **MASTER-MEMORY:** `02_analyze-requirements/MASTER-MEMORY.md`
- **Project Rules:** `02_analyze-requirements/Project_rule.md`

## Quy trình làm việc (Workflow)
```
00_input/v2.0/ (tài liệu gốc)
  → 01_test-plans/ (create-test-plan)
    → 02_analyze-requirements/v2.0/ (analyze-requirements)
      → 03_test-cases/v2.0/ (generate-tc → consolidate → TC-MASTER)
        → 11_tc-review/ (review-tc + review-src-tc)
          → 08_test-runs/ (execute)
            → 05_bug-reports/ (log bugs)
              → 09_reports/ (summary report)
```

## MEMORY Files
- **MASTER-MEMORY:** `02_analyze-requirements/MASTER-MEMORY.md` — cross-version registry
- **Version MEMORY:** `02_analyze-requirements/v2.0/MEMORY.md` — version-scoped analysis
- **Source-code MEMORY:** N/A — project không có automation (`10_source-code/` chưa scaffold)

## Naming Conventions
→ **Nguồn duy nhất: section `Naming Conventions` trong `02_analyze-requirements/Project_rule.md`.**
Mọi skill đọc ở đó, không hardcode.
Bug (`bug_id` · tên file · `title`/Jira Summary, gồm cả biến thể `[Suggest]`) → `§Bug` của
`Project_rule.md §Naming Conventions`. ⛔ **Không chép công thức xuống đây** — bản chép trước đó
thiếu biến thể `[Suggest]` và sống nhiều tuần, đúng lý do dòng trên nói "không hardcode".
Template bug: `~/.claude/skills/log-bug/assets/bug-report-template.md` (skill đọc trực tiếp, KHÔNG copy vào repo).

## Folder Reference
| # | Folder | Mục đích | Skill liên quan |
|---|--------|----------|----------------|
| 00 | input/v2.0/ | Tài liệu đầu vào (theo version) | analyze-requirements |
| 00 | input/shared/ | Tài liệu dùng chung | analyze-requirements |
| 01 | test-plans/ | Test plan tổng thể | create-test-plan |
| 02 | analyze-requirements/ | MASTER-MEMORY + Project_rule | analyze-requirements |
| 02 | analyze-requirements/v2.0/ | Analysis output theo version | analyze-requirements |
| 03 | test-cases/v2.0/ | TC-MASTER + fragments | generate-tc |
| 04 | test-data/ | Dữ liệu test | — |
| 05 | bug-reports/ | Báo cáo lỗi | log-bug |
| 06 | checklists/ | Smoke + release checklists | — |
| 07 | environments/ | Config môi trường | — |
| 08 | test-runs/ | Logs chạy test | test-report |
| 09 | reports/ | Báo cáo tổng hợp | test-report |
| 10 | source-code/ | (chưa có — không automation) | init-source-code |
| 11 | tc-review/ | Review reports (TC + SRC-TC) | review-tc, review-src-tc |

## Project Rules
→ Xem chi tiết: `02_analyze-requirements/Project_rule.md`

## Tools
- Manual testing project scaffolded by `init-project` skill
- Framework version: Multi-Version (MASTER-MEMORY enabled)
- Created on: 2026-10-07

## Test Plan — v2.0
- **Document:** `01_test-plans/TP-master-InvoiceIssuance-v2.0.md`
- **Scope IN:** XHD (đồng bộ đơn & xuất HĐ) · GN (gạch nợ) · HK (hậu kỳ, tiền trả trước) — cả đơn bán mới và bán thêm · Scope test 11 chức năng FR01–FR11 (mã phân tích F01–F29)
- **Scope OUT:** xuất HĐ tay · TL — điều chỉnh tính lương FPT Play SA (gồm đối soát FHR) · điều chỉnh/hủy HĐ · gạch nợ EVC (đội EVC) · ServiceID 2, 22 · xử lý HĐ dư khi trùng · quét tay giai đoạn giao thoa · xuất bổ sung case-by-case · Performance/Security
- **Approach:** Manual E2E (Kafka + dữ liệu bảng, mock/stub hệ thống ngoài) | Automation: không
- **Exit criteria (= Quality Gates):** G1–G6 (G7 N/A; G8 bỏ 13/10/2026) — xem test plan §4
- **Lịch:** (QC lead chốt 14/10) Clear nghiệp vụ 19–20/10 (4 QC) · Review + gen TC 21–22/10 · Update TC + setup 23/10 (2 task này không có HuyenNHK) · R1 26–30/10 · buffer 02–03/11 · R2 04–10/11 · buffer 11/11 · R3 recheck bug 12–13/11/2026 (4 QC) · 1.264 TC · effort lịch 65 md (estimate công thức 145 md với AI gen TC 80% — KHÔNG ĐÁP ỨNG theo tham số) · bản xuất 3 QC · 47 md (TP §6B)
- **Doc readiness:** CONDITIONAL (lần rà 2, URD rev 2.2) · GAP mở 45 (3 Blocker · 18 Critical) · PM xác nhận trước 16/10/2026 (Clear nghiệp vụ 19/10/2026)

## Analyze — v2.0
- **Output:** `02_analyze-requirements/v2.0/` — layout **module-first v2**: router `MEMORY.md` + `XHD/`, `GN/`, `HK/` (mỗi module 6 file: `CHANGELOG`, `requirement_traceability`, `test_scenario_map`, `test_data_catalog`, `risk_assessment`) + `quotes/` (sidecar quote dài). TL ngoài phạm vi — không có thư mục.
- **Kết quả INIT 16/10/2026:** 73 REQ · 180 SC (P1 138 · P2 40 · P3 2) · 49 CL (7 BLOCKING) · 21 RISK — số canonical ở frontmatter `counts:` file module; router §2 là bản dẫn xuất.
- **DOC-ID:** `DOC-v2.0-01` URD 2.2 (chính) · `-02` URD 2.1 (tham chiếu) · `-03` PDF · `-04` mail PM · `-05` HT triển khai (xlsx) · `-FIG-01/02` ảnh màn Hệ thống Thông tin — registry ở `MASTER-MEMORY.md §2`.
- **Tra quote:** `DOC_DIR=00_input/v2.0/Doc DOC_DEFAULT="Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx" scripts/doc/search-doc.sh "<từ khoá>"` — `L<n>` trong Source Location là số dòng của bản trích này.
- **Bước tiếp:** resolve CL BLOCKING (router §2) → `/generate-tc --version v2.0` (hoặc `--module XHD|GN|HK`).
