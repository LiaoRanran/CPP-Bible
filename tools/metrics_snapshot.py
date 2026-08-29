#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""metrics_snapshot.py — 项目度量「单一真相源」

背景（2026-08-29 全量审计实测）
==============================
同一事实在本仓库曾有 **5 套互相矛盾的数字**：
  * 章数：147 vs 150 vs 编号上限 165
  * 编译豁免：65 / 66 / 76 三套并存
  * 示例自含率：58% vs 70%（定义不同：按 `#include` / 按 `#include 或 int main`）
  * 进度：AGENT.md「0/45 子项」vs WORKLIST「100%」
  * ASM：叙事称「覆盖 100%」，实测可机校锚定率仅 13.8%

根因是**没有唯一真相源**。本工具把所有度量收敛到 `build/metrics.json`，
所有文档的数字一律从该文件派生。

能力
====
1. 单次遍历 `Book/**/*.md`（排除 `_legacy_`），产出全量度量；
2. `--check` 打印「极致打磨 15 条验收标准」的进度看板，
   让每一次改动都能看到 15 项指标朝目标推进了多少；
3. `--strict` 供 CI 使用：任一指标未达标即非零退出。

设计约束
========
- 零第三方依赖（与 tools/toolchain.py 一致）。
- 只读取 `Book/` 与已有报告，只写 `build/`。
- 输出 JSON 强制 `newline="\\n"`（LF 红线）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOK = ROOT / "Book"
BUILD = ROOT / "build"
DEFAULT_OUT = BUILD / "metrics.json"

# 围栏开/闭：支持 3+ 个反引号（4 反引号围栏若只认 3 会让状态机错位，
# 导致 cpp/asm/mermaid 计数偏小、text 虚高）。
FENCE_RE = re.compile(r"^(`{3,})([A-Za-z0-9_+.-]*)\s*(.*)$")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
CH_NUM_RE = re.compile(r"^ch(\d+)")
TPL_CIRCLED = re.compile(r"[①-⑳]")

# 难度星分布
STAR_RE = re.compile(r"★+")
# 练习标记
EXERCISE_RE = re.compile(r"\[难度")

# 教学脚手架 / 文学性 关键词（用于进度看板）
MARKERS = {
    "one_liner": "一句话结论",
    "analogy": "类比",
    "pitfall": "常见误区",
    "progressive": "循序渐进",
    "people": "人物",
    "anecdote": "[轶]",
    "history": "[史]",
    "commentary": "[评]",
    "prereq": "前置知识",
    "intuition": "直觉",
    "summary": "小结",
}
VERIFY_MARKERS = {
    "verified": "[VERIFIED]",
    "unverified": "[UNVERIFIED]",
    "needs_verify": "[NEEDS-VERIFY]",
}

# 「极致打磨」15 条验收标准（name, 目标, 方向 min/max, 说明）
TARGETS = [
    ("chapter_levels", 147, "min", "章级 L1/L2/L3 分层（当前未实施）"),
    ("one_liner", 147, "min", "一句话结论"),
    ("analogy", 294, "min", "类比（每章 ≥2，须带失效边界）"),
    ("pitfall", 147, "min", "常见误区"),
    ("exercise_zero_chapters", 0, "max", "零练习章节数"),
    ("exercise_median", 5, "min", "每章练习数中位数"),
    ("asm_anchor_rate", 0.60, "min", "ASM 证据可机校锚定率"),
    ("d5_coverage", 147, "min", "D5 性能附录覆盖章数"),
    ("unverified", 120, "max", "[UNVERIFIED] 标记数"),
    ("extra_css_lines", 400, "min", "站点自定义 CSS 行数"),
    ("material_features", 16, "min", "mkdocs-material 启用特性数"),
    ("root_docs", 10, "max", "根目录 .md 文档数"),
    ("changelog_lag", 0, "max", "CHANGELOG 落后提交数"),
    ("glossary_lines", 800, "min", "术语表行数"),
    ("gcc_hardcodes", 0, "max", "工具链路径硬编码处数"),
]


def git(*args: str) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8")
        return r.stdout.strip()
    except Exception:
        return ""


