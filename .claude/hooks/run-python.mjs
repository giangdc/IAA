#!/usr/bin/env node
/**
 * run-python.mjs — chạy một script Python bằng interpreter CÓ THẬT trên máy này.
 *
 * Vì sao cần: không tên nào portable cả.
 *   macOS/Linux → có `python3`, thường KHÔNG có `python`
 *   Windows (installer python.org) → có `python` + `py`, KHÔNG có `python3`
 * Hardcode một tên là hỏng nửa team, và vì hook fail im lặng nên không ai biết.
 * Lịch sử repo đã lật `python3` ⇄ `python` một vòng — file này chấm dứt vòng đó.
 *
 * Dùng:  node .claude/hooks/run-python.mjs <script.py> [args...]
 *
 * Hợp đồng exit code — QUAN TRỌNG với PostToolUse:
 *   - Forward NGUYÊN exit code của script (2 = chặn, 0 = cho qua).
 *   - ⛔ Không được nuốt exit 2 thành 0, cũng không được biến "thiếu python"
 *     thành exit 2.
 *   - Không tìm được interpreter nào ⇒ exit 0 (fail-safe, cùng luật với
 *     validate-vibe-run.mjs): hook hỏng thì cảnh báo, ⛔ không chặn người dùng.
 */
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const CANDIDATES = [['python3'], ['python'], ['py', '-3']];
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('[run-python] thiếu đường dẫn script .py');
  process.exit(0); // fail-safe
}

// 🔴 Script thiếu ⇒ Python thoát 2, mà 2 = CHẶN ở PostToolUse ⇒ khoá mọi
// Write/Edit vì một file hook không tồn tại. Bắt trước, trả 0.
if (!existsSync(args[0])) {
  console.error(`[run-python] không thấy ${args[0]} — bỏ qua hook.`);
  process.exit(0); // fail-safe
}

for (const [bin, ...pre] of CANDIDATES) {
  const r = spawnSync(bin, [...pre, ...args], { stdio: 'inherit' });
  // r.error = không có binary đó trên PATH → thử tên tiếp theo.
  // status === null = bị signal giết → coi như không chạy được, thử tiếp.
  if (r.error || r.status === null) continue;
  process.exit(r.status);
}

console.error(
  '[run-python] không tìm thấy python3 / python / py trên PATH — bỏ qua hook.\n' +
  '             Cài Python 3.9+ rồi mở lại session để hook hoạt động.'
);
process.exit(0); // fail-safe: thiếu môi trường thì KHÔNG chặn
