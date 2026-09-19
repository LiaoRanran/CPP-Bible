"""592 任务3 · 命题闭包（`tools/prop_closure.py`）回归锁。

闭包是 R4 grounded 论证层的前置：**图算法的错法很多**（漏方向、环死循环、读写混用），
所以这里锁四件事：
  * 手工小图上的闭包**逐元素**正确（含环、含孤立点）；
  * Python 实现与 SQL `WITH RECURSIVE` 实现**在同一份边集上相等**（含真实库 79/79）；
  * 真实库**只读**：跑完哈希不变（闭包工具绝不改 `propositions.db`）；
  * 对账**真会红**：把 SQL 实现换成一个错的（只返回自身）⇒ `cross_check` 必须报 79 条不一致。
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import prop_closure as pc
import prop_graph as pg
import pytest

REAL_DB = pc.DEFAULT_DB


def _make_db(tmp_path: Path, props: list[tuple[str, str, str]],
             ev: list[tuple[str, str]], name: str = "p.db") -> Path:
    """建**临时**命题库（最小列面：props + prop_evidence），不碰真实 data/。"""
    p = tmp_path / name
    conn = sqlite3.connect(str(p))
    conn.executescript(
        "CREATE TABLE props(prop_key TEXT PRIMARY KEY, card TEXT NOT NULL,"
        " prop_id TEXT NOT NULL);"
        "CREATE TABLE prop_evidence(prop_key TEXT NOT NULL, evidence_id TEXT NOT NULL,"
        " PRIMARY KEY(prop_key, evidence_id));")
    conn.executemany("INSERT INTO props VALUES(?,?,?)", props)
    conn.executemany("INSERT INTO prop_evidence VALUES(?,?)", ev)
    conn.commit()
    conn.close()
    return p


# 手工图：5 命题（p1..p5）+ 1 卡（c1），6 条边
#   p1→p2→p3→p1 成环；p3→p4；p1→c1；c1→p2（卡再引回命题）
#   p5 **完全无边** ⇒ 孤立命题，闭包 = {p5}（锁"孤立"这一条）
MANUAL_EDGES = [("p1", "p2"), ("p2", "p3"), ("p3", "p1"),
                ("p3", "p4"), ("p1", "c1"), ("c1", "p2")]


def test_manual_graph_python_closure_is_elementwise_correct(tmp_path: Path):
    """5 命题 6 边手工图：闭包逐元素正确；环不死循环；够不到的命题不在闭包里。"""
    assert len(MANUAL_EDGES) == 6
    adj = pc.build_adjacency(MANUAL_EDGES)
    assert pc.closure("p1", adj) == {"p1", "p2", "p3", "p4", "c1"}
    assert pc.closure("p3", adj) == {"p1", "p2", "p3", "p4", "c1"}, "环内任一点闭包相同"
    assert "p5" not in pc.closure("p1", adj), "够不到的命题不得进闭包"
    assert pc.closure("p5", adj) == {"p5"}, "p5 无边 ⇒ 闭包 = 自身（孤立）"


def test_sql_closure_equals_python_on_manual_graph(tmp_path: Path):
    """同一份边集上，SQL `WITH RECURSIVE` 与 Python BFS 必须集合相等（含孤立点）。"""
    db = _make_db(tmp_path, [("p1", "c", "prop-1")], [])
    conn = sqlite3.connect(str(db))
    try:
        for start in ("p1", "p3", "p5", "z"):
            sq = pc.closure_sql(conn, start, MANUAL_EDGES)
            assert sq == pc.closure(start, pc.build_adjacency(MANUAL_EDGES)), start
        assert pc.closure_sql(conn, "p5", MANUAL_EDGES) == {"p5"}
        assert pc.closure_sql(conn, "z", MANUAL_EDGES) == {"z"}, "不在边里的起点 ⇒ 只返回自身"
    finally:
        conn.close()


def test_self_loop_and_cycle_terminate(tmp_path: Path):
    """自环 + 二元环必须终止（visited/UNION 去重），不得无限递归。"""
    edges = [("a", "a"), ("a", "b"), ("b", "a")]
    assert pc.closure("a", pc.build_adjacency(edges)) == {"a", "b"}
    db = _make_db(tmp_path, [("a", "c", "prop-1")], [])
    conn = sqlite3.connect(str(db))
    try:
        assert pc.closure_sql(conn, "a", edges) == {"a", "b"}
    finally:
        conn.close()


def test_edge_derivation_and_stats_on_temp_db(tmp_path: Path):
    """边从卡/证据**推导**（不是手写）：命题↔本卡、命题→证据卡、卡→命题。"""
    db = _make_db(tmp_path,
                  [("A/prop-1", "A", "prop-1"), ("A/prop-2", "A", "prop-2"),
                   ("B/prop-1", "B", "prop-1")],
                  [("A/prop-1", "EV-X"), ("B/prop-1", "EV-Y")])
    edges = set(pc.load_edges(db))
    assert edges == {
        ("A", "A/prop-1"), ("A", "A/prop-2"), ("B", "B/prop-1"),        # 卡 → 命题
        ("A/prop-1", "A"), ("A/prop-2", "A"), ("B/prop-1", "B"),        # 命题 → 本卡
        ("A/prop-1", "EV-X"), ("B/prop-1", "EV-Y"),                     # 命题 → 证据卡
    }, "边推导口径漂移"
    st = pc.stats(db)
    assert st["propositions"] == 3 and st["cards"] == 2 and st["edges"] == 8
    assert st["isolated"] == [], "本图每个命题都连着自己的卡 ⇒ 无孤立命题"
    # A/prop-1 闭包 = {A/prop-1, A, A/prop-2, EV-X}；B/prop-1 闭包 = {B/prop-1, B, EV-Y}
    assert st["closure_sizes"]["A/prop-1"] == 4
    assert st["closure_sizes"]["B/prop-1"] == 3
    assert st["max_closure_size"] == 4


def test_resolve_prefers_exact_key_then_prop_id(tmp_path: Path):
    db = _make_db(tmp_path, [("A/prop-1", "A", "prop-1"), ("B/prop-1", "B", "prop-1")], [])
    assert pc.resolve(db, "A/prop-1") == ["A/prop-1"], "全名精确命中优先"
    assert pc.resolve(db, "prop-1") == ["A/prop-1", "B/prop-1"], "卡内 id 重名 ⇒ 全量且排序确定"
    assert pc.resolve(db, "不存在") == []


def test_cross_check_is_falsifiable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """可证伪：把 SQL 实现换成一个**错的**（只返回自身）⇒ 对账必须报不一致（不是恒绿）。"""
    bad = []
    for key in pc.prop_keys(REAL_DB):
        bad.append({"prop_key": key, "only_python": [], "only_sql": []})
    monkeypatch.setattr(pc, "closure_sql", lambda _conn, start, _edges=None: {start})
    mism = pc.cross_check(REAL_DB)
    assert len(mism) == len(bad) == 79, f"错实现应被逐条抓出，实得 {len(mism)}"
    assert all(m["only_python"] for m in mism), "差异方向应指向 Python 多出来的节点"


def test_cross_check_and_stats_on_real_db():
    """真实库：双实现 79/79 一致；统计与 `prop_graph` 的命题数**交叉一致**。"""
    mismatches = pc.cross_check(REAL_DB)
    assert mismatches == [], f"双实现不一致：{mismatches[:5]}"
    st = pc.stats(REAL_DB)
    assert st["propositions"] == pg.stats(REAL_DB)["propositions"] == 79
    assert st["cards"] == 27
    assert st["edges"] == 274
    assert st["isolated"] == []
    assert st["max_closure_size"] <= 50, "闭包异常（>50）应在台账里单列"


def test_real_db_is_not_modified_by_readonly_ops():
    """只读硬纪律：stats/cross-check/load_edges 跑完，`propositions.db` 字节哈希不变。"""
    before = hashlib.sha256(REAL_DB.read_bytes()).hexdigest()
    pc.stats(REAL_DB)
    pc.cross_check(REAL_DB)
    pc.load_edges(REAL_DB)
    pc.resolve(REAL_DB, "prop-1")
    after = hashlib.sha256(REAL_DB.read_bytes()).hexdigest()
    assert before == after, "闭包工具改动了真实命题库（只读纪律被破坏）"


def test_missing_or_incompatible_db_fails_loud(tmp_path: Path):
    """缺库 / 缺表 ⇒ fail-loud + 直接给重建命令（不抛裸 OperationalError）。"""
    with pytest.raises(SystemExit, match="库不存在"):
        pc.stats(tmp_path / "nope.db")
    empty = tmp_path / "empty.db"
    sqlite3.connect(str(empty)).close()
    with pytest.raises(SystemExit, match="缺表"):
        pc.stats(empty)
    no_col = tmp_path / "nocol.db"
    conn = sqlite3.connect(str(no_col))
    conn.executescript("CREATE TABLE props(prop_key TEXT);"
                       "CREATE TABLE prop_evidence(a TEXT);")
    conn.commit()
    conn.close()
    with pytest.raises(SystemExit, match="缺列"):
        pc.stats(no_col)