def scan_chapters() -> dict:
    """单次遍历 Book/**/*.md，收集全部内容度量。"""
    md_files = [p for p in BOOK.rglob("*.md") if "_legacy_" not in str(p)]
    ch_files = [p for p in md_files if CH_NUM_RE.match(p.name)]

    total_lines = 0
    fences: dict[str, int] = {}
    cpp_total = cpp_main = cpp_include = 0
    stars: dict[int, int] = {}
    markers = {k: 0 for k in MARKERS}
    verify = {k: 0 for k in VERIFY_MARKERS}
    d5_chapters = 0
    admonitions = 0
    exercise_counts: dict[str, int] = {}
    per_file_headings: dict[str, list[str]] = {}
    chapter_nums: list[int] = []

    for p in md_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        # splitlines() 而非 split("\n")：后者会把每个文件末尾换行多算一行
        lines = text.splitlines()
        total_lines += len(lines)

        # —— 围栏状态机（同时统计 cpp 块自含性）——
        # 开围栏记录反引号长度；闭围栏必须 ≥ 该长度且无语言标记。
        in_fence = False
        open_marker = ""
        lang = ""
        buf: list[str] = []
        for ln in lines:
            m = FENCE_RE.match(ln)
            if m:
                marker, flang = m.group(1), m.group(2)
                if not in_fence:
                    in_fence = True
                    open_marker = marker
                    lang = flang or "text"
                    fences[lang] = fences.get(lang, 0) + 1
                    buf = []
                elif len(marker) >= len(open_marker) and not flang:
                    in_fence = False
                    if lang == "cpp":
                        body = "\n".join(buf)
                        cpp_total += 1
                        if re.search(r"\bint\s+main\s*\(", body):
                            cpp_main += 1
                        if "#include" in body:
                            cpp_include += 1
                    open_marker = ""
                    lang = ""
                continue
            if in_fence:
                buf.append(ln)

        # —— 标题（用于脚手架税）——
        hs = [h.strip() for h in re.findall(r"^(?:#{2,4})\s+(.+?)\s*$",
                                            text, re.M)]
        per_file_headings[p.name] = hs

        # —— 各类标记 ——
        for key, word in MARKERS.items():
            markers[key] += text.count(word)
        for key, word in VERIFY_MARKERS.items():
            verify[key] += text.count(word)

        for m in STAR_RE.finditer(text):
            n = len(m.group(0))
            stars[n] = stars.get(n, 0) + 1

        if re.search(r"^#{2,4}\s*D5\b", text, re.M):
            d5_chapters += 1
        admonitions += len(re.findall(r"^(?:!!!|\?\?\?)\s", text, re.M))

        n_ex = len(EXERCISE_RE.findall(text))
        if CH_NUM_RE.match(p.name):
            exercise_counts[p.name] = n_ex
            chapter_nums.append(int(CH_NUM_RE.match(p.name).group(1)))

    # —— 脚手架税：出现在 ≥50% 章节的标题 = 强制脚手架 ——
    freq: dict[str, int] = {}
    for hs in per_file_headings.values():
        for h in set(hs):
            freq[h] = freq.get(h, 0) + 1
    n_ch = max(1, len(ch_files))
    scaffold = {h for h, c in freq.items() if c >= n_ch * 0.5}
    shares = []
    for p in ch_files:
        hs = per_file_headings.get(p.name, [])
        if hs:
            shares.append(sum(1 for h in hs if h in scaffold) / len(hs))

    ex_vals = list(exercise_counts.values())

    return {
        "files": {"md_total": len(md_files), "chapters": len(ch_files)},
        "lines": total_lines,
        "chapter_numbering": {
            "min": min(chapter_nums) if chapter_nums else 0,
            "max": max(chapter_nums) if chapter_nums else 0,
            "gaps": sorted(set(range(min(chapter_nums), max(chapter_nums) + 1))
                           - set(chapter_nums)) if chapter_nums else [],
        },
        "blocks": dict(sorted(fences.items(), key=lambda x: -x[1])),
        "self_containment": {
            "cpp_total": cpp_total,
            "with_main": cpp_main,
            "with_include": cpp_include,
            "ratio_main": round(cpp_main / cpp_total, 4) if cpp_total else 0,
            "ratio_include": round(cpp_include / cpp_total, 4) if cpp_total else 0,
        },
        "difficulty": {
            "example_stars": sum(stars.values()),
            "distribution": {str(k): v for k, v in sorted(stars.items())},
        },
        "scaffold": {
            "mandatory_sections": len(scaffold),
            "median_heading_share": round(statistics.median(shares), 4) if shares else 0,
        },
        "teaching_markers": markers,
        "verification": verify,
        "d5_coverage": d5_chapters,
        "admonitions": admonitions,
        "exercises": {
            "total": sum(ex_vals),
            "chapters_zero": sum(1 for v in ex_vals if v == 0),
            "median_per_chapter": int(statistics.median(ex_vals)) if ex_vals else 0,
            "max_per_chapter": max(ex_vals) if ex_vals else 0,
        },
    }


