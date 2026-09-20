#!/usr/bin/env python3
"""A3 回归测试：golden_lock_proposal_613（只读提案，绝不 accept）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import golden_lock_proposal_613 as a3  # noqa: E402


def test_locked_baseline_and_delta():
    d = a3.build()
    assert d["locked_warn"] == 136
    assert d["current_warn"] == 186
    assert d["delta"] == 50


def test_block_unchanged():
    d = a3.build()
    assert d["locked_block"] == 0 and d["current_block"] == 0


def test_proposal_is_not_an_accept():
    page = a3.render(a3.build())
    assert "提案，不是执行" in page
    assert "人审权力" in page
    assert "OBSERVATION-LIVENESS" in page
    assert "legacy" in page


def test_snapshot_has_classify_table():
    d = a3.build()
    assert isinstance(d["classify_now"], dict)


def test_check_passes():
    assert a3.main(["--check"]) == 0
