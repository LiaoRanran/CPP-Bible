#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPP-Bible 交叉引用门禁 (xref_check.py)
=====================================
与既有「双门禁」(compile/consistency) 哲学一致，新增第三道结构性门禁：
  - 校验所有正文(非代码栅栏)内部 .md 链接可解析
  - 报告孤儿章(零入链) / 信息孤岛(零出链)
  - 可选 --json 输出供仪表盘

退出码:
  0 = 通过(可带 WARN 级提示)
  1 = 存在断裂链接(BLOCK)
  2 = 用法错误

用法:
  python3 tools/xref_check.py              # 控制台报告, 断裂则非零退出
  python3 tools/xref_check.py --json out.json
  python3 tools/xref_check.py --allow-orphans   # 孤儿/孤岛仅 WARN 不 BLOCK
"""
import os, re, sys, json, argparse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(HERE, "Book")

FENCE = re.compile(r"^\s*```")
LINK  = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
CHNUM = re.compile(r"ch(\d+)_")

def strip_fences(text):
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
    if "/" in t:                      # Book/part../chX.md 等含斜杠路径
        return True
    if t.endswith((".md", ".html", ".pdf", ".txt")):
        return True
    return False

def resolve(relpath, src):
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="写 JSON 报告到指定路径")
    ap.add_argument("--allow-orphans", action="store_true",
                    help="孤儿/孤岛仅 WARN, 不 BLOCK")
    args = ap.parse_args()

    chapters = {}
    for part in sorted(os.listdir(BOOK)):
        pdir = os.path.join(BOOK, part)
        if not os.path.isdir(pdir) or part.startswith("_"):
            continue
        for fn in sorted(os.listdir(pdir)):
            if not fn.endswith(".md"):
                continue
            m = CHNUM.match(fn)
            if not m:
                continue
            ch = int(m.group(1))
            path = os.path.join(pdir, fn)
            title = ""
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# "):
                        title = line[2:].strip(); break
            chapters[ch] = {"path": path, "part": part, "stem": fn[:-3], "title": title}

    inbound = {ch: [] for ch in chapters}
    broken = []
    internal = 0
    external = 0
    outbound = {}
    for ch, meta in chapters.items():
        body = strip_fences(open(meta["path"], encoding="utf-8").read())
        out_n = 0
        for txt, tgt in LINK.findall(body):
            t = tgt.split("#")[0].strip()
            if not is_navigable(t):
                continue   # 跳过 lambda / 函数参数列表等非链接
            cand, st = resolve(t, meta["path"])
            if st == "external":
                external += 1
            elif st == "ok":
                internal += 1
                bn = os.path.basename(cand)
                mm = CHNUM.match(bn)
                if mm:
                    tch = int(mm.group(1))
                    if tch in inbound and tch != ch:
                        inbound[tch].append(ch)
                        out_n += 1
            elif st == "broken":
                broken.append({"from": ch, "target": tgt, "text": txt})
        outbound[ch] = out_n

    orphans = [ch for ch in chapters if not inbound[ch]]
    islands = [ch for ch in chapters if outbound.get(ch, 0) == 0]

    # 报告
    print("=" * 58)
    print("CPP-Bible 交叉引用门禁")
    print("=" * 58)
    print(f"章节总数         : {len(chapters)}")
    print(f"内部链接(正文)   : {internal}")
    print(f"外部链接         : {external}")
    print(f"断裂链接         : {len(broken)}")
    print(f"孤儿章(零入链)   : {len(orphans)} -> {sorted(orphans)}")
    print(f"信息孤岛(零出链) : {len(islands)} -> {sorted(islands)}")
    if broken:
        print("\n[FAIL] 断裂链接:")
        for b in broken:
            print(f"  ch{b['from']} -> [{b['text']}]({b['target']})")
    if orphans and not args.allow_orphans:
        print("\n[WARN] 孤儿章(建议在相关章增加入链):", sorted(orphans))
    if islands and not args.allow_orphans:
        print("\n[WARN] 信息孤岛(建议补相关章节出链):", sorted(islands))

    report = {
        "total_chapters": len(chapters),
        "internal_links": internal,
        "external_links": external,
        "broken_links": broken,
        "orphans": orphans,
        "islands": islands,
        "inbound": {str(k): len(v) for k, v in inbound.items()},
        "outbound": {str(k): v for k, v in outbound.items()},
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
