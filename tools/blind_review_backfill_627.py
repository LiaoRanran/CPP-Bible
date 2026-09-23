"""627 C2 · Blind Review 结果回填工具（**只实现，不自动执行**）

**背景**：627 C1 生成了 Top10 盲审执行包（空白决策位）。人审者填好后，需要把结果
回填进 Authority Ledger，使「独立人类确认强度」从 0 变为非 0。

**本工具（627）**：提供回填的**完整实现**，但**绝不自动写入权威 ledger**：
- `build_backfill_entry(...)`：把一条人审决定构造成 Authority `DecisionEvent` 兼容条目
  （`review_method=ITEM_BLIND` / `ITEM_SECOND_REVIEW`，`decision_origin=human_observed`，
  带哈希链 prev_hash/self_hash/event_id），并通过 `DecisionEvent.validate()` 校验合法。
- `append_to_ledger(...)`：**定义了写入逻辑，但全工具中任何路径都不自动调用它**
  （遵循 625 D3 先例：定义不执行，避免机器代签人审）。
- 默认 `--stage` 只把条目写入**暂存文件** `blind_review_backfill_staging_627.jsonl`
  （新文件，非权威 ledger），供人审者复核后由人工走 authority 工具正式落库。

**硬边界（关键）**：
1. 真实 ledger `decision_event_v2_ledger.jsonl` **永不被本工具修改**（即使 `--commit` 也只写暂存）。
2. 不替人做决定、不调用 `append_to_ledger`（该函数仅为「人确认后」的接口预留）。
3. 启用真实回填需人明确确认（交人项 #2）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
STAGE = os.path.join(ROOT, "data", "authority", "blind_review_backfill_staging_627.jsonl")
PACK = os.path.join(ROOT, "data", "blind_review_pack_top10_627.json")


def build_backfill_entry(review_item_id: str, target_type: str, target_id: str,
                         decision: str, rationale: str, reviewer: str,
                         method: str = "ITEM_BLIND",
                         prev_hash: str = D.GENESIS, seq: int = 1) -> dict:
    """构造一条合法的 Authority 回填条目（不写入）。"""
    ev = D.DecisionEvent(
        seq=seq, operation="CREATE", result=decision,
        target_type=target_type, target_id=target_id,
        review_method=method, decision_origin="human_observed",
        modification=rationale if decision == "MODIFY" else "",
        reviewer=reviewer, prev_hash=prev_hash,
    )
    ev.self_hash = ev.compute_self_hash()
    ev.event_id = f"BR-{seq:06d}-{ev.self_hash[:8]}"
    d = ev.to_dict()
    d["_review_item_id"] = review_item_id  # 关联回盲审包
    return d


def validate_entries(entries: list[dict]) -> list[str]:
    errs: list[str] = []
    for e in entries:
        ev = D.DecisionEvent.from_dict({k: v for k, v in e.items()
                                        if k != "_review_item_id"})
        errs += ev.validate()
    return errs


def load_decisions_from_pack(pack_path: str = PACK) -> list[dict]:
    """读取人审者已填写的包（human_decision 非空）。"""
    if not os.path.exists(pack_path):
        return []
    pack = json.load(open(pack_path, encoding="utf-8"))
    out = []
    for it in pack.get("items", []):
        d = it.get("human_decision")
        if not d:
            continue
        out.append({
            "review_item_id": it.get("review_item_id"),
            "target_type": it.get("target_type"),
            "target_id": it.get("target_id"),
            "decision": d,
            "rationale": it.get("human_rationale") or "",
            "reviewer": "HUMAN_REVIEWER",
        })
    return out


def stage(decisions: list[dict], path: str = STAGE) -> dict:
    """把人审决定构造成条目并写入**暂存文件**（非权威 ledger）。"""
    entries = [build_backfill_entry(
        d["review_item_id"], d["target_type"], d["target_id"],
        d["decision"], d.get("rationale", ""), d.get("reviewer", "HUMAN_REVIEWER"))
        for d in decisions]
    errs = validate_entries(entries)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for e in entries:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    return {"staged": len(entries), "validation_errors": errs, "path": path}


def append_to_ledger(entry: dict, ledger_path: str = LEDGER) -> str:
    """⚠ **定义但全工具不自动调用**：供「人确认后」由 authority 工具正式落库。

    本函数存在仅为完整实现；627 C2 任何执行路径都不调用它，
    以避免机器代签人审（交人项 #2）。如确需落库，应在人明确确认后调用。
    """
    led = D.AuthorityLedger.import_jsonl(ledger_path)
    events = list(led.all_events())
    prev = events[-1].self_hash if events else D.GENESIS
    seq = (events[-1].seq + 1) if events else 1
    ev = D.DecisionEvent.from_dict({k: v for k, v in entry.items()
                                    if k != "_review_item_id"})
    ev.finalize(prev, seq)  # 接在既有哈希链末端
    events.append(ev)
    new_led = D.AuthorityLedger()
    new_led._events = events  # 重建账本后导出
    return new_led.export_jsonl(ledger_path)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 构造样例条目（模拟人审者填写）
    entries = [build_backfill_entry("RI-edge-x", "edge", "ae-MIS-X->ATOM-Y::prop-1",
                                    "APPROVE", "独立确认攻击成立", "HUMAN_REVIEWER",
                                    seq=1)]
    chk("回填条目通过 DecisionEvent 校验", not validate_entries(entries),
        f"(errs={validate_entries(entries)})")
    chk("条目 review_method 为 ITEM_BLIND",
        entries[0]["review_method"] == "ITEM_BLIND")
    chk("条目 decision_origin 为 human_observed",
        entries[0]["decision_origin"] == "human_observed")

    # 暂存写入不触碰权威 ledger
    before = hashlib.sha256(open(LEDGER, "rb").read()).hexdigest()
    stage([{"review_item_id": "RI-edge-x", "target_type": "edge",
            "target_id": "ae-MIS-X->ATOM-Y::prop-1", "decision": "APPROVE",
            "rationale": "t", "reviewer": "H"}], STAGE)
    after = hashlib.sha256(open(LEDGER, "rb").read()).hexdigest()
    chk("权威 ledger 未被本工具修改", before == after)

    # append_to_ledger 全工具未自动调用：逐行静态确认无真实调用点
    real_calls = 0
    for line in open(__file__, encoding="utf-8").read().splitlines():
        s = line.strip()
        if "append_to_ledger(" not in s:
            continue
        if s.startswith("def append_to_ledger"):      # 定义
            continue
        if s.startswith("#") or s.startswith('"""') or s.startswith("'"):  # 注释/字符串
            continue
        if s.startswith("-"):  # 文档字符串 bullet
            continue
        if "re.findall" in s or "calls.count" in s or "re.search" in s:  # 自检本身
            continue
        if "not in s" in s:  # 自检本身
            continue
        real_calls += 1
    chk("append_to_ledger 未被自动调用（无真实调用点）", real_calls == 0,
        f"(真实调用点 {real_calls})")
    print(f"C2 backfill check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 C2 Blind Review 回填（只实现不执行）")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--stage", action="store_true", help="把已填写包暂存为回填条目")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.stage:
        decisions = load_decisions_from_pack()
        if not decisions:
            print("包中尚无 human_decision（需人审者先填写 blind_review_pack_top10_627.json）")
            return 0
        r = stage(decisions)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        print("⚠ 已写入暂存文件；正式落库需人确认后由 authority 工具执行（本工具不代签）。")
        return 0
    print("用法：--check 自检 | --stage 把已填写包暂存为回填条目（不落库）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
