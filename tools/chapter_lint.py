#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chapter_lint.py — 单章级质量门禁（行号级缺陷反馈）

为什么需要这个轮子
==================
现有审计工具（density_audit / expansion_audit / deduplication_audit /
crossref_audit）都是**全局聚合**，给的是"整库平均分"。Hy3 每天扩写的是
**单章**，改完一章后需要立刻知道：

  - 这一章有没有空洞代码块（注水）？
  - 标题层级有没有跳级（# 直接到 ####）？
  - 长代码块是不是零注释（教学手册应逐行讲）？
  - 这一章有没有连到其他章（知识图谱完整性）？
  - 章内有没有重复段落（v4 去水词）？
  - 有没有遗留 TBD/TODO/FIXME/XXX 标记？
  （注：未验证占位符 ~N/≈N 不进自动门禁——本手册 N 多为泛型变量/模板参数/
   复杂度符号，正则误报率极高，交由人工 + expansion_audit 处理。）

本工具提供**单章级、行号级**的即时反馈，每条缺陷带 (行号, 规则, 严重度,
说明)，直接可定位修复。它不替代全局审计，而是把全局标准下沉到"每次改完
一章就能跑"的粒度。

设计约束（对齐 AGENT.md 红线）
==============================
- 只读 Book/，绝不修改源文件。
- 结果只写 build/chapter_lint.json，不污染源码树。
- 纯正则解析，不编译，秒级完成，可放进 pre_push_check 的快路径。
- 不新增章节、不注水、不引入幻觉。

评分模型
========
每章起点 100 分，按缺陷严重度扣分：
  HIGH = 15  (空洞代码块、未验证占位符)
  MED  = 7   (标题跳级、章内重复、零交引)
  LOW  = 3   (长代码块零注释、TODO/XXX 标记)
得分下限 0。等级：A≥90 B≥80 C≥70 D≥60 F<60。

用法
====
  python tools/chapter_lint.py                      # 全库扫描 + 摘要
  python tools/chapter_lint.py --top 20             # 按缺陷数排前 20 章
  python tools/chapter_lint.py --chapter Book/part03_language/ch19_variables.md
  python tools/chapter_lint.py --json out.json      # 指定 JSON 输出路径
  python tools/chapter_lint.py --fail-under 80      # 有章低于 80 则 exit 1
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

# ---- 复用 chapter_compile_check 的围栏判定，保证与断言/编译工具一致 ----
try:
    sys.path.insert(0, str(HERE))
    from chapter_compile_check import CPP_FENCE, FENCE_END  # noqa: E402
except Exception:  # 兜底，防止工具被单独移动后 import 失败
    CPP_FENCE = re.compile(r"^```cpp\s*$")
    FENCE_END = re.compile(r"^```\s*$")

# ---- 缺陷规则定义 ----
SEV_WEIGHT = {"HIGH": 15, "MED": 7, "LOW": 2}
GRADE_BAND = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]

# 显式待办标记（在正文/注释里遗留的未完成记号）
TODO_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b")
# 交叉引用：本项目用 `⟶ Book/partNN/chNN.md` 箭头 + markdown 链接两种
XREF_ARROW_RE = re.compile(r"⟶\s*Book/")
XREF_LINK_RE = re.compile(r"\]\((?:Book/|part\d{2}/|.*?\.md)\)")
COMMENT_RE = re.compile(r"^\s*//|^\s*/\*|^\s*\*")


