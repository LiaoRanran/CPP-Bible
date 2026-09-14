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
