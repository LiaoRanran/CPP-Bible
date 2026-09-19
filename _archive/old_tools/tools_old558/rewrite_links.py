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
# 路径形态（三选一）：
#   A) `Book/partNN/chNN.md`   —— 带 Book/ 前缀（裸文本 ⟶、markdown 链接、反引号皆可）
#   B) `partNN/chNN.md`        —— 相对 Book 根、无前缀（仅出现在已有的 `](...)` 链接内，
#      共 1461+ 处 / 399 文件；正文散落的裸 partNN/chNN.md 不予匹配，见 repl 中的守卫）
#   C) `../partNN/chNN.md`     —— 源相对（tools/fix_book_links.py 改写后的 md 链接形态；
#      标准渲染器里正确，发布时由本脚本对 PDF 归一化为 #chNN 锚点）
CHREF_RE = re.compile(
    r"(?P<mdlink>\]\()?"                                      # markdown 链接前缀 ](
    r"(?P<btick>`)?"                                          # 反引号前缀
    r"(?P<path>(?:(?:\.\./)+|Book/)?part\d+[A-Za-z0-9_]*/ch\d+[A-Za-z0-9_]*\.md)"  # 书内路径(../或Book/可选)
    r"(?P<anchor>#[-\w]+)?"                                   # 可选锚点
    r"(?(btick)`)"                                            # 若有反引号则闭合
    r"(?(mdlink)\))"                                          # 若有 ]( 则闭合 )
)

