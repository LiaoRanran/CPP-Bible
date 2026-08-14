#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CROSSREF.md 生成器
==================
从 Book/ 下全部 ch*.md 抽取交叉引用，生成一份根级全局章节依赖索引
CROSSREF.md，用于速查：

  - 每章的出链（本章指向哪些章）与入链（哪些章指向本章 = 反向依赖）
  - 策展学习路径：内联元数据行 `前置：/后续：`（39 章），含区间/斜杠列表展开
  - Part 总览、枢纽章节 Top10、孤立章节、断链报告

数据来源（与 crossref_audit.py 同口径，但输出的是"依赖图"而非"覆盖率审计"）：
  1. 箭头链接 ：(?:⟶|→)\\s*`?Book/...chYY_name.md`?   （尾部反引号已清洗）
  2. 反引号链接： `Book/...chYY_name.md`
  3. 内联元数据： > ...｜前置：ch01–ch03｜后续：ch21/22/...｜难度：★

依赖边的"章目标"判定：路径须匹配 ch\\d+_.*\\.md$（忽略 AGENT.md / tools / 非章文件）。

输出契约：
  - 落点为仓库根的 CROSSREF.md（非 ch*.md，不计入一致性门禁）
  - 幂等：重跑即整体重写，不增量追加
  - 纯派生数据，禁止人工手改（顶部已注明）

用法:
    python tools/gen_crossref.py
    python tools/gen_crossref.py --root /path/to/CPP-Bible
