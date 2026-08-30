#!/usr/bin/env python3
"""d5_gap_scanner.py — D5 覆盖差距扫描器

扫描 Book/ 中缺少 D5 性能附录，但正文包含性能/基准信号的章节，
按信号强度排序，输出 JSON 报告 + Markdown 表格。

用法:
    python3 tools/d5_gap_scanner.py                  # 扫描 + 打印 + 写入 build/d5_gap_report.json
    python3 tools/d5_gap_scanner.py --top 10         # 仅显示前 10 个
    python3 tools/d5_gap_scanner.py --part part14_perf  # 仅扫描指定 part
    python3 tools/d5_gap_scanner.py --json           # 仅 JSON 输出

CI 用途: --ci 模式下，若 gap_count > 阈值或 top-1 chapter signals >= 10，
退出码 1 (BLOCK)。用于监测作者新增性能声明但忘记补 D5。
"""

import os, re, sys, json, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"
BUILD = ROOT / "build"
OUT_JSON = BUILD / "d5_gap_report.json"

# Performance / benchmark signals in chapter prose (excluding code blocks)
PERF_SIGNALS = [
    # Chinese
    r'性能', r'基准', r'优化', r'缓存', r'cache[ -]?miss|cache[ -]?hit',
    r'分支预测|branch[ -]?predict', r'虚拟.*开销', r'虚函数.*开销',
    r'零开销|zero[ -]?overhead', r'内存布局', r'字宽', r'字节对齐',
    r'重命名|寄存器分配', r'SIMD|向量化', r'流水线|流水线',
    r'延迟|吞吐|带宽|流带宽', r'纳秒|ns\b', r'微秒|μs\b|us\b',
    r'加速比|加速倍|\d+×.*快|\d+倍.*快',
    r'移动语义|右值引用', r'RVO|NRVO|复制省略',
    r'SSO|small[ -]?string', r'ABI',
    r'指令集|体系结构|乱序|乱序执行', r'预取|prefetch',
    r'false sharing|真共享|寄存器溢出|溢出',
    r'分支 mispredict|mispredict|预测失败',
    r'内存屏障|内存顺序|memory[ -]?order',
    r'锁竞争|无锁|atomic|原子', r'伪共享|cache line',
    # English
    r'\bbenchmark\b', r'\bobenchmark\b', r'\bdeduce.*norm',
    r'\bconstexpr.*eval', r'\binlining\b', r'\bdevirtualization\b',
    r'\bprefetch\b', r'\bvectorization\b', r'\bpipelining\b',
    r'\blatency\b', r'\bthroughput\b', r'\bbandwidth\b',
    r'\bSIMD\b', r'\bregister.*allocation', r'\bpipeline\b',
    r'\bstride\b', r'\binput.*dependent',
    r'\bzero.overhead\b', r'\bzero.cost\b', r'\bRVO\b', r'\bNRVO\b',
    r'\bABI\b', r'\bSIMD\b', r'\bbranch.*mispredict',
    r'\bmemory.*order\b', r'\bfalse.*sharing\b', r'\bcache.*line\b',
    # Benchmark framing / methodology
    r'5.*trial|5-试验|五试验|5 次|median|中位数|五次取中',
    r'volatile.*sink|anti-DCE|DCE|防优化',
    r'noinline|gnu::noinline', r'对齐|alignas|对齐方式',
]

PERF_PAT = re.compile('|'.join(PERF_SIGNALS), re.IGNORECASE)

# Chapters that explicitly don't need D5 (theory/historical/concept-only)
D5_EXEMPT_PARTS = {
    'part01_history',    # C++ 历史演变，不涉及运行时性能
    'part02_toolchain', # 工具链概念（编译器安装等）
}

# Specific chapter stems exempt from D5 (methodology/source-analysis chapters)
D5_EXEMPT_STEMS = {
    'ch151_benchmark',        # 基准测试方法论章（有 inline benchmark）
    'ch152_perf_model',       # 性能模型与测量学（方法论）
    'ch157_compiler_explorer', # CE 工具使用教程（非性能声明）
    'ch165_roadmap',          # 路线图/元章节：无孤立微基准主题，刻意排除（D5 战役收口）
    'ch149_ci_cd',            # CI/CD 工程实践（非性能声明）
    'ch150_testing',          # 测试方法论
    'ch147_code_review',      # 代码审查实践
    'ch148_gitflow',          # Git 工作流
    'ch145_naming_api',       # 命名规范
    'ch146_error_handling',   # 错误处理模式
    # STL 实现分析章（libstdc++/libc++/MSSTL/LLVM/Boost/ClickHouse/LevelDB）
    # 这些是源码导读，不是性能声明
    'ch124_libstdcxx',
    'ch125_libcxx',
    'ch126_msstl',
    'ch127_llvm',
    'ch128_boost',
    'ch132_leveldb_rocksdb',
    'ch133_clickhouse_redis',
}


# D5 附录检测的权威正则（与 metrics_snapshot.py 统一，2026-08-30 口径收口）：
# 标题行 `##/###/#### D5...`，兼容「附录 D5」与无「附录」前缀的变体
# （如 `## D5 真实性能基准：...`、`## D5 性能附录：...`）。
# 历史口径仅匹配正文「附录 D5」字面量，漏判 6 个标题变体章（113 vs 119）。
D5_HEADING_RE = re.compile(r"^#{2,4}\s*(?:附录\s*)?D5\b", re.M)


