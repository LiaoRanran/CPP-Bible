# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g E2/E3/E4/E5：ITT/过拟合/证据链/不确定度（23 条）。"""
from __future__ import annotations

import itt_discipline_671g as ITT
import overfitting_defense_671g as OF
import evidence_chain_671g as EC
import uncertainty_budget_671g as U


# ── E2 ITT（5）───────────────────────────────────────────────────────────────

def _entry(pap="pap1", ids=("s1",), reason="detector_unavailable", pre=True):
    return {"pap_id": pap, "exclusions": [
        {"id": i, "reason": reason, "preregistered": pre} for i in ids]}


def test_itt_valid():
    assert ITT.validate_entry("e1", _entry()) == []


def test_itt_missing_pap():
    e = _entry(pap="")
    assert any("pap_id" in x["message"] for x in ITT.validate_entry("e1", e))


def test_itt_bad_reason():
    e = _entry(reason="i_dont_like_it")
    assert any("排除理由" in x["message"] for x in ITT.validate_entry("e1", e))


def test_itt_posthoc_exclusion_blocked():
    e = _entry(pre=False)
    assert any("事后排除" in x["message"] for x in ITT.validate_entry("e1", e))


def test_itt_registry_and_real():
    reg = {"experiments": {"e1": _entry(), "e2": {"pap_id": "p", "exclusions": []}}}
    assert not any(x["severity"] == "block" for x in ITT.validate_entry("e1", reg["experiments"]["e1"]))
    f = ITT.check(ITT.ROOT)
    assert f == []


# ── E3 过拟合（6）─────────────────────────────────────────────────────────

def test_split_disjoint_passes():
    cfg = {"train_ids": ["a"], "validation_ids": ["b"], "test_ids": ["c"], "rule_tuning": []}
    assert OF.check_split(cfg) == []


def test_split_overlap_blocks():
    cfg = {"train_ids": ["a", "b"], "validation_ids": ["b"], "test_ids": []}
    f = OF.check_split(cfg)
    assert f and f[0]["target"] == "train∩validation"


def test_tuning_on_test_blocks():
    cfg = {"train_ids": [], "validation_ids": [], "test_ids": ["x"],
           "rule_tuning": [{"rule": "R1", "set": "test"}]}
    f = OF.check_split(cfg)
    assert any("test" in x["message"] for x in f)


def test_holm_basic():
    # 4 个 p 值，最小时 0.001 < 0.05/4=0.0125，第二 0.02 不<0.05/3=0.0167 ⇒ 拒绝 1 个
    rej = OF.holm([0.001, 0.02, 0.5, 0.9])
    assert rej == [0]


def test_bh_basic():
    rej = OF.benjamini_hochberg([0.01, 0.02, 0.03, 0.9], 0.05)
    # 阈值 0.0125,0.025,0.0375,0.05：前三个 ≤ 阈值(k=3)
    assert set(rej) == {0, 1, 2}


def test_overfit_real_unarmed_warn():
    f = OF.check(OF.ROOT)
    assert all(x["severity"] != "block" for x in f)


# ── E4 证据链（7）──────────────────────────────────────────────────────────

def test_add_and_verify_chain(tmp_path):
    (tmp_path / "y.json").write_text('{"v":1}', encoding="utf-8")
    (tmp_path / "x.json").write_text('{"v":2}', encoding="utf-8")
    EC.add_artifact(tmp_path, "x.json", ["y.json"])
    assert EC.check(tmp_path) == []


def test_missing_parent_blocks(tmp_path):
    EC.add_artifact(tmp_path, "x.json", ["ghost.json"])
    f = EC.check(tmp_path)
    assert any("来源文件缺失" in x["message"] for x in f)


def test_parent_changed_without_rerun_blocks(tmp_path):
    (tmp_path / "y.json").write_text('{"v":1}', encoding="utf-8")
    (tmp_path / "x.json").write_text('{"v":2}', encoding="utf-8")
    EC.add_artifact(tmp_path, "x.json", ["y.json"])
    (tmp_path / "y.json").write_text('{"v":999}', encoding="utf-8")
    f = EC.check(tmp_path)
    assert any("来源哈希变了" in x["message"] for x in f)


def test_poisoned_tree_fruit(tmp_path):
    # z 干净；y 依赖毒 z_dirty 改名？构造：artifact y 的 parent d 标毒
    (tmp_path / "clean.json").write_text('{}', encoding="utf-8")
    (tmp_path / "mid.json").write_text('{}', encoding="utf-8")
    (tmp_path / "final.json").write_text('{}', encoding="utf-8")
    EC.add_artifact(tmp_path, "mid.json", ["clean.json"])
    EC.add_artifact(tmp_path, "final.json", ["mid.json"])
    EC.save(tmp_path, {**EC.load_registry(tmp_path), "poisoned": ["clean.json"]})
    f = EC.check(tmp_path)
    targets = {x["target"] for x in f}
    assert "final.json" in targets and "mid.json" in targets


def test_poison_nonancestor_ok(tmp_path):
    (tmp_path / "clean.json").write_text('{}', encoding="utf-8")
    (tmp_path / "indep.json").write_text('{}', encoding="utf-8")
    EC.add_artifact(tmp_path, "indep.json", [])
    EC.save(tmp_path, {**EC.load_registry(tmp_path), "poisoned": ["clean.json"]})
    assert EC.check(tmp_path) == []


def test_self_changed_warns(tmp_path):
    (tmp_path / "x.json").write_text('{}', encoding="utf-8")
    EC.add_artifact(tmp_path, "x.json", [])
    (tmp_path / "x.json").write_text('{"changed":true}', encoding="utf-8")
    f = EC.check(tmp_path)
    assert any(x["severity"] == "warn" and "产物已更新" in x["message"] for x in f)


def test_real_chain_clean():
    assert EC.check(EC.ROOT) == []


# ── E5 不确定度预算（5）─────────────────────────────────────────────────

def test_stat_component():
    # 半宽 = (98.45-61.65)/2 = 18.4，再 /1.96
    assert abs(U.stat_component(61.65, 98.45) - (18.4 / 1.96)) < 1e-9


def test_components_nonnegative_and_combine():
    b = U.budget(14, 16, 61.65, 98.45, detector_gap_pp=81.3,
                 unknown_frac=1 / 30, kappa=0.8)
    c = b["components_pp"]
    assert c["u_stat"] > 0 and c["u_detector"] == 40.65
    assert b["u_sys_pp"] >= c["u_detector"]
    assert b["combined_std_pp"] >= c["u_stat"]
    # 扩展区间对称
    lo, hi = b["interval_combined_pct"]
    assert abs((hi - b["point_pct"]) - (b["point_pct"] - lo)) < 1e-6


def test_zero_system_components():
    b = U.budget(100, 100, 96.38, 100.0, detector_gap_pp=0, unknown_frac=0, kappa=1.0)
    assert b["components_pp"]["u_detector"] == 0
    assert b["components_pp"]["u_environment"] == 0
    assert b["components_pp"]["u_labeling"] == 0


def test_kappa_zero_raises_label_component():
    assert U.labeling_component(0.0) == 50.0
    assert U.labeling_component(1.0) == 0.0
    assert abs(U.labeling_component(0.6) - 20.0) < 1e-9


def test_budget_makes_uncertainty_visible():
    # 87.5%(14/16)：统计宽区间 + 81.3pp 仪器差 ⇒ 合成不确定度必须显著，不能把 87.5 当精确值
    b = U.budget(14, 16, 61.65, 98.45, detector_gap_pp=81.3)
    assert b["combined_std_pp"] > 10.0
