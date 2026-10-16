#!/usr/bin/env python3
"""PostToolUse guard cho memory layer — chan history creep.

VAN DE NO CHUA: file "trang thai hien hanh" (MEMORY / router / leaf / registry)
bi dung lam noi ghi LICH SU, roi phinh toi muc khong doc duoc nhu trang thai.
Trieu chung da gap that: mot thu muc analyze nang vai MB, mot luot generate-tc
nap hang tram nghin token, mot O BANG nang >80 KB.

Hook nay la LOP CUNG cua policy `Project_rule.md §Memory / Write-back Policy` (policy noi luat,
hook cuong che). Ca hai deu can: policy mot minh thi bi quen, hook mot minh thi
khong ai hieu vi sao bi chan.

⚠️ KHONG dung chung HARD_PATTERNS cua guard cho CLAUDE.md / cot Notes. Trong
memory file thi `VR-021` la BANG CHUNG cua mot clarification, `RISK-xxx`/`CL-xxx`
la KHOA TRACE, ngay thang la DIEU KIEN AP DUNG. Tai dung nguyen xi se
false-positive hang tram dong HOP LE va hook se bi tat sau vai lan — luc do khong
con lop cung nao. Chi bat mau LUON mang nghia "so da chet".

Chi soi cac dong nam trong diff (`git diff HEAD -U0`) — khong quet toan file, nen
file chua don khong bi chan lai moi lan ai do sua MOT dong khac.

🔑 Co che "chi chan khi lam xau di": vuot tran ma file DANG THU NHO so `HEAD` ⇒
WARN ("dang don, tot"), khong chan. Nho vay hook khong chan chinh luot don.

🔒 PHEP THU NGUOC KHI HIEU CHUAN: tran nao lam file HIEN CO do OAN la tran SAI —
NOI TRAN, dung sua file. Tran sinh ra de chan LICH SU tich tu, khong phai de ep
noi dung that phai nho lai.

────────────────────────────────────────────────────────────────────────────────
HIEU CHUAN CHO PROJECT CUA BAN — doc truoc khi dung
────────────────────────────────────────────────────────────────────────────────
Moi tran duoi day la GIA TRI KHOI DIEM, khong phai hang so vu tru. Cach dat:

  1. Do hien trang:  find <folder> -name '*.md' | xargs ls -l | sort -k5 -n
  2. Bo qua file da biet la phinh vi lich su (chung se duoc don).
  3. Lay nhom LANH (file chi chua noi dung that) lam goc, nhan ~1,4–1,7.
  4. Chay thu: khong file lanh nao do. Co ⇒ noi tran (xem PHEP THU NGUOC).

Phan "tru ra" (strip_writeback / strip_detail) cung phai khai theo project: do la
cac section CO CHU Y lon dan (dich write-back). Do ca chung vao tran = ep nguoi ta
cat dung cho dang luu lich su hop le.
"""

import json
import os
import re
import subprocess
import sys

# ── TRAN (bytes) — hieu chuan theo project, xem docstring ────────────────────
CELL_WARN_BYTES = 2 * 1024
CELL_FAIL_BYTES = 4 * 1024

TIER1_LIMIT = 60 * 1024   # MASTER-MEMORY.md
TIER2_LIMIT = 90 * 1024   # router per-version. ⚠️ DO PHAN NGOAI cac section la
                          # DICH WRITE-BACK (changelog / TC-gen-log / scenario index)
                          # — xem strip_writeback(). Khong tru ra thi tran nay chan
                          # nham chinh cho duoc phep lon dan.
TIER3_LIMIT = 250 * 1024  # leaf per-module
TIER3_BIG_LIMIT = 450 * 1024   # 🔓 leaf cua module RAT LON (nhieu SC): lon vi NOI
                               # DUNG THAT (~2 KB/SC), khong vi lich su. Dat 0 de tat
                               # ngoai le nay neu project khong co module nao nhu vay.
SC_BIG_THRESHOLD = 150         # so SC de mot leaf duoc huong TIER3_BIG_LIMIT
TIER4_LIMIT = 16 * 1024   # WORKING-STATE.md — trang thai tac nghiep (prose).
                          # KHONG co phan lon dan chinh dang: no dong lai thi file
                          # PHAI co lai. Tran chat hon cac tier khac la co y.

