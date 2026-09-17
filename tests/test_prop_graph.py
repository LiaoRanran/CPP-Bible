"""565 Part 3 · 命题状态图（`tools/prop_graph.py`）回归锁。

锁四件事：
  ① 幂等：连跑两次 build，**逐行内容一致**（表全 DROP 重建、不存时间戳 ⇒ 可重建视图）；
  ② 总量与分布：79 命题 / 27 卡 / observation 50 / inference 29（与 T0 实测底座一致）；
  ③ 查询正确：按 claim_type / 签署状态 / 机验状态 / 卡 / 命题 id 检索都对得上；
  ④ **重建不改卡**：build 前后受控目录（atoms/evidence）git status 零差异——
     这是"只读派生视图，绝不自动入库新命题、绝不改卡"的机器证据。

库写在 pytest 的 tmp 目录（不碰 `data/propositions.db` 真库），但**读的还是真实卡**。
"""
from __future__ import annotations

import sqlite3
import subprocess
from pathlib import Path

import pytest

import prop_graph as pg

REPO = pg.ROOT


def _dump(db: Path) -> list[tuple]:
    """把库内容导成可比对的元组列表（含两张表；顺序固定 ⇒ 幂等判据）。"""
    conn = sqlite3.connect(str(db))
    try:
        props = conn.execute(
            "SELECT * FROM props ORDER BY prop_key").fetchall()
        ev = conn.execute(
            "SELECT * FROM prop_evidence ORDER BY prop_key, evidence_id").fetchall()
        meta = conn.execute("SELECT * FROM meta ORDER BY key").fetchall()
    finally:
        conn.close()
    return props + [("--ev--",)] + ev + [("--meta--",)] + meta


def test_build_totals_and_distributions(tmp_path: Path):
    """79 命题 / 27 卡 / obs 50 / inf 29（T0 实测底座）。"""
    db = pg.build(tmp_path / "p.db")
    st = pg.stats(db)
    assert st["propositions"] == 79, st
    assert st["cards"] == 27, st
    assert st["by_claim_type"] == {"inference": 29, "observation": 50}, st["by_claim_type"]
    # 当前实测底座：命题级 signed_by 0 条 ⇒ 签署只能落在 card_signed / unsigned
    assert st["by_signoff"].get("prop_signed", 0) == 0, st["by_signoff"]
    assert sum(st["by_signoff"].values()) == 79
    assert st["by_anchor_source"].get("none", 0) == 0, st["by_anchor_source"]


def test_build_is_idempotent(tmp_path: Path):
    """连跑两次 build：两张表 + meta **逐行一致**（视图可重建，不含时间戳）。"""
    db = tmp_path / "p.db"
    pg.build(db)
    first = _dump(db)
    pg.build(db)
    second = _dump(db)
    assert first == second, "build 不幂等：两次内容不一致"
    assert len(first) > 79, "导出应含 props + prop_evidence"


def test_build_does_not_touch_cards(tmp_path: Path):
    """build 前后受控目录 git status 零差异（只读派生 ⇒ 绝不改卡）。"""

    def _status() -> str:
        out = subprocess.run(["git", "status", "--porcelain", "--", "atoms", "evidence"],
                             cwd=str(REPO), capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        # pre-existing 的 M（evidence/conc/EV-CONC-001.md）与本批无关，剔除后要求空
        lines = [ln for ln in out.stdout.splitlines()
                 if "EV-CONC-001.md" not in ln]
        return "\n".join(lines)

    before = _status()
    pg.build(tmp_path / "p.db")
    assert _status() == before == "", "build 动了受控目录（必须只读）"


def test_query_by_type_and_sign(tmp_path: Path):
    """按类型/签署/机验/卡/命题 id 检索：计数与逐条归属都对得上。"""
    db = pg.build(tmp_path / "p.db")
    obs = pg.query(db, ctype="observation")
    inf = pg.query(db, ctype="inference")
    assert len(obs) == 50 and len(inf) == 29
    assert {r["claim_type"] for r in obs} == {"observation"}
    uns = pg.query(db, sign="unsigned")
    signed = pg.query(db, sign="card_signed")
    assert len(uns) + len(signed) == 79 and len(uns) == 3
    assert pg.query(db, machine=False) == []
    assert len(pg.query(db, machine=True)) == 79
    one = pg.query(db, prop_id=inf[0]["prop_key"])
    assert len(one) == 1 and one[0]["prop_key"] == inf[0]["prop_key"]
    some_card = obs[0]["card"]
    assert {r["card"] for r in pg.query(db, card=some_card)} == {some_card}
    assert len(pg.query(db, ctype="observation", sign="unsigned")) <= 3


def test_unsigned_props_have_no_card_signoff(tmp_path: Path):
    """unsigned 的判据必须与卡的 `verified_by` 一致（不是随手标的）。"""
    import gate_engine as ge
    db = pg.build(tmp_path / "p.db")
    for r in pg.query(db, sign="unsigned"):
        meta = ge._meta(REPO / r["card_path"])
        assert not str(meta.get("verified_by") or ""), r["prop_key"]
        assert not r["signed_by"], r["prop_key"]
    for r in pg.query(db, sign="card_signed"):
        meta = ge._meta(REPO / r["card_path"])
        assert str(meta.get("verified_by") or ""), r["prop_key"]


def test_anchor_source_splits_card_vs_evidence(tmp_path: Path):
    """有锚要分清来源。实测底座：命题**全部来自 27 张 atom 卡**（证据卡不带
    `claim_structured`），而 atom 卡自身无机械锚点 ⇒ 命题的锚一律是 `evidence`（靠证据卡带）。"""
    db = pg.build(tmp_path / "p.db")
    rows = pg.query(db)
    assert {r["card_kind"] for r in rows} == {"atom"}, "claim_structured 只在原子卡上（实测）"
    assert {r["anchor_source"] for r in rows} == {"evidence"}, \
        "atom 卡自身无锚（实测 27/27）⇒ 命题只能靠 evidence 卡带锚"
    assert all(r["machine_verified"] == 1 for r in rows)
    # 机验状态与签署状态**互相独立**：有锚 ≠ 已签（当前 3 条 unsigned 也有锚）
    assert any(r["anchor_source"] == "evidence" and r["signoff_state"] == "unsigned"
               for r in rows), "应存在「有机器锚点但未签」的命题（这正是要显形的态）"


def test_cli_build_stats_query(tmp_path: Path, capsys):
    """CLI：build / stats / query 三条子命令可用（--json 机器可读）。"""
    db = str(tmp_path / "p.db")
    assert pg.main(["build", "--db", db]) == 0
    assert "命题 79" in capsys.readouterr().out
    assert pg.main(["stats", "--db", db, "--json"]) == 0
    st = __import__("json").loads(capsys.readouterr().out)
    assert st["propositions"] == 79
    assert pg.main(["query", "--db", db, "--sign", "unsigned", "--json"]) == 0
    data = __import__("json").loads(capsys.readouterr().out)
    assert data["count"] == 3 and all(r["signoff_state"] == "unsigned" for r in data["rows"])
    # 库不存在 ⇒ fail-loud（不静默给空结果）
    with pytest.raises(SystemExit):
        pg.query(tmp_path / "nope.db")
