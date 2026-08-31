#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_mkdocs_nav.py — 生成 MkDocs 站点配置与导航

职责
====
1. 复用 rewrite_links.build_chapter_index() 拿到 147 章的 {路径,标题,part,章号}。
2. 从 INDEX.md 解析 16 个 part 的中文标题，作为 nav 分组名。
3. 生成完整 build/site/mkdocs.yml（Material 主题 + mermaid2 插件 + 中文搜索）。
4. 生成 build/site/docs/index.md 站点欢迎页（不注水，仅导航与统计）。

前置：需先运行 `rewrite_links.py --mode site` 生成 build/site/docs/。
nav 路径相对 docs_dir(=docs)，与重写后的目录结构一致。
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rewrite_links import build_chapter_index, ROOT  # noqa: E402

SITE_DIR = ROOT / "build" / "site"
DOCS_DIR = SITE_DIR / "docs"
INDEX_MD = ROOT / "INDEX.md"

PART_TITLE_RE = re.compile(r"^##\s+Part\s+(\d+):\s*(.+?)\s*(?:\(\d+章\))?\s*$", re.MULTILINE)

# 兜底中文 part 标题：目录名 partNN 与主题 1:1 对应。
# 当 INDEX.md 未提供 `## Part N: <标题>` 时启用，确保导航显示可读标题而非裸目录名。
DEFAULT_PART_TITLES = {
    1: "C++ 历史与标准",
    2: "开发环境与工具链",
    3: "语言基础",
    4: "内存管理",
    5: "面向对象",
    6: "模板与元编程",
    7: "STL 容器",
    8: "算法",
    9: "并发",
    10: "现代 C++",
    11: "源码解析",
    12: "设计模式",
    13: "工程实践",
    14: "性能优化",
    15: "工业案例",
    16: "源码阅读路线",
}


def parse_part_titles() -> dict:
    """从 INDEX.md 解析 {part序号: 中文标题}。序号 1..16 对应 partNN 目录。"""
    titles = {}
    if INDEX_MD.exists():
        text = INDEX_MD.read_text(encoding="utf-8", errors="replace")
        for m in PART_TITLE_RE.finditer(text):
            titles[int(m.group(1))] = m.group(2).strip()
    return titles


def _part_seq(part_dirname: str) -> int:
    """'part07_stl' → 7。"""
    m = re.match(r"part(\d+)", part_dirname)
    return int(m.group(1)) if m else 999


def yq(s: str) -> str:
    """YAML 双引号安全转义。"""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_nav(index: dict, part_titles: dict) -> str:
    # 按 part 目录聚合，再按章号排序
    parts: dict[str, list] = {}
    for rel, meta in index.items():
        parts.setdefault(meta["part"], []).append(meta)
    for lst in parts.values():
        lst.sort(key=lambda m: m["num"])

    lines = ["nav:"]
    lines.append('  - "首页": index.md')
    lines.append('  - "搜索": search.md')
    # 全局导航件
    if (DOCS_DIR / "CROSSREF.md").exists():
        lines.append('  - "全局导航":')
        lines.append('    - "交叉引用依赖索引 (CROSSREF)": CROSSREF.md')
    # 外部资产（docs/、Appendix/ 中被书内链接引用，由 rewrite_links 写入 manifest）
    # strict 模式要求所有文档文件出现在 nav，否则报 not-in-nav 警告。
    manifest_path = SITE_DIR / "external_assets.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = []
        if manifest:
            lines.append('  - "附录 / 外部资源":')
            for item in manifest:
                lines.append(f"    - {yq(item['title'])}: {item['path']}")
    # 各 part
    for part_dir in sorted(parts.keys(), key=_part_seq):
        seq = _part_seq(part_dir)
        ptitle = part_titles.get(seq) or DEFAULT_PART_TITLES.get(seq, part_dir)
        lines.append(f'  - {yq(f"Part {seq}｜{ptitle}")}:')
        for meta in parts[part_dir]:
            nav_path = f"Book/{part_dir}/{meta['name']}"
            lines.append(f"    - {yq(meta['title'])}: {nav_path}")
    return "\n".join(lines)


