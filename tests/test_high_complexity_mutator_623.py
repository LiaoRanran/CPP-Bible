"""623 A1 · 高复杂度带 mutation 生成器单元测试（≥8 例）

覆盖：4 策略各 1 例 + 复杂度评分 + 规则触达预测 + 去重 + 异常处理。
另含沙箱新算子（MSET/M16/M31/M32/M34/M35/M36/M37/M40）与生成器端到端集成。
"""
from __future__ import annotations

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "high_complexity_mutator_623.py")
SANDBOX = os.path.join(ROOT, "tools", "sandbox_apply_622.py")


def _load(path):
    spec = importlib.util.spec_from_file_location("mod_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = _load(TOOL)


def test_generate_count():
    muts = mod.build_mutations()
    assert len(muts) == 80, f"应为 80 条，实际 {len(muts)}"


def test_strategy_coverage():
    muts = mod.build_mutations()
    strats = {m["attack_type"] for m in muts}
    assert {"H1", "H2", "H3", "H4"}.issubset(strats), "4 策略 H1–H4 必须均出现"


def test_complexity_over_60():
    muts = mod.build_mutations()
    assert all(m["complexity"] > 60 for m in muts), "所有 mutation 复杂度应 >60"


def test_predicted_rules_nonempty():
    muts = mod.build_mutations()
    assert all(len(m["predicted_rules"]) >= 1 for m in muts), "每条预测触达规则非空"


def test_schema_aware():
    muts = mod.build_mutations()
    atoms, evs = mod.collect_cards()
    cardmap = {c["rel"]: c for c in atoms + evs}
    for m in muts:
        c = cardmap.get(m["target_card"])
        need = __import__("json").loads(m["content"]).get("field")
        assert c is not None, f"目标卡缺失 {m['target_card']}"
        if need:
            assert mod._key_present(c["fm"], need), f"{m['target_card']} 缺字段 {need}"


def test_dedup_unique_ids():
    muts = mod.build_mutations()
    ids = [m["mutation_id"] for m in muts]
    assert len(ids) == len(set(ids)), "mutation_id 必须唯一"


def test_exception_handling_missing_dir():
    save_a, save_e = mod.ATOMS_DIR, mod.EVIDENCE_DIR
    try:
        mod.ATOMS_DIR = os.path.join(ROOT, "no_atoms_623")
        mod.EVIDENCE_DIR = os.path.join(ROOT, "no_ev_623")
        assert mod.build_mutations() == [], "卡目录缺失应优雅返回空列表"
    finally:
        mod.ATOMS_DIR, mod.EVIDENCE_DIR = save_a, save_e


def test_rule_distribution_ge_30():
    muts = mod.build_mutations()
    rules = {m["target_rule"] for m in muts}
    assert len(rules) >= 30, f"覆盖规则数应 ≥30，实际 {len(rules)}"


def test_content_parse():
    muts = mod.build_mutations()
    import json
    for m in muts:
        assert isinstance(json.loads(m["content"]), dict)


def test_sandbox_new_ops_apply():
    sb = _load(SANDBOX)
    t = (
        "---\nid: ATOM-X-001\nstatus: verified\nsuperiority: better\n"
        "relations:\n - supports: ATOM-Y-002\nrun_match_keys:\n - a\n"
        'artifact_assert:\n - {kind: exists, text: "sym"}\ncommand: g++ x.cpp\n---\nbody\n'
    )
    for op, c in [
        ("MSET", {"op": "MSET", "field": "status", "value": "bogus_enum"}),
        ("M16", {"op": "M16"}),
        ("M31", {"op": "M31"}),
        ("M32", {"op": "M32"}),
        ("M34", {"op": "M34"}),
        ("M35", {"op": "M35"}),
        ("M36", {"op": "M36"}),
        ("M37", {"op": "M37"}),
        ("M40", {"op": "M40"}),
    ]:
        r = sb.plan_edit(c, t)
        assert r is not None, f"新算子 {op} 应可施加"
