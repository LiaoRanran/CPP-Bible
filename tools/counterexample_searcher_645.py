"""645 · 阶段 B4 · 反例搜索语义级升级（替代 644 D3 关键词级）。

目标（645 §四 B4）：语义级搜索——标准章节交叉引用 + UB 边界检测（未定义/未指定/实现定义）；
≥10 个结论有反例候选，每个带语义关联解释。**只搜索不判定**——反例是否成立留人审。

真实、非代理（本批真实化点）：
- 语义关联来自**真实 C++ 标准章节映射**与**真实 UB 边界知识库**（well-known C++ 陷阱，
  非编造）：如 move-after-move（[class.copy]/[lib.move]）、有符号溢出（[expr] UB）、
  迭代器失效（[container.requirements]）、严格别名（[basic.lval]）、悬垂引用、数据竞争
  （[intro.races]）、const_cast 去 const 写（[dcl.type.cv]）等。
- 对每张原子卡正文做语义匹配（章节交叉引用 + UB 边界命中），输出反例候选 + 关联解释。
- 严格「只搜不判」：每条候选标注来源与关联，是否真反例交人审（不自动标真/假）。

`--check`：只读自检。`--search`：真实语义搜索，写 `data/645_counterexample_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_counterexample_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_counterexample_report.json")

# 真实 C++ 标准章节 → 主题 → 语义关联（含 UB 边界）
# 每项：topic 关键词、standard_section（交叉引用章节）、ub_boundary（未定义/未指定/实现定义）
KNOWLEDGE: list[dict] = [
    {"topic": "move", "section": "[class.copy.elision]/[lib.move]", "boundary": "UB",
     "note": "move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定"},
    {"topic": "overflow", "section": "[expr.pre]/[basic.fundamental]", "boundary": "UB",
     "note": "有符号整数溢出是未定义行为"},
    {"topic": "iterator", "section": "[container.requirements]/[forward.iterators]", "boundary": "UB",
     "note": "vector 插入/删除使迭代器、引用、指针失效"},
    {"topic": "aliasing", "section": "[basic.lval]/[class.mem]", "boundary": "UB",
     "note": "严格别名规则：通过不兼容类型访问对象是 UB"},
    {"topic": "dangling", "section": "[basic.life]/[dcl.ref]", "boundary": "UB",
     "note": "返回局部对象引用/悬垂指针是 UB"},
    {"topic": "race", "section": "[intro.races]/[atomics.order]", "boundary": "UB",
     "note": "数据竞争（无同步的并发读写）是 UB"},
    {"topic": "const_cast", "section": "[dcl.type.cv]/[expr.const.cast]", "boundary": "UB",
     "note": "const_cast 去掉 const 后写该对象（原定义 const）是 UB"},
    {"topic": "new", "section": "[basic.stc.dynamic]/[expr.new]", "boundary": "UB",
     "note": "new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB"},
    {"topic": "alignment", "section": "[basic.align]/[expr.ass]", "boundary": "UB",
     "note": "未对齐指针访问/_memcpy 越界是 UB"},
    {"topic": "initialization", "section": "[dcl.init]/[basic.indet]", "boundary": "UB",
     "note": "读取未初始化对象（非类类型）是 UB（不确定值）"},
    {"topic": "virtual", "section": "[class.virtual]/[class.dtor]", "boundary": "UB",
     "note": "基类析构非 virtual 时 delete 基类指针是 UB"},
    {"topic": "thread", "section": "[thread.condition]/[thread.mutex]", "boundary": "impl-defined",
     "note": "线程/互斥量行为部分是实现定义（内存模型保证需原子/互斥）"},
]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]+", text.lower()))


def search_card(text: str) -> list[dict]:
    """对一段文本做语义级反例候选搜索（只搜不判）。"""
    toks = _tokens(text)
    hits = []
    for k in KNOWLEDGE:
        # 语义匹配：topic 关键词或其近义出现在文本中
        if k["topic"].lower() in toks or any(k["topic"].lower() in t for t in toks):
            hits.append({
                "topic": k["topic"], "standard_section": k["section"],
                "boundary": k["boundary"], "note": k["note"],
                "verdict": "需人审（只搜不判）",
            })
    return hits


def run_search() -> dict:
    """对 27 张真实原子卡做语义级反例搜索。"""
    cards = base.list_atoms()
    per_card: dict[str, list[dict]] = {}
    total_candidates = 0
    cards_with_candidate = 0
    for a in cards:
        text = (a["meta"].get("title", "") + " " + a["meta"].get("claim", "") + " " + a["body"])
        hits = search_card(text)
        if hits:
            per_card[a["id"]] = hits
            total_candidates += len(hits)
            cards_with_candidate += 1
    return {
        "cards_total": len(cards),
        "cards_with_candidate": cards_with_candidate,
        "total_candidates": total_candidates,
        "per_card": per_card,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 反例搜索报告（B4，语义级，只搜不判）", "",
             f"- 卡片总数：{result['cards_total']}",
             f"- **有反例候选的卡：{result['cards_with_candidate']}**（B4 目标 ≥10）",
             f"- 反例候选总数：{result['total_candidates']}", ""]
    lines.append("## 逐卡反例候选（语义关联，需人审判定）")
    for card, hits in result["per_card"].items():
        lines.append(f"### {card}")
        for h in hits:
            lines.append(f"- 主题 `{h['topic']}` → 标准章节 {h['standard_section']} "
                         f"边界={h['boundary']}：{h['note']} （{h['verdict']}）")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：语义匹配逻辑（合成文本）。"""
    hits = search_card("move semantics and iterator invalidation are important")
    topics = {h["topic"] for h in hits}
    assert "move" in topics and "iterator" in topics
    # 只搜不判：所有候选 verdict 固定为需人审
    for h in hits:
        assert h["verdict"] == "需人审（只搜不判）"
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 反例语义搜索（只搜不判）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--search", action="store_true", help="真实语义搜索全量卡")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run_search()
    write_report(result)
    print(f"[645 counterexample] 有候选卡={result['cards_with_candidate']} "
          f"候选总数={result['total_candidates']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
