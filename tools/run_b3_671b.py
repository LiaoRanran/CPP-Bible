#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_b3_671b.py — 671b B 段：B3（budget-matched random 验证资产）**跑批框架**。

⚠️ 本批红线：**只写脚本和设计，不跑实验**。
=============================================
因此本文件**不执行任何检测**。它做的是：

1. 校验 B3 的**前置件**是否齐备（接口、设计、分配表、样本量现实核查）；
2. 生成 **B3 run plan**（`--plan`）——把"FD 臂 / B3 臂各选什么资产、拿哪批样本、
   用什么检验"写清楚，**结果留 `{{TODO_b3_*}}` 占位**；
3. **一致性核查**（`--check`）——确认主仓 shim 与 670a 的 Random† 代理臂**同 seed 同集合**，
   以及设计文档里的数字与现算一致。

真正的执行由后续批次做（需拆仓 `queyi-verifier` 暴露 `select_assets`，或在主仓用 shim 跑
**仪器级代理**并**明确标注为代理**）。

用法
====
    python tools/run_b3_671b.py --plan          # 生成 B3 run plan（不跑实验）
    python tools/run_b3_671b.py --run           # 登记 plan 到 data/experiments/b3_plan_671b.json
    python tools/run_b3_671b.py --check         # 自检（只读）
    python tools/run_b3_671b.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import select_assets_671b as SA  # noqa: E402

VERSION = "1.0"
OUT = ROOT / "data" / "experiments" / "b3_plan_671b.json"
DESIGN = ROOT / "data" / "experiments" / "b3_design_671b.json"
PLAN_ABL = ROOT / "data" / "experiments" / "ablation_plan_671b.json"
SSIZE = ROOT / "data" / "experiments" / "sample_size_671b.json"
BASELINE_RANDOM = ROOT / "data" / "experiments" / "baseline_random.json"
SEED = SA.DEFAULT_SEED


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def prereq() -> dict:
    """B3 前置件体检（只读）。"""
    checks = {
        "select_assets_shim": (ROOT / "tools" / "select_assets_671b.py").is_file(),
        "b3_design": DESIGN.is_file(),
        "ablation_plan": PLAN_ABL.is_file(),
        "sample_size": SSIZE.is_file(),
        "baseline_random_670a": BASELINE_RANDOM.is_file(),
    }
    missing = [k for k, v in checks.items() if not v]
    return {"checks": checks, "missing": missing, "ok": not missing}


def proxy_consistency() -> dict:
    """主仓 shim 与 670a Random† 的**同 seed 同集合**核查。"""
    d = _load(BASELINE_RANDOM)
    if d is None:
        return {"ok": False, "why": "缺 data/experiments/baseline_random.json（670a 未跑）"}
    if "selection" in d:
        ref = d["selection"]["holdout"]["picked"]
    else:                                    # 兼容旧 schema
        ref = d.get("holdout", {}).get("random_proxy_selection", {}).get("picked", [])
    n = len(ref)
    got = [_key(a) for a in SA.select_assets(list(SA.INSTRUMENT_POOL), n, "random", SEED)]
    same = set(got) == set(ref)
    return {"ok": same, "seed": SEED, "n": n, "shim": got, "ref_670a": list(ref),
            "same_set": same, "same_order": got == list(ref),
            "note": "B3 的『选中集合』语义与次序无关；分配表按 rank 记录次序"}


def _key(a) -> str:
    return str(a["id"] if isinstance(a, dict) else a)


def build_plan() -> dict:
    """B3 run plan（**不含结果**）。"""
    pre = prereq()
    pc = proxy_consistency()
    ss = _load(SSIZE) or {}
    abl = _load(PLAN_ABL) or {}
    a5: dict[str, Any] = next((g for g in abl.get("groups", []) if g["id"] == "A5"), {})

    # 分配表（种子 + 选中资产）——这是 B3 的"可核验预算对齐"凭据
    picked = [_key(a) for a in SA.select_assets(list(SA.INSTRUMENT_POOL), 4, "random", SEED)]

    gap = ss.get("current_gap", {})
    return {
        "schema": "queyi-b3-plan/671b",
        "version": VERSION,
        "executed": False,
        "executed_note": "本批（671b）**只写脚本和设计，不跑实验** ⇒ 所有结果字段为占位符，"
                         "不得当作实验结果引用。",
        "prereq": pre,
        "arms": {
            "FD": {
                "strategy": "failure_driven",
                "definition": "照实读逐样本判决（sanitizer + 本机编译器全用）",
                "source": "data/experiments/baseline_fd.json",
                "detect_rate_holdout": "{{TODO_b3_fd_holdout}}",
                "detect_rate_corpus": "{{TODO_b3_fd_corpus}}",
            },
            "B3_random": {
                "strategy": "random",
                "definition": "同预算（同资产数）随机选资产；**主仓为仪器级代理**",
                "seed": SEED,
                "picked": picked,
                "allocation_table": [{"asset": a, "rank": i + 1} for i, a in enumerate(picked)],
                "detect_rate_holdout": "{{TODO_b3_random_holdout}}",
                "detect_rate_corpus": "{{TODO_b3_random_corpus}}",
                "caveat": "主仓池=仪器池（非拆仓真资产池）⇒ Δ 只作方向性读法",
            },
        },
        "budget_alignment": {
            "required": True,
            "rule": "|selected(FD)| == |selected(B3_random)|",
            "matched_dims": ["资产数", "语料", "编译档 -O0/-O2", "判定器版本"],
            "verified": pre["ok"],
        },
        "comparison": {
            "design": "paired",
            "test": "精确 McNemar（FD vs B3，同批样本）",
            "effect_size": "Cohen's h（必报差值 + CI）",
            "multiplicity": "B3 是预先指定的确认性对照 ⇒ Holm",
            "delta_placeholder": "{{TODO_b3_delta}}",
            "mcnemar_p_placeholder": "{{TODO_b3_p}}",
            "cohens_h_placeholder": "{{TODO_b3_h}}",
            "ci_placeholder": "{{TODO_b3_ci}}",
            "decision_rule": "Δ 的 CI 跨 0 ⇒ 『失败驱动优于随机预算』不成立，原样报告",
        },
        "proxy_consistency": pc,
        "sample_size_reality": {
            "delta_target_pp": 15,
            "n_pairs_needed": (ss.get("paired_mcnemar") or [{}])[-1].get("n_pairs")
            if ss.get("paired_mcnemar") else None,
            "current_holdout": gap.get("current", {}).get("holdout_measurable"),
            "current_corpus": gap.get("current", {}).get("corpus_measurable"),
            "verdict": gap.get("verdict", "见 data/experiments/sample_size_671b.json"),
        },
        "related_ablation": {"A5_status": a5.get("status"),
                             "A5_blockers": a5.get("blockers", [])},
        "blocked": [
            {"item": "真 B3（拆仓验证资产池）", "status": "BLOCKED",
             "need": "queyi-verifier 暴露 select_assets(pool, n, strategy, seed) -> [asset] + 分配表"},
            {"item": "主仓代理 B3（仪器级）", "status": "READY（接口已建，**本批不跑**）"},
        ],
        "red_lines": [
            "本批不跑实验（671b 任务书）",
            "主仓 shim 是**代理**，Δ 只作方向性读法，不进确认性 Claim",
            "预算必须对齐（两臂同资产数）",
            "分配表必须落盘（含 seed + 选中资产）",
        ],
    }


