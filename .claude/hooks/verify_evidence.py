#!/usr/bin/env python3
"""
vibe-test — EVIDENCE + COVERAGE GATE (lưới an toàn cuối run).

★ NGUỒN CHUẨN = `skills/vibe-test/scripts/verify_evidence.py`.
  Bản thứ hai ở `skills/init-project/assets/hooks/verify_evidence.py` là BẢN SAO BYTE-IDENTICAL,
  tồn tại để `/init-project` copy vào `.claude/hooks/` của project — hook Stop gọi được mà không
  phụ thuộc máy có cài toolkit hay không.
  ⚠️ SỬA NGUỒN CHUẨN XONG PHẢI COPY ĐÈ NGAY trong cùng lần thay đổi:
      cp skills/vibe-test/scripts/verify_evidence.py skills/init-project/assets/hooks/verify_evidence.py
  2 file phải luôn giống hệt nhau — `health-check` H-05 dùng `diff` để bắt lệch.

Kiểm 2 chiều, mỗi chiều bịt một kiểu khai khống đã xảy ra thật:

A. EVIDENCE — `vibe-log.md` ↔ FILE ẢNH THẬT trong `screenshots/`:
  · TC ghi PASS/FAIL/BLOCKED mà KHÔNG có file ảnh nào      → MISSING
  · 1 ảnh gộp nhiều TC (`TC-PD-002-003_x.png`)             → BATCHED
  · tên file không theo quy ước / sai slot                  → BADNAME · NO_VERIFY
  · ảnh của TC không hề xuất hiện trong vibe-log            → ORPHAN
  · log gom kết quả vào 1 bảng chung → không map được TC ↔ ảnh (LOG_FORMAT)

C. RÀNG BUỘC 2 CHIỀU TC ↔ ẢNH (rule 1 của QC — "ảnh trích dẫn phải tồn tại"):
   Chiều xuôi (output → file): section `## TC-<ID>` trong vibe-log phải TRÍCH tên ảnh, và
  · section không trích tên ảnh nào                          → NO_CITATION
  · trích tên ảnh KHÔNG có trên disk                         → DANGLING
  · trích ảnh mang TC ID của TC KHÁC                         → MIS_ATTRIBUTED
   Chiều ngược (file → output): mọi ảnh trong `screenshots/` phải được trích ở đúng chỗ
  · ảnh của TC nhưng section TC đó không trích               → UNCITED
  · ảnh không mang TC ID và không ai trích (trừ `_setup__`/`_recon__`) → UNCITED
   → Không có 2 chiều này thì QC lead bấm vào tên ảnh trong report là gặp link chết
     (VR-005: 2 link chết · VR-006: 8) mà gate vẫn xanh.

D. RUN FOLDER — tên folder + phiên chạy:
  · tên không theo `VR-<NNN>-<MOD>-<date>` (legacy `VR-<NNN>-<date>` = cảnh báo) → FOLDER_NAME
  · `<MOD>` không khớp `module X` trong header sổ cái        → MODULE_MISMATCH
    (nguồn thứ 2 độc lập: header sai → find_cumulative() âm thầm chấm nhầm sổ cái)
  · thiếu `vibe-report.md` / `vibe-log.md`                   → MISSING_FILES
  · file có mtime rơi vào ngày KHÔNG khai ở header `> Phiên:` → UNDECLARED_SESSION
    (ghi tiếp vào run cũ được phép — nhưng phải khai, xem SKILL.md §"Luật nối tiếp")

B. COVERAGE — sổ cái, ưu tiên `08_test-runs/vibe/coverage/coverage-<module>.md` (TÍCH LŨY xuyên run,
   tự tìm theo tên module trong header ledger) rồi mới tới `scope-ledger.md` của run:
  · TC còn nợ: `⏳ NOT_RUN` / `⚠️ NOT_EVIDENCED`             → §8 phải là PARTIAL
  · `⛔ N-A` hoặc `⏳ NOT_RUN` KHÔNG kèm lý do               → làm giả mẫu số
  · TC có kết quả trong log nhưng VẮNG trong ledger          → ledger lệch scope
  → Không có ledger: chỉ kiểm được evidence, KHÔNG kiểm được coverage
    (25/82 TC vẫn pass — đúng lỗ hổng của VR-013).

KHÔNG phải cơ chế enforcement chính. Tầng chính là inline gate "CHỐT TC" trong
references/execute.md (chụp TRƯỚC khi ghi kết quả, lúc app còn đúng state).
Script này chặn việc ghi §8 = COMPLETED khi còn thiếu, và in đúng phần sót.

Usage:
    python3 verify_evidence.py <run-folder> [--min-per-tc 1] [--json] [--quiet]
                               [--scope <file|TC-A,TC-B>] [--scope-prefix TC-TB]
                               [--ledger <path>]

    <run-folder>    = 08_test-runs/vibe/VR-<NNN>-<MOD>-<date>/
    --scope         = ĐÈ mẫu số scope: file (fragment TC .md) hoặc TC-A,TC-B.
                      Dùng khi audit run cũ chưa có sổ cái.
    --scope-prefix  = lọc prefix module khi file --scope cross-reference module khác
    --ledger        = ĐÈ nguồn chấm coverage (mặc định: coverage/coverage-<module>.md → scope-ledger.md)
    --no-mtime      = bỏ check phiên theo mtime (dùng khi repo vừa clone/copy → mtime vô nghĩa)

Exit code:
    0 = mọi TC trong scope có verdict cuối + đã evidenced → được ghi §8 = COMPLETED
    1 = còn thiếu (evidence / coverage / ràng buộc TC↔ảnh / folder / phiên) → §8 = PARTIAL
    2 = không audit được (không tìm thấy run folder, hoặc folder rỗng)
"""
import argparse
import datetime
import json
import os
import re
import sys

