"""596 任务2 · W2 可信度加权 AF 求解器回归锁。

锁四件事：
  * 正例：真实数据（194+194 候选边 / 121 节点）⇒ **IN=79 / OUT=42 / UNDEC=0**（594 实证对账）；
  * 反例 1：**缺对称边** ⇒ 退化（语义倒置：误解全 IN、命题无一 IN）——594 S1；
  * 反例 2：**W1 阈值加权**（单向边 + 阈值二值化）⇒ 退化（误解恒 IN）——594 W1；
  * 反例 3：**可信度相等** ⇒ 不构成击败（严格大于），AF 无攻击 ⇒ 误解同样不会 OUT（退化）。
另锁：不动点轮数 < 100、`--check` 可证伪（把结果改坏必须报错）。
"""
from __future__ import annotations

import json

import attack_edge_generator as aeg
import weighted_af_solver as w2


def _node(nid: str, kind: str, cred: int, conf: str = "low") -> dict:
    return {"id": nid, "type": kind, "confidence": conf, "credibility": cred}


def _edge(src: str, tgt: str, direction: str, conf: str = "low") -> dict:
    return {"source": src, "target": tgt, "direction": direction, "confidence": conf}


# ── 正例：沙箱小图 + 真实数据 ────────────────────────────────────────────────────
def test_sandbox_small_graph_prop_wins():
    """命题可信度 > 误解 ⇒ 命题击败误解：命题 IN、误解 OUT。"""
    nodes = {"ATOM-X::prop-1": _node("ATOM-X::prop-1", "proposition", 2, "medium"),
             "MIS-X": _node("MIS-X", "misconception", 1, "low")}
    edges = [_edge("MIS-X", "ATOM-X::prop-1", "mis_to_prop"),
             _edge("ATOM-X::prop-1", "MIS-X", "prop_to_mis")]
    defeats = w2.defeats_of(edges, nodes)
    assert defeats == {("ATOM-X::prop-1", "MIS-X")}
    labels, rounds = w2.grounded_labels(nodes, defeats)
    assert labels == {"ATOM-X::prop-1": "IN", "MIS-X": "OUT"} and rounds < w2.MAX_ROUNDS


def test_real_data_reproduces_594_grounded_result():
    """真实 79 命题 + 42 MIS ⇒ IN=79 / OUT=42 / UNDEC=0（594 实证，独立复算）。"""
    doc = w2.solve(w2.load_edges())
    s = doc["summary"]
    assert (s["IN"], s["OUT"], s["UNDEC"]) == (79, 42, 0), s
    assert s["nodes"] == 121 and s["IN_propositions"] == 79 and s["IN_misconceptions"] == 0
    assert doc["rounds"] < w2.MAX_ROUNDS, "不动点必须真收敛（不是撞上限）"
    props = [v for v in doc["nodes"].values() if v["type"] == "proposition"]
    mis = [v for v in doc["nodes"].values() if v["type"] == "misconception"]
    assert len(props) == 79 and len(mis) == 42
    assert all(v["label"] == "IN" for v in props) and all(v["label"] == "OUT" for v in mis)
    # 逐字段完整（任务书 596 任务2 的输出契约）
    for v in doc["nodes"].values():
        assert set(v) >= {"id", "type", "label", "defenders", "attackers", "defeated_attackers"}
        assert v["label"] in ("IN", "OUT", "UNDEC")
    # 实测：**4 条命题没有任何误解攻击**（ATOM-CONC-FENCE-001 / ATOM-CONC-LOCK-001 的命题）——
    # 这两张卡的关联记在**原子卡侧**的 `misconceptions` 字段（反向种子），本批按任务书只读
    # MIS 侧 `related_atoms` ⇒ 不产边（偏差 D5）。它们仍应 IN（无攻击者 ⇒ 立即 IN）。
    no_atk = sorted(v["id"] for v in props if not v["attackers"])
    assert len(no_atk) == 4, f"无攻击者命题数漂移：{no_atk}"
    assert all(v["label"] == "IN" for v in props if not v["attackers"])


def test_defeated_attackers_are_the_misconceptions():
    doc = w2.solve(w2.load_edges())
    sample = next(v for v in doc["nodes"].values()
                  if v["type"] == "proposition" and v["attackers"])
    assert sample["defeated_attackers"] == sample["attackers"], \
        "命题应击败它的每一个攻击者（误解）"
    mis = doc["nodes"][sample["attackers"][0]]
    assert mis["label"] == "OUT" and mis["attackers"], "误解应被命题击败且有自己的攻击者"


