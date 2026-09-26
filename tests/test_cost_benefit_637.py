"""637 D · cost_benefit_637 单测（纯标准库，≥5 例）。编号 TD-1..TD-6。"""
from __future__ import annotations

import cost_benefit_637 as C


# TD-1：收益/成本映射
def test_level_map():
    assert C.LEVEL == {"低": 1, "中": 2, "高": 3}


# TD-2：风险系数（report/tool/core）
def test_risk_factor():
    assert C.RISK_FACTOR == {"report": 0.5, "tool": 1.0, "core": 1.5}


# TD-3：评分公式（高收益/低成本/report = 1.5）
def test_formula():
    assert C.score_one("低", "高", "report") == 1.5
    assert C.score_one("高", "高", "tool") == 1.0


# TD-4：flatten 把 异常×候选 展平
def test_flatten():
    items = [{"anomaly": {"name": "接地率低", "severity": "P1"},
              "candidates": [{"name": "a", "action": "x", "cost": "低", "benefit": "高",
                              "dependency": "无", "risk_class": "report"},
                             {"name": "b", "action": "y", "cost": "中", "benefit": "中",
                              "dependency": "无", "risk_class": "core"}]}]
    rows = C.flatten(items)
    assert len(rows) == 2 and rows[0]["score"] == 1.5


# TD-5：排序高分在前
def test_rank():
    rows = [{"score": 0.2, "benefit": "低", "cost": "高", "anomaly_severity": "P0",
             "anomaly_name": "B", "candidate": "y"},
            {"score": 1.5, "benefit": "高", "cost": "低", "anomaly_severity": "P1",
             "anomaly_name": "A", "candidate": "x"}]
    assert C.rank(rows)[0]["candidate"] == "x"


# TD-6：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
