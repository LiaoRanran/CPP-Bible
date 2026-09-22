"""624 A5 · VFDR 更新 v2 + 规则触达热力图 v2 + 盲区缩减报告

**输入（6 轮闭环真跑）**：
- R1 = 622 A2（`mutation_sandbox_run_622_results.json`）
- R2 = 622 A4（`mutation_sandbox_run_622_round2_results.json`）
- R3 = 623 A2（`high_complexity_sandbox_run_623.json`）
- R4 = 623 A4（`adversarial_loop_round3_sandbox_run_623.json`）
- R5 = 624 A2（`cross_card_sandbox_run_624.json`）
- R6 = 624 A4（`adversarial_loop_round5_624.json`）

**口径**：
- 检测率（VFDR）= (blocked + detected_nonblock) / (total − infra_error)。
- 触达 = 该轮任一 row 的 new_block_rules ∪ new_nonblock_rules。
- 盲区 v2 = 63 规则 − 6 轮累计触达。

铁律：只读统计，不改数据。必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ROUNDS = [
    ("R1", "622 A2（单卡低复杂）", "mutation_sandbox_run_622_results.json"),
    ("R2", "622 A4（单卡 v2 M8/M9）", "mutation_sandbox_run_622_round2_results.json"),
    ("R3", "623 A2（单卡高复杂）", "high_complexity_sandbox_run_623.json"),
    ("R4", "623 A4（单卡定向）", "adversarial_loop_round3_sandbox_run_623.json"),
    ("R5", "624 A2（跨卡）", "cross_card_sandbox_run_624.json"),
    ("R6", "624 A4（跨卡定向 X5-X8）", "adversarial_loop_round5_624.json"),
]

BLIND_623 = 37  # 623 盲区


def _load_rules() -> list[dict]:
    p = os.path.join(ROOT, "data", "_gate_rules.json")
    with open(p, encoding="utf-8") as fh:
        data = json.load(fh)
    out = []
    for r in data:
        if isinstance(r, str):
            out.append({"id": r, "severity": ""})
        else:
            out.append({"id": r.get("id") or r.get("rule") or "",
                        "severity": r.get("severity") or r.get("severity_level") or ""})
    return out


def _round_touched(path: str) -> tuple[set, dict]:
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    touched: set[str] = set()
    for r in d.get("rows") or []:
        touched |= set(r.get("new_block_rules") or [])
        touched |= set(r.get("new_nonblock_rules") or [])
    dist = d.get("distribution") or {}
    total = d.get("total") or len(d.get("rows") or [])
    return touched, {"distribution": dist, "total": total}


def compute() -> dict:
    rules = _load_rules()
    all_ids = [r["id"] for r in rules if r["id"]]
    rounds: list[dict] = []
    cumulative: set[str] = set()
    for rid, label, fn in ROUNDS:
        p = os.path.join(ROOT, "data", fn)
        touched, info = _round_touched(p)
        cumulative |= touched
        dist = info["distribution"]
        infra = dist.get("infra_error", 0)
        denom = info["total"] - infra
        caught = dist.get("blocked", 0) + dist.get("detected_nonblock", 0)
        rounds.append({
            "round": rid, "label": label, "file": fn, "total": info["total"],
            "blocked": dist.get("blocked", 0), "detected_nonblock": dist.get("detected_nonblock", 0),
            "neutral": dist.get("neutral", 0), "infra_error": infra,
            "escaped": len(json.load(open(p, encoding="utf-8")).get("escaped") or []),
            "detect_rate": round(caught / denom, 4) if denom else None,
            "touched": sorted(touched), "n_touched": len(touched),
        })
    heatmap = {rid: {r["round"]: (rid in r["touched"]) for r in rounds} for rid in all_ids}
    untouched = sorted(set(all_ids) - cumulative)
    return {
        "total_rules": len(all_ids),
        "rounds": rounds,
        "cumulative_touched": sorted(cumulative),
        "cumulative_count": len(cumulative),
        "untouched_v2": untouched,
        "blind_count": len(untouched),
        "blind_reduction": {"from": BLIND_623, "to": len(untouched),
                            "reduced_by": BLIND_623 - len(untouched)},
        "heatmap": heatmap,
    }


def to_markdown(res: dict) -> str:
    rules = _load_rules()
    sev = {r["id"]: r["severity"] for r in rules}
    lines = ["# 624 A5 · 规则触达热力图 v2（63 规则 × 6 轮）", "",
             "> 图例：`T`=该轮触达；`.`=未触达。", "",
             "| 规则 | 严重 | R1 | R2 | R3 | R4 | R5 | R6 | 累计 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rules:
        rid = r["id"]
        if not rid:
            continue
        cols = ["T" if res["heatmap"][rid][f"R{i}"] else "." for i in range(1, 7)]
        cum = "T" if rid in set(res["cumulative_touched"]) else "."
        lines.append(f"| {rid} | {sev.get(rid,'')} | " + " | ".join(cols) + f" | {cum} |")
    lines += ["", f"**累计触达 {res['cumulative_count']}/63；盲区 {res['blind_count']}"
                  f"（623 为 {BLIND_623}，缩减 {res['blind_reduction']['reduced_by']}）**", ""]
    return "\n".join(lines) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    rules = _load_rules()
    chk("规则清单 63 条", len(rules) == 63)
    res = compute()
    chk("6 轮齐全", [r["round"] for r in res["rounds"]] == ["R1", "R2", "R3", "R4", "R5", "R6"])
    chk("累计触达 ≥32 且 ≤63", 32 <= res["cumulative_count"] <= 63)
    chk("盲区 = 63 − 累计", res["blind_count"] == 63 - res["cumulative_count"])
    chk("盲区缩减报告存在", res["blind_reduction"]["to"] == res["blind_count"])
    chk("热力图覆盖 63 规则", len(res["heatmap"]) == 63)
    chk("R5/R6 均在热力图中", all("R5" in v and "R6" in v for v in res["heatmap"].values()))
    print(f"A5 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="624 A5 VFDR v2 + 热力图 v2 + 盲区缩减")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--md", help="同时输出 markdown 热力图")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    res = compute()
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(to_markdown(res))
    print(json.dumps({"cumulative_count": res["cumulative_count"],
                      "blind_count": res["blind_count"],
                      "blind_reduction": res["blind_reduction"],
                      "rounds": [{k: r[k] for k in ("round", "n_touched", "detect_rate",
                                                    "blocked", "detected_nonblock", "escaped")}
                                 for r in res["rounds"]]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
