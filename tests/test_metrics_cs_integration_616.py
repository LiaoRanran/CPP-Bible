#!/usr/bin/env python3
"""616 A3 回归测试：metrics_collector 集成置信序列（cs_* 字段）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import confidence_sequence as cs  # noqa: E402
import metrics_collector as mc  # noqa: E402


def _rate() -> dict:
    return mc.collect_curves()["mutation_escape_rate"]


def test_new_cs_fields_exist() -> None:
    r = _rate()
    for k in ("cs_alpha", "cs_lower", "cs_upper", "cs_lower_raw", "cs_upper_raw",
              "peeking_correction", "cp_vs_cs_note"):
        assert k in r, f"缺字段 {k}"
    # 旧字段保留
    for k in ("point", "cp_low", "cp_high"):
        assert k in r
    assert r["peeking_correction"] is True and r["cs_alpha"] == 0.05


def test_cs_upper_more_conservative_than_cp() -> None:
    r = _rate()
    assert r["cs_upper_raw"] > r["cp_high_raw"]          # anytime 更保守


def test_zero_escape_cs_upper_correct() -> None:
    # 与 A1/A2 一致；0 逃逸轨迹对齐 p02（n=1000,x=0 ⇒ 0.9856%）
    assert abs(cs.cs_upper(1406, 1) - 0.009062) < 5e-5
    assert abs(cs.cs_upper(1000, 0) - 0.009856) < 5e-5


def test_schema_doc_exists() -> None:
    p = ROOT / "data" / "metrics_schema_616.md"
    assert p.is_file() and p.stat().st_size > 0
    text = p.read_text(encoding="utf-8")
    assert "cs_upper" in text and "历史参考" in text
