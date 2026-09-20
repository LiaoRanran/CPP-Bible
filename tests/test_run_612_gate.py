#!/usr/bin/env python3
"""Z 线回归测试：run_612_gate（收工门禁脚本）。

注意：不在 pytest 内重跑全部门禁（会触发 250s+ 全量回归）；仅校验门禁模块自身的可用性与
污染检查逻辑（git 调用走 _run 直接执行，不绕 venv python）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import run_612_gate as z  # noqa: E402


def test_all_tools_exist_and_have_check():
    for t in z.TOOLS:
        p = Path(__file__).resolve().parents[1] / "tools" / f"{t}.py"
        assert p.is_file(), f"{t}.py 不存在"
        assert '"--check"' in p.read_text(encoding="utf-8"), f"{t}.py 缺 --check"


def test_pollution_clean():
    # 当前受控目录应干净（相对 HEAD 无改动）
    res = z.gate_pollution()
    assert res["atoms/"] is True
    assert res["evidence/"] is True
    assert res["Examples/"] is True
    assert res["Book/"] is True
    assert res["untracked_or_modified"] is True


def test_render_runs():
    tool_res = {t: {"rc": 0, "tail": "ok", "sec": 0.1} for t in z.TOOLS}
    page = z.render(tool_res, (0, 0.1), (0, "ok", 1.0), (0, "x passed", 1.0),
                    (0, "clean", 1.0), {"atoms/": True, "evidence/": True,
                    "Examples/": True, "Book/": True, "untracked_or_modified": True}, quick=False)
    assert "612 收工验收报告" in page
    assert "门禁全绿" in page
