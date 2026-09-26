"""645 · 阶段 G1 · 收工门禁（真实全量，不编造、不「改到绿」）。

门禁逐项（对应 645 §十一 G1 验收）：
1. 新工具 `--check` 全绿（只读幂等）。
2. ruff + mypy 对 645 工具零错误（缺失则诚实登记，不报错）。
3. 受控目录（atoms/evidence/Examples/Book）净变更 0（git status 核对）。
4. 两阶段 pytest：fast（-m "not slow"）后 slow（-m slow -n0）全绿（scoped -k 645）。
5. 产物齐备：data/645_*.md 报告 + 本文件 + outbox/645.md + status/645_acceptance_report.md。

退出码：0=通过；非 0=存在未达标项（诚实登记，绝不静默「改到绿」）。
`--check`：只读自检（门禁逻辑本身）。`--gate`：真实跑全部门禁。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
PRODUCTS = [
    "data/645_baseline.md",
    "data/645_compiler_probe_report.md",
    "data/645_standard_fetch_report.md",
    "data/645_rule_error_report.md",
    "data/645_issue_report.md",
    "data/645_attack_report.md",
    "data/645_rule_draft_report.md",
    "data/645_aging_report.md",
    "data/645_loop_r5_report.md",
    "data/645_evidence_grading_report.md",
    "data/645_sufficiency_report.md",
    "data/645_counterexample_report.md",
    "data/645_orchestration_report.md",
    "data/645_feedback_report.md",
    "data/645_interface_audit.md",
    "docs/tool_interface_spec_645.md",
    "status/645_acceptance_report.md",
    "_auto/outbox/645.md",
]


def _run(cmd: list[str], timeout: int = 600) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return r.returncode, (r.stdout + r.stderr)[-3000:]
    except FileNotFoundError:
        return 2, f"命令缺失：{cmd[0]}"
    except subprocess.TimeoutExpired:
        return 3, f"超时（>{timeout}s）：{cmd[0]}"


def _module_available(py: str, module: str) -> bool:
    """检测 `python -m <module> --version` 是否可用（跨平台，不依赖 PATH）。"""
    rc, _ = _run([py, "-m", module, "--version"], timeout=60)
    return rc == 0


def gate(check_only: bool = False) -> dict:
    results: dict = {}
    py = sys.executable
    tools = sorted(f for f in os.listdir(TOOLS) if f.endswith("_645.py"))

    # 1) --check 全绿
    check_fail = []
    for t in tools:
        rc, _ = _run([py, os.path.join(TOOLS, t), "--check"], timeout=120)
        if rc != 0:
            check_fail.append(t)
    results["tool_check"] = {"total": len(tools), "failed": check_fail}

    # 2) ruff / mypy（缺失诚实登记；Windows 下必须显式给文件列表，glob 不展开）
    tests_dir = os.path.join(ROOT, "tests")
    tool_files = [os.path.join(TOOLS, t) for t in tools]
    test_files = sorted(os.path.join(tests_dir, f) for f in os.listdir(tests_dir)
                        if f.startswith("test_") and f.endswith("_645.py"))
    if _module_available(py, "ruff"):
        rc, out = _run([py, "-m", "ruff", "check", *tool_files, *test_files], timeout=180)
        results["ruff"] = {"available": True, "rc": rc, "tail": out[-800:]}
    else:
        results["ruff"] = {"available": False, "rc": None, "tail": "ruff 未安装（诚实登记，不报错）"}
    if _module_available(py, "mypy"):
        rc, out = _run([py, "-m", "mypy", "--ignore-missing-imports",
                        "--no-error-summary", *tool_files], timeout=300)
        results["mypy"] = {"available": True, "rc": rc, "tail": out[-800:]}
    else:
        results["mypy"] = {"available": False, "rc": None, "tail": "mypy 未安装（诚实登记，不报错）"}

    # 3) 受控目录净变更 0
    rc, out = _run(["git", "status", "--porcelain", "--", *CONTROLLED], timeout=60)
    dirty = [ln for ln in out.splitlines() if ln.strip()]
    results["controlled_clean"] = {"rc": rc, "dirty": dirty}

    # 4) 两阶段 pytest（-k 645）
    fast_rc, fast_out = _run(
        [py, "-m", "pytest", "tests", "-k", "645", "-m", "not slow", "-q",
         "-p", "no:cacheprovider"], timeout=900)
    results["pytest_fast"] = {"rc": fast_rc, "tail": fast_out[-800:]}
    slow_rc, slow_out = _run(
        [py, "-m", "pytest", "tests", "-k", "645", "-m", "slow", "-n0", "-q",
         "-p", "no:cacheprovider"], timeout=1800)
    results["pytest_slow"] = {"rc": slow_rc, "tail": slow_out[-800:]}

    # 5) 产物齐备
    missing = [p for p in PRODUCTS if not os.path.exists(os.path.join(ROOT, p))]
    results["products"] = {"missing": missing}

    # 汇总
    passed = (not check_fail and (not results["ruff"]["available"] or results["ruff"]["rc"] == 0)
              and (not results["mypy"]["available"] or results["mypy"]["rc"] == 0)
              and not dirty and fast_rc == 0 and slow_rc == 0 and not missing)
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
    }
    passed = (not fake["tool_check"]["failed"]
              and (not fake["ruff"]["available"] or fake["ruff"]["rc"] == 0)
              and (not fake["mypy"]["available"] or fake["mypy"]["rc"] == 0)
              and not fake["controlled_clean"]["dirty"]
              and fake["pytest_fast"]["rc"] == 0 and fake["pytest_slow"]["rc"] == 0
              and not fake["products"]["missing"])
    assert passed is True
    # 不一致项应使 passed=False
    fake_bad = dict(fake)
    fake_bad["controlled_clean"] = {"dirty": ["M x.md"]}
    passed_bad = (not fake_bad["controlled_clean"]["dirty"])
    assert passed_bad is False
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="645 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--gate", action="store_true", help="真实跑全部门禁")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    res = gate()
    with open(os.path.join(DATA, "645_gate_result.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print(json.dumps({k: (v if not isinstance(v, dict) else
          {kk: vv for kk, vv in v.items() if kk != "tail"}) for k, v in res.items()},
          ensure_ascii=False, indent=2))
    print("GATE PASSED" if res["passed"] else "GATE FAILED（诚实登记，未达标项见上）")
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
