"""638 E1 · 收工门禁单测（>=5 例，轻量；**不触发** build()/pytest 以免递归）。"""
from __future__ import annotations

import os

import tools.run_638_gate as m


# E1-1：7 个新工具清单且文件都在
def test_new_tools_manifest():
    assert len(m.NEW_TOOLS) == 7
    assert "run_638_gate" in m.NEW_TOOLS
    for t in m.NEW_TOOLS:
        assert os.path.exists(os.path.join(m.ROOT, "tools", f"{t}.py")), t


# E1-2：8 个任务与编号
def test_task_deliverables_manifest():
    assert len(m.TASK_DELIVERABLES) == 8
    assert [d["task"] for d in m.TASK_DELIVERABLES] == [
        "0", "3.1", "3.2", "B1", "B2", "C1", "C2", "E1"]
    for d in m.TASK_DELIVERABLES:
        assert d["name"] and d["files"]


# E1-3：交付物检查结构（行数 = 文件总数）
def test_check_deliverables_shape():
    d = m.check_deliverables()
    total = sum(len(x["files"]) for x in m.TASK_DELIVERABLES)
    assert d["n"] == total and len(d["rows"]) == total
    assert isinstance(d["missing"], list)
    assert d["ok"] == (not d["missing"])


# E1-4：自举——本报告按 pending 处理，不会因「报告尚不存在」而失败
def test_self_report_pending_bootstrap():
    d = m.check_deliverables(pending=["data/638_acceptance_report.md"])
    row = [r for r in d["rows"] if r["file"].endswith("638_acceptance_report.md")][0]
    assert row["ok"] is True
    assert "data/638_acceptance_report.md" not in d["missing"]


# E1-5：受控目录定义与零污染实测
def test_controlled_dirs():
    assert m.CONTROLLED == ["atoms", "evidence", "Examples", "Book"]
    c = m.check_controlled()
    assert c["ok"] is True and c["exit"] == 0


# E1-6：测试套件发现逻辑（只查文件，不执行）
def test_638_test_files_found():
    import glob
    files = sorted(glob.glob(os.path.join(m.ROOT, "tests", "test_*638*.py")))
    assert len(files) >= 7
    names = {os.path.basename(f) for f in files}
    for t in m.NEW_TOOLS:
        if t == "run_638_gate":
            continue
        assert f"test_{t}.py" in names, t


# E1-7：只读契约与输出路径
def test_paths_and_readonly_contract():
    assert m.ACCEPTANCE.startswith(os.path.join(m.ROOT, "data"))
    assert m.RESULT_JSON.startswith(os.path.join(m.ROOT, "data"))
    src = open(os.path.join(m.ROOT, "tools", "run_638_gate.py"), encoding="utf-8").read()
    assert "--check" in src and "--report" in src
