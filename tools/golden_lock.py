#!/usr/bin/env python3
"""S4 黄金非回归锁：达标状态固化为快照，任何指标**恶化** → exit 1。

底座 = ADR-0005（`l2_state.py` 的快照-漂移三件套：measure → save → check）。

指标（全部机器可复算，禁止手工填写）：
    block_findings   gate_engine 的 block 级命中数（↑ = 质量下降 → 红）
    warn_findings    warn 级命中数（↑ = 记债增加 → 红）
    atoms_total      原子数（↓ = 回滚 → 红）
    evidence_total   证据卡数（↓ = 证据被删 → 红）
    verified_atoms   verified 原子数（↓ = 降级 → 红）
    replay_confirm   证据卡机器复算通过数（↓ = 证据失效 → 红）

语义：
    * 恶化 → 红；改善（数量↑ / 命中↓）→ 提示 `sync` 更新基线。
    * 口径/阈值变更**不得静默**：`check --accept "理由"` 显式接受并写入快照审计字段。

用法：
    python tools/golden_lock.py sync                    # 达标时固化快照
    python tools/golden_lock.py check                   # 比对（CI / prepush 用）
    python tools/golden_lock.py check --accept "理由"    # 显式接受恶化（留痕）
    python tools/golden_lock.py show
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Sequence, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

STATE = ROOT / "tools/golden_state.json"
SCHEMA = "cppbible-golden-lock/1.0"

# key → True 表示「上升是恶化」，False 表示「下降是恶化」
WORSE: dict[str, bool] = {
    "block_findings": True,
    "warn_findings": True,
    "atoms_total": False,
    "evidence_total": False,
    "verified_atoms": False,
    "replay_confirm": False,
}


def measure() -> dict[str, int]:
    """全部指标现场复算（不读任何手工数字）。"""
    import gate_engine as ge
    import atom_evidence_replay as replay

    findings = ge.run(include_advice=False)
    atoms_root, evid_root = Path(ge.ATOMS), Path(ge.EVIDENCE)
    atoms = sorted(atoms_root.rglob("ATOM-*.md")) if atoms_root.exists() else []
    evids = sorted(evid_root.rglob("EV-*.md")) if evid_root.exists() else []

    def _status(p: Path) -> str:
        try:
            return str(replay.parse_frontmatter(
                p.read_text(encoding="utf-8", errors="replace")).get("status") or "")
        except ValueError:
            return ""

    confirm = 0
    for p in evids:
        verdict, _ = replay.replay_card(p, do_sanitizer=False)
        if verdict == "confirm":
            confirm += 1

    return {
        "block_findings": sum(1 for f in findings if f.severity == "block"),
        "warn_findings": sum(1 for f in findings if f.severity == "warn"),
        "atoms_total": len(atoms),
        "evidence_total": len(evids),
        "verified_atoms": sum(1 for p in atoms if _status(p) == "verified"),
        "replay_confirm": confirm,
    }


def _load() -> dict[str, Any]:
    if not STATE.exists():
        return {"schema": SCHEMA, "updated": "", "commit": "", "metrics": {},
                "accepted": []}
    return cast(dict[str, Any], json.loads(STATE.read_text(encoding="utf-8")))


def _save(state: dict[str, Any]) -> None:
    payload = json.dumps(state, ensure_ascii=False, indent=1) + "\n"
    STATE.write_bytes(payload.encode("utf-8"))


def cmd_sync() -> int:
    state = _load()
    state.update({"schema": SCHEMA, "updated": _dt.date.today().isoformat(),
                  "metrics": measure()})
    _save(state)
    print(f"[golden] 快照已固化：{state['metrics']}（{STATE.name}）")
    return 0


def cmd_check(accept: str | None) -> int:
    state = _load()
    base = state.get("metrics") or {}
    if not base:
        print("[golden] 无基线——先跑 `sync` 固化当前达标状态")
        return 2
    now = measure()
    worse: list[str] = []
    improved: list[str] = []
    for key, up_is_worse in WORSE.items():
        b, n = base.get(key, 0), now.get(key, 0)
        if (n > b) if up_is_worse else (n < b):
            worse.append(f"{key}: {b} → {n}")
        elif (n < b) if up_is_worse else (n > b):
            improved.append(f"{key}: {b} → {n}")
    print(f"[golden] 恶化 {len(worse)} · 改善 {len(improved)}")
    for w in worse:
        print(f"  WORSE {w}")
    for i in improved:
        print(f"  BETTER {i}")
    if worse:
        if accept:
            state.setdefault("accepted", []).append(
                {"ts": _dt.datetime.now().isoformat(timespec="seconds"),
                 "reason": accept, "worse": worse})
            _save(state)
            print(f"[golden] 已显式接受并留痕（{len(state['accepted'])} 条审计记录）")
            return 0
        print("[golden] ✗ 指标恶化——修复，或 `check --accept \"理由\"` 显式留痕")
        return 1
    if improved:
        print("[golden] 有改善：跑 `sync` 更新基线（把进步锁进黄金快照）")
    print("[golden] ✅ 无恶化")
    return 0


def cmd_show() -> int:
    state = _load()
    print(json.dumps(state, ensure_ascii=False, indent=1))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="S4 黄金非回归锁")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync", help="固化当前状态为快照").set_defaults(fn=lambda _a: cmd_sync())
    p_ck = sub.add_parser("check", help="比对快照，恶化即 exit 1")
    p_ck.add_argument("--accept", help="显式接受恶化（必须给理由，审计留痕）")
    p_ck.set_defaults(fn=lambda a: cmd_check(a.accept))
    sub.add_parser("show", help="查看快照").set_defaults(fn=lambda _a: cmd_show())
    a = ap.parse_args(argv)
    return int(a.fn(a))


if __name__ == "__main__":
    raise SystemExit(main())
