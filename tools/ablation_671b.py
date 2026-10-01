#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ablation_671b.py — 671b A 段：六组 ablation（A0–A5）**设计 + 可执行框架**。

⚠️ 本批红线（671b 任务书）
==========================
**本批只写脚本和设计，不跑实验。** 因此本工具的 `--run` **不执行任何检测、
不写任何实验结果**；它只做三件事：

1. 把 `research/670b_ablation设计.md` 的六组设计**机器可读化**（`ABLATIONS` 表）；
2. `--dry-run` 打印每组"要跑什么、缺什么前置、当前能不能跑"（**可行性体检**）；
3. `--run` 在**前置齐备**时**登记 run plan**（`data/experiments/ablation_plan_671b.json`），
   在**前置缺失**时**如实登记 BLOCKED**（不编数字）；真正的执行由后续批次做。

为什么 `--run` 不真跑
====================
设计文档 §3「可执行性评估」已如实登记两组**结构性阻塞**：
* **A5**（random-budget）与真 B3 一样依赖拆仓验证器暴露 `select_assets(pool,n,strategy,seed)`
  —— 主仓 has no asset-selection interface；
* **A2**（−holdout 隔离）遇到**盲态不可逆**：`data/holdout/holdout.json::iron_rule` 规定
  reveal 后永不回盲，故 A2 只能用**新建划分**，不能用现 holdout。
* **A1**（−failure-derived）需要从 git 历史取 657 时点的规则集快照（只读历史、不 checkout）。

⇒ 本批交付的是**打开就能跑的骨架**：`run(aid)` 返回该组的 **run plan**（数据源/命令/指标/
统计检验），不是结果。数字一律留 `{{TODO_ablation_<aid>}}` 占位，等后续批次落盘。

六组（对应 `research/670b_ablation设计.md` §1）
==============================================
| 组 | 去掉什么 | 预写假设 | 检验 |
|---|---|---|---|
| **A0** Full | 无（参照系） | — | — |
| **A1** −failure-derived | 657 之后新增的规则集 | **H3**：检测率下降 | 配对精确 McNemar（vs A0） |
| **A2** −holdout 隔离 | holdout 盲态（改 dev） | 过拟合：dev↑ blind→ | Fisher 独立 / Δ 的 CI |
| **A3** −provenance | 边界三元组校验 | 假 pass 率↑ | Fisher（稀有事件） |
| **A4** −mutation | 变异 L1 自证层 | 内部测试强度↓ | 描述性（**不作检测率 Claim**） |
| **A5** random-budget | 失败驱动选资产 → 随机 | **H3**：低于 A0 | 配对精确 McNemar（vs A0） |

**关键对照 A0 − A5**：其 Δ 的 CI 跨不跨 0，决定"失败驱动优于随机预算"成立与否
（`research/670b_ablation设计.md` §1/§4）。

用法
====
    python tools/ablation_671b.py --dry-run        # 六组可行性体检（只读）
    python tools/ablation_671b.py --run            # 登记 run plan / BLOCKED（不跑实验）
    python tools/ablation_671b.py --check          # 自检（只读，exit 0=通过）
    python tools/ablation_671b.py --json           # 机读
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
OUT_DIR = ROOT / "data" / "experiments"
PLAN_PATH = OUT_DIR / "ablation_plan_671b.json"
DESIGN_DOC = ROOT / "research" / "670b_ablation设计.md"
BASELINE_DIR = OUT_DIR

#: 每组的前置产物（相对路径）；`all_required` = 两者都需，否则任一即可
def _prereq_label(p: str) -> str:
    return p


