#!/bin/bash
# generate_epub.sh — 生成《现代 C++ 终极圣经》EPUB（L2 发布管线）
#
# 依赖（CI 环境已装；本地 Windows 通常缺，见文末降级方案）：
#   - pandoc >= 3.x
#   - mermaid-filter（npm，可选；缺失则 Mermaid 块降级为代码块，不阻断）
#
# 复用 rewrite_links --mode pdf 产出的 combined.md（跨章引用已重写为
# 书内锚点 #chNN，H1 已显式注入 {#chNN}；EPUB/PDF 跨章跳转经本地 pandoc 端到端验证可用）。
#
# 用法：
#   bash tools/generate_epub.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUTPUT_DIR="build/epub"
COMBINED="build/pdf/combined_src/combined.md"
PYTHON="${PYTHON:-python3}"

# ---- 0. 依赖检测 ----
missing=()
command -v pandoc >/dev/null 2>&1 || missing+=("pandoc")
if [ "${#missing[@]}" -gt 0 ]; then
  echo "ERROR: 缺少必要依赖: ${missing[*]}" >&2
  echo "  Ubuntu/CI:  sudo apt-get install -y pandoc" >&2
  echo "  本地 Windows 降级：在 WSL/CI 中运行本脚本。" >&2
  exit 2
fi

MERMAID_FILTER=""
if command -v mermaid-filter >/dev/null 2>&1; then
  MERMAID_FILTER="--filter mermaid-filter"
  echo "[info] 检测到 mermaid-filter：Mermaid 块将渲染为 SVG 嵌入 EPUB。"
else
  echo "[warn] 未检测到 mermaid-filter：Mermaid 块将降级为普通代码块（不阻断）。"
fi

# ---- 1. 链接重写 → combined.md ----
echo "[1/2] 重写跨章引用为书内锚点 (rewrite_links --mode pdf) ..."
"$PYTHON" tools/rewrite_links.py --mode pdf

# ---- 2. pandoc → EPUB3 ----
mkdir -p "$OUTPUT_DIR"
echo "[2/2] pandoc 生成 EPUB (epub3) ..."
pandoc "$COMBINED" -o "$OUTPUT_DIR/现代C++终极圣经.epub" \
  --toc --toc-depth=2 \
  --epub-chapter-level=1 \
  --epub-cover-image=assets/cover.png \
  --metadata title="现代 C++ 终极圣经" \
  --metadata author="LiaoRanran" \
  --metadata lang=zh \
  --metadata publisher="CPP-Bible Project" \
  --metadata rights="CC BY-NC-SA 4.0" \
  $MERMAID_FILTER
echo "Done: $OUTPUT_DIR/现代C++终极圣经.epub"
ls -lh "$OUTPUT_DIR"/*.epub
