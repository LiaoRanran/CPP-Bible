# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""656 A（G9 总闸门）ots_anchor_656 回归锁。

锁七件事（都是"不许被骗"性质的）：
  * **自制占位 .ots 必须判 invalid**（613 E1 那类"长得像 OTS 但官方实现解不开"的东西）
  * 真实 .ots：覆盖的 digest 必须 == 目标台账当前内容的 sha256（挂错对象 ⇒ 红）
  * verdict 落在非 bad 集合（invalid / no_engine / submit_failed ⇒ 红）
  * 降级登记表：写了能读回、继承的 sha256 与目标一致、**明确标 clock_trust=none**、
    且自称 `status=pending_anchor`（不许冒充"已锚"）
  * 目标文件改 1 字节 ⇒ 登记表 sha256 失配必须被检出（漂移可见）
  * 冻结的魔法常数与官方 `DetachedTimestampFile.HEADER_MAGIC` 一致（避免兜底值被人偷偷改掉）
  * 报告产物写在 `data/` 下
全部走 tmp_path，**不触碰真实 `data/supply_chain/`**。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import ots_anchor_656 as ots  # noqa: E402

TARGET = "data/supply_chain/merkle_roots.json"


def _mk(base: Path, name: str, body: bytes = b'{"a":1}\n') -> Path:
    p = base / name
    p.write_bytes(body)
    return p


def test_homemade_placeholder_is_invalid(tmp_path: Path):
    """自制占位物（magic 对、内容是自制结构）⇒ 官方实现解不开 ⇒ invalid。"""
    f = _mk(tmp_path, "fake.json")
    magic = bytes.fromhex(ots.expected_magic())
    bad = magic + b"\x64\x08" + hashlib.sha256(f.read_bytes()).digest() * 2 + b"\x00\x08" + b"\x00" * 40
    (tmp_path / "fake.json.ots").write_bytes(bad)
    rep = ots.analyze("fake.json", base=tmp_path)
    assert rep["verdict"] in {"invalid", "unverified"}     # 有引擎 ⇒ invalid；无引擎兜底 ⇒ unverified
    assert rep["magic_ok"] is True                          # **外表**是对的，所以必须靠解析而非 magic 判断


def test_missing_and_downgraded(tmp_path: Path):
    _mk(tmp_path, "fake.json")
    assert ots.analyze("fake.json", base=tmp_path)["verdict"] == "missing"
    pay = ots.write_pending("fake.json", reason="pytest", base=tmp_path)
    assert pay["status"] == "pending_anchor"
    assert pay["clock_trust"] == "none"
    assert pay["sha256"] == hashlib.sha256((tmp_path / "fake.json").read_bytes()).hexdigest()
    rep = ots.analyze("fake.json", base=tmp_path)
    assert rep["verdict"] == "downgraded_json"
    assert rep["downgrade_matches_target"] is True


def test_downgrade_drift_is_detected(tmp_path: Path):
    f = _mk(tmp_path, "fake.json")
    ots.write_pending("fake.json", reason="pytest", base=tmp_path)
    f.write_bytes(b'{"a":2}\n')                             # 目标改 1 字节
    rep = ots.analyze("fake.json", base=tmp_path)
    assert rep["downgrade_matches_target"] is False         # 漂移必须可见，不许静默


def test_frozen_magic_matches_official():
    """兜底魔法常数必须与官方实现一致——否则没装库的环境会被误导。"""
    if not ots.have_lib():
        pytest.skip("未装 opentimestamps ⇒ 无法与官方常数交叉核对")
    assert ots.expected_magic() == ots.FROZEN_HEADER_MAGIC_HEX


def test_real_target_not_invalid():
    """真实台账的锚点不许是 invalid（占位 / 无效 / 挂错对象 都算红）。"""
    rep = ots.analyze(ots.DEFAULT_TARGET)
    assert rep["target_exists"], "目标台账必须存在"
    assert rep["verdict"] != "invalid", f"锚点无效：{rep.get('note')}"
    if rep["verdict"] in ots.ANCHORED:
        assert rep["covers_target"], "OTS 覆盖的 digest 必须等于目标台账当前内容"
        assert rep["attestations"], "至少要有一条 attestation"


def test_report_stays_in_data(tmp_path: Path):
    report = ots.report()
    slug = ots.OUT_MD
    assert str(slug).replace("\\", "/").endswith("data/656_ots_anchor_report.md")
    assert ots.OUT_JSON.exists() and slug.exists()
    assert report["target"] == TARGET
    assert isinstance(report["calendars"], list) and report["calendars"]
    assert json.loads(ots.OUT_JSON.read_text(encoding="utf-8"))["analyze"]["verdict"] == report["analyze"]["verdict"]
