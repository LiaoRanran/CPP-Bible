"""tool_integrity 回归锁（498 任务 3）。

四态：全匹配 exit 0 / 被改 exit 1 / 缺基准 exit 2 / 工具缺失 exit 1。
全部走 tmp_path（不触碰真实 tools/ 与 .tool_checksums）。
"""
from __future__ import annotations

from pathlib import Path

import tool_integrity as ti

NAMES = ("a_tool.py", "b_tool.py")


def _mk(tmp: Path, *, content: dict[str, str] | None = None) -> Path:
    tools = tmp / "tools"
    tools.mkdir(exist_ok=True)
    for n in NAMES:
        (tools / n).write_text((content or {}).get(n, f"# {n}\n"), encoding="utf-8")
    return tools


def test_update_then_verify_ok(tmp_path: Path):
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    assert cs.is_file()
    changed, missing, code = ti.verify(path=cs, tools_dir=tools)
    assert (changed, missing, code) == ([], [], 0)


def test_tamper_detected(tmp_path: Path):
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    (tools / "a_tool.py").write_text("# 被篡改\n", encoding="utf-8")
    changed, missing, code = ti.verify(path=cs, tools_dir=tools)
    assert code == 1 and len(changed) == 1
    name, want, got = changed[0]
    assert name == "a_tool.py" and want != got


def test_missing_baseline_exit2(tmp_path: Path):
    tools = _mk(tmp_path)
    _, _, code = ti.verify(path=tmp_path / "nope.txt", tools_dir=tools)
    assert code == 2, "缺基准必须 exit 2（不得静默放行）"


def test_missing_tool_detected(tmp_path: Path):
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    (tools / "b_tool.py").unlink()
    changed, missing, code = ti.verify(path=cs, tools_dir=tools)
    assert code == 1 and missing == ["b_tool.py"]


def test_baseline_format_and_self_exclusion(tmp_path: Path):
    """基准格式 `<sha256>  <name>`；且 .tool_checksums 自己不在清单里（递归无解）。"""
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    lines = cs.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(NAMES)
    for ln in lines:
        h, _, n = ln.partition("  ")
        assert len(h) == 64 and n in NAMES
        assert n != ".tool_checksums"
