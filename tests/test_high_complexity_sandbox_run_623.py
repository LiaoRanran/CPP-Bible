"""623 A2 · 80 条高复杂度带 mutation 沙箱实跑 单元测试（≥4 例）

覆盖：结果格式 / 沙箱运行可复现性 / 与 622 对比（触达规则数提升）/ 异常处理（缺失 target_card）。
不重复跑全量 80 条（已在 data/high_complexity_sandbox_run_623.json 落盘），仅做单条复现验证。
"""
from __future__ import annotations

import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")
MUT = os.path.join(ROOT, "data", "high_complexity_mutations_623.json")
SANDBOX = os.path.join(ROOT, "tools", "sandbox_apply_622.py")


def _load(path):
    spec = importlib.util.spec_from_file_location("mod_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sb = _load(SANDBOX)
res = json.load(open(RESULT, encoding="utf-8"))
muts = {m["mutation_id"]: m for m in json.load(open(MUT, encoding="utf-8"))}


def test_results_structure():
    assert res["total"] == 80
    assert "rows" in res and "distribution" in res and "escaped" in res
    assert len(res["rows"]) == 80
    assert res["distribution"]["blocked"] >= 40


def test_touched_rules_exceed_622():
    touched = set()
    for r in res["rows"]:
        touched.update(r.get("new_block_rules", []))
        touched.update(r.get("new_nonblock_rules", []))
    # 622 单轮触达 9 条；623 必须显著超越
    assert len(touched) > 9, f"应超过 622 的 9 条，实际 {len(touched)}"
    assert len(touched) >= 20


def test_escaped_are_content_removal_artifacts():
    esc = res["escaped"]
    assert len(esc) == 4
    for e in esc:
        # 全部是 M1 删除 claim_structured，消失的是 warn/内容级 findings
        assert "claim_structured" in (e.get("edit") or "")
        assert e.get("new_block_rules") == []  # 无新增 block（非真实安全逃逸）


def test_sandbox_reproducibility():
    # 取一条 blocked mutation，连跑两次，verdict 应一致（确定性）
    target = next(r for r in res["rows"] if r["verdict"] == "blocked")
    m = muts[target["mutation_id"]]
    content = json.loads(m["content"])
    card = content.get("target_card") or m.get("target_card")
    base = sb.Sandbox().gate_all()
    bf = sb.Sandbox.findings_for(base, card)
    r1 = sb.Sandbox().apply_and_run(m, card, bf)
    r2 = sb.Sandbox().apply_and_run(m, card, bf)
    assert r1["verdict"] == r2["verdict"], "同输入应得同判决（可复现）"


def test_exception_missing_target_card():
    m = {"mutation_id": "MUT-TEST", "content": json.dumps({"op": "M1", "field": "id"})}
    r = sb.Sandbox().apply_and_run(m, "", None)
    assert r["verdict"] == "infra_error"
