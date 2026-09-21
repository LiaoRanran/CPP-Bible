#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 C2 · test_classifier_618 单测（≥3 例）"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import test_classifier_618 as c  # noqa: E402


def _make(tmp, name, content):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return p


def test_membership_gate_by_import():
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_foo.py", "import gate_engine\n")
        assert "gate" in c.classify_membership(p)


def test_membership_poison_by_name():
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_poison_something.py", "x=1\n")
        assert "poison" in c.classify_membership(p)


def test_membership_replay_by_import():
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_bar.py", "from atom_evidence_replay import X\n")
        assert "replay" in c.classify_membership(p)


def test_primary_snapshot_self_test():
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_snapshot_thing.py", "y=2\n")
        assert c.classify_file(p) == "snapshot"


def test_primary_unclassified():
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_random_xyz.py", "z=3\n")
        assert c.classify_file(p) == "其他"


def test_scan_and_summarize_membership():
    with tempfile.TemporaryDirectory() as d:
        _make(d, "test_g.py", "import gate_engine\n")
        _make(d, "test_p.py", "import poison_drill\n")
        _make(d, "test_r.py", "import atom_evidence_replay\n")
        _make(d, "test_s.py", "import snapshot_manifest\n")
        _make(d, "test_u.py", "q=1\n")
        results = c.scan(d)
        s = c.summarize(results)
        assert s["total"] == 5
        # 成员关系三向
        assert s["three_way"]["gate"] == 1 and s["three_way"]["poison"] == 1
        assert s["three_way"]["replay"] == 1 and s["three_way"]["其他"] == 2
        # 真实 vs 自测 vs 未分类
        assert s["real_verification"] == 3
        assert s["script_self_test"] == 1
        assert s["unclassified"] == 1


def test_priority_gate_over_replay():
    # 同时 import gate 与 replay → primary 为 gate
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_mix.py", "import gate_engine\nimport atom_evidence_replay\n")
        assert c.classify_file(p) == "gate"
        assert "gate" in c.classify_membership(p) and "replay" in c.classify_membership(p)


def test_poison_named_but_imports_gate_counts_both():
    # test_poison_x.py 同时命中 poison（名）与 gate（import）→ 三向均计
    with tempfile.TemporaryDirectory() as d:
        p = _make(d, "test_poison_x.py", "import gate_engine\nimport poison_drill\n")
        m = c.classify_membership(p)
        assert "poison" in m and "gate" in m
        s = c.summarize({os.path.basename(p): m})
        assert s["three_way"]["poison"] == 1 and s["three_way"]["gate"] == 1


if __name__ == "__main__":
    test_membership_gate_by_import()
    test_membership_poison_by_name()
    test_membership_replay_by_import()
    test_primary_snapshot_self_test()
    test_primary_unclassified()
    test_scan_and_summarize_membership()
    test_priority_gate_over_replay()
    test_poison_named_but_imports_gate_counts_both()
    print("ALL C2 TESTS PASSED")