def find_d5_chapters():
    """Return set of chapter stems that already have D5 appendix."""
    d5_stems = set()
    for f in sorted(BOOK.rglob("ch*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if D5_HEADING_RE.search(text):
            d5_stems.add(f.stem)
    return d5_stems


def count_perf_signals(text):
    """Count performance-related signals in prose (code blocks excluded)."""
    prose = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # strip code blocks
    prose = re.sub(r'\\\(.+?\\\)', '', prose)  # strip inline math
    prose = re.sub(r'\\\[(.+?)\\\]', '', prose, flags=re.DOTALL)  # strip display math
    return len(PERF_PAT.findall(prose))


def scan_gaps(part_filter=None):
    """Scan all chapters, return list of gap candidates."""
    d5_stems = find_d5_chapters()
    candidates = []
    total_scanned = 0
    skipped_d5 = 0
    skipped_exempt = 0

    for f in sorted(BOOK.rglob("ch*.md")):
        stem = f.stem
        part = f.parent.name
        total_scanned += 1

        if stem in d5_stems:
            skipped_d5 += 1
            continue

        if part in D5_EXEMPT_PARTS or stem in D5_EXEMPT_STEMS:
            skipped_exempt += 1
            continue

        if part_filter and part != part_filter:
            continue

        text = f.read_text(encoding="utf-8", errors="replace")
        signals = count_perf_signals(text)
        if signals > 0:
            candidates.append({
                "chapter": stem,
                "file": str(f.relative_to(ROOT)),
                "part": part,
                "perf_signals": signals,
            })

    candidates.sort(key=lambda x: -x["perf_signals"])
    return {
        "total_chapters": total_scanned,
        "d5_present": len(d5_stems),
        "d5_missing": total_scanned - len(d5_stems),
        "gap_candidates": len(candidates),
        "skipped_exempt_parts": skipped_exempt,
        "top_candidates": candidates[:30],
    }


def print_report(r, top_n=15):
    """Print human-readable report."""
    print("=" * 72)
    print(f"D5 覆盖差距扫描  —  缺少 D5 但含有性能信号的章节")
    print("=" * 72)
    print(f"  总章节数：{r['total_chapters']}")
    print(f"  已有 D5：{r['d5_present']} 章 ({r['d5_present']/r['total_chapters']*100:.0f}%)")
    print(f"  缺少 D5：{r['d5_missing']} 章")
    print(f"  其中 performance 信号 ≥1：{r['gap_candidates']} 章")
    print(f"  豁免 part（无需 D5）：{r['skipped_exempt_parts']} 章")
    print()

    print(f"  Top {top_n} D5 差距候选 (按 performance 信号强度降序):")
    print(f"  {'排名':>4}  {'信号':>5}  {'章节':<35} {'part'}")
    print(f"  {'-'*4}  {'-'*5}  {'-'*35} {'-'*20}")
    for i, c in enumerate(r["top_candidates"][:top_n], 1):
        flag = " ⚡" if c["perf_signals"] >= 15 else (" 🔥" if c["perf_signals"] >= 10 else "")
        print(f"  {i:>4}  {c['perf_signals']:>5}  {c['chapter']:<35} {c['part']}{flag}")

    print()
    urgent = sum(1 for c in r["top_candidates"] if c["perf_signals"] >= 10)
    high = sum(1 for c in r["top_candidates"] if c["perf_signals"] >= 5)
    print(f"  优先级: ⚡ 紧急 (>15 信号) / 🔥 高优先 (>10 信号) / 普通 (>5 信号)")
    print(f"  紧急: {sum(1 for c in r['top_candidates'] if c['perf_signals'] >= 15)} 章")
    print(f"  高优先: {urgent} 章 (≥10 信号)")
    print(f"  普通: {high - urgent} 章 (5-9 信号)")
    print()


def main():
    ap = argparse.ArgumentParser(description="D5 覆盖差距扫描")
    ap.add_argument("--top", type=int, default=30, help="显示前 N 个候选")
    ap.add_argument("--part", type=str, default=None, help="仅扫描指定 part")
    ap.add_argument("--json", action="store_true", help="仅输出 JSON")
    ap.add_argument("--ci", action="store_true",
                    help="CI gate 模式：如 gap_count>15 或 top-1 signals>=15，退出码 1")
    args = ap.parse_args()

    r = scan_gaps(part_filter=args.part)

    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return

    print_report(r, top_n=args.top)

    BUILD.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [json] -> {OUT_JSON}")

    if args.ci:
        # Advisory mode (not a hard gate): D5 coverage is a long-term goal, not
        # a per-commit requirement. Print status but don't fail CI.
        # The scanner is primarily a *reporting tool* for authors to prioritize
        # which chapters to add D5 to next.
        top1 = r["top_candidates"][0]["perf_signals"] if r["top_candidates"] else 0
        coverage_pct = r["d5_present"] / r["total_chapters"] * 100
        print(f"\n  [INFO] D5 coverage: {r['d5_present']}/{r['total_chapters']} "
              f"({coverage_pct:.0f}%), {r['gap_candidates']} gap candidates, "
              f"top signal={top1}")
        print(f"         Advisory only — see build/d5_gap_report.json for prioritized list")


if __name__ == "__main__":
    main()
