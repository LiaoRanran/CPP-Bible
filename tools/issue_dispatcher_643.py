"""643 B5 · **问题分发器**（智能层联调：把 B1–B4 合成统一问题清单 + Top 10）。

**定位**：B1–B4 各自出"线索"，本工具把它们**归一化**成同一张问题清单，按可复算的优先级排序，
输出 **Top 10** 与每个问题的**建议下一步**（生成新攻击 / 提新规则 / 人审 / 补数据）。

**统一 schema**：`{issue_id, source, kind, target, severity, impact, cost, score, next_step, why}`
- `severity`：0=提示 / 1=低 / 2=中 / 3=高（按问题类别的**性质**定，口径见 `SEVERITY`）
- `impact`：**受影响对象数**（卡/规则/向量），来自各扫描器的实测计数
- `cost`：修复成本档 1=低（改阈值/补文档）/ 2=中（提规则草案）/ 3=高（改架构或需跨批）
- **`score = severity × impact / cost`** —— 刻意**把严重度放进公式**：
  637 的已知缺陷正是"`score = 收益/成本 × 风险系数` **不含严重度** ⇒ 优先级倒挂"
  （637 `loop_quality_audit.md` §四·附 实测两轮都出现）。本工具是**对该缺陷的显式修法**。

**下一步映射**（kind → next_step，机械）：
`rule_missing/rule_weak → 提新规则草案(D)` · `escape/deep_low → 生成新攻击(C)` ·
`rule_hot/rule_dead → 人审(E2/人)` · `missing_dimension → 补数据(人)` · `coverage_gap → 人审(B1)`

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_issue_list.md` + `.json`。
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

import attack_gap_scanner_643 as B2  # noqa: E402
import autoimmune_hotspot_scanner_643 as B3  # noqa: E402
import coverage_gap_scanner_643 as B1  # noqa: E402
import escape_hotspot_scanner_643 as B4  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_issue_list.md")
OUT_JSON = os.path.join(ROOT, "data", "643_issue_list.json")
TOP_N = 10

SEVERITY = {
    "card_no_rule_hit": 2, "block_rule_zero_hit": 2, "rule_single_card": 1,
    "card_over_hit": 1, "attack_underrun": 3, "attack_structural_only": 2,
    "rule_dead": 2, "rule_inapplicable": 2, "rule_too_hot": 1, "rule_too_narrow": 1,
    "escape_rule_missing": 3, "escape_rule_weak": 3, "escape_capability": 1,
    "na_capability": 2, "missing_dimension": 2, "card_group_hotspot": 2,
}
NEXT_STEP = {
    "card_no_rule_hit": "人审（B1：确认真盲区还是卡太干净）",
    "block_rule_zero_hit": "人审（B1：规则空转 vs 卡全合规）",
    "rule_single_card": "人审（B1：是否过拟合到单卡）",
    "card_over_hit": "人审（B1：规则冗余/噪声）",
    "attack_underrun": "生成新攻击（C2 定向变异）",
    "attack_structural_only": "生成新攻击（C2 定向变异）",
    "rule_dead": "人审 + 可能退役（E2 老化检测）",
    "rule_inapplicable": "人审（E2：收紧/退役）",
    "rule_too_hot": "人审（E2：升 block 或收窄）",
    "rule_too_narrow": "人审（E2：条件是否写死）",
    "escape_rule_missing": "提新规则草案（D2）",
    "escape_rule_weak": "提规则修改草案（D2：收紧/升 block）",
    "escape_capability": "人审（可能是能力天花板，不该自动化）",
    "na_capability": "生成新攻击（C2：补 N/A 面的可判别变异）",
    "missing_dimension": "补数据（人：落盘缺该维度）",
    "card_group_hotspot": "生成新攻击（C2：打该卡片域）",
}


def issue(source: str, kind: str, target: str, impact: int, cost: int,
          why: str) -> dict[str, Any]:
    sev = SEVERITY.get(kind, 1)
    score = round(sev * max(impact, 1) / max(cost, 1), 4)
    return {"issue_id": f"{source}:{kind}:{target}", "source": source, "kind": kind,
            "target": target, "severity": sev, "impact": impact, "cost": cost,
            "score": score, "next_step": NEXT_STEP.get(kind, "人审"), "why": why}


def collect() -> list[dict[str, Any]]:
    """把 B1–B4 的输出归一化成问题清单（含数据缺口类）。"""
    out: list[dict[str, Any]] = []

    # B1 覆盖盲区（按 kind 聚合，避免 44 条 block 零命中刷屏 ⇒ impact 记条数）
    a1 = B1.report()["analysis"]
    for kind, lst in (("card_no_rule_hit", a1["cards_no_rule_hit"]),
                      ("block_rule_zero_hit", a1["block_rules_zero_hit"]),
                      ("rule_single_card", a1["rules_single_card"]),
                      ("card_over_hit", a1["cards_over_10_rules"])):
        if lst:
            out.append(issue("B1", kind, f"共{len(lst)}项", len(lst), 1,
                             f"覆盖盲区：{'、'.join(lst[:5])}"
                             f"{' …' if len(lst) > 5 else ''}"))

    # B2 攻击面
    a2 = B2.assess()
    if a2["untouched"]:
        out.append(issue("B2", "attack_underrun", f"共{len(a2['untouched'])}向量",
                         len(a2["untouched"]), 2,
                         "深度 0（未触达）：" + "、".join(a2["untouched"])))
    if a2["only_structural"]:
        out.append(issue("B2", "attack_structural_only",
                         f"共{len(a2['only_structural'])}向量", len(a2["only_structural"]), 2,
                         "深度 1（仅结构性探针，未证明拦住）："
                         + "、".join(a2["only_structural"])))
    if a2["risky_low_depth"]:
        out.append(issue("B2", "attack_structural_only",
                         f"高风险低深度共{len(a2['risky_low_depth'])}向量",
                         len(a2["risky_low_depth"]), 1,
                         "risk=high 且深度 ≤1：" + "、".join(a2["risky_low_depth"])))

    # B3 自身免疫
    a3 = B3.assess()
    bv = a3["by_verdict"]
    for verdict, kind in (("退役候选", "rule_dead"), ("不适用候选", "rule_inapplicable"),
                          ("收紧候选", "rule_too_hot"), ("放宽候选", "rule_too_narrow")):
        if bv.get(verdict):
            out.append(issue("B3", kind, f"共{bv[verdict]}规则", bv[verdict], 1,
                             f"自身免疫热点「{verdict}」{bv[verdict]} 条"))
    if a3["unavailable"]:
        out.append(issue("B3", "missing_dimension", "每规则判决级别统计",
                         len(a3["unavailable"]), 2,
                         "数据缺口：" + "；".join(a3["unavailable"])))

    # B4 逃逸
    a4 = B4.assess()
    for attr, kind in (("规则缺失", "escape_rule_missing"), ("规则太弱", "escape_rule_weak"),
                       ("验证器能力天花板", "escape_capability")):
        n = a4["escaped"]["by_attribution"].get(attr, 0)
        if n:
            out.append(issue("B4", kind, f"共{n}案例", n, 2 if kind != "escape_capability" else 1,
                             f"逃逸归因「{attr}」{n} 条"))
    if a4["na"]["capability_na_hint"]:
        out.append(issue("B4", "na_capability", "N/A 能力不足候选",
                         int(a4["na"]["capability_na_hint"]), 2,
                         "N/A 启发式拆分出的「验证器能力不足候选」条数（inferred）"))
    hot_groups = [g for g in a4["card_groups"]["rows"]
                  if (g["escape_rate"] or 0) > 0]
    if hot_groups:
        out.append(issue("B4", "card_group_hotspot",
                         f"共{len(hot_groups)}域", len(hot_groups), 2,
                         "逃逸率 >0 的卡片域：" + "、".join(g["group"] for g in hot_groups)))
    return out


def dedup(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """按 `issue_id` 去重（保留 impact 更大的那条）；再按 score 降序。"""
    best: dict[str, dict[str, Any]] = {}
    for it in items:
        cur = best.get(it["issue_id"])
        if cur is None or it["impact"] > cur["impact"]:
            best[it["issue_id"]] = it
    return sorted(best.values(), key=lambda x: (-x["score"], x["issue_id"]))


def dispatch() -> dict[str, Any]:
    items = dedup(collect())
    return {"issues": items, "n": len(items), "top": items[:TOP_N],
            "by_source": {s: sum(1 for i in items if i["source"] == s)
                          for s in ("B1", "B2", "B3", "B4")},
            "by_next_step": _count(items, "next_step"),
            "formula": "score = severity × impact / cost（**含严重度**，修 637 倒挂缺陷）",
            "notes": ["impact 是实测计数，cost 是**人工档位**（1/2/3），severity 是按类别的**性质**定档",
                      "优先级**不按出现次数**，按 `severity × impact / cost`"]}


def _count(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    d: dict[str, int] = {}
    for it in items:
        d[str(it[key])] = d.get(str(it[key]), 0) + 1
    return d


def write_report() -> str:
    d = dispatch()
    lines = [
        "# 643 B5 · 问题分发器（智能层联调：统一清单 + Top 10）", "",
        f"> 公式：`{d['formula']}`",
        f"> 合并后 **{d['n']}** 条问题（来源分布 `{d['by_source']}`）。", "",
        "## 一、Top 10（按 score 降序）", "",
        "| # | 来源 | 类别 | 对象 | severity | impact | cost | score | 建议下一步 |",
        "|---|---|---|---|---|---|---|---|---|"]
    for i, it in enumerate(d["top"], 1):
        lines.append(f"| {i} | {it['source']} | `{it['kind']}` | {it['target']} | "
                     f"{it['severity']} | {it['impact']} | {it['cost']} | **{it['score']}** | "
                     f"{it['next_step']} |")
    lines += ["", "### 1.1 Top 10 的逐条理由", ""]
    for i, it in enumerate(d["top"], 1):
        lines.append(f"{i}. **{it['source']}/{it['kind']}**（{it['target']}）：{it['why']}")
    lines += ["", "## 二、全量清单", "",
              "| 来源 | 类别 | 对象 | severity | impact | cost | score | 下一步 |",
              "|---|---|---|---|---|---|---|---|"]
    for it in d["issues"]:
        lines.append(f"| {it['source']} | `{it['kind']}` | {it['target']} | {it['severity']} | "
                     f"{it['impact']} | {it['cost']} | {it['score']} | {it['next_step']} |")
    lines += ["", "## 三、按下一步分组", "",
              f"- `{d['by_next_step']}`", "",
              "## 诚实登记", "",
              "1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：Top 10 是**线索排序**，需人复核；",
              "2. **优先级公式含人工档位**：`severity` 按类别定档、`cost` 是人工 1/2/3 档 ⇒ "
              "公式**可复算**但**未被历史数据校准**（与 642 C1 的 score 同性质）；",
              "3. **`impact` 用实测计数**（条数/向量数/规则数），但**不同 kind 的 impact 量纲不同**"
              "（卡 vs 规则 vs 向量）⇒ 跨 kind 比较 score 只有**粗排序**意义；",
              "4. **刻意把严重度放进公式**是为了修 637 的优先级倒挂（实测两轮都出现）——"
              "本工具**未**回溯修正 637/638 的历史排序（那是改历史结论，不做）；",
              "5. 本工具**只读**：不跑 B1–B4 的写盘入口（只调其纯函数/assess），不生成攻击、不提规则。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    a = issue("B4", "escape_rule_missing", "x", 3, 2, "w")
    chk("公式含严重度", a["score"] == round(3 * 3 / 2, 4), str(a["score"]))
    b = issue("B4", "escape_rule_missing", "x", 3, 2, "w")
    # 637 的倒挂缺陷：不含严重度时"低成本小问题"会压过"高严重度问题"。这里必须相反：
    chk("高严重度 × 中面 > 低严重度 × 大面",
        issue("X", "escape_rule_missing", "t", 3, 1, "")["score"]
        > issue("X", "rule_single_card", "t", 5, 1, "")["score"])
    chk("成本高 ⇒ score 低",
        issue("X", "escape_rule_missing", "t", 5, 3, "")["score"]
        < issue("X", "escape_rule_missing", "t", 5, 1, "")["score"])
    chk("impact 下限保护（0 也按 1 算）", issue("X", "rule_single_card", "t", 0, 1, "")
        ["score"] == 1.0)
    chk("未知 kind ⇒ 默认档 + 人审", issue("X", "zzz", "t", 1, 1, "")["next_step"] == "人审")

    chk("去重：同 issue_id 只留一条", len(dedup([a, b])) == 1)
    chk("去重保留 impact 更大者",
        dedup([a, {**b, "impact": 9}])[0]["impact"] == 9)

    d = dispatch()
    chk("Top 10 非空", len(d["top"]) > 0 and len(d["top"]) <= TOP_N, str(len(d["top"])))
    chk("合并无重复", len({i["issue_id"] for i in d["issues"]}) == d["n"])
    chk("优先级降序正确",
        all(d["issues"][i]["score"] >= d["issues"][i + 1]["score"]
            for i in range(len(d["issues"]) - 1)))
    chk("四来源都有条目", all(v > 0 for v in d["by_source"].values()), str(d["by_source"]))
    chk("数据缺口类 issue 在册",
        any(i["kind"] == "missing_dimension" for i in d["issues"]))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 B5 问题分发器")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印清单（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    d = dispatch()
    if x.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(f"[issue-dispatcher] {d['n']} 条 ⇒ Top{len(d['top'])}；来源 {d['by_source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
