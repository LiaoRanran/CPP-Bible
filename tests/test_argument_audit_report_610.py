"""610 C3 · 论证漏洞报告回归锁（完整报告 + 优先级 + 修复建议 + summary JSON）。

**640c A1/A2 重写**：原版把报告里的派生量写死（`IN 114 / OUT 7`、`构成击败 17`、
`P0 2 / P1 4 / P2 3`、`194 个 2-环`…），人签重算后批量过期。

现在：
1. **报告内部一致性**：报告里的每个数字都取自已生成它的同一份现算结果
   （`aa.collect_findings` / `aa.priority_counts`），测试只断言"报告与现算一致"；
2. **条件逻辑（真验证力）**：`P0` 段落必须随"`high` 档是否为空"出现/消解 —— 这正是原版
   的真 bug（无条件声称"无 `high` 档节点"，却打印出 high 79，自相矛盾）；
3. 权威取值走 `tools/w2_derived_640c.py`（现算 vs 入库产物两条路径）。
"""
from __future__ import annotations

import json
from pathlib import Path

import argument_audit as aa
import defense_chain as dc
import w2_derived_640c as wd

EDGES, VERDICTS, CRED = aa.load_state()
ANNS = aa.dc.load_annotations()
F = aa.collect_findings(EDGES, ANNS, VERDICTS, CRED)
CNT = aa.priority_counts(F)
REPORT = aa.generate_full_report(EDGES, ANNS, VERDICTS, CRED)
PIN = wd.pinned()
N_MIS = sum(1 for n in VERDICTS if dc.node_type_of(n, EDGES) == "misconception")
N_PROPS = len(VERDICTS) - N_MIS


def test_generate_full_report_sections():
    for sec in ("## 1. 总览", "## 2. P0 漏洞", "## 3. P1 漏洞", "## 4. P2 漏洞",
                "## 5. 详细描述 / 影响 / 修复建议", "## 6. 漏洞统计", "## 7. 后续建议（NDW 分类）"):
        assert sec in REPORT, f"报告缺小节：{sec}"
    # 总览数字 = 现算（不写死）
    assert f"- 节点 **{len(VERDICTS)}**（命题 {N_PROPS} + 误解 {N_MIS}）" in REPORT
    assert f"边 **{LIVE_EDGES()}**（其中**构成击败** {PIN['defeating_edges']}）" in REPORT
    assert f"- 判决 **IN {PIN['in']} / OUT {PIN['out']} / UNDEC {PIN['undec']}**" in REPORT


def LIVE_EDGES() -> int:
    return int(dc.solve_summary(EDGES, CRED)["edges"])


def test_report_p0_matches_credibility_reality():
    """P0 的"无 `high` 档节点"条目必须与实况一致（原版无条件输出 ⇒ 自相矛盾）。"""
    dist = PIN["credibility_distribution"]
    if dist["high"] == 0:
        assert "- **无 `high` 可信度节点**" in REPORT
    else:
        assert "**已消解**" in REPORT, "high 档非空时该条目必须标为已消解"
        assert f"`high` {dist['high']} 个" in REPORT
    if F["no_attacker_props"]:
        assert f"**论证盲区：{len(F['no_attacker_props'])} 个命题无任何攻击者**" in REPORT
    assert f"| P0 | {CNT['p0']} |" in REPORT, "P0 条数必须现算"


def test_report_p0_when_no_high_credibility():
    """夹具（真验证力）：把全部可信度压到 low ⇒ 必须出现"无 `high` 档"P0 且条数变 2。"""
    low_cred = {k: "low" for k in CRED}
    rep = aa.generate_full_report(EDGES, ANNS, VERDICTS, low_cred)
    f = aa.collect_findings(EDGES, ANNS, VERDICTS, low_cred)
    cnt = aa.priority_counts(f)
    assert "- **无 `high` 可信度节点**" in rep
    assert "已消解" not in rep, "压到 low 后不该再出现「已消解」"
    assert cnt["p0"] == 2, "此时 P0 = 无 high + 无攻击者命题 = 2"
    assert f"| P0 | {cnt['p0']} |" in rep


