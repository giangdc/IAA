## 📋 Thay đổi này làm gì?
<!-- Mô tả ngắn: LÀM GÌ và TẠI SAO. KHÔNG mô tả HOW (code/diff tự nói) -->

## 🔗 Ticket
Closes #<issue-number> | Ref: <PROJ-XXX>
<!-- Không có ticket (vd: dọn dẹp nội bộ) → ghi N/A và nêu lý do ngắn -->

## 🧪 Cách kiểm tra
1.
2.

## ✅ Self-review checklist

- [ ] Commit messages đúng Conventional Commits (mục 2.1), có tag `[AI]` khi cần
- [ ] Không commit file rác: `.bak`, output tạm, evidence trùng, `__pycache__`

## 🤖 AI Disclosure
<!-- Mục 2.5 — KPI team, đo tự động qua Git log. Khai báo trung thực. -->
- [ ] Không dùng AI trong MR này
- [ ] Dùng AI — đã thêm tag `[AI]` vào cuối subject của các commit liên quan
  - [ ] Phân tích yêu cầu / sinh scenario
  - [ ] Viết hoặc mở rộng test case
  - [ ] Viết code automation
  - [ ] Debug / investigate fail
  - [ ] Viết báo cáo / tài liệu
  - [ ] % nội dung AI-assisted (ước tính): ____%
  - [ ] Đã đọc kỹ và hiểu toàn bộ nội dung AI sinh ra

## ⚠️ Breaking Changes (nếu không có, ghi N/A)
<!-- Với QA Artifact, tính là breaking khi: đổi ID scheme (SC/TC/REQ), đổi
     cấu trúc thư mục sprint, đổi cột TC-MASTER, retire file mà skill khác đang đọc -->