SEARCH_PAGE = """\
# 全文搜索

本页由 PageFind 提供中英文全文检索（章标题、正文、代码标识符均可命中）。

<div id="search"></div>
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<script src="/pagefind/pagefind-ui.js"></script>
<script>
window.addEventListener('DOMContentLoaded', function () {
  new PagefindUI({ element: "#search", showSubResults: true });
});
</script>
"""

MKDOCS_TEMPLATE = """\
# mkdocs.yml — 《现代 C++ 终极圣经》静态站点配置
# 由 tools/gen_mkdocs_nav.py 生成，请勿手改；重生成：python tools/gen_mkdocs_nav.py
site_name: 现代 C++ 终极圣经
site_description: 147 章 · 14 万行 · 生产级现代 C++ 知识工程
docs_dir: docs
site_dir: ../../build/site_out
use_directory_urls: true

theme:
  name: material
  language: zh
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.top
    - navigation.indexes
    - navigation.sections
    - navigation.path
    - navigation.footer
    - toc.follow
    - toc.integrate
    - content.action.edit
    - content.code.copy
    - content.code.annotate
    - content.code.select
    - content.tooltips
    - search.suggest
    - search.highlight
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: 切换到深色
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: 切换到浅色

plugins:
  - mermaid2

markdown_extensions:
  - toc:
      permalink: true
      toc_depth: 3
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:mermaid2.fence_mermaid_custom
  - pymdownx.highlight:
      anchor_linenums: true
      use_pygments: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - attr_list
  - md_in_html

extra:
  generator: false

extra_css:
  - assets/extra.css

{nav}
"""


