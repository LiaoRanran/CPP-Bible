#!/usr/bin/env python3
"""614 线E E2 · oracle 验证流程（机制设计 · **不跑监工门禁**）。

背景：本仓**没有真 oracle**（无自动裁决者）。E2 设计的是「**人/外部独立源如何执行验证**」的
可审计流程，而非自动裁决：

  1. **计划**：读现有 `data/oracle_verification_plan_611.jsonl`（83 卡），为每卡分配
     **≥2 个独立验证者**（验证者池来自 `data/oracle_registry.json` 的理念；独立性=不同验证者）。
  2. **记录**：验证者给出裁决 `confirm | refute | abstain`，append-only 落
     `data/oracle_verification_records_614.jsonl`（`latest-wins` 读取）。
  3. **判决（fail-closed）**：
       * 任一验证者 `refute` ⇒ 卡判 **refuted**；
       * ≥2 个**独立**验证者 `confirm` 且无 refute ⇒ **confirmed**；
       * 否则 **pending**（1 个 confirm 不算）。
  4. `abstain` 不计入；**同一验证者的重复记录只取最新一条**（防刷）。

⚠️ **不执行** `gate/poison/replay/tool_integrity --check`（614 §五 铁律：苦力不跑监工门禁）。
   `oracle_verifier.py`（612 C1）跑三门禁的"oracle 专用"例外，**本批不适用**。

CLI：
  python tools/oracle_verification_614.py plan                 # 写 614 分配计划
  python tools/oracle_verification_614.py record --card <id> --verifier <v> --verdict confirm|refute|abstain [--evidence ..]
  python tools/oracle_verification_614.py status [--card <id>]
  python tools/oracle_verification_614.py --check              # 自验证（exit 0=通过）

铁律：append-only；**不填** `verified_by_oracle`（人审权力）；不跑监工门禁；不改受控目录。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

PLAN_611 = ROOT / "data" / "oracle_verification_plan_611.jsonl"
PLAN_614 = ROOT / "data" / "oracle_verification_plan_614.jsonl"
RECORDS = ROOT / "data" / "oracle_verification_records_614.jsonl"
VERDICTS = ("confirm", "refute", "abstain")
VERIFIER_POOL = ("oracle-tsan", "oracle-gcc", "oracle-replay", "oracle-human")
DEFAULT_REQUIRED = 2


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_plan() -> list[dict]:
    if not PLAN_611.is_file():
        return []
    out: list[dict] = []
    for line in PLAN_611.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(cast("dict[str, Any]", json.loads(line)))
    return out


def assign_verifiers(cards: list[dict], n: int = DEFAULT_REQUIRED) -> list[dict]:
    """为每卡分配 n 个**互不相同**的验证者（确定性：优先 suggested_primary_oracle，再从池补齐）。"""
    planned: list[dict] = []
    for c in cards:
        suggested = str(c.get("suggested_primary_oracle") or "").strip()
        pool = [f"oracle-{suggested}"] if suggested else []
        pool += [v for v in VERIFIER_POOL if v not in pool]
        assigned = pool[:max(1, n)]
        planned.append({"card": c["card"], "path": c.get("path"),
                        "kind": c.get("kind"), "verifiers": assigned,
                        "required": len(assigned)})
    return planned


def write_plan(planned: list[dict]) -> int:
    PLAN_614.parent.mkdir(parents=True, exist_ok=True)
    with PLAN_614.open("w", encoding="utf-8") as fh:
        for r in planned:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(planned)


def load_records(store: Path) -> list[dict]:
    if not store.is_file():
        return []
    out: list[dict] = []
    for line in store.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(cast("dict[str, Any]", json.loads(line)))
    return out


def record(store: Path, card: str, verifier: str, verdict: str,
           evidence: str | None = None) -> dict:
    if verdict not in VERDICTS:
        raise ValueError(f"verdict 必须 ∈ {VERDICTS}，收到 {verdict!r}")
    rec = {"card": card, "verifier": verifier, "verdict": verdict, "recorded_at": _now()}
    if evidence:
        rec["evidence"] = evidence
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def latest_by_verifier(store: Path, card: str) -> dict[str, str]:
    """→ {verifier: 最新 verdict}（append-only + latest-wins，同一验证者只取最新）。"""
    out: dict[str, str] = {}
    for r in load_records(store):
        if r.get("card") == card:
            out[str(r.get("verifier"))] = str(r.get("verdict"))
    return out


def verdict_for(store: Path, card: str, required: int = DEFAULT_REQUIRED) -> str:
    """fail-closed：任一 refute ⇒ refuted；≥required 独立 confirm 且无 refute ⇒ confirmed；否则 pending。"""
    v = latest_by_verifier(store, card)
    if any(x == "refute" for x in v.values()):
        return "refuted"
    confirms = {k for k, x in v.items() if x == "confirm"}
    return "confirmed" if len(confirms) >= required else "pending"


def status(store: Path, planned: list[dict], card: str | None = None) -> list[dict]:
    rows: list[dict] = []
    for p in planned:
        if card and p["card"] != card:
            continue
        rows.append({"card": p["card"], "verifiers": p.get("verifiers", []),
                     "required": p.get("required", DEFAULT_REQUIRED),
                     "verdict": verdict_for(store, p["card"], p.get("required", DEFAULT_REQUIRED))})
    return rows


def check() -> list[str]:
    import tempfile
    problems: list[str] = []
    # 计划：83 卡，每卡 ≥2 独立验证者
    cards = load_plan()
    if len(cards) != 83:
        problems.append(f"计划应为 83 卡（实测 {len(cards)}）")
    planned = assign_verifiers(cards)
    for p in planned:
        if len(set(p["verifiers"])) != len(p["verifiers"]) or len(p["verifiers"]) < 2:
            problems.append(f"{p['card']} 验证者应 ≥2 且互不相同")
            break
    # 判决规则（合成记录）
    with tempfile.TemporaryDirectory() as td:
        store = Path(td) / "rec.jsonl"
        c = cards[0]["card"] if cards else "ATOM-X"
        # 1 confirm ⇒ pending
        record(store, c, "oracle-tsan", "confirm")
        if verdict_for(store, c, 2) != "pending":
            problems.append("1 个 confirm 应判 pending")
        # 第 2 个独立 confirm ⇒ confirmed
        record(store, c, "oracle-gcc", "confirm")
        if verdict_for(store, c, 2) != "confirmed":
            problems.append("2 个独立 confirm 应判 confirmed")
        # 同一验证者重复 confirm 不叠加
        record(store, c, "oracle-gcc", "confirm")
        if verdict_for(store, c, 3) != "pending":
            problems.append("同一验证者重复 confirm 不应叠加（required=3 时仍 pending）")
        # 任一 refute ⇒ refuted（fail-closed）
        record(store, c, "oracle-replay", "refute")
        if verdict_for(store, c, 2) != "refuted":
            problems.append("任一 refute 应判 refuted")
        # abstain 不计入
        store2 = Path(td) / "rec2.jsonl"
        record(store2, c, "oracle-tsan", "abstain")
        if verdict_for(store2, c, 2) != "pending":
            problems.append("abstain 不应计入 confirm")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="oracle_verification_614",
                                 description="614 E2 oracle 验证流程（机制，不跑监工门禁）")
    ap.add_argument("command", nargs="?", default="status",
                    choices=["plan", "record", "status"], help="子命令（默认 status）")
    ap.add_argument("--card", default=None)
    ap.add_argument("--verifier", default=None)
    ap.add_argument("--verdict", default=None)
    ap.add_argument("--evidence", default=None)
    ap.add_argument("--required", type=int, default=DEFAULT_REQUIRED)
    ap.add_argument("--store", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    store = Path(a.store) if a.store else RECORDS

    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[E2] ❌ {p}", file=sys.stderr)
            return 1
        print("[E2] ✅ 自验证通过：83 卡计划 / ≥2 独立验证者 / fail-closed 判决规则 均一致")
        return 0

    cards = load_plan()
    planned = assign_verifiers(cards, a.required)
    if a.command == "plan":
        n = write_plan(planned)
        print(f"[E2] 已写 {PLAN_614.relative_to(ROOT).as_posix()}（{n} 卡，每卡 {a.required} 独立验证者）")
        return 0
    if a.command == "record":
        if not a.card or not a.verifier or not a.verdict:
            print("[E2] ❌ record 需要 --card --verifier --verdict", file=sys.stderr)
            return 2
        rec = record(store, a.card, a.verifier, a.verdict, a.evidence)
        print(json.dumps(rec, ensure_ascii=False))
        return 0
    rows = status(store, planned, a.card)
    print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