def scan_asm() -> dict:
    """从 ASM 证据报告读取分级统计（若报告缺失则回退计数）。"""
    rep = BUILD / "asm_evidence_report.json"
    if rep.is_file():
        try:
            data = json.loads(rep.read_text(encoding="utf-8"))
            recs = data.get("records", data) if isinstance(data, dict) else data
            if isinstance(recs, list):
                c: dict[str, int] = {}
                for r in recs:
                    st = r.get("status", "?")
                    c[st] = c.get(st, 0) + 1
                total = sum(c.values())
                acc = c.get("ACCURATE", 0)
                return {
                    "total": total,
                    "accurate": acc,
                    "drift": c.get("DRIFT", 0),
                    "empty": c.get("EMPTY", 0),
                    "missing_file": c.get("MISSING_FILE", 0),
                    "unanchored": c.get("UNANCHORED", 0),
                    "anchor_rate": round(acc / total, 4) if total else 0,
                    "source": str(rep),
                }
        except Exception:
            pass
    return {"total": None, "source": "build/asm_evidence_report.json (缺失)"}


def scan_env() -> dict:
    """环境与工程卫生度量（不扫描正文，开销极低）。"""
    try:
        sys.path.insert(0, str(HERE))
        from toolchain import report as tc_report  # type: ignore
        tc = tc_report()
    except Exception as e:  # 配置损坏也不应拖垮度量
        tc = {"error": str(e)}

    # 工具链硬编码残留（排除配置源 toolchain.py；
    # 也排除本文件——它自身含有该字面量用于探测，否则会自匹配）
    hardcodes = 0
    for p in HERE.glob("*.py"):
        if p.name in ("toolchain.py", "metrics_snapshot.py"):
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
            hardcodes += len(re.findall(r"C:/Qt/Tools", t))
        except Exception:
            pass

    root_docs = len(list(ROOT.glob("*.md")))
    css = ROOT / "docs" / "assets" / "extra.css"
    if not css.is_file():
        css = BUILD / "site" / "docs" / "assets" / "extra.css"
    css_lines = 0
    if css.is_file():
        css_lines = len(css.read_text(encoding="utf-8",
                                      errors="replace").splitlines())

    glossary = ROOT / "Book" / "GLOSSARY.md"
    glossary_lines = 0
    if glossary.is_file():
        glossary_lines = len(glossary.read_text(
            encoding="utf-8", errors="replace").splitlines())

    # material features
    mk = BUILD / "site" / "mkdocs.yml"
    feats = 0
    if mk.is_file():
        txt = mk.read_text(encoding="utf-8", errors="replace")
        blk = re.search(r"features:\s*\n((?:\s+- .*\n)+)", txt)
        if blk:
            feats = len(re.findall(r"^\s+-\s+\S", blk.group(1), re.M))

    # CHANGELOG 落后提交数
    lag = None
    cl = ROOT / "CHANGELOG.md"
    if cl.is_file():
        m = re.search(r"^##\s*\[[^\]]+\]\s*-\s*(\d{4}-\d{2}-\d{2})",
                      cl.read_text(encoding="utf-8", errors="replace"), re.M)
        if m:
            out = git("log", "--oneline", f"--since={m.group(1)}")
            lag = len([x for x in out.split("\n") if x.strip()])

    return {
        "toolchain": tc,
        "gcc_hardcodes": hardcodes,
        "root_docs": root_docs,
        "extra_css_lines": css_lines,
        "material_features": feats,
        "glossary_lines": glossary_lines,
        "changelog_lag": lag,
    }


def scan_chapter_levels() -> dict:
    """章级 L1/L2/L3 分层覆盖率（P2/T1）。

    检测每章头部 meta 行中的 `层级：L1/L2/L3`（与示例级 [难度] 星分离）。
    为避免与正文里的「缓存层级：L1/L2/L3」「内存层级：L1/L2/L3」混淆，要求
    `层级：Lx` 必须出现在含 `标准基：`/`预计阅读：` 的同一 meta 行上。
    纯文本块注，三模式天然安全；metrics 借此使 chapter_levels 成为可量化进度。
    """
    pat = re.compile(r'层级\s*[:：]\s*L([123])')
    meta_anchor = re.compile(r'标准基\s*[:：]|预计阅读\s*[:：]')
    files = [p for p in BOOK.rglob("*.md") if "_legacy_" not in str(p)]
    counts = {"L1": 0, "L2": 0, "L3": 0}
    total = 0
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for line in t.splitlines():
            if meta_anchor.search(line) and pat.search(line):
                total += 1
                counts["L" + pat.search(line).group(1)] += 1
                break
    return {"total": total, "L1": counts["L1"], "L2": counts["L2"], "L3": counts["L3"]}


