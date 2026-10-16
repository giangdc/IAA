#!/usr/bin/env bash
# map-section.sh — tra ký hiệu § (dùng trong Source Location) → heading + nội dung thật trong doc.
#
# Vì sao cần: khi doc KHÔNG đánh số FR/VR/AC (`req_notation: none`), traceability trace bằng
# `DOC-ID §<section>` — nhưng ký hiệu § đó do analyst TỰ ĐÁNH, doc gốc không chứa chuỗi này.
# Không có bảng ánh xạ thì reviewer không tra được §C.1 là mục nào ⇒ Source Location thành vô nghĩa.
# Script đọc doc-section-index.md (bảng § ↔ heading ↔ dòng) rồi in đúng đoạn doc của section đó.
#
# Cách dùng (chạy từ đâu cũng được):
#   scripts/doc/map-section.sh "C.1"      # hoặc "§C.1", "E.3", "G.III.2"
#   scripts/doc/map-section.sh            # không tham số → in toàn bộ bảng ánh xạ
#
# Cấu hình qua env (KHÔNG hardcode tên project/doc):
#   DOC_VERSION=v2.0                      # đổi version (mặc định v1.0)
#   DOC_DIR=... DOC_INDEX=... DOC_DEFAULT="PRD v2.docx"

set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="${DOC_ROOT:-$(cd "$DIR/../.." && pwd)}"
VERSION="${DOC_VERSION:-v1.0}"
DOC_DIR="${DOC_DIR:-$ROOT/00_input/$VERSION/Doc}"
INDEX="${DOC_INDEX:-$ROOT/02_analyze-requirements/$VERSION/_global/doc-section-index.md}"

[ -f "$INDEX" ] || { echo "❌ Không thấy index: $INDEX"; echo "   Chạy analyze-requirements để sinh doc-section-index.md, hoặc set DOC_INDEX="; exit 1; }
[ -d "$DOC_DIR" ] || { echo "❌ Không thấy thư mục doc: $DOC_DIR — set DOC_DIR= hoặc DOC_VERSION="; exit 1; }

# Chọn doc: $DOC_DEFAULT > tự nhận nếu chỉ có 1 file .docx
DOCX="${DOC_DEFAULT:-}"
if [ -z "$DOCX" ]; then
  # KHÔNG dùng mapfile/array — bash 3.2 (macOS mặc định) không có mapfile.
  docx_list="$(cd "$DOC_DIR" && ls -1 *.docx 2>/dev/null || true)"
  docx_count="$(printf '%s\n' "$docx_list" | grep -c . || true)"
  if [ "$docx_count" -eq 0 ]; then
    echo "❌ Không có file .docx nào trong $DOC_DIR"; exit 1
  elif [ "$docx_count" -eq 1 ]; then
    DOCX="$docx_list"
  else
    echo "❌ Có $docx_count file .docx — set DOC_DEFAULT= để chỉ rõ doc primary (KHÔNG tự đoán):"
    printf '%s\n' "$docx_list" | sed 's/^/   - /'
    exit 1
  fi
fi
[ -f "$DOC_DIR/$DOCX" ] || { echo "❌ Không thấy: $DOC_DIR/$DOCX"; exit 1; }

# Không tham số → in cả bảng
if [ $# -eq 0 ]; then
  echo "📖 Bảng ánh xạ § ↔ heading ↔ dòng ($(basename "$INDEX")):"; echo
  grep -E '^\| `§' "$INDEX"
  echo; echo "→ Dùng: $(basename "$0") \"C.1\"  để xem nội dung 1 section."
  exit 0
fi

SEC="${1#§}"                                   # bỏ § đầu nếu có
ROW="$(grep -E "^\| \`§${SEC}\` " "$INDEX" || true)"
[ -n "$ROW" ] || { echo "❌ Không tìm thấy §${SEC} trong index. Xem danh sách: $(basename "$0")"; exit 1; }
START="$(echo "$ROW" | sed -E 's/.*\| *([0-9]+) *\|$/\1/')"
HEAD="$(echo "$ROW"  | sed -E 's/^\| `[^`]+` \| (.+) \| [0-9]+ \|$/\1/')"

# dòng bắt đầu của section KẾ TIẾP (điểm dừng)
NEXT="$(grep -E '^\| `§' "$INDEX" | awk -v s="$START" -F'|' '{gsub(/ /,"",$4); if ($4+0>s){print $4+0; exit}}')"
[ -n "$NEXT" ] || NEXT=99999

echo "🔎 §${SEC} → \"${HEAD}\"  ($(basename "$DOCX") dòng ${START}..$((NEXT-1)))"
echo "---"
python3 - "$DOC_DIR/$DOCX" "$START" "$NEXT" <<'PY'
import sys, zipfile, re
src, start, nxt = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
xml = zipfile.ZipFile(src).read('word/document.xml').decode('utf-8', 'ignore').replace('</w:p>', '\n')
txt = re.sub(r'<[^>]+>', '', xml)
for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")]:
    txt = txt.replace(a, b)
lines = [l.strip() for l in txt.split('\n') if l.strip()]
for i in range(start - 1, min(nxt - 1, len(lines))):
    print(f"{i+1}: {lines[i]}")
PY
