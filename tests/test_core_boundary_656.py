# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""656 B3 · 核心边界清理的回归锁。

背景：任务书要求"审查核心，找出未处理的空输入 / 冲突证据 / 保护器触发 / 隐式假设"。
本批**实测**到并修掉的三类（每一条都先有"原来会怎样"的描述，再锁"现在必须怎样"):
  1. `four_state_verdict_638.classify` / `has_boundary` 对 **None / 非 dict** 入参会
     抛 `AttributeError`——把"判不出来"变成"崩掉"，与四态语义冲突 ⇒ 现在显式 unknown；
  2. `classify_card(None / "")` 的 `open()` 抛 `TypeError`（不属于 `OSError` ⇒ 漏出捕获）
     ⇒ 现在显式 unknown 并给原因；
  3. `AuthorityLedger.append` **隐式假设单线程**（取 prev → 分 seq → 追加三段不加锁，
     并发会算出同一 prev_hash/seq，哈希链悄悄分叉）⇒ 现在临界区显式加锁，
     `verify_chain` 持同一把锁。
另：冲突证据（`pass_with_exception` 缺 explanation）、保护器触发（`conflict` 标记）
的边界行为一并锁在这里，避免下次重构把"降级"悄悄改成"放行"。
"""
from __future__ import annotations

import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import decision_event_v2_626 as de  # noqa: E402
import four_state_verdict_638 as fs  # noqa: E402
import ledger_checkpoint_651 as lc  # noqa: E402

GOOD = {"verdict": "pass", "explanation": "", "mutation_set_hash": "a" * 64,
        "mutation_count": "10", "generator_version": "v7"}


# ── ① 空 / 坏入参 ⇒ unknown，不许抛异常 ────────────────────────────────────
@pytest.mark.parametrize("bad", [None, "x", 123, [], (), object()])
def test_classify_non_dict_is_unknown(bad):
    out = fs.classify(bad)          # 不许抛 AttributeError
    assert out["state"] == "unknown", out
    assert out["boundary_ok"] is False
    assert any("dict" in r for r in out["reasons"]), out["reasons"]


@pytest.mark.parametrize("bad", [None, "x", 123, []])
def test_has_boundary_non_dict_is_false(bad):
    assert fs.has_boundary(bad) is False


@pytest.mark.parametrize("bad_path", [None, "", "   ", 123, []])
def test_classify_card_bad_path_is_unknown(bad_path):
    out = fs.classify_card(bad_path)     # 不许抛 TypeError
    assert out["state"] == "unknown", out
    assert out["downgraded"] is True
    assert out["reasons"], out


def test_classify_card_missing_file_is_unknown(tmp_path: Path):
    out = fs.classify_card(str(tmp_path / "nope.md"))
    assert out["state"] == "unknown"
    assert "不可读" in out["reasons"][0]


# ── ② 冲突证据 / 保护器触发 ⇒ 降级而不是放行 ───────────────────────────────
def test_pass_with_exception_boundary():
    """`pass_with_exception` 的两个边界：有 explanation ⇒ 保留；缺 ⇒ 降级 unknown。"""
    with_expl = dict(GOOD, verdict="pass", exception="有例外条款", explanation="为什么保留")
    assert fs.classify(with_expl)["state"] == "pass_with_exception"
    # 注意：`_raw_state` 见 `exception` 为真就判 pass_with_exception ⇒ 缺 explanation 必须降级
    no_expl = dict(GOOD, verdict="pass", exception="有例外条款", explanation="")
    assert fs.classify(no_expl)["state"] == "unknown"
    assert fs.classify(no_expl)["downgraded"] is True


def test_conflict_word_does_not_sneak_into_pass():
    """`verdict` 写 'block/conflict' 这类词 ⇒ 走 fail，绝不能被当成 pass。"""
    for w in ("block", "fail", "reject", "refuted", "false"):
        assert fs.classify(dict(GOOD, verdict=w))["state"] == "fail", w


def test_unknown_verdict_word_is_unknown():
    assert fs.classify(dict(GOOD, verdict="weird-word"))["state"] == "unknown"


# ── ③ 账本并发边界（B3 加锁后：**不**依赖调用方加锁）───────────────────────
def test_ledger_append_is_internally_locked():
    """并发追加 **不加外部锁** 也必须：不丢、seq 不重、链成立。"""
    led = de.AuthorityLedger()
    n_threads, per_thread = 8, 6
    errs: list[str] = []

    def worker(tid: int) -> None:
        for i in range(per_thread):
            try:
                led.append(de.DecisionEvent(target_type="edge", target_id=f"T{tid}-{i}",
                                            result="APPROVE", decision_origin="human_observed",
                                            review_method="BATCH_AUTH", operation="CREATE"))
            except Exception as e:  # noqa: BLE001
                errs.append(f"{tid}-{i}: {type(e).__name__}: {str(e)[:100]}")

    ts = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errs, errs[:3]
    assert len(led) == n_threads * per_thread, "并发丢条目 ⇒ 隐式单线程假设仍然存在"
    seqs = [e.seq for e in led.all_events()]
    assert sorted(seqs) == list(range(1, len(led) + 1)), "seq 必须连续且唯一"
    assert led.verify_chain() is True


def test_ledger_rejects_invalid_event_explicitly():
    led = de.AuthorityLedger()
    with pytest.raises(ValueError) as ei:
        led.append(de.DecisionEvent(target_type="edge", target_id="", result="APPROVE"))
    assert "target_id" in str(ei.value)


def test_ledger_supersede_chain_current_is_latest_alive():
    led = de.AuthorityLedger()
    e1 = de.DecisionEvent(target_type="edge", target_id="E1", result="APPROVE",
                          decision_origin="human_observed", review_method="BATCH_AUTH",
                          operation="CREATE")
    led.append(e1)
    e2 = de.DecisionEvent(target_type="edge", target_id="E1", result="REJECT",
                          decision_origin="human_observed", review_method="BATCH_AUTH",
                          operation="REPLACE", supersedes=[e1.event_id])
    led.append(e2)
    cur = led.get_current("edge", "E1")
    assert cur is not None and cur.event_id == e2.event_id


# ── ④ Merkle 空输入边界 ────────────────────────────────────────────────────
def test_merkle_empty_ledger_no_crash():
    assert lc.mth([]) is None
    # 空树上做 inclusion/consistency 不允许抛异常（只能给 False / 空证明）
    assert lc.inclusion_path(0, []) == [] or isinstance(lc.inclusion_path(0, []), list)


def test_merkle_single_leaf():
    leaf = b"only"
    root = lc.mth([leaf])
    assert root is not None
    assert lc.verify_inclusion(0, 1, leaf, lc.inclusion_path(0, [leaf]), root) is True
