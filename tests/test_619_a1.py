"""619 A1 单测：攻击目标函数 v1（tools/adversarial_objective_619.py）

纯函数验证：确定性、口径一致性、子目标代理、n_a/等效处理、`--check` 自检。
不写盘、不 import mutation_fuzz。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adversarial_objective_619 as A  # noqa: E402

ESC = {"card": "c", "op": "M1", "point": "删 negative_controls", "verdict": "escaped",
       "kind": None, "new_block": [], "new_warn": [], "equivalent": False}
WARN = {"card": "c", "op": "M2", "point": "路径转大写（A → B）", "verdict": "blocked",
        "kind": "warn_only", "new_block": [], "new_warn": ["CARD-PATH-NOT-CANONICAL:x"], "equivalent": False}
SHA = {"card": "c", "op": "M7", "point": "sha256 改一位（abc → abd）", "verdict": "blocked",
       "kind": "strict", "new_block": ["EV-ARTIFACT-PRODUCER:x"], "new_warn": [], "equivalent": False}
NA = {"card": "c", "op": "M1", "point": "-", "verdict": "n_a",
      "kind": None, "new_block": [], "new_warn": [], "equivalent": False}
EQ = {"card": "c", "op": "M6", "point": "块式 → flow 写法（matrix）", "verdict": "escaped",
      "kind": None, "new_block": [], "new_warn": [], "equivalent": True}
STRICT_GEN = {"card": "c", "op": "M1", "point": "删 artifact_sha256", "verdict": "blocked",
              "kind": "strict", "new_block": ["EV-FM-REQUIRED:x"], "new_warn": [], "equivalent": False}


def test_weights_sum_is_one():
    assert A.weights_sum() == 1.0


def test_declared_5_subgoals_4_computable():
    assert len(A.DECLARED_SUB_GOALS) == 5
    assert len(A.COMPUTABLE_SUB_GOALS) == 4


def test_determinism():
    assert A.score_result(ESC) == A.score_result(ESC)


def test_verifier_disagreement_is_na():
    assert A.sub_verifier_disagreement(STRICT_GEN) is None


def test_na_excluded_from_denominator():
    sc = A.score_result(NA)
    assert sc["composite"] is None
    assert sc["judgeable"] is False
    assert sc["severity"] == "not_judgeable"


def test_real_escape_outranks_warn_only_path():
    assert A.score_result(ESC)["composite"] > A.score_result(WARN)["composite"]


def test_warn_only_no_double_count():
    sc = A.score_result(WARN)
    assert sc["sub"]["verdict_regime_disagreement"] == 1.0
    assert sc["sub"]["rule_blind_spot"] == 0.0


def test_generic_rule_block_is_blind_spot_06():
    assert A.score_result(STRICT_GEN)["sub"]["rule_blind_spot"] == 0.6


def test_sha256_triggers_provenance():
    assert A.score_result(SHA)["sub"]["provenance_inconsistency"] == 1.0


def test_equivalent_excluded_from_ranking():
    sc = A.score_result(EQ)
    assert sc["known_equivalent"] is True
    assert sc["ranked"] is False


def test_pareto_front_contains_true_escape():
    rows = A.pareto_rows([ESC, WARN, SHA, NA])
    front = A.pareto_front(rows)
    assert A.variant_id(ESC) in front


def test_check_runs_clean():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "adversarial_objective_619.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
