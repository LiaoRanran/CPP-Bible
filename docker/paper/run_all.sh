#!/usr/bin/env bash
# =====================================================================
# 676h · 论文数字一键复算（docker/paper/run_all.sh）
#
# 用法：
#   docker build -f docker/paper/Dockerfile -t queyi-paper-repro .
#   docker run --rm -v "$PWD/out:/workspace/out" queyi-paper-repro
# 或直接在本机跑：PY=python bash docker/paper/run_all.sh
#
# 设计原则（fail-loud）：
#   * 每一步拿不到数字就**报错退出**，不做静默降级；
#   * 输出统一落在 out/，不覆盖 data/ 下任何已落盘产物
#     （避免"复现"变成"改数据"，这正是论文 §Analysis(3) 批评过的失败模式）。
# =====================================================================
set -euo pipefail

PY="${PY:-python3}"
OUT="${OUT:-out}"
mkdir -p "$OUT"
log() { echo "[run_all] $*"; }
fail() { echo "[run_all][FAIL] $*" >&2; exit 1; }
check_eq() {                       # check_eq <actual> <expected> <label>
  if [ "$1" != "$2" ]; then fail "$3: got '$1', expected '$2'"; fi
  log "OK  $3 = $1"
}

log "== 0. 环境自检 =="
"$PY" --version > "$OUT/00_python.txt" 2>&1 || fail "python 不可用"
(g++ --version 2>/dev/null || g++-13 --version) | head -1 > "$OUT/01_gxx.txt" || echo "g++: MISSING" > "$OUT/01_gxx.txt"
{ setarch --version 2>/dev/null || echo "setarch: MISSING"; } > "$OUT/02_setarch.txt"
cat "$OUT/00_python.txt" "$OUT/01_gxx.txt" "$OUT/02_setarch.txt"

log "== 1. 系统计数 =="
RULES=$("$PY" -c "import sys;sys.path.insert(0,'tools');import gate_engine;print(len(gate_engine.RULES))")
check_eq "$RULES" 67 "判决规则数 len(RULES)"

LEDGER=$("$PY" -c "print(sum(1 for l in open('data/authority/decision_event_v2_ledger.jsonl',encoding='utf-8') if l.strip()))")
check_eq "$LEDGER" 452 "权威账本事件数"

ATOMS=$("$PY" tools/counts_659.py --json | "$PY" -c "import json,sys;print(json.load(sys.stdin)['atoms_real'])")
check_eq "$ATOMS" 42 "实卡数 atoms_real"

SEV=$("$PY" -c "import sys;sys.path.insert(0,'tools');import gate_engine;from collections import Counter;c=Counter(getattr(r,'severity',None) for r in gate_engine.RULES);print(c.get('block',0),c.get('warn',0),c.get('advice',0))")
echo "规则严重度分解 block/warn/advice = $SEV" | tee "$OUT/10_rule_severity.txt"

"$PY" -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(31,42)])" > "$OUT/11_vc_ci.txt"
log "Verifier Coverage 31/42 的 CP95 = $(cat "$OUT/11_vc_ci.txt")"

log "== 2. 头版检出率重算（从已落盘 reveal 产物读算，不重跑检测器）=="
"$PY" - <<'PYEOF' | tee "$OUT/20_headline.txt"
import json

h = json.load(open("data/holdout_reveal_5_672h.json", encoding="utf-8"))["cumulative"]
c = json.load(open("data/external_corpus_reveal_672h.json", encoding="utf-8"))["cumulative"]
print("holdout  %.1f%% (%d/%d)" % (h["error_subset"]["detect_rate_pct"],
                                  h["error_subset"]["catch"], h["denominator"]["value"]))
print("corpus   %.1f%% (%d/%d)" % (c["detect_rate_pct"], c["catch"], c["denominator"]["value"]))
print("corpusC  %.1f%% (%d/%d)" % (100.0 * c["catch"] / c["total"], c["catch"], c["total"]))
for name in ("sanitizer", "compiler-warn", "cross-compile"):
    layer = c["by_layer"][name]
    print("layer %-14s %.1f%% (%d/%d)" % (name, layer["detect_rate_pct"],
                                          layer["catch"], layer["denominator"]["value"]))
