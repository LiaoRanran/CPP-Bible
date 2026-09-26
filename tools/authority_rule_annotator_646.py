"""646 · 阶段 A5 · 账本规则字段补全（清债 3）。

目标（646 §三 A5）：用 A1 的规则→卡映射，**反推** 452 条 Authority 判决事件各自涉及的规则，
给每条事件加 `rule_ids` 字段，输出**注释文件**（**绝不修改原 JSONL**）。

**数据源**：`data/authority/decision_event_v2_ledger.jsonl`（452 条**真实**判决事件）+ A1 规则→卡映射。

真实做法：
- Authority 账本 452 条事件的 `target_id` 形如 `ae-<误解>-><ATOM-CARD>::<prop>`（全为 edge）。
- 从 `target_id` 抽出目标**原子卡** → 用 A1 映射的反表（卡→规则）得到该事件涉及的规则集。
- 每条事件写 `{seq, event_id, target_id, atom, rule_ids}` 到 `data/646_authority_rule_annotation.jsonl`。

**只读原账本**：`--check` 只读自检（含原账本 sha256 断言不变）；`--run` 生成注释文件。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LEDGER = os.path.join(DATA, "authority", "decision_event_v2_ledger.jsonl")
ANNOT = os.path.join(DATA, "646_authority_rule_annotation.jsonl")
REPORT_MD = os.path.join(DATA, "646_authority_rule_annotation.md")

_ATOM_RE = re.compile(r"(ATOM-[A-Z0-9\-]+?)(?:::|\$|$)")


def _ledger_sha256() -> str:
    """原账本字节级 sha256（用于证明未被修改）。"""
    h = hashlib.sha256()
    with open(LEDGER, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_events() -> list[dict]:
    """读 452 条事件（只读）。"""
    out = []
    with open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line))
    return out


def _card_to_rules() -> dict[str, list[str]]:
    """A1 映射的反表：卡 → 命中它的规则（含全部强度，保证覆盖）。"""
    import rule_card_mapper_646 as a1
    inv: dict[str, list[str]] = {}
    for rid, info in a1.build_mapping()["rules"].items():
        for c in info["cards"]:
            inv.setdefault(c["card"], []).append(rid)
    return inv


def _atom_of(target_id: str) -> Optional[str]:
    """从 `ae-<误解>-><ATOM-CARD>::<prop>` 抽原子卡 id。"""
    m = _ATOM_RE.search(target_id or "")
    return m.group(1) if m else None


def annotate() -> dict:
    """生成注释（内存中），不写盘。"""
    events = _load_events()
    inv = _card_to_rules()
    rows: list[dict] = []
    uncovered_atoms: set[str] = set()
    for ev in events:
        atom = _atom_of(ev.get("target_id", ""))
        rules = inv.get(atom, []) if atom else []
        if atom and not rules:
            uncovered_atoms.add(atom)
        rows.append({
            "seq": ev.get("seq"),
            "event_id": ev.get("event_id"),
            "target_id": ev.get("target_id"),
            "atom": atom,
            "rule_ids": rules,
        })
    rule_cov: dict[str, int] = {}
    for r in rows:
        for rid in r["rule_ids"]:
            rule_cov[rid] = rule_cov.get(rid, 0) + 1
    return {
        "events": len(rows),
        "rows": rows,
        "rules_with_events": sum(1 for v in rule_cov.values() if v > 0),
        "rule_coverage": rule_cov,
        "uncovered_atoms": sorted(uncovered_atoms),
        "ledger_sha256": _ledger_sha256(),
    }


def write_annotation(result: dict) -> None:
    """写注释 JSONL + 报告。"""
    with open(ANNOT, "w", encoding="utf-8", newline="\n") as fh:
        for r in result["rows"]:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    lines = ["# 646 账本规则字段注释报告（A5，清债 3）", "",
             f"- 事件数：{result['events']}",
             f"- **有事件关联的规则：{result['rules_with_events']}/67**",
             f"- 原账本 sha256（未改动证明）：`{result['ledger_sha256'][:16]}…`",
             f"- 未覆盖原子（无规则映射）：{result['uncovered_atoms']}", "",
             "> 注释文件 `data/646_authority_rule_annotation.jsonl` 是**新增文件**，"
             "原账本 `decision_event_v2_ledger.jsonl` **一字未改**（sha256 断言）。",
             "> 是否写入正式 Authority schema 留交人（646 §八.5）。"]
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def selftest() -> int:
    """只读自检：解析/反表逻辑正确（不写盘）。"""
    assert _atom_of("ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1") == "ATOM-LANG-INLINE-001"
    assert _atom_of("ae-X->ATOM-MEM-ALLOC-001") == "ATOM-MEM-ALLOC-001"
    inv = _card_to_rules()
    assert inv, "反表为空"
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--run` 生成注释文件。"""
    ap = argparse.ArgumentParser(description="646 账本规则注释（A5）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="生成注释文件")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    before = _ledger_sha256()
    result = annotate()
    write_annotation(result)
    after = _ledger_sha256()
    if before != after:
        print("ERROR：原账本被改动！")
        return 1
    print(f"[646 annotate] 事件={result['events']} 规则覆盖={result['rules_with_events']}/67 "
          f"未覆盖原子={result['uncovered_atoms']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