# Quy ước tên file evidence — PHẢI khớp §"Quy ước tên file" trong SKILL.md
NAME_RE = re.compile(
    r"^(?:"
    r"TC-[A-Z]+-\d+__(?:pre|verify|step\d+-(?:FAIL|BLOCKED))(?:-[a-z0-9-]+)?"
    r"|_(?:setup|recon)__[a-z0-9-]+"
    r"|BUG-\d+__[a-z0-9-]+"
    r")\.png$"
)
# TC ID hợp lệ (dùng cả khi parse log và khi tách prefix của file)
TC_ID_RE = re.compile(r"TC-[A-Z]+-\d+")
# Tên file gộp nhiều TC theo lối viết tắt: TC-VG-051-058-060-068-071_... / TC-PD-002-003_...
# (chỉ TC đầu có prefix, các TC sau chỉ còn số) — dạng này TC_ID_RE bắt được đúng 1 ID nên
# phải nhận diện riêng, nếu không ảnh gộp sẽ lọt gate.
TC_ID_RUN_RE = re.compile(r"(TC-[A-Z]+)-(\d+(?:-\d+)+)")
# Heading TC trong vibe-log.md: "## TC-TB-020 — ..." / "## TC-TB-020: ..."
TC_HEAD_RE = re.compile(r"^#{2,3}\s+(TC-[A-Z]+-\d+)\b")
# Heading bất kỳ — dùng để biết section TC kết thúc ở đâu (heading cùng cấp hoặc cao hơn)
HEAD_RE = re.compile(r"^(#{1,6})\s+")
# Dòng kết quả: "**Result: ✅ PASS ...**" / "**Result:** 🚫 BLOCKED"
RESULT_RE = re.compile(r"\*\*Result:?\*?\*?:?\s*(.+)$")
# Tên file ảnh được TRÍCH trong log/report (có thể kèm path: `screenshots/TC-X__verify.png`)
IMG_RE = re.compile(r"[A-Za-z0-9_\-./]+\.(?:png|jpe?g)", re.IGNORECASE)
# Header khai phiên: "> Phiên: 2026-07-21 (khởi tạo) · 2026-07-22 (follow-up)"
SESSION_RE = re.compile(r"^>?\s*\**\s*Phi[êe]n\s*:?\**\s*", re.IGNORECASE)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Tên run folder: VR-<NNN>-<MOD>-<date> (mới) · VR-<NNN>-<date> (legacy, chỉ cảnh báo)
FOLDER_RE = re.compile(r"^VR-(\d{3,})-([A-Z0-9]+)-(\d{4}-\d{2}-\d{2})$")
FOLDER_LEGACY_RE = re.compile(r"^VR-(\d{3,})-(\d{4}-\d{2}-\d{2})$")
# MOD không trỏ 1 module cụ thể → bỏ qua bước đối chiếu với header sổ cái
MOD_GENERIC = ("MULTI", "ALL")
# Ảnh không thuộc TC nào nhưng hợp lệ (preflight/recon) → không đòi trích dẫn
FREE_PREFIX = ("_setup__", "_recon__")

# Trạng thái ĐÃ CHẠY → bắt buộc phải có evidence
RAN_MARKS = {
    "PASS": ("PASS",),
    "FAIL": ("FAIL",),
    "BLOCKED": ("BLOCKED", "BLOCK"),
}
# Trạng thái KHÔNG đòi evidence
SKIP_MARKS = ("NOT_EVIDENCED", "SKIP", "N/A", "N-A", "DEPRECATED", "PENDING")


"""Verdict trong scope-ledger.md — phải khớp §"Verdict hợp lệ" của SKILL.md."""
# Verdict cuối: TC đã được xử lý xong, không còn nợ
LEDGER_FINAL = ("PASS", "FAIL", "BLOCKED", "N-A", "N/A", "NA")
# Verdict còn nợ: chặn §8 = COMPLETED
LEDGER_OPEN = ("NOT_RUN", "NOT_EVIDENCED")
# Verdict bắt buộc kèm lý do (cột cuối của dòng ledger không được trống/—)
LEDGER_NEEDS_REASON = ("NOT_RUN", "N-A", "N/A", "NA")


MODULE_RE = re.compile(r"module\s+([A-Za-z0-9_-]+)", re.IGNORECASE)


def ledger_module(path):
    """Tên module lấy từ header sổ cái: '# Scope Ledger — VR-020 — module TB — SCOPE_TOTAL = 82 TC'."""
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                m = MODULE_RE.search(line)
                if m:
                    return m.group(1)
            if line.lstrip().startswith("|"):
                break
    return None


def find_cumulative(run_dir, module):
    """`08_test-runs/vibe/coverage/coverage-<module>.md` — sổ cái TÍCH LŨY xuyên run.

    Đây mới là nguồn chấm coverage: module lớn chạy nhiều phiên, ledger của 1 phiên
    không biết các phiên khác đã làm gì → chấm trên ledger phiên sẽ báo còn nợ sai
    và §8 mãi không lên được COMPLETED.

    Layout (refactor 2026-08-04): sổ nằm trong `vibe/coverage/`. Vẫn thử vị trí CŨ
    (`vibe/coverage-<module>.md`, cùng cấp run) để không vỡ khi skill `vibe-test`
    chưa patch — nhưng vị trí cũ là dấu hiệu skill cũ.
    Run trong vùng sealed `vibe/v<X>/` thì `vibe/coverage/` cách 2 tầng, nên thử cả 2 độ sâu.
    """
    if not module:
        return None
    run_abs = os.path.abspath(run_dir)
    parent = os.path.dirname(run_abs)          # …/vibe  (hoặc …/vibe/v1.0 với run đã seal)
    grand = os.path.dirname(parent)            # …/08_test-runs (hoặc …/vibe)
    for cand in (
        os.path.join(parent, "coverage", f"coverage-{module}.md"),   # layout mới
        os.path.join(grand, "coverage", f"coverage-{module}.md"),    # run trong vibe/v<X>/
        os.path.join(parent, f"coverage-{module}.md"),               # layout CŨ (trước 04/08)
    ):
        if os.path.isfile(cand):
            return cand
    return None


def parse_ledger(path):
    """Đọc sổ cái (scope-ledger.md hoặc coverage-<module>.md) → {tc_id: {"verdict":…, "reason":…}}.

    Nhận dòng bảng markdown: | TC-TB-020 | ✅ PASS | 1 | run này | file.png |
    Verdict lấy từ cột 2, lý do/evidence = cột cuối cùng có nội dung.
    """
    ledger = {}
    if not path or not os.path.isfile(path):
        return ledger

    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            m = TC_ID_RE.fullmatch(cells[0].strip("`* "))
            if not m:
                continue
            verdict = cells[1].upper()
            for token in LEDGER_FINAL + LEDGER_OPEN:
                if token in verdict:
                    verdict = token
                    break
            else:
                verdict = "UNKNOWN"
            reason = cells[-1].strip("`* ") if len(cells) > 2 else ""
            if reason in ("—", "-", "–", ""):
                reason = ""
            ledger[cells[0].strip("`* ")] = {"verdict": verdict, "reason": reason}
    return ledger


