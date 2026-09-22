"""626 A1 · 统计重算校验器回归测试（≥5 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import stats_recalc_verifier_626 as S  # noqa: E402


def test_recompute_matches_expected():
    got = S.recompute()
    for k, want in S.EXPECTED.items():
        assert got[k] == want, f"{k}: 实测 {got[k]} != 预期 {want}"


def test_median_is_67_5():
    assert S.recompute()["reason_median"] == 67.5


def test_union_is_93_not_110():
    r = S.recompute()
    assert r["union_615_624"] == 93
    assert r["unique_615"] + r["unique_624"] - r["overlap_615_624"] == 93
    # 记录条数 110 ≠ 唯一 93（硬伤 3）
    assert r["unique_615"] + r["unique_624"] == 110


def test_exemptions_31_split():
    r = S.recompute()
    assert r["exemptions_total"] == 31
    assert r["exemptions_legacy"] == 27
    assert r["exemptions_hc"] == 4


def test_selftest_passes():
    assert S.selftest() == 0


def test_readonly_no_mutation():
    before = os.path.getsize(os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl"))
    S.recompute()
    after = os.path.getsize(os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl"))
    assert before == after
