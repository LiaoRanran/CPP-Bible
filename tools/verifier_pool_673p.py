#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""verifier_pool_673p.py — 673p B：**验证资产池**的显式定义（拆仓的第一层）。

为什么要有这个文件
==================
673p 之前的管线把两件事混在一起：

    「哪些检测资产存在」（资产池）  ×  「在给定预算下选哪些资产运行」（选择策略）

`tools/select_assets_672g.py` 只声明了一个 `ASSET_POOL` 的**名字元组**——没有成本、
没有能力描述、没有适用缺陷类型，也没有"这个资产到底实现了没有"的标记。于是：

* 池里既有**已实测**的资产（asan/ubsan/tsan/…），也隐含了**没实现**的口径；
* "预算"只能退化成一个整数（资产个数），"时间预算"根本无从表达；
* 无法回答 A5 真正要问的问题——「**同样预算**下换一种选择策略，检出率掉不掉」。

本文件把**第一层**独立出来：资产池 = 一组**带元数据的验证资产**。
第二层（选择策略）见 `tools/selection_strategies_673p.py`；第三/四层（运行 + 评估）
见 `tools/run_a5_experiment_673p.py`。

资产的定义（沿用 671b/672g 口径）
=================================
> 一个**可复用的验证手段**：一条规则 / 一个检测器 / 一个编译档 / 一个平台配置。
> 它**不是**一条被检样本。

本池**刻意排除** `measure` / `perf-counter`：它们是**性能测量仪器**，不产出缺陷判决，
把测量仪器塞进验证资产池正是 670a `Random†` 代理臂的"仪器级退化"（670a §0 红线）。

成本口径（**声明式，非实测**）
==============================
`cost_units` 是**序数**，不是秒数：

    1 = 静态/编译期，不执行
    2 = 单次编译器 pass（本地，秒级）
    3 = 插桩构建 + 执行（运行时 sanitizer；双档 × 多回合）
    4 = 全量动态分析工具（valgrind / gdb / ptrace）
    5 = 事后 core dump 分析

**诚实边界**：本批**没有**测每个资产的墙钟耗时 ⇒ `cost_basis="declared_ordinal"`。
把序数当秒数是错的；`run_a5_experiment_673p.py` 的"时间预算"因此只做**同口径**比较，
不得写成"省了多少秒"。

实现状态
========
`implemented=True`  = 本仓有实测数据（`data/holdout/reveal_5_detail_672h.json` /
                      `data/external_corpus/reveal_detail_672h.json` 里有它的判决归属）。
`implemented=False` = **声明但未接线**（论文口径里列了、本仓尚无实测归属）。
未实现资产**不进** replay 实验（无实测归属 ⇒ 无从复算），只登记在池里供后续接线。

用法
====
    python tools/verifier_pool_673p.py --check          # 自检（只读）
    python tools/verifier_pool_673p.py --list --json    # 打印池（机读）
    python tools/verifier_pool_673p.py --list           # 打印池（人读表）
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable

VERSION = "1.0"

#: 缺陷类型受控词表（`AssetSpec.defect_types` 的取值域）。
DEFECT_TYPES: tuple[str, ...] = (
    "memory-use-after-free",      # 释放后使用 / 悬垂引用
    "memory-double-free",         # 重复释放
    "memory-stack-escape",        # 栈逃逸 / 返回后使用
    "memory-buffer-overflow",     # 越界读写
    "memory-leak",                # 泄漏
    "memory-uninitialized",       # 未初始化读
    "ub-arithmetic",              # 有符号溢出 / 移位 / 除零
    "ub-pointer",                 # 空指针 / 悬垂指针 / 无效转换
    "ub-array-index",             # 数组越界下标
    "ub-alignment",               # 对齐 / 严格别名
    "concurrency-race",           # 数据竞争
    "concurrency-deadlock",       # 锁序倒置 / 死锁
    "language-sequencing",        # 未定序修改 / 求值顺序
    "odr-link",                   # ODR / 重复符号 / 缺符号
    "portability-divergence",     # 实现定义 / 跨平台分歧
    "api-misuse",                 # 误用标准库/接口
)

#: 能力受控词表（`AssetSpec.capabilities` 的取值域）。
CAPABILITIES: tuple[str, ...] = (
    "runtime-detection",   # 运行期动态判定
    "static-analysis",     # 静态分析/编译诊断
    "instrumentation",     # 插桩（需重编译）
    "post-mortem",         # 事后取证
    "tracing",             # 调用/系统调用追踪
    "cross-toolchain",     # 跨工具链对照
)


@dataclass(frozen=True)
class AssetSpec:
    """一个验证资产的元数据（不可变）。"""

    id: str
    kind: str                                   # sanitizer / compiler / linker / dynamic / postmortem
    cost_units: int                             # 序数成本（见模块 docstring 的 rubric）
    cost_basis: str                             # declared_ordinal（本批全部）
    capabilities: tuple[str, ...]
    defect_types: tuple[str, ...]
    implemented: bool                           # 本仓是否有实测判决归属
    evidence_source: str                        # 实测来源 / "declared"
    note: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


