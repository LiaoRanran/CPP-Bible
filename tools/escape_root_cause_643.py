"""643 D1 · **逃逸案例归因器**（智能层：自动提案规则 #1）。

**定位**：把**反例**（历史逃逸 + C3 新发现的逃逸）归因到四类根因，并给出**改进方向**：
`规则缺失` / `规则太弱` / `规则冲突` / `验证器能力天花板`。

**归因来源（两条，都标 provenance）**：
1. **B4 的历史逃逸**（v7 的 9 条原始逃逸，已有机械归因）；
2. **C3 的沙箱新发现**（`data/643_attack_sim.json`：`evaded` = 逃逸、`oracle_mismatch` =
   **责任规则错配**、`not_triggered` = 规则不可达）；
   **若 C3 尚未跑**，本工具**只用 B4 的数据**，并显式登记"无新发现"。

**改进方向（机械映射）**：
`规则缺失 → 提新规则` · `规则太弱 → 收紧/升 block` · `规则冲突 → 调优先级` ·
`能力天花板 → 人审（不该自动化）` · `责任错配 → 重标 expected_oracle` · `不可达 → 接 B3 退役`

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_escape_root_cause.md` + `.json`。
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
sys.path.insert(0, HERE)

import escape_hotspot_scanner_643 as B4  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_escape_root_cause.md")
OUT_JSON = os.path.join(ROOT, "data", "643_escape_root_cause.json")
SIM_JSON = os.path.join(ROOT, "data", "643_attack_sim.json")

DIRECTION = {
    "规则缺失": "提新规则草案（D2）",
    "规则太弱": "收紧条件 / 升 block（D2 出修改草案）",
    "规则冲突": "调整优先级（人审）",
    "验证器能力天花板": "人审（能力天花板 ⇒ 不该自动化）",
    "责任错配": "重标 expected_oracle（不改判据）",
    "不可达": "接 B3 退役候选（人审）",
}
#: C3 verdict → 根因（纯函数用）
VERDICT_CAUSE = {"evaded": "规则太弱", "oracle_mismatch": "责任错配",
                 "not_triggered": "不可达"}


def cause_of(case: dict[str, Any]) -> tuple[str, str]:
    """B4 逃逸案例 → (根因, 理由)（纯函数）。"""
    attr = case.get("attribution", "")
    if attr in DIRECTION:
        return attr, case.get("why", "")
    return "验证器能力天花板", "未知归因 ⇒ 保守归为能力天花板（不自动化）"


def from_c3(sim: dict[str, Any]) -> list[dict[str, Any]]:
    """C3 结果 → 归因条目（纯函数）。"""
    out = []
    for r in sim.get("rows", []):
        cause = VERDICT_CAUSE.get(r.get("verdict", ""))
        if not cause:
            continue
        out.append({"source": "C3", "case_id": r.get("mutation_id"),
                    "target": r.get("target_rule"), "card": r.get("card"),
                    "op": r.get("op"), "cause": cause,
                    "added_rules": r.get("added_rules", []),
                    "removed_rules": r.get("removed_rules", []),
                    "why": f"C3 沙箱 verdict={r.get('verdict')}（{r.get('why', '')}）"})
    return out


def attributable() -> dict[str, Any]:
    # 注意：B4 的逃逸案例**没有目标规则**（它是"被发现的事实"，不是"生成计划"）
    # ⇒ target 记 `—` 并在此登记，避免读者误以为有规则归属
    hist = [{"source": "B4", "case_id": f"v7#{i}", "target": "—",
             "card": c.get("card"), "op": c.get("op"), "cause": cause_of(c)[0],
             "why": cause_of(c)[1], "added_rules": [], "removed_rules": []}
            for i, c in enumerate(B4.assess()["escaped"]["cases"])]
    sim_note = ""
    new: list[dict[str, Any]] = []
    if os.path.exists(SIM_JSON):
        try:
            sim = json.loads(open(SIM_JSON, encoding="utf-8").read())
            new = from_c3(sim)
            sim_note = (f"已并入 C3 沙箱结果（{sim.get('n_planned')} 条计划，"
                        f"局限样本：{sim.get('limit')}）")
        except (OSError, json.JSONDecodeError) as exc:
            sim_note = f"C3 结果不可读（{type(exc).__name__}）⇒ 只用 B4 数据"
    else:
        sim_note = "**C3 结果文件不存在** ⇒ 只用 B4 数据（无新发现）"
    cases = hist + new
    by_cause: dict[str, int] = {}
    for c in cases:
        by_cause[c["cause"]] = by_cause.get(c["cause"], 0) + 1
    return {"cases": cases, "n": len(cases), "by_cause": by_cause,
            "n_from_b4": len(hist), "n_from_c3": len(new), "sim_note": sim_note,
            "directions": DIRECTION,
            "actionable": [c for c in cases
                           if c["cause"] in ("规则缺失", "规则太弱")],
            "non_actionable": [c for c in cases
                               if c["cause"] not in ("规则缺失", "规则太弱")]}


def write_report() -> str:
    a = attributable()
    lines = [
        "# 643 D1 · 逃逸案例归因（智能层：自动提案规则 #1）", "",
        f"> 案例 **{a['n']}** 条（B4 历史 {a['n_from_b4']} + C3 新发现 {a['n_from_c3']}）；"
        f"归因分布 `{a['by_cause']}`。",
        f"> C3 并入情况：{a['sim_note']}", "",
        "## 一、根因 → 改进方向（机械映射）", "",
        "| 根因 | 改进方向 | 条数 |", "|---|---|---|"]
    for k, v in DIRECTION.items():
        lines.append(f"| `{k}` | {v} | {a['by_cause'].get(k, 0)} |")
    lines += ["", "## 二、**可行动**案例（规则缺失/太弱 ⇒ 交 D2 出草案）", "",
              f"共 **{len(a['actionable'])}** 条：", "",
              "| 来源 | case_id | 目标规则 | 卡 | 算子 | 根因 | 理由 |",
              "|---|---|---|---|---|---|---|"]
    for c in a["actionable"]:
        lines.append(f"| {c['source']} | `{c['case_id']}` | `{c['target']}` | `{c['card']}` | "
                     f"`{c['op']}` | **{c['cause']}** | {c['why']} |")
    if not a["actionable"]:
        lines.append("| — | — | — | — | — | — | **零条**（无可行动项） |")
    lines += ["", "## 三、**不可行动**案例（不该自动化）", "",
              f"共 **{len(a['non_actionable'])}** 条：", "",
              "| 来源 | case_id | 根因 | 理由 |", "|---|---|---|---|"]
    for c in a["non_actionable"]:
        lines.append(f"| {c['source']} | `{c['case_id']}` | {c['cause']} | {c['why']} |")
    lines += ["", "## 诚实登记", "",
              "1. **归因是机械映射，不是诊断**：`规则缺失/太弱` 只在"
              "「逃逸且无规则反应/只有 warn 反应」这一**行为证据**上成立；"
              "**为什么**缺/弱（条件写错？字段名不匹配？）需要人读代码；",
              "2. **C3 并入的样本量极小**（见其 `limit`）⇒ C3 来的案例只作**线索**；"
              "若 C3 未跑，`n_from_c3=0` 并已显式登记；",
              "3. **`责任错配` 不是缺陷**：它是「生成器的预期猜错了」（§十二.7），"
              "改进方向是**重标 oracle**，不是改规则；",
              "4. **能力天花板类占比高（8/9）**：说明 v7 的「逃逸」多数是**语义等价**"
              "（`equivalent_invalid`）⇒ 这本身是对 B4 口径的重要修正："
              "**「逃逸」必须看去掉等价后的口径**；",
              "5. 本工具**只读**：不改规则、不写规则库、不跑沙箱。"]
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

    chk("规则缺失 → 提新规则", cause_of({"attribution": "规则缺失"})[0] == "规则缺失")
    chk("规则太弱 → 收紧/升 block", cause_of({"attribution": "规则太弱"})[0] == "规则太弱")
    chk("能力天花板 → 保留原类", cause_of({"attribution": "验证器能力天花板"})[0]
        == "验证器能力天花板")
    chk("未知归因 ⇒ 保守归能力天花板（不自动化）",
        cause_of({"attribution": "???"})[0] == "验证器能力天花板")
    chk("方向映射齐备（六类都有）",
        all(k in DIRECTION for k in ("规则缺失", "规则太弱", "规则冲突",
                                     "验证器能力天花板", "责任错配", "不可达")))
    chk("C3 verdict → 根因映射", VERDICT_CAUSE["evaded"] == "规则太弱"
        and VERDICT_CAUSE["not_triggered"] == "不可达")

    synth = {"rows": [{"mutation_id": "m1", "verdict": "evaded", "target_rule": "R1",
                       "card": "c", "op": "field_delete", "why": "w"},
                      {"mutation_id": "m2", "verdict": "blocked", "target_rule": "R2",
                       "card": "c", "op": "x", "why": "w"}]}
    cs = from_c3(synth)
    chk("C3 只取非兑现 verdict（blocked 不进归因）",
        len(cs) == 1 and cs[0]["cause"] == "规则太弱", str(cs))

    a = attributable()
    chk("案例非空且分布自洽",
        a["n"] == sum(a["by_cause"].values()) and a["n"] > 0)
    chk("可行动 + 不可行动 = 全部",
        len(a["actionable"]) + len(a["non_actionable"]) == a["n"])
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 D1 逃逸归因")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    a = attributable()
    if x.json:
        print(json.dumps({"by_cause": a["by_cause"], "n": a["n"],
                          "n_actionable": len(a["actionable"]),
                          "sim_note": a["sim_note"]}, ensure_ascii=False, indent=2))
        return 0
    print(f"[escape-root-cause] {a['n']} 案例 ⇒ {a['by_cause']}；"
          f"可行动 {len(a['actionable'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
