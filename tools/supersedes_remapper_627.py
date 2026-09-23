"""627 A2 · 51 条 supersedes 旧式 ID 重映射（**不修改原 ledger**）

**背景**：626 的 `decision_event_v2_ledger.jsonl` 中 51 条 `REPLACE` 事件的 `supersedes`
指向**旧式 ID**：
- `legacy:pre_annotation:ae-<edge>` × 34
- `dec-0001XX` × 17
- 指向有效 v2 `event_id` 的：**0**

这导致 Authority 哈希链的 `supersedes` 链**断裂**，可追溯性半残。

**修复方案（627 实测确认 51/51 可恢复）**：
- `legacy:pre_annotation:<edge>` → 同一 `<edge>` 在 v2 ledger 中**首条** `CREATE` 事件的 `event_id`
- `dec-0001XX` → authority_log 中 `decision_id == dec-0001XX` 的 `target.edge`
  → 该 edge 在 v2 ledger 的首条 event_id

**关键约束（硬边界）**：
1. **不修改原 ledger** —— 生成全新文件 `decision_event_v2_ledger_remapped.jsonl`。
2. 保留每条事件的**原始 `event_id`**（作为溯源标识），仅重算 `prev_hash/self_hash`
   以反映新 `supersedes`；`verify_chain()` 仍通过（它只校验 prev_hash + self_hash）。
3. 重映射后：每条 `REPLACE` 的 `supersedes` 均指向 remapped 文件中**确实存在**的 `event_id`。

> 为何保留原始 event_id 而非重算：event_id 由 self_hash 派生，而 self_hash 含 supersedes，
> 重算会触发「id↔supersedes」循环依赖。保留原始 id 既保证溯源连续，又使 supersedes 可解析，
> remapped 文件内部自洽（verify_chain 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Callable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402

SRC_LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
AUTH_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
OUT_LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger_remapped.jsonl")
OUT_MAP = os.path.join(ROOT, "data", "authority", "supersedes_remap_627.json")


def _load(path: str) -> list:
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def build_mapping(src_ledger: str = SRC_LEDGER,
                  auth_log: str = AUTH_LOG
                  ) -> tuple[dict, dict, dict, Callable[[str], Optional[str]]]:
    """返回 (mapping空占位, edge->v2event_id, dec->edge, resolve 函数)。"""
    led = D.AuthorityLedger.import_jsonl(src_ledger)
    edge2eid: dict[str, str] = {}
    for e in led.all_events():
        if e.target_type == "edge" and e.target_id not in edge2eid:
            edge2eid[e.target_id] = e.event_id
    # dec-XXXX -> edge
    dec2edge: dict[str, str] = {}
    for a in _load(auth_log):
        did = a.get("decision_id")
        t = a.get("target") or {}
        if did and str(did).startswith("dec-") and isinstance(t, dict):
            dec2edge[str(did)] = t.get("id") or ""

    def resolve(old: str) -> Optional[str]:
        if old.startswith("legacy:pre_annotation:"):
            edge = old.split(":", 2)[2]
            return edge2eid.get(edge)
        if old.startswith("dec-"):
            e2 = dec2edge.get(old)
            return edge2eid.get(e2) if e2 else None
        return None  # 已是 v2 event_id

    return {}, edge2eid, dec2edge, resolve  # type: ignore[return-value]


def remap(src_ledger: str = SRC_LEDGER, out_ledger: str = OUT_LEDGER) -> dict:
    """生成 remapped ledger（不修改原文件）。返回统计与映射表。"""
    mapping, _e, _d, resolve = build_mapping(src_ledger)
    led = D.AuthorityLedger.import_jsonl(src_ledger)
    events = [D.DecisionEvent.from_dict(e.to_dict()) for e in led.all_events()]

    remap_table: list[dict] = []
    n_replace = 0
    n_resolved = 0
    n_unresolved = 0
    new_supersedes_log: dict[str, dict] = {}
    for e in events:
        if e.operation != "REPLACE":
            continue
        n_replace += 1
        new_sup: list[str] = []
        for old in (e.supersedes or []):
            old = str(old)
            new = resolve(old)
            if new:
                new_sup.append(new)
                n_resolved += 1
                remap_table.append({"event_id": e.event_id, "old": old, "new": new})
            else:
                new_sup.append(old)  # 保留原始（理论上不会发生）
                n_unresolved += 1
        new_supersedes_log[e.event_id] = {"old": list(e.supersedes or []), "new": new_sup}
        e.supersedes = new_sup

    # 重算哈希链（保留原始 event_id，仅更新 prev_hash/self_hash）
    prev = D.GENESIS
    valid_ids = {e.event_id for e in events}
    for e in events:
        e.prev_hash = prev
        e.self_hash = e.compute_self_hash()
        prev = e.self_hash

    os.makedirs(os.path.dirname(out_ledger) or ".", exist_ok=True)
    with open(out_ledger, "w", encoding="utf-8", newline="\n") as fh:
        for e in events:
            fh.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")

    # 校验重映射后 supersedes 全部指向存在 id
    unresolved_refs = [s for e in events if e.operation == "REPLACE"
                       for s in (e.supersedes or []) if s not in valid_ids]
    with open(OUT_MAP, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"remap_table": remap_table,
                   "summary": {"replace_events": n_replace,
                               "resolved": n_resolved, "unresolved": n_unresolved,
                               "unresolved_refs_in_output": len(unresolved_refs)}},
                  fh, ensure_ascii=False, indent=2)
    return {"replace_events": n_replace, "resolved": n_resolved,
            "unresolved": n_unresolved,
            "unresolved_refs_in_output": len(unresolved_refs),
            "out": out_ledger}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 原 ledger 不被修改（先记录指纹）
    import hashlib
    before = hashlib.sha256(open(SRC_LEDGER, "rb").read()).hexdigest()
    r = remap()
    after = hashlib.sha256(open(SRC_LEDGER, "rb").read()).hexdigest()
    chk("原 ledger 未被修改", before == after)

    chk("51 条 REPLACE 全部解析成功",
        r["replace_events"] == 51 and r["resolved"] == 51 and r["unresolved"] == 0,
        f"(REPLACE {r['replace_events']}, resolved {r['resolved']})")
    chk("remapped 文件无悬空 supersedes", r["unresolved_refs_in_output"] == 0)

    # remapped 文件自洽
    rem = D.AuthorityLedger.import_jsonl(r["out"])
    chk("remapped 哈希链完整", rem.verify_chain())
    chk("remapped 事件数 = 452", len(rem.all_events()) == 452)

    # 所有 REPLACE 的 supersedes 指向存在 id
    ids = {e.event_id for e in rem.all_events()}
    bad = [s for e in rem.all_events() if e.operation == "REPLACE"
           for s in (e.supersedes or []) if s not in ids]
    chk("remapped supersedes 全部指向有效 event_id", not bad, f"({len(bad)})")

    # 原 ledger 仍自洽（未动）
    orig = D.AuthorityLedger.import_jsonl(SRC_LEDGER)
    chk("原 ledger 哈希链仍完整", orig.verify_chain())
    print(f"A2 remapper check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 A2 supersedes 重映射")
    ap.add_argument("--check", action="store_true", help="自检")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = remap()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
