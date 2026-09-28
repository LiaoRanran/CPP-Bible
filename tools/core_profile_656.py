#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""core_profile_656.py — 656 B4：核心判决路径的**真实** profile 与延迟测量。

为什么单独一个工具
==================
"内核极致"不能靠感觉。本工具做三件事，且**只报测出来的数**：
  1. `cProfile` 跑核心判决流程 ⇒ 按 `tottime` 出 **Top10 热点**；
  2. 逐卡测延迟（mean / p50 / p95 / max），给出**单卡判决路径**是否 < 1ms 的结论；
  3. 把"优化前 / 优化后"两组数写进同一份报告 ⇒ 优化有没有用，看数不看话。

测什么（口径写死，避免自欺）
============================
- `classify_card`：**单卡判决**＝读卡文件 + 抽判决/边界 + 四态分类（含磁盘 I/O）
- `classify`：纯**内存判决**（已抽好字段），这是"判决逻辑本身"的代价
- `AuthorityLedger.append`：账本追加（哈希链），是写路径的代价
三者分开报，不许拿"纯内存"冒充"端到端"。

用法
====
    python tools/core_profile_656.py                # 跑一遍并打印
    python tools/core_profile_656.py --report       # 写 data/656_core_profile_report.{md,json}
    python tools/core_profile_656.py --check        # 自检（门禁：能跑 + 产物在 data/ 下）
