"""625 C1 · PathConfig 路径解耦回归测试（≥8 例）。"""
import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import path_config_625 as pc  # noqa: E402

AUX20 = ["golden_lock", "debt_ledger", "governance_doc_guard", "supply_chain", "metrics_collector",
         "mutation_fuzz", "weighted_af_solver", "replay_invariants", "merkle_integrity",
         "attack_edge_generator", "knowledge_graph", "defense_chain", "escape_rate_honest_613",
         "human_review_queue", "human_review_dashboard", "exemption_expiry", "learner_state",
         "prop_graph", "ci_local_precheck", "trust_root_status_check"]
CORE6 = ["gate_engine", "atom_evidence_replay", "poison_drill", "tool_integrity", "toolchain", "cppbible"]


def test_default_root_is_repo_root():
    assert pc.root() == pc.DEFAULT_ROOT


def test_resolve_functions():
    assert pc.resolve_atom_path("ATOM-X") == pc.atoms_dir() / "ATOM-X.md"
    assert pc.resolve_evidence_path("EV-X") == pc.evidence_dir() / "EV-X.md"
    assert pc.resolve_data_path("a.json") == pc.data_dir() / "a.json"
    assert pc.resolve_mutation_path("m1").name == "m1.json"


def test_env_override_root(monkeypatch, tmp_path):
    monkeypatch.setenv("QUEYI_ROOT", str(tmp_path))
    assert pc.root() == tmp_path
    assert pc.atoms_dir() == tmp_path / "atoms"


def test_env_override_subdir(monkeypatch, tmp_path):
    monkeypatch.setenv("QUEYI_ATOMS_DIR", str(tmp_path / "a"))
    assert pc.atoms_dir() == tmp_path / "a"


def test_config_file_override(monkeypatch, tmp_path):
    cfg = tmp_path / "queyi_config.json"
    cfg.write_text(json.dumps({"evidence_dir": str(tmp_path / "ev")}), encoding="utf-8")
    monkeypatch.setenv("QUEYI_CONFIG", str(cfg))
    monkeypatch.delenv("QUEYI_EVIDENCE_DIR", raising=False)
    assert pc.evidence_dir() == tmp_path / "ev"


def test_core_tools_use_pathconfig():
    for m in CORE6:
        src = open(os.path.join(ROOT, "tools", m + ".py"), encoding="utf-8").read()
        assert "path_config_625" in src, f"{m} 未接入 PathConfig"


def test_aux_tools_use_pathconfig():
    for m in AUX20:
        src = open(os.path.join(ROOT, "tools", m + ".py"), encoding="utf-8").read()
        assert "path_config_625" in src, f"{m} 未接入 PathConfig"


def test_backward_compat_identity_without_env(monkeypatch):
    for k in ("QUEYI_ROOT", "QUEYI_ATOMS_DIR", "QUEYI_EVIDENCE_DIR", "QUEYI_DATA_DIR",
              "QUEYI_EXAMPLES_DIR", "QUEYI_BOOK_DIR", "QUEYI_CONFIG"):
        monkeypatch.delenv(k, raising=False)
    importlib.reload(pc)
    assert pc.root() == pc.DEFAULT_ROOT
    assert pc.atoms_dir() == pc.DEFAULT_ROOT / "atoms"
    assert pc.evidence_dir() == pc.DEFAULT_ROOT / "evidence"


def test_validate_and_selftest():
    assert pc.validate() == []
    assert pc.selftest() == 0


def test_report_exists():
    p = os.path.join(ROOT, "data", "path_config_625.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
