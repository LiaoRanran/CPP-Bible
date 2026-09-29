#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_658_gate.py — 658 批次验收门禁（编排器）。

把 658 各段交付串成一条可一键复跑的验收流水线，逐阶段收集 pass/fail，
产出 data/658_gate_status.json 与 data/658_acceptance_report.md。

设计：不重复实现判据，只**调用**各段工具；任一 L0 阶段失败即整体 exit 1。

阶段：
  S0 元状态对账   status_reconciler_658.py --check      （D，L0）
  S1 门禁分层合法 gate_tier_check_658.py --check        （B，L0）
  S2 真实缺陷检出 defect_fixture_658.py --rate          （A1，L0）
  S3 盲化 holdout  holdout_658.py --status              （A2，L0）
  S4 边界 provenance boundary_scope_658.py --report      （C，L1）
  S5 research 骨架 文件存在性检查                        （G，L1）
  S6 单元测试      pytest tests/*658*                    （L0）
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def _run(cmd, timeout=600):
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return 99, f"EXC: {e}"


def _tail(s, n=400):
    s = s.strip()
    return s[-n:] if len(s) > n else s


def stage(name, tier, cmd, timeout=600):
    code, out = _run(cmd, timeout)
    return {"stage": name, "tier": tier, "cmd": " ".join(cmd), "exit": code,
            "pass": code == 0, "tail": _tail(out)}


def research_check():
    required = ["PROTOCOL_v0.1.md", "00_problem.md", "01_research_questions.md",
                "02_hypotheses.md", "03_system_boundary.md", "04_threat_model.md",
                "05_evaluation_protocol.md", "06_datasets.md", "07_baselines.md",
                "08_metrics.md", "09_ablations.md", "10_analysis_plan.md",
                "11_reproducibility.md", "12_threats_to_validity.md",
                "13_ai_use_and_authorship.md", "CHANGELOG.md"]
    missing = [f for f in required if not os.path.isfile(os.path.join(ROOT, "research", f))]
    return {"stage": "S5 research 骨架", "tier": "L1",
            "cmd": "存在性: research/*.md", "exit": 1 if missing else 0,
            "pass": not missing, "tail": ("missing: " + ", ".join(missing)) if missing else "16/16 存在"}


def main():
    stages = []
    stages.append(stage("S0 元状态对账", "L0", [PY, "tools/status_reconciler_658.py", "--check"]))
    stages.append(stage("S1 门禁分层合法", "L0", [PY, "tools/gate_tier_check_658.py", "--check"]))
    stages.append(stage("S2 真实缺陷检出", "L0", [PY, "tools/defect_fixture_658.py", "--rate"]))
    stages.append(stage("S3 盲化 holdout", "L0", [PY, "tools/holdout_658.py", "--status"]))
    stages.append(stage("S4 边界 provenance", "L1", [PY, "tools/boundary_scope_658.py", "--report"]))
    stages.append(research_check())
    tests = sorted(glob.glob(os.path.join(ROOT, "tests", "*658*.py")))
    if tests:
        stages.append(stage("S6 单元测试(658)", "L0",
                            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + tests))

    l0_fail = [s for s in stages if s["tier"] == "L0" and not s["pass"]]
    l1_fail = [s for s in stages if s["tier"] == "L1" and not s["pass"]]
    overall = "PASS" if not l0_fail else "FAIL"

    status = {"gate": "658", "overall": overall,
              "l0_pass": sum(1 for s in stages if s["tier"] == "L0" and s["pass"]),
              "l0_total": sum(1 for s in stages if s["tier"] == "L0"),
              "l1_fail": len(l1_fail),
              "stages": stages}
    json.dump(status, open(os.path.join(ROOT, "data", "658_gate_status.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    lines = ["# 658 验收门禁报告", "",
             f"总体：**{overall}**（L0 {status['l0_pass']}/{status['l0_total']} 通过；L1 失败 {len(l1_fail)}）", "",
             "| 阶段 | 层级 | 结果 | 命令 |", "|---|---|---|---|"]
    for s in stages:
        lines.append(f"| {s['stage']} | {s['tier']} | {'PASS' if s['pass'] else 'FAIL'} | `{s['cmd']}` |")
    lines.append("")
    for s in stages:
        if not s["pass"]:
            lines += [f"## {s['stage']} — FAIL (exit {s['exit']})", "```", s["tail"], "```", ""]
    open(os.path.join(ROOT, "data", "658_gate_report.md"), "w", encoding="utf-8").write("\n".join(lines))

    print(f"[658 gate] overall={overall}  L0 {status['l0_pass']}/{status['l0_total']}  L1_fail={len(l1_fail)}")
    for s in stages:
        print(f"  [{'PASS' if s['pass'] else 'FAIL'}] {s['stage']} ({s['tier']})")
    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
