#!/usr/bin/env python3
"""614 F1 回归测试：run_614_gate（收工门禁脚本）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_614_gate as g  # noqa: E402


def test_tools_exist() -> None:
    for t in g.TOOLS:
        assert (ROOT / "tools" / f"{t}.py").is_file(), f"缺 tools/{t}.py"


def test_render_has_sections() -> None:
    tools = {t: {"rc": 0, "tail": "ok", "sec": 0.1} for t in g.TOOLS}
    page = g.render(tools, None, None, True, True)
    assert "614 收工验收报告" in page
    assert "614 工具 --check" in page
    assert "PASS" not in page or "可收工" in page


def test_render_full_includes_monitor_note() -> None:
    tools = {t: {"rc": 0, "tail": "ok", "sec": 0.1} for t in g.TOOLS}
    hyg = {"ruff": {"rc": 0, "tail": "ok", "sec": 1},
           "mypy": {"rc": 0, "tail": "ok", "sec": 1},
           "pytest_614": {"rc": 0, "tail": "ok", "sec": 1},
           "pytest_full": {"rc": 1, "tail": "既有红灯", "sec": 1}}
    page = g.render(tools, hyg, {"clean": True, "detail": ""}, False, True)
    assert "本批不跑" in page and "交监工" in page
    assert "tool_integrity --check" in page
    assert "614 自身门禁全绿" in page


def test_update_status_writes_batch_614(tmp_path: Path) -> None:
    sp = tmp_path / "status.json"
    g.update_status(True, sp)
    st = json.loads(sp.read_text(encoding="utf-8"))
    assert st["batch"] == "614" and st["status"] == "awaiting_review"
    assert st["history"][-1]["verdict"] == "PASS"
