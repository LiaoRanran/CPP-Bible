"""643 阶段0 · pytest_two_phase_643 单测（命令定义 / junit 计数 / 标记机制 / 预算）。
编号 P0-1..P0-7。**本模块不真跑 pytest**（真跑由 `run_643_gate` 与命令行负责）。
"""
from __future__ import annotations

import json
import os

import pytest_two_phase_643 as T


# P0-1：两阶段命令定义正确（fast 并行 / slow 串行）
def test_phase_commands():
    assert T.PHASES["fast"] == ["-m", "not slow", "-n", "auto"]
    assert T.PHASES["slow"] == ["-m", "slow", "-n0"]


# P0-2：junit 计数口径（含 passed 反推）
def test_counts_from_junit(tmp_path):
    xml = ('<?xml version="1.0"?><testsuites>'
           '<testsuite name="p" tests="7" failures="1" errors="1" skipped="2">'
           '<testcase classname="tests.x" name="a"/>'
           '<testcase classname="tests.x" name="b"><failure message="m"/></testcase>'
           '<testcase classname="tests.x" name="c"><error message="m"/></testcase>'
           '</testsuite></testsuites>')
    f = tmp_path / "j.xml"
    f.write_text(xml, encoding="utf-8")
    c = T.counts_from_junit(str(f))
    assert c == {"tests": 7, "failures": 1, "errors": 1, "skipped": 2, "passed": 3}


# P0-3：失败 node id 提取（**必须含 .py**，否则 pytest 选不中而静默 0 例）
def test_failed_node_ids(tmp_path):
    xml = ('<?xml version="1.0"?><testsuite name="p" tests="2" failures="1">'
           '<testcase classname="tests.test_a" name="ok"/>'
           '<testcase classname="tests.test_a" name="bad"><failure message="m"/></testcase>'
           '</testsuite>')
    f = tmp_path / "j.xml"
    f.write_text(xml, encoding="utf-8")
    assert T.failed_node_ids(str(f)) == ["tests/test_a.py::bad"]
    assert T.node_id_of.__doc__ and ".py" in T.node_id_of.__doc__


# P0-3b：净化 —— ANSI/控制字符不得落进 data/（本批实测踩过的真缺陷）
def test_sanitize_removes_ansi_and_control_chars(tmp_path):
    dirty = "\x1b[33m'atoms'\x1b[39;49;00m\x08\x0c tail"
    clean = T.sanitize(dirty)
    assert "\x1b" not in clean and "\x08" not in clean and "\x0c" not in clean
    assert "atoms" in clean and "tail" in clean
    assert T.sanitize("a\tb\nc\rd") == "a\tb\nc\rd", "Tab/换行必须保留"
    f = tmp_path / "d.txt"
    f.write_bytes(b"x\x1by\x08z")
    assert T.sanitize_file(str(f)) == 2
    assert f.read_bytes() == b"xyz"
    assert T.sanitize_file(str(f)) == 0, "已干净 ⇒ 报 0"
    # 本模块写盘路径上的**所有**文本产物都必须过净化
    src = open(T.__file__, encoding="utf-8").read() if hasattr(T, "__file__") else ""
    assert "--color=no" in src, "pytest 命令必须禁色（源头不产 ANSI）"


# P0-4：缺失 XML ⇒ 零计数（不抛错，便于"未跑"判定）
def test_missing_junit_is_zero(tmp_path):
    c = T.counts_from_junit(str(tmp_path / "nope.xml"))
    assert c["tests"] == 0 and c["passed"] == 0
    assert T.failed_node_ids(str(tmp_path / "nope.xml")) == []


# P0-5：green 语义 —— 跑了且 0 失败/0 错误才算绿
def test_green_requires_tests_and_no_failures(tmp_path, monkeypatch):
    xml = ('<?xml version="1.0"?><testsuite name="p" tests="3" failures="0" errors="0" '
           'skipped="1"/>')
    f = tmp_path / "643_pytest_fast.xml"
    f.write_text(xml, encoding="utf-8")
    monkeypatch.setattr(T, "junit_path", lambda ph: str(f))
    assert T.green("fast") is True
    xml_bad = xml.replace('failures="0"', 'failures="1"')
    f.write_text(xml_bad, encoding="utf-8")
    assert T.green("fast") is False


# P0-6：标记机制在册（conftest 打标 + pyproject 不把 -n auto 放 addopts）
def test_marker_machinery_is_in_place():
    conf = open(os.path.join(T.ROOT, "tests", "conftest.py"), encoding="utf-8").read()
    assert "SLOW_MODULES" in conf and "SERIAL_EXTRA" in conf
    assert "item.add_marker(pytest.mark.slow if slow else pytest.mark.fast)" in conf
    pyproj = open(os.path.join(T.ROOT, "pyproject.toml"), encoding="utf-8").read()
    ini = pyproj.split("[tool.pytest.ini_options]")[1]
    assert "-n auto" not in ini.split("addopts =")[1].splitlines()[0]


# P0-7：--check 自检 + 报告 JSON schema 可写
def test_selftest_and_json_schema(tmp_path, monkeypatch):
    assert T.selftest() == 0
    f = tmp_path / "p.json"
    monkeypatch.setattr(T, "OUT_JSON", str(f))
    T._save_meta("fast", {"exit_code": 0, "seconds": 12.5, "cmd": "c", "budget_s": 120.0})
    d = json.loads(f.read_text(encoding="utf-8"))
    assert d["schema"] == "pytest_two_phase/1"
    assert d["phases"]["fast"]["seconds"] == 12.5
