"""643 C4 · attack_quality_evaluator_643 单测（Wilson/指标/等预算对比/改进建议）。
编号 C4-1..C4-8。**不真跑沙箱**（真跑由 `--report` 负责）。
"""
from __future__ import annotations

import attack_quality_evaluator_643 as C4

SIM = {"rows": [
    {"verdict": "noop", "direction": "A", "change": []},
    {"verdict": "evaded", "direction": "A", "change": ["X"]},
    {"verdict": "blocked", "direction": "A", "change": []},
    {"verdict": "not_triggered", "direction": "B", "change": []},
    {"verdict": "triggered", "direction": "B", "change": ["Y"]},
    {"verdict": "oracle_mismatch", "direction": "B", "change": ["Z"]},
], "by_verdict": {}, "production_atoms_unchanged": True}


# C4-1：Wilson 区间基本性质
def test_wilson():
    assert C4.wilson(10, 10)[1] == 1.0 and C4.wilson(10, 10)[0] > 0.6
    assert C4.wilson(0, 10)[0] == 0.0 and C4.wilson(0, 10)[1] < 0.4
    assert C4.wilson(0, 0) == (0.0, 1.0)
    lo, hi = C4.wilson(5, 10)
    assert lo < 0.5 < hi


# C4-2：有效攻击率排除 noop
def test_effective_rate_excludes_noop():
    m = C4.metrics(SIM)
    assert m["noop"] == 1 and m["effective"] == 5
    assert m["effective_rate"] == round(5 / 6, 4)


# C4-3：产生影响率（firing 集合有变化的比例）
def test_impact_rate():
    assert C4.metrics(SIM)["impact_rate"] == 0.6


# C4-4：预期兑现率 = (blocked+triggered)/有效 —— **evaded 不算兑现**
def test_oracle_hit_rate():
    # 合成里 blocked 1 + triggered 1 = 2，有效 5 ⇒ 0.4（evaded 不计入）
    assert C4.metrics(SIM)["oracle_hit_rate"] == 0.4


# C4-4b：**回归锁** —— 早先把 evaded 计入"命中"会让方向 A 基线构造性满分（本批实测踩过）
def test_evaded_is_not_oracle_hit():
    only_evaded = {"rows": [{"verdict": "evaded", "direction": "A", "change": ["X"]}] * 4,
                   "by_verdict": {}, "production_atoms_unchanged": True}
    m = C4.metrics(only_evaded)
    assert m["oracle_hit_rate"] == 0.0, "evaded 必须算预期落空"
    assert m["escape_find_rate"] == 1.0, "但逃逸发现率应为 100%"


# C4-5：逃逸发现率与不可达候选率**分母分开**（A/B 不混用，且排除 noop）
def test_direction_specific_rates():
    m = C4.metrics(SIM)
    assert m["n_dir_a"] == 2 and m["n_dir_b"] == 3
    assert m["escape_find_rate"] == 0.5
    assert m["unreachable_rate"] == round(1 / 3, 4)


# C4-6：空输入不除零
def test_empty_input():
    m = C4.metrics({"rows": [], "by_verdict": {}})
    assert m["effective_rate"] is None and m["escape_find_rate"] is None
    assert m["total"] == 0


# C4-7：小样本不得声称统计显著（等预算对比的核心诚实点）
def test_small_sample_not_significant():
    a = {"rows": [{"verdict": "blocked", "direction": "A", "change": []}] * 5,
         "by_verdict": {}, "production_atoms_unchanged": True}
    b = {"rows": [{"verdict": "evaded", "direction": "A", "change": []}] * 5,
         "by_verdict": {}, "production_atoms_unchanged": True}
    c = C4.compare(a, b)
    assert c["statistically_significant"] is False
    assert "不能声称" in c["verdict"]
    assert c["n_per_arm"] == 5


# C4-8：改进建议非空 + 只读自检
def test_suggestions_and_selftest():
    a = {"rows": [{"verdict": "noop", "direction": "A", "change": []}] * 10,
         "by_verdict": {}, "production_atoms_unchanged": True}
    c = C4.compare(a, a)
    sug = C4.suggestions(c)
    assert len(sug) >= 1
    assert any("有效攻击率" in s or "样本量" in s for s in sug)
    assert C4.selftest() == 0
