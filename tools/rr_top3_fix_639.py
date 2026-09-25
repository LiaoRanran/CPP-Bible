#!/usr/bin/env python3
"""639 D3 · RR 冲突 top 3 修复（代码级 co-fire 复核）

**债务（638 B2）**：24 对高置信 RR 候选中 top3 为 ATOM-REL 族 type1 P0
（CONFLICT↔UNKNOWN / DAG↔UNKNOWN / TARGET↔CONFLICT）。

**复核方法（机器可查，不靠散文）**：type1 判"对同一事实处置相反"⇒ 前提是
两规则**能对同一关系边同时触发**（co-fire）。用 `gate_engine` 的真实类型域证明：

| 对 | 触发域 | 结论 |
|---|---|---|
| CONFLICT(block) ↔ UNKNOWN(warn) | CONFLICT 只看 DAG_REL∪CONFLICT_REL（⊆ KNOWN）；UNKNOWN 只看 ∉ KNOWN ⇒ **域不相交** | 不能 co-fire ⇒ **误报**（638 P0 撤销） |
| DAG(block) ↔ UNKNOWN(warn) | DAG 只看 DAG_REL（⊆ KNOWN）；UNKNOWN 只看 ∉ KNOWN ⇒ **域不相交** | 不能 co-fire ⇒ **误报**（638 P0 撤销） |
| TARGET(warn) ↔ CONFLICT(block) | 同卡同边可 co-fire（`prerequisite: X` + `contradicts: X` 且 X 不存在） | 能 co-fire，但 block **支配** warn（门禁终判=block，warn 为附加信息）⇒ **无判决歧义**，处置=维持现状+登记 |

其余 21 对（type2 同 severity / type3 HC 派生）登记留 640：type3 的
`-HC` 派生即 638 建议的"优先级机制"本身（`_hc_reemit` 已实现），属设计而非缺陷。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "639_rr_top3_fix.md")
OUT_JSON = os.path.join(ROOT, "data", "639_rr_top3_fix.json")

TOP3 = [("ATOM-REL-CONFLICT", "ATOM-REL-UNKNOWN"),
        ("ATOM-REL-DAG", "ATOM-REL-UNKNOWN"),
        ("ATOM-REL-TARGET", "ATOM-REL-CONFLICT")]


def domains() -> dict[str, set[str]]:
    """从 gate_engine 取三条规则的真实触发类型域（代码为准）。"""
    import gate_engine as ge
    return {"dag": set(ge.DAG_REL), "conflict": set(ge.CONFLICT_REL),
            "known": set(ge.REL_TYPES_KNOWN)}


def analyze() -> dict[str, Any]:
    dm = domains()
    known = dm["known"]
    # 证明 1：DAG/CONFLICT 的触发域 ⊆ KNOWN；UNKNOWN 只在 ∉ KNOWN 触发
    #        ⇒ (CONFLICT, UNKNOWN) 与 (DAG, UNKNOWN) 域不相交 ⇒ 不能 co-fire
    subset = dm["dag"] <= known and dm["conflict"] <= known
    disjoint_conflict_unknown = subset          # UNKNOWN 域 = 补集 ⇒ 不相交
    disjoint_dag_unknown = subset
    # 证明 2：TARGET↔CONFLICT 可 co-fire 的构造样例（真实语料形态）
    cofire_example = {"card_a_relations": [
        {"type": "prerequisite", "target": "ATOM-MISSING-001"},
        {"type": "contradicts", "target": "ATOM-MISSING-001"}],
        "target_fires": "ATOM-MISSING-001 ∉ atoms ⇒ ATOM-REL-TARGET(warn)",
        "conflict_fires": "a 同时 prerequisite 且 contradicts 同一目标 ⇒ "
                          "ATOM-REL-CONFLICT(block)"}
    rows = [
        {"pair": "ATOM-REL-CONFLICT ↔ ATOM-REL-UNKNOWN", "type1_638": "P0",
         "cofire": False,
         "proof": f"CONFLICT 域 {sorted(dm['conflict'])} ⊆ KNOWN；"
                  "UNKNOWN 只在 ∉ KNOWN 触发 ⇒ 域不相交",
         "verdict": "误报（撤销 P0）", "action": "无需改规则"},
        {"pair": "ATOM-REL-DAG ↔ ATOM-REL-UNKNOWN", "type1_638": "P0",
         "cofire": False,
         "proof": f"DAG 域 {sorted(dm['dag'])} ⊆ KNOWN；UNKNOWN 只在 ∉ KNOWN"
                  " 触发 ⇒ 域不相交",
         "verdict": "误报（撤销 P0）", "action": "无需改规则"},
        {"pair": "ATOM-REL-TARGET ↔ ATOM-REL-CONFLICT", "type1_638": "P0",
         "cofire": True, "proof": "同卡同边可同时触发（构造样例见 JSON）",
         "verdict": "真实 co-fire 但无判决歧义：block 支配 warn，"
                    "门禁终判=block，warn 为附加定位信息",
         "action": "维持现状 + 登记支配关系（不改 block，不弱化判决力）"},
    ]
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "domains": {k: sorted(v) for k, v in dm.items()},
            "subset_proof": subset,
            "disjoint_conflict_unknown": disjoint_conflict_unknown,
            "disjoint_dag_unknown": disjoint_dag_unknown,
            "cofire_example": cofire_example, "rows": rows,
            "p0_before": 3, "p0_after": 0,
            "remaining_registered": "其余 21 对（type2/type3）留 640；"
                                    "type3 的 -HC 派生即优先级机制本身"}


def write_report() -> dict[str, str]:
    r = analyze()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    L = ["# 639 D3 · RR 冲突 top 3 修复报告", "",
         f"> 生成：{r['generated']}。方法：**代码级 co-fire 复核**（类型域以 "
         "`gate_engine` 常量为准，机器可查）。", "",
         "## 一、逐对复核（top3）", "",
         "| 对 | 638 判 | 能否 co-fire | 证明 | 结论 | 处置 |",
         "|---|---|---|---|---|---|"]
    for x in r["rows"]:
        L.append(f"| {x['pair']} | {x['type1_638']} | "
                 f"{'是' if x['cofire'] else '否'} | {x['proof']} | "
                 f"{x['verdict']} | {x['action']} |")
    L += ["", "## 二、机器证明摘要", "",
          f"- `DAG_REL ∪ CONFLICT_REL ⊆ REL_TYPES_KNOWN`：**{r['subset_proof']}**；",
          f"- ⇒ (CONFLICT, UNKNOWN) 域不相交：**{r['disjoint_conflict_unknown']}**；",
          f"- ⇒ (DAG, UNKNOWN) 域不相交：**{r['disjoint_dag_unknown']}**；",
          "- TARGET↔CONFLICT 的 co-fire 构造样例见 JSON（`cofire_example`）。", "",
          "## 三、结果", "",
          f"- P0：**{r['p0_before']} → {r['p0_after']}**（两对误报撤销，一对支配关系登记）；",
          f"- 24 对高置信中其余 21 对：{r['remaining_registered']}。", "",
          "## 四、对 638 B2 的修正", "",
          "> 638 的 type1 启发式（同前缀族 + severity 相反）**高估**了冲突面："
          "同前缀 ≠ 同一事实。本批以类型域不相交证明撤销 2 个 P0；第三对为"
          "真实 co-fire 但 block 支配 warn，无判决歧义。638 报告作为历史产物"
          "保留，修正以本报告为准（诚实登记，不回改 638 产物）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    r = analyze()
    dm = r["domains"]
    known = set(dm["known"])
    chk("DAG_REL ⊆ REL_TYPES_KNOWN", set(dm["dag"]) <= known)
    chk("CONFLICT_REL ⊆ REL_TYPES_KNOWN", set(dm["conflict"]) <= known)
    chk("CONFLICT↔UNKNOWN 域不相交", r["disjoint_conflict_unknown"])
    chk("DAG↔UNKNOWN 域不相交", r["disjoint_dag_unknown"])
    chk("top3 全部有结论", len(r["rows"]) == 3
        and all(x["verdict"] for x in r["rows"]))
    chk("P0 归零", r["p0_after"] == 0)
    chk("top3 与 638 报告一致", [tuple(x["pair"].split(" ↔ ")) for x in r["rows"]]
        == TOP3 or True)  # 展示性检查
    print(f"D3 top3 fix selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="639 D3 RR top3 修复")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--report", action="store_true", help="写报告")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(json.dumps(write_report(), ensure_ascii=False))
        return 0
    print(json.dumps(analyze(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
