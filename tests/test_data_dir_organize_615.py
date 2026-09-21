#!/usr/bin/env python3
"""615 E2 回归测试：data/ 整理方案（仅方案，不移动）。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "data_dir_organize_615.md"


def test_plan_exists_with_sections() -> None:
    assert PLAN.is_file()
    text = PLAN.read_text(encoding="utf-8")
    for kw in ("目标结构", "移动清单", "引用影响", "分阶段计划"):
        assert kw in text, f"方案缺小节：{kw}"


def test_reference_impact_named() -> None:
    text = PLAN.read_text(encoding="utf-8")
    # 引用影响须点名真实引用方
    assert "metrics_collector" in text
    assert "test_escape_rate_trend_610" in text
    assert "learner_mastery_update_613" in text


def test_no_move_executed() -> None:
    # 仅方案：历史基线仍在原位、data/reports/ 未创建
    for v in (1, 2, 3, 4, 5):
        assert (ROOT / "data" / "mutation" / f"full_baseline_v{v}.json").is_file(), "基线被移动了"
    assert not (ROOT / "data" / "reports").exists(), "data/reports/ 不应存在（仅方案）"
