#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ledger_invariants_671g.py — 671g D6：账本 10 条不变式（哈希链/追加性/单调性…）+ PBT 入口。

守哪 10 条
============
  INV-01 schema      每条记录 schema=queyi-ledger/671g
  INV-02 必填字段    seq_idx / ts / kind / payload / prev_hash / hash / rules_version
  INV-03 序号连续   seq_idx 严格 0..n-1，无重复无跳号
  INV-04 时间单调   ts 非递减（ISO 字符串字典序即时间序）
  INV-05 哈希链     r[n].prev_hash == r[n-1].hash
  INV-06 内容哈希   hash == sha256(prev_hash + canonical(payload+定长字段))，改任一字段即断链
  INV-07 追加性     工具只暴露 append_record（不提供改历史 API）；篡改由 INV-05/06 捕获
  INV-08 判决合法   kind=verdict 时 payload.verdict ∈ {catch,miss,unknown,not_error}
  INV-09 卡数单调   payload.cards_total（若出现）只许不减
  INV-10 规则钉扎   每条 rules_version 必须等于现行 manifest 版本（规则变了旧账本需显式归档）

新事件走 :func:`append_record`（自动维护链）。**不碰**冻结的 452 账本
（data/authority/decision_event_v2_ledger.jsonl），本工具的账本是 data/671g/ledger_671g.jsonl。

PBT：tests/test_ledger_pbt_671g.py 用 hypothesis 随机生成合法链与单点篡改，验证全部不变式。
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SCHEMA = "queyi-ledger/671g"
LEDGER_PATH = Path("data/671g/ledger_671g.jsonl")
REQUIRED_FIELDS = ("seq_idx", "ts", "kind", "payload", "prev_hash", "hash", "rules_version")
VALID_VERDICTS = {"catch", "miss", "unknown", "not_error"}
GENESIS = "GENESIS"


def canonical(rec: dict[str, Any]) -> str:
    body = {k: rec.get(k) for k in ("seq_idx", "ts", "kind", "payload",
                                       "prev_hash", "rules_version")}
    return json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def hash_of(prev_hash: str, rec: dict[str, Any]) -> str:
    return hashlib.sha256((prev_hash + canonical(rec)).encode("utf-8")).hexdigest()


def make_record(prev: dict[str, Any] | None, kind: str, payload: dict[str, Any],
              rules_version: str, *, ts: str | None = None) -> dict[str, Any]:
    seq_idx = 0 if prev is None else int(prev["seq_idx"]) + 1
    prev_hash = GENESIS if prev is None else str(prev["hash"])
    if ts is None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
    rec = {"schema": SCHEMA, "seq_idx": seq_idx, "ts": ts, "kind": kind,
           "payload": payload, "prev_hash": prev_hash, "rules_version": rules_version}
    rec["hash"] = hash_of(prev_hash, rec)
    return rec


def append_record(path: Path, kind: str, payload: dict[str, Any],
                rules_version: str = "1.0.0", *, ts: str | None = None) -> dict[str, Any]:
    """**唯一**写入口：读最后一条→链上→追加。不提供任何改历史接口（INV-07）。"""
    recs = read_ledger(path)
    if ts is None and recs:
        ts = max(str(r.get("ts", "")) for r in recs + [{"ts": time.strftime("%Y-%m-%d %H:%M:%S")}])
        if ts < time.strftime("%Y-%m-%d %H:%M:%S"):
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
    rec = make_record(recs[-1] if recs else None, kind, payload, rules_version, ts=ts)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def validate(records: list[dict[str, Any]], expected_rules_version: str | None = None
            ) -> list[dict[str, Any]]:
    """返回违例清单（inv, seq_idx, why）。空 = 全部 10 条不变式成立。"""
    out: list[dict[str, Any]] = []
    seen_idx: set[int] = set()
    prev: dict[str, Any] | None = None
    for i, r in enumerate(records):
        def bad(inv: str, why: str) -> None:
            out.append({"inv": inv, "seq_idx": r.get("seq_idx", i), "why": why})

        if r.get("schema") != SCHEMA:
            bad("INV-01", f"schema={r.get('schema')!r}")
        missing = [f for f in REQUIRED_FIELDS if f not in r]
        if missing:
            bad("INV-02", f"缺字段 {missing}")
        idx = r.get("seq_idx")
        if idx != i:
            bad("INV-03", f"seq_idx={idx} 与位置 {i} 不一致（跳号/乱序）")
        if idx in seen_idx:
            bad("INV-03", f"seq_idx={idx} 重复")
        seen_idx.add(i)
        if prev is not None and str(r.get("ts", "")) < str(prev.get("ts", "")):
            bad("INV-04", f"ts {r.get('ts')} 早于前一条 {prev.get('ts')}")
        expect_prev = GENESIS if prev is None else str(prev.get("hash"))
        if r.get("prev_hash") != expect_prev:
            bad("INV-05", f"prev_hash={r.get('prev_hash')} ≠ 前一条 hash={expect_prev}")
        expect_hash = hash_of(str(r.get("prev_hash", "")), r)
        if r.get("hash") != expect_hash:
            bad("INV-06", "内容哈希对不上（字段被改过或链断）")
        if r.get("kind") == "verdict":
            v = (r.get("payload") or {}).get("verdict")
            if v not in VALID_VERDICTS:
                bad("INV-08", f"非法 verdict={v!r}")
        pl = r.get("payload") or {}
        if isinstance(pl, dict) and "cards_total" in pl and prev is not None:
            pp = prev.get("payload") or {}
            if isinstance(pp, dict) and "cards_total" in pp and \
                    int(pp["cards_total"]) > int(pl["cards_total"]):
                bad("INV-09", f"cards_total 回退 {pp['cards_total']} → {pl['cards_total']}")
        if expected_rules_version is not None and r.get("rules_version") != expected_rules_version:
            bad("INV-10", f"rules_version={r.get('rules_version')!r} ≠ manifest {expected_rules_version!r}")
        prev = r
    return out


def validate_file(root: Path = ROOT, path: str | Path = LEDGER_PATH,
                expected_rules_version: str | None = None) -> list[dict[str, Any]]:
    return validate(read_ledger(root / path), expected_rules_version)


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="671g D6：账本不变式")
    ap.add_argument("--root", default=None)
    ap.add_argument("--ledger", default=LEDGER_PATH.as_posix())
    ap.add_argument("--rules-version", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    v = validate_file(root, a.ledger, a.rules_version)
    if v:
        for x in v:
            print(f"  [BLOCK] {x['inv']} seq={x['seq_idx']}: {x['why']}")
        return 1
    n = len(read_ledger(root / a.ledger))
    print(f"[ledger] PASS（{n} 条记录，10 条不变式全成立）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
