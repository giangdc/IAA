# Project Rules — qc-invoice-issuance-architecture

> Bản runtime mọi skill đọc. Framework default: `~/.claude/skills/init-project/`.
> Sửa tại đây để override cho project này.
> ⚠️ Skill trích section theo **TÊN**, không theo số — thêm section mới thì đặt cuối file.

## Project Info

- **Tên project:** qc-invoice-issuance-architecture
- **Tên đầy đủ:** Invoice Issuance Architecture — Phase 2 (xuất hóa đơn đa kênh, 1 đơn 1..n HĐ, gạch nợ Paid/Cọc)
- **App type:** API
  <!-- Hệ thống backend event-driven: SPF → Kafka (Order Event / Invoice Event) → INVOICE
       (Invoice Consumer – Rule Engine – Worker phát hành) → Billing System. URD KHÔNG mô tả màn hình
       UI nào ⇒ verify chủ yếu qua dữ liệu (OB_OrderRaw*, OB_OrderBill*, Paid/Orderpaid), bản tin
       Kafka và lịch worker. Bug log lên Jira vẫn phải chọn `Platform` trong danh mục Web · App ·
       "Web, App" — chốt giá trị khi push bug đầu tiên. -->
- **Loại kiểm thử:** Functional, Regression, Integration, Smoke
  <!-- Regression: luồng Phase 1 (kênh TMĐT Shopee/TikTok Shop, autobill 1 đơn = 1 bill) phải
       vẫn đúng sau khi gộp rule đa kênh. Integration: SPF ↔ INVOICE ↔ thanh toán ↔ hậu kỳ ↔ tính lương. -->
- **Môi trường:** STG `TBD` (mặc định — cập nhật ở `07_environments/environments.md`)
- **Team:** Team — 4 QC theo Test Plan v2.0 (bản 1.3, 13/10/2026)
- **QC phụ trách (owner):** HuyenNHK
- **Thành viên:** HuyenNHK (FR02, FR03, FR04) · GiangDC2 (FR01, FR03, FR05, FR06) · AnhPTM17 (FR07–FR09) · DatDGD (FR10, FR11 + thông tin khách trong FR01; TL ra ngoài phạm vi 14/10/2026) — mã chức năng Scope test, xem TP §2.1a
  - ⛔ **DatDGD là thực tập sinh** (chốt 14/10/2026): file export Excel + Email Test Plan **không có tên DatDGD, không tính effort DatDGD** — export lấy Resources / Schedule / Effort từ `TP-master §6B` (bản xuất 3 QC; phần HK + F27 ghi PIC HuyenNHK). Bản nội bộ (có DatDGD) ở `TP-master §6`.
- **Version hiện tại:** v2.0
- **Sprint hiện tại:** —
- **Ngôn ngữ viết TC:** Tiếng Việt (tech terms / keyword / enum status giữ tiếng Anh)
- **Automation:** Không (manual + vibe-test). `10_source-code/` chưa scaffold.
- **Tài liệu gốc:** `00_input/v2.0/Doc/Invoice_Issuance_Architecture_v2_2_URD_v2_0.docx` (URD rev 2.2 — bản chính từ 13/10/2026)
  <!-- Revision history trong doc: 1.0 (25/02/2026, Phase 1) · 2.0 (10/07/2026, Phase 2) ·
       2.1 (26/08/2026, cập nhật theo MoM 19.08.2026) · 2.2 (08/10/2026, rút gọn theo PO: gộp BR,
       thêm BR-XHD-18, chốt worker 12h/18h, thêm A.2/A.3). Author Vuongnd17 · Reviewer Leltm.
       PO: Nguyễn Thị Ngọc Hoa (hoantn13) – DVKH, từ rev 2.2 (rev 2.1: Nguyễn Thị Nhung – Nhungnt3) · PM: Lê Thị Mỹ Lệ (Leltm). -->

## Module Codes

