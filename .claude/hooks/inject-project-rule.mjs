#!/usr/bin/env node
/**
 * inject-project-rule.mjs — SessionStart hook: LUÔN nạp Project_rule vào context.
 *
 * Case "Project_rule phải luôn được đọc" bị lờ vì không có gì ép. Hook này chèn
 * inventory rule (path + danh sách section headers) vào đầu mỗi session → model
 * không thể "quên biết" là Project_rule tồn tại và phải tuân thủ. Precondition,
 * không phải khuyến nghị.
 *
 * Output: JSON {hookSpecificOutput:{hookEventName, additionalContext}} (chuẩn
 * SessionStart/UserPromptSubmit của Claude Code). Fail-safe: lỗi → exit 0 im lặng.
 */
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

try {
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const repoRoot = resolve(scriptDir, '..', '..');

  // path Project_rule (chỉnh nếu project để chỗ khác)
  const candidates = [
    join(repoRoot, '02_analyze-requirements', 'Project_rule.md'),
    join(repoRoot, 'Project_rule.md'),
  ];
  const rulePath = candidates.find(existsSync);
  if (!rulePath) process.exit(0); // không có → không chèn gì

  const text = readFileSync(rulePath, 'utf8');
  const rel = rulePath.replace(repoRoot + '/', '').replace(repoRoot + '\\', '');
  // Lấy CẢ `##` VÀ `###`, thụt lề cấp 3 để giữ phân cấp.
  // 🔴 Vì sao không chỉ lọc `##`: các rule cụ thể nhất — thứ dễ vi phạm nhất — thường
  // nằm ở heading cấp 3 (`### §x.y`). Chỉ lọc `##` thì inventory hiện mục cha mà KHÔNG
  // hiện mục con ⇒ phiên mới vẫn "không biết" chúng tồn tại, tức hook chạy nhưng
  // VÔ DỤNG đúng chỗ cần nhất.
  const headers = text.split(/\r?\n/)
    .filter((l) => /^#{2,3}\s+/.test(l))
    .map((l) => /^###\s+/.test(l)
      ? l.replace(/^###\s+/, '  - ')
      : l.replace(/^##\s+/, '- '));

  const context =
    `🔒 PROJECT RULES (bắt buộc tuân thủ mọi giai đoạn) — nguồn: \`${rel}\`\n` +
    `Các skill (analyze/generate-tc/vibe-test/log-bug…) PHẢI đọc & giữ rule này. ` +
    `Trước khi tạo/ghi artifact, ĐỌC LẠI file trên nếu chưa chắc. Inventory section:\n` +
    headers.join('\n') +
    `\n(Đây là ràng buộc dự án, không phải gợi ý. Vi phạm rule = output không hợp lệ.)`;

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: context },
  }));
  process.exit(0);
} catch {
  process.exit(0);
}
