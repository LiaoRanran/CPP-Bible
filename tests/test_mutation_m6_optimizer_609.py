"""609 E4 · M6 优化方案回归锁（**只方案不落地**）。

锁三件事（任务书 3 例 + 3 例自加）：
  1. 4 类有效 + 4 类等价，分类齐全且每条都有"为什么"；
  2. 分母测算是**可复核的算术**（716 - 8 = 708），且明确标注"测算非实测"；
  3. `--check` 抓得住"前提变了"（改判分 denominators ⇒ 必须 FAIL）；
  +. 数字必须来自 v7 基线，不是任务书的占位值（M6 judged 716 / n_a 0 / equivalent_invalid 8）；
  +. 明确"未落地"（`landed is False` + authority 字段写明要监工授权）；
  +. 静态断言：工具不 npm `mutation_fuzz`（没有 import、没有写盘调用）。
"""
from __future__ import annotations

import json
from pathlib import Path

import mutation_m6_optimizer as m6

BASE = m6.DEFAULT_BASELINE


def test_four_effective_and_four_equivalent_classes():
    p = m6.plan(m6.m6_stats(m6.load_baseline()))
    assert len(p["keep_classes"]) == 4 and len(p["drop_classes"]) == 4
    for c in p["keep_classes"] + p["drop_classes"]:
        assert c["id"] and c["name"] and c["why"], f"分类 {c} 缺字段（不许空口分类）"
    assert all(c["id"].startswith("E") for c in p["keep_classes"])
    assert all(c["id"].startswith("Q") for c in p["drop_classes"])


def test_denominator_estimate_is_recomputable():
    s = m6.m6_stats(m6.load_baseline())
    p = m6.plan(s)
    assert s["judged"] == 716, "M6 可判变了 ⇒ 整套方案要重算"
    assert p["judged_before"] == 716 and p["judged_after_est"] == 716 - m6.EST_EQUIVALENT_IN_M6
    assert p["judged_after_est"] == 708 and p["delta"] == 8
    report = m6.render_report(m6.load_baseline())
    assert "真实值只能靠重冻结实测出来" in report, "报告必须标注「测算非实测」口径"
    assert "716" in report and "⇒ 708" in report or "708" in report


def test_check_fails_when_premise_changes(tmp_path: Path):
    assert m6.check() == []
    doc = m6.load_baseline()
    doc["by_operator"]["M6"]["blocked"] = 500          # 前提变了
    bad = tmp_path / "fake.json"
    bad.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    assert m6.check(bad) != [], "分母变了还报 OK ⇒ 拿旧方案糊新数据"


def test_numbers_are_from_baseline_not_from_taskbook():
    """任务书写 332→~323；v7 实测是 716（n_a=0，且全批 8 条等价全来自 M6）。"""
    s = m6.m6_stats(m6.load_baseline())
    assert (s["judged"], s["n_a"], s["equivalent_invalid"]) == (716, 0, 8)
    assert s["escaped"] == 0 and s["variants"] == 1593


def test_plan_is_not_landed_and_needs_authority():
    p = m6.plan(m6.m6_stats(m6.load_baseline()))
    assert p["landed"] is False
    assert "监工" in p["authority"] and "未落地" in p["authority"]
    assert "重冻结" in p["authority"], "必须写明真实值是靠重冻结才能拿到"


def test_no_import_of_mutation_fuzz():
    src = Path(m6.__file__).read_text(encoding="utf-8")
    for bad in ("import mutation_fuzz", "from mutation_fuzz", "importlib"):
        assert bad not in src, f"出现 {bad} ⇒ 有自动落地/改算子的风险"


def test_report_write_roundtrip(tmp_path: Path):
    out = tmp_path / "plan.md"
    assert m6.main(["--write", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "未落地" in text and "716" in text and "M6 算子优化方案" in text