> Bảng map **mã chức năng ↔ module** — nguồn duy nhất. `sync-jira-bugs` map bug → module bằng
> prefix summary `[<mã> - <tên>]`; `analyze-requirements` dùng cột `Module` làm tên thư mục fragment.
> Module ngừng phát triển thì đổi `Status` = `DEPRECATED`, **KHÔNG xoá dòng** — 0 REQ/SC/TC của
> module DEPRECATED là ĐÚNG, không phải coverage gap; `health-check` đọc cột này để khỏi báo nhầm.

| Mã | Module | Tên chức năng | Status |
|---|---|---|---|
| FR01 | XHD | Đồng bộ đơn hàng SPF → INVOICE (17 kênh × 20 nhóm DV × bán mới / bán thêm), tín hiệu giao hàng 3 nguồn, thông tin khách xuất HĐ | Active |
| FR02 | XHD | Lịch xuất HĐ + phân luồng worker / realtime (gồm kênh FPL) | Active |
| FR03 | XHD | Điều kiện phát hành DV / TB (PĐK, hợp đồng con) + điều kiện hợp lệ | Active |
| FR04 | XHD | Gộp / tách HĐ (1 đơn n HĐ) + chống phát hành trùng | Active |
| FR05 | XHD | Phát hành HĐ qua Billing + Invoice Event + chi nhánh xuất HĐ | Active |
| FR06 | XHD | Cutover v1 → v2 + kiểm tra chéo | Active |
| FR07 | GN | Đồng bộ Paid + điểm chạm + xác định phương thức Paid / Cọc | Active |
| FR08 | GN | Gạch nợ bằng Paid: gạch nợ tạm (kênh sàn), gạch nợ thật, chừa phần EVC bị lock | Active |
| FR09 | GN | Gạch nợ bằng Cọc | Active |
| FR10 | HK | Đẩy hậu kỳ theo đơn: ký hiệu + ID, nội dung + tổng tiền theo thuế suất, thông tin mẫu, đẩy HĐĐT | Active |
| FR11 | HK | Tiền trả trước một lần mỗi đơn | Active |
| — | TL | Điều chỉnh tính lương FPT Play SA (URD §B.IV) | Out-of-scope |
<!-- Điền bởi analyze-requirements --init 16/10/2026. Mã FRxx = mã chức năng Scope test (TP §2.1a, chốt
     14/10/2026); cột Module = tên thư mục analyze `02_analyze-requirements/v2.0/<Module>/`.
     TL: QC lead chốt ngoài phạm vi 14/10/2026 — KHÔNG có thư mục analyze; 0 REQ/SC/TC là ĐÚNG
     (health-check: xử lý như DEPRECATED, không báo coverage gap). -->

## Naming Conventions

> Framework default (`~/.claude/skills/init-project/references/naming-conventions.md`).
> Sửa tại đây để override cho project này — mọi skill đọc section này, không đọc file framework.

| Type | Pattern |
|---|---|
| Document | `DOC-v[VERSION]-[NN]` |
| Requirement | `REQ-[MODULE]-[NNN]` |
| Scenario | `SC-[MODULE]-[NNN]` |
| Testcase | `TC-[MODULE]-[NNN]-[short-title]` |
| Bug ID | `BUG-[NNN]` |
| Test run | `TR-[SPRINT]-[YYYY-MM-DD]` |
| TC-MASTER | `TC-MASTER-v[VERSION].xlsx` |
| Report | `REPORT-[MODE]-[CTX]-[YYYY-MM-DD].{md,xlsx}` |

### Bug — 2 field điền, còn lại dẫn xuất
- Điền: `module` (từ section `Module Codes`) + `bug_desc` (tiếng Việt, ≤12 từ)
- `title` = `[<module>] - <bug_desc>` → dùng cho **cả H1 md và Jira Summary** (nguyên văn)
- `severity: Suggest` ⇒ `title` = `[Suggest][<module>] - <bug_desc>` (đề xuất cải tiến, **chỉ QC gán**)
- File: `draft/BUG-<NNN>-<slug(bug_desc)>.md` → sau push: `jira/<JIRA-KEY>-<slug>.md`
- Label bắt buộc khi push: `bug-<nnn>` (dùng cho `match_jql`)

