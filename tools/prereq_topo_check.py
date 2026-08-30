#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
前置依赖拓扑校验 (T1-3)
=====================
校验各章 `前置：` 元数据声明的依赖编号是否均小于自身编号；
若存在「前置编号 > 自身编号」的倒置，即拓扑矛盾，报警。
同时检查前置编号是否落在有效编号集合（悬空前置）。

复用 gen_indexes.py 的解析约定：
    前置[：:]\s*([^｜|/]+)   抽元数据行
    ch(\d+)                   抽依赖编号

这是给 tools/gen_indexes.py 的前置依赖生成加的「校验护栏」：
原来它默默吐出一张可能自相矛盾的依赖表，现在在生成时（或单独跑本脚本）
即可报警。

用法:
    python tools/prereq_topo_check.py
    python tools/prereq_topo_check.py --json out.json
退出码: 发现倒置或悬空前置返回 1（可作 CI 门禁），否则 0。
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOK = ROOT / "Book"

PRE_RE = re.compile(r"前置[：:]\s*([^｜|/]+)")
CHNUM = re.compile(r"ch(\d+)")
SKIP_FILES = {"SUMMARY.md", "PREREQUISITES.md", "GLOSSARY.md",
              "INDEX.md", "README.md", "changelog.md"}

# 前瞻导读豁免（file, self, pre）：历史/演进导读章会"提及未来主题"作为路径预告，
# 属作者设计意图，非依赖矛盾。逐项记录依据（见 docs/references/chapter_mapping.md §3）。
# 判定优先级高于倒置/悬空检测；新增项必须带依据注释，禁止盲目扩大。
FORWARD_PRE_EXEMPT = {
    ("ch07_cpp20.md", 7, 60),   # 导读：模板基础（本章提及 ch60 模板背景）
    ("ch07_cpp20.md", 7, 63),   # 导读：变参模板（本章提及）
    ("ch09_cpp26.md", 9, 67),   # 导读：Concepts（C++26 反射基础）
    ("ch09_cpp26.md", 9, 113),  # 导读：协程（与执行器协作）
    ("ch19_variables.md", 19, 20),  # 语言章导读：引用与指针（前后衔接）
    ("ch19_variables.md", 19, 31),  # 语言章导读：const_cast（本章提及）
}


def valid_from_disk(book: Path) -> set:
    s = set()
    for p in book.rglob("ch*.md"):
        m = re.match(r"ch(\d+)_", p.name)
        if m:
            s.add(int(m.group(1)))
    return s


def main():
    ap = argparse.ArgumentParser(description="前置依赖拓扑校验 (T1-3)")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    book = Path(args.book)
    valid = valid_from_disk(book)

    inverted = []      # (file, self, pre)  pre > self
    dangling_pre = []  # (file, self, pre)  pre 不在 valid
    checked = 0

    for ch in sorted(book.rglob("ch*.md")):
        if ch.name in SKIP_FILES:
            continue
        m = re.match(r"ch(\d+)_", ch.name)
        if not m:
            continue
        self_n = int(m.group(1))
        pm = None
        for ln in ch.read_text(encoding="utf-8").splitlines():
            x = PRE_RE.search(ln)
            if x:
                pm = x.group(1)
                break
        if not pm:
            continue
        pres = sorted(set(int(x) for x in CHNUM.findall(pm)))
        checked += 1
        for c in pres:
            if c == self_n:
                continue
            # 前瞻导读白名单：命中即跳过（见 FORWARD_PRE_EXEMPT 依据）
            if (ch.name, self_n, c) in FORWARD_PRE_EXEMPT:
                continue
            if c not in valid:
                dangling_pre.append((ch.name, self_n, c))
                continue
            if c > self_n:
                inverted.append((ch.name, self_n, c))

    print(f"[*] 检查了 {checked} 章的显式前置元数据；有效编号集合大小 {len(valid)}")
    print(f"[!] 拓扑倒置（前置编号 > 自身编号）: {len(inverted)} 处")
    for f, s, c in inverted:
        print(f"    {f}: 前置 ch{c} > 自身 ch{s}")
    print(f"[!] 悬空前置（指向不存在的章节）: {len(dangling_pre)} 处")
    for f, s, c in dangling_pre:
        print(f"    {f}: 前置 ch{c} 不存在")

    if not inverted and not dangling_pre:
        print("[PASS] 无拓扑倒置、无悬空前置。")

    if args.json:
        payload = {
            "checked": checked,
            "inverted": [{"file": f, "self": s, "pre": c} for f, s, c in inverted],
            "dangling_pre": [{"file": f, "self": s, "pre": c} for f, s, c in dangling_pre],
        }
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)  # CI 干净 checkout 无 outputs/，需自建
        out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[+] JSON 写入: {args.json}")

    return 1 if (inverted or dangling_pre) else 0


if __name__ == "__main__":
    sys.exit(main())