def parse_scope_arg(value, prefix=None):
    """--scope: danh sách TC ID phân tách dấu phẩy, hoặc đường dẫn file chứa TC ID.

    File fragment thường **cross-reference** TC của module khác (vd fragment TC-TB nhắc
    TC-DV-001..009) → lọc theo `--scope-prefix`, hoặc tự lấy prefix áp đảo nếu không truyền,
    để mẫu số scope không bị phồng.
    """
    if os.path.isfile(value):
        with open(value, encoding="utf-8", errors="replace") as fh:
            ids = set(TC_ID_RE.findall(fh.read()))
    else:
        ids = {t.strip() for t in value.split(",") if TC_ID_RE.fullmatch(t.strip())}

    if not ids:
        return ids, None

    def pref(tc):
        return tc.rsplit("-", 1)[0]

    if prefix:
        chosen = prefix if prefix.startswith("TC-") else f"TC-{prefix}"
    else:
        counts = {}
        for tc in ids:
            counts[pref(tc)] = counts.get(pref(tc), 0) + 1
        chosen = max(counts, key=counts.get)
        if len(counts) == 1:
            return ids, None  # thuần 1 module, không cần cảnh báo

    dropped = sorted(tc for tc in ids if pref(tc) != chosen)
    return {tc for tc in ids if pref(tc) == chosen}, (chosen, dropped)


def parse_result(text):
    """Chuẩn hoá dòng **Result:** → PASS / FAIL / BLOCKED / NOT_EVIDENCED / SKIPPED."""
    up = text.upper()
    for mark in SKIP_MARKS:
        if mark in up:
            return "NOT_EVIDENCED" if mark == "NOT_EVIDENCED" else "SKIPPED"
    for norm, aliases in RAN_MARKS.items():
        if any(a in up for a in aliases):
            return norm
    return "UNKNOWN"


def parse_vibe_log(path):
    """→ (results, mentioned, cited_by_tc, cited_all, sessions).

    `results`     = {tc_id: result} — TC có section riêng (`## TC-...`), đơn vị audit được.
    `mentioned`   = mọi TC ID xuất hiện bất kỳ đâu trong log — dùng để phát hiện log gom hết
                    vào 1 bảng `## Results` (format drift), khi đó không audit được per-TC.
    `cited_by_tc` = {tc_id: [tên ảnh được trích TRONG section của chính TC đó]} — đây là thứ
                    cho phép kiểm rule 1: cái QC lead bấm vào phải là cái tồn tại trên disk.
    `cited_all`   = mọi tên ảnh được trích ở bất kỳ đâu trong log (gồm section follow-up).
    `sessions`    = ngày khai ở header `> Phiên: 2026-07-21 · 2026-07-22 (follow-up)`.

    Section của 1 TC kéo dài tới heading kế tiếp CÙNG CẤP hoặc CAO HƠN — nhờ vậy `**Evidence:**`
    (nằm SAU `**Result:**`) vẫn được tính, còn ảnh của section `## 🆕 Follow-up` không bị quy
    nhầm cho TC đứng trước nó.
    """
    results, cited_by_tc, sessions = {}, {}, set()
    if not os.path.isfile(path):
        return results, set(), cited_by_tc, set(), sessions

    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    cited_all = {os.path.basename(m) for m in IMG_RE.findall(text)}
    current, cur_level = None, 0

    for raw in text.splitlines():
        line = raw.strip()

        if SESSION_RE.match(line):
            sessions.update(DATE_RE.findall(line))
            continue

        head = HEAD_RE.match(line)
        if head:
            level = len(head.group(1))
            tc_head = TC_HEAD_RE.match(line)
            if tc_head:
                current, cur_level = tc_head.group(1), level
                results.setdefault(current, "UNKNOWN")
                cited_by_tc.setdefault(current, [])
            elif current and level <= cur_level:
                current = None  # rời section TC (vd sang `## 🆕 Follow-up session`)
            continue

        if current:
            m = RESULT_RE.search(line)
            if m and results[current] == "UNKNOWN":
                results[current] = parse_result(m.group(1))
            for img in IMG_RE.findall(line):
                cited_by_tc[current].append(os.path.basename(img))

    return results, set(TC_ID_RE.findall(text)), cited_by_tc, cited_all, sessions


def scan_screenshots(shot_dir):
    """→ (by_tc, batched, badname, non_tc) từ file thật trên disk."""
    by_tc, batched, badname, non_tc = {}, [], [], []
    if not os.path.isdir(shot_dir):
        return by_tc, batched, badname, non_tc

    for name in sorted(os.listdir(shot_dir)):
        low = name.lower()
        if not low.endswith((".png", ".jpg", ".jpeg")):
            continue  # file khác (csv/log) không tính là evidence

        # Dạng viết tắt "TC-VG-051-058-060_..." cũng được bung thành từng TC ID đầy đủ
        ids = tc_ids_of(name)

        # >1 TC ID trong 1 tên file = ảnh gộp nhiều case — lỗi bị cấm
        if len(ids) > 1:
            batched.append({"file": name, "tcs": sorted(ids)})
            for tc in ids:
                by_tc.setdefault(tc, []).append(name)
            continue

        ids = sorted(ids)

        if not NAME_RE.match(name):
            badname.append(name)

        if ids:
            by_tc.setdefault(ids[0], []).append(name)
        else:
            non_tc.append(name)

    return by_tc, batched, badname, non_tc


def slot_of(name):
    """'verify' | 'pre' | 'step' | None — phần sau `__` của tên file."""
    if "__" not in name:
        return None
    tail = name.split("__", 1)[1]
    for slot in ("verify", "pre"):
        if tail.startswith(slot):
            return slot
    if tail.startswith("step"):
        return "step"
    return None


def tc_ids_of(name):
    """Mọi TC ID mà tên file này mang, kể cả dạng viết tắt `TC-VG-051-058-060_...`."""
    ids = set(TC_ID_RE.findall(name))
    for prefix, nums in TC_ID_RUN_RE.findall(name):
        ids.update(f"{prefix}-{n}" for n in nums.split("-"))
    return ids


