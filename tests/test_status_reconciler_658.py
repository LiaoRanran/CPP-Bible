"""658 D 段：status_reconciler_658 的反自证能力自检。

原则：这个测试**只**验证 reconciler 本身不依赖 queyi core、能独立产出事实、
能对账、且 tolerate 规则口径差。它不验证任何验证器语义。
"""
import importlib.util
import os
import sys

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


def test_reconcile_tolerates_rules_discrepancy():
    f = mod.observed_facts()
    baseline = {
        "git": {"head": f["head"], "ahead_of_origin_master": f["ahead_of_origin_master"],
                "behind_origin_master": f["behind_origin_master"]},
        "cards": {"atoms_total": f["cards_atoms_total"]},
        "graph": {"nodes": f.get("graph_nodes"), "links": f.get("graph_links")},
        "mutation": {"core_kill_rate_pct": f.get("mutation", {}).get("core"),
                     "all_kill_rate_pct": f.get("mutation", {}).get("all")},
        # rules 故意给错值，reconciler 必须容忍（不在 conflict 里）
        "rules": {"documented_brief": 67, "documented_actual_claim": 63},
    }
    conflicts = mod.reconcile(f, baseline)
    assert all("规则" not in c for c in conflicts), f"规则口径差不应判冲突: {conflicts}"
