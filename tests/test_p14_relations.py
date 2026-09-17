"""472 P1-4（N3）回归锁：refutes/denies 归一 + 未知关系类型 warn。"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge
import pytest


def _atom(base: Path, aid: str, rel: str) -> None:
    d = base / "atoms" / "mem"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{aid}.md").write_text(
        f"---\nid: {aid}\ntitle: t\ndomain: MEM\ntype: mechanism\nstatus: draft\n"
        "claim: c\nclaim_boundary: b\nevidence: []\n"
        "sources: '[{kind: iso, ref: X, independent: true}]'\nfirst_hand: 'false'\n"
        f"superiority: s\ndepth: d\npedagogy: p\nrelations:\n  - {rel}\n---\n",
        encoding="utf-8")


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    (tmp_path / "atoms").mkdir()
    return tmp_path


@pytest.mark.parametrize("syn", ["refutes", "denies", "cancels", "opposes",
                                 "contradiction", "conflicts"])
def test_conflict_synonyms_normalized(sb: Path, syn: str):
    """N3：同义词归一后参与冲突检测（矛盾原子不得静默共存）。"""
    _atom(sb, "ATOM-P", "prerequisite: ATOM-Q")
    _atom(sb, "ATOM-Q", f"{syn}: ATOM-P")
    hits = ge.check_atom_rel_conflict()
    assert hits, f"{syn} 未归一 → 矛盾静默共存（逃逸）"


def test_unknown_relation_type_warned(sb: Path):
    """表外类型必须可见（不再静默丢弃）。"""
    _atom(sb, "ATOM-U1", "prerequisite: ATOM-U2")
    _atom(sb, "ATOM-U2", "some_future_relation: ATOM-U1")
    hits = ge.check_relations_unknown_type()
    assert hits and "some_future_relation" in hits[0].message


def test_known_relation_types_not_warned(sb: Path):
    """阴性：白名单内类型（含实务补入的 evolved_to/misconceived_as）不 warn。"""
    _atom(sb, "ATOM-K1", "evolved_to: ATOM-K2")
    _atom(sb, "ATOM-K2", "misconceived_as: ATOM-K3")
    _atom(sb, "ATOM-K3", "contrasts: ATOM-K1")
    assert ge.check_relations_unknown_type() == []
