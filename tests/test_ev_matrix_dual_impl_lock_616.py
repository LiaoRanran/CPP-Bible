#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
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
    # 去写死（669 P0）：applicable 原写死 == 19。新证据卡只增不减，故改历史下限锁。
    assert c["applicable"] >= 19   # 历史下限（615 时 19 张多编译器适用卡）
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
