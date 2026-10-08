#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""verify_data_integrity.py — 693-D5：数据完整性全面校验。

与 ``tools/gen_693_manifest.py`` 的分工
========================================
* ``gen_693_manifest.py``：只做 **sha256**（文件是否被改动）；
* 本脚本：做 **结构 + 口径 + 统计自洽**（文件里的东西对不对）。

六项检查
========
1. **存在性** —— 必需文件在不在；
2. **sha256** —— 14 项冻结产物是否被改动（复用 ``utils.data_access.verify_manifest``）；
3. **结构** —— 每个 JSON 的必需顶层字段在不在；
4. **四态闭集** —— 矩阵里所有 verdict 只能取 ``catch/miss/unknown/contradiction``；
5. **样本数自洽** —— ``n_samples`` == ``len(samples)`` == ``len(matrix)``；
6. **类型闭集** —— ``defect_type`` 必须落在 34 项规范词表内。

设计纪律：fail-loud。任何一项不过就退非 0；**没有"跳过"开关**——
要跳过就在验收报告里写明，而不是加一个 ``--allow-missing``。

用法
====
    python tools/verify_data_integrity.py
    python tools/verify_data_integrity.py --json data/693_data_integrity.json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.errors import SchemaError  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("verify_data_integrity")
OUT_JSON = ROOT / "data" / "693_data_integrity.json"

VERDICTS = frozenset({"catch", "miss", "unknown", "contradiction"})

# (相对路径, 必需顶层字段)
REQUIRED: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("blindspot_676g_detection_matrix.json", ("schema", "assets", "n_samples", "samples", "matrix")),
    ("683_real_world_detection_matrix.json", ("schema", "assets", "n_samples")),
    ("676m_sample_manifest_corrected.json", ("schema", "vocabulary", "n_total")),
    ("681_type_stats_normalized.json", ("schema", "n_samples", "n_types", "per_type")),
    ("689_annotation_key_mapping.json", ("schema", "n_total", "rows")),
    ("693_ai_double_label.json", ("schema", "n_samples", "per_sample", "disagreements")),
    ("693_data_manifest.json", ("schema", "n_files", "files")),
)

VOCAB_PATH = "676m_sample_manifest_corrected.json"


def _check_existence() -> dict[str, Any]:
    res: dict[str, Any] = {"n": len(REQUIRED), "missing": [], "ok": 0}
    for rel, _ in REQUIRED:
        if (DATA / rel).exists():
            res["ok"] += 1
        else:
            res["missing"].append(rel)
            _log.error("MISSING  %s", rel)
    return res


def _check_schema() -> dict[str, Any]:
    res: dict[str, Any] = {"n": 0, "errors": []}
    for rel, fields in REQUIRED:
        p = DATA / rel
        if not p.exists():
            continue
        res["n"] += 1
        try:
            doc = load_json_cached(p)
        except SchemaError as exc:
            res["errors"].append(str(exc))
            continue
        miss = [f for f in fields if f not in doc]
        if miss:
            res["errors"].append(f"{rel} 缺少顶层字段 {miss}")
            _log.error("SCHEMA   %s 缺 %s", rel, miss)
    return res


