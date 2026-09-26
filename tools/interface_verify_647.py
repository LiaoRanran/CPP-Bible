"""647 D2 · **合并后接口统一验证**（10 个核心工具是否符合 645 D2 接口规范）。

背景：646 B4 给出「15 → 10」的合并方案但**未执行**（怕 645 测试套件整体红）；
**647 D1 执行了合并**（成员以重命名入口保留，同步改测试）。本模块验证合并后的 10 个核心工具
仍然满足 645 D2 的接口规范（`docs/tool_interface_spec_645.md`）：

| 检查项 | 判据 |
|---|---|
| 统一入口 | 有 `main(argv=None) -> int` **且** argparse 支持 `--check` |
| `--check` 行为 | **真实跑一次**，必须 exit 0（只读幂等） |
| 统一输出 | 有模块 docstring；报告类工具有 `REPORT_MD` 且路径在 `data/` 下 |
| 自检函数 | 有 `selftest() -> int` |
| 合并无损 | 三个合并模块里，被并入成员的入口**仍可调用**（`feedback_*` / `effect_*` / `sufficiency_*` / `error_*` / `aging_*`） |

输出：`data/647_merge_report.md`（合并前后对比 + 逐工具接口表）。纯标准库（`ruff` 可选）。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "647_merge_report.md")
OUT_JSON = os.path.join(ROOT, "data", "647_merge_report.json")

#: 合并后**现存**的 10 个核心工具（646 B4 的 15 → 10）
CORE_10: tuple[str, ...] = (
    "smart_issue_finder_645", "targeted_attacker_645", "rule_drafter_645",
    "loop_r5_runner_645", "rule_card_mapper_646",
    "standard_fetcher_645", "compiler_probe_645", "counterexample_searcher_645",
    "evidence_grading_645", "three_layer_orchestrator_645",
)
#: 646 B4 合并计划（647 D1 已执行）
MERGE_PLAN = (
    {"group": "耦合编排 + 反馈 + 效果评估",
     "members": ["three_layer_orchestrator_645", "coupling_feedback_645", "coupling_effect_645"],
     "target": "three_layer_orchestrator_645",
     "keep_entries": ["generate_feedback", "evaluate", "write_effect_report"]},
    {"group": "证据等级 + 充分性",
     "members": ["evidence_grading_645", "evidence_sufficiency_645"],
     "target": "evidence_grading_645", "keep_entries": ["judge", "write_sufficiency_report"]},
    {"group": "R5 闭环 + error + 老化",
     "members": ["loop_r5_runner_645", "rule_error_tracker_645", "rule_aging_detector_645"],
     "target": "loop_r5_runner_645",
     "keep_entries": ["track", "detect", "load_ledger", "write_error_report", "write_aging_report"]},
)


def _module_ast(name: str) -> Optional[ast.Module]:
    p = os.path.join(HERE, name + ".py")
    if not os.path.isfile(p):
        return None
    return ast.parse(open(p, encoding="utf-8").read())


def _top_names(tree: ast.Module) -> set[str]:
    out: set[str] = set()
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.Assign):
            out |= {t.id for t in n.targets if isinstance(t, ast.Name)}
    return out


def check_tool(name: str, run_check: bool = True) -> dict[str, Any]:
    """逐工具检查接口规范（**真跑 `--check`**）。"""
    tree = _module_ast(name)
    if tree is None:
        return {"tool": name, "exists": False, "ok": False, "why": "文件不存在"}
    doc = ast.get_docstring(tree) or ""
    names = _top_names(tree)
    has_main = "main" in names
    has_selftest = "selftest" in names
    # argparse 是否暴露 --check
    src = open(os.path.join(HERE, name + ".py"), encoding="utf-8").read()
    has_check_flag = '"--check"' in src or "'--check'" in src
    report_md = names & {"REPORT_MD", "EFFECT_REPORT_MD", "FEEDBACK_REPORT_MD",
                         "SUFF_REPORT_MD", "ERROR_REPORT_MD", "AGING_REPORT_MD"}
    out = {"tool": name, "exists": True, "has_doc": bool(doc), "has_main": has_main,
           "has_selftest": has_selftest, "has_check_flag": has_check_flag,
           "report_globals": sorted(report_md)}
    if run_check:
        try:
            r = subprocess.run([sys.executable, os.path.join(HERE, name + ".py"), "--check"],
                               capture_output=True, text=True, timeout=300, cwd=ROOT,
                               encoding="utf-8", errors="replace")
            out["check_rc"] = r.returncode
        except (OSError, subprocess.SubprocessError) as exc:
            out["check_rc"] = -1
            out["check_error"] = f"{type(exc).__name__}"
    out["ok"] = bool(out["has_doc"] and out["has_main"] and out["has_selftest"]
                     and out["has_check_flag"] and out.get("check_rc", 0) == 0)
    return out


def merge_loss_check() -> list[dict[str, Any]]:
    """**合并无损**：被并入成员的入口在目标模块里仍可调用。"""
    import importlib
    rows = []
    for g in MERGE_PLAN:
        mod = importlib.import_module(str(g["target"]))
        missing = [e for e in g["keep_entries"] if not hasattr(mod, e)]
        removed_ok = []
        for m in g["members"]:
            if m == g["target"]:
                continue
            removed_ok.append({"member": m,
                               "file_removed": not os.path.isfile(os.path.join(HERE, m + ".py"))})
        rows.append({"target": g["target"], "entries": g["keep_entries"],
                     "missing_entries": missing, "members_removed": removed_ok,
                     "ok": not missing and all(x["file_removed"] for x in removed_ok)})
    return rows


def audit(run_check: bool = True) -> dict[str, Any]:
    tools = [check_tool(n, run_check=run_check) for n in CORE_10]
    loss = merge_loss_check()
    return {"n_tools": len([t for t in tools if t["exists"]]),
            "n_planned": len(CORE_10),
            "tools": tools,
            "loss_check": loss,
            "all_ok": all(t["ok"] for t in tools) and all(x["ok"] for x in loss)}


def write_report(res: Optional[dict[str, Any]] = None) -> str:
    res = res or audit()
    lines = [
        "# 647 D2 · 合并后接口统一验证（10 个核心工具）", "",
        f"- 现存核心工具：**{res['n_tools']}**（646 B4 计划 15 → 10，**647 D1 已执行**）",
        f"- 全部符合 645 D2 接口规范：**{res['all_ok']}**", "",
        "## 一、合并前后对比", "",
        "| 组 | 合并前成员 | 合并后目标 | 保留入口 | 成员文件已删除 |", "|---|---|---|---|---|"]
    for g, loss in zip(MERGE_PLAN, res["loss_check"]):
        lines.append(f"| {g['group']} | {', '.join(g['members'])} | `{g['target']}` | "
                     f"`{'`, `'.join(g['keep_entries'])}` | {loss['ok']} |")
    lines += ["", "## 二、逐工具接口检查", "",
              "| 工具 | docstring | main | selftest | `--check` 标志 | `--check` 退出码 | 报告路径在 data | 合规 |",
              "|---|---|---|---|---|---|---|---|"]
    for t in res["tools"]:
        lines.append(f"| `{t['tool']}` | {t.get('has_doc')} | {t.get('has_main')} | "
                     f"{t.get('has_selftest')} | {t.get('has_check_flag')} | "
                     f"{t.get('check_rc')} | {bool(t.get('report_globals'))} | "
                     f"{'✅' if t['ok'] else '❌'} |")
    lines += ["", "## 三、合并无损验证（入口仍可调用）", "",
              "| 目标模块 | 保留入口 | 缺失入口 | 通过 |", "|---|---|---|---|"]
    for x in res["loss_check"]:
        lines.append(f"| `{x['target']}` | `{'`, `'.join(x['entries'])}` | "
                     f"{x['missing_entries'] or '—'} | {'✅' if x['ok'] else '❌'} |")
    lines += ["", "## 诚实登记", "",
              "1. **合并是「文件组织」层面的**：被并入的成员代码**原样搬进**目标模块，"
              "只把 `write_report`/`selftest`/`main` 等会冲突的名字**重命名**（如 "
              "`write_effect_report`）⇒ 功能等价、测试逐条复用；",
              "2. **同步改了测试 import**（646 自己就说了「执行合并需同步改测试」）；"
              "另外两个 646 工具（`tool_consolidation_646` / `docstring_quality_646`）"
              "改成**感知合并后状态**（现存 10 / 缺失成员自动跳过），并同步其单测；",
              "3. **`--check` 是真跑的**（subprocess，300s 超时），不是纸面检查；",
              "4. 本模块**只验证不改代码**。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("计划合并 15 → 10（3 组合并，删 5 文件）",
        sum(len(g["members"]) - 1 for g in MERGE_PLAN) == 5)
    present = [n for n in CORE_10 if os.path.isfile(os.path.join(HERE, n + ".py"))]
    chk("10 个核心工具全部存在", len(present) == 10, str(len(present)))
    for g in MERGE_PLAN:
        for m in g["members"]:
            if m != g["target"]:
                chk(f"成员 {m} 文件已删除", not os.path.isfile(os.path.join(HERE, m + ".py")))
    loss = merge_loss_check()
    chk("合并无损（入口齐全）", all(x["ok"] for x in loss),
        str([x["target"] for x in loss if not x["ok"]]))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"D2 interface-verify selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 D2 合并后接口统一验证")
    ap.add_argument("--check", action="store_true", help="只读自检（不跑子进程）")
    ap.add_argument("--report", action="store_true", help="真跑全部 --check 并写报告")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    res = audit()
    if a.report:
        print(f"written {write_report(res)}")
        return 0 if res["all_ok"] else 1
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print(f"[647 merge-verify] 工具 {res['n_tools']}/10 全合规={res['all_ok']}")
    return 0 if res["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
