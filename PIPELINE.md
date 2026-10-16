# PIPELINE — qc-invoice-issuance-architecture

> Sổ đăng ký skill của project. Trạng thái **live** nằm ở `02_analyze-requirements/MASTER-MEMORY.md §8`
> (bảng dưới đây là bản khởi tạo; MASTER-MEMORY thắng khi 2 bên lệch).
> Cheat sheet lệnh: `COMMANDS.md`. Tài liệu framework: `~/.claude/skills/ONBOARDING.md`.

## 1. Pipeline chính — 12 bước

```
        init-project (root)  ───  create-test-plan (01_)
               │                          │
               └────────────┬─────────────┘
                            ↓
                 analyze-requirements (02_)
                            ↓
                     generate-tc (03_)  ──→  export-tc-rp (03_/09_)   [renderer, 4b]
                            ↓
                      review-tc (11_)
                            ↓
                      vibe-test (08_)          ← AI thay manual tester
                            ↓
   scan-source-code (10_) → implement-automation (10_) → review-src-tc (11_)
                            ↓
                  execute-maintain (08_test-runs/runs/)
                            ↓
                       log-bug (05_)  ←──→  sync-jira-bugs (05_)      [Jira mirror, 11b]
                            ↓
                  test-report (08_ + 09_)

Cross-cutting:  health-check (chạy bất kỳ lúc nào)
Kề pipeline:    init-source-code (0.5) · export-tc-rp (4b) · sync-jira-bugs (11b)
Utility:        fetch-us (kéo US từ Jira) · commit-code (commit chuẩn ISC)
```

Mỗi mũi tên = dependency: skill downstream cần upstream đạt **≥ PARTIAL**.

## 2. Skill Registry

| # | Skill | Vai trò trong project này | Folder ghi |
|---|-------|---------------------------|-----------|
| 0.5 | `init-source-code` | Scaffold `10_source-code/` theo archetype | `10_` |
| 1 | `init-project` | Scaffold cấu trúc + doc gốc | root, `00_`–`11_` |
| 2 | `create-test-plan` | Test Plan + Exit Criteria | `01_` |
| 3 | `analyze-requirements` | REQ/SC/data/risk + MASTER-MEMORY | `02_` |
| 4 | `generate-tc` | Fragment TC + TC-MASTER | `03_` |
| 4b | `export-tc-rp` | Render TC-MASTER → deliverable FPT | `03_`, `09_` |
| 5 | `review-tc` | Review chất lượng TC (gate G1) | `11_` |
| 6 | `scan-source-code` | Index source → `MEMORY.md` | `10_` |
| 7 | `vibe-test` | Chạy TC thật qua MCP + evidence | `08_` |
| 8 | `implement-automation` | Sinh code automation từ TC | `10_` |
| 9 | `review-src-tc` | Đối chiếu TC ↔ code | `11_` |
| 10 | `execute-maintain` | Chạy suite + classify fail | `08_test-runs/runs/` — `INDEX.md` + `RUN-*.md` + `FAIL-REGISTRY.md` |
| 11 | `log-bug` | Bug report + push Jira | `05_` |
| 11b | `sync-jira-bugs` | Pull toàn bộ bug Jira → mirror local | `05_` |
| 12 | `test-report` | Report stakeholder + GO/NO-GO | `08_`, `09_` |
| 13 | `health-check` | Validate consistency toàn project | `09_/health-check/` |
| — | `fetch-us` | Kéo User Story từ Jira (utility) | `00_` |
| — | `package-version` | Đóng gói version ĐÃ CHỐT: 2 tầng `analyze` + `test-runs`, oracle gác mất chữ (utility). ⛔ KHÔNG merge | ⛔ không sở hữu folder state |
| — | `commit-code` | Commit chuẩn Conventional Commits ISC + tạo MR (`--mr`) | — |

## 3. Prerequisites Matrix

