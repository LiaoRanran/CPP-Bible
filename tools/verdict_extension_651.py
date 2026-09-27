#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verdict_extension_651.py — T1 判决扩展 schema（651 W2，**只加字段不改语义**）。

为什么（651 W2-T1）：现有判决表达不了四类边界事实（条件/部分命题/显式冲突/unknown 原因）。
本工具按 `docs/verdict_extension.md` 提供 **schema 校验 + 历史回填（dry-run）**，铁律：
- **只加字段，绝不改** `state` / `decision_id` / 哈希链字段；
- 旧证书（无新字段）校验 **PASS**（视为 v1，向后兼容）；
- 新写入的枚举值必须在**封闭白名单**内，否则**拒绝**（fail-closed，封 647 A2 默认值洞）。

用法
====
    python tools/verdict_extension_651.py --check                 # 合成自检
    python tools/verdict_extension_651.py --backfill [PATH]       # 历史回填 dry-run（默认 452 账本）
    python tools/verdict_extension_651.py --json

诚实边界：真正的"每卡四态判决"存在卡/证书层；本工具以**可得历史产物**（默认 452 账本）
做回填试跑，并报告"改了 N 条 / 原文件 sha256 不变"。卡级判决回填需卡→判决映射（交人）。
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

QUEYI_PLUGIN = {"kind": "schema", "name": "verdict_extension_651", "entry": "validate",
                "description": "T1 判决扩展 schema（conditions/partial_atoms/conflict/unknown_reason），fail-closed"}

DEFAULT_LEDGER = ROOT / "data" / "authority" / "decision_event_v2_ledger.jsonl"
SCHEMA_VERSION = 2

CONDITION_KINDS = {"platform", "compiler_version", "std_version", "optimization", "input_domain", "assumption", "other"}
CONFLICT_STATES = {"none", "detected", "resolved"}
UNKNOWN_REASONS = {
    "no_evidence", "evidence_conflict", "out_of_scope", "implementation_defined",
    "insufficient_samples", "tool_unavailable", "not_applicable", "other",
}
# 必须原样保留的字段（回填不得改动）
IMMUTABLE = ("state", "decision_id", "event_id", "result", "prev_hash", "entry_hash")


def validate(v: dict) -> list[str]:
    """返回错误列表（空=通过）。旧证书缺新字段 ⇒ 不报错（v1 兼容）。"""
    errs: list[str] = []
    for f in IMMUTABLE:
        if f in v and v[f] is None:
            errs.append(f"{f} 为 null（不允许）")
    # conditions
    conds = v.get("conditions")
    if conds is not None:
        if not isinstance(conds, list):
            errs.append("conditions 必须是数组")
        else:
            for i, c in enumerate(conds):
                if not isinstance(c, dict) or "kind" not in c:
                    errs.append(f"conditions[{i}] 缺 kind")
                    continue
                if c["kind"] not in CONDITION_KINDS:
                    errs.append(f"conditions[{i}].kind={c['kind']} 不在白名单（fail-closed）")
    # partial_atoms
    pas = v.get("partial_atoms")
    if pas is not None:
        if not isinstance(pas, list):
            errs.append("partial_atoms 必须是数组")
        else:
            for i, p in enumerate(pas):
                if not isinstance(p, dict) or "atom_id" not in p or not isinstance(p.get("covered"), bool):
                    errs.append(f"partial_atoms[{i}] 需 atom_id + covered(bool)")
    # conflict
    cs = v.get("conflict_state")
    if cs is not None:
        if cs not in CONFLICT_STATES:
            errs.append(f"conflict_state={cs} 不在白名单")
        if cs == "resolved" and not isinstance(v.get("conflict_detail"), dict):
            errs.append("conflict_state=resolved 需 conflict_detail")
    # unknown_reason
    ur = v.get("unknown_reason")
    if ur is not None and ur not in UNKNOWN_REASONS:
        errs.append(f"unknown_reason={ur} 不在白名单（fail-closed）")
    if ur == "other" and not v.get("unknown_note"):
        errs.append("unknown_reason=other 需 unknown_note")
    return errs