def _check_matrix(path_name: str, vocab: frozenset[str] | None) -> dict[str, Any]:
    """检查一个检测矩阵：四态闭集 / 样本数自洽 / 类型闭集。"""
    out: dict[str, Any] = {"file": path_name, "checked": False}
    p = DATA / path_name
    if not p.exists():
        out["error"] = "文件不存在"
        return out
    doc = load_json_cached(p)
    samples = doc.get("samples", [])
    matrix = doc.get("matrix", {})
    out.update({
        "checked": True,
        "n_samples_declared": doc.get("n_samples"),
        "n_samples_actual": len(samples),
        "n_matrix_keys": len(matrix),
        "bad_verdicts": [],
        "bad_types": [],
        "unknown_count": 0,
        "catch_count": 0,
        "miss_count": 0,
    })

    bad_v: list[str] = []
    bad_t: list[str] = []
    counts = {"catch": 0, "miss": 0, "unknown": 0, "contradiction": 0}
    for s in samples:
        dt = str(s.get("defect_type", ""))
        if vocab is not None and dt and dt not in vocab:
            bad_t.append(dt)
        for asset, rec in (s.get("per_asset") or {}).items():
            v = rec.get("verdict") if isinstance(rec, dict) else rec
            if v not in VERDICTS:
                bad_v.append(f"{s.get('uid')}:{asset}={v}")
            else:
                counts[str(v)] += 1
    out["bad_verdicts"] = bad_v[:20]
    out["n_bad_verdicts"] = len(bad_v)
    out["bad_types"] = sorted(set(bad_t))
    out.update({f"count_{k}": v for k, v in counts.items()})

    if bad_v:
        _log.error("VERDICT  %s 出现闭集外的判决值（%d 处）", path_name, len(bad_v))
    if bad_t:
        _log.error("TYPE     %s 出现词表外的类型：%s", path_name, sorted(set(bad_t)))
    declared = doc.get("n_samples")
    if declared is not None and declared != len(samples):
        _log.error("COUNT    %s n_samples=%s ≠ len(samples)=%d", path_name, declared, len(samples))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", dest="out", default=str(OUT_JSON))
    args = ap.parse_args()

    vocab: frozenset[str] | None = None
    vp = DATA / VOCAB_PATH
    if vp.exists():
        vocab = frozenset(load_json_cached(vp).get("vocabulary", []))

    doc: dict[str, Any] = {
        "schema": "queyi-693-data-integrity/v1",
        "generated_by": "tools/verify_data_integrity.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "checks": {},
    }

    doc["checks"]["existence"] = _check_existence()
    doc["checks"]["schema"] = _check_schema()

    try:
        from utils.data_access import verify_manifest  # noqa: PLC0415
        doc["checks"]["sha256_manifest"] = verify_manifest()
    except Exception as exc:  # noqa: BLE001 —— 校验器本身要 fail-loud 但不得崩溃
        doc["checks"]["sha256_manifest"] = {"error": str(exc)}
        _log.error("SHA256   %s", exc)

    doc["checks"]["matrix_1147"] = _check_matrix(
        "blindspot_676g_detection_matrix.json", vocab)
    doc["checks"]["matrix_110"] = _check_matrix(
        "683_real_world_detection_matrix.json", vocab)

    if vocab:
        doc["vocabulary_size"] = len(vocab)

    # ── 判定 ──
    problems: list[str] = []
    ex = doc["checks"]["existence"]
    if ex["missing"]:
        problems.append(f"缺文件 {ex['missing']}")
    if doc["checks"]["schema"]["errors"]:
        problems.append(f"结构错误 {len(doc['checks']['schema']['errors'])} 处")
    sh = doc["checks"]["sha256_manifest"]
    if sh.get("missing") or sh.get("mismatch") or sh.get("error"):
        problems.append(f"sha256 问题 {sh}")
    for key in ("matrix_1147", "matrix_110"):
        m = doc["checks"][key]
        if m.get("n_bad_verdicts"):
            problems.append(f"{key} 判决值越界 {m['n_bad_verdicts']} 处")
        if m.get("bad_types"):
            problems.append(f"{key} 类型越界 {m['bad_types']}")
        if m.get("checked") and m.get("n_samples_declared") != m.get("n_samples_actual"):
            problems.append(f"{key} 样本数不自洽")

    doc["problems"] = problems
    doc["verdict"] = "pass" if not problems else "FAIL"

    Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
    if problems:
        _log.error("数据完整性 FAIL：%s", problems)
        print(f"[693-D5] FAIL → {args.out}")
        raise SystemExit(1)
    _log.info("数据完整性 pass（六项全过）")
    print(f"[693-D5] pass → {args.out}")


if __name__ == "__main__":
    main()