EXTRA_CSS = """\
/* ============================================================================
   CPP-Bible 站点自定义样式（extra.css）
   由 tools/gen_mkdocs_nav.py 注入 build/site/docs/assets/extra.css。
   分区：0 层级徽章 / 1 排版 / 2 代码块 / 3 标注块(admonition) /
        4 表格 / 5 定义列表 / 6 任务列表 / 7 引用与脚注 / 8 行内元素 /
        9 TOC 与导航 / 10 搜索 / 11 Mermaid / 12 打印与响应式
   ========================================================================== */

/* ---------- 0. 层级徽章（[标准]/[实现]/[经验]/[ABI]/[平台]/[微架构]/[史]/[轶]/[评]） ---------- */
/*   在 site 渲染为彩色标签；PDF/EPUB 走 pandoc 时 span 降级为纯文本，不崩。 */
.md-typeset .badge {
  display: inline-block;
  padding: 0.02em 0.55em;
  border-radius: 0.35em;
  font-size: 0.72em;
  font-weight: 700;
  line-height: 1.6;
  vertical-align: 0.12em;
  margin: 0 0.18em;
  letter-spacing: 0.02em;
  white-space: nowrap;
}
.md-typeset .badge-std  { background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }
.md-typeset .badge-impl { background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
.md-typeset .badge-exp  { background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }
.md-typeset .badge-abi  { background: #f3e5f5; color: #6a1b9a; border: 1px solid #ce93d8; }
.md-typeset .badge-platform { background: #e0f7fa; color: #006064; border: 1px solid #80deea; }
.md-typeset .badge-microarch { background: #ede7f6; color: #4527a0; border: 1px solid #b39ddb; }
.md-typeset .badge-history { background: #fce4ec; color: #ad1457; border: 1px solid #f48fb1; }
.md-typeset .badge-anecdote { background: #fff8e1; color: #f57f17; border: 1px solid #ffe082; }
.md-typeset .badge-comment { background: #eceff1; color: #455a64; border: 1px solid #b0bec5; }
.md-typeset .badge-ref { background: #e0f2f1; color: #00695c; border: 1px solid #80cbc4; }
.md-typeset .badge-measured { background: #dcedc8; color: #33691e; border: 1px solid #aed581; }
.md-typeset .badge-perf { background: #fbe9e7; color: #bf360c; border: 1px solid #ffab91; }

/* ---------- 1. 中文高密度技术文档排版优化：缓解「拥挤感」 ---------- */
.md-typeset {
  line-height: 1.8;
  font-feature-settings: "liga" 1, "calt" 1;
  text-rendering: optimizeLegibility;
}
.md-typeset p {
  margin: 0.9em 0;
}
.md-typeset ul, .md-typeset ol {
  margin: 0.7em 0;
}
.md-typeset li + li {
  margin-top: 0.35em;
}
.md-typeset h1 { letter-spacing: 0.01em; }
.md-typeset h2, .md-typeset h3 {
  margin-top: 1.7em;
  margin-bottom: 0.6em;
  font-weight: 700;
}
.md-typeset h4, .md-typeset h5, .md-typeset h6 {
  margin-top: 1.3em;
  margin-bottom: 0.4em;
  font-weight: 600;
}
.md-typeset hr {
  margin: 2em 0;
  border: none;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}
.md-typeset img {
  margin: 1em auto;
  border-radius: 4px;
  max-width: 100%;
  height: auto;
}
.md-typeset a {
  text-decoration: none;
}
.md-typeset a:hover {
  text-decoration: underline;
}

/* ---------- 2. 代码块增强 ---------- */
.md-typeset pre {
  margin: 1.1em 0;
  line-height: 1.55;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.16);
}
.md-typeset pre > code {
  display: block;
  padding: 0.9em 1.1em;
  font-size: 0.82rem;
}
.md-typeset .highlight pre,
.md-typeset pre code {
  tab-size: 4;
}
/* 行内代码 */
.md-typeset code {
  background-color: rgba(135, 131, 120, 0.15);
  padding: 0.12em 0.35em;
  border-radius: 3px;
  font-size: 0.86em;
  word-break: break-word;
}
.md-typeset a > code {
  color: inherit;
}
/* 代码注解高亮（content.code.annotate：#!python ...） */
.md-typeset .highlight .linenodiv,
.md-typeset .highlight .hll {
  background-color: rgba(255, 235, 59, 0.18);
  display: block;
  margin: 0 -1.1em;
  padding: 0 1.1em;
}
/* 复制按钮 */
.md-typeset .md-clipboard {
  color: var(--md-default-fg-color--light);
  transition: color 0.2s;
}
.md-typeset .md-clipboard:hover {
  color: var(--md-accent-fg-color);
}
/* 代码字体回退：优先等宽且支持连字 */
.md-typeset pre code,
.md-typeset code {
  font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", "Source Code Pro",
    "DejaVu Sans Mono", "Sarasa Mono SC", "Noto Sans Mono CJK SC", monospace;
}

/* ---------- 3. 标注块(admonition) 配色与强调 ---------- */
.md-typeset .admonition {
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}
.md-typeset .admonition-title {
  font-weight: 700;
}
.md-typeset .admonition.note { border-left: 4px solid #448aff; }
.md-typeset .admonition.info { border-left: 4px solid #00b8d4; }
.md-typeset .admonition.success { border-left: 4px solid #00c853; }
.md-typeset .admonition.tip { border-left: 4px solid #00bfa5; }
.md-typeset .admonition.warning { border-left: 4px solid #ff9100; }
.md-typeset .admonition.danger { border-left: 4px solid #ff1744; }
.md-typeset .admonition.bug { border-left: 4px solid #f50057; }
.md-typeset .admonition.example { border-left: 4px solid #7c4dff; }
.md-typeset .admonition.quote { border-left: 4px solid #9e9e9e; }
/* 「类比：…」标注块在导航中更醒目 */
.md-typeset .admonition.note .admonition-title::before {
  margin-right: 0.4em;
}
/* 标注块内代码块去掉外阴影，避免嵌套过深 */
.md-typeset .admonition pre {
  box-shadow: none;
}

/* ---------- 4. 表格：斑马纹 + 粘性表头 ---------- */
.md-typeset table:not([class]) {
  margin: 1.1em 0;
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  overflow: hidden;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.10);
}
.md-typeset table:not([class]) th,
.md-typeset table:not([class]) td {
  padding: 0.55em 0.9em;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}
.md-typeset table:not([class]) th {
  background: var(--md-primary-fg-color, #3f51b5);
  color: #fff;
  font-weight: 600;
  text-align: left;
  position: sticky;
  top: 0;
}
.md-typeset table:not([class]) tr:nth-child(even) td {
  background: rgba(0, 0, 0, 0.025);
}
.md-typeset table:not([class]) tr:hover td {
  background: rgba(66, 165, 245, 0.08);
}

/* ---------- 5. 定义列表 ---------- */
.md-typeset dl {
  margin: 1em 0;
}
.md-typeset dl dt {
  font-weight: 700;
  margin-top: 0.6em;
}
.md-typeset dl dd {
  margin: 0 0 0.6em 1.4em;
  color: var(--md-default-fg-color--light);
}

/* ---------- 6. 任务列表（GFM checkbox） ---------- */
.md-typeset li.task-list-item {
  list-style: none;
}
.md-typeset li.task-list-item::before {
  content: "";
}
.md-typeset input[type="checkbox"] {
  margin: 0 0.4em 0 -1.4em;
  vertical-align: middle;
}

/* ---------- 7. 引用与脚注 ---------- */
.md-typeset blockquote {
  margin: 1em 0;
  padding: 0.4em 1em;
  border-left: 4px solid #90caf9;
  background: #f5f9ff;
  color: var(--md-default-fg-color--light);
  border-radius: 0 4px 4px 0;
}
.md-typeset blockquote p {
  margin: 0.4em 0;
}
.md-typeset .footnote {
  font-size: 0.85em;
  color: var(--md-default-fg-color--light);
}
.md-typeset .footnote-ref {
  font-size: 0.8em;
}

/* ---------- 8. 行内元素：kbd / abbr / mark / 键位 ---------- */
.md-typeset kbd {
  display: inline-block;
  padding: 0.1em 0.5em;
  font-size: 0.78em;
  font-family: var(--md-code-font-family, monospace);
  color: #fff;
  background: #455a64;
  border-radius: 4px;
  box-shadow: 0 2px 0 #263238;
  margin: 0 0.15em;
}
.md-typeset abbr[title] {
  text-decoration: underline dotted;
  cursor: help;
}
.md-typeset mark {
  background: #fff59d;
  padding: 0 0.15em;
  border-radius: 2px;
}
.md-typeset .keys {
  color: var(--md-accent-fg-color);
  font-weight: 600;
}

/* ---------- 9. TOC 与侧边导航 ---------- */
.md-typeset .toc a {
  transition: color 0.15s;
}
.md-nav__link--active,
.md-nav__link--active:hover {
  color: var(--md-accent-fg-color);
  font-weight: 600;
}
.md-sidebar--secondary .md-nav__link {
  font-size: 0.82rem;
}
/* 当前阅读位置高亮 */
.md-nav__item .md-nav__link--active::before {
  content: "\\2022";
  margin-right: 0.3em;
  color: var(--md-accent-fg-color);
}

/* ---------- 10. 搜索结果 ---------- */
.md-search__input {
  border-radius: 4px;
}
.md-search-result__article {
  border-radius: 4px;
  padding: 0.4em 0.8em;
}
.md-search-result__article--document {
  border-left: 3px solid var(--md-accent-fg-color);
}
.md-search-result__title {
  font-weight: 600;
}
.md-search-result em {
  background: #fff59d;
  font-style: normal;
  padding: 0 0.1em;
}

/* ---------- 11. Mermaid 容器 ---------- */
.md-typeset .mermaid {
  margin: 1.2em auto;
  padding: 1em;
  background: #fafafa;
  border: 1px solid #eeeeee;
  border-radius: 6px;
  text-align: center;
  overflow-x: auto;
}
.md-typeset .mermaid svg {
  max-width: 100%;
  height: auto;
}

/* ---------- 12. 打印与响应式 ---------- */
@media print {
  .md-typeset a {
    text-decoration: none;
  }
  .md-typeset .badge {
    border: 1px solid #999;
    color: #000 !important;
    background: #f0f0f0 !important;
  }
  .md-typeset pre,
  .md-typeset table:not([class]) {
    box-shadow: none;
    border: 1px solid #ccc;
  }
  .md-typeset .admonition {
    border-left-width: 3px;
    page-break-inside: avoid;
  }
  .md-typeset h2, .md-typeset h3 {
    page-break-after: avoid;
  }
}
@media (max-width: 768px) {
  .md-typeset {
    line-height: 1.7;
  }
  .md-typeset table:not([class]) th,
  .md-typeset table:not([class]) td {
    padding: 0.4em 0.6em;
  }
  .md-typeset pre > code {
    font-size: 0.78rem;
  }
}
/* 滚动条细窄化（WebKit/旧 Edge） */
.md-typeset pre::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}
.md-typeset pre::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.25);
  border-radius: 4px;
}
::selection {
  background: rgba(66, 165, 245, 0.25);
}

/* ---------- 13. 补充：折叠 / 选项卡 / 行内标注 / 可访问性 ---------- */
/* 折叠块（pymdownx.details） */
.md-typeset details {
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.10);
  padding: 0 1em;
}
.md-typeset details > summary {
  cursor: pointer;
  font-weight: 600;
  padding: 0.5em 0;
}
/* 选项卡（pymdownx.tabbed） */
.md-typeset .tabbed-set {
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.10);
}
.md-typeset .tabbed-labels > label {
  font-size: 0.84rem;
}
/* 行内标注（content.code.annotate 的 #! 注释高亮） */
.md-typeset .highlight .cp,
.md-typeset .highlight .c1 {
  font-style: italic;
  opacity: 0.85;
}
/* 「编辑此页」按钮间距（content.action.edit） */
.md-content__edit {
  font-size: 0.8rem;
}
/* 焦点可见性（可访问性） */
.md-typeset a:focus-visible,
.md-typeset button:focus-visible,
.md-typeset input:focus-visible {
  outline: 2px solid var(--md-accent-fg-color);
  outline-offset: 2px;
}
/* 尊重「减少动画」系统偏好 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }
}
/* 顶部阅读进度条 */
.md-typeset .progress {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: var(--md-accent-fg-color);
  z-index: 9999;
}
"""


