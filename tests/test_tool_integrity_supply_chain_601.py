"""601 任务 0.3 · 信任根数据文件入哈希面（`SUPPLY_CHAIN_FILES`）回归锁。

病（600 调研 · 585 攻击1 的真盲点）：哈希面只盖"5 个工具 + 2 个测试配置"，而"什么算通过"
还取决于**数据文件**（毒样例豁免台账、覆盖率台账、治理 manifest、Merkle 根、layout）——
改它们不动一行代码、checksum 全绿。本文件锁四件事：
  * 三节（core / test_config / supply_chain）能同写同校，且**互不串味**；
  * 篡改信任根数据 ⇒ `--check` exit 1 并点名文件（这是要抓的攻击面）；
  * 未钉 / 缺文件 ⇒ **只警告不报错**（部分检出与"任务1 尚未产出"都靠这条不误红）；
  * 旧格式基准（只有 core 行）仍可读（向后兼容）；护栏不许裸 `except Exception`。
"""
from __future__ import annotations

from pathlib import Path

import pytest
import tool_integrity as ti

COVERED = ("tools/poison_exemptions.yaml", "data/governance_docs_manifest.json")


def _mk_root(tmp: Path) -> Path:
    """假仓库根：两个受覆盖的数据文件 + 假核心工具。"""
    for rel in COVERED:
        f = tmp / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# {rel}\n", encoding="utf-8")
    tools = tmp / "tools"
    tools.mkdir(exist_ok=True)
    (tools / "a_tool.py").write_text("# a\n", encoding="utf-8")
    return tmp


def _write_all(tmp: Path, cs: Path, root: Path) -> None:
    ti.write_baseline(path=cs, tools_dir=root / "tools", names=("a_tool.py",))
    with cs.open("a", encoding="utf-8") as f:
        f.write("# test_config\n")
    ti.write_supply_chain_baseline(path=cs, root=root, names=COVERED)


# ── 声明与正例 ─────────────────────────────────────────────────────────────────
def test_supply_chain_files_declared():
    assert ti.SUPPLY_CHAIN_FILES, "SUPPLY_CHAIN_FILES 不得为空"
    joined = " ".join(ti.SUPPLY_CHAIN_FILES)
    for key in ("poison_exemptions.yaml", "governance_docs_manifest.json",
                "merkle_roots.json", "layout.json"):
        assert key in joined, f"信任根数据缺 {key}"
    assert not set(ti.SUPPLY_CHAIN_FILES) & set(ti.CORE_TOOLS), "与 CORE_TOOLS 不得混"


def test_update_then_verify_all_sections(tmp_path: Path):
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    _write_all(tmp_path, cs, root)
    assert ti.verify(cs, root / "tools") == ([], [], 0)
    assert ti.verify_supply_chain(cs, root, names=COVERED) == ([], [], 0)
    assert ti.load_supply_chain_baseline(cs) is not None


def test_tamper_supply_chain_detected(tmp_path: Path):
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    _write_all(tmp_path, cs, root)
    (root / COVERED[0]).write_text("# 被篡改：偷偷加一条假豁免\n", encoding="utf-8")
    changed, warnings, code = ti.verify_supply_chain(cs, root)
    assert code == 1 and [c[0] for c in changed] == [COVERED[0]], (changed, warnings)
    assert changed[0][1] != changed[0][2], "必须给出期望/实际两个 hash"


def test_missing_listed_file_skipped_with_warning(tmp_path: Path):
    """任务书：不存在的文件**跳过并警告，不报错**（任务1/2 的产出还没出现时靠这条不误红）。"""
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    names = (*COVERED, "data/supply_chain/merkle_roots.json")
    ti.write_baseline(path=cs, tools_dir=root / "tools", names=("a_tool.py",))
    ti.write_supply_chain_baseline(path=cs, root=root, names=names)
    changed, warnings, code = ti.verify_supply_chain(cs, root, names=names)
    assert code == 0 and changed == [], (changed, warnings)
    assert any("merkle_roots.json" in w for w in warnings), warnings


def test_unpinned_existing_file_warns_not_errors(tmp_path: Path):
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=root / "tools", names=("a_tool.py",))
    with cs.open("a", encoding="utf-8") as f:
        f.write("# supply_chain\n")            # 空节：文件存在但没钉
    changed, warnings, code = ti.verify_supply_chain(cs, root, names=COVERED)
    assert code == 0 and changed == []
    assert all("未钉" in w for w in warnings), warnings


def test_old_format_baseline_is_backward_compatible(tmp_path: Path):
    """旧格式（只有 core 行）仍可读：core 校验照常，supply_chain 只警告不报错。"""
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=root / "tools", names=("a_tool.py",))
    assert ti.load_supply_chain_baseline(cs) is None
    assert ti.verify(cs, root / "tools") == ([], [], 0), "core 节解析不得被新节影响"
    changed, warnings, code = ti.verify_supply_chain(cs, root, names=COVERED)
    assert code == 0 and changed == [] and len(warnings) == len(COVERED)


# ── CLI ────────────────────────────────────────────────────────────────────────
def test_cli_check_and_check_supply_chain_green_on_real_repo():
    assert ti.main(["--check"]) == 0
    assert ti.main(["--check-supply-chain"]) == 0


def test_cli_check_red_on_tampered_supply_chain(tmp_path: Path, monkeypatch, capsys):
    """`--check` 必须把 supply_chain 的篡改算进退出码（core 全绿也不能掩盖）。"""
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=ti.TOOLS, names=ti.CORE_TOOLS)
    ti.write_supply_chain_baseline(path=cs, root=root, names=COVERED)
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    monkeypatch.setattr(ti, "ROOT", root)
    assert ti.main(["--check"]) == 0
    (root / COVERED[1]).write_text("# 篡改 manifest\n", encoding="utf-8")
    assert ti.main(["--check"]) == 1
    out = capsys.readouterr().out
    assert "supply_chain" in out and COVERED[1] in out, out


def test_enforce_still_core_only(tmp_path: Path, monkeypatch):
    """入口闸门只校验 CORE（信任根数据由 --check/--check-supply-chain 管，避免循环依赖）。"""
    root = _mk_root(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=ti.TOOLS, names=ti.CORE_TOOLS)
    ti.write_supply_chain_baseline(path=cs, root=root, names=COVERED)
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    monkeypatch.setattr(ti, "ROOT", root)
    (root / COVERED[0]).write_text("# 篡改\n", encoding="utf-8")
    ti.enforce("gate_engine.py")            # 不抛（core 未变）


# ── 可证伪性 ───────────────────────────────────────────────────────────────────
def test_no_bare_except_exception_in_module():
    """护栏不许裸 `except Exception`：本模块内每处都必须带 `noqa` 标注（显式豁免才可接受）。"""
    src = (ti.TOOLS / "tool_integrity.py").read_text(encoding="utf-8")
    bad = [ln for ln in src.splitlines()
           if "except Exception" in ln and "noqa" not in ln]
    assert not bad, f"发现裸 except Exception：{bad}"


def test_supply_chain_verify_has_no_bare_except():
    """`verify_supply_chain` 自身不许吞异常（读不了就是读不了，不许静默判绿）。"""
    import inspect

    src = inspect.getsource(ti.verify_supply_chain)
    assert "except" not in src, "本函数不该有任何 except（要容错必须点名具体类型并显式登记）"
    with pytest.raises(TypeError):
        ti.verify_supply_chain(root=123)          # 传错类型要炸，不许静默
