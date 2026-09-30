# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
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

import counts_659 as counts  # 666 A2：去写死——命题/卡数一律从事实源现算
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
    """派生库 vs **卡面事实源**：命题数/卡数不写死，分布只锁结构。

    666 A2 去写死（原：79 命题 / 27 卡 / obs 50 / inf 29 —— 640 时点的**测量快照**）。
    冻结测量值 = 语料一长就假红，且逼后人"改到绿"。改为：
      · 总数对齐事实源：命题 `counts.PROPOSITIONS`（扫卡面 claim_structured）、
        卡 `counts.ATOMS_REAL`（实卡域，不含 atoms/draft650 的插画草稿）；
      · 分布只锁**结构**（两类齐 + 合计 = 命题数），比值是测量值、不冻结；
      · 签署只锁**可加性**（prop_signed + unsigned == 命题数）——"全签"是 640 的
        **状态**而非事实，后面新增卡可以重新引入未签命题（本轮就有 10 条）。
    """
    db = pg.build(tmp_path / "p.db")
    st = pg.stats(db)
    assert st["propositions"] == counts.PROPOSITIONS, st
    assert st["cards"] == counts.ATOMS_REAL, st
    assert set(st["by_claim_type"]) == {"inference", "observation"}, st["by_claim_type"]
    assert sum(st["by_claim_type"].values()) == counts.PROPOSITIONS, st["by_claim_type"]
    # 669 修订：签署状态域是**三态**（prop_signed / card_signed / unsigned，见 prop_graph.extract）——
    # 668 的 5 张机器卡在 669 补了机器 principal 署名（`verified_by: machine:*`，gate 的
    # S1-AUTHOR-SELF-VERIFY 要求），于是它们 10 条命题合法地进入 `card_signed`（卡级签署）。
    # 原断言只认两态 ⇒ 把"域"当成"当时的观测值"锁死了。改为锁**域 + 可加性**。
    sign = st["by_signoff"]
    assert set(sign) <= {"prop_signed", "card_signed", "unsigned"}, sign
    assert sum(sign.values()) == counts.PROPOSITIONS, sign
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
    """按类型/签署/机验/卡/命题 id 检索：计数与逐条归属都对得上。

    666 A2 去写死：`obs==50 / inf==29 / signed==79` 是 640 时点快照。改为
    **划分性**断言（两类互斥且合起来是全集；已签/未签互斥且合起来是全集）。
    """
    db = pg.build(tmp_path / "p.db")
    obs = pg.query(db, ctype="observation")
    inf = pg.query(db, ctype="inference")
    assert {r["claim_type"] for r in obs} == {"observation"}
    assert {r["claim_type"] for r in inf} == {"inference"}
    uns = pg.query(db, sign="unsigned")
    signed = pg.query(db, sign="prop_signed")
    card_signed = pg.query(db, sign="card_signed")     # 669：机器 principal 卡级署名（第三态）
    assert len(obs) + len(inf) == counts.PROPOSITIONS
    assert len(uns) + len(signed) + len(card_signed) == counts.PROPOSITIONS
    keysets = [{r["prop_key"] for r in g} for g in (uns, signed, card_signed)]
    assert not (keysets[0] & keysets[1]) and not (keysets[0] & keysets[2]) \
        and not (keysets[1] & keysets[2]), "三态必须互斥"
    assert pg.query(db, machine=False) == []
    assert len(pg.query(db, machine=True)) == counts.PROPOSITIONS
    one = pg.query(db, prop_id=inf[0]["prop_key"])
    assert len(one) == 1 and one[0]["prop_key"] == inf[0]["prop_key"]
    some_card = obs[0]["card"]
    assert {r["card"] for r in pg.query(db, card=some_card)} == {some_card}
    # 666 A2：原来断言"观测类未签集为空"（640 全签状态）。改为**口径**断言：
    # 组合过滤 = 两个单条件结果的交集（而不是恒空）。
    combo = pg.query(db, ctype="observation", sign="unsigned")
    assert {r["prop_key"] for r in combo} == \
        ({r["prop_key"] for r in obs} & {r["prop_key"] for r in uns})


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
    # 666 A2：原断言"全部 prop_signed"是 640 的全签**状态**；本轮新增 10 条未签命题。
    # 改锁**状态域**（只允许两态，且与 sign= 查询口径一致），不锁谁多谁少。
    # 669 修订：状态域扩到三态（prop_signed / card_signed / unsigned）——668 的 5 张机器卡
    # 补齐机器 principal 署名后进入 card_signed；"未签"与"命题级人签"两态仍须显形。
    states = {r["signoff_state"] for r in rows}
    assert states <= {"prop_signed", "card_signed", "unsigned"}, states
    assert {"prop_signed", "unsigned"} <= states, "未签与命题级签署两态都必须显形"
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
    assert st["propositions"] == counts.PROPOSITIONS and st["cards"] == counts.ATOMS_REAL
    assert sum(st["by_claim_type"].values()) == counts.PROPOSITIONS
    cols = {r[1] for r in sqlite3.connect(str(db)).execute("PRAGMA table_info(props)")}
    assert set(pg.PROPS_COLUMNS) <= cols, sorted(set(pg.PROPS_COLUMNS) - cols)
    # 666 A2：自愈后**两态都可检索**（原断言 unsigned==0 = 640 全签状态，非口径）。
    # 669：状态域为三态（`card_signed` 见 prop_graph.extract）⇒ 用全和断言。
    assert sum(len(pg.query(db, sign=s)) for s in
               ("unsigned", "prop_signed", "card_signed")) == counts.PROPOSITIONS
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

    666 A2 去写死：原断言"视图恒空 + signed==79"是 640 全签状态；本轮新增 10 条未签。
    改锁**口径**：视图内容 == `sign=unsigned` 的集合（逐条同 id），且与已签互斥。
    """
    db = pg.build(tmp_path / "p.db")
    rows = pg.pending_signoff(db)
    uns = pg.query(db, sign="unsigned")
    signed = pg.query(db, sign="prop_signed")
    card_signed = pg.query(db, sign="card_signed")     # 669：机器 principal 卡级署名（第三态）
    assert {r["prop_key"] for r in rows} == {r["prop_key"] for r in uns}
    # 口径不变：待签视图 = 命题级未签，**不含**卡级署名（否则"卡级签过"会被当成"人已核准"）
    assert not ({r["prop_key"] for r in rows} & {r["prop_key"] for r in card_signed}), \
        "卡级署名（card_signed）不得进待签视图"
    assert len(rows) + len(signed) + len(card_signed) == counts.PROPOSITIONS


def test_566_backlog_counts_atoms_minus_with_props(tmp_path: Path):
    """待回填 = 总原子卡 − 带命题卡。

    666 A2 去写死：原写死"27 − 27 = 0 ⇒ 无待办"。650 批次往 `atoms/draft650/` 放了
    10 张**无 claim_structured 的插画草稿**，`backlog.total` 随之口径为 ATOMS_TOTAL(47)，
    待回填非空（10）——这正是 backlog 视图该显形的东西，不是坏。改为现算：
    分母用 `counts.ATOMS_TOTAL`，分子 == 分母 − 已有命题的卡数，且逐条与之一致。
    """
    db = pg.build(tmp_path / "p.db")
    items, total = pg.backlog(db)
    have = {r["card"] for r in pg.query(db)}
    assert total == counts.ATOMS_TOTAL, total
    assert len(items) == total - len(have), (len(items), total, len(have))
    assert {i["card"] for i in items} & have == set(), "已有命题的卡不得出现在待回填里"


def test_566_views_are_fail_soft_and_json(tmp_path: Path, capsys, monkeypatch):
    """空结果 fail-soft（打印"无待办"不崩）+ 两个视图都支持 --json。
    640 A1：签署后 pending-signoff 真实结果就是空 ⇒ 本测试同时覆盖真实空与 patch 空。"""
    db = pg.build(tmp_path / "p.db")
    n_uns = len(pg.query(db, sign="unsigned"))
    assert pg.main(["query", "--db", str(db), "--pending-signoff"]) == 0
    out = capsys.readouterr().out
    # 666 A2：非空时列人签指引，空时才打印"无待办"（两种都必须 fail-soft 不崩）
    assert ("无待办" in out) if n_uns == 0 else ("未人签命题" in out), out[:200]
    assert pg.main(["query", "--db", str(db), "--backlog"]) == 0
    capsys.readouterr()
    assert pg.main(["query", "--db", str(db), "--pending-signoff", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["view"] == "pending_signoff" and data["count"] == n_uns
    assert pg.main(["query", "--db", str(db), "--backlog", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["view"] == "backlog" and data["atoms_total"] == counts.ATOMS_TOTAL
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
    # 666 A2：视图非空时打印**人签指引**（本例要锁的就是指引），空时才打印"无待办"。
    assert ("无待办" in out) or ("未人签命题" in out), out[:200]
    assert ("verified_by: human:" in out) or ("未人签命题" not in out), \
        "非空视图必须给出人签指引（卡面 verified_by: human:）"
    # howto 文案（human: + git 校验 + 重建视图）仍是工具的固定指引文本：
    src = (REPO / "tools" / "prop_graph.py").read_text(encoding="utf-8")
    assert "verified_by: human:" in src
    assert "git 提交" in src, "必须提到 gate 的 git-作者校验规则"
    assert "prop_graph.py build" in src, "签完要重建视图"


def test_cli_build_stats_query(tmp_path: Path, capsys):
    """CLI：build / stats / query 三条子命令可用（--json 机器可读）。"""
    db = str(tmp_path / "p.db")
    assert pg.main(["build", "--db", db]) == 0
    assert f"命题 {counts.PROPOSITIONS}" in capsys.readouterr().out   # 666 A2：现算
    assert pg.main(["stats", "--db", db, "--json"]) == 0
    st = __import__("json").loads(capsys.readouterr().out)
    assert st["propositions"] == counts.PROPOSITIONS
    n_uns = len(pg.query(Path(db), sign="unsigned"))
    assert pg.main(["query", "--db", db, "--sign", "unsigned", "--json"]) == 0
    data = __import__("json").loads(capsys.readouterr().out)
    assert data["count"] == n_uns and len(data["rows"]) == n_uns    # 666 A2：与查询现算一致
    # 库不存在 ⇒ fail-loud（不静默给空结果）
    with pytest.raises(SystemExit):
        pg.query(tmp_path / "nope.db")
