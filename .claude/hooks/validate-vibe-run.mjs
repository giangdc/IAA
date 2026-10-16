#!/usr/bin/env node
/**
 * validate-vibe-run.mjs — HARNESS-ENFORCED evidence gate cho vibe-test.
 *
 * "Best of both": cơ chế ENFORCEMENT (Stop hook — harness tự chạy, AI không bỏ được)
 * + engine DETECTION là `verify_evidence.py` (904 dòng, audit 2 chiều TC↔ảnh của teammate).
 * Biến gate advisory (skill bảo AI tự chạy) thành gate cưỡng chế: AI định dừng → hook
 * tự gọi verify_evidence.py; có FABRICATION evidence → CHẶN, buộc sửa mới được dừng.
 *
 * Chặn (fabrication — luôn sai): missing · batched · dangling · misattr · no_citation
 *   · orphan · uncited · badname · log_format_broken.
 * KHÔNG chặn coverage-owed (TC NOT_RUN còn lại = run partial hợp lệ → §8 PARTIAL, không phải lỗi).
 *
 * Chế độ:
 *   - Stop hook (mặc định): đọc payload stdin. Chỉ soi VR folder MỚI NHẤT nếu fresh (<45').
 *   - Manual:  node validate-vibe-run.mjs --check <VR-folder>   (chạy verify_evidence.py trực tiếp, exit theo nó)
 *
 * Fail-safe: thiếu python / thiếu verify_evidence.py / parse lỗi / bất kỳ exception → KHÔNG chặn (exit 0).
 * Interpreter dò qua pyBin(): python3 → python → py -3 (Windows không có python3).
 * Tôn trọng stop_hook_active (chống loop).
 */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

/** Interpreter Python có thật trên máy này. macOS/Linux có python3, Windows có python/py. */
let _py;
function pyBin() {
  if (_py !== undefined) return _py;
  for (const c of [['python3'], ['python'], ['py', '-3']]) {
    const r = spawnSync(c[0], [...c.slice(1), '-c', 'pass'], { stdio: 'ignore' });
    if (!r.error && r.status === 0) return (_py = c);
  }
  return (_py = null);
}
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import { homedir } from 'node:os';

const FRESH_MINUTES = 45;
const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, '..', '..');
const vibeDir = join(repoRoot, '08_test-runs', 'vibe');

const args = process.argv.slice(2);
const manualIdx = args.indexOf('--check');
const manual = manualIdx !== -1;
const manualFolder = manual ? args[manualIdx + 1] : null;

// category fabrication → chặn (mảng non-empty = vi phạm)
const FAB = {
  missing: 'TC ghi verdict PASS/FAIL/BLOCKED nhưng KHÔNG có ảnh nào',
  batched: '1 ảnh gộp nhiều TC (không chứng minh được từng case)',
  no_verify: 'ảnh không phải điểm verify / sai slot',
  badname: 'tên ảnh sai quy ước (không map được TC↔ảnh)',
  orphan: 'ảnh mang TC ID mà TC đó không có section trong log',
  no_citation: 'section TC không trích tên ảnh nào',
  dangling: 'report trích tên ảnh KHÔNG tồn tại trên disk (link chết)',
  misattr: 'ảnh mang TC ID của TC KHÁC (trích nhầm)',
  uncited: 'ảnh trên disk không được trích ở đâu',
};

function readStdin() { try { return readFileSync(0, 'utf8'); } catch { return ''; } }
function allow(msg) { if (msg && manual) console.log(msg); process.exit(0); }
function block(reason) {
  if (manual) { console.error(reason); process.exit(2); }
  process.stdout.write(JSON.stringify({ decision: 'block', reason }));
  process.exit(0);
}

function findVerifyScript() {
  const cands = [
    join(scriptDir, 'verify_evidence.py'),                                            // bundled trong .claude/hooks (travels với repo)
    join(homedir(), '.claude', 'skills', 'vibe-test', 'scripts', 'verify_evidence.py'), // bản skill (fallback)
  ];
  return cands.find(existsSync) || null;
}

