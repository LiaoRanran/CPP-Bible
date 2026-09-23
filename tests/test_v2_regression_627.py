"""627 B2 · V2 回归验证（静态）单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import v2_regression_627 as R


def test_core_tools_isolated():
    r = R.check()
    assert r["all_isolated"]
    assert all(x["isolated"] for x in r["core_tools"])


def test_w2_solver_unchanged():
    r = R.check()
    assert r["w2_solver_unchanged"]


def test_no_core_change():
    r = R.check()
    assert r["no_core_change"]


def test_regression_passed():
    r = R.check()
    assert r["passed"]


def test_forbidden_patterns_absent():
    # 在 CORE_TOOLS 中不应出现任何被禁模式
    import re
    here = os.path.join(os.path.dirname(__file__), "..", "tools")
    for ct in R.CORE_TOOLS:
        p = os.path.join(here, ct)
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8", errors="ignore").read()
        for pat in R.FORBIDDEN_PATTERNS:
            assert not re.search(re.escape(pat), txt), f"{ct} 含禁项 {pat}"
