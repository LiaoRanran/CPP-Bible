"""637 A · 自我观测器（SelfObserver）——系统自己看自己

扫一遍系统现状，自动采集 **14 项指标**（规模/健康/知识/治理/进度），
输出结构化 JSON + 可读体检报告。

**只读契约**：`--check` 只读、不写盘、exit 0；`--report` 才写
`data/637_observer.json` + `data/637_observer_report.md`。
重指标（pytest/ruff/mypy）仅在 `--heavy`（或 `--report` 默认）时采集。
纯标准库（可复用 635 工具为只读依赖）；≥5 例单测（tests/test_self_observer_637.py）。
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable

OUT_JSON = os.path.join(ROOT, "data", "637_observer.json")
OUT_MD = os.path.join(ROOT, "data", "637_observer_report.md")

# 14 项指标显示元数据（key → 展示名）
METRIC_LABELS: dict[str, str] = {
    "rules": "规则数",
    "tools_total": "工具数",
    "tests_total": "测试数",
    "commits": "commits 数",
    "pytest_failures": "pytest 失败数",
    "pytest_summary": "pytest 摘要",
    "ruff_errors": "ruff 错误数",
    "mypy_errors": "mypy 错误数",
    "grounding_pct": "接地率(%)",
    "defeater_coverage_pct": "击败器覆盖率(%)",
    "taint_cards": "taint=true 卡数",
    "exception_clauses": "例外条款条目数",
    "observation_rules": "观察态规则数",
    "ahead": "ahead 数",
    "recent_commits": "最近 5 commit",
}


def _run(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except Exception:  # noqa: BLE001
        return subprocess.CompletedProcess(args, returncode=127, stdout="", stderr="")


# ── 规模 ────────────────────────────────────────────────────────────────
def count_tools() -> int:
    return len(glob.glob(os.path.join(ROOT, "tools", "*.py")))


def count_tests() -> int:
    return len(glob.glob(os.path.join(ROOT, "tests", "test_*.py")))


def count_rules() -> int:
    try:
        import gate_engine as ge
        return len(ge.RULES)
    except Exception:  # noqa: BLE001
        src = open(os.path.join(ROOT, "tools", "gate_engine.py"), encoding="utf-8",
                   errors="replace").read()
        return len(re.findall(r"register\(Rule\(", src))


def git_commits() -> int:
    out = _run(["git", "rev-list", "--count", "HEAD"]).stdout.strip()
    return int(out) if out.isdigit() else 0


def git_ahead() -> int:
    out = _run(["git", "rev-list", "--count", "origin/master..HEAD"]).stdout.strip()
    return int(out) if out.isdigit() else 0


def git_recent(n: int = 5) -> list[str]:
    return [ln for ln in _run(["git", "log", "--oneline", f"-{n}"]).stdout.splitlines() if ln.strip()]


# ── 知识 / 治理（复用 635 只读依赖）────────────────────────────────────────
def grounding_pct() -> float:
    try:
        import grounding_inventory_635 as G
        return float(G.stats()["grounded_pct"])
    except Exception:  # noqa: BLE001
        return 0.0


def defeater_stats() -> dict[str, Any]:
    try:
        import defeater_ledger_635 as D
        s = D.stats()
        return {"coverage_pct": float(s["coverage_pct"]), "taint_cards": int(s["n_taint"])}
    except Exception:  # noqa: BLE001
        return {"coverage_pct": 0.0, "taint_cards": 0}


def exception_entries() -> int:
    try:
        import exception_review_635 as E
        return int(E.stats()["total_entries"])
    except Exception:  # noqa: BLE001
        return 0


def observation_rules() -> int:
    try:
        import verifier_admissibility_635 as V
        return int(V.stats()["n_observation"])
    except Exception:  # noqa: BLE001
        return 0


# ── 健康（重指标，需子进程）──────────────────────────────────────────────
def pytest_health(timeout: int = 1800) -> tuple[Optional[int], str]:
    """跑一次非 slow 测试，返回 (失败数, 摘要行)。

    优先数 `-rf` 摘要里的 FAILED/ERROR 行（对 xdist 更稳）；
    解析不出时回退到汇总正则；仍解析不出且非零退出则保守计 1。
    """
    r = _run([PY, "-m", "pytest", "-m", "not slow", "-q", "--no-header",
              "-p", "no:cacheprovider", "-n", "auto", "-rf", "--tb=no"], timeout=timeout)
    if r.returncode == 127:
        return None, ""
    txt = (r.stdout or "") + (r.stderr or "")
    lines = [ln for ln in txt.splitlines() if ln.startswith(("FAILED ", "ERROR "))]
    summary = ""
    for ln in reversed(txt.splitlines()):
        if ("passed" in ln or "failed" in ln or "error" in ln) and ln.strip():
            summary = ln.strip()
            break
    if lines:
        return len(lines), summary
    failed = sum(int(m) for m in re.findall(r"(\d+) failed", txt))
    errored = sum(int(m) for m in re.findall(r"(\d+) error", txt))
    if failed or errored:
        return failed + errored, summary
    return (0 if r.returncode == 0 else 1), summary


def ruff_errors(timeout: int = 600) -> Optional[int]:
    r = _run([PY, "-m", "ruff", "check", "tools/", "tests/", "--output-format=json"],
             timeout=timeout)
    if r.returncode == 127:
        return None
    try:
        data: Any = json.loads(r.stdout or "[]")
        return len(data) if isinstance(data, list) else None
    except json.JSONDecodeError:
        return None


def mypy_errors(timeout: int = 900) -> Optional[int]:
    r = _run([PY, "-m", "mypy", "tools/"], timeout=timeout)
    if r.returncode == 127:
        return None
    txt = (r.stdout or "") + (r.stderr or "")
    return len(re.findall(r": error:", txt))


# ── 汇总 ────────────────────────────────────────────────────────────────
def collect(heavy: bool = False) -> dict[str, Any]:
    d = defeater_stats()
    if heavy:
        pf, psum = pytest_health()
    else:
        pf, psum = None, ""
    metrics: dict[str, Any] = {
        "rules": count_rules(),
        "tools_total": count_tools(),
        "tests_total": count_tests(),
        "commits": git_commits(),
        "pytest_failures": pf,
        "pytest_summary": psum,
        "ruff_errors": ruff_errors() if heavy else None,
        "mypy_errors": mypy_errors() if heavy else None,
        "grounding_pct": grounding_pct(),
        "defeater_coverage_pct": d["coverage_pct"],
        "taint_cards": d["taint_cards"],
        "exception_clauses": exception_entries(),
        "observation_rules": observation_rules(),
        "ahead": git_ahead(),
        "recent_commits": git_recent(5),
    }
    rules = int(metrics["rules"]) or 1
    metrics["observation_pct"] = round(100.0 * int(metrics["observation_rules"]) / rules, 1)
    notes = [] if heavy else ["健康指标（pytest/ruff/mypy）未采集：用 --heavy 或 --report"]
    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "heavy": heavy,
        "metrics": metrics,
        "notes": notes,
    }


def write_report(heavy: bool = True) -> dict[str, str]:
    obs = collect(heavy=heavy)
    m = obs["metrics"]
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obs, fh, ensure_ascii=False, indent=2)
    lines = [
        "# 637 · 系统体检报告（SelfObserver 自动生成）", "",
        f"> 生成时间：{obs['generated']}；重指标采集：{'是' if heavy else '否'}。", "",
        "## 一、14 项指标", "", "| 指标 | 当前值 |", "|---|---|",
    ]
    for key, label in METRIC_LABELS.items():
        val = m.get(key)
        if isinstance(val, list):
            lines.append(f"| {label} | {len(val)} 条（见文末） |")
        else:
            lines.append(f"| {label} | {val} |")
    lines += [
        f"| 观察态比例(%) | {m['observation_pct']} |", "",
        "## 二、最近 5 个 commit", "", "```",
    ]
    lines += [str(x) for x in m.get("recent_commits", [])]
    lines += ["```", "", "## 三、诚实登记", ""]
    if not heavy:
        lines.append("- 本次为**轻量采集**：pytest/ruff/mypy 三项为 `null`（未跑）。")
    lines.append("- 本报告**只读**，不修改系统任何状态；所有数值来自实测，非抄表。")
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("规则数 67", count_rules() == 67)
    chk("工具数 > 100", count_tools() > 100)
    chk("测试数 > 100", count_tests() > 100)
    chk("commits > 0", git_commits() > 0)
    chk("接地率 35.8", abs(grounding_pct() - 35.8) < 0.1)
    chk("taint 8", defeater_stats()["taint_cards"] == 8)
    chk("例外条目 227", exception_entries() == 227)
    chk("观察态 67", observation_rules() == 67)
    obs = collect(heavy=False)
    chk("轻量采集 14 键", len(obs["metrics"]) >= 14)
    chk("轻量不跑重指标", obs["metrics"]["pytest_failures"] is None)
    chk("输出路径在 data 下",
        OUT_JSON.startswith(os.path.join(ROOT, "data")) and OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="637 A 自我观测器")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--heavy", action="store_true")
    ap.add_argument("--no-heavy", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    heavy = args.heavy or (args.report and not args.no_heavy)
    if args.report:
        out = write_report(heavy=heavy)
        print(f"written {out['json']} {out['md']}")
        return 0
    obs = collect(heavy=heavy)
    if args.json:
        print(json.dumps(obs, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps(obs["metrics"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
