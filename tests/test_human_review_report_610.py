"""610 A2 · 人审质量报告回归锁（只读 · 纯标准库）。

锁七件事（任务书 7 例）：
  1. load_annotations：加载 **388** 条且字段齐全；
  2. summarize_by_verdict：approve=354 / modify=34 / reject=0（比例可复算）；
  3. summarize_by_mis：**42** 个 MIS，且 `MIS-LANG-001` 的 modify 比例 = 1.0（6 条 6 modify）；
  4. summarize_by_topic：MEM 最多（实测 **312** 条 / 80.4%；任务书写"~264"是旧数）；
  5. detect_quality_anomalies：**7** 个 `modify_ratio_1.0` + 耗时缺失异常（存量无人审耗时字段）；
  6. generate_report：八个章节齐全且数字与统计函数一致；
  7. --check：与事实源逐字段一致 ⇒ exit 0；篡改报告 ⇒ exit 2。

⚠️ 全部走**仓库真实数据**（只读）；写盘只写 tmp_path（不污染 data/）。
"""
from __future__ import annotations

import json
from pathlib import Path

import human_review_report as hr


def test_load_annotations():
    anns = hr.load_annotations()
    assert len(anns) == 388
    for i, a in enumerate(anns, 1):
        assert a.get("edge_id") and a.get("reason") and a.get("reviewer"), f"第 {i} 条字段缺失"
        assert (a.get("action") or a.get("kind")) in ("approve", "modify", "reject")


def test_summarize_by_verdict():
    v = hr.summarize_by_verdict(hr.load_annotations())
    assert v["approve"]["count"] == 354
    assert v["modify"]["count"] == 34
    assert v["reject"]["count"] == 0
    assert v["approve"]["ratio"] == round(354 / 388, 4) == 0.9124      # 0.912371… ⇒ 四位
    assert round(v["approve"]["ratio"] + v["modify"]["ratio"], 4) == 1.0


def test_summarize_by_mis():
    rows = hr.summarize_by_mis(hr.load_annotations())
    assert len(rows) == 42, f"MIS 组数应为 42（实测 {len(rows)}）"
    lang = [r for r in rows if r["mis_id"] == "MIS-LANG-001"][0]
    assert lang["total"] == 6 and lang["modify"] == 6 and lang["modify_ratio"] == 1.0
    assert rows[0]["modify_ratio"] == 1.0, "排序应把 modify 比例最高者放最前"
    assert all(rows[i]["modify_ratio"] >= rows[i + 1]["modify_ratio"] for i in range(len(rows) - 1))


def test_summarize_by_topic():
    topics = hr.summarize_by_topic(hr.load_annotations())
    assert list(topics)[0] == "MEM", f"MEM 应为最大主题：{list(topics)}"
    assert topics["MEM"]["total"] == 312, f"MEM 实测 312 条（任务书 ~264 为旧数）：{topics['MEM']}"
    assert round(topics["MEM"]["ratio"], 3) == 0.804
    assert set(topics) == {"MEM", "UB", "HIST", "CONC", "LANG"}
    assert sum(t["total"] for t in topics.values()) == 388


def test_detect_quality_anomalies():
    an = hr.detect_quality_anomalies(hr.load_annotations())
    z = [x for x in an if x["type"] == "modify_ratio_1.0"]
    assert len(z) == 7, f"modify 比例=1.0 的 MIS 应为 7 个：{[x['mis_id'] for x in z]}"
    assert {x["mis_id"] for x in z} == {"MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003",
                                        "MIS-UB-001", "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"}
    miss = [x for x in an if x["type"] == "review_seconds_missing"][0]
    assert "388/388" in miss["detail"], miss
    assert not [x for x in an if x["type"] == "reason_too_short"], "理由最短 47 字符 ⇒ 不该报过短"
    assert not [x for x in an if x["type"] == "rubber_stamp_risk"], "无全 approve 的 MIS 组"


def test_generate_report(tmp_path: Path):
    text = hr.generate_report(hr.load_annotations())
    for sec in ("## 1. 总览", "## 2. 按 verdict 分布", "## 3. 按 MIS 分组",
                "## 4. 按主题分布", "## 5. 按方向分布", "## 6. 质量异常检测",
                "## 7. modify 比例 = 1.0 的 MIS", "## 8. 后续建议"):
        assert sec in text, f"报告缺章节：{sec}"
    assert "记录 **388** 条" in text and "MIS 组 **42** 个" in text
    assert "抽样验证准确率100%(20/20)" in text, "抽样准确率必须来自理由原文"
    assert "| prop_to_mis | 194 |" in text and "| mis_to_prop | 194 |" in text
    p = hr.write_report(text, tmp_path / "r.md")
    assert p.read_text(encoding="utf-8") == text


def test_check_consistency(tmp_path: Path):
    rep = tmp_path / "q.md"
    hr.write_report(hr.generate_report(hr.load_annotations()), rep)
    assert hr.check(rep) == []
    assert hr.main(["--report", str(rep), "--check"]) == 0
    rep.write_text("stale\n", encoding="utf-8")
    assert hr.main(["--report", str(rep), "--check"]) == 2


def test_cli_stats_and_anomalies(capsys):
    assert hr.main(["stats"]) == 0
    st = json.loads(capsys.readouterr().out)
    assert st["by_verdict"]["approve"]["count"] == 354
    assert st["mis_count"] == 42 and st["by_direction"] == {"mis_to_prop": 194, "prop_to_mis": 194}
    assert hr.main(["anomalies"]) == 0
    an = json.loads(capsys.readouterr().out)
    assert len([x for x in an if x["type"] == "modify_ratio_1.0"]) == 7
