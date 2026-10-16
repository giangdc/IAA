#!/usr/bin/env python3
"""oracle_runs.py — oracle của tầng `08_test-runs/`, chứng minh một lượt ĐÓNG GÓI không mất căn cứ.

Song song với `oracle_pack.py` của tầng analyze, nhưng gác thứ khác:
tầng này không có `Source Quote` per REQ — nó có **verdict per-TC** và **đường dẫn evidence**.

Bảng kiểm canonical: skill `package-version` → `references/runs-oracle.md` (luật đã rời repo 2026-09-08;
`Project_rule.md` section `Đóng gói test-runs` — địa chỉ cũ `§13.6` — giữ H2 stub trỏ về đó). File này là bản THỰC THI; rule là bản lưu chính thức.
🔑 File này CÓ CHỦ ĐÍCH ở lại vùng TRACKED của repo — vết audit `.close-run/` phải có công cụ kiểm
lại được; `.claude/skills/` bị `.gitignore` nên bản duy nhất ⛔ không được nằm trong đó.

    python3 .claude/hooks/oracle_runs.py --baseline          # chụp mốc (working tree SẠCH)
    python3 .claude/hooks/oracle_runs.py --check             # đối chiếu với mốc
    python3 .claude/hooks/oracle_runs.py --audit             # chỉ đo, không cần mốc

🔑 Ranh giới: oracle gác **MẤT CĂN CỨ**. Nó ⛔ KHÔNG gác việc thay phát biểu A bằng phát biểu B —
chỗ đó chỉ người đọc diff mới bắt được. Người điều phối **bắt buộc đọc diff** trước khi commit.
"""
import argparse
import hashlib
import subprocess
import json
import os
import re
import sys
from collections import Counter, defaultdict
from glob import glob

# 🔑 Gốc repo lấy bằng `git rev-parse`, ⛔ KHÔNG suy từ vị trí file: script này có 2 bản
# (trong skill và bản chép ở `.claude/hooks/`) nằm ở độ sâu KHÁC nhau — suy theo vị trí thì
# một trong hai bản luôn trỏ sai gốc và mọi glob trả rỗng, im lặng.
def _repo_root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True, cwd=os.getcwd())
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

REPO = _repo_root()
VIBE = os.path.join(REPO, "08_test-runs", "vibe")
RUNS = os.path.join(REPO, "08_test-runs", "runs")
# ⛔ KHÔNG còn thư mục state. Giữ hằng số chỉ để `read_allow_legacy()` đọc được dotfile
# của dự án CHƯA migrate; dự án mới ⛔ không tạo thư mục này.
STATE_DIR = os.path.join(REPO, ".close-run")

ID_RE = re.compile(r"\b(?:TC|SC|REQ|CL|RISK|BUG|FCP|VR|RUN|TR|FR|AC|ERR|MSG|DOC|GAP|FX|FAIL)-[A-Z]*-?\d+\b")
TC_CELL_RE = re.compile(r"^TC-[A-Z]+-\d+$")
PNG_RE = re.compile(r"[A-Za-z0-9_./…-]+\.png")
# 🪤 Loại `|` khỏi 2 lớp ký tự: `⛔` nằm trong Ô BẢNG (cột Verdict) thì regex cũ nuốt cả
# các ô bên cạnh — nên chỉ cần RE-POINT đường dẫn evidence (thao tác HỢP LỆ của đóng gói)
# là câu ⛔ bị đọc thành "mất". Cùng nguyên tắc `oracle_pack.py` đã dùng.
STOP_RE = re.compile(r"[^.!?\n|]*⛔[^.!?\n|]*")
INQ_RE = re.compile(r'\*"[^"]{4,}"\*')
VERDICTS = ("PASS", "FAIL", "BLOCKED", "N-A", "N/A", "NOT_RUN", "NOT_EVIDENCED")

# Nhãn khai báo "ảnh này đã bị hạ CÓ CHỦ ĐÍCH khi đóng gói" — đặt ngay sau tên ảnh trong sổ.
# Xem skill `package-version` -> `references/runs-packaging.md` §"Trích dẫn ảnh đã hạ CÓ CHỦ ĐÍCH".
# 🔑 Khớp theo TIỀN TỐ: có nhiều tầng xoá (`[đã hạ tầng A — git show …]` · `[đã hạ tầng B]`),
# và nhãn tầng A còn mang kèm lệnh lấy lại ⇒ so khớp chuỗi đầy đủ sẽ bỏ sót.
DECLARED_DROPPED = "[đã hạ tầng "

