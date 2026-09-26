"""646 · 阶段 A3/A4 · 进程内记忆化（性能优化，只读）。

目标（646 §三 A3/A4）：消除耦合管线里的**重复重计算**——多个工具反复调用同一批重读函数
（`gate_engine.run` 全库 gate 扫描、`evidence_base_644.list_atoms/card_evidence_map/iter_stored`），
每次都重新解析/读盘。本模块用 `functools.lru_cache` 做**进程内单次缓存**，供 646 工具共享。

安全边界：
- **只读**：只缓存，不改任何生产数据；返回的是同一对象（调用方只读，不修改）。
- 缓存键为「无参」⇒ 一次进程内结果一致（本批所有工具在同一仓库快照上运行）。
- `clear()` 供测试隔离使用（避免跨测试污染）。
- `--check`：只读自检（验证缓存命中与一致性）。`--stats`：打印缓存与计时信息。
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from functools import lru_cache
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@lru_cache(maxsize=1)
def finding_rule_ids() -> tuple[str, ...]:
    """全库 gate 扫描的命中规则 id（真实，缓存）。"""
    import gate_engine as ge
    return tuple(f.rule_id for f in ge.run(include_advice=True))


@lru_cache(maxsize=1)
def finding_counts() -> dict[str, int]:
    """命中规则 id → 次数（真实，缓存）。"""
    counts: dict[str, int] = {}
    for rid in finding_rule_ids():
        counts[rid] = counts.get(rid, 0) + 1
    return counts


@lru_cache(maxsize=1)
def atoms() -> tuple[dict, ...]:
    """真实原子卡（缓存；元素只读）。"""
    import evidence_base_644 as base
    return tuple(base.list_atoms())


@lru_cache(maxsize=1)
def card_evidence_map() -> dict:
    """EV→卡 映射（缓存）。"""
    import evidence_base_644 as base
    return dict(base.card_evidence_map())


@lru_cache(maxsize=1)
def stored_records() -> tuple[tuple, ...]:
    """落库证据记录（evidence_id, grade, credibility, source_type, card）（缓存）。"""
    import evidence_base_644 as base
    out = []
    for rec in base.iter_stored():
        out.append((rec.evidence_id, rec.grade, rec.credibility,
                    rec.source_type, rec.meta.get("card")))
    return tuple(out)


def clear() -> None:
    """清空全部缓存（测试隔离用）。"""
    for fn in (finding_rule_ids, finding_counts, atoms, card_evidence_map, stored_records):
        fn.cache_clear()


def selftest() -> int:
    """只读自检：第二次调用命中缓存且结果一致。"""
    a = atoms()
    b = atoms()
    assert a is b, "缓存未命中"
    assert len(a) >= 1
    # counts 与 ids 一致
    assert sum(finding_counts().values()) == len(finding_rule_ids())
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--stats` 打印缓存计时。"""
    ap = argparse.ArgumentParser(description="646 进程内记忆化（A3/A4，只读）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--stats", action="store_true", help="打印缓存计时")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    t0 = time.perf_counter()
    n = len(finding_rule_ids())
    t1 = time.perf_counter()
    _ = finding_rule_ids()
    t2 = time.perf_counter()
    print(f"[646 perf] 命中规则 {n}；首算 {(t1-t0)*1000:.1f}ms，缓存命中 {(t2-t1)*1000:.3f}ms")
    for name, fn in (("atoms", atoms), ("card_evidence_map", card_evidence_map),
                     ("stored_records", stored_records)):
        print(f"  {name}: info={fn.cache_info()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
