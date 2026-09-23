"""627 D1 · push 前检查清单 单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pre_push_checklist_627 as P


def test_tools_all_check_pass():
    r = P.run_all()
    assert all(t["ok"] for t in r["tools"])


def test_static_clean():
    r = P.run_all()
    assert r["static"]["ruff_ok"] and r["static"]["mypy_ok"]


def test_controlled_clean():
    r = P.run_all()
    assert r["controlled"]["clean"]


def test_core_untouched():
    r = P.run_all()
    assert r["core_untouched"]["untouched"]


def test_no_git_push_in_source():
    src = open(P.__file__, encoding="utf-8").read()
    import re
    cmds = re.findall(r'\["git",\s*"([^"]+)"', src)
    assert "push" not in cmds


def test_run_all_aggregates_ok():
    import unittest.mock as mock
    # check_tests 会嵌套调用 pytest，在 pytest 内部运行会冲突；此处打桩以验证聚合逻辑
    with mock.patch.object(P, "check_tests", return_value={
            "test_files": 10, "tests_passed": True, "pytest_rc": 0}):
        r = P.run_all()
    assert r["all_ok"]
