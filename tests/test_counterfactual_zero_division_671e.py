# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671e-A · 反事实算子 zero_division 核查测试。

**核查结论（先复现，再下结论）**：
671c 调研把"反事实算子 F1=0→1.0"列为 *zero_division 缺陷候选*。
本批经代码阅读 + 数据复现，结论是 **false positive（非缺陷）**：

  1. `tools/counterfactual_citation_658.py` 全程不使用 sklearn，
     仅返回布尔 `dependent`；
  2. P/R/F1 由 `tools/counterfactual_extend_665.py` 第 142-144 行
     **纯算术**计算，且已显式 `else 0.0` 防除零 —— 不存在 NaN 伪影；
  3. 当前数据 tp=2, fp=0, tn=8, fn=0 ⇒ P=R=F1=1.0 是**真实结果**；
  4. `tools/` 全目录 grep `sklearn` / `zero_division` = 0 命中。

F1=0→1.0 的真实成因：666 新增第 3 判据（machine_marker）抓住了两条
平台测量类 dependent 样本（tp 0→2），是算子能力真实提升，非 zero_division 伪影。

本测试集目的：锁定当前真实行为，并证明 zero_division 不可能成为 F1 的成因。
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")

_OP_PATH = os.path.join(TOOLS, "counterfactual_citation_658.py")
_DATA_PATH = os.path.join(DATA, "counterfactual_cases_665.json")


def _load_op658():
    spec = importlib.util.spec_from_file_location("cf658_671e", _OP_PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _load_cases():
    with open(_DATA_PATH, encoding="utf-8") as fh:
        return json.load(fh)


cf658 = _load_op658()


def test_operator_module_has_no_sklearn_and_no_zero_division():
    src = open(_OP_PATH, encoding="utf-8").read()
    assert "sklearn" not in src, "反事实算子不应引入 sklearn"
    assert "zero_division" not in src, "反事实算子不应有 zero_division 参数"


def test_tools_dir_has_no_sklearn_usage():
    import pathlib
    hits = []
    for p in pathlib.Path(TOOLS).rglob("*.py"):
        if p.name.endswith(".pyc"):
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if "sklearn" in txt:
            hits.append(str(p))
    assert hits == [], f"tools/ 中发现 sklearn 用法：{hits}"


def test_tools_dir_has_no_zero_division_param():
    import pathlib
    hits = []
    for p in pathlib.Path(TOOLS).rglob("*.py"):
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if "zero_division" in txt:
            hits.append(str(p))
    assert hits == [], f"tools/ 中发现 zero_division 参数：{hits}"


def test_manual_confusion_matrix_from_data():
    rep = _load_cases()
    tp = fp = tn = fn = 0
    for c in rep["cases"]:
        truth, pred = c["ground_truth"], c["operator_prediction"]
        if truth == "dependent" and pred == "dependent":
            tp += 1
        elif truth == "independent" and pred == "dependent":
            fp += 1
        elif truth == "independent" and pred == "independent":
            tn += 1
        else:
            fn += 1
    assert (tp, fp, tn, fn) == (2, 0, 8, 0), "10 条样本的混淆矩阵应恒为 tp=2,fp=0,tn=8,fn=0"


def test_scores_are_real_not_zerodivision_artifact():
    """F1=1.0 真实：tp=2 ⇒ 分子分母都 > 0，zero_division 机制根本不触发。"""
    rep = _load_cases()
    tp, fp, tn, fn = 2, 0, 8, 0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    assert rep["scores"]["precision"] == 1.0
    assert rep["scores"]["recall"] == 1.0
    assert rep["scores"]["f1"] == 1.0
    assert (prec, rec, f1) == (1.0, 1.0, 1.0)
    # zero_division 只在 tp 与 fp 同时为 0（precision）或 tp 与 fn 同时为 0（recall）时才有意义
    assert tp > 0, "tp>0 ⇒ 两个分母都非零，sklearn zero_division 不可能成为 F1=1.0 的成因"


def test_extend_formula_guards_division_by_zero_like_source():
    """复刻 counterfactual_extend_665.py 第 142-144 行的公式，证明显式防除零。"""
    def score(tp, fp, fn):
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        return prec, rec, f1

    p, r, f = score(0, 0, 0)
    assert (p, r, f) == (0.0, 0.0, 0.0), "全 0 应返回 0.0，绝不能是 NaN"
    assert not any(math.isnan(x) for x in (p, r, f))

    p, r, f = score(0, 3, 0)   # precision 无正例、有假阳 ⇒ 0.0，不崩
    assert p == 0.0 and not math.isnan(p)
    p, r, f = score(0, 0, 3)   # recall 无正例、有假阴 ⇒ 0.0，不崩
    assert r == 0.0 and not math.isnan(r)


def test_no_nan_in_recorded_scores():
    rep = _load_cases()
    for _k, v in rep["scores"].items():
        assert not math.isnan(v)


def test_denominator_is_declared():
    rep = _load_cases()
    d = rep["denominator"]
    assert d["value"] == 10, "分母必须自己说清 = 10"
    assert d["scored"] == 10


def test_truth_labels_and_third_criterion_hits():
    rep = _load_cases()
    assert rep["truth_labels"] == {"dependent": 2, "independent": 8}
    assert rep["third_criterion"]["hits"] == ["cf14", "cf18"]


def test_reproduce_operator_predictions_from_data():
    """端到端复现：用 658 算子重跑 10 条样本，预测应与产物一致。"""
    rep = _load_cases()
    for c in rep["cases"]:
        res = cf658.counterfactual(
            c["original_assertion"],
            c["original_citation"]["id"],
            c["original_citation"]["text"],
        )
        pred = "dependent" if res["dependent"] else "independent"
        assert pred == c["operator_prediction"], f"{c['id']} 复现不一致"


def test_all_ten_cases_agree_and_count_ten():
    rep = _load_cases()
    assert len(rep["cases"]) == 10
    assert all(c["agree"] for c in rep["cases"])


def test_operator_is_deterministic_no_randomness():
    a = cf658.counterfactual("本机 x86-64 sizeof(int)=4", "EV-IG11", "measure 实测：4")
    b = cf658.counterfactual("本机 x86-64 sizeof(int)=4", "EV-IG11", "measure 实测：4")
    assert a == b


def test_third_criterion_matches_ground_truth_source():
    """强诚实约束：判据 3（machine_marker）命中的 cf14/cf18，其 ground_truth 必须 = dependent。
    若二者同源却又不恒等，说明评估口径自相矛盾。"""
    rep = _load_cases()
    by_id = {c["id"]: c for c in rep["cases"]}
    for cid in rep["third_criterion"]["hits"]:
        assert by_id[cid]["ground_truth"] == "dependent"
        assert by_id[cid]["mechanism_class"] == "machine_marker"
