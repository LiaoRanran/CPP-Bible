#!/usr/bin/env python3
"""615 F1 回归测试：run_615_gate（收工门禁脚本）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_615_gate as g  # noqa: E402


def test_all_tools_green_config() -> None:
    """2 例之一：全绿——所有 615 工具文件存在且 render 判 PASS。"""
    for t in g.TOOLS:
        assert (ROOT / "tools" / f"{t}.py").is_file(), f"缺 tools/{t}.py"
    tools = {t: {"rc": 0, "tail": "ok", "sec": 0.1} for t in g.TOOLS}
    page = g.render(tools, None, None, True, True)
    assert "615 收工验收报告" in page and "可收工" in page


def test_simulated_failure_and_status(tmp_path: Path) -> None:
    """2 例之二：模拟失败——render 判未通过；update_status 写 batch 615。"""
    tools = {t: {"rc": 0, "tail": "ok", "sec": 0.1} for t in g.TOOLS}
    tools[g.TOOLS[0]]["rc"] = 1
    page = g.render(tools, None, None, True, False)
    assert "615 自身门禁未通过" in page
    sp = tmp_path / "status.json"
    g.update_status(False, sp)
    st = json.loads(sp.read_text(encoding="utf-8"))
    assert st["last_completed_batch"] == 615 and st["history"][-1]["verdict"] == "FAIL"
