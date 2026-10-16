# Smoke Test Checklist — qc-invoice-issuance-architecture

> Chạy trước mỗi chu kỳ kiểm thử. Nếu bất kỳ mục nào fail, chặn testing và thông báo cho dev.

## Xác thực (Authentication)
- [ ] Người dùng có thể đăng nhập với thông tin hợp lệ
- [ ] Người dùng không thể đăng nhập với thông tin không hợp lệ
- [ ] Luồng quên mật khẩu hoạt động

## Luồng chính (Core Flows)
- [ ] [Luồng quan trọng 1]
- [ ] [Luồng quan trọng 2]
- [ ] [Luồng quan trọng 3]

## Hạ tầng (Infrastructure)
- [ ] Ứng dụng load không có lỗi console
- [ ] API endpoints phản hồi (kiểm tra network tab)
- [ ] Không có hình ảnh bị hỏng hoặc tài nguyên bị thiếu

---
Kiểm thử bởi: ___________  Ngày: ___________  Build: ___________
