#!/usr/bin/env python3
# tools/table_style_audit.py
# 审计 Markdown 表格视觉规范（CONVENTIONS §4.2）：
#   - 断表（连续 pipe 行却无分隔行，且不在代码围栏内）
#   - 表头/分隔行列数不一致
#   - 数据行列数与表头不一致
#   - 分隔行紧上方误插块引用 `>`（已知会破坏渲染的 BREAK）
#   - 分隔行无表头
# 可靠性：
#   * 跳过 ``` / ~~~ 代码围栏内的"伪表格"（那是代码/ASCII 示意，非 Markdown 表）
#   * 单元格内的 `\|` 与反引号代码跨 ` `...|...` ` 中的 `|` 视为字面量，不计入列分割
# 用法: python tools/table_style_audit.py [path]   (默认 Book/)
import os
import re
import sys

PIPE_RE = re.compile(r"^\s*\|.*\|\s*$")
SEP_CELL_RE = re.compile(r"^:?-+:?$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

def mask_pipes(s):
    # 先处理转义 \|
    s = s.replace(r"\|", "\x00")
    # 反引号代码跨内的 | 视为字面量
    def repl(m):
        return m.group(0).replace("|", "\x00")
    return re.sub(r"`[^`]*`", repl, s)

def split_cells(line):
    s = mask_pipes(line.strip())
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]

def audit_file(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        raw = f.read().split("\n")
    issues = []
    in_fence = False
    pipe = []  # (lineno, cells, is_sep)
    for i, ln in enumerate(raw):
        if FENCE_RE.match(ln):
            # 切换围栏状态（仅当不在围栏内时开，在内时关）
            if not in_fence:
                in_fence = True
            else:
                in_fence = False
            continue
        if in_fence:
            continue
        if PIPE_RE.match(ln):
            cells = split_cells(ln)
            is_sep = bool(cells) and all(SEP_CELL_RE.match(c) for c in cells)
            pipe.append((i, cells, is_sep))
    # 按连续行号分组
    groups, cur, prev = [], [], None
    for row in pipe:
        if prev is None or row[0] == prev + 1:
            cur.append(row)
        else:
            groups.append(cur); cur = [row]
        prev = row[0]
    if cur:
        groups.append(cur)
    for g in groups:
        seps = [r for r in g if r[2]]
        if not seps:
            issues.append((g[0][0], "断表：连续表格行却无分隔行(|---|)（且不在代码围栏内）"))
            continue
        for idx, (ln, cells, is_sep) in enumerate(g):
            if not is_sep:
                continue
            if idx == 0:
                issues.append((ln, "分隔行位于表首，缺少表头行"))
                continue
            hdr_ln, hdr_cells, _ = g[idx-1]
            if len(hdr_cells) != len(cells):
                issues.append((ln, f"表头/分隔行列数不一致：表头 {len(hdr_cells)} vs 分隔 {len(cells)}"))
            if hdr_ln + 1 != ln:
                mid = raw[hdr_ln+1] if hdr_ln+1 < len(raw) else ""
                if mid.lstrip().startswith(">"):
                    issues.append((hdr_ln+1, "块引用 `>` 插在表头与分隔行之间（破坏渲染）"))
            if idx+1 < len(g):
                nxt_ln, nxt_cells, nxt_sep = g[idx+1]
                if nxt_ln == ln + 2 and raw[ln+1].lstrip().startswith(">"):
                    issues.append((ln+1, "块引用 `>` 插在分隔行与首数据行之间（破坏渲染）"))
            for (dln, dcells, dsep) in g[idx+1:]:
                if dsep:
                    continue
                if len(dcells) != len(hdr_cells):
                    issues.append((dln, f"数据行列数与表头不一致：{len(dcells)} vs 表头 {len(hdr_cells)}"))
    return issues

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "Book"
    files = []
    if os.path.isdir(root):
        for r, _, fs in os.walk(root):
            for fn in fs:
                if fn.endswith(".md"):
                    files.append(os.path.join(r, fn))
    else:
        files = [root]
    total = 0
    for fp in sorted(files):
        iss = audit_file(fp)
        if iss:
            total += len(iss)
            print(f"== {fp} ({len(iss)}) ==")
            for ln, msg in iss:
                print(f"   L{ln+1}: {msg}")
    print(f"\n合计 {total} 处表格问题（扫描 {len(files)} 文件，已排除代码围栏内伪表）")

if __name__ == "__main__":
    main()
