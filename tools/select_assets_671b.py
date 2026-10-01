#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""select_assets_671b.py — 671b B 段：**主仓侧**验证资产选择接口（真 B3 的接口形状）。

背景（为什么必须有它）
======================
`docs/670a_实验结果.md` §3 登记了本文**最大的实验缺口**：
> **B3 budget-matched random（验证资产口径，论文 §5.2）= BLOCKED**
> 资产选择接口 `select_assets(pool, n, strategy, seed)` 在拆仓验证器 `queyi-verifier`，
> **主仓不可见**。

670a 的 `Random†` 是**仪器级代理**（把"资产"退化成"检测仪器"），**不是**真 B3；
`docs/670a_实验结果.md` §0 明文写"`†` = 代理，禁止进论文结论"。

本文件做的事
============
把"真 B3 需要的那个接口"在主仓**按论文口径实现出来**，从而：
1. 让 **A5（random-budget）与 B3** 有一个**形状正确**的接口可以先写单测、先冻结口径
   （`select_assets(pool, n, strategy, seed) -> [asset]`）；
2. 当拆仓 `queyi-verifier` 暴露真接口后，**只需替换实现**，调用方与统计管线不变；
3. **本批不跑实验** ⇒ 本文件只提供**函数 + 干跑（dry-run）**，不产生任何检测结果。

**资产（asset）** 在本文的定义
============================
> 一个**可复用的验证手段**：一条规则 / 一个检测器 / 一个编译档 / 一个平台配置。
> 它**不是**一条被检样本。B3 问的是："在**同等预算**下，把'按失败驱动挑选的资产'
> 换成'随机挑选的资产'，检出率会不会掉？"

三种策略
========
* `failure_driven`：按历史失败归因排序（miss/unknown 命中最多的资产优先）——**FD 臂**；
* `random`：均匀随机抽 n 个（**带种子**，可复现）——**B3 臂**；
* `oracle`：按"能抓到的真错数"排序（**上界**，仅供参照，不用于任何 Claim）——诚实登记为 upper bound。

⚠ **诚实边界（写进返回值）**：本接口在主仓上是**仪器级近似**（pool = 检测仪器池），
与拆仓的**真资产池**不同 ⇒ 主仓跑出来的 Δ **只能作方向性读法**，不得写成
"失败驱动优于随机预算"的**确认性**结论（670a §0 红线）。

用法
====
    python tools/select_assets_671b.py --pool build/pool.json --n 4 --strategy random --seed 20260930
    python tools/select_assets_671b.py --check                  # 自检（只读）
    python tools/select_assets_671b.py --check --json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
DEFAULT_SEED = 20260930           # 与 670a 的 Random† 同种子（口径可对照）
STRATEGIES = ("failure_driven", "random", "oracle")

#: 主仓仪器池（与 tools/baseline_670a.py::INSTRUMENT_POOL 同源，**不是**真资产池）
INSTRUMENT_POOL: tuple[str, ...] = (
    "asan", "compile-time", "compiler-warn", "cross-compile", "linker",
    "measure", "perf-counter", "tsan", "ubsan", "wunsequenced",
)


# ─────────────────────────────────────────────────────────────────────────────
# 核心接口：select_assets(pool, n, strategy, seed)
# ─────────────────────────────────────────────────────────────────────────────
def _as_list(pool: Iterable[Any]) -> list[Any]:
    """把 pool 规整成 list（支持 list[str] 或 list[dict]）。"""
    return list(pool)


def _key(asset: Any) -> str:
    return str(asset["id"] if isinstance(asset, dict) else asset)