def _a(id_: str, kind: str, cost: int, caps: tuple[str, ...], defects: tuple[str, ...],
       implemented: bool, evidence_source: str, note: str = "") -> AssetSpec:
    return AssetSpec(id=id_, kind=kind, cost_units=cost, cost_basis="declared_ordinal",
                     capabilities=caps, defect_types=defects, implemented=implemented,
                     evidence_source=evidence_source, note=note)


_MEASURED = "data/holdout/reveal_5_detail_672h.json + data/external_corpus/reveal_detail_672h.json"

#: 验证资产池（**字典序钉死次序**：`random.sample` 依赖序列次序 ⇒ 次序即契约）。
#: 12 项 = 8 个已实测资产 + 4 个声明未接线资产；不含 measure/perf-counter。
#: 注意：已实测子集（`implemented_ids()`）的次序 = 672g `ASSET_POOL` 的次序（字典序），
#: 这样 673p 的选择结果与 672g 可直接对照。
ASSET_POOL: tuple[AssetSpec, ...] = (
    _a("asan", "sanitizer", 3,
       ("runtime-detection", "instrumentation"),
       ("memory-use-after-free", "memory-double-free", "memory-stack-escape",
        "memory-buffer-overflow", "memory-leak"),
       True, _MEASURED, "AddressSanitizer；双档 -O0/-O2 × 3 回合，WSL g++"),
    _a("compile-time", "compiler", 1,
       ("static-analysis",),
       ("ub-arithmetic", "ub-pointer", "api-misuse"),
       True, _MEASURED, "编译期 static_assert / constexpr 判定；不执行"),
    _a("compiler-warn", "compiler", 2,
       ("static-analysis",),
       ("ub-arithmetic", "ub-pointer", "ub-array-index", "api-misuse", "language-sequencing"),
       True, _MEASURED, "编译器诊断（-Wall -Wextra 家族）；本机 g++ 13.1.0 / clang++ 22.1.8"),
    _a("coredump", "postmortem", 5,
       ("post-mortem",),
       ("memory-use-after-free", "memory-buffer-overflow", "ub-pointer"),
       False, "declared", "core dump 事后取证；本批未接线"),
    _a("cross-compile", "compiler", 2,
       ("static-analysis", "cross-toolchain"),
       ("portability-divergence", "odr-link", "api-misuse"),
       True, _MEASURED, "跨工具链/跨平台对照编译"),
    _a("gdb", "dynamic", 4,
       ("tracing", "post-mortem"),
       ("memory-use-after-free", "memory-buffer-overflow", "ub-pointer", "api-misuse"),
       False, "declared", "gdb 断点/单步；本批未接线"),
    _a("linker", "linker", 2,
       ("static-analysis",),
       ("odr-link",),
       True, _MEASURED, "链接期诊断（重复符号 / 缺符号 / ODR）"),
    _a("ptrace", "dynamic", 4,
       ("tracing",),
       ("api-misuse", "concurrency-race"),
       False, "declared", "ptrace 系统调用追踪；本批未接线"),
    _a("tsan", "sanitizer", 3,
       ("runtime-detection", "instrumentation"),
       ("concurrency-race", "concurrency-deadlock"),
       True, _MEASURED, "ThreadSanitizer；需 -pthread"),
    _a("ubsan", "sanitizer", 3,
       ("runtime-detection", "instrumentation"),
       ("ub-arithmetic", "ub-pointer", "ub-array-index", "ub-alignment", "language-sequencing"),
       True, _MEASURED, "UndefinedBehaviorSanitizer"),
    _a("valgrind", "dynamic", 4,
       ("runtime-detection", "post-mortem"),
       ("memory-use-after-free", "memory-uninitialized", "memory-leak", "concurrency-race"),
       False, "declared", "Valgrind memcheck/helgrind；本批未接线"),
    _a("wunsequenced", "compiler", 2,
       ("static-analysis",),
       ("language-sequencing",),
       True, _MEASURED, "`-Wunsequenced`：未定序修改"),
)

#: 静态/编译期资产（Static 臂口径；与 672g `STATIC_ASSETS` 语义一致）。
STATIC_ASSETS: frozenset[str] = frozenset(
    {"compiler-warn", "wunsequenced", "cross-compile", "linker"})

#: 池**刻意排除**的测量仪器（登记在案，防止有人又塞回来）。
EXCLUDED_MEASUREMENT_INSTRUMENTS: tuple[str, ...] = ("measure", "perf-counter")


# ─────────────────────────────────────────────────────────────────────────────
# 查询辅助
# ─────────────────────────────────────────────────────────────────────────────
def ids(pool: Iterable[AssetSpec] = ASSET_POOL) -> list[str]:
    """池中资产 id（保持池次序）。"""
    return [a.id for a in pool]


def by_id(asset_id: str, pool: Iterable[AssetSpec] = ASSET_POOL) -> AssetSpec:
    """按 id 取资产；不存在 ⇒ KeyError（fail-loud，不返回 None）。"""
    for a in pool:
        if a.id == asset_id:
            return a
    raise KeyError(f"资产 {asset_id!r} 不在池中")