def resolve_citation(cited, tc, own_files, disk):
    """Tên ảnh được trích trong section TC → 'ok' | 'dangling' | 'misattr'.

    Chấp nhận lối viết tắt của template (`(+ __pre-credentials-filled.png)`): token không mang
    TC ID được coi là hợp lệ nếu khớp ĐUÔI một file của chính TC đó — vẫn truy ra 1 file thật.
    """
    if cited in disk:
        ids = tc_ids_of(cited)
        return "ok" if (not ids or tc in ids) else "misattr"
    if not TC_ID_RE.search(cited):
        if any(f.endswith(cited) for f in own_files):
            return "ok"
    return "dangling"


def check_binding(tc_results, cited_by_tc, cited_all, by_tc, non_tc, disk):
    """RÀNG BUỘC 2 CHIỀU TC ↔ ảnh (rule 1). → (no_citation, dangling, misattr, uncited)."""
    no_citation, dangling, misattr, uncited = [], [], [], []

    for tc, result in tc_results.items():
        if result not in ("PASS", "FAIL", "BLOCKED"):
            continue  # NOT_EVIDENCED/SKIPPED đã tự khai là không có evidence
        own = by_tc.get(tc, [])
        cites = cited_by_tc.get(tc, [])
        if not cites:
            no_citation.append({"tc": tc, "result": result, "files": own})
            continue
        for c in cites:
            verdict = resolve_citation(c, tc, own, disk)
            if verdict == "dangling":
                dangling.append({"tc": tc, "file": c})
            elif verdict == "misattr":
                misattr.append({"tc": tc, "file": c, "belongs": sorted(tc_ids_of(c))})

    # Chiều ngược: ảnh nằm trên disk mà section TC không hề trích → không map được khi audit
    for tc, files in by_tc.items():
        if tc not in tc_results:
            continue  # ảnh của TC không có trong log = ORPHAN, đã báo riêng
        cites = set(cited_by_tc.get(tc, []))
        loose = [c for c in cites if not TC_ID_RE.search(c)]
        for f in files:
            if f in cites or any(f.endswith(c) for c in loose):
                continue
            uncited.append({"tc": tc, "file": f})

    # Ảnh không mang TC ID: `_setup__`/`_recon__` được miễn, còn lại (vd `BUG-011__*`,
    # ảnh đặt tên tự do) phải được trích ở đâu đó trong log — nếu không thì không ai biết nó là gì.
    for f in non_tc:
        if f.startswith(FREE_PREFIX) or f in cited_all:
            continue
        uncited.append({"tc": "—", "file": f})

    return no_citation, dangling, misattr, sorted(uncited, key=lambda x: x["file"])


def check_folder_name(run_dir, module):
    """Tên run folder → {ok, legacy, mod, date, mismatch}."""
    name = os.path.basename(os.path.abspath(run_dir))
    m = FOLDER_RE.match(name)
    if m:
        mod, date = m.group(2), m.group(3)
        mismatch = bool(
            module and mod not in MOD_GENERIC and mod.upper() != module.upper()
        )
        return {"name": name, "ok": True, "legacy": False, "mod": mod, "date": date,
                "mismatch": mismatch, "ledger_module": module}
    m = FOLDER_LEGACY_RE.match(name)
    if m:
        return {"name": name, "ok": True, "legacy": True, "mod": None, "date": m.group(2),
                "mismatch": False, "ledger_module": module}
    return {"name": name, "ok": False, "legacy": False, "mod": None, "date": None,
            "mismatch": False, "ledger_module": module}


def scan_mtime_dates(run_dir):
    """{'YYYY-MM-DD': [file, …]} theo mtime — dùng để đối chiếu với phiên đã khai."""
    dates = {}
    for root, _dirs, files in os.walk(run_dir):
        for f in files:
            path = os.path.join(root, f)
            try:
                day = datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
            except OSError:
                continue
            dates.setdefault(day, []).append(os.path.relpath(path, run_dir))
    return dates


def check_sessions(run_dir, declared, folder_date, skip=False):
    """Ngày ghi file phải nằm trong danh sách phiên đã khai (hoặc chính ngày của folder).

    Ghi tiếp vào run cũ được PHÉP (retest 1 TC, xác nhận bug, chụp bù) — nhưng phải khai ở
    header `> Phiên:`, nếu không thì ảnh ngày sau nằm im trong folder ngày trước và không ai
    biết nó thuộc phiên nào (ca VR-004: 2 ảnh 22/07 trong folder 21/07, log dừng ở 09:32).

    Toàn bộ file cùng 1 ngày ≠ ngày folder → gần như chắc là clone/copy repo (mtime bị đặt lại)
    → chỉ cảnh báo, không tính vi phạm.
    """
    by_date = scan_mtime_dates(run_dir)
    known = set(declared) | ({folder_date} if folder_date else set())
    undeclared = {d: fs for d, fs in by_date.items() if d not in known}
    copied = len(by_date) == 1 and bool(folder_date) and folder_date not in by_date
    if skip or copied or not folder_date:
        return {"undeclared": {}, "declared": sorted(declared), "copied": copied,
                "skipped": skip, "dates": sorted(by_date)}
    return {"undeclared": undeclared, "declared": sorted(declared), "copied": False,
            "skipped": False, "dates": sorted(by_date)}


