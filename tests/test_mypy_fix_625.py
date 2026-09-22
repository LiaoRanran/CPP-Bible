"""625 A1 · mypy 存量债修复回归测试（≥5 例）。

验证：mypy 配置覆盖 / mypy tools 清零 / 关键工具可导入 / 无批量 ignore / ruff 干净。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
PYPROJECT = os.path.join(ROOT, "pyproject.toml")
TOOLS = os.path.join(ROOT, "tools")


def test_pyproject_has_yaml_override():
    txt = open(PYPROJECT, encoding="utf-8").read()
    assert "[tool.mypy]" in txt
    assert "[[tool.mypy.overrides]]" in txt
    assert 'module = "yaml.*"' in txt
    assert "ignore_missing_imports = true" in txt


def test_mypy_tools_clean():
    p = subprocess.run([PY, "-m", "mypy", "tools/"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "Success" in (p.stdout + p.stderr)


def test_key_tools_importable():
    sys.path.insert(0, TOOLS)
    for mod in ("round3_mutator_623", "high_complexity_mutator_623", "pck_abstain_sync_621",
                "escape_root_cause_622", "adversarial_loop_620"):
        __import__(mod)


def test_no_bulk_type_ignore():
    # 无批量 ignore：任一工具文件 type: ignore 计数 ≤ 5，且全库总数 ≤ 20
    total = 0
    for fn in os.listdir(TOOLS):
        if not fn.endswith(".py"):
            continue
        src = open(os.path.join(TOOLS, fn), encoding="utf-8", errors="replace").read()
        n = len(re.findall(r"#\s*type:\s*ignore", src))
        assert n <= 5, f"{fn} type: ignore 过多（{n}）——疑似批量忽略"
        total += n
    assert total <= 20, f"全库 type: ignore 过多（{total}）"


def test_ruff_clean_after_fix():
    p = subprocess.run([PY, "-m", "ruff", "check", "tools/", "tests/"],
                       cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


def test_report_exists():
    p = os.path.join(ROOT, "data", "mypy_fix_625.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