# Ô `Verdict` phải MỞ ĐẦU bằng token và không nhắc token khác (bẫy substring của
# `verify_evidence.py`: `❌ FAIL — đã PASS ở tier automation` bị đọc thành PASS).
VERDICT_HEAD_RE = re.compile(r"^[^A-Za-z]*(?:\*\*)?(PASS|FAIL|BLOCKED|N-A|N/A|NOT_RUN|NOT_EVIDENCED)\b")


def md_files():
    out = sorted(glob(os.path.join(VIBE, "**", "*.md"), recursive=True))
    out += sorted(glob(os.path.join(RUNS, "**", "*.md"), recursive=True))
    return out


def clean(text):
    """Bỏ nhấn mạnh markdown TRƯỚC khi bóc token — nếu không, `**TC-X**__slot.png` bị cắt đôi."""
    return text.replace("**", "").replace("`", "").replace("*", "")


def table_rows(text):
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            yield line, cells


def md_from_ref(ref):
    """[(relpath, text)] mọi .md dưới 08_test-runs/ tại một git ref — ⛔ không cần file mốc."""
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref, "--", "08_test-runs"],
                       capture_output=True, text=True, cwd=REPO)
    if r.returncode:
        sys.exit(f"⛔ ref không đọc được: {ref} ({r.stderr.strip()})")
    out = []
    for f in sorted(x for x in r.stdout.split("\n") if x.endswith(".md")):
        b = subprocess.run(["git", "show", f"{ref}:{f}"], capture_output=True, text=True, cwd=REPO)
        if b.returncode == 0:
            out.append((f, b.stdout))
    if not out:
        sys.exit(f"⛔ ở ref {ref} không có .md nào dưới 08_test-runs/ — mốc sai, ⛔ đừng đoán.")
    return out


def snap(ref=None):
    """Mốc: định danh · verdict per-TC · trích dẫn evidence · câu ⛔ · trích nguyên văn inline.

    🔑 `ref` != None ⇒ đọc từ git thay vì đĩa. Mốc CHÍNH LÀ một commit; lưu ra `.base.json`
    chỉ tạo thêm thứ có thể MẤT — và khi mất, chạy lại `--baseline` trên tree đã đóng gói
    cho ra mốc vô nghĩa, `--check` PASS trơn tru mà không kiểm gì.
    """
    ids = defaultdict(list)
    verdicts, stops, inq, files = {}, set(), set(), {}
    src = md_from_ref(ref) if ref else [(os.path.relpath(p, REPO),
                                         open(p, encoding="utf-8", errors="replace").read())
                                        for p in md_files()]
    for rel, raw in src:
        files[rel] = len(raw.encode("utf-8"))
        flat = clean(raw)
        for m in ID_RE.finditer(flat):
            ids[m.group(0)].append(rel)
        for s in STOP_RE.findall(raw):
            t = " ".join(s.split())
            if len(t) > 8:
                stops.add(t)
        for s in INQ_RE.findall(raw):
            inq.add(" ".join(s.split()))
        # verdict per-TC CHỈ lấy từ sổ coverage (nguồn canonical), ⛔ không lấy từ ledger phiên:
        # ledger là bằng chứng của 1 lượt, sổ mới là trạng thái cuối.
        if os.path.basename(rel).startswith("coverage-"):
            for _, cells in table_rows(raw):
                tc = cells[0].strip("`* ")
                if not TC_CELL_RE.match(tc):
                    continue
                up = cells[1].upper()
                v = next((t for t in VERDICTS if t in up), "UNKNOWN")
                verdicts[f"{os.path.basename(rel)}::{tc}"] = v
    ev = check_evidence_paths()
    return {
        "ids": {k: sorted(set(v)) for k, v in ids.items()},
        "verdicts": verdicts,
        "stops": sorted(stops),
        "inq": sorted(inq),
        "files": files,
        # 🔑 Mốc ghi luôn tập `dangling` ĐANG CÓ. `--check` chỉ đỏ khi xuất hiện cái MỚI.
        # Nếu không: 15 `dangling` có sẵn (hệ quả tầng B) làm oracle đỏ vĩnh viễn ⇒ mất tác
        # dụng làm gate "lượt sửa này có làm vỡ gì không", và cảnh báo đỏ oan bị bỏ qua mỗi
        # lần sẽ dạy cả người lẫn agent bỏ qua nó luôn (`§10.5` phép thử ngược).
        "dangling": sorted(f"{a} -> {b}" for a, b in ev["dangling"]),
        "bare_name": sorted(f"{a} -> {b}" for a, b in ev["bare_name"]),
    }


