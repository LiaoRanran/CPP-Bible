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

import json
import sqlite3
import subprocess
from pathlib import Path

import prop_graph as pg
import pytest

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
    # 640 A1 更新：632/634 人审授权填充后命题级 signed_by 79/79 全签（原 0）
    assert st["by_signoff"].get("prop_signed", 0) == 79, st["by_signoff"]
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
    signed = pg.query(db, sign="prop_signed")
    # 640 A1：签署后全部 79 条为 prop_signed，unsigned=0
    assert len(uns) == 0 and len(signed) == 79
    assert pg.query(db, machine=False) == []
    assert len(pg.query(db, machine=True)) == 79
    one = pg.query(db, prop_id=inf[0]["prop_key"])
    assert len(one) == 1 and one[0]["prop_key"] == inf[0]["prop_key"]
    some_card = obs[0]["card"]
    assert {r["card"] for r in pg.query(db, card=some_card)} == {some_card}
    assert pg.query(db, ctype="observation", sign="unsigned") == []


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
    # 640 A1：签署后不存在 unsigned ⇒ 「有锚未签」态为空集（该显形口径保留在
    # pending_signoff 视图的 fail-soft 路径里）；机验与签署仍互相独立地分列记录。
    assert all(r["signoff_state"] == "prop_signed" for r in rows)
    assert all(r["anchor_source"] == "evidence" for r in rows)


# ── 566 任务 0：旧 schema 库必须自愈（监工验收踩到的真 bug）────────────────────
# 病：565b 给 props 加了 `anchor_source`，但已存在的旧库（15 列）不会被升级 ⇒ 直接跑
# `stats` 崩 `sqlite3.OperationalError: no such column`（测试用新临时库全绿、用户一跑就崩）。
_OLD_SCHEMA = """
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE props(            -- 565b 之前的 15 列版本：**没有 anchor_source**
  prop_key TEXT PRIMARY KEY, card TEXT NOT NULL, card_path TEXT NOT NULL,
  card_kind TEXT NOT NULL, prop_id TEXT NOT NULL, claim_type TEXT NOT NULL,
  subject TEXT NOT NULL DEFAULT '', predicate TEXT NOT NULL DEFAULT '',
  object TEXT NOT NULL DEFAULT '', statement TEXT NOT NULL DEFAULT '',
  extracted_by TEXT NOT NULL DEFAULT '', signed_by TEXT NOT NULL DEFAULT '',
  evidence TEXT NOT NULL DEFAULT '', machine_verified INTEGER NOT NULL,
  signoff_state TEXT NOT NULL);
CREATE TABLE prop_evidence(prop_key TEXT NOT NULL, evidence_id TEXT NOT NULL,
                           PRIMARY KEY(prop_key, evidence_id));
"""


def _make_old_db(path: Path) -> Path:
    conn = sqlite3.connect(str(path))
    conn.executescript(_OLD_SCHEMA)
    conn.execute("INSERT INTO meta(key,value) VALUES('tool','prop_graph.py')")   # 无 schema_version
    conn.execute("INSERT INTO props(prop_key,card,card_path,card_kind,prop_id,claim_type,"
                 "machine_verified,signoff_state) VALUES('OLD-CARD/prop-1','OLD-CARD','x.md',"
                 "'atom','prop-1','inference',0,'unsigned')")
    conn.commit()
    conn.close()
    return path


def test_566_old_schema_is_detected(tmp_path: Path):
    """旧库必须被**识别**（版本=1 且缺 anchor_source），不是等到崩了才知道。"""
    db = _make_old_db(tmp_path / "old.db")
    ver, missing = pg.schema_state(db)
    assert ver == "1", ver
    assert missing == ["anchor_source"], missing
    assert pg._needs_rebuild(db)[0] is True
    # 全新库：无需重建（首次构建）
    assert pg._needs_rebuild(tmp_path / "nope.db") == (False, "库不存在或表缺失（首次构建）")


def test_566_old_schema_read_path_fails_loud_with_fix(tmp_path: Path):
    """读路径遇旧库：**清晰报错 + 给出重建命令**，绝不抛裸 OperationalError。"""
    db = _make_old_db(tmp_path / "old.db")
    for fn in (pg.stats, pg.query):
        with pytest.raises(SystemExit) as ei:
            fn(db)
        msg = str(ei.value)
        assert "build" in msg and "anchor_source" in msg, msg


def test_566_old_schema_build_self_heals(tmp_path: Path, capsys):
    """监工场景端到端：旧库 → build（自愈且**可见**）→ stats/query 都不崩、列齐、命题数 79。"""
    db = _make_old_db(tmp_path / "old.db")
    pg.build(db)
    assert "旧 schema 自愈" in capsys.readouterr().out, "自愈必须打出来（否则用户不知道发生了什么）"
    st = pg.stats(db)
    assert st["propositions"] == 79 and st["cards"] == 27
    assert st["by_claim_type"] == {"inference": 29, "observation": 50}
    cols = {r[1] for r in sqlite3.connect(str(db)).execute("PRAGMA table_info(props)")}
    assert set(pg.PROPS_COLUMNS) <= cols, sorted(set(pg.PROPS_COLUMNS) - cols)
    assert len(pg.query(db, sign="unsigned")) == 0  # 640 A1：签署后无未签命题
    ver, missing = pg.schema_state(db)
    assert ver == pg.SCHEMA_VERSION and missing == []