### Ngôn ngữ
- Narrative (test case, mô tả bug, steps): **Tiếng Việt**
- Tech terms · code block · enum Status/Priority/Severity: **English**

### Enum
- Bug Status (= Jira): `To Do` · `In Progress` · `In review` · `Pending` · `Done` · `Cancel` — đã đóng = `Done`+`Cancel`
- TC Priority: `P1` · `P2` · `P3` (nội bộ) — Bug Priority: `P1`..`P5` ↔ Jira `Highest`..`Lowest`
- Severity: `Critical` · `Major` · `Medium` · `Low` · `Suggest` (weight 20/10/5/2/0) · Resolution: `Fixed` · `Won't Fix`
- TC Status: `Pass` · `Fail` · `Blocked` · `Skipped` · `Not Run`

## Layout Conventions

> Quy ước máy đọc — quyết định skill GHI vào đâu và health-check TÌM ở đâu.
> Đổi giá trị ở đây là đổi hành vi skill; đừng đổi giữa chừng 1 version.

```yaml
analyze_layout:     module-first   # module-first (mặc định) | flat (legacy, 1 module)
                                   # module-first v2 (mặc định project mới): v[X]/MEMORY.md = router
                                   #   (CHỈ §1 Function Register + §2 Module Summary)
                                   #   + v[X]/<MODULE>/{CHANGELOG, requirement_traceability,
                                   #     test_scenario_map, test_data_catalog, risk_assessment}.md
                                   #   KHÔNG có _global/ — CL về <MODULE>/risk_assessment.md
                                   # ⚠️ Skill DÒ layout bằng SỰ TỒN TẠI của <MODULE>/CHANGELOG.md,
                                   #   KHÔNG bằng field này (field chỉ có 2 nhánh module-first|flat).
tc_fragment_format: md             # md (mặc định) | xlsx — TC-MASTER luôn .xlsx dù chọn gì
bug_folders:
  jira:  05_bug-reports/jira/      # bug ĐÃ log Jira — mirror do sync-jira-bugs ghi đè, KHÔNG sửa tay
  draft: 05_bug-reports/draft/     # bug LOCAL chưa log Jira
  evidence: 05_bug-reports/evidence/   # ảnh minh chứng bug. Template bug nhúng
                                   #   `![BUG-NNN-01](../evidence/BUG-NNN-01.png)` — đường dẫn
                                   #   TƯƠNG ĐỐI từ `draft/` ⇒ đổi chỗ này thì phải đổi cả template
  exports: 05_bug-reports/exports/ # file xuất cho stakeholder (nếu dùng) — không bắt buộc
  index: 05_bug-reports/bug-index.md
  # GHI phẳng ở gốc 2 thư mục trên. ĐỌC phải ĐỆ QUY (`jira/**/*.md`) — bug có thể nằm
  # trong sub-folder theo sprint (`<version>-sprint-N/`) do lượt đóng sổ trước để lại;
  # glob phẳng đọc ra 0 bug mà KHÔNG báo lỗi (health-check E-07).
runs_layout:
  auto:  08_test-runs/runs/        # execute-maintain — INDEX.md + RUN-*.md + FAIL-REGISTRY.md + TR-*.md
  vibe:  08_test-runs/vibe/        # vibe-test
  # ⚠️ Gốc `08_test-runs/` CHỈ chứa router. `runs/` mới là đích execution log; sự tồn tại của
  #   `runs/FAIL-REGISTRY.md` là thứ execute-maintain/log-bug/test-report/health-check dùng để dò
  #   `runs/ v2` vs `legacy §15-§16`. Vùng `runs/<version>-sprint-N/` và `vibe/<version>-sprint-N/`
  #   là archive seal của sprint đã đóng (`/package-version --tier test-runs`), ⛔ không ghi vào đó.
router_filename:    README.md      # README.md (mặc định) | INDEX.md — tên file router của 08_/09_
```

## DOC Notation

