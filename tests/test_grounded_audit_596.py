"""596 任务3 · grounded 对照报告回归锁。

锁四件事：
  * 正例：真实数据能生成含**全部六节**的报告，且 §6 与 594 实证对账一致；
  * **异常必须显形**（fail-loud）：注入一条 OUT 命题 / IN 误解 / UNDEC ⇒ 报告 §5 必须出现异常清单，
    且 CLI exit 2 —— 绝不允许"有异常还静默判绿"；
  * 幂等：连续两次生成逐字节一致（报告里不含时间戳）；
  * `--check`：报告与事实源一致 ⇒ 0；不一致/异常 ⇒ 2。
"""
from __future__ import annotations

import json

import grounded_audit as ga

SECTIONS = ("## §1 grounded 标注总览", "## §2 与 `claim_type` 对照",
            "## §3 与 replay verdict 对照", "## §4 辩护链示例",
            "## §5 异常检测", "## §6 与 594 实证对账")


def _labels() -> dict:
    return ga.load_labels()


def test_report_has_all_sections_and_reconciles_with_594():
    """章节结构不变；**数字更新为人审全量后的真实值**（IN114/OUT7，与 594 实证不再一致 ⇒ ❌）。"""
    text = ga.render(ga.collect())
    for s in SECTIONS:
        assert s in text, f"报告缺小节：{s}"
    assert "IN 114 / OUT 7 / UNDEC 0" in text
    assert "in_propositions 79 · in_misconceptions 35" in text
    # 人审把 35 个 MIS 抬到与命题同档 ⇒ 不再被击败 ⇒ 误解判 IN ⇒ 命中"理论应为 0"的异常档
    assert "### ❌❌ 异常【必须人审，不得静默通过】❌❌" in text
    assert "❌ 误解被判 **IN**（35 条" in text
    assert "| IN | 79 | 114 | ❌ |" in text and "| OUT | 42 | 7 | ❌ |" in text
    assert "| UNDEC | 0 | 0 | ✓ |" in text


def test_anomalies_are_loud_in_report_and_cli(tmp_path, monkeypatch):
    """注入三类异常 ⇒ 报告必须标出 ❌ 清单（不静默），CLI 必须 exit 2。"""
    doc = _labels()
    prop = next(k for k, v in doc["nodes"].items() if v["type"] == "proposition")
    mis = next(k for k, v in doc["nodes"].items() if v["type"] == "misconception")
    bad = json.loads(json.dumps(doc))
    bad["nodes"][prop]["label"] = "OUT"
    bad["nodes"][mis]["label"] = "IN"
    p = tmp_path / "labels.json"
    p.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")

    data = ga.collect(p)
    an = ga.anomalies(data["nodes"])
    assert prop in an["prop_out"] and mis in an["mis_in"], an
    text = ga.render(data)
    assert "异常【必须人审，不得静默通过】" in text and "❌" in text
    assert prop in text and mis in text
    # CLI：生成 ⇒ exit 2（报告照样落盘供人读）；--stdout 不落盘
    out = tmp_path / "report.md"
    assert ga.main(["--labels", str(p), "--out", str(out)]) == 2
    assert out.is_file() and "异常" in out.read_text(encoding="utf-8")


def test_undec_is_also_an_anomaly(tmp_path):
    doc = json.loads(json.dumps(_labels()))
    k = next(iter(doc["nodes"]))
    doc["nodes"][k]["label"] = "UNDEC"
    p = tmp_path / "l.json"
    p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    an = ga.anomalies(ga.collect(p)["nodes"])
    assert k in an["undec"], "UNDEC 也是异常（攻击边不完整）"


def test_report_is_idempotent_and_check_works(tmp_path):
    """幂等性不变；**exit 码随"存在异常"变化**（人审后 35 个误解判 IN ⇒ fail-loud 2）：
    写盘 2（异常）· 一致但异常 2 · 过期 2（用 stderr 文案区分后两者）。"""
    d1 = ga.collect()
    d2 = ga.collect()
    assert ga.render(d1) == ga.render(d2)
    out = tmp_path / "r.md"
    assert ga.main(["--out", str(out)]) == 2, "有异常时写盘必须 fail-loud（exit 2）"
    assert out.is_file()
    assert ga.main(["--out", str(out), "--check"]) == 2
    fresh = ga.render(ga.collect())
    out.write_text("stale\n", encoding="utf-8")
    assert ga.main(["--out", str(out), "--check"]) == 2
    assert out.read_text(encoding="utf-8") == "stale\n", "--check 不得改写报告"
    out.write_text(fresh, encoding="utf-8")
    assert ga.main(["--out", str(out), "--check"]) == 2


def test_real_committed_report_matches_fresh_render():
    """已提交报告必须与现读事实源重新渲染**逐字节**一致（锁"不过期"）。

    610 A1：报告已按人审后的事实源**重新生成并入库**（IN114/OUT7 + 35 条 IN 误解异常）；
    `--check` 因异常存在 ⇒ **exit 2**（fail-loud，这是设计而非回归）。
    """
    assert ga.OUT_DEFAULT.is_file(), "报告缺失：跑 `tools/grounded_audit.py`"
    assert ga.OUT_DEFAULT.read_text(encoding="utf-8") == ga.render(ga.collect())
    assert ga.main(["--check"]) == 2, "有异常时 --check 必须 fail-loud（exit 2）"
