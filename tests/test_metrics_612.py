#!/usr/bin/env python3
"""E 线回归测试：metrics_612（E1-E3 度量，只读）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import metrics_612 as e  # noqa: E402


def test_e2_fragmentation_counts():
    d = e.e2_fragmentation()
    assert d["atomic"] == 27
    assert d["mis"] == 79
    assert d["evidence"] > 0
    assert d["total"] == d["atomic"] + d["evidence"] + d["mis"]
    assert d["artifacts_per_kc"] > 0


def test_e3_oracle_quality_zero_review():
    q = e.e3_oracle_quality()
    assert q["total"] == 83
    assert q["distinct_reviewers"] == 0
    assert q["reviews_done"] == 0
    assert q["modifications"] == 0
    assert "gate" in q["gate_time"] and "poison" in q["gate_time"]
    assert q["quality_note"]


def test_e1_modify_modes_locked():
    m = e.e1_modify_modes()
    assert (m["keep-low"]["IN"], m["keep-low"]["OUT"]) == (114, 7)
    assert (m["upgrade-medium"]["IN"], m["upgrade-medium"]["OUT"]) == (121, 0)


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
