"""625 D3 · 人审执行框架（只准备不代签）回归测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import human_review_executor_625 as E  # noqa: E402

AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")


def test_selftest_passes():
    assert E.selftest() == 0


def test_build_entry_makes_hashed_entry():
    e = E.build_entry("EV-X", "ACCEPT", "approve", "reviewer:A", "ok",
                      prev_hash=E._read_last_hash(AUTH))
    assert e["hash"] and len(e["hash"]) == 64
    assert e["power"] == "ACCEPT" and e["decision"] == "approve"


def test_illegal_power_rejected():
    try:
        E.build_entry("EV-X", "BOGUS", "approve", "A", "r")
        assert False, "应抛 ValueError"
    except ValueError:
        pass


def test_no_signing_no_mutation():
    before = os.path.getsize(AUTH)
    # 调用框架自检 / 构造条目，但绝不调用 append_entry
    e = E.build_entry("EV-Y", "REJECT", "reject", "A", "r", prev_hash="GENESIS")
    assert callable(E.append_entry)
    after = os.path.getsize(AUTH)
    assert before == after, "本批绝不代签：Authority 日志不可被修改"