# ─────────────────────────── các kiểm không cần mốc ────────────────────────────

def check_evidence_paths():
    """③ Trích dẫn evidence: 0 `dangling`.

    Resolve theo NGUỒN, vì 2 tầng sổ dùng 2 quy ước khác nhau — trộn lẫn là sinh dương tính giả:
      - `coverage-<MOD>.md` → đường dẫn **ĐỦ**, gốc là `08_test-runs/vibe/` (`§13` R6)
      - `scope-ledger.md`   → **tên trần**, gốc là `screenshots/` của chính run
    Bỏ qua dạng viết tắt `…__slot.png` / `__slot.png` (cùng prefix với đường dẫn liền trước).
    """
    dead, bare, total, short, declared = [], [], 0, 0, 0

    def scan(path, resolvers):
        """Quét THEO DÒNG (không quét cả file) để đọc được nhãn đứng ngay sau tên ảnh."""
        nonlocal total, short, declared
        for line in open(path, encoding="utf-8", errors="replace"):
            flat = clean(line)
            for m in PNG_RE.finditer(flat):
                s = m.group(0)
                if s.startswith("__") or s.startswith("…"):
                    short += 1
                    continue
                # 🪤 Chỉ token theo QUY ƯỚC TÊN EVIDENCE mới là trích dẫn: có `__` (dấu tách
                # TC↔slot) hoặc nằm dưới `screenshots/`. Bản gộp toàn phần chứa cả văn xuôi
                # của `vibe-log`, trong đó có **tên fixture** (`tothinh.png`, `hoso-01.jpg`)
                # và cả chuỗi định dạng (`.jpg/.png`) ⇒ không lọc là 6/7 "dangling" dương
                # tính giả (đo 2026-09-07).
                if "__" not in s and "screenshots/" not in s:
                    continue
                # 🔑 Allowlist ĐẶT NGAY CẠNH trích dẫn. Ảnh bị hạ CÓ CHỦ ĐÍCH khi đóng gói mang
                # nhãn `[đã hạ tầng B]` ngay sau tên ⇒ dòng đó KHÔNG còn khẳng định "file tồn
                # tại", nó là một KHAI BÁO. Đặt lý do cạnh trích dẫn tốt hơn file allowlist rời:
                # người đọc sổ thấy ngay, và không thể sửa 1 bên mà quên bên kia (§13.6).
                if DECLARED_DROPPED in flat[m.end():m.end() + 24]:
                    declared += 1
                    continue
                total += 1
                if any(os.path.exists(r(s)) for r in resolvers):
                    continue
                # còn tồn tại ở chỗ khác ⇒ không phải link chết mà là TÊN TRẦN (§13 R6 cấm)
                hit = glob(os.path.join(VIBE, "**", os.path.basename(s)), recursive=True)
                (bare if hit else dead).append((os.path.relpath(path, REPO), s))

    for p in sorted(glob(os.path.join(VIBE, "coverage", "coverage-*.md"))):
        scan(p, [lambda s: os.path.join(VIBE, s)])
    for p in sorted(glob(os.path.join(VIBE, "v*", "VR-*", "scope-ledger.md"))):
        run = os.path.dirname(p)
        scan(p, [lambda s, r=run: os.path.join(r, "screenshots", os.path.basename(s)),
                 lambda s: os.path.join(VIBE, s)])
    # Vùng GỘP TOÀN PHẦN: ledger/report nằm TRONG `<zone>/VIBE-REPORT-*.md`, ảnh ở
    # `<zone>/screenshots/` phẳng ⇒ tên trần trong đó resolve theo thư mục của chính bản gộp.
    # ⛔ Không bỏ qua file này: nó chứa 15 nhãn `[đã hạ tầng B]` và toàn bộ trích dẫn của
    # 12 ledger — không quét là mất luôn phần audit đó (đo 2026-09-07: 15 → 0 nhãn).
    for p in sorted(glob(os.path.join(VIBE, "v*", "VIBE-REPORT-*.md"))):
        zone = os.path.dirname(p)
        scan(p, [lambda s, z=zone: os.path.join(z, "screenshots", os.path.basename(s)),
                 lambda s, z=zone: os.path.join(z, s),
                 lambda s: os.path.join(VIBE, s)])
    return {"total": total, "shorthand": short, "declared_dropped": declared,
            "dangling": dead, "bare_name": bare}