/**
 * Layout `vibe/` (refactor 2026-08-04):
 *   VR-*        phiên chạy TC của version ĐANG CHẠY → hợp đồng ĐẦY ĐỦ (verify_evidence.py)
 *   repro/RP-*  phiên repro/verify bug            → hợp đồng NHẸ (report + ≤3 ảnh, KHÔNG per-TC)
 *   v<X>/       phiên của version ĐÃ ĐÓNG         → 🔒 SEALED, MIỄN TRỪ gate
 *   coverage/ locators/  sổ + locator, không phải phiên chạy
 * ⚠️ Trước refactor hook chỉ lọc `^VR-` ở root — sau khi seal thì root không còn VR nào ⇒ gate
 * sẽ im lặng bất động. Nên phải khai tường minh vùng nào bị kiểm, vùng nào miễn trừ.
 */
const SEALED_RE = /^v\d+\.\d+$/;

function newestDir(baseDir, nameRe) {
  if (!existsSync(baseDir)) return null;
  const c = readdirSync(baseDir)
    .filter((n) => nameRe.test(n))
    .map((n) => { const p = join(baseDir, n); try { return statSync(p).isDirectory() ? { n, p, m: statSync(p).mtimeMs } : null; } catch { return null; } })
    .filter(Boolean).sort((a, b) => b.m - a.m);
  return c[0] || null;
}

/** Phiên mới nhất cần gate: `VR-*` ở ROOT (đầy đủ) hoặc `repro/RP-*` (nhẹ) — KHÔNG bao giờ `v<X>/`. */
function latestRun() {
  const vr = newestDir(vibeDir, /^VR-/);
  const rp = newestDir(join(vibeDir, 'repro'), /^RP-/);
  const cands = [vr && { ...vr, mode: 'full' }, rp && { ...rp, mode: 'light' }].filter(Boolean);
  cands.sort((a, b) => b.m - a.m);
  return cands[0] || null;
}

/** Hợp đồng NHẸ cho `repro/RP-*`: có report `.md` · ≤3 ảnh · không video. Trả mảng vi phạm. */
function lightCheck(dir) {
  const viol = [];
  const files = readdirSync(dir, { recursive: true, encoding: 'utf8' });
  if (!files.some((f) => /\.md$/.test(f))) viol.push('- thiếu `report.md` — `missing_report`');
  const imgs = files.filter((f) => /\.(png|jpe?g)$/i.test(f));
  if (imgs.length === 0) viol.push('- không có ảnh nào chứng minh kết luận — `no_evidence`');
  if (imgs.length > 3) viol.push(`- ${imgs.length} ảnh > mức 3 của hợp đồng nhẹ — `+'`too_many_images`'+' (phiên chạy TC thì dùng `VR-`, không dùng `repro/`)');
  const vids = files.filter((f) => /\.(webm|mp4)$/i.test(f));
  if (vids.length) viol.push(`- ${vids.length} video trong repo (⛔ đính Jira, không commit) — \`video_committed\``);
  return viol;
}

/** Path nằm trong vùng sealed `vibe/v<X>/`? */
function isSealed(target) {
  const rel = target.startsWith(vibeDir) ? target.slice(vibeDir.length + 1) : '';
  return SEALED_RE.test(rel.split(/[/\\]/)[0] || '');
}

// chạy verify_evidence.py <dir> --json → {data} | {skip}
function runGate(dir) {
  const script = findVerifyScript();
  if (!script) return { skip: 'không thấy verify_evidence.py (bundle vào .claude/hooks/ hoặc cài vibe-test skill)' };
  const py = pyBin();
  if (!py) return { skip: 'không tìm thấy python3/python/py' };
  const r = spawnSync(py[0], [...py.slice(1), script, dir, '--json'], { encoding: 'utf8', timeout: 60000 });
  if (r.error || r.status === null) return { skip: 'python không chạy được' };
  if (r.status === 2) return { skip: 'verify_evidence usage error' };
  let data; try { data = JSON.parse(r.stdout); } catch { return { skip: 'không parse được JSON' }; }
  return { data };
}

