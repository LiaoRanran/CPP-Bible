"""612 B1 回归测试：活性锚自动候选生成（只读）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import liveness_candidate_generator as b1  # noqa: E402


def test_generation_covers_all_missing_props():
    d = b1.build()
    assert d["total_props"] == 50
    assert len(d["per_prop"]) == 50


def test_classes_all_present():
    d = b1.build()
    assert d["counts"]["A"] > 0 and d["counts"]["B"] > 0 and d["counts"]["C"] > 0


def test_generic_symbols_never_high():
    d = b1.build()
    for r in d["rows"]:
        if r["symbol"] in b1.GENERIC:
            assert r["confidence"] != "high"


def test_candidate_format():
    d = b1.build()
    for r in d["rows"][:20]:
        assert {"proposition_id", "symbol", "confidence", "source_file", "kind"} <= set(r)
        assert r["kind"] == "fixture_symbol"
        assert r["confidence"] in ("high", "medium", "low")


def test_c_class_has_no_high_candidate():
    d = b1.build()
    for p in d["per_prop"]:
        if p["class"] == "C":
            assert all(c["confidence"] != "high" for c in p["candidates"])


def test_check_passes():
    assert b1.main(["--check"]) == 0
