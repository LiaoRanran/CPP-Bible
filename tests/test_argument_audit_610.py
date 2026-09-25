"""610 C1 · 论证漏洞检测（基础）回归锁。

**640c A1/A2 重写**：原版把 W2 的派生量（可信度分布 {high:0,medium:114,low:7}、
OUT 无辩护者 1、无辩护者合计 7、分量 11/孤立 4/最大 80、节点 121）**写死在断言里**，
632/634 命题级人签之后批量过期（640b 的涟漪、640c 的 14 项）。

现在的分两层（§三.4 "防自我证明"）：

1. **夹具测试（真验证力）**：人造小图 / 人造可信度 → **已知输入 → 已知输出**，
   直接锁五个探测器的语义（`_synthetic` 一节）；
2. **真实库测试（不变量 + 跨源）**：不再断言"当前数字是多少"，只断言
   * 探测结果满足定义性不变量（子集关系、排序、W2 辩护者为空…）；
   * 现算与**入库 W2 产物**两条独立路径一致（`tools/w2_derived_640c.py`）。

⇒ 仓库正常演进（人签/重算/加边）不会批量红；只有真破坏不变量或产物与现算漂移才红。
"""
from __future__ import annotations

import json
from pathlib import Path

import argument_audit as aa
import defense_chain as dc
import w2_derived_640c as wd

EDGES, VERDICTS, CRED = aa.load_state()
NODES = aa.all_nodes(VERDICTS, EDGES)
PROPS = [n for n in VERDICTS if dc.node_type_of(n, EDGES) == "proposition"]
#: 权威源（派生量只在这里"写数"）
LIVE = wd.live()
PIN = wd.pinned()


# ── 一、夹具：已知输入 → 已知输出（真验证力，与真实库数字无关）──────────────────
def _synthetic() -> tuple[list[dc.AttackEdge], dict[str, str], dict[str, str]]:
    """人造图（5 节点 / 3 边）：

        P1(high) ⇄ M1(low)          M2(high) → P2(low)          P3(high) 孤立（无边）

    现算判决：P1 IN · P2 OUT · P3 IN · M1 OUT · M2 IN。
    关键点：`P1` 除 `M1` 外**没有别的攻击者**，故 `M1` 的 W2 辩护者为空（真"无人挡刀"）。
    """
    p1, p2, p3 = "ATOM-X-001::prop-1", "ATOM-Y-001::prop-1", "ATOM-Z-001::prop-1"
    m1, m2 = "MIS-X-001", "MIS-Y-001"

    def e(i: str, s: str, t: str, kind: str) -> dc.AttackEdge:
        return dc.AttackEdge(edge_id=i, source=s, target=t, kind=kind,
                             confidence="medium", human_verdict="approve")

    edges = [e("E1", m1, p1, "mis_to_prop"), e("E2", p1, m1, "prop_to_mis"),
             e("E3", m2, p2, "mis_to_prop")]
    cred = {p1: "high", p2: "low", p3: "low", m1: "low", m2: "high"}
    verdicts = dc.solve_verdicts(edges, cred)
    return edges, verdicts, cred


def test_fixture_verdicts_are_as_designed():
    """先把夹具本身的判决钉死（否则后面所有检测断言都建立在错误前提上）。"""
    _edges, verdicts, _cred = _synthetic()
    assert verdicts == {"ATOM-X-001::prop-1": "IN", "ATOM-Y-001::prop-1": "OUT",
                        "ATOM-Z-001::prop-1": "IN", "MIS-X-001": "OUT", "MIS-Y-001": "IN"}


def test_fixture_detectors_known_output():
    edges, verdicts, cred = _synthetic()
    props = [n for n in verdicts if dc.node_type_of(n, edges) == "proposition"]

    assert aa.detect_no_attacker_propositions(edges, props) == ["ATOM-Z-001::prop-1"]
    assert aa.detect_no_defender_mis(edges, verdicts, cred) == ["MIS-X-001"]
    assert aa.detect_no_defender_nodes(edges, verdicts, cred) == sorted(verdicts)
    comps = aa.detect_isolated_subgraphs(edges, aa.all_nodes(verdicts, edges))
    assert [len(c) for c in comps] == [1, 2, 2], comps
    assert comps[0] == ["ATOM-Z-001::prop-1"]
    assert aa.detect_unreviewed_edges(edges) == []


def test_fixture_credibility_gaps_semantics():
    """缺口判据的**语义**：high 为空 ⇒ 报结构性缺口；high 非空 ⇒ 不报。"""
    assert aa.detect_credibility_gaps({"a": "low", "b": "medium"})["gaps"], \
        "无 high 档必须报缺口"
    gaps = aa.detect_credibility_gaps({"a": "high", "b": "low"})
    assert gaps["distribution"] == {"high": 1, "medium": 0, "low": 1}
    assert gaps["total"] == 2 and gaps["gaps"] == []


def test_fixture_unreviewed_edges_detected():
    edges, _v, _c = _synthetic()
    edges[0].human_verdict = "unreviewed"
    assert [e.edge_id for e in aa.detect_unreviewed_edges(edges)] == ["E1"]


