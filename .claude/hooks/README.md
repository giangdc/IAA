# .claude/hooks — Ràng buộc "hiến pháp" harness-enforced

> Rule quan trọng nếu chỉ nằm trong SKILL.md sẽ bị model lờ (advisory). Các hook ở đây **ép** bằng harness (deterministic), không phụ thuộc thiện chí model. Wire trong `../settings.json`.

## Hook đang bật

| Hook | Event | Tác dụng |
|------|-------|----------|
| `validate-vibe-run.mjs` | **Stop** | Sau khi Claude định dừng: soi VR folder **mới nhất** (nếu vừa chạy <45') → gọi **`verify_evidence.py`** (engine detection). Có **fabrication evidence** (ảnh thiếu/gộp/link-chết/trích nhầm/không trích) → **CHẶN dừng**. Coverage-owed (TC NOT_RUN còn lại = partial hợp lệ) **KHÔNG** chặn. |
| `verify_evidence.py` | (bundled) | Engine audit 2 chiều TC↔ảnh + coverage (nguồn từ skill `vibe-test`). Hook gọi qua `--json`; chạy tay: `node validate-vibe-run.mjs --check <VR>`. Bundle ở đây để travel theo repo. |
| `inject-project-rule.mjs` | **SessionStart** | Chèn inventory `Project_rule.md` (path + section headers **cấp 2 VÀ cấp 3**) vào context mỗi session → không thể "quên đọc" rule dự án. |
| `run-python.mjs` | (bundled) | Dò interpreter Python **có thật** trên máy: `python3` → `python` → `py -3`, rồi forward **nguyên exit code** (2 = chặn). macOS/Linux không có `python`, Windows không có `python3` ⇒ hardcode tên nào cũng hỏng nửa team. Thiếu cả 3, hoặc thiếu file `.py` ⇒ **exit 0** (fail-safe, ⛔ không chặn). |
| `memory-guard.py` | **PostToolUse** (`Write`/`Edit`/`MultiEdit`) | Chặn **history creep** ở memory layer: trần dung lượng theo tầng (MASTER / router / leaf / WORKING-STATE / source MEMORY / FAIL-REGISTRY), trần **ô bảng**, và mẫu "số đã chết" (`số cũ:` · `trước đó:` · gạch ngang). Chỉ soi dòng **trong diff**, và **không chặn khi file đang thu nhỏ**. |
| `oracle_runs.py` | (bundled, **không wire hook**) | Oracle 12 kiểm của `/package-version --tier test-runs` — bản chép **byte-identical** của `~/.claude/skills/package-version/scripts/oracle_runs.py`. Bundle **ở đây chứ không ở `.claude/skills/`** vì `.claude/skills/` bị `.gitignore` mà vết audit phải **kiểm lại được** ⇒ script buộc nằm trong vùng tracked. Chạy tay: `python3 .claude/hooks/oracle_runs.py --baseline\|--check\|--audit`. `health-check` **H-06** đối chiếu 2 bản. |

### ⚠️ Giới hạn của `inject-project-rule.mjs` — phải biết để không tin nhầm

Hook này chèn **TÊN SECTION**, ⛔ **không chèn NỘI DUNG** rule.

⇒ Nó bảo đảm **"biết là có rule"**, ⛔ **không** bảo đảm **"tuân thủ rule"**.

Muốn chắc, skill vẫn phải **đọc file** trước khi ghi artifact. Coi inventory là bằng chứng đã tuân thủ là hiểu sai công dụng của hook.

### ⚠️ Hiệu chuẩn `memory-guard.py` trước khi tin vào nó

Mọi trần trong file là **giá trị khởi điểm**, không phải hằng số. Đọc docstring đầu file để biết cách đo và đặt lại.

🔒 **Phép thử ngược:** trần nào làm **file hiện có đỏ oan** là trần **SAI** — **nới trần**, ⛔ đừng sửa file. Trần sinh ra để chặn *lịch sử tích tụ*, không phải để ép *nội dung thật* phải nhỏ lại.

Hai thứ **phải khai theo project** (nếu không, hook chặn nhầm hoặc im lặng vô dụng):
- `VERSION_DIR_RE` — regex thư mục version. Không khớp convention thật ⇒ `classify_tier()` trả `None` ⇒ file **không có trần nào** mà hook vẫn "chạy bình thường".
- `strip_writeback()` / `strip_detail()` — các section **cố ý lớn dần** (đích write-back) phải được **trừ ra** trước khi đo. Không trừ = ép người ta cắt đúng chỗ được phép lưu lịch sử.

## "Best of both" — vì sao hook GỌI script
- **Script `verify_evidence.py`** = detection mạnh (bắt link-chết/batched/misattributed) nhưng nếu **AI tự gọi** thì = advisory (AI có thể quên/lờ).
- **Hook Stop** = harness tự chạy, AI **không bỏ được** → guarantee. Nhưng logic đếm đơn giản.
- **Kết hợp:** hook Stop **gọi** verify_evidence.py → vừa *đủ* (detection sâu) vừa *đúng* (cưỡng chế). Chặn fabrication (luôn sai); coverage đầy đủ vẫn do gate advisory trước khi §8=COMPLETED.

## Đặc tính an toàn
- **Fail-safe:** mọi lỗi parse / không tìm thấy file → **KHÔNG chặn** (exit 0). Hook không bao giờ làm kẹt session vì bug của chính nó.
- **Chỉ soi run FRESH** (<45'): run cũ không bị chặn lại mỗi lần dừng.
- **Chống loop:** tôn trọng `stop_hook_active`.
- **Cross-platform:** Node thuần, path tương đối (hook chạy từ project root). Chạy được Mac/Windows nếu có `node` trong PATH.

## Kiểm thủ công
```bash
node .claude/hooks/validate-vibe-run.mjs --check 08_test-runs/vibe/VR-XXX-YYYY-MM-DD   # exit 2 nếu fail
node .claude/hooks/inject-project-rule.mjs                                              # in JSON context
node .claude/hooks/run-python.mjs .claude/hooks/memory-guard.py < /dev/null                                        # no-op; xem docstring de chay that
```

## Tắt tạm
Xoá event tương ứng trong `../settings.json`, hoặc đổi tên VR folder để bỏ qua 1 run cụ thể.

## Convention `verify_evidence.py` phụ thuộc (skill vibe-test phải giữ)
- Folder run: `VR-<NNN>-<MOD>-<date>/` (legacy `VR-<NNN>-<date>` = chỉ cảnh báo).
- `vibe-log.md`: mỗi TC 1 section `## TC-<ID>` + dòng `**Evidence:**` **trích đúng tên file ảnh** trong `screenshots/`.
- `screenshots/`: mỗi TC đã chạy có ≥1 ảnh RIÊNG tên `TC-<ID>__(pre|verify|stepN-FAIL/BLOCKED)*.png`. Cấm 1 ảnh gộp nhiều TC.
- `scope-ledger.md` (per-run) + `coverage-<module>.md` (tích lũy): chấm coverage. Thiếu ledger → chỉ kiểm được evidence.
- Chi tiết đầy đủ: `~/.claude/skills/vibe-test/SKILL.md` §EVIDENCE MANDATORY RULE.
