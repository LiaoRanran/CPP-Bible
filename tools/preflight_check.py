#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
preflight_check.py — 推送前本地/CI 预检门禁（错误左移，秒级反馈）

背景
----
全书 PDF (pandoc + xelatex) 曾连续多次在 CI 才暴露构建失败，来回浪费 10+ 分钟。
根因分类（截至 2026-07-13）：
  1. Chromium sandbox FATAL          → 已由 .puppeteer.json 解决
  2. Mermaid 解析语法错误            → 由 mermaid oracle (mjs) 校验，见 --mermaid
  3. LaTeX 标题裸反斜杠 \n           → 本脚本 CHECK-1 捕获
  4. LaTeX 表格/正文裸反斜杠 \n      → 本脚本 CHECK-1 捕获

本脚本用纯 Python（零依赖）在 push 前 <1s 抓出会让 xelatex 崩溃的
"Undefined control sequence" 类错误，避免进 CI 才发现。

检查项
------
CHECK-1  致命反斜杠：fenced code / inline code / 行内数学 之外的 `\<letter>`
         （如 '\n' '\t'，或 Windows 路径 C:\Users 里的 \U）。pandoc 会把它原样
         送进 LaTeX，`\n` 等非法控制序列导致整本 xelatex 中断 (exit 43)。
         修复：包进行内代码 `\n`（LaTeX 渲染为 \texttt，标签/交叉引用不受影响）。

用法
----
  python3 tools/preflight_check.py                 # 扫描 Book/，有问题非零退出
  python3 tools/preflight_check.py --json out.json # 额外输出 JSON 报告
  python3 tools/preflight_check.py Book/part14_perf # 只扫指定子树

退出码：0=干净；1=发现致命问题。
"""
import sys, re, json, pathlib

# ---- 正则 ----
FENCE_RE  = re.compile(r'^\s*(```|~~~)')            # fenced code 起止
DANGER_RE = re.compile(r'\\[a-zA-Z]')              # 反斜杠 + ASCII 字母
DBLTICK   = re.compile(r'``[^`]*``')               # 行内代码（双反引号）
TICK      = re.compile(r'`[^`]*`')                 # 行内代码（单反引号）
IMATH     = re.compile(r'\$[^$]*\$')               # 行内数学 $...$

def strip_protected(line: str) -> str:
    """移除行内代码与行内数学（这些区域内的反斜杠对 LaTeX 安全）。"""
    line = DBLTICK.sub('', line)
    line = TICK.sub('', line)
    line = IMATH.sub('', line)
    return line

def scan_file(path: pathlib.Path):
    hits = []
    in_fence = False
    fence_marker = None
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except UnicodeDecodeError:
        return hits  # 非 utf-8 跳过（不应出现）
    for i, raw in enumerate(lines, 1):
        m = FENCE_RE.match(raw)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence, fence_marker = False, None
            continue
        if in_fence:
            continue
        text = strip_protected(raw)
        for mm in DANGER_RE.finditer(text):
            seq = mm.group(0)
            hits.append({
                "line": i,
                "seq": seq,
                "content": raw.strip()[:160],
            })
    return hits

def main(argv):
    args = [a for a in argv[1:] if not a.startswith('--')]
    json_out = None
    if '--json' in argv[1:]:
        idx = argv.index('--json')
        if idx + 1 < len(argv):
            json_out = argv[idx + 1]
            args = [a for a in args if a != json_out]
    roots = args or ['Book']

    md_files = []
    for r in roots:
        p = pathlib.Path(r)
        if p.is_file() and p.suffix == '.md':
            md_files.append(p)
        elif p.is_dir():
            md_files.extend(sorted(p.rglob('*.md')))
    # 排除 legacy 归档
    md_files = [f for f in md_files if '_legacy' not in str(f)]

    total_hits = 0
    report = {}
    for f in md_files:
        hits = scan_file(f)
        if hits:
            report[str(f).replace('\\', '/')] = hits
            total_hits += len(hits)

    print("=" * 70)
    print("preflight_check — CHECK-1 致命反斜杠（LaTeX Undefined control sequence）")
    print("=" * 70)
    print(f"扫描 {len(md_files)} 个 .md 文件")
    if not report:
        print("[OK] 未发现 fenced/inline code 之外的致命反斜杠序列。")
    else:
        print(f"[FAIL] 发现 {total_hits} 处致命反斜杠，分布在 {len(report)} 个文件：\n")
        for fp, hits in report.items():
            print(f"  {fp}")
            for h in hits:
                print(f"    L{h['line']:<5} {h['seq']}   | {h['content']}")
            print()

    if json_out:
        pathlib.Path(json_out).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"[JSON] 报告已写入 {json_out}")

    return 1 if report else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
