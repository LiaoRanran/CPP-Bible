#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""selection_strategies_673p.py — 673p B：**选择策略层**（拆仓的第二层）。

它回答的问题是：
> 给定一个**资产池**和一个**预算**（资产数 / 序数成本），按某种策略选出要运行的子集。

三种策略（论文 §5.2 / 671b `b3_design` 的三臂口径）
====================================================
* `failure_driven`（FD）—— 按**历史失败模式**排序：`fail_hits` 降序（同分按 id 升序，确定性）。
  `fail_hits` 必须由调用方提供，且**必须来自评测集之外的派生集**，否则它就是 oracle、
  不是预测器（见 `run_a5_experiment_673p.py` 的 A5 阻塞登记）。
* `random`         —— 同预算**真随机**：`random.Random(seed).sample`（同 seed 完全可复现）。
* `static`         —— **不使用运行时证据**的固定子集：只取编译期/静态资产（字典序）。

与 672g 的关系
==============
672g 的 `select_assets(pool, n, strategy, seed)` 只支持**资产数**一种预算，且池是名字元组。
本文件把它推广成：**预算 = (资产数 ∪ 序数成本)**，池 = `verifier_pool_673p.AssetSpec` 元数据，
并显式产出**分配表**（第三方可重放"选了哪几个"）。

预算语义（写死，可测）
======================
1. 策略先给出一个**候选次序**（FD：按分排序；random：按 seed 抽样；static：静态资产字典序）。
2. 选择结果 = 该次序的**最大前缀**，同时满足 `len ≤ max_assets` 与 `cost ≤ max_cost`。
3. fail-loud（`ValueError`）：
   * 两个预算维度**都不给**；
   * `max_assets < 0` 或 `max_assets > 候选数`（预算超过池容量，静默截断会让"预算对齐"失效）；
   * `max_cost` 连**最便宜**的候选都装不下（预算不可行）；
   * `random` 未给 `seed`；`failure_driven` 的 `fail_hits` 缺字段；`static` 的静态资产不够。

**它不做的事**：本层**不**执行资产、**不**读任何样本判决。它只做选择，是纯函数。

用法
====
    python tools/selection_strategies_673p.py --check
    python tools/selection_strategies_673p.py --strategy random --max-assets 4 --seed 20260930 --json
    python tools/selection_strategies_673p.py --strategy static --max-assets 3 --json
