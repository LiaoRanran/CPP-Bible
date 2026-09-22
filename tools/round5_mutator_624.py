"""624 A4 · 闭环第五轮（针对性跨卡 mutation，策略 X5–X8）

**依据**：A3 的四问分析指出——X1–X4 只触达引用类规则（新增仅 2 条），因为未针对
「嵌套字段 / 证据 verdict 绑定 / 命题-工件闭环 / verified 绑定」构造编辑。本工具据 A3 建议
新增 4 种策略（X5–X8），各生成 10 条、共 40 条，复用 A1 的多卡沙箱真跑 gate。

| 策略 | 目标规则 | 构造 |
|---|---|---|
| X5 幽灵证据引用 | S2-EVIDENCE-VERDICT | verified 原子 `evidence[]` 追加不存在的 EV id |
| X6 观测断链 | OBSERVATION-NEEDS-ARTIFACT | observation 命题的 `evidence` 指向不存在的卡 |
| X7 误解引用孤儿（修正） | ATOM-MISCONCEPTION-REF | 改**嵌套** `pedagogy.misconceptions` 为不存在 MIS id |
| X8 verified 未绑定 | ATOM-VERIFIED-BOUND | 删 verified 原子 `first_hand` |

铁律：只读生成 + 沙箱临时改（备份+还原），不修改原始卡、不改 gate_engine；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cross_card_attack_624 as cc  # noqa: E402

ROUND5_PREDICT = {
    "X5": ["S2-EVIDENCE-VERDICT"],
    "X6": ["OBSERVATION-NEEDS-ARTIFACT"],
    "X7": ["ATOM-MISCONCEPTION-REF"],
    "X8": ["ATOM-VERIFIED-BOUND"],
}


def _key_line(text: str, key: str):
    return re.search(rf"(?m)^{re.escape(key)}\s*:.*$", text)


def plan_edit_r5(content: dict, text: str):
    """X5–X8 新编辑原语；否则回落到 624 A1 的 plan_edit_624。"""
    op = content.get("op")

    if op == "APPEND_EVIDENCE":  # X5：给 evidence[] 追加幽灵 id
        val = content.get("value", "EV-NOPE-999")
        m = _key_line(text, "evidence")
        if not m:
            m = _key_line(text, "id")
            if not m:
                return None
            return text[:m.end()] + f"\nevidence:\n  - {val}" + text[m.end():], \
                f"新建 evidence → {val}"
        line = m.group(0)
        if re.search(r"evidence\s*:\s*\[", line):
            inline = re.search(r"evidence\s*:\s*\[([^\]]*)\]", line)
            if inline is None:
                return None
            items = [x.strip() for x in inline.group(1).split(",") if x.strip()]
            items.append(val)
            new = text[:m.start()] + f"evidence: [{', '.join(items)}]" + text[m.end():]
            return new, f"evidence 追加 {val}"
        # 块列表：在 evidence: 行后插入
        return text[:m.end()] + f"\n  - {val}" + text[m.end():], f"evidence 追加 {val}"

    if op == "SET_PROP_EVIDENCE":  # X6：observation 命题 evidence → 幽灵
        val = content.get("value", "EV-NOPE-999")
        mm = re.search(r"(?m)^(\s*)claim_type\s*:\s*observation\s*$", text)
        if not mm:
            return None
        tail = text[mm.end():]
        em = re.search(r"(?m)^(\s*)evidence\s*:\s*\[([^\]]*)\]\s*$", tail)
        if not em:
            return None
        start = mm.end() + em.start()
        end = mm.end() + em.end()
        return text[:start] + f"{em.group(1)}evidence: [{val}]" + text[end:], \
            f"observation 命题 evidence → {val}"

    if op == "SET_PED_MIS":  # X7：嵌套 pedagogy.misconceptions → 幽灵
        val = content.get("value", "MIS-NOPE-999")
        m = re.search(r"(?m)^(\s*)misconceptions\s*:\s*.*$", text)
        if not m:
            return None
        return text[:m.start()] + f"{m.group(1)}misconceptions: [{val}]" + text[m.end():], \
            f"pedagogy.misconceptions → {val}"

    if op == "DEL_FIRST_HAND":  # X8：删 first_hand
        m = _key_line(text, "first_hand")
        if not m:
            return None
        return text[:m.start()] + text[m.end():].lstrip("\n"), "删除 first_hand"

    return cc.plan_edit_624(content, text)


class Round5Sandbox(cc.CrossCardSandbox):
    """用 X5–X8 原语覆盖编辑原语的跨卡沙箱（备份/还原仍走 A1 修复后的 apply_multi）。"""

    def _plan(self, content: dict, text: str):
        return plan_edit_r5(content, text)


def _text(card_rel: str) -> str:
    return open(os.path.join(ROOT, card_rel), encoding="utf-8").read()


def generate_round5(inv: dict, per_strategy: int = 10) -> list[dict]:
    atoms = inv["atoms"]
    out: list[dict] = []

    def pick(marker, need_verified=False, exclude=()):
        res = []
        for a in atoms:
            if a["card"] in exclude or a["id"] in exclude:
                continue
            if need_verified and "verified" not in (a["status"] or "").lower():
                continue
            if re.search(marker, _text(a["card"])):
                res.append(a)
        return res

    # X5 幽灵证据引用：verified 原子 evidence[] 追加幽灵 EV
    pool5 = pick(r"(?m)^\s*evidence\s*:", need_verified=True) or pick(r"(?m)^\s*evidence\s*:")
    for i in range(per_strategy):
        a = pool5[i % len(pool5)] if pool5 else None
        if not a:
            break
        out.append({"mutation_id": f"X5-{i+1:03d}", "strategy": "X5", "attack_type": "幽灵证据引用",
                    "complexity": 74, "predicted_rules": ROUND5_PREDICT["X5"],
                    "edits": [{"card": a["card"], "op": "APPEND_EVIDENCE", "value": "EV-NOPE-999"},
                              {"card": a["card"], "op": "APPEND_EVIDENCE", "value": "EV-GHOST-624"}]})

    # X6 观测断链：observation 命题 evidence → 幽灵
    pool6 = pick(r"(?m)^\s*claim_type\s*:\s*observation\s*$")
    for i in range(per_strategy):
        a = pool6[i % len(pool6)] if pool6 else None
        if not a:
            break
        out.append({"mutation_id": f"X6-{i+1:03d}", "strategy": "X6", "attack_type": "观测断链",
                    "complexity": 76, "predicted_rules": ROUND5_PREDICT["X6"],
                    "edits": [{"card": a["card"], "op": "SET_PROP_EVIDENCE",
                               "value": "EV-NOPE-999"}]})

    # X7 误解引用孤儿（嵌套 pedagogy.misconceptions）
    pool7 = pick(r"(?m)^\s*misconceptions\s*:")
    for i in range(per_strategy):
        a = pool7[i % len(pool7)] if pool7 else None
        if not a:
            break
        out.append({"mutation_id": f"X7-{i+1:03d}", "strategy": "X7", "attack_type": "误解引用孤儿",
                    "complexity": 72, "predicted_rules": ROUND5_PREDICT["X7"],
                    "edits": [{"card": a["card"], "op": "SET_PED_MIS", "value": "MIS-NOPE-999"}]})

    # X8 verified 未绑定：删 first_hand
    pool8 = pick(r"(?m)^first_hand\s*:\s*true\s*$", need_verified=True)
    for i in range(per_strategy):
        a = pool8[i % len(pool8)] if pool8 else None
        if not a:
            break
        out.append({"mutation_id": f"X8-{i+1:03d}", "strategy": "X8", "attack_type": "verified未绑定",
                    "complexity": 71, "predicted_rules": ROUND5_PREDICT["X8"],
                    "edits": [{"card": a["card"], "op": "DEL_FIRST_HAND"}]})

    return out


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    text = ("---\nid: ATOM-X\nstatus: verified\nfirst_hand: true\n"
            "evidence: [EV-A]\nclaim_structured:\n  - id: p1\n    claim_type: observation\n"
            "    evidence: [EV-A]\npedagogy:\n  misconceptions: [MIS-A]\n---\nbody\n")
    chk("X5 APPEND_EVIDENCE 可行",
        (plan_edit_r5({"op": "APPEND_EVIDENCE", "value": "EV-NOPE-999"}, text) or [None])[0] is not None)
    e6 = plan_edit_r5({"op": "SET_PROP_EVIDENCE", "value": "EV-NOPE-999"}, text)
    chk("X6 SET_PROP_EVIDENCE 命中 observation evidence", e6 is not None and "EV-NOPE-999" in e6[0])
    e7 = plan_edit_r5({"op": "SET_PED_MIS", "value": "MIS-NOPE-999"}, text)
    chk("X7 SET_PED_MIS 可行", e7 is not None and "MIS-NOPE-999" in e7[0])
    e8 = plan_edit_r5({"op": "DEL_FIRST_HAND"}, text)
    chk("X8 DEL_FIRST_HAND 可行", e8 is not None and "first_hand" not in e8[0])

    inv = cc.load_inventory()
    muts = generate_round5(inv, per_strategy=10)
    chk("生成 40 条（4 策略各 10）", len(muts) == 40)
    chk("X5–X8 覆盖", {m["strategy"] for m in muts} == {"X5", "X6", "X7", "X8"})
    chk("目标规则齐全", {r for m in muts for r in m["predicted_rules"]} ==
        {"S2-EVIDENCE-VERDICT", "OBSERVATION-NEEDS-ARTIFACT",
         "ATOM-MISCONCEPTION-REF", "ATOM-VERIFIED-BOUND"})
    print(f"A4 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="624 A4 闭环第五轮（X5–X8）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--gen", action="store_true", help="生成并打印 40 条")
    ap.add_argument("--run", action="store_true", help="沙箱实跑（真跑 gate）")
    ap.add_argument("--out")
    ap.add_argument("--per-strategy", type=int, default=10)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    inv = cc.load_inventory()
    muts = generate_round5(inv, per_strategy=args.per_strategy)
    if args.gen:
        print(json.dumps(muts, ensure_ascii=False, indent=2))
        return 0
    if args.run:
        res = cc.run_batch(muts, sb=Round5Sandbox())
        res["predicted_rules"] = sorted({r for m in muts for r in m["predicted_rules"]})
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump({"mutations": muts, **res}, fh, ensure_ascii=False, indent=2)
        print(json.dumps({k: v for k, v in res.items() if k != "rows"}, ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
