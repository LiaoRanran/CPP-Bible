#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rewrite_links.py — 发布管线跨章链接重写器（站点 / PDF 共用）

背景
====
全书 147 章正文中的跨章引用绝大多数是**裸文本** `⟶ Book/partXX/chYY.md`
（并非 markdown `[text](url)` 语法），共 ~2830 处 / 439 文件。这类裸路径在
MkDocs 站点与 pandoc PDF 中都**不会**渲染为可点击链接，且相对路径基准也不对。
本脚本在发布时把它们重写为正确的、可点击的链接——**只写临时构建区，绝不改源**。

两种模式
========
1. site：将源树复制到 build/site/docs/，并把每处 `Book/partXX/chYY.md`
   重写为相对当前文件位置的 `.md` 链接（MkDocs 会转成页内跳转）。
   - 裸引用          `Book/..chYY.md`     → `[章短标题](相对路径)`
   - markdown 链接内 `](Book/..chYY.md)`  → `](相对路径)`
   - 反引号内        `` `Book/..chYY.md` `` → `` `相对路径` ``（保持 code 样式）
2. pdf：为「全书合并单文件」重写，把跨章引用指向书内锚点 `#chYY-slug`
   （pandoc `-N --toc` 下每章 H1 生成可跳转 id）。裸引用转 `[章短标题](#anchor)`。

设计约束（对齐 AGENT.md 红线）
==============================
- 不改源：所有输出落 build/，源文件只读。
- 幂等：可反复运行，结果稳定。
- 零内容注水：只重写链接，不增删正文语义。
- 可维护：章索引与相对路径计算集中在此，nav / pdf 生成器复用。

用法
====
  python tools/rewrite_links.py --mode site   # 生成 build/site/docs/
  python tools/rewrite_links.py --mode pdf    # 生成 build/pdf/combined_src/
