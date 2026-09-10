"""锁定证据卡复算契约（G3 首项）与三类 refute —— 把"毒样例"固化为回归。

覆盖：
  1. 解析器能读真实卡的全部形态（block scalar / 嵌套映射 / flow 序列 / 尾注释 / 折叠续行）
  2. `refute:missing_field`（缺 artifact / artifact_sha256 / actual.run_*）
  3. `refute:sha256_mismatch` —— 首版验收标准：旧工件 hash 喂进去必须被拦
  4. `refute:run_mismatch` —— 输出与 `run_*` 不逐字一致
  5. `confirm` —— 一致时放行（阴性对照：门禁不能恒红）
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest

import atom_evidence_replay as rp

REAL_CARD = rp.ROOT / "evidence/mem/EV-MEM-001.md"


def _compiler() -> str:
    """解析本机 g++（与工具同源：prefer 列表 → PATH → 兜底）。"""
    from toolchain import resolve_gpp
    return resolve_gpp()


def _has_compiler() -> bool:
    gpp = _compiler()
    return bool(shutil.which(gpp) or Path(gpp).exists())


needs_gpp = pytest.mark.skipif(not _has_compiler(), reason="本机无 g++")


# ── 1. 解析器契约 ──────────────────────────────────────────────────────────
def test_parse_frontmatter_real_card_shapes():
    """真实卡（EV-MEM-001）的字段全部可解析，形态覆盖卡模板的所有用法。"""
    meta = rp.parse_frontmatter(REAL_CARD.read_text(encoding="utf-8"))
    assert meta["id"] == "EV-MEM-001"
    assert meta["matrix"]["std"] == ["c++23", "c++17"]          # flow 序列 + 尾注释剥离
    assert str(meta["command"]).startswith("g++ -std=c++23")     # block scalar（|）保换行
    assert str(meta["artifact_sha256"]).startswith("d8b6b18d")
    run_keys = [k for k in meta["actual"] if k.startswith("run")]
    assert len(run_keys) == 6, "6 组矩阵实测"
    assert str(meta["hypothesis"]).startswith("对含堆缓冲的类型")  # 折叠 scalar（>-）


def test_parse_frontmatter_rejects_non_card():
    with pytest.raises(ValueError):
        rp.parse_frontmatter("no frontmatter here\n")


# ── 2. 缺字段 ─────────────────────────────────────────────────────────────
def test_missing_field_refutes(tmp_path: Path):
    card = tmp_path / "EV-T-001.md"
    card.write_text("---\nid: EV-T-001\ncommand: echo hi\n---\n", encoding="utf-8")
    verdict, log = rp.replay_card(card)
    assert verdict == "refute:missing_field"
    assert any("artifact" in ln and "artifact_sha256" in ln for ln in log)


# ── 3~5. 真编译三类结局 ────────────────────────────────────────────────────
def _make_card(tmp_path: Path, *, expect: str, sha: str) -> Path:
    """造一张自包含卡：fixture 打印 A/B 两行，artifact 为 -S 产物。"""
    gpp = _compiler()
    fx = tmp_path / "fx.cpp"
    fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\nB\\n"); }\n',
                  encoding="utf-8")
    exe = tmp_path / "fx.exe"
    asm = tmp_path / "fx.asm"

    def q(p: object) -> str:
        """卡内路径一律正斜杠（M2 command 契约）。"""
        return '"' + str(p).replace("\\", "/") + '"'
    command = (f'{q(gpp)} -std=c++17 -O2 {q(fx)} -o {q(exe)} && {q(exe)}\n'
               f'{q(gpp)} -std=c++17 -O2 -S {q(fx)} -o {q(asm)}')
    card = tmp_path / "EV-T-002.md"
    card.write_text(
        "---\n"
        "id: EV-T-002\n"
        "command: |\n"
        + "".join(f"  {ln}\n" for ln in command.split("\n")) +
        f"artifact: {asm.as_posix()}\n"
        f"artifact_sha256: {sha}\n"
        "fixture: " + fx.as_posix() + "\n"
        "actual:\n"
        f'  run_case: "{expect.replace(chr(10), " | ")}"\n'
        "---\n",
        encoding="utf-8")
    return card


@needs_gpp
def test_sha256_mismatch_refutes(tmp_path: Path):
    """毒样例：工件 hash 与卡不符（本次 G2 缺陷的机器化回归）。"""
    card = _make_card(tmp_path, expect="A\nB", sha="0" * 64)
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:sha256_mismatch", log
    assert any("工件与卡不同代" in ln for ln in log)


@needs_gpp
def test_run_mismatch_refutes(tmp_path: Path):
    """毒样例：运行输出与 run_* 不逐字一致（精确比对，非包含）。"""
    card = _make_card(tmp_path, expect="A\nWRONG", sha="0" * 64)
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:run_mismatch", log
    assert any("实际 2 行" in ln for ln in log)


@needs_gpp
def test_confirm_when_artifact_and_output_match(tmp_path: Path):
    """阴性对照：一致的卡必须放行（门禁不得恒红）。"""
    gpp = _compiler()
    fx = tmp_path / "fx.cpp"
    fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\nB\\n"); }\n',
                  encoding="utf-8")
    asm = tmp_path / "fx.asm"
    subprocess.run([gpp, "-std=c++17", "-O2", "-S", fx.as_posix(), "-o", asm.as_posix()],
                   check=True, capture_output=True)
    real = hashlib.sha256(asm.read_bytes()).hexdigest()
    card = _make_card(tmp_path, expect="A\nB", sha=real)
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "confirm", log


# ── 6. 不支持的 shell 特性必须诚实报错（不猜） ─────────────────────────────
def test_unsupported_shell_feature_is_reported():
    assert rp._split_argv("g++ a.cpp | tee log") is None
    assert rp._split_argv("g++ a.cpp > out.txt") is None
    assert rp._split_argv('g++ a.cpp -o b.exe && b.exe') is not None
