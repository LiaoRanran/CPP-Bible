#!/usr/bin/env python3
"""expansion_audit.py — 扩写空间审计

扫描全书，按四维度（广度/深度/样例/经验）定位扩写靶点，输出优先队列。

用法:
    python3 tools/expansion_audit.py              # 标准报告
    python3 tools/expansion_audit.py --top 20     # Top 20 靶章
    python3 tools/expansion_audit.py --chapter ch04_cpp11  # 单章详情
    python3 tools/expansion_audit.py --json       # JSON 输出(供下游工具消费)

四维度定义:
  广度(Breadth):   该章是否覆盖了足够多的关联知识点?
                   度量=交引数+二级标题数+工业引用数
  深度(Depth):     该章是否深入到底层(汇编/性能数据/标准提案)?
                   度量=深cpp块比例+无估算用语+有源码引用
  样例(Example):   代码示例是否可独立编译、规模足够?
                   度量=自含率+浅块比例(反)+含main块数
  经验(Experience): 该章是否有工业实践/踩坑/最佳实践?
                   度量=工业引用+断言块+有"陷阱"关键词
"""

import argparse
import json
import pathlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent
CPP_FENCE = re.compile(r'^\s*```cpp')
FENCE_END = re.compile(r'^\s*```\s*$')

# ── 数据采集 ──────────────────────────────────────────────


@dataclass
class ChapterStats:
    stem: str
    part: str = ""
    total_lines: int = 0
    cpp_blocks: int = 0
    total_cpp_lines: int = 0
    shallow_blocks: int = 0          # <5 lines
    deep_blocks: int = 0             # >=20 lines
    self_contained_blocks: int = 0   # has #include
    has_main_blocks: int = 0
    has_assert_blocks: int = 0
    tilde_claims: int = 0            # ~N unit
    industry_refs: int = 0
    h2_count: int = 0
    xref_count: int = 0              # cross-references
    pitfall_mentions: int = 0        # "陷阱/注意/误区/踩坑/常见错误"
    assembly_mentions: int = 0       # "汇编/mov/lea/call/ret/x86/ARM/RISC-V"

    # computed
    shallow_pct: float = 0.0
    self_pct: float = 0.0
    deep_pct: float = 0.0
    score_breadth: float = 0.0
    score_depth: float = 0.0
    score_example: float = 0.0
    score_experience: float = 0.0
    score_total: float = 0.0


TILDE_RE = re.compile(r'~\d+\s*(ns|us|ms|cycles|s|μs|MB|KB|GB)')
INDUSTRY_RE = re.compile(
    r'(github\.com|llvm\.org|boost\.org|chromium|abseil|leveldb|rocksdb'
    r'|clickhouse|redis|qt\.io|unreal|fmtlib|spdlog|protobuf|grpc|tbb'
    r'|oneAPI|cuda|openmp|dotnet|webkit|v8|node\.js)', re.I)
PITFALL_RE = re.compile(r'(陷阱|注意|误区|踩坑|常见错误|切勿|不要|避免|危险|警告)')
ASM_RE = re.compile(r'(汇编|mov\b|lea\b|call\b|ret\b|x86|ARM|RISC-V|AVX|SSE|NEON|objdump|Compiler Explorer|godbolt)', re.I)


def collect() -> dict[str, ChapterStats]:
    """扫描全书，返回 ch_stem → ChapterStats"""
    stats: dict[str, ChapterStats] = {}
    for fpath in sorted((ROOT / "Book").glob("**/ch*.md")):
        if '.bak' in str(fpath):
            continue
        stem = fpath.stem
        cs = ChapterStats(stem=stem, part=fpath.parent.name)
        text = fpath.read_text(encoding='utf-8')
        lines = text.splitlines()
        cs.total_lines = len(lines)
        cs.tilde_claims = len(TILDE_RE.findall(text))
        cs.industry_refs = len(set(INDUSTRY_RE.findall(text)))
        cs.h2_count = sum(1 for ln in lines if ln.startswith('## '))
        cs.pitfall_mentions = len(PITFALL_RE.findall(text))
        cs.assembly_mentions = len(ASM_RE.findall(text))
        cs.xref_count = sum(1 for ln in lines if '⟶' in ln or 'ch' in ln.lower() and '.md' in ln)

        i = 0
        while i < len(lines):
            if CPP_FENCE.match(lines[i]):
                j = i + 1
                buf = []
                while j < len(lines) and not FENCE_END.match(lines[j]):
                    buf.append(lines[j])
                    j += 1
                blk = "\n".join(buf)
                blk_lines = len(buf)
                cs.cpp_blocks += 1
                cs.total_cpp_lines += blk_lines
                if blk_lines < 5:
                    cs.shallow_blocks += 1
                if blk_lines >= 20:
                    cs.deep_blocks += 1
                if '#include' in blk:
                    cs.self_contained_blocks += 1
                if 'int main' in blk:
                    cs.has_main_blocks += 1
                if 'static_assert' in blk or 'assert(' in blk:
                    cs.has_assert_blocks += 1
                i = j + 1
            else:
                i += 1

        stats[stem] = cs
    return stats