def build() -> dict:
    chapters = scan_chapters()
    asm = scan_asm()
    env = scan_env()

    return {
        "schema": "cppbible-metrics/1.0",
        "commit": git("rev-parse", "--short", "HEAD"),
        "chapter_levels": scan_chapter_levels()["total"],  # 章级 L1/L2/L3 分层覆盖章数（P2/T1）
        "content": chapters,
        "asm": asm,
        "env": env,
        "one_liner": chapters["teaching_markers"]["one_liner"],
        "analogy": chapters["teaching_markers"]["analogy"],
        "pitfall": chapters["teaching_markers"]["pitfall"],
    }


def _get(m: dict, dotted: str):
    """按 dotted path 取值，缺失返回 None。"""
    cur = m
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


# 指标在 metrics.json 中的取值路径
PATHS = {
    "chapter_levels": "chapter_levels",
    "one_liner": "one_liner",
    "analogy": "analogy",
    "pitfall": "pitfall",
    "exercise_zero_chapters": "content.exercises.chapters_zero",
    "exercise_median": "content.exercises.median_per_chapter",
    "asm_anchor_rate": "asm.anchor_rate",
    "d5_coverage": "content.d5_coverage",
    "unverified": "content.verification.unverified",
    "extra_css_lines": "env.extra_css_lines",
    "material_features": "env.material_features",
    "root_docs": "env.root_docs",
    "changelog_lag": "env.changelog_lag",
    "glossary_lines": "env.glossary_lines",
    "gcc_hardcodes": "env.gcc_hardcodes",
}


def render_check(m: dict, strict: bool) -> int:
    print("\n极致打磨 · 15 条验收标准进度看板")
    print("=" * 74)
    print(f"{'指标':<26}{'现状':>10}{'目标':>10}   {'状态':<6} 说明")
    print("-" * 74)
    unmet = 0
    for name, target, direction, desc in TARGETS:
        cur = _get(m, PATHS.get(name, name))
        if cur is None:
            print(f"{name:<26}{'—':>10}{target:>10}   {'N/A':<6} {desc}")
            continue
        if direction == "min":
            ok = cur >= target
            pct = min(1.0, cur / target) if target else 1.0
        else:
            ok = cur <= target
            pct = min(1.0, target / cur) if cur else 1.0
        if not ok:
            unmet += 1
        shown = f"{cur:.3f}" if isinstance(cur, float) else str(cur)
        bar_n = int(pct * 10)
        bar = "█" * bar_n + "░" * (10 - bar_n)
        print(f"{name:<26}{shown:>10}{target:>10}   {bar}  {desc}")
    print("-" * 74)
    met = len(TARGETS) - unmet
    print(f"达标 {met}/{len(TARGETS)}" + ("" if not unmet else f"，未达标 {unmet} 项"))
    print("=" * 74)
    if strict and unmet:
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="项目度量单一真相源")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help=f"输出路径（默认 {DEFAULT_OUT}）")
    ap.add_argument("--check", action="store_true",
                    help="打印 15 条验收标准进度看板")
    ap.add_argument("--strict", action="store_true",
                    help="配合 --check：有未达标项则非零退出（CI 用）")
    ap.add_argument("--quiet", action="store_true", help="不打印摘要")
    args = ap.parse_args()

    m = build()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    # LF 红线：Windows 下必须显式 newline
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")

    if not args.quiet:
        c = m["content"]
        print(f"[metrics] commit={m['commit']}  -> {out}")
        print(f"  章节 {c['files']['chapters']} 章 / {c['files']['md_total']} 文件 / "
              f"{c['lines']:,} 行")
        b = c["blocks"]
        top = ", ".join(f"{k}={v}" for k, v in list(b.items())[:5])
        print(f"  代码块 {top}")
        sc = c["self_containment"]
        print(f"  自含率 main={sc['ratio_main']:.1%} include={sc['ratio_include']:.1%} "
              f"(cpp={sc['cpp_total']})")
        a = m["asm"]
        if a.get("total"):
            print(f"  ASM 锚定 {a['accurate']}/{a['total']} = {a['anchor_rate']:.1%} "
                  f"(unanchored={a['unanchored']})")
        print(f"  D5 {c['d5_coverage']}/{c['files']['chapters']} · "
              f"练习零章 {c['exercises']['chapters_zero']} · "
              f"脚手架税 {c['scaffold']['median_heading_share']:.1%}")

    if args.check:
        return render_check(m, args.strict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