PYEOF

log "== 3. 统计口径自检 =="
"$PY" tools/stats_672k.py --selftest > "$OUT/30_stats_selftest.txt" || fail "stats_672k 自检不过"
tail -3 "$OUT/30_stats_selftest.txt"

log "== 3b. A5 全量 + 能力边界：从原始矩阵独立重算 =="
"$PY" tools/recompute_a5_676f.py > "$OUT/31_a5_recompute.txt" || fail "A5/盲区重算与登记不一致"
tail -3 "$OUT/31_a5_recompute.txt"

log "== 3c. 数据完整性（1137 样本清单）=="
"$PY" tools/data_integrity_676h.py > "$OUT/32_data_integrity.txt" || fail "样本清单完整性检查失败"
tail -2 "$OUT/32_data_integrity.txt"

log "== 3d. 随机种子审计（实验类未固定种子数须为 0）=="
# 676m：输出改到 $OUT/ —— 与脚本自身"不覆盖 data/ 下任何已落盘产物"的原则一致
# （676h 的原始调用会把 data/676h_seed_audit.{json,md} 重写，导致工作树被污染）。
"$PY" tools/seed_audit_676h.py \
  --out-json "$OUT/33_seed_audit.json" --out-md "$OUT/33_seed_audit.md" \
  > "$OUT/33_seed_audit.txt" || fail "存在未固定种子的实验类脚本"
tail -2 "$OUT/33_seed_audit.txt"

log "== 3e. 676m 数据修复自检（幂等门禁：H1 残留须为 0、待迁移须为 0）=="
"$PY" tools/fix_676m_schema.py --verify > "$OUT/34_fix_676m_verify.txt" \
  || fail "676m 修复未落盘或非幂等（见 $OUT/34_fix_676m_verify.txt）"
tail -2 "$OUT/34_fix_676m_verify.txt"

log "== 3f. 676m A5 重算门禁（修正标签后主端点须与 676f 逐位一致）=="
"$PY" tools/recompute_a5_676m.py --check > "$OUT/35_a5_676m_check.txt" \
  || fail "676m 重算与 676f 登记值不一致（见 $OUT/35_a5_676m_check.txt）"
tail -2 "$OUT/35_a5_676m_check.txt"

log "== 3g. 676k 数据质量审计（只读；去重 + 字段完整性）=="
"$PY" tools/audit_676k_integrity.py --json "$OUT/36_integrity_676k.json" \
  > "$OUT/36_integrity_676k.txt" || fail "676k 完整性审计失败"
tail -3 "$OUT/36_integrity_676k.txt"
"$PY" tools/audit_676k_dedup.py --json "$OUT/37_dedup_676k.json" --quiet \
  > "$OUT/37_dedup_676k.txt" || fail "676k 去重审计失败"
tail -3 "$OUT/37_dedup_676k.txt"
cat <<'NOTE' | tee "$OUT/38_676k_network_note.txt"
[note] 676k 的另两项审计需要外部条件，本脚本默认不跑：
  * tools/audit_676k_compile.py --sample --run   （需要 g++ 13.x + WSL，约 10 分钟）
  * tools/audit_676k_source.py  --collect --probe（需要联网访问 NVD / GitHub API）
已落盘结果：data/676k_compile_results.json（217/217）、data/676k_source_results.json（74/74）。
NOTE

log "== 4. 论文数字 vs 权威源（676h 审计工具）=="
"$PY" tools/verify_paper_numbers.py --out-json "$OUT/40_number_audit.json" --out-md "$OUT/41_number_audit.md" \
  || fail "存在与权威源不一致的论文数字"
tail -3 "$OUT/41_number_audit.md" >/dev/null 2>&1 || true

log "== 5. 论文编译 =="
if command -v tectonic >/dev/null 2>&1; then
  (cd research/latex && tectonic -X compile queyi_neurips2027_v1.1.tex --outdir ../../out) \
    || fail "论文编译失败"
else
  echo "tectonic 未安装 ⇒ 跳过编译（本机 v0.17.0；见 REPRODUCE.md §6）" | tee "$OUT/50_build_skipped.txt"
fi

log "全部完成。输出目录：$OUT"