"""

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ---- 正则 ----
ARROW_RE = re.compile(r"(?:⟶|→)\s*`?(Book/[^\s\)\]>。，；：、》）(（`]+)")
BACKTICK_RE = re.compile(r"`(Book/[A-Za-z0-9_/.\-]+\.md)`")
META_LINE_RE = re.compile(r"^\s*>\s*.*?(前置[:：]).*?(后续[:：]).*?$", re.S)
PRE_SEG_RE = re.compile(r"前置[:：]\s*([^｜|]+)")
POST_SEG_RE = re.compile(r"后续[:：]\s*([^｜|]+)")
CHCODE_RE = re.compile(r"ch(\d+)")
CHRANGE_RE = re.compile(r"ch(\d+)\s*[–\-]\s*ch(\d+)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$")
LEAD_CH_RE = re.compile(r"^第\d+章[　\s]*")  # 去掉 H1 前缀"第01章　"

CHAPTER_FILE_RE = re.compile(r"ch\d+_.*\.md$", re.I)


def find_book_root(explicit=None):
    if explicit:
        return Path(explicit).resolve()
    here = Path(__file__).resolve().parent
    for p in (here.parent, here):
        if (p / "Book").is_dir():
            return p
    return here.parent


def chapter_num(path: Path) -> int:
    m = re.match(r"ch(\d+)", path.stem)
    return int(m.group(1)) if m else 0


def clean_title(h1: str) -> str:
    t = h1.strip()
    t = LEAD_CH_RE.sub("", t)
    t = t.replace("　", " ").strip()
    return t or "（无标题）"


def resolve_targets_from_text(text: str) -> set:
    """返回本章指向的章文件路径集合（绝对于 Book 根的 posix 形式）。"""
    out = set()
    # 箭头：清洗尾部反引号
    for raw in ARROW_RE.findall(text):
        tg = raw.strip().strip("`").replace("\\", "/")
        if CHAPTER_FILE_RE.search(tg):
            out.add(tg)
    # 反引号
    for raw in BACKTICK_RE.findall(text):
        tg = raw.strip().replace("\\", "/")
        if CHAPTER_FILE_RE.search(tg):
            out.add(tg)
    return out


def parse_meta_codes(seg: str):
    """从 `前置/后续` 片段抽取章号集合。

    支持的写法：
      - 单章   ：ch02、ch19、ch50
      - 区间   ：ch01–ch03  → ch01,ch02,ch03
      - 斜杠列表：ch21/22/27/31  → ch21,ch22,ch27,ch31（仅首个带 ch 前缀，其余为续号）
    忽略「等…」「无」等描述性文字。
    """
    codes = set()
    if not seg:
        return codes
    s = seg.strip()
    if s in ("无", "None", "none", "—", "-", "无（"):
        return codes
    # 先展开区间 chA–chB → "chA chA+1 ... chB"
    def repl(m):
        a, b = int(m.group(1)), int(m.group(2))
        lo, hi = min(a, b), max(a, b)
        return " ".join(f"ch{n}" for n in range(lo, hi + 1))

    s2 = CHRANGE_RE.sub(repl, s)
    # 章号 token：chNN 或 /NN（斜杠续号，ch 前缀可选）
    TOKEN_RE = re.compile(r"ch(\d+)|/(?:ch)?(\d+)")
    for m in TOKEN_RE.finditer(s2):
        if m.group(1):
            codes.add(int(m.group(1)))
        elif m.group(2):
            codes.add(int(m.group(2)))
    return codes


def parse_meta(text: str):
    """抽取内联元数据行的策展前置/后续章号集合。返回 (pre:set, post:set) 或 (None,None)。"""
    pre = set()
    post = set()
    found = False
    for line in text.splitlines():
        if "前置" not in line and "后续" not in line:
            continue
        if not line.lstrip().startswith(">"):
            continue
        mpre = PRE_SEG_RE.search(line)
        mpost = POST_SEG_RE.search(line)
        if not (mpre or mpost):
            continue
        found = True
        if mpre:
            pre |= parse_meta_codes(mpre.group(1))
        if mpost:
            post |= parse_meta_codes(mpost.group(1))
    if not found:
        return None, None
    return pre, post


def build(root: Path):
    book = root / "Book"
    files = sorted(
        (p for p in book.rglob("ch*.md") if not p.name.endswith(".bak")),
        key=chapter_num,
    )

    # 章号 -> (path, title, part, short)
    info = {}
    # 出链: short -> set(short)
    out_edges = defaultdict(set)
    # 策展
    curated_pre = {}
    curated_post = {}

    # 已知章号集合（用于断链判定）
    known_nums = {chapter_num(p) for p in files}

    for p in files:
        num = chapter_num(p)
        text = p.read_text(encoding="utf-8")
        title = "（无标题）"
        for ln in text.splitlines():
            if ln.startswith("# "):
                title = clean_title(ln[2:])
                break
        part = p.parent.name
        short = f"ch{num:02d}"
        info[num] = {
            "num": num,
            "path": p.relative_to(root).as_posix(),
            "title": title,
            "part": part,
            "short": short,
        }

        # 出链
        targets = resolve_targets_from_text(text)
        for tg in targets:
            # 取文件名章号
            fn = tg.split("/")[-1]
            m = re.match(r"ch(\d+)", fn)
            if m:
                tnum = int(m.group(1))
                if tnum != num and tnum in known_nums:
                    out_edges[num].add(tnum)

        # 策展
        pre, post = parse_meta(text)
        if pre is not None:
            curated_pre[num] = pre
            curated_post[num] = post

    # 入链（反向） + 断链
    in_edges = defaultdict(set)
    broken = []
    for src, dsts in out_edges.items():
        for d in dsts:
            if d not in known_nums:
                broken.append((info[src]["short"], f"ch{d:02d}"))
            else:
                in_edges[d].add(src)

    return info, out_edges, in_edges, curated_pre, curated_post, broken, sorted(known_nums)


def fmt_link(info, num) -> str:
    c = info[num]
    return f"[ch{num:02d} {c['title']}]({c['path']})"


def generate(root: Path) -> str:
    info, out_edges, in_edges, curated_pre, curated_post, broken, nums = build(root)

    parts = []
    seen = []
    for n in nums:
        pt = info[n]["part"]
        if not seen or seen[-1] != pt:
            seen.append(pt)
        parts = seen

    # Part 总览
    part_map = defaultdict(list)
    for n in nums:
        part_map[info[n]["part"]].append(n)
    part_overview = []
    for pt in sorted(part_map):
        chs = part_map[pt]
        lo, hi = chs[0], chs[-1]
        part_overview.append(
            f"| `{pt}` | {len(chs)} | ch{lo:02d}–ch{hi:02d} |"
        )

    # 枢纽 Top10（按入链数）
    hub = sorted(nums, key=lambda n: len(in_edges[n]), reverse=True)[:10]
    hub_rows = []
    for n in hub:
        ins = in_edges[n]
        hub_rows.append(
            f"| [ch{n:02d}]({info[n]['path']}) {info[n]['title']} | {len(ins)} | {len(out_edges[n])} |"
        )

    # 孤立章节（出链=0 且 入链=0）
    isolated = [n for n in nums if not out_edges[n] and not in_edges[n]]

    # 统计
    total_edges = sum(len(v) for v in out_edges.values())
    ch_with_out = sum(1 for n in nums if out_edges[n])
    ch_with_in = sum(1 for n in nums if in_edges[n])
    ch_with_curated = sum(1 for n in nums if n in curated_pre)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    L = []
    L.append("# CROSSREF.md — 《现代 C++ 终极圣经》全局章节依赖索引\n")
    L.append(f"> **自动生成文档 · {now} · 禁止手改**\n")
    L.append(
        "本文件由 `tools/gen_crossref.py` 从各章内嵌交叉引用抽取生成，"
        "是独立于正文的**导航/速查件**（非 `chXXX.md`，不计入一致性门禁）。"
        "重生成命令：\n"
    )
    L.append("```bash\npython tools/gen_crossref.py\n```\n")
    L.append("## 0. 速读说明\n")
    L.append(f"- **章节总数**：{len(nums)}")
    L.append(f"- **依赖边总数**（出链去重后）：{total_edges}")
    L.append(f"- **有出链的章**：{ch_with_out} ｜ **有入链的章**：{ch_with_in}")
    L.append(f"- **含策展 `前置/后续` 字段的章**：{ch_with_curated}")
    L.append(f"- **断链**：{len(broken)}（应为 0）")
    L.append("")
    L.append("**三类引用来源**：")
    L.append("1. 箭头链接 `⟶ Book/...chYY.md`（145 章）")
    L.append("2. 反引号链接 `` `Book/...chYY.md` ``（44 章）")
    L.append("3. 策展元数据 `> ...｜前置：…｜后续：…｜`（39 章，权威学习路径）")
    L.append("")
    L.append("**出链** = 本章主动指向的章；**入链** = 指向本章的章（即「本章是哪些章的前置」）。")
    L.append("")
    L.append("## 1. Part 总览\n")
    L.append("| Part | 章数 | 章节范围 |")
    L.append("|---|---|---|")
    L.extend(part_overview)
    L.append("")
    L.append("## 2. 全局依赖速查主表\n")
    L.append("> 行序按章号。点击 `chXX 标题` 直达正文；`出链/入链` 为该章依赖边数。\n")
    L.append("| 章 | 标题 | Part | 出链 | 入链 | 策展前置 | 策展后续 |")
    L.append("|---|---|---|---:|---:|---|---|")
    for n in nums:
        c = info[n]
        pre = (
            "、".join(f"ch{x:02d}" for x in sorted(curated_pre[n]))
            if n in curated_pre and curated_pre[n]
            else "—"
        )
        post = (
            "、".join(f"ch{x:02d}" for x in sorted(curated_post[n]))
            if n in curated_post and curated_post[n]
            else "—"
        )
        L.append(
            f"| [ch{n:02d}]({c['path']}) | {c['title']} | `{c['part']}` | "
            f"{len(out_edges[n])} | {len(in_edges[n])} | {pre} | {post} |"
        )
    L.append("")
    L.append("## 3. 依赖明细（出链 / 入链 / 策展路径）\n")
    L.append("> 每章一个小节；`出链` 为本章指向，`入链` 为指向本章（反向依赖）。\n")
    for n in nums:
        c = info[n]
        L.append(f"### ch{n:02d} · {c['title']}\n")
        L.append(f"- 文件：`{c['path']}` ｜ Part：`{c['part']}`")
        # 出链
        outs = sorted(out_edges[n])
        if outs:
            L.append("- **出链**（本章指向）：")
            L.append("  " + "、".join(fmt_link(info, x) for x in outs))
        else:
            L.append("- **出链**：无")
        # 入链
        ins = sorted(in_edges[n])
        if ins:
            L.append("- **入链**（指向本章）：")
            L.append("  " + "、".join(fmt_link(info, x) for x in ins))
        else:
            L.append("- **入链**：无")
        # 策展
        if n in curated_pre or n in curated_post:
            pre = sorted(curated_pre.get(n, set()))
            post = sorted(curated_post.get(n, set()))
            L.append(
                "- **策展路径**：前置 "
                + ("、".join(f"ch{x:02d}" for x in pre) if pre else "无")
                + " ｜ 后续 "
                + ("、".join(f"ch{x:02d}" for x in post) if post else "无")
            )
        L.append("")

    L.append("## 4. 枢纽章节 Top10（按入链数）\n")
    L.append("> 入链越高，越多章节以它为前置——优先掌握这些「地基章」。\n")
    L.append("| 章节 | 入链数 | 出链数 |")
    L.append("|---|---:|---:|")
    L.extend(hub_rows)
    L.append("")
    L.append("## 5. 孤立章节与断链\n")
    if isolated:
        L.append(f"- **孤立章节**（出链=0 且 入链=0）：" + "、".join(f"ch{n:02d}" for n in isolated))
    else:
        L.append("- **孤立章节**：无（每章至少在一侧有连接）")
    L.append("")
    if broken:
        L.append(f"- **断链**（{len(broken)} 条，需修复）：")
        for src, tgt in broken:
            L.append(f"  - `{src}` → `{tgt}`（目标章不存在）")
    else:
        L.append("- **断链**：0（全部交叉引用目标均存在）")
    L.append("")

    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="生成 CROSSREF.md 全局依赖索引")
    ap.add_argument("--root", default=None, help="CPP-Bible 根目录（默认自动探测）")
    args = ap.parse_args()

    root = find_book_root(args.root)
    out_path = root / "CROSSREF.md"

    md = generate(root)
    out_path.write_text(md, encoding="utf-8")

    info, out_edges, in_edges, curated_pre, curated_post, broken, nums = build(root)
    total_edges = sum(len(v) for v in out_edges.values())
    print(f"[*] 根目录     : {root}")
    print(f"[*] 输出       : {out_path}")
    print(f"[*] 章节数     : {len(nums)}")
    print(f"[*] 依赖边数   : {total_edges}")
    print(f"[*] 策展字段章 : {sum(1 for n in nums if n in curated_pre)}")
    print(f"[*] 断链       : {len(broken)}")
    print(f"[*] 文件大小   : {out_path.stat().st_size} B")


if __name__ == "__main__":
    main()
