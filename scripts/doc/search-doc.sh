#!/usr/bin/env bash
# search-doc.sh — tra cứu nội dung file .docx gốc để verify Source Quote (verbatim quoting).
#
# Vì sao cần: quoting-guide bắt quote VERBATIM. Không có cách tra nhanh thì analyst gõ lại theo
# ký ức → quote drift so với doc, mà drift kiểu này không có check nào bắt được. Script trích text
# từ .docx (unzip word/document.xml → strip XML) rồi grep, in kèm SỐ DÒNG để ghi vào Source Location.
#
# Cách dùng (chạy từ đâu cũng được — resolve theo repo root):
#   scripts/doc/search-doc.sh "từ khoá"                      # tìm trong doc mặc định
#   scripts/doc/search-doc.sh "từ khoá" "Tên file.docx"       # chỉ định doc khác
#
# Cấu hình qua env (KHÔNG hardcode tên project/doc trong script):
#   DOC_DIR=00_input/v2.0/Doc  scripts/doc/search-doc.sh "..."   # đổi version
#   DOC_DEFAULT="PRD v2.docx"  scripts/doc/search-doc.sh "..."   # đổi doc mặc định
#
# Nếu không set DOC_DEFAULT: có đúng 1 file .docx trong DOC_DIR → tự dùng file đó;
# nhiều file → liệt kê ra và yêu cầu chọn (KHÔNG tự đoán).

set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="${DOC_ROOT:-$(cd "$DIR/../.." && pwd)}"
VERSION="${DOC_VERSION:-v1.0}"
DOC_DIR="${DOC_DIR:-$ROOT/00_input/$VERSION/Doc}"

QUERY="${1:?Cần truyền từ khoá cần tìm}"

[ -d "$DOC_DIR" ] || { echo "❌ Không thấy thư mục doc: $DOC_DIR"; echo "   Set DOC_DIR= hoặc DOC_VERSION= cho đúng."; exit 1; }

# Chọn doc: arg 2 > $DOC_DEFAULT > tự nhận nếu chỉ có 1 file .docx
DOCX="${2:-${DOC_DEFAULT:-}}"
if [ -z "$DOCX" ]; then
  # KHÔNG dùng mapfile/array — bash 3.2 (macOS mặc định) không có mapfile.
  docx_list="$(cd "$DOC_DIR" && ls -1 *.docx 2>/dev/null || true)"
  docx_count="$(printf '%s\n' "$docx_list" | grep -c . || true)"
  if [ "$docx_count" -eq 0 ]; then
    echo "❌ Không có file .docx nào trong $DOC_DIR"; exit 1
  elif [ "$docx_count" -eq 1 ]; then
    DOCX="$docx_list"
  else
    echo "❌ Có $docx_count file .docx — chỉ định rõ file cần tra (KHÔNG tự đoán):"
    printf '%s\n' "$docx_list" | sed 's/^/   - /'
    echo "   Dùng: $(basename "$0") \"$QUERY\" \"<tên file>\"   hoặc set DOC_DEFAULT="
    exit 1
  fi
fi

[ -f "$DOC_DIR/$DOCX" ] || { echo "❌ Không thấy: $DOC_DIR/$DOCX"; exit 1; }

TXT="/tmp/$(echo "${DOCX}" | tr ' /' '__').txt"

# Trích text từ .docx (cache ở /tmp; xoá cache nếu .docx mới hơn)
if [ ! -f "$TXT" ] || [ "$DOC_DIR/$DOCX" -nt "$TXT" ]; then
  python3 - "$DOC_DIR/$DOCX" "$TXT" <<'PY'
import sys, zipfile, re
src, out = sys.argv[1], sys.argv[2]
xml = zipfile.ZipFile(src).read('word/document.xml').decode('utf-8', 'ignore')
xml = xml.replace('</w:p>', '\n')
txt = re.sub(r'<[^>]+>', '', xml)
for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")]:
    txt = txt.replace(a, b)
open(out, 'w').write('\n'.join(l.strip() for l in txt.split('\n') if l.strip()))
PY
fi

echo "🔎 Tìm \"$QUERY\" trong: $DOCX"
echo "---"
grep -in --color=always "$QUERY" "$TXT" \
  || echo "❌ KHÔNG tìm thấy — Source Quote có thể đã drift (không còn khớp doc gốc), hoặc doc đã đổi bản."