def check_verdict_has_evidence():
    """Thay thế `packaged_unevidenced` cho vùng GỘP TOÀN PHẦN (không còn thư mục run).

    Luật: TC nào sổ khai verdict **PASS/FAIL** *và* **có trích ảnh** thì ≥1 ảnh đó phải
    **tồn tại**. ⛔ Bỏ qua dòng **không trích ảnh nào** — đó là verdict của round **manual**
    (`coverage-PQ.md`, 29 dòng) hoặc **tier automation** (`RUN-xxx`, evidence là log `§15`);
    đòi ảnh ở đó là đỏ oan, đã thử và bị bác 2026-09-07.
    """
    bad = []
    for p in sorted(glob(os.path.join(VIBE, "coverage", "coverage-*.md"))):
        for _, cells in table_rows(open(p, encoding="utf-8").read()):
            tc = cells[0].strip("`* ")
            if not TC_CELL_RE.match(tc):
                continue
            blob = clean(" ".join(cells))
            up = cells[1].upper()
            if not any(t in up for t in ("PASS", "FAIL")):
                continue
            shots = [s for s in PNG_RE.findall(blob) if not s.startswith(("__", "…"))]
            if not shots:
                continue                                   # tier manual/automation
            if not any(os.path.exists(os.path.join(VIBE, s))
                       or glob(os.path.join(VIBE, "**", os.path.basename(s)), recursive=True)
                       for s in shots):
                bad.append((os.path.relpath(p, REPO), tc, len(shots)))
    return bad


def check_table_shape():
    """④ số ô mỗi dòng = số ô header · ⑤ ô Verdict mở đầu bằng token · ⑥ bẫy `parse_ledger`."""
    ragged, bad_verdict, bad_h1, tc_first_in_aux = [], [], [], []
    for p in sorted(glob(os.path.join(VIBE, "coverage", "coverage-*.md"))):
        rel = os.path.relpath(p, REPO)
        raw = open(p, encoding="utf-8").read()
        # ⑥a H1 phải mang `module <MÃ>` — `ledger_module` đọc ở đây
        first_h = next((l for l in raw.splitlines() if l.startswith("#")), "")
        if not re.search(r"module\s+[A-Za-z0-9_-]+", first_h, re.I):
            bad_h1.append(rel)
        # ⚠️ Một file có NHIỀU bảng với số cột khác nhau (bảng TC · bảng phiên · bảng nguồn).
        # Nhận header bằng **dòng phân cách ngay sau nó**, ⛔ không đoán theo nhãn ô đầu —
        # đoán theo nhãn làm dòng header của bảng thứ 2 bị chấm như dòng dữ liệu của bảng 1
        # (sinh 17 dương tính giả ở lượt đầu 2026-09-07).
        rows = list(table_rows(raw))
        is_sep = [bool(cs) and set("".join(cs)) <= set("-: ") for _, cs in rows]
        header = None
        for i, (line, cells) in enumerate(rows):
            if is_sep[i]:
                continue
            if i + 1 < len(rows) and is_sep[i + 1]:
                header = len(cells)                       # đây là dòng header
                continue
            if header is None:
                continue
            if len(cells) != header:
                ragged.append((rel, cells[0][:28], len(cells), header))
            tc = cells[0].strip("`* ")
            if TC_CELL_RE.match(tc):
                if not VERDICT_HEAD_RE.match(cells[1].strip("`* ")):
                    bad_verdict.append((rel, tc, cells[1][:40]))
                extra = [t for t in VERDICTS if t in cells[1].upper()]
                if len(extra) > 1:
                    bad_verdict.append((rel, tc, f"ô Verdict nhắc {len(extra)} token {extra} — "
                                                 f"§13 bẫy 2 (match bằng substring theo thứ tự)"))
            elif TC_CELL_RE.match(cells[1].strip("`* ")) if len(cells) > 1 else False:
                pass                                      # TC ID ở cột 2 = đúng khuôn bảng phụ
    return {"ragged_rows": ragged, "bad_verdict_cell": bad_verdict,
            "h1_missing_module": bad_h1, "tc_first_in_aux_table": tc_first_in_aux}