def test_report_has_p1_vulnerabilities():
    assert f"OUT 的 MIS 中 {len(F['no_defender_mis'])} 个无 W2 辩护者" in REPORT
    assert f"{len(F['high_modify'])} 个 MIS 的 modify 比例 = 1.0" in REPORT
    if F["topic"]["imbalanced"]:
        assert "主题失衡" in REPORT
    assert f"{F['components']['count']} 个连通分量" in REPORT
    assert f"| P1 | {CNT['p1']} |" in REPORT


def test_report_p2_and_recommendations():
    assert f"`{F['prop_overload'][0]['proposition']}` 被 " \
           f"{F['prop_overload'][0]['attackers']} 个 MIS 攻击" in REPORT
    assert f"`{F['mis_overload'][0]['mis_id']}` 攻击 " \
           f"{F['mis_overload'][0]['propositions']} 个不同命题" in REPORT
    assert f"{len(F['cycles'])} 个 2-环" in REPORT
    for dw in ("**Need（必须做）**", "**Do（可做）**", "**Won't（本批不做）**"):
        assert dw in REPORT
    assert "只呈现事实与建议" in REPORT
    assert f"| P2 | {CNT['p2']} |" in REPORT


def test_summary_json():
    s = aa.summary_json(EDGES, ANNS, VERDICTS, CRED)
    assert s["p0"] == {"no_high_credibility": PIN["credibility_distribution"]["high"] == 0,
                       "no_attacker_propositions": len(F["no_attacker_props"])}
    assert s["p1"]["no_defender_out_mis"] == len(F["no_defender_mis"])
    assert s["p1"]["high_modify_mis"] == len(F["high_modify"])
    assert s["p1"]["components"] == F["components"]["count"]
    assert s["p1"]["topic_imbalanced"] == F["topic"]["imbalanced"]
    assert s["p2"]["top_prop_overload"] == F["prop_overload"][0]["attackers"]
    assert s["p2"]["top_mis_overload"] == F["mis_overload"][0]["propositions"]
    assert s["p2"]["cycles"] == len(F["cycles"])
    # 关键回归：totals.p0 曾写死 2，与 p0.no_high_credibility 脱钩 ⇒ 自相矛盾
    assert s["totals"]["p0"] == (1 if s["p0"]["no_high_credibility"] else 0) \
        + (1 if s["p0"]["no_attacker_propositions"] else 0)
    assert s["totals"]["p0"] == CNT["p0"] and s["totals"]["p1"] == CNT["p1"] \
        and s["totals"]["p2"] == CNT["p2"]
    assert s["totals"]["defeating_edges"] == PIN["defeating_edges"]
    assert "不估未知" in s["note"]


def test_report_and_summary_agree_on_p1_counts():
    """报告 §6 与 summary 的 P1 明细必须逐项一致（同源现算的另一条路径）。"""
    s = aa.summary_json(EDGES, ANNS, VERDICTS, CRED)
    assert f"无辩护者 OUT MIS {s['p1']['no_defender_out_mis']}" in REPORT
    assert f"modify=1.0 的 MIS {s['p1']['high_modify_mis']}" in REPORT
    assert f"2-环 {s['p2']['cycles']}" in REPORT


def test_cli_report_and_summary(tmp_path: Path, capsys):
    out = tmp_path / "audit.md"
    assert aa.main(["report", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == REPORT, "CLI 产物必须与函数输出逐字一致"
    assert f"P0 {CNT['p0']} · P1 {CNT['p1']} · P2 {CNT['p2']}" in capsys.readouterr().out
    assert aa.main(["summary", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["p1"]["components"] == F["components"]["count"]


def test_report_is_idempotent():
    assert aa.generate_full_report(EDGES, ANNS, VERDICTS, CRED) == REPORT
    assert "2026-" not in REPORT, "报告不得含时间戳（否则幂等/入库 diff 全乱）"
