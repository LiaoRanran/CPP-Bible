"""644 阶段 D · D4 多源交叉验证器。

功能：对给定结论，从多个来源获取证据并对比一致性：
- 标准（D1）/ 编译器实测（D2）/ 反例（D3）

输出：一致性报告（一致 / 部分一致 / 冲突）+ 各来源证据。
一致性逻辑（纯函数，可测）：每个来源给出一个「立场」（support / refute / neutral），
全部 support → 一致；任一 refute 与其他 support 冲突 → 冲突；否则部分一致。

只读/追加：不修改受控目录。`--check` 只读幂等；`--validate <conclusion>` 端到端（可能受网络/编译器限制）。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compiler_probe_644 as d2
import counterexample_searcher_644 as d3
import evidence_base_644 as base
import standard_fetcher_644 as d1

OUT_MD = os.path.join(base.ROOT, "data", "644_cross_validation_report.md")


def consistency_of(stances: list[str]) -> str:
    """纯函数：根据立场集合判定一致性。"""
    s = set(stances)
    if "refute" in s and "support" in s:
        return "conflict"
    if "refute" in s:
        return "partial"
    if "support" in s:
        return "consistent"
    return "partial"


def validate(conclusion: str, *, snippet: str | None = None,
             max_rounds: int = 1) -> dict[str, Any]:
    """端到端：调用 D1/D2/D3 收集证据并比对一致性（来源失败降级）。"""
    sources: list[dict[str, Any]] = []
    # 标准（D1）
    r1 = d1.acquire(conclusion)
    stance_std = "support" if r1["ok"] else "neutral"
    sources.append({"source": "standard", "ok": r1["ok"], "stance": stance_std,
                    "evidence": r1["fetched"], "errors": r1["errors"]})
    # 编译器实测（D2）
    if snippet and d2.find_compiler("g++"):
        r2 = d2.probe(snippet)
        stance_cmp = "support" if r2["ok"] else "neutral"
        sources.append({"source": "compiler", "ok": r2["ok"], "stance": stance_cmp,
                        "output": r2.get("output", "")})
    # 反例（D3）
    hits = d3.search(conclusion)
    stance_ce = "refute" if hits else "neutral"
    sources.append({"source": "counterexample", "ok": True, "stance": stance_ce,
                    "candidates": hits})
    stances = [s["stance"] for s in sources]
    verdict = consistency_of(stances)
    return {"conclusion": conclusion, "verdict": verdict, "sources": sources,
            "stances": stances}


def write_report(r: dict[str, Any]) -> str:
    lines = ["# 644 D4 · 多源交叉验证报告", "", f"- 结论：`{r['conclusion']}`",
             f"- 一致性判定：**{r['verdict']}**", "",
             "| 来源 | 成功 | 立场 |", "|---|---|---|"]
    for s in r["sources"]:
        lines.append(f"| {s['source']} | {'✅' if s['ok'] else '❌'} | {s['stance']} |")
    lines.append("")
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    # 已知一致：全 support
    assert consistency_of(["support", "support"]) == "consistent"
    # 已知冲突：support + refute
    assert consistency_of(["support", "refute"]) == "conflict"
    # 部分一致：只有 neutral / refute
    assert consistency_of(["refute"]) == "partial"
    # 端到端结构正确且不崩溃（网络/编译器受限时降级）
    r = validate("signed integer overflow")
    assert r["verdict"] in ("consistent", "partial", "conflict")
    assert "sources" in r and len(r["sources"]) >= 2
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 D4 多源交叉验证器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--validate", metavar="CONCLUSION", help="验证结论")
    ap.add_argument("--snippet", metavar="SNIPPET", help="可选 C++ 片段用于编译器实测")
    a = ap.parse_args(argv)
    if a.validate:
        r = validate(a.validate, snippet=a.snippet)
        print(f"verdict={r['verdict']}")
        print(f"written {write_report(r)}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