def check_shared_evidence():
    """⑩ 2 TC KHÁC NHAU dùng chung byte ảnh y hệt — vi phạm `vibe-test` D3.

    D3: *"1 ảnh không chứng minh được 2 case → **chụp lại riêng**; đổi tên **không** tạo
    bằng chứng mới"*. Nhóm md5 trùng mà mang ≥2 mã TC ⇒ verdict của những TC đó **không có
    bằng chứng riêng**.

    ⚠️ Kiểm này là **THÔNG TIN, không chặn**: nó phát hiện lỗi ở lượt CHỤP (đã xảy ra), và
    ⛔ cách chữa **không phải xoá ảnh** (xoá làm TC mất luôn bằng chứng) mà là **chụp lại**.
    """
    import hashlib
    by = defaultdict(list)
    for p in sorted(glob(os.path.join(VIBE, "v*", "screenshots", "*.png"))):
        try:
            by[hashlib.md5(open(p, "rb").read()).hexdigest()].append(os.path.basename(p))
        except OSError:
            continue
    out = []
    for names in by.values():
        if len(names) < 2:
            continue
        tcs = {m.group(1) for n in names if (m := re.match(r"(TC-[A-Z]+-\d+)__", n))}
        if len(tcs) > 1:
            out.append(sorted(names))
    return out


def check_run_pointers():
    """RUN-xxx được sổ coverage trích làm nguồn verdict nhưng KHÔNG có file nào trong `runs/`."""
    have = {m.group(0) for f in os.listdir(RUNS) if (m := re.match(r"RUN-\d+", f))} if os.path.isdir(RUNS) else set()
    cited = set()
    for p in glob(os.path.join(VIBE, "coverage", "coverage-*.md")):
        cited |= set(re.findall(r"RUN-\d+", open(p, encoding="utf-8").read()))
    return sorted(cited - have)


def audit():
    ev = check_evidence_paths()
    sh = check_table_shape()
    orphan_runs = check_run_pointers()
    print("── ③ trích dẫn evidence ────────────────────────────────────────────")
    print(f"   đầy đủ: {ev['total']} · viết tắt `…`: {ev['shorthand']}"
          f" · khai đã hạ `{DECLARED_DROPPED}`: {ev.get('declared_dropped', 0)}")
    print(f"   🔴 dangling (mất thật): {len(ev['dangling'])}")
    for f, s in ev["dangling"]:
        print(f"      {f} -> {s}")
    print(f"   ⚠️  tên trần (§13 R6 cấm — ảnh còn nhưng path không audit được): {len(ev['bare_name'])}")
    for f, s in ev["bare_name"]:
        print(f"      {f} -> {s}")
    print("── ④⑤⑥ hình dạng bảng ─────────────────────────────────────────────")
    print(f"   dòng lệch số ô: {len(sh['ragged_rows'])}   ô Verdict sai: {len(sh['bad_verdict_cell'])}"
          f"   H1 thiếu `module`: {len(sh['h1_missing_module'])}")
    for r in sh["ragged_rows"][:10]:
        print(f"      ragged {r}")
    for r in sh["bad_verdict_cell"][:10]:
        print(f"      verdict {r}")
    for r in sh["h1_missing_module"]:
        print(f"      h1 {r}")
    ve = check_verdict_has_evidence()
    print("── ③b verdict PASS/FAIL có trích ảnh thì ảnh phải tồn tại ─────────")
    print(f"   vi phạm: {len(ve)}" + (" 🔴" if ve else " ✅"))
    for r in ve[:10]:
        print(f"      {r}")
    print("── ⑨ con trỏ RUN-xxx ──────────────────────────────────────────────")
    print(f"   RUN được trích mà `runs/` không có file: {orphan_runs or '0'}")
    if orphan_runs:
        print("      ⇒ với các run này `10_source-code/MEMORY.md §15` là artifact DUY NHẤT (đã khai ở §15)")
    bad = bool(ev["dangling"] or sh["ragged_rows"] or sh["bad_verdict_cell"]
               or sh["h1_missing_module"] or ve)
    return 1 if bad else 0


def state_path():
    return os.path.join(STATE_DIR, "test-runs.base.json")


def allow_path(kind):
    return os.path.join(STATE_DIR, f"test-runs.allow-{kind}.txt")


def sig(text):
    """Khoá allowlist cho chuỗi dài/chứa markdown: `sha1:<8 hex>` của bản đã normalize."""
    return "sha1:" + hashlib.sha1(" ".join(text.split()).encode("utf-8")).hexdigest()[:8]


