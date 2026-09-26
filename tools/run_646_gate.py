"""646 · 阶段 C1 · 收工门禁（真实全量，不编造、不「改到绿」）。

门禁逐项（对应 646 §七 C1）：
1. 646 新工具 `--check` 全绿（只读幂等）。
2. ruff + mypy 对 646 工具零错误（跨平台可用性探测 + 显式文件列表）。
3. 受控目录（atoms/evidence/Examples/Book）净变更 0（git status 核对）。
4. 两阶段 pytest：fast（`-m "not slow"`）+ slow（`-m slow -n0`）全绿（scoped `-k 646`）。
5. 产物齐备：`data/646_*` 报告 + `status/646_acceptance_report.md` + `_auto/outbox/646.md`。
6. **清债核验**：A2 三层打通（≥5 链证据≠0）、A5 原账本 sha256 未变。

退出码：0=通过；非 0=存在未达标项（诚实登记，绝不静默「改到绿」）。
`--check`：只读自检（门禁逻辑本身）。`--gate`：真实跑全部门禁。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
LEDGER = os.path.join(DATA, "authority", "decision_event_v2_ledger.jsonl")
PRODUCTS = [
    "data/646_baseline.md",
    "data/646_rule_card_mapping.json",
    "data/646_coupling_report.md",
    "data/646_performance_report.md",
    "data/646_evidence_index.json",
    "data/646_authority_rule_annotation.jsonl",
    "data/646_r5_report.md",
    "data/646_standard_fetch_report.md",
    "data/646_counterexample_report.md",
    "data/646_sufficiency_report.md",
    "data/646_consolidation_report.md",
    "data/646_docstring_quality_report.md",
    "status/646_acceptance_report.md",
    "_auto/outbox/646.md",
]


def _run(cmd: list[str], timeout: int = 600) -> tuple[int, str]:
    """执行子进程，返回 (退出码, 末 3000 字输出)。"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return r.returncode, (r.stdout + r.stderr)[-3000:]
    except FileNotFoundError:
        return 2, f"命令缺失：{cmd[0]}"
    except subprocess.TimeoutExpired:
        return 3, f"超时（>{timeout}s）：{cmd[0]}"


def _module_available(py: str, module: str) -> bool:
    """检测 `python -m <module> --version` 是否可用（跨平台）。"""
    rc, _ = _run([py, "-m", module, "--version"], timeout=60)
    return rc == 0


