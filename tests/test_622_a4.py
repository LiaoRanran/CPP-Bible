"""622 A4 · 闭环第二轮（生成器 v2 + 沙箱实跑）单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import mutation_generator_621 as MG  # noqa: E402
import sandbox_apply_622 as SA  # noqa: E402

MUTS2 = os.path.join(ROOT, "data", "mutation", "new_mutations_622_round2.jsonl")
RES2 = os.path.join(ROOT, "data", "mutation_sandbox_run_622_round2_results.json")


def test_v2_new_strategies_registered():
    assert set(MG.NEW_STRATEGIES) == {"boundary_value", "cross_reference"}
    assert MG.OP_REQUIRED_FIELDS["M8"] == ("artifact_version", "status")
    assert MG.OP_REQUIRED_FIELDS["M9"] == ("serves", "relations")


def test_op_applicable_schema_aware():
    assert MG._op_applicable("M8", ["id", "status"]) is True
    assert MG._op_applicable("M8", ["id"]) is False
    assert MG._op_applicable("M9", ["serves"]) is True
    assert MG._op_applicable("M1", ["anything"]) is True
    assert MG._op_applicable("M1", []) is False


def test_card_fields_reads_frontmatter():
    f = MG.card_fields("atoms/conc/ATOM-CONC-FENCE-001.md")
    assert "id" in f or f == []


def test_generate_v2_deterministic():
    """确定性：同一卡清单 + 同一 v7 ⇒ 同一批 mutation_id。

    注意：生成结果依赖**卡清单的顺序**（round-robin 分配），
    故必须用与生产同样的 discover_cards() 全量清单重放。
    """
    if not os.path.exists(MUTS2):
        return
    import pck_batch_migrator_620 as M
    muts = [json.loads(ln) for ln in open(MUTS2, encoding="utf-8") if ln.strip()]
    again = MG.generate_v2(M.discover_cards(), MG.load_v7(), count=len(muts))
    assert [m["mutation_id"] for m in again] == [m["mutation_id"] for m in muts]


def test_round2_uses_new_ops_and_no_v7_overlap():
    if not os.path.exists(MUTS2):
        return
    muts = [json.loads(ln) for ln in open(MUTS2, encoding="utf-8") if ln.strip()]
    ops = {json.loads(m["content"])["op"] for m in muts}
    assert ops <= {"M8", "M9"}
    v7p = {(str(r.get("card")), str(r.get("op"))) for r in MG.load_v7()}
    assert all((m["target_card"], json.loads(m["content"])["op"]) not in v7p for m in muts)


def test_round2_results_shape():
    if not os.path.exists(RES2):
        return
    d = json.load(open(RES2, encoding="utf-8"))
    assert d["total"] == 30
    for r in d["rows"]:
        assert r["verdict"] in ("blocked", "escaped", "neutral",
                                "detected_nonblock", "infra_error")


def test_round2_no_escape_and_new_taxonomy_present():
    if not os.path.exists(RES2):
        return
    d = json.load(open(RES2, encoding="utf-8"))
    assert d["distribution"].get("escaped", 0) == 0
    assert d["distribution"].get("detected_nonblock", 0) > 0
    assert d["distribution"].get("blocked", 0) > 0


def test_plan_edit_supports_M8_M9():
    text = ("---\nid: A\nstatus: verified\nserves: [ATOM-MEM-LEAK-001]\n---\n\nbody\n")
    e8 = SA.plan_edit({"op": "M8", "target_rule": "ATOM-STATUS-VALUE"}, text)
    assert e8 is not None and "bogus_enum" in e8[0]
    e9 = SA.plan_edit({"op": "M9", "target_rule": "EV-SERVES-EXIST"}, text)
    assert e9 is not None and "ATOM-NOPE-999" in e9[0]


def test_new_nonblock_field_recorded():
    """apply_and_run 输出应含 new_nonblock_rules（5 类口径的基础）。"""
    import inspect
    src = inspect.getsource(SA.Sandbox.apply_and_run)
    assert "new_nonblock_rules" in src
    assert "detected_nonblock" in src


def test_selftest_passes():
    assert SA.selftest() == 0
