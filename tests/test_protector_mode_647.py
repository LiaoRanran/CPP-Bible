"""647 B5 公共件 · 保护器全局模式开关回归锁（编号 PM-1..PM-6）。"""
from __future__ import annotations

import json
import os

import pytest

import protector_mode_647 as M


def test_pm1_default_is_enforce():
    assert M.DEFAULT_MODE == "enforce"
    assert M.MODES == ("enforce", "shadow")


def test_pm2_env_overrides(monkeypatch):
    monkeypatch.setenv(M.ENV, "shadow")
    assert M.mode() == "shadow" and M.is_enforce() is False
    assert M.source().startswith("环境变量")
    monkeypatch.setenv(M.ENV, "enforce")
    assert M.is_enforce() is True


def test_pm3_illegal_env_falls_back(monkeypatch):
    monkeypatch.setenv(M.ENV, "bogus")
    assert M.mode() in M.MODES


def test_pm4_set_mode_rejects_illegal():
    with pytest.raises(ValueError):
        M.set_mode("nope")


def test_pm5_mode_file_roundtrip(tmp_path, monkeypatch):
    f = tmp_path / "mode.json"
    monkeypatch.setattr(M, "MODE_FILE", str(f))
    monkeypatch.delenv(M.ENV, raising=False)
    M.rollback()
    assert json.loads(f.read_text(encoding="utf-8"))["mode"] == "shadow"
    assert M.mode() == "shadow" and M.is_enforce() is False
    assert M.source().startswith("模式文件")
    M.enforce()
    assert M.mode() == "enforce"


def test_pm6_selftest_and_status():
    assert M.selftest() == 0
    st = M.status()
    assert {"mode", "source", "default", "mode_file"} <= set(st)
    assert os.path.basename(st["mode_file"]) == "647_protector_mode.json"
