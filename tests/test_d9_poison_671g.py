# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D9：投毒检测 canary + 配对探针（8 条）。"""
from __future__ import annotations

import poison_detection_671g as P


def _detail(rows):
    return {"per_sample": [
        {"id": k, "verdict": (v.get("verdict") if isinstance(v, dict) else v),
         "detector": (v.get("detector", "asan") if isinstance(v, dict) else "asan")}
        for k, v in rows.items()]}


def test_real_canaries_hold():
    rep = P.evaluate(P.ROOT)
    assert rep["status"] == "pass" and rep["n_canaries"] == 5 and rep["n_pairs"] == 3


def test_canary_flipped_blocks():
    cfg = P.default_config()
    rows = {"h21": {"verdict": "miss", "detector": "ubsan"}}
    f = P.check_canaries(cfg, rows)
    assert f and f[0]["kind"] == "canary_flipped" and f[0]["severity"] == "block"


def test_canary_missing_blocks():
    cfg = P.default_config()
    f = P.check_canaries(cfg, {})
    assert any(x["kind"] == "canary_missing" for x in f)


def test_canary_detector_change_warns():
    cfg = P.default_config()
    rows = {"h21": {"verdict": "catch", "detector": "asan"}}   # 登记 ubsan
    f = P.check_canaries(cfg, rows)
    assert any(x["kind"] == "canary_detector_changed" and x["severity"] == "warn" for x in f)


def test_pair_inconsistent_blocks():
    cfg = P.default_config()
    rows = {"h22": {"verdict": "catch"}, "h23": {"verdict": "miss"},
            "h27": {"verdict": "catch"}, "h32": {"verdict": "catch"},
            "h25": {"verdict": "catch"}, "h30": {"verdict": "catch"}}
    f = P.check_pairs(cfg, rows)
    assert f and f[0]["kind"] == "pair_inconsistent" and f[0]["severity"] == "block"


def test_pair_consistent_passes():
    cfg = P.default_config()
    rows = {"h22": {"verdict": "catch"}, "h23": {"verdict": "catch"},
            "h27": {"verdict": "catch"}, "h32": {"verdict": "catch"},
            "h25": {"verdict": "catch"}, "h30": {"verdict": "catch"}}
    assert P.check_pairs(cfg, rows) == []


def test_pair_missing_blocks():
    cfg = P.default_config()
    assert P.check_pairs(cfg, {})[0]["kind"] == "pair_missing"


def test_unarmed_without_detail(tmp_path):
    rep = P.evaluate(tmp_path)
    assert rep["status"] == "unarmed" and rep["severity"] == "warn"


def test_evaluate_status():
    cfg = P.default_config()
    rows = {c["id"]: {"verdict": c["expected_verdict"], "detector": c["detector"]}
            for c in cfg["canaries"]}
    for pr in cfg["pairs"]:
        rows[pr["a"]] = {"verdict": "catch"}
        rows[pr["b"]] = {"verdict": "catch"}
    rep = P.evaluate(P.ROOT, cfg, _detail(rows))
    assert rep["status"] == "pass", rep["findings"]
