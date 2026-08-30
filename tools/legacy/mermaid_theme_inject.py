#!/usr/bin/env python3
# tools/mermaid_theme_inject.py
# 幂等注入统一 Mermaid frontmatter（theme: neutral + 九层真相模型 classDef 调色板）。
# 仅当 ```mermaid 块首个非空内容行不是 `---`(frontmatter) 且不含 `%%{init` 时插入。
# 用法:
#   python tools/mermaid_theme_inject.py --check  <path>    # 仅报告，不写
#   python tools/mermaid_theme_inject.py --apply  <path>    # 写入（默认 Book/）
# <path> 可为文件或目录（目录递归 .md）。
import argparse
import os

FRONTMATTER = """---
theme: neutral
classDef std   fill:#1f77b4,stroke:#13507a,color:#fff
classDef impl  fill:#ff7f0e,stroke:#a4520a,color:#fff
classDef plat  fill:#2ca02c,stroke:#16401a,color:#fff
classDef uarch fill:#d62728,stroke:#a11414,color:#fff
classDef algo  fill:#9467bd,stroke:#513470,color:#fff
classDef eng   fill:#8c564b,stroke:#512c26,color:#fff
classDef exp   fill:#e377c2,stroke:#a13e7f,color:#fff
classDef hyp   fill:#7f7f7f,stroke:#444444,color:#fff
classDef xp    fill:#bcbd22,stroke:#767706,color:#fff
---"""

def has_frontmatter(block_lines):
    for ln in block_lines:
        s = ln.strip()
        if not s:
            continue
        if s == "---":
            return True
        if s.startswith("%%{init"):
            return True
        return False  # first non-empty content line is not frontmatter
    return False

def process_file(path, apply):
    with open(path, "r", encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    out = []
    i = 0
    n = len(lines)
    changed = 0
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            # 收集块内容直到闭合 ```
            out.append(line)
            i += 1
            block = []
            while i < n and lines[i].strip() != "```":
                block.append(lines[i])
                i += 1
            # 闭合 ```
            close = lines[i] if i < n else "```"
            if not has_frontmatter(block):
                for fm in FRONTMATTER.split("\n"):
                    out.append(fm)
                changed += 1
            out.extend(block)
            out.append(close)
            i += 1
        else:
            out.append(line)
            i += 1
    if apply and changed:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(out))
    return changed

def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, fs in os.walk(p):
                for fn in fs:
                    if fn.endswith(".md"):
                        files.append(os.path.join(root, fn))
        elif p.endswith(".md"):
            files.append(p)
    return sorted(set(files))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=["Book"])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    files = collect(args.paths)
    total_changed = 0
    changed_files = []
    for fp in files:
        c = process_file(fp, args.apply)
        if c:
            total_changed += c
            changed_files.append((fp, c))
    mode = "APPLY" if args.apply else "CHECK"
    print(f"[{mode}] 扫描 {len(files)} 个 .md 文件")
    print(f"[{mode}] 注入 frontmatter 的 mermaid 块: {total_changed}")
    if not args.apply:
        for fp, c in changed_files:
            print(f"   {fp}: +{c}")

if __name__ == "__main__":
    main()
