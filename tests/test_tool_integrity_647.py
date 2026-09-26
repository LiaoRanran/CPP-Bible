"""647 A1 · tool_integrity supply_chain **严格模式**回归锁（fail-open 修复 1）。

病（642 B3 审计 FO-A，实测）：缺信任根文件只 warning、exit 0 ⇒ 删掉一个信任根文件，verifier 仍绿。
647 A1 修法：`verify_supply_chain(..., strict=True)`（**CLI `--check` 默认**）把
「**基准已钉但磁盘上没有**」判红；`--warn-only` 退回 601 宽容口径。

本文件锁五件事（编号 A1-1..A1-8）：
  * 缺件（已钉）在 strict 下必 FAIL，在 lenient 下不 FAIL；
  * 文件齐全 ⇒ strict PASS；
  * CLI `--check` **默认 strict**，`--warn-only` 是唯一后门；
  * 不误红「尚未生成的产物」（基准里没有 + 磁盘上没有）；
  * 不影响 core 判定（core 节与 supply_chain 节互不串味）。
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import tool_integrity as ti

ALL = ti.SUPPLY_CHAIN_FILES


def _mk_root(tmp: Path) -> Path:
    """假仓库根：5 个信任根文件全在（可被删/改）+ 一个假核心工具。"""
    for rel in ALL:
        f = tmp / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# {rel}\n", encoding="utf-8")
    tools = tmp / "tools"
    tools.mkdir(exist_ok=True)
    (tools / "a_tool.py").write_text("# a\n", encoding="utf-8")
    return tmp


def _pin(tmp: Path, names=ALL, core: str = "fake") -> Path:
    """把 core + supply_chain 两节钉进 tmp 基准，返回基准路径。

    `core="fake"`：core 节用假工具（测 supply_chain 时不受 core 干扰）；
    `core="real"`：core 节用**真实** CORE_TOOLS（测 CLI 全程时必须 —— `verify()` 读的是真 `TOOLS`）。
    """
    cs = tmp / ".tool_checksums"
    if core == "real":
        ti.write_baseline(path=cs, tools_dir=ti.TOOLS, names=ti.CORE_TOOLS)
    else:
        ti.write_baseline(path=cs, tools_dir=tmp / "tools", names=("a_tool.py",))
    ti.write_supply_chain_baseline(path=cs, root=tmp, names=names)
    return cs


# ── A1-1：齐全 ⇒ 两档都 PASS ────────────────────────────────────────────────────
def test_a1_1_all_files_present_passes_both_modes(tmp_path: Path):
    root = _mk_root(tmp_path)
    cs = _pin(root)
    assert ti.verify_supply_chain(cs, root, strict=True) == ([], [], 0)
    assert ti.verify_supply_chain(cs, root, strict=False) == ([], [], 0)


# ── A1-2：删一个**已钉**信任根文件 ⇒ strict 必 FAIL（lenient 不红）──────────────
def test_a1_2_missing_pinned_file_fails_in_strict(tmp_path: Path):
    root = _mk_root(tmp_path)
    cs = _pin(root)
    (root / ALL[0]).unlink()

    ch, wn, code = ti.verify_supply_chain(cs, root, strict=True)
    assert code == 1 and ch == [], (ch, wn)
    assert any(ALL[0] in w and "strict" in w for w in wn), wn

    # 601 历史口径（lenient）**不变** ⇒ 642 B3 的 FO-A 复现路径仍成立
    ch2, wn2, code2 = ti.verify_supply_chain(cs, root, strict=False)
    assert code2 == 0 and ch2 == []
    assert any(ALL[0] in w for w in wn2), wn2


# ── A1-3：5 个信任根文件逐个删，strict 全都能抓到 ───────────────────────────────
def test_a1_3_every_supply_chain_file_is_guarded(tmp_path: Path):
    for rel in ALL:
        root = _mk_root(tmp_path / rel.replace("/", "_"))
        cs = _pin(root)
        (root / rel).unlink()
        _, wn, code = ti.verify_supply_chain(cs, root, strict=True)
        assert code == 1 and any(rel in w for w in wn), (rel, wn)


# ── A1-4：篡改内容 ⇒ 两档都 FAIL（这条 601 已有，此处防回归）──────────────────
def test_a1_4_tampered_content_fails_even_lenient(tmp_path: Path):
    root = _mk_root(tmp_path)
    cs = _pin(root)
    (root / ALL[1]).write_text("# 篡改\n", encoding="utf-8")
    for strict in (True, False):
        ch, _, code = ti.verify_supply_chain(cs, root, strict=strict)
        assert code == 1 and [c[0] for c in ch] == [ALL[1]], (strict, ch)


# ── A1-5：不误红「尚未生成的产物」（基准没有 + 磁盘也没有）──────────────────────
def test_a1_5_unpinned_and_absent_is_not_red(tmp_path: Path):
    root = _mk_root(tmp_path)
    partial = (ALL[0],)
    cs = _pin(root, names=partial)          # 只钉 1 个
    for rel in ALL[1:]:
        (root / rel).unlink()               # 其余 4 个"还没产出"
    _, wn, code = ti.verify_supply_chain(cs, root, strict=True)
    assert code == 0, wn                    # 未钉且不存在 ⇒ 只警告（601 设计理由仍成立）


# ── A1-6：CLI `--check` 默认 strict；`--warn-only` 是唯一后门 ────────────────────
def test_a1_6_cli_default_is_strict_and_warn_only_is_the_backdoor(tmp_path: Path, monkeypatch):
    root = _mk_root(tmp_path)
    cs = _pin(root, core="real")           # core 用真工具 ⇒ CLI 全程只被 supply_chain 影响
    monkeypatch.setattr(ti, "ROOT", root)
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    # Merkle 台账在真实仓库里（不受 ROOT monkeypatch 控制），xdist 并行时会被别的测试改写 ⇒
    # 本用例只测 supply_chain 口径，把 Merkle 校验打桩（避免测出"别的测试正在写盘"这种假失败）
    monkeypatch.setattr(ti, "verify_merkle", lambda *a, **k: ([], [], 0))
    (root / ALL[2]).unlink()
    assert ti.main(["--check"]) == 1, "缺信任根文件 ⇒ 默认必须红（fail-closed）"
    assert ti.main(["--check-supply-chain"]) == 1
    assert ti.main(["--check", "--warn-only"]) == 0, "--warn-only 是显式后门（迁移/副本用）"
    assert ti.main(["--check", "--strict-supply-chain"]) == 1


# ── A1-7：不影响 core 判定（core 节 / supply_chain 节互不串味）──────────────────
def test_a1_7_core_verdict_unaffected(tmp_path: Path, monkeypatch):
    root = _mk_root(tmp_path)
    cs = _pin(root, core="real")
    monkeypatch.setattr(ti, "ROOT", root)
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    (root / ALL[3]).unlink()                     # 只动 supply_chain
    changed, missing, code = ti.verify()         # core 节（读真 TOOLS）
    assert (changed, missing, code) == ([], [], 0), (changed, missing)
    # `enforce()` 只校验 core ⇒ 信任根数据缺失不该让判定入口拒绝运行（避免循环依赖）
    ti.enforce("gate_engine.py")


# ── A1-8：常量与真实仓库口径自述 ────────────────────────────────────────────────
def test_a1_8_strict_default_declared_and_real_repo_green():
    assert ti.SUPPLY_CHAIN_STRICT_DEFAULT is True
    assert ti.verify_supply_chain(strict=True)[2] == 0, "真实仓库信任根必须齐备"
    assert ti.verify()[2] == 0, "真实仓库 core 节必须一致"
    # 只用 supply_chain 相关的 CLI（`--check` 还会跑 Merkle/ruler，xdist 并行下会被别的测试干扰）
    assert ti.main(["--check-supply-chain"]) == 0
    # 信任根基准里确实钉了这 5 个文件（不是空节）
    base = ti.load_supply_chain_baseline() or {}
    assert set(ALL) <= set(base), sorted(base)
    assert len(base[ALL[0]]) == len(hashlib.sha256(b"").hexdigest())
