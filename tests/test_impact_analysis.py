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


# ── 558 Part C（557 D 停点）：多跳传递闭包 + 环检测 ─────────────────────────────


def test_558_chain_multihop_no_duplicates(sb: Path):
    """链式 A→B→C：闭包出 B(1 跳) 与 A(2 跳)，且同一原子**不重复**出现。"""
    _atom(sb, "ATOM-A", "\n  - prerequisite: ATOM-B")
    _atom(sb, "ATOM-B", "\n  - prerequisite: ATOM-C")
    _atom(sb, "ATOM-C", "[]")
    got = ia.upstream_closure("ATOM-C")
    assert [(d["atom"], d["depth"]) for d in got] == [("ATOM-B", 1), ("ATOM-A", 2)], got
    assert len({d["atom"] for d in got}) == len(got), "同一原子不得重复计数"
    got2 = ia.downstream_closure("ATOM-A")
    assert [(d["atom"], d["depth"]) for d in got2] == [("ATOM-B", 1), ("ATOM-C", 2)], got2


def test_558_diamond_counts_sink_once(sb: Path):
    """菱形 A→B→D、A→C→D：汇点 D 只算一次（最短跳数），不因两条路径重复计数。"""
    _atom(sb, "ATOM-A", "\n  - prerequisite: ATOM-B\n  - prerequisite: ATOM-C")
    _atom(sb, "ATOM-B", "\n  - prerequisite: ATOM-D")
    _atom(sb, "ATOM-C", "\n  - prerequisite: ATOM-D")
    _atom(sb, "ATOM-D", "[]")
    got = ia.upstream_closure("ATOM-D")
    assert [(d["atom"], d["depth"]) for d in got] == \
        [("ATOM-B", 1), ("ATOM-C", 1), ("ATOM-A", 2)], got
    assert len(got) == len({d["atom"] for d in got}), "菱形依赖不得重复计数"


def test_558_depth_caps_hops(sb: Path):
    """`depth` 封顶：depth=1 只出直接邻居；`None` = 不限跳数。"""
    _atom(sb, "ATOM-A", "\n  - prerequisite: ATOM-B")
    _atom(sb, "ATOM-B", "\n  - prerequisite: ATOM-C")
    _atom(sb, "ATOM-C", "[]")
    assert [d["atom"] for d in ia.upstream_closure("ATOM-C", depth=1)] == ["ATOM-B"]
    assert [d["atom"] for d in ia.upstream_closure("ATOM-C", depth=None)] == \
        ["ATOM-B", "ATOM-A"]


def test_558_self_loop_raises(sb: Path):
    """自环（A prerequisite A）⇒ 显式 `CycleError`（不无限递归、不静默截断）。"""
    _atom(sb, "ATOM-A", "\n  - prerequisite: ATOM-A")
    with pytest.raises(ia.CycleError) as ei:
        ia.upstream_closure("ATOM-A")
    assert ei.value.cycle[0] == ei.value.cycle[-1] == "ATOM-A", ei.value.cycle
    with pytest.raises(ia.CycleError):
        ia.downstream_closure("ATOM-A")


def test_558_cycle_raises_with_path(sb: Path):
    """成环 A→B→A ⇒ `CycleError`，cycle 首尾同节点（把环路显式打出来给人看）。"""
    _atom(sb, "ATOM-A", "\n  - specializes: ATOM-B")
    _atom(sb, "ATOM-B", "\n  - realizes: ATOM-A")
    with pytest.raises(ia.CycleError) as ei:
        ia.downstream_closure("ATOM-A")
    cyc = ei.value.cycle
    assert cyc[0] == cyc[-1] and len(cyc) >= 3, cyc
    assert set(cyc) == {"ATOM-A", "ATOM-B"}, cyc


def test_558_missing_target_fail_loud(sb: Path):
    """缺目标节点 ⇒ fail-loud（`SystemExit`），三种 depth 都不许静默给空影响面。"""
    _atom(sb, "ATOM-A", "[]")
    for d in (1, 2, 0):
        with pytest.raises(SystemExit):
            ia.report("upstream", "ATOM-NOPE", depth=d)


def test_558_report_multihop_schema(sb: Path):
    """多跳条目带 depth/via/path；`depth=1`（原口径）**不得**多出字段（向后兼容）。"""
    _atom(sb, "ATOM-A", "\n  - prerequisite: ATOM-B")
    _atom(sb, "ATOM-B", "[]")
    one = ia.report("upstream", "ATOM-B")
    assert set(one["deps"][0]) == {"atom", "rel_type", "path"}, "depth=1 输出不得加字段"
    multi = ia.report("upstream", "ATOM-B", depth=2)
    assert set(multi["deps"][0]) == {"atom", "rel_type", "path", "depth", "via"}
    assert multi["deps"][0]["via"] == "ATOM-B" and multi["summary"]["max_depth"] == 2
