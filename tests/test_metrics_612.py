#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""E 线回归测试：metrics_612（E1-E3 度量，只读）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import counts_659 as counts  # noqa: E402
import metrics_612 as e  # noqa: E402
import w2_authority_640b as auth  # noqa: E402


def test_e2_fragmentation_counts():
    d = e.e2_fragmentation()
    assert d["atomic"] == counts.ATOMS_TOTAL
    assert d["mis"] == 79
    assert d["evidence"] > 0
    assert d["total"] == d["atomic"] + d["evidence"] + d["mis"]
    assert d["artifacts_per_kc"] > 0


def test_e3_oracle_quality_zero_review():
    """670a 去写死：oracle 分母改为与 611 D3 同口径现算（CARDS_TOTAL），不再冻结 CARDS_REAL。"""
    q = e.e3_oracle_quality()
    assert q["total"] == counts.CARDS_TOTAL
    assert q["distinct_reviewers"] == 0
    assert q["reviews_done"] == 0
    assert q["modifications"] == 0
    assert "gate" in q["gate_time"] and "poison" in q["gate_time"]
    assert q["quality_note"]


def test_e1_modify_modes_locked():
    """670a 去写死：原冻结 (89,42)（640 时点快照）。改为与 W2 权威源现算一致 + 双档趋同。"""
    m = e.e1_modify_modes()
    ref = auth.current()
    assert (m["keep-low"]["IN"], m["keep-low"]["OUT"]) == (ref["IN"], ref["OUT"])
    assert (m["upgrade-medium"]["IN"], m["upgrade-medium"]["OUT"]) == (ref["IN"], ref["OUT"])


def test_render_has_three_sections():
    e1 = e.e1_modify_modes()
    e2 = e.e2_fragmentation()
    e3 = e.e3_oracle_quality()
    page = e.render(e1, e2, e3)
    assert "## E1 · modify 双模式一致性" in page
    assert "## E2 · artifact 碎片化统计" in page
    assert "## E3 · oracle 人审质量指标" in page
    assert "原子卡" in page and "MIS" in page


def test_main_check_passes():
    assert e.main(["--check"]) == 0


def test_main_writes_report():
    rc = e.main([])
    assert rc == 0
    p = Path(__file__).resolve().parents[1] / "data" / "metrics_612.md"
    assert p.is_file() and p.stat().st_size > 1000
