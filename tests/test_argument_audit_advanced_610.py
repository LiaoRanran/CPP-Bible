"""610 C2 · 高级漏洞检测回归锁（modify 比例 / rubber-stamp / 主题不平衡 / 命题过载 / MIS 过载 / 循环论证）。

锁七件事（任务书 C2 的 7 例 + 2 例自加）：
  1. `detect_high_modify_ratio_mis`：**7** 个 MIS 的 modify 比例 = 1.0（全部 OUT 的那 7 个）；
  2. `detect_rubber_stamp_risk`：实测**空**（最短理由 47 字符 ≥ 20 ⇒ 无盖章机风险）；
  3. `detect_topic_imbalance`：MEM 主导 **312 条 / 80.4%**（阈值 60% ⇒ imbalanced=True）；
  4. `detect_proposition_overload`：第一名 `ATOM-UB-GRAY-001::prop-1` 被 **10** 个 MIS 攻击；
  5. `detect_mis_overload`：第一名 `MIS-MEM-031` 攻击 **12** 个不同命题；
  6. `detect_cycle_arguments`：**194** 个 2-环（= 388 边 / 2 的对称配对）；
  7. CLI `high-modify` 输出正确。
  +. 过载榜严格降序；`topic-imbalance` 的比值可复算（312/388）。
"""
from __future__ import annotations

import json

import argument_audit as aa
import human_review_report as hrr

EDGES, VERDICTS, CRED = aa.load_state()
ANNS = aa.dc.load_annotations()


def test_detect_high_modify_ratio_mis():
    rows = aa.detect_high_modify_ratio_mis(ANNS)
    assert len(rows) == 7, f"modify 比例 >0.5 的 MIS 应为 7，实得 {len(rows)}"
    assert all(r["modify_ratio"] == 1.0 for r in rows)
    assert {r["mis_id"] for r in rows} == {"MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003",
                                          "MIS-UB-001", "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"}
    assert rows[0]["total"] == 6, "并列 1.0 时按总条数降序 ⇒ 6 条的排前"
    assert "第二轮人审" in rows[0]["reason"]


def test_detect_rubber_stamp_risk():
    rows = aa.detect_rubber_stamp_risk(ANNS)
    assert rows == [], f"实测无 rubber-stamp 风险（最短理由 47 ≥ 20）：{rows}"
    shortest = min(len(a["reason"]) for a in ANNS)
    assert shortest == 47, f"最短理由实测 47 字符（实得 {shortest}）⇒ 阈值未命中是数据事实"


def test_detect_topic_imbalance():
    res = aa.detect_topic_imbalance(ANNS)
    assert res["dominant_topic"] == "MEM" and res["imbalanced"] is True
    assert res["distribution"]["MEM"]["total"] == 312
    assert res["dominant_ratio"] == round(312 / 388, 4) == 0.8041
    assert res["distribution"]["MEM"]["mis_count"] == 27
    assert "80.4%" in res["note"]
    assert sum(v["total"] for v in res["distribution"].values()) == 388


def test_detect_proposition_overload():
    rows = aa.detect_proposition_overload(EDGES)
    assert len(rows) == 10
    assert rows[0]["proposition"] == "ATOM-UB-GRAY-001::prop-1"
    assert rows[0]["attackers"] == 10 and len(rows[0]["nodes"]) == 10
    assert all(rows[i]["attackers"] >= rows[i + 1]["attackers"] for i in range(len(rows) - 1))
    assert rows[1]["proposition"] == "ATOM-UB-GRAY-001::prop-2"


def test_detect_mis_overload():
    rows = aa.detect_mis_overload(EDGES)
    assert len(rows) == 10
    assert rows[0]["mis_id"] == "MIS-MEM-031"
    assert rows[0]["propositions"] == 12 and rows[0]["edges"] == 12
    assert all(len(r["targets"]) == r["propositions"] for r in rows)
    assert all(rows[i]["propositions"] >= rows[i + 1]["propositions"]
               for i in range(len(rows) - 1))


def test_detect_cycle_arguments():
    cycles = aa.detect_cycle_arguments(EDGES)
    assert len(cycles) == 194, f"2-环应为 194（388 边的对称配对），实得 {len(cycles)}"
    assert all(len(c) == 2 for c in cycles)
    assert ["ATOM-CONC-RACE-001::prop-1", "MIS-CONC-003"] in cycles
    assert len({tuple(c) for c in cycles}) == 194, "环不重复计数"


def test_cli_high_modify(capsys):
    assert aa.main(["high-modify", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert len(rows) == 7 and rows[0]["modify"] == 6
    assert aa.main(["rubber-stamp"]) == 0
    assert capsys.readouterr().out.strip() == ""
    assert aa.main(["cycles"]) == 0
    assert len([x for x in capsys.readouterr().out.splitlines() if x.strip()]) == 194


def test_cli_overload_and_topic(capsys):
    assert aa.main(["proposition-overload", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["attackers"] == 10
    assert aa.main(["mis-overload", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["propositions"] == 12
    assert aa.main(["topic-imbalance", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["dominant_ratio"] == 0.8041


def test_helpers_agree_with_human_review_report():
    """跨工具单一真源：C2 的 MIS/主题统计必须与 A2 的报告工具逐字段一致。"""
    a2 = {r["mis_id"]: r["modify_ratio"] for r in hrr.summarize_by_mis(ANNS)}
    c2 = {r["mis_id"]: r["modify_ratio"] for r in aa.detect_high_modify_ratio_mis(ANNS, 0.0)}
    assert all(c2[k] == v for k, v in a2.items() if k in c2)
    t2 = hrr.summarize_by_topic(ANNS)
    c2t = aa.detect_topic_imbalance(ANNS)["distribution"]
    assert c2t["MEM"]["total"] == t2["MEM"]["total"] == 312
