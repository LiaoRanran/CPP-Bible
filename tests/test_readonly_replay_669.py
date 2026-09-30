# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""669 P0-1 回归锁：`--check` 必须只读 —— 校验不得改写受控目录。

背景（668 §6 实测、且后台跑 pytest 时反复发生）：`atom_evidence_replay.py --check`
过去靠「**删仓库工件 → 在仓库里重生成 → 比 sha256 → 还原**」实现"工件必须与断言同代"，
一旦进程被中断（SIGTERM/kill）或并发抢占，还原就不完整 —— `Examples/atoms/*.asm` 出现
**3 删 6 改**；而 `Examples/` 在供应链 Merkle 覆盖内 ⇒ 信任根失效。更糟的是"删除"会被
**固化**：下一轮看到文件不存在 ⇒ `original=None` ⇒ 不再还原，文件永久缺失。

本批的治法（三处，逐条锁死）：
  1. 只读模式把**产出受控工件**的命令行 `-o` 目标改写到暂存目录（`_stage_artifact_writes`），
     sha / 结构断言 / 阴面全部用暂存产物判定 ⇒ **仓库零写**（不删，也就不需要还原）；
  2. 就地重生成只在显式写入模式发生（CLI `--write`；API `read_only=False`）；
  3. 中断（SIGINT/SIGTERM）时先还原在飞工件再放锁退出（`_emergency_restore`），
     杜绝"删了没来得及重生成"被固化成永久缺失。
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import atom_evidence_replay as rp  # noqa: E402


def _compiler() -> str:
    from toolchain import resolve_gpp
    return resolve_gpp()


def _has_compiler() -> bool:
    c = _compiler()
    return bool(c) and Path(c).is_file()


needs_gpp = pytest.mark.skipif(not _has_compiler(), reason="无可用 g++")


@pytest.fixture(autouse=True)
def _clear_inflight_after_test():
    """在飞登记表是模块级状态：每个用例前后都清干净，避免跨用例串味。"""
    rp._clear_inflight()
    yield
    rp._clear_inflight()


# ── 1. 纯函数：只有**受控工件**的 -o 目标被改写，其它写目标与注释行逐字不动 ──────
def test_stage_redirects_only_declared_artifacts(tmp_path: Path):
    lines = [
        'g++ -std=c++23 -O2 -S fx.cpp -o Examples/atoms/fx.asm',
        'g++ -std=c++23 -O2 fx.cpp -o build/fx.exe && ./build/fx.exe',
        '#   g++ -S fx.cpp -o Examples/atoms/fx.asm   （注释行不执行，也不动）',
    ]
    stage_dir = tmp_path / "STAGE"
    out, stage, warns = rp._stage_artifact_writes(
        lines, ["Examples/atoms/fx.asm"], stage_dir)
    assert set(stage) == {"Examples/atoms/fx.asm"}
    assert stage["Examples/atoms/fx.asm"].as_posix() in out[0]      # 受控目标已改写
    assert "Examples/atoms/fx.asm" not in out[0]
    assert "build/fx.exe" in out[1] and "STAGE" not in out[1]       # 非受控目标不动
    assert out[2] == lines[2]                                       # 注释行逐字不动
    assert warns == []


def test_stage_basename_fallback_and_unredirectable_warning(tmp_path: Path):
    """写法差异（`-o ./fx.asm`）按 basename 兜底；匹配不上的行必须**告警**而非静默。"""
    out, stage, warns = rp._stage_artifact_writes(
        ['g++ -S fx.cpp -o ./fx.asm'], ["Examples/atoms/fx.asm"], tmp_path / "st")
    assert stage["Examples/atoms/fx.asm"].as_posix() in out[0]
    assert warns == []

    out2, _stage2, warns2 = rp._stage_artifact_writes(
        ['bash gen_asm.sh Examples/atoms/fx.asm'], ["Examples/atoms/fx.asm"],
        tmp_path / "st2")
    assert out2 == ['bash gen_asm.sh Examples/atoms/fx.asm']       # 原样保留
    assert len(warns2) == 1 and "无法重定向" in warns2[0]


# ── 2. 中断自愈：在飞工件必须能被还原回运行前字节 ─────────────────────────────
def test_emergency_restore_puts_back_inflight_bytes(tmp_path: Path):
    art = tmp_path / "a.asm"
    art.write_text("ORIGINAL", encoding="utf-8")
    rp._register_inflight(art_path=art, original=art.read_bytes(), bak=None, extras=[])
    art.write_text("REGENERATED", encoding="utf-8")     # 中断发生在"已删/已重写"窗口
    rp._emergency_restore()
    assert art.read_text(encoding="utf-8") == "ORIGINAL"

    rp._clear_inflight()
    art.write_text("AFTER-CLEAR", encoding="utf-8")
    rp._emergency_restore()                            # 无在飞登记 ⇒ no-op
    assert art.read_text(encoding="utf-8") == "AFTER-CLEAR"


def test_terminate_handler_restores_before_exit(tmp_path: Path, monkeypatch):
    """`_on_terminate` 必须先还原在飞工件再退出（668 的"3 删"直接根因）。"""
    art = tmp_path / "b.asm"
    art.write_text("PRISTINE", encoding="utf-8")
    rp._register_inflight(art_path=art, original=art.read_bytes(), bak=None, extras=[])
    art.unlink()                                       # 已删、尚未重生成
    called: list[int] = []
    monkeypatch.setattr(rp, "_release_replay_lock", lambda: called.append(1))
    with pytest.raises(SystemExit):
        rp._on_terminate(15, None)
    assert art.read_text(encoding="utf-8") == "PRISTINE"
    assert called == [1]                               # 还原之后仍然放锁（不泄漏锁）


