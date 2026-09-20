"""610 E4 · M6 方案落地准备回归锁（**只写文档，不改算子**）。

锁两件事（任务书 E4 的 2 例 + 3 例自加）：
  1. `data/m6_improvement_plan.md` 存在且九节齐全（现状 / 问题分析 / 三个方案 / 预期效果 /
     毒样例 / 风险 / 实施步骤 / 与 587-588 关系 / 不做清单）；
  2. 毒样例 **≥6** 条（A/B/C 各 2 条），每条都给了**期望判决**；
  +. 文档数字与 v7 基线**逐项一致**（716 / 0 逃逸 / n_a 0 / equivalent_invalid 8 / 379 / 0.52933）；
  +. 文档必须写明"**不落地**"（不改 `mut_m6`、不重冻结）；
  +. 文档不得声称"检测力提升"（716⇒708 是口径修正）—— 防"把口径修正当进步"的老毛病。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "data" / "m6_improvement_plan.md"
BASELINE = ROOT / "data" / "mutation" / "full_baseline_v7.json"
M6_TOOL = ROOT / "tools" / "mutation_m6_optimizer.py"


def _text() -> str:
    assert DOC.is_file(), f"方案缺失：{DOC}（610 E4 的产物）"
    return DOC.read_text(encoding="utf-8")


def _m6() -> dict:
    d = json.loads(BASELINE.read_text(encoding="utf-8"))
    return d["by_operator_rates"]["M6"]


def test_plan_document_exists():
    text = _text()
    for sec in ("## 1. M6 算子现状", "## 2. 问题分析", "## 3. 改进方案",
                "## 4. 预期效果", "## 5. 毒样例设计", "## 6. 风险评估",
                "## 7. 实施步骤", "## 8. 与 587/588 的 matrix 取值校验的关系",
                "## 9. 本批明确不做"):
        assert sec in text, f"方案缺小节：{sec}"
    # 方案 A/B/C 三支都要在
    for plan in ("### 方案 A", "### 方案 B", "### 方案 C"):
        assert plan in text, f"缺方案：{plan}"
    assert "本批**未改**" in text and "未重冻结" in text or "不落地" in text


def test_plan_has_poison_samples():
    text = _text()
    ids = re.findall(r"\|\s*(P-[ABC]\d)\s*\|", text)
    assert len(ids) >= 6, f"毒样例应 ≥6 条（实测 {ids}）"
    assert sorted(set(ids)) == ["P-A1", "P-A2", "P-B1", "P-B2", "P-C1", "P-C2"], ids
    for pid in ("P-A1", "P-A2", "P-B1", "P-B2", "P-C1", "P-C2"):
        row = [ln for ln in text.splitlines() if f"| {pid} |" in ln][0]
        assert "refute" in row, f"{pid} 未给出期望判决：{row}"
        assert "漏检后果" not in row and len(row.split("|")) >= 6, row
    assert "应触发的检测器" in text and "漏检后果" in text


def test_numbers_match_v7_baseline():
    text = _text()
    m6 = _m6()
    assert m6["judged"] == 716 and m6["n_a"] == 0 and m6["equivalent_invalid"] == 8
    assert m6["escaped"] if "escaped" in m6 else True                     # 速率区无该键
    assert m6["strict"]["numerator"] == 379 and m6["strict"]["point"] == 0.52933
    for want in ("**716**", "**8**（全批 `equivalent=8` **全部**来自 M6）",
                 "**379/716 = 0.52933**", "**708**（算术下界）"):
        assert want in text, f"方案缺实测数字：{want}"
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    assert base["by_operator"]["M6"]["escaped"] == 0 and "**0**" in text


def test_plan_is_honest_about_ruler_change():
    text = _text()
    assert "口径修正" in text, "必须点明 716⇒708 是口径修正"
    assert "不是**检测力提升" in text or "不是检测力提升" in text or "**不是**检测力提升" in text
    assert "必须先小样本验" in text, "新形态若逃逸，必须先小样本验证（不许直接全量）"


def test_plan_states_not_landed_and_no_code_change():
    text = _text()
    assert "`tools/mutation_fuzz.py` 的 `mut_m6` 本批**未改**" in text
    assert "landed=false" in text
    src = M6_TOOL.read_text(encoding="utf-8")
    assert "EST_EQUIVALENT_IN_M6 = 8" in src, "工具与文档的口径必须一致（单一真源）"
    # 本测试只读文档与工具，绝不改算子
    assert "mut_m6(" not in text.split("## 9")[1], "§9 不该出现改算子的动作"
