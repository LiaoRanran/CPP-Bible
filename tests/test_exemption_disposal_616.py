#!/usr/bin/env python3
"""616 C2 回归测试：27 条 legacy 豁免到期处置清单。"""
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import exemption_expiry as ex  # noqa: E402


def test_all_27_have_disposal() -> None:
    disp = ex.dispose()
    assert len(disp) == len(ex.load_exemptions())     # 624 D3：动态口径
    for x in disp:
        assert x["suggestion"] and x["rationale"] and x["risk"]
        assert x["category"] in ("advice级", "教学/资产类", "字段/枚举/结构类")


def test_category_summary_correct() -> None:
    disp = ex.dispose()
    cats = Counter(x["category"] for x in disp)
    assert sum(cats.values()) == len(ex.load_exemptions())
    # 每条的类别必须与其建议并存（分类汇总可复算）
    assert set(cats) <= {"advice级", "教学/资产类", "字段/枚举/结构类"}


def test_disposal_file_exists() -> None:
    p = ROOT / "data" / "exemption_expiry_disposal_616.md"
    assert p.is_file() and p.stat().st_size > 0
    text = p.read_text(encoding="utf-8")
    assert "不自动删除" in text and "分类汇总" in text and "逐条处置建议" in text
