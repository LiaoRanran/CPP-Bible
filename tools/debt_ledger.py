#!/usr/bin/env python3
"""S5 豁免 = 带息债务：豁免必须开票（原因/风险/补偿/负责人/到期），到期未清即停线。

规则（全部机器判定）：
    * 票据字段齐全：id / cause / risk / compensation / owner / opened / due；
      **owner 必须 `human:*`** —— Agent 不得自批（S1 同源）。
    * `due` 距开票日 ≤ 90 天：**无永久豁免**。
    * `due < today` → 到期未清，exit 1（停线）。
    * 负债率 = 票据数 / quality 门禁项数，> 15% → exit 1（停线）。
    * 清票必须写 `reason`（清票也是留痕）。

用法：
    python tools/debt_ledger.py check
    python tools/debt_ledger.py add --cause "..." --risk "..." --compensation "..." \
        --owner human:liaoranran --days 30
    python tools/debt_ledger.py clear --id DEBT-001 --reason "已修复"
    python tools/debt_ledger.py show
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
from typing import Any, Sequence, cast

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "tools/debt_ledger.json"
SCHEMA = "cppbible-debt-ledger/1.0"
MAX_AGE_DAYS = 90
MAX_RATIO = 0.15
QUALITY_GATES = 20          # 与 cppbible cmd_check 的 quality 项数一致（meta-manifest 已锁）

REQUIRED = ("id", "cause", "risk", "compensation", "owner", "opened", "due")


def _load() -> dict[str, Any]:
    if not LEDGER.exists():
        return {"schema": SCHEMA, "tickets": []}
    return cast(dict[str, Any], json.loads(LEDGER.read_text(encoding="utf-8")))


def _save(state: dict[str, Any]) -> None:
    LEDGER.write_bytes((json.dumps(state, ensure_ascii=False, indent=1) + "\n")
                       .encode("utf-8"))


def _today() -> _dt.date:
    return _dt.date.today()


def cmd_check() -> int:
    state = _load()
    tickets = state.get("tickets", [])
    today = _today()
    problems: list[str] = []
    for t in tickets:
        tid = str(t.get("id") or "?")
        miss = [k for k in REQUIRED if not t.get(k)]
        if miss:
            problems.append(f"{tid} 缺字段：{', '.join(miss)}")
        owner = str(t.get("owner") or "")
        if owner and not owner.startswith("human:"):
            problems.append(f"{tid} owner 非人工（{owner}）——Agent 不得自批（S1）")
        try:
            opened = _dt.date.fromisoformat(str(t["opened"]))
            due = _dt.date.fromisoformat(str(t["due"]))
        except (KeyError, ValueError):
            continue
        if (due - opened).days > MAX_AGE_DAYS:
            problems.append(f"{tid} 到期距开票 {(due - opened).days} 天 > {MAX_AGE_DAYS}（无永久豁免）")
        if due < today:
            problems.append(f"{tid} 已到期未清（due={due}）——停线")
    ratio = len(tickets) / max(1, QUALITY_GATES)
    if ratio > MAX_RATIO:
        problems.append(f"负债率 {ratio:.0%} > {MAX_RATIO:.0%}（{len(tickets)}/{QUALITY_GATES}）——停线")
    print(f"[debt] 票据 {len(tickets)} · 负债率 {ratio:.0%} · 问题 {len(problems)}")
    for p in problems:
        print(f"  ✗ {p}")
    return 1 if problems else 0


def cmd_add(a: argparse.Namespace) -> int:
    if not a.owner.startswith("human:"):
        print("[debt] ✗ owner 必须 human:*（Agent 不得自批豁免）")
        return 2
    state = _load()
    today = _today()
    n = len(state.get("tickets", [])) + 1
    ticket = {
        "id": f"DEBT-{n:03d}",
        "cause": a.cause, "risk": a.risk, "compensation": a.compensation,
        "owner": a.owner, "opened": today.isoformat(),
        "due": (today + _dt.timedelta(days=a.days)).isoformat(),
    }
    state.setdefault("tickets", []).append(ticket)
    _save(state)
    print(f"[debt] 已开票 {ticket['id']}（due={ticket['due']}，{a.days} 天）")
    return 0


def cmd_clear(a: argparse.Namespace) -> int:
    state = _load()
    before = len(state.get("tickets", []))
    state["tickets"] = [t for t in state.get("tickets", []) if t.get("id") != a.id]
    if len(state["tickets"]) == before:
        print(f"[debt] ✗ 未找到 {a.id}")
        return 2
    state.setdefault("cleared", []).append(
        {"id": a.id, "cleared": _today().isoformat(), "reason": a.reason})
    _save(state)
    print(f"[debt] 已清票 {a.id}（留痕：{a.reason}）")
    return 0


def cmd_show() -> int:
    print(json.dumps(_load(), ensure_ascii=False, indent=1))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="S5 豁免带息债务台账")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="校验台账（到期/字段/负债率）").set_defaults(
        fn=lambda _a: cmd_check())
    p_add = sub.add_parser("add", help="开票（owner 必须 human:*）")
    p_add.add_argument("--cause", required=True)
    p_add.add_argument("--risk", required=True)
    p_add.add_argument("--compensation", required=True)
    p_add.add_argument("--owner", required=True)
    p_add.add_argument("--days", type=int, default=30)
    p_add.set_defaults(fn=cmd_add)
    p_cl = sub.add_parser("clear", help="清票（必须写 reason）")
    p_cl.add_argument("--id", required=True)
    p_cl.add_argument("--reason", required=True)
    p_cl.set_defaults(fn=cmd_clear)
    sub.add_parser("show", help="查看台账").set_defaults(fn=lambda _a: cmd_show())
    a = ap.parse_args(argv)
    return int(a.fn(a))


if __name__ == "__main__":
    raise SystemExit(main())
