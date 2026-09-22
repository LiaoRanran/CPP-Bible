"""625 D1 · 尺子入根 22→>30 回归测试（≥4 例）。"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tool_integrity as ti  # noqa: E402

_TC = "# test_config"
_SC = "# supply_chain"
_RL = "# ruler"


def _section_count(mark: str) -> int:
    txt = open(os.path.join(ROOT, "tools", ".tool_checksums"), encoding="utf-8").read()
    lines = txt.splitlines()
    out = 0
    started = False
    for ln in lines:
        if ln.strip() == mark:
            started = True
            continue
        if started:
            if ln.startswith("# "):
                break
            if re.search(r"\.(py|toml|yaml|json)$", ln.strip()):
                out += 1
    return out


def test_ruler_tools_extended_to_22():
    assert len(ti.RULER_TOOLS) == 22, f"RULER_TOOLS 应为 22，实际 {len(ti.RULER_TOOLS)}"


def test_total_nailed_exceeds_30():
    total = (5 + _section_count(_TC) + _section_count(_SC) + _section_count(_RL))
    assert total > 30, f"入根总数应 >30，实际 {total}"
    assert total == 34, f"预期 34，实际 {total}"


def test_new_rulers_present():
    added = {"weighted_af_solver.py", "debt_ledger.py", "governance_doc_guard.py",
             "human_review_queue.py", "exemption_expiry.py", "metrics_collector.py",
             "merkle_integrity.py", "supply_chain.py",
             "authority_to_annotations_sync_623.py", "escape_rate_honest_613.py",
             "pck_certificate_verifier_619.py", "defense_chain.py"}
    assert added.issubset(set(ti.RULER_TOOLS))


def test_integrity_check_passes():
    rc = ti.main(["--check"])
    assert rc == 0


def test_d1_no_core_logic_changed():
    # 仅扩展 RULER_TOOLS 元组，CORE_TOOLS 不变
    assert ti.CORE_TOOLS == ("gate_engine.py", "atom_evidence_replay.py",
                             "poison_drill.py", "toolchain.py", "cppbible.py")
