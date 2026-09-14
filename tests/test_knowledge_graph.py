"""知识图谱 L1 回归锁（508 任务5）。

纪律：测试**不得**写真实 `data/knowledge_graph.db`，一律用 `tmp_path` 的库 + 沙箱
`ge.ATOMS/EVIDENCE`（与 test_gate_engine 的 sandbox 同法），否则并行/重复跑会互相踩。
覆盖：①建图与幂等；②deps/chain 沿 relations 走；③impact 由工件路径穿到原子。
"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge
import knowledge_graph as kg


def _write(path: Path, fields: dict[str, object]) -> None:
    """极简 frontmatter 写入（嵌套块以 `\\n` 起头，与 poison_drill._write 同约定）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    body = ""
    for k, v in fields.items():
        s = str(v)
        body += f"{k}:{s}\n" if s.startswith("\n") else f"{k}: {s}\n"
    path.write_text("---\n" + body + "---\n", encoding="utf-8")


@pytest.fixture()
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """沙箱：ATOMS/EVIDENCE 指向 tmp，RULES 清空（避免 55 个真实规则节点干扰计数）。"""
    atoms = tmp_path / "atoms"
    ev = tmp_path / "evidence"
    (atoms / "mem").mkdir(parents=True)
    (ev / "mem").mkdir(parents=True)
    monkeypatch.setattr(ge, "ATOMS", atoms)
    monkeypatch.setattr(ge, "EVIDENCE", ev)
    monkeypatch.setattr(ge, "RULES", [])
    monkeypatch.setattr(kg, "ROOT", tmp_path)
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    return tmp_path


def test_build_creates_graph_and_is_idempotent(sandbox: Path, tmp_path: Path):
    """① 建图：节点/边类型正确；连跑两次计数不变（幂等，不产生重复边）。"""
    db = tmp_path / "kg.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-A.md",
           {"id": "ATOM-MEM-A", "title": "A", "status": "verified",
            "relations": "\n  - {type: prerequisite, target: ATOM-MEM-B}"})
    _write(sandbox / "evidence" / "mem" / "EV-MEM-A.md",
           {"id": "EV-MEM-A", "hypothesis": "h", "verdict": "confirm",
            "serves": "[ATOM-MEM-A]", "artifact": "Examples/atoms/a.asm"})
    conn = kg.connect(db)
    first = kg.build(conn, verbose=False)
    # 4 节点 = ATOM-MEM-A + EV-MEM-A + stub ATOM-MEM-B（前置未锻造）+ artifact stub
    assert first["nodes"] == 4, first
    # 3 边 = PREREQUISITE(A→B) + SERVES(EV→A) + ASSERTS(EV→artifact)
    assert first["edges"] == 3, first
    st = kg.stats(conn)
    assert st["nodes_by_type"].get("ATOM") == 2, "真卡 1 + 前置 stub 1（悬空目标不吞）"
    assert st["nodes_by_type"].get("EVIDENCE") == 1
    assert st["nodes_by_type"].get("ARTIFACT") == 1, "artifact 字段应建工件节点"
    assert "ATOM-MEM-B" in st["dangling"], "未锻造的目标应留为 dangling 而非被丢弃"
    assert st["edges_by_type"].get("ASSERTS") == 1
    again = kg.build(conn, verbose=False)      # 幂等
    assert again["nodes"] == first["nodes"] and again["edges"] == first["edges"]


def test_deps_and_chain_follow_relations(sandbox: Path, tmp_path: Path):
    """② deps 取直接前置、chain 走多跳（A→B→C ⇒ deps(A)=[B] / chain(A)={B:1, C:2}）。"""
    db = tmp_path / "kg2.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-A.md",
           {"id": "ATOM-MEM-A",
            "relations": "\n  - {type: prerequisite, target: ATOM-MEM-B}"})
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-B.md",
           {"id": "ATOM-MEM-B",
            "relations": "\n  - {type: prerequisite, target: ATOM-MEM-C}"})
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-C.md", {"id": "ATOM-MEM-C"})
    conn = kg.connect(db)
    kg.build(conn, verbose=False)
    assert kg.deps(conn, "ATOM-MEM-A")["deps"] == [{"id": "ATOM-MEM-B",
                                                    "type": "PREREQUISITE"}]
    chain = {c["id"]: c["depth"] for c in kg.chain(conn, "ATOM-MEM-A")["chain"]}
    assert chain == {"ATOM-MEM-B": 1, "ATOM-MEM-C": 2}, chain


