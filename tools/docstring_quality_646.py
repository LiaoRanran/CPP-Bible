"""646 · 阶段 B5 · 注释质量提升（不只是覆盖率）。

目标（646 §四 B5）：645 做到了 100% docstring **覆盖**，但**质量**参差。本批抽查关键工具，按
D2 规范（§二 文档契约）评估：模块 docstring 是否含「目标 / 数据源 / 铁律」、是否说明「做什么」、
关键函数是否有 docstring 与行内注释，并给出可改进清单。

评分维度（各 1 分，满分 5）：
1. 有模块 docstring；
2. 含「目标」段；
3. 含「数据源」或「真实、非代理」说明；
4. 含「铁律 / 只读 / 边界」说明；
5. 行内注释密度（`#` 注释行 ≥ 5 或注释行/代码行 ≥ 3%）。

`--check` 只读自检；`--audit` 真实抽查，写 `data/646_docstring_quality_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "646_docstring_quality_report.md")
REPORT_JSON = os.path.join(DATA, "646_docstring_quality_report.json")

# 抽查对象：**647 D1 合并前**的 645 核心 15 + 646 新增若干（关键路径）。
# 647 D1 执行合并后，被并入的 5 个成员文件已删除 ⇒ `audit()` 自动跳过并登记 `skipped_missing`。
SAMPLE = [
    "smart_issue_finder_645", "targeted_attacker_645", "rule_drafter_645",
    "rule_error_tracker_645", "rule_aging_detector_645", "loop_r5_runner_645",
    "standard_fetcher_645", "compiler_probe_645", "counterexample_searcher_645",
    "evidence_grading_645", "evidence_sufficiency_645", "queyi_data_models_645",
    "three_layer_orchestrator_645", "coupling_effect_645", "coupling_feedback_645",
    "rule_card_mapper_646", "three_layer_orchestrator_646", "performance_optimizer_646",
    "evidence_index_646", "authority_rule_annotator_646",
]


def score_file(path: str) -> dict:
    """对单文件 docstring 打分（0-5）+ 问题清单。"""
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    doc = ast.get_docstring(tree) or ""
    lines = src.splitlines()
    comment_lines = sum(1 for ln in lines if ln.strip().startswith("#"))
    code_lines = sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#"))
    checks: dict[str, bool] = {
        "has_module_doc": bool(doc),
        "has_goal": ("目标" in doc),
        "has_source": ("数据源" in doc or "真实、非代理" in doc or "真实" in doc and "代理" in doc),
        "has_boundary": ("铁律" in doc or "只读" in doc or "边界" in doc),
        "has_comments": comment_lines >= 5 or bool(code_lines) and comment_lines / code_lines >= 0.03,
    }
    score = 0
    for v in checks.values():
        if v:
            score += 1
    issues = [k for k, v in checks.items() if not v]
    return {"score": score, "checks": checks, "issues": issues,
            "comment_lines": comment_lines, "code_lines": code_lines}


def audit() -> dict:
    """真实抽查全部样本。

    **647 D1 起**：样本里有些工具**已被合并删除**（15 → 10 的一部分）——
    它们从样本中**剔除并单独登记**（`skipped_missing`），不再按"0 分"计入平均
    （否则平均分会被"文件不存在"这种与注释质量无关的原因拉低，是错误的度量）。
    """
    rows: dict[str, dict] = {}
    skipped: list[str] = []
    for name in SAMPLE:
        p = os.path.join(TOOLS, name + ".py")
        if not os.path.exists(p):
            skipped.append(name)
            continue
        rows[name] = score_file(p)
    avg = round(sum(int(r["score"]) for r in rows.values()) / (len(rows) or 1), 3)
    return {"sample": len(rows), "avg_score": avg, "max_score": 5, "rows": rows,
            "skipped_missing": skipped}


def write_report(result: dict) -> None:
    """写报告。"""
    lines = ["# 646 注释质量报告（B5）", "",
             f"- 抽查工具数：{result['sample']}",
             f"- 平均分：**{result['avg_score']}/{result['max_score']}**", "",
             "| 工具 | 分数 | 问题 |", "|---|---|---|"]
    for name, r in result["rows"].items():
        lines.append(f"| `{name}` | {r['score']} | {r.get('issues', [])} |")
    lines += ["", "## 评分维度", "",
              "1. 有模块 docstring；2. 含「目标」段；3. 含「数据源/真实」说明；"
              "4. 含「铁律/只读/边界」说明；5. 行内注释密度达标。"]
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：评分维度数量正确（满分 5）。"""
    import tempfile
    src = '"""645 目标：x。数据源：真实、非代理。铁律：只读。\n\n# 注释\n# 注释\n# 注释\n# 注释\n# 注释\n"""\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8", newline="\n") as fh:
        fh.write(src)
        p = fh.name
    try:
        r = score_file(p)
        assert r["score"] >= 4, r
    finally:
        os.unlink(p)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--audit` 真实抽查。"""
    ap = argparse.ArgumentParser(description="646 注释质量（B5）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--audit", action="store_true", help="真实抽查")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = audit()
    write_report(result)
    print(f"[646 docstring] 抽查={result['sample']} 平均分={result['avg_score']}/5")
    for name, r in result["rows"].items():
        if r["score"] < 4:
            print(f"  低分 {name}: {r['score']} issues={r['issues']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
