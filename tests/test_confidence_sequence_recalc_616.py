#!/usr/bin/env python3
"""616 A2 回归测试：v1-v7 置信序列重算。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import confidence_sequence as cs  # noqa: E402

VERSIONS = [("v1", 956, 227), ("v2", 969, 61), ("v3", 997, 38), ("v4", 998, 38),
            ("v5", 1375, 1), ("v6", 1379, 1), ("v7", 1406, 1)]
REPORT = ROOT / "data" / "confidence_sequence_recalc_616.md"


def test_v7_recalc_matches_a1() -> None:
    up = cs.cs_upper(1406, 1)
    assert abs(up - 0.009062) < 5e-5          # 与 A1 一致
    assert abs(cs.cp_upper(1406, 1) - 0.003370) < 5e-5


def test_cs_ge_cp_for_all_versions() -> None:
    for _v, n, x in VERSIONS:
        assert cs.cs_upper(n, x) > cs.cp_upper(n, x), f"{_v}: CS 应 > CP"


def test_peeking_inflation_recorded_and_directional() -> None:
    # 报告须记录历史参考虚报 13.80%（覆盖率 86.2% < 95%）
    text = REPORT.read_text(encoding="utf-8")
    assert "13.80%" in text and "86.2%" in text and "0.9062%" in text
    # 小规模 MC 方向：置信序列虚报不高于固定样本 CP
    mc = cs.monte_carlo_peek(reps=200, nmax=300, step=20)
    assert mc["cs_false_alarm"] <= mc["cp_false_alarm"]