def backfill(v: dict) -> tuple[dict, dict]:
    """返回 (新对象, 变更 diff)。**只加字段**，不动 IMMUTABLE。"""
    out = dict(v)
    diff: dict = {}
    if "schema_version" not in out:
        out["schema_version"] = SCHEMA_VERSION
        diff["schema_version"] = SCHEMA_VERSION
    if "conditions" not in out:
        out["conditions"], diff["conditions"] = [], []
    if "partial_atoms" not in out:
        out["partial_atoms"], diff["partial_atoms"] = [], []
    if "conflict_state" not in out:
        out["conflict_state"], diff["conflict_state"] = "none", "none"
    if "unknown_reason" not in out:
        # 不臆测根因：仅当原文显式 unknown 才填 other+note，否则保持 null
        state = str(v.get("state", "")).lower()
        if state == "unknown":
            out["unknown_reason"] = "other"
            out["unknown_note"] = "回填：旧证书未记原因，待人工判定"
            diff["unknown_reason"] = "other"
        else:
            out["unknown_reason"] = None
            diff["unknown_reason"] = None
    return out, diff


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def backfill_file(path: Path, dry_run: bool = True) -> dict:
    before = _sha256(path)
    rows = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    changed, errors = 0, 0
    samples: list[dict] = []
    for ln in rows:
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            errors += 1
            continue
        _, diff = backfill(obj)
        if diff:
            changed += 1
            if len(samples) < 3:
                samples.append({"keys_added": list(diff.keys())})
    after = _sha256(path)
    return {
        "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "records": len(rows), "would_change": changed, "parse_errors": errors,
        "sha256_before": before[:16], "sha256_after": after[:16], "unchanged": before == after,
        "dry_run": dry_run, "samples": samples,
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 旧证书（无新字段）⇒ 校验通过（v1 兼容）
    chk("旧证书校验通过", validate({"decision_id": "D1", "state": "pass"}) == [])
    # 非法枚举 ⇒ 拒绝
    chk("非法 conflict_state 被拒", validate({"conflict_state": "maybe"}) != [])
    chk("非法 unknown_reason 被拒", validate({"unknown_reason": "wat"}) != [])
    chk("resolved 缺 detail 被拒", validate({"conflict_state": "resolved"}) != [])
    chk("other 缺 note 被拒", validate({"unknown_reason": "other"}) != [])
    chk("合法扩展通过", validate({"conflict_state": "detected", "unknown_reason": "no_evidence",
                                   "conditions": [{"kind": "platform", "expr": "x"}],
                                   "partial_atoms": [{"atom_id": "A", "covered": False}]}) == [])
    # 回填只加字段，不动 immutables
    v = {"decision_id": "D1", "state": "unknown", "result": "APPROVE"}
    new, diff = backfill(v)
    chk("回填不动 immutable", new["decision_id"] == "D1" and new["state"] == "unknown" and new["result"] == "APPROVE")
    chk("回填加 schema_version=2", new["schema_version"] == 2)
    chk("unknown 态回填 other+note", new["unknown_reason"] == "other" and bool(new.get("unknown_note")))
    # 非 unknown 不回填 reason（不臆测）
    new2, _ = backfill({"state": "pass"})
    chk("pass 态 unknown_reason=None", new2["unknown_reason"] is None)
    # 幂等
    new3, diff3 = backfill(new)
    chk("回填幂等（二次无 diff）", diff3 == {})
    print(f"verdict_extension_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 T1 判决扩展 schema（只加字段/fail-closed）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--backfill", nargs="?", const=str(DEFAULT_LEDGER), default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.backfill:
        rep = backfill_file(Path(a.backfill))
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps({"schema_version": SCHEMA_VERSION, "condition_kinds": sorted(CONDITION_KINDS),
                      "conflict_states": sorted(CONFLICT_STATES), "unknown_reasons": sorted(UNKNOWN_REASONS)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
