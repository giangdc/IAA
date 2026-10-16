# Execution Runs — Index

> Bảng tra **mọi lần chạy suite**. Cách ghi: `execute-maintain`.
>
> | Tầng | File | Phạm vi | Bất biến? |
> |---|---|---|---|
> | **A. File RUN** | `RUN-NNN-S<N>-<scope>-<date>.md` | 1 lần chạy suite | ✅ viết 1 lần |
> | **B. FAIL registry** | `FAIL-REGISTRY.md` | lỗi sống xuyên nhiều RUN | ❌ **ghi đè** |
> | **C. TR log** | `TR-S<N>-v<ver>-<date>[-<account>].md` | 1 ngày / 1 người = nhiều RUN | ❌ append trong ngày |
> | **D. Index** | file này | toàn bộ | ❌ thêm 1 dòng |
>
> ⛔ **1 RUN = 1 FILE, không phải thư mục.** Chỉ nâng lên thư mục khi run thật sự sinh artifact kèm.
> 🔴 **Cấp ID: `max + 1`, ⛔ KHÔNG tái dụng ID — kể cả các lỗ trống.**

| RUN | Ngày | Sprint | Module | Scope | Kết quả | Chi tiết | TR |
|---|---|---|---|---|---|---|---|
