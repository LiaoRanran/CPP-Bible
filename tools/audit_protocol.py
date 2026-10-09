#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""audit_protocol.py — 707-D：**五步审计协议**（可执行版），Step 3 = **双设计**。

科研依据（700-C 双设计要求；权威源 ``data/700_design_simulation.json`` L22-25、
``data/700_sample_complexity.json``）
================================================================================
700-C 发现：**配对设计对 Type III/IV 功效恒为 0**（标签/聚合漂移不改变任何逐样本裁决
⇒ ψ = 0）。因此审计协议的 **Step 3 必须是「双设计」**，而不是单一配对设计：

* **样本级配对**（sample-level pairing）：检出 Type I（构成退化）/ Type II（环境）—— 二者 ψ > 0；
* **设计级对照**（design-level contrast）：检出 Type III（标签词表）/ Type IV（聚合规则）——
  二者 ψ = 0，配对设计无用，必须在**报告口径轴**上做对照（用已存逐资产矩阵重算）。

协议五步（对齐论文 The Evaluator-Audit Protocol）：
    1. **声明**（claim declaration）：写出声明与其**口径签名** (A,E,Θ,P[,λ])。
    2. **暴露隐含假设**：列出未声明的假设（校准臂、分母、聚合规则、标签轴 λ）。
    3. **双设计**（Step 3，700-C）：自动判定漂移类型 ⇒ I/II 走配对（附样本量），III/IV 走设计级对照。
    4. **同口径重测**（same-caliber re-test）：在声明口径下重测；获取层漂移**不可事后纠正**（698-B T6）。
    5. **预声明判决规则**（pre-registered decision rule）：判决阈值在观测前固定。

红线：纯计算/编排，``detect_calls = 0``。

用法
====
    python tools/audit_protocol.py --psi 0.35 --epsilon 0.35      # Type II 风格 ⇒ 配对
    python tools/audit_protocol.py --psi 0.0                       # Type III/IV ⇒ 设计级对照
    python tools/audit_protocol.py --plan                           # 打印五步协议（含四型判定）
"""
from __future__ import annotations

import argparse
import json
from typing import Any, Final

import sample_size_calculator as ssc  # 707-D 样本量计算器（700-C）

# 四型漂移（698-A / 700-C）。pairing_effective 指「逐样本裁决是否变化（ψ>0）」。
DRIFT_TYPES: Final[dict[str, dict[str, Any]]] = {
    "I": {"name": "composition-drop（构成退化）", "psi_positive": True, "axis": "sample-level"},
    "II": {"name": "environment（环境）", "psi_positive": True, "axis": "sample-level"},
    "III": {"name": "label-vocabulary（标签词表）", "psi_positive": False, "axis": "report-level"},
    "IV": {"name": "aggregation-rule（聚合规则）", "psi_positive": False, "axis": "report-level"},
}


def classify(psi: float, type_hint: str | None = None) -> str:
    """按 ψ 判定漂移类型（700-C：ψ=0 ⇒ III/IV）。"""
    if psi <= 0:
        return type_hint if type_hint in ("III", "IV") else "III/IV（ψ=0：标签/聚合）"
    return type_hint if type_hint in ("I", "II") else "I/II（ψ>0：构成/环境）"


def dual_design(psi: float, epsilon: float, *, alpha: float = 0.05, power: float = 0.8) -> dict[str, Any]:
    """**Step 3 双设计**（700-C）：配对臂 + 设计级对照臂。"""
    paired = ssc.required_n(psi, epsilon, alpha, power)
    use_paired = paired["detectable_by_paired_design"]
    return {
        "step3_dual_design": True,
        "paired_arm": {
            "applicable": use_paired,
            "design": "sample-level pairing（配对符号检验 / 精确 McNemar）",
            "targets_types": ["I", "II"],
            **paired,
        },
        "design_level_arm": {
            "applicable": True,
            "design": "design-level contrast（在报告口径轴上对照：用已存逐资产矩阵重算聚合/标签）",
            "targets_types": ["III", "IV"],
            "why": ("ψ=0（逐样本裁决不变）⇒ 配对设计功效恒 0 ⇒ 必须做设计级对照"
                    if not use_paired else "作为配对臂的补充：跨口径的对照仍需要"),
        },
        "routing": ("paired（Type I/II）" if use_paired else "design-level contrast（Type III/IV）"),
    }


def audit_plan(psi: float, epsilon: float, *, declaration: str = "(未提供声明)",
               caliber_signature: str = "(A,E,Θ,P[,λ])") -> dict[str, Any]:
    """生成五步审计协议（Step 3 = 双设计）。"""
    t = classify(psi)
    return {
        "claim_declaration": {
            "claim": declaration,
            "caliber_signature": caliber_signature,
            "note": "口径签名必须显式且有限；未声明 λ（标签轴）的分组统计不可比较（缺 A8，707-A）。",
        },
        "expose_implied_assumptions": {
            "checklist": ["校准臂是否被当作检测臂", "分母（catch+miss vs 全样本）",
                          "聚合规则（OR/max/at-least-2/mean）是否声明", "标签轴 λ 是否声明"],
            "note": "任何未声明的假设都可能在换口径时移动报告值（Type III/IV 的入口）。",
        },
        "dual_design": dual_design(psi, epsilon),
        "same_caliber_retest": {
            "rule": "在**声明口径**下重测，不做事后校正",
            "correctability": ("获取层漂移不可事后纠正 ⇒ 见 698-B T6 / tools/check_drift_correctability.py"),
        },
        "preregistered_decision_rule": {
            "rule": "判决阈值在观测前固定；多口径变化逐口径分别声明（A5 超可加 ⇒ 不可线性相加）",
        },
        "drift_type": t,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="707-D：五步审计协议（Step 3 = 双设计，700-C）")
    ap.add_argument("--psi", type=float, default=None)
    ap.add_argument("--epsilon", type=float, default=None)
    ap.add_argument("--plan", action="store_true", help="打印四型判定 + 双设计路由")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.plan or a.psi is None:
        rows = {t: (dual_design(0.353357, 0.353357) if d["psi_positive"]
                    else dual_design(0.0, 0.0)) for t, d in DRIFT_TYPES.items()}
        for t, d in DRIFT_TYPES.items():
            r = rows[t]["routing"]
            det = rows[t]["paired_arm"]["applicable"]
            print(f"  Type {t:<3} {d['name']:<28} axis={d['axis']:<13} 配对可用={det}  ⇒ {r}")
        print("  ⇒ Step 3 = 双设计（I/II 配对，III/IV 设计级对照），与 700-C 一致")
        return 0

    eps = a.epsilon if a.epsilon is not None else a.psi
    plan = audit_plan(a.psi, eps)
    if a.json:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 0
    dd = plan["dual_design"]
    print("== 707-D 五步审计协议（Step 3 = 双设计，700-C）==")
    print(f"  漂移类型：{plan['drift_type']}")
    print(f"  Step 3 路由：{dd['routing']}")
    print(f"  配对臂可用={dd['paired_arm']['applicable']}  所需 n={dd['paired_arm']['n_total']}")
    print(f"  设计级对照臂：{dd['design_level_arm']['design']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
