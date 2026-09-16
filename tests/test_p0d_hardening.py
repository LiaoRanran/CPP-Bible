"""470 P0-D 解析硬化回归锁：E07 走私 / E08 重复键 / 语法 invalid / 同义词归一。"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge


def _write(base: Path, sub: str, name: str, body: str) -> Path:
    d = base / sub
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(body, encoding="utf-8")
    return p


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "atoms").mkdir()
    (tmp_path / "evidence").mkdir()
    return tmp_path


def test_indent_smuggle_blocked(sb: Path):
    """E07：标量值后缩进 verdict → indent-smuggle block。"""
    _write(sb, "evidence/mem", "EV-S.md",
           "---\nid: EV-S\nstatus: draft\nfixture: f.cpp &x\n  verdict: confirm\n---\n")
    hits = [f for f in ge.check_frontmatter_hardening() if f.severity == "block"]
    assert any("indent-smuggle" in f.message for f in hits)


def test_nc_flow_rejected(sb: Path):
    """547 B5：[nc-flow] flow 式 negative_controls 必须被硬化层 block（与 replay 判决一致）。"""
    _write(sb, "evidence/mem", "EV-NCFLOW.md",
           "---\nid: EV-NCFLOW\nstatus: draft\n"
           "negative_controls: [{id: nc1, variant: v1, mutation: fence, "
           "fixture: a.cpp, anchor: f, remove: x, retain: [y], "
           "probe: {channel: artifact, symbol: s, op: becomes_absent, text: t}}]\n---\n")
    hits = [f for f in ge.check_frontmatter_hardening() if f.severity == "block"]
    assert any("nc-flow" in f.message for f in hits)


def test_nc_block_style_not_flagged(sb: Path):
    """阴性：block 式 negative_controls 不得触发 [nc-flow]（存量 nc 卡零误伤）。"""
    _write(sb, "evidence/mem", "EV-NCBLOCK.md",
           "---\nid: EV-NCBLOCK\nstatus: draft\n"
           "negative_controls:\n  - id: nc1\n    variant: v1\n    fixture: a.nc1.cpp\n---\n")
    hits = [f for f in ge.check_frontmatter_hardening()
            if f.severity == "block" and "nc-flow" in f.message]
    assert hits == [], f"block 式 nc 误伤：{hits}"


def test_flow_dup_key_blocked(sb: Path):
    """E08：flow-map 内重复键 → dup-key block（唯一键加载器）。"""
    _write(sb, "evidence/mem", "EV-D.md",
           "---\nid: EV-D\nactual: {run_match_file: x.out, run_match_file: y.out}\n---\n")
    hits = [f for f in ge.check_frontmatter_hardening() if f.severity == "block"]
    assert any("dup-key" in f.message for f in hits)


def test_yaml_invalid_warn(sb: Path):
    """语法非法（存量 3 张同因）→ warn 不 block（渐进发布）。"""
    _write(sb, "evidence/mem", "EV-I.md",
           "---\nid: EV-I\nhypothesis: `backtick start\n---\n")
    hits = [f for f in ge.check_frontmatter_hardening()]
    assert any(f.severity == "warn" and "invalid" in f.message for f in hits)


def test_legal_card_and_comment_scalar_pass(sb: Path):
    """阴性：合法块结构 +「键: # 注释」后跟缩进键 → 不得误伤。"""
    _write(sb, "evidence/mem", "EV-OK.md",
           "---\nid: EV-OK\nstatus: draft\nmatrix:   # 注释行\n"
           "  compiler: [GCC 15.3.0]\n  std: [c++17]\n---\n")
    hits = [f for f in ge.check_frontmatter_hardening()
            if "EV-OK" in f.target or f.target.endswith("EV-OK.md")]
    assert hits == [], f"合法卡误伤：{hits}"


def test_conflict_synonym_normalized(sb: Path):
    """E11：`contradiction` 同义词归一后参与冲突检测 → block。"""
    def atom(aid: str, rel: str) -> None:
        _write(sb, "atoms/mem", f"{aid}.md",
               f"---\nid: {aid}\ntitle: t\ndomain: MEM\ntype: mechanism\n"
               f"status: draft\nclaim: c\nclaim_boundary: b\nevidence: []\n"
               f"sources: '[{{kind: iso, ref: X, independent: true}}]'\n"
               f"first_hand: 'false'\nsuperiority: s\ndepth: d\npedagogy: p\n"
               f"relations:\n  - {rel}\n---\n")
    atom("ATOM-P", "prerequisite: ATOM-Q")
    atom("ATOM-Q", "contradiction: ATOM-P")     # 旧版静默丢弃
    hits = ge.check_atom_rel_conflict()
    assert hits and hits[0].severity == "block"


def test_indent_key_re_helpers():
    """检测器单元：注释/空值/block-scalar 起始不算标量值行。"""
    assert not ge._line_is_scalar_key("matrix:   # 注释")
    assert not ge._line_is_scalar_key("matrix:")
    assert not ge._line_is_scalar_key("hypothesis: >-")
    assert not ge._line_is_scalar_key("command: |")
    assert ge._line_is_scalar_key("fixture: f.cpp &x")
    assert ge._indent_smuggle_lines("fixture: f.cpp\n  verdict: confirm") != []
    assert ge._indent_smuggle_lines("matrix:\n  compiler: [GCC]") == []