# ── 评分 ──────────────────────────────────────────────────


def score_all(stats: dict[str, ChapterStats]) -> list[ChapterStats]:
    """计算四维得分 + 总分，返回排序列表"""
    all_cs = list(stats.values())
    n = len(all_cs)

    # 归一化辅助
    def norm(val, max_val):
        return min(val / max(max_val, 1), 1.0)

    blk_max = max(cs.cpp_blocks for cs in all_cs)
    xref_max = max(cs.xref_count for cs in all_cs)
    h2_max = max(cs.h2_count for cs in all_cs)
    ind_max = max(cs.industry_refs for cs in all_cs)
    tilde_max = max(cs.tilde_claims for cs in all_cs)
    asm_max = max(cs.assembly_mentions for cs in all_cs)
    pit_max = max(cs.pitfall_mentions for cs in all_cs)

    for cs in all_cs:
        blk = max(1, cs.cpp_blocks)
        cs.shallow_pct = cs.shallow_blocks / blk
        cs.self_pct = cs.self_contained_blocks / blk
        cs.deep_pct = cs.deep_blocks / blk

        # 广度: 交引面 + 标题覆盖面 + 工业引用面 (越高越好, 但这里算"待扩写"=反)
        cs.score_breadth = round((
            (1 - norm(cs.xref_count, xref_max)) * 35 +
            (1 - norm(cs.h2_count, h2_max)) * 30 +
            (1 - norm(cs.industry_refs, ind_max)) * 35
        ), 1)

        # 深度: 缺汇编 + 估算多 + 缺深块 (越高=越薄)
        cs.score_depth = round((
            (1 - norm(cs.assembly_mentions, asm_max)) * 35 +
            norm(cs.tilde_claims, tilde_max) * 35 +
            (1 - cs.deep_pct) * 30
        ), 1)

        # 样例: 不自含 + 浅块多 + 缺完整程序 (越高=样例越弱)
        cs.score_example = round((
            (1 - cs.self_pct) * 40 +
            cs.shallow_pct * 30 +
            (1 - norm(cs.has_main_blocks, blk_max)) * 30
        ), 1)

        # 经验: 缺工业引用 + 缺踩坑 + 缺断言
        cs.score_experience = round((
            (1 - norm(cs.industry_refs, ind_max)) * 40 +
            (1 - norm(cs.pitfall_mentions, pit_max)) * 30 +
            (1 - norm(cs.has_assert_blocks, blk_max)) * 30
        ), 1)

        cs.score_total = round(
            cs.score_breadth * 0.25 +
            cs.score_depth * 0.25 +
            cs.score_example * 0.30 +
            cs.score_experience * 0.20, 1
        )

    return sorted(all_cs, key=lambda x: -x.score_total)


# ── 输出 ──────────────────────────────────────────────────