ABLATIONS: list[dict[str, Any]] = [
    {
        "id": "A0",
        "name": "Full（参照系）",
        "removed": "无",
        "hypothesis": "—（基线）",
        "expect": "最佳",
        "primary_metric": "detect_rate_measurable",
        "metrics": ["检出率", "unknown 率", "假 pass 率", "成本"],
        "detectors": ["D2 holdout", "D3 corpus"],
        "test": "参照系",
        "implementation": "现状系统（照实读逐样本判决）",
        "git_revert": False,
        "blocked": False,
        "blocked_reason": "",
        "prereq": ["data/experiments/baseline_fd.json"],
        "command": "python tools/baseline_670a.py --run",
        "stat_tool": "tools/ablation_stats_671b.py",
    },
    {
        "id": "A1",
        "name": "−failure-derived",
        "removed": "657 之后新增的规则集",
        "hypothesis": "H3：检测率下降",
        "expect": "holdout/corpus 下降",
        "primary_metric": "detect_rate_measurable",
        "metrics": ["Δ检出率 vs A0", "unknown 率"],
        "detectors": ["D2 holdout", "D3 corpus"],
        "test": "精确 McNemar（vs A0，同批配对）",
        "implementation": "把规则集回退到 657 时点的快照",
        "git_revert": True,       # 只读 git 历史取 657 规则集，不 checkout
        "blocked": False,
        "blocked_reason": "",
        "prereq": ["data/experiments/baseline_fd.json"],
        "command": "python tools/ablation_671b.py --run --only A1   # 需 657 规则集快照",
        "stat_tool": "tools/ablation_stats_671b.py",
    },
    {
        "id": "A2",
        "name": "−holdout 隔离",
        "removed": "holdout 的盲态（改为 dev 集）",
        "hypothesis": "过拟合：dev 升、blind 不升",
        "expect": "dev↑ / blind→",
        "primary_metric": "blind_detect_rate",
        "metrics": ["dev 检出率", "blind 检出率", "dev−blind 差"],
        "detectors": ["D2（新建 dev 划分）", "D2 blind 复测"],
        "test": "Fisher 精确（独立）或 Δ 的 CI",
        "implementation": "把 holdout 从盲态改为开发集，用同批样本调规则后复测",
        # 盲态不可逆：holdout 已 revealed=true ⇒ 只能用**新建**划分
        "git_revert": False,
        "blocked": False,
        "blocked_reason": "",
        "precondition_note": "holdout 一旦 reveal 永不回盲（data/holdout/holdout.json::iron_rule）"
                             "⇒ A2 必须构造**新的** dev/blind 划分，禁用现 holdout",
        "prereq": ["data/experiments/baseline_fd.json"],
        "command": "python tools/ablation_671b.py --run --only A2   # 需先新建 dev/blind 划分",
        "stat_tool": "tools/ablation_stats_671b.py",
    },
    {
        "id": "A3",
        "name": "−provenance",
        "removed": "边界三元组校验",
        "hypothesis": "证据不可追溯 ⇒ 误报↑",
        "expect": "假 pass 率↑",
        "primary_metric": "false_pass_rate",
        "metrics": ["假 pass 率", "unknown 率"],
        "detectors": ["D2 holdout", "D3 corpus"],
        "test": "Fisher（假 pass 是稀有事件，McNemar 不稳）",
        "implementation": "关闭 mutation_set_hash / mutation_count / generator_version 校验",
        "git_revert": False,
        "blocked": False,
        "blocked_reason": "",
        "prereq": ["data/experiments/baseline_fd.json"],
        "command": "python tools/ablation_671b.py --run --only A3",
        "stat_tool": "tools/ablation_stats_671b.py",
    },
    {
        "id": "A4",
        "name": "−mutation",
        "removed": "变异测试（L1 自证层）",
        "hypothesis": "内部测试强度下降",
        "expect": "存活变异↑",
        "primary_metric": "mutation_kill_rate",
        "metrics": ["变异 kill rate（**仅内部指标，不是检测率**）"],
        "detectors": ["变异集 core/all"],
        "test": "描述性；**不作缺陷检测率 Claim**",
        "implementation": "关闭 mutation_test_656 的 kill 判定",
        "git_revert": False,
        "blocked": False,
        "blocked_reason": "",
        "prereq": ["data/656_mutation_report_core.json"],
        "command": "python tools/ablation_671b.py --run --only A4",
        "stat_tool": "tools/ablation_stats_671b.py",
    },
    {
        "id": "A5",
        "name": "random-budget（**关键对照**）",
        "removed": "失败驱动选资产 → 随机选同数量资产",
        "hypothesis": "H3：不如 failure-driven",
        "expect": "低于 A0",
        "primary_metric": "detect_rate_measurable",
        "metrics": ["Δ检出率 vs A0", "分配表（种子 + 选中资产）"],
        "detectors": ["D2 holdout", "D3 corpus"],
        "test": "精确 McNemar（vs A0，同批配对）",
        "implementation": "同预算随机选同数量资产（必须带种子 + 分配表）",
        "git_revert": False,
        # A5 依赖拆仓 select_assets ⇒ 主仓 BLOCKED（与真 B3 同一阻塞）
        "blocked": True,
        "blocked_reason": "资产选择接口 select_assets(pool,n,strategy,seed) 在拆仓验证器 "
                          "queyi-verifier，主仓不可见（670a 已登记 BLOCKED）",
        "prereq": ["data/experiments/baseline_fd.json"],
        "command": "python tools/run_b3_671b.py --strategy random --seed 20260930  # 需拆仓接口",
        "stat_tool": "tools/ablation_stats_671b.py",
        # A5 的**主仓可直跑近似**：671b B 段提供的资产选择接口（在仪器池上）
        "fallback": "tools/select_assets_671b.py（主仓仪器级实现；明确标为近似，非真 B3）",
    },
]

