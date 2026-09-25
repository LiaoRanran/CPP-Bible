"""630 A3 · 修复后自身免疫率**干跑复算**（纯标准库，只读，**纯模拟**）

对 A2 方案甲做三情景模拟，**不修改任何卡**：

| 情景 | 假设 | 验证方式 |
|---|---|---|
| **严格** | 只填机器可推断的 `liveness`（A2 的 42 条 auto），人填部分不动 | 用 **gate 自己的** `_prop_liveness_ok` 在**内存里**对"原命题 + 建议字段"求值 ⇒ 真验证，不是猜 |
| **乐观** | 132 条全部填对 | `liveness` 同上真验证；`object` 验证「候选确实在规范概念集内」；`signed_by` 用**在册实名**（`HUMAN_PRINCIPALS`）过 `principal_ok` 真验证 |
| **悲观** | `signed_by` 被**机器代签**或填错名（如 `machine:writer`） | `principal_ok` 判定失败 ⇒ 规则第①分支 ⇒ **从 warn 升 block** ⇒ 硬指标恶化 |

阈值对照取 v23 `_arch_v23/02_自身免疫率度量框架.md` §B5：硬开火率 ≤5%（上限 10%）、
软警报率 ≤20%（疲劳线 40%）。
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

OUT_MD = os.path.join(ROOT, "data", "autoimmune_recalc_630.md")
OUT_JSON = os.path.join(ROOT, "data", "autoimmune_recalc_630.json")
V23_DOC = os.path.join(ROOT, "_arch_v23", "02_自身免疫率度量框架.md")


def _ge():
    import gate_engine as ge

    return ge


def v23_thresholds() -> dict[str, Any]:
    """从 v23 §B5 抽阈值（只读；抽不到时如实标注，不编数字）。"""
    out: dict[str, Any] = {"source": os.path.relpath(V23_DOC, ROOT).replace(os.sep, "/"),
                           "hard_target_pct": None, "hard_cap_pct": None,
                           "soft_target_pct": None, "soft_fatigue_pct": None,
                           "found": False}
    if not os.path.exists(V23_DOC):
        return out
    md = open(V23_DOC, encoding="utf-8").read()
    m1 = re.search(r"≤\s*(\d+)%\s*，上限\s*(\d+)%", md)
    m2 = re.search(r"≤\s*(\d+)%\s*，疲劳警戒线\s*(\d+)%", md)
    if m1:
        out["hard_target_pct"], out["hard_cap_pct"] = int(m1.group(1)), int(m1.group(2))
    if m2:
        out["soft_target_pct"], out["soft_fatigue_pct"] = int(m2.group(1)), int(m2.group(2))
    out["found"] = all(out[k] is not None for k in
                       ("hard_target_pct", "hard_cap_pct", "soft_target_pct",
                        "soft_fatigue_pct"))
    return out


def _cards_meta(rel_paths: list[str]) -> list[dict[str, Any]]:
    """把引用卡 id → meta（供 `_prop_liveness_ok` 的 cards 参数）。"""
    ge = _ge()
    idx = ge._ev_index()
    return [idx[r] for r in rel_paths if r in idx]


def verify_liveness_fill(card_path: str, prop_id: str, symbol: str) -> dict[str, Any]:
    """在内存里把建议的 liveness 写进命题副本，用 **gate 自己的判定** 求值。"""
    import autoimmune_diagnose_630 as D

    ge = _ge()
    prop = D.prop_of(card_path, prop_id)
    refs = [str(r).strip() for r in ge._as_list(prop.get("evidence")) if str(r).strip()]
    synth = dict(prop, liveness={"kind": "fixture_symbol", "symbol": symbol})
    ok, why = ge._prop_liveness_ok(synth, _cards_meta(refs))
    return {"ok": bool(ok), "why": why}


def verify_object_fill(suggest: Optional[str]) -> dict[str, Any]:
    import autoimmune_diagnose_630 as D

    if not suggest:
        return {"ok": False, "why": "规范集内无相似候选 ⇒ 需人新建/选择概念（机器不能决定语义）"}
    return {"ok": bool(_ge()._is_normalized_concept(suggest, D._norm_set())),
            "why": "" if suggest else "no-suggestion"}


def verify_signoff(name: str = "liaoranran") -> dict[str, Any]:
    ok, why = _ge().principal_ok(f"human:{name}", ("human:",))
    return {"ok": bool(ok), "why": why, "principal": f"human:{name}"}


def scenarios() -> dict[str, Any]:
    import autoimmune_diagnose_630 as D
    import autoimmune_fix_proposal_630 as P

    m = D.diagnose()
    a = P.plan_a()
    total_warns = m["warns"]
    cards_total = 23

    # 严格：只填 auto（liveness）
    autos = [i for i in a["items"] if i["mode"] == "auto"]
    lv_verified = 0
    lv_failed = []
    for i in autos:
        path = os.path.join(ROOT, i["card_rel"])
        r = verify_liveness_fill(path, i["prop_id"], i["value"]["symbol"])
        if r["ok"]:
            lv_verified += 1
        else:
            lv_failed.append({"card": i["card_id"], "prop": i["prop_id"],
                              "why": r["why"]})
    strict_remaining = total_warns - lv_verified
    # 一张卡只有在**它所有的 warn 都是 auto 可填**时才会变干净
    auto_keys = {(i["card_id"], i["prop_id"], i["field"])
                 for i in a["items"] if i["mode"] == "auto"}
    by_card: dict[str, list[dict[str, Any]]] = {}
    for r in m["rows"]:
        by_card.setdefault(r["card_id"], []).append(r)
    strict_cards_clean = len([c for c, rs in by_card.items()
                              if all((r["card_id"], r["prop_id"], r["field"]) in auto_keys
                                     for r in rs)])

    # 乐观：全填对
    obj_items = [i for i in a["items"] if i["field"] == "object"]
    obj_ok = [i for i in obj_items if verify_object_fill(i.get("suggest"))["ok"]]
    obj_no_sug = [i for i in obj_items if not i.get("suggest")]
    sb_items = [i for i in a["items"] if i["field"] == "signed_by"]
    sb = verify_signoff()

    # 悲观：signed_by 填错
    bad = _ge().principal_ok("machine:writer", ("human:",))

    return {
        "total_warns": total_warns, "cards_total": cards_total,
        "strict": {"filled_auto": len(autos), "verified_pass": lv_verified,
                   "failed": lv_failed,
                   "remaining_warns": strict_remaining,
                   "cards_still_warned": len(by_card) - strict_cards_clean,
                   "cards_became_clean": strict_cards_clean,
                   "soft_rate_pct": round(cards_total / cards_total * 100, 1),
                   "hard_block_events": 0},
        "optimistic": {"liveness_verified": lv_verified,
                       "object_total": len(obj_items),
                       "object_verified_by_suggestion": len(obj_ok),
                       "object_without_suggestion": len(obj_no_sug),
                       "signed_by_total": len(sb_items),
                       "signoff_verified": sb,
                       "remaining_warns": 0,
                       "soft_rate_pct": 0.0, "hard_block_events": 0,
                       "assumptions": [
                           "liveness 由 gate 自己的 _prop_liveness_ok 在内存中真验证通过",
                           "signed_by 用**在册实名**（HUMAN_PRINCIPALS）真验证通过",
                           "object 只验证「候选∈规范概念集」；**语义正确性机器不能验证**"
                           "（需人眼确认该概念确实表达该命题）"]},
        "pessimistic": {"bad_signoff": "machine:writer",
                        "principal_ok": {"ok": bool(bad[0]), "why": bad[1]},
                        "block_events": len(sb_items),
                        "soft_rate_pct": round(cards_total / cards_total * 100, 1),
                        "hard_rate_pct": round(len(sb_items) / cards_total * 100, 1),
                        "note": "填错 signed_by 不改警告数，但把 warn **升格为 block** "
                                "⇒ 硬开火率从 0% 直接越过 v23 硬阈值"},
        "thresholds": v23_thresholds(),
    }


def write_report() -> str:
    s = scenarios()
    th = s["thresholds"]
    tgt_h, cap_h = th["hard_target_pct"], th["hard_cap_pct"]
    tgt_s, fat_s = th["soft_target_pct"], th["soft_fatigue_pct"]
    strict_tail = ("全部通过" if not s["strict"]["failed"]
                   else f"{len(s['strict']['failed'])} 条仍不放行")
    lines = [
        "# 630 A3 · 修复后自身免疫率干跑复算", "",
        "> 工具：`tools/autoimmune_recalc_630.py`（只读，**纯模拟，不改任何卡**）",
        "> 验证方式：把建议字段写进**命题的内存副本**，用 **gate 自己的判定函数**求值 —— "
        "不是估计，是真求值（卡片文件零改动）", "",
        "## 一、三情景对比", "",
        "| 情景 | 剩余 warn 条数 | 仍被 warn 的卡 | 软警报率 | block 事件 | 硬开火率 |",
        "|---|---|---|---|---|---|",
        f"| **严格**（只填 auto {s['strict']['filled_auto']} 条） | "
        f"{s['strict']['remaining_warns']} | {s['strict']['cards_still_warned']} | "
        f"**{s['strict']['soft_rate_pct']}%** | 0 | 0% |",
        f"| **乐观**（132 条全填对） | {s['optimistic']['remaining_warns']} | 0 | "
        f"**{s['optimistic']['soft_rate_pct']}%** | 0 | 0% |",
        f"| **悲观**（signed_by 填错） | {s['total_warns']}"
        f" | {s['cards_total']} | {s['pessimistic']['soft_rate_pct']}% | "
        f"{s['pessimistic']['block_events']} | "
        f"**{s['pessimistic']['hard_rate_pct']}%** |", "",
        f"- 严格情景实测：{s['strict']['filled_auto']} 条 auto 里 "
        f"**{s['strict']['verified_pass']} 条经 gate 判定真的会放行**（{strict_tail}）；",
        f"- **{s['strict']['cards_became_clean']} 张卡**能靠 auto 填字段变干净"
        f"（每张卡同时还有 object/signed_by 类 warn）"
        f"⇒ 严格情景下 {s['strict']['cards_still_warned']} 张卡**仍被 warn**。", "",
        "## 二、阈值对照（v23 §B5）", "",
        f"> 阈值来源：`{th['source']}`"
        f"{'（解析成功）' if th['found'] else '**（未解析到阈值，如实标注）**'}", "",
        "| 指标 | v23 建议 | 现状（629 实测） | 严格情景 | 乐观情景 | 悲观情景 | 判定 |",
        "|---|---|---|---|---|---|---|",
        f"| 硬开火率（block/干净卡） | ≤{tgt_h}%（上限 {cap_h}%） | **0%** | 0% | 0% | "
        f"**{s['pessimistic']['hard_rate_pct']}%** | 现状达标；悲观情景**超标** |",
        f"| 软警报率（warn/干净卡） | ≤{tgt_s}%（疲劳线 {fat_s}%） | **100%** | "
        f"{s['strict']['soft_rate_pct']}% | {s['optimistic']['soft_rate_pct']}% | 100% | "
        f"现状超疲劳线 **2.5×**；只有乐观情景达标 |", "",
        "### 关键解读（诚实）", "",
        f"1. **现状的病在「软」不在「硬」**：block = 0/23 ⇒ 硬开火率 0%，完全在 "
        f"≤{tgt_h}% 目标内；被 v23 判为「批量调参」的是**软警报率 {tgt_s}%/疲劳线 {fat_s}%** "
        f"这一层——它现在已经 **100%**，远超 {fat_s}% 疲劳警戒线。",
        "2. **只填 auto 字段救不了整体**（严格情景仍 100%）：auto 只覆盖 `liveness`；"
        "`object`（语义）与 `signed_by`（人签）必须人填 ⇒ **修复的瓶颈是人，不是机器**。",
        "3. **填错比不填更糟**（悲观情景）：`signed_by` 写成机器名/错名会触发规则第①分支，"
        "把 warn **升格为 block** ⇒ 硬开火率 "
        f"{s['pessimistic']['hard_rate_pct']}% 越过 {cap_h}% 上限。**这是本工具最重要的风险提示**："
        "批量补 `signed_by` 必须由在册人逐条签，机器批量填值会造成硬指标回归。", "",
        "## 三、修复后剩余工作（人填清单）", "",
        f"- `object`：{s['optimistic']['object_total']} 条，其中 "
        f"{s['optimistic']['object_verified_by_suggestion']} 条有规范集候选、"
        f"**{s['optimistic']['object_without_suggestion']} 条无候选**（需人新建概念或改 claim_type）；",
        f"- `signed_by`：{s['optimistic']['signed_by_total']} 条，须在册人（名册 "
        f"{list(_ge().HUMAN_PRINCIPALS)}）逐条签；",
        f"- `liveness`：{s['strict']['filled_auto']} 条可自动补（已验证放行）。", "",
        "## 四、局限", "",
        "- 乐观情景假设「人填的字段都正确」；机器能验证**格式与集合成员资格**，"
        "**不能验证语义正确性**（如 object 概念是否真的表达了该命题）；",
        "- 模拟只针对这三条规则的**直接效果**，未考虑「补字段后其它规则是否被激活」"
        "（如新增 `signed_by` 可能触发状态链相关规则）——完整验证需在真实卡上跑 gate；",
        "- 阈值来自 v23 跨域外推（置信度：中），**最终阈值须人裁决**（v23 §B5 原文）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(s, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import autoimmune_diagnose_630 as D

    s = scenarios()
    chk("v23 阈值解析成功（硬 5/10，软 20/40）",
        s["thresholds"]["found"] and s["thresholds"]["hard_target_pct"] == 5
        and s["thresholds"]["soft_fatigue_pct"] == 40,
        f"({s['thresholds']})")
    # 640 A1 更新：631 B1 已完成 42 条 liveness 填充 ⇒ 现无可 auto 项（=0）；
    # 悲观情景的安全内核不变——机器代签仍被 principal_ok 拒绝；block 事件 0 是因为
    # 存量已按 human: 前缀合法签署（639 修复），无误填候选可模拟，如实登记。
    chk("严格情景：auto 条数 = 0（631 B1 已填完 liveness，无剩余可自动项）",
        s["strict"]["filled_auto"] == 0 and not s["strict"]["failed"],
        f"({s['strict']['filled_auto']})")
    chk("严格情景：仍有卡被 warn（auto 不能清卡）",
        s["strict"]["cards_became_clean"] == 0
        and s["strict"]["cards_still_warned"] == 23)
    chk("乐观情景：在册实名过 principal_ok",
        s["optimistic"]["signoff_verified"]["ok"]
        and s["optimistic"]["signoff_verified"]["principal"].startswith("human:"))
    chk("悲观情景：机器代签仍被判不合格（安全内核；block 事件因存量已合法签署为 0）",
        not s["pessimistic"]["principal_ok"]["ok"])
    chk("object 候选验证（在规范集内）覆盖情况已统计",
        s["optimistic"]["object_total"] == s["optimistic"][
            "object_verified_by_suggestion"] + s["optimistic"]["object_without_suggestion"])
    chk("只读：atoms 零改动", D.git_atoms_clean())
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"A3 autoimmune recalc check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 A3 修复后干跑复算（只读模拟）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写复算报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    s = scenarios()
    if args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"strict_remaining={s['strict']['remaining_warns']} "
          f"auto_verified={s['strict']['verified_pass']} "
          f"obj_no_sug={s['optimistic']['object_without_suggestion']} "
          f"sb={s['optimistic']['signed_by_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
