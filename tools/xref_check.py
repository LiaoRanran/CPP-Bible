#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPP-Bible 交叉引用门禁 (xref_check.py)
=====================================
与既有「双门禁」(compile_gate / consistency_check) 哲学一致的第三道结构性门禁。

职责（与 crossref_audit.py 互补）:
  - crossref_audit.py : 统计 ⟶ 箭头式"相关章节"引用覆盖度（part 级视角）
  - xref_check.py     : 校验所有可导航引用的完整性 + 孤儿/孤岛（章级视角）

两类引用都纳入判据（关键）:
  1. Markdown 链接  [text](Book/partXX/chNN_*.md)
  2. 箭头式相关章节  ⟶ Book/partXX/chNN_*.md — 说明   （全书主力格式）

检测:
  - 断裂链接 (BLOCK, 退出码 1) —— 指向不存在的 .md 目标
  - 孤儿章   (WARN)            —— 零入链（无人引用它）
  - 信息孤岛 (WARN)            —— 零出链（它不引用任何章）

用法:
  python3 tools/xref_check.py                 # 控制台报告；断裂则非零退出
  python3 tools/xref_check.py --json out.json # 附带写 JSON 报告
  python3 tools/xref_check.py --allow-orphans # 孤儿/孤岛仅 WARN（默认即 WARN）
"""
import os, re, sys, json, argparse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(HERE, "Book")

FENCE  = re.compile(r"^\s*```")
LINK   = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")            # [text](target)
ARROW  = re.compile(r"(?:⟶|→)\s*([^\n。]+)")               # ⟶ 后的整段引用文本
PATHTOK= re.compile(r"Book/[^\s—、,，)）]+\.md")            # 段内每个可导航路径（顿号/逗号分隔）
CHFILE = re.compile(r"ch(\d+)_")                           # 章文件名: chNN_*.md
CHBASE = re.compile(r"ch(\d+)")                            # basename 提取章号


def strip_fences(text):
    """移除代码栅栏，避免 C++ lambda `[](...)` 等被误判为链接。"""
    out, inf = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            inf = not inf
            continue
        if not inf:
            out.append(line)
    return "\n".join(out)


def is_navigable(t):
    """只有像导航目标的才算链接；排除 C++ lambda `[](auto a, auto b)` 等参数列表。"""
    if t.startswith("http") or t.startswith("mailto:") or t.startswith("#"):
        return True
    if t.startswith("./") or t.startswith("../") or t.startswith("/"):
        return True
    if "/" in t:                      # 含斜杠路径 Book/part../chX.md 等
        return True
    if t.endswith((".md", ".html", ".pdf", ".txt")):
        return True
    return False


def resolve(relpath, src):
    """返回 (候选绝对路径, 状态)。状态 = external / ok / broken。"""
    if relpath.startswith("http") or relpath.startswith("mailto:"):
        return None, "external"
    if relpath.startswith("/"):
        cand = os.path.join(HERE, relpath.lstrip("/"))
    elif relpath.startswith("Book/"):
        cand = os.path.join(HERE, relpath)
    else:
        cand = os.path.normpath(os.path.join(os.path.dirname(src), relpath))
    if cand and os.path.isfile(cand):
        return cand, "ok"
    return (cand, "broken") if cand else (None, "broken")


def collect_targets(body):
    """从正文(已去代码栅栏)收集所有引用目标 (text, target)。"""
    targets = []
    for txt, tgt in LINK.findall(body):
        t = tgt.split("#")[0].strip()
        if is_navigable(t):
            targets.append((txt, t))
    for seg in ARROW.findall(body):
        for tgt in PATHTOK.findall(seg):   # 一个箭头可含多个 Book/...md（顿号分隔）
            targets.append(("(相关章节)", tgt))
    return targets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="写 JSON 报告到指定路径")
    ap.add_argument("--allow-orphans", action="store_true",
                    help="孤儿/孤岛仅 WARN（当前默认即 WARN，不 BLOCK）")
    args = ap.parse_args()

    # 建章节表
    chapters = {}
    for part in sorted(os.listdir(BOOK)):
        pdir = os.path.join(BOOK, part)
        if not os.path.isdir(pdir) or part.startswith("_"):
            continue
        for fn in sorted(os.listdir(pdir)):
            if not fn.endswith(".md"):
                continue
            m = CHFILE.match(fn)
            if not m:
                continue
            ch = int(m.group(1))
            path = os.path.join(pdir, fn)
            title = ""
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
            chapters[ch] = {"path": path, "part": part,
                            "stem": fn[:-3], "title": title}

    inbound  = {ch: set() for ch in chapters}
    outbound = {ch: set() for ch in chapters}
    broken = []
    internal = external = 0

    for ch, meta in chapters.items():
        body = strip_fences(open(meta["path"], encoding="utf-8").read())
        for txt, t in collect_targets(body):
            cand, st = resolve(t, meta["path"])
            if st == "external":
                external += 1
            elif st == "ok":
                internal += 1
                mm = CHBASE.match(os.path.basename(cand))
                if mm:
                    tch = int(mm.group(1))
                    if tch in chapters and tch != ch:
                        inbound[tch].add(ch)
                        outbound[ch].add(tch)
            elif st == "broken":
                broken.append({"from": ch, "target": t, "text": txt})

    orphans = sorted(ch for ch in chapters if not inbound[ch])
    islands = sorted(ch for ch in chapters if not outbound[ch])

    print("=" * 58)
    print("CPP-Bible 交叉引用门禁 (xref_check)")
    print("=" * 58)
    print(f"章节总数         : {len(chapters)}")
    print(f"内部链接(正文)   : {internal}  (Markdown + ⟶ 箭头式)")
    print(f"外部链接         : {external}")
    print(f"断裂链接         : {len(broken)}")
    print(f"孤儿章(零入链)   : {len(orphans)} -> {orphans}")
    print(f"信息孤岛(零出链) : {len(islands)} -> {islands}")
    if broken:
        print("\n[FAIL] 断裂链接:")
        for b in broken:
            print(f"  ch{b['from']} -> [{b['text']}]({b['target']})")
    if orphans:
        print("\n[WARN] 孤儿章(建议在相关章增加入链):", orphans)
    if islands:
        print("\n[WARN] 信息孤岛(建议补相关章节出链):", islands)

    report = {
        "total_chapters": len(chapters),
        "internal_links": internal,
        "external_links": external,
        "broken_links": broken,
        "orphans": orphans,
        "islands": islands,
        "inbound":  {str(k): sorted(v) for k, v in inbound.items()},
        "outbound": {str(k): sorted(v) for k, v in outbound.items()},
    }
    if args.json:
        json.dump(report, open(args.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\nJSON 报告 -> {args.json}")

    if broken:
        print("\nRESULT: FAIL (存在断裂链接)")
        sys.exit(1)
    print("\nRESULT: PASS (链接完整性 OK)")
    sys.exit(0)


if __name__ == "__main__":
    main()