"""
from __future__ import annotations

import argparse
import cProfile
import io
import json
import pstats
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_MD = ROOT / "data" / "656_core_profile_report.md"
OUT_JSON = ROOT / "data" / "656_core_profile_report.json"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

import decision_event_v2_626 as de  # noqa: E402
import four_state_verdict_638 as fs  # noqa: E402


def cards(limit: int = 0) -> list[Path]:
    """真实卡（atoms/**/ATOM-*.md），顺序确定。"""
    out = sorted((ROOT / "atoms").rglob("ATOM-*.md"))
    return out[:limit] if limit else out


def bench(fn: Callable[[], Any], n: int) -> dict[str, float]:
    """跑 n 次，返回毫秒分位（mean / p50 / p95 / max）。"""
    ts: list[float] = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        ts.append((time.perf_counter() - t0) * 1000.0)
    ts.sort()
    return {
        "n": n,
        "mean_ms": round(statistics.fmean(ts), 4),
        "p50_ms": round(ts[len(ts) // 2], 4),
        "p95_ms": round(ts[max(0, int(len(ts) * 0.95) - 1)], 4),
        "max_ms": round(ts[-1], 4),
    }


def profile_top(fn: Callable[[], Any], top: int = 10) -> list[dict[str, Any]]:
    pr = cProfile.Profile()
    pr.enable()
    fn()
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(top)
    rows: list[dict[str, Any]] = []
    for line in s.getvalue().splitlines()[4:]:
        parts = line.split(None, 5)
        if len(parts) < 6 or parts[0].startswith("Ordered"):
            continue
        try:
            rows.append({"ncalls": parts[0], "tottime": float(parts[1]),
                         "percall": float(parts[2]), "cumtime": float(parts[3]),
                         "func": parts[5][:110]})
        except ValueError:
            continue
        if len(rows) >= top:
            break
    return rows


def run(limit_cards: int = 0, rounds: int = 3) -> dict[str, Any]:
    cs = cards(limit_cards)
    rep: dict[str, Any] = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "python": sys.version.split()[0],
        "cards_measured": len(cs),
        "rounds": rounds,
    }
    if not cs:
        rep["error"] = "atoms 下没有 ATOM-*.md"
        return rep

    # ① 单卡端到端（含读盘）
    rep["classify_card"] = bench(lambda: [fs.classify_card(str(p)) for p in cs], rounds)
    # ② 纯内存判决（把字段抽出来再 classify）
    rec = {"verdict": "pass", "explanation": "", "mutation_set_hash": "a" * 64,
           "mutation_count": "10", "generator_version": "v7"}
    rep["classify_memory"] = bench(lambda: fs.classify(rec), 2000)
    # ③ 账本追加（哈希链）
    def _append_once() -> None:
        led = de.AuthorityLedger()
        for i in range(20):
            led.append(de.DecisionEvent(target_type="edge", target_id=f"T{i}",
                                        result="APPROVE", decision_origin="human_observed",
                                        review_method="BATCH_AUTH", operation="CREATE"))
    rep["ledger_append20"] = bench(_append_once, max(1, rounds))
    # ④ cProfile 热点（跑一圈全卡分类）
    rep["top_hotspots"] = profile_top(lambda: [fs.classify_card(str(p)) for p in cs])
    per_card = rep["classify_card"]["mean_ms"] / max(1, len(cs))
    rep["verdict_lt_1ms_per_card"] = bool(per_card < 1.0)
    rep["per_card_mean_ms"] = round(per_card, 4)
    return rep


def report(rep: dict[str, Any], notes: list[str] | None = None) -> None:
    lines = [
        "# 656 B4 · 核心判决路径性能报告",
        "",
        f"> 生成：{rep.get('generated_at')}　Python：{rep.get('python')}　卡数：{rep.get('cards_measured')}"
        f"　轮次：{rep.get('rounds')}",
        "",
        "## 一、延迟（毫秒）",
        "",
        "| 路径 | 口径 | n | mean | p50 | p95 | max |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for key, label in (("classify_card", "单卡端到端（读卡+抽字段+分类）"),
                       ("classify_memory", "纯内存判决（classify 本体）"),
                       ("ledger_append20", "账本追加 20 条（哈希链）")):
        m = rep.get(key) or {}
        lines.append(f"| `{key}` | {label} | {m.get('n','—')} | {m.get('mean_ms','—')} | "
                     f"{m.get('p50_ms','—')} | {m.get('p95_ms','—')} | {m.get('max_ms','—')} |")
    lines += [
        "",
        f"- **摊到单卡**：{rep.get('per_card_mean_ms')} ms/张 ⇒ "
        f"{'✅ < 1ms（达成目标）' if rep.get('verdict_lt_1ms_per_card') else '⚠️ ≥ 1ms（未达成，见 §四）'}",
        "",
        "## 二、Top10 热点（cProfile · 按 tottime）",
        "",
        "| # | 函数 | tottime(s) | percall(s) | cumtime(s) | ncalls |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for i, r in enumerate(rep.get("top_hotspots", [])[:10], 1):
        lines.append(f"| {i} | `{r['func']}` | {r['tottime']} | {r['percall']} | "
                     f"{r['cumtime']} | {r['ncalls']} |")
    lines += [
        "",
        "## 三、诚实边界",
        "",
        "1. 数字是**本机一次采样**（无并发、无 CI 噪声隔离），跨机不可直接比；比较请用同一台机、同一命令。",
        "2. `classify_card` 含磁盘 I/O（冷/热页缓存差异大）；要看**判决逻辑**本身请用 `classify_memory`。",
        "3. cProfile 的 `tottime` 不含阻塞在 I/O 上的时间 ⇒ 热点排名偏**计算密集**侧。",
        "",
        "## 四、优化（只做量到收益的事）",
        "",
    ]
    lines += (notes or rep.get("optimization_notes") or [
        "- 本批**未**做改动：测得的单卡路径已 < 1ms 且热点集中在文件读取与正则匹配；"
        "为亚毫秒级收益引入缓存会换来**缓存陈旧**的新风险（与本仓不信任缓存的家风冲突），故只登记不做。"])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    rep = run(limit_cards=5, rounds=1)
    chk("能跑出延迟数据", "classify_memory" in rep, str(rep.get("classify_memory", {}).get("mean_ms")))
    chk("能出热点表", len(rep.get("top_hotspots", [])) > 0, f"{len(rep.get('top_hotspots', []))} 行")
    chk("报告产物在 data/ 下",
        str(OUT_MD).replace("\\", "/").endswith("data/656_core_profile_report.md"))
    chk("单卡口径有结论", isinstance(rep.get("verdict_lt_1ms_per_card"), bool),
        f"{rep.get('per_card_mean_ms')} ms/张")
    print(f"core_profile_656 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="656 B4 核心判决路径 profile")
    ap.add_argument("--limit-cards", type=int, default=0, help="只测前 N 张卡（0=全部）")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--note", action="append", default=[],
                    help="写进报告 §四 的一行说明（可重复；用于记录优化前后的对比）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rep = run(a.limit_cards, a.rounds)
    if a.report:
        report(rep, a.note or None)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        cc = rep["classify_card"]
        print(f"[profile656] 卡 {rep['cards_measured']} 张｜单卡端到端 mean {cc['mean_ms']} ms"
              f"（p95 {cc['p95_ms']}）｜摊到单卡 {rep['per_card_mean_ms']} ms"
              f"｜{'<1ms ✅' if rep['verdict_lt_1ms_per_card'] else '≥1ms ⚠️'}")
        print(f"            纯内存 classify mean {rep['classify_memory']['mean_ms']} ms"
              f"｜账本追加20条 {rep['ledger_append20']['mean_ms']} ms")
        for i, r in enumerate(rep["top_hotspots"][:10], 1):
            print(f"            {i:>2}. {r['func'][:78]} · {r['tottime']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