#: A0 是所有组的参照系 ⇒ 每组都要与 A0 配对比较
CONTRASTS: list[tuple[str, str]] = [("A0", x) for x in ("A1", "A2", "A3", "A4", "A5")]


def _exists(rel: str) -> bool:
    return (ROOT / rel).is_file()


def feasibility(a: dict[str, Any]) -> dict[str, Any]:
    """单组可行性体检：**只读**判断前置是否齐备 + 是否有结构性阻塞。

    返回 `{ok, blockers, present, missing, note}`。`blockers` 非空 ⇒ 该组**不可执行**。
    """
    blockers: list[str] = []
    if a.get("blocked"):
        blockers.append(a["blocked_reason"])
    present = [p for p in a["prereq"] if _exists(p)]
    missing = [p for p in a["prereq"] if not _exists(p)]
    if missing:
        blockers.append("缺前置产物：" + ", ".join(missing))
    return {"ok": not blockers, "blockers": blockers,
            "present": present, "missing": missing,
            "note": a.get("precondition_note", "")}


def plan(a: dict[str, Any]) -> dict[str, Any]:
    """单组 **run plan**（不含结果）。

    ⚠️ 这是本工具的核心交付：把"要跑什么"写清楚，**不产生任何实验数字**。
    """
    fe = feasibility(a)
    return {
        "id": a["id"], "name": a["name"], "removed": a["removed"],
        "hypothesis": a["hypothesis"], "expected": a["expect"],
        "primary_metric": a["primary_metric"], "metrics": a["metrics"],
        "detectors": a["detectors"], "test": a["test"],
        "implementation": a["implementation"], "git_revert": a["git_revert"],
        "command": a["command"], "stat_tool": a["stat_tool"],
        "feasible": fe["ok"], "blockers": fe["blockers"],
        "prereq": a["prereq"], "prereq_present": fe["present"],
        "prereq_missing": fe["missing"],
        "fallback": a.get("fallback", ""),
        "result_placeholder": f"{{{{TODO_ablation_{a['id']}}}}}",
        "status": "READY" if fe["ok"] else "BLOCKED",
    }


