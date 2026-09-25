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
    """章节结构不变；数字取现算权威值（640b：不再写死 114/7）。"""
    from w2_authority_640b import current as _w2
    exp = _w2()
    text = ga.render(ga.collect())
    for s in SECTIONS:
        assert s in text, f"报告缺小节：{s}"
    assert f"IN {exp['IN']} / OUT {exp['OUT']} / UNDEC {exp['UNDEC']}" in text
    # §6 与 594 实证对账：现算与实证一致 ⇒ 全 ✓（640 人签后误解层全 OUT，异常清空）
    assert f"| IN | {exp['IN']} | {exp['IN']} | ✓ |" in text
    assert f"| OUT | {exp['OUT']} | {exp['OUT']} | ✓ |" in text


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
    """幂等性不变；exit 码**随"存在异常"动态**（640b：不再写死 2）：
    无异常 ⇒ 0；注入异常 ⇒ 2（由 ga.anomalies 现算，见下一条测试的注入路径）。"""
    d1 = ga.collect()
    d2 = ga.collect()
    assert ga.render(d1) == ga.render(d2)
    an = ga.anomalies(d1["nodes"])
    bad = bool(an["prop_out"] or an["mis_in"] or an["undec"])
    expect = 2 if bad else 0
    out = tmp_path / "r.md"
    assert ga.main(["--out", str(out)]) == expect
    assert out.is_file()
    assert ga.main(["--out", str(out), "--check"]) == expect
    fresh = ga.render(ga.collect())
    out.write_text("stale\n", encoding="utf-8")
    assert ga.main(["--out", str(out), "--check"]) == 2, "过期必须 fail-loud"
    assert out.read_text(encoding="utf-8") == "stale\n", "--check 不得改写报告"
    out.write_text(fresh, encoding="utf-8")
    assert ga.main(["--out", str(out), "--check"]) == expect


def test_real_committed_report_matches_fresh_render():
    """已提交报告必须与现读事实源重新渲染**逐字节**一致（锁"不过期"）。

    640b：640 人签后误解层全部 OUT ⇒ 异常清空 ⇒ `--check` **exit 0**（无异常）；
    过期/异常仍 fail-loud（2）。
    """
    assert ga.OUT_DEFAULT.is_file(), "报告缺失：跑 `tools/grounded_audit.py`"
    assert ga.OUT_DEFAULT.read_text(encoding="utf-8") == ga.render(ga.collect())
    an = ga.anomalies(ga.collect()["nodes"])
    bad = bool(an["prop_out"] or an["mis_in"] or an["undec"])
    assert ga.main(["--check"]) == (2 if bad else 0)
