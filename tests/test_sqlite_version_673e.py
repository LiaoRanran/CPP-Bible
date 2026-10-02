#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673e 任务 D · SQLite 版本管理的**独立复现 + 最小修复验证**。

671e 的结论（本批独立复现并确认）：`meta.schema_version` 已有且与代码一致，
但 **`PRAGMA user_version` 恒为 0** —— 这是**真实存在的低严重度 gap**（671e 唯一没修的一条）：
SQLite 的**标准**版本机制没被用上，`sqlite3` CLI / ORM 等标准工具看不到版本，
只有本项目自己的读路径能判兼容。

673e 的最小修复（`tools/prop_graph.py`，只改这一处）：
  1. 新增只读访问器 `user_version(db)`；
  2. `build()` 在建库后写 `PRAGMA user_version = int(SCHEMA_VERSION)`；
  3. `_needs_rebuild()` 把 `PRAGMA user_version` 不符也当作需要重建（自愈一次即可收敛）。

**本批刻意不重建活库 `data/propositions.db`**：它由 671e 的
`test_current_db_user_version_is_zero_documents_gap` 断言"== 0"来记录 gap，而该测试文件
**正被 673b 在途修改** ⇒ 重建会打破 673b 的工作树（红线 4：跳过并登记）。
交接项见 `data/673e_验收报告.md`。
"""
from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def _load_prop_graph():
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location("_pg_673e", TOOLS / "prop_graph.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_pg_673e"] = mod          # 671g 教训：exec 前先登记，否则 @dataclass 会崩
    spec.loader.exec_module(mod)
    return mod


pg = _load_prop_graph()


def _fresh_db(tmp_path) -> Path:
    db = tmp_path / "props.db"
    pg.build(db)
    return db


# ── 1. 修复本体：build 必须把版本同步进 PRAGMA ───────────────────────────────
def test_fresh_build_sets_pragma_user_version(tmp_path):
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    uv = con.execute("PRAGMA user_version").fetchone()[0]
    con.close()
    assert uv == int(pg.SCHEMA_VERSION), \
        f"build 后 PRAGMA user_version 应为 {pg.SCHEMA_VERSION}，实际 {uv}"


def test_fresh_build_meta_and_pragma_agree(tmp_path):
    """两条版本通道必须一致（自建 meta 与标准 PRAGMA 不能各说各话）。"""
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    meta = con.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0]
    uv = con.execute("PRAGMA user_version").fetchone()[0]
    con.close()
    assert str(meta) == str(uv) == pg.SCHEMA_VERSION


def test_user_version_accessor_reads_zero_for_absent_db(tmp_path):
    assert pg.user_version(tmp_path / "nope.db") == 0


def test_user_version_accessor_reads_written_value(tmp_path):
    db = _fresh_db(tmp_path)
    assert pg.user_version(db) == int(pg.SCHEMA_VERSION)


# ── 2. 镜像语义：PRAGMA 落后 **不重建**，就地回填即可 ────────────────────────
def test_pragma_mismatch_does_not_trigger_rebuild(tmp_path):
    """设计取舍（673e 踩坑后修正）：`PRAGMA user_version` 是 `meta.schema_version` 的**镜像**，
    镜像落后 ≠ 数据损坏 ⇒ **不应**触发整库重建（否则白跑一次全量抽取）。

    实测依据：673e 初版把镜像不符当重建条件，直接让 3 条既有测试变红
    （`test_needs_rebuild_returns_false_for_current_real_db`、
    `test_needs_rebuild_ok_when_current_schema_and_version`、
    `test_build_does_not_touch_cards`）。
    """
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    con.execute("PRAGMA user_version = 0")          # 模拟 671e 实测的旧库状态
    con.commit()
    con.close()
    stale, why = pg._needs_rebuild(db)
    assert stale is False, f"镜像落后不应触发重建；实际 why={why!r}"
    assert "镜像" in why or "user_version" in why, "应把镜像落后这件事说出来（可见性）"


def test_sync_user_version_backfills_in_place(tmp_path):
    """就地回填：纯元数据写，不动数据行。"""
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    con.execute("PRAGMA user_version = 0")
    con.commit()
    n_rows_before = con.execute("SELECT COUNT(*) FROM props").fetchone()[0]
    con.close()

    assert pg.sync_user_version(db) == int(pg.SCHEMA_VERSION)
    assert pg.user_version(db) == int(pg.SCHEMA_VERSION)

    con = sqlite3.connect(str(db))
    n_rows_after = con.execute("SELECT COUNT(*) FROM props").fetchone()[0]
    con.close()
    assert n_rows_after == n_rows_before, "回填镜像不得改动数据行"


def test_sync_user_version_is_idempotent(tmp_path):
    db = _fresh_db(tmp_path)
    assert pg.sync_user_version(db) == int(pg.SCHEMA_VERSION)
    assert pg.sync_user_version(db) == int(pg.SCHEMA_VERSION)
    assert pg._needs_rebuild(db)[0] is False


def test_build_backfills_stale_mirror_without_rebuilding(tmp_path):
    """`build` 在"库已最新"路径上也要把镜像补上（幂等）。"""
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    con.execute("PRAGMA user_version = 0")
    con.commit()
    con.close()
    pg.build(db)
    assert pg.user_version(db) == int(pg.SCHEMA_VERSION)


def test_sync_user_version_on_absent_db_returns_zero(tmp_path):
    assert pg.sync_user_version(tmp_path / "nope.db") == 0


def test_needs_rebuild_false_for_fresh_db(tmp_path):
    db = _fresh_db(tmp_path)
    stale, why = pg._needs_rebuild(db)
    assert stale is False, why


# ── 3. 版本升级路径：旧 schema 必须 fail-loud 或自愈，绝不抛裸异常 ─────────────
def test_schema_state_reports_missing_columns(tmp_path):
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    con.execute("DROP TABLE props")
    con.execute("CREATE TABLE props(prop_key TEXT)")   # 缺列
    con.commit()
    con.close()
    _ver, missing = pg.schema_state(db)
    assert missing, "缺列必须被体检出来"


def test_read_path_fails_loud_on_incompatible_schema(tmp_path):
    db = _fresh_db(tmp_path)
    con = sqlite3.connect(str(db))
    con.execute("DROP TABLE props")
    con.execute("CREATE TABLE props(prop_key TEXT)")
    con.commit()
    con.close()
    with pytest.raises(SystemExit) as e:
        pg._connect(db)
    assert "schema 不兼容" in str(e.value) or "重建" in str(e.value)


def test_read_path_ok_for_fresh_db(tmp_path):
    db = _fresh_db(tmp_path)
    con = pg._connect(db)                            # 不应抛
    con.close()


def test_pragma_round_trip_is_viable_on_this_sqlite(tmp_path):
    """修复可行性：本机 sqlite3 支持 PRAGMA user_version 往返（671e 曾验证过，这里再验一次）。"""
    p = tmp_path / "rt.db"
    con = sqlite3.connect(str(p))
    con.execute("PRAGMA user_version = 7")
    con.commit()
    assert con.execute("PRAGMA user_version").fetchone()[0] == 7
    con.close()
    con = sqlite3.connect(str(p))
    assert con.execute("PRAGMA user_version").fetchone()[0] == 7
    con.close()


# ── 4. 登记：活库仍未同步（交接项，非本批可做）──────────────────────────────
def test_live_db_state_is_registered_not_assumed():
    """如实登记活库状态：本批**不重建**活库（会打破 673b 在途的 671e 测试）。

    本断言只做"状态可见"，不做"必须为 0/2"的强断言 —— 一旦 673b 落盘并重建，
    这里仍然通过（两侧都被接受），避免本测试成为交接的绊脚石。
    """
    live = ROOT / "data" / "propositions.db"
    if not live.is_file():
        pytest.skip("活库不存在（本机未建）")
    uv = pg.user_version(live)
    assert uv in (0, int(pg.SCHEMA_VERSION)), \
        f"活库 PRAGMA user_version={uv} 既不是 0（未同步）也不是 {pg.SCHEMA_VERSION}（已同步）"
