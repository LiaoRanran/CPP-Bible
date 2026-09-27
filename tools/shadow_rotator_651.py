#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""shadow_rotator_651.py — M2 变异器/规则/模型 shadow 轮转（651 W3，**只记账，不上岗**）。

为什么（651 W3-M2）：647 的实测教训是"保护器触发≈0"——因为新东西一上来就被当成品/或压根没进
监督视野。解药：**任何新变异器 / 新规则 / 新模型，一律先 shadow 一批（N 轮只记账）**，
攒够轮次才"**有资格**"被人审考虑上岗；本工具**只做轮转与记账，绝不自动上岗/拦截**。

用法
====
    python tools/shadow_rotator_651.py --check                 # 合成自检
    python tools/shadow_rotator_651.py --advance               # 轮转一轮（读/写 shadow 台账）
    python tools/shadow_rotator_651.py --status                # 看台账
    python tools/shadow_rotator_651.py --register NAME --kind mutator

诚实边界：`eligible` 只是"影子轮次攒够"，**≠ 通过**；上岗需人审 + 校准（M3）。台账 append-only。
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "protector", "name": "shadow_rotator_651", "entry": "ShadowRotator",
                "description": "M2 新变异器/规则/模型先 shadow N 轮（只记账，不上岗）"}

LEDGER = ROOT / "data" / "651_m2_shadow_log.json"
SHADOW_ROUNDS_DEFAULT = 3
KINDS = ("mutator", "rule", "model")


@dataclass
class Candidate:
    name: str
    kind: str
    entered_round: int
    remaining: int
    state: str = "shadow"  # shadow | eligible


@dataclass
class Rotator:
    round: int = 0
    candidates: list[Candidate] = field(default_factory=list)
    log: list[dict] = field(default_factory=list)

    def register(self, name: str, kind: str, shadow_rounds: int = SHADOW_ROUNDS_DEFAULT) -> Candidate:
        if kind not in KINDS:
            raise ValueError(f"未知 kind={kind}（白名单 {KINDS}）")
        if any(c.name == name for c in self.candidates):
            raise ValueError(f"重复注册 {name}")
        c = Candidate(name, kind, self.round, shadow_rounds)
        if shadow_rounds <= 0:
            c.state = "eligible"
        self.candidates.append(c)
        self.log.append({"round": self.round, "event": "register", "name": name, "kind": kind})
        return c

    def advance(self) -> dict:
        self.round += 1
        for c in self.candidates:
            if c.state == "shadow":
                c.remaining -= 1
                if c.remaining <= 0:
                    c.remaining = 0
                    c.state = "eligible"
                    self.log.append({"round": self.round, "event": "eligible", "name": c.name})
        snapshot = {"round": self.round, "candidates": [asdict(c) for c in self.candidates]}
        self.log.append({"round": self.round, "event": "advance"})
        return snapshot

    def status(self) -> dict:
        return {
            "round": self.round,
            "shadow": [c.name for c in self.candidates if c.state == "shadow"],
            "eligible": [c.name for c in self.candidates if c.state == "eligible"],
            "note": "eligible ≠ 通过：需人审 + 校准（M3）才可上岗；本工具不上岗/不拦截。",
        }

    def to_dict(self) -> dict:
        return {"round": self.round, "candidates": [asdict(c) for c in self.candidates], "log": self.log}

    @classmethod
    def from_dict(cls, d: dict) -> "Rotator":
        r = cls(round=d.get("round", 0), log=list(d.get("log", [])))
        r.candidates = [Candidate(**c) for c in d.get("candidates", [])]
        return r


def load_ledger() -> Rotator:
    if LEDGER.is_file():
        return Rotator.from_dict(json.loads(LEDGER.read_text(encoding="utf-8")))
    return Rotator()


def save_ledger(r: Rotator) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(r.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = Rotator()
    r.register("m_new", "mutator", 3)
    chk("注册后 shadow", r.status()["shadow"] == ["m_new"])
    r.advance()
    chk("1 轮后仍 shadow", r.candidates[0].state == "shadow" and r.candidates[0].remaining == 2)
    r.advance()
    r.advance()
    chk("3 轮后 eligible", r.candidates[0].state == "eligible")
    chk("eligible 不再在 shadow", r.status()["shadow"] == [])
    # 非法 kind / 重复注册
    try:
        r.register("x", "bogus")
        chk("非法 kind 被拒", False)
    except ValueError:
        chk("非法 kind 被拒", True)
    try:
        r.register("m_new", "mutator")
        chk("重复注册被拒", False)
    except ValueError:
        chk("重复注册被拒", True)
    # 0 轮直接 eligible
    r2 = Rotator()
    r2.register("z", "rule", 0)
    chk("0 轮 ⇒ eligible", r2.candidates[0].state == "eligible")
    # 序列化往返
    r3 = Rotator.from_dict(r.to_dict())
    chk("往返一致", r3.round == r.round and len(r3.candidates) == len(r.candidates))
    print(f"shadow_rotator_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 M2 shadow 轮转（只记账）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--advance", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--register", default=None)
    ap.add_argument("--kind", default="mutator", choices=list(KINDS))
    ap.add_argument("--rounds", type=int, default=SHADOW_ROUNDS_DEFAULT)
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    r = load_ledger()
    if a.register:
        r.register(a.register, a.kind, a.rounds)
        save_ledger(r)
        print(f"已注册 {a.register}({a.kind}) 进 shadow {a.rounds} 轮")
        return 0
    if a.advance:
        snap = r.advance()
        save_ledger(r)
        print(json.dumps(snap, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps(r.status(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
