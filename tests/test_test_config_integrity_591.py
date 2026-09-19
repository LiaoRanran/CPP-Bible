"""591 任务 3 · 测试器配置入哈希面回归锁（A2 防御）。

conftest.py / pyproject.toml 进 `.tool_checksums` 的 `# test_config` 节；
`--check-test-config` 独立校验；core 节解析必须**不受** test_config 节影响。
"""
from __future__ import annotations

from pathlib import Path

import tool_integrity as ti


def test_test_config_tools_list():
    assert ti.TEST_CONFIG_TOOLS, "TEST_CONFIG_TOOLS 不得为空"
    assert "tests/conftest.py" in ti.TEST_CONFIG_TOOLS
    assert "pyproject.toml" in ti.TEST_CONFIG_TOOLS


def test_verify_test_config_clean():
    changed, missing, code = ti.verify_test_config()
    assert code == 0 and not changed and not missing, (changed, missing, code)


def test_verify_test_config_detects_tamper(tmp_path: Path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "conftest.py").write_text("original\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("orig\n", encoding="utf-8")
    ck = tmp_path / "checks.txt"
    ti.write_test_config_baseline(path=ck, root=tmp_path)
    assert ti.verify_test_config(ck, tmp_path)[2] == 0
    (tmp_path / "tests" / "conftest.py").write_text("tampered\n", encoding="utf-8")
    changed, _missing, code = ti.verify_test_config(ck, tmp_path)
    assert code == 1 and any("conftest.py" in c[0] for c in changed), (changed, code)


def test_check_test_config_cli_clean():
    assert ti.main(["--check-test-config"]) == 0


def test_core_section_ignores_test_config_section():
    """core 节解析必须在 `# test_config` 标记处停止（否则 `tests/conftest.py` 会被当成 tools/ 缺失）。"""
    base = ti.load_baseline()
    assert base is not None
    assert not any("/" in n for n in base), f"core 基准混入了路径式条目：{list(base)}"
    tc = ti.load_test_config_baseline()
    assert tc is not None and "tests/conftest.py" in tc
