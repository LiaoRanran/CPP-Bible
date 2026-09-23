"""627 B3 · V2 启用/回滚 单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import authority_v2_switch_627 as S


def test_enable_sets_mode():
    try:
        S.write_mode(True, by="test")
        assert S.read_mode()["enabled"] is True
    finally:
        S.write_mode(False, by="test")


def test_rollback_resets_mode():
    S.write_mode(True, by="test")
    S.write_mode(False, by="test")
    assert S.read_mode()["enabled"] is False


def test_default_off():
    p = S.MODE_FILE
    if os.path.exists(p):
        os.remove(p)
    assert S.read_mode()["enabled"] is False


def test_effective_env_in_range():
    assert S.effective_env_value() in ("0", "1")


def test_run_compiler_mode(tmp_path=None):
    # 关闭模式下 run 不应崩溃（返回 0）
    S.write_mode(False, by="test")
    rc = S.run_compiler_in_mode("w2")
    assert rc == 0
