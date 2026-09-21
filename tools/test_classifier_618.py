#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 C2 · 测试分类计数脚本（replay/poison/gate category + 真实验证 vs 脚本自测）

- 扫描 tests/ 下所有 .py，按文件名 + import 内容特征自动分类（617 C1 taxonomy 落地）。
- 成员关系（membership）计数：一个文件若同时命中 gate/poison/replay，分别计入（三向视图可重叠）。
- primary 类别（优先级）：gate > poison > replay > mutation > evidence >
  independent_verification > statistics > tooling_integrity > snapshot > script_self_test > 其他。
- 真实验证 = 命中前 8 类之一（对验证系统正确性做断言）；脚本自测 = snapshot/script_self_test。
- 纯标准库；只读 tests/ 与已知受控工具名，不 import 任何受控工具。
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, "tests")

# (primary 顺序, 是否真实验证, 名称/import 匹配特征)
CATEGORIES = [
    ("gate", True, ["gate"]),
    ("poison", True, ["poison"]),
    ("replay", True, ["replay"]),
    ("mutation", True, ["mutation"]),
    ("evidence", True, ["evidence", "atom_evidence"]),
    ("independent_verification", True, ["independent_verification", "verify_independence"]),
    ("statistics", True, ["confidence_sequence", "escape_rate", "statistic"]),
    ("tooling_integrity", True, ["tool_integrity", "tool_checksum"]),
    ("snapshot", False, ["snapshot"]),
    ("script_self_test", False, ["_script", "self_test", "run_618", "conftest"]),
]

IMPORT_TARGETS = {
    "gate": "gate_engine",
    "poison": "poison_drill",
    "replay": "atom_evidence_replay",
    "mutation": "mutation_fuzz",
    "evidence": None,
    "independent_verification": None,
    "statistics": "confidence_sequence",
    "tooling_integrity": "tool_integrity",
    "snapshot": "snapshot_manifest",
    "script_self_test": None,
}

REAL_CATS = ("gate", "poison", "replay", "mutation", "evidence",
             "independent_verification", "statistics", "tooling_integrity")


def classify_membership(path):
    name = os.path.basename(path).lower()
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        content = ""
    matched = []
    for cat, _is_real, hints in CATEGORIES:
        targets = [IMPORT_TARGETS[cat]] if IMPORT_TARGETS.get(cat) else []
        match_name = any(h in name for h in hints)
        match_import = any(
            re.search(r"(?:import|from)\s+" + re.escape(t), content) for t in targets if t
        ) if targets else False
        if match_name or match_import:
            matched.append(cat)
    return matched


def classify_file(path):
    """primary 类别（兼容旧测试）。"""
    matched = classify_membership(path)
    if not matched:
        return "其他"
    for cat, _is_real, _h in CATEGORIES:
        if cat in matched:
            return cat
    return "其他"


def scan(tests_dir=TESTS):
    files = sorted(
        os.path.join(tests_dir, f) for f in os.listdir(tests_dir)
        if f.endswith(".py") and not f.endswith(".pyc")
    )
    return {os.path.basename(p): classify_membership(p) for p in files}


def summarize(results):
    from collections import Counter
    primary_counts = Counter()
    three = {"gate": 0, "poison": 0, "replay": 0}
    real = 0
    self_test = 0
    unclassified = 0
    for name, matched in results.items():
        primary = classify_file if False else None
        # primary：第一个在 CATEGORIES 顺序中命中的类别
        prim = "其他"
        for cat, _r, _h in CATEGORIES:
            if cat in matched:
                prim = cat
                break
        primary_counts[prim] += 1
        for k in three:
            if k in matched:
                three[k] += 1
        if any(c in REAL_CATS for c in matched):
            real += 1
        elif "snapshot" in matched or "script_self_test" in matched:
            self_test += 1
        else:
            unclassified += 1
    three["其他"] = sum(1 for m in results.values() if not ("gate" in m or "poison" in m or "replay" in m))
    return {
        "total": len(results),
        "counts": dict(primary_counts),
        "three_way": three,
        "real_verification": real,
        "script_self_test": self_test,
        "unclassified": unclassified,
    }


def render_markdown(results, summary):
    L = []
    L.append("# 测试分类计数（618 C2 · 落地 617 C1 taxonomy）\n")
    L.append("> 纯标准库；扫描 tests/ 下 %d 个 .py，按文件名 + import 内容特征分类（成员关系计数）。\n" % summary["total"])
    L.append("> 真实验证 = 命中 gate/poison/replay/mutation/evidence/independent_verification/statistics/tooling_integrity 之一；"
             "脚本自测 = snapshot/script_self_test（工具链自身，不计入验证覆盖）。\n")
    L.append("## 一、三向分类（gate/poison/replay 成员关系，可重叠 / 其他=三者均未命中）\n")
    for k in ("replay", "poison", "gate", "其他"):
        L.append("- **%s**：%d" % (k, summary["three_way"][k]))
    L.append("\n## 二、primary 全类别计数（单文件归入优先级最高的一类）\n")
    for k, v in sorted(summary["counts"].items(), key=lambda kv: -kv[1]):
        L.append("- %s：%d" % (k, v))
    L.append("\n## 三、真实验证 vs 脚本自测\n")
    L.append("- **真实验证**：%d（占比 %.1f%%）" % (summary["real_verification"], 100.0 * summary["real_verification"] / summary["total"]))
    L.append("- **脚本自测**：%d（占比 %.1f%%）" % (summary["script_self_test"], 100.0 * summary["script_self_test"] / summary["total"]))
    L.append("- **未分类（需人工 review）**：%d（不匹配任何已知特征）" % summary["unclassified"])
    L.append("\n## 四、未分类文件清单（需人工复核）\n")
    unc = [n for n, m in sorted(results.items()) if not m]
    if unc:
        for n in unc:
            L.append("- %s" % n)
    else:
        L.append("- （无）")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="618 C2 测试分类计数")
    ap.add_argument("--tests", default=TESTS)
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "test_classification_618.md"))
    args = ap.parse_args()
    results = scan(args.tests)
    summary = summarize(results)
    txt = render_markdown(results, summary)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)
    return results, summary


if __name__ == "__main__":
    main()