def test_impact_maps_artifact_path_to_atoms(sandbox: Path, tmp_path: Path):
    """③ impact：给**文件路径**（而非节点 id）能穿 工件→证据卡→原子；未知路径返回 found=False。"""
    db = tmp_path / "kg3.db"
    _write(sandbox / "evidence" / "mem" / "EV-MEM-X.md",
           {"id": "EV-MEM-X", "serves": "[ATOM-MEM-X]",
            "artifact": "Examples/atoms/_x.asm"})
    conn = kg.connect(db)
    kg.build(conn, verbose=False)
    out = kg.impact(conn, "Examples/atoms/_x.asm")
    assert out["found"] is True and out["atoms"] == ["ATOM-MEM-X"], out
    assert kg.impact(conn, "Examples/atoms/_nope.asm")["found"] is False


_PROPS = ("\n  - id: prop-1\n    subject: 内存屏障(fence)\n    predicate: 落在循环体内时\n"
          "    object: 阻止编译器消除该循环\n    claim_type: observation\n"
          "    statement: st1\n    extracted_by: writer\n"
          "  - id: prop-2\n    subject: 内存屏障(fence)\n    predicate: 不提供\n"
          "    object: 原子性\n    claim_type: inference\n    statement: st2\n"
          "    extracted_by: writer")


def test_concept_layer_built_from_claim_structured(sandbox: Path, tmp_path: Path):
    """526 Step4：命题的 subject/object 进概念层；**无 claim_structured 的卡不进**。"""
    db = tmp_path / "kgc.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-C.md",
           {"id": "ATOM-MEM-C", "title": "t", "status": "draft",
            "claim_structured": _PROPS})
    # 一张没有命题的卡：不该给概念层贡献任何东西（图谱只反映"可推理的命题"）
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-BARE.md",
           {"id": "ATOM-MEM-BARE", "title": "t2", "status": "draft"})
    conn = kg.connect(db)
    out = kg.build(conn, verbose=False)
    # 3 个概念 = {内存屏障(fence), 阻止编译器消除该循环, 原子性}；2 条命题边
    assert out["concepts"] == 3, out
    assert out["concept_edges"] == 2, out
    st = kg.stats(conn)
    assert st["concepts"] == 3 and st["concept_edges"] == 2
    again = kg.build(conn, verbose=False)          # 幂等
    assert again["concepts"] == 3 and again["concept_edges"] == 2


def test_concepts_query_lists_props_and_unknown_is_explicit(sandbox: Path,
                                                            tmp_path: Path):
    """526 Step4：`concepts <名>` 回该概念出现在哪些命题；查不到必须**显式**说没有。"""
    db = tmp_path / "kgc2.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-C.md",
           {"id": "ATOM-MEM-C", "title": "t", "status": "draft",
            "claim_structured": _PROPS})
    conn = kg.connect(db)
    kg.build(conn, verbose=False)
    out = kg.concepts(conn, "内存屏障(fence)")
    assert out["found"] is True and out["props"] == 2, out
    assert out["claim_types"] == {"observation": 1, "inference": 1}
    assert {i["atom"] for i in out["items"]} == {"ATOM-MEM-C"}
    assert all(i["prop"].startswith("prop-") for i in out["items"])
    lst = kg.concepts(conn)
    assert lst["concepts"] == 3
    assert lst["items"][0]["props"] == 2, "按命题数降序，内存屏障(fence) 应排首位"
    miss = kg.concepts(conn, "栅栏")               # Book/ 层的口语写法，概念层没有
    assert miss["found"] is False and miss["props"] == 0


def test_real_repo_graph(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """真实仓库建图（只读）：卡节点 ≥ 160，且每条边的两端都在 nodes 里（外键完整性）。"""
    conn = kg.connect(tmp_path / "real.db")
    kg.build(conn, verbose=False)
    st = kg.stats(conn)
    assert st["card_nodes"] >= 160, st["card_nodes"]
    orphan = conn.execute(
        "SELECT COUNT(*) FROM edges e LEFT JOIN nodes n1 ON e.src = n1.id "
        "LEFT JOIN nodes n2 ON e.dst = n2.id WHERE n1.id IS NULL OR n2.id IS NULL"
    ).fetchone()[0]
    assert orphan == 0, "存在端点不在 nodes 表的边（悬空目标未被补为 stub 节点）"
