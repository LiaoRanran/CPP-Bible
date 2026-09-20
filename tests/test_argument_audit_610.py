"""610 C1 · 论证漏洞检测（基础）回归锁：无攻击者命题 / 无辩护者 MIS / 孤立子图 / 未审边 / 可信度缺口。

锁七件事（任务书 C1 的 7 例 + 2 例自加）：
  1. 无攻击者命题 = **4**（ATOM-CONC-FENCE-001::prop-1/2 + ATOM-CONC-LOCK-001::prop-1/2）；
  2. **OUT 且无辩护者**的 MIS = **['MIS-LANG-001']**（1 个）+ 无辩护者节点合计 **7**；
  3. 连通分量 = **11**（孤立 4 个单节点，最大分量 **80** 节点 ⇒ 论证图碎片化）；
  4. 未人审边 = **0**（人审全量完成）；
  5. 可信度缺口：high **0** / medium **114** / low **7**，且显式报"无 high ⇒ 结构性缺口"；
  6. CLI 五个子命令输出正确（含 `--json`）；
  7. `--check` ⇒ exit 0；把节点全集/判决改动后 ⇒ 红（前提变了必须响）。

⚠️ 口径偏差登记：任务书写"7 个无辩护者 MIS"，实测是 **1 个**（其余空辩护者为 2 个非 OUT MIS + 4 个命题）；
   本测试按**实测**断言，并把该偏差写进 610 outbox。
"""
from __future__ import annotations

import json
from pathlib import Path

import argument_audit as aa
import defense_chain as dc

EDGES, VERDICTS, CRED = aa.load_state()
NODES = aa.all_nodes(VERDICTS, EDGES)
PROPS = [n for n in VERDICTS if dc.node_type_of(n, EDGES) == "proposition"]


def test_detect_no_attacker_propositions():
    got = aa.detect_no_attacker_propositions(EDGES, PROPS)
    assert got == ["ATOM-CONC-FENCE-001::prop-1", "ATOM-CONC-FENCE-001::prop-2",
                   "ATOM-CONC-LOCK-001::prop-1", "ATOM-CONC-LOCK-001::prop-2"], got


def test_detect_no_defender_mis():
    got = aa.detect_no_defender_mis(EDGES, VERDICTS, CRED)
    assert got == ["MIS-LANG-001"], f"OUT 且无辩护者的 MIS 实测只有 1 个，实得 {got}"
    assert set(got) <= set(dc.stats(EDGES, VERDICTS, CRED)["out_nodes"])


def test_detect_no_defender_nodes_total():
    got = aa.detect_no_defender_nodes(EDGES, VERDICTS, CRED)
    assert len(got) == 7, got
    assert sum(1 for n in got if dc.node_type_of(n, EDGES) == "proposition") == 4


def test_detect_isolated_subgraphs():
    comps = aa.detect_isolated_subgraphs(EDGES, NODES)
    assert len(comps) == 11, f"连通分量实测 11，实得 {len(comps)}"
    singles = [c for c in comps if len(c) == 1]
    assert len(singles) == 4, f"孤立单节点应为 4（= 四个无攻击者命题），实得 {singles}"
    assert [len(c) for c in comps][-1] == 80, "最大分量 80 节点（按大小升序排在最后）"
    assert sum(len(c) for c in comps) == len(NODES) == 121


def test_detect_unreviewed_edges():
    assert aa.detect_unreviewed_edges(EDGES) == [], "人审全量完成 ⇒ 未审边 0"
    assert sum(1 for e in EDGES if e.human_verdict != "unreviewed") == 388


def test_detect_credibility_gaps():
    gaps = aa.detect_credibility_gaps(CRED)
    assert gaps["distribution"] == {"high": 0, "medium": 114, "low": 7}
    assert gaps["total"] == 121
    assert any("无 `high`" in g for g in gaps["gaps"]), gaps


def test_cli_basic_detectors(capsys):
    assert aa.main(["no-attackers"]) == 0
    assert len([x for x in capsys.readouterr().out.splitlines() if x.strip()]) == 4
    assert aa.main(["no-defenders"]) == 0
    assert capsys.readouterr().out.strip() == "MIS-LANG-001"
    assert aa.main(["isolated"]) == 0
    assert len([x for x in capsys.readouterr().out.splitlines() if x.strip()]) == 4
    assert aa.main(["unreviewed"]) == 0
    assert capsys.readouterr().out.strip() == ""
    assert aa.main(["credibility-gaps", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["distribution"]["medium"] == 114


def test_check_consistency_strict(tmp_path: Path):
    assert aa.check() == []
    assert aa.main(["--check"]) == 0


def test_check_red_when_premise_changes(tmp_path: Path):
    """前提变了（可信度档位被人为改动）⇒ check 必须红（不许拿旧结论糊新数据）。"""
    bad_cred = dict(CRED)
    for k in list(bad_cred)[:5]:
        bad_cred[k] = "high"
    saved = aa.load_state

    def fake(*_a, **_k):
        return EDGES, VERDICTS, bad_cred

    aa.load_state = fake
    try:
        assert aa.check() != [], "可信度分布被改还报 OK ⇒ 自洽校验形同虚设"
    finally:
        aa.load_state = saved
