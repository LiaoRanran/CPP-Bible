"""470 P0-C 判别力证明回归锁（452 E03）。

contains_in 的 text 若在所有函数区间（N≥2）出现 ⇒ 背景噪音、恒真断言 → 失败；
absent_in 不做频率统计（缺席即强断言）；部分区间出现 → 放行。
"""
from __future__ import annotations

from pathlib import Path

import pytest

import atom_evidence_replay as replay


ASM_UNIVERSAL = """\
\t.text
_Z10helper_av:
\tmov %eax, %ebx
\tret
_Z10helper_bv:
\tmov %ecx, %edx
\tret
"""

ASM_PARTIAL = """\
\t.text
_Z10spinv:
\tlock xchg %eax, %ebx
\tret
_Z10helperv:
\tmov %ecx, %edx
\tret
"""


def _write_partial(tmp_path: Path) -> Path:
    p = tmp_path / "fx.asm"
    p.write_text(ASM_PARTIAL, encoding="utf-8")
    return p


def test_function_ranges_enumeration():
    ranges = replay._function_ranges(ASM_UNIVERSAL)
    assert [n for n, _ in ranges] == ["_Z10helper_av", "_Z10helper_bv"]
    assert replay._discriminative_span(ASM_UNIVERSAL, "mov") == (2, 2)
    assert replay._discriminative_span(ASM_PARTIAL, "lock") == (1, 2)


def test_universal_contains_in_refuted(tmp_path: Path):
    """正例（E03）：text 在所有函数区间出现 → 判别力不足 → 断言失败。"""
    (tmp_path / "fx.asm").write_text(ASM_UNIVERSAL, encoding="utf-8")
    meta = {"artifact_assert": [
        {"kind": "contains_in", "symbol": "_Z10helper_av", "text": "mov"}]}
    ok, lines = replay.check_artifact_assert(meta, tmp_path / "fx.asm")
    assert not ok, "\n".join(lines)
    assert any("判别力不足" in ln for ln in lines)


def test_partial_contains_in_passes(tmp_path: Path):
    """反例：text 只在部分区间出现 → 有判别力 → 放行。"""
    art = _write_partial(tmp_path)
    meta = {"artifact_assert": [
        {"kind": "contains_in", "symbol": "_Z10spinv", "text": "lock"}]}
    ok, lines = replay.check_artifact_assert(meta, art)
    assert ok, "\n".join(lines)


def test_absent_in_not_scored(tmp_path: Path):
    """absent_in 不做频率统计：缺席恰是强断言（证该函数没有某行为）。"""
    art = _write_partial(tmp_path)
    meta = {"artifact_assert": [
        {"kind": "absent_in", "symbol": "_Z10helperv", "text": "lock"}]}
    ok, _lines = replay.check_artifact_assert(meta, art)
    assert ok, "absent_in 不得因频率统计被误判"


def test_single_function_artifact_not_scored(tmp_path: Path):
    """N<2（工具工件太小）不判——避免小夹具误伤。"""
    (tmp_path / "one.asm").write_text(
        "\t.text\n_Z3foov:\n\tmov %eax, %ebx\n\tret\n", encoding="utf-8")
    meta = {"artifact_assert": [
        {"kind": "contains_in", "symbol": "_Z3foov", "text": "mov"}]}
    ok, _lines = replay.check_artifact_assert(meta, tmp_path / "one.asm")
    assert ok
