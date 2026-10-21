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
> Host của các menu `Quản lý kế toán ›`: **https://inside.fpt.net/** (QC owner 21/10/2026). TC ghi bước tra cứu dạng: `Truy cập https://inside.fpt.net/ menu: Quản lý kế toán › Liệt kê cước, tra theo số hóa đơn.`

| Mục đích | Tool / đường dẫn menu | Module dùng | Ghi chú |
|---|---|---|---|
| Tra cứu đơn hàng | Web admin | XHD | Xem chi tiết dịch vụ: ID dịch vụ, nhóm DV, gói DV, chính sách, câu lệnh giá, CTKM (CL-XHD-15) |
| Tra cứu hóa đơn | Quản lý kế toán › Liệt kê cước | XHD · HK | Màn Hệ thống Thông tin (DOC-v2.0-FIG-01/02): số tháng, thông tin KH, số tiền, tình trạng thanh toán, CN (CL-XHD-28) |
| Tra cứu khoản thu | Foxpay › Thanh toán online › Đối soát khoản thu online | GN | Chỉ tìm theo số hợp đồng. ⛔ **Luồng sàn (Shopee / TikTok) không có data trên màn này** — đơn sàn chỉ verify gạch nợ trên hóa đơn (QC owner 21/10/2026) |
| Gạch nợ hóa đơn bằng tay | Quản lý kế toán › Gạch nợ bổ sung TT online | GN | Thao tác tay — ⚠️ không dùng thay cho gạch nợ tự động khi verify luồng INVOICE |
| Tra cứu đặt cọc | Quản lý kế toán › Tiền đặt cọc › Tra cứu | GN | Tồn cọc theo hợp đồng / loại cọc (nhánh Cọc) |
| Giả lập sàn quyết toán (Paid đơn sàn → "thanh toán hoàn tất") | SPF Web Admin › Queue › Push custom task — Refer type = `Order`, Refer ID = **OrderID** (xem trên SPF Web Admin), Action code = `SPFShopeeCompletedOrder` (Shopee), Instance = `v1`, **tick 1 task bất kỳ** → **Import** | GN | QC owner 21/10/2026 · ảnh `00_input/v2.0/Design/webadmin.png`. **Bùa data do dev hỗ trợ, không phải luồng thật.** Chưa chốt: Action code TikTok · URL STG |
| Tra cứu tiền trả trước | Quản lý kế toán › Cước trả trước › Tra cứu new | HK | Verify add tiền trả trước (BR-HK-09) |
| Cập nhật tình trạng PĐK | Báo cáo phiếu đăng ký › Duyệt HD › Chuyển tình trạng PDK | XHD | Chuẩn bị hợp đồng doanh nghiệp đã / chưa duyệt PĐK (BR-XHD-03, CL-XHD-07) |
| Xem ký hiệu hóa đơn điện tử | Danh sách hóa đơn (Quản lý kế toán › Liệt kê cước) › cột Chuyển đổi hóa đơn › icon máy in ⇒ biên bản điện tử | HK | Biên bản điện tử có ký hiệu hóa đơn điện tử (BR-HK-03, CL-HK-11) |
| Kiểm tra trạng thái PĐK | Web admin › Chi tiết đơn hàng › Thông tin khác › Thông tin duyệt đơn | XHD | Mỗi kênh bán test 1 hợp đồng doanh nghiệp (CL-XHD-07) |
| Cập nhật thông tin hợp đồng | Inside › Quản lý hợp đồng › Cập nhật hợp đồng | XHD | Đổi thông tin khách trên hợp đồng khi đơn đang chờ phát hành hóa đơn (BR-DB-03, SC-XHD-020); tạo thông tin hợp đồng khác đơn (SC-XHD-030). QC owner 20/10/2026 |

> ⚠️ **Đơn sàn (Shopee / TikTok): QC không tự tạo được trên STG — dev hỗ trợ data** (QC owner 21/10/2026).
> ⚠️ QC **không có quyền xem log** (CL-XHD-15, CL-XHD-19, CL-HK-06) — verify bằng hành vi trên các tool trên, không verify cột Note / log.

## Flow QC test E2E (QC owner, cập nhật 19/10/2026)
KH / nhân viên lên đơn hàng thành công → KH thanh toán, ký BBĐT → **xuất hóa đơn cho dịch vụ trước** → triển khai (nếu có) → giao hàng / triển khai thành công → cập nhật đơn hàng đã hoàn tất → **hệ thống gen tiếp hóa đơn cho thiết bị**. Một đơn hàng có thể có nhiều hóa đơn.

> ✅ Khớp URD 2.2 BR-XHD-03 (L396: DV khi có tín hiệu "đã thanh toán", TB khi giao hàng hoàn tất — xét độc lập) và BR-XHD-14 (1 đơn nhiều hóa đơn).
> ✅ hóa đơn thiết bị được kích hoạt bởi **tín hiệu giao hàng của từng phương thức triển khai** (phiếu thi công / Vendor / quầy) — QC owner 19/10/2026, khớp BR-DB-02, BR-XHD-06 ⇒ đơn nhiều phương thức ra hóa đơn thiết bị theo từng phương thức.
> ⚠️ Còn hỏi BA (CL-XHD-34): thiết bị hình thức triển khai "Không" (không có phiếu / Vendor / quầy) lấy tín hiệu nào để phát hành.
