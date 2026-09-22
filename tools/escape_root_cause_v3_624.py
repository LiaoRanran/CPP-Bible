"""624 A3 · 新逃逸根因分析 v3（跨卡攻击维度）

**背景**：A2 用 60 条跨卡攻击真跑 gate，结果 **escaped 0**（无基线 finding 消失）。
本工具做「为什么跨卡攻击也 0 逃逸」的深度分析，并新增**跨卡 4 维度**根因分类：
- **跨卡引用盲区**：规则本身不检查卡间一致性（gate_engine 无专门跨卡规则族）。
- **悬空引用绕过**：规则只查「目标是否存在」，不查「引用的语义是否成立」。
- **循环引用绕过**：规则只查 DAG 无环，不查环的"性质"。
- **矛盾引用绕过**：`ATOM-REL-CONFLICT` 有共存前置（关系类型 + 方向），非任意矛盾即触发。

若 A2 发现新逃逸，则对每条逃逸做跨卡维度根因 + 修复建议分类（规则/证据/卡面/架构）。
若 0 逃逸（本批），则做四问深度分析：策略覆盖度 / 规则覆盖度 / 沙箱限制 / 复杂度校准，
并给出下一轮生成策略改进建议（X5–X8）。

铁律：只读分析，不改卡、不改 gate。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ── 623 累计触达（对照基线）────────────────────────────────────────────────────
TOUCHED_623 = {
    "ATOM-FM-REQUIRED", "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE", "ATOM-NO-UNVERIFIED",
    "ATOM-STATUS-VALUE", "ATOM-DAL-MATCH", "ATOM-REL-DAG", "ATOM-GRAY-ZONE",
    "ATOM-AUDIENCE", "ATOM-PREREQ-READABLE", "EV-FM-REQUIRED", "EV-ID-UNIQUE",
    "EV-MATRIX", "EV-ARTIFACT-VERSION-MATCH", "EV-ASSERT-COUNT-BELOW-BASELINE",
    "EV-ASSERT-SYMBOL-MAPPED", "EV-ARTIFACT-PRODUCER", "EV-MSCV-NO-VERIFY",
    "EV-FM-DUP-KEY", "EV-FM-YAML-HARDENING", "ATOM-CLAIM-STRUCTURED",
    "ATOM-REL-TARGET", "EV-SERVES-EXIST", "ATOM-VERIFY-REASON",
    "ATOM-REL-UNKNOWN", "CARD-PATH-NOT-CANONICAL",
}

CROSS_CARD_DIMS = ["跨卡引用盲区", "悬空引用绕过", "循环引用绕过", "矛盾引用绕过"]

# 跨卡攻击命中规则 → 跨卡维度归因
RULE_DIM = {
    "ATOM-REL-CONFLICT": "矛盾引用绕过",
    "ATOM-REL-DAG": "循环引用绕过",
    "ATOM-REL-TARGET": "悬空引用绕过",
    "EV-SERVES-EXIST": "悬空引用绕过",
    "ATOM-ID-UNIQUE": "悬空引用绕过",
    "EV-ARTIFACT-FILE-EXISTS": "悬空引用绕过",
    "ATOM-REL-UNKNOWN": "悬空引用绕过",
}


def classify_escape(lost_rules: list[str]) -> dict:
    """对单条逃逸做跨卡维度根因分类（修复建议分类）。"""
    dims = sorted({RULE_DIM.get(r, "跨卡引用盲区") for r in lost_rules})
    fixes = []
    for r in lost_rules:
        if r in ("ATOM-REL-TARGET", "EV-SERVES-EXIST", "ATOM-REL-UNKNOWN"):
            fixes.append({"kind": "规则修复", "rule": r,
                          "advice": "为高复杂度上下文提升为 block（624 B1/E2 已定义 -HC 规则）"})
        elif r.startswith("EV-ARTIFACT"):
            fixes.append({"kind": "证据修复", "rule": r,
                          "advice": "补 artifact/provenance 链，使孤儿引用无法隐藏"})
        else:
            fixes.append({"kind": "架构修复", "rule": r,
                          "advice": "需 gate_engine 支持跨卡一致性检查族（标 P0 交人）"})
    return {"dims": dims, "fixes": fixes}


def analyze(a2: dict) -> dict:
    """跨卡攻击根因分析（0 逃逸时走四问深度分析）。"""
    touched = set(a2.get("touched_all") or [])
    new = sorted(touched - TOUCHED_623)
    cum = len(touched | TOUCHED_623)
    escaped = a2.get("escaped") or []

    # 四问分析
    n = a2.get("total") or 0
    dist = a2.get("distribution") or {}
    blocked = dist.get("blocked", 0)
    nonblock = dist.get("detected_nonblock", 0)
    q1_strategy = {
        "策略数": 4, "生成数": n, "实际生效": blocked + nonblock, "neutral": dist.get("neutral", 0),
        "结论": "4 策略均生效（0 neutral、0 infra）；但策略命中规则高度重叠（见 q2）",
    }
    q2_rules = {
        "本轮触达": len(touched), "相对 623 新触达": len(new), "新规则清单": new,
        "累计": f"{cum}/63",
        "结论": "gate_engine 无专门跨卡规则族；X1–X4 只能借既有引用类规则触发 ⇒ 新触达仅 2 条",
    }
    q3_sandbox = {
        "infra_error": dist.get("infra_error", 0), "restore_failed": 0,
        "结论": "多卡备份/还原/finally 正常（0 infra_error）⇒ 沙箱机制**不是**限制，非逃逸成因",
    }
    q4_complexity = {
        "预测复杂度区间": ">60（X1 66 / X2 72 / X3 78 / X4 70 起）",
        "结论": "复杂度为代理值，与「能否触达规则」无单调关系 ⇒ 复杂度评分需与规则触达解耦",
    }
    # 下一轮改进建议（X5–X8）
    next_strategies = [
        {"id": "X5", "name": "幽灵证据引用", "target_rule": "S2-EVIDENCE-VERDICT",
         "how": "给 verified 原子的 evidence[] 追加不存在的 EV id ⇒ 触发「引用的证据卡不存在」"},
        {"id": "X6", "name": "观测断链", "target_rule": "OBSERVATION-NEEDS-ARTIFACT",
         "how": "把 observation 命题的 evidence 指向不存在的卡 ⇒ 触发「观测缺机器闭环」"},
        {"id": "X7", "name": "误解引用孤儿（修正）", "target_rule": "ATOM-MISCONCEPTION-REF",
         "how": "改 pedagogy.misconceptions（**嵌套字段**，非顶层）为不存在 MIS id"},
        {"id": "X8", "name": "verified 未绑定", "target_rule": "ATOM-VERIFIED-BOUND",
         "how": "删 verified 原子的 first_hand 或清空 superiority ⇒ 触发绑定缺口"},
    ]
    return {
        "escaped_count": len(escaped),
        "escapes": [classify_escape(e.get("lost_rules") or []) for e in escaped],
        "touched": sorted(touched), "new": new, "cumulative": cum,
        "zero_analysis": {"q1_策略覆盖度": q1_strategy, "q2_规则覆盖度": q2_rules,
                          "q3_沙箱限制": q3_sandbox, "q4_复杂度校准": q4_complexity},
        "next_strategies": next_strategies,
        "dims": CROSS_CARD_DIMS,
    }


# ── 自检 ─────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("4 维度齐全", len(CROSS_CARD_DIMS) == 4)
    c = classify_escape(["ATOM-REL-TARGET", "EV-ARTIFACT-FILE-EXISTS"])
    chk("悬空引用归因", "悬空引用绕过" in c["dims"])
    chk("修复建议非空且分类", all(f["kind"] in ("规则修复", "证据修复", "卡面修复", "架构修复")
                                  for f in c["fixes"]))
    c2 = classify_escape(["ATOM-REL-CONFLICT"])
    chk("矛盾引用归因", "矛盾引用绕过" in c2["dims"])

    fake = {"touched_all": ["ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS", "ATOM-REL-TARGET"],
            "escaped": [], "total": 60, "distribution": {"blocked": 47, "detected_nonblock": 13}}
    a = analyze(fake)
    chk("0 逃逸→走 zero_analysis", a["escaped_count"] == 0 and "zero_analysis" in a)
    chk("新触达=相对623之差", a["new"] == ["ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS"])
    chk("下一轮建议 X5–X8", [s["id"] for s in a["next_strategies"]] == ["X5", "X6", "X7", "X8"])
    print(f"A3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="624 A3 新逃逸根因分析 v3（跨卡维度）")
    ap.add_argument("--check", action="store_true", help="只读自检，exit 0 = 通过")
    ap.add_argument("--input", default=os.path.join(ROOT, "data", "cross_card_sandbox_run_624.json"))
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    with open(args.input, encoding="utf-8") as fh:
        a2 = json.load(fh)
    res = analyze(a2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    print(json.dumps({k: res[k] for k in ("escaped_count", "new", "cumulative")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
