"""643 B3 · **自身免疫热点扫描器**（智能层：自动发现问题 #3）。

**定位**：找出"**规则自己在制造噪声**"的热点（自身免疫病）：太严的、该升 block 的、
不适用的、空转的，给出**收紧/放宽/拆分/退役**建议。**只出建议，不改规则**。

**每规则指标（全部来自在册数据、可复算）**：

| 指标 | 来源 | 含义 |
|---|---|---|
| `severity` | `gate_engine.RULES` | 规则声明的级别（block/warn/advice） |
| `live_hits` / `live_by_sev` | 现算 `gate_engine.run()` | 当前命中数与级别混合 |
| `touched_rounds` / 6 | `data/vfdr_report_v2_624.json` 热力图 | 在 6 轮变异跑批里被触达的轮数 |
| `exempt_rate` | `mdl_gate_642.exempt_rate()` | **未触达轮次占比**（642 口径，可复算） |
| `known_error_rate` / `is_proxy` | `calibration_tracker_642` | 错误率（**当前 67/67 为代理**） |

**分类判据（阈值可复算；边界已测）**：

| 建议 | 判据 |
|---|---|
| **退役候选** | `touched_rounds == 0` 且 `live_hits == 0`（从没触达、当前也不报） |
| **不适用候选** | `exempt_rate ≥ 0.30`（642 的豁免率阈值）且非退役 |
| **收紧候选** | `live_hits ≥ 10` 且 `severity == "advice"`（常报却只是建议 ⇒ 要么升 warn、要么收窄） |
| **放宽候选** | `touched_rounds ≥ 4` 且 `live_hits == 0`（在变异场里很活跃、现网不报 ⇒ 条件可能写死） |
| 观察 | 其余 |

**⚠️ 数据缺口（如实登记）**：inbox 想要的"**warn 率 >50%**""**block 率 =0 但 warn 率高**"
需要**每规则的逐次判决级别统计**，而现有落盘数据（624 只到"轮次 × 规则是否触达"，
630/631 只到向量级）**没有**这一维 ⇒ 本工具**不编造**：把它作为 `unavailable` 明确列出，
并交由 B5 作为"**数据缺口类 issue**"上报。这本身是智能层照出的第一条真缺陷。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_autoimmune_hotspot.md` + `.json`。
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

import calibration_tracker_642 as ct  # noqa: E402
import gate_engine as ge  # noqa: E402
import mdl_gate_642 as mg  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_autoimmune_hotspot.md")
OUT_JSON = os.path.join(ROOT, "data", "643_autoimmune_hotspot.json")
VFDR = os.path.join(ROOT, "data", "vfdr_report_v2_624.json")
EXEMPT_THRESHOLD = 0.30      # 与 642 一致
LIVE_HOT = 10                # 常报阈值
ACTIVE_ROUNDS = 4            # 变异场活跃阈值


def heatmap() -> dict[str, dict[str, bool]]:
    try:
        data: dict[str, Any] = json.loads(open(VFDR, encoding="utf-8").read())
        hm: dict[str, dict[str, bool]] = data.get("heatmap", {})
        return hm
    except (OSError, json.JSONDecodeError):
        return {}


def classify(severity: str, live_hits: int, touched: int, exempt: Optional[float],
             rounds_total: int) -> tuple[str, str]:
    """(建议, 理由)。判据顺序固定，阈值可复算。"""
    if touched == 0 and live_hits == 0:
        return "退役候选", "从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规）"
    if exempt is not None and exempt >= EXEMPT_THRESHOLD:
        return "不适用候选", (f"豁免率 {exempt:.3f} ≥ {EXEMPT_THRESHOLD}（未触达 "
                            f"{rounds_total - touched}/{rounds_total} 轮）⇒ 规则可能不适用")
    if live_hits >= LIVE_HOT and severity == "advice":
        return "收紧候选", f"当前命中 {live_hits} ≥ {LIVE_HOT} 却只是 advice ⇒ 升 warn 或收窄条件"
    if touched >= ACTIVE_ROUNDS and live_hits == 0:
        return "放宽候选", (f"变异场触达 {touched}/{rounds_total} 轮但当前零命中"
                          f" ⇒ 条件可能写死到特定变异形态")
    return "观察", "指标未越阈"


def assess() -> dict[str, Any]:
    hm = heatmap()
    rounds_total = max((len(v) for v in hm.values()), default=6)
    finds = ge.run(include_advice=True)
    live: dict[str, dict[str, int]] = {}
    for f in finds:
        row = live.setdefault(f.rule_id, {})
        row[f.severity] = row.get(f.severity, 0) + 1
    tracker = ct.build_tracker().snapshot()
    stats = {r["rule_id"]: r for r in tracker["rows"]}

    rows: list[dict[str, Any]] = []
    for r in ge.RULES:
        rid = r.id
        hit_sev = live.get(rid, {})
        live_hits = sum(hit_sev.values())
        touched = sum(1 for v in hm.get(rid, {}).values() if v)
        exempt = mg.exempt_rate(rid, hm)
        verdict, why = classify(r.severity, live_hits, touched, exempt, rounds_total)
        st = stats.get(rid, {})
        rows.append({"rule_id": rid, "title": r.title, "severity": r.severity,
                     "live_hits": live_hits, "live_by_sev": hit_sev,
                     "touched_rounds": touched, "rounds_total": rounds_total,
                     "exempt_rate": exempt, "in_heatmap": rid in hm,
                     "known_error_rate": st.get("known_error_rate"),
                     "is_proxy": st.get("is_proxy"),
                     "verdict": verdict, "why": why})
    by_verdict: dict[str, int] = {}
    for rw in rows:
        by_verdict[rw["verdict"]] = by_verdict.get(rw["verdict"], 0) + 1
    return {"rows": rows, "n_rules": len(rows), "by_verdict": by_verdict,
            "rounds_total": rounds_total,
            "thresholds": {"exempt_rate": EXEMPT_THRESHOLD, "live_hot": LIVE_HOT,
                           "active_rounds": ACTIVE_ROUNDS},
            "proxied_rules": sum(1 for r in rows if r["is_proxy"]),
            "unavailable": [
                "每规则的 **warn 率**（需逐次判决级别统计 ⇒ 现有落盘数据无此维）",
                "每规则的 **block 率**（同上 ⇒ 无法判'block 率=0 但 warn 率高'）",
                "每规则的**误报率趋势**（需时序标签 ⇒ 只有 1/1406 的逃逸样本）",
            ]}


def write_report() -> str:
    a = assess()
    rows = a["rows"]
    hot = [r for r in rows if r["verdict"] != "观察"]
    lines = [
        "# 643 B3 · 自身免疫热点扫描（智能层 #3：自动发现问题）", "",
        f"> 规模：**{a['n_rules']} 条规则**；阈值：豁免率 ≥ {EXEMPT_THRESHOLD}、"
        f"常报 ≥ {LIVE_HOT}、变异场活跃 ≥ {ACTIVE_ROUNDS}/{a['rounds_total']} 轮。",
        f"> 代理初值：**{a['proxied_rules']}/{a['n_rules']} 条规则**的 `known_error_rate` 仍是代理"
        "（642 实测：全库无自身样本）⇒ 本工具**不用它做判据**，只展示。", "",
        "## 一、热点清单（非'观察'条目）", "",
        "| 规则 | 声明级别 | 当前命中 | 触达轮数 | 豁免率 | known_error_rate | 建议 | 理由 |",
        "|---|---|---|---|---|---|---|---|"]
    for r in sorted(hot, key=lambda x: (x["verdict"], -x["live_hits"], x["rule_id"])):
        ker = r["known_error_rate"]
        ex_s = "—" if r["exempt_rate"] is None else f"{r['exempt_rate']:.3f}"
        proxy = "（代理）" if r["is_proxy"] else ""
        ker_s = "—" if ker is None else f"{ker:.4f}{proxy}"
        lines.append(f"| `{r['rule_id']}` | {r['severity']} | {r['live_hits']} | "
                     f"{r['touched_rounds']}/{r['rounds_total']} | {ex_s} | {ker_s} | "
                     f"**{r['verdict']}** | {r['why']} |")
    if not hot:
        lines.append("| — | — | — | — | — | — | 零条目 | — |")
    lines += ["", "## 二、建议分布", "",
              f"- `{a['by_verdict']}`", "",
              "## 三、四类建议的逐条清单", ""]
    for v in ("退役候选", "不适用候选", "收紧候选", "放宽候选"):
        ids = [r["rule_id"] for r in rows if r["verdict"] == v]
        lines.append(f"- **{v}**（{len(ids)}）："
                     + (", ".join(f"`{i}`" for i in ids) if ids else "（无）"))
    lines += ["", "## 四、⚠️ 数据缺口（inbox 要求但**现有数据无法支撑**）", ""]
    for u in a["unavailable"]:
        lines.append(f"- {u}")
    lines += ["", "> 这三项**不是漏做**，而是**落盘数据缺该维度**：智能层照出的第一条真缺陷。",
              "> 已作为 issue 交给 B5（`missing_dimension` 类）。", "",
              "## 诚实登记", "",
              "1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：分类是**启发式**，"
              "`退役候选` 也可能是「卡全合规」（好事）⇒ 必须人审；",
              "2. **`known_error_rate` 全是代理**（67/67）⇒ 本工具**不**用它做判据，"
              "只作展示；用它下结论等于自己骗自己；",
              "3. **豁免率是 642 口径**（热力图未触达轮次占比），反映的是「变异场里没打到」，"
              "不等于「生产里没用」—— 两种含义已并列展示，交集才建议退役；",
              "4. 阈值（0.30 / 10 / 4）沿用 642 既有值或本批新定，**属经验值**，"
              "边界已在单测里固定，改阈值会改变分类结果；",
              "5. **不改任何规则**：本工具只读 `gate_engine.RULES`、不写规则库、不重钉台账。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"by_verdict": a["by_verdict"], "thresholds": a["thresholds"],
                   "proxied_rules": a["proxied_rules"], "unavailable": a["unavailable"],
                   "rows": [{k: r[k] for k in ("rule_id", "severity", "live_hits",
                                               "touched_rounds", "exempt_rate", "verdict")}
                            for r in rows]}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("退役：从未触达且零命中", classify("warn", 0, 0, 1.0, 6)[0] == "退役候选")
    chk("不适用：豁免率越阈", classify("warn", 1, 1, 0.50, 6)[0] == "不适用候选")
    chk("收紧：常报但只是 advice", classify("advice", 12, 3, 0.10, 6)[0] == "收紧候选")
    chk("放宽：变异场活跃但零命中", classify("block", 0, 5, 0.10, 6)[0] == "放宽候选")
    chk("观察：未越阈", classify("block", 2, 3, 0.10, 6)[0] == "观察")
    chk("阈值边界：豁免率恰好 0.30 判不适用",
        classify("warn", 1, 1, 0.30, 6)[0] == "不适用候选")
    chk("阈值边界：命中恰好 10 且 advice 判收紧",
        classify("advice", 10, 1, 0.10, 6)[0] == "收紧候选")
    chk("阈值边界：触达恰好 4 判放宽", classify("block", 0, 4, 0.10, 6)[0] == "放宽候选")

    a = assess()
    chk("66+ 规则在册", a["n_rules"] == 67, str(a["n_rules"]))
    chk("建议分布自洽", sum(a["by_verdict"].values()) == a["n_rules"])
    chk("数据缺口登记非空", len(a["unavailable"]) >= 3)
    chk("known_error_rate 全代理（不据它下判）",
        a["proxied_rules"] == 67, str(a["proxied_rules"]))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 B3 自身免疫热点扫描")
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
        print(json.dumps({"by_verdict": a["by_verdict"], "unavailable": a["unavailable"],
                          "thresholds": a["thresholds"]}, ensure_ascii=False, indent=2))
        return 0
    print(f"[autoimmune] {a['n_rules']} 规则 ⇒ {a['by_verdict']}；"
          f"数据缺口 {len(a['unavailable'])} 项")
    return 0


if __name__ == "__main__":
    sys.exit(main())