TIER5_LIMIT = 130 * 1024  # 10_source-code/MEMORY.md — context automation.
                          # ⚠️ File nay RAT de bi bo sot khoi moi tier (no khong nam
                          # trong thu muc analyze) va khi bi sot thi KHONG CO TRAN NAO
                          # — da co tien le phinh len hang tram KB, ~88% la lich su.
                          # ⚠️ Vuot tran KHONG co nghia cat registry: kiem xem execution
                          # log co bi append tro lai vao file nay khong.
TIER6_LIMIT = 200 * 1024  # 08_test-runs/runs/FAIL-REGISTRY.md — bang GHI DE.
                          # DO PHAN NGOAI `## Chi tiet` (muc do la DICH WRITE-BACK,
                          # lon dan CHINH DANG) — xem strip_detail().
                          # ⇒ Tran nay chi chan khi BANG TRANG THAI bi APPEND them dong
                          # cho cung mot FAIL ID — dung cai luat "ghi de" muon chan.
                          # ⛔ KHONG dat tran cho IMPLEMENTATION-HISTORY / EXECUTION-
                          # ARCHIVE / RUN-*.md: dich lich su thuan, khong nap vao
                          # context, file RUN bat bien.

# Thu muc version duoi 02_analyze-requirements/ — sua cho khop convention project.
VERSION_DIR_RE = re.compile(r"^v[\d.]+(-sprint-\d+)?$")

HIST_LABELS_BLOCK = 3  # >=3 nhãn lịch sử thêm mới trong 1 lượt => blocker

LEAF_BASENAMES = {
    "memory.md",
    "changelog.md",   # layout module-first 2026-09-01: thay module MEMORY.md
    "requirement_traceability.md",
    "test_scenario_map.md",
    "test_data_catalog.md",
    "risk_assessment.md",
    "coverage-gap-report.md",
}

# Dòng ĐANG PHÁT BIỂU LUẬT (trích chính mẫu bị cấm làm ví dụ) — miễn trừ CHECK 3.
# Nếu không có, chính banner `⛔ Không nối khối (trước đó:) / (lịch sử)` sẽ tự
# kích hoạt hook, và cảnh báo báo oan là cách nhanh nhất để hook bị tắt.
RULE_CITATION = re.compile(
    r"Project_rule|§10\.5|CONSOLIDATE không APPEND|không phải changelog"
    r"|đích lịch sử|memory-guard", re.IGNORECASE)

# Mẫu LUÔN mang nghĩa "số/kết luận đã chết" — neo ^ mượn khuôn HIST của
# tc-notes-guard để không bắt nhầm nhãn nằm GIỮA câu (điều kiện áp dụng thật).
HIST_PATTERNS = [
    (r"\((?:số cũ|bản trước|mốc cũ|lịch sử|bản lượt \d)",
     "khối `(số cũ:/trước đó:/lịch sử)` — sửa TẠI CHỖ, đừng nối bản cũ (§Memory / Write-back Policy)"),
    (r"hết hiệu lực|đã bị thay thế|đừng trích lại|SUPERSEDED",
     "nhãn số liệu đã bị thay thế — xoá hẳn, đừng giữ lại để đối chiếu (§Memory / Write-back Policy)"),
    (r"~~.+~~",
     "gạch ngang = nội dung đã chết ⚠️ TRỪ khi cả ô là căn cứ còn hiệu lực (§Memory / Write-back Policy)"),
    (r"\d+\s*(?:→|->)\s*\d+",
     "biến động số cũ→số mới — chỉ giữ số hiện hành (§Memory / Write-back Policy)"),
]

# CHECK 4 — số đếm ngoài nguồn canonical (§Memory / Write-back Policy). Chỉ WARN: regex chắc chắn có
# false-positive (dải ID, tham chiếu chéo), nên không được phép chặn.
COUNT_PATTERN = re.compile(r"(REQ|SC|CL|RISK|TC)\D{0,12}\d{2,3}")