# ── 3. 端到端（沙箱根）：只读两跑零写；就地模式仍会刷新工件 ────────────────────
def _sandbox_card(tmp_path: Path) -> tuple[Path, Path, str]:
    """造一个自包含沙箱根 + 卡：工件先真编译（取 sha 当卡值），随后被伪造成"过期字节"。"""
    root = tmp_path / "sbx"
    (root / "build").mkdir(parents=True, exist_ok=True)
    (root / "fx.cpp").write_text(
        '#include <cstdio>\nint main(){ std::printf("A\\n"); }\n', encoding="utf-8")
    art_rel = "Examples/fx.asm"
    art = root / art_rel
    art.parent.mkdir(parents=True, exist_ok=True)
    gpp = _compiler()
    subprocess.run([gpp, "-std=c++17", "-O2", "-S", "fx.cpp", "-o", art_rel],
                   cwd=root, check=True, capture_output=True)
    sha = hashlib.sha256(art.read_bytes()).hexdigest()
    card = root / "EV-T-RL.md"
    # 运行行用**绝对路径**：Windows 的 CreateProcess 不按子进程 cwd 解析相对可执行路径
    # （真实卡靠"工具 cwd == 工具父进程 cwd"侥幸成立，测试里必须显式）。
    exe = (root / "build" / "fx.exe").as_posix()
    card.write_text(
        "---\n"
        "id: EV-T-RL\n"
        "command: |\n"
        f'  g++ -std=c++17 -O2 fx.cpp -o "{exe}" && "{exe}"\n'
        f"  g++ -std=c++17 -O2 -S fx.cpp -o {art_rel}\n"
        f"artifact: {art_rel}\n"
        f"artifact_sha256: {sha}\n"
        "fixture: fx.cpp\n"
        "actual:\n"
        '  run_case: "A"\n'
        "---\n",
        encoding="utf-8")
    return root, art, sha


@needs_gpp
def test_readonly_check_is_zero_write_and_write_mode_still_refreshes(tmp_path: Path):
    root, art, sha = _sandbox_card(tmp_path)
    card = root / "EV-T-RL.md"
    art.write_bytes(b"STALE-BYTES-FROM-AN-OLD-TOOLCHAIN\n")   # 伪造"过期工件"
    stale = art.read_bytes()

    with rp.batch_root(root):
        v1, log1 = rp.replay_card(card, do_sanitizer=False, read_only=True)
        v2, log2 = rp.replay_card(card, do_sanitizer=False, read_only=True)
        assert art.read_bytes() == stale, "只读模式改写了仓库工件"
        assert not list(root.rglob("*.bak")), "只读模式留下了 .bak 残留"
        # 就地模式（--write 的语义，逐字保持 472 P0-4 契约）：真的删旧→重生成→**还原**，
        # 所以盘上字节仍是 stale；与只读的差别是它"动过盘"（有中断风险窗口）。
        v3, log3 = rp.replay_card(card, do_sanitizer=False, read_only=False)
        assert art.read_bytes() == stale, "就地模式的还原契约（472 P0-4）被改坏"

    assert (v1, v2) == ("confirm", "confirm"), log1 + log2
    assert v3 == "confirm", log3
    assert not list(root.rglob("*.bak"))

    # 工件"原本不存在"（新卡首跑）：就地模式把重生成产物**留在仓库**（既有语义，未改）；
    # 只读模式不写盘 ⇒ 仍然不存在。这一条把两种模式的口径差异钉死。
    art.unlink()
    with rp.batch_root(root):
        v4, log4 = rp.replay_card(card, do_sanitizer=False, read_only=False)
        assert art.is_file(), "就地模式应把新卡首次生成的工件留在仓库（既有语义）"
        assert hashlib.sha256(art.read_bytes()).hexdigest() == sha, log4
        art.unlink()
        v5, log5 = rp.replay_card(card, do_sanitizer=False, read_only=True)
    assert (v4, v5) == ("confirm", "confirm"), log4 + log5
    assert not art.exists(), "只读模式凭空造出了工件（仓库零写被破坏）"


def _fingerprint_sources(root: Path) -> dict[str, str]:
    """受控目录指纹（**排除 gitignore 的 `build/`**——卡命令本来就往那里写编译产物）。"""
    return {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file() and "build" not in p.parts}


@needs_gpp
def test_cli_check_three_runs_leave_sandbox_untouched(tmp_path: Path, monkeypatch):
    """CLI 层：`--check`（默认只读）连跑 3 次，沙箱受控目录零变化（验收口径的缩小版）。"""
    root, art, sha = _sandbox_card(tmp_path)
    card = root / "EV-T-RL.md"
    art.write_bytes(b"STALE-BYTES\n")
    before = _fingerprint_sources(root)

    monkeypatch.setattr(rp.tool_integrity, "enforce", lambda *a, **k: None)
    with rp.batch_root(root):
        for _ in range(3):
            rc = rp.main(["--check", "--card", card.as_posix()])
            assert rc == 0, "只读 --check 出现非 confirm（判决被改坏）"
    after = _fingerprint_sources(root)
    assert before == after, f"受控目录被改写：{set(after) ^ set(before)}"