# ── 反例 1：缺对称边 ⇒ 语义倒置 ─────────────────────────────────────────────────
def test_no_symmetric_edges_degenerates_inversion():
    """只有 MIS→命题 单向边 ⇒ 两种走法都退化，命题都拿不到 IN。"""
    edges = [e for e in w2.load_edges() if e["direction"] == "mis_to_prop"]
    nodes = w2.build_graph(edges)
    props = {n for n, v in nodes.items() if v["type"] == "proposition"}

    # (a) 无权重单向 AF（594 S1）：所有边都算攻击 ⇒ 误解无入边恒 IN，被攻击的命题全被压成非 IN
    defeats_plain = {(str(e["source"]), str(e["target"])) for e in edges}
    attacked = {str(e["target"]) for e in edges}
    labels_plain, _ = w2.grounded_labels(nodes, defeats_plain)
    assert all(labels_plain[n] != "IN" for n in props & attacked), \
        "594 S1：单向 ⇒ 被攻击的命题无一 IN（语义倒置）"
    assert all(labels_plain[n] == "IN" for n in nodes if n not in props)

    # (b) 只用单向边跑 W2：误解可信度 1 不 > 命题 2 ⇒ 无击败 ⇒ 全 IN（另一种退化）
    assert w2.defeats_of(edges, nodes) == set()
    labels_w2, _ = w2.grounded_labels(nodes, set())
    assert set(labels_w2.values()) == {"IN"}, "无击败关系 ⇒ 误解同样被接受（退化）"


# ── 反例 2：W1 阈值加权 ⇒ 误解恒 IN ────────────────────────────────────────────
def test_w1_threshold_sweep_always_degenerates():
    """594 W1 失败复现：单向边 + 阈值二值化，θ 全程扫过，**误解始终全 IN**。"""
    one_way = [e for e in w2.load_edges() if e["direction"] == "mis_to_prop"]
    nodes = w2.build_graph(one_way)
    weights = {mid: w2.w1_weight(info["refutations"])
               for mid, info in aeg.read_mis().items()}
    mis = [n for n, v in nodes.items() if v["type"] == "misconception"]
    for theta in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        labels = w2.w1_threshold_labels(nodes, one_way, weights, theta)
        assert all(labels[m] == "IN" for m in mis), \
            f"θ={theta}：W1 竟然把误解判出局了 —— 与 594 实证矛盾"
        assert labels != {n: "OUT" for n in mis}, "退化：不可能出现'误解全 OUT'"


# ── 反例 3：可信度相等 ⇒ 不构成击败（严格大于）────────────────────────────────
def test_equal_credibility_never_defeats():
    nodes = {"P": _node("P", "proposition", 2, "medium"),
             "M": _node("M", "misconception", 2, "medium")}
    edges = [_edge("M", "P", "mis_to_prop", "medium"), _edge("P", "M", "prop_to_mis", "medium")]
    assert w2.defeats_of(edges, nodes) == set(), "相等可信度绝不许构成击败（严格大于）"
    labels, rounds = w2.grounded_labels(nodes, set())
    assert set(labels.values()) == {"IN"} and rounds < w2.MAX_ROUNDS
    # 严格大于才击败：差一级就成立
    nodes2 = dict(nodes)
    nodes2["M"] = _node("M", "misconception", 1, "low")
    assert w2.defeats_of(edges, nodes2) == {("P", "M")}


# ── 不动点 / 幂等 / 校验 ───────────────────────────────────────────────────────
def test_fixpoint_and_idempotence(tmp_path):
    doc1 = w2.solve(w2.load_edges())
    doc2 = w2.solve(w2.load_edges())
    assert doc1 == doc2, "同输入两次求解必须完全一致"
    p1 = w2.write_labels(doc1, tmp_path / "a.json")
    p2 = w2.write_labels(doc2, tmp_path / "b.json")
    assert p1.read_bytes() == p2.read_bytes()


def test_check_is_falsifiable(tmp_path):
    doc = w2.solve(w2.load_edges())
    assert w2.check(doc) == []
    # 可证伪 1：把一条命题改成 OUT
    bad = json.loads(json.dumps(doc))
    victim = next(k for k, v in bad["nodes"].items() if v["type"] == "proposition")
    bad["nodes"][victim]["label"] = "OUT"
    bad["summary"]["IN"] = 78
    assert any("不符" in p or "命题被判 OUT" in p for p in w2.check(bad))
    # 可证伪 2：把一条误解改成 IN
    bad2 = json.loads(json.dumps(doc))
    mid = next(k for k, v in bad2["nodes"].items() if v["type"] == "misconception")
    bad2["nodes"][mid]["label"] = "IN"
    assert any("误解被判 IN" in p for p in w2.check(bad2))
    # 可证伪 3：未收敛（撞上限）
    bad3 = json.loads(json.dumps(doc))
    bad3["rounds"] = w2.MAX_ROUNDS
    assert any("未真正收敛" in p for p in w2.check(bad3))


def test_cli_solve_stats_check_exit_codes(tmp_path):
    out = tmp_path / "labels.json"
    assert w2.main(["solve", "--edges", str(w2.DEFAULT_EDGES), "--out", str(out)]) == 0
    assert out.is_file()
    assert w2.main(["stats", "--edges", str(w2.DEFAULT_EDGES), "--out", str(out), "--json"]) == 0
    assert w2.main(["--check", "--out", str(out)]) == 0
    out.write_text("{}\n", encoding="utf-8")
    assert w2.main(["--check", "--out", str(out)]) == 2
