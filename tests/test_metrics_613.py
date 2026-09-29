#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
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
    """666 A2 去写死：原断言 50 / 9 / 差值 9（613 时点快照，语料长到 60 就假红）。

    改为**口径不变量 + 事实源对齐**：
      · 投影差值 == 低成本可补条数（投影只吃 low 档）；
      · 缺锚数 == 线A 工具现场算出的候选数（派生 vs 事实源）；
      · low 是缺锚的子集且非空。
    """
    import liveness_priority_613 as a1

    m = f2.collect()
    A = m["A_liveness"]
    assert A["warn_after"] == A["warn_before"] - A["low_cost"]
    assert 0 < A["low_cost"] <= A["missing_anchors"]
    assert A["missing_anchors"] == len(a1.build())


def test_line_c_kc_and_empty_behavior():
    m = f2.collect()
    assert m["C_learner"]["kc"] == 27
    assert m["C_learner"]["behavior_events"] == 0, "尚无真实行为事件"


def test_line_d_honest_status():
    """666 A2 去写死：原断言 candidates==98 / components_now==11（613 时点快照）。

    改为**诚实态 + 不变量**：人审仍为 0（这是"诚实"本身，必须锁死）；
    分量投影不得多于现状（合并只减不增）；深度 > 0。
    """
    import argument_fragmentation_613 as frag

    m = f2.collect()
    D = m["D_argument"]
    assert D["human_reviewed"] == 0, "人审数一旦非 0，本行就该改写口径（诚实登记）"
    assert D["components_now"] == frag.projection()["components_before"]
    assert D["components_projection"] <= D["components_now"]
    assert D["max_defense_depth"] and D["max_defense_depth"] > 0


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
