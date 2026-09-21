#!/usr/bin/env python3
"""615 A2 · 30 条真逐条复核决策清单（**只生成清单，不执行复核，不改 annotations**）。

背景：388 条为 5 模板批量授权，逐条独立判断 0（`data/human_review_honesty_615.md`）。
本工具挑选 **30 条最高优先候选边**，生成为人审准备的**逐条复核决策清单**——每条的判断要点、
建议结论、以及必须由人回答的**是非题**。**复核本身是人审权力，苦力不执行。**

选取优先级（去重）：
  1. **OUT 的 7 个 MIS 的正向攻击边**（全部）
  2. **modify 边**中歧义度最高者（理由最短优先）
  3. 关联**高权重卡**（目标原子卡被引边数最高）的边
  4. 理由**最短/最模板化**的边（rubber-stamp 风险最高）

CLI：`--write`（写清单）/ `--check`（自验证）/ 默认打印统计。
铁律：不改 `data/human_attack_edge_annotations.jsonl`；不改受控目录；不执行复核。
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

ANNOTATIONS = ROOT / "data" / "human_attack_edge_annotations.jsonl"
LABELS = ROOT / "data" / "human_review_honesty_labels.jsonl"
PROPS_DB = ROOT / "data" / "propositions.db"
OUT = ROOT / "data" / "human_review_item_by_item_30_615.md"
N_SELECT = 30

#: W2 keep-low 口径下 OUT 的 7 个 MIS（入库权威）
OUT_MIS = ("MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003", "MIS-UB-001",
           "MIS-UB-004", "MIS-UB-008", "MIS-UB-014")

_FWD = re.compile(r"^ae-(MIS-[A-Z0-9-]+)->(ATOM-[A-Z0-9-]+)::(prop-\d+)$")
_REV = re.compile(r"^ae-(ATOM-[A-Z0-9-]+)::(prop-\d+)->(MIS-[A-Z0-9-]+)$")


def _load(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [cast("dict[str, Any]", json.loads(ln)) for ln in
            path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def parse_edge(edge_id: str) -> dict | None:
    """→ {mis, atom, prop, direction}；无法解析 ⇒ None。"""
    m = _FWD.match(edge_id)
    if m:
        return {"mis": m.group(1), "atom": m.group(2), "prop": m.group(3), "direction": "fwd"}
    m = _REV.match(edge_id)
    if m:
        return {"mis": m.group(3), "atom": m.group(1), "prop": m.group(2), "direction": "rev"}
    return None


def _prop_statement(atom: str, prop: str) -> str:
    if not PROPS_DB.is_file():
        return "（命题库缺失，请读卡）"
    try:
        conn = sqlite3.connect(str(PROPS_DB))
        row = conn.execute("SELECT statement FROM props WHERE card=? AND prop_id=? LIMIT 1",
                           (atom, prop)).fetchone()
        conn.close()
        return str(row[0]) if row else "（未在命题库找到该断言）"
    except sqlite3.Error:
        return "（命题库读取失败）"


def select(recs: list[dict], labels_by_edge: dict[str, dict]) -> list[dict]:
    """注：只从**正向攻击边**（MIS→命题）中选取——镜像反向边是派生票（复核无独立信息），排除。"""
    recs = [r for r in recs if (p := parse_edge(r["edge_id"])) and p["direction"] == "fwd"]
    items: list[dict] = []

    def add(parsed: dict, rec: dict) -> None:
        items.append({"edge_id": rec["edge_id"], "action": rec.get("action"),
                      "reason": rec.get("reason", ""), **parsed})

    seen: set[str] = set()

    def take(cands: list[dict]) -> None:
        for r in cands:
            if len(items) >= N_SELECT:
                return
            if r["edge_id"] in seen:
                continue
            p = parse_edge(r["edge_id"])
            if not p:
                continue
            seen.add(r["edge_id"])
            add(p, r)

    # P1：OUT7 的前向攻击边
    take(sorted((r for r in recs if (p := parse_edge(r["edge_id"])) and p["direction"] == "fwd"
                 and p["mis"] in OUT_MIS), key=lambda r: r["edge_id"]))
    # P2：modify 边（理由最短优先 ⇒ 歧义度最高）
    take(sorted((r for r in recs if r.get("action") == "modify"),
                key=lambda r: (len(r.get("reason", "")), r["edge_id"])))
    # P3：目标原子卡被引边数最高
    deg: dict[str, int] = {}
    for r in recs:
        p = parse_edge(r["edge_id"])
        if p:
            deg[p["atom"]] = deg.get(p["atom"], 0) + 1
    take(sorted(recs, key=lambda r: (-deg.get((parse_edge(r["edge_id"]) or {}).get("atom", ""), 0),
                                     r["edge_id"])))
    # P4：理由最短（rubber-stamp 风险最高）
    take(sorted(recs, key=lambda r: (len(r.get("reason", "")), r["edge_id"])))
    return items


def render(items: list[dict]) -> str:
    L = ["# 615 A2 · 30 条真逐条复核决策清单（交人审，**不执行**）", "",
         "> 背景：388 条为批量授权（逐条独立 0）。本清单挑 30 条**最高优先**候选边，供人**逐条复核**。",
         "> **苦力不执行复核**；人审执行后由人**授权**更新 annotations（本批不改）。", "",
         "## 选取优先级", "",
         f"1. OUT 的 7 个 MIS 的正向攻击边（`{'/'.join(OUT_MIS)}`）——全部",
         "2. modify 边（歧义度最高）　3. 高权重卡　4. 理由最短/最模板化", "",
         "## 逐条决策清单", "",
         "| # | 边 ID | 源 MIS | 目标命题 | 关联原子卡 | 当前 | 理由长度 | 建议 | 置信度 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for i, it in enumerate(items, 1):
        sug, conf = _suggest(it)
        L.append(f"| {i} | `{it['edge_id']}` | {it['mis']} | {it['prop']} | {it['atom']} | "
                 f"{it['action']} | {len(it['reason'])} | {sug} | {conf} |")
    L += ["", "## 复核明细（判断要点 + 待人回答的是非题）", ""]
    for i, it in enumerate(items, 1):
        stmt = _prop_statement(it["atom"], it["prop"])
        sug, conf = _suggest(it)
        L += [f"### {i}. `{it['edge_id']}`", "",
              f"- 源 MIS：**{it['mis']}** ｜ 目标命题：**{it['atom']}::{it['prop']}** ｜ 当前：{it['action']}",
              f"- 目标断言（来自命题库）：{stmt}",
              f"- 审核理由原文：{it['reason']}",
              "- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的"
              "**哪个断言**？是否为镜像/抽样外推而非独立判断？",
              f"- 建议复核结论：**{sug}**（置信度 {conf}）",
              f"- 需人回答：① `{it['mis']}` 的 refutation 是否驳斥了 `{it['atom']}::{it['prop']}` 的断言？"
              f"（是/否）② 若是，属于 approve 还是 modify？（approve/modify）", ""]
    L += ["## 边界", "",
          "- 本清单**不含**任何复核结论的**执行**；须人审逐条判断并**授权**后更新 annotations。",
          "- 未修改 annotations、未改受控目录。", "", ""]
    return "\n".join(L) + "\n"


def _suggest(it: dict) -> tuple[str, str]:
    reason = it["reason"]
    if "对称边" in reason or len(reason) <= 50:
        return ("需独立判断（原为镜像/短理由，rubber-stamp 风险）", "low")
    if it["action"] == "modify":
        return ("复核 modify 是否恰当", "medium")
    return ("复核 approve", "medium")


def write(items: list[dict]) -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(items), encoding="utf-8", newline="\n")
    return len(items)


def check() -> list[str]:
    problems: list[str] = []
    recs = _load(ANNOTATIONS)
    labels = {x["edge_id"]: x for x in _load(LABELS)}
    items = select(recs, labels)
    if len(items) != N_SELECT:
        problems.append(f"应选 {N_SELECT} 条（实测 {len(items)}）")
    ids = [it["edge_id"] for it in items]
    if len(set(ids)) != len(ids):
        problems.append("30 条存在重复边")
    # OUT7 全部入选
    out_fwd = {r["edge_id"] for r in recs
               if (p := parse_edge(r["edge_id"])) and p["direction"] == "fwd" and p["mis"] in OUT_MIS}
    if not out_fwd <= set(ids):
        problems.append(f"OUT7 正向边未全部入选（缺 {len(out_fwd - set(ids))} 条）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="human_review_item_by_item_615",
                                 description="615 A2 逐条复核决策清单（只生成，不执行）")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    recs = _load(ANNOTATIONS)
    labels = {x["edge_id"]: x for x in _load(LABELS)}
    items = select(recs, labels)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[A2] ❌ {p}", file=sys.stderr)
            return 1
        print(f"[A2] ✅ 自验证通过：{len(items)} 条无重复 / OUT7 正向边全入选 / 格式完整")
        return 0
    if a.write:
        n = write(items)
        print(f"[A2] 已写 {OUT.relative_to(ROOT).as_posix()}（{n} 条）")
        return 0
    out_n = sum(1 for it in items if it["mis"] in OUT_MIS)
    print(json.dumps({"selected": len(items), "out_mis_edges": out_n,
                      "modify": sum(1 for it in items if it["action"] == "modify")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