CHNUM_RE = re.compile(r"/ch(\d+)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def _gitignored_dirs(root: str) -> list[str]:
    """返回 .gitignore 中 `root/...` 形式、被整体忽略（以 / 结尾、无通配符）的子目录相对路径。

    发布管线复制外部资产根目录时须排除这些 gitignored 目录，否则本地会把 gitignored 素材
    （人文库/书籍/标准等）带进站点 nav，触发 mkdocs --strict 断链与 site_audit 假红
    （CI 上这些目录本就不存在，故仅影响本地）。
    """
    gi = ROOT / ".gitignore"
    if not gi.exists():
        return []
    prefix = root.rstrip("/") + "/"
    out: list[str] = []
    for line in gi.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if any(c in s for c in "*?["):
            continue
        if s.startswith(prefix) and s.endswith("/"):
            out.append(s[len(prefix):].rstrip("/"))
    return out
# 发布产物自检用：markdown 链接/图片 `](target)` / `![alt](target)`。
# 同时覆盖图片与内联链接（图片语法 `[alt](path)` 也会被本式匹配，无妨）。
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _clean_link_target(raw: str) -> str:
    """从 markdown 链接目标里剥离可选 title（`](path "title")`）与首尾空白。"""
    raw = raw.strip()
    if '"' in raw:
        raw = raw[: raw.index('"')].strip()
    else:
        raw = raw.split(" ")[0].strip()
    return raw


def _skip_link(tgt: str) -> bool:
    """跳过非文件系统链接：绝对 URL / 邮件 / 纯锚点。"""
    if not tgt:
        return True
    if tgt.startswith(("http://", "https://", "mailto:", "ftp://")):
        return True
    if tgt.startswith("#"):
        return True
    return False


# MkDocs 当成静态资源目录、不渲染为页面的目录名（nav 覆盖自检须排除）。
STATIC_DIRS = {"assets", "img", "images", "static", "theme",
               ".git", ".github", "__pycache__"}
DOC_EXT = (".md", ".html", ".htm", ".jpg", ".jpeg", ".png", ".gif",
           ".svg", ".pdf", ".css", ".js", ".txt")


def _is_file_link(tgt: str) -> bool:
    """目标是否像文件系统路径（含 '/' 或以文档/图片扩展名结尾）。

    C++ 代码里的 `[](auto)`, `std::tuple<T,T,T>`, `T*` 等会被 LINK_RE 误匹配，
    但它们既不是相对路径也不带扩展名，据此过滤掉，避免误报。"""
    if "/" in tgt:
        return True
    low = tgt.lower()
    return low.endswith(DOC_EXT)


def _strip_code(text: str) -> str:
    """剔除围栏代码块（``` / ~~~）与内联代码，避免 C++ 泛型 lambda `[](auto&&){}`
    或代码里的 `](` 被误判为 markdown 链接。仅对渲染后的正文做链接自检。"""
    out = []
    infence = False
    fence = ""
    for line in text.split("\n"):
        s = line.lstrip()
        if not infence:
            if s.startswith("```") or s.startswith("~~~"):
                infence = True
                fence = s[:3]
                continue
            out.append(line)
        else:
            if s.startswith(fence):
                infence = False
                fence = ""
            # 围栏内行直接丢弃
    joined = "\n".join(out)
    joined = re.sub(r"`[^`]*`", "", joined)  # 去内联代码
    return joined


def validate_site(index: dict) -> list:
    """自检 site 产物（build/site/docs）：

    1) 资产/链接存在性：所有 markdown 图片与链接目标（剥离锚点/title 后）相对
       当前 .md 解析为文件必须存在，否则 mkdocs --strict 报 broken link 中断。
    2) 导航覆盖：docs 树内每个 .md 必须落在 nav（章节 / index / search /
       CROSSREF / 外部根目录拷贝），否则 mkdocs --strict 报 not-in-nav 中断。
    返回断裂清单（空=通过）。独立于 gen_mkdocs_nav，可单独运行。
    """
    out_docs = ROOT / "build" / "site" / "docs"
    if not out_docs.exists():
        return []  # 尚未生成，跳过
    broken: list[str] = []
    # 1) 资产/链接存在性（site 模式：图片与 .md 链接缺失均会被 mkdocs --strict 判失败）
    for md in sorted(out_docs.rglob("*.md")):
        base = md.parent
        text = _strip_code(md.read_text(encoding="utf-8", errors="replace"))
        for m in LINK_RE.finditer(text):
            tgt = _clean_link_target(m.group(1))
            if _skip_link(tgt):
                continue
            pathpart = tgt.split("#")[0]
            if pathpart == "" or not _is_file_link(pathpart):
                continue  # 非文件路径（代码误匹配）→ 跳过
            p = (base / pathpart).resolve()
            if not p.exists():
                rel = md.relative_to(out_docs).as_posix()
                broken.append(f"[site] 断链 {rel}: {tgt}")
    # 2) 导航覆盖（排除 MkDocs 静态资源目录，如 Book/assets/）
    expected = {"index.md", "search.md"}
    if (out_docs / "CROSSREF.md").exists():
        expected.add("CROSSREF.md")
    for rel in index:  # 章节路径 'Book/partXX/chYY.md'
        expected.add(rel)
    roots = collect_external_roots(index)
    for root in roots:
        for emd in (out_docs / root).rglob("*.md"):
            expected.add(emd.relative_to(out_docs).as_posix())
    actual = set()
    for md in out_docs.rglob("*.md"):
        rp = md.relative_to(out_docs).as_posix()
        if any(seg in STATIC_DIRS for seg in rp.split("/")):
            continue  # 静态资源目录内的 .md 不算页面
        actual.add(rp)
    for u in sorted(actual - expected):
        broken.append(f"[site] nav 未收录(将触发 mkdocs strict not-in-nav): {u}")
    return broken


def validate_pdf() -> list:
    """自检 pdf/epub 产物（build/pdf/combined_src/combined.md）：所有 markdown
    图片与链接目标相对 combined.md 解析必须存在（否则 pandoc 报 ResourceNotFound
    致整本生成失败）。返回断裂清单（空=通过）。"""
    combined = ROOT / "build" / "pdf" / "combined_src" / "combined.md"
    if not combined.exists():
        return []
    base = combined.parent
    text = _strip_code(combined.read_text(encoding="utf-8", errors="replace"))
    broken: list[str] = []        # 致命：图片缺失（pandoc ResourceNotFound 致整本失败）
    warns: list[str] = []         # 软：.md 超链接失效（pandoc 不报错，仅生成死链）
    for m in LINK_RE.finditer(text):
        tgt = _clean_link_target(m.group(1))
        if _skip_link(tgt):
            continue
        pathpart = tgt.split("#")[0]
        if pathpart == "" or not _is_file_link(pathpart):
            continue
        is_image = m.start() > 0 and text[m.start() - 1] == "!"
        p = (base / pathpart).resolve()
        if not p.exists():
            if is_image:
                broken.append(f"[pdf] 图片缺失 combined.md: {tgt}")
            else:
                warns.append(f"[pdf][warn] 链接失效(不阻断 pandoc): {tgt}")
    if warns:
        print(f"[pdf] 自检 {len(warns)} 处失效 .md 链接（单文件 PDF 内无法跳转，仅警告）：")
        for w in warns[:10]:
            print(f"        {w}")
        if len(warns) > 10:
            print(f"        ... 共 {len(warns)} 处")
    return broken

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
    return str(meta["title"])


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
        raw = m.group("path")                  # 形态 A: Book/...；B: part...；C: ../part...
        anchor = m.group("anchor") or ""
        if raw.startswith("Book/"):
            target = raw
        elif raw.startswith("../"):
            # 源相对（fix_book_links 改写形态）：归一化回 Book 根目标
            if not m.group("mdlink"):
                return str(m.group(0))
            target = "Book/" + raw.lstrip("./")
        else:
            # 无 Book/ 前缀（相对 Book 根）：仅在 markdown 链接 `](...)` 上下文内才算跨章引用，
            # 否则可能是正文里无关的 partNN/chNN.md 文本，原样保留（不臆造）。
            if not m.group("mdlink"):
                return str(m.group(0))
            target = "Book/" + raw
        meta = index.get(target)
        if meta is None:
            return str(m.group(0))                  # 未知目标，原样保留（不臆造）
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


def run_site(index: dict) -> list:
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
    # 1.5) 章节内联资产（Book/assets/，如历史贴图 *.jpg）
    #     书内以 `../assets/history/x.jpg` 相对链接引用，解析到 docs 树内的
    #     `Book/assets/history/x.jpg`；须随章文件一同进入 docs 树，否则
    #     mkdocs --strict 把断链当错误中止构建（CI #273+ site 红的根因）。
    src_assets = ROOT / "Book" / "assets"
    if src_assets.is_dir():
        dst_assets = out_docs / "Book" / "assets"
        if dst_assets.exists():
            shutil.rmtree(dst_assets)
        shutil.copytree(src_assets, dst_assets)
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
        for gdir in _gitignored_dirs(root):
            p = dst_root / gdir
            if p.is_dir():
                shutil.rmtree(p)
        for md in sorted(dst_root.rglob("*.md")):
            rel = md.relative_to(out_docs).as_posix()
            t = md.read_text(encoding="utf-8", errors="replace")
            h1 = H1_RE.search(t)
            title = h1.group(1).strip() if h1 else rel
            manifest.append({"path": rel, "title": title})
    (ROOT / "build" / "site" / "external_assets.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    total_files += len(manifest)
    broken = validate_site(index)
    print(f"[site] 输出 {out_docs}")
    print(f"[site] 文件 {total_files} · 重写引用 {total_rw} · 外部根 {roots} · 外部md {len(manifest)}")
    if broken:
        print(f"[site] ⚠ 自检发现 {len(broken)} 处断裂（mkdocs --strict 将失败）：")
        for b in broken:
            print(f"        {b}")
    else:
        print("[site] 自检通过：无断链 / nav 全覆盖")
    return broken


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


_ADMONITION_RE = re.compile(
    r'^(\s*)(?:!!!|\?\?\?)\s+([A-Za-z0-9_-]+)(?:\s+"([^"]*)")?\s*$'
)


def _convert_admonitions(content: str) -> str:
    """把 mkdocs-material 的 `!!!`/`???` admonition 转为 pandoc fenced div `:::`
    （仅 pdf/epub 合并源调用；site 模式保留 `!!!` 由 mkdocs 原生渲染）。

    mkdocs 语法（正文缩进 4 空格，块以缩进不足为界）:
        !!! note "标题"
            正文（缩进 4 空格）
            继续正文
    pandoc fenced div 语法（不缩进，`:::` 闭合）:
        ::: {.note}
        **标题**

        正文
        :::

    幂等：只匹配行首（可带缩进）的 `!!!`/`???`，不碰已转换的 `:::`；
    正文统一去 4 空格缩进；块内空行保留；块结束补 `:::`。
    """
    lines = content.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        m = _ADMONITION_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        indent = m.group(1)
        kind = m.group(2)
        title = m.group(3)
        out.append(f"{indent}::: {{{kind}}}")
        if title:
            out.append(f"{indent}**{title}**")
        j = i + 1
        while j < n:
            ln = lines[j]
            if ln.startswith(indent + "    "):
                out.append(ln[len(indent) + 4:])
                j += 1
            elif ln.strip() == "":
                # 空行：若后续仍有缩进正文则保留该空行，否则视为块结束
                k = j
                while k < n and lines[k].strip() == "":
                    k += 1
                if k < n and lines[k].startswith(indent + "    "):
                    out.append("")
                    j = k
                else:
                    break
            else:
                break
        out.append(f"{indent}:::")
        i = j
    return "\n".join(out)


def run_pdf(index: dict) -> list:
    out_dir = ROOT / "build" / "pdf" / "combined_src"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 章节内联资产（Book/assets/，如历史贴图 *.jpg）
    # 书内以 `../assets/history/x.jpg` 相对链接引用，combined.md 位于
    # build/pdf/combined_src/，解析到 build/pdf/assets/history/x.jpg；
    # 须随 combined.md 一同进入 build/pdf/，否则 pandoc(EPUB) 与
    # xelatex(PDF) 图片断链致整本生成失败（与 run_site 同类根因）。
    src_assets = ROOT / "Book" / "assets"
    if src_assets.is_dir():
        dst_assets = ROOT / "build" / "pdf" / "assets"
        if dst_assets.exists():
            shutil.rmtree(dst_assets)
        shutil.copytree(src_assets, dst_assets)

    ordered = sorted(index.values(), key=lambda m: m["num"])
    parts = []
    total_rw = 0
    anchored = 0
    for meta in ordered:
        src = ROOT / meta["path"]
        content = src.read_text(encoding="utf-8", errors="replace")
        new, n = rewrite_content(content, meta["path"], index, mode="pdf")
        total_rw += n
        # mkdocs `!!!` admonition → pandoc `:::` fenced div（PDF/EPUB 不再字面渲染 `!!!`）
        new = _convert_admonitions(new)
        # 给每章首个 H1 显式注入 pandoc id {#chNN}，使 #chNN 锚点可跳转。
        new, subs = inject_chapter_anchor(new, meta["slug"])
        anchored += subs
        parts.append(new)
    combined = "\n\n\\newpage\n\n".join(parts)
    (out_dir / "combined.md").write_text(combined, encoding="utf-8")
    broken = validate_pdf()
    print(f"[pdf] 输出 {out_dir / 'combined.md'}")
    print(f"[pdf] 章 {len(ordered)} · 重写引用 {total_rw} · 注入 H1 锚点 {anchored}")
    if broken:
        print(f"[pdf] ⚠ 自检发现 {len(broken)} 处断裂（pandoc 将 ResourceNotFound 失败）：")
        for b in broken:
            print(f"        {b}")
    else:
        print("[pdf] 自检通过：无断链")
    return broken


def main() -> int:
    ap = argparse.ArgumentParser(description="发布管线跨章链接重写器")
    ap.add_argument("--mode", choices=["site", "pdf"], required=True)
    ap.add_argument("--check", action="store_true",
                    help="仅自检已生成的 build/ 产物（site/pdf），不重新生成；断裂则退出码 1")
    args = ap.parse_args()
    index = build_chapter_index()
    if not index:
        print("ERROR: 未发现章文件", file=sys.stderr)
        return 1
    print(f"[index] 章索引 {len(index)} 条")
    if args.check:
        broken = validate_site(index) if args.mode == "site" else validate_pdf()
        if broken:
            print(f"[check] ⚠ 发现 {len(broken)} 处断裂：")
            for b in broken:
                print(f"        {b}")
            return 1
        print("[check] 自检通过：无断链 / nav 全覆盖")
        return 0
    broken = run_site(index) if args.mode == "site" else run_pdf(index)
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
