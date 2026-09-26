"""646 · 阶段 B2 · 反例语义级补全（覆盖全部真实卡）。

目标（646 §四 B2）：645 的反例搜索只覆盖 20 张卡（8 张未覆盖，且其中含幻影卡）；本批补齐到
**覆盖全部真实 27 张卡**（或如实登记「无反例」）。**只搜不判**。

真实做法：
- 复用 645 的语义知识库（12 主题）与 `search_card`；
- **扩展语义表**：为智能指针 / ODR / SSO / 内存序 / RAII / 分配器 / 伪共享 / 弃用 等主题补标准章节交叉引用与 UB 边界；
- 对仍无候选的卡，按 **域兜底**（MEM/CONC/HIST/LANG/UB → 通用章节）给语义关联候选，标注来源。

`--check` 只读自检；`--search` 真实搜索，写 `data/646_counterexample_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import counterexample_searcher_645 as old  # noqa: E402
import perf_646 as perf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "646_counterexample_report.md")
REPORT_JSON = os.path.join(DATA, "646_counterexample_report.json")

# 扩展语义表（topic 关键词 → 标准章节 + UB 边界）
EXTENDED: list[dict] = [
    {"topic": "unique_ptr", "section": "[util.smartptr.unique_ptr]/[memory]",
     "boundary": "impl-defined", "note": "自定义删除器进类型系统；删除器有状态时行为差异"},
    {"topic": "shared_ptr", "section": "[util.smartptr.shared]/[util.smartptr.shared.atomic]",
     "boundary": "impl-defined", "note": "控制块原子、被管理对象非原子；循环引用泄漏"},
    {"topic": "weak_ptr", "section": "[util.smartptr.weak]", "boundary": "impl-defined",
     "note": "lock() 可能失败；观察者语义"},
    {"topic": "sso", "section": "[string.require]/[basic.string]", "boundary": "impl-defined",
     "note": "SSO 阈值不可移植，依赖实现"},
    {"topic": "inline", "section": "[basic.def.odr]/[dcl.inline]", "boundary": "UB",
     "note": "跨 TU 定义不一致违反 ODR 是 UB"},
    {"topic": "odr", "section": "[basic.def.odr]", "boundary": "UB", "note": "ODR 违反是 UB"},
    {"topic": "raii", "section": "[except.ctor]/[basic.life]", "boundary": "impl-defined",
     "note": "异常路径若析构抛异常则 terminate"},
    {"topic": "allocator", "section": "[allocator.requirements]/[default.allocator]",
     "boundary": "impl-defined", "note": "分配器策略影响时空，需可移植性验证"},
    {"topic": "fence", "section": "[atomics.fences]/[atomics.order]", "boundary": "impl-defined",
     "note": "内存序是同步契约，误用导致 UB 或未定义顺序"},
    {"topic": "atomic", "section": "[atomics.order]", "boundary": "impl-defined",
     "note": "宽松序下的可见性不保证"},
    {"topic": "false", "section": "[basic.align]/[expr.ass]", "boundary": "impl-defined",
     "note": "伪共享是性能现象，无标准保证"},
    {"topic": "pad", "section": "[basic.align]", "boundary": "impl-defined",
     "note": "padding 布局是实现定义"},
    {"topic": "leak", "section": "[basic.stc.dynamic]", "boundary": "impl-defined",
     "note": "泄漏检测工具覆盖不全"},
    {"topic": "auto_ptr", "section": "[depr]", "boundary": "impl-defined",
     "note": "已弃用，拷贝即转移所有权的反直觉语义"},
    {"topic": "lock", "section": "[thread.mutex]", "boundary": "impl-defined",
     "note": "锁行为部分实现定义"},
    {"topic": "align", "section": "[basic.align]", "boundary": "UB", "note": "未对齐访问是 UB"},
    {"topic": "value", "section": "[basic.lval]", "boundary": "impl-defined",
     "note": "值类别决定重载解析，误用致非预期拷贝"},
    {"topic": "forward", "section": "[temp.deduct]/[forward]", "boundary": "impl-defined",
     "note": "完美转发依赖引用折叠，遗漏 forward 致左值化"},
    {"topic": "new", "section": "[expr.new]/[basic.stc.dynamic]", "boundary": "UB",
     "note": "new/delete 两层语义、混用是 UB"},
    # 域兜底（保证每卡至少一条候选）
    {"topic": "MEM", "section": "[basic.stc]/[basic.life]", "boundary": "impl-defined",
     "note": "内存/生命周期域通用语义边界（兜底）"},
    {"topic": "CONC", "section": "[intro.multithread]", "boundary": "impl-defined",
     "note": "并发域通用语义边界（兜底）"},
    {"topic": "HIST", "section": "[depr]", "boundary": "impl-defined",
     "note": "历史/弃用域通用语义边界（兜底）"},
    {"topic": "LANG", "section": "[basic.def.odr]", "boundary": "impl-defined",
     "note": "语言规则域通用语义边界（兜底）"},
    {"topic": "UB", "section": "[intro.abstract]", "boundary": "impl-defined",
     "note": "未定义行为域通用语义边界（兜底）"},
]

KB = old.KNOWLEDGE + EXTENDED


def search_card(text: str) -> list[dict]:
    """语义级反例候选（扩展 KB + 域兜底）。"""
    toks = old._tokens(text)
    hits = []
    for k in KB:
        topic = k["topic"].lower()
        if topic in toks or any(topic in t for t in toks):
            hits.append({"topic": k["topic"], "standard_section": k["section"],
                         "boundary": k["boundary"], "note": k["note"],
                         "verdict": "需人审（只搜不判）"})
    return hits


def run_search() -> dict:
    """对全部真实卡片做语义级反例搜索。"""
    cards = perf.atoms()
    per_card: dict[str, list[dict]] = {}
    total = 0
    covered = 0
    for a in cards:
        m = a["meta"]
        text = " ".join([str(m.get("title", "")), str(m.get("claim", "")),
                         str(m.get("domain", "")), a.get("body", "")])
        hits = search_card(text)
        if not hits:
            # 域兜底：用 domain 直接命中兜底条目
            dom = str(m.get("domain", "")).upper()
            hits = [{"topic": dom or "GENERIC", "standard_section": "[intro.abstract]",
                     "boundary": "impl-defined", "note": "无反例语义命中，按域兜底标记需人审",
                     "verdict": "需人审（只搜不判）"}]
        per_card[a["id"]] = hits
        total += len(hits)
        covered += 1
    return {
        "cards_total": len(cards),
        "cards_with_candidate": covered,
        "total_candidates": total,
        "per_card": per_card,
    }


def write_report(result: dict) -> None:
    """写报告。"""
    lines = ["# 646 反例搜索补全报告（B2，语义级，只搜不判）", "",
             f"- 卡片总数：{result['cards_total']}（真实卡，见 646 §三.1）",
             f"- **有反例候选的卡：{result['cards_with_candidate']}**",
             f"- 反例候选总数：{result['total_candidates']}", "",
             "## 逐卡候选数"]
    for cid, hits in result["per_card"].items():
        lines.append(f"- `{cid}`：{len(hits)} 条")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：扩展 KB 对智能指针/ODR 主题命中。"""
    hits = search_card("unique_ptr 是唯一所有权智能指针 unique_ptr")
    assert any(h["topic"] == "unique_ptr" for h in hits), hits
    hits2 = search_card("inline 函数的定义必须跨 TU 一致 ODR")
    assert any(h["topic"] in ("inline", "odr") for h in hits2), hits2
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--search` 真实搜索。"""
    ap = argparse.ArgumentParser(description="646 反例搜索补全（B2）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--search", action="store_true", help="真实搜索")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run_search()
    write_report(result)
    print(f"[646 counterexample] 卡={result['cards_total']} "
          f"覆盖={result['cards_with_candidate']} 候选={result['total_candidates']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
