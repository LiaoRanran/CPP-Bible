#!/usr/bin/env python3
"""615 B1 回归测试：ev_matrix_unbacked_v2（独立第二实现）。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_unbacked_v2 as v2  # noqa: E402

_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+gate_engine\b")


def test_no_gate_engine_import() -> None:
    src = (ROOT / "tools" / "ev_matrix_unbacked_v2.py").read_text(encoding="utf-8")
    # 只看真正的 import 语句（注释/文档串里的说明不算）
    assert not any(_IMPORT_RE.match(ln) for ln in src.splitlines())
    # 独立运行不崩
    c = v2.compare()
    assert c["n_crash"] == 0


def test_all_evidence_cards_get_verdict_or_skip() -> None:
    c = v2.compare()
    assert c["raw_cards"] >= 56            # 全证据卡被扫
    assert c["applicable"] == 19           # 多编译器适用卡
    assert len(c["natural"]) == 19 and len(c["official"]) == 19


def test_agreement_in_reasonable_range() -> None:
    c = v2.compare()
    rate = c["agree"] / c["applicable"]
    assert 0.50 <= rate <= 1.0
    # 与历史记录一致（68.4% / 6 分歧卡）
    assert rate == 13 / 19
    assert {r["card"] for r in c["diverge"]} == v2.HISTORICAL_DIVERGENT
