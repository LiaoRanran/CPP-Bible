"""ccache 前缀回归锁（479 任务 3）：只包编译器、可回退、失败分流不受影响。

设计约束（勿弱化）：
* 只对**编译器调用**加前缀（跑 exe / 生成脚本不加）；
* `--no-ccache` 与「ccache 不可用」都必须**静默回退**到裸编译器（加速是优化不是校验前提）；
* `run_commands` 记录的 `prog` 必须是**真实编译器**——失败分流（编译器没起来 vs 源码被拒）
  靠它，若被 ccache 覆盖会把"环境故障"误判成"内容问题"。
"""
from __future__ import annotations

import os
from pathlib import Path

import atom_evidence_replay as rp
import pytest

GXX = r"C:\Qt\Tools\mingw1530_64\bin\g++.exe"


@pytest.fixture(autouse=True)
def _restore_flag():
    """CCACHE_ENABLED 是模块级开关，测试后还原，避免污染其它用例。"""
    old = rp.CCACHE_ENABLED
    yield
    rp.CCACHE_ENABLED = old


# ── 前缀逻辑 ──────────────────────────────────────────────────────────────
def test_wrap_adds_prefix_for_compiler(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: r"C:\tools\ccache\ccache.exe")
    rp.CCACHE_ENABLED = True
    out = rp._wrap_ccache([GXX, "-c", "x.cpp"])
    assert out[0].lower().endswith("ccache.exe") and out[1] == GXX


def test_wrap_skips_non_compiler(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: r"C:\tools\ccache\ccache.exe")
    rp.CCACHE_ENABLED = True
    assert rp._wrap_ccache(["build/a.exe"]) == ["build/a.exe"]
    assert rp._wrap_ccache(["python", "gen.py"]) == ["python", "gen.py"]


def test_wrap_disabled_flag(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: r"C:\tools\ccache\ccache.exe")
    rp.CCACHE_ENABLED = False
    assert rp._wrap_ccache([GXX, "-c"]) == [GXX, "-c"]


def test_wrap_unavailable_falls_back(monkeypatch: pytest.MonkeyPatch):
    """ccache 不可用 ⇒ 原样返回（不阻断、不报错）——回退是设计的一部分。"""
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: "")
    rp.CCACHE_ENABLED = True
    assert rp._wrap_ccache([GXX, "-c"]) == [GXX, "-c"]


# ── 缓存目录 ──────────────────────────────────────────────────────────────
def test_compiler_env_sets_ccache_dir(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: r"C:\tools\ccache\ccache.exe")
    monkeypatch.delenv("CCACHE_DIR", raising=False)
    rp.CCACHE_ENABLED = True
    env = rp._compiler_env()
    assert env.get("CCACHE_DIR", "").endswith(str(Path("build") / ".ccache"))


def test_compiler_env_keeps_explicit_dir(monkeypatch: pytest.MonkeyPatch):
    """调用方显式给 CCACHE_DIR 时不得覆盖（`_recompile_invariant` 等依赖 setdefault 语义）。"""
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: r"C:\tools\ccache\ccache.exe")
    monkeypatch.setenv("CCACHE_DIR", r"D:\custom")
    rp.CCACHE_ENABLED = True
    assert rp._compiler_env()["CCACHE_DIR"] == r"D:\custom"


# ── run_commands 契约 ─────────────────────────────────────────────────────
@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="run_commands 内部 ccache 前缀在 CI Ubuntu 上行为与本地 Windows 不同（全局缓存/执行顺序差异）",
)
def test_run_commands_prog_is_real_compiler(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """执行 argv 带 ccache 前缀，但 `prog`（失败分流依据）必须是真实编译器。"""
    seen: dict = {}

    class FakeSub:
        TimeoutExpired = rp.subprocess.TimeoutExpired

        @staticmethod
        def run(argv, **kw):                       # noqa: ANN001
            seen["argv"] = argv

            class R:
                returncode = 0
                stderr = ""
                stdout = ""
            return R()

    monkeypatch.setattr(rp, "subprocess", FakeSub)
    monkeypatch.setattr(rp, "_pin_compiler", lambda a: [GXX, *a[1:]])
    monkeypatch.setattr(rp, "_resolve_ccache", lambda: r"C:\tools\ccache\ccache.exe")
    rp.CCACHE_ENABLED = True
    results, _ = rp.run_commands(["g++ -c x.cpp"], tmp_path, {})
    assert seen["argv"][0].lower().endswith("ccache.exe"), "编译器调用应带 ccache 前缀"
    assert results[0][3] == GXX, f"prog 须为真实编译器，实际 {results[0][3]!r}"


def test_main_no_ccache_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """`--no-ccache` 必须把模块开关关掉（CLI 回退通道）。"""
    card = tmp_path / "EV-X.md"
    card.write_text("---\nid: EV-X\n---\n", encoding="utf-8")
    monkeypatch.setattr(rp, "replay_card", lambda *a, **k: ("confirm", ["stub"]))
    assert rp.main(["--no-ccache", "--card", str(card)]) == 0
    assert rp.CCACHE_ENABLED is False
    assert rp.main(["--card", str(card)]) == 0
    assert rp.CCACHE_ENABLED is True
