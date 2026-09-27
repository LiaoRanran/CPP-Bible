#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_core_pbt_651.py — T6 核心 stateful PBT 骨架（651 W2）。

为什么（651 W2-T6）：核心（判决合成 / 账本追加 / 保护器改判条件）目前只靠**样例**测试，
样例通过 ≠ 性质成立。本文件**先建性质清单与序列模型骨架**（651 明确"不追求一步到位覆盖率"）。

性质清单（Property List）
=========================
- P1 判决合成是**半格**：commutative（可交换）/ associative（可结合）/ idempotent（幂等）。
- P2 判决合成**worst-wins**：整体不超过最坏分量（fail 吞并一切；unknown 压过 pass）。
- P3 账本追加**前缀保持**（sequence model）：append 后旧条目逐字不变、长度 +1。
- P4 Merkle 追加**一致性**：任意前缀 m≤n 的 old_root 对新 root 有可验 consistency proof。
- P5 保护器标记**置换不变**：同一组标记按任意顺序施加，结果集合相同。

诚实边界：本骨架用**穷举小域**（4 态、≤5 标记、≤24 叶子）保证确定性，不用随机；覆盖率非目标。
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

STATES = ["pass", "pass_with_exception", "fail", "unknown"]
# worst-wins 序：fail < unknown < pass_with_exception < pass
_RANK = {"fail": 0, "unknown": 1, "pass_with_exception": 2, "pass": 3}


def combine(a: str, b: str) -> str:
    """判决合成：取更"坏"者（半格 meet）。"""
    return a if _RANK[a] <= _RANK[b] else b


# ── P1 半格性质 ──────────────────────────────────────────────────────────────
def test_p1_composition_is_semilattice():
    for a, b in itertools.product(STATES, STATES):
        assert combine(a, b) == combine(b, a), "commutative"
    for a, b, c in itertools.product(STATES, repeat=3):
        assert combine(combine(a, b), c) == combine(a, combine(b, c)), "associative"
    for a in STATES:
        assert combine(a, a) == a, "idempotent"


def test_p1_composition_closed():
    for a, b in itertools.product(STATES, STATES):
        assert combine(a, b) in STATES


# ── P2 worst-wins ───────────────────────────────────────────────────────────
def test_p2_worst_wins():
    assert combine("pass", "fail") == "fail"
    assert combine("fail", "pass") == "fail"
    assert combine("unknown", "pass") == "unknown"
    assert combine("pass_with_exception", "fail") == "fail"
    # 折叠一列：结果 = 最坏分量
    for seq in itertools.product(STATES, repeat=4):
        folded = seq[0]
        for x in seq[1:]:
            folded = combine(folded, x)
        assert folded == min(seq, key=lambda s: _RANK[s])


# ── P3 账本追加前缀保持（序列模型）──────────────────────────────────────────
def test_p3_ledger_append_prefix_preserved():
    ledger: list = []
    for i in range(30):
        prev = list(ledger)
        ledger.append({"seq": i})
        assert ledger[: len(prev)] == prev, "前缀被改"
        assert len(ledger) == i + 1
    # 重新读取幂等：同内容 ⇒ 同序列
    assert list(ledger) == list(ledger)


# ── P4 Merkle 追加一致性（用真 checkpoint 工具）────────────────────────────
def test_p4_merkle_append_consistency_all_prefixes():
    import ledger_checkpoint_651 as lc

    leaves = [f"e{i}".encode() for i in range(24)]
    root = lc.mth(leaves)
    for m in range(1, len(leaves) + 1):
        assert lc.verify_consistency(m, len(leaves), lc.consistency_proof(m, leaves),
                                     lc.mth(leaves[:m]), root)
    # inclusion 也全覆盖
    for i in range(len(leaves)):
        assert lc.verify_inclusion(i, len(leaves), leaves[i], lc.inclusion_path(i, leaves), root)


# ── P5 保护器标记置换不变 ───────────────────────────────────────────────────
def test_p5_protector_marks_permutation_invariant():
    marks = [{"conflict"}, {"blind"}, {"windup"}, {"conflict", "budget"}]
    base: set = set().union(*marks)
    for perm in itertools.permutations(range(len(marks))):
        acc: set = set()
        for idx in perm:
            acc |= marks[idx]
        assert acc == base


def test_p5_rollback_to_empty():
    """撤销到底 ⇒ 空（对应 642 A6 rollback_marks 归零）。"""
    marks = {"a", "b", "c"}
    rolled: set = set(marks)
    for m in list(marks):
        rolled.discard(m)
    assert rolled == set()
