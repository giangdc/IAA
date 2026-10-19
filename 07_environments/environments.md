# Test Environments

## STG
| Field    | Value |
|----------|-------|
| URL      |  |
| API URL  |       |
| Database |       |
| Ghi chú | Dữ liệu mirror từ production (đã ẩn danh) |

## Tài khoản kiểm thử (Test Accounts)
> Không lưu mật khẩu thực ở đây. Sử dụng password manager của team.

| Vai trò | Username | Ghi chú |
|---------|----------|---------|
| Admin   |          |         |
| User    |          |         |

## Tool tra cứu / verify (STG)
> Nguồn: QC owner cung cấp 19/10/2026. Đường dẫn menu ghi theo nguyên văn QC gửi.

| Mục đích | Tool / đường dẫn menu | Module dùng | Ghi chú |
|---|---|---|---|
| Tra cứu đơn hàng | Web admin | XHD | Xem chi tiết dịch vụ: ID dịch vụ, nhóm DV, gói DV, chính sách, câu lệnh giá, CTKM (CL-XHD-15) |
| Tra cứu hóa đơn | Quản lý kế toán › Liệt kê cước | XHD · HK | Màn Hệ thống Thông tin (DOC-v2.0-FIG-01/02): số tháng, thông tin KH, số tiền, tình trạng thanh toán, CN (CL-XHD-28) |
| Tra cứu khoản thu | Foxpay › Thanh toán online › Đối soát khoản thu online | GN | Đối chiếu Paid / khoản thu |
| Gạch nợ hóa đơn bằng tay | Quản lý kế toán › Gạch nợ bổ sung TT online | GN | Thao tác tay — ⚠️ không dùng thay cho gạch nợ tự động khi verify luồng INVOICE |
| Tra cứu đặt cọc | Quản lý kế toán › Tiền đặt cọc › Tra cứu | GN | Tồn cọc theo hợp đồng / loại cọc (nhánh Cọc) |
| Tra cứu tiền trả trước | Quản lý kế toán › Cước trả trước › Tra cứu new | HK | Verify add tiền trả trước (BR-HK-09) |

> ⚠️ QC **không có quyền xem log** (CL-XHD-15, CL-XHD-19, CL-HK-06) — verify bằng hành vi trên các tool trên, không verify cột Note / log.

## Flow QC test E2E (QC owner, cập nhật 19/10/2026)
KH / nhân viên lên đơn hàng thành công → KH thanh toán, ký BBĐT → **xuất HĐ cho dịch vụ trước** → triển khai (nếu có) → giao hàng / triển khai thành công → cập nhật đơn hàng đã hoàn tất → **hệ thống gen tiếp HĐ cho thiết bị**. Một đơn hàng có thể có nhiều hóa đơn.

> ✅ Khớp URD 2.2 BR-XHD-03 (L396: DV khi có tín hiệu "đã thanh toán", TB khi giao hàng hoàn tất — xét độc lập) và BR-XHD-14 (1 đơn nhiều HĐ).
> ✅ HĐ thiết bị được kích hoạt bởi **tín hiệu giao hàng của từng phương thức triển khai** (phiếu thi công / Vendor / quầy) — QC owner 19/10/2026, khớp BR-DB-02, BR-XHD-06 ⇒ đơn nhiều phương thức ra HĐ thiết bị theo từng phương thức.
> ⚠️ Còn hỏi BA (CL-XHD-34): thiết bị hình thức triển khai "Không" (không có phiếu / Vendor / quầy) lấy tín hiệu nào để phát hành.