def print_header():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  扩写空间审计  (广度/深度/样例/经验 四维)                   ║")
    print("║  得分越高 = 越急需扩写   得分越低 = 已足够饱满              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def print_global(stats: dict[str, ChapterStats]):
    """全局摘要"""
    n = len(stats)
    total_blk = sum(cs.cpp_blocks for cs in stats.values())
    total_shallow = sum(cs.shallow_blocks for cs in stats.values())
    total_self = sum(cs.self_contained_blocks for cs in stats.values())
    total_tilde = sum(cs.tilde_claims for cs in stats.values())
    total_ind = sum(cs.industry_refs for cs in stats.values())
    no_ind = sum(1 for cs in stats.values() if cs.industry_refs == 0)

    print(f"── 全局概要 (n={n} 章) ──")
    print(f"  cpp块: {total_blk}  浅(<5行): {total_shallow} ({100*total_shallow/max(1,total_blk):.0f}%)  深(>=20): {sum(cs.deep_blocks for cs in stats.values())}")
    print(f"  自含: {total_self} ({100*total_self/max(1,total_blk):.0f}%)  估算用语: {total_tilde}  工业引用: {total_ind}")
    print(f"  零工业引用: {no_ind}/{n} ({100*no_ind//n}%)")
    print()


def report_completion(stats: dict[str, ChapterStats]):
    """绝对阈值完成度报告（不依赖 max 归一化）。

    归一化评分只能排序"相对最弱"，无法判断"是否已达标"。本函数用
    绝对阈值给出四维度"已达标章数 / 147"，使 ROADMAP_v3 的真实剩余
    缺口（样例浅块、深度估算用语）可见、可度量、可驱动。

    阈值（可调，基于全书分布经验值）：
      广度:  xref_count >= 12                —— 已有顶部+底部交叉引用簇
      深度:  assembly_mentions >= 2 且 tilde_claims <= 3  —— 有底层分析且少伪造估算
      样例:  shallow_pct <= 0.30 且 self_pct >= 0.80  —— 少浅块且高自含
      经验:  industry_refs >= 3 且 pitfall_mentions >= 4  —— 有工业引用且点出陷阱
    """
    BREADTH_OK = 12
    DEPTH_ASM_OK = 2
    DEPTH_TILDE_OK = 3
    EX_SHALLOW_OK = 0.30
    EX_SELF_OK = 0.80
    EXP_IND_OK = 3
    EXP_PIT_OK = 4

    n = len(stats)
    c_breadth = sum(1 for cs in stats.values() if cs.xref_count >= BREADTH_OK)
    c_depth = sum(1 for cs in stats.values()
                  if cs.assembly_mentions >= DEPTH_ASM_OK and cs.tilde_claims <= DEPTH_TILDE_OK)
    c_example = sum(1 for cs in stats.values()
                    if cs.shallow_pct <= EX_SHALLOW_OK and cs.self_pct >= EX_SELF_OK)
    c_exp = sum(1 for cs in stats.values()
                if cs.industry_refs >= EXP_IND_OK and cs.pitfall_mentions >= EXP_PIT_OK)

    print(f"── 四维度绝对完成度（阈值法，n={n}）──")
    print(f"  广度(交引≥{BREADTH_OK}):        {c_breadth:>3}/{n}  ({100*c_breadth//n:>3}%)")
    print(f"  深度(汇编≥{DEPTH_ASM_OK} 且 估算≤{DEPTH_TILDE_OK}): {c_depth:>3}/{n}  ({100*c_depth//n:>3}%)")
    print(f"  样例(浅块≤{int(EX_SHALLOW_OK*100)}% 且 自含≥{int(EX_SELF_OK*100)}%): {c_example:>3}/{n}  ({100*c_example//n:>3}%)")
    print(f"  经验(工业≥{EXP_IND_OK} 且 陷阱≥{EXP_PIT_OK}): {c_exp:>3}/{n}  ({100*c_exp//n:>3}%)")
    print()


def print_top(ranked: list[ChapterStats], top_n: int = 20):
    """优先队列"""
    print(f"── 扩写优先队列 (Top {top_n}) ──")
    print(f"  {'章':<30} {'总分':>5} {'广度':>5} {'深度':>5} {'样例':>5} {'经验':>5}  {'浅/总':>6} {'自含%':>5} {'估算':>4} {'工业':>4}")
    print(f"  {'─'*30} {'─'*5} {'─'*5} {'─'*5} {'─'*5} {'─'*5}  {'─'*6} {'─'*5} {'─'*4} {'─'*4}")
    for cs in ranked[:top_n]:
        print(f"  {cs.stem:<30} {cs.score_total:>5.0f} {cs.score_breadth:>5.0f} {cs.score_depth:>5.0f} "
              f"{cs.score_example:>5.0f} {cs.score_experience:>5.0f}  "
              f"{cs.shallow_blocks:>3}/{cs.cpp_blocks:<3} {100*cs.self_pct:>4.0f}% {cs.tilde_claims:>4} {cs.industry_refs:>4}")
    print()


def print_chapter_detail(cs: ChapterStats):
    """单章详细诊断"""
    print(f"\n── {cs.stem} ({cs.part}) 扩写诊断 ──")
    print(f"  总行数: {cs.total_lines}  cpp块: {cs.cpp_blocks} ({cs.total_cpp_lines}行)")
    print(f"  浅块(<5行): {cs.shallow_blocks} ({100*cs.shallow_pct:.0f}%)  深块(>=20): {cs.deep_blocks} ({100*cs.deep_pct:.0f}%)")
    print(f"  自含(#include): {cs.self_contained_blocks} ({100*cs.self_pct:.0f}%)  main: {cs.has_main_blocks}  assert: {cs.has_assert_blocks}")
    print(f"  估算用语: {cs.tilde_claims}  工业引用: {cs.industry_refs}")
    print(f"  交引: {cs.xref_count}  H2: {cs.h2_count}  踩坑: {cs.pitfall_mentions}  汇编: {cs.assembly_mentions}")
    print()
    print(f"  四维得分 (越高越急需):")
    print(f"    广度: {cs.score_breadth:.0f}/100  {'⚠️ 缺关联知识' if cs.score_breadth>60 else '✓ 覆盖面够'}")
    print(f"    深度: {cs.score_depth:.0f}/100  {'⚠️ 缺底层分析' if cs.score_depth>60 else '✓ 深度够'}")
    print(f"    样例: {cs.score_example:.0f}/100  {'⚠️ 样例需强化' if cs.score_example>60 else '✓ 样例够'}")
    print(f"    经验: {cs.score_experience:.0f}/100  {'⚠️ 缺工业实践' if cs.score_experience>60 else '✓ 经验够'}")
    print(f"    综合: {cs.score_total:.0f}/100")

    # 针对性建议
    suggestions = []
    if cs.score_breadth > 60:
        suggestions.append("补交叉引用 + 关联知识旁注 + 真实工业项目引用")
    if cs.score_depth > 60:
        suggestions.append("补汇编分析(godbolt链接) + 实测性能数据 + WG21提案溯源")
    if cs.score_example > 60:
        suggestions.append("浅块合并为完整示例(含main+#include) + 展示运行输出")
    if cs.score_experience > 60:
        suggestions.append("补工业踩坑案例(真实issue/bug链接) + 常见错误对比 + 断言验证")
    if suggestions:
        print(f"  建议扩写方向:")
        for sug in suggestions:
            print(f"    → {sug}")


# ── CLI ───────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="扩写空间审计")
    parser.add_argument("--top", type=int, default=20, help="Top N 靶章")
    parser.add_argument("--chapter", type=str, help="单章诊断 (e.g. ch04_cpp11)")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    stats = collect()
    ranked = score_all(stats)

    if args.chapter:
        if args.chapter in stats:
            print_chapter_detail(stats[args.chapter])
        else:
            print(f"章 {args.chapter} 不存在", file=sys.stderr)
            sys.exit(1)
        return

    if args.json:
        out = []
        for cs in ranked:
            out.append({
                "stem": cs.stem, "part": cs.part, "total_lines": cs.total_lines,
                "cpp_blocks": cs.cpp_blocks, "shallow_blocks": cs.shallow_blocks,
                "deep_blocks": cs.deep_blocks, "self_contained": cs.self_contained_blocks,
                "tilde_claims": cs.tilde_claims, "industry_refs": cs.industry_refs,
                "scores": {
                    "breadth": cs.score_breadth, "depth": cs.score_depth,
                    "example": cs.score_example, "experience": cs.score_experience,
                    "total": cs.score_total,
                }
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print_header()
    print_global(stats)
    report_completion(stats)
    print_top(ranked, args.top)
    print()
    print("  单章诊断: python3 tools/expansion_audit.py --chapter chXX_xxx")
    print("  JSON输出: python3 tools/expansion_audit.py --json")
    print()


if __name__ == "__main__":
    main()
