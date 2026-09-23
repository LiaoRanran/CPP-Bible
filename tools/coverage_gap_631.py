"""631 D1 · coverage 未跑向量清单 + 探针优先级（纯标准库，只读）

输入（只读调用既有工具）：
- `attack_surface_taxonomy.VECTORS`（629 B1）：(id, name, desc, risk, probe)
- `coverage_metric_630.measure()`（630 C1）：`never_run` / `no_probe` / `ran`

对 **19 个从未跑过的向量**给出：层 / 名称 / risk / 是否有探针 / 优先级(P0-P2) / 补探针难度。

优先级规则（人定，写死在代码里可审）：
| 条件 | 优先级 | 理由 |
|---|---|---|
| risk=high **且无探针** | **P0** | 高风险 + 完全裸奔 |
| risk=high 且有探针（只是没跑过） | P1 | 有工具，补一次执行即可 |
| risk≠high 且无探针 | P1 | 无探针 ⇒ 永远不会被覆盖 |
| 其他 | P2 | — |

难度规则：
- **低**：`probe` 非 null（有现成工具可驱动）；
- **中**：无探针但属结构化层（L1/L2/L3/L5/L6/L7），可用模板/变异生成输入；
- **高**：无探针且需语义判断或外部依赖（时间/调度/人审），见 `DIFFICULTY_OVERRIDE`。
  （`DIFFICULTY_OVERRIDE` 是**人读向量描述后的判断**，逐条可审。）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "coverage_gap_631.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_gap_631.json")

STRUCTURED_LAYERS = ("L1", "L2", "L3", "L5", "L6", "L7")

# 人读描述后给的难度覆盖（无探针的 6 个逐条判定）
DIFFICULTY_OVERRIDE = {
    "L1.2": ("高", "多义指代需语义/指代消解，模板生成没有判别力"),
    "L2.3": ("中", "证据漂移可用「改证据文件 + 重跑 replay」驱动，需造证据变体"),
    "L4.2": ("中", "规则绕过可用变异算子造「绕过某条规则」的样本"),
    "L4.4": ("高", "判据冲突需两个判据给出相反结论，需人工构造争议样本"),
    "L7.5": ("高", "调度/时序类需外部时钟或并发编排，纯静态难造"),
    "L8.4": ("高", "跨层组合需多工具联动，成本最高"),
}


def vectors() -> list[dict[str, Any]]:
    """629 B1 的向量表（tuple → dict）。"""
    import attack_surface_taxonomy as T

    out = []
    for item in T.VECTORS:
        vid, name, desc, risk, probe = item
        out.append({"id": vid, "name": name, "desc": desc, "risk": risk,
                    "probe": probe, "layer": str(vid).split(".")[0]})
    return out


def coverage() -> dict[str, Any]:
    import coverage_metric_630 as C

    return C.measure()


def priority_of(risk: str, no_probe: bool) -> str:
    high = str(risk).lower() == "high"
    if high and no_probe:
        return "P0"
    if high or no_probe:
        return "P1"
    return "P2"


def difficulty_of(v: dict[str, Any], no_probe: bool) -> tuple[str, str]:
    if v["id"] in DIFFICULTY_OVERRIDE:
        return DIFFICULTY_OVERRIDE[v["id"]]
    if not no_probe:
        return ("低", "有现成工具可驱动（`probe` 字段非 null）⇒ 补一次执行即可")
    if v["layer"] in STRUCTURED_LAYERS:
        return ("中", "无探针但属结构化层 ⇒ 可用模板/变异算子生成输入")
    return ("高", "无探针且需语义判断或外部依赖")


def rows() -> list[dict[str, Any]]:
    cov = coverage()
    never = list(cov.get("never_run") or [])
    noprobe = set(cov.get("no_probe") or [])
    vmap = {v["id"]: v for v in vectors()}
    out = []
    for vid in never:
        v = vmap.get(vid, {"id": vid, "name": "（未知）", "desc": "", "risk": "?",
                           "probe": None, "layer": str(vid).split(".")[0]})
        np_ = vid in noprobe
        prio = priority_of(v.get("risk", ""), np_)
        diff, why = difficulty_of(v, np_)
        out.append({"id": vid, "layer": v["layer"], "name": v.get("name"),
                    "desc": v.get("desc"), "risk": v.get("risk"),
                    "has_probe": not np_, "probe": v.get("probe"),
                    "priority": prio, "difficulty": diff, "difficulty_why": why})
    order = {"P0": 0, "P1": 1, "P2": 2}
    dorder = {"低": 0, "中": 1, "高": 2}
    return sorted(out, key=lambda r: (order[r["priority"]], dorder[r["difficulty"]],
                                      r["id"]))


def counts(rr: Optional[list[dict[str, Any]]] = None) -> dict[str, int]:
    rr = rr if rr is not None else rows()
    out: dict[str, int] = {}
    for r in rr:
        out[r["priority"]] = out.get(r["priority"], 0) + 1
    return {k: out.get(k, 0) for k in ("P0", "P1", "P2")}


def write_report() -> str:
    rr = rows()
    cov = coverage()
    c = counts(rr)
    lines = [
        "# 631 D1 · coverage 未跑向量清单 + 探针优先级", "",
        f"- 当前 coverage：**{cov['ran_count']}/{cov['total']} = "
        f"{cov['coverage_pct']}%**",
        f"- 从未跑过的向量：**{cov['never_run_count']}** 个"
        f"（其中 **{cov['no_probe_count']}** 个连探针都没有）",
        f"- 优先级：**P0 {c['P0']} / P1 {c['P1']} / P2 {c['P2']}**", "",
        "> 630 C1 还发现一处**向量表缺口**：`M1 删字段` 在向量表里没有对应项"
        "（630 D2 跑了 10 条删字段变异，却无处归类）⇒ 见 §三。", "",
        "## 一、19 个未跑向量逐条清单（按 优先级→难度→ID）", "",
        "| # | 优先级 | 向量 | 层 | 名称 | risk | 有探针 | 补探针难度 | 难度理由 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rr, 1):
        lines.append(f"| {i} | **{r['priority']}** | `{r['id']}` | {r['layer']} | "
                     f"{r['name']} | {r['risk']} | {'是' if r['has_probe'] else '**否**'} | "
                     f"{r['difficulty']} | {r['difficulty_why'][:34]} |")
    lines += [
        "", "## 二、优先级与难度规则（可审）", "",
        "| 条件 | 优先级 |", "|---|---|",
        "| risk=high **且无探针** | **P0**（高风险 + 完全裸奔） |",
        "| risk=high 且有探针（只是没跑过） | P1 |",
        "| risk≠high 且无探针 | P1 |",
        "| 其他 | P2 |", "",
        "| 难度 | 判定 |", "|---|---|",
        "| 低 | 有现成工具（`probe` 非 null） |",
        "| 中 | 无探针但属结构化层，可模板/变异生成 |",
        "| 高 | 需语义判断或外部依赖（逐条见 `DIFFICULTY_OVERRIDE`） |", "",
        "## 三、诚实登记", "",
        "1. **难度是人工判断**（`DIFFICULTY_OVERRIDE` 逐条给理由），不是测量值；",
        "2. **优先级只用了 risk + 有无探针两个维度**，没考虑「该向量实际发生过吗」"
        "——630 的 `real_event_count = 15` 说明有 15 个向量**真实发生过**，"
        "若按「真实发生过」加权，排序会变（本批未加权，避免与 630 口径打架）；",
        "3. **向量表本身不完备**：`M1 删字段` 无对应向量 ⇒ 补全探针前应先补向量表"
        "（否则探针无处登记）⇒ 列入交人/后续；",
        "4. 本工具只读：不跑任何探针、不改任何向量表。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"rows": rr, "counts": c}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rr = rows()
    cov = coverage()
    chk("未跑向量 = 19", len(rr) == cov["never_run_count"] == 19, f"({len(rr)})")
    chk("无探针 = 6 且都在未跑清单里",
        cov["no_probe_count"] == 6
        and set(cov["no_probe"]) <= {r["id"] for r in rr})
    chk("每条都有层/名称/risk/优先级/难度",
        all(r["layer"] and r["name"] and r["risk"] and r["priority"]
            and r["difficulty"] for r in rr))
    chk("P0 判定 = high risk 且无探针",
        all((r["risk"] == "high" and not r["has_probe"]) for r in rr
            if r["priority"] == "P0")
        and any(r["priority"] == "P0" for r in rr),
        f"(P0={[r['id'] for r in rr if r['priority'] == 'P0']})")
    chk("优先级计数合计 = 19", sum(counts(rr).values()) == 19)
    chk("难度覆盖表逐条有理由",
        all(len(v) == 2 and v[0] in ("低", "中", "高") and v[1]
            for v in DIFFICULTY_OVERRIDE.values()))

    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    rows()
    write_report()
    chk("只读：不跑探针、不改工作区", snap() == before)
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"D1 coverage gap check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 D1 coverage 缺口清单（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写清单 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    rr = rows()
    if args.json:
        print(json.dumps({"rows": rr, "counts": counts(rr)},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"never_run={len(rr)} counts={counts(rr)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
