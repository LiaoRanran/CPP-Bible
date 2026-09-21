#!/usr/bin/env python3
"""616 B3 回归测试：EV-MATRIX 双实现一致性回归锁。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_dual_impl_lock as lock  # noqa: E402


def test_lock_tool_and_comparison() -> None:
    assert (ROOT / "tools" / "ev_matrix_dual_impl_lock.py").is_file()
    c = lock.compare()
    assert c["applicable"] == 19
    assert c["agree"] + len(c["diverge"]) == c["applicable"]


def test_baseline_file_exists() -> None:
    p = ROOT / "data" / "ev_matrix_dual_impl_baseline_616.json"
    assert p.is_file()
    d = json.loads(p.read_text(encoding="utf-8"))
    for k in ("applicable", "agree", "rate", "status", "pass_threshold"):
        assert k in d
    assert d["rate"] >= 0.95 and d["status"] == "pass"


def test_check_passes() -> None:
    assert lock.check() == []
