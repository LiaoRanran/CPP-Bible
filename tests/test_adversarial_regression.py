"""adversarial_regression 回归锁（494 任务 6）。

纪律：测试**不真跑探针**（那是 `--dir` 实跑路径的职责，耗时且依赖沙箱目录），
只锁三件可机器验证的事：①自述解析分类正确（含阴性对照）②回归锁映射可解析且**文件真实存在**
③escape/gap → exit 1、blocked → exit 0。
"""
from __future__ import annotations

import adversarial_regression as ar
import pytest


def test_parse_output_classifies():
    """自述行解析：『逃逸』→ escape、『已拦』→ blocked、『对照』→ control（阴性不计逃逸）。"""
    text = (
        "[N2 全局恒真断言        ] confirm  | 逃逸（零信息断言，卡 confirm）\n"
        "[E10a 字段位移          ] refute   | gate=block → 已拦\n"
        "[  对照·纯计算夹具      ] confirm  | exp-scan=False（阴性应无命中）\n"
        "无法解析的噪声行\n")
    rows = ar.parse_output(text)
    assert [r["kind"] for r in rows] == ["escape", "blocked", "control"]


def test_lock_mapping_and_files_exist():
    """标签前缀能映射到回归锁，且**锁文件必须真实存在**（否则映射就是假的）。"""
    assert ar._lock_for("E10a 字段位移")[0].endswith("test_p0f_zerodiag.py")
    assert ar._lock_for("E05 cat 式证据")[0].endswith("test_p0b_echo.py")
    assert ar._lock_for("NO-SUCH-PROBE") is None
    missing = [lock for lock, _ in ar._LOCKS.values() if not (ar.ROOT / lock).is_file()]
    assert missing == [], f"映射的回归锁文件缺失（锁表失真）：{missing}"


def test_exit_code_follows_escape_and_gap(monkeypatch: pytest.MonkeyPatch):
    """escape/gap → exit 1；只有 blocked/skip → exit 0（skip ≠ pass 由计数体现）。"""
    monkeypatch.setattr(ar, "scan", lambda d: ([{"probe": "p", "kind": "script",
                                                "status": "escape", "reason": "自述仍逃逸"}], []))
    assert ar.main([]) == 1
    monkeypatch.setattr(ar, "scan", lambda d: ([{"probe": "p", "kind": "script",
                                                "status": "gap", "reason": "无锁"}], []))
    assert ar.main([]) == 1
    monkeypatch.setattr(ar, "scan", lambda d: ([{"probe": "p", "kind": "script",
                                                "status": "blocked", "reason": "ok"},
                                               {"probe": "q", "kind": "doc",
                                                "status": "skip", "reason": "需人判"},
                                               {"probe": "v", "kind": "script",
                                                "status": "visible", "reason": "warn"}], []))
    assert ar.main([]) == 0, "visible（可见化层）不得阻断门禁，但须计数"