def audit(run_dir, min_per_tc, scope_arg=None, scope_prefix=None, ledger_arg=None,
          no_mtime=False):
    log_path = os.path.join(run_dir, "vibe-log.md")
    shot_dir = os.path.join(run_dir, "screenshots")

    # Nguồn chấm coverage, ưu tiên giảm dần:
    #   --ledger <path>  >  coverage-<module>.md (tích lũy)  >  scope-ledger.md (1 phiên)
    run_ledger_path = os.path.join(run_dir, "scope-ledger.md")
    module = ledger_module(run_ledger_path)
    cumulative = find_cumulative(run_dir, module)
    if ledger_arg:
        ledger_path, ledger_kind = ledger_arg, "--ledger"
    elif cumulative:
        ledger_path, ledger_kind = cumulative, f"coverage-{module}.md (tích lũy)"
    else:
        ledger_path, ledger_kind = run_ledger_path, "scope-ledger.md (chỉ run này)"
    ledger = parse_ledger(ledger_path)

    tc_results, mentioned, cited_by_tc, cited_all, sessions = parse_vibe_log(log_path)
    by_tc, batched, badname, non_tc = scan_screenshots(shot_dir)
    disk = {f for fs in by_tc.values() for f in fs} | set(non_tc)

    # ── D. RUN FOLDER: tên · file bắt buộc · phiên ─────────────────────────────
    folder = check_folder_name(run_dir, module)
    # Mọi run của vibe-test đều là EXECUTE/RETEST → luôn phải có log + report. (Mode EXPLORE đã bị
    # bỏ 2026-08-03; run folder cũ chỉ có `explore-report.md` sẽ bị báo thiếu file — đúng ý, vì nó
    # không phải run có evidence per-TC.)
    required = ["vibe-log.md", "vibe-report.md"]
    missing_files = [f for f in required if not os.path.isfile(os.path.join(run_dir, f))]
    sess = check_sessions(run_dir, sessions, folder["date"], skip=no_mtime)

    # Không có TC nào có section riêng → KHÔNG audit được per-TC, dù vì log gom hết vào 1 bảng
    # (`## Results`) hay vì log dùng TC ID sai định dạng. Đây chính là format của các run đã mất
    # sạch evidence → phải FAIL, tuyệt đối không im lặng pass.
    # (log không tồn tại → đã tính là missing_files, không báo trùng ở đây)
    log_format_broken = not tc_results and os.path.isfile(log_path)
    # TC được nhắc trong log nhưng không có section riêng (có thể là cross-reference) → cảnh báo
    unsectioned = sorted(mentioned - set(tc_results)) if tc_results else sorted(mentioned)

    missing, no_verify, ok = [], [], []
    for tc, result in tc_results.items():
        files = by_tc.get(tc, [])
        if result in ("SKIPPED", "NOT_EVIDENCED"):
            continue  # không đòi evidence (NOT_EVIDENCED đã tự khai là thiếu)
        if len(files) < min_per_tc:
            missing.append({"tc": tc, "result": result, "files": files})
            continue

        # Slot bắt buộc theo kết quả: PASS phải có ảnh tại điểm verify;
        # FAIL/BLOCKED phải có ảnh tại step lỗi (hoặc verify). File tên sai quy ước
        # (không có `__slot`) KHÔNG tính là evidence — nếu không, ảnh đặt tên tuỳ tiện
        # vẫn lọt gate và mất luôn khả năng map ảnh ↔ TC.
        need = ("verify",) if result == "PASS" else ("step", "verify")
        if not any(slot_of(f) in need for f in files):
            no_verify.append(
                {"tc": tc, "result": result, "files": files, "need": "/".join(need)}
            )
            continue
        ok.append(tc)

    orphan = sorted(set(by_tc) - set(tc_results))
    total_ran = len(ok) + len(missing) + len(no_verify)

    # ── C. RÀNG BUỘC 2 CHIỀU TC ↔ ẢNH (rule 1) ────────────────────────────────
    no_citation, dangling, misattr, uncited = check_binding(
        tc_results, cited_by_tc, cited_all, by_tc, non_tc, disk
    )
    # TC vừa có ảnh trên disk, vừa trích đúng tên ảnh đó trong section của mình
    bound_bad = {m["tc"] for m in no_citation + dangling + misattr}
    tc_bound = len([t for t in ok if t not in bound_bad])

    # ── B. COVERAGE ────────────────────────────────────────────────────────────
    scope_filter = None
    if scope_arg:
        scope, scope_filter = parse_scope_arg(scope_arg, scope_prefix)
    else:
        scope = set(ledger)
    has_scope = bool(scope)

    open_tcs, no_reason = [], []
    for tc in sorted(scope):
        entry = ledger.get(tc)

        if entry is None:
            # Không có dòng ledger → lấy vibe-log làm nguồn dự phòng (hữu ích khi audit
            # lại run cũ chưa có ledger). Không dấu vết ở đâu cả = chưa chạy.
            log_result = tc_results.get(tc)
            if log_result in ("PASS", "FAIL", "BLOCKED"):
                continue  # có verdict trong log → tính là đã xử lý
            verdict = (
                log_result if log_result in ("NOT_EVIDENCED", "SKIPPED") else "KHÔNG_CÓ_DẤU_VẾT"
            )
            open_tcs.append({"tc": tc, "verdict": verdict, "reason": ""})
            continue

        if entry["verdict"] in LEDGER_OPEN or entry["verdict"] == "UNKNOWN":
            open_tcs.append({"tc": tc, "verdict": entry["verdict"], "reason": entry["reason"]})
        if entry["verdict"] in LEDGER_NEEDS_REASON and not entry["reason"]:
            no_reason.append({"tc": tc, "verdict": entry["verdict"]})

    # TC có kết quả trong log nhưng vắng trong ledger → ledger lệch scope
    not_in_ledger = sorted(set(tc_results) - set(ledger)) if ledger else []

    return {
        "run": os.path.basename(os.path.abspath(run_dir)),
        "tc_in_log": len(tc_results),
        "tc_ran": total_ran,
        "tc_evidenced": len(ok),
        "image_files": len({f for fs in by_tc.values() for f in fs}) + len(non_tc),
        "log_format_broken": log_format_broken,
        "tc_mentioned": len(mentioned),
        "unsectioned": unsectioned,
        "missing": missing,
        "no_verify": no_verify,
        "batched": batched,
        "badname": sorted(badname),
        "orphan": orphan,
        "not_evidenced_in_log": [t for t, r in tc_results.items() if r == "NOT_EVIDENCED"],
        # ràng buộc TC ↔ ảnh (rule 1)
        "tc_bound": tc_bound,
        "no_citation": no_citation,
        "dangling": dangling,
        "misattr": misattr,
        "uncited": uncited,
        # run folder
        "folder": folder,
        "missing_files": missing_files,
        "sessions": sess,
        # coverage
        "has_scope": has_scope,
        "module": module,
        "scope_source": ledger_kind if not scope_arg else f"--scope {scope_arg}",
        "cumulative_missing": cumulative is None and not scope_arg and bool(ledger),
        "scope_filter": {"kept_prefix": scope_filter[0], "dropped": scope_filter[1]}
        if scope_filter
        else None,
        "scope_total": len(scope),
        "scope_final": len(scope) - len(open_tcs) if has_scope else 0,
        "open_tcs": open_tcs,
        "no_reason": no_reason,
        "not_in_ledger": not_in_ledger,
    }


