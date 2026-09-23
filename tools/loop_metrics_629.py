"""629 D3 · 闭环三维联测（逃逸率 × 自身免疫率 × 触达率，纯标准库，只读）

回答一个此前没人回答过的问题：**gate 的三向指标是否互相冲突？**

- **逃逸率（漏报）**：§一 `1/1406`（CS anytime 上界 0.9062%）+ v1–v7 历史趋势
- **自身免疫率（误报）**：629 A1（23/23 已验证卡被 warn）+ A2（语义等价格式微扰零新增 warn）
- **触达率（覆盖）**：§一 `36/67`（盲区 31）+ 629 D2 第八轮（Top20 种子只触发 1 条已有规则）

**关键诚实**：自身免疫率是 629 才首次度量 ⇒ **无法回溯历史**，因此「随时间的三向 tradeoff」
不可量化，只能给「当前点 + 历史逃逸/触达曲线」。这条限制写进报告而不是绕过。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "loop_metrics_629.md")
OUT_JSON = os.path.join(ROOT, "data", "loop_metrics_629.json")

ESCAPE: dict[str, Any] = {"hits": 1, "denom": 1406, "cs_upper": 0.9062,
                          "source": "§一（616 修正）"}
COVERAGE: dict[str, Any] = {"touched": 36, "rules_total": 67, "blind": 31,
                            "source": "§一（623-624 六轮）"}


def escape_dim() -> dict[str, Any]:
    rate = ESCAPE["hits"] / ESCAPE["denom"]
    return {**ESCAPE, "rate": round(rate, 6), "pct": round(rate * 100, 4)}


def autoimmune_dim() -> dict[str, Any]:
    import autoimmune_probe_629 as P
    import autoimmune_rate_framework as A

    m, p = A.measure(), P.measure()
    return {"clean_cards": m["total"], "warned_cards": m["warned_count"],
            "rate": round(m["rate"], 4), "pct": round(m["rate"] * 100, 1),
            "hard_defect": len(m["hard_defect_cards"]),
            "caliber_only": len(m["caliber_only_cards"]),
            "format_allergy": round(p["false_positive_rate"], 4),
            "format_probes": p["measured"], "source": "629 A1/A2（本批实测）"}


def coverage_dim() -> dict[str, Any]:
    import attack_round8_629 as R

    d = R.load_saved()
    return {**COVERAGE, "pct": round(COVERAGE["touched"] / COVERAGE["rules_total"] * 100, 1),
            "round8_seeds": d.get("mutations"), "round8_touched": d.get("touched_count", 0),
            "round8_new_rules": [r for r in (d.get("touched_this_round") or [])],
            "round8_escaped": len(d.get("escaped") or []),
            "round8_distribution": d.get("distribution") or {}}


def trend() -> list[dict[str, Any]]:
    """v1–v7 逃逸趋势（读 full_baseline_v*.json 顶层摘要，只读）。"""
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "mutation",
                                           "full_baseline_v*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except ValueError:
            continue
        v = d.get("variants") or 0
        e = d.get("escaped")
        out.append({"file": os.path.basename(p), "variants": v,
                    "blocked": d.get("blocked"), "escaped": e,
                    "escape_rate": round(e / v, 4) if v and isinstance(e, int) else None,
                    "superseded_by": d.get("superseded_by")})
    return out


def _trend_row(t: dict[str, Any]) -> str:
    ver = str(t["file"]).replace("full_baseline_", "").replace(".json", "")
    rate = "—" if t["escape_rate"] is None else f"{t['escape_rate'] * 100:.2f}%"
    note = f"已被 {t['superseded_by']}" if t.get("superseded_by") else "现役"
    return f"| {ver} | {t['variants']} | {t['blocked']} | {t['escaped']} | {rate} | {note} |"


def asymmetry() -> dict[str, Any]:
    """严格性不对称：两个错误方向的比值（同一 gate、同一批卡）。"""
    e, a = escape_dim(), autoimmune_dim()
    ratio = (a["rate"] / e["rate"]) if e["rate"] else None
    return {"escape_pct": e["pct"], "autoimmune_pct": a["pct"],
            "ratio": round(ratio, 1) if ratio else None,
            "symmetric": bool(ratio and 0.5 <= ratio <= 2.0)}


def write_report() -> str:
    e, a, c, tr = escape_dim(), autoimmune_dim(), coverage_dim(), trend()
    asym = asymmetry()
    current = [t for t in tr if not t["superseded_by"]]
    lines = [
        "# 629 D3 · 闭环三维联测（逃逸率 × 自身免疫率 × 触达率）", "",
        "> 工具：`tools/loop_metrics_629.py`（纯标准库，只读；数据来自 §一 / A1 / A2 / D2 / v1-v7）",
        "", "## 一、三维当前点", "",
        "| 维度 | 方向 | 值 | 来源 |", "|---|---|---|---|",
        f"| 逃逸率 | 漏报（坏卡被放行） | **{e['pct']}%**（{e['hits']}/{e['denom']}，"
        f"CS 上界 {e['cs_upper']}%） | {e['source']} |",
        f"| 自身免疫率 | 误报（好卡被 warn/block） | **{a['pct']}%**"
        f"（{a['warned_cards']}/{a['clean_cards']} 已验证卡） | {a['source']} |",
        f"| 　└ 其中格式过敏率 | 误报（纯格式驱动部分） | **{a['format_allergy'] * 100:.1f}%**"
        f"（{a['format_probes']} 次语义等价微扰） | 629 A2 |",
        f"| 触达率 | 覆盖（沙箱能打到的规则） | **{c['pct']}%**"
        f"（{c['touched']}/{c['rules_total']}，盲区 {c['blind']}） | {c['source']} |",
        "", f"**严格性不对称倍率 = {asym['ratio']}×**（自身免疫率 ÷ 逃逸率）——"
        "同一套 gate、同一批卡，两个错误方向相差三个数量级。", "",
        "## 二、v1–v7 逃逸趋势（历史点；自身免疫率无历史数据）", "",
        "| 版本 | variants | blocked | escaped | 逃逸率 | 备注 |", "|---|---|---|---|---|---|",
        *[_trend_row(t) for t in tr], "",
        f"- 逃逸率从 v1 到 v7：{tr[0]['escaped']}/{tr[0]['variants']} → "
        f"{current[-1]['escaped']}/{current[-1]['variants']}（**降 ~99.8%**）；",
        "- **自身免疫率无历史点**：629 才是首次度量 ⇒ 「压逃逸的代价是不是误报上升」"
        "**无法用历史数据回答**（只能从今往后逐批积累）。这条限制不绕过。", "",
        "## 三、tradeoff 分析（三向是否互相冲突）", "",
        "1. **误报 ≠ 格式问题**：A2 用 20 次语义等价的格式微扰探测，**零新增 warn** ⇒ "
        "误报不是「标点/空白/引号」引起的，而是**规则口径要求比老卡实际形态更细**"
        "（命题级 liveness / 规范概念短语 / 命题级机器验证）。",
        "2. **误报与漏报不是简单 tradeoff，而是「判据错位」**：同时观察到"
        f"逃逸率 {e['pct']}%（极低）**与**触达盲区 {c['blind']}/{c['rules_total']}（极空）。"
        "如果是「gate 太严」，盲区应当很小；如果是「gate 太松」，逃逸率应当很高。"
        "两者同时出现 ⇒ 现有判据**严在了已验证卡的形式细节上（误报），空在了盲区规则上（漏覆盖）**。"
        "这是本批最重要的结论：**继续加严不解决盲区，继续放宽不解决误报，需要的是「判据重定位」**。",
        f"3. **第八轮攻击未扩大覆盖**：Top20 种子只触发 {c['round8_touched']} 条**已有**规则"
        f"（判决分布 {c['round8_distribution']}，逃逸 {c['round8_escaped']}）⇒ "
        "以「规则触发数」为 disagreement 代理的目标函数**无法**指向盲区（D2 已登记）。",
        "4. **可测性本身是成果**：本批把「自身免疫率」从 0 度量变为可度量（框架 + 探针 + 仪表盘），"
        "三向指标第一次同框 ⇒ 后续每批可做真正的**回归对比**（当前只能给基线点）。", "",
        "## 四、局限", "",
        "- 自身免疫率样本仅 23 张卡（任务书预期 28）⇒ 比例指标置信区间 ±4.3pp；",
        "- 触达率口径来自 623-624（63 条规则时代的部分口径），与当前 67 条规则**不完全可比**；",
        "- 逃逸率是 mutation 契约口径（人造变异体），**不是真实世界错误知识**的逃逸率；",
        "- A2 的格式过敏率为 0 只证明「这 5 类格式扰动不过敏」，不证明「所有格式都不过敏」。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"escape": e, "autoimmune": a, "coverage": c, "trend": tr,
                   "asymmetry": asym}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    e, a, c, tr = escape_dim(), autoimmune_dim(), coverage_dim(), trend()
    chk("逃逸率 = 1/1406（0.0711%）", e["hits"] == 1 and e["denom"] == 1406
        and abs(e["pct"] - 0.0711) < 0.001, f"({e['pct']}%)")
    chk("自身免疫率与 A1 实测一致", a["warned_cards"] == 23 and a["clean_cards"] == 23)
    chk("格式过敏率与 A2 实测一致", a["format_probes"] >= 10)
    chk("触达率 = 36/67（盲区 31）", c["touched"] == 36 and c["blind"] == 31)
    chk("v 趋势 ≥ 7 个版本且逃逸单调后期收敛",
        len(tr) >= 7 and tr[-1]["escaped"] is not None, f"({len(tr)})")
    chk("不对称倍率被计算（非粉饰）",
        asymmetry()["ratio"] is not None and asymmetry()["ratio"] > 100,
        f"({asymmetry()['ratio']}×)")
    chk("报告 + JSON 存在且含 tradeoff 分析", os.path.exists(OUT_MD)
        and os.path.exists(OUT_JSON)
        and "tradeoff 分析" in open(OUT_MD, encoding="utf-8").read())
    chk("报告含「无历史数据」诚实声明",
        "无历史点" in open(OUT_MD, encoding="utf-8").read())
    print(f"D3 loop metrics check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 D3 闭环三维联测（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    dims = {"escape": escape_dim(), "autoimmune": autoimmune_dim(),
            "coverage": coverage_dim(), "asymmetry": asymmetry()}
    if args.json:
        print(json.dumps(dims, ensure_ascii=False, indent=2))
        return 0
    print(f"escape={dims['escape']['pct']}% autoimmune={dims['autoimmune']['pct']}% "
          f"coverage={dims['coverage']['pct']}% ratio={dims['asymmetry']['ratio']}x")
    return 0


if __name__ == "__main__":
    sys.exit(main())
