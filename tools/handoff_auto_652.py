#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""handoff_auto_652.py — A2/A3 交人项自动化（652 A，真回填但**原文件 sha256 不变**）。

为什么（652 A）：651 留下两条"只 dry-run 未落地"的交人项：
- **A2 / T1**：判决扩展 schema 的 452 条历史回填（651 只出计划）；
- **A3 / M7**：人审队列迁移到新格式（字段别名 + 枚举映射，651 只出对照）。

本工具**真回填**，但铁律是**原文件一个字节不动**（append-only 信任资产）：
产物写到**新文件**，并在报告里给出原文件回填前后的 sha256（必须相等）。

用法
====
    python tools/handoff_auto_652.py --check
    python tools/handoff_auto_652.py --t1        # 452 判决回填 → data/authority/decision_event_v2_ledger_backfilled_652.jsonl
    python tools/handoff_auto_652.py --m7        # 30 人审迁移 → data/authority/pending_review_migrated_652.jsonl
    python tools/handoff_auto_652.py --all
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "schema", "name": "handoff_auto_652", "entry": "run_t1",
                "description": "A2/A3 T1 判决真回填 + M7 队列迁移（写新文件，原 sha256 不变）"}

LEDGER = ROOT / "data" / "authority" / "decision_event_v2_ledger.jsonl"
LEDGER_OUT = ROOT / "data" / "authority" / "decision_event_v2_ledger_backfilled_652.jsonl"
QUEUE = ROOT / "data" / "authority" / "pending_review_621.jsonl"
QUEUE_OUT = ROOT / "data" / "authority" / "pending_review_migrated_652.jsonl"


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_t1() -> dict:
    import verdict_extension_651 as ve

    before = _sha256(LEDGER)
    rows = [ln for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out_lines, added = [], 0
    for ln in rows:
        obj = json.loads(ln)
        new, diff = ve.backfill(obj)
        if diff:
            added += 1
        out_lines.append(json.dumps(new, ensure_ascii=False))
    LEDGER_OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    after = _sha256(LEDGER)
    return {"tool": "T1", "records": len(rows), "with_added_fields": added,
            "original_sha256_before": before[:16], "original_sha256_after": after[:16],
            "original_unchanged": before == after, "output": str(LEDGER_OUT.relative_to(ROOT))}


def run_m7() -> dict:
    import human_review_queue_651 as hr

    before = _sha256(QUEUE)
    rows = [ln for ln in QUEUE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out_lines, migrated, rejected = [], 0, 0
    for ln in rows:
        obj = json.loads(ln)
        adapted, log = hr.adapt_item(obj)
        ok, why = hr.validate_item(adapted)
        rec = {"source": obj, "migrated": adapted, "adapt_log": log, "valid": ok, "reject_reason": why}
        if ok:
            migrated += 1
        else:
            rejected += 1
        out_lines.append(json.dumps(rec, ensure_ascii=False))
    QUEUE_OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    after = _sha256(QUEUE)
    return {"tool": "M7", "items": len(rows), "migrated_ok": migrated, "rejected": rejected,
            "original_sha256_before": before[:16], "original_sha256_after": after[:16],
            "original_unchanged": before == after, "output": str(QUEUE_OUT.relative_to(ROOT))}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import verdict_extension_651 as ve
    new, diff = ve.backfill({"decision_id": "D", "state": "pass"})
    chk("T1 回填只加字段", "schema_version" in diff and new["decision_id"] == "D")
    import human_review_queue_651 as hr
    ad, log = hr.adapt_item({"proposal_id": "p", "atom_card": "A", "suggested_reason": "复核 approve"})
    chk("M7 适配别名+枚举", ad.get("item_id") == "p" and ad.get("reason") == "needs_human" and bool(log))
    chk("源文件存在（T1）", LEDGER.is_file())
    chk("源文件存在（M7）", QUEUE.is_file())
    print(f"handoff_auto_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="652 A2/A3 交人项自动化（写新文件）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--t1", action="store_true")
    ap.add_argument("--m7", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    reps = []
    if a.t1 or a.all:
        reps.append(run_t1())
    if a.m7 or a.all:
        reps.append(run_m7())
    if not reps:
        print("用法：--check | --t1 | --m7 | --all")
        return 0
    for r in reps:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if all(r["original_unchanged"] for r in reps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
