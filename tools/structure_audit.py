#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
structure_audit.py — 围栏感知的 Markdown 结构缺陷扫描器（只读，默认不修）

检测两类现有门禁未覆盖的机械缺陷：
  S1 标题大纲缺陷：
      - S1A stray H1：文档首个标题之外又出现 `# ` 一级标题（应为 ##）
      - S1B level jump：标题层级越过一级（如 H3 直接跳 H5）
  S5 参差表格：GFM 表格的数据行单元格数 ≠ 表头列数（围栏感知，排除代码块内 |）

用法：
  python3 tools/structure_audit.py [--root Book] [--dir Book/partXX] [--json out.json]
默认扫描 Book/ 下所有 ch*.md。
"""
import os, re, json, argparse

H_RE = re.compile(r'^(#{1,6})\s+(.*\S)\s*$')
SEP_RE = re.compile(r'^\[([^\]]+)\]:\s*\S+')
LINK_ANCHOR_RE = re.compile(r'\]\(#([a-zA-Z0-9_\-]+)\)')

def collect_files(root):
    files = []
    for dp, _, fnames in os.walk(root):
        for fn in fnames:
            if fn.startswith("ch") and fn.endswith(".md"):
                files.append(os.path.join(dp, fn))
    return sorted(files)

def split_row(row):
    """按未转义的顶层 | 切分表格行；忽略反引号行内代码与转义 \\|。
    反引号内的 |（如 `enum|E`）与 \\| 转义竖线不计为列分隔符。"""
    # 先剥离反引号代码段（成对 `...`），其内部 | 全部视为字面
    # 用占位符替换，避免误切
    cleaned = []
    in_backtick = False
    i = 0
    while i < len(row):
        ch = row[i]
        if ch == '`':
            in_backtick = not in_backtick
            cleaned.append(ch)
        elif ch == '|' and not in_backtick:
            # 检查前一字符是否为转义 \
            if i > 0 and row[i-1] == '\\':
                cleaned.append(ch)
            else:
                cleaned.append('\x00')  # 列分隔占位
        else:
            cleaned.append(ch)
        i += 1
    s = "".join(cleaned)
    return [c.strip() for c in s.split('\x00')]

def is_gfm_sep(cells):
    if not cells:
        return False
    return all(set(c) <= set("-: ") for c in cells) and any("-" in c for c in cells)

def audit_file(fp):
    hits = []
    lines = open(fp, encoding="utf-8", errors="replace").read().split("\n")
    in_fence = False
    headings = []          # (lineno, level, text)
    prev_level = 0
    first_h_seen = False
    h1_count = 0
    for i, l in enumerate(lines, 1):
        if l.strip().startswith("```") or l.strip().startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = H_RE.match(l)
        if m:
            lvl = len(m.group(1))
            txt = m.group(2).strip()
            h1_count += 1
            if lvl == 1 and (first_h_seen or h1_count > 1):
                hits.append((i, "S1A-stray-H1", txt[:50]))
            first_h_seen = True
            if prev_level and lvl > prev_level + 1:
                hits.append((i, "S1B-level-jump", f"H{lvl} after H{prev_level}: {txt[:30]}"))
            prev_level = lvl
            headings.append((i, lvl, txt))
    # S5 tables, fence-aware block scan
    n = len(lines)
    j = 0
    while j < n:
        l = lines[j]
        if l.strip().startswith("```") or l.strip().startswith("~~~"):
            in_fence = not in_fence
            j += 1
            continue
        if in_fence:
            j += 1
            continue
        s = l.rstrip()
        if s.startswith("|") and s.endswith("|"):
            block = []
            k = j
            while k < n and lines[k].strip().startswith("|") and lines[k].strip().endswith("|"):
                block.append(lines[k].strip())
                k += 1
            sep_idx = None
            for bi, bl in enumerate(block):
                cells = split_row(bl.strip().strip("|"))
                if is_gfm_sep(cells):
                    sep_idx = bi
                    break
            if sep_idx is not None and sep_idx + 1 < len(block):
                hdr = split_row(block[sep_idx].strip().strip("|"))
                hn = len(hdr)
                for ri in range(sep_idx + 1, len(block)):
                    cells = split_row(block[ri].strip().strip("|"))
                    if len(cells) != hn:
                        hits.append((j + 1 + ri, "S5-ragged-table", f"row has {len(cells)} cells, header has {hn}"))
            j = k
        else:
            j += 1
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Book")
    ap.add_argument("--dir", default=None, help="limit to a single directory")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    if args.dir:
        files = sorted(os.path.join(args.dir, f) for f in os.listdir(args.dir)
                       if f.startswith("ch") and f.endswith(".md"))
    else:
        files = collect_files(args.root)

    all_hits = {}
    counts = {}
    for fp in files:
        h = audit_file(fp)
        if h:
            all_hits[fp] = h
            for (_, cls, _) in h:
                counts[cls] = counts.get(cls, 0) + 1
        for (ln, cls, msg) in h:
            print(f"{fp}:{ln}:{cls}:{msg}")

    print(f"--- summary: files_with_hits={len(all_hits)} counts={counts}", file=__import__("sys").stderr)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(all_hits, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
