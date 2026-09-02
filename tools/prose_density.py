"""prose_density —— 叙述密度测量：每章「纯段落行」占比。

锐评诊断「全书叙述密度仅 32%、147 章平均真正在讲东西的不到 530 行」，
但该数字从未固化为工具——深耕专项（30 章真深耕）需要可测的验收基线。

口径：
- 总行   ：非空、非 fence 边界的正文行
- 剔除   ：代码/asm/mermaid/svg 等 fence 内行、表格行、标题行、
           HTML 标签行、目录/链接导航行（纯链接列表）、列表项行
- 段落行 ：以上剔除后剩下的普通叙述行（含完整句子的散文）
- 列表行单列：列表项常含完整句子，算「半叙述」，供人工判断参考

定位：报告型工具（不进门禁）——深耕是质量工程，密度是参考信号而非红线；
单章密度高≠写得好，密度过低（<20%）≈ 几乎全是代码/表格堆砌，是深耕候选。

用法：
  python tools/prose_density.py               # 全书基线 + 最贫血 TOP N
  python tools/prose_density.py --top 30      # 输出 30 章深耕候选名单
  python tools/prose_density.py Book/part07_stl/ch77_vector.md   # 单章
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^#{1,6}\s")
TABLE_RE = re.compile(r"^\s*\|")
LIST_RE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s)")
HTML_TAG_RE = re.compile(r"^\s*<[^>]+>\s*$")
# 纯导航链接行：整行只有 markdown 链接/加粗链接，没有实质句子
LINK_ONLY_RE = re.compile(r"^\s*(?:\*\*)?\[.+?\]\(.+?\)(?:\*\*)?\s*$")


def scan_file(path: str) -> dict[str, float]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")

    total = prose = list_lines = 0
    in_fence = False
    for ln in lines:
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence or not ln.strip():
            continue
        if HEADING_RE.match(ln) or TABLE_RE.match(ln) or HTML_TAG_RE.match(ln):
            continue
        if LINK_ONLY_RE.match(ln):
            continue
        total += 1
        if LIST_RE.match(ln):
            list_lines += 1
        else:
            prose += 1
    return {
        "total": total,
        "prose": prose,
        "list": list_lines,
        "density": prose / total if total else 0.0,
    }


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
    ap = argparse.ArgumentParser(description="叙述密度测量（报告型，不阻断）")
    ap.add_argument("path", nargs="?", default="Book", help="扫描根（默认 Book/）")
    ap.add_argument("--top", type=int, default=20, help="最贫血章排名条数")
    args = ap.parse_args()

    rows = []
    for fp in _iter_md(args.path):
        s = scan_file(fp)
        if s["total"] >= 50:  # 过滤极短的非正文章
            rows.append((fp, s))

    grand_total = sum(s["total"] for _, s in rows)
    grand_prose = sum(s["prose"] for _, s in rows)
    print(f"全书叙述密度：{grand_prose}/{grand_total} = {grand_prose / grand_total:.1%}"
          f"（{len(rows)} 章，含列表半叙述口径见下）\n")

    rows.sort(key=lambda t: t[1]["density"])
    print(f"最贫血 TOP {args.top}（深耕候选，密度=纯段落行/正文行）：")
    for fp, s in rows[: args.top]:
        name = os.path.relpath(fp, ".")
        print(f"  {s['density']:6.1%}  段落 {s['prose']:5d} / 正文 {s['total']:5d}"
              f"（列表 {s['list']:4d}）  {name}")

    if len(rows) > args.top:
        top = rows[: args.top]
        tp = sum(s["prose"] for _, s in top)
        tt = sum(s["total"] for _, s in top)
        print(f"\nTOP {args.top} 合计密度 {tp / tt:.1%}；深耕后单章目标 ≥50%")
    return 0


if __name__ == "__main__":
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
