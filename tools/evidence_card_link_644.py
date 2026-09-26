"""644 阶段 C · C2 证据-卡片关联层（多对多）。

建立证据和卡片的多对多关联，独立索引文件 `data/evidence_index.json`，**不修改卡片 YAML**：
- 一张卡可以挂多条证据
- 一条证据可以被多张卡引用
- 关联带：引用方式（support / refute / background）、引用时间、引用者

关联 index 结构：
```
{ "links": [ {"evidence_id","card_id","relation","linked_at","linked_by"} ],
  "by_card": {card_id: [evidence_id,...]}, "by_evidence": {evidence_id: [card_id,...]} }
```
只读（除非显式 --build/--write；只写 data/evidence_index.json，绝不碰受控目录）。
--check 只读幂等。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

INDEX_FILE = base.INDEX_FILE


def _relation_of(verdict: str) -> str:
    v = (verdict or "").lower()
    if v == "refute":
        return "refute"
    if v == "partial":
        return "background"
    return "support"


def new_index() -> dict[str, Any]:
    return {"links": [], "by_card": {}, "by_evidence": {}}


def link(index: dict[str, Any], evidence_id: str, card_id: str, relation: str,
         linked_at: str, linked_by: str) -> dict[str, Any]:
    """在内存 index 上建立一条关联（多对多）。重复关联幂等。"""
    for lk in index["links"]:
        if lk["evidence_id"] == evidence_id and lk["card_id"] == card_id:
            lk.update(relation=relation, linked_at=linked_at, linked_by=linked_by)
            break
    else:
        index["links"].append({
            "evidence_id": evidence_id, "card_id": card_id, "relation": relation,
            "linked_at": linked_at, "linked_by": linked_by,
        })
    index["by_card"].setdefault(card_id, [])
    if evidence_id not in index["by_card"][card_id]:
        index["by_card"][card_id].append(evidence_id)
    index["by_evidence"].setdefault(evidence_id, [])
    if card_id not in index["by_evidence"][evidence_id]:
        index["by_evidence"][evidence_id].append(card_id)
    return index


def build_index_from_existing() -> dict[str, Any]:
    """从现有 evidence/ 的 serves + 原子卡引用，重建只读关联索引（不写盘）。"""
    idx = new_index()
    m = base.card_evidence_map()
    for card in base.list_atoms():
        cid = card["id"]
        for e in m.get(cid, []):
            link(idx, e["id"], cid, _relation_of(e.get("verdict", "")),
                 "legacy", "evidence_card_link_644.build_index_from_existing")
    return idx


def load_index(path: str = INDEX_FILE) -> dict[str, Any]:
    if not os.path.exists(path):
        return new_index()
    with open(path, encoding="utf-8") as fh:
        data: dict[str, Any] = json.load(fh)
    data.setdefault("links", [])
    data.setdefault("by_card", {})
    data.setdefault("by_evidence", {})
    return data


def save_index(index: dict[str, Any], path: str = INDEX_FILE) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2, sort_keys=True)
    return path


def query_card(index: dict[str, Any], card_id: str) -> list[str]:
    return list(index["by_card"].get(card_id, []))


def query_evidence(index: dict[str, Any], evidence_id: str) -> list[str]:
    return list(index["by_evidence"].get(evidence_id, []))


def render_md(index: dict[str, Any]) -> str:
    n_links = len(index["links"])
    n_cards = len(index["by_card"])
    n_ev = len(index["by_evidence"])
    rel_dist: dict[str, int] = {}
    for link in index["links"]:
        rel_dist[link["relation"]] = rel_dist.get(link["relation"], 0) + 1
    lines = ["# 644 C2 · 证据-卡片关联索引", "",
             f"- 关联条目：**{n_links}**  涉及卡片：**{n_cards}**  涉及证据：**{n_ev}**", "",
             "## 关系类型分布", "", "| 关系 | 数量 |", "|---|---|"]
    for k in ("support", "refute", "background"):
        lines.append(f"| {k} | {rel_dist.get(k, 0)} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    idx = build_index_from_existing()
    out = os.path.join(base.ROOT, "data", "644_link_report.md")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(idx))
    return out


def selftest() -> int:
    idx = new_index()
    link(idx, "E1", "C1", "support", "2026-09-26", "t")
    link(idx, "E1", "C2", "refute", "2026-09-26", "t")
    link(idx, "E2", "C1", "background", "2026-09-26", "t")
    # 多对多正确
    assert sorted(query_card(idx, "C1")) == ["E1", "E2"]
    assert sorted(query_evidence(idx, "E1")) == ["C1", "C2"]
    # 引用方式分类合理
    sup = [lk for lk in idx["links"] if lk["evidence_id"] == "E1" and lk["card_id"] == "C2"]
    assert sup and sup[0]["relation"] == "refute"
    # 幂等：重复 link 不增加条目
    n0 = len(idx["links"])
    link(idx, "E1", "C1", "support", "2026-09-26", "t")
    assert len(idx["links"]) == n0
    # 从现有证据构建索引可跑且非空
    real = build_index_from_existing()
    assert len(real["links"]) > 0
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 C2 证据-卡片关联层")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--build", action="store_true", help="由现有证据重建索引并写盘")
    ap.add_argument("--report", action="store_true", help="写关联报告（不写索引）")
    a = ap.parse_args(argv)
    if a.build:
        idx = build_index_from_existing()
        print(f"written {save_index(idx)}  ({len(idx['links'])} 条关联)")
        return 0
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