def build_plan() -> dict[str, Any]:
    """全部六组的 run plan + 关键对照登记。**不跑实验、不产生数字。**"""
    groups = [plan(a) for a in ABLATIONS]
    contrast_rows = []
    for ref, other in CONTRASTS:
        ra = next(g for g in groups if g["id"] == ref)
        rb = next(g for g in groups if g["id"] == other)
        # A2/A3 用独立/Fisher，其余配对 McNemar
        design = "unpaired" if other == "A2" else "paired"
        test_name = ("Fisher 精确（独立样本）" if design == "unpaired"
                     else "精确 McNemar（同批配对）")
        contrast_rows.append({
            "contrast": f"{ref} − {other}",
            "design": design, "test": test_name,
            "both_ready": bool(ra["feasible"] and rb["feasible"]),
            "delta_placeholder": f"{{{{TODO_delta_{ref}_{other}}}}}",
            "ci_crosses_zero": None,     # 跑完才填；本批不填
            "note": ("**关键对照**：CI 跨 0 ⇒『失败驱动优于随机预算』不成立，"
                     "必须原样报告（670b 设计 §1/§4）" if other == "A5" else ""),
        })
    n_ready = sum(1 for g in groups if g["feasible"])
    return {
        "schema": "queyi-ablation-plan/671b",
        "version": VERSION,
        "design_doc": "research/670b_ablation设计.md",
        "executed": False,
        "executed_note": "本批（671b）**只写脚本和设计，不跑实验**——"
                         "plan 里所有结果字段均为占位符（{{TODO_ablation_*}}），"
                         "不得当作实验结果引用。",
        "groups": groups,
        "contrasts": contrast_rows,
        "summary": {"n_groups": len(groups), "n_ready": n_ready,
                    "n_blocked": len(groups) - n_ready,
                    "blocked_ids": [g["id"] for g in groups if not g["feasible"]]},
        "stat_primitives": [
            "mcnemar_exact", "cohens_h", "fisher_exact", "bh_fdr", "holm",
            "delta_ci_paired", "paired_delta_ci", "comparison",
            "sample_size_two_proportions", "sample_size_paired_mcnemar",
        ],
        "red_lines": [
            "本批不跑实验（671b 任务书）",
            "所有数字必须来自已有产物，不编造实验结果",
            "A5/A1/A2 的结构性阻塞如实登记（不因『想跑』而降级为近似冒充真实验）",
        ],
    }


