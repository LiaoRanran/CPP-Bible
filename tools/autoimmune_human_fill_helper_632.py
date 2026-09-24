"""632 C1 · human 90 交互式填充助手（纯标准库，只读，绝不代决策）。

读取 631 留下的 `data/autoimmune_human_queue_631.jsonl`（90 条 human 字段），
对每条输出给「人」看的辅助信息（不写卡、不替人裁决）：
- 字段定位：atom 卡 path + prop_id 所在行号；
- 建议候选值：object 取队列 `suggest`（若有），signed_by 给「human:<在册实名>」提醒（机器不代签）；
- 权威依据：rule + §零.3（机器永不代签人审）/ ATOM-CLAIM-CONCEPT-NORMALIZED（object 为语义判断）。

铁律：纯标准库、新工具必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
QUEUE = REPO_ROOT / "data" / "autoimmune_human_queue_631.jsonl"


def load_queue(path: Path = QUEUE) -> list[dict]:
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def locate_in_card(card_rel: str, prop_id: str, root: Path = REPO_ROOT) -> tuple[int, str]:
    """返回 (行号(1-based), 该行片段)；找不到返回 (0, '')。"""
    p = root / card_rel
    if not p.is_file():
        return (0, "")
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if prop_id in ln:
            return (i, ln.strip()[:80])
    return (0, "")


def candidate_for(item: dict) -> str:
    """建议候选值（不臆造；signed_by 只给提醒，不代签）。"""
    field = item.get("field")
    if field == "signed_by":
        return "human:<在册实名>（机器永不代签，§零.3；填错会把 warn 升 block）"
    # object
    sug = item.get("suggest")
    if sug:
        return str(sug)
    return "（无候选：须人裁决 → 改 object / 改 claim_type / 补概念条目）"


def authority_for(item: dict) -> str:
    rule = item.get("rule", "")
    field = item.get("field")
    if field == "signed_by":
        return f"{rule}；§零.3 机器永不代签人审；填不规范会把 warn 升格为 block"
    return f"{rule}；object 为语义判断，机器不改（631 B2 清单，why_not_auto 见队列）"


def synthesize(item: dict, root: Path = REPO_ROOT) -> dict:
    line, snippet = locate_in_card(item.get("card_rel", ""), item.get("prop_id", ""), root)
    return {
        "card_id": item.get("card_id"),
        "prop_id": item.get("prop_id"),
        "field": item.get("field"),
        "location": f"{item.get('card_rel')}:{line}" if line else item.get("card_rel"),
        "loc_snippet": snippet,
        "candidate": candidate_for(item),
        "authority": authority_for(item),
        "priority": item.get("priority"),
    }


def digest(items: list[dict], root: Path = REPO_ROOT) -> list[dict]:
    return [synthesize(it, root) for it in items]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 C1 human 90 交互式填充助手（只读）")
    ap.add_argument("--check", action="store_true", help="只读：打印待办计数与样例，exit 0")
    ap.add_argument("--queue", default=str(QUEUE))
    ap.add_argument("--out", default=None, help="写 digest md 到该路径")
    args = ap.parse_args(argv)
    items = load_queue(args.queue)
    if args.check:
        pri = {}
        for it in items:
            pri[it.get("priority")] = pri.get(it.get("priority"), 0) + 1
        print(f"632 C1 --check OK：human 待填 {len(items)} 条，优先级 {pri}")
        for it in items[:3]:
            s = synthesize(it)
            print(f"  样例 {s['location']} [{s['field']}] 候选={s['candidate'][:40]} | {s['authority'][:40]}")
        return 0
    recs = digest(items)
    if args.out:
        lines = ["# 632 C1 · human 90 填充辅助（只读，不代决策）", ""]
        for s in recs:
            lines.append(f"## {s['card_id']} / {s['prop_id']} / `{s['field']}`（{s['priority']}）")
            lines.append(f"- 定位：`{s['location']}`  {s['loc_snippet']}")
            lines.append(f"- 候选：{s['candidate']}")
            lines.append(f"- 依据：{s['authority']}")
            lines.append("")
        Path(args.out).write_text("\n".join(lines), encoding="utf-8")
        print("written", args.out)
        return 0
    for s in recs:
        print(f"{s['location']} [{s['field']}] 候选={s['candidate']} | {s['authority']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
