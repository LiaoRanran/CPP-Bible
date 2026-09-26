"""646 · 阶段 A4 · 证据检索提速（倒排索引，清债 2 续）。

目标（646 §三 A4）：把证据检索从「全量线性扫描」改为「索引查询」，提速 ≥50%。

**数据源**：`data/evidence_store/` 与 `card_evidence_map()` 的**真实**证据（非代理、不编造）。

真实做法：
- 对 `evidence_store` 的真实证据建两类索引：
  - **倒排索引**：关键词 token → 证据 id 列表（来源 topic/section/source 等字段）。
  - **等级索引**：L1..L5 → 证据 id 列表。
- 查询 API：`search_by_token(tok)` / `search_by_grade(g)` 走 dict 直取。
- 基准：同一批查询，**线性扫描**（逐条子串匹配）vs **索引查询**，测真实提速。

**只读**：不改证据、不改卡片。`--check` 只读自检；`--run` 真实建索引 + 基准，写
`data/646_evidence_index.json` + `data/646_evidence_index_report.md`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
INDEX_JSON = os.path.join(DATA, "646_evidence_index.json")
REPORT_MD = os.path.join(DATA, "646_evidence_index_report.md")
THRESHOLD = 0.50


def _records() -> list[dict]:
    """真实落库证据（id/grade/source/card），供建索引与线性对照。"""
    import perf_646 as perf
    out = []
    for eid, grade, _cred, src, card in perf.stored_records():
        out.append({"id": eid, "grade": grade, "source": src, "card": card or ""})
    # 叠加 card_evidence_map（EV→卡）作为额外证据面
    for card, evs in perf.card_evidence_map().items():
        for e in evs:
            out.append({"id": str(e.get("id", "")), "grade": str(e.get("grade", "")),
                        "source": str(e.get("source", "")), "card": card})
    return out


def _tokens(rec: dict) -> set[str]:
    """证据的可索引 token（id/来源/卡 id 的英文词）。"""
    text = f"{rec['id']} {rec['source']} {rec['card']}"
    return {w.lower() for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text)}


def build_index() -> dict:
    """建倒排索引 + 等级索引。"""
    recs = _records()
    inverted: dict[str, list[str]] = {}
    by_grade: dict[str, list[str]] = {}
    for i, rec in enumerate(recs):
        rid = rec["id"] or f"#{i}"
        by_grade.setdefault(rec["grade"] or "L5", []).append(rid)
        for tok in _tokens(rec):
            inverted.setdefault(tok, []).append(rid)
    for k in inverted:
        inverted[k] = sorted(set(inverted[k]))
    for k in by_grade:
        by_grade[k] = sorted(set(by_grade[k]))
    return {"records": recs, "inverted": inverted, "by_grade": by_grade}


def _linear_search(recs: list[dict], tok: str) -> list[str]:
    """线性扫描对照实现（逐条重新分词后判定 token 命中，与索引同语义）。"""
    out = []
    for rec in recs:
        if tok in _tokens(rec):
            out.append(rec["id"])
    return out


def benchmark(index: dict, queries: list[str]) -> dict:
    """同一批查询：线性 vs 索引，测真实提速。"""
    recs = index["records"]
    inverted = index["inverted"]
    # 线性
    s = time.perf_counter()
    lin_total = 0
    for q in queries:
        lin_total += len(set(_linear_search(recs, q)))
    lin_ms = (time.perf_counter() - s) * 1000
    # 索引
    s = time.perf_counter()
    idx_total = 0
    for q in queries:
        idx_total += len(inverted.get(q, []))
    idx_ms = (time.perf_counter() - s) * 1000
    speedup = 0.0 if lin_ms <= 0 else round((1 - idx_ms / lin_ms) * 100, 1)
    return {
        "queries": len(queries),
        "linear_ms": round(lin_ms, 4),
        "indexed_ms": round(idx_ms, 4),
        "speedup_pct": speedup,
        "met": speedup >= THRESHOLD * 100,
        "linear_hits": lin_total, "indexed_hits": idx_total,
    }


def run() -> dict:
    """建索引 + 基准（用索引中出现频次最高的若干 token 作为查询集）。"""
    index = build_index()
    inverted = index["inverted"]
    # 取高频 token 作为查询集（真实检索热点）
    hot = sorted(inverted, key=lambda k: len(inverted[k]), reverse=True)[:20]
    bench = benchmark(index, hot)
    return {
        "records": len(index["records"]),
        "inverted_terms": len(inverted),
        "grade_index": {g: len(v) for g, v in index["by_grade"].items()},
        "bench": bench,
        "queries": hot,
    }


def write_report(result: dict) -> None:
    """写索引文件 + 报告。"""
    idx = build_index()
    with open(INDEX_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"inverted": idx["inverted"], "by_grade": idx["by_grade"]},
                  fh, ensure_ascii=False, indent=2, sort_keys=True)
    b = result["bench"]
    lines = ["# 646 证据检索提速报告（A4，清债 2 续）", "",
             f"- 索引证据数：{result['records']}",
             f"- 倒排 token 数：{result['inverted_terms']}",
             f"- 等级索引：{result['grade_index']}",
             f"- 基准查询数：{b['queries']}",
             f"- 线性扫描：{b['linear_ms']} ms；索引查询：{b['indexed_ms']} ms",
             f"- **提速：{b['speedup_pct']}%**（目标 ≥{THRESHOLD*100}%）达标：{b['met']}",
             f"- 命中数一致（线性 {b['linear_hits']} vs 索引 {b['indexed_hits']}）："
             f"{b['linear_hits'] == b['indexed_hits']}", "",
             "## 与 645 的差别", "",
             "645 的证据检索是全量扫描（`card_evidence_map` 遍历）；646 建**倒排 + 等级索引**，"
             "查询走 dict 直取。索引文件：`data/646_evidence_index.json`。"]
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def selftest() -> int:
    """只读自检：索引命中与线性扫描一致。"""
    idx = build_index()
    recs = idx["records"]
    for tok in list(idx["inverted"])[:5]:
        lin = sorted(set(_linear_search(recs, tok)))
        got = idx["inverted"][tok]
        assert set(lin) == set(got), (tok, lin, got)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--run` 建索引 + 基准。"""
    ap = argparse.ArgumentParser(description="646 证据检索提速（A4）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="建索引 + 基准")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run()
    write_report(result)
    print(f"[646 index] 证据={result['records']} token={result['inverted_terms']} "
          f"提速={result['bench']['speedup_pct']}% 达标={result['bench']['met']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
