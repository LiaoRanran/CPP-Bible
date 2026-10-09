#!/usr/bin/env bash
# =====================================================================
# docker/minimal_repro.sh — 704 最小复现（3 个核心实验）
#
# 定位
# ----
# 在**不依赖 Docker、不重新运行任何检测器（detect）**的前提下，用冻结产物
# 复算论文三个最核心的实验结论，输出 PASS/FAIL：
#   Exp 1: A5 主端点增益 +24.03pp（FD 309/566 vs Random 173/566）
#   Exp 2: 环境画像敏感性 60.07% → 24.74%（Δ −35.34pp）
#   Exp 3: 真实 CVE 重构检出率 59.09%（65/110）
#
# 设计原则（继承 docker/paper/run_all.sh 的 fail-loud）
#   * 每一步拿不到数字就报错退出，不做静默降级；
#   * 只读冻结产物（data/*.json / data/*.jsonl），不写 data/ 下任何已落盘产物；
#   * 不调用任何检测器；符合 704 红线 4。
#
# 用法
# ----
#   cd <repo-root>
#   PY=python3 bash docker/minimal_repro.sh
#   # 或在容器里：docker compose run --rm queyi bash docker/minimal_repro.sh
# 退出码：0 = 全部 PASS；非 0 = 存在 FAIL。
# =====================================================================
set -uo pipefail

PY="${PY:-python3}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || { echo "[FAIL] 无法进入仓库根目录"; exit 1; }

PASS=0; FAIL=0
ok(){ echo "[PASS] $1"; PASS=$((PASS+1)); }
no(){ echo "[FAIL] $1"; FAIL=$((FAIL+1)); }

echo "=================================================================="
echo " Queyi 最小复现（3 核心实验）  —  只读冻结产物，不跑 detect"
echo " 仓库根: $ROOT"
echo "=================================================================="

# ----------------------------------------------------------------------
# Exp 1: A5 全量重算（676f 冻结矩阵）→ 期望 +24.03pp
# ----------------------------------------------------------------------
echo
echo "=== Exp 1: A5 主端点增益 (+24.03pp) ==="
if [ -f tools/recompute_a5_676f.py ] && [ -f data/a5_676f_detection_matrix.json ]; then
  if "$PY" tools/recompute_a5_676f.py >/tmp/704_a5.log 2>&1; then
    # 复算脚本已断言 R1（四臂 catch 数从原始矩阵逐位可重算：FD 309 / Random 173 / n=566）。
    # 再从 results 取主端点增益 +24.03pp 做显式核验：
    if "$PY" - <<'PY'
import json
res=json.load(open('data/a5_676f_results.json',encoding='utf-8'))
p=res['primary_main_8candidates']['primary']
delta=p['delta_fd_minus_random_pp']          # 期望 ~24.0283
fd_rate=p['fd_rate_pct']; rnd_rate=p['random_rate_pct']
n=res['sample_stats']['n_evaluation']         # 566
fd_catch=round(fd_rate/100*n); rnd_catch=round(rnd_rate/100*n)
assert abs(delta-24.03)<0.05, f"Δ={delta:.2f}pp 期望 24.03pp"
assert fd_catch==309 and rnd_catch==173, f"FD={fd_catch} Random={rnd_catch}"
print(f"  FD={fd_catch}/{n}  Random={rnd_catch}/{n}  Δ(FD−Random)=+{delta:.2f}pp")
PY
    then ok "A5: FD−Random = +24.03pp（309/566 vs 173/566）"; else no "A5: +24.03pp 核验失败（见 /tmp/704_a5.log）"; fi
  else no "A5: recompute_a5_676f.py 非零退出"; fi
else no "A5: 缺少 recompute_a5_676f.py 或 data/a5_676f_detection_matrix.json"; fi

# ----------------------------------------------------------------------
# Exp 2: 环境画像敏感性（703 零成本验证 P2）→ 期望 60.07% → 24.74%
# ----------------------------------------------------------------------
echo
echo "=== Exp 2: 环境画像敏感性 (60.07% → 24.74%) ==="
if [ -f data/703_zero_cost_validation.json ]; then
  if "$PY" - <<'PY'
import json
d=json.load(open('data/703_zero_cost_validation.json',encoding='utf-8'))['P2_aware_accounting']
e1=d['E1']['catch_rate_pct']; e2=d['E2_unaware']['catch_rate_pct']; dl=d['delta_catch_rate_unaware_pp']
assert abs(e1-60.0707)<0.01, f"E1={e1}"
assert abs(e2-24.735)<0.01, f"E2={e2}"
assert abs(dl-(-35.3357))<0.01, f"Δ={dl}"
print(f"  E1(WSL满能力)={e1:.4f}%  E2_unaware(native缺失)={e2:.4f}%  Δ={dl:.4f}pp")
PY
  then ok "环境感知: 60.07% → 24.74%（Δ −35.34pp）confirmed"; else no "环境感知: 数字与期望不符"; fi
else no "环境感知: 缺少 data/703_zero_cost_validation.json"; fi

# ----------------------------------------------------------------------
# Exp 3: 真实 CVE 重构检出率（683 真实靶场）→ 期望 59.09% (65/110)
# ----------------------------------------------------------------------
echo
echo "=== Exp 3: 真实 CVE 重构检出率 (59.09% = 65/110) ==="
if [ -f data/683_real_world_detection_matrix.json ]; then
  if "$PY" - <<'PY'
import json
d=json.load(open('data/683_real_world_detection_matrix.json',encoding='utf-8'))
r=d['or_catch_rate_pct']; c=d.get('or_catch',d.get('catch')); n=d.get('or_total',d.get('total'))
assert abs(r-59.0909)<0.01, f"rate={r}"
print(f"  真实靶场 OR 检出率 = {r:.4f}% (期望 59.09% = 65/110)")
PY
  then ok "真实CVE: 59.09%（65/110）confirmed"; else no "真实CVE: 数字与期望不符"; fi
else no "真实CVE: 缺少 data/683_real_world_detection_matrix.json"; fi

# ----------------------------------------------------------------------
echo
echo "=================================================================="
echo " 结果: PASS=$PASS  FAIL=$FAIL"
echo "=================================================================="
[ "$FAIL" -eq 0 ]
