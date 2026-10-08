#!/usr/bin/env bash
# =====================================================================
# 693-B2 · Scripts/reproduce_all.sh — 一键复现（按依赖顺序）
#
# 用法：
#   bash Scripts/reproduce_all.sh                 # 全链（含需联网/需 WSL 的步骤会跳过并登记）
#   bash Scripts/reproduce_all.sh --out out/693   # 指定输出目录
#   bash Scripts/reproduce_all.sh --skip-env      # 跳过环境体检（不建议）
#
# 五个阶段（依赖顺序，前一步失败即停 —— fail-loud，不做静默降级）：
#   S0 环境体检        Scripts/verify_environment.sh --report
#   S1 数据完整性      sha256 校验 + data_integrity_676h.py
#   S2 数字复算        复用 docker/paper/run_all.sh 的 1–4 步（权威口径）
#   S3 门禁            paper_quality_gate + fast_gate
#   S4 验证报告        汇总到 $OUT/99_reproduce_report.md
#
# 诚实边界（693 红线 7）
# ---------------------
# 本脚本**未在容器内实测**：693 执行环境未安装 Docker。
# 它在**宿主机**（Windows + Git Bash）上的 S0/S1/S3 段是可跑的，S2 依赖既有
# docker/paper/run_all.sh（676h 已验证口径）。
# =====================================================================
set -uo pipefail

OUT="${OUT:-out/693_reproduce}"
SKIP_ENV=0
# 用 while+shift 解析（for 循环里 shift 不会缩短 $@，会误把取值当选项）
while [ "$#" -gt 0 ]; do
  case "$1" in
    --out=*) OUT="${1#--out=}" ; shift ;;
    --out)   OUT="${2:-}"; shift 2 ;;
    --skip-env) SKIP_ENV=1; shift ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "[reproduce] 未知参数: $1" >&2; exit 2 ;;
  esac
done

PY="${PY:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY="python"

mkdir -p "$OUT"
log() { echo; echo "[reproduce] $*"; }
fail() { echo "[reproduce][FAIL] $*" >&2; exit 1; }
skip() { echo "[reproduce][SKIP] $*"; echo "$*" >> "$OUT/99_skipped.txt"; }

START_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
: > "$OUT/99_skipped.txt"

echo "=============================================="
echo " 693-B2 · Queyi 一键复现"
echo " 输出目录：$OUT"
echo " 开始：$START_TS"
echo "=============================================="

# ── S0：环境体检 ────────────────────────────────────────────────────────
log "S0 环境体检"
if [ "$SKIP_ENV" = "1" ]; then
  skip "S0 环境体检（--skip-env）"
else
  bash Scripts/verify_environment.sh --report 2>&1 | tee "$OUT/00_environment.txt" \
    || fail "环境体检脚本自身执行失败（不是版本不符）"
fi

# ── S1：数据完整性（sha256）──────────────────────────────────────────────
log "S1 数据完整性校验（sha256）"
MANIFEST="data/693_data_manifest.sha256"
if [ -f "$MANIFEST" ]; then
  # 有清单就逐条比对；缺一条即 FAIL（不做"找不到就跳过"的静默降级）
  MISSING=0; MISMATCH=0
  while IFS=  read -r line; do
    [ -z "$line" ] && continue
    case "$line" in \#*) continue ;; esac   # 跳过清单里的注释行
    exp_hash="$(printf '%s' "$line" | awk '{print $1}')"
    rel="$(printf '%s' "$line" | awk '{ $1=""; sub(/^ /,""); print }')"
    if [ ! -f "$rel" ]; then echo "  MISSING  $rel"; MISSING=$((MISSING+1)); continue; fi
    if command -v sha256sum >/dev/null 2>&1; then
      act="$(sha256sum "$rel" | cut -d' ' -f1)"
    elif command -v shasum >/dev/null 2>&1; then
      act="$(shasum -a 256 "$rel" | cut -d' ' -f1)"
    else
      fail "找不到 sha256sum / shasum，无法做完整性校验（不跳过）"
    fi
    if [ "$act" != "$exp_hash" ]; then echo "  MISMATCH $rel"; MISMATCH=$((MISMATCH+1)); fi
  done < "$MANIFEST"
  echo "  missing=$MISSING mismatch=$MISMATCH" | tee "$OUT/10_sha256.txt"
  [ "$MISSING" -eq 0 ] && [ "$MISMATCH" -eq 0 ] \
    || fail "数据完整性校验未通过（missing=$MISSING mismatch=$MISMATCH）"
else
  skip "S1 sha256 清单 $MANIFEST 不存在（本批未生成全量清单，见验收报告诚实清单）"
  "$PY" tools/data_integrity_676h.py > "$OUT/10_data_integrity.txt" 2>&1 \
    && { echo "  OK  数据完整性脚本通过"; tail -2 "$OUT/10_data_integrity.txt"; } \
    || fail "data_integrity_676h.py 未通过（见 $OUT/10_data_integrity.txt）"
