"""619 A2 单测：攻击者原型（tools/adversarial_attacker_619.py）

不写盘、不 import mutation_fuzz / gate_engine。验证排序、契约校验、去重帕累托、等价/na 剔除。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adversarial_attacker_619 as T  # noqa: E402

RECORDS = [
    {"card": "c", "op": "M1", "point": "删 negative_controls", "verdict": "escaped",
     "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M2", "point": "路径转大写（A → B）", "verdict": "blocked",
     "kind": "warn_only", "new_block": [], "new_warn": ["CARD-PATH-NOT-CANONICAL:x"], "equivalent": False},
    {"card": "c", "op": "M7", "point": "sha256 改一位（abc → abd）", "verdict": "blocked",
     "kind": "strict", "new_block": ["EV-ARTIFACT-PRODUCER:x"], "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M7", "point": "-", "verdict": "n_a",
     "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M6", "point": "块式 → flow 写法（matrix）", "verdict": "escaped",
     "kind": None, "new_block": [], "new_warn": [], "equivalent": True},
]


def test_analyze_top20_len():
    an = T.analyze(RECORDS)
    assert 0 < len(an["top20"]) <= 20


def test_ranked_excludes_na_and_equivalent():
    an = T.analyze(RECORDS)
    for r in an["top20"]:
        assert r["rec"]["verdict"] != "n_a"
        assert not r["rec"].get("equivalent")


def test_contract_mini():
    c = T.check_contract(RECORDS)
    assert c["escaped_real"] == 1
    assert c["n_a"] == 1
    assert c["denom"] == 3
    assert c["contract_ok"] is False  # mini 不是 1406，只验证算法正确


def test_pareto_front_vectors_deduped():
    an = T.analyze(RECORDS)
    vecs = an["pareto_vectors"]
    assert len(vecs) >= 1
    assert len(vecs) == len(set(vecs))  # 去重


def test_escape_rank_reported():
    an = T.analyze(RECORDS)
    assert an["escape_rank"] is not None
    assert an["n_ranked"] == 3  # 4 records - 1 n_a - 1 equivalent


def test_render_contains_contract_line():
    md = T.render_markdown(RECORDS)
    assert "contract_ok =" in md
    assert "帕累托前沿" in md


def test_check_runs_clean():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "adversarial_attacker_619.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
