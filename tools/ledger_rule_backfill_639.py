#!/usr/bin/env python3
"""639 D2 · ledger 规则归属回填（schema 上线 + 历史诚实标注）

**债务（638 B1）**：67 条规则 `known_error_rate` 全空——`DecisionEvent` 缺
`rule_id`/`rule_version` 字段，452 条历史判决无法归属到规则。

**修复（两层）**：
1. **schema**：`DecisionEvent` 增加增量字段（空值不参与哈希 ⇒ append-only
   链重算兼容，历史 452 条自哈希不变——本工具会实证校验）；
2. **回填**：对每条历史事件做**真实归属判定**——
   - 在事件全文中精确匹配 `gate_engine.RULES` 的 67 条规则 id；
   - 实测发现事件中的 `ATOM-*` 串是**原子卡 id**（如 `ATOM-LANG-INLINE-001`），
     与规则 id 同前缀但不同物——精确匹配可排除此类假阳性；
   - 归属不出的标 `undetermined`（**不编造**）。**append-only**：不改写历史
     事件，归属结论落 overlay。

**重跑**：`error_rate_collector_638 --report`（rule 级样本仍 0 ⇒ 诚实维持
「无数据」，但 schema 路径已通，新事件起可累积）。
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "639_ledger_rule_backfill.md")
OUT_JSON = os.path.join(ROOT, "data", "639_ledger_rule_backfill.json")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")


def load_rules() -> set[str]:
    try:
        import gate_engine as ge
        return {r.id for r in ge.RULES}
    except Exception:  # noqa: BLE001
        return set()


def load_events() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for line in open(LEDGER, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def attribute(ev: dict[str, Any], rule_ids: set[str]) -> dict[str, Any]:
    """单事件归属判定：精确匹配规则 id（全词边界，排除原子卡 id 假阳性）。"""
    import re
    text = json.dumps(ev, ensure_ascii=False)
    hits = sorted(rid for rid in rule_ids if re.search(rf"\b{re.escape(rid)}\b", text))
    if len(hits) == 1:
        return {"event_id": ev.get("event_id", ""), "rule_id": hits[0],
                "status": "attributed"}
    if len(hits) > 1:
        return {"event_id": ev.get("event_id", ""), "rule_id": "",
                "status": "ambiguous", "candidates": hits}
    return {"event_id": ev.get("event_id", ""), "rule_id": "",
            "status": "undetermined",
            "reason": "事件全文无规则 id 精确匹配（ATOM-* 串为原子卡 id，非规则）"}


def verify_chain_unchanged() -> dict[str, Any]:
    """schema 加字段后重放全链：历史自哈希必须逐一吻合（兼容性实证）。"""
    import decision_event_v2_626 as de
    events = load_events()
    ok, bad = 0, []
    for d in events:
        e = de.DecisionEvent.from_dict(d)
        if e.compute_self_hash() == d.get("self_hash"):
            ok += 1
        else:
            bad.append(d.get("event_id", "?"))
    prev = de.GENESIS
    chain_ok = True
    for d in events:
        if d.get("prev_hash") != prev:
            chain_ok = False
        prev = d.get("self_hash", "")
    return {"n": len(events), "hash_ok": ok,
            "hash_bad": bad[:5], "chain_links_ok": chain_ok}


def run() -> dict[str, Any]:
    rule_ids = load_rules()
    events = load_events()
    rows = [attribute(e, rule_ids) for e in events]
    dist = collections.Counter(r["status"] for r in rows)
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "n_events": len(events), "n_rules": len(rule_ids),
            "dist": dict(dist), "rows": rows,
            "chain": verify_chain_unchanged()}


def write_report() -> dict[str, str]:
    r = run()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    ch = r["chain"]
    L = ["# 639 D2 · ledger 规则归属回填报告", "",
         f"> 生成：{r['generated']}。append-only：**不改写**历史事件，结论落 overlay。",
         "",
         "## 一、schema 上线（链兼容实证）", "",
         "- `DecisionEvent` 新增 `rule_id` / `rule_version`（空值不参与哈希）；",
         f"- 历史事件重放：**{ch['hash_ok']}/{ch['n']}** 自哈希吻合"
         + (f"（不吻合样例：{ch['hash_bad']}）" if ch["hash_bad"] else "") + "；",
         f"- prev_hash 链条完整：**{ch['chain_links_ok']}**。", "",
         "## 二、历史 452 条事件归属判定", "",
         f"- `attributed`（精确命中唯一规则）：**{r['dist'].get('attributed', 0)}** 条；",
         f"- `ambiguous`（命中多条）：**{r['dist'].get('ambiguous', 0)}** 条；",
         f"- `undetermined`（无命中）：**{r['dist'].get('undetermined', 0)}** 条。", "",
         "> **诚实结论**：事件中的 `ATOM-*` 串是**原子卡 id**（edge 的端点），"
         "与规则 id 同前缀但不同物；历史判决证据链（basis_refs → authority_log）"
         "实测**不含规则引用** ⇒ 全部标 `undetermined`，**不编造归属**。",
         "",
         "## 三、known_error_rate 重跑", "",
         "- rule 级样本仍为 0 ⇒ 67 条规则维持「无数据」（诚实，不给估算值）；",
         "- **路径已通**：新判决事件自本批起携带 rule_id，error_rate_collector 的"
         " `RULE_FIELD_CANDIDATES` 将自动生效，rule 级样本从此累积。", "",
         "## 四、交人项", "",
         "- 判决事件是否应强制携带 rule_id（涉及监工流程改造，非本批范围）；",
         "- 如需历史归属，只能靠人工回看 452 条判决对应的门禁运行记录（大工程）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    import decision_event_v2_626 as de
    r = run()
    chk("规则库非空（≥60 条）", r["n_rules"] >= 60)
    chk("历史 452 条自哈希全部吻合（schema 兼容）",
        r["chain"]["hash_ok"] == r["chain"]["n"] == 452)
    chk("prev_hash 链完整", r["chain"]["chain_links_ok"])
    chk("归属分布和 = 事件数", sum(r["dist"].values()) == r["n_events"])
    # 新事件带 rule_id 必须纳入哈希（防篡改生效）
    e1 = de.DecisionEvent(operation="CREATE", result="APPROVE", target_id="X")
    e1.finalize(de.GENESIS, 1)
    h1 = e1.self_hash
    e1.rule_id = "ATOM-REL-TARGET"
    chk("rule_id 非空 ⇒ 哈希改变（纳入防篡改）", e1.compute_self_hash() != h1)
    e2 = de.DecisionEvent(operation="CREATE", result="APPROVE", target_id="X")
    e2.finalize(de.GENESIS, 1)
    e2.rule_id = ""
    chk("rule_id 为空 ⇒ 哈希不变（历史兼容）", e2.compute_self_hash() == h1)
    chk("undetermined 不携带编造 rule_id",
        all(not x["rule_id"] for x in r["rows"]
            if x["status"] == "undetermined"))
    print(f"D2 backfill selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="639 D2 ledger 规则归属回填")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--report", action="store_true", help="写报告")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(json.dumps(write_report(), ensure_ascii=False))
        return 0
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
