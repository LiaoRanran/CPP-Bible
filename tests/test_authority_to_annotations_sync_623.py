"""623 D1 · Authority→annotations 同步工具 单元测试（≥4 例）"""
from __future__ import annotations

import importlib.util
import json
import os
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "authority_to_annotations_sync_623.py")


def _load():
    spec = importlib.util.spec_from_file_location("auth_sync_623", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _jl(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_power_map():
    mod = _load()
    assert mod.POWER_MAP["ACCEPT"] == "approve"
    assert mod.POWER_MAP["REJECT"] == "reject"
    assert mod.POWER_MAP["MODIFY"] == "modify"


def test_sync_adds_new_edge():
    mod = _load()
    with tempfile.TemporaryDirectory() as td:
        auth = [{"decision_id": "d1", "power": "ACCEPT", "target": {"id": "ae-NEW->ATOM-X::p1"},
                 "decided_at": "2026-09-20T00:00:00", "reviewer": "human:Alice", "reason": "r"}]
        ann = [{"edge_id": "ae-OLD->ATOM-Y::p1", "action": "approve", "reviewer": "Bob",
                "timestamp": "2026-09-19T00:00:00"}]
        _jl(os.path.join(td, "a.jsonl"), auth)
        _jl(os.path.join(td, "b.jsonl"), ann)
        synced, stats = mod.sync(mod.load_jsonl(os.path.join(td, "a.jsonl")),
                                  mod.load_jsonl(os.path.join(td, "b.jsonl")))
        assert stats["added"] == 1
        assert len(synced) == 2
        assert any(s["edge_id"] == "ae-NEW->ATOM-X::p1" for s in synced)


def test_sync_idempotent():
    mod = _load()
    with tempfile.TemporaryDirectory() as td:
        auth = [{"decision_id": "d1", "power": "ACCEPT", "target": {"id": "ae-A->ATOM-B::p1"},
                 "decided_at": "2026-09-20T00:00:00", "reviewer": "human:Alice", "reason": "r"}]
        ann = []
        _jl(os.path.join(td, "a.jsonl"), auth)
        _jl(os.path.join(td, "b.jsonl"), ann)
        s1, _ = mod.sync(mod.load_jsonl(os.path.join(td, "a.jsonl")), [])
        s2, _ = mod.sync(mod.load_jsonl(os.path.join(td, "a.jsonl")), s1)
        assert len(s1) == len(s2) == 1, "按 edge_id 去重，不应重复"


def test_newer_overrides_action():
    mod = _load()
    with tempfile.TemporaryDirectory() as td:
        ann = [{"edge_id": "ae-A->ATOM-B::p1", "action": "approve",
                "timestamp": "2026-09-19T00:00:00", "source": "annotations"}]
        auth = [{"decision_id": "d1", "power": "REJECT", "target": {"id": "ae-A->ATOM-B::p1"},
                 "decided_at": "2026-09-20T00:00:00", "reviewer": "human:Alice", "reason": "r"}]
        _jl(os.path.join(td, "a.jsonl"), auth)
        _jl(os.path.join(td, "b.jsonl"), ann)
        synced, stats = mod.sync(mod.load_jsonl(os.path.join(td, "a.jsonl")),
                                  mod.load_jsonl(os.path.join(td, "b.jsonl")))
        rec = next(s for s in synced if s["edge_id"] == "ae-A->ATOM-B::p1")
        assert rec["action"] == "reject", "较新 authority 决策应覆盖旧 annotations 的 action"
        assert stats["updated"] == 1
