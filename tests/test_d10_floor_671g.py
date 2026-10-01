# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D10：标注地板检查（5 条）。"""
from __future__ import annotations

import json

import trajectory_floor_check_671g as F


def _batch(n, errors, seed=1):
    labels = [{"id": i, "label": "x"} for i in range(n)]
    reviewed = []
    sample = F.pick_sample(n, 10, seed)
    for j, i in enumerate(sample):
        reviewed.append({"id": i, "label": "x", "truth": "y", "error": j < errors})
    return {"batch_id": "b1", "labels": labels, "review": {"seed": seed, "reviewed": reviewed}}


def test_floor_pass():
    r = F.evaluate(_batch(50, 2))   # 2/10 = 20% 正好不超
    assert r["status"] == "pass" and r["error_rate"] == 0.2


def test_floor_block_whole_batch():
    r = F.evaluate(_batch(50, 3))   # 30% > 20%
    assert r["status"] == "block" and "全部重标" in r["action"]


def test_inconclusive_no_review():
    batch = {"batch_id": "b", "labels": [{"id": 0}], "review": {}}
    r = F.evaluate(batch)
    assert r["status"] == "inconclusive"


def test_sample_deterministic():
    a = F.pick_sample(50, 10, seed=123)
    b = F.pick_sample(50, 10, seed=123)
    assert a == b and len(a) == 10 and len(set(a)) == 10
    assert len(F.pick_sample(5, 10, seed=1)) == 5


def test_check_unarmed_and_clean(tmp_path):
    assert F.check(tmp_path)[0]["severity"] == "warn"
    d = tmp_path / "data" / "671g" / "labels"
    d.mkdir(parents=True)
    (d / "b.json").write_text(json.dumps(_batch(20, 1)), encoding="utf-8")
    f = F.check(tmp_path)
    assert [x for x in f if x["severity"] == "block"] == []
