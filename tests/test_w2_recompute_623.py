"""623 D2 · W2 重算 单元测试（可复现性 / 关键结论）"""
from __future__ import annotations

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "w2_recompute_623.py")
ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
SYNCED = os.path.join(ROOT, "data", "human_attack_edge_annotations.synced.jsonl")


def _load():
    spec = importlib.util.spec_from_file_location("w2_623", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_atom_parsing():
    mod = _load()
    assert mod._atom_of("ae-MIS-X->ATOM-Y::prop-3") == "ATOM-Y"
    assert mod._atom_of("bad-format") is None


def test_verdict_aggregation():
    mod = _load()
    anns = [
        {"edge_id": "ae-A->ATOM-B::p1", "action": "approve"},
        {"edge_id": "ae-C->ATOM-B::p2", "action": "reject"},
        {"edge_id": "ae-D->ATOM-E::p1", "action": "modify"},
    ]
    v = mod.verdicts(anns)
    assert v["ATOM-B"] == "OUT"   # 有 reject
    assert v["ATOM-E"] == "UNRESOLVED"  # 仅 modify


def test_recompute_reports_eight_changes():
    mod = _load()
    orig = mod.verdicts(mod.load(ANN))
    sync = mod.verdicts(mod.load(SYNCED))
    changed = [a for a in sorted(set(orig) | set(sync)) if orig.get(a) != sync.get(a)]
    assert len(changed) == 8, f"应有 8 原子变化，实际 {len(changed)}"
    assert all(orig.get(a) == "UNRESOLVED" for a in changed)
    assert all(sync.get(a) == "IN" for a in changed)
