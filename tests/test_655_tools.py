#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""655 批工具回归锁：许可证头检查 / 增量测试选择 / pytest 结果缓存。

设计原则（与 655 任务书一致）：
- **只读**：所有用例不写生产文件；结果缓存用 ``tmp_path`` 隔离；
- **不依赖环境**：无 git / 无 pytest 历史时走退化路径，断言"不炸且给出诚实结论"。
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

lic = importlib.import_module("license_header_check_655")
sel = importlib.import_module("test_selector_655")
rcl = importlib.import_module("result_cache_655")
shd = importlib.import_module("pytest_shard_655")


# ── A：许可证头 ─────────────────────────────────────────────────────────────
def test_header_insert_idempotent_and_preserves_body() -> None:
    src = '"""模块文档。"""\n\nVALUE = 1\n'
    once = lic.insert_header(src)
    assert once.splitlines()[0] == lic.SPDX_LINE
    assert once.splitlines()[1] == lic.COPYRIGHT_LINE
    assert lic.insert_header(once) == once, "二次插入必须无变化（幂等）"
    assert src.rstrip("\n") in once, "原正文不得丢字节"


def test_header_after_shebang_and_coding() -> None:
    src = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nX = 1\n"
    out = lic.insert_header(src)
    lines = out.splitlines()
    assert lines[0].startswith("#!"), "shebang 必须仍是第 1 行"
    assert "coding" in lines[1], "coding 行必须仍在前两行（PEP 263）"
    assert (lines[2], lines[3]) == (lic.SPDX_LINE, lic.COPYRIGHT_LINE)


def test_header_preserves_crlf_and_bom() -> None:
    crlf = "#!/usr/bin/env python3\r\nX = 1\r\n"
    out = lic.insert_header(crlf)
    assert out.count(lic.SPDX_LINE + "\r") == 1, "CRLF 文件插入的头也必须是 CRLF"
    assert "\n" not in out.replace("\r\n", ""), "不得引入裸 LF"
    bom = lic.insert_header("\ufeffX = 1\n")
    assert bom.startswith("\ufeff"), "BOM 必须保持在文件第 1 字节"


def test_header_detection() -> None:
    assert lic.header_status("# SPDX-License-Identifier: Apache-2.0\n")[0] is True
    assert lic.header_status("# SPDX-License-Identifier: MIT\n")[0] is False
    assert lic.header_status("X = 1\n")[0] is False


def test_scope_membership() -> None:
    assert lic.in_scope(ROOT / "tools" / "a.py", "active") is True
    assert lic.in_scope(ROOT / "tests" / "a.py", "active") is True
    assert lic.in_scope(ROOT / "web" / "a.py", "active") is True
    assert lic.in_scope(ROOT / "conftest.py", "active") is True
    assert lic.in_scope(ROOT / "_archive" / "a.py", "active") is False
    assert lic.in_scope(ROOT / "_archive" / "a.py", "all") is True


def test_active_scope_fully_covered() -> None:
    """回归锁：活跃源码必须 100% 带 Apache-2.0 头（655 A 的验收点）。"""
    rep = lic.scan("active")
    assert rep["checked"] > 0
    assert rep["missing_count"] == 0, f"缺头文件：{rep['missing'][:10]}"
    assert rep["no_copyright_count"] == 0, f"缺版权行：{rep['no_copyright'][:10]}"


def test_selftest_exit_zero() -> None:
    assert lic.selftest() == 0


@pytest.mark.parametrize("flag", ["--check", "--json"])
def test_cli_readonly_paths(flag: str, capsys: pytest.CaptureFixture[str]) -> None:
    code = lic.main([flag, "--scope", "active"])
    capsys.readouterr()
    assert code == 0


# ── C 杠杆 1：增量测试选择（fail-safe 是核心不变量）──────────────────────────
def test_selector_picks_own_test_for_tool_change() -> None:
    rep = sel.select(["tools/license_header_check_655.py"])
    assert rep["full_suite"] is False
    assert "tests/test_655_tools.py" in rep["selected"]


def test_selector_fail_safe_on_high_risk_and_unknown() -> None:
    for risky in (["tools/gate_engine.py"], ["tools/.tool_checksums"], ["pyproject.toml"],
                  ["某个/没见过的.bin"]):
        rep = sel.select(risky)
        assert rep["full_suite"] is True, risky
        assert rep["selected_count"] == rep["total_test_files"]


def test_selector_no_change_is_empty() -> None:
    rep = sel.select([])
    assert rep["selected"] == [] and rep["full_suite"] is False


def test_selector_selftest() -> None:
    assert sel.selftest() == 0


# ── C 杠杆 2：结果缓存（哈希校验是核心不变量）────────────────────────────────
def test_cache_hit_then_drift_then_tamper(tmp_path: Path) -> None:
    dep = ROOT / ".pytest_tmp" / "cache655_test" / "dep.py"
    dep.parent.mkdir(parents=True, exist_ok=True)
    dep.write_text("X = 1\n", encoding="utf-8")
    cpath = tmp_path / "cache.json"
    rel = dep.relative_to(ROOT).as_posix()
    inputs = {rel: rcl._sha256_file(dep)}
    key = rcl.make_key(["tests/not-exist.py"], inputs)
    rcl.record(key, {"tests": 1}, inputs, cpath)
    assert rcl.lookup(key, cpath)["hit"] is True
    dep.write_text("X = 2\n", encoding="utf-8")
    miss = rcl.lookup(key, cpath)
    assert miss["hit"] is False and rel in miss.get("drift", [])
    # 篡改条目 ⇒ 拒绝采信
    data = rcl.load(cpath)
    data["entries"][key]["summary"]["tests"] = 42
    rcl.save(data, cpath)
    assert rcl.lookup(key, cpath)["hit"] is False
    assert len(rcl.verify(cpath)["tampered"]) == 1


def test_cache_env_fingerprint_tracks_config() -> None:
    env = rcl.env_fingerprint()
    assert "python" in env and "pytest" in env
    assert env.get("file:pyproject.toml") not in (None, "absent")


def test_cache_selftest() -> None:
    assert rcl.selftest() == 0


# ── C 杠杆 3：按时长均衡分片 ────────────────────────────────────────────────
def test_shard_lpt_balances_and_is_deterministic() -> None:
    weights = {"a.py": 100.0, "b.py": 60.0, "c.py": 50.0, "d.py": 40.0, "e.py": 10.0}
    plan = shd.balance(weights, 3)
    assert sorted(plan["shard_of"]) == sorted(weights)
    assert abs(plan["total_s"] - sum(weights.values())) < 1e-6
    assert plan["imbalance"] <= shd.naive_imbalance(weights, 3)
    assert shd.balance(weights, 3) == plan


def test_shard_module_of_from_junit_classname() -> None:
    assert shd.module_of("tests.test_653_tools", "test_x") == "test_653_tools.py"
    assert shd.module_of("", "test_verdict_spec_v1_655.py::test_x") == \
        "test_verdict_spec_v1_655.py"


def test_shard_selftest() -> None:
    assert shd.selftest() == 0

