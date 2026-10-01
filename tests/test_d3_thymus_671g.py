# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D3：误报率"胸腺"阴性选择（8 条）。"""
from __future__ import annotations

import json

import false_positive_thymus_671g as T


def _clean(root, n):
    d = root / "data" / "671g" / "thymus" / "clean"
    d.mkdir(parents=True)
    for i in range(n):
        (d / f"c{i}.cpp").write_text(f"// clean {i}\nint main(){{return 0;}}", encoding="utf-8")
    return d


def test_pass_low_fp(tmp_path):
    _clean(tmp_path, 10)
    # 10 个里 0 误报 ⇒ pass
    r = T.evaluate_rule(tmp_path, "R1", {}, checker=lambda p: False,
                       clean_files=sorted((tmp_path / "data/671g/thymus/clean").glob("*.cpp")))
    assert r["status"] == "pass" and r["false_positive"] == 0


def test_block_high_fp(tmp_path):
    _clean(tmp_path, 10)
    # 10 个里 1 误报 = 10% > 5% ⇒ block（胸腺不让发布）
    files = sorted((tmp_path / "data/671g/thymus/clean").glob("*.cpp"))
    def chk(p):
        return p.name == "c0.cpp"
    r = T.evaluate_rule(tmp_path, "R1", {}, checker=chk, clean_files=files)
    assert r["status"] == "block" and r["false_positive"] == 1


def test_five_pct_boundary(tmp_path):
    _clean(tmp_path, 20)
    files = sorted((tmp_path / "data/671g/thymus/clean").glob("*.cpp"))
    def chk(p):
        return p.name in ("c0.cpp",)       # 1/20 = 5% 正好不超
    r = T.evaluate_rule(tmp_path, "R1", {}, checker=chk, clean_files=files)
    assert r["status"] == "pass"


def test_inconclusive_small_sample(tmp_path):
    _clean(tmp_path, 3)
    r = T.evaluate_rule(tmp_path, "R1", {}, checker=lambda p: False,
                       clean_files=sorted((tmp_path / "data/671g/thymus/clean").glob("*.cpp")))
    assert r["status"] == "inconclusive" and r["severity"] == "warn"


def test_checker_exception_counts_as_fp(tmp_path):
    _clean(tmp_path, 10)
    files = sorted((tmp_path / "data/671g/thymus/clean").glob("*.cpp"))
    def boom(p):
        if p.name == "c0.cpp":
            raise RuntimeError("checker crashed on clean code")
        return False
    r = T.evaluate_rule(tmp_path, "R1", {}, checker=boom, clean_files=files)
    assert r["status"] == "block" and r["false_positive"] == 1


def test_evaluate_unarmed_when_no_rules(tmp_path):
    cfg_dir = tmp_path / "data" / "671g" / "thymus"
    cfg_dir.mkdir(parents=True)
    (cfg_dir / "config.json").write_text(json.dumps(
        {"threshold_pct": 5.0, "min_samples": 10, "rules": {}}), encoding="utf-8")
    out = T.evaluate(tmp_path)
    assert out[0]["status"] == "unarmed" and out[0]["severity"] == "warn"


def test_evaluate_registered_block(tmp_path):
    _clean(tmp_path, 10)
    cfg_dir = tmp_path / "data" / "671g" / "thymus"
    (cfg_dir / "config.json").write_text(json.dumps(
        {"threshold_pct": 5.0, "min_samples": 10,
         "rules": {"R1": {"checker": "", "files_glob": "*.cpp"}}}), encoding="utf-8")
    out = T.evaluate(tmp_path, checkers={"R1": lambda p: True})
    assert out[0]["status"] == "block" and out[0]["n_clean"] == 10


def test_real_repo_framework_unarmed_not_blocking():
    out = T.evaluate(T.ROOT)
    # 真实仓 67 规则无 .cpp 检查器 ⇒ unarmed warn，不判 block
    assert out[0]["status"] == "unarmed"
