"""630 C3 · 自身免疫率**阈值对照**（纯标准库，只读）

把 v23 `_arch_v23/02_自身免疫率度量框架.md` §B5 的**分级阈值建议**与本批实测摆在一张表上，
并给出**紧迫度评估**与**v23 建议动作**的映射。**阈值是建议，最终由人裁决**（v23 原文）。

v23 的两个分子（本工具严格区分，这是解读的关键）：
- **硬开火率** = 被 block 的干净卡 ÷ 干净卡（"发病"指标）
- **软警报率** = 被 warn 的干净卡 ÷ 干净卡（"库存宽度"指标）
- 外加 **库存误伤面** = 在已知正确语料上**触发任意规则**的比例（v23 建议 2）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "autoimmune_threshold_630.md")
OUT_JSON = os.path.join(ROOT, "data", "autoimmune_threshold_630.json")
V23_DOC = os.path.join(ROOT, "_arch_v23", "02_自身免疫率度量框架.md")

DEFAULTS = {"hard_target": 5, "hard_cap": 10, "soft_target": 20, "soft_fatigue": 40}


def v23() -> dict[str, Any]:
    """解析 v23 §B5 的阈值与外部依据（抽不到就标注，不编数字）。"""
    out: dict[str, Any] = {"source": os.path.relpath(V23_DOC, ROOT).replace(os.sep, "/"),
                           "found": False, **{k: None for k in DEFAULTS},
                           "external_basis": {}, "actions": []}
    if not os.path.exists(V23_DOC):
        return out
    md = open(V23_DOC, encoding="utf-8").read()
    m1 = re.search(r"≤\s*(\d+)%\s*，上限\s*(\d+)%", md)
    m2 = re.search(r"≤\s*(\d+)%\s*，疲劳警戒线\s*(\d+)%", md)
    if m1:
        out["hard_target"], out["hard_cap"] = int(m1.group(1)), int(m1.group(2))
    if m2:
        out["soft_target"], out["soft_fatigue"] = int(m2.group(1)), int(m2.group(2))
    out["found"] = all(out[k] is not None for k in DEFAULTS)
    for k, pat in (("Google 测试 flaky", r"Google：约 \*\*(\d+)%"),
                   ("Meta 单测 flakiness", r"单元测试 flakiness\*\*远低于 (\d+)%"),
                   ("SOC 成熟团队误报率", r"误报率 \*\*<(\d+-\d+)%\*\*"),
                   ("SOC 平均误报占比", r"平均 \*\*(\d+)%\*\*告警为误报"),
                   ("支付硬拦目标", r"只挡 <(\d+\.\d+)% 合法交易"),
                   ("免疫库自反应存量", r"自反应细胞库存 (\d+-\d+)%")):
        m = re.search(pat, md)
        if m:
            out["external_basis"][k] = m.group(1) + "%"
    for line in md.splitlines():                     # §建议 3 的动作映射表
        if line.startswith("| ") and ("开火率" in line or "警报率" in line
                                     or "重判" in line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2:
                out["actions"].append({"observation": cells[0],
                                       "action": cells[1].replace("**", "")})
    return out


def measured() -> dict[str, Any]:
    """实测三元：硬开火率 / 软警报率 / 库存误伤面（数据来自 629 A1 框架，只读）。"""
    import autoimmune_rate_framework as F

    m = F.measure()
    total = max(m["total"], 1)
    return {"cards": m["total"], "hard_block_cards":
            sum(1 for r in m["cards"] if r["block"]),
            "soft_warn_cards": m["warned_count"],
            "inventory_hit_cards": len([r for r in m["cards"]
                                        if r["warn"] or r["block"] or r["advice"]]),
            "hard_rate_pct": round(sum(1 for r in m["cards"] if r["block"]) / total * 100, 1),
            "soft_rate_pct": round(m["warned_count"] / total * 100, 1),
            "inventory_rate_pct": round(len([r for r in m["cards"]
                                             if r["warn"] or r["block"] or r["advice"]])
                                        / total * 100, 1),
            "caliber_cards": len(m["caliber_only_cards"]),
            "hard_defect_cards": len(m["hard_defect_cards"])}


def compare() -> dict[str, Any]:
    v, me = v23(), measured()
    th = {k: (v[k] if v[k] is not None else DEFAULTS[k]) for k in DEFAULTS}
    hard_ratio = (me["hard_rate_pct"] / th["hard_target"]) if th["hard_target"] else None
    soft_ratio = (me["soft_rate_pct"] / th["soft_target"]) if th["soft_target"] else None
    fatigue_ratio = (me["soft_rate_pct"] / th["soft_fatigue"]) if th["soft_fatigue"] else None
    return {"thresholds": {**th, "found": v["found"], "source": v["source"]},
            "external_basis": v["external_basis"], "actions": v["actions"],
            "measured": me, "hard_ratio": hard_ratio, "soft_ratio": soft_ratio,
            "fatigue_ratio": fatigue_ratio,
            "verdict": {
                "hard": ("达标" if me["hard_rate_pct"] <= th["hard_target"] else
                         ("越上限" if me["hard_rate_pct"] > th["hard_cap"] else "越目标")),
                "soft": ("达标" if me["soft_rate_pct"] <= th["soft_target"] else
                         ("**超疲劳线**" if me["soft_rate_pct"] > th["soft_fatigue"]
                          else "超目标")),
            },
            "urgency": ("高——软警报率已超疲劳线，按 v23 §建议3 应触发"
                        "「批量调参/合并该层规则」；但硬开火率 0%，"
                        "**不要动 block 层**（硬指标是健康的）")}


def write_report() -> str:
    c = compare()
    th, me, v = c["thresholds"], c["measured"], c["verdict"]
    lines = [
        "# 630 C3 · 自身免疫率阈值对照（实测 vs v23 建议）", "",
        "> 工具：`tools/autoimmune_threshold_630.py`（只读；实测取自 629 A1 框架）",
        f"> 阈值来源：`{th['source']}`"
        f"{'（解析成功）' if th['found'] else '**（未解析到，使用工具内置默认值）**'}", "",
        "## 一、对照表", "",
        "| 指标 | v23 建议 | 实测（630） | 倍数 | 判定 |", "|---|---|---|---|---|",
        f"| **硬开火率**（block/干净卡） | ≤{th['hard_target']}%（上限 {th['hard_cap']}%） | "
        f"**{me['hard_rate_pct']}%**（{me['hard_block_cards']}/{me['cards']}） | "
        f"{c['hard_ratio']:.2f}× | **{v['hard']}** |",
        f"| **软警报率**（warn/干净卡） | ≤{th['soft_target']}%（疲劳线 {th['soft_fatigue']}%） | "
        f"**{me['soft_rate_pct']}%**（{me['soft_warn_cards']}/{me['cards']}） | "
        f"{c['soft_ratio']:.2f}× 目标 / {c['fatigue_ratio']:.2f}× 疲劳线 | **{v['soft']}** |",
        f"| 库存误伤面（触发任意规则） | v23：**允许较高**（照 5-20% / Google 16% flaky） | "
        f"**{me['inventory_rate_pct']}%** | ≥5× 参照上限 | 需监控（单调上升即回归） |", "",
        "## 二、外部依据（v23 摘录）", "",
        "| 来源 | 数值 |", "|---|---|",
        *[f"| {k} | {val} |" for k, val in c["external_basis"].items()],
        "", "## 三、紧迫度评估", "",
        f"**{c['urgency']}**", "",
        "关键区分（v23 §B5 建议 1 的两个分子）：", "",
        f"- **硬指标健康**：block = {me['hard_block_cards']}/{me['cards']} ⇒ 硬开火率 "
        f"{me['hard_rate_pct']}%，在 ≤{th['hard_target']}% 目标内 ⇒ **不要动 block 层规则**；",
        f"- **软指标超标**：warn = {me['soft_warn_cards']}/{me['cards']} ⇒ 软警报率 "
        f"{me['soft_rate_pct']}%，是目标的 {c['soft_ratio']:.1f} 倍、疲劳线的 "
        f"{c['fatigue_ratio']:.2f} 倍 ⇒ 按 v23 应**批量调参该层规则**；",
        f"- 其中 {me['caliber_cards']} 张是**命题级口径**造成（630 A1 诊断），"
        f"{me['hard_defect_cards']} 张是硬缺陷 ⇒ 修复方向明确（A2 方案甲）。", "",
        "## 四、v23 建议动作映射", "",
        "| v23 观测 | v23 建议动作 | 当前命中 |", "|---|---|---|",
        *[f"| {a['observation']} | {a['action']} | "
          f"{'**是**' if ('40%' in a['observation'] and me['soft_rate_pct'] > th['soft_fatigue']) or ('≤5%' in a['observation'] and me['hard_rate_pct'] <= th['hard_target']) else '否'} |"
          for a in c["actions"]], "",
        "## 五、诚实登记", "",
        "- 阈值是**跨域外推的先验**（v23 置信度：中），本节只做对照，**不代人裁决**；",
        "- 「库存误伤面」的参照（5-20% 免疫库自反应 / 16% Google flaky）来自**异构系统**，"
        "迁移到知识验证系统只有类比意义；",
        "- 本工具**不改任何规则、不改任何卡**；软层调参属于 A2 方案乙（本批只出方案）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    c = compare()
    th, me = c["thresholds"], c["measured"]
    chk("v23 阈值解析成功（5/10/20/40）", th["found"]
        and (th["hard_target"], th["hard_cap"]) == (5, 10)
        and (th["soft_target"], th["soft_fatigue"]) == (20, 40), f"({th})")
    chk("外部依据已摘录（≥3 条）", len(c["external_basis"]) >= 3,
        f"({list(c['external_basis'])})")
    chk("v23 动作映射已摘录", bool(c["actions"]), f"({len(c['actions'])})")
    chk("硬开火率 × 干净卡数自洽",
        me["hard_block_cards"] == 0 and me["hard_rate_pct"] == 0.0)
    chk("软警报率 = warn 卡数 ÷ 干净卡数",
        abs(me["soft_rate_pct"] - me["soft_warn_cards"] / me["cards"] * 100) < 0.05,
        f"({me['soft_rate_pct']}%)")
    chk("判定：硬达标 + 软超疲劳线",
        c["verdict"]["hard"] == "达标" and "超疲劳线" in c["verdict"]["soft"])
    chk("紧迫度明确要求不动 block 层",
        "不要动 block 层" in c["urgency"])
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"C3 autoimmune threshold check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 C3 自身免疫率阈值对照（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    c = compare()
    if args.json:
        print(json.dumps(c, ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"hard={c['measured']['hard_rate_pct']}% soft={c['measured']['soft_rate_pct']}% "
          f"verdict={c['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
