# 00_input/v2.0 — Tài liệu đầu vào

> Thư mục này **chỉ chứa BẢN LATEST** của mỗi tài liệu. Bản cũ đã bị bản mới thay thế thì xoá khỏi
> working tree — **DOC-ID vẫn giữ** trong registry để citation lịch sử còn đọc được.

**Danh sách DOC-ID ↔ file ↔ `Status` ↔ `Superseded by` — nguồn chuẩn DUY NHẤT, KHÔNG copy sang đây:**
- `../../02_analyze-requirements/MASTER-MEMORY.md` **§2** — registry cross-version
- `../../02_analyze-requirements/v2.0/MEMORY.md` **frontmatter `doc_source:`** — bản version-scoped (router layout v2: file, md5, revision, loại)

**Lấy lại file đã xoá:** `git show <commit-trước-khi-xoá>:'00_input/v2.0/<path>'`
(blob vẫn nằm trong git history — KHÔNG rewrite history để "dọn" cho nhỏ).

## Quy tắc (áp cho mọi version)

1. **Chỉ bản latest nằm trong `00_input/<version>/`.** BA gửi bản mới thay bản cũ ⇒ xoá bản cũ,
   đừng để cạnh nhau — 2 bản cùng chỗ là nguồn nhầm lẫn cho lần phân tích sau.
2. **Không bao giờ xoá DOC-ID.** Đổi `Status` → `Removed <ngày>` + điền `Superseded by` trong registry.
   Citation cũ nhờ đó vẫn lần ra được bản latest.
3. **Không rewrite citation trong artifact/report đã ký** (analyze fragment · TC · bug · test-run
   report) — nguyên tắc append-log, bằng chứng lịch sử đóng cứng.
4. **Bổ sung ≠ thay thế.** Doc bổ sung lấy DOC-ID mới và ghi rõ bản nào thắng khi 2 bản mâu thuẫn.
5. **Thư mục input chỉ chứa TÀI LIỆU, không chứa tooling.** Script tra cứu doc để ở `scripts/`.
6. **Đổi tên / gộp / xoá file phải cập nhật registry NGAY** (cùng lần thay đổi). Path chết trong
   registry làm mọi Source Quote trỏ vào đó không verify được — `health-check` **F-07/F-08** bắt việc này.

> ⚠️ **Không dựng bảng liệt kê DOC-ID trong file này.** Đây là thư mục input, không phải registry —
> 2 bản cùng số liệu là đúng lỗi `health-check` **G-02** (drift đa nguồn). Muốn biết file nào Active
> thì `ls`; muốn biết DOC-ID thì mở registry ở trên.

## Cấu trúc

```
00_input/
├── shared/          # tài liệu dùng chung mọi version
└── v2.0/
    ├── Doc/         # tài liệu đặc tả (.docx / .pdf / .md) — bản latest
    ├── Design/      # prototype / mockup UI
    └── README.md    # file này (quy ước, KHÔNG phải registry)
```
