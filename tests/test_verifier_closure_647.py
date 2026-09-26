"""647 A3 · 信任根闭包扩展回归锁（编号 A3-1..A3-9）。

锁定：闭包覆盖 5 CORE_TOOLS + 67 规则指纹 + Authority schema + 透明日志 anchor +
tool_integrity 基线 + 证据库索引；**缺失即 FAIL**（不真删）；sha256 正确；与 tool_integrity 一致；
**不修改 641 闭包**（历史 run 的 digest 不能被这次扩展带跑）。
"""
from __future__ import annotations

import os

import tool_integrity as ti
import verifier_closure_641 as v641
import verifier_closure_647 as V


# ── A3-1：闭包覆盖全部新增信任根面 ──────────────────────────────────────────────
def test_a3_1_closure_covers_all_new_trust_roots():
    cl = V.build_closure()
    paths = {e["path"] for e in cl["files"]}
    for t in ti.CORE_TOOLS:
        assert f"tools/{t}" in paths, t
    for rel in V.EXTRA_FILES:
        assert rel in paths, rel
    assert V.RULESET_ID in paths
    assert cl["n_rules"] == 67
    assert cl["status"] == "OK"


# ── A3-2：闭包比 641 更大（扩展确实发生）───────────────────────────────────────
def test_a3_2_closure_strictly_larger_than_641():
    n641 = len(v641.closure_files())
    n647 = len(V.closure_files())
    assert n647 > n641, (n641, n647)
    assert set(v641.closure_files()) <= set(V.closure_files()), "641 闭包必须是子集（不回退）"


# ── A3-3：缺失即 FAIL（不真删）＋ 点名 ─────────────────────────────────────────
def test_a3_3_missing_trust_root_is_fail_not_warning():
    targets = ["tools/gate_engine.py", ti.SUPPLY_CHAIN_FILES[0], V.RULESET_ID]
    r = V.build_closure(missing=targets)
    assert r["status"] == "FAIL"
    assert r["missing"] == sorted(targets)
    assert r["digest"] != V.closure_digest()
    # 受控文件**一个都没被真删**
    for rel in targets[:-1]:
        assert os.path.isfile(os.path.join(V.ROOT, rel)), rel


# ── A3-4：sha256 正确（与直接读盘一致）────────────────────────────────────────
def test_a3_4_sha256_matches_disk():
    cl = V.build_closure()
    for e in cl["files"]:
        if e["path"] == V.RULESET_ID:
            assert e["sha256"] == V.ruleset_fingerprint()
            continue
        assert e["sha256"] == V._sha256_file(os.path.join(V.ROOT, e["path"])), e["path"]
        assert len(e["sha256"]) == 64


# ── A3-5：与 tool_integrity 一致（core 节 + supply_chain 节）───────────────────
def test_a3_5_consistent_with_tool_integrity():
    cl = V.build_closure()
    cons = V.consistency_with_tool_integrity(cl)
    assert cons["consistent"] is True, cons["mismatches"]
    assert cons["core_tools_in_closure"] == len(ti.CORE_TOOLS)
    assert cons["supply_chain_pinned"] == len(ti.SUPPLY_CHAIN_FILES)


# ── A3-6：规则集指纹对规则变化敏感（增删改 id 必须变）──────────────────────────
def test_a3_6_ruleset_fingerprint_sensitivity():
    fp = V.ruleset_fingerprint()
    assert len(fp) == 64
    ids = V.rule_ids()
    assert len(ids) == 67 and ids == sorted(ids)
    # 模拟"少一条规则" ⇒ 指纹必须变（不依赖真实改 gate_engine）
    import hashlib
    payload = "\n".join(ids[:-1])
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest() != fp


# ── A3-7：**不修改 641 闭包**（历史 digest 不能被带跑）─────────────────────────
def test_a3_7_641_closure_untouched():
    d641 = v641.closure_digest()
    _ = V.build_closure()          # 跑 647 闭包
    _ = V.closure_digest()
    assert v641.closure_digest() == d641, "647 扩展不得改动 641 的 digest"
    assert v641.build_closure()["status"] == "OK"


# ── A3-8：--simulate-missing CLI 语义（FAIL ⇒ exit 0，未缺失 ⇒ exit 1）─────────
def test_a3_8_simulate_missing_cli():
    assert V.main(["--simulate-missing", "tools/gate_engine.py"]) == 0
    assert V.main(["--simulate-missing", "data/__nope__.json"]) == 1


# ── A3-9：产物与自检 ─────────────────────────────────────────────────────────
def test_a3_9_report_and_selftest():
    assert V.selftest() == 0
    assert V.main(["--report"]) == 0
    assert os.path.isfile(V.OUT_MD) and os.path.isfile(V.OUT_JSON)
    import json
    doc = json.load(open(V.OUT_JSON, encoding="utf-8"))
    assert doc["closure"]["status"] == "OK"
    assert doc["consistency"]["consistent"] is True
    assert doc["attack"]["status"] == "FAIL"