def violated(res):
    """VI PHẠM (phải sửa): thiếu evidence · PASS thiếu `__verify` · ảnh gộp nhiều TC ·
    log không audit được per-TC · ledger lệch scope · verdict thiếu lý do bắt buộc ·
    ràng buộc TC↔ảnh đứt (rule 1) · run folder sai tên/thiếu file/phiên không khai."""
    return bool(
        res["missing"]
        or res["no_verify"]
        or res["batched"]
        or res["log_format_broken"]
        or res["not_in_ledger"]
        or res["no_reason"]
        # rule 1 — ràng buộc 2 chiều TC ↔ ảnh
        or res["no_citation"]
        or res["dangling"]
        or res["misattr"]
        or res["uncited"]
        or res["orphan"]
        # run folder
        or not res["folder"]["ok"]
        or res["folder"]["mismatch"]
        or res["missing_files"]
        or res["sessions"]["undeclared"]
    )


def failed(res):
    """Không được ghi §8 = COMPLETED: có vi phạm, HOẶC còn TC nợ — dù là tự khai
    NOT_EVIDENCED trong log hay ⏳ NOT_RUN trong ledger (trung thực nhưng chưa xong)."""
    return violated(res) or bool(res["not_evidenced_in_log"]) or bool(res["open_tcs"])