```yaml
req_notation: BR
# BR (custom) : URD đánh số Business Rule theo mẫu `BR-<NHÓM>-<NN>` — dùng NGUYÊN VĂN ID này cho cột
#               `Maps (Ref DOC)` (traceability Schema A) và cột `Nguồn` (test-data-catalog).
#               67 BR trong URD (đếm 07/10/2026): BR-DB-01..08 (đồng bộ đơn) · BR-XHD-01..14 (xuất HĐ)
#               · BR-DP-01..03 (đồng bộ Paid) · BR-XL-01..05 (điểm chạm/phương thức) · BR-NT-01..04
#               (nợ tạm) · BR-GN-01..05 (gạch nợ) · BR-VC-01..07 (EVC — 01, 06 đánh [Bỏ]) · BR-GC-01..07
#               (gạch cọc) · BR-HK-01..10 (hậu kỳ) · BR-TL-01..04 (tính lương) + `RISK-01` (rủi ro, map như BR).
#               ⚠️ Đếm trên đây là của URD rev 2.1. URD rev 2.2 (bản chính) còn 41 BR (đếm 16/10/2026):
#               XHD §B.I 17 (BR-DB-01..05, 07 · BR-XHD-01..03, 05, 06, 08, 10, 12..14, 18) · GN §B.II 14
#               (BR-DP-01 · BR-XL-01, 03 · BR-NT-01, 02, 04 · BR-GN-01, 03..05 · BR-GC-01..03 · BR-VC)
#               · HK §B.III 6 (BR-HK-01..03, 05, 07, 09) · TL §B.IV 4. Số nhảy là có chủ đích (2.2 giữ ID 2.1).
#               2.2 bỏ bảng "Mô tả Flow" (BƯỚC n) — chỉ có lưu đồ ảnh; requirement không có BR
#               (bảng phạm vi §A.2/§A.3, phụ lục §D) ⇒ cột `Maps (Ref DOC)` = `—`, neo bằng `DOC-ID §section (L…)`.
#               Bước flow (BƯỚC n) không có ID riêng ⇒ trỏ `DOC-ID §<chức năng> · bước n`.
#               `OI-<n>` = open issue / câu hỏi cần PO-FTQ quyết (URD §V) — KHÔNG phải requirement,
#               đi vào clarification, ⛔ không map làm REQ.
# Giá trị chuẩn khác: FR/VR · AC · UC · US-key · none · auto
```

## Jira Integration

> Sinh bởi `/init-project` từ Q9 + Q10 + Q10b. Template đầy đủ:
> `~/.claude/skills/init-project/references/jira-block-template.md`.
> ⚠️ **`project_key` CHƯA CÓ (TBD)** lúc init 07/10/2026 — `fetch-us` / `log-bug --push-jira` /
> `sync-jira-bugs` sẽ dừng và hỏi cho tới khi điền key thật.

