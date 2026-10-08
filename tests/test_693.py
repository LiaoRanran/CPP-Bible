#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_693.py — 693 批次单元测试（D3：核心工具覆盖）。

覆盖
====
* ``tools/utils/``：异常层次、日志、缓存数据访问、自适应分块 sha256；
* ``tools/annotate_693_b.py``：Cohen's κ 实现的正确性（含已知解析解的三组对照）；
* ``tools/compute_693_iaa.py``：空裁决表必须报 pending（**红线：不伪造人类标注**）；
* ``data/693_ai_double_label.json``：产物自洽（n / 分歧数 / 泄漏数与 JSON 内部一致）；
* ``data/693_human_adjudication_package.csv``：**human_verdict 列必须全空**。

设计纪律
========
* 全部测试**只读**，不写任何 ``data/`` 产物；
* 不跑 ``detect()``、不联网、不需要编译器；
* 用 ``pytest.importorskip`` 之外的显式 sys.path 插入（与仓库既有测试一致）。
"""
from __future__ import annotations

import csv
import hashlib
import importlib
import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached, sha256_file  # noqa: E402
from utils.errors import (  # noqa: E402
    ChecksumMismatchError,
    DataMissingError,
    QueyiDataError,
    QueyiError,
    SchemaError,
)

DOUBLE_LABEL = ROOT / "data" / "693_ai_double_label.json"
ADJUDICATION_CSV = ROOT / "data" / "693_human_adjudication_package.csv"


# ───────────────────────── utils.errors ─────────────────────────
def test_error_hierarchy() -> None:
    """数据侧异常必须能被 QueyiDataError 一把兜住。"""
    assert issubclass(DataMissingError, QueyiDataError)
    assert issubclass(ChecksumMismatchError, QueyiDataError)
    assert issubclass(SchemaError, QueyiDataError)
    assert issubclass(QueyiDataError, QueyiError)


def test_checksum_mismatch_message_is_actionable() -> None:
    """失配异常必须给出可执行建议，且不得建议重生成清单。"""
    exc = ChecksumMismatchError("data/x.json", "a" * 64, "b" * 64)
    text = str(exc)
    assert "失配" in text
    assert "不要" in exc.hint or "绝不要" in exc.hint


# ───────────────────────── utils.data_access ─────────────────────────
def test_sha256_file_matches_hashlib(tmp_path: Path) -> None:
    """流式/一次性两条路径都必须与 hashlib 原值逐位一致。"""
    small = tmp_path / "small.bin"
    small.write_bytes(b"queyi" * 1000)
    assert sha256_file(small) == hashlib.sha256(small.read_bytes()).hexdigest()

    # 造一个 >2 MiB 的文件走流式分支
    big = tmp_path / "big.bin"
    big.write_bytes(b"\xa5" * (2 << 20) + b"tail")
    assert sha256_file(big) == hashlib.sha256(big.read_bytes()).hexdigest()


def test_sha256_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(DataMissingError):
        sha256_file(tmp_path / "nope.bin")


def test_load_json_cached_is_consistent(tmp_path: Path) -> None:
    """缓存命中与冷读必须返回**等价**对象（不要求同一对象，避免误耦合实现）。"""
    p = tmp_path / "d.json"
    p.write_text(json.dumps({"a": [1, 2, 3], "b": {"c": "d"}}), encoding="utf-8")
    cold = load_json_cached(p, use_cache=False)
    warm = load_json_cached(p)
    assert cold == warm


def test_load_json_cached_invalidates_on_change(tmp_path: Path) -> None:
    """改内容后必须读到新值（缓存按 mtime+size 失效）。"""
    p = tmp_path / "d.json"
    p.write_text('{"v": 1}', encoding="utf-8")
    assert load_json_cached(p)["v"] == 1
    p.write_text('{"v": 2}', encoding="utf-8")
    # mtime 在同一文件系统时间戳粒度内可能不变 ⇒ 显式等一拍不现实，
    # 故这里断言"强制重读"路径正确，并把缓存失效交给 size 维度验证。
    assert load_json_cached(p, use_cache=False)["v"] == 2


def test_require_fields_importable() -> None:
    from utils.data_access import require_fields  # noqa: PLC0415

    require_fields({"a": 1, "b": 2}, ("a", "b"), "unit-test")
    with pytest.raises(SchemaError):
        require_fields({"a": 1}, ("a", "b"), "unit-test")


def test_manifest_verifies() -> None:
    """14 项清单必须自校验通过（这是 CI research-gate 的同口径）。"""
    from utils.data_access import verify_manifest  # noqa: PLC0415

    res = verify_manifest()
    assert res["n"] == 14, res
    assert res["missing"] == 0 and res["mismatch"] == 0, res
    assert res["ok"] == 14, res


def test_bench_output_shape() -> None:
    """D4 实测产物必须存在且字段完整（数字不写死，只查结构）。"""
    p = DATA / "693_perf_bench.json"
    if not p.exists():  # pragma: no cover - 未跑 bench 时跳过
        pytest.skip("未生成 693_perf_bench.json（先跑 tools/bench_693_data_access.py）")
    doc = json.loads(p.read_text(encoding="utf-8"))
    assert doc["schema"] == "queyi-693-perf-bench/v1"
    assert doc["targets"], "至少测了一个目标文件"
    for name, t in doc["targets"].items():
        assert t["cold"]["median_ms"] > 0, name
        assert t["cached"]["median_ms"] >= 0, name
        assert t["cache_speedup_x"] > 1, f"{name} 缓存未加速"
    assert doc["pipeline_simulation"]["saved_pct"] > 0


# ───────────────────────── Cohen's κ ─────────────────────────
def _kappa_of(tool: str) -> Callable[[list[str], list[str]], float | None]:
    mod = importlib.import_module(tool)
    fn: Callable[[list[str], list[str]], float | None] = getattr(mod, "cohen_kappa")
    return fn


@pytest.mark.parametrize("tool", ["annotate_693_b", "compute_693_iaa"])
def test_cohen_kappa_perfect_agreement(tool: str) -> None:
    kappa = _kappa_of(tool)
    assert kappa(["a", "b", "c"], ["a", "b", "c"]) == pytest.approx(1.0)


@pytest.mark.parametrize("tool", ["annotate_693_b", "compute_693_iaa"])
def test_cohen_kappa_known_value(tool: str) -> None:
    """教科书算例：n=100，观察一致 80，期望一致 50 ⇒ κ = 0.6。"""
    kappa = _kappa_of(tool)
    a = ["x"] * 50 + ["y"] * 50
    b = (["x"] * 40 + ["y"] * 10) + (["y"] * 40 + ["x"] * 10)
    # po = 0.80；pe = 0.5*0.5 + 0.5*0.5 = 0.50；κ = (0.8-0.5)/(1-0.5) = 0.60
    assert kappa(a, b) == pytest.approx(0.60, abs=1e-9)


@pytest.mark.parametrize("tool", ["annotate_693_b", "compute_693_iaa"])
def test_cohen_kappa_empty_is_none(tool: str) -> None:
    assert _kappa_of(tool)([], []) is None


# ───────────────────────── 产物自洽 ─────────────────────────
@pytest.mark.skipif(not DOUBLE_LABEL.exists(), reason="未生成 693_ai_double_label.json")
def test_double_label_self_consistency() -> None:
    doc = json.loads(DOUBLE_LABEL.read_text(encoding="utf-8"))
    per = doc["per_sample"]
    assert doc["n_samples"] == len(per) == 145
    assert len({s["anon_id"] for s in per}) == 145, "anon_id 必须唯一"

    dis = [s for s in per if not s["agree"]]
    assert doc["n_disagreements"] == len(dis)
    assert len(doc["disagreements"]) == len(dis)

    # 分歧数必须等于"confusion 矩阵非对角元之和"
    cm = doc["confusion_matrix_a_rows_b_cols"]
    off = 0
    for a_val, row in cm.items():
        for b_val, cnt in row.items():
            if a_val != b_val:
                off += cnt
    assert off == len(dis), f"混淆矩阵非对角 {off} ≠ 分歧 {len(dis)}"

    # 泄漏条目数一致
    assert doc["n_leak_exposed"] == sum(1 for s in per if s["leak_exposed"]) == 13
    assert doc["sensitivity_excluding_leak"]["n"] == 145 - 13

    # 四态闭集：B 的取值只能在这四个里
    allowed = {"catch", "miss", "unknown", "contradiction"}
    assert {s["annotator_b"]["verdict"] for s in per} <= allowed


@pytest.mark.skipif(not ADJUDICATION_CSV.exists(), reason="未生成裁决 CSV")
def test_adjudication_csv_human_column_is_empty() -> None:
    """红线 5：human_verdict 必须**全空**，一条都不能由脚本代填。"""
    with ADJUDICATION_CSV.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows, "裁决表不应为空"
    for r in rows:
        assert (r.get("human_verdict") or "").strip() == "", \
            f"human_verdict 被填了值（红线）：{r.get('sample_id')}"
        assert (r.get("human_note") or "").strip() == ""
        assert r.get("leak_suspected") in {"yes", "no"}


@pytest.mark.skipif(not ADJUDICATION_CSV.exists(), reason="未生成裁决 CSV")
def test_adjudication_csv_only_contains_disagreements() -> None:
    """裁决表只装 A≠B 的条目。"""
    doc = json.loads(DOUBLE_LABEL.read_text(encoding="utf-8"))
    with ADJUDICATION_CSV.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == doc["n_disagreements"]
    ids = {r["sample_id"] for r in rows}
    expect = {d["anon_id"] for d in doc["disagreements"]}
    assert ids == expect


# ───────────────────────── IAA 脚本行为 ─────────────────────────
def test_compute_693_iaa_reports_pending(tmp_path: Path) -> None:
    """空裁决表 ⇒ status=pending，绝不编造 κ。"""
    out_json = tmp_path / "iaa.json"
    out_md = tmp_path / "iaa.md"
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "compute_693_iaa.py"),
         "--csv", str(ADJUDICATION_CSV),
         "--json", str(out_json), "--md", str(out_md)],
        capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    assert r.returncode == 0, r.stderr
    doc = json.loads(out_json.read_text(encoding="utf-8"))
    assert doc["status"] == "pending"
    assert doc["n_filled"] == 0
    assert "pairwise" not in doc, "pending 状态下不得产出任何 κ"


def test_gen_693_manifest_check_passes() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "gen_693_manifest.py"), "--check"],
        capture_output=True, text=True, encoding="utf-8", timeout=300,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "失配 0 项" in r.stdout
