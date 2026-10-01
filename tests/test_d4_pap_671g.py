# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D4：PAP 预注册（8 条红绿路径）。"""
from __future__ import annotations

import json

import pap_register_671g as P


def _pap(**over):
    p = P.scaffold("b1")
    p.update({f: "x" for f in P.REQUIRED_FIELDS})
    p["alpha"] = 0.05
    p["experiment_start"] = ""
    p.update(over)
    return p


def test_complete_pap_valid():
    assert P.validate(_pap()) == []


def test_missing_field_blocked():
    p = _pap()
    del p["sample_size"]
    assert any("sample_size" in x for x in P.validate(p))


def test_alpha_bounds():
    assert any("alpha" in x for x in P.validate(_pap(alpha=1.5)))
    assert any("alpha" in x for x in P.validate(_pap(alpha="abc")))


def test_alpha_na_requires_descriptive_method():
    bad = _pap(alpha="不适用", statistical_method="假设检验 p 值")
    assert any("纯描述" in x for x in P.validate(bad))
    ok = _pap(alpha="不适用（只报 CP 区间）", statistical_method="Clopper-Pearson 区间")
    assert P.validate(ok) == []


def test_posthoc_requires_note():
    p = _pap(registration_type="posthoc")
    assert any("posthoc_note" in x for x in P.validate(p))
    p["posthoc_note"] = "实验后补"
    assert P.validate(p) == []


def test_preregister_after_start_blocked():
    p = _pap(registered_at="2026-10-01", experiment_start="2026-09-20")
    assert any("晚于实验开始" in x for x in P.validate(p))


def test_require_without_pap_blocks(tmp_path):
    d = tmp_path / "data" / "671g" / "pap"
    d.mkdir(parents=True)
    (d / "registry.json").write_text(json.dumps(
        {"require": ["exp-x"], "pap_files": {"exp-x": "pap_x.json"}}), encoding="utf-8")
    f = P.check(tmp_path)
    assert any("exp-x" in x["target"] for x in f)


def test_require_with_pap_passes(tmp_path):
    d = tmp_path / "data" / "671g" / "pap"
    d.mkdir(parents=True)
    p = _pap()
    p["batch_id"] = "exp-x"
    (d / "pap_exp-x.json").write_text(json.dumps(p), encoding="utf-8")
    (d / "registry.json").write_text(json.dumps(
        {"require": ["exp-x"], "pap_files": {"exp-x": "exp-x"}}, ensure_ascii=False),
        encoding="utf-8")
    assert P.check(tmp_path) == []


def test_real_registry_valid():
    assert P.check(P.ROOT) == []