WELCOME_TEMPLATE = """\
# 现代 C++ 终极圣经

> 147 章 · 约 14 万行 · 21,000+ 可编译 `cpp` 示例 · 生产级现代 C++ 知识工程

本站由项目源 Markdown 经发布管线（链接重写 + Mermaid 渲染 + Material 主题）自动生成。
所有跨章引用已重写为站内可点击链接；架构类章节内嵌 Mermaid 流程图。

## 如何使用

- **左侧导航**：按 16 个 Part（历史 → 工具链 → 语言核心 → … → 性能 → 案例 → 阅读路线）浏览全部 147 章。
- **「搜索」页**：基于 PageFind 的中英文全文检索（章标题、正文、代码标识符均可命中）。
- **交叉引用索引**：见「全局导航 → 交叉引用依赖索引 (CROSSREF)」，含全书 732 条章间依赖边、枢纽章 Top10 与孤立章清单。

## 全书结构一览

| Part | 主题 | 章数 |
|---|---|---|
{part_table}

## 工程约束（编者说明）

- 每个 `cpp` 代码块均为自包含、可独立编译（`g++ -std=c++23 -O2 -Wall -Wextra`，GCC 13.1.0）。
- 内容区分「标准规定 / 编译器实现 / 平台差异 / 工程经验」四类来源，避免混淆。
- 一致性门禁（章节完整性 + 交叉引用断链）持续维持 100/100。
"""


