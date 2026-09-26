"""644 阶段 D · D5 证据获取编排器。

功能（原型级）：输入一张卡片或一个知识点，自动调用 D1–D4 获取证据；
用 B2 判定证据充分性；若不足，继续获取（最多 N 轮，防止无限循环）；
输出：证据包 + 充分性判定 + 获取日志。

**只获取不修改卡片**——证据包独立保存，不写 atoms/。

只读/追加：不修改受控目录。`--check` 只读幂等；`--run <topic>` 编排（受网络/编译器限制）。
为可测，D1/D2 取证据的函数可注入（默认用真实 D1/D2）。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compiler_probe_644 as d2
import counterexample_searcher_644 as d3
import evidence_base_644 as base
import evidence_sufficiency_644 as b2
import standard_fetcher_644 as d1

OUT_MD = os.path.join(base.ROOT, "data", "644_orchestrator_report.md")


def _ev_from_d1(fetched: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for f in fetched:
        rec = base.load_evidence(f["evidence_id"])
        if rec is not None:
            out.append({"id": rec.evidence_id, "grade": rec.grade, "verdict": "confirm",
                        "acquired_at": rec.acquired_at, "artifact_sha256_present": True,
                        "falsification": False})
    return out


def _ev_from_d3(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # 反例候选按「潜在 refute」进入证据包（不判定，留人审）
    return [{"id": f"CE-{i}", "grade": "L4", "verdict": "refute",
             "acquired_at": None, "artifact_sha256_present": False,
             "falsification": True} for i, f in enumerate(hits)]


def orchestrate(topic: str, snippet: str | None = None, max_rounds: int = 3,
                d1_acquire: Callable[..., dict] = d1.acquire,
                d2_probe: Callable[..., dict] = d2.probe) -> dict[str, Any]:
    """编排 D1–D4 获取并用 B2 判充分性，最多 max_rounds 轮。返回证据包 + 充分性 + 日志。"""
    log: list[dict[str, Any]] = []
    evidence_package: list[dict[str, Any]] = []
    last_sufficiency: dict[str, Any] = {}
    rounds = 0
    while rounds < max_rounds:
        rounds += 1
        # D1 标准
        r1 = d1_acquire(topic, None if rounds == 1 else f"std{topic}")
        std_ev = _ev_from_d1(r1.get("fetched", []))
        # D2 编译器（仅在提供 snippet 时）
        cmp_ev: list[dict[str, Any]] = []
        if snippet:
            r2 = d2_probe(snippet)
            if r2.get("ok"):
                rec = d2.make_evidence(snippet, r2)
                cmp_ev = [{"id": rec.evidence_id, "grade": rec.grade, "verdict": "confirm",
                          "acquired_at": rec.acquired_at, "artifact_sha256_present": True,
                          "falsification": False}]
        # D3 反例
        hits = d3.search(topic)
        ce_ev = _ev_from_d3(hits)
        # 汇总（避免重复）
        for e in std_ev + cmp_ev + ce_ev:
            if not any(x["id"] == e["id"] for x in evidence_package):
                evidence_package.append(e)
        # B2 充分性
        suf = b2.judge(topic, evidence_package)
        last_sufficiency = suf
        log.append({"round": rounds, "n_evidence": len(evidence_package),
                    "n_std": len(std_ev), "n_cmp": len(cmp_ev), "n_ce": len(ce_ev),
                    "verdict": suf["verdict"]})
        if suf["verdict"] == "充分":
            break
    return {"topic": topic, "rounds": rounds, "max_rounds": max_rounds,
            "evidence_package": evidence_package, "sufficiency": last_sufficiency,
            "log": log, "cards_untouched": True}


def write_report(r: dict[str, Any]) -> str:
    lines = ["# 644 D5 · 证据获取编排报告", "",
             f"- 主题：`{r['topic']}`  轮次：**{r['rounds']}/{r['max_rounds']}**",
             f"- 充分性判定：**{r['sufficiency'].get('verdict','')}**",
             f"- 证据包条目：**{len(r['evidence_package'])}**", "",
             "## 获取日志", "", "| 轮 | 累计证据 | 标准 | 编译 | 反例 | 判定 |",
             "|---|---|---|---|---|---|"]
    for row in r["log"]:
        lines.append(f"| {row['round']} | {row['n_evidence']} | {row['n_std']} | {row['n_cmp']} | {row['n_ce']} | {row['verdict']} |")
    lines += ["", "> 仅获取与保存证据，未修改任何卡片（cards_untouched=True）。", ""]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    # 注入快速失败的 fetcher（避免网络），验证编排流程 / 轮次上限 / 不改卡片
    def stub_acquire(topic, section=None):
        return {"ok": False, "fetched": [], "errors": ["stub"], "topic": topic}

    def stub_probe(snippet, opts=None, compiler="g++"):
        return {"ok": False, "error": "stub", "sandbox": None}

    # 改前快照一张卡
    atom = base.list_atoms()[0]
    with open(atom["path"], encoding="utf-8") as fh:
        before = fh.read()
    r = orchestrate("signed integer overflow", snippet=None, max_rounds=2,
                    d1_acquire=stub_acquire, d2_probe=stub_probe)
    # 流程正确
    assert r["rounds"] == 2  # 不足 → 跑到上限
    assert r["max_rounds"] == 2
    assert "evidence_package" in r and "sufficiency" in r
    assert r["log"][0]["round"] == 1
    # 充分性触发继续获取：不足时轮次增长（此处上限 2）
    assert r["rounds"] <= r["max_rounds"]
    # 不修改卡片：原文件内容一致
    with open(atom["path"], encoding="utf-8") as fh:
        after = fh.read()
    assert before == after
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 D5 证据获取编排器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--run", metavar="TOPIC", help="编排获取主题")
    ap.add_argument("--snippet", metavar="SNIPPET", help="可选 C++ 片段")
    ap.add_argument("--max-rounds", type=int, default=3, help="最大轮次")
    a = ap.parse_args(argv)
    if a.run:
        r = orchestrate(a.run, snippet=a.snippet, max_rounds=a.max_rounds)
        print(f"rounds={r['rounds']} verdict={r['sufficiency'].get('verdict')}")
        print(f"written {write_report(r)}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