def report(res, quiet=False):
    bad = res["missing"] + res["no_verify"]
    if violated(res):
        head = "❌ GATE FAIL"
    elif res["not_evidenced_in_log"] or res["open_tcs"]:
        head = "⚠️  RUN CHƯA HOÀN TẤT (không vi phạm, nhưng còn TC nợ)"
    else:
        head = "✅ GATE PASS"
    print(f"{head} — {res['run']}")
    print(
        f"   Evidence: {res['tc_evidenced']}/{res['tc_ran']} TC đã chạy "
        f"· {res['tc_in_log']} TC có section trong log · {res['image_files']} file ảnh"
    )
    print(
        f"   Trích dẫn: {res['tc_bound']}/{res['tc_ran']} TC có ảnh THẬT được trích đúng trong "
        "section của mình (rule 1)"
    )
    if res["has_scope"]:
        print(
            f"   Coverage: {res['scope_final']}/{res['scope_total']} TC của scope có verdict cuối "
            f"· còn nợ {len(res['open_tcs'])}   (scope từ: {res['scope_source']})"
        )
        if res["scope_filter"]:
            f = res["scope_filter"]
            print(
                f"             ℹ️ lọc scope về prefix {f['kept_prefix']}, bỏ "
                f"{len(f['dropped'])} TC cross-reference module khác: {', '.join(f['dropped'][:6])}"
            )
        if res["cumulative_missing"]:
            mod = res["module"] or "<module>"
            print(
                f"             ⚠️ chưa có `coverage-{mod}.md` (sổ cái tích lũy) → đang chấm trên"
                " ledger của 1 phiên."
                f"\n                Module cần nhiều phiên: tạo/merge `coverage-{mod}.md` (Step 4.5),"
                " nếu không mỗi phiên lại đếm lại từ 0."
            )
    else:
        print(
            "   Coverage: ⚠️ KHÔNG kiểm được — thiếu `scope-ledger.md` (và không truyền --scope)."
            "\n             → không biết scope thật bao nhiêu TC; 25/82 cũng sẽ 'pass'."
        )

    fold = res["folder"]
    if not fold["ok"]:
        print(f"\n🚫 TÊN RUN FOLDER SAI QUY ƯỚC: `{fold['name']}`")
        print("   Đúng: `VR-<NNN>-<MOD>-<YYYY-MM-DD>` (vd `VR-020-TB-2026-07-30`)")
        print("   MOD = prefix TC ID viết hoa (TB · VG · PD…) · nhiều module = MULTI · không filter = ALL")
    elif fold["mismatch"]:
        print(
            f"\n🚫 MODULE LỆCH: tên folder ghi `{fold['mod']}` nhưng header sổ cái ghi "
            f"`module {fold['ledger_module']}`"
        )
        print("   2 nguồn phải khớp — sai header thì gate tìm nhầm `coverage-<module>.md` và"
              " chấm coverage trên mẫu số của module khác.")
    elif fold["legacy"] and not quiet:
        print(f"\nℹ️  Tên folder dạng legacy (`VR-NNN-date`), thiếu MOD: `{fold['name']}`")
        print("   Run cũ giữ nguyên, KHÔNG đổi tên. Run mới dùng `VR-<NNN>-<MOD>-<date>`.")

    if res["missing_files"]:
        print(f"\n🚫 THIẾU FILE BẮT BUỘC CỦA RUN: {', '.join(res['missing_files'])}")
        print("   Run folder chỉ có ảnh mà không có log/report = không ai biết ảnh đó chứng minh gì")
        print("   (đúng ca VR-018 / VR-019 / retest-BUG-015: 1–2 ảnh, không log, không report).")

    sess = res["sessions"]
    if sess["undeclared"]:
        print(f"\n🚫 PHIÊN KHÔNG KHAI ({len(sess['undeclared'])} ngày) — ghi tiếp vào run cũ phải khai:")
        for day, files in sorted(sess["undeclared"].items()):
            head_files = ", ".join(sorted(files)[:4]) + (f" (+{len(files) - 4})" if len(files) > 4 else "")
            print(f"   · {day}: {head_files}")
        print(f"   Đã khai: {', '.join(sess['declared']) or '(không có dòng `> Phiên:`)'}"
              f" · ngày của folder: {res['folder']['date']}")
        print("   Sửa: thêm vào header vibe-log.md → `> Phiên: <ngày tạo> · <ngày làm tiếp> (follow-up)`")
        print("        + mỗi phiên tiếp là 1 section riêng trong log (vd `## 🆕 Follow-up 2026-07-28`).")
    elif sess["copied"] and not quiet:
        print("\nℹ️  Bỏ qua check phiên: mọi file cùng 1 ngày mtime khác ngày folder → folder có vẻ"
              " được clone/copy (mtime bị đặt lại), không phải chạy nối tiếp.")

    if res["log_format_broken"]:
        print("\n🚫 vibe-log.md KHÔNG AUDIT ĐƯỢC: 0 TC có section riêng.")
        if res["tc_mentioned"]:
            print(
                f"   Log nhắc {res['tc_mentioned']} TC nhưng gom kết quả vào 1 bảng chung"
                " (`## Results`) → không map được TC ↔ evidence."
            )
        else:
            print("   Log không chứa TC ID nào ở dạng chuẩn `TC-<MOD>-<NNN>` (vd `TC-PV-004`).")
            print("   Dùng đúng TC ID của TC-MASTER, không viết tắt (`PV-004`, `DSCS-041`).")
        print("   Sửa: mỗi TC 1 section `## TC-<ID>: <tên>` + bảng step có cột Evidence")
        print("        + dòng `**Result:**` + `**Evidence:**` (xem execute.md Step 5).")

    if res["missing"]:
        print(f"\n🚫 THIẾU EVIDENCE ({len(res['missing'])} TC) — KHÔNG được ghi PASS:")
        for m in res["missing"]:
            print(f"   · {m['tc']:<18} log ghi {m['result']:<8} nhưng 0 file ảnh")

    if res["no_verify"]:
        print(f"\n⚠️  CÓ ẢNH NHƯNG SAI SLOT / SAI QUY ƯỚC TÊN ({len(res['no_verify'])} TC):")
        for m in res["no_verify"]:
            print(
                f"   · {m['tc']:<18} {m['result']:<8} cần `__{m['need']}`, "
                f"chỉ có: {', '.join(m['files'])}"
            )

    if res["no_citation"]:
        print(f"\n🚫 SECTION TC KHÔNG TRÍCH TÊN ẢNH ({len(res['no_citation'])} TC) — rule 1:")
        for m in res["no_citation"]:
            have = ", ".join(m["files"]) if m["files"] else "(không có ảnh nào)"
            print(f"   · {m['tc']:<18} {m['result']:<8} trên disk có: {have}")
        print("   Ảnh có tồn tại vẫn chưa đủ — section TC phải TRÍCH tên file, nếu không người")
        print("   audit phải tự đoán ảnh nào của TC nào. Thêm dòng:")
        print("     **Evidence:** `screenshots/TC-<ID>__verify-<slug>.png`")

    if res["dangling"]:
        print(f"\n🚫 TRÍCH ẢNH KHÔNG TỒN TẠI ({len(res['dangling'])}) — rule 1, link chết khi audit:")
        for m in res["dangling"]:
            print(f"   · {m['tc']:<18} trích `{m['file']}` — không có trên disk")
        print("   Trích ĐÚNG tên file thật (copy từ tool response lúc chụp), không gõ lại từ trí nhớ.")

    if res["misattr"]:
        print(f"\n🚫 TRÍCH ẢNH CỦA TC KHÁC ({len(res['misattr'])}) — rule 1:")
        for m in res["misattr"]:
            print(f"   · section {m['tc']:<18} trích `{m['file']}` (ảnh của {', '.join(m['belongs'])})")
        print("   Mỗi TC trích ảnh của CHÍNH nó — dùng ảnh TC khác làm evidence là sai quy kết.")

    if res["uncited"]:
        print(f"\n🚫 ẢNH KHÔNG ĐƯỢC TRÍCH TRONG LOG ({len(res['uncited'])} file) — rule 1 chiều ngược:")
        for m in res["uncited"]:
            where = f"section {m['tc']}" if m["tc"] != "—" else "bất kỳ đâu trong log"
            print(f"   · {m['file']:<52} không xuất hiện ở {where}")
        print("   Ảnh không ai trích = không biết nó chứng minh điều gì (ca VR-004: 2 ảnh 22/07 thả")
        print("   vào folder run 21/07). Trích nó vào đúng section, hoặc xoá nếu là ảnh thừa.")
        print("   Miễn trừ: `_setup__*` · `_recon__*` (preflight/recon, không thuộc TC nào).")

    if res["batched"]:
        print(f"\n🚫 ẢNH GỘP NHIỀU TC ({len(res['batched'])} file) — banned:")
        for b in res["batched"]:
            print(f"   · {b['file']}  → gộp {len(b['tcs'])} TC: {', '.join(b['tcs'])}")
        print("   Mỗi TC phải có file RIÊNG (kể cả khi verify trên cùng 1 state).")

    if res["unsectioned"] and not quiet:
        print(
            f"\n⚠️  TC được nhắc trong log nhưng KHÔNG có section riêng ({len(res['unsectioned'])}): "
            f"{', '.join(res['unsectioned'])}"
        )
        print("   (cross-reference thì bỏ qua; nếu là TC đã chạy → thiếu section = thiếu audit trail)")

    if res["badname"] and not quiet:
        print(f"\n⚠️  SAI QUY ƯỚC TÊN ({len(res['badname'])} file):")
        for n in res["badname"]:
            print(f"   · {n}")
        print("   Đúng: TC-<ID>__verify[-slug].png · __pre · __step<N>-FAIL/BLOCKED · _setup__ · _recon__ · BUG-<N>__")

    if res["orphan"]:
        print(f"\n🚫 ẢNH CỦA TC KHÔNG CÓ SECTION TRONG vibe-log ({len(res['orphan'])} TC) — rule 1:")
        print(f"   {', '.join(res['orphan'])}")
        print("   Ảnh mang tên 1 TC nhưng TC đó không có section nào trong log → trông như evidence")
        print("   của một lần chạy không được ghi lại (ca VR-018/VR-019). Thêm section `## TC-<ID>`")
        print("   với `**Result:**` + `**Evidence:**`, hoặc xoá ảnh nếu nó không chứng minh gì.")

    if res["not_in_ledger"]:
        print(
            f"\n🚫 LEDGER LỆCH SCOPE — {len(res['not_in_ledger'])} TC có kết quả trong log nhưng"
            f" VẮNG trong scope-ledger.md: {', '.join(res['not_in_ledger'])}"
        )
        print("   Ledger phải kê ĐỦ mọi TC của scope (SCOPE_TOTAL), không chỉ TC đã chạy.")

    if res["no_reason"]:
        print(f"\n🚫 VERDICT THIẾU LÝ DO BẮT BUỘC ({len(res['no_reason'])} TC):")
        for m in res["no_reason"]:
            print(f"   · {m['tc']:<18} {m['verdict']} — cột cuối ledger trống")
        print("   `⏳ NOT_RUN` và `⛔ N-A` phải kèm lý do cụ thể, nếu không = làm giả mẫu số.")

    if res["open_tcs"]:
        by_verdict = {}
        for m in res["open_tcs"]:
            by_verdict.setdefault(m["verdict"], []).append(m["tc"])
        print(f"\n⏳ CÒN NỢ COVERAGE ({len(res['open_tcs'])} TC trên tổng {res['scope_total']}):")
        for verdict, tcs in sorted(by_verdict.items()):
            head_list = ", ".join(tcs[:12]) + (f" … (+{len(tcs) - 12})" if len(tcs) > 12 else "")
            print(f"   · {verdict:<18} {len(tcs):>3} TC: {head_list}")

    if res["not_evidenced_in_log"]:
        print(
            f"\nℹ️  Đã tự khai ⚠️ NOT_EVIDENCED trong log ({len(res['not_evidenced_in_log'])}): "
            f"{', '.join(res['not_evidenced_in_log'])}"
        )
        print("   Trung thực — nhưng run CHƯA hoàn tất: các TC này không tính PASS.")

    rerun = sorted(
        {m["tc"] for m in bad}
        | {t for b in res["batched"] for t in b["tcs"]}
        | set(res["not_evidenced_in_log"])
    )

    notes = f"evidence: {res['tc_evidenced']}/{res['tc_ran']} TC"
    if res["has_scope"]:
        notes = (
            f"scope {res['scope_total']}: có verdict {res['scope_final']} · "
            f"còn nợ {len(res['open_tcs'])} · " + notes
        )

    if violated(res):
        print("\n→ Xử lý VI PHẠM (theo execute.md Step 6.5):")
        print("   1. Thiếu evidence: quay lại state RẺ → chụp bù (1 file/TC), chạy lại script")
        print("   2. Không bù được → hạ TC đó thành ⚠️ NOT_EVIDENCED (vibe-log + ledger + report + §4)")
        print("   3. Ledger lệch scope / thiếu lý do → kê đủ SCOPE_TOTAL + ghi lý do, chạy lại script")
        print("   4. Rule 1 (trích dẫn): sửa NGAY TRONG LOG — thêm `**Evidence:**` với tên file THẬT,")
        print("      sửa tên trích sai, trích nốt ảnh chưa ai nhắc. KHÔNG cần chạy lại TC.")
        print("   5. Folder sai tên / thiếu phiên: đổi tên folder về `VR-<NNN>-<MOD>-<date>` (chỉ khi")
        print("      chưa ai tham chiếu), khai `> Phiên:` ở header log cho ngày làm tiếp.")
        print(f"   6. Ghi §8 = PARTIAL, Notes: `{notes}`")
        if rerun:
            print(f"   7. Chạy lại CHỈ phần sót:  /vibe-test --tc {','.join(rerun)}")
        print("   ⚠️ KHÔNG đổi tên/copy ảnh cho khớp log, KHÔNG xoá TC khỏi ledger, KHÔNG sửa mtime")
        print("      để lách gate — đó là làm giả evidence.")
    elif res["not_evidenced_in_log"] or res["open_tcs"]:
        print(f"\n→ Ghi §8 = PARTIAL, Notes: `{notes}`")
        print("   Report phải có bảng Scope Coverage; ledger ghi lý do cho từng TC còn nợ.")
        if res["open_tcs"]:
            print("   Chạy tiếp phần còn nợ:  /vibe-test --module <X>   (pending tự bốc đúng phần này)")
        if rerun and res["not_evidenced_in_log"]:
            print(f"   Bổ sung evidence:  /vibe-test --tc {','.join(sorted(set(res['not_evidenced_in_log'])))}")
    else:
        print(f"\n→ Được ghi §8 = COMPLETED (Notes phải có `{notes}`)")


