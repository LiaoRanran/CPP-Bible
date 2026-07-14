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
    - toc.follow
    - content.code.copy
    - content.code.annotate
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

{nav}
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
