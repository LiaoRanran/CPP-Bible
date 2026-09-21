#!/usr/bin/env python3
"""616 D1 回归测试：他验三件套架构设计。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "data" / "independent_verification_architecture_616.md"


def test_architecture_doc_exists() -> None:
    assert DOC.is_file() and DOC.stat().st_size > 0
    text = DOC.read_text(encoding="utf-8")
    assert "核心设计原则" in text and "风险与挑战" in text


def test_three_pieces_designed() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "独立复核层" in text
    assert "VSA" in text and "验证凭证" in text
    assert "透明日志" in text
