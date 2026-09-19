"""609 E3 · M1 TCE 定性分析回归锁（**只分析不攻坚**）。

锁三件事（任务书 3 例 + 2 例自加）：
  1. 六步齐全且**每步都有evidence**（不许空口下结论）；
  2. 第 5 步的定性结论必须是 **TCE**，且第 6 步明确"不攻坚/不改 mutation_fuzz/不重冻结"；
  3. `--check` 对 v7 基线自洽（M1 escaped==1 且 EV-CONC-001 escaped==1 ⇒ 逃逸格定位成立）；
  +. 报告里的数字必须来自 v7 基线（M1 judged 65 / blocked 64 / escaped 1 / n_a 27）；
  +. 前提变了要响 invoked：把 escaped 改成 2 ⇒ `--check` 必须 **fail**（不许拿旧结论糊新数据）。
"""
from __future__ import annotations

import json
from pathlib import Path

import m1_tce_analysis as m1

BASE = m1.DEFAULT_BASELINE


def test_six_steps_each_with_evidence():
    doc = m1.load_baseline()
    steps = m1.six_steps(m1.extract(doc))
    assert [s["step"] for s in steps] == [1, 2, 3, 4, 5, 6]
    for s in steps:
        assert s["title"] and s["question"] and s["answer"]
        assert str(s["evidence"]).strip(), f"第 {s['step']} 步缺 evidence（不许空口结论）"


def test_verdict_is_tce_and_no_fix():
    doc = m1.load_baseline()
    steps = {s["step"]: s for s in m1.six_steps(m1.extract(doc))}
    assert "TCE" in steps[5]["answer"], "第 5 步的定性结论必须是 TCE"
    for word in ("不攻坚", "不改", "不重冻结"):
        assert word in steps[6]["answer"], f"第 6 步缺硬边界表述：{word}"
    src = Path(m1.__file__).read_text(encoding="utf-8")
    # 分析器必须**不 import、不写** mutation_fuzz（改算子=改判决口径，需单独授权）
    for bad in ("import mutation_fuzz", "from mutation_fuzz", "open("):
        assert bad not in src, f"源码出现 {bad} ⇒ 有自动改算子/写盘风险"


def test_numbers_come_from_v7_baseline():
    e = m1.extract(m1.load_baseline())
    assert (e["m1"]["judged"] if "judged" in e["m1"] else e["rates"]["judged"]) == 65
    assert e["m1"]["blocked"] == 64 and e["m1"]["escaped"] == 1 and e["m1"]["n_a"] == 27
    assert e["card"]["blocked"] == 25 and e["card"]["escaped"] == 1 and e["card"]["n_a"] == 1
    assert e["variants"] == 1593 and e["escaped"] == 1 and e["n_a"] == 179


def test_check_passes_on_v7_and_fails_when_premise_changes(tmp_path: Path):
    assert m1.check() == []
    doc = m1.load_baseline()
    doc["by_operator"]["M1"]["escaped"] = 2          # 前提变了
    bad = tmp_path / "fake_v8.json"
    bad.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    assert m1.check(bad) != [], "逃逸数变了还报 OK ⇒ 拿旧结论糊新数据"


def test_report_contains_contract_and_card(tmp_path: Path):
    text = m1.render_report(m1.load_baseline())
    for key in ("1/1406", m1.M1_CARD, "TCE", "第 6 步 · 不做什么"):
        assert key in text, f"报告缺 {key}"
    assert text.count("## 第 ") == 6
    out = tmp_path / "m1.md"
    assert m1.main(["--write", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == text
    assert m1.main(["--check"]) == 0
