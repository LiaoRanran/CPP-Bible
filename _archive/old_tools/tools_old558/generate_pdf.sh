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
  --lua-filter "$ROOT/tools/details.lua"
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

def _strip_fence_title(t: str) -> str:
    # pandoc 不支持 `title="…"` 围栏属性（mkdocs superfences 专有）：任何非法属性
    # 都会让 pandoc 拒绝识别整个代码块（0 Verbatim），代码沦为散文，其内的 \n、
    # %s 等反斜杠序列进入 LaTeX → ! Undefined control sequence（exit 43）。
    # PDF 渲染不需要 title（题注行已含标题信息），构建期统一清洗为裸 ```lang。
    cleaned = []
    for ln in t.split("\n"):
        if ln.startswith("```") and " " in ln:
            ln = "```" + ln[3:].split()[0]
        cleaned.append(ln)
    return "\n".join(cleaned)

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
    (outdir / f"{part}.md").write_text(
        _strip_fence_title("\n\n\\newpage\n\n".join(parts)), encoding="utf-8")
    total_anchored += anchored
    print(f"  卷 {part}: {len(metas)} 章 · 注入锚点 {anchored}")
print(f"[by-part] 合计注入 H1 锚点 {total_anchored}/{len(idx)}")
PY
  echo "[3/3] pandoc 逐卷生成 PDF ..."
  # 与 epub 同理：part*.md 位于 build/pdf/parts/，以 `../assets/...` 引用历史贴图；
  # cd 进 parts 使 `../assets` 命中 build/pdf/assets/（由 rewrite_links --mode pdf 复制）。
  # 输出用 $ROOT 绝对路径，避免 cd 影响落点。
  # mermaid-filter 依赖 Chromium；若其渲染崩溃则整 job 红，故失败时降级为纯代码块重试。
  # 诊断增强（2026-09-04）：CI 日志匿名不可读（API 403 / 网页要求登录），pandoc/xelatex
  # 的错误行曾是排障盲区（exit 43 黑盒）。改为逐卷收集失败（一卷失败不再中断后续卷），
  # 把 `!` 错误行写入 GITHUB_STEP_SUMMARY（check-runs API 匿名可读 output.summary，
  # mypy 步骤已验证该通道）+ ::error annotation，一轮 CI 即可拿到全部失败卷的报错。
  build_part_pdf() {
    local filter="$1"
    local fail_total=0
    local summary="${GITHUB_STEP_SUMMARY:-}"
    cd "$OUTPUT_DIR/parts" || return 1
    for pf in part*.md; do
      base="$(basename "$pf" .md)"
      errf="$ROOT/$OUTPUT_DIR/$base.pandoc.err"
      echo "  → $base.pdf"
      set +e
      pandoc "$pf" -o "$ROOT/$OUTPUT_DIR/$base.pdf" "${PANDOC_COMMON[@]}" $filter &> "$errf"
      rc=$?
      set -e
      if [ "$rc" -eq 0 ]; then
        rm -f "$errf"
        continue
      fi
      fail_total=$((fail_total + 1))
      echo "[error] $base 构建失败 (pandoc exit=$rc)" >&2
      if [ -n "$summary" ]; then
        {
          echo "## PDF 构建失败：$base（pandoc exit=$rc）"
          echo ''
          echo '```text'
          grep -E '^!|^l\.[0-9]+|LaTeX Error|Emergency stop|Fatal error' "$errf" | head -50 || true
          echo '```'
        } >> "$summary"
      fi
      if grep -qE '^!' "$errf" 2>/dev/null; then
        export PDF_LATEX_ERR=1
        # 带上下文（-B1 取上一行 / -A3 取错误命令名与 l.NNN 行号），压平为单行
        # 写入 annotation message（API 可返回完整 message，是匿名可见的取证通道）。
        first_err="$( { grep -m1 -B1 -A3 -E '^!' "$errf" || true; } | tr '\n' ' ' | tr -s ' ' | cut -c1-600 | tr -d '%' || true)"
        if [ -n "$first_err" ]; then
          echo "::error title=PDF $base::$first_err"
        fi
      fi
    done
    cd "$ROOT" >/dev/null || return 1
    if [ "$fail_total" -gt 0 ]; then return 1; fi
    return 0
  }
  if [ -n "$MERMAID_FILTER" ]; then
    if ! build_part_pdf "$MERMAID_FILTER"; then
      if [ "${PDF_LATEX_ERR:-0}" = "1" ]; then
        echo "[error] 存在 LaTeX 层错误（非 mermaid 渲染问题），跳过降级重试；错误行见 Step Summary。" >&2
        exit 1
      fi
      echo "[warn] mermaid-filter 渲染失败（Chromium 缺失/崩溃），降级为纯代码块重试..." >&2
      build_part_pdf ""
    fi
  else
    build_part_pdf ""
  fi
  echo "Done: $OUTPUT_DIR/part*.pdf"
  ls -lh "$OUTPUT_DIR"/part*.pdf
else
  echo "[2/3] 前置首页 INDEX.md ..."
  TMP="$OUTPUT_DIR/combined_src/full.md"
  { cat INDEX.md; printf '\n\\newpage\n\n'; cat "$COMBINED"; } > "$TMP"
  echo "[3/3] pandoc 单卷生成 PDF (xelatex) ..."
  # cd 进 combined_src：full.md 以 `../assets/...` 引用贴图，`../assets` 命中 build/pdf/assets/
  # mermaid-filter 崩溃时降级为纯代码块重试。
  build_single_pdf() {
    local filter="$1"
    ( cd "$(dirname "$TMP")" && pandoc "$(basename "$TMP")" -o "$ROOT/$OUTPUT" "${PANDOC_COMMON[@]}" $filter )
  }
  if [ -n "$MERMAID_FILTER" ]; then
    if ! build_single_pdf "$MERMAID_FILTER"; then
      echo "[warn] mermaid-filter 渲染失败（Chromium 缺失/崩溃），降级为纯代码块重试..." >&2
      build_single_pdf ""
    fi
  else
    build_single_pdf ""
  fi
  echo "Done: $OUTPUT"
  ls -lh "$OUTPUT"
fi
