#!/usr/bin/env python3
"""616 D3 回归测试：他验落地路线图。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "data" / "independent_verification_roadmap_616.md"


def test_roadmap_exists() -> None:
    assert DOC.is_file() and DOC.stat().st_size > 0
    text = DOC.read_text(encoding="utf-8")
    assert "关键决策点" in text and "边界" in text


def test_five_phases_with_acceptance() -> None:
    text = DOC.read_text(encoding="utf-8")
    for ph in ("阶段 0", "阶段 1", "阶段 2", "阶段 3", "阶段 4"):
        assert ph in text, f"缺 {ph}"
    # 每阶段都有验收标准
    assert text.count("验收标准") >= 4
