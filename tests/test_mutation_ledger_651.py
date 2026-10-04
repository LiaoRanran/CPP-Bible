#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_mutation_ledger_651.py — 676i 工程批：杀死 ledger_checkpoint_651 的 size-0 存活变异体。

为什么（676i / 676a 定位）
=========================
    ledger_checkpoint_651 的 `_subproof` 在 666 批次被改为 fail-loud（line 143）：

        assert m > 0, "size-0 树没有 consistency proof"

    该断言的 cmp 变异 `>` → `>=` 在 672f 重跑后从 import_error 变成 survived
    （658 时点该位置注入后 SyntaxError ⇒ 免测；源码演进后注入成功，暴露
    "没有任何 kill 测试能区分 `m > 0` 与 `m >= 0`" 的真实缺口）。
    这把 mutation.core 从 97.3%（110/113）拉到 96.5%（110/114）。

kill 设计（为什么用断言信息作判别）
==================================
    `_subproof(0, [], False)` 是**唯一**能令 m=0 抵达 line 143 的调用
    （public `consistency_proof` / `verify_consistency` 在 m=0 时提前返回，永不至此）。

    - 原始：`assert 0 > 0` ⇒ 抛「size-0 树没有 consistency proof」。
    - 变异体 `assert 0 >= 0` 越过 143 后，line 144 的 `_mth_nonempty([])` 仍会因
      `mth([]) is None` 抛「内部契约破坏：非空切片不应得到 None」。

    因此**仅用 `pytest.raises(AssertionError)` 无法杀死该变异体**——两版都抛
    AssertionError，只是位置/信息不同。必须用**断言信息**作判别：改 `>` 为 `>=`
    后，本测试断言的信息不再匹配 ⇒ 测试 FAIL ⇒ 变异体被杀死。

诚实边界
========
    本测试刻意耦合断言信息字符串。这是该存活变异体在当前代码结构下唯一干净的
    判别点；若未来 666 的 fail-loud 信息文案变更，需同步更新本测试（属预期维护成本，
    远小于"变异体永久存活、mutation.core 卡在 96.5"）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def test_subproof_size0_fail_loud_kills_mutant():
    """m=0 的 size-0 树 consistency 路径必须 fail-loud，杀死 `>`→`>=` 变异体。"""
    import ledger_checkpoint_651 as lc

    with pytest.raises(AssertionError, match="size-0 树没有 consistency proof"):
        lc._subproof(0, [], False)


def test_subproof_size0_b_true_returns_empty():
    """对照（不杀变异体，仅作回归基线）：`consistency_proof` 的 public 入口走 b=True，

    m==n==0 时返回空证明 `[]`、不抛异常。本测试锁住"正常路径不被 size-0 守卫误伤"。
    """
    import ledger_checkpoint_651 as lc

    assert lc._subproof(0, [], True) == []
