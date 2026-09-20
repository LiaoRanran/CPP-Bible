"""611 收工门禁（Z1）。

逐条跑 611 各新工具的 `--check`（锁死冻结数据与图结构的已知数字）+ 全图 `--check` +
`metrics_collector`（确认 metrics_611 不崩）+ `tool_integrity --check` + 611 回归测试。

⚠️ 按 611 基线 §9 行 3 的**禁止**纪律：本门禁**不跑** `gate_engine --check` / `poison_drill` /
`replay --check`（那些是监工的事，且会改基线）；只跑 611 自己的自检 + 工具完整性自检 + 测试。

用法：`python tools/run_611_gate.py`（exit 0 = 全绿 / 2 = 有红）。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

PY = sys.executable
TOOLS = ["argument_graph_analysis", "bridge_edge_candidates", "fragmentation_repair_analysis",
         "out_mis_review_support", "liveness_completion_plan", "oracle_verification_plan",
         "human_review_quality_deepen", "defense_chain_deepen"]
CHECKS: list[tuple[str, str]] = []


def _run(modname: str, args: list[str]) -> int:
    try:
        mod = __import__(modname)
        return int(mod.main(args))
    except Exception as exc:                       # noqa: BLE001
        print(f"[gate] ❌ {modname} {' '.join(args)} 抛异常：{type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2


def main(argv: list[str] | None = None) -> int:
    print("=" * 64)
    print("611 收工门禁 · 开始")
    print("=" * 64)
    rc = 0

    # 1) 各新工具 + C1 的 --check（锁死已知数字）
    for t in TOOLS:
        code = _run(t, ["--check"])
        tag = "✓" if code == 0 else "❌"
        print(f"  {tag} {t} --check")
        if code != 0:
            rc = 2
            CHECKS.append((t, "FAIL"))

    # 2) metrics_collector（确认 metrics_611 不崩 + 含 611 嵌套）
    try:
        import metrics_collector as mc  # noqa: E402
        snap = mc.collect(with_heavy=False)
        ok = "metrics_611" in snap and isinstance(snap.get("metrics_611"), dict)
        print(f"  {'✓' if ok else '❌'} metrics_collector（含 metrics_611 嵌套）")
        if not ok:
            rc = 2
    except Exception as exc:                       # noqa: BLE001
        print(f"[gate] ❌ metrics_collector 抛异常：{type(exc).__name__}: {exc}", file=sys.stderr)
        rc = 2

    # 3) tool_integrity --check（工具完整性自检；未改 CORE 工具应为绿）
    code = _run("tool_integrity", ["--check"])
    print(f"  {'✓' if code == 0 else '❌'} tool_integrity --check")
    if code != 0:
        rc = 2

    # 4) 611 回归测试
    proc = subprocess.run([PY, "-m", "pytest", "tests/test_611_tools.py", "-q"],
                          cwd=str(ROOT), capture_output=True, text=True)
    passed = proc.returncode == 0
    print(f"  {'✓' if passed else '❌'} pytest tests/test_611_tools.py（returncode={proc.returncode}）")
    if not passed:
        rc = 2
        tail = "\n".join(proc.stdout.strip().splitlines()[-12:])
        print(tail, file=sys.stderr)

    print("=" * 64)
    if rc == 0:
        print("611 收工门禁：全绿 ✓")
    else:
        print("611 收工门禁：有红 ❌（见上）")
    print("=" * 64)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