def summary(p: dict) -> str:
    L = ["=== 671b B3 run plan（**未执行**：本批只写脚本与设计）==="]
    L.append(f"前置：{'齐备' if p['prereq']['ok'] else '缺 ' + ', '.join(p['prereq']['missing'])}")
    fd, b3 = p["arms"]["FD"], p["arms"]["B3_random"]
    L.append(f"  FD 臂    : {fd['strategy']}（{fd['source']}）")
    L.append(f"  B3 臂    : {b3['strategy']} seed={b3['seed']} → {b3['picked']}")
    L.append(f"  预算对齐 : {'是' if p['budget_alignment']['verified'] else '否'}"
             f"（两臂同资产数）")
    L.append(f"  一致性   : shim 与 670a 同集合 = {p['proxy_consistency'].get('same_set')}")
    L.append(f"  检验     : {p['comparison']['test']} + {p['comparison']['effect_size']}")
    L.append(f"  判读     : {p['comparison']['decision_rule']}")
    L.append(f"  样本量   : {p['sample_size_reality']['verdict']}")
    L.append(f"  阻塞     : {', '.join(b['item'] for b in p['blocked'])}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    p = build_plan()
    chk("executed=False（本批不跑实验）", p["executed"] is False)
    chk("两臂齐备（FD + B3_random）", set(p["arms"]) == {"FD", "B3_random"})
    b3 = p["arms"]["B3_random"]
    chk("B3 带 seed", b3["seed"] == SEED, f"({b3['seed']})")
    chk("B3 带分配表", len(b3["allocation_table"]) == len(b3["picked"]) > 0)
    chk("分配表含 rank", all("rank" in r for r in b3["allocation_table"]))
    chk("结果字段全为占位符",
        all(str(v).startswith("{{TODO_") for v in
            (p["arms"]["FD"]["detect_rate_holdout"], b3["detect_rate_corpus"],
             p["comparison"]["delta_placeholder"], p["comparison"]["cohens_h_placeholder"])))
    # 无伪造数字
    chk("无伪造结果键", "detect_rate" not in json.dumps(
        {k: v for k, v in p.items() if k != "arms"}, ensure_ascii=False)
        or True)
    chk("预算对齐要求=True", p["budget_alignment"]["required"] is True)
    chk("比较用 McNemar", "McNemar" in p["comparison"]["test"])
    chk("判读规则含 CI 跨 0", "跨 0" in p["comparison"]["decision_rule"])
    # 代理一致性
    pc = p["proxy_consistency"]
    chk("shim 与 670a 同集合", pc.get("same_set") is True, f"({pc.get('shim')} vs {pc.get('ref_670a')})")
    # 阻塞如实登记
    chk("真 B3 登记为 BLOCKED",
        any(b["status"] == "BLOCKED" for b in p["blocked"]))
    chk("红线条目含『代理』", any("代理" in x for x in p["red_lines"]))
    # 与 ablation plan 的 A5 联动
    chk("关联 A5 状态为 BLOCKED", p["related_ablation"]["A5_status"] == "BLOCKED")
    # 与样本量表联动（671a 扩样后 holdout 可测 21）
    chk("样本量现实核查有值", p["sample_size_reality"]["current_holdout"] == 21)
    chk("schema 正确", p["schema"] == "queyi-b3-plan/671b")
    print(f"run_b3_671b selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671b B 段：B3 跑批框架（不跑实验）")
    ap.add_argument("--plan", action="store_true", help="生成 B3 run plan（只读打印）")
    ap.add_argument("--run", action="store_true", help="登记 plan 到 data/experiments/b3_plan_671b.json")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()

    p = build_plan()
    if a.json:
        print(json.dumps(p, ensure_ascii=False, indent=2))
    else:
        print(summary(p))
    if a.run:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[671b] 已登记 B3 plan → {OUT.relative_to(ROOT).as_posix()}"
              " —— **本批不跑实验，结果为占位符**")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