def implemented_ids(pool: Iterable[AssetSpec] = ASSET_POOL) -> list[str]:
    """有实测判决归属的资产 id（replay 实验只能用这些）。"""
    return [a.id for a in pool if a.implemented]


def selectable_ids(pool: Iterable[AssetSpec] = ASSET_POOL) -> list[str]:
    """可作为选择候选的资产 id（本批 = 已实测资产）。"""
    return implemented_ids(pool)


def total_cost(asset_ids: Iterable[str], pool: Iterable[AssetSpec] = ASSET_POOL) -> int:
    """一组资产的**序数成本**之和（缺失 id ⇒ KeyError）。"""
    idx = {a.id: a for a in pool}
    return sum(idx[i].cost_units for i in asset_ids)


def verify_pool_integrity(pool: Iterable[AssetSpec] = ASSET_POOL) -> list[str]:
    """池自洽性检查；返回问题清单（空 = 健康）。fail-loud 由调用方决定。"""
    problems: list[str] = []
    items = list(pool)
    names = [a.id for a in items]

    if names != sorted(names):
        problems.append("池次序不是字典序（random.sample 依赖次序 ⇒ 必须钉死）")
    if len(names) != len(set(names)):
        problems.append("池中存在重复 id")
    for a in items:
        if a.id in EXCLUDED_MEASUREMENT_INSTRUMENTS:
            problems.append(f"{a.id}: 测量仪器不得进验证资产池")
        if a.cost_units < 1:
            problems.append(f"{a.id}: cost_units 必须 ≥1（实得 {a.cost_units}）")
        if not a.capabilities:
            problems.append(f"{a.id}: capabilities 为空")
        if not a.defect_types:
            problems.append(f"{a.id}: defect_types 为空")
        bad_c = set(a.capabilities) - set(CAPABILITIES)
        if bad_c:
            problems.append(f"{a.id}: capabilities 越出受控词表 {sorted(bad_c)}")
        bad_d = set(a.defect_types) - set(DEFECT_TYPES)
        if bad_d:
            problems.append(f"{a.id}: defect_types 越出受控词表 {sorted(bad_d)}")
        if a.implemented and a.evidence_source == "declared":
            problems.append(f"{a.id}: implemented=True 但 evidence_source=declared（自相矛盾）")
        if not a.implemented and a.evidence_source != "declared":
            problems.append(f"{a.id}: implemented=False 但 evidence_source≠declared")
    if not set(STATIC_ASSETS) <= set(names):
        problems.append(f"STATIC_ASSETS 有成员不在池中：{sorted(set(STATIC_ASSETS) - set(names))}")
    return problems


# ─────────────────────────────────────────────────────────────────────────────
# 自检
# ─────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    probs = verify_pool_integrity()
    chk("池自洽性无问题", not probs, f"({probs})")
    chk("池大小 = 12（8 实测 + 4 声明）", len(ASSET_POOL) == 12, f"({len(ASSET_POOL)})")
    chk("已实测资产 = 8", len(implemented_ids()) == 8, f"({implemented_ids()})")
    chk("池次序 = 字典序", ids() == sorted(ids()))
    chk("池不含 measure/perf-counter",
        not (set(ids()) & set(EXCLUDED_MEASUREMENT_INSTRUMENTS)))
    chk("STATIC_ASSETS ⊆ 池", set(STATIC_ASSETS) <= set(ids()))
    chk("每个资产都有成本/能力/适用类型",
        all(a.cost_units >= 1 and a.capabilities and a.defect_types for a in ASSET_POOL))
    chk("未知 id ⇒ KeyError", _raises(lambda: by_id("nope")))
    chk("total_cost 可算", total_cost(["asan", "compile-time"]) == 4,
        f"({total_cost(['asan', 'compile-time'])})")

    print(f"verifier_pool_673p selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _raises(fn) -> bool:
    try:
        fn()
    except (KeyError, ValueError, TypeError):
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def _fmt_table() -> str:
    rows = ["id                 kind        cost impl  capabilities / defect_types",
            "─" * 100]
    for a in ASSET_POOL:
        rows.append(f"{a.id:<18} {a.kind:<11} {a.cost_units:>4} {'Y' if a.implemented else 'n':<5}"
                    f" {','.join(a.capabilities)} | {','.join(a.defect_types)}")
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="673p B：验证资产池定义（拆仓第一层）")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--list", action="store_true", help="打印资产池")
    ap.add_argument("--json", action="store_true", help="机读输出")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()

    if a.list or a.json:
        doc = {
            "tool": "verifier_pool_673p",
            "version": VERSION,
            "pool_size": len(ASSET_POOL),
            "implemented": implemented_ids(),
            "static_assets": sorted(STATIC_ASSETS),
            "excluded_measurement_instruments": list(EXCLUDED_MEASUREMENT_INSTRUMENTS),
            "cost_basis": "declared_ordinal（本批未实测墙钟耗时）",
            "pool": [a.as_dict() for a in ASSET_POOL],
        }
        print(json.dumps(doc, ensure_ascii=False, indent=2) if a.json else _fmt_table())
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
