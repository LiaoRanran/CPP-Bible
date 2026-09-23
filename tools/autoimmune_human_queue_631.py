"""631 B2 · human 90 条字段清单（纯标准库，只读）

630 A2 方案甲把 132 条 warn 分成 auto 42 / human 90；B1 已执行 auto 42，
本工具为 **human 90** 出逐条清单：

- 卡 ID / 命题 / 字段 / **为什么不能 auto** / 建议值（给候选，**不代填**）/ 优先级；
- 输出 `data/autoimmune_human_queue_631.md`（按优先级排序）
  与 `data/autoimmune_human_queue_631.jsonl`（每行一条，便于后续批量导入）；
- **§零.3**：不代签人审、不做语义判断 ⇒ 本工具**只输出清单**，一个字段都不填。

优先级规则（显式、可审）：
| 条件 | 优先级 | 理由 |
|---|---|---|
| `signed_by` | 高 | 机器永不代签；且填得不规范会把 warn **升格为 block**（630 A3 悲观情景） |
| `object` 且**无**候选 | 高 | 需裁决：改 object / 改 claim_type / 补概念条目 |
| `object` 且有候选 | 中 | 人只需确认候选是否正确 |
| 其他 | 低 | — |
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "autoimmune_human_queue_631.md")
OUT_JSONL = os.path.join(ROOT, "data", "autoimmune_human_queue_631.jsonl")

PRIORITY_RULES = [
    ("signed_by", None, "高", "§零.3 机器永不代签人审；填得不规范会把 warn 升格为 block"
                              "（630 A3 悲观情景实测）"),
    ("object", "no_suggest", "高", "无规范集候选 ⇒ 需裁决：改 object / 改 claim_type / 补概念条目"),
    ("object", "has_suggest", "中", "有规范集内最相似候选 ⇒ 人只需确认"),
]


def plan_human() -> list[dict[str, Any]]:
    """630 A2 方案甲里 `mode == human` 的条目（只读调用 630 工具）。"""
    import autoimmune_fix_proposal_630 as P

    return [i for i in P.plan_a()["items"] if i.get("mode") == "human"]


def priority_of(item: dict[str, Any]) -> tuple[str, str]:
    """返回 (优先级, 理由)。"""
    field = str(item.get("field", ""))
    has_suggest = bool(item.get("suggest"))
    for f, cond, prio, why in PRIORITY_RULES:
        if field != f:
            continue
        if cond is None:
            return (prio, why)
        if cond == "no_suggest" and not has_suggest:
            return (prio, why)
        if cond == "has_suggest" and has_suggest:
            return (prio, why)
    if field == "object" and not has_suggest:
        return ("高", PRIORITY_RULES[1][3])
    return ("低", "未匹配高/中规则 ⇒ 默认低（人工复核时再定）")


def rows() -> list[dict[str, Any]]:
    out = []
    for i in plan_human():
        prio, why = priority_of(i)
        out.append({
            "card_id": i.get("card_id"),
            "card_rel": i.get("card_rel"),
            "prop_id": i.get("prop_id"),
            "rule": i.get("rule"),
            "field": i.get("field"),
            "diag_type": i.get("diag_type"),
            "current": i.get("current"),
            "suggest": i.get("suggest"),
            "why_not_auto": i.get("basis") or "（630 A2 未给 basis）",
            "priority": prio,
            "priority_reason": why,
        })
    order = {"高": 0, "中": 1, "低": 2}
    return sorted(out, key=lambda r: (order[r["priority"]], r["card_id"] or "",
                                      r["prop_id"] or "", r["field"] or ""))


def counts(rr: Optional[list[dict[str, Any]]] = None) -> dict[str, int]:
    rr = rr if rr is not None else rows()
    out: dict[str, int] = {}
    for r in rr:
        out[r["priority"]] = out.get(r["priority"], 0) + 1
    return {k: out.get(k, 0) for k in ("高", "中", "低")}


def field_counts(rr: Optional[list[dict[str, Any]]] = None) -> dict[str, int]:
    rr = rr if rr is not None else rows()
    out: dict[str, int] = {}
    for r in rr:
        out[r["field"]] = out.get(r["field"], 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def write_outputs() -> tuple[str, str]:
    rr = rows()
    c, fc = counts(rr), field_counts(rr)
    lines = [
        "# 631 B2 · human 90 条字段清单（**只出清单，不代填**）", "",
        "> §零.3：不代签人审、机器不做语义判断。本清单给出**候选值供人确认**，"
        "一个字段都不代填。", "",
        "## 一、总览", "",
        "| 优先级 | 条数 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in c.items()],
        f"| **合计** | **{len(rr)}** |", "",
        "| 字段 | 条数 |", "|---|---|",
        *[f"| `{k}` | {v} |" for k, v in fc.items()], "",
        "> `signed_by` 全部为**高**：机器永不代签（§零.3），且填错会把 warn 升格为 block。",
        "",
        "## 二、逐条清单（按优先级）", "",
        "| # | 优先级 | 卡 | 命题 | 字段 | 当前值 | 建议候选 | 为什么不能 auto |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rr, 1):
        cur = str(r["current"] or "（缺失）").replace("|", "\\|")[:28]
        sug = str(r["suggest"] or "—").replace("|", "\\|")[:24]
        why = str(r["why_not_auto"]).replace("|", "\\|")[:40]
        lines.append(f"| {i} | **{r['priority']}** | `{r['card_id']}` | {r['prop_id']} | "
                     f"`{r['field']}` | {cur} | {sug} | {why} |")
    lines += [
        "", "## 三、机器可读输出", "",
        f"- JSONL：`data/autoimmune_human_queue_631.jsonl`（{len(rr)} 行，每行一条，"
        "字段含 card_id/prop_id/field/suggest/priority/why_not_auto）", "",
        "## 四、诚实登记", "",
        "1. **建议候选来自规范集相似度**（630 A2 `suggest_object`），**不是语义正确性保证**；"
        "人可拒绝候选并选择「改 claim_type」或「补概念条目」；",
        "2. `signed_by` 的建议值写作 `human:<在册实名>`——**不是让机器填**，"
        "而是提醒：该字段只能由**在册人**签；",
        "3. 优先级规则是**人定**的（见本文件 `PRIORITY_RULES`），可审可改；"
        "若人认为 `object` 应先于 `signed_by`，改这张表即可重排；",
        "4. 本工具**不写任何卡**（只读 630 方案 + 输出清单文件）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSONL, "w", encoding="utf-8", newline="\n") as fh:
        for r in rr:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return OUT_MD, OUT_JSONL


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rr = rows()
    chk("human 条目 = 90 条", len(rr) == 90, f"({len(rr)})")
    chk("全部字段都是 signed_by 或 object（机器绝不代填的类型）",
        all(r["field"] in ("signed_by", "object") for r in rr),
        f"({sorted({r['field'] for r in rr})})")
    chk("signed_by 全部为高优先级",
        all(r["priority"] == "高" for r in rr if r["field"] == "signed_by"))
    chk("无候选的 object 为高、有候选为中",
        all((r["priority"] == "高") if not r["suggest"] else (r["priority"] == "中")
            for r in rr if r["field"] == "object"))
    chk("优先级计数合计 = 90", sum(counts(rr).values()) == 90, f"({counts(rr)})")
    chk("每行都有『为什么不能 auto』", all(r["why_not_auto"] for r in rr))

    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain", "--", "atoms", "evidence"],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    rows()
    write_outputs()
    after = snap()
    chk("只读：不写受控目录", before == after)
    chk("报告 + JSONL 存在且行数一致",
        os.path.exists(OUT_MD)
        and os.path.exists(OUT_JSONL)
        and sum(1 for _ in open(OUT_JSONL, encoding="utf-8")) == len(rr))
    print(f"B2 human queue check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 B2 human 90 条清单（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写清单 md + jsonl")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        md, jl = write_outputs()
        print(f"written {md} + {jl}")
        return 0
    rr = rows()
    if args.json:
        print(json.dumps({"counts": counts(rr), "fields": field_counts(rr)},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"human_items={len(rr)} counts={counts(rr)} fields={field_counts(rr)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
