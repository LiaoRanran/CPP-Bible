"""634 A1 · 生产 data/ 写隔离单测（纯标准库，≥5 例）。编号 A1-1..A1-6。

直接加载根级 `conftest.py` 的助手函数，在 tmp 目录上验证（不碰真实 data/）。
"""
from __future__ import annotations

import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("root_conftest_634", os.path.join(_ROOT, "conftest.py"))
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


# A1-1：快照记录现存文件字节
def test_snapshot_captures(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"hello")
    snap = m._snapshot(str(tmp_path))
    assert snap[str(tmp_path / "a.txt")] == b"hello"


# A1-2：还原被改文件
def test_restore_modified(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"orig")
    snap = m._snapshot(str(tmp_path))
    p.write_bytes(b"changed")
    restored, deleted = m._restore(snap, str(tmp_path))
    assert p.read_bytes() == b"orig" and restored == 1


# A1-3：删除新建文件
def test_restore_deletes_new(tmp_path):
    snap = m._snapshot(str(tmp_path))
    (tmp_path / "new.txt").write_bytes(b"x")
    _restored, deleted = m._restore(snap, str(tmp_path))
    assert not (tmp_path / "new.txt").exists() and deleted == 1


# A1-4：未改动文件不动（restored/deleted 均为 0）
def test_restore_noop(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"same")
    snap = m._snapshot(str(tmp_path))
    restored, deleted = m._restore(snap, str(tmp_path))
    assert restored == 0 and deleted == 0


# A1-5：大文件只记存在（None）不整读
def test_big_file_presence_only(tmp_path):
    big = tmp_path / "big.bin"
    big.write_bytes(b"0" * (m._MAX_SNAPSHOT_BYTES + 1))
    snap = m._snapshot(str(tmp_path))
    assert snap[str(big)] is None


# A1-6：autouse 会话 fixture 已注册
def test_fixture_registered():
    assert hasattr(m, "_isolate_production_data")
