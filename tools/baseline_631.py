"""631 任务0 · 开工基线台账（纯标准库，只读）

1. 把 §一 standing baseline 全部录入 `data/631_baseline.md`；
2. 额外测量：工具/测试文件计数、git 事实（HEAD/远端/ahead/behind）、
   **CI pytest 红的失败用例列表**（读已落盘的原始输出 `data/ci_pytest_raw_631.txt`，
   不重跑全量）；
3. 交叉核对：只读 import 630 的基线/分类/门禁模块，把「任务书数字 vs 实测」摆出来
   （§零.10：不符只标注，不回写基线）；
4. `--check`：只读，exit 0。

**不改任何基线数字**；原始输出缺失时在报告里显式标注"未采集"。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "631_baseline.md")
OUT_JSON = os.path.join(ROOT, "data", "631_baseline.json")
RAW = os.path.join(ROOT, "data", "ci_pytest_raw_631.txt")

# §一 standing baseline（631 开工冻结，来源=任务书 §一）
STANDING: dict[str, Any] = {
    "gate_rules": 67,
    "gate_hits": 191,
    "gate_block": 0,
    "gate_warn": 186,
    "gate_advice": 5,
    "poison": "124/124",
    "replay": "confirm=56 refute=0 infra=0",
    "tool_integrity": "22 尺子",
    "w2": "IN114/OUT7/UNDEC0",
    "pck": "83 张，authorized 27/83",
    "authority_v2_ledger": 452,
    "touched": "37/67",
    "escape": "1/1406（CS 0.9062%）",
    "autoimmune": "100%（23/23，132 条 warn：auto 42 / human 90）",
    "coverage": "16/35 = 45.7%（19 向量从未跑过）",
    "ci_pytest": "❌ 红（至少 7 项在 CI 同样成立）",
    "head": "1438cd5e",
    "remote": "1438cd5e（同步）",
}

# 630 留下的冻结基线（交叉核对用：既有的非 slow 失败集）
FROZEN_630_FAILURES = 12


def sh(args: list) -> str:
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    return (p.stdout or "").strip()


def file_counts() -> dict[str, int]:
    def count(sub: str, pat: str) -> int:
        n = 0
        for _b, _d, files in os.walk(os.path.join(ROOT, sub)):
            n += sum(1 for f in files if f.endswith(pat))
        return n

    return {"tools_py": count("tools", ".py"), "tests_py": count("tests", ".py"),
            "tools_629": sum(1 for f in os.listdir(os.path.join(ROOT, "tools"))
                             if f.endswith("_629.py")),
            "tools_630": sum(1 for f in os.listdir(os.path.join(ROOT, "tools"))
                             if f.endswith("_630.py")),
            "tools_631": sum(1 for f in os.listdir(os.path.join(ROOT, "tools"))
                             if f.endswith("_631.py"))}


def git_facts() -> dict[str, Any]:
    head = sh(["git", "rev-parse", "--short", "HEAD"])
    remote = sh(["git", "rev-parse", "--short", "origin/master"])
    ahead = sh(["git", "rev-list", "--count", "origin/master..HEAD"])
    behind = sh(["git", "rev-list", "--count", "HEAD..origin/master"])
    return {"head": head, "remote": remote,
            "ahead": int(ahead) if ahead.isdigit() else None,
            "behind": int(behind) if behind.isdigit() else None,
            "log3": sh(["git", "log", "--oneline", "-3"]).splitlines()}


def ci_failures() -> list[str]:
    """从已落盘的原始 pytest 输出里取失败用例（`FAILED xxx` 行），只读。"""
    if not os.path.exists(RAW):
        return []
    out = open(RAW, encoding="utf-8", errors="replace").read()
    return sorted({ln.split()[1] for ln in out.splitlines()
                   if ln.startswith("FAILED ") and len(ln.split()) > 1})


def measure() -> dict[str, Any]:
    return {"standing": STANDING, "counts": file_counts(), "git": git_facts(),
            "ci_failures": ci_failures(),
            "raw_present": os.path.exists(RAW),
            "dirty": [ln for ln in sh(["git", "status", "--short"]).splitlines()
                      if ln.startswith((" M", " D"))]}


def metrics() -> dict[str, Any]:
    """只读 import 630/629 的工具取四元指标快照（不跑监工门禁）。"""
    out: dict[str, Any] = {}
    try:
        import autoimmune_rate_framework as F

        m = F.measure()
        out["clean_cards"] = m["total"]
        out["autoimmune_rate_pct"] = round(m["rate"] * 100, 1)
        out["caliber_cards"] = len(m["caliber_only_cards"])
        out["hard_defect_cards"] = len(m["hard_defect_cards"])
    except Exception as exc:                                  # noqa: BLE001
        out["autoimmune_error"] = str(exc)
    try:
        import coverage_metric_630 as C

        c = C.measure()
        out["coverage"] = f"{c['ran_count']}/{c['total']} ({c['coverage_pct']}%)"
        out["coverage_never_ran"] = c.get("never_ran")
    except Exception as exc:                                  # noqa: BLE001
        out["coverage_error"] = str(exc)
    try:
        import run_630_gate as G

        out["frozen_630_failures"] = len(G.BASELINE_FAILURES)
    except Exception as exc:                                  # noqa: BLE001
        out["gate630_error"] = str(exc)
    return out


def write_report() -> str:
    m, mt = measure(), metrics()
    st = m["standing"]
    g = m["git"]
    head_note = "一致" if g["head"] == st["head"] else f"**不符**（实测 {g['head']}）"
    rem_note = "一致" if g["remote"] == st["head"] else f"**不符**（实测 {g['remote']}）"
    fails = m["ci_failures"]
    lines = [
        "# 631 任务0 · 开工基线台账", "",
        "> 工具：`tools/baseline_631.py`（只读）· **不改任何基线数字**（§零.10：不符只标注）",
        "", "## 一、§一 standing baseline", "",
        "| 指标 | 值 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in st.items()], "",
        "## 二、实测核对（任务书 vs 实测）", "",
        "| 项 | 任务书 | 实测 | 判定 |", "|---|---|---|---|",
        f"| HEAD | `{st['head']}` | `{g['head']}` | {head_note} |",
        f"| 远程 | `{st['remote']}` | `{g['remote']}`（ahead={g['ahead']} "
        f"/ behind={g['behind']}） | {rem_note} |",
        f"| 干净卡（自身免疫率分母） | 23 | {mt.get('clean_cards')} | "
        f"{'一致' if mt.get('clean_cards') == 23 else '**不符**'} |",
        f"| 自身免疫率 | 100% | {mt.get('autoimmune_rate_pct')}% | "
        f"{'一致' if mt.get('autoimmune_rate_pct') == 100.0 else '**不符**'} |",
        f"| 其中口径级 | 22 张 | {mt.get('caliber_cards')} 张 | "
        f"{'一致' if mt.get('caliber_cards') == 22 else '**不符**'} |",
        f"| coverage | 16/35（45.7%） | {mt.get('coverage')} | "
        f"{'一致' if mt.get('coverage') == '16/35 (45.7%)' else '**不符**'} |",
        f"| 630 冻结的既有失败基线 | — | {mt.get('frozen_630_failures')} 项 | "
        f"（631 开工实测 {len(fails)} 项，见 §三） |", "",
        "## 三、CI pytest 红的失败用例（本地实测）", "",
    ]
    if not m["raw_present"]:
        lines += ["> ⚠️ **未采集**：`data/ci_pytest_raw_631.txt` 不存在"
                  "（全量输出需另跑 `pytest -m \"not slow\" -q --tb=line`）。", ""]
    else:
        lines += [f"- 共 **{len(fails)}** 项失败：", "",
                  "| # | 失败用例 |", "|---|---|",
                  *[f"| {i} | `{n}` |" for i, n in enumerate(fails, 1)],
                  "",
                  "> 这是 **A1 逐条分类**的输入；分类与根因见 `data/ci_pytest_triage_631.md`。",
                  ""]
    lines += [
        "## 四、额外测量", "",
        "| 项 | 值 |", "|---|---|",
        f"| `tools/*.py` | {m['counts']['tools_py']} |",
        f"| `tests/*.py` | {m['counts']['tests_py']} |",
        f"| 629 工具 | {m['counts']['tools_629']} |",
        f"| 630 工具 | {m['counts']['tools_630']} |",
        f"| 631 工具（本批，随任务增长） | {m['counts']['tools_631']} |",
        "", "### recent commits", "", "```", *g["log3"], "```", "",
        "## 五、偏差登记（§零.10）", "",
        "1. **§一 `触达规则 37/67`**：629 台账记 36/67，630 任务书写 37/67（差 1 来自 629 D2 "
        "第八轮重跑）。631 沿用 37/67 并标注口径分歧（未裁定）。",
        "2. **CI pytest 失败清单为**本地实测**：CI 端的真实失败集合可能因 `_arch_v2x/` 未跟踪 "
        "残留而与本地不同（本地 4 项环境依赖型在 CI 不应成立）；**无 token ⇒ 未取 CI 日志**，"
        "630 已登记为缺口，本批沿用。",
        "3. 630 冻结基线 12 项 ↔ 631 开工实测项数若有差异，在 A1 逐条解释"
        "（本批正是要修掉其中跨批脆弱型与工具自检过期型）。", "",
        "## 六、局限", "",
        "- 只读测量：数字取自 git 与既有工具，**未跑监工四门禁**（§零.1）；",
        "- `gate_hits` 等冻结数字不重测（需 `gate_engine --check`，属监工门禁）；",
        "- 631 工具计数随本批后续任务增长（快照性质）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"measure": m, "metrics": mt}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m, mt = measure(), metrics()
    st = m["standing"]
    chk("§一 条目齐全（≥15 项）", len(st) >= 15, f"({len(st)})")
    chk("HEAD/远端短哈希可读", len(m["git"]["head"]) >= 7 and len(m["git"]["remote"]) >= 7)
    chk("git 事实：ahead/behind 为非负整数",
        isinstance(m["git"]["ahead"], int) and m["git"]["ahead"] >= 0
        and isinstance(m["git"]["behind"], int) and m["git"]["behind"] >= 0,
        f"(ahead={m['git']['ahead']}, behind={m['git']['behind']})")
    chk("tools/ 文件数 ≥ 300", m["counts"]["tools_py"] >= 300,
        f"({m['counts']['tools_py']})")
    chk("tests/ 文件数 ≥ 300", m["counts"]["tests_py"] >= 300,
        f"({m['counts']['tests_py']})")
    chk("四元指标可读（自身免疫率 + coverage）",
        bool(mt.get("autoimmune_rate_pct") is not None and mt.get("coverage")),
        f"({sorted(mt)})")
    chk("自身免疫率 = 100% 且 22 张口径级（与 §一 一致）",
        mt.get("autoimmune_rate_pct") == 100.0 and mt.get("caliber_cards") == 22,
        f"({mt.get('autoimmune_rate_pct')}% / {mt.get('caliber_cards')} 张)")
    chk("失败用例解析器：无原始文件时返回空且不报错",
        isinstance(ci_failures(), list))

    def snap() -> str:
        return sh(["git", "status", "--porcelain"])

    before = snap()
    measure()
    metrics()
    chk("只读：measure()/metrics() 不改变工作区", snap() == before)
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"631 baseline check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 任务0 基线台账（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写基线报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps({"measure": m, "metrics": metrics()},
                         ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"head={m['git']['head']} ahead={m['git']['ahead']} "
          f"tools={m['counts']['tools_py']} tests={m['counts']['tests_py']} "
          f"failures={len(m['ci_failures'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