def select_assets(pool: Iterable[Any], n: int, strategy: str = "random",
                  seed: int = DEFAULT_SEED) -> list[Any]:
    """**真 B3 的接口形状**：从资产池中按策略选 n 个资产。

    参数
    ----
    pool : 资产池。元素可为 `str`（仪器名）或 `dict`（`{"id":..., "fail_hits":int, ...}`）。
    n : 要选的资产数。`n == 0` ⇒ `[]`；`n > len(pool)` ⇒ ValueError（fail-loud，不静默截断）。
    strategy : `"failure_driven"` / `"random"` / `"oracle"`。
    seed : 随机种子（**仅 random 用**；但签名里始终在，保证调用方形状统一）。

    返回
    ----
    长度为 n 的**有序**列表（failure_driven/oracle 按分数降序，random 按抽样顺序）。

    排序规则
    --------
    * `failure_driven`：按 `fail_hits` 降序（同分按 id 升序，保证**确定性**）。
    * `oracle`：按 `true_catch` 降序（同上）——**上界参照**。
    * `random`：`random.Random(seed).sample(...)` —— 同 seed 完全可复现。

    Raises
    ------
    ValueError : 未知 strategy / n 为负 / n > len(pool) / oracle 缺 true_catch 字段。
    """
    items = _as_list(pool)
    if strategy not in STRATEGIES:
        raise ValueError(f"未知 strategy={strategy!r}（应为 {STRATEGIES}）")
    if n < 0:
        raise ValueError(f"n 必须 ≥0（n={n}）")
    if n > len(items):
        raise ValueError(f"n={n} 超过资产池大小 {len(items)}："
                         "预算不匹配 ⇒ fail-loud，不静默截断（否则 B3 预算对齐失效）")
    if n == 0:
        return []

    if strategy == "random":
        return random.Random(seed).sample(items, n)

    field = "fail_hits" if strategy == "failure_driven" else "true_catch"
    if any(not (isinstance(a, dict) and field in a) for a in items):
        raise ValueError(f"strategy={strategy} 要求池中每个资产都有 {field!r} 字段")
    # 降序主键 + 升序 id 次键 ⇒ 确定性排序（同分可复现）
    ordered = sorted(items, key=lambda a: (-int(a[field]), _key(a)))
    return ordered[:n]


def budget(arm: str, samples: list[dict], verdicts: dict[str, str]) -> list[str]:
    """算某个臂实际"用掉"的资产预算（= 该臂在 catch 样本上用到的资产集合）。

    这是 B3 **预算对齐**的锚：两边必须用**同一数量**的资产，否则"随机不如失败驱动"
    可能只是"随机用得更少"。本函数对 `failure_driven` 与 `random` 都适用。
    """
    used = {str(s.get("detector") or "unknown") for s in samples
            if verdicts.get(s["id"]) == "catch"}
    return sorted(a for a in used if a in INSTRUMENT_POOL)


def select_for_arm(arm: str, pool: list[Any], samples: list[dict],
                   verdicts: dict[str, str], seed: int = DEFAULT_SEED) -> dict:
    """给定一个臂，算它的资产选择 + 预算分配表（**B3 的"分配表"**）。

    `failure_driven` ⇒ 按 FD 实际用到的资产（= 预算基线）；
    `random` ⇒ 与 FD **同数量**的随机资产（预算匹配）。
    """
    if arm == "failure_driven":
        picked = budget(arm, samples, verdicts)
        return {"arm": arm, "strategy": "failure_driven", "n_assets": len(picked),
                "picked": picked, "seed": None,
                "allocation_table": [{"asset": a, "rank": i + 1} for i, a in enumerate(picked)]}
    if arm == "random":
        n = len(budget("failure_driven", samples, verdicts))
        picked = select_assets(pool, n, "random", seed)
        names = [_key(a) for a in picked]
        return {"arm": arm, "strategy": "random", "n_assets": n,
                "picked": names, "seed": seed,
                "allocation_table": [{"asset": nm, "rank": i + 1} for i, nm in enumerate(names)]}
    raise ValueError(f"未知 arm={arm!r}（应为 failure_driven / random）")


