# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_queyi_common_696.py — 696 批次：``tools/queyi_common.py`` 单元测试。

覆盖点（对应 696 交付物 5）：
* 异常层次继承关系（QueyiError 基类 + GateError / DataIntegrityError / SchemaError）；
* ``setup_logging`` 配置**幂等**（多次调用只留一个本库 handler，级别正确）；
* ``read_json`` 正常 / 缺文件 / 非法 JSON / 顶层非对象四条路径；
* ``sha256_file`` 已知向量（``b"abc"``）+ 空文件 + 缺文件；
* ``atomic_write_text`` 往返 + 覆盖写 + 不留临时残骸。

说明：本仓 CI 用 ``mypy tools/``（不检查 tests/）；本文件类型检查用
``MYPYPATH=tools mypy tests/test_queyi_common_696.py``（见 696 工程报告）。
"""
from __future__ import annotations

import hashlib
import json
import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import queyi_common as qc  # noqa: E402

#: ``b"abc"`` 的 sha256（NIST 常用测试向量）
ABC_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


# ── 异常层次 ────────────────────────────────────────────────────────────────
def test_exception_hierarchy() -> None:
    assert issubclass(qc.QueyiError, Exception)
    assert issubclass(qc.GateError, qc.QueyiError)
    assert issubclass(qc.DataIntegrityError, qc.QueyiError)
    assert issubclass(qc.SchemaError, qc.DataIntegrityError)
    assert issubclass(qc.SchemaError, qc.QueyiError)


def test_exception_str_with_and_without_hint() -> None:
    assert str(qc.QueyiError("boom")) == "boom"
    rendered = str(qc.QueyiError("boom", "run X"))
    assert "boom" in rendered and "run X" in rendered


def test_base_exception_catches_all_subclasses() -> None:
    for exc_type in (qc.GateError, qc.DataIntegrityError, qc.SchemaError):
        with pytest.raises(qc.QueyiError):
            raise exc_type("x")


# ── setup_logging ───────────────────────────────────────────────────────────
def test_setup_logging_idempotent() -> None:
    qc.setup_logging("DEBUG")
    qc.setup_logging(logging.WARNING)
    qc.setup_logging(logging.INFO)

    root = logging.getLogger()
    ours = [h for h in root.handlers if isinstance(h, qc._QueyiStreamHandler)]
    assert len(ours) == 1, f"幂等失败：本库 handler 应恰为 1，实际 {len(ours)}"
    assert root.level == logging.INFO


def test_setup_logging_accepts_int_and_str() -> None:
    assert qc._coerce_level(logging.ERROR) == logging.ERROR
    assert qc._coerce_level("debug") == logging.DEBUG
    assert qc._coerce_level("not-a-level") == logging.INFO


# ── read_json ───────────────────────────────────────────────────────────────
def test_read_json_ok(tmp_path: Path) -> None:
    p = tmp_path / "ok.json"
    p.write_text(json.dumps({"k": 1, "nested": {"a": [1, 2]}}), encoding="utf-8")
    assert qc.read_json(p) == {"k": 1, "nested": {"a": [1, 2]}}


def test_read_json_accepts_str_path(tmp_path: Path) -> None:
    p = tmp_path / "ok.json"
    p.write_text('{"x": true}', encoding="utf-8")
    assert qc.read_json(str(p)) == {"x": True}


def test_read_json_missing_raises_data_integrity(tmp_path: Path) -> None:
    with pytest.raises(qc.DataIntegrityError):
        qc.read_json(tmp_path / "nope.json")


def test_read_json_invalid_raises_schema_error(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(qc.SchemaError):
        qc.read_json(p)


def test_read_json_non_object_raises_schema_error(tmp_path: Path) -> None:
    p = tmp_path / "arr.json"
    p.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(qc.SchemaError):
        qc.read_json(p)


# ── sha256_file ─────────────────────────────────────────────────────────────
def test_sha256_known_vector(tmp_path: Path) -> None:
    p = tmp_path / "abc.txt"
    p.write_bytes(b"abc")
    assert qc.sha256_file(p) == ABC_SHA256


def test_sha256_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "empty.bin"
    p.write_bytes(b"")
    assert qc.sha256_file(p) == hashlib.sha256(b"").hexdigest()


def test_sha256_missing_raises_data_integrity(tmp_path: Path) -> None:
    with pytest.raises(qc.DataIntegrityError):
        qc.sha256_file(tmp_path / "nope.bin")


# ── atomic_write_text ───────────────────────────────────────────────────────
def test_atomic_write_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "out.txt"
    returned = qc.atomic_write_text(p, "hello\nworld")
    assert returned == p
    assert p.read_text(encoding="utf-8") == "hello\nworld"


def test_atomic_write_overwrite(tmp_path: Path) -> None:
    p = tmp_path / "out.txt"
    qc.atomic_write_text(p, "old")
    qc.atomic_write_text(p, "new")
    assert p.read_text(encoding="utf-8") == "new"


def test_atomic_write_leaves_no_tmp_residue(tmp_path: Path) -> None:
    p = tmp_path / "out.txt"
    qc.atomic_write_text(p, "x")
    leftovers = sorted(f.name for f in tmp_path.iterdir() if f.name != "out.txt")
    assert leftovers == [], f"临时文件残骸：{leftovers}"
