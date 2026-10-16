# Release Checklist — [Version]

## Trước Release (Pre-Release)
- [ ] Tất cả bug P1/P2 đã được giải quyết
- [ ] Bộ test Regression đã pass
- [ ] UAT đã được sign-off
- [ ] Release notes đã soạn xong
- [ ] Kế hoạch rollback đã được ghi nhận
- [ ] SRC-TC review score ≥ 70 (nếu có automation)
- [ ] TC Review score ≥ 70

## Ngày Release (Release Day)
- [ ] Smoke test trên production sau khi deploy
- [ ] Theo dõi error logs trong 30 phút
- [ ] Thông báo cho các stakeholders

## Sau Release (Post-Release)
- [ ] Đóng các bug đã resolved trong tracker
- [ ] Lưu trữ kết quả test run
- [ ] Ghi nhận retrospective notes
- [ ] Update MASTER-MEMORY.md version status → "✅ Released"
