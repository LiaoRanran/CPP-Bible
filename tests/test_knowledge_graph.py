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
    # 526 时"按口语名查不到"是痛点；527 接上别名表后**同一条查询应当查得到**
    # （栅栏 → 内存屏障(fence)），并有 aliased 标记说明发生了别名解析
    hit = kg.concepts(conn, "栅栏")
    assert hit["found"] is True and hit["aliased"] is True, hit
    assert hit["concept"] == "内存屏障(fence)" and hit["props"] == 2
    # 真正不存在的概念仍须显式说没有（别把"别名解析"变成"什么都能查到"）
    miss = kg.concepts(conn, "这个概念不存在")
    assert miss["found"] is False and miss["props"] == 0


_ALIAS_PROP = ("\n  - id: prop-1\n    subject: 栅栏\n    predicate: 落在循环体内时\n"
               "    object: 阻止编译器消除该循环\n    claim_type: observation\n"
               "    statement: st1\n    extracted_by: writer")


def test_alias_table_normalizes_proposition_subject(sandbox: Path, tmp_path: Path,
                                                   monkeypatch):
    """527 任务C：命题里若写 Book/ 口语别名，入图前须归一到规范名（否则同概念两个节点）。"""
    tbl = tmp_path / "aliases.txt"
    tbl.write_text("# 测试表\n内存屏障(fence) <- 栅栏, memory fence\n"
                   "互斥量(mutex) <- 互斥锁\n", encoding="utf-8")
    monkeypatch.setattr(kg, "CONCEPT_ALIASES", tbl)
    db = tmp_path / "kga.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-AL.md",
           {"id": "ATOM-MEM-AL", "title": "t", "status": "draft",
            "claim_structured": _ALIAS_PROP})
    conn = kg.connect(db)
    out = kg.build(conn, verbose=False)
    assert out["aliases"] == 3 and out["alias_hits"] == 1, out   # 仅 subject 命中
    names = {r["name"] for r in kg.concepts(conn)["items"]}
    assert "内存屏障(fence)" in names and "栅栏" not in names, names
    # 查询侧也走别名：按口语名查得到规范名下的命题
    hit = kg.concepts(conn, "栅栏")
    assert hit["found"] and hit["aliased"] and hit["concept"] == "内存屏障(fence)", hit
    assert hit["props"] == 1
    # 别名表缺失时不得报错（可选增强，不是硬依赖）
    monkeypatch.setattr(kg, "CONCEPT_ALIASES", tmp_path / "nope.txt")
    assert kg.load_concept_aliases() == {}
    assert kg.build(conn, verbose=False)["alias_hits"] == 0


def test_alias_matching_is_exact_not_substring(sandbox: Path, tmp_path: Path,
                                              monkeypatch):
    """527 任务C（边界）：别名**整串**匹配，不做子串替换（`自旋锁`≠`锁`，`signal_fence`≠`fence`）。"""
    tbl = tmp_path / "aliases2.txt"
    tbl.write_text("互斥量(mutex) <- 锁\n内存屏障(fence) <- fence\n", encoding="utf-8")
    monkeypatch.setattr(kg, "CONCEPT_ALIASES", tbl)
    al = kg.load_concept_aliases()
    assert kg._canon_concept("锁", al) == ("互斥量(mutex)", True)
    assert kg._canon_concept("自旋锁", al) == ("自旋锁", False)
    assert kg._canon_concept("atomic_signal_fence", al) == ("atomic_signal_fence", False)
    assert kg._canon_concept("FENCE", al) == ("内存屏障(fence)", True)   # ASCII 大小写不敏感
    assert kg._canon_concept(" 栅栏 ", al) == ("栅栏", False)             # 不在本表


def _prop(subject: str, predicate: str, obj: str, ctype: str = "observation") -> str:
    return (f"\n  - id: prop-1\n    subject: {subject}\n    predicate: {predicate}\n"
            f"    object: {obj}\n    claim_type: {ctype}\n    statement: st\n"
            f"    extracted_by: writer")


def test_conflicts_detects_opposite_polarity(sandbox: Path, tmp_path: Path):
    """528 任务2：同 subject 且 object 极性相反的两条命题须被列为候选。"""
    db = tmp_path / "kgconf1.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-X1.md",
           {"id": "ATOM-MEM-X1", "title": "t", "status": "draft",
            "claim_structured": _prop("内存屏障(fence)", "在循环体内", "阻止编译器消除该循环")})
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-X2.md",
           {"id": "ATOM-MEM-X2", "title": "t", "status": "draft",
            "claim_structured": _prop("内存屏障(fence)", "对普通 int", "提供原子性")})
    conn = kg.connect(db)
    kg.build(conn, verbose=False)
    out = kg.conflicts(conn)
    assert out["candidates"] == 1, out
    it = out["items"][0]
    assert it["kind"] == "polarity" and it["polarity_pairs"], it
    assert {it["a_atom"], it["b_atom"]} == {"ATOM-MEM-X1", "ATOM-MEM-X2"}


def test_conflicts_no_false_positive_on_neutral_props(sandbox: Path, tmp_path: Path):
    """528 任务2（阴性）：同 subject 但 object 无极性相反 ⇒ 不得误报。"""
    db = tmp_path / "kgconf2.db"
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-Y1.md",
           {"id": "ATOM-MEM-Y1", "title": "t", "status": "draft",
            "claim_structured": _prop("sizeof", "在 x86-64 下", "8 字节")})
    _write(sandbox / "atoms" / "mem" / "ATOM-MEM-Y2.md",
           {"id": "ATOM-MEM-Y2", "title": "t", "status": "draft",
            "claim_structured": _prop("sizeof", "在 32 位下", "4 字节")})
    conn = kg.connect(db)
    kg.build(conn, verbose=False)
    assert kg.conflicts(conn) == {"candidates": 0, "items": []}


def test_conflicts_empty_graph_does_not_crash(sandbox: Path, tmp_path: Path):
    """528 任务2（边界）：空图（无任何命题）不崩、候选 0。"""
    db = tmp_path / "kgconf3.db"
    conn = kg.connect(db)
    kg.build(conn, verbose=False)
    assert kg.conflicts(conn)["candidates"] == 0


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
