"""472 P0-2（N2）回归锁：contains/contains_any 的判别力（结构判据，非频次）。

判据：命中的候选若**全是工件样板**（以 `.` 开头的汇编伪指令）→ 断言零信息 → 失败。
absent/absent_in 不做此判定（缺席恰是强断言）。
"""
from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import atom_evidence_replay as replay  # noqa: E402

ASM = """\
\t.text
\t.file\t"a.cpp"
main:
\tret
\t.section\t.note.GNU-stack
"""


def _assert(kind: str, **kw) -> tuple[bool, list[str]]:
    rule = {"kind": kind, **kw}
    return replay.check_artifact_assert({"artifact_assert": [rule]}, None) \
        if False else _call(rule)


def _call(rule: dict) -> tuple[bool, list[str]]:
    # 直接调用内部评估：构造最小 meta 并把工件文本注入（避免真编译）
    import tempfile
    d = Path(tempfile.mkdtemp())
    art = d / "a.asm"
    art.write_text(ASM, encoding="utf-8")
    return replay.check_artifact_assert({"artifact_assert": [rule]}, art)


def test_boilerplate_only_candidates_refused():
    """阳性：候选全是样板（.file/.text）→ 命中也判无判别力。"""
    ok, lines = _call({"kind": "contains_any", "texts": [".file", ".text"]})
    assert not ok, "\n".join(lines)
    assert any("判别力不足" in ln for ln in lines)


def test_never_hitting_candidate_does_not_excuse():
    """攻击者加"永不命中的非样板候选"不得规避：仍看**实际命中**的候选。"""
    ok, lines = _call({"kind": "contains_any", "texts": ["zzz_absent", ".file"]})
    assert not ok, "靠样板命中即应判无判别力"
    assert any("判别力不足" in ln for ln in lines)


def test_real_hit_candidate_passes():
    """阴性：命中候选含非样板（ret）→ 放行。"""
    ok, lines = _call({"kind": "contains_any", "texts": ["ret", ".file"]})
    assert ok, "\n".join(lines)


def test_contains_boilerplate_refused():
    """contains 单文本为样板 → 判无判别力。"""
    ok, lines = _call({"kind": "contains", "text": ".text"})
    assert not ok
    assert any("判别力不足" in ln for ln in lines)


def test_contains_real_symbol_passes():
    """阴性：contains 非样板（main）→ 放行。"""
    ok, _ = _call({"kind": "contains", "text": "main"})
    assert ok


def test_absent_not_affected():
    """absent/absent_in 不参与判别力判定（缺席是强断言）。"""
    ok, _ = _call({"kind": "absent", "text": ".text"})      # .text 存在 → absent 应失败
    assert not ok
    ok2, _ = _call({"kind": "absent", "text": "zzz_absent"})
    assert ok2


def test_boilerplate_helper():
    assert replay._is_boilerplate_text(".file")
    assert replay._is_boilerplate_text(".cfi_startproc")
    assert replay._is_boilerplate_text("")
    assert not replay._is_boilerplate_text("call malloc")
    assert not replay._is_boilerplate_text("ret")
