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

# mermaid-filter 默认关闭：CI 实测（run #373 及 2026-08-30 多轮）pandoc + mermaid-filter
# 在 ubuntu runner 上于 1~3 分钟内连带 bash 被信号终止（步骤显示 cancelled，降级逻辑
# 来不及生效），EPUB 从未产出。需要渲染时显式 CPPBIBLE_EPUB_MERMAID=1。
MERMAID_FILTER=""
if [ "${CPPBIBLE_EPUB_MERMAID:-0}" = "1" ] && command -v mermaid-filter >/dev/null 2>&1; then
  MERMAID_FILTER="--filter mermaid-filter"
  echo "[info] 检测到 mermaid-filter：Mermaid 块将渲染为 SVG 嵌入 EPUB。"
else
  echo "[info] mermaid-filter 未启用（CPPBIBLE_EPUB_MERMAID!=1 或未安装）：Mermaid 块为普通代码块。"
fi

# ---- 1. 链接重写 → combined.md ----
echo "[1/2] 重写跨章引用为书内锚点 (rewrite_links --mode pdf) ..."
"$PYTHON" tools/rewrite_links.py --mode pdf

# ---- 2. pandoc → EPUB3 ----
mkdir -p "$OUTPUT_DIR"
echo "[2/2] pandoc 生成 EPUB (epub3) ..."
# 关键：combined.md 以 `../assets/history/x.jpg` 引用历史贴图。pandoc 按 *工作目录*
# 解析资源路径（实测：并非 input 文件所在目录），故 cd 进 combined_src，使 `../assets`
# 命中 rewrite_links --mode pdf 已复制的 build/pdf/assets/。否则图片断链仅报 WARNING、
# EPUB 虽生成但配图缺失。输出改用 $ROOT 绝对路径避免 cd 影响落点。
# mermaid-filter 依赖 Chromium；若 CI 环境缺 Chromium/系统库导致渲染崩溃（exit≠0），
# 则降级为纯代码块重试，保证 EPUB 始终产出（不整 job 红）。
build_epub() {
  local filter="$1"
  ( cd "$(dirname "$COMBINED")" && \
    pandoc "$(basename "$COMBINED")" -o "$ROOT/$OUTPUT_DIR/现代C++终极圣经.epub" \
      --toc --toc-depth=2 --split-level=1 \
      --metadata title="现代 C++ 终极圣经" \
      --metadata author="LiaoRanran" --metadata lang=zh \
      --metadata publisher="CPP-Bible Project" --metadata rights="CC BY-NC-SA 4.0" \
      $filter )
}
if [ -n "$MERMAID_FILTER" ]; then
  if ! build_epub "$MERMAID_FILTER"; then
    echo "[warn] mermaid-filter 渲染失败（Chromium 缺失/崩溃），降级为纯代码块重试..." >&2
    build_epub ""
  fi
else
  build_epub ""
fi
echo "Done: $OUTPUT_DIR/现代C++终极圣经.epub"
ls -lh "$OUTPUT_DIR"/*.epub