def repo_root_for(path):
    try:
        out = subprocess.run(
            ["git", "-C", os.path.dirname(path) or ".", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
        )
    except Exception:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def diff_added_lines(root, fp):
    """Dòng '+' của file so với HEAD (gồm cả thay đổi đã stage) — chỉ soi phần vừa đổi."""
    try:
        out = subprocess.run(
            ["git", "-C", root, "diff", "HEAD", "-U0", "--", fp],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
        )
    except Exception:
        return []
    if out.returncode != 0 or not out.stdout:
        return []
    return [ln[1:] for ln in out.stdout.splitlines()
            if ln.startswith("+") and not ln.startswith("+++")]


def head_blob(root, relpath):
    """Nội dung file ở HEAD (None nếu file mới)."""
    try:
        out = subprocess.run(
            ["git", "-C", root, "show", "HEAD:" + relpath],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
        )
    except Exception:
        return None
    return out.stdout if out.returncode == 0 else None


def classify_tier(relpath):
    """TIER1/TIER2/TIER3 hoặc None. Phân biệt TIER2 ⇄ TIER3 bằng ĐỘ SÂU PATH —
    cả hai đều tên `MEMORY.md`, đây là chỗ dễ sai nhất."""
    norm = relpath.replace(os.sep, "/")
    parts = norm.split("/")
    base = parts[-1].lower()

    # TIER5: 10_source-code/MEMORY.md — context automation (structure/stack/registry).
    # TIER6: 08_test-runs/runs/FAIL-REGISTRY.md — registry FAIL, bảng GHI ĐÈ.
    # Cả hai nằm NGOÀI 02_analyze-requirements ⇒ phải quyết TRƯỚC guard dưới,
    # nếu không sẽ rơi vào `return None` như trước 2026-09-01 (= không có trần).
    if base == "memory.md" and "10_source-code" in parts:
        return "TIER5"
    if base == "fail-registry.md" and "runs" in parts:
        return "TIER6"

    if "02_analyze-requirements" not in parts:
        return None
    i = parts.index("02_analyze-requirements")
    rest = parts[i + 1:]

    # TIER1: 02_analyze-requirements/MASTER-MEMORY.md
    if base == "master-memory.md":
        return "TIER1"

    # TIER4: 02_analyze-requirements/WORKING-STATE.md — ràng buộc execute + nợ mở
    # + quyết định cấu trúc, tách khỏi CLAUDE.md 2026-08-25 (file đó nạp mọi phiên).
    # Cùng luật §Memory / Write-back Policy nhưng KHÁC vai 3 tier kia: prose chứ không phải bảng SC/quote.
    if base == "working-state.md" and len(rest) == 1:
        return "TIER4"

    # Thu muc version — chap nhan CA HAI convention:
    #   `v1.0/`              (khong tach sprint)
    #   `v1.0-sprint-6/`     (mot tang, co token sprint)
    # ⚠️ Sua regex nay cho khop convention THAT cua project. Khong khop ⇒ ham tra
    # None ⇒ file KHONG CO TRAN NAO va hook im lang vo dung — da co tien le.
    if len(rest) < 2 or not VERSION_DIR_RE.match(rest[0]):
        return None

    # TIER2: v*-sprint-*/MEMORY.md  (parent = thư mục sprint ⇒ đúng 2 phần)
    # `VERSION_MEMORY.md` la TEN CUA CHINH ROUTER DO sau khi `/package-version --tier analyze`
    # doi hinh dang. Cung vai, cung tang, cung tran ⇒ phai khop o day. Bo sot no thi ham tra
    # None ⇒ router da dong goi KHONG CO TRAN NAO va hook im lang vo dung (dung canh bao o
    # comment tren), trong khi `package-version/references/packaged-layout.md` lai khai la
    # "memory-guard da nhan VERSION_MEMORY.md la TIER2".
    if len(rest) == 2 and base in ("memory.md", "version_memory.md"):
        return "TIER2"

    # TIER3: v*-sprint-*/<module>/<leaf>.md  (đúng 3 phần)
    if len(rest) == 3 and base in LEAF_BASENAMES:
        return "TIER3"

    return None


def strip_writeback(text):
    """Bỏ các section là ĐÍCH WRITE-BACK khỏi router trước khi so trần.

    Ba section lớn dần CHÍNH ĐÁNG mỗi lượt ghi, không phải "phình":
      · `§4  Scenario Index` — generate-tc/vibe-test ghi cột TC/Vibe Status (`§12.1`)
      · `§0.1 Changelog`     — đích lịch sử từng lượt UPDATE của analyze (`§Memory / Write-back Policy`)
      · `§9  TC Generation Log` — đích write-back của generate-tc (`§Memory / Write-back Policy`)
    Không trừ thì hook chặn đúng lượt write-back hợp lệ và sẽ bị tắt sau vài lần.
    Đo 2026-08-28: trừ đủ 3 section ⇒ nhóm lành S1/2/3/5 còn 47–65 KB (trần 80 vẫn
    tách đúng), S6 100→82 KB · S7 109→84 KB.
    """
    out = []
    skip_h2 = False   # đang trong §4 / §9 — kết thúc ở `##` kế tiếp
    skip_h3 = False   # đang trong §0.1 — kết thúc ở `###` hoặc `##` kế tiếp
    for ln in text.splitlines(keepends=True):
        m2 = re.match(r"^##\s+(?:§)?(\d+)\.", ln)
        m3 = re.match(r"^###\s+(?:§)?([\d.]+)\.", ln)
        if m2:
            skip_h2 = m2.group(1) in ("4", "9")
            skip_h3 = False
        elif m3 and not skip_h2:
            skip_h3 = (m3.group(1) == "0.1")
        if not (skip_h2 or skip_h3):
            out.append(ln)
    return "".join(out)


def strip_detail(text):
    """TIER6: bỏ mục `## Chi tiết` của FAIL-REGISTRY.md trước khi so trần.

    Mục đó là ĐÍCH WRITE-BACK — chứa Error/Root-cause/Fix NGUYÊN VĂN của từng
    `FAIL-xxx`, lớn dần chính đáng mỗi lượt recheck. Cùng lý lẽ với `strip_writeback`
    ở TIER2: không trừ thì hook chặn đúng lượt ghi hợp lệ và sẽ bị tắt sau vài lần.
    Cái CẦN chặn là BẢNG trạng thái phình vì append thêm dòng cho cùng 1 FAIL ID.
    """
    out = []
    skip = False
    for ln in text.splitlines(keepends=True):
        if re.match(r"^##\s+", ln):
            skip = ln.strip().lower().startswith("## chi ti")
        if not skip:
            out.append(ln)
    return "".join(out)


def leaf_limit(root, relpath):
    """Trần TIER3: 450 KB nếu module có >150 SC, ngược lại 250 KB.

    Đếm SC ở NGUỒN CANONICAL `<module>/test_scenario_map.md` (`Project_rule §Memory / Write-back Policy`),
    không ước theo dung lượng. Thiếu file ⇒ trần mặc định.
    """
    smap = os.path.join(root, os.path.dirname(relpath), "test_scenario_map.md")
    try:
        with open(smap, encoding="utf-8") as fh:
            n = sum(1 for ln in fh if re.match(r"^\| ?\*{0,2}SC-", ln))
    except OSError:
        return TIER3_LIMIT, None
    return (TIER3_BIG_LIMIT if n > SC_BIG_THRESHOLD else TIER3_LIMIT), n


def oversized_cells(text):
    """[(lineno, field_idx, nbytes)] cho mọi ô bảng vượt trần WARN."""
    hits = []
    for n, ln in enumerate(text.splitlines(), 1):
        if not ln.startswith("|"):
            continue
        for i, cell in enumerate(ln.split("|")):
            nb = len(cell.encode("utf-8"))
            if nb > CELL_WARN_BYTES:
                hits.append((n, i, nb))
    return hits


def main():
    # Thông báo có tiếng Việt — stderr trên Windows mặc định cp1252 sẽ vỡ.
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    fp = ((payload.get("tool_input") or {}).get("file_path")
          or (payload.get("tool_response") or {}).get("filePath") or "")
    if not fp:
        return 0
    fp = os.path.abspath(fp)

    root = repo_root_for(fp)
    if not root:
        return 0
    try:
        relpath = os.path.relpath(fp, root)
    except ValueError:
        return 0

    tier = classify_tier(relpath)
    if tier is None:
        return 0

    try:
        with open(fp, "r", encoding="utf-8", newline="") as f:
            text = f.read()
    except OSError:
        return 0

    added = diff_added_lines(root, relpath)
    added_set = {ln.rstrip("\n") for ln in added}

    blockers, warnings = [], []

    # ── CHECK 1 — độ dài ô bảng (gate chính) ───────────────────────────────────
    # Ô >4 KB VÀ nằm trong dòng vừa đổi ⇒ blocker. Đã vượt từ trước mà không
    # phình thêm ⇒ warning (file chưa dọn, Plan B).
    cells = oversized_cells(text)
    if cells:
        by_line = {}
        for n, i, nb in cells:
            by_line.setdefault(n, []).append((i, nb))
        file_lines = text.splitlines()
        fail_touched, fail_stale, warn_cells = [], [], []
        for n, items in sorted(by_line.items()):
            line_text = file_lines[n - 1] if n - 1 < len(file_lines) else ""
            touched = line_text in added_set
            for i, nb in items:
                if nb > CELL_FAIL_BYTES:
                    (fail_touched if touched else fail_stale).append((n, i, nb))
                else:
                    warn_cells.append((n, i, nb))
        if fail_touched:
            blockers.append(
                f"CHECK 1 (gate chính) — {len(fail_touched)} ô bảng vượt trần FAIL "
                f"{CELL_FAIL_BYTES}B TRÊN DÒNG VỪA ĐỔI. Ô bảng là nơi lịch sử tích tụ "
                "im lặng nhất (IDE Find bỏ sót dòng dài, git diff không đọc được) — "
                "rút về đúng 4 thành phần: ngày · trạng thái · số liệu hiện hành · "
                "1 link đích lịch sử (`Project_rule.md §Memory / Write-back Policy`):")
            for n, i, nb in fail_touched[:6]:
                blockers.append(f"  · dòng {n} ô {i}: {nb}B")
        if fail_stale:
            warnings.append(
                f"CHECK 1 — {len(fail_stale)} ô >{CELL_FAIL_BYTES}B đã vượt TỪ TRƯỚC "
                "(không phình thêm ở lượt này) ⇒ nợ Plan B, không chặn.")
        if warn_cells:
            warnings.append(
                f"CHECK 1 — {len(warn_cells)} ô vượt trần WARN {CELL_WARN_BYTES}B.")

    # ── CHECK 2 — kích thước file so HEAD ("chỉ chặn khi làm xấu đi") ──────────
    if tier == "TIER3":
        limit, sc_n = leaf_limit(root, relpath)
        note4 = f" (module {sc_n} SC ⇒ trần 450 KB)" if limit == TIER3_BIG_LIMIT else ""
    else:
        limit = {"TIER1": TIER1_LIMIT, "TIER2": TIER2_LIMIT,
                 "TIER4": TIER4_LIMIT, "TIER5": TIER5_LIMIT,
                 "TIER6": TIER6_LIMIT}[tier]
        note4 = ""
        if tier == "TIER2":
            note4 = " (đã trừ §4 · §0.1 · §9 — đích write-back)"
        elif tier == "TIER6":
            note4 = " (đã trừ `## Chi tiết` — đích write-back)"
    if tier == "TIER2":
        measured = strip_writeback(text)
    elif tier == "TIER6":
        measured = strip_detail(text)
    else:
        measured = text
    size = len(measured.encode("utf-8"))

    if size > limit:
        head = head_blob(root, relpath)
        if head is None:
            head_size = None
        else:
            if tier == "TIER2":
                head_measured = strip_writeback(head)
            elif tier == "TIER6":
                head_measured = strip_detail(head)
            else:
                head_measured = head
            head_size = len(head_measured.encode("utf-8"))
        if head_size is not None and size < head_size:
            warnings.append(
                f"CHECK 2 — {tier} {size / 1024:.0f} KB{note4} > trần "
                f"{limit / 1024:.0f} KB, nhưng ĐANG THU NHỎ so HEAD "
                f"({head_size / 1024:.0f} KB) ⇒ đang dọn, tốt. Không chặn.")
        elif head_size is not None and size == head_size:
            warnings.append(
                f"CHECK 2 — {tier} {size / 1024:.0f} KB{note4} > trần "
                f"{limit / 1024:.0f} KB (không đổi so HEAD) ⇒ nợ dọn Plan B, "
                "lượt sửa này không làm xấu đi. Không chặn.")
        else:
            head_txt = (f"HEAD {head_size / 1024:.0f} KB"
                        if head_size is not None else "file mới")
            blockers.append(
                f"CHECK 2 — {tier} {size / 1024:.0f} KB{note4} > trần "
                f"{limit / 1024:.0f} KB VÀ lớn hơn {head_txt} ⇒ lượt sửa này làm "
                "PHÌNH THÊM. " + (
                    "Nợ đóng lại thì file PHẢI co — kiểm mục nào đã xong mà chưa xoá."
                    if tier == "TIER4" else
                    "§15/§16/§13 có đang bị append trở lại? Đích đúng là `08_test-runs/runs/` "
                    "(`Project_rule.md §Memory / Write-back Policy`). ⛔ Đừng cắt §6/§7/§9 — "
                    "3 registry đó là TRẠNG THÁI, lứn theo số spec/TC thật."
                    if tier == "TIER5" else
                    "Bảng trạng thái phình = có dòng append cho cùng 1 `FAIL ID`. "
                    "Luật là GHI ĐÈ: sửa dòng cũ, đẩy diễn biến xuống `## Chi tiết`."
                    if tier == "TIER6" else
                    "Mốc thực đo: router đúng vai ≈ 60–69 KB ngoài §4 "
                    "(`Project_rule.md §Memory / Write-back Policy②`)."))

    # ── CHECK 3 — nhãn lịch sử THÊM MỚI (chỉ soi dòng trong diff) ─────────────
    # 77% dòng có marker lịch sử lại chứa tín hiệu căn cứ SỐNG ⇒ quét toàn file sẽ
    # đỏ ~250 dòng hợp lệ. Chỉ soi dòng thêm mới.
    hist_hits = []
    for line in added:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if RULE_CITATION.search(stripped):
            continue  # dòng đang phát biểu luật, không phải dòng lịch sử
        for pat, why in HIST_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                hist_hits.append((why, stripped[:110]))
                break
    if hist_hits:
        head = (f"CHECK 3 — {len(hist_hits)} nhãn lịch sử THÊM MỚI ở lượt này "
                "(CONSOLIDATE không APPEND — `Project_rule.md §Memory / Write-back Policy`):")
        bucket = blockers if len(hist_hits) >= HIST_LABELS_BLOCK else warnings
        bucket.append(head)
        for why, sample in hist_hits[:6]:
            bucket.append(f"  · {why}\n    → {sample}")
        if len(hist_hits) > 6:
            bucket.append(f"  · … và {len(hist_hits) - 6} dòng nữa")

    # ── CHECK 4 — số đếm ngoài nguồn canonical (WARN only) ────────────────────
    if tier in ("TIER1", "TIER2"):
        count_hits = [ln.strip()[:110] for ln in added
                      if ln.strip() and not ln.strip().startswith("#")
                      and COUNT_PATTERN.search(ln)]
        if count_hits:
            warnings.append(
                f"CHECK 4 — {len(count_hits)} dòng mới ở {tier} có dạng số đếm "
                "REQ/SC/CL/RISK/TC. Tầng này KHÔNG ghi số, chỉ `→ xem <path>` — nguồn "
                "canonical ở `Project_rule.md §Memory / Write-back Policy`. ⚠️ Check này hay báo oan (dải "
                "ID, tham chiếu chéo) ⇒ chỉ nhắc, không chặn.")
            for sample in count_hits[:3]:
                warnings.append(f"  · {sample}")

    if not blockers and not warnings:
        return 0

    msg = ["[memory-guard] MEMORY.md = TRẠNG THÁI hiện hành, không phải changelog "
           f"(`Project_rule.md §Memory / Write-back Policy`). File: {relpath} [{tier}]"]
    if blockers:
        msg.append("")
        msg.extend(blockers)
    if warnings:
        msg.append("")
        msg.extend(warnings)
    msg.append("")
    msg.append(
        "Tự kiểm trước khi giữ nguyên:\n"
        "  1. Nội dung này có đích write-back chính thức không? (`§Memory / Write-back Policy`) → ghi ở "
        "đó rồi xoá khỏi đây. ⛔ KHÔNG tạo file lịch sử mới.\n"
        "  2. Là trạng thái đang đúng hay việc đã xảy ra? → việc đã xảy ra thì bỏ.\n"
        "  3. Xoá dòng này thì lượt analyze/generate/execute sau có làm SAI không "
        "(mất căn cứ `CL-xxx`, mất cảnh báo `⛔`, mất đường `BLOCKED`)? Có rủi ro "
        "thì GIỮ — 77% dòng mang marker lịch sử vẫn chứa căn cứ sống (`§Memory / Write-back Policy`).\n"
        "Nếu đã cân nhắc và vẫn cần giữ, nói rõ lý do cho user rồi đi tiếp.")
    print("\n".join(msg), file=sys.stderr)
    return 2 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