| Skill | Cần có trước |
|---|---|
| `create-test-plan` | `CLAUDE.md` |
| `analyze-requirements` | tài liệu trong `00_input/v[X]/` |
| `generate-tc` | `analyze-requirements` ≥ PARTIAL |
| `export-tc-rp` | `generate-tc --consolidate` = COMPLETED |
| `review-tc` | TC-MASTER tồn tại |
| `scan-source-code` | `10_source-code/` có code |
| `vibe-test` | TC-MASTER + MCP kết nối |
| `implement-automation` | `10_source-code/MEMORY.md` + TC-MASTER |
| `review-src-tc` | code đã implement |
| `execute-maintain` | code build được |
| `log-bug` | `08_test-runs/runs/FAIL-REGISTRY.md` có `ASSERTION_FAIL` còn OPEN |
| `sync-jira-bugs` | `Project_rule.md §Jira Integration` |
| `test-report` | các skill trên ≥ PARTIAL |

Thiếu prerequisite ⇒ skill báo `[MISSING]` và chỉ ra cần chạy gì trước.

## 4. Pipeline Status (khởi tạo)

> ⚠️ **Bản live là `02_analyze-requirements/MASTER-MEMORY.md §8`.** Bảng này chỉ là ảnh chụp lúc init.

| # | Skill | Status |
|---|-------|--------|
| 0.5 | init-source-code | SKIPPED (no automation) |
| 1 | init-project | COMPLETED |
| 2 | create-test-plan | COMPLETED (07/10/2026 · cập nhật 13/10/2026 theo URD rev 2.2 — TP-master-InvoiceIssuance-v2.0.md bản 1.3) |
| 3 | analyze-requirements | NOT_STARTED |
| 4 | generate-tc | NOT_STARTED |
| 4b | export-tc-rp | NOT_STARTED |
| 5 | review-tc | NOT_STARTED |
| 6 | scan-source-code | SKIPPED (no automation) |
| 7 | vibe-test | NOT_STARTED |
| 8 | implement-automation | SKIPPED (no automation) |
| 9 | review-src-tc | SKIPPED (no automation) |
| 10 | execute-maintain | SKIPPED (no automation) |
| 11 | log-bug | NOT_STARTED |
| 11b | sync-jira-bugs | NOT_STARTED |
| 12 | test-report | NOT_STARTED |
| 13 | health-check | NOT_STARTED |

Status ∈ `NOT_STARTED` · `IN_PROGRESS` · `PARTIAL` · `COMPLETED` · `SKIPPED` · `FAILED`.

## 5. Mode Quick-Reference

| Skill | Mode chính |
|---|---|
| `analyze-requirements` | `--init` · `--delta` · `--update` · `--review` · `--sweep` · `--migrate` |
| `generate-tc` | mặc định · `--consolidate` · `--sync` · `--regenerate` · `--mode comprehensive` · `--techniques` |
| `export-tc-rp` | `--phase design` · `--phase report --round R<N>` |
| `review-tc` | FULL · `--module` · `--recheck` |
| `vibe-test` | mặc định (TC pending) · `--all` · `--retest` |
| `execute-maintain` | `--run-all` · `--run <class>` · `--recheck` · `--status` |
| `log-bug` | `--log` · `--update` · `--close` · `--status` · `--push-jira` · `--pull-jira` |
| `test-report` | `--sprint` · `--release` · `--adhoc` · `--cross-version` · `--trend` |
| `health-check` | QUICK · `--full` · `--version v[X]` |

## 6. Quy ước riêng project

- **Không automation** (Q7) ⇒ 5 skill automation = `SKIPPED`. Muốn bật lại: `/init-source-code` rồi đổi status.
- **Không review TC trên Google Sheet** (Q12) ⇒ đã gỡ `review-tc-ba` (4c) + `sync-online`. Có sheet thì
  bổ sung section `Online Sheet Integration` vào `Project_rule.md` (template `init-project/references/sheet-block-template.md`).
- **Jira:** `project_key` còn TBD ⇒ `fetch-us` / `log-bug --push-jira` / `sync-jira-bugs` dừng và hỏi tới khi điền key.
- **App type = API (backend, không UI)** ⇒ `vibe-test` không có màn hình để thao tác; verify qua DB / Kafka / log worker.


Xem `02_analyze-requirements/Project_rule.md` — trích theo **TÊN section**, không theo số.
