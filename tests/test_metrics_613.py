#!/usr/bin/env python3
"""F2 回归测试：metrics_613（六线关键数字汇总，现场复算）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import metrics_613 as f2  # noqa: E402


def test_collect_has_all_six_lines():
    m = f2.collect()
    for k in ("A_liveness", "B_d5", "C_learner", "D_argument", "E_trust", "F_escape"):
        assert k in m


def test_line_a_numbers():
    m = f2.collect()
    assert m["A_liveness"]["missing_anchors"] == 50
    assert m["A_liveness"]["low_cost"] == 9
    assert m["A_liveness"]["warn_after"] == m["A_liveness"]["warn_before"] - 9


def test_line_c_kc_and_empty_behavior():
    m = f2.collect()
    assert m["C_learner"]["kc"] == 27
    assert m["C_learner"]["behavior_events"] == 0, "尚无真实行为事件"


def test_line_d_honest_status():
    m = f2.collect()
    assert m["D_argument"]["candidates"] == 98
    assert m["D_argument"]["human_reviewed"] == 0
    assert m["D_argument"]["components_now"] == 11


def test_line_e_pending_and_proofs():
    m = f2.collect()
    assert "pending" in m["E_trust"]["ots_attestation"]
    assert m["E_trust"]["merkle_proofs_ok"] == m["E_trust"]["merkle_proofs_total"]


def test_line_f_multi_caliber():
    m = f2.collect()
    assert len(m["F_escape"]) == 5
    first = m["F_escape"][0]
    assert first["k"] == 1 and first["n"] == 1406


def test_render_covers_six_sections():
    page = f2.render(f2.collect())
    for sec in ("线A", "线B", "线C", "线D", "线E", "线F"):
        assert sec in page


def test_check_passes():
    assert f2.main(["--check"]) == 0