# ── 二、真实库：不变量（不锁数字 ⇒ 正常演进不红）────────────────────────────────
def test_detect_no_attacker_propositions():
    got = aa.detect_no_attacker_propositions(EDGES, PROPS)
    attacked = {e.target for e in EDGES}
    assert got == sorted(p for p in PROPS if p not in attacked) == sorted(got)


def test_detect_no_defender_mis():
    got = aa.detect_no_defender_mis(EDGES, VERDICTS, CRED)
    out = set(dc.stats(EDGES, VERDICTS, CRED)["out_nodes"])
    assert set(got) <= out, "无辩护者 MIS 必须都是 OUT"
    assert all(dc.node_type_of(n, EDGES) == "misconception" for n in got)
    assert all(not dc.get_defense_chain(n, EDGES, VERDICTS, CRED).w2_defenders for n in got)
    # 与权威源同一口径（同实现 ⇒ 一致性锁；真验证力在夹具测试）
    assert got == wd.out_mis_no_defender()


def test_detect_no_defender_nodes_total():
    got = aa.detect_no_defender_nodes(EDGES, VERDICTS, CRED)
    assert set(aa.detect_no_defender_mis(EDGES, VERDICTS, CRED)) <= set(got)
    assert all(not dc.get_defense_chain(n, EDGES, VERDICTS, CRED).w2_defenders for n in got)
    assert got == sorted(got) and len(got) == len(set(got))
    assert got == LIVE["no_defender_nodes"]


def test_detect_isolated_subgraphs():
    comps = aa.detect_isolated_subgraphs(EDGES, NODES)
    assert sum(len(c) for c in comps) == len(NODES), "分量必须是节点全集的划分"
    assert all(len(c) == len(set(c)) for c in comps)
    assert [len(c) for c in comps] == sorted(len(c) for c in comps), "按大小升序"
    assert len(comps) == LIVE["components"]["count"]
    assert sum(1 for c in comps if len(c) == 1) == LIVE["components"]["isolated"]


def test_detect_unreviewed_edges():
    assert aa.detect_unreviewed_edges(EDGES) == [], "人审全量完成 ⇒ 未审边 0"
    assert sum(1 for e in EDGES if e.human_verdict != "unreviewed") == len(EDGES)


def test_detect_credibility_gaps():
    """分布取自**入库产物**（独立路径）⇒ 有真实验证力（现算 vs 磁盘）。"""
    gaps = aa.detect_credibility_gaps(CRED)
    assert gaps["distribution"] == PIN["credibility_distribution"]
    assert gaps["total"] == len(CRED) == sum(gaps["distribution"].values())
    assert any("无 `high`" in g for g in gaps["gaps"]) == (gaps["distribution"]["high"] == 0)


# ── 三、真实库：跨源一致性（漂移告警）─────────────────────────────────────────
def test_authority_cross_source_consistent():
    d = wd.derived()
    assert d["consistent"], f"现算与入库产物不一致（漂移告警）：{d['mismatch']}"


# ── 四、CLI ───────────────────────────────────────────────────────────────────
def test_cli_basic_detectors(capsys):
    assert aa.main(["no-attackers"]) == 0
    lines = [x for x in capsys.readouterr().out.splitlines() if x.strip()]
    assert lines == wd.no_attacker_propositions()

    assert aa.main(["no-defenders"]) == 0
    out = [x for x in capsys.readouterr().out.strip().splitlines() if x.strip()]
    assert out == wd.out_mis_no_defender()

    assert aa.main(["isolated"]) == 0
    assert len([x for x in capsys.readouterr().out.splitlines() if x.strip()]) \
        == LIVE["components"]["isolated"]

    assert aa.main(["unreviewed"]) == 0
    assert capsys.readouterr().out.strip() == ""

    assert aa.main(["credibility-gaps", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["distribution"] == PIN["credibility_distribution"]


def test_check_consistency_strict():
    """不变量 + 跨源全绿（`check()` 已重写为**不变量**校验，不再锁快照数字）。"""
    assert aa.check() == []
    assert aa.main(["--check"]) == 0


def test_check_red_when_premise_changes():
    """前提变了（把 5 个**非 high** 节点的可信度改成 high）⇒ check 必须红。

    注：旧版把"改前 5 个 key"改成 high —— 那 5 个本来已是 high ⇒ **变异是空操作**，
    旧 check 之所以红只是因为它的写死数字过期（**恒红型无效测试**，640c §六.2 登记）。
    """
    targets = [k for k, v in CRED.items() if v != "high"][:5]
    assert targets, "库里必须存在非 high 节点（否则本用例无从构造变异）"
    bad_cred = dict(CRED)
    for k in targets:
        bad_cred[k] = "high"
    assert bad_cred != CRED, "变异必须真的改变前提"
    saved = aa.load_state

    def fake(*_a, **_k):
        return EDGES, VERDICTS, bad_cred

    aa.load_state = fake
    try:
        problems = aa.check()
        assert problems != [], "可信度分布被改还报 OK ⇒ 跨源校验形同虚设"
        assert any("可信度分布" in p for p in problems), problems
    finally:
        aa.load_state = saved


def test_check_red_when_product_missing(tmp_path: Path):
    """产物缺失 ⇒ 跨源校验无从进行 ⇒ 必须报（fail-loud，不静默放行）。"""
    problems = aa.check(None, None, tmp_path / "nope.json")
    assert any("W2 产物" in p for p in problems), problems
