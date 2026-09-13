"""425 上游依赖遍历回归锁：依赖（prerequisite/specializes/realizes）与引用
（contrasts/see_also 等）必须区分；对存量原子全部可运行（零风险只读）。
"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge
import impact_analysis as ia


def _atom(base: Path, aid: str, relations: str) -> None:
    d = base / "atoms" / "mem"
    d.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": aid, "title": "t", "domain": "MEM", "type": "mechanism",
        "status": "draft", "claim": "c", "claim_boundary": "b",
        "relations": relations, "evidence": "[]",
        "sources": "[{kind: iso, ref: X, independent: true}]",
        "first_hand": "false", "superiority": "s", "depth": "d", "pedagogy": "p",
    }
    body = "".join(f"{k}: {v}\n" for k, v in fields.items())
    (d / f"{aid}.md").write_text("---\n" + body + "---\n", encoding="utf-8")


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    (tmp_path / "atoms").mkdir()
    return tmp_path


def test_upstream_finds_dependents(sb: Path):
    """A prerequisite B（mapping-form，417 归一后）→ upstream(B) 含 A。"""
    _atom(sb, "ATOM-A", "\n  - prerequisite: ATOM-B")
    _atom(sb, "ATOM-B", "[]")
    deps = ia.upstream("ATOM-B")
    assert [(d["atom"], d["rel_type"]) for d in deps] == [("ATOM-A", "prerequisite")]


def test_upstream_excludes_contrasts(sb: Path):
    """contrasts 是引用不是依赖：upstream(B) 不含 A，references(B) 含 A。"""
    _atom(sb, "ATOM-A", "\n  - contrasts: ATOM-B")
    _atom(sb, "ATOM-B", "[]")
    assert ia.upstream("ATOM-B") == [], "contrasts 不得计入依赖"
    assert [r["atom"] for r in ia.references("ATOM-B")] == ["ATOM-A"]


def test_upstream_empty_for_isolated_atom(sb: Path):
    _atom(sb, "ATOM-SOLO", "[]")
    assert ia.upstream("ATOM-SOLO") == [] and ia.references("ATOM-SOLO") == []


def test_downstream(sb: Path):
    _atom(sb, "ATOM-A", "\n  - specializes: ATOM-B")
    _atom(sb, "ATOM-B", "[]")
    deps = ia.downstream("ATOM-A")
    assert [(d["atom"], d["rel_type"]) for d in deps] == [("ATOM-B", "specializes")]


def test_real_atoms_all_run():
    """对存量全部原子跑 upstream/downstream——只读查询不得抛错。"""
    ids = [str(ge._meta(p).get("id") or p.stem) for p in ge._cards(ge.ATOMS, "ATOM-*.md")]
    assert ids, "存量原子不应为空"
    for aid in ids:
        assert isinstance(ia.upstream(aid), list)
        assert isinstance(ia.downstream(aid), list)
        assert isinstance(ia.references(aid), list)


def test_json_report_format():
    """JSON 输出与四工具风格一致（tool/version/timestamp/summary）。"""
    ids = [str(ge._meta(p).get("id") or p.stem) for p in ge._cards(ge.ATOMS, "ATOM-*.md")]
    data = ia.report("upstream", ids[0])
    assert data["tool"] == "impact_analysis" and data["direction"] == "upstream"
    assert {"deps", "refs", "summary", "version", "timestamp"} <= set(data)
    assert isinstance(data["summary"]["deps"], int)