# ---------------------------------------------------------------------------
# 解析：把一章拆成 (行号, 类型, 内容) 流，便于规则判断
# ---------------------------------------------------------------------------
def parse_chapter(text: str):
    """返回结构：
      lines: list[str]                      原始行
      fences: list[(start, end, body)]      cpp 围栏块（含行号，1-based）
      headings: list[(lineno, level)]       标题
      paras: list[(start, end, text)]       连续非空正文段（排除围栏/标题/列表）
    """
    lines = text.splitlines()
    n = len(lines)
    fences = []
    headings = []
    paras = []
    i = 0
    cur_para = []
    cur_start = None
    in_fence = False

    def flush_para():
        nonlocal cur_para, cur_start
        if cur_para:
            body = "\n".join(cur_para).strip()
            if body and len(body) > 20:
                paras.append((cur_start, i, body))
        cur_para = []
        cur_start = None

    while i < n:
        ln = lines[i]
        hm = re.match(r"^(#+)\s", ln)
        if hm:
            flush_para()
            headings.append((i + 1, len(hm.group(1))))
            i += 1
            continue
        if CPP_FENCE.match(ln):
            flush_para()
            j = i + 1
            buf = []
            while j < n and not FENCE_END.match(lines[j]):
                buf.append(lines[j])
                j += 1
            fences.append((i + 1, j + 1, "\n".join(buf)))
            i = j + 1
            in_fence = False
            continue
        if ln.strip() == "":
            flush_para()
        else:
            if cur_start is None:
                cur_start = i + 1
            cur_para.append(ln)
        i += 1
    flush_para()
    return lines, fences, headings, paras


