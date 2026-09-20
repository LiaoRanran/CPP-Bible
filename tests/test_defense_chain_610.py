"""610 B1 · 辩护链核心引擎回归锁（只读 · 确定性推理）。

锁十件事（任务书 B1 的 10 例）：
  1. load_data：388 边 / 121 节点 / IN114-OUT7 / 可信度 medium 114 + low 7 + high 0；
  2. is_defeating：命题(medium)→MIS(low) = True；MIS(medium)→命题(medium) = False；
  3. MIS-LANG-001（OUT）：有攻击者、**无 W2 辩护者**、defeated_by 非空；
  4. ATOM-UB-GRAY-001::prop-1（IN）：有 10 个攻击者、defeated_by 空、击败 4 个攻击者；
  5. MIS-MEM-002（IN，approve ⇒ medium）：defeated_by 空（同档不构成击败）；
  6. what_if(MIS-LANG-001, medium) ⇒ OUT→IN，总 IN **115** / OUT **6**；
  7. what_if(MIS-MEM-002, low) ⇒ IN→OUT，总 OUT **8**；
  8. what_if_overturned(命题) ⇒ forced_out=True 且受影响节点非空；
  9. find_min_attack_set(ATOM-UB-GRAY-001::prop-1) ⇒ {'MIS-CONC-001'} 且 achieved=True；
 10. batch_report：五节齐全 + 关键数字（IN114/OUT7/击败边 17）。

⚠️ 本引擎的口径 = **modify 保持 low**（实测与入库 `grounded_labels_w2.json` **逐节点一致**，
由 `defense_chain.check()` 单独锁死）；609 A3 的 `modify⇒new_confidence` 口径会得 IN121/OUT0。
"""
from __future__ import annotations

import json
from pathlib import Path

import defense_chain as dc

EDGES, VERDICTS, CRED = dc.load_data()
PROP = "ATOM-UB-GRAY-001::prop-1"
OUT_MIS = "MIS-LANG-001"
IN_MIS = "MIS-MEM-002"


def test_load_data():
    assert len(EDGES) == 388
    assert len(VERDICTS) == 121
    s = dc.solve_summary(EDGES, CRED)
    assert (s["in"], s["out"], s["undec"]) == (114, 7, 0)
    assert s["defeating_edges"] == 17 and s["rounds"] == 3
    dist = {k: sum(1 for v in CRED.values() if v == k) for k in ("high", "medium", "low")}
    assert dist == {"high": 0, "medium": 114, "low": 7}


def test_is_defeating():
    prop_to_mis = next(e for e in EDGES if e.kind == "prop_to_mis"
                       and VERDICTS[e.target] == "OUT")
    mis_to_prop = next(e for e in EDGES if e.kind == "mis_to_prop"
                       and VERDICTS[e.source] == "IN")
    assert dc.is_defeating(prop_to_mis, CRED) is True, "命题(medium) → MIS(low) 应构成击败"
    assert dc.is_defeating(mis_to_prop, CRED) is False, "MIS(medium) → 命题(medium) 不构成击败"


def test_defense_chain_out_node():
    c = dc.get_defense_chain(OUT_MIS, EDGES, VERDICTS, CRED)
    assert c.verdict == "OUT" and c.credibility == "low"
    assert len(c.attackers) == 3 and c.defeated_by, "OUT 节点必须有击败它的攻击者"
    assert len(c.defeated_by) == 3
    assert c.w2_defenders == [], "MIS-LANG-001 无 W2 辩护者（无人替它挡刀）"
    assert c.defeats == []


def test_defense_chain_in_proposition():
    c = dc.get_defense_chain(PROP, EDGES, VERDICTS, CRED)
    assert c.verdict == "IN" and c.node_type == "proposition"
    assert len(c.attackers) == 10 and c.defeated_by == []
    assert len(c.defeats) == 4, "它击败 4 个攻击者（low 档 MIS）"
    assert len(c.w2_defenders) == 1


def test_defense_chain_in_mis():
    c = dc.get_defense_chain(IN_MIS, EDGES, VERDICTS, CRED)
    assert c.verdict == "IN" and c.credibility == "medium"
    assert c.attackers and c.defeated_by == [], "approve 后同档 ⇒ 不被击败"
    assert len(c.w2_defenders) == 5


def test_what_if_approve_out_mis():
    res = dc.what_if(OUT_MIS, "medium", EDGES, VERDICTS, CRED)
    assert res["changed_nodes"] == [{"node_id": OUT_MIS, "old_verdict": "OUT",
                                     "new_verdict": "IN"}]
    assert res["total_in"] == 115 and res["total_out"] == 6 and res["total_undec"] == 0
    assert res["defeating_edges"] == 14, "该 MIS 的 3 条击败边消失 ⇒ 17-3=14"


def test_what_if_modify_in_mis():
    res = dc.what_if(IN_MIS, "low", EDGES, VERDICTS, CRED)
    assert res["changed_nodes"][0]["node_id"] == IN_MIS
    assert res["total_out"] == 8 and res["total_in"] == 113


def test_what_if_overturned_proposition():
    res = dc.what_if_overturned(PROP, EDGES, VERDICTS, CRED)
    assert res["forced_out"] is True and res["overturned_self_verdict"] == "OUT"
    assert res["affected_nodes"], "推翻一个被 10 个 MIS 攻击的命题必有连带影响"
    assert PROP in res["affected_nodes"]
    assert res["total_out"] == 8


def test_find_min_attack_set():
    res = dc.find_min_attack_set(PROP, EDGES, CRED, verdicts=VERDICTS)
    assert res["achieved"] is True
    assert res["set"] == ["MIS-CONC-001"], f"实测贪心解：{res['set']}"
    assert "贪心近似" in res["note"]
    already = dc.find_min_attack_set(OUT_MIS, EDGES, CRED, verdicts=VERDICTS)
    assert already == {"target": OUT_MIS, "set": [], "achieved": True,
                       "note": "目标本来就是 OUT ⇒ 空集已达成"}


def test_batch_report(tmp_path: Path):
    text = dc.batch_report(EDGES, VERDICTS, CRED)
    for sec in ("## 1. 总览", "## 2. OUT 节点", "## 3. 无辩护者的节点",
                "## 4. 无攻击者的命题", "## 5. 逐节点辩护链"):
        assert sec in text, f"报告缺小节：{sec}"
    assert "IN 114 / OUT 7 / UNDEC 0" in text and "击败边 **17**" in text
    assert "`MIS-LANG-001`" in text and "`ATOM-CONC-FENCE-001::prop-1`" in text
    p = tmp_path / "rep.md"
    assert dc.main(["report", "--out", str(p)]) == 0
    assert p.read_text(encoding="utf-8") == text


def test_check_matches_authoritative_w2_artifact():
    """与入库 W2 产物**逐节点**一致（含数字档 credibility 映射）⇒ exit 0。"""
    assert dc.check() == []
    st = dc.stats(EDGES, VERDICTS, CRED)
    assert st["no_defenders"] == 7 and st["no_attackers"] == 4
    auth = json.loads((dc.ROOT / "data" / "grounded_labels_w2.json").read_text(encoding="utf-8"))
    assert auth["summary"]["IN"] == 114 and auth["defeating_edges"] == 17
