"""627 C1 · Blind Review 执行包（Top 10）+ 人审操作指南

**背景**：626 C1 已实现 Blind Review v1（Pass A 盲审禁 AI 推荐 + Pass B 解盲一致性）。
但**真实 Blind Review 从未执行**——这是把「独立人类确认强度」从 0 变为非 0 的**唯一途径**。

**本工具（627）**：为人审者准备**真实可执行的盲审包**：
1. 从 626 B3 的「唯一审查账本」（`review_item_ledger.jsonl`，93 unique）中，
   按 `ambiguity_score` 取 **Top 10** 最高歧义项，作为首批盲审优先级。
2. **盲审包严格遵循 Pass A 盲性**：每条只呈现
   `问题（edge + 方向）+ 可选证据引用 + 空白决策位`，**绝不呈现既有 Authority 结果 / AI 推荐**
   （否则违反 Pass A，盲审失效）。
3. 附带**人审操作指南**（Pass A 怎么做、Pass B 怎么做、automation_bias 风险、如何回填）。

**硬边界**：本工具**只生成执行包与指南，绝不代执行、绝不写入任何 ledger / 受控目录**。
真实盲审由人审者执行，结果经 627 C2 的回填工具（同样不自动写入）交人落库。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

LEDGER = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
OUT_PACK = os.path.join(ROOT, "data", "blind_review_pack_top10_627.json")
OUT_GUIDE = os.path.join(ROOT, "data", "blind_review_human_guide_627.md")
TOP_N = 10

# 盲审包禁止泄露的字段（Pass A 盲性）
_LEAK_FIELDS = {"current_decision_id", "result", "authority_result",
                "recommendation", "ai_recommendation", "decision", "status"}


def load_items() -> list[dict]:
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(line) for line in open(LEDGER, encoding="utf-8") if line.strip()]


def top10() -> list[dict]:
    items = load_items()
    items.sort(key=lambda x: float(x.get("ambiguity_score") or 0), reverse=True)
    return items[:TOP_N]


def build_pack() -> dict:
    items = top10()
    pack = []
    for it in items:
        # 仅保留盲审必需信息，剥离任何既有裁定（Pass A 盲性）
        entry = {
            "review_item_id": it.get("review_item_id"),
            "target_type": it.get("target_type"),
            "target_id": it.get("target_id"),
            "review_revision": it.get("review_revision"),
            "question": _question(it),
            "evidence_refs": it.get("evidence_refs") or [],
            # 决策位：留空，由人审者填写
            "human_decision": None,
            "human_rationale": None,
        }
        # 防御性：任何泄露字段都不进入包
        for f in _LEAK_FIELDS:
            entry.pop(f, None)
        pack.append(entry)
    return {"top_n": len(pack),
            "source": "review_item_ledger.jsonl (626 B3, 93 unique)",
            "blindness": "Pass A: 不含任何既有 Authority 结果 / AI 推荐",
            "items": pack}


def _question(it: dict) -> str:
    tgt = it.get("target_id") or ""
    return (f"对攻击边 {tgt} 的独立人类裁定："
            f"该攻击是否成立（approve/reject/modify）？"
            f"请仅依据证据独立判断，不要参考任何既有结论。")


def write_guide() -> None:
    lines = [
        "# 627 C1 · Blind Review 人审操作指南",
        "",
        "## 零、为什么需要你（人）",
        "- 当前「独立人类确认强度 = 0」：622 的 30 条执行被标注为 `user_authorized_execution`，"
        "**不计入独立人审**。",
        "- 把强度从 0 变非 0 的**唯一途径**是真实 Blind Review——机器无法代办。",
        "",
        "## 一、Pass A（盲审，最重要）",
        "1. 打开 `blind_review_pack_top10_627.json`，逐条阅读 `question` 与 `evidence_refs`。",
        "2. **在查看任何既有结论前**，先填写 `human_decision` 与 `human_rationale`。",
        "3. ⚠ **严禁**参考包中以外提供的「AI 推荐 / Authority 结果」——一旦在盲态下看到推荐即视为盲审失效。",
        "4. automation_bias 风险：人对 AI 推荐有顺从倾向，盲审的目的正是隔离该偏差。",
        "",
        "## 二、Pass B（解盲一致性）",
        "1. 盲审完成后，对照 626 C1 的 `blind_review_v1_626.py` 做解盲：",
        "   - 将你的 `human_decision` 与既有 Authority `result` 比对。",
        "2. 记录一致性比例与分歧项；对分歧项标注 `automation_bias_risk`（是否因看到推荐而动摇）。",
        "",
        "## 三、回填（不自动写入）",
        "- 结果经 `blind_review_backfill_627.py`（627 C2）**生成回填条目**，但**不自动落库**；",
        "  最终写入 Authority Ledger 需人明确确认（交人项 #2）。",
        "",
        "> 本指南与执行包**不修改任何 ledger / 受控目录**；盲审执行本身由人完成。",
    ]
    with open(OUT_GUIDE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    pack = build_pack()
    chk("生成 Top 10 执行包", pack["top_n"] == TOP_N, f"(n={pack['top_n']})")
    # 盲性：包中不含任何泄露字段
    leak = False
    for it in pack["items"]:
        if any(f in it for f in _LEAK_FIELDS):
            leak = True
    chk("盲审包不含既有裁定（Pass A 盲性）", not leak)
    # 每条都有空白决策位
    chk("每条均有空白 human_decision", all("human_decision" in it for it in pack["items"]))
    print(f"C1 blind review pack check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 C1 Blind Review 执行包")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="输出执行包 + 指南")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    pack = build_pack()
    with open(OUT_PACK, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(pack, fh, ensure_ascii=False, indent=2)
    if args.report:
        write_guide()
        print(f"written {OUT_PACK} + {OUT_GUIDE}")
    else:
        print(json.dumps(pack, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
