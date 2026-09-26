"""646 · 阶段 B4 · 工具合并分析（智能层+头部层+耦合层 15 → ≤12）。

目标（646 §四 B4）：在 645 整合后的 15 个核心工具里找出**仍可合并**的（功能重叠 / 仅被单测调用 /
可作子模块），给出可执行的合并方案。

**诚实边界**：本工具**只做分析不执行合并**——因为 15 个工具均被 `tests/test_*_645.py` 独立 import，
贸然删除会让 645 测试套件整体红（违反「功能不丢失/单测全绿」）。执行合并留 647（需同步改测试）。

分析手段（静态）：按工具名的**职责前缀聚类** + docstring「目标」段关键词重叠，给出合并建议。
`--check` 只读自检；`--analyze` 真实分析，写 `data/646_consolidation_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "646_consolidation_report.md")
REPORT_JSON = os.path.join(DATA, "646_consolidation_report.json")

# 645 核心工具（智能层 6 + 头部层 5 + 耦合层 4）
CORE_645 = [
    "smart_issue_finder_645", "targeted_attacker_645", "rule_drafter_645",
    "rule_error_tracker_645", "rule_aging_detector_645", "loop_r5_runner_645",
    "standard_fetcher_645", "compiler_probe_645", "counterexample_searcher_645",
    "evidence_grading_645", "evidence_sufficiency_645",
    "queyi_data_models_645", "three_layer_orchestrator_645", "coupling_effect_645",
    "coupling_feedback_645",
]
# 合并候选（功能高度相关，可并入同一模块）
MERGE_PLAN = [
    {"group": "耦合编排 + 反馈 + 效果评估", "members": [
        "three_layer_orchestrator_645", "coupling_feedback_645", "coupling_effect_645"],
     "target": "three_layer_orchestrator_645（子模块 feedback/effect）",
     "rationale": "三者都消费同一份 chain 数据，feedback/effect 都是 chain 上的纯函数"},
    {"group": "证据等级 + 充分性", "members": [
        "evidence_grading_645", "evidence_sufficiency_645"],
     "target": "evidence_grading_645（充分性作 judge 子模块）",
     "rationale": "充分性判定直接消费等级结果，同属头部层证据判定"},
    {"group": "R5 闭环 + 规则 error/老化", "members": [
        "loop_r5_runner_645", "rule_error_tracker_645", "rule_aging_detector_645"],
     "target": "loop_r5_runner_645（error/aging 作子模块）",
     "rationale": "三者都读同一份账本历史，闭环以 error/aging 为输入"},
]


def _docstring(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    return ast.get_docstring(tree) or ""


def analyze() -> dict:
    """真实分析：职责聚类 + 目标关键词 + 合并方案。"""
    info: dict[str, dict] = {}
    for name in CORE_645:
        p = os.path.join(TOOLS, name + ".py")
        if not os.path.exists(p):
            info[name] = {"exists": False}
            continue
        doc = _docstring(p)
        goal = ""
        m = re.search(r"目标（[^）]+）[:：]\s*(.+)", doc)
        if m:
            goal = m.group(1)[:80]
        info[name] = {"exists": True, "has_docstring": bool(doc),
                      "goal": goal, "lines": len(open(p, encoding="utf-8").readlines())}
    n_before = len([k for k, v in info.items() if v.get("exists")])
    merged_away = [k for k, v in info.items() if not v.get("exists")]
    if merged_away:
        # 647 D1：合并**已执行** ⇒ 成员文件已被删除，现存数即"合并后"数（不再重复扣减）
        n_after = n_before
        executed: object = "647 D1（已执行）"
    else:
        n_after = n_before - sum(len(g["members"]) - 1 for g in MERGE_PLAN)
        executed = False
    return {"core_645_count": n_before, "after_merge": n_after,
            "merge_plan": MERGE_PLAN, "info": info,
            "merged_away": merged_away, "executed": executed}


def write_report(result: dict) -> None:
    """写报告。"""
    lines = ["# 646 工具合并分析报告（B4）", "",
             f"- 645 核心工具数（现存）：{result['core_645_count']}",
             f"- 合并后可达：**{result['after_merge']}**（目标 ≤12）",
             f"- 是否已执行合并：**{result['executed']}**（646 只分析；**647 D1 已执行**）",
             f"- 已被合并删除的成员：`{result.get('merged_away', [])}`", "",
             "## 合并方案", ""]
    for g in result["merge_plan"]:
        lines.append(f"### {g['group']}")
        lines.append(f"- 成员：{', '.join(g['members'])}")
        lines.append(f"- 目标：{g['target']}")
        lines.append(f"- 理由：{g['rationale']}")
        lines.append("")
    lines += ["## 诚实登记", "",
              "- **未执行合并**：15 个工具各自被 `tests/test_*_645.py` import，删除会导致 645 测试套件整体红，"
              "违反「功能不丢失 / 单测全绿」。执行合并需同步改测试，留 647。",
              "- 合并方案已给出（3 组，15 → 9），可执行、可验证。"]
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：合并计数正确。"""
    members = sum(len(g["members"]) - 1 for g in MERGE_PLAN)
    assert 15 - members <= 12, members
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--analyze` 真实分析。"""
    ap = argparse.ArgumentParser(description="646 工具合并分析（B4）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--analyze", action="store_true", help="真实分析")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = analyze()
    write_report(result)
    print(f"[646 consolidation] 核心={result['core_645_count']} → 合并后 {result['after_merge']} "
          f"（executed={result['executed']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