try {
  // ---- manual: chạy verify_evidence.py trực tiếp, exit theo nó ----
  if (manual) {
    const target = resolve(repoRoot, manualFolder);
    if (!existsSync(target)) { console.error('không thấy folder: ' + manualFolder); process.exit(0); }
    if (isSealed(target)) {
      console.log(
        `🔒 MIỄN TRỪ — \`${manualFolder}\` nằm trong vùng SEALED \`vibe/v<X>/\`.\n` +
        `   Hợp đồng evidence ra đời SAU khi các phiên này chạy (Nợ #1/#1b — 45/45 phiên v1.0 thiếu\n` +
        `   scope-ledger.md, 0/45 có vibe-log.md). Chấm chúng bằng hợp đồng hiện tại là vô nghĩa, và\n` +
        `   ⛔ bịa ledger cho phiên đã chạy là điều luật cấm. Xem 08_test-runs/INDEX.md §Nợ đã biết.`
      );
      process.exit(0);
    }
    if (/[/\\]repro[/\\]/.test(target)) {
      const viol = lightCheck(target);
      if (!viol.length) { console.log(`✓ ${manualFolder} — hợp đồng NHẸ (repro) OK`); process.exit(0); }
      console.error(`🔒 REPRO CONTRACT — \`${manualFolder}\`:\n${viol.join('\n')}`);
      process.exit(2);
    }
    const script = findVerifyScript();
    if (!script) { console.error('không thấy verify_evidence.py'); process.exit(0); }
    const py = pyBin() || ['python3'];
    const r = spawnSync(py[0], [...py.slice(1), script, target], { stdio: 'inherit' });
    process.exit(r.status === null ? 0 : r.status);
  }

  // ---- Stop hook ----
  const raw = readStdin();
  if (raw) { try { if (JSON.parse(raw).stop_hook_active) process.exit(0); } catch {} }

  const t = latestRun();
  if (!t) process.exit(0);
  if ((Date.now() - statSync(t.p).mtimeMs) / 60000 > FRESH_MINUTES) process.exit(0); // run cũ → không chặn

  // repro/RP-* → hợp đồng NHẸ, KHÔNG chấm bằng verify_evidence.py (nó đòi ảnh per-TC)
  if (t.mode === 'light') {
    const viol = lightCheck(t.p);
    if (viol.length === 0) process.exit(0);
    block(
      `🔒 REPRO CONTRACT — phiên \`repro/${t.n}\` chưa đủ để kết thúc:\n` + viol.join('\n') +
      `\n\nHợp đồng nhẹ: \`report.md\` + ≤3 ảnh + không video (08_test-runs/vibe/repro/README.md).` +
      ` Nếu phiên này thực sự chạy TC và có verdict per-TC thì nó phải là \`vibe/VR-<NNN>-<MOD>-<date>/\`, không phải \`repro/\`.`
    );
  }

  const g = runGate(t.p);
  if (g.skip) process.exit(0); // fail-safe: không chặn khi không gate được

  const d = g.data;
  const viol = [];
  for (const k of Object.keys(FAB)) {
    const v = d[k];
    if (Array.isArray(v) && v.length) viol.push(`- ${FAB[k]} — \`${k}\`: ${v.length}`);
  }
  if (d.log_format_broken) viol.push('- vibe-log gom 1 bảng chung, không map được TC↔ảnh — `log_format_broken`');

  if (viol.length === 0) process.exit(0); // sạch fabrication (coverage-owed = partial hợp lệ, không chặn)

  block(
    `🔒 VIBE-TEST EVIDENCE GATE — run \`${t.n}\` có bằng chứng KHÔNG hợp lệ, không được kết thúc:\n` +
    viol.join('\n') +
    `\n\nĐây là fabrication/link-chết evidence (verify_evidence.py). Sửa (đa số chỉ sửa chữ trong vibe-log.md, ` +
    `không cần chạy lại TC) rồi mới dừng. Xem chi tiết: \`node .claude/hooks/validate-vibe-run.mjs --check ${t.n}\`.`
  );
} catch {
  process.exit(0); // fail-safe tuyệt đối
}