def main():
    ap = argparse.ArgumentParser(description="vibe-test evidence + coverage gate")
    ap.add_argument("run_dir", help="08_test-runs/vibe/VR-<NNN>-<date>/")
    ap.add_argument("--min-per-tc", type=int, default=1, help="số ảnh tối thiểu mỗi TC (default 1)")
    ap.add_argument(
        "--scope",
        help="ĐÈ mẫu số scope: đường dẫn file (fragment TC .md) hoặc TC-A,TC-B. "
        "Mặc định đọc scope-ledger.md trong run folder",
    )
    ap.add_argument(
        "--ledger",
        help="ĐÈ nguồn chấm coverage: đường dẫn sổ cái. Mặc định ưu tiên "
        "coverage-<module>.md (tích lũy) rồi mới tới scope-ledger.md của run",
    )
    ap.add_argument(
        "--scope-prefix",
        help="lọc scope theo prefix module (vd TC-TB) khi file --scope có cross-reference "
        "TC của module khác; không truyền → tự lấy prefix áp đảo",
    )
    ap.add_argument(
        "--no-mtime",
        action="store_true",
        help="bỏ check phiên theo mtime (repo vừa clone/copy → mtime không còn phản ánh phiên chạy)",
    )
    ap.add_argument("--json", action="store_true", help="in JSON thay vì bảng")
    ap.add_argument("--quiet", action="store_true", help="bỏ mục badname/orphan")
    args = ap.parse_args()

    if not os.path.isdir(args.run_dir):
        print(f"✗ Không thấy run folder: {args.run_dir}", file=sys.stderr)
        return 2
    if not any(os.scandir(args.run_dir)):
        print(f"✗ Run folder rỗng: {args.run_dir}", file=sys.stderr)
        return 2
    # Thiếu vibe-log.md KHÔNG còn là "lỗi input" cho qua: run chỉ có mỗi ảnh chính là ca mất dấu
    # tệ nhất (VR-018/VR-019) → vẫn audit và tính là VI PHẠM missing_files.

    res = audit(
        args.run_dir,
        args.min_per_tc,
        scope_arg=args.scope,
        scope_prefix=args.scope_prefix,
        ledger_arg=args.ledger,
        no_mtime=args.no_mtime,
    )
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        report(res, quiet=args.quiet)

    return 1 if failed(res) else 0


if __name__ == "__main__":
    sys.exit(main())
