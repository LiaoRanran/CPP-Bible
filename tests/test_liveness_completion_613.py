#!/usr/bin/env python3
"""A2 回归测试：liveness_completion_613（低成本补全补丁集 · 不落卡）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import liveness_completion_613 as a2  # noqa: E402
import liveness_priority_613 as a1  # noqa: E402


def test_low_cost_count():
    assert len(a2.load_low_cost()) == 9


def test_all_patches_valid():
    for r in a2.load_low_cost():
        assert a2.validate_anchor(r) == [], f"{r['proposition_id']}: {a2.validate_anchor(r)}"


def test_patch_shape():
    for r in a2.load_low_cost():
        p = a2.patch_of(r)
        assert p["liveness"]["kind"] == "fixture_symbol"
        assert p["liveness"]["symbol"]
        assert p["claim_type"] == "observation"
        assert p["card"] and p["proposition_id"].startswith(p["card"])


def test_validate_rejects_universal_and_empty():
    bad_empty = {"best_symbol": "", "best_kind": "fixture_symbol", "source_file": "EV-X"}
    bad_univ = {"best_symbol": "main", "best_kind": "fixture_symbol", "source_file": "EV-X"}
    bad_kind = {"best_symbol": "_Z3foov", "best_kind": "external_basis", "source_file": "EV-X"}
    assert a2.validate_anchor(bad_empty)
    assert a2.validate_anchor(bad_univ)
    assert a2.validate_anchor(bad_kind)


def test_projection_is_before_minus_addressed():
    proj = a2.projection(9)
    assert proj["warn_before"] == 50
    assert proj["warn_after"] == 41
    assert proj["addressed"] == 9


def test_render_contains_yaml_fragment():
    rows = a2.load_low_cost()
    patches = [a2.patch_of(r) for r in rows]
    page = a2.render(patches, {}, a2.projection(len(patches)), len(a1.build()))
    assert "待插入 YAML 片段" in page
    assert "kind: fixture_symbol" in page
    assert "尚未落卡" in page


def test_check_passes():
    assert a2.main(["--check"]) == 0