```
# Tên tool theo mcp_axis → tra log-bug/references/jira-tools.md. KHÔNG hardcode tool ở đây.
mcp_axis:        connector          # BẮT BUỘC — Atlassian connector của claude.ai (OAuth qua /mcp, 1 lần/máy)
qc_name:         HuyenNHK
site:            https://foxproject.atlassian.net
cloud_id:        f192baca-4acd-46c2-8d8d-ce0d4e636d4e   # cùng site với các project QC khác trong workspace
project_key:     TBD                # ⚠️ điền KEY thật khi có link Jira dự án
issue_type:      Bug
reporter:                           # để trống = tài khoản auth
parent_epic:                        # để trống nếu screen không bắt parent
fix_version:                        # để trống
priority_map:    P1=Highest, P2=High, P3=Medium, P4=Low, P5=Lowest
#                Bug Priority ↔ Jira priority scheme. ⚠️ `TC Priority` (P1·P2·P3) là trục KHÁC.
severity_map:    Critical=20, Major=10, Medium=5, Low=2, Suggest=0  # tên khoá = enum Severity (KHÔNG phải Priority)
#                `Suggest` (0) = đề xuất cải tiến, chỉ QC gán. Board không có option `0` ⇒ bỏ `Suggest=0`.
#                ⚠️ Field Severity là **cascading select** (`option-with-child`).
severity_field:  <TBD>              # = custom_fields.Severity.key
custom_fields:                   # REGISTRY field custom — sync-jira-bugs (pull) + log-bug --push-jira (push) cùng đọc.
                                 # Thiếu ⇒ skill DỪNG và hỏi. log-bug tự khám phá lần push đầu rồi GHI NGƯỢC.
                                 # ℹ️ Các project khác cùng site đang dùng Severity=customfield_10678,
                                 #    Platform=customfield_10681 — ⛔ chưa đối chiếu với board của project này,
                                 #    phải kiểm bằng *metadata field lúc tạo* trước khi điền.
  Severity:      { key: <TBD>, name: "Severity",      values: [Critical, Major, Medium, Low, Suggest] }
  Platform:      { key: <TBD>, name: "Platform",      values: [Web, App, "Web, App"] }
  Effect:        { key: <TBD>, name: "Effect",        values: [Functionality, Performance, Security, Serviceability, Usability] }
  Defect Type:   { key: <TBD>, name: "Defect Type",   values: [Data, Interface, Logic, Requirement, Server, Other] }
  Test method:   { key: <TBD>, name: "Test method",   values: [Auto, Manual] }   # default `Manual`; ⛔ không phải `Automation`
  Test Round:    { key: <TBD>, name: "Test Round",    values: [1, 2, 3, 4, 5, 6, 7] }   # số trần — strip chữ `R` khi push
  Reject Number: { key: <TBD>, name: "Reject Number", values: [] }   # free text "Lần N"
  Reason for Wontfix: { key: <TBD>, name: "Reason for Wontfix", values: [] }
  Verify Date:   { key: <TBD>, name: "Verify Date",   values: [] }
  Duplicate:     { key: <TBD>, name: "Duplicate",     values: [No, Yes] }   # default `No`
# 🔴 `Reject Number` · `Reason for Wontfix` · `Verify Date` · `labels` có thể KHÔNG có trên màn hình
#    CREATE ⇒ kiểm *metadata field lúc tạo*; field nào không có thì set ở bước edit ngay sau create.
required_fields:                 # field BẮT BUỘC khi create — log-bug tự khám phá rồi điền
recommended_fields:
status_map:      To Do=To Do, In Progress=In Progress, In review=In review, Pending=Pending, Done=Done, Cancel=Cancel
#                = workflow Jira (framework default). Board khác ⇒ lấy lại bằng *liệt kê transition*.
#                🔴 Đã đóng = `Done` + `Cancel`; `Pending` VẪN LÀ MỞ dù statusCategory=done.
match_jql:       project = {project_key} AND labels = "bug-{nnn}"   # label do log-bug gắn khi push
userstory:                       # sub-section riêng cho fetch-us
  issue_types:   [Story]
  jql_template:  project = {project_key} AND issuetype in ({issue_types}) AND fixVersion = "{version}" ORDER BY key ASC
  link_handling:
    figma:   record
    gsheets: read_text
    gdocs:   read_text
    gdrive:
      enabled: true
    other:   record
  attachment_download:
    env_file: ~/.config/jira/.env   # chỉ cần khi tải binary attachment
```

## Automation Rules

N/A — project không có automation (Q7 = Không). Bổ sung khi chạy `/init-source-code`.

## Execution Rules

> `execute-maintain` + `vibe-test` đọc.

- **Chạy test thật**, parse output thật. KHÔNG bịa số liệu — chạy không được thì báo blocked.
- **Classify fail:** `LOCATOR_STALE` · `ASSERTION_FAIL` · `ENV_ERROR` · `UNKNOWN`.
- **KHÔNG auto-fix.** Skill report → người sửa.
- **Credentials:** `~/.qc-invoice-issuance-architecture/credentials.env` (ngoài repo, `chmod 600`).
  ⛔ KHÔNG inline password vào command · ⛔ KHÔNG đọc file credentials rồi copy giá trị ra context.
  Check bằng `test -n "$<VAR>" && echo ENV_OK || echo ENV_MISSING` (KHÔNG echo giá trị).
