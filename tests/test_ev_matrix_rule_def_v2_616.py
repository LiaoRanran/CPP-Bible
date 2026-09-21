#!/usr/bin/env python3
"""616 B1 回归测试：EV-MATRIX 规则定义补全文档 v2。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "data" / "ev_matrix_rule_definition_v2.md"

DIVERGENT = ["EV-CONC-001", "EV-CONC-002", "EV-MEM-001", "EV-MEM-039", "EV-MEM-042", "EV-MEM-043"]


def test_doc_exists_nonempty() -> None:
    assert DOC.is_file() and DOC.stat().st_size > 0
    text = DOC.read_text(encoding="utf-8")
    for kw in ("规则目的", "判定语义", "预处理清单", "版本历史"):
        assert kw in text


def test_preprocessing_includes_artifact_sha256() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "artifact_sha256" in text
    assert "剥去 `actual:`" in text or "剥去 `actual:` 段" in text.replace("- ", "")


def test_all_divergent_cards_listed() -> None:
    text = DOC.read_text(encoding="utf-8")
    for card in DIVERGENT:
        assert card in text, f"分歧卡 {card} 未在预处理说明中列出"
