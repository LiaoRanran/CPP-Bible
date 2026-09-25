"""640 A5 · conftest 会话清理器安全化单测（≥6 例）。

直接测根级 conftest 的分类/日志逻辑（不整会话跑）：
  1. tracked 文件永不删；
  2. 豁免名单（批次产物模式）不删；
  3. 临时产物（.tmp/probe/canary）删；
  4. 非临时未跟踪文件保守保留；
  5. 处置全部留痕 _auto/cleanup_log.jsonl；
  6. _restore 返回 (restored, deleted, kept) 三元组。
"""
from __future__ import annotations

import importlib.util
import json
import os

_SPEC = importlib.util.spec_from_file_location(
    "root_conftest", os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "conftest.py"))
CT = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(CT)  # type: ignore[union-attr]


def test_tracked_file_never_deleted(tmp_path):
    p = tmp_path / "data_x.md"
    p.write_text("new", encoding="utf-8")
    tracked = {os.path.normpath(str(p))}
    do_del, reason = CT._classify_new(str(p), tracked)
    assert do_del is False and "tracked" in reason


def test_keep_list_batch_artifacts_not_deleted(tmp_path):
    p = tmp_path / "640_some_report.md"
    p.write_text("x", encoding="utf-8")
    do_del, reason = CT._classify_new(str(p), set())
    assert do_del is False and "豁免" in reason


def test_temp_artifacts_deleted(tmp_path):
    for name in ("640_probe_del.tmp", "canary_x.txt", "probe_y.md"):
        p = tmp_path / name
        p.write_text("x", encoding="utf-8")
        do_del, reason = CT._classify_new(str(p), set())
        assert do_del is True, (name, reason)


def test_unknown_new_file_conservative_keep(tmp_path):
    p = tmp_path / "mystery_blob.bin"
    p.write_text("x", encoding="utf-8")
    do_del, reason = CT._classify_new(str(p), set())
    assert do_del is False and "保守" in reason


def test_restore_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setattr(CT, "CLEANUP_LOG", str(tmp_path / "cleanup_log.jsonl"))
    gone = tmp_path / "640_probe_del.tmp"        # 应删
    kept = tmp_path / "640_keep_report.md"       # 应留（豁免名单）
    snap = CT._snapshot(str(tmp_path))           # 先取快照（此时两者尚不存在）
    gone.write_text("x", encoding="utf-8")
    kept.write_text("x", encoding="utf-8")
    restored, deleted, keptn = CT._restore(snap, base=str(tmp_path), tracked=set())
    assert deleted == 1 and not gone.exists()
    assert keptn == 1 and kept.exists()
    log = [json.loads(ln) for ln in
           open(tmp_path / "cleanup_log.jsonl", encoding="utf-8") if ln.strip()]
    actions = {e["action"] for e in log}
    assert actions == {"deleted", "kept"}
    assert all("path" in e and "reason" in e and "ts" in e for e in log)


def test_snapshot_restore_roundtrip(tmp_path):
    p = tmp_path / "data_a.md"
    p.write_text("v1", encoding="utf-8")
    snap = CT._snapshot(str(tmp_path))
    p.write_text("v2-changed", encoding="utf-8")
    restored, _d, _k = CT._restore(snap, base=str(tmp_path), tracked=set())
    assert restored == 1 and p.read_text(encoding="utf-8") == "v1"
