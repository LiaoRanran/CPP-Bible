#!/usr/bin/env python3
"""615 B3 回归测试：判决尺子纳入 tool_integrity 保护（ruler 节）。"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import tool_integrity as ti  # noqa: E402


def test_ruler_tools_nonempty_and_key_entries() -> None:
    assert len(ti.RULER_TOOLS) >= 5
    for f in ("mutation_fuzz.py", "tool_integrity.py", "golden_lock.py", "replay_invariants.py"):
        assert f in ti.RULER_TOOLS, f"{f} 应纳入判决尺子"
    # 与 CORE_TOOLS 不重叠（避免双节重复钉）
    assert not (set(ti.RULER_TOOLS) & set(ti.CORE_TOOLS))


def test_ruler_section_written_with_entries() -> None:
    base = ti.load_ruler_baseline()
    assert base is not None, "缺 # ruler 节（须先跑 --update）"
    assert len(base) >= 10
    # 每条对应的文件都在磁盘上
    for name in base:
        assert (ROOT / "tools" / name).is_file(), f"{name} 不存在"


def test_verify_ruler_logic_detects_change_and_missing(tmp_path: Path) -> None:
    """用**临时**基准验证逻辑（不碰真仓、不跑监工 --check CLI）。"""
    td = tmp_path / "tools"
    td.mkdir()
    (td / "a.py").write_text("x", encoding="utf-8")
    base = tmp_path / ".tool_checksums"
    h = hashlib.sha256(b"x").hexdigest()
    base.write_text(f"# ruler\n{h}  a.py\n{'0' * 64}  gone.py\n", encoding="utf-8")
    # 缺文件检测
    _changed, missing, code = ti.verify_ruler(path=base, tools_dir=td)
    assert "gone.py" in missing
    assert code == 1
    # 内容变更检测
    (td / "a.py").write_text("y", encoding="utf-8")
    changed2, _missing2, code2 = ti.verify_ruler(path=base, tools_dir=td)
    assert any(n == "a.py" for n, _, _ in changed2)
    assert code2 == 1
