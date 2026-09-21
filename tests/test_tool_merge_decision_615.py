#!/usr/bin/env python3
"""615 E1 回归测试：工具合并决策（仅决策，不执行）。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "data" / "tool_merge_decision_615.md"


def _rows() -> list[tuple[str, str, str]]:
    """解析决策表：返回 (族, 决策, 理由)。"""
    out = []
    for ln in DECISION.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|$", ln)
        if m and m.group(1) not in ("族", "---"):
            out.append((m.group(1), m.group(2), m.group(3)))
    return out


def test_decision_file_exists_with_rows() -> None:
    assert DECISION.is_file()
    rows = _rows()
    assert len(rows) >= 10                  # 覆盖多族


def test_decision_values_are_known() -> None:
    for _family, _tools, decision in _rows():
        assert decision in ("不合并", "标注（交人）", "合并"), f"未知决策：{decision}"


def test_no_execution_performed() -> None:
    """仅决策：报告须显式声明未执行，且工具文件仍在（未被删/合并）。"""
    text = DECISION.read_text(encoding="utf-8")
    assert "仅决策" in text or "未执行" in text
    # 抽样确认被点名的工具仍在
    for name in ("run_614_gate.py", "metrics_613.py", "learner_twin_dashboard_614.py"):
        assert (ROOT / "tools" / name).is_file()