# ---------------------------------------------------------------------------
# 单章规则
# ---------------------------------------------------------------------------
def lint_chapter(path: Path):
    text = path.read_text(encoding="utf-8")
    lines, fences, headings, paras = parse_chapter(text)
    defects = []  # (lineno, rule, sev, msg)

    # R1 空洞 cpp 块（真正为空：无任何非空行）
    # 注释-only 块是章节分隔注解，合法；单行合法示例（1 行有效代码）也合法。
    # 仅标记完全无内容的 ```cpp ```，避免把正常短示例误判为注水。
    for (s, e, body) in fences:
        non_blank = [l for l in body.splitlines() if l.strip()]
        if not non_blank:
            defects.append((s, "EMPTY_CODE", "HIGH",
                            "cpp 块完全为空（无任何内容，应删除或补示例）"))

    # R2 遗留待办标记（在正文/注释里遗留的未完成记号）
    # 注：未验证占位符（~N/≈N）不进入自动门禁——本手册大量把 N 用作泛型变量、
    # 模板参数、复杂度符号（如 ~N() 析构、~ N/2 复杂度、bitset<N>），正则无法区分
    # "未知占位"与"已知变量"，误报率极高。该维度交由人工 + expansion_audit 处理。
    for idx, ln in enumerate(lines, 1):
        if TODO_RE.search(ln):
            defects.append((idx, "TODO_MARK", "LOW",
                            f"遗留待办标记：{ln.strip()[:60]}"))

    # R3 标题层级跳级（level 增量 > 1）
    prev_level = 0
    for (lnno, level) in headings:
        if prev_level and level > prev_level + 1:
            defects.append((lnno, "HEADING_JUMP", "MED",
                            f"标题层级从 H{prev_level} 跳到 H{level}（缺中间层）"))
        prev_level = level

    # R4 长代码块零注释（≥12 行有效代码却无一行注释，教学手册建议逐行讲）
    for (s, e, body) in fences:
        cl = body.splitlines()
        code_n = sum(1 for l in cl if l.strip() and not l.strip().startswith("//"))
        cmt_n = sum(1 for l in cl if COMMENT_RE.match(l))
        if code_n >= 12 and cmt_n == 0:
            defects.append((s, "UNCOMMENTED_CODE", "LOW",
                            f"长代码块 {code_n} 行有效代码却 0 注释（教学手册建议逐行讲）"))

    # R5 缺交引（章内无任何跨章引用）
    xref_n = sum(1 for ln in lines if XREF_ARROW_RE.search(ln) or XREF_LINK_RE.search(ln))
    if xref_n == 0:
        defects.append((1, "NO_XREF", "MED",
                        "本章 0 条跨章引用（知识图谱完整性不足）"))

    # R6 章内重复段落（连续两段完全相同）
    for k in range(1, len(paras)):
        if paras[k][2] == paras[k - 1][2]:
            defects.append((paras[k][0], "DUP_PARA", "MED",
                            f"与第 {paras[k-1][0]} 行段落完全重复（v4 去水词）"))

    # ---- 计分 ----
    score = 100
    for (_, _, sev, _) in defects:
        score -= SEV_WEIGHT[sev]
    score = max(0, score)
    grade = next(g for thr, g in GRADE_BAND if score >= thr)
    sev_count = {s: sum(1 for d in defects if d[2] == s) for s in SEV_WEIGHT}
    return {
        "chapter": str(path.relative_to(ROOT)).replace("\\", "/"),
        "score": score,
        "grade": grade,
        "defects_total": len(defects),
        "sev": sev_count,
        "xref": xref_n,
        "defects": [{"line": d[0], "rule": d[1], "sev": d[2], "msg": d[3]}
                    for d in sorted(defects, key=lambda x: x[0])],
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def iter_chapters():
    return sorted(ROOT.glob("Book/**/*.md"), key=lambda p: str(p))


def main():
    ap = argparse.ArgumentParser(description="单章级质量门禁")
    ap.add_argument("--chapter", help="只检查单个章文件")
    ap.add_argument("--top", type=int, default=0, help="按缺陷数输出前 N 章")
    ap.add_argument("--json", default=str(BUILD / "chapter_lint.json"),
                    help="JSON 输出路径")
    ap.add_argument("--fail-under", type=int, default=0,
                    help="有章得分低于该值则 exit 1")
    ap.add_argument("--fail-on", choices=["HIGH", "MED", "LOW"], default=None,
                    help="存在该级别及以上缺陷则 exit 1（用于 pre_push 硬门禁）")
    args = ap.parse_args()

    if args.chapter:
        res = lint_chapter(Path(args.chapter).resolve())
        print(f"章节: {res['chapter']}  评分: {res['score']} ({res['grade']})  "
              f"缺陷: {res['defects_total']}  [H{res['sev']['HIGH']} "
              f"M{res['sev']['MED']} L{res['sev']['LOW']}]")
        print("-" * 70)
        if not res["defects"]:
            print("  ✅ 无缺陷")
        for d in res["defects"]:
            print(f"  L{d['line']:<5} [{d['sev']:<4}] {d['rule']:<16} {d['msg']}")
        return 0

    results = [lint_chapter(p) for p in iter_chapters()]
    results.sort(key=lambda r: r["score"])

    gpa = sum(r["score"] for r in results) / max(1, len(results))
    grade_dist = {}
    for r in results:
        grade_dist[r["grade"]] = grade_dist.get(r["grade"], 0) + 1

    print(f"扫描章节: {len(results)}  项目 GPA: {gpa:.1f}")
    print("等级分布:", "  ".join(f"{g}={grade_dist.get(g,0)}"
                                for g in ["A", "B", "C", "D", "F"]))
    print("-" * 78)
    print(f"{'章节':<52}{'分':>4} {'级':>2} {'缺':>3} {'H':>2}{'M':>2}{'L':>2}")
    print("-" * 78)
    shown = results if not args.top else results[:args.top]
    for r in shown:
        print(f"{r['chapter']:<52}{r['score']:>4} {r['grade']:>2} "
              f"{r['defects_total']:>3} "
              f"{r['sev']['HIGH']:>2}{r['sev']['MED']:>2}{r['sev']['LOW']:>2}")

    out = {"gpa": round(gpa, 1), "grade_dist": grade_dist,
           "chapters": results}
    Path(args.json).write_text(json.dumps(out, ensure_ascii=False, indent=2),
                              encoding="utf-8")
    print(f"\n明细已写: {args.json}")

    if args.fail_under and any(r["score"] < args.fail_under for r in results):
        print(f"⚠️ 存在得分 < {args.fail_under} 的章节")
        return 1
    if args.fail_on:
        thr = SEV_WEIGHT[args.fail_on]
        bad = [(r["chapter"], d["rule"], d["sev"], d["line"])
               for r in results for d in r["defects"]
               if SEV_WEIGHT[d["sev"]] >= thr]
        if bad:
            print(f"⚠️ {len(bad)} 处 ≥{args.fail_on} 缺陷，门禁失败（前 5）:")
            for b in bad[:5]:
                print(f"   {b[0]} L{b[3]} {b[1]} ({b[2]})")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
