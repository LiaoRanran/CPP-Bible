#!/bin/bash
# generate_pdf.sh — 生成《现代 C++ 终极圣经》PDF（v2 发布管线）
#
# 依赖（CI 环境已装；本地 Windows 通常缺，见文末降级方案）：
#   - pandoc >= 3.x
#   - texlive-xetex（xelatex）
#   - Noto Sans CJK SC / Noto Sans Mono CJK SC 字体
#   - mermaid-filter（npm，可选；缺失则 Mermaid 块降级为代码块，不阻断）
#
# 相比 v1 的改进：
#   1. 用 tools/rewrite_links.py --mode pdf 产出的 combined.md，跨章引用已重写为
#      书内锚点 (#chNN)，合并 PDF 内可正确跳转（v1 的裸路径在 PDF 中失效）。
#   2. 检测 mermaid-filter：存在则渲染 127 处 Mermaid 图为矢量，缺失则安全降级。
#   3. 支持 --by-part 分卷：142K 行单文件 xelatex 易爆内存/超时，分卷更稳。
#   4. 依赖缺失时明确报错并给出安装指引，不产出半成品。
#
# 用法：
#   bash tools/generate_pdf.sh            # 单卷全书
#   bash tools/generate_pdf.sh --by-part  # 按 16 个 part 分卷
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUTPUT_DIR="build/pdf"
OUTPUT="$OUTPUT_DIR/现代C++终极圣经.pdf"
COMBINED="$OUTPUT_DIR/combined_src/combined.md"
BY_PART="${1:-}"

PYTHON="${PYTHON:-python3}"

# ---- 0. 依赖检测 ----
missing=()
command -v pandoc  >/dev/null 2>&1 || missing+=("pandoc")
command -v xelatex >/dev/null 2>&1 || missing+=("xelatex(texlive-xetex)")
if [ "${#missing[@]}" -gt 0 ]; then
  echo "ERROR: 缺少必要依赖: ${missing[*]}" >&2
  echo "" >&2
  echo "  Ubuntu/CI:  sudo apt-get install -y pandoc texlive-xetex texlive-lang-chinese fonts-noto-cjk" >&2
  echo "              npm install -g mermaid-filter   # 可选，渲染 Mermaid" >&2
  echo "  本地 Windows 降级：改用静态站点(make site)在浏览器打印为 PDF，" >&2
  echo "                    或在 WSL/CI 中运行本脚本。" >&2
  exit 2
fi

MERMAID_FILTER=""
if command -v mermaid-filter >/dev/null 2>&1; then
  MERMAID_FILTER="--filter mermaid-filter"
  echo "[info] 检测到 mermaid-filter：将渲染 Mermaid 图为矢量。"
else
  echo "[warn] 未检测到 mermaid-filter：Mermaid 块将降级为普通代码块（不阻断）。"
fi

# ---- 1. 链接重写 → combined.md ----
echo "[1/3] 重写跨章引用为书内锚点 (rewrite_links --mode pdf) ..."
"$PYTHON" tools/rewrite_links.py --mode pdf

PANDOC_COMMON=(
  --pdf-engine=xelatex
  -V mainfont="Noto Sans CJK SC"
  -V monofont="Noto Sans Mono CJK SC"
  -V geometry:margin=2cm
  -V fontsize=11pt
  -V colorlinks=true
  -V linkcolor=blue
  -V toccolor=black
  --toc --toc-depth=2 -N
  --highlight-style=tango
)

if [ "$BY_PART" = "--by-part" ]; then
  echo "[2/3] 按 part 分卷生成 ..."
  # 分卷：从章索引按 part 切分（复用 Python 计算顺序）
  "$PYTHON" - <<'PY'
import re, pathlib, subprocess, os, sys
sys.path.insert(0, "tools")
from rewrite_links import build_chapter_index, rewrite_content, inject_chapter_anchor, ROOT
idx = build_chapter_index()
by_part = {}
for meta in idx.values():
    by_part.setdefault(meta["part"], []).append(meta)
outdir = pathlib.Path("build/pdf/parts"); outdir.mkdir(parents=True, exist_ok=True)
total_anchored = 0
for part, metas in sorted(by_part.items(), key=lambda kv: int(re.match(r"part(\d+)", kv[0]).group(1))):
    metas.sort(key=lambda m: m["num"])
    parts = []
    anchored = 0
    for m in metas:
        c = (ROOT / m["path"]).read_text(encoding="utf-8", errors="replace")
        nc, _ = rewrite_content(c, m["path"], idx, mode="pdf")
        # 与单卷路径一致：给每章 H1 注入 {#chNN}，使分卷内跨章链接可跳转。
        nc, subs = inject_chapter_anchor(nc, m["slug"])
        anchored += subs
        parts.append(nc)
    (outdir / f"{part}.md").write_text("\n\n\\newpage\n\n".join(parts), encoding="utf-8")
    total_anchored += anchored
    print(f"  卷 {part}: {len(metas)} 章 · 注入锚点 {anchored}")
print(f"[by-part] 合计注入 H1 锚点 {total_anchored}/{len(idx)}")
PY
  echo "[3/3] pandoc 逐卷生成 PDF ..."
  for pf in build/pdf/parts/part*.md; do
    base="$(basename "$pf" .md)"
    echo "  → $base.pdf"
    pandoc "$pf" -o "$OUTPUT_DIR/$base.pdf" "${PANDOC_COMMON[@]}" $MERMAID_FILTER
  done
  echo "Done: $OUTPUT_DIR/part*.pdf"
  ls -lh "$OUTPUT_DIR"/part*.pdf
else
  echo "[2/3] 前置首页 INDEX.md ..."
  TMP="$OUTPUT_DIR/combined_src/full.md"
  { cat INDEX.md; printf '\n\\newpage\n\n'; cat "$COMBINED"; } > "$TMP"
  echo "[3/3] pandoc 单卷生成 PDF (xelatex) ..."
  pandoc "$TMP" -o "$OUTPUT" "${PANDOC_COMMON[@]}" $MERMAID_FILTER
  echo "Done: $OUTPUT"
  ls -lh "$OUTPUT"
fi