- **Env vars cần thiết:** TBD (quyền truy cập DB INVOICE / Kafka / SPF STG — bổ sung khi có env)
- **Evidence vibe-test:** ≥1 ảnh riêng / TC tại điểm verify; giữ ảnh phụ chỉ khi FAIL/BLOCKED.
  <!-- Hệ thống backend: evidence thường là ảnh kết quả query DB / bản tin Kafka / log worker
       tại điểm verify — vẫn 1 ảnh riêng mỗi TC. -->

## Bug Rules

> `log-bug` đọc.

- **Bug từ evidence**, không suy đoán. `LOCATOR_STALE` ≠ app bug (trừ khi UI thật sự đổi).
- **Traceability không đứt:** Bug → FAIL → RUN → Method → TC → SC → REQ.
- **Lifecycle = workflow Jira**, ⛔ framework KHÔNG tự định nghĩa:
  `To Do → In Progress → In review → Done`, cộng 2 nhánh `Pending` (gác lại, chờ retest) và
  `Cancel`. **Đã đóng = `Done` + `Cancel`**; `Pending` 🔴 **VẪN LÀ MỞ** dù Jira gắn
  `statusCategory = done`.
  ⚠️ Chưa đối chiếu board của project này (project_key TBD) ⇒ kiểm bằng *liệt kê transition* rồi
  sửa dòng này + `status_map` cho khớp.
- **Source of truth phía local** = file bug `.md`; mirror `jira/**/*.md` (đệ quy) do `sync-jira-bugs` ghi đè,
  KHÔNG sửa tay. Đổi trạng thái trên Jira ⇒ chạy `/sync-jira-bugs`, đừng sửa mirror.
- **Aging:** cảnh báo bug `Open` > 7 ngày. Version đã đóng ⇒ miễn cảnh báo.
- **Severity ↔ Priority** theo enum ở `§Naming Conventions`; map sang Jira ở `§Jira Integration`.

## Test Data Rules

> `generate-tc` + `review-tc` đọc. Đây là **DỮ LIỆU riêng dự án**;
> quy tắc TRÌNH BÀY nằm ở `~/.claude/skills/generate-tc/references/testcase-guide.md`.

- **Base URL / endpoint theo env:** STG TBD
- **Kênh tích hợp:** SPF → Kafka (Order Event / Invoice Event) → INVOICE → Billing System (theo URD §I Actor)
- **Bảng dữ liệu verify chính:** `OB_OrderRaw` / `OB_OrderRaw_Detail` · `OB_OrderBill` / `OB_OrderBill_Detail`
  (`Ob_OrderBill` lưu cả phương thức gạch nợ Paid/Cọc) · `Paid` / `Orderpaid` (`paymentstatus` quyết định
  gạch nợ tạm hay thật) — tên trường chi tiết do `analyze-requirements` trích từ URD
- **Tham số cấu hình:** giờ chốt + giờ chạy worker theo từng đợt, số đợt (URD BR-XHD-01) — ⛔ không
  hardcode giá trị giờ trong TC, ghi theo "giờ chốt của đợt"
- **Tài khoản test theo role:** TBD (giá trị thật để ở credentials.env — KHÔNG ghi ở đây)
- **Định dạng dữ liệu đặc thù:** ngày `dd/MM/yyyy`, tiền VND không phần thập phân

## Report Rules & Quality Gates

> `test-report` + `create-test-plan` đọc.

- **Aggregation, không generation.** KHÔNG estimate, KHÔNG suy diễn số chưa có.
- **Trung thực:** NO-GO thì ghi NO-GO.
- **Trùng ngày ⇒ thêm suffix, KHÔNG ghi đè** file report cùng loại.
- **Nhiều người chạy cùng ngày ⇒ mỗi người 1 file** (suffix `-<account>`) để tránh conflict git.

**Quality Gates** (G1–G7 là baseline framework; G8+ là gate riêng project):