def read_allow_from_manifests(kind):
    """Allowlist đọc TỪ bảng `#### Miễn trừ oracle — <kind>` trong mọi SEAL-MANIFEST.md.

    🔑 Vì sao rời `.close-run/*.allow*.txt`: miễn trừ là **phán đoán của người** — nó thuộc về
    artifact mà người đọc mở, ⛔ không thuộc một dotfile `.gitignore` có thể nuốt (đã xảy ra
    thật ở tier analyze: 17 allowlist bị ignore ⇒ 13/18 đơn vị FAIL oan trên máy mới clone).
    Máy đọc **cột 1**, người đọc cả 3 cột — cùng một bảng, không thể lệch nhau.
    """
    out = set()
    for mf in sorted(glob(os.path.join(REPO, "08_test-runs", "*", "v*", "SEAL-MANIFEST.md"))):
        txt = open(mf, encoding="utf-8").read()
        m = re.search(r'^#{3,4} *Miễn trừ oracle *— *' + re.escape(kind) + r'[^\n]*\n(.*?)(?=^#{1,4} |\Z)',
                      txt, re.M | re.S)
        if not m:
            continue
        for line, cells in table_rows(m.group(1)):
            key = cells[0].strip().strip('`*').strip()
            if not key or key.lower() in ("miễn trừ", "khoá") or set(key) <= set(':- '):
                continue
            if len(cells) < 2 or not cells[1].strip():      # ⛔ không lý do = không miễn trừ
                continue
            out.add(key)
    return out


def read_allow_legacy(kind):
    """Đọc allowlist. Mỗi dòng: `<khoá>  # <lý do do NGƯỜI viết>`.

    Khoá là **chuỗi literal** (cho ID ngắn) hoặc **`sha1:<8 hex>`** (cho câu dài).
    🪤 Vì sao cần dạng hash: `line.split("#")[0]` cắt mất mọi thứ sau `#` — mà câu `⛔`
    có thể **mở đầu bằng `###`** (heading markdown) ⇒ khoá literal thành chuỗi rỗng và
    allowlist im lặng không có tác dụng. Đã mắc đúng lỗi này 2026-09-07.
    """
    p = allow_path(kind)
    if not os.path.isfile(p):
        return set()
    out = set()
    for line in open(p, encoding="utf-8"):
        if line.lstrip().startswith("#"):
            continue
        key = line.split("  #")[0].strip()
        if key:
            out.add(key)
    return out