fi

# ── S2：数字复算（复用 676h 权威口径）────────────────────────────────────
log "S2 论文数字复算（复用 docker/paper/run_all.sh）"
if [ -f docker/paper/run_all.sh ]; then
  # 只跑到"论文数字 vs 权威源"为止；**不**做论文编译（容器里没装 tectonic）
  OUT="$OUT" PY="$PY" bash docker/paper/run_all.sh > "$OUT/20_run_all.log" 2>&1 \
    && { echo "  OK  run_all 通过"; tail -5 "$OUT/20_run_all.log"; } \
    || { echo "  run_all 退出非 0（可能是 tectonic 缺失导致的第 5 步失败）：";
         tail -25 "$OUT/20_run_all.log";
         grep -q "tectonic 未安装" "$OUT/20_run_all.log" \
           && echo "  ⇒ 判定为 tectonic 缺失（预期内），继续" \
           || fail "run_all 失败且非 tectonic 缺失（见 $OUT/20_run_all.log）"; }
else
  fail "docker/paper/run_all.sh 不存在：无法复算论文数字（不静默跳过）"
fi

# ── S3：门禁 ────────────────────────────────────────────────────────────
log "S3 门禁检查"
"$PY" tools/paper_quality_gate_670c2.py > "$OUT/30_paper_gate.txt" 2>&1 \
  && { echo "  OK  paper_quality_gate"; tail -3 "$OUT/30_paper_gate.txt"; } \
  || { echo "  paper_quality_gate 退出非 0："; tail -20 "$OUT/30_paper_gate.txt";
       echo "  ⇒ 不阻断复现流程，但报告会标记 GATE=FAIL"; GATE_FAIL=1; }
GATE_FAIL="${GATE_FAIL:-0}"

"$PY" tools/fast_gate.py --tests tests/ > "$OUT/31_fast_gate.txt" 2>&1 \
  && { echo "  OK  fast_gate"; tail -3 "$OUT/31_fast_gate.txt"; } \
  || { echo "  fast_gate 退出非 0："; tail -20 "$OUT/31_fast_gate.txt";
       echo "  ⇒ 不阻断复现流程，但报告会标记 GATE=FAIL"; GATE_FAIL=1; }

# ── S4：验证报告 ────────────────────────────────────────────────────────
log "S4 生成验证报告"
END_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{
  echo "# 693-B2 · 复现验证报告"
  echo
  echo "- 开始：$START_TS"
  echo "- 结束：$END_TS"
  echo "- 输出目录：\`$OUT\`"
  echo "- Python：\`$($PY --version 2>&1)\`"
  echo "- OS：\`$(uname -s 2>/dev/null) $(uname -r 2>/dev/null)\`"
  echo
  echo "## 阶段结果"
  echo
  echo "| 阶段 | 内容 | 状态 | 证据文件 |"
  echo "|---|---|---|---|"
  echo "| S0 | 环境体检 | $( [ -f "$OUT/00_environment.txt" ] && echo done || echo skipped ) | \`$OUT/00_environment.txt\` |"
  echo "| S1 | 数据完整性 | $( [ -f "$OUT/10_sha256.txt" ] && echo done || echo 'script-only' ) | \`$OUT/10_*.txt\` |"
  echo "| S2 | 论文数字复算 | $( [ -f "$OUT/20_run_all.log" ] && echo done || echo missing ) | \`$OUT/20_run_all.log\` |"
  echo "| S3 | 门禁 | $( [ "$GATE_FAIL" = "0" ] && echo PASS || echo FAIL ) | \`$OUT/3*.txt\` |"
  echo
  echo "## 跳过/未执行项"
  echo
  if [ -s "$OUT/99_skipped.txt" ]; then
    sed 's/^/- /' "$OUT/99_skipped.txt"
  else
    echo "（无）"
  fi
  echo
  echo "## 诚实边界"
  echo
  echo "- 本脚本**未在 Docker 容器内实测**：693 执行环境未安装 Docker（693 红线 7）。"
  echo "- 本脚本**不重跑 \`detect()\`**：S2 复用 676h 已验证的 \`docker/paper/run_all.sh\` 口径，"
  echo "  从**已落盘**的 reveal/矩阵产物读算，符合 693 红线 8（科研强化阶段不跑新 detect）。"
  echo "- 若 S2 因 tectonic 缺失而在第 5 步退出非 0，属于预期内（容器镜像未装 tectonic）。"
} > "$OUT/99_reproduce_report.md"

echo
echo "=============================================="
echo " 复现完成。报告：$OUT/99_reproduce_report.md"
[ "$GATE_FAIL" = "0" ] || echo " ⚠ 门禁存在 FAIL，见报告"
echo "=============================================="
exit 0
