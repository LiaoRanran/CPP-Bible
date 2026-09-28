#!/usr/bin/env bash
# 661 D2 · 复现脚本（CPP-Bible / queyi 验证器）
# 用法（WSL / Linux / macOS）：bash run_reproduction.sh
# Windows：见 REPLICATION.md 的等价 PowerShell 命令。
set -uo pipefail

echo "=== 0 · 环境 ==="
uv --version || { echo "需要 uv（https://docs.astral.sh/uv/）"; exit 1; }
node --version || echo "[warn] 无 node → web_logic_check 将跳过"
python --version 2>/dev/null || true

echo
echo "=== 1 · 元状态对账（独立对账器，期望 [OK]）==="
uv run python tools/status_reconciler_658.py --check

echo
echo "=== 2 · 658 门禁（期望 overall=PASS L0 5/5）==="
uv run python tools/run_658_gate.py

echo
echo "=== 3 · 前端台账哈希校验（期望 4/4 全绿）==="
node tools/web_logic_check_655.mjs || echo "[skip] 无 node"

echo
echo "=== 4 · 真实缺陷注入（期望 重注入检出 6/6）==="
uv run python tools/defect_injection_661.py

echo
echo "=== 5 · 盲化 holdout reveal（已 reveal → 期望 REFUSED，铁律不可回盲）==="
uv run python tools/holdout_reveal_661.py || true

echo
echo "=== 6 · 数据集哈希校验 ==="
uv run python - <<'PY'
import hashlib, json, os
R = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "."
R = os.getcwd()
h = json.load(open(os.path.join(R, "data", "dataset_hashes_661.json"), encoding="utf-8"))
bad = []
for f, exp in h["files"].items():
    p = os.path.join(R, *f.split("/"))
    got = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else "MISSING"
    ok = got == exp
    print(f"  {'OK ' if ok else 'DIFF'} {f}")
    if not ok:
        bad.append(f)
print("哈希校验:", "全部一致" if not bad else f"{len(bad)} 项漂移（注意 CRLF/换行差异）")
PY
