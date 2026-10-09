#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_axiom_independence.py — 707-A：漂移代数公理系统独立性的**回归测试**。

科研依据（700-A 元理论发现；权威源 ``data/700_axiom_independence.json``，生成者
``tools/compute_700_axiom_independence.py``）
================================================================================
在覆盖型框架内（漂移算子 τ = 资产列删去；报告函数 R 由聚合族给定）：

* **A3（幂等）/ A4（交换闭包）/ A6（不可逆）是定义域内的恒真命题（定理）** ——
  由 τ 的构造直接推出，把它们写成公理是冗余；
* **A7（可观测性分层）在把记账规则写进结构后也可证**（698-B 定理 T3）；
* 真正起约束作用的结构公理只有 **A2（撤除单调）与 A5（超可加）**，外加元公理 A1；
* 系统**不完备**：缺 **A8（标签轴闭包）**，Type III（标签）漂移不可表达。

本文件用 700-A 的 **4096 结构穷举**方法独立**重算**并断言上述分类，作为回归护栏：
若未来有人改动聚合族/检查逻辑，把「真公理」悄悄退化成「恒真」（或反之），本测试变红。

红线：``detect_calls = 0``；只读；产出只写 ``data/707_*``。
输出：``data/707_axiom_independence_test.json``；退出码 0 = 分类与 700-A 一致。

用法
====
    python tools/test_axiom_independence.py
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

OUT_JSON = ROOT / "data" / "707_axiom_independence_test.json"

# 700-A 的期望分类（权威源 data/700_axiom_independence.json）
EXPECTED_GENUINE = ["A2", "A5"]            # 有反例 ⇒ 真公理
EXPECTED_THEOREMS = ["A3", "A4", "A6", "A7"]  # 恒真 ⇒ 定理
EXPECTED_META = ["A1"]                     # 元公理


def load_700() -> Any:
    """按文件路径加载 700-A 穷举模型检查器（不执行其 main，不改其一行代码）。"""
    spec = importlib.util.spec_from_file_location(
        "cm700", str(HERE / "compute_700_axiom_independence.py"))
    if spec is None or spec.loader is None:
        raise ImportError("无法构造 compute_700_axiom_independence 的模块规格")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cm700"] = mod
    spec.loader.exec_module(mod)
    return mod


def classify(cm700: Any) -> dict[str, Any]:
    """在 4096 结构 × 7 聚合族上重算 A2/A3/A4/A5 真值表，并分类。"""
    structures = cm700.all_coverages()
    truth: dict[str, dict[str, bool]] = {}
    for aname, checker in (("A2", cm700.check_a2), ("A3", cm700.check_a3),
                           ("A4", cm700.check_a4), ("A5", cm700.check_a5)):
        truth[aname] = {agg: all(checker(cov, fn) for cov in structures)
                        for agg, fn in cm700.AGGREGATIONS.items()}
    a6 = cm700.check_a6(structures)
    a7 = cm700.a7_witness_search(structures)

    genuine: list[str] = []
    theorems: list[str] = []
    for aname in ("A2", "A3", "A4", "A5"):
        violators = [k for k, v in truth[aname].items() if not v]
        (genuine if violators else theorems).append(aname)
    (theorems if a6["holds"] else genuine).append("A6")
    (theorems if a7["witness_exists"] else genuine).append("A7")

    return {
        "n_structures": len(structures),
        "n_aggregations": len(cm700.AGGREGATIONS),
        "truth_table": truth,
        "a6_non_injective_holds": a6["holds"],
        "a7_witness_exists": a7["witness_exists"],
        "genuine_axioms": sorted(genuine),
        "theorems": sorted(theorems),
        "violating_aggregations": {a: [k for k, v in truth[a].items() if not v]
                                   for a in ("A2", "A5")},
    }


def main(argv: list[str] | None = None) -> int:
    cm700 = load_700()
    cls = classify(cm700)
    completeness = cm700.completeness_probe()

    # A8（标签轴闭包）占位：现有 7 公理系统无标签槽 ⇒ Type III 不可表达。
    a8_placeholder = {
        "axiom": "A8（标签轴闭包）",
        "status": "MISSING / TODO",
        "why": completeness["conclusion"],
        "cannot_auto_verify_reason": (
            "标签轴 λ 属于**报告规范层**，不是覆盖结构性质；本穷举域（覆盖 + 聚合）"
            "无法表达它 ⇒ 只能以「未声明 λ 的分组统计不可比较」这一规则人工/规范约束，"
            "无法像 A2/A5 那样给出结构反例。"
        ),
        "candidate_formalization": completeness["missing_axiom_candidate"],
    }

    checks = {
        "only_A2_A5_genuine": cls["genuine_axioms"] == EXPECTED_GENUINE,
        "A3_A4_A6_A7_are_theorems": sorted(cls["theorems"]) == sorted(EXPECTED_THEOREMS),
        "A2_has_counterexample": len(cls["violating_aggregations"]["A2"]) >= 1,
        "A5_has_counterexample": len(cls["violating_aggregations"]["A5"]) >= 1,
        "A8_missing_confirmed": bool(completeness.get("missing_axiom_candidate")),
    }
    ok = all(checks.values())

    doc: dict[str, Any] = {
        "schema": "queyi-707/axiom-independence-test/v1",
        "generated_by": "tools/test_axiom_independence.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        # 科研依据（红线 8）：700-A 元理论发现
        "research_basis": "700-A 元理论发现：A3/A4/A6 恒真，A2/A5 独立（data/700_axiom_independence.json）",
        "authority_source": "data/700_axiom_independence.json",
        "classification": cls,
        "expected": {
            "genuine_axioms": EXPECTED_GENUINE,
            "theorems": EXPECTED_THEOREMS,
            "meta_axioms": EXPECTED_META,
        },
        "a8_placeholder": a8_placeholder,
        "checks": checks,
        "pass": ok,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print("== 707-A 公理独立性回归测试（4096 结构 × 7 聚合）==")
    print(f"  结构域 = {cls['n_structures']}；聚合族 = {cls['n_aggregations']}")
    print(f"  真公理（有反例） = {cls['genuine_axioms']}")
    print(f"  恒真（定理）     = {cls['theorems']}")
    print(f"  A2 反例聚合 = {cls['violating_aggregations']['A2']}")
    print(f"  A5 反例聚合 = {cls['violating_aggregations']['A5']}")
    print(f"  A8（标签轴闭包） = {a8_placeholder['status']}（{a8_placeholder['why'][:40]}...）")
    for k, v in checks.items():
        print(f"  [{'ok' if v else 'FAIL'}] {k}")
    print(f"test_axiom_independence: {'PASS' if ok else 'FAIL'}  → {OUT_JSON.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
