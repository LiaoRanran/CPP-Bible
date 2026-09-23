"""627 D1 · push 前检查清单 单测（≥4 例）。

631 A3：其中 2 例依赖 627 工具 `pck_hash_drift_analyzer_627 --check`，而该自检断言的是
**628 A2 修复之前**的状态（"全部有缺口"）。628 把 PCK hash 修好后该断言不可能成立；
修它要改 **627 工具**（§零.11 越界）⇒ 本批只在测试侧按**条件跳过**，条件由实测数据算出
（drift==0 ⇒ 该自检必然失败），不是无条件 skip。
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pck_hash_drift_analyzer_627 as A
import pre_push_checklist_627 as P


def _drift_resolved() -> bool:
    """实测：内容漂移是否已修好（628 A2）⇒ 627 工具的"全有缺口"断言必然过期。"""
    try:
        return int(A.analyze()["n_content_drift_certs"]) == 0
    except Exception:                                         # noqa: BLE001
        return False


# 条件+理由都写死在代码里，运行时 `-rs` 可见，**不静默通过**
skip_if_drift_resolved = pytest.mark.skipif(
    _drift_resolved(),
    reason="627 工具 pck_hash_drift_analyzer_627 --check 断言『无健康证书（全部有缺口）』；"
           "628 A2 修复 PCK hash 后实测 content_drift=0 ⇒ 该自检必然失败。"
           "修它需改 627 工具（§零.11 越界）⇒ 631 A3 条件跳过，交人")


@skip_if_drift_resolved
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


@skip_if_drift_resolved
def test_run_all_aggregates_ok():
    import unittest.mock as mock
    # check_tests 会嵌套调用 pytest，在 pytest 内部运行会冲突；此处打桩以验证聚合逻辑
    with mock.patch.object(P, "check_tests", return_value={
            "test_files": 10, "tests_passed": True, "pytest_rc": 0}):
        r = P.run_all()
    assert r["all_ok"]
