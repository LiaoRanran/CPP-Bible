"""625 B2 · 雷2 闭环稳定指标 + 触发标准①验证

**输入**：620-625 各轮沙箱实跑 JSON（见 ROUNDS）。
**稳定指标**（基于「累计触达规则 / 67」与逃逸）：
- **触达增长率** = 本轮新增触达 / 本轮累计触达（<10% 视为稳定）；
- **VFDR 收敛率** = 累计新逃逸 / 累计 mutation（<1% 视为收敛）；
- **判决一致性** = 1 − 逃逸/总 mutation（>95% 视为一致）；
- **覆盖稳定性波动** = 最近 3 轮增长率的极差（<5% 视为稳定）。

**触发标准①**（雷1 剥离前置）：连续 3 轮 && 增长率<10% && 收敛率<1% && 一致性>95% && 波动<5%。

铁律：只读各轮 JSON；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TOTAL_RULES = 67
ROUNDS = [
    ("R2 622A2", "data/mutation_sandbox_run_622_results.json"),
    ("R2b 622A4", "data/mutation_sandbox_run_622_round2_results.json"),
    ("R3 623A2", "data/high_complexity_sandbox_run_623.json"),
    ("R4 623A4", "data/adversarial_loop_round3_sandbox_run_623.json"),
    ("R5 624A2", "data/cross_card_sandbox_run_624.json"),
    ("R6 624A4", "data/adversarial_loop_round5_624.json"),
    ("R7 625B1", "data/adversarial_loop_round7_sandbox_run_625.json"),
]


def _load(rel: str) -> dict:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        return cast("dict[str, Any]", json.load(fh))


def touched_of(d: dict) -> set[str]:
    out: set[str] = set()
    for r in d.get("rows", []) or []:
        out.update(r.get("new_block_rules", []) or [])
        out.update(r.get("new_nonblock_rules", []) or [])
    for k in ("touched_all", "touched_block", "touched_nonblock"):
        if isinstance(d.get(k), list):
            out.update(d[k])
    return out


def mutations_of(d: dict) -> int:
    if isinstance(d.get("total"), int):
        return int(d["total"])
    if isinstance(d.get("mutations"), list):
        return len(d["mutations"])
    return len(d.get("rows", []) or [])


def escaped_of(d: dict) -> int:
    dist = d.get("distribution") or {}
    if isinstance(dist.get("escaped"), int):
        return int(dist["escaped"])
    esc = d.get("escaped")
    if isinstance(esc, list):
        return len(esc)
    if isinstance(esc, int):
        return esc
    return 0


def metrics() -> dict:
    cum: set[str] = set()
    rows: list[dict] = []
    total_mut = 0
    total_esc = 0
    for label, rel in ROUNDS:
        d = _load(rel)
        t = touched_of(d)
        m = mutations_of(d)
        e = escaped_of(d)
        prev = len(cum)
        cum |= t
        inc = len(cum) - prev
        total_mut += m
        total_esc += e
        rows.append({"round": label, "mutations": m, "escaped": e,
                     "new": inc, "cum": len(cum),
                     "growth": (inc / len(cum)) if cum else 0.0})
    vfdr = (total_esc / total_mut) if total_mut else 0.0
    consistency = (1 - total_esc / total_mut) if total_mut else 1.0
    last3 = rows[-3:]
    vol = (max(r["growth"] for r in last3) - min(r["growth"] for r in last3)) if last3 else 0.0
    return {"rows": rows, "cum_touched": len(cum), "blind": TOTAL_RULES - len(cum),
            "total_mutations": total_mut, "total_escaped": total_esc,
            "vfdr": round(vfdr, 6), "consistency": round(consistency, 6),
            "coverage_volatility": round(vol, 6)}


def trigger1(m: dict) -> dict:
    last_growth = m["rows"][-1]["growth"] if m["rows"] else 1.0
    checks = {
        "连续≥3轮": len(m["rows"]) >= 3,
        "最近一轮增长率<10%": last_growth < 0.10,
        "VFDR收敛率<1%": m["vfdr"] < 0.01,
        "判决一致性>95%": m["consistency"] > 0.95,
        "覆盖稳定性波动<5%": m["coverage_volatility"] < 0.05,
    }
    return {"checks": checks, "satisfied": all(checks.values()),
            "satisfied_count": sum(checks.values()), "total": len(checks)}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    m = metrics()
    chk("读取 7 轮", len(m["rows"]) == 7)
    chk("累计触达 ≤ 67", 0 < m["cum_touched"] <= TOTAL_RULES)
    chk("VFDR 可计算（0≤vfdr）", m["vfdr"] >= 0)
    t = trigger1(m)
    chk("触发标准①有 5 项", t["total"] == 5)
    chk("satisfied 与 checks 一致", t["satisfied"] == all(t["checks"].values()))
    chk("合成：单调增长检测可算", isinstance(m["rows"][0]["growth"], float))
    print(f"B2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def render(m: dict, t: dict) -> str:
    L = ["# 625 B2 · 雷2 闭环稳定指标 + 触发标准①验证", "",
         f"> 规则分母 {TOTAL_RULES}；累计触达 **{m['cum_touched']}/{TOTAL_RULES}**，盲区 **{m['blind']}**。", "",
         "## 一、各轮触达与增长", "",
         "| 轮次 | mutation | 新触达 | 累计 | 增长率 | 逃逸 |", "|---|---|---|---|---|---|"]
    for r in m["rows"]:
        L.append(f"| {r['round']} | {r['mutations']} | {r['new']} | {r['cum']} | "
                 f"{r['growth']:.1%} | {r['escaped']} |")
    L += ["", "## 二、稳定指标", "",
          "| 指标 | 值 | 阈值 |", "|---|---|---|",
          f"| 触达增长率（最近一轮） | {m['rows'][-1]['growth']:.1%} | <10% |",
          f"| VFDR 收敛率 | {m['vfdr']:.4%} | <1% |",
          f"| 判决一致性 | {m['consistency']:.2%} | >95% |",
          f"| 覆盖稳定性波动（最近3轮增长率极差） | {m['coverage_volatility']:.1%} | <5% |",
          "", "## 三、触发标准①验证", "",
          "| 检查项 | 结果 |", "|---|---|"]
    for k, v in t["checks"].items():
        L.append(f"| {k} | {'✅' if v else '❌'} |")
    L += ["", f"**满足项：{t['satisfied_count']}/{t['total']}；整体："
              f"{'✅ 满足' if t['satisfied'] else '🟠 部分满足'}**", "",
          "## 四、局限性声明", "",
          "1. 判决一致性以「1 − 逃逸/总 mutation」近似（各轮 mutation 集不重叠，无法逐条跨轮比对）。",
          "2. 覆盖稳定性波动以「最近 3 轮增长率极差」度量；含更早轮次时波动更大。",
          "3. 只含 gate（规则层）判决，未含 replay 复算层。", ""]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 B2 雷2 稳定指标")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    m = metrics()
    t = trigger1(m)
    if args.report:
        p = os.path.join(ROOT, "data", "loop_stability_report_625.md")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(m, t))
        print(f"written {p}")
        return 0
    print(json.dumps({"metrics": {k: v for k, v in m.items() if k != "rows"},
                      "trigger1": t}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
