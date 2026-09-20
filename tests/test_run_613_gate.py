#!/usr/bin/env python3
"""F3 回归测试：run_613_gate（收工门禁脚本）。

注意：不在 pytest 内跑全量门禁（含 ~245s 回归 + 监工记录，且与收工门禁重复）；
只校验门禁清单构造、单步执行器、报告渲染与 status 更新逻辑。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_613_gate as g  # noqa: E402


def test_all_listed_tools_exist_and_have_check():
    for t in g.TOOLS:
        p = ROOT / "tools" / f"{t}.py"
        assert p.is_file(), f"{t}.py 不存在"
        # 有的工具用单引号注册 '--check'（如 d5_source_integrity）⇒ 只匹配 --check 本身
        assert "--check" in p.read_text(encoding="utf-8"), f"{t}.py 缺 --check"


def test_monitors_are_separate_from_conclusion():
    """监工类必须在 MONITORS 里，且不在结论项 TOOLS 里（铁律：只记录不作结论）。"""
    names = {m[0] for m in g.MONITORS}
    assert {"tool_integrity", "gate_engine", "poison_drill", "atom_evidence_replay"} <= names
    for m in g.MONITORS:
        assert m[0] not in g.TOOLS


def test_run_step_reports_rc():
    r = g._run(["-c", "import sys; sys.exit(0)"], 60)
    assert r[0] == 0
    r2 = g._run(["-c", "import sys; sys.exit(3)"], 60)
    assert r2[0] == 3


def test_render_marks_failures_and_verdict():
    page = g.render({"x": {"rc": 1, "tail": "boom", "sec": 0.1}}, None, None, None, True, False)
    assert "❌" in page and "门禁未通过" in page
    page2 = g.render({"x": {"rc": 0, "tail": "ok", "sec": 0.1}}, None, None, None, True, True)
    assert "门禁全绿" in page2


def test_render_includes_monitors_section_when_full():
    page = g.render({"x": {"rc": 0, "tail": "ok", "sec": 0.1}},
                    {"ruff": {"rc": 0, "tail": "clean", "sec": 0.1}},
                    {"clean": True, "detail": ""},
                    {"tool_integrity": {"rc": 0, "tail": "ok", "sec": 1.0}}, False, True)
    assert "仅记录，不作结论" in page
    assert "零污染" in page


def test_update_status_sets_awaiting_review(tmp_path, monkeypatch):
    st = tmp_path / "status.json"
    monkeypatch.setattr(g, "STATUS", st)
    g.update_status(True)
    doc = json.loads(st.read_text(encoding="utf-8"))
    assert doc["status"] == "awaiting_review"
    assert doc["batch"] == "613"
    assert doc["history"][-1]["verdict"] == "PASS"
