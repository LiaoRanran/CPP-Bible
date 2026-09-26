"""644 阶段 D · D3 反例搜索器（原型级，§十二.3 只搜不判）。

功能：对给定结论，搜索反例候选：
- 标准中有没有例外条款？
- 编译器有没有已知 bug？
- 有没有 UB 边界情况？

策略：关键词组合 + 标准章节交叉引用，命中内置「已知例外/UB 知识库」（离线、可复核）。
**不自动判定反例是否成立**——只搜索，判定留人审。

只读：不修改受控目录。`--check` 只读幂等；`--search <conclusion>` 搜索。
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base  # noqa: F401  (used by write_report_all)


def write_report_all() -> str:
    """对全库卡片标题跑反例覆盖扫描，写覆盖报告（只读）。"""
    rows = []
    covered = 0
    for a in base.list_atoms():
        title = str(a["meta"].get("title", a["id"]))
        hits = search(title)
        if hits:
            covered += 1
        rows.append((a["id"], title, len(hits)))
    total = len(rows)
    lines = ["# 644 D3 · 反例覆盖扫描报告", "",
             f"- 卡片总数：**{total}**  命中反例候选：**{covered}**  覆盖率：**{covered/total:.0%}**", "",
             "| 卡片 | 标题 | 候选数 |", "|---|---|---|"]
    for cid, title, n in rows:
        lines.append(f"| {cid} | {title} | {n} |")
    lines.append("")
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD

OUT_MD = os.path.join(base.ROOT, "data", "644_counterexample_report.md")

#: 内置「已知例外 / UB」知识库（离线、带来源；原型级，可人审扩充）。
KNOWN_EXCEPTIONS: list[dict[str, Any]] = [
    {"keywords": ["signed", "overflow", "有符号", "溢出"], "statement": "有符号整数溢出是未定义行为(UB)，不可假设回绕",
     "source": "ISO C++ [expr] / cppreference (Undefined behavior)", "credibility": 0.9},
    {"keywords": ["vector", "push_back", "迭代器", "iterator", "失效", "invalidate"],
     "statement": "std::vector::push_back 可能引发重分配，使所有迭代器/引用失效（除非未重分配）",
     "source": "ISO C++ [vector.modifiers]", "credibility": 0.9},
    {"keywords": ["initializer_list", "推导", "deduce", "auto"], "statement": "auto x = {1,2} 推导为 std::initializer_list，而非 std::vector",
     "source": "ISO C++ [dcl.type.auto.deduct]", "credibility": 0.85},
    {"keywords": ["array", "数组", "decay", "退化", "衰减"], "statement": "数组在多数语境退化为指针，导致 sizeof 语义变化",
     "source": "ISO C++ [conv.array]", "credibility": 0.85},
    {"keywords": ["placement", "new", "launder"], "statement": "placement new 后需用 std::launder 才能合法访问对象",
     "source": "ISO C++ [ptr.launder] / WG21", "credibility": 0.85},
    {"keywords": ["null", "空指针", "dereference", "解引用"], "statement": "解引用空指针/悬垂指针是 UB",
     "source": "ISO C++ [basic.stc] / Undefined behavior", "credibility": 0.95},
    {"keywords": ["thread", "数据竞争", "data race", "race"], "statement": "无同步的并发写共享变量构成数据竞争(UB)",
     "source": "ISO C++ [intro.races]", "credibility": 0.9},
    {"keywords": ["template", "模板", "推导", "SFINAE"], "statement": "模板实参推导失败可能是 SFINAE（非错）或硬错误，边界易误判",
     "source": "ISO C++ [temp.deduct]", "credibility": 0.8},
]


def search(conclusion: str) -> list[dict[str, Any]]:
    """关键词组合搜索反例候选（离线，带来源/可信度）。"""
    text = (conclusion or "").lower()
    tokens = set(re.findall(r"[a-z一-鿿]+", text))
    hits: list[dict[str, Any]] = []
    for item in KNOWN_EXCEPTIONS:
        kws = set(item["keywords"])
        if tokens & kws:  # 关键词交集命中
            hits.append({"statement": item["statement"], "source": item["source"],
                         "credibility": item["credibility"],
                         "matched": sorted(tokens & kws)})
    # 按可信度排序
    return sorted(hits, key=lambda h: -h["credibility"])


def write_report(conclusion: str, hits: list[dict[str, Any]]) -> str:
    lines = ["# 644 D3 · 反例搜索报告", "", f"- 结论：`{conclusion}`",
             f"- 候选数：**{len(hits)}**", "", "> 仅搜索，不判定反例是否成立（判定留人审）。", "",
             "| 候选 | 来源 | 可信度 | 命中词 |", "|---|---|---|---|"]
    for h in hits:
        lines.append(f"| {h['statement']} | {h['source']} | {h['credibility']} | {','.join(h['matched'])} |")
    if not hits:
        lines.append("| 未检出反例候选 | — | — | — |")
    lines.append("")
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    # 已知有反例的结论必检出候选
    hits = search("signed integer overflow behavior")
    assert any("溢出" in h["statement"] or "overflow" in h["statement"].lower() for h in hits)
    # 无反例的结论不误报
    none = search("the sky is blue and unrelated to cpp")
    assert none == []
    # 候选带来源
    for h in search("vector push_back iterator invalidation"):
        assert h["source"] and h["credibility"] > 0
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 D3 反例搜索器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--search", metavar="CONCLUSION", help="搜索反例的结论")
    ap.add_argument("--report", action="store_true", help="对全库卡片标题跑反例覆盖扫描并写报告")
    a = ap.parse_args(argv)
    if a.search:
        hits = search(a.search)
        print(f"hits={len(hits)}")
        print(f"written {write_report(a.search, hits)}")
        return 0
    if a.report:
        print(f"written {write_report_all()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
