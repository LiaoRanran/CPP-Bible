"""609 C3 · 论证 CLI 回归锁（status/proposition/mis/card/defense/--check）。

锁六件事（任务书 6 例）：
  1. `status` 出判决分布（IN/OUT/UNDEC + 节点数）；
  2. `proposition <id>` 出命题详情；传了 MIS id ⇒ 明确拒绝（不许张冠李戴）；
  3. `mis <id>` 出误解详情；传了命题 id ⇒ 明确拒绝；
  4. `card <card>` 按证据卡反查（查不到要明说，不许返回空还说"通过"）；
  5. `defense <id>` 的辩护链 **精确到边级**：四段齐全，边 id 形如 `ae-<source>-><target>`；
  6. `--check` 结构合法 exit 0；`defense` 不存在的节点 ⇒ 明说"不存在"。
"""
from __future__ import annotations

import json

import grounded_cli as gcli

DOC = gcli.load_doc()
EDGES = gcli.load_edges()
PROP = sorted(n for n, v in DOC["nodes"].items() if v["type"] == "proposition")[0]
MIS = sorted(n for n, v in DOC["nodes"].items() if v["type"] == "misconception")[0]


def test_status_prints_verdict_distribution():
    s = gcli.render_status(DOC)
    for key in ("IN", "OUT", "UNDEC", "节点", "击败边"):
        assert key in s, f"status 缺 {key}"
    assert str(DOC["summary"]["IN"]) in s


def test_proposition_detail_and_type_mismatch():
    out = gcli._detail(DOC, PROP, EDGES, want_type="proposition")
    assert PROP in out and "proposition" in out and "攻击者" in out
    assert "不是 proposition" in gcli._detail(DOC, MIS, EDGES, want_type="proposition")


def test_mis_detail_and_type_mismatch():
    out = gcli._detail(DOC, MIS, EDGES, want_type="misconception")
    assert MIS in out and "misconception" in out
    assert "不是 misconception" in gcli._detail(DOC, PROP, EDGES, want_type="misconception")


def test_card_lookup_and_miss_is_explicit():
    card = next(v["card"] for v in DOC["nodes"].values() if v.get("card"))
    out = gcli.render_card(DOC, card)
    assert card in out and out.count("- `") >= 1
    assert "没有节点挂" in gcli.render_card(DOC, "EV-DOES-NOT-EXIST")


def test_defense_chain_is_edge_precise():
    out = gcli.render_defense(DOC, PROP, EDGES)
    for seg in ("## 1.", "## 2.", "## 3.", "## 4."):
        assert seg in out, f"辩护链缺第 {seg} 段"
    v = DOC["nodes"][PROP]
    if v["attackers"]:
        first = sorted(v["attackers"])[0]
        assert f"ae-{first}->{PROP}" in out, "辩护链没精确到边级（缺 ae-<source>-><target> id）"
    assert "可信度" in out and "严格大于" in out


def test_cli_commands_exit_zero_and_missing_node_is_explicit(capsys):
    for argv in (["status"], ["proposition", PROP], ["mis", MIS], ["defense", PROP]):
        assert gcli.main(argv) == 0, f"{argv} 退出码非 0"
    cards = sorted({v["card"] for v in DOC["nodes"].values() if v.get("card")})
    assert gcli.main(["card", cards[0]]) == 0
    assert gcli.main(["defense", "NO-SUCH-NODE"]) == 0
    assert "节点不存在" in capsys.readouterr().out
    assert gcli.main(["--check"]) == 0


def test_check_flags_broken_document(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"nodes": {"A": {"type": "weird", "label": "?"}},
                               "summary": {"nodes": 1}}), encoding="utf-8")
    assert gcli.check(bad) != []
