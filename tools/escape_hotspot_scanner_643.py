"""643 B4 · **逃逸热点扫描器**（智能层：自动发现问题 #4）。

**定位**：从 616 的 v7 聚合基线与 622/623/624 的沙箱跑批里，自动找出**逃逸热点**并**归因**：
规则缺失 / 规则太弱 / 规则冲突 / 验证器能力天花板。

**数据源（全部在册、可复算）**：
- `data/mutation/full_baseline_v7.json`：1593 变异、blocked 1405、escaped 1、n_a 179、
  `by_operator_rates`（M1–M7 × strict/treated/escape 的 CP 区间）、`by_card`、`results[]`、`escaped_list[]`；
- `data/mutation_sandbox_run_622_results.json`、`data/high_complexity_sandbox_run_623.json`、
  `data/adversarial_loop_round3_sandbox_run_623.json`、`data/cross_card_sandbox_run_624.json`、
  `data/adversarial_loop_round5_624.json`：定向跑批（`new_block_rules`/`lost_rules`/`verdict`）。

**归因判据（机械，逐条可核）**：

| 归因 | 判据 |
|---|---|
| **规则缺失** | 逃逸且 `new_block` 与 `new_warn` **均为空**（没有任何规则对该变异有反应） |
| **规则太弱** | 逃逸但 `new_warn` 非空（有规则反应了，但只到 warn ⇒ 拦不住） |
| **验证器能力天花板** | 该变异被标 `equivalent`（语义等价 ⇒ **本就不该报**）或 `replay_skipped` 非空（机制跑不动） |
| **规则冲突** | 同一卡上既产生 new_block 又 lost_rules 非空（判据互相顶掉）—— 需 623/624 定向跑批数据 |

**⚠️ 口径差异（必须登记）**：`results[]` 里 `verdict=="escaped"` 有 **9** 条，
但聚合字段 `escaped` 只有 **1** —— 差额 8 条正是 `equivalent_invalid`（语义等价被剔除）。
本工具**两个口径都报**（`raw_escaped` / `counted_escaped`），不合并。

**⚠️ 数据缺口**：v7 的 `results[]` **没有 N/A 原因字段** ⇒ inbox 要的"N/A 里哪些是验证器能力不足"
只能给**启发式推测**（按算子族），并标 `inferred: True`；"Horizon 60 断崖"的精确口径**未找到定义**
⇒ 用"高复杂度定向跑批（623）vs 基线（v7）"作**粗代理**，并登记。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_escape_hotspot.md` + `.json`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "643_escape_hotspot.md")
OUT_JSON = os.path.join(ROOT, "data", "643_escape_hotspot.json")
V7 = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
RUNS = ("data/mutation_sandbox_run_622_results.json",
        "data/high_complexity_sandbox_run_623.json",
        "data/adversarial_loop_round3_sandbox_run_623.json",
        "data/cross_card_sandbox_run_624.json",
        "data/adversarial_loop_round5_624.json")
#: 语义/等价类算子族（用于 N/A 的启发式归因）
SEMANTIC_OPS = ("M5", "M6")
N_A_HINT = {"semantic": "样本可能不可判（语义等价/格式微扰）",
            "capability": "验证器能力不足候选（非语义类算子仍判 N/A）"}


def _load(path: str) -> Any:
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    try:
        return json.loads(open(p, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return None


def attribute(row: dict[str, Any]) -> tuple[str, str]:
    """单条逃逸的归因（纯函数，可用合成行测试）。"""
    nb = row.get("new_block") or []
    nw = row.get("new_warn") or []
    if row.get("equivalent"):
        return "验证器能力天花板", "该变异被标 equivalent（语义等价 ⇒ 本就不该报）"
    if row.get("replay_skipped") and row.get("verdict") == "escaped":
        return "验证器能力天花板", f"replay_skipped 非空：{row['replay_skipped']}"
    if not nb and not nw:
        return "规则缺失", "逃逸且 new_block / new_warn 均为空 ⇒ 没有任何规则对该变异有反应"
    if not nb and nw:
        return "规则太弱", f"逃逸但 new_warn 非空（{len(nw)} 条）⇒ 有反应但只到 warn"
    return "规则冲突", "逃逸且 new_block 非空（判据互相顶掉）"


def operator_hotspots() -> dict[str, Any]:
    v7 = _load(V7) or {}
    rates = v7.get("by_operator_rates", {})
    rows = []
    for op, d in sorted(rates.items()):
        esc = d.get("escape", {})
        rows.append({"op": op, "judged": d.get("judged"), "n_a": d.get("n_a"),
                     "escape_point": esc.get("point"), "cp_low": esc.get("cp_low"),
                     "cp_high": esc.get("cp_high"),
                     "numerator": esc.get("numerator")})
    rows.sort(key=lambda r: (-(r["escape_point"] or 0), r["op"]))
    return {"rows": rows}


def card_group_stats() -> dict[str, Any]:
    v7 = _load(V7) or {}
    groups: dict[str, dict[str, int]] = {}
    for card, d in (v7.get("by_card") or {}).items():
        seg = "/".join(card.split("/")[:2])       # evidence/conc 这样的域
        g = groups.setdefault(seg, {"blocked": 0, "escaped": 0, "n_a": 0, "cards": 0})
        g["blocked"] += d.get("blocked", 0)
        g["escaped"] += d.get("escaped", 0)
        g["n_a"] += d.get("n_a", 0)
        g["cards"] += 1
    out = []
    for seg, g in sorted(groups.items()):
        judged = g["blocked"] + g["escaped"]
        out.append({"group": seg, "cards": g["cards"], "blocked": g["blocked"],
                    "escaped": g["escaped"], "n_a": g["n_a"], "judged": judged,
                    "escape_rate": round(g["escaped"] / judged, 6) if judged else None,
                    "na_rate": round(g["n_a"] / (judged + g["n_a"]), 6)
                    if (judged + g["n_a"]) else None})
    out.sort(key=lambda r: -(r["escape_rate"] or 0))
    return {"rows": out}


def na_attribution() -> dict[str, Any]:
    v7 = _load(V7) or {}
    by_op = {r["op"]: r for r in operator_hotspots()["rows"]}
    semantic_na = sum((by_op[op]["n_a"] or 0) for op in SEMANTIC_OPS if op in by_op)
    total_na = sum((d.get("n_a") or 0) for d in (v7.get("by_operator_rates") or {}).values())
    return {"total_n_a": total_na, "semantic_ops": list(SEMANTIC_OPS),
            "semantic_na": semantic_na, "capability_na_hint": total_na - semantic_na,
            "variants": v7.get("variants"), "na_rate": (round(total_na / v7["variants"], 5)
                                                        if v7.get("variants") else None),
            "reason_available": False,
            "hints": dict(N_A_HINT),
            "inferred": True}


def escaped_cases() -> dict[str, Any]:
    v7 = _load(V7) or {}
    results = v7.get("results") or []
    raw = [r for r in results if r.get("verdict") == "escaped"]
    cases = []
    for r in raw:
        verdict, why = attribute(r)
        cases.append({"card": r.get("card"), "op": r.get("op"), "point": r.get("point"),
                      "equivalent": bool(r.get("equivalent")), "attribution": verdict,
                      "why": why, "reproduce": r.get("reproduce")})
    by_attr: dict[str, int] = {}
    for c in cases:
        by_attr[c["attribution"]] = by_attr.get(c["attribution"], 0) + 1
    return {"raw_escaped": len(raw), "counted_escaped": v7.get("escaped"),
            "equivalent_invalid": v7.get("equivalent_invalid"),
            "by_attribution": by_attr, "cases": cases}


def directed_runs() -> dict[str, Any]:
    """622/623/624 定向跑批的汇总（含规则冲突证据）。"""
    out = []
    for rel in RUNS:
        d = _load(rel)
        if d is None:
            out.append({"run": rel, "available": False})
            continue
        rows = d if isinstance(d, list) else (d.get("results") or d.get("rows") or [])
        if not isinstance(rows, list):
            out.append({"run": rel, "available": False})
            continue
        verd: dict[str, int] = {}
        conflict = 0
        lost = 0
        for r in rows:
            if not isinstance(r, dict):
                continue
            verd[str(r.get("verdict"))] = verd.get(str(r.get("verdict")), 0) + 1
            if r.get("lost_rules"):
                lost += 1
            if r.get("new_block_rules") and r.get("lost_rules"):
                conflict += 1
        out.append({"run": rel, "available": True, "n": len(rows), "verdicts": verd,
                    "rows_with_lost_rules": lost, "conflict_rows": conflict})
    return {"runs": out}


def assess() -> dict[str, Any]:
    return {"operators": operator_hotspots(), "card_groups": card_group_stats(),
            "na": na_attribution(), "escaped": escaped_cases(), "directed": directed_runs()}


def write_report() -> str:
    a = assess()
    ops = a["operators"]["rows"]
    esc = a["escaped"]
    na = a["na"]
    lines = [
        "# 643 B4 · 逃逸热点扫描（智能层 #4：自动发现问题）", "",
        f"> 数据源：`data/mutation/full_baseline_v7.json`（variants **{na['variants']}**、"
        f"n_a **{na['total_n_a']}**、`escaped`(计数口径) **{esc['counted_escaped']}**、"
        f"`equivalent_invalid` **{esc['equivalent_invalid']}**）+ 5 份定向跑批。", "",
        "## 一、算子的逃逸热点（按 escape 点估计降序）", "",
        "| 算子 | 可判数 | N/A | escape 点估计 | 95% CP 区间 | 分子 |", "|---|---|---|---|---|---|"]
    for r in ops:
        lo = "—" if r["cp_low"] is None else f"{r['cp_low']:.5f}"
        hi = "—" if r["cp_high"] is None else f"{r['cp_high']:.5f}"
        pt = "—" if r["escape_point"] is None else f"{r['escape_point']:.5f}"
        lines.append(f"| `{r['op']}` | {r['judged']} | {r['n_a']} | {pt} | [{lo}, {hi}] | "
                     f"{r['numerator']} |")
    lines += ["", "## 二、卡片域的逃逸/N-A 热点", "",
              "| 域 | 卡数 | blocked | escaped | N/A | 逃逸率 | N/A 率 |", "|---|---|---|---|---|---|---|"]
    for r in a["card_groups"]["rows"]:
        er = "—" if r["escape_rate"] is None else f"{r['escape_rate']:.5f}"
        nr = "—" if r["na_rate"] is None else f"{r['na_rate']:.5f}"
        lines.append(f"| `{r['group']}` | {r['cards']} | {r['blocked']} | {r['escaped']} | "
                     f"{r['n_a']} | {er} | {nr} |")
    lines += ["", "## 三、逃逸案例的归因", "",
              f"- `results[]` 里 `verdict==escaped` 原始 **{esc['raw_escaped']}** 条；"
              f"聚合计数口径 **{esc['counted_escaped']}** 条；差额 = `equivalent_invalid` "
              f"**{esc['equivalent_invalid']}** 条（语义等价被剔除）—— **两口径都报，不合并**；",
              f"- 归因分布：`{esc['by_attribution']}`", "",
              "| 卡片 | 算子 | 变异点 | equivalent | 归因 | 理由 |", "|---|---|---|---|---|---|"]
    for c in esc["cases"]:
        lines.append(f"| `{c['card']}` | {c['op']} | {c['point']} | "
                     f"{'✅' if c['equivalent'] else '—'} | **{c['attribution']}** | {c['why']} |")
    lines += ["", "## 四、N/A 的归因（**启发式**，`inferred=True`）", "",
              f"- N/A 总数 **{na['total_n_a']}**（占 variants **{na['na_rate']}**）；"
              f"其中语义类算子（{', '.join(na['semantic_ops'])}）贡献 **{na['semantic_na']}** 条；",
              f"- ⇒ 启发式拆分：**样本不可判候选 {na['semantic_na']}** / "
              f"**验证器能力不足候选 {na['capability_na_hint']}**；",
              f"- **原因字段可用性：{na['reason_available']}** ⇒ 以上拆分是**按算子族的推测**，"
              "不是逐条归因（无法逐条，因为 v7 没落盘原因）；",
              "- 两类提示口径：" + "；".join(f"`{k}`={v}" for k, v in na["hints"].items()), "",
              "## 五、定向跑批（622/623/624）的规则冲突证据", "",
              "| 跑批 | 可用 | 条数 | verdict 分布 | 含 lost_rules | 冲突行 |",
              "|---|---|---|---|---|---|"]
    for r in a["directed"]["runs"]:
        if not r["available"]:
            lines.append(f"| `{r['run']}` | ❌ | — | — | — | — |")
            continue
        lines.append(f"| `{r['run']}` | ✅ | {r['n']} | `{r['verdicts']}` | "
                     f"{r['rows_with_lost_rules']} | {r['conflict_rows']} |")
    lines += ["", "## 诚实登记", "",
              "1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：逃逸点估计的 CP 区间很宽"
              "（如 M1 的 [0.0004, 0.083]）⇒ **小样本下「热点」排序不稳**，需人复核；",
              "2. **口径差异已显式并列**：`escaped` 1 vs `verdict==escaped` 9 —— "
              "差额是语义等价剔除（`equivalent_invalid`）；本工具不替读者选口径；",
              "3. **N/A 细分是推测**（`inferred: True`）：v7 **没有** N/A 原因字段；"
              "按算子族拆只是**启发式**，且 179 条里只有 130 条在别处有原因样本（634 登记）；",
              "4. **「Horizon 60 断崖」未找到精确口径** ⇒ 用「高复杂度定向跑批（623）vs "
              "基线（v7）」作粗代理，**不等于** inbox 要的那两个复杂度区间；",
              "5. **沙箱逃逸率 ≠ 生产逃逸率**（§十二.6）：本节全部来自沙箱/受控跑批；",
              "6. 本工具**只读**：不改基线、不跑变异、不写 `data/mutation/`。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("规则缺失：new_block/new_warn 全空",
        attribute({"new_block": [], "new_warn": []})[0] == "规则缺失")
    chk("规则太弱：只有 new_warn",
        attribute({"new_block": [], "new_warn": ["X"]})[0] == "规则太弱")
    chk("能力天花板：equivalent",
        attribute({"equivalent": True, "new_block": [], "new_warn": []})[0]
        == "验证器能力天花板")
    chk("规则冲突：new_block 非空",
        attribute({"new_block": ["Y"], "new_warn": []})[0] == "规则冲突")
    chk("能力天花板优先于规则缺失（equivalent 先判）",
        attribute({"equivalent": True, "new_block": ["Y"], "new_warn": ["W"]})[0]
        == "验证器能力天花板")

    a = assess()
    chk("算子 7 个", len(a["operators"]["rows"]) == 7, str(len(a["operators"]["rows"])))
    chk("已知逃逸案例必归入（原始 9 条）", a["escaped"]["raw_escaped"] == 9,
        str(a["escaped"]["raw_escaped"]))
    chk("两口径并列（1 vs 9）",
        a["escaped"]["counted_escaped"] == 1 and a["escaped"]["raw_escaped"] == 9)
    chk("归因分类互斥且合计一致",
        sum(a["escaped"]["by_attribution"].values()) == a["escaped"]["raw_escaped"])
    chk("N/A 分类正确（语义 + 能力 = 总数）",
        a["na"]["semantic_na"] + a["na"]["capability_na_hint"] == a["na"]["total_n_a"])
    chk("N/A 标为 inferred（原因字段不可用）",
        a["na"]["inferred"] is True and a["na"]["reason_available"] is False)
    chk("卡片域分组非空", len(a["card_groups"]["rows"]) > 0)
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 B4 逃逸热点扫描")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印分析（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    a = assess()
    if x.json:
        print(json.dumps({"operators": a["operators"]["rows"][:3],
                          "escaped": {k: v for k, v in a["escaped"].items() if k != "cases"},
                          "na": a["na"]}, ensure_ascii=False, indent=2))
        return 0
    print(f"[escape-hotspot] 算子 {len(a['operators']['rows'])}；逃逸原始 "
          f"{a['escaped']['raw_escaped']}（计数口径 {a['escaped']['counted_escaped']}）⇒ "
          f"{a['escaped']['by_attribution']}；N/A {a['na']['total_n_a']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