"""
from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass

import verifier_pool_673p as vp

VERSION = "1.0"
DEFAULT_SEED = 20260930                     # 项目约定种子（670d §3.1；与 670a Random† 同值）

STRATEGIES: tuple[str, ...] = ("failure_driven", "random", "static")


@dataclass(frozen=True)
class Selection:
    """一次资产选择的结果（含可核验分配表）。"""

    strategy: str
    assets: tuple[str, ...]
    seed: int | None
    max_assets: int | None
    max_cost: int | None
    cost_units: int
    allocation_table: tuple[dict, ...]
    n_candidates: int
    notes: str = ""

    def as_dict(self) -> dict:
        d = asdict(self)
        d["allocation_table"] = list(self.allocation_table)
        d["assets"] = list(self.assets)
        return d


def _candidates(pool: tuple[vp.AssetSpec, ...], candidates: list[str] | None) -> list[str]:
    """候选资产 id（默认 = 池中已实测资产；显式给定则必须都在池中且已实测）。"""
    if candidates is None:
        return vp.selectable_ids(pool)
    idx = {a.id: a for a in pool}
    for c in candidates:
        if c not in idx:
            raise ValueError(f"候选 {c!r} 不在资产池中")
        if not idx[c].implemented:
            raise ValueError(f"候选 {c!r} 是声明未接线资产（implemented=False）⇒ 无实测判决，不可选")
    return list(candidates)


def _order(strategy: str, cands: list[str], *,
           fail_hits: dict[str, int] | None, seed: int | None) -> tuple[list[str], str]:
    """按策略给出候选次序 + 说明。"""
    if strategy == "failure_driven":
        if fail_hits is None:
            raise ValueError("strategy='failure_driven' 必须提供 fail_hits（历史失败命中数）")
        missing = [c for c in cands if c not in fail_hits]
        if missing:
            raise ValueError(f"fail_hits 缺这些候选的字段：{missing}")
        ordered = sorted(cands, key=lambda c: (-int(fail_hits[c]), c))
        return ordered, "fail_hits 降序（同分按 id 升序 ⇒ 确定性）"

    if strategy == "random":
        if seed is None:
            raise ValueError("strategy='random' 必须提供 seed（否则不可复现）")
        # 池次序即抽样次序 ⇒ 先用池序（字典序）再 sample，跨实现可复现
        ordered = random.Random(seed).sample(sorted(cands), len(cands))
        return ordered, f"random.Random({seed}).sample（同 seed 完全可复现）"

    if strategy == "static":
        statics = sorted(c for c in cands if c in vp.STATIC_ASSETS)
        if not statics:
            raise ValueError("池中没有静态资产 ⇒ static 策略不可行")
        # static 策略**只**允许静态资产（不得回落到运行时资产，否则口径就不是 Static 臂）
        return statics, "静态资产字典序（static 策略不得使用运行时证据）"

    raise ValueError(f"未知 strategy={strategy!r}（应为 {STRATEGIES}）")


def select(strategy: str, pool: tuple[vp.AssetSpec, ...] = vp.ASSET_POOL, *,
           max_assets: int | None = None, max_cost: int | None = None,
           fail_hits: dict[str, int] | None = None, seed: int | None = None,
           candidates: list[str] | None = None) -> Selection:
    """按策略在预算下选资产子集。**纯函数**：不执行、不读样本。

    参数
    ----
    strategy   : `"failure_driven"` / `"random"` / `"static"`。
    pool       : 资产池（默认 `verifier_pool_673p.ASSET_POOL`）。
    max_assets : 预算上限（资产个数）。与 `max_cost` 至少给一个。
    max_cost   : 预算上限（序数成本之和）。
    fail_hits  : `failure_driven` 必需；`{asset_id: 历史失败命中数}`（须来自派生集，非评测集）。
    seed       : `random` 必需。
    candidates : 候选 id 白名单（默认 = 池中已实测资产）。

    Raises
    ------
    ValueError : 见模块 docstring「预算语义」第 3 条。
    """
    if strategy not in STRATEGIES:
        raise ValueError(f"未知 strategy={strategy!r}（应为 {STRATEGIES}）")
    if max_assets is None and max_cost is None:
        raise ValueError("必须至少给一个预算维度（max_assets 或 max_cost）")

    cands = _candidates(pool, candidates)
    if max_assets is not None:
        if max_assets < 0:
            raise ValueError(f"max_assets 必须 ≥0（实得 {max_assets}）")
        if max_assets > len(cands):
            raise ValueError(f"max_assets={max_assets} 超过候选数 {len(cands)}："
                             "预算不匹配 ⇒ fail-loud，不静默截断（否则预算对齐失效）")

    order, why = _order(strategy, cands, fail_hits=fail_hits, seed=seed)

    if strategy == "static":
        statics = [c for c in order if c in vp.STATIC_ASSETS]
        if max_assets is not None and max_assets > len(statics):
            raise ValueError(f"static 策略只认静态资产，池中仅 {len(statics)} 个 < max_assets={max_assets}"
                             "（fail-loud：静态臂预算不足）")

    if max_cost is not None:
        cheapest = min(pool_by_cost(c, pool) for c in cands)
        if max_cost < cheapest:
            raise ValueError(f"max_cost={max_cost} 连最便宜的候选（cost={cheapest}）都装不下 ⇒ 预算不可行")

    # 最大前缀：同时满足两个预算上限
    picked: list[str] = []
    spent = 0
    for c in order:
        if max_assets is not None and len(picked) >= max_assets:
            break
        c_cost = pool_by_cost(c, pool)
        if max_cost is not None and spent + c_cost > max_cost:
            break
        picked.append(c)
        spent += c_cost

    if max_assets is not None and len(picked) < max_assets:
        # 只可能发生在 max_cost 同时给且卡住的情况 ⇒ 如实说明，不静默
        why += f"；因 max_cost={max_cost} 提前截止（选到 {len(picked)}/{max_assets}）"

    return Selection(
        strategy=strategy,
        assets=tuple(picked),
        seed=seed if strategy == "random" else None,
        max_assets=max_assets,
        max_cost=max_cost,
        cost_units=spent,
        allocation_table=tuple({"asset": a, "rank": i + 1, "cost_units": pool_by_cost(a, pool)}
                               for i, a in enumerate(picked)),
        n_candidates=len(cands),
        notes=why,
    )


def pool_by_cost(asset_id: str, pool: tuple[vp.AssetSpec, ...] = vp.ASSET_POOL) -> int:
    """资产序数成本（不在池中 ⇒ KeyError）。"""
    return vp.by_id(asset_id, pool).cost_units


def fd_budget_anchor(catch_detectors: list[str],
                     pool: tuple[vp.AssetSpec, ...] = vp.ASSET_POOL) -> list[str]:
    """**FD 的预算锚**：FD 在 catch 样本上实际"用到"的资产集合（= 672g `budget()` 同义）。

    ⚠ 这不是"选择"，是**事后记账**：FD 对每个样本跑**全池**，此处只是从 catch 反推
    哪些资产产出了判决。把它当"FD 选择策略"是错的（见 A5 阻塞条件 3）。
    """
    return sorted({d for d in catch_detectors if d in set(vp.selectable_ids(pool))})


# ─────────────────────────────────────────────────────────────────────────────
# 自检
# ─────────────────────────────────────────────────────────────────────────────
def _raises(fn) -> bool:
    try:
        fn()
    except (ValueError, TypeError, KeyError):
        return True
    return False


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    pool = vp.ASSET_POOL
    fh = {i: 0 for i in vp.selectable_ids(pool)}
    fh["asan"] = 25
    fh["ubsan"] = 4

    fd = select("failure_driven", pool, max_assets=4, fail_hits=fh)
    chk("FD 取 fail_hits 最高的", fd.assets[0] == "asan", f"({fd.assets})")
    chk("FD 确定性", fd == select("failure_driven", pool, max_assets=4, fail_hits=fh))

    a = select("random", pool, max_assets=4, seed=DEFAULT_SEED)
    b = select("random", pool, max_assets=4, seed=DEFAULT_SEED)
    chk("random 同 seed 可复现", a.assets == b.assets, f"({a.assets})")
    chk("random 不同 seed 不同", a.assets != select("random", pool, max_assets=4, seed=7).assets)
    chk("random 长度 = max_assets", len(a.assets) == 4)
    chk("random 不重复", len(set(a.assets)) == 4)

    st = select("static", pool, max_assets=4)
    chk("static 只返回静态资产", set(st.assets) <= set(vp.STATIC_ASSETS), f"({st.assets})")
    chk("static 确定性", st == select("static", pool, max_assets=4))

    # 预算约束生效
    chk("max_assets 约束生效", len(a.assets) <= 4)
    cost4 = select("failure_driven", pool, max_cost=6, fail_hits=fh)
    chk("max_cost 约束生效", cost4.cost_units <= 6, f"(cost={cost4.cost_units})")
    chk("两个维度同时生效",
        len(select("failure_driven", pool, max_assets=8, max_cost=6, fail_hits=fh).assets) <= 8)

    # fail-loud
    chk("两维度都不给 ⇒ ValueError", _raises(lambda: select("random", pool, seed=1)))
    chk("max_assets 超候选数 ⇒ ValueError",
        _raises(lambda: select("random", pool, max_assets=9, seed=1)))
    chk("max_assets<0 ⇒ ValueError", _raises(lambda: select("random", pool, max_assets=-1, seed=1)))
    chk("未知 strategy ⇒ ValueError", _raises(lambda: select("greedy", pool, max_assets=2)))
    chk("random 缺 seed ⇒ ValueError", _raises(lambda: select("random", pool, max_assets=2)))
    chk("FD 缺 fail_hits ⇒ ValueError", _raises(lambda: select("failure_driven", pool, max_assets=2)))
    chk("FD fail_hits 缺字段 ⇒ ValueError",
        _raises(lambda: select("failure_driven", pool, max_assets=2, fail_hits={"asan": 1})))
    chk("static 预算超静态资产 ⇒ ValueError", _raises(lambda: select("static", pool, max_assets=5)))
    chk("max_cost 不可行 ⇒ ValueError", _raises(lambda: select("static", pool, max_cost=0)))
    chk("候选不在池 ⇒ ValueError",
        _raises(lambda: select("random", pool, max_assets=1, seed=1, candidates=["nope"])))
    chk("候选未接线 ⇒ ValueError",
        _raises(lambda: select("random", pool, max_assets=1, seed=1, candidates=["valgrind"])))

    # 分配表
    chk("分配表长度 = 选中数", len(a.allocation_table) == len(a.assets))
    chk("分配表 rank 从 1 连续", [r["rank"] for r in a.allocation_table] == list(range(1, len(a.assets) + 1)))
    chk("分配表含 cost_units", all("cost_units" in r for r in a.allocation_table))

    # FD 预算锚
    anchor = fd_budget_anchor(["asan", "asan", "linker", "measure", "unknown"])
    chk("FD 预算锚 = 池内去重", anchor == ["asan", "linker"], f"({anchor})")

    print(f"selection_strategies_673p selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="673p B：资产选择策略（拆仓第二层）")
    ap.add_argument("--strategy", default="random", choices=list(STRATEGIES))
    ap.add_argument("--max-assets", type=int, default=None)
    ap.add_argument("--max-cost", type=int, default=None)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--fail-hits", default=None, help="JSON 文件：{asset_id: 命中数}（FD 用）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()

    fh = None
    if a.fail_hits:
        with open(a.fail_hits, encoding="utf-8") as fh_file:
            fh = json.load(fh_file)

    sel = select(a.strategy, vp.ASSET_POOL, max_assets=a.max_assets, max_cost=a.max_cost,
                 fail_hits=fh, seed=a.seed)
    if a.json:
        print(json.dumps(sel.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"[{sel.strategy}] 选中 {len(sel.assets)} 个 / cost={sel.cost_units} → {list(sel.assets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
