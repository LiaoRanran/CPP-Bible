"""610 C3 · 论证漏洞报告回归锁（完整报告 + 优先级 + 修复建议 + summary JSON）。

锁四件事（任务书 C3 的 4 例 + 2 例自加）：
  1. `generate_full_report`：七节齐全（总览 / P0 / P1 / P2 / 详细 / 统计 / 建议）；
  2. P0 含"无 high 可信度节点" + "4 个无攻击者命题"；
  3. P1 含"OUT 无辩护者 1" + "modify=1.0 的 7 个" + "主题失衡" + "图碎片化 11 分量"；
  4. `summary --json` 的计数与报告一致（P0 2 / P1 4 / P2 3，击败边 17）；
  +. 报告落盘幂等；`report --out` 与函数输出逐字一致；
  +. 报告里的数字**可复算**（312/388=80.4%、10、12、194 都来自探测器）。
"""
from __future__ import annotations

import json
from pathlib import Path

import argument_audit as aa

EDGES, VERDICTS, CRED = aa.load_state()
ANNS = aa.dc.load_annotations()
REPORT = aa.generate_full_report(EDGES, ANNS, VERDICTS, CRED)


def test_generate_full_report_sections():
    for sec in ("## 1. 总览", "## 2. P0 漏洞", "## 3. P1 漏洞", "## 4. P2 漏洞",
                "## 5. 详细描述 / 影响 / 修复建议", "## 6. 漏洞统计", "## 7. 后续建议（NDW 分类）"):
        assert sec in REPORT, f"报告缺小节：{sec}"
    assert "IN 114 / OUT 7 / UNDEC 0" in REPORT
    assert "边 **388**（其中**构成击败** 17）" in REPORT


def test_report_has_p0_vulnerabilities():
    assert "无 `high` 可信度节点" in REPORT
    assert "论证盲区：4 个命题无任何攻击者" in REPORT
    assert "ATOM-CONC-FENCE-001::prop-1" in REPORT
    assert "| P0 | 2 |" in REPORT


def test_report_has_p1_vulnerabilities():
    assert "OUT 的 MIS 中 1 个无 W2 辩护者" in REPORT
    assert "7 个 MIS 的 modify 比例 = 1.0" in REPORT
    assert "主题失衡" in REPORT and "80.4%" in REPORT
    assert "论证图碎片化" in REPORT and "11 个连通分量" in REPORT
    assert "| P1 | 4 |" in REPORT


def test_report_p2_and_recommendations():
    assert "ATOM-UB-GRAY-001::prop-1` 被 10 个 MIS 攻击" in REPORT
    assert "MIS-MEM-031` 攻击 12 个不同命题" in REPORT
    assert "194 个 2-环" in REPORT
    for dw in ("**Need（必须做）**", "**Do（可做）**", "**Won't（本批不做）**"):
        assert dw in REPORT
    assert "只呈现事实与建议" in REPORT


def test_summary_json():
    s = aa.summary_json(EDGES, ANNS, VERDICTS, CRED)
    assert s["p0"] == {"no_high_credibility": True, "no_attacker_propositions": 4}
    assert s["p1"]["no_defender_out_mis"] == 1 and s["p1"]["high_modify_mis"] == 7
    assert s["p1"]["components"] == 11 and s["p1"]["topic_imbalanced"] is True
    assert s["p2"] == {"top_prop_overload": 10, "top_mis_overload": 12, "cycles": 194}
    assert s["totals"] == {"p0": 2, "p1": 4, "p2": 3, "defeating_edges": 17}
    assert "不估未知" in s["note"]


def test_cli_report_and_summary(tmp_path: Path, capsys):
    out = tmp_path / "audit.md"
    assert aa.main(["report", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == REPORT, "CLI 产物必须与函数输出逐字一致"
    assert "P0 2 · P1 4 · P2 3" in capsys.readouterr().out
    assert aa.main(["summary", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["p1"]["components"] == 11


def test_report_is_idempotent():
    assert aa.generate_full_report(EDGES, ANNS, VERDICTS, CRED) == REPORT
    assert "2026-" not in REPORT, "报告不得含时间戳（否则幂等/入库 diff 全乱）"