def do_baseline():
    os.makedirs(STATE_DIR, exist_ok=True)
    if os.path.isfile(state_path()):
        print(f"✗ đã có mốc {os.path.relpath(state_path(), REPO)} — ⛔ KHÔNG chụp lại.\n"
              f"  Mốc phải lấy từ working tree SẠCH, chụp lại sau khi đã sửa là tự xoá bằng chứng.",
              file=sys.stderr)
        return 2
    s = snap()
    json.dump(s, open(state_path(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"✓ mốc: {os.path.relpath(state_path(), REPO)}")
    print(f"  {len(s['ids'])} định danh · {len(s['verdicts'])} verdict per-TC · "
          f"{len(s['stops'])} câu ⛔ · {len(s['inq'])} trích nguyên văn inline · {len(s['files'])} file")
    return 0


def find_pack_base():
    """`PACK_BASE: <sha>` khai trong SEAL-MANIFEST của vùng. Mốc = một COMMIT, ⛔ không phải file."""
    seen = {}
    for mf in sorted(glob(os.path.join(REPO, "08_test-runs", "*", "v*", "SEAL-MANIFEST.md"))):
        m = re.search(r'^[>\s|*`]*PACK_BASE[`*\s]*:[\s`*]*([0-9a-f]{7,40})',
                      open(mf, encoding="utf-8").read(), re.M)
        if m:
            seen.setdefault(m.group(1), []).append(os.path.relpath(mf, REPO))
    if not seen:
        return None
    if len(seen) > 1:
        print(f"⚠️  nhiều PACK_BASE khác nhau: { {k: v[:1] for k, v in seen.items()} } — dùng cái đầu",
              file=sys.stderr)
    return sorted(seen)[0]


def do_check(ref=None):
    ref = ref or find_pack_base()
    if not ref:
        print("✗ không biết mốc. Thêm dòng `PACK_BASE: <sha>` vào SEAL-MANIFEST.md của vùng,\n"
              "  hoặc truyền --since <ref>. 🔑 Mốc là commit NGAY TRƯỚC lượt đóng gói —\n"
              "  ⛔ đừng lấy HEAD, tree đã đóng gói rồi thì oracle thành no-op.", file=sys.stderr)
        return 2
    base = snap(ref=ref)
    now = snap()
    allow_id = read_allow_from_manifests("id") | read_allow_legacy("id")
    allow_stop = read_allow_from_manifests("stop") | read_allow_legacy("stop")
    fail = 0

    lost = sorted(set(base["ids"]) - set(now["ids"]) - allow_id)
    print(f"① định danh mất: {len(lost)}" + (f" 🔴 {lost}" if lost else " ✅"))
    fail |= bool(lost)

    # Allowlist ② dạng `<sổ>::<TC>` hoặc `<sổ>::<TC>:<cũ>-><mới>`. Verdict đổi vì **quyết định
    # nghiệp vụ** (vd hoà giải 2 tier) là **thay đổi trạng thái có thẩm quyền**, không phải mất
    # căn cứ ⇒ cho allowlist thay vì `--baseline` lại. ⛔ Re-baseline là tự xoá bằng chứng: nó
    # làm MỌI lệch biến mất, kể cả lệch do sơ suất.
    allow_v = read_allow_from_manifests("verdict") | read_allow_legacy("verdict")
    drift, allowed = [], 0
    for k in base["verdicts"]:
        nv = now["verdicts"].get(k, "—MẤT DÒNG—")
        if nv == base["verdicts"][k]:
            continue
        if k in allow_v or f"{k}:{base['verdicts'][k]}->{nv}" in allow_v:
            allowed += 1
            continue
        drift.append((k, base["verdicts"][k], nv))
    print(f"② verdict per-TC lệch: {len(drift)}" + (" 🔴" if drift else " ✅")
          + (f"   ({allowed} đã allowlist kèm lý do)" if allowed else ""))
    for d in drift[:20]:
        print(f"      {d[0]}: {d[1]} -> {d[2]}")
    fail |= bool(drift)

    lost_stop = sorted(s0 for s0 in set(base["stops"]) - set(now["stops"])
                       if s0 not in allow_stop and sig(s0) not in allow_stop)
    print(f"⑧ câu ⛔ mất: {len(lost_stop)}" + (" 🔴" if lost_stop else " ✅"))
    for s in lost_stop[:20]:
        print(f"      {sig(s)}  {s[:130]}")
    fail |= bool(lost_stop)

    allow_inq = read_allow_from_manifests("inq") | read_allow_legacy("inq")
    lost_inq = sorted(s0 for s0 in set(base["inq"]) - set(now["inq"])
                      if s0 not in allow_inq and sig(s0) not in allow_inq)
    print(f"⑦ trích nguyên văn inline mất: {len(lost_inq)}" + (" 🔴" if lost_inq else " ✅"))
    for s in lost_inq[:20]:
        print(f"      {sig(s)}  {s[:130]}")
    fail |= bool(lost_inq)

    new_dang = sorted(set(now.get("dangling", [])) - set(base.get("dangling", [])))
    old_dang = sorted(set(base.get("dangling", [])) - set(now.get("dangling", [])))
    print(f"③ dangling MỚI: {len(new_dang)}" + (" 🔴" if new_dang else " ✅")
          + (f"   (đã xử lý được {len(old_dang)} cái cũ 🎉)" if old_dang else ""))
    for s in new_dang:
        print(f"      {s}")
    fail |= bool(new_dang)
    carried = len(set(now.get("dangling", [])) & set(base.get("dangling", [])))
    if carried:
        print(f"   ⚠️  {carried} dangling CÓ SẴN từ mốc — không chặn lượt này, nhưng vẫn là nợ:"
              f" ⛔ chặn việc khai `SEAL_STATE: PACKAGED` (§13.6 giữ `dangling` tử hình).")

    new_bare = sorted(set(now.get("bare_name", [])) - set(base.get("bare_name", [])))
    print(f"   tên trần MỚI (§13 R6): {len(new_bare)}" + (" 🔴" if new_bare else " ✅"))
    for s in new_bare:
        print(f"      {s}")
    fail |= bool(new_bare)

    b, n = sum(base["files"].values()), sum(now["files"].values())
    print(f"   bytes: {b:,} -> {n:,} ({(n - b) / b * 100:+.1f}%)  "
          f"file: {len(base['files'])} -> {len(now['files'])}")
    print("── hình dạng bảng (không cần mốc) ──────────────────────────────────")
    sh = check_table_shape()
    print(f"④ dòng lệch số ô: {len(sh['ragged_rows'])}" + (" 🔴" if sh["ragged_rows"] else " ✅"))
    for r in sh["ragged_rows"][:10]:
        print(f"      {r}")
    print(f"⑤ ô Verdict sai: {len(sh['bad_verdict_cell'])}" + (" 🔴" if sh["bad_verdict_cell"] else " ✅"))
    for r in sh["bad_verdict_cell"][:10]:
        print(f"      {r}")
    print(f"⑥ H1 thiếu `module`: {len(sh['h1_missing_module'])}" + (" 🔴" if sh["h1_missing_module"] else " ✅"))
    for r in sh["h1_missing_module"]:
        print(f"      {r}")
    fail |= bool(sh["ragged_rows"] or sh["bad_verdict_cell"] or sh["h1_missing_module"])
    vev = check_verdict_has_evidence()
    print(f"③b verdict PASS/FAIL trích ảnh mà ảnh không tồn tại: {len(vev)}"
          + (" 🔴" if vev else " ✅"))
    for r in vev[:10]:
        print(f"      {r}")
    fail |= bool(vev)
    shared = check_shared_evidence()
    print(f"⑩ 2 TC khác nhau dùng chung byte ảnh (`vibe-test` D3): {len(shared)} nhóm"
          + (" ⚠️ THÔNG TIN, không chặn" if shared else " ✅"))
    for g in shared[:12]:
        print("      " + " ⇄ ".join(g))
    if shared:
        print("      ⛔ Cách chữa KHÔNG phải xoá ảnh (xoá là TC mất luôn bằng chứng) mà là CHỤP LẠI.")
    mc = check_manifest_counts()
    print(f"⑫ số ảnh manifest tự khai lệch cây file: {len(mc)}" + (" 🔴" if mc else " ✅"))
    for r in mc:
        print(f"      {r}")
    fail |= bool(mc)
    orphan = check_run_pointers()
    print(f"⑨ RUN-xxx được trích mà `runs/` không có file: {orphan or '0 ✅'}")
    if orphan:
        print("      ⇒ với các run này `10_source-code/MEMORY.md §15` là artifact DUY NHẤT (đã khai ở §15)"
              " — thông tin, không chặn.")
    print()
    if fail:
        print("❌ ORACLE FAIL — ⛔ không đi tiếp. `git checkout` đúng phạm vi vừa sửa.")
        print("   Định danh/câu ⛔ bỏ có chủ đích thì phải có 1 dòng lý do do NGƯỜI viết ở "
              f"{os.path.relpath(allow_path('id'), REPO)} / {os.path.relpath(allow_path('stop'), REPO)}")
        return 1
    print("✅ ORACLE PASS — không mất căn cứ máy đo được.")
    print("⚠️  Oracle KHÔNG gác việc thay phát biểu A bằng B ⇒ vẫn phải ĐỌC DIFF trước khi commit.")
    return 0



def check_manifest_counts():
    """⑫ Số ảnh mà SEAL-MANIFEST tự khai phải khớp cây file nó niêm phong.

    Vì sao cần: manifest sprint-6 từng khai `GIỮ: 306/314 ảnh` trong khi vùng chỉ còn **236** —
    viết trước một tầng xoá rồi không đồng bộ lại. Manifest khai sai số là **bằng chứng sai**,
    không phải lỗi chính tả: nó là thứ người sau đọc để tin vùng còn nguyên.
    ⛔ Chỉ đối chiếu con số đứng ngay cạnh chữ "ảnh" — không đoán mọi số trong file.
    🪤 **Bỏ qua nội dung trong trích dẫn `*"…"*`.** Luật đóng gói BẮT BUỘC chép nguyên văn câu đã bị
       thay thế ("Bản trước ghi *\"GIỮ: 306/314 ảnh\"* — sai"), nên quét cả file sẽ bắt chính câu
       đính chính và báo đỏ vĩnh viễn. Cùng loại bẫy với `PACKAGED_RE` quét cả file thay vì neo dòng.
    """
    bad = []
    pat = re.compile(r'(?:GIỮ|GIU)\s*:?\s*\*{0,2}(\d+)\s*(?:/\s*(\d+)\s*)?ảnh', re.I)
    for mf in sorted(glob(os.path.join(REPO, "08_test-runs", "*", "v*", "SEAL-MANIFEST.md"))):
        zone = os.path.dirname(mf)
        real = sum(1 for r, _d, fs in os.walk(zone) for f in fs if f.lower().endswith(".png"))
        txt = re.sub(r'\*"[^"]*"\*', '', open(mf, encoding="utf-8").read())   # gỡ trích dẫn nguyên văn
        for m in pat.finditer(txt):
            claimed = int(m.group(1))
            if claimed != real:
                bad.append(f"{os.path.relpath(mf, REPO)}: khai {claimed} ảnh, cây file có {real}")
    return bad

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="đối chiếu với mốc + chạy mọi kiểm")
    g.add_argument("--audit", action="store_true", help="chỉ các kiểm không cần mốc")
    ap.add_argument("--since", help="git ref của mốc; để trống ⇒ đọc `PACK_BASE:` trong SEAL-MANIFEST")
    a = ap.parse_args()
    if a.audit:
        return audit()
    return do_check(a.since)


if __name__ == "__main__":
    sys.exit(main())
