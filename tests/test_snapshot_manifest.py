#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""617 D2 · snapshot_manifest 单测（纯标准库；实时计数仅校验结构与类型）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import snapshot_manifest as m  # noqa: E402


def test_live_counts_structure():
    man = m.build_manifest()
    lc = man["live_counts"]
    assert set(lc.keys()) == {"commits", "tools_py", "tests_py", "atoms_md", "evidence_ev_md"}
    for v in lc.values():
        assert isinstance(v, int) and v >= 0
    assert lc["commits"] > 0
    assert len(man["head_commit"]) == 40


def test_frozen_numbers():
    man = m.build_manifest()
    fb = man["verification_baseline_frozen"]
    assert fb["gate"]["rules"] == 63 and fb["gate"]["warn"] == 186
    assert fb["poison"]["passed"] == 124 and fb["poison"]["total"] == 124
    assert fb["replay"]["confirm"] == 56 and fb["replay"]["refute"] == 0
    assert fb["mutation_v7"]["escape_rate_contract"] == "1/1406"
    assert fb["confidence"]["cs_anytime_upper_95"] == 0.009062
    assert fb["human_review"]["total"] == 388
    assert fb["independence"]["discrete_level"] == 1


def test_verify_clean_returns_bool():
    assert isinstance(m.verify_clean(), bool)


def test_generated_at_present():
    man = m.build_manifest()
    assert "generated_at" in man and man["generated_at"].endswith("Z") or "+" in man["generated_at"]


if __name__ == "__main__":
    test_live_counts_structure()
    test_frozen_numbers()
    test_verify_clean_returns_bool()
    test_generated_at_present()
    print("ALL D2 TESTS PASSED")
