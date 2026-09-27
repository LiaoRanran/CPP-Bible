#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""calibration_upgrade_651.py — M3 校准升级（651 W3，**SCOPE-BPE + swap 双跑 + 分层 α 预算**）。

为什么（651 W3-M3）：单一全局校准率会把"某类来源特别不可靠"平均掉。M3 要求：
**分层 α 预算**（每层允许误差）+ **双跑产出**（SCOPE-BPE 与 swap 两条独立估计）+
**双跑不一致即升级为"强制重校准"**（机器强制，不靠人记得）。

用法
====
    python tools/calibration_upgrade_651.py --check                 # 合成自检
    python tools/calibration_upgrade_651.py --run                   # 对真账本分层 → data/651_m3_calibration.json
    python tools/calibration_upgrade_651.py --json

诚实边界：
- 分层按账本 `source`（BATCH_AUTH/MIRROR_DERIVED/ITEM_OPEN）；α 默认 0.2（可 --alpha 调）。
- 双跑 = 两条**估计口径**（计数式 vs 置信加权式），非两次真实实验；不一致 ⇒ 标 `unstable`。
- 只读账本，不改任何判决。
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "protector", "name": "calibration_upgrade_651", "entry": "run_calibration",
                "description": "M3 分层 α 预算 + 双跑不一致 ⇒ 强制重校准"}

LEDGER = ROOT / "data" / "authority" / "decision_event_v2_ledger.jsonl"
OUT = ROOT / "data" / "651_m3_calibration.json"
ALPHA_DEFAULT = 0.2
DISAGREE_TOL = 0.1
REJUDGE = "MODIFY"


@dataclass
class StratumRow:
    stratum: str
    n: int
    rejudge_count: int
    rate_count: float
    rate_weighted: float
    alpha: float
    over_budget: bool
    unstable: bool
    forced_recalibration: bool


def _conf_weight(c: str) -> float:
    return {"high": 1.0, "medium": 0.5, "low": 0.25}.get(str(c).lower(), 0.5)


def dual_run(events: list[dict], alpha: float = ALPHA_DEFAULT) -> list[StratumRow]:
    """按 source 分层；两条口径（计数 / 置信加权）；不一致或超 α ⇒ 强制重校准。"""
    groups: dict[str, list[dict]] = {}
    for e in events:
        groups.setdefault(str(e.get("source", "UNKNOWN")), []).append(e)
    rows: list[StratumRow] = []
    for name, evs in sorted(groups.items()):
        n = len(evs)
        rj = [e for e in evs if str(e.get("result", "")).upper() == REJUDGE]
        rate_count = len(rj) / n if n else 0.0
        wsum = sum(_conf_weight(e.get("confidence", "")) for e in evs) or 1.0
        rate_weighted = sum(_conf_weight(e.get("confidence", "")) for e in rj) / wsum
        over = rate_count > alpha
        unstable = abs(rate_count - rate_weighted) > DISAGREE_TOL
        rows.append(StratumRow(name, n, len(rj), round(rate_count, 4), round(rate_weighted, 4),
                               alpha, over, unstable, over or unstable))
    return rows


def run_calibration(ledger: Path = LEDGER, alpha: float = ALPHA_DEFAULT) -> dict:
    events = []
    for ln in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            events.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    rows = dual_run(events, alpha)
    return {
        "ledger": str(ledger.relative_to(ROOT)),
        "alpha": alpha,
        "strata": len(rows),
        "events": len(events),
        "forced_recalibration": [r.stratum for r in rows if r.forced_recalibration],
        "rows": [asdict(r) for r in rows],
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 层A：改判 4/5=0.8 > 0.2 ⇒ over_budget & forced
    # 层B：改判 0/5=0.0 ⇒ 不 over
    events = ([{"source": "A", "result": "MODIFY", "confidence": "high"}] * 4
              + [{"source": "A", "result": "APPROVE", "confidence": "high"}]
              + [{"source": "B", "result": "APPROVE", "confidence": "high"}] * 5)
    rows = {r.stratum: r for r in dual_run(events, 0.2)}
    chk("层A 超预算", rows["A"].over_budget is True and rows["A"].forced_recalibration is True)
    chk("层B 不超预算", rows["B"].over_budget is False)
    chk("rate_count 正确", rows["A"].rate_count == 0.8)
    # 双跑不一致 ⇒ unstable
    events2 = ([{"source": "C", "result": "MODIFY", "confidence": "low"}] * 4
               + [{"source": "C", "result": "APPROVE", "confidence": "high"}] * 16)
    r = {x.stratum: x for x in dual_run(events2, 0.2)}["C"]
    chk("双跑口径不一致 ⇒ unstable", r.unstable is True, f"count={r.rate_count} w={r.rate_weighted}")
    print(f"calibration_upgrade_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 M3 校准升级（分层 α + 双跑）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--alpha", type=float, default=ALPHA_DEFAULT)
    ap.add_argument("--ledger", default=str(LEDGER))
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rep = run_calibration(Path(a.ledger), a.alpha)
    if a.run:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"strata={rep['strata']} events={rep['events']} forced={rep['forced_recalibration']}\n→ {OUT.name}")
        return 0
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json
          else f"strata={rep['strata']} forced={rep['forced_recalibration']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
