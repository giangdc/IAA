# COMMANDS — qc-invoice-issuance-architecture

> Cheat sheet copy-paste. Mode: **Solo** · **không automation** · Jira `project_key` **TBD** · không review TC online.
> Không nhớ cú pháp thì cứ gõ tiếng Việt, Claude tự route
> (vd "phân tích yêu cầu v1.0", "viết test case cho module AUTH").
> Sơ đồ pipeline + prerequisite: `PIPELINE.md`. Quy ước riêng: `02_analyze-requirements/Project_rule.md`.

## 0. Mở đầu mỗi phiên

```bash
# Nạp credentials (1 lần / session) — prefix ! để env sống suốt phiên
! source ~/.qc-invoice-issuance-architecture/credentials.env

# Đang ở đâu trong pipeline?
/health-check
```

## 1. Chuẩn bị

| Việc | Lệnh |
|---|---|
| Khởi tạo project (đã chạy rồi) | `/init-project` |
| Kéo User Story từ Jira | `/fetch-us --version v2.0` |
| Tạo Test Plan | `/create-test-plan --create` |
| Xuất Test Plan bản FPT | `/create-test-plan --export` |

## 2. Phân tích yêu cầu

| Việc | Lệnh |
|---|---|
| Phân tích lần đầu | `/analyze-requirements --init @00_input/v2.0/` |
| Version mới (so với version trước) | `/analyze-requirements --delta --version v2.0 @00_input/v2.0/` |
| Cập nhật theo feedback BA | `/analyze-requirements --update "<nội dung BA chốt>"` |
| Rà lượt 2 tìm requirement bỏ sót | `/analyze-requirements --sweep --version v2.0` |
| Xem tổng quan (không sửa file) | `/analyze-requirements --review` |

## 3. Test case

| Việc | Lệnh |
|---|---|
| Sinh TC 1 module | `/generate-tc --module <MODULE>` |
| Sinh TC đầy đủ kỹ thuật thiết kế | `/generate-tc --module <MODULE> --mode comprehensive` |
| Chỉ vài kỹ thuật | `/generate-tc --techniques EP,BVA,EG` |
| Gộp fragment → TC-MASTER | `/generate-tc --consolidate` |
| Đồng bộ lại TC-MASTER | `/generate-tc --sync` |
| Review chất lượng TC (gate G1 ≥ 70) | `/review-tc --version v2.0` |
| Xuất bản thiết kế TC bản FPT | `/export-tc-rp --phase design` |


## 4. Chạy test bằng AI (vibe-test)

| Việc | Lệnh |
|---|---|
| Chạy TC chưa chạy của 1 module | `/vibe-test --module <MODULE>` |
| Chạy lại TOÀN BỘ TC (kể cả đã PASS) | `/vibe-test --all` |
| Retest sau khi dev fix | `/vibe-test --retest <TC-ID\|BUG-ID>` |
| Xem tiến độ vibe | `/vibe-test --status` |

> Mỗi TC phải có **≥1 ảnh riêng** tại điểm verify. Không có ảnh ⇒ không được ghi PASS.

## 7. Bug

| Việc | Lệnh |
|---|---|
| Tạo bug từ fail | `/log-bug` |
| Cập nhật trạng thái | `/log-bug --update BUG-001 --status "Fixed"` |
| Đóng bug (đã verify) | `/log-bug --close BUG-001` |
| Xem tổng quan bug | `/log-bug --status` |
| Đẩy bug lên Jira (chỉ tạo mới) | `/log-bug --push-jira BUG-001` |
| Kéo toàn bộ bug Jira về local | `/sync-jira-bugs` |
| Chỉ đối chiếu, không ghi mirror | `/sync-jira-bugs --reconcile` |

## 8. Báo cáo

| Việc | Lệnh |
|---|---|
| Report sprint | `/test-report --sprint` |
| Report release (GO/NO-GO) | `/test-report --release --version v2.0` |
| So sánh 2 version | `/test-report --cross-version` |
| Xuất báo cáo kết quả bản FPT | `/export-tc-rp --phase report --round R1` |

## 9. Kiểm tra sức khoẻ dữ liệu

| Việc | Lệnh |
|---|---|
| Nhanh (< 30s) | `/health-check` |
| Đầy đủ (parse Excel, ghi file report) | `/health-check --full` |
| 1 version cụ thể | `/health-check --version v2.0` |

## Đóng sổ sprint (trước khi merge)

| Việc | Lệnh |
|---|---|
| Xem quy mô, chưa sửa gì | `/package-version v2.0 --audit-only` |
| Đóng gói tầng analyze | `/package-version v2.0 --tier analyze` |
| Đóng gói 1 function | `/package-version v2.0 --tier analyze --function [tên]` |
| Đóng gói 1 vùng test-runs | `/package-version 08_test-runs/vibe/v2.0-sprint-[N] --tier test-runs` |
| Đóng gói cả version (analyze → test-runs) | `/package-version v2.0` |

## 10. Commit

```bash
/commit-code                # sinh commit message chuẩn Conventional Commits (ISC) + self-review trước khi commit
/commit-code --mr           # điền MR description theo template ISC + in link tạo MR (không push)
/commit-code --mr --push    # điền MR description rồi push tạo MR trên GitLab (cần user duyệt)
```

## Skill bản riêng HuyenNHK (chạy song song bản trơn)

| Việc | Lệnh |
|---|---|
| Sinh TC theo house style riêng | `/generate-tc-huyennhk --module <MODULE>` |
| Render TC-MASTER → template FPT (bản riêng) | `/export-tc-rp-huyennhk --phase design` |
| Gộp kết quả vibe-test + manual vào 1 Round | `/merge-vibe-manual-huyennhk` |

## Thứ tự chạy điển hình

```
/init-project → /create-test-plan → /analyze-requirements --init
→ /generate-tc → /generate-tc --consolidate → /review-tc
→ /vibe-test → /log-bug → /test-report
```

Sau mỗi bước lớn: `/health-check`.
