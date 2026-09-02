#!/usr/bin/env python3
"""tools/data_sanity_audit.py — 数据健全性审计（报告型，离线跑）。

把 L2 深耕三轮沉淀的三类真实错误模式固化为可复用的全书扫描能力，
防止同类错误再被批量生成流程灌进书稿：

  1. HEX_QUANTITY (ERROR) —— 量级描述误用十六进制。
     例：`≈ 0x0100 KB`、`0x0008 种组合`、`0x0040 字符`
     （正确写法：256 KB / 8 种 / 64 字符）。
     十六进制只该出现在地址 / 偏移 / 位掩码 / mangled 符号等真·机器语境。
     历史事故：2026-09-02 全书扫描发现 8 章 10 处（ch72/ch61/ch50/ch16/
     ch152/ch13/ch132/ch134）性能量级被写成十六进制，已修复并复扫清零。

  2. PERF_CONFLICT (WARN) —— 同章内同一算法的性能数字数量级冲突。
     例：ch96 同章既写 `sort ≈ 22ms` 又写 `~87ms`，真机实测 88.3ms，
     说明 22ms 是坏数据（同章自相矛盾是最容易被批量生成漏掉的信号）。
     需人工复核：不同负载 / 数据规模本就可能差数倍，工具只负责提示。

  3. UNANCHORED_EVIDENCE (WARN) —— 声称「实测 / 真机」却无 Examples 锚定的 asm 块，
     即「推断示意伪装成真机证据」，违反 TEACHING「亲手跑过」红线。
     历史事故：ch22 ⑨ 汇编节原为「[实现-推断] 示意」，后由真机 objdump 替换并锚定。

可靠性：
  * 跳过 ``` / ~~~ 代码围栏内的内容（汇编 / 代码里的 0x 是合法写法）。
  * 真·十六进制语境自动豁免：≥8 位长串、0x7f… 栈地址、全 f 掩码，
    以及「偏移 / offset / 地址 / 位掩码 / 掩码 / mangled」上下文。
  * PERF_CONFLICT 仅在「同一关键词 + 同一单位」下比较且阈值 3×，仍可能误报，
    故定位为 WARN 而非阻断。

用法:
    python tools/data_sanity_audit.py [path] [--json|--porcelain] [--fail-on ERROR|WARN|never]
默认扫描 Book/。定位为报告型工具（与 disclaimer_audit / title_style_lint 同层），
定期跑、看报告、人工处置；确需门禁时可用 `--fail-on ERROR`（HEX_QUANTITY 零误报）。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

SEVERITY: dict[str, str] = {
    "HEX_QUANTITY": "ERROR",
    "PERF_CONFLICT": "WARN",
    "UNANCHORED_EVIDENCE": "WARN",
}

FENCE_RE = re.compile(r"^\s*(```|~~~)")

# ① 量级描述误用十六进制：0x 后紧跟中文量词 / 时间·容量单位
HEX_QUANTITY_RE = re.compile(
    r"(?:≈\s*)?0x[0-9A-Fa-f]{1,4}\s*[`\s]*"
    r"(?:字节行|字节|种|次|字符|路|对象|倍|个|行|位|项|ms|us|µs|ns|KB|MB|GB|GFLOP|FLOP)"
)
# 真·十六进制语境，命中则豁免：
#   * HEX_LEGIT_RE  —— 长地址(0x7f…)、≥8 位长串、全 f 掩码
#   * ABI_CTX_RE    —— ABI / 底层语境（偏移、对齐、标签、哨兵值、vptr、槽位、MSR…），
#                      这些地方十六进制是惯例写法，改成十进制反而不专业
#   * OFFSET_ARITH  —— `0x8 * i` 这类地址算术
HEX_LEGIT_RE = re.compile(r"0x(?:7[fF][0-9A-Fa-f]{6,}|[0-9A-Fa-f]{8,}|[fF]{4,})")
ABI_CTX_RE = re.compile(
    r"(?:偏移|offset|对齐|align|标签|哨兵|vptr|槽|slot|标志|MSR|地址|位掩码|掩码"
    r"|mangled|符号名|指针|首)",
    re.I,
)
OFFSET_ARITH_RE = re.compile(r"0x[0-9A-Fa-f]+\s*\*")
OFFSET_CTX_RE = re.compile(r"(?:偏移|offset|地址|位掩码|掩码|mangled|符号名)\s*[：:]?\s*0x", re.I)

# ② 性能数字 + 算法关键词（长词在前，保证 std::stable_sort 优先于 sort）
PERF_NUM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(ms|us|µs|ns)\b")
ALGO_KEYWORDS: tuple[str, ...] = (
    "std::stable_sort",
    "std::sort",
    "stable_sort",
    "sort_heap",
    "push_back",
    "std::atomic",
    "atomic",
    "malloc",
    "mutex",
    "vector",
    "sort",
)

# ③ 实测声称与 asm 锚定
CLAIM_RE = re.compile(r"(?:本机实测|真机|实测输出|本机运行结果|实测)")


def _join(lines: list[str], start: int, end: int) -> str:
    return "\n".join(lines[max(0, start):end])


def scan_lines(lines: list[str]) -> list[tuple[int, str, str]]:
    """扫描单个文件的行序列，返回 [(行号(1-based), 类别, 说明)]。"""
    issues: list[tuple[int, str, str]] = []
    perf: dict[tuple[str, str], list[tuple[float, int]]] = {}

    in_fence = False
    fence_lang = ""
    fence_start = 0
    fence_buf: list[str] = []

    for i, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            if not in_fence:
                in_fence = True
                fence_lang = ln.strip().lstrip("`~").strip().lower()
                fence_start = i
                fence_buf = []
            else:
                in_fence = False
                if fence_lang.startswith("asm"):
                    body = "\n".join(fence_buf)
                    anchored = "节选自" in body
                    marked = re.search(r";\s*(示意|推断)", body) is not None
                    if not anchored and not marked:
                        before = _join(lines, fence_start - 8, fence_start)
                        if CLAIM_RE.search(before):
                            issues.append((
                                fence_start + 1,
                                "UNANCHORED_EVIDENCE",
                                "声称「实测/真机」的 asm 块既无 Examples 锚定、"
                                "也无「示意/推断」标注——疑似推断示意伪装成真机证据",
                            ))
                fence_buf = []
            continue

        if in_fence:
            fence_buf.append(ln)
            continue

        # ① HEX_QUANTITY
        for m in HEX_QUANTITY_RE.finditer(ln):
            tok = m.group(0)
            if HEX_LEGIT_RE.search(tok):
                continue
            # 扩大上下文窗口，命中 ABI / 底层语境（偏移、对齐、vptr、槽位…）即豁免
            ctx = ln[max(0, m.start() - 30): m.end() + 12]
            if ABI_CTX_RE.search(ctx) or OFFSET_CTX_RE.search(ctx):
                continue
            if OFFSET_ARITH_RE.search(ctx):
                continue
            issues.append((i + 1, "HEX_QUANTITY", f"量级描述误用十六进制：{tok.strip()}"))

        # ② 采集性能数字（按该行命中的第一个关键词归类）
        nums = PERF_NUM_RE.findall(ln)
        if nums:
            for kw in ALGO_KEYWORDS:
                if kw in ln:
                    for val, unit in nums:
                        perf.setdefault((kw, unit), []).append((float(val), i + 1))
                    break

    # ② PERF_CONFLICT：同关键词 + 同单位下，极值比 ≥3× 即提示复核
    for (kw, unit), items in perf.items():
        if len(items) < 2:
            continue
        vals = sorted(v for v, _ in items)
        lo, hi = vals[0], vals[-1]
        if lo <= 0 or hi / lo < 3.0:
            continue
        lo_ln = min(ln for v, ln in items if v == lo)
        hi_ln = min(ln for v, ln in items if v == hi)
        issues.append((
            lo_ln,
            "PERF_CONFLICT",
            f"同章「{kw}」性能数字差 {hi / lo:.1f}×（{lo:g}{unit} @L{lo_ln} vs "
            f"{hi:g}{unit} @L{hi_ln}）——请核哪一个是真机值"
            "（不同负载本就可能差数倍，需人工判定）",
        ))

    issues.sort(key=lambda t: (t[0], t[1]))
    return issues


def _iter_md(root: str) -> list[str]:
    if os.path.isdir(root):
        out: list[str] = []
        for r, _dirs, fs in os.walk(root):
            for fn in fs:
                if fn.endswith(".md"):
                    out.append(os.path.join(r, fn))
        return sorted(out)
    return [root]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="数据健全性审计：十六进制污染 / 性能数字冲突 / 未锚定证据",
    )
    ap.add_argument("path", nargs="?", default="Book", help="扫描根（默认 Book/）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--porcelain", action="store_true", help="机器可读：file:line:kind:msg")
    ap.add_argument(
        "--fail-on",
        choices=("ERROR", "WARN", "never"),
        default="never",
        help="ERROR=存在 ERROR 即 exit 1；WARN=存在任意问题即 exit 1；never=始终 0（默认）",
    )
    args = ap.parse_args()

    files = _iter_md(args.path)
    rows: list[dict[str, object]] = []
    for fp in files:
        with open(fp, "r", encoding="utf-8", newline="") as f:
            lines = f.read().split("\n")
        for ln, kind, msg in scan_lines(lines):
            rows.append({
                "file": fp,
                "line": ln,
                "kind": kind,
                "severity": SEVERITY[kind],
                "msg": msg,
            })

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif args.porcelain:
        for it in rows:
            print(f"{it['file']}:{it['line']}:{it['kind']}:{it['msg']}")
    else:
        cur = ""
        for it in rows:
            fp = str(it["file"])
            if fp != cur:
                cur = fp
                n = sum(1 for x in rows if str(x["file"]) == cur)
                print(f"== {cur} ({n}) ==")
            print(f"   L{it['line']}: [{it['severity']}] {it['kind']} — {it['msg']}")
        n_err = sum(1 for x in rows if x["severity"] == "ERROR")
        n_warn = sum(1 for x in rows if x["severity"] == "WARN")
        print(
            f"\n合计 {len(rows)} 处（ERROR {n_err} / WARN {n_warn}），"
            f"扫描 {len(files)} 文件；HEX_QUANTITY 零误报可用 --fail-on ERROR 接门禁"
        )

    if args.fail_on == "ERROR" and any(x["severity"] == "ERROR" for x in rows):
        return 1
    if args.fail_on == "WARN" and rows:
        return 1
    return 0


if __name__ == "__main__":
    # 仅对真实 TextIOWrapper 重配编码（本机 GBK 终端直接 print 中文会抛 UnicodeEncodeError）
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
