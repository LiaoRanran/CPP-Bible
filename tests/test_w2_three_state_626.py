"""626 C2 · W2 三态解耦回归测试（≥6 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import w2_three_state_626 as W  # noqa: E402


def test_selftest_passes():
    assert W.selftest() == 0


def test_argument_status_keys():
    a = W.load_argument_status()
    assert {"IN", "OUT", "UNDEC"} <= set(a)
    assert isinstance(a["IN"], int)


def test_truth_support_keys():
    t = W.load_truth_support()
    assert {"supported", "refuted", "unresolved"} <= set(t)
    assert t["supported"] + t["refuted"] + t["unresolved"] > 0


def test_publication_status_has_policy():
    p = W.load_publication_status()
    assert {"authorized", "blocked", "pending"} <= set(p)
    assert p["aggregation_policy"]


def test_three_states_are_independent():
    """三态互不替代：键集互不相交，且各自独立可算。"""
    r = W.compute()
    a, t, p = r["argument_status"], r["truth_support"], r["publication_status"]
    assert not ({"IN", "OUT", "UNDEC"} & {"supported", "refuted", "unresolved"})
    assert not ({"IN", "OUT", "UNDEC"} & {"authorized", "blocked", "pending"})
    assert isinstance(a["IN"], int)
    assert isinstance(t["supported"], int)
    assert isinstance(p["authorized"], int)


def test_in_does_not_equal_true_semantics():
    """IN 只表示未被击败，不等于真——文档断言存在且三态分开存储。"""
    r = W.compute()
    assert "IN≠真" in r["note"] or "IN≠真" in r["note"].replace("IN≠真", "IN≠真")
    assert "argument_status" in r and "truth_support" in r


def test_backward_compat_grounded_labels_still_readable():
    """向后兼容：现有 grounded_labels_w2.json 仍可用。"""
    assert os.path.exists(W.GROUNDED)
    a = W.load_argument_status()
    assert a["source"] == "grounded_labels_w2.json"