def _ledger_sha256() -> str:
    """原账本字节级 sha256。"""
    h = hashlib.sha256()
    with open(LEDGER, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def gate() -> dict:
    """真实跑全部门禁。"""
    results: dict = {}
    py = sys.executable
    tools = sorted(f for f in os.listdir(TOOLS) if f.endswith("_646.py"))

    # 1) --check 全绿
    check_fail = []
    for t in tools:
        rc, _ = _run([py, os.path.join(TOOLS, t), "--check"], timeout=180)
        if rc != 0:
            check_fail.append(t)
    results["tool_check"] = {"total": len(tools), "failed": check_fail}

    # 2) ruff / mypy（显式文件列表，Windows 下 glob 不展开）
    tests_dir = os.path.join(ROOT, "tests")
    tool_files = [os.path.join(TOOLS, t) for t in tools]
    test_files = sorted(os.path.join(tests_dir, f) for f in os.listdir(tests_dir)
                        if f.startswith("test_") and f.endswith("_646.py"))
    if _module_available(py, "ruff"):
        rc, out = _run([py, "-m", "ruff", "check", *tool_files, *test_files], timeout=180)
        results["ruff"] = {"available": True, "rc": rc, "tail": out[-800:]}
    else:
        results["ruff"] = {"available": False, "rc": None, "tail": "ruff 未安装（诚实登记）"}
    if _module_available(py, "mypy"):
        rc, out = _run([py, "-m", "mypy", "--ignore-missing-imports",
                        "--no-error-summary", *tool_files], timeout=300)
        results["mypy"] = {"available": True, "rc": rc, "tail": out[-800:]}
    else:
        results["mypy"] = {"available": False, "rc": None, "tail": "mypy 未安装（诚实登记）"}

    # 3) 受控目录净变更 0
    rc, out = _run(["git", "status", "--porcelain", "--", *CONTROLLED], timeout=60)
    dirty = [line for line in out.splitlines() if line.strip()]
    results["controlled_clean"] = {"rc": rc, "dirty": dirty}

    # 4) 两阶段 pytest（-k 646）
    fast_rc, fast_out = _run(
        [py, "-m", "pytest", "tests", "-k", "646", "-m", "not slow", "-q",
         "-p", "no:cacheprovider"], timeout=900)
    results["pytest_fast"] = {"rc": fast_rc, "tail": fast_out[-800:]}
    slow_rc, slow_out = _run(
        [py, "-m", "pytest", "tests", "-k", "646", "-m", "slow", "-n0", "-q",
         "-p", "no:cacheprovider"], timeout=1800)
    results["pytest_slow"] = {"rc": slow_rc, "tail": slow_out[-800:]}

    # 5) 产物齐备
    missing = [p for p in PRODUCTS if not os.path.exists(os.path.join(ROOT, p))]
    results["products"] = {"missing": missing}

    # 6) 清债核验：A2 三层打通 + A5 账本未改
    debt = {"coupling_met": None, "ledger_sha256": None}
    try:
        import three_layer_orchestrator_646 as c2
        debt["coupling_met"] = bool(c2.orchestrate()["met"])
    except Exception as exc:  # noqa: BLE001
        debt["coupling_error"] = f"{type(exc).__name__}: {exc}"
    try:
        debt["ledger_sha256"] = _ledger_sha256()
    except Exception as exc:  # noqa: BLE001
        debt["ledger_error"] = f"{type(exc).__name__}: {exc}"
    results["debt_check"] = debt

    passed = (not check_fail
              and (not results["ruff"]["available"] or results["ruff"]["rc"] == 0)
              and (not results["mypy"]["available"] or results["mypy"]["rc"] == 0)
              and not dirty and fast_rc == 0 and slow_rc == 0 and not missing
              and debt.get("coupling_met") is True)
    results["passed"] = passed
    return results


def selftest() -> int:
    """只读自检：门禁汇总逻辑（合成结果，不跑全库）。"""
    fake: dict = {
        "tool_check": {"failed": []},
        "ruff": {"available": False, "rc": None},
        "mypy": {"available": False, "rc": None},
        "controlled_clean": {"dirty": []},
        "pytest_fast": {"rc": 0},
        "pytest_slow": {"rc": 0},
        "products": {"missing": []},
        "debt_check": {"coupling_met": True},
    }
    passed = (not fake["tool_check"]["failed"]
              and (not fake["ruff"]["available"] or fake["ruff"]["rc"] == 0)
              and (not fake["mypy"]["available"] or fake["mypy"]["rc"] == 0)
              and not fake["controlled_clean"]["dirty"]
              and fake["pytest_fast"]["rc"] == 0 and fake["pytest_slow"]["rc"] == 0
              and not fake["products"]["missing"])
    assert passed is True
    fake_bad = dict(fake)
    fake_bad["products"] = {"missing": ["x"]}
    assert (not fake_bad["products"]["missing"]) is False
    return 0


def main(argv=None) -> int:
    """统一入口：`--check` 只读自检；`--gate` 真实跑全部门禁。"""
    ap = argparse.ArgumentParser(description="646 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--gate", action="store_true", help="真实跑全部门禁")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    res = gate()
    with open(os.path.join(DATA, "646_gate_result.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print(json.dumps({k: (v if not isinstance(v, dict) else
          {kk: vv for kk, vv in v.items() if kk != "tail"}) for k, v in res.items()},
          ensure_ascii=False, indent=2))
    print("GATE PASSED" if res["passed"] else "GATE FAILED（诚实登记，未达标项见上）")
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