def test_566_official_db_is_current():
    """正式库要么已是当前 schema，要么能被自愈——防"测试全绿、用户一跑就崩"重演。"""
    f = pg.DEFAULT_DB
    if not f.is_file():
        pytest.skip("data/propositions.db 不在（未构建）")
    ver, missing = pg.schema_state(f)
    assert missing == [], (f"正式库缺列 {missing} ⇒ 跑 `.venv\\Scripts\\python.exe "
                           f"tools/prop_graph.py build`（版本 {ver}）")
    assert ver == pg.SCHEMA_VERSION, f"正式库 schema_version={ver} ∈ {pg.SCHEMA_VERSION}"


# ── 566 任务 1：人审交接视图 ──────────────────────────────────────────────────
def test_566_pending_signoff_lists_unsigned_only(tmp_path: Path):
    """待签视图 = `unsigned`（命题级 signed_by 与卡级 verified_by 都没有）——
    卡级人签（card_signed）**不进**本视图（口径不与 stats 混）。
    640 A1：签署后 unsigned=0 ⇒ 待签视图为空（fail-soft 路径由下方视图测试覆盖）。"""
    db = pg.build(tmp_path / "p.db")
    rows = pg.pending_signoff(db)
    assert rows == []
    assert len(pg.query(db, sign="card_signed")) == 0
    assert len(pg.query(db, sign="prop_signed")) == 79
    assert len(rows) + len(pg.query(db, sign="prop_signed")) == 79


def test_566_backlog_counts_atoms_minus_with_props(tmp_path: Path):
    """待回填 = 总原子卡 − 带命题卡（实测 27 − 27 = 0 ⇒ 无待办，fail-soft）。"""
    db = pg.build(tmp_path / "p.db")
    items, total = pg.backlog(db)
    have = len({r["card"] for r in pg.query(db)})
    assert total == 27, total
    assert len(items) == total - have, (len(items), total, have)
    assert items == [], "实测：27 张原子卡全部已有 claim_structured（与提示词假设的 26 张待回填不符）"


def test_566_views_are_fail_soft_and_json(tmp_path: Path, capsys, monkeypatch):
    """空结果 fail-soft（打印"无待办"不崩）+ 两个视图都支持 --json。
    640 A1：签署后 pending-signoff 真实结果就是空 ⇒ 本测试同时覆盖真实空与 patch 空。"""
    db = pg.build(tmp_path / "p.db")
    assert pg.main(["query", "--db", str(db), "--pending-signoff"]) == 0
    assert "无待办" in capsys.readouterr().out  # 640 A1：签署后无待签命题
    assert pg.main(["query", "--db", str(db), "--backlog"]) == 0
    assert "无待办" in capsys.readouterr().out
    assert pg.main(["query", "--db", str(db), "--pending-signoff", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["view"] == "pending_signoff" and data["count"] == 0
    assert pg.main(["query", "--db", str(db), "--backlog", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["view"] == "backlog" and data["atoms_total"] == 27
    # 真·空结果（patch 掉查询源）也必须是 fail-soft，不是 IndexError/KeyError
    monkeypatch.setattr(pg, "query", lambda *a, **k: [])
    assert pg.main(["query", "--db", str(db), "--pending-signoff"]) == 0
    assert "无待办" in capsys.readouterr().out
    monkeypatch.setattr(pg, "backlog", lambda *a, **k: ([], 27))
    assert pg.main(["query", "--db", str(db), "--backlog"]) == 0
    assert "无待办" in capsys.readouterr().out


def test_566_pending_view_prints_card_frontmatter_howto(tmp_path: Path, capsys):
    """人签指引必须落在**仓库既有接口**上（卡面 `verified_by: human:<名>` + git 作者校验）。
    640 A1：签署后待签视图恒为空 ⇒ howto 文案只在 --json 的 howto 字段/工具 help 里可见；
    此处锁定空态行为 + howto 文案仍可从 json 空态以外的常量途径获得。"""
    db = pg.build(tmp_path / "p.db")
    pg.main(["query", "--db", str(db), "--pending-signoff"])
    out = capsys.readouterr().out
    assert "无待办" in out, "签署后待签视图应为空（fail-soft）"
    # howto 文案（human: + git 校验 + 重建视图）仍是工具的固定指引文本：
    src = (REPO / "tools" / "prop_graph.py").read_text(encoding="utf-8")
    assert "verified_by: human:" in src
    assert "git 提交" in src, "必须提到 gate 的 git-作者校验规则"
    assert "prop_graph.py build" in src, "签完要重建视图"


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
    assert data["count"] == 0 and data["rows"] == []  # 640 A1：签署后无未签
    # 库不存在 ⇒ fail-loud（不静默给空结果）
    with pytest.raises(SystemExit):
        pg.query(tmp_path / "nope.db")
