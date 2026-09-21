#!/usr/bin/env python3
"""615 B2 回归测试：EV-MATRIX 分歧修复（一致率不降 + 提案文件存在）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_unbacked_v2 as v2  # noqa: E402


def test_aligned_rate_not_below_before() -> None:
    before = v2._rate(v2.compare())
    after = v2.compare_aligned()["rate"]
    assert after >= before
    assert after == 1.0            # 补上预处理后 100%（19/19）
    assert abs(before - 13 / 19) < 1e-9


def test_proposal_and_fix_report_exist() -> None:
    for name in ("ev_matrix_rule_definition_proposal_615.md",
                 "ev_matrix_dual_impl_fix_615.md"):
        p = ROOT / "data" / name
        assert p.is_file() and p.stat().st_size > 0, f"缺 {name}"
    fix = (ROOT / "data" / "ev_matrix_dual_impl_fix_615.md").read_text(encoding="utf-8")
    assert "68.4%" in fix and "100" in fix