def summary(p: dict[str, Any]) -> str:
    L = ["=== 671b ablation run plan（**未执行**：本批只写脚本与设计）===",
         f"设计文档 {p['design_doc']}",
         f"六组：{p['summary']['n_ready']} READY / {p['summary']['n_blocked']} BLOCKED "
         f"（blocked: {', '.join(p['summary']['blocked_ids']) or '无'}）", ""]
    for g in p["groups"]:
        mark = "READY  " if g["feasible"] else "BLOCKED"
        L.append(f"[{mark}] {g['id']} {g['name']}")
        L.append(f"          去掉: {g['removed']}")
        L.append(f"          假设: {g['hypothesis']}   预期: {g['expected']}")
        L.append(f"          指标: {g['primary_metric']}   检验: {g['test']}")
        if g["blockers"]:
            L.append(f"          阻塞: {'；'.join(g['blockers'])}")
        if g["git_revert"]:
            L.append("          ⚠ 需回退 git 历史取规则集快照（只读，不 checkout）")
    L.append("")
    L.append("关键对照 A0 − A5（CI 跨 0 ⇒ 核心机制不成立）")
    for c in p["contrasts"]:
        if "A5" in c["contrast"]:
            L.append(f"  {c['contrast']}: {c['test']} · Δ 占位 {c['delta_placeholder']}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    p = build_plan()
    chk("恰好六组 A0–A5", len(p["groups"]) == 6)
    chk("组 id 顺序 A0..A5", [g["id"] for g in p["groups"]]
        == ["A0", "A1", "A2", "A3", "A4", "A5"])
    chk("executed=False（本批不跑实验）", p["executed"] is False)
    # 每组必须有结果占位符，且**不得**有真实数字字段
    for g in p["groups"]:
        chk(f"{g['id']} 结果字段为占位符",
            g["result_placeholder"].startswith("{{TODO_ablation_")
            and g["result_placeholder"].endswith("}}"))
        chk(f"{g['id']} 无伪造结果键",
            not any(k in g for k in ("result", "detect_rate", "k", "n", "catch")))
    # A5 必须 BLOCKED（结构性阻塞）
    a5 = next(g for g in p["groups"] if g["id"] == "A5")
    chk("A5 登记为 BLOCKED", a5["feasible"] is False)
    chk("A5 阻塞理由提到 select_assets", "select_assets" in " ".join(a5["blockers"]))
    # A0 应 READY（baseline_fd.json 存在）
    a0 = next(g for g in p["groups"] if g["id"] == "A0")
    chk("A0 READY（baseline_fd.json 已存在）", a0["feasible"] is True, f"({a0['blockers']})")
    # A1 需 git 回退
    a1 = next(g for g in p["groups"] if g["id"] == "A1")
    chk("A1 登记 git_revert=True", a1["git_revert"] is True)
    # A2 盲态不可逆说明
    a2 = next(g for g in p["groups"] if g["id"] == "A2")
    chk("A2 无结果键", not any(k in a2 for k in ("result", "k", "n")))
    # 关键对照
    chk("对照共 5 条（A0 vs A1..A5）", len(p["contrasts"]) == 5)
    key = next(c for c in p["contrasts"] if "A5" in c["contrast"])
    chk("A0−A5 为关键对照", "关键对照" in key["note"])
    chk("A0−A5 Δ 为占位符", key["delta_placeholder"].startswith("{{TODO_delta_"))
    chk("A2 对照用独立设计", next(c for c in p["contrasts"] if "A2" in c["contrast"])
        ["design"] == "unpaired")
    chk("A1 对照用配对设计", next(c for c in p["contrasts"] if "A1" in c["contrast"])
        ["design"] == "paired")
    # 设计文档存在
    chk("设计文档存在", DESIGN_DOC.is_file())
    print(f"ablation_671b selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _write_json(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671b A 段：ablation 六组设计 + 可执行框架（不跑实验）")
    ap.add_argument("--dry-run", action="store_true", help="六组可行性体检（只读）")
    ap.add_argument("--run", action="store_true",
                    help="登记 run plan（**不跑实验**；BLOCKED 组如实登记）")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--json", action="store_true", help="机读输出")
    ap.add_argument("--only", default=None, help="只处理某一组（A0–A5）")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()

    if a.only:
        grp = next((x for x in ABLATIONS if x["id"] == a.only.upper()), None)
        if grp is None:
            print(f"未知组：{a.only}（应为 A0–A5）", file=sys.stderr)
            return 2
        doc = plan(grp)
        print(json.dumps(doc, ensure_ascii=False, indent=2) if a.json else
              f"[{doc['status']}] {doc['id']} {doc['name']}\n"
              f"  命令: {doc['command']}\n"
              f"  阻塞: {'；'.join(doc['blockers']) or '无'}")
        return 0 if doc["feasible"] else 1

    p = build_plan()
    if a.json:
        print(json.dumps(p, ensure_ascii=False, indent=2))
    else:
        print(summary(p))
    if a.run:
        _write_json(PLAN_PATH, p)
        print(f"[671b] 已登记 run plan → {PLAN_PATH.relative_to(ROOT).as_posix()}")
        print(f"[671b] READY {p['summary']['n_ready']} / BLOCKED {p['summary']['n_blocked']}"
              f"（{', '.join(p['summary']['blocked_ids']) or '无'}）"
              " —— **本批不跑实验，所有结果为占位符**")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
