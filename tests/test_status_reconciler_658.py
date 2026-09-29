# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""658 D 段：status_reconciler_658 的反自证能力自检。

原则：这个测试**只**验证 reconciler 本身不依赖 queyi core、能独立产出事实、
能对账、且 tolerate 规则口径差。它不验证任何验证器语义。
"""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "status_reconciler_658", os.path.join(ROOT, "tools", "status_reconciler_658.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_reconciler_is_core_free():
    # 反自证：reconciler 源码不得 *import* gate_engine / four_state / queyi core
    # （文档字符串里提到这些名字是允许的，只禁止真实 import 语句）
    src = open(os.path.join(ROOT, "tools", "status_reconciler_658.py"), encoding="utf-8").read()
    for line in src.splitlines():
        s = line.strip()
        if s.startswith(("import ", "from ")):
            assert "gate_engine" not in s, "reconciler 不得 import gate_engine"
            assert "four_state_verdict" not in s, "reconciler 不得 import four_state_verdict"
            assert "import queyi" not in s, "reconciler 不得 import queyi core"


def test_observed_facts_shape():
    f = mod.observed_facts()
    assert isinstance(f, dict)
    assert f["head"]
    assert "ahead_of_origin_master" in f
    assert "cards_atoms_total" in f


def test_reconcile_rules_converged_to_gate_rules():
    f = mod.observed_facts()
    # 660 B5：口径已收敛为 data/_gate_rules.json 实测，baseline 写实际数则无冲突
    baseline = {
        "git": {"head": f["head"], "ahead_of_origin_master": f["ahead_of_origin_master"],
                "behind_origin_master": f["behind_origin_master"]},
        "cards": {"atoms_total": f["cards_atoms_total"]},
        "graph": {"nodes": f.get("graph_nodes"), "links": f.get("graph_links")},
        "mutation": {"core_kill_rate_pct": f.get("mutation", {}).get("core"),
                     "all_kill_rate_pct": f.get("mutation", {}).get("all")},
        "rules": {"documented_brief": f["rules_actual"], "documented_actual_claim": f["rules_actual"]},
    }
    conflicts = mod.reconcile(f, baseline)
    assert all("规则" not in c for c in conflicts), f"规则已收敛为实际数，不应判冲突: {conflicts}"
    # 661 A2：口径裁定为 67（gate_engine.RULES 执行权威；_gate_rules.json 已同步 67）
    assert f["rules_actual"] == 67, f"规则实际数应为 67，得 {f['rules_actual']}"
    # 反证：baseline 仍写 stale 63 时，reconciler 必须抓出
    stale = {**baseline, "rules": {"documented_brief": 63, "documented_actual_claim": 63}}
    c2 = mod.reconcile(f, stale)
    assert any("规则" in c for c in c2), f"baseline 写 63(stale) 应被对账抓出: {c2}"
