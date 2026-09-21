#!/usr/bin/env python3
"""A3 回归测试：golden_lock_proposal_613（只读提案，绝不 accept）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import golden_lock_proposal_613 as a3  # noqa: E402


def test_locked_baseline_and_delta():
    d = a3.build()
    # OBSERVATION-LIVENESS 50 条已按 A3 方案② 分类为 legacy（commit dd5b029），
    # 基线 136→186，current==locked、delta=0（已锁定）。
    assert d["current_warn"] == d["locked_warn"]
    assert d["delta"] == 0
    assert d["classify_now"].get("OBSERVATION-LIVENESS") == "legacy"


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