# ─────────────────────────────────────────────────────────────────────────────
# 自检
# ─────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    pool = list(INSTRUMENT_POOL)
    chk("池大小 = 10", len(pool) == 10, f"({len(pool)})")

    # random 可复现
    a = select_assets(pool, 4, "random", 20260930)
    b = select_assets(pool, 4, "random", 20260930)
    chk("random 同 seed 可复现", a == b, f"({a})")
    c = select_assets(pool, 4, "random", 99999)
    chk("random 不同 seed 结果不同（大概率）", a != c, f"({c})")
    chk("random 返回长度 = n", len(a) == 4)
    chk("random 不重复", len(set(a)) == 4)

    # failure_driven 确定性 + 按 fail_hits 降序
    dpool = [{"id": x, "fail_hits": i} for i, x in enumerate(
        ["a", "b", "c", "d", "e"])]
    fd = select_assets(dpool, 3, "failure_driven")
    chk("failure_driven 降序", [x["id"] for x in fd] == ["e", "d", "c"],
        f"({[x['id'] for x in fd]})")
    chk("failure_driven 确定性", fd == select_assets(dpool, 3, "failure_driven"))

    # oracle 上界
    opool = [{"id": x, "true_catch": v} for x, v in
             [("a", 1), ("b", 9), ("c", 5), ("d", 7)]]
    orc = select_assets(opool, 2, "oracle")
    chk("oracle 取 top-2", [x["id"] for x in orc] == ["b", "d"], f"({[x['id'] for x in orc]})")

    # n = 0
    chk("n=0 ⇒ []", select_assets(pool, 0, "random") == [])
    # 边界错误
    chk("n > len(pool) ⇒ ValueError", _raises(lambda: select_assets(pool, 11, "random")))
    chk("n < 0 ⇒ ValueError", _raises(lambda: select_assets(pool, -1, "random")))
    chk("未知 strategy ⇒ ValueError", _raises(lambda: select_assets(pool, 2, "greedy")))
    chk("oracle 缺字段 ⇒ ValueError",
        _raises(lambda: select_assets([{"id": "x"}], 1, "oracle")))
    chk("failure_driven 缺字段 ⇒ ValueError",
        _raises(lambda: select_assets([{"id": "x"}], 1, "failure_driven")))

    # 全池选取
    chk("n == len(pool) 合法", len(select_assets(pool, 10, "random")) == 10)

    # 预算对齐：random 与 failure_driven 同数量
    samples = [{"id": "s1", "detector": "asan"}, {"id": "s2", "detector": "ubsan"},
               {"id": "s3", "detector": "linker"}]
    verd = {"s1": "catch", "s2": "catch", "s3": "miss"}
    fd_sel = select_for_arm("failure_driven", pool, samples, verd)
    rn_sel = select_for_arm("random", pool, samples, verd, seed=1)
    chk("预算对齐：两臂资产数一致",
        fd_sel["n_assets"] == rn_sel["n_assets"] == 2,
        f"({fd_sel['n_assets']} vs {rn_sel['n_assets']})")
    chk("failure_driven 选中 = FD 实际使用", fd_sel["picked"] == ["asan", "ubsan"])
    chk("random 分配表长度 = n", len(rn_sel["allocation_table"]) == 2)
    chk("分配表含 rank", all("rank" in r for r in rn_sel["allocation_table"]))

    print(f"select_assets_671b selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _raises(fn) -> bool:
    try:
        fn()
    except (ValueError, TypeError):
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671b B 段：主仓侧验证资产选择接口（真 B3 形状）")
    ap.add_argument("--pool", default=None, help="资产池 JSON 文件（缺省用主仓仪器池）")
    ap.add_argument("--n", type=int, default=4, help="要选的资产数")
    ap.add_argument("--strategy", default="random", choices=list(STRATEGIES))
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()

    if a.pool:
        pool = json.loads(Path(a.pool).read_text(encoding="utf-8"))
        if isinstance(pool, dict) and "pool" in pool:
            pool = pool["pool"]
    else:
        pool = list(INSTRUMENT_POOL)
    picked = select_assets(pool, a.n, a.strategy, a.seed)
    out = {"strategy": a.strategy, "n": a.n, "seed": a.seed,
           "pool_size": len(pool), "picked": [_key(x) for x in picked],
           "caveat": "主仓口径：池=仪器池（非拆仓真资产池）⇒ Δ 只作方向性读法"}
    print(json.dumps(out, ensure_ascii=False, indent=2) if a.json else
          f"[{a.strategy}] n={a.n} seed={a.seed} → {out['picked']}\n  ⚠ {out['caveat']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