| Gate | Tiêu chí | Ngưỡng | Skill chịu trách nhiệm |
|---|---|---|---|
| G1 | TC Review score | ≥ 70 | review-tc |
| G2 | P1 TC đã execute | 100% | execute-maintain → test-report |
| G3 | Pass rate (effective) | ≥ 80% | test-report |
| G4 | P1 bug còn Open | = 0 | log-bug → test-report |
| G5 | Bug fix rate | ≥ 80% | test-report |
| G6 | Summary report đã tạo + review | Yes | test-report |
| G7 | SRC-TC Review score (chỉ project có automation) | N/A (không automation) | review-src-tc |
| G8 | Bảng mapping chi nhánh hóa đơn (loại DV, kênh bán) → chi nhánh có trước mốc kiểm thử | Yes | create-test-plan |

> G8 lấy từ URD: *"thiếu bảng mapping thì … QC không có căn cứ để test và không đủ điều kiện
> go-live. Cần có bảng trước mốc kiểm thử, không phải trước mốc release."*

## Automation Context

> ⚠️ Section này do `/init-source-code` GHI (append/replace). Không có automation ⇒ để `N/A`.

N/A — chưa scaffold source code. Chạy `/init-source-code --archetype <stack>` để sinh.

## Memory / Write-back Policy

> Section này trả lời: **file nào được phép to tới đâu**, và **lịch sử làm việc bị cắt ra thì đi
> về đâu**. Hook `memory-guard.py` đọc ở đây và cưỡng chế. Không khai ⇒ hook dùng trần khởi điểm
> của chính nó, ⛔ không tự đoán theo project.
>
> ℹ️ `/package-version` **KHÔNG đọc section này** — skill đó tự chứa luật đóng gói. Nếu section này
> khai luật đóng gói và **lệch** với skill: 🛑 skill DỪNG và báo, ⛔ không tự chọn bên thắng.

**① Trần dung lượng từng tầng** — con số khởi điểm, chỉnh theo project:

| Tầng | File | Trần |
|---|---|---|
| 1 | `02_analyze-requirements/MASTER-MEMORY.md` | 60 KB |
| 2 | `02_analyze-requirements/<version>/MEMORY.md` (router) | 90 KB |
| 3 | `02_analyze-requirements/<version>/<MODULE>/*.md` (lá) | 250 KB |
| 4 | `WORKING-STATE.md` | 16 KB |
| 5 | `10_source-code/MEMORY.md` | 130 KB |
| 6 | `08_test-runs/runs/FAIL-REGISTRY.md` | 200 KB |

🔴 **Trần nào làm file của sprint ĐÃ ĐÓNG đỏ là trần SAI** — nới trần, ⛔ đừng sửa file đã chốt.

**② Đích write-back chính thức** — lịch sử cắt ra khỏi MEMORY đi về đây, ⛔ không đẻ file mới
(`docs/history/`, `*-log.md`, `*.bak`):

| Loại lịch sử | Đích |
|---|---|
| Lịch sử phân tích từng lượt | `<version>/<MODULE>/CHANGELOG.md §1` (layout v2) · `<version>/MEMORY.md §10` (layout v1) |
| Lịch sử chạy test | `08_test-runs/runs/RUN-*.md` + `INDEX.md` |
| Lịch sử implement | `10_source-code/MEMORY.md` §Implementation Log |
| Quyết định xuyên version | `MASTER-MEMORY.md` §9 Notes |
| Còn lại | `git log -p` — ⛔ không chép ra file |

**③ Nguồn canonical của số đếm:** frontmatter `counts:` của file module — router và MASTER chỉ là
bản dẫn xuất; lệch thì file module thắng.

**④ Khối bất khả xâm phạm:** mọi dòng có `⛔`.

## Active Memory Rules

> Rule riêng của project mà framework không biết: UI quirk theo platform, ràng buộc môi trường
> build, quy ước field custom, định dạng dữ liệu đặc thù, quyết định đã chốt với BA/Dev…
> Mỗi rule ghi kèm **ngày** + **ai quyết** — để lần sau còn biết rule nào đã hết hiệu lực.

| Ngày | Rule | Người quyết |
|---|---|---|
| | *(trống lúc init — bổ sung dần)* | |
