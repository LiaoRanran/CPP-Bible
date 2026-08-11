#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verification_audit.py — 验证状态标记覆盖度审计（对应 CONVENTIONS.md §10 / 宪章 §6）

度量"实现细节可靠性"这一最弱维度：
  1. 各章 [VERIFIED]/[UNVERIFIED]/[NEEDS-VERIFY] 标记覆盖度（含中文别名）。
  2. 高风险章（并发/内存模型/lock-free/perf/asm/ABI/优化）中"零标记"的 backlog，
     这些章是优先需要补 [VERIFIED]/[UNVERIFIED] 的对象。
  3. 九层真相标签 [标准]/[实现]/[ABI]/[平台]/[微架构]/[算法]/[工程]/[实验]/[假设] 的使用覆盖（对应 §1）。

用法：
  python tools/verification_audit.py [--root <repo>] [--json <path>] [--book <Book>]

输出：汇总到 stdout；可选 JSON 报告。
退出码：0（仅统计，不阻塞 CI）；可用作人工 backlog 跟踪。
"""
import argparse
import json
import os
import re
import sys

# 验证状态标记（含中文别名）
MARKERS = {
    "VERIFIED": re.compile(r"\[(?:VERIFIED|已验证)\]"),
    "UNVERIFIED": re.compile(r"\[(?:UNVERIFIED|未验证)\]"),
    "NEEDS-VERIFY": re.compile(r"\[(?:NEEDS-VERIFY|待验证|需核验)\]"),
}

# 九层真相标签
# 同时匹配 CONVENTIONS.md §1 规定的「裸标签」([标准]) 与「带后缀标签」([标准·xxx] / [实现·GCC15] / [平台·x86-64] / [微架构·Skylake] / [算法] / [工程] / [实验] / [假设])
TRUTH_LAYERS = {
    "标准": re.compile(r"\[标准(?:·[^\]]+)?\]"),
    "实现": re.compile(r"\[实现(?:·[^\]]+)?\]"),
    "ABI": re.compile(r"\[ABI(?:·[^\]]+)?\]"),
    "平台": re.compile(r"\[平台(?:·[^\]]+)?\]"),
    "微架构": re.compile(r"\[微架构(?:·[^\]]+)?\]"),
    "算法": re.compile(r"\[算法(?:·[^\]]+)?\]"),
    "工程": re.compile(r"\[工程(?:·[^\]]+)?\]"),
    "实验": re.compile(r"\[实验(?:·[^\]]+)?\]"),
    "假设": re.compile(r"\[假设(?:·[^\]]+)?\]"),
}

# 高风险关键词（命中即视为该章含高风险断言，需验证标记）
RISK_KEYWORDS = {
    "concurrency": re.compile(
        r"atomic|memory_order|lock[_ -]?free|data race|std::mutex|std::thread|"
        r"happens[_ -]?before|acquire|release|seq_cst|hazard|RCU|\bABA\b|"
        r"并发|原子|内存序|无锁|数据竞争", re.I),
    "memory_model": re.compile(r"memory model|内存模型|consume|relaxed", re.I),
    "perf": re.compile(
        r"benchmark|基准|cache|SIMD|分支预测|false sharing|伪共享|throughput|"
        r"latency|吞吐|延迟|cache line", re.I),
    "asm": re.compile(r"反汇编|assembly|disassembly|汇编|call \[|寄存器|`-O2`|vtable 布局", re.I),
    "abi": re.compile(r"名称修饰|mangling|调用约定|对象布局|vtable|RTTI|abi", re.I),
    "optimization": re.compile(r"内联|inline|devirtual|常量传播|循环展开|`-O[0-9]`|优化", re.I),
}


def iter_chapter_files(book_root):
    """遍历 Book 下所有 .md（主章 +  legacy 一并统计，但主章单独标记）。"""
    for dirpath, _dirs, files in os.walk(book_root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, book_root)
            is_main = bool(re.search(r"ch\d+_", fn)) and not rel.startswith("_legacy")
            yield full, rel, is_main


def audit_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return None
    counts = {k: len(rx.findall(text)) for k, rx in MARKERS.items()}
    truth = {k: len(rx.findall(text)) for k, rx in TRUTH_LAYERS.items()}
    risks = {k: bool(rx.search(text)) for k, rx in RISK_KEYWORDS.items()}
    is_risk = any(risks.values())
    total_markers = sum(counts.values())
    return {
        "counts": counts,
        "truth": truth,
        "risks": risks,
        "is_risk": is_risk,
        "total_markers": total_markers,
        "has_any_marker": total_markers > 0,
    }


def main():
    ap = argparse.ArgumentParser(description="验证状态标记覆盖度审计")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--book", default="Book")
    ap.add_argument("--json", default=None, help="输出 JSON 报告路径")
    args = ap.parse_args()

    book_root = os.path.join(args.root, args.book)
    if not os.path.isdir(book_root):
        print(f"[ERR] Book 目录不存在: {book_root}", file=sys.stderr)
        return 2

    main_files = []
    legacy_files = []
    for full, rel, is_main in iter_chapter_files(book_root):
        res = audit_file(full)
        if res is None:
            continue
        rec = {"rel": rel, **res}
        if is_main:
            main_files.append(rec)
        else:
            legacy_files.append(rec)

    # 统计
    def summarize(recs):
        n = len(recs)
        with_marker = sum(1 for r in recs if r["has_any_marker"])
        risk_recs = [r for r in recs if r["is_risk"]]
        risk_zero = [r for r in risk_recs if not r["has_any_marker"]]
        truth_any = sum(1 for r in recs if any(r["truth"].values()))
        return {
            "n": n,
            "with_marker": with_marker,
            "with_marker_pct": round(100.0 * with_marker / n, 1) if n else 0.0,
            "risk_n": len(risk_recs),
            "risk_zero": len(risk_zero),
            "truth_any": truth_any,
            "risk_zero_list": [r["rel"] for r in risk_zero],
        }

    s_main = summarize(main_files)
    s_legacy = summarize(legacy_files)

    # 各标记类型总量
    marker_totals = {k: sum(r["counts"][k] for r in main_files) for k in MARKERS}
    truth_totals = {k: sum(r["truth"][k] for r in main_files) for k in TRUTH_LAYERS}

    # 风险类别命中（主章）
    risk_cat = {k: sum(1 for r in main_files if r["risks"][k]) for k in RISK_KEYWORDS}

    print("=" * 60)
    print("CPP-Bible 验证状态标记审计 (verification_audit)")
    print("=" * 60)
    print(f"主章文件数        : {s_main['n']}")
    print(f"含验证标记的主章  : {s_main['with_marker']} ({s_main['with_marker_pct']}%)")
    print(f"使用真相标签的主章: {s_main['truth_any']} ({round(100.0*s_main['truth_any']/s_main['n'],1) if s_main['n'] else 0}%)")
    print(f"高风险主章数      : {s_main['risk_n']}")
    print(f"  其中零标记      : {s_main['risk_zero']}  <-- 优先 backlog")
    print("-" * 60)
    print("验证标记总量(主章):", marker_totals)
    print("真相标签总量(主章):", truth_totals)
    print("风险类别命中(主章):", risk_cat)
    print("-" * 60)
    print(f"legacy 文件       : {s_legacy['n']} (含标记 {s_legacy['with_marker']}, 高风险零标记 {s_legacy['risk_zero']})")
    print("=" * 60)
    print(f"RESULT: 主章验证标记覆盖 {s_main['with_marker_pct']}%；高风险零标记 backlog = {s_main['risk_zero']} 章")
    if s_main["risk_zero_list"]:
        print("BACKLOG (高风险且零验证标记的主章):")
        for rel in s_main["risk_zero_list"]:
            print(f"  - {rel}")

    if args.json:
        report = {
            "summary_main": s_main,
            "summary_legacy": s_legacy,
            "marker_totals": marker_totals,
            "truth_totals": truth_totals,
            "risk_categories": risk_cat,
            "details": main_files,
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nJSON 报告 -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
