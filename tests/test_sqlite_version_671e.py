# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671e-D · SQLite 版本管理核查测试。

**核查结论（先复现，再下结论）**：
671c 调研把"SQLite 无版本管理 ⇒ 数据库不可复算"列为 *缺陷候选*。
本批经读库 + 读构建脚本，结论是 **false positive（"无版本管理"不成立）**：

  * `data/propositions.db` 的 `meta` 表存有 `schema_version='2'`、`tool='prop_graph.py'`；
  * `tools/prop_graph.py` 定义 `SCHEMA_VERSION = "2"`，并提供
    `_needs_rebuild(db) -> (bool, reason)`：比对 `meta.schema_version` 与代码常量，
    并用 `PRAGMA table_info(props)` 检测缺列 —— **这就是应用层版本管理 + 兼容检查**。
  * 唯一真实 gap：`PRAGMA user_version` 当前为 **0**（标准 SQLite 版本机制未用），
    属**低严重度建议**（标准工具看不到版本；但应用层已能拒绝不兼容旧库）。

本测试集目的：锁定"应用层版本管理存在且有效"，并锁定 PRAGMA user_version
机制可用（为后续把版本同步进 PRAGMA 留好最小改动点）。
"""
from __future__ import annotations

import importlib.util
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

DB = os.path.join(ROOT, "data", "propositions.db")


def _load():
    spec = importlib.util.spec_from_file_location("prop_graph_671e", os.path.join(TOOLS, "prop_graph.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


pg = _load()


def _fresh_db_with(schema_sql: str, meta_version: str) -> str:
    import tempfile
    import pathlib
    p = pathlib.Path(tempfile.mkdtemp()) / "t.db"
    con = sqlite3.connect(str(p))
    con.executescript(schema_sql)
    con.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)", (meta_version,))
    con.commit()
    con.close()
    return str(p)


def test_current_db_user_version_is_zero_documents_gap():
    """锁定当前真实状态：PRAGMA user_version == 0（低严重度 gap，标准机制未用）。"""
    con = sqlite3.connect(DB)
    uv = con.execute("PRAGMA user_version").fetchone()[0]
    con.close()
    assert uv == 0


def test_current_db_meta_schema_version_matches_code():
    con = sqlite3.connect(DB)
    row = con.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
    con.close()
    assert row is not None
    assert row[0] == pg.SCHEMA_VERSION


def test_needs_rebuild_returns_false_for_current_real_db():
    """对当前真实库：`_needs_rebuild` 应判定为无需重建（版本与列都匹配）。只读，无副作用。"""
    needs, reason = pg._needs_rebuild(DB)
    assert needs is False, f"当前库应判定为最新，但得到：{reason}"


def test_needs_rebuild_detects_version_mismatch():
    """版本不一致 ⇒ 必须判定需要重建（应用层版本管理有效）。"""
    p = _fresh_db_with(pg.SCHEMA, "1")   # 代码期望 "2"
    needs, reason = pg._needs_rebuild(p)
    assert needs is True
    assert "schema_version" in reason and "≠" in reason


def test_needs_rebuild_detects_missing_column():
    """props 缺列 ⇒ 必须判定需要重建。"""
    schema = ("CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);"
              "CREATE TABLE props(prop_key TEXT PRIMARY KEY);"
              "CREATE TABLE prop_evidence(prop_key TEXT, evidence_id TEXT);")
    p = _fresh_db_with(schema, pg.SCHEMA_VERSION)
    needs, reason = pg._needs_rebuild(p)
    assert needs is True
    assert "缺列" in reason or "props" in reason


def test_needs_rebuild_ok_when_current_schema_and_version():
    """完整 schema + 正确版本 ⇒ 无需重建。"""
    p = _fresh_db_with(pg.SCHEMA, pg.SCHEMA_VERSION)
    needs, reason = pg._needs_rebuild(p)
    assert needs is False, reason


def test_pragma_user_version_round_trip_is_viable_fix():
    """锁定推荐的最小修复（把版本同步进 PRAGMA user_version）是可行且低风险的：
    在临时库上设置/读回 PRAGMA user_version 应一致。后续批次可让 prop_graph 在建库后
    `conn.execute("PRAGMA user_version = <SCHEMA_VERSION>")` 并加一组开库校验。"""
    import tempfile
    import pathlib
    p = pathlib.Path(tempfile.mkdtemp()) / "uv.db"
    con = sqlite3.connect(str(p))
    con.execute("PRAGMA user_version = 2")
    con.commit()
    got = con.execute("PRAGMA user_version").fetchone()[0]
    con.close()
    assert got == 2