def build_part_table(index: dict, part_titles: dict) -> str:
    counts: dict[int, int] = {}
    for meta in index.values():
        counts[_part_seq(meta["part"])] = counts.get(_part_seq(meta["part"]), 0) + 1
    rows = []
    for seq in sorted(counts.keys()):
        rows.append(f"| {seq} | {part_titles.get(seq, '')} | {counts[seq]} |")
    return "\n".join(rows)


def main() -> int:
    if not DOCS_DIR.exists():
        print("ERROR: build/site/docs 不存在，请先运行 rewrite_links.py --mode site", file=sys.stderr)
        return 1
    index = build_chapter_index()
    part_titles = parse_part_titles()
    nav = build_nav(index, part_titles)
    mkdocs_yml = MKDOCS_TEMPLATE.format(nav=nav)
    (SITE_DIR / "mkdocs.yml").write_text(mkdocs_yml, encoding="utf-8")
    (DOCS_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "assets" / "extra.css").write_text(EXTRA_CSS, encoding="utf-8")
    welcome = WELCOME_TEMPLATE.format(part_table=build_part_table(index, part_titles))
    (DOCS_DIR / "index.md").write_text(welcome, encoding="utf-8")
    (DOCS_DIR / "search.md").write_text(SEARCH_PAGE, encoding="utf-8")
    print(f"[nav] 章 {len(index)} · part {len(part_titles)}")
    print(f"[nav] 写 {SITE_DIR / 'mkdocs.yml'}")
    print(f"[nav] 写 {DOCS_DIR / 'index.md'}")
    print(f"[nav] 写 {DOCS_DIR / 'search.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
