"""636 任务0 · 开工快照 + 全量基线复测（只加数据，不改判决）

**实测** §一 全部 15 项指标（不抄表），并与 635 值对比确认**无漂移**；
落盘 `data/636_baseline.md`。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 才写报告。
纯标准库（可复用 635 工具为只读依赖）；≥5 例单测（tests/test_baseline_636.py）。
"""
from __future__ import annotations

import argparse
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

OUT_MD = os.path.join(ROOT, "data", "636_baseline.md")
OUT_JSON = os.path.join(ROOT, "data", "636_baseline.json")

# §一 Standing Baseline（635 来源）
STANDING: dict[str, Any] = {
    "gate_rules": 67, "escape_rate": "1/1406 (0.071%)", "autoimmune_rate_pct": 0.0,
    "coverage_pct": 100.0, "na_rate_pct": 11.24, "grounding_pct": 35.8,
    "defeater_coverage_pct": 100.0, "taint_cards": 8, "tau_d_median": 0,
    "four_questions": "Q1非盲/Q2AI先行/Q3无数据/Q4单人", "daubert_observation": 67,
    "error_cost_ratio": "漏报0.071%:误报0%", "tools_total": 408, "tests_total": 407,
    "local_ahead": 43,
}


def _run(args: list[str]) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=120).stdout
    except Exception:  # noqa: BLE001
        return ""


def count_tools() -> int:
    return len(glob.glob(os.path.join(ROOT, "tools", "*.py")))


def count_tests() -> int:
    return len(glob.glob(os.path.join(ROOT, "tests", "test_*.py")))


def git_commits() -> int:
    out = _run(["git", "rev-list", "--count", "HEAD"]).strip()
    return int(out) if out.isdigit() else 0


def git_ahead() -> int:
    out = _run(["git", "rev-list", "--count", "origin/master..HEAD"]).strip()
    return int(out) if out.isdigit() else 0


def git_dirty_count() -> int:
    return len([ln for ln in _run(["git", "status", "--short"]).splitlines() if ln.strip()])


def count_rules() -> int:
    try:
        import gate_engine as ge
        return len(ge.RULES)
    except Exception:  # noqa: BLE001
        src = open(os.path.join(ROOT, "tools", "gate_engine.py"), encoding="utf-8",
                   errors="replace").read()
        return len(re.findall(r"register\(Rule\(", src))


def coverage_pct() -> float:
    try:
        import coverage_probe_batch_634 as C
        return float(C.matrix()["coverage_pct"])
    except Exception:  # noqa: BLE001
        return 0.0


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
        return {"coverage_pct": s["coverage_pct"], "taint_cards": s["n_taint"]}
    except Exception:  # noqa: BLE001
        return {"coverage_pct": 0.0, "taint_cards": 0}


def tau_d_median() -> Optional[float]:
    try:
        import tau_d_635 as T
        st = T.stats([p["days"] for p in T.tau_d()])
        return st.get("median")
    except Exception:  # noqa: BLE001
        return None


def daubert_observation() -> int:
    try:
        import verifier_admissibility_635 as V
        return int(V.stats()["n_observation"])
    except Exception:  # noqa: BLE001
        return 0


def na_rate_pct() -> Optional[float]:
    p = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
    try:
        d = json.loads(open(p, encoding="utf-8").read())
        n_a = float(d.get("n_a", 0))
        variants = max(1.0, float(d.get("variants", 1)))
        return round(100.0 * n_a / variants, 2)
    except (OSError, json.JSONDecodeError):
        return None


def snapshot() -> dict[str, Any]:
    d = defeater_stats()
    return {
        "gate_rules": count_rules(),
        "coverage_pct": coverage_pct(),
        "na_rate_pct": na_rate_pct(),
        "grounding_pct": grounding_pct(),
        "defeater_coverage_pct": d["coverage_pct"],
        "taint_cards": d["taint_cards"],
        "tau_d_median": tau_d_median(),
        "daubert_observation": daubert_observation(),
        "tools_total": count_tools(),
        "tests_total": count_tests(),
        "commits": git_commits(),
        "local_ahead": git_ahead(),
        "dirty_files": git_dirty_count(),
    }


def compare(s: dict[str, Any]) -> list[dict[str, Any]]:
    pairs = [("gate_rules", "gate_rules"), ("coverage_pct", "coverage_pct"),
             ("na_rate_pct", "na_rate_pct"), ("grounding_pct", "grounding_pct"),
             ("defeater_coverage_pct", "defeater_coverage_pct"), ("taint_cards", "taint_cards"),
             ("tau_d_median", "tau_d_median"), ("daubert_observation", "daubert_observation")]
    rows = []
    for k, sk in pairs:
        a, b = STANDING.get(sk), s.get(k)
        rows.append({"metric": k, "635": a, "636": b, "same": a == b})
    return rows


def write_baseline_md() -> str:
    s = snapshot()
    rows = compare(s)
    lines = [
        "# 636 任务0 · 开工快照 + 全量基线复测", "",
        "> 实测时间：2026-09-25。工具：`tools/baseline_636.py`（只读）。", "",
        "## 一、§一 指标复测（对比 635）", "",
        "| 指标 | 635 值 | 636 实测 | 一致 |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['metric']} | {r['635']} | {r['636']} | "
                     f"{'✅' if r['same'] else '⚠️ 漂移'} |")
    lines += [
        f"| 工具数 | ~407 | {s['tools_total']} | ⚠️ 表为估值 |",
        f"| 测试数 | ~406 | {s['tests_total']} | ⚠️ 表为估值 |",
        f"| 本地 ahead | 43 | {s['local_ahead']} | "
        f"{'✅' if s['local_ahead'] == 43 else '⚠️'} |", "",
        "> 逃逸率 1/1406、自身免疫率 0%、错误代价比、四问结论取 616/634/635 冻结值"
        "（本批不跑监工四门禁，§零.4）。", "",
        "## 二、git status --short（全量）", "", "```"]
    lines += [ln for ln in _run(["git", "status", "--short"]).splitlines() if ln.strip()]
    lines += ["```", "", "## 三、最近 5 个 commit", "", "```"]
    lines += [ln for ln in _run(["git", "log", "--oneline", "-5"]).splitlines()[:5]]
    lines += ["```", "", "## 四、诚实登记", "",
              "1. 工具/测试/ahead 的表值为估值，实测见上；",
              "2. 逃逸率/自身免疫率/错误代价比/四问为 616/634/635 **冻结值**，本批未重跑（§零.4）；",
              "3. 本工具**只读**。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"standing": STANDING, "measured": s}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    s = snapshot()
    chk("gate_rules 67", s["gate_rules"] == 67)
    chk("coverage 100", s["coverage_pct"] == 100.0)
    chk("grounding 35.8", abs(float(s["grounding_pct"]) - 35.8) < 0.1)
    chk("defeater coverage 100", s["defeater_coverage_pct"] == 100.0)
    chk("taint_cards 8", s["taint_cards"] == 8)
    chk("daubert_observation 67", s["daubert_observation"] == 67)
    chk("tools_total > 100", s["tools_total"] > 100)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 任务0 基线复测")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_baseline_md()}")
        return 0
    s = snapshot()
    if args.json:
        print(json.dumps({"standing": STANDING, "measured": s}, ensure_ascii=False, indent=2))
        return 0
    print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