"""
from __future__ import annotations
import argparse
import json
import posixpath
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 项目根 CPP-Bible/
BOOK = ROOT / "Book"

# 匹配一处跨章引用：可选前导 "](" 或反引号，路径主体，可选 #锚点，条件闭合。
# 用 conditional group 一次性区分三种上下文。
# 路径两种形态：
#   A) `Book/partNN/chNN.md`   —— 带 Book/ 前缀（裸文本 ⟶、markdown 链接、反引号皆可）
#   B) `partNN/chNN.md`        —— 相对 Book 根、无前缀（仅出现在已有的 `](...)` 链接内，
#      共 1461 处 / 399 文件；正文散落的裸 partNN/chNN.md 不予匹配，见 repl 中的守卫）
CHREF_RE = re.compile(
    r"(?P<mdlink>\]\()?"                                      # markdown 链接前缀 ](
    r"(?P<btick>`)?"                                          # 反引号前缀
    r"(?P<path>(?:Book/)?part\d+[A-Za-z0-9_]*/ch\d+[A-Za-z0-9_]*\.md)"  # 书内路径(Book/可选)
    r"(?P<anchor>#[-\w]+)?"                                   # 可选锚点
    r"(?(btick)`)"                                            # 若有反引号则闭合
    r"(?(mdlink)\))"                                          # 若有 ]( 则闭合 )
)

CHNUM_RE = re.compile(r"/ch(\d+)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

# 书内对仓库根级外部目录的链接：形如 `](../../docs/compiler-matrix.md)` 或
# `](../../Appendix/ub/README.md#anchor)`。从 `Book/partNN/chYY.md` 起算，`../../`
# 解析到仓库根，故目标的顶层目录（docs / Appendix）即被引用的外部根。
# run_site 把整个外部根目录复制进 mkdocs 文档树，使其内部 .md 互相链接可解析。
EXT_ASSET_RE = re.compile(r"\]\((\.\./\.\./([^\s)]+))\)")


def build_chapter_index() -> dict:
    """扫 Book/part*/ch*.md → {book_relpath: {num,title,part,slug}}。

    book_relpath 形如 'Book/part07_stl/ch77_vector.md'（posix 风格）。
    title 取文件首个 H1；slug 为 PDF 锚点用（ch<NN>）。
    """
    index = {}
    for md in sorted(BOOK.rglob("ch*.md")):
        if "_legacy" in md.as_posix() or md.name.endswith(".bak"):
            continue
        rel = md.relative_to(ROOT).as_posix()
        m = CHNUM_RE.search(rel)
        if not m:
            continue
        num = int(m.group(1))
        text = md.read_text(encoding="utf-8", errors="replace")
        h1 = H1_RE.search(text)
        title = h1.group(1).strip() if h1 else md.stem
        # 压缩过长标题，nav / 链接文字用
        short = title
        index[rel] = {
            "num": num,
            "title": title,
            "short": short,
            "part": md.parent.name,
            "slug": f"ch{num}",
            "path": rel,
            "name": md.name,
        }
    return index


def collect_external_roots(index: dict) -> list:
    """扫描所有章正文，收集被 `](../../TOPDIR/...)` 引用的仓库根级目录名（去重、排序）。

    如某章链接 `../../docs/compiler-matrix.md` 或 `../../Appendix/ub/README.md#x`，
    则 roots = ['Appendix', 'docs']。这些目录需整目录复制进 mkdocs 文档树，其内部
    所有 .md 互相链接才能解析，且每个 .md 须出现在 nav（strict 模式要求）。
    """
    roots = set()
    for src_rel in index:
        src = ROOT / src_rel
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        for m in EXT_ASSET_RE.finditer(text):
            top = m.group(2).split("#")[0].split("/")[0]   # 去锚点 → 取顶层目录
            roots.add(top)
    return sorted(roots)


def _short_link_text(meta: dict) -> str:
    """裸引用转链接时的锚文本：保留原有信息量，避免注水。"""
    return meta["title"]


def rewrite_content(content: str, src_book_rel: str, index: dict, mode: str) -> tuple[str, int]:
    """重写单文件正文中的所有跨章引用。

    src_book_rel: 源文件在项目内的 posix 相对路径（如 'Book/part01_history/ch01_c_history.md'
                  或根级 'CROSSREF.md'）。用于计算相对路径基准目录。
    返回 (新内容, 重写计数)。
    """
    src_dir = posixpath.dirname(src_book_rel)  # 目录基准
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        raw = m.group("path")                  # 形态 A: Book/partPP/chQQ.md；形态 B: partPP/chQQ.md
        anchor = m.group("anchor") or ""
        if raw.startswith("Book/"):
            target = raw
        else:
            # 无 Book/ 前缀（相对 Book 根）：仅在 markdown 链接 `](...)` 上下文内才算跨章引用，
            # 否则可能是正文里无关的 partNN/chNN.md 文本，原样保留（不臆造）。
            if not m.group("mdlink"):
                return m.group(0)
            target = "Book/" + raw
        meta = index.get(target)
        if meta is None:
            return m.group(0)                  # 未知目标，原样保留（不臆造）
        count += 1
        if mode == "pdf":
            # 合并单文件：一律指向书内锚点
            link = f"#{meta['slug']}"
            if m.group("mdlink"):
                return f"]({link})"
            if m.group("btick"):
                return f"`{link}`"
            return f"[{_short_link_text(meta)}]({link})"
        # site 模式：相对路径
        rel = posixpath.relpath(target, src_dir if src_dir else ".")
        rel = rel + anchor
        if m.group("mdlink"):
            return f"]({rel})"
        if m.group("btick"):
            return f"`{rel}`"
        return f"[{_short_link_text(meta)}]({rel})"

    new = CHREF_RE.sub(repl, content)
    return new, count


def run_site(index: dict) -> None:
    out_docs = ROOT / "build" / "site" / "docs"
    if out_docs.exists():
        shutil.rmtree(out_docs)
    (out_docs / "Book").mkdir(parents=True, exist_ok=True)

    total_files = 0
    total_rw = 0
    # 1) 章文件
    for src_rel, meta in index.items():
        src = ROOT / src_rel
        content = src.read_text(encoding="utf-8", errors="replace")
        new, n = rewrite_content(content, src_rel, index, mode="site")
        dst = out_docs / src_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(new, encoding="utf-8")
        total_files += 1
        total_rw += n
    # 2) 根级导航件 CROSSREF.md（若存在）
    for extra in ("CROSSREF.md",):
        p = ROOT / extra
        if p.exists():
            content = p.read_text(encoding="utf-8", errors="replace")
            new, n = rewrite_content(content, extra, index, mode="site")
            (out_docs / extra).write_text(new, encoding="utf-8")
            total_files += 1
            total_rw += n
    # 3) 外部资产根目录（docs/、Appendix/ 等被书内链接引用的仓库根级目录）
    #    整目录复制进 mkdocs 文档树对应位置，使其内部所有 .md 互相链接可解析；
    #    并写 manifest（含各 .md 的首个 H1 标题）供 nav 生成器收录（strict 模式
    #    要求所有文档文件出现在 nav，否则报 not-in-nav 警告）。
    roots = collect_external_roots(index)
    manifest = []
    for root in roots:
        src_root = ROOT / root
        if not src_root.is_dir():
            continue
        dst_root = out_docs / root
        if dst_root.exists():
            shutil.rmtree(dst_root)
        shutil.copytree(src_root, dst_root)
        for md in sorted(dst_root.rglob("*.md")):
            rel = md.relative_to(out_docs).as_posix()
            t = md.read_text(encoding="utf-8", errors="replace")
            h1 = H1_RE.search(t)
            title = h1.group(1).strip() if h1 else rel
            manifest.append({"path": rel, "title": title})
    (ROOT / "build" / "site" / "external_assets.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    total_files += len(manifest)
    print(f"[site] 输出 {out_docs}")
    print(f"[site] 文件 {total_files} · 重写引用 {total_rw} · 外部根 {roots} · 外部md {len(manifest)}")


def inject_chapter_anchor(content: str, slug: str) -> tuple[str, int]:
    """给章节首个 H1 显式注入 pandoc 显式 id {#slug}。

    pandoc 默认按标题文本（含中文/全角空格/冒号）自动生成 id，既不可预测
    也可能与我们的 `#chNN` 跨章链接不匹配；显式标注后 pandoc 输出
    `<h1 id="chNN">`，`#chNN` 链接即可在 PDF（单卷）与 EPUB（章节拆分后
    pandoc 自动改写为跨文件链接）中正确跳转。

    返回 (新内容, 注入次数 0/1)。已含 `{#slug}` 则跳过（幂等）。
    """
    if f"{{#{slug}}}" in content:
        return content, 0
    new, subs = re.subn(
        r"^(#\s+.+?)\s*$",
        lambda mm: f"{mm.group(1)} {{#{slug}}}",
        content, count=1, flags=re.MULTILINE,
    )
    return new, subs


def run_pdf(index: dict) -> None:
    out_dir = ROOT / "build" / "pdf" / "combined_src"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ordered = sorted(index.values(), key=lambda m: m["num"])
    parts = []
    total_rw = 0
    anchored = 0
    for meta in ordered:
        src = ROOT / meta["path"]
        content = src.read_text(encoding="utf-8", errors="replace")
        new, n = rewrite_content(content, meta["path"], index, mode="pdf")
        total_rw += n
        # 给每章首个 H1 显式注入 pandoc id {#chNN}，使 #chNN 锚点可跳转。
        new, subs = inject_chapter_anchor(new, meta["slug"])
        anchored += subs
        parts.append(new)
    combined = "\n\n\\newpage\n\n".join(parts)
    (out_dir / "combined.md").write_text(combined, encoding="utf-8")
    print(f"[pdf] 输出 {out_dir / 'combined.md'}")
    print(f"[pdf] 章 {len(ordered)} · 重写引用 {total_rw} · 注入 H1 锚点 {anchored}")


def main() -> int:
    ap = argparse.ArgumentParser(description="发布管线跨章链接重写器")
    ap.add_argument("--mode", choices=["site", "pdf"], required=True)
    args = ap.parse_args()
    index = build_chapter_index()
    if not index:
        print("ERROR: 未发现章文件", file=sys.stderr)
        return 1
    print(f"[index] 章索引 {len(index)} 条")
    if args.mode == "site":
        run_site(index)
    else:
        run_pdf(index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
