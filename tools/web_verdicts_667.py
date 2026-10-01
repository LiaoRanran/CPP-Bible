#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_verdicts_667.py — 667 阶段2：给前端「状态仪表盘 + 判决历史表格 + 数据对比表」提供**现算**数据。

目标
====
667 阶段2 要求前端有三样东西：① 大数字仪表盘（通过率/逃逸率/卡数）② 判决历史表格（时间倒序 +
状态色标 + 筛选排序）③ 数据对比表。**三者都不许写死数字**，所以数字必须先由本工具现算落成 JSON。

数据源（全部现场复算，不抄写）
============================
| 字段 | 来源 |
|---|---|
| 卡数 / 草稿 | `counts_659.ATOMS_REAL` / `ATOMS_DRAFT`（扫 `atoms/`） |
| 规则数 | `len(gate_engine.RULES)`（与 `data/_gate_rules.json` 同源） |
| holdout 检出率 | `data/holdout_reveal_3_665.json::error_subset` **现算**；并与 `web/data/metrics_666.json` 的**落盘值**比对 ⇒ 漂移可见 |
| external 检出率 | `data/external_corpus_reveal_665.json`，**分母算两遍**（32 与 40）并同时给出 |
| 逃逸率 / 保护器 | `web/data/status.json`（616 冻结契约；保护器镜像自拆仓） |
| 账本事件 | `data/646_authority_rule_annotation.jsonl` 非空行数（红线：只读） |
| 判决历史 | `data/cards_665/index_665.json`（16 张机器卡）+ `data/defect_injection_661.json`（15 条缺陷夹具） |
| 反事实 F1 | `data/counterfactual_cases_665.json`（**只登记，不入仪表盘**：见 `excluded`） |

边界（诚实边界，不是免责声明）
============================
1. **判决历史只有 31 条**（16 + 15）。holdout 30 条与外部 corpus 40 条**没有逐条结果落盘**
   （产物里只有聚合数）⇒ 本工具把它们登记进 `excluded`，**不伪造逐条行**。这是 667 阶段0
   认定的 P1 缺陷（M0-A3），本工具不替它遮掩。
2. **反事实 10 条有逐条预测，但算子已改、产物未重跑**（产物 F1=0.0，论文写 1.0/20 条）⇒
   同样进 `excluded` 与 `drift`，**不进仪表盘**。
3. 本工具**只读**；`--write` 只写 `web/data/verdicts_667.json` 一个文件。
4. 拿不到的项记 `null` 并进 `unavailable`，**不用占位值冒充**。

用法
====
    python tools/web_verdicts_667.py --selftest   # 自检（数据源可达 / 字段齐全 / 漂移可见）
    python tools/web_verdicts_667.py --check      # 只读：现算 vs 已落盘（漂移可见）
    python tools/web_verdicts_667.py --write      # 写 web/data/verdicts_667.json
    python tools/web_verdicts_667.py --json       # 打印现算结果（不写盘）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT = os.path.join(ROOT, "web", "data", "verdicts_667.json")
LEDGER = os.path.join(ROOT, "data", "646_authority_rule_annotation.jsonl")
METRICS_666 = os.path.join(ROOT, "web", "data", "metrics_666.json")

#: verdict（检测器语义）→ 四态（判决语义）。**色标只认四态**，不认 verdict 字面量。
VERDICT_STATE: dict[str, str] = {
    "catch": "pass",
    "measure": "pass_with_exception",
    "miss": "fail",
    "unknown": "unknown",
}
STATE_LABEL: dict[str, str] = {
    "pass": "pass · 通过",
    "pass_with_exception": "pass_with_exception · 带例外通过",
    "fail": "fail · 不通过",
    "unknown": "unknown · 未知",
}


def _json(rel: str) -> dict[str, Any]:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        data: dict[str, Any] = json.load(fh)
        return data


def _count_lines(path: str) -> int:
    if not os.path.isfile(path):
        return -1
    with open(path, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ln in fh if ln.strip())


def _pct(num: float, den: float) -> float | None:
    """比率现算；分母为 0 ⇒ None（**不返回 0.0 冒充**）。"""
    if not den:
        return None
    return round(num / den * 100, 1)


def _day(value: str | None, fallback: str) -> str:
    """把可能带时分秒的时间戳收敛到 `YYYY-MM-DD`；空值用来源文件的日期。"""
    if not value:
        return fallback
    return str(value)[:10] if len(str(value)) >= 10 else fallback


# ── 判决历史（逐条）──────────────────────────────────────────────────────────
def collect_verdicts() -> tuple[list[dict[str, Any]], list[str]]:
    """从**有逐条结果**的产物里抽判决记录；没有逐条结果的一律不进表（登记到 excluded）。"""
    rows: list[dict[str, Any]] = []
    excluded: list[str] = []

    # ① 665 B1 机器卡：16 张，逐张有 verdict / four_state / measured_at
    try:
        ig = _json("data/cards_665/index_665.json")
        day = str(ig.get("generated_at") or "")[:10] or "—"
        for c in ig.get("cards") or []:
            v = str(c.get("verdict") or "unknown")
            rows.append({
                "id": str(c.get("id") or "—"),
                "source": "ig_cards_665",
                "source_label": "机器卡（665 B1）",
                "when": _day(c.get("measured_at"), day),
                "verdict": v,
                "state": str(c.get("four_state") or VERDICT_STATE.get(v, "unknown")),
                "detector": str(c.get("detector") or "—"),
                "expect": str(c.get("expect") or "—"),
                "detail": str(c.get("support_reason") or c.get("note") or "")[:160],
                "repro": "python tools/ig_cards_665.py --check",
            })
    except Exception as e:  # noqa: BLE001
        excluded.append(f"data/cards_665/index_665.json：{e}")

    # ② 661 缺陷夹具：15 条，逐条有 status / caught
    try:
        di = _json("data/defect_injection_661.json")
        day = str(di.get("generated_at") or "")[:10] or "—"
        for r in di.get("results") or []:
            status = str(r.get("status") or "")
            caught = r.get("caught")
            if status == "reinjectable" and caught is True:
                st, v = "pass", "catch"
            elif status == "reinjectable" and caught is False:
                st, v = "fail", "miss"
            else:
                st, v = "unknown", "not_reinjectable"
            rows.append({
                "id": str(r.get("id") or "—"),
                "source": "defect_injection_661",
                "source_label": "缺陷夹具（661）",
                "when": day,
                "verdict": v,
                "state": st,
                "detector": "gate",
                "expect": "catch",
                "detail": str(r.get("note") or r.get("gate") or "")[:160],
                "repro": "python tools/defect_injection_661.py",
            })
    except Exception as e:  # noqa: BLE001
        excluded.append(f"data/defect_injection_661.json：{e}")

    # ③ 反事实：有逐条预测，但**算子已改、产物未重跑** ⇒ 只登记，不进表
    excluded.append(
        "data/counterfactual_cases_665.json：产物仍是改判据前的算子（10 条，F1=0.0），"
        "与论文 v0.4 的「20 条 / F1=1.0 上界」不一致 ⇒ 重跑前不进判决历史表"
    )
    # ④ holdout / external：只有聚合，无逐条 ⇒ 不进表（M0-A3 待办）
    excluded.append(
        "data/holdout_reveal_3_665.json 与 data/external_corpus_reveal_665.json："
        "产物只有聚合计数，**无逐条 verdict** ⇒ 不进判决历史表（667 阶段0 登记的 P1 缺陷）"
    )

    rows.sort(key=lambda r: (r["when"], r["source"], r["id"]), reverse=True)   # 时间倒序
    for i, r in enumerate(rows):
        r["seq"] = i
        r["state_label"] = STATE_LABEL.get(r["state"], r["state"])
    return rows, excluded


# ── 数据对比表（口径差 / 漂移都在这里**显形**，不允许静默）─────────────────────
def collect_compare(dash: dict[str, Any], drift: list[dict[str, Any]]) -> list[dict[str, Any]]:
    h = dash.get("holdout") or {}
    e = dash.get("external") or {}
    rows: list[dict[str, Any]] = []

    if h.get("stored_rate_pct") is not None and h.get("rate_pct") is not None:
        rows.append({
            "metric": "holdout 检出率",
            "left": f"{h['stored_rate_pct']}%（落盘 {h.get('stored_catch')}/{h.get('stored_den')}）",
            "right": f"{h['rate_pct']}%（现算 {h.get('catch')}/{h.get('den')}）",
            "kind": "drift" if h.get("drift") else "ok",
            "note": "落盘值来自 web/data/metrics_666.json；现算值来自 holdout_reveal_3_665.json。"
                    "两者不一致 ⇒ 667 阶段0 P0 缺陷，需人裁决（重跑 reveal 或作废旧值）。",
        })
    if e.get("rate_pct") is not None:
        rows.append({
            "metric": "外部语料检出率",
            "left": f"{e['rate_pct']}%（分母 {e.get('den')} = catch+miss）",
            "right": f"{e.get('rate_pct_all')}%（分母 {e.get('total')} = 全部样本）",
            "kind": "caliber",
            "note": "两个分母都合法，**必须写明用哪个**。产物与前端此前只写「40 条」，读者会误算。",
        })
    mu = dash.get("mutation") or {}
    rows.append({
        "metric": "内部变异率",
        "left": f"on_scored：core {mu.get('core')}% / all {mu.get('all')}%",
        "right": f"全部变异体：core {mu.get('core_all')}% / all {mu.get('all_all')}%",
        "kind": "caliber",
        "note": "**两种分母差 22.5pp / 24.1pp**（on_scored 的分母排除了未评分变异体）。"
                "656 报告的 62.5%→97.3% 变化里，一部分就是口径换挡。两者都报，且一律不作缺陷检测率。",
    })
    rows.append({
        "metric": "卡数",
        "left": f"{dash.get('cards_real')} 实卡 + {dash.get('cards_draft')} 草稿 = {dash.get('cards_total')}",
        "right": f"atoms/**/*.md = {dash.get('atoms_md_files')} 个文件",
        "kind": "caliber",
        "note": "48 是 md 文件数（含 atoms/README.md），47 才是卡数（counts_659 口径）。",
    })
    rows.append({
        "metric": "逃逸率",
        "left": f"{dash.get('escape', {}).get('rate_pct')}%（{dash.get('escape', {}).get('escaped')}/{dash.get('escape', {}).get('denominator')}）",
        "right": f"variants {dash.get('escape', {}).get('variants')} / blocked {dash.get('escape', {}).get('blocked')}",
        "kind": "frozen",
        "note": "616 冻结契约（v7 基线漏检率）。**不是**本书真实错误率，不可与检出率并列当能力证据。",
    })
    # 668：反事实是"上界"而不是"能力"——单独一行讲清分母与同源问题
    try:
        c = _json("data/counterfactual_cases_665.json")
        sc = c.get("scores") or {}
        rows.append({
            "metric": "反事实算子 P/R/F1",
            "left": f"P={sc.get('precision')} R={sc.get('recall')} F1={sc.get('f1')}",
            "right": f"分母 {c.get('cases_total')} 条（第三判据命中 {(c.get('third_criterion') or {}).get('hit_count')}）",
            "kind": "caliber",
            "note": "**上界**：真值标签与第三判据同源（都按『是否平台测量』判），且 n=10 时 "
                    "95% CI 约 ±30pp。660 的另 10 条**无真值标签**，不计入分母。",
        })
    except Exception as e:  # noqa: BLE001
        rows.append({"metric": "反事实算子 P/R/F1", "left": "读取失败", "right": str(e)[:60],
                     "kind": "drift", "note": "产物不可用"})
    for d in drift:
        rows.append({
            "metric": f"漂移 · {d['field']}",
            "left": f"落盘 {d['stored']}",
            "right": f"现算 {d['fresh']}",
            "kind": "drift",
            "note": d["note"],
        })
    return rows


# ── 仪表盘 ───────────────────────────────────────────────────────────────────
def collect() -> dict[str, Any]:
    """现算全部指标；任何一项拿不到 ⇒ 记 null 并进 `unavailable`，不猜。"""
    unavailable: list[str] = []
    import counts_659 as counts  # noqa: E402
    import gate_engine as ge  # noqa: E402

    dash: dict[str, Any] = {}
    dash["cards_real"] = counts.ATOMS_REAL
    dash["cards_draft"] = counts.ATOMS_DRAFT
    dash["cards_total"] = counts.ATOMS_TOTAL
    dash["atoms_md_files"] = sum(
        1 for d, _, fs in os.walk(os.path.join(ROOT, "atoms")) for f in fs if f.endswith(".md")
    )
    dash["rules_total"] = len(ge.RULES)
    dash["propositions"] = counts.PROPOSITIONS

    # holdout：**现算** + 与落盘比对（漂移可见 —— 666 的 --check 没查这两个字段）
    hold: dict[str, Any] = {}
    try:
        # 672h（W3 扩样）：切到第 5 轮产物（可测 41）；旧 3_665（16）只作历史
        r5 = _json("data/holdout_reveal_5_672h.json")
        cum5 = r5.get("cumulative", {})
        sub = cum5.get("error_subset", {})
        catch, miss, unknown = int(sub.get("catch", 0)), int(sub.get("miss", 0)), int(sub.get("unknown", 0))
        hold = {
            "rate_pct": sub.get("detect_rate_pct"),
            "catch": catch, "miss": miss, "unknown": unknown,
            "den": catch + miss,
            "samples": int(cum5.get("labels", {}).get("error", 0)),
            "denominator": "catch+miss（可测；unknown 不计）",
            "caliber": str(r5.get("honest_note") or r5.get("caliber") or "产物未声明口径"),
            "source": "data/holdout_reveal_5_672h.json",
        }
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"holdout_reveal_5_672h.json：{e}")
    try:
        m6 = _json("web/data/metrics_666.json")
        s = (m6.get("metrics") or {}).get("holdout") or {}
        hold["stored_rate_pct"] = s.get("rate_pct")
        hold["stored_catch"] = s.get("catch")
        hold["stored_den"] = (s.get("catch") or 0) + (s.get("miss") or 0)
        hold["drift"] = (hold.get("rate_pct") != s.get("rate_pct"))
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"metrics_666.json：{e}")
    dash["holdout"] = hold

    # external：**分母算两遍**
    ext: dict[str, Any] = {}
    try:
        # 672h（W3 扩样）：切到 corpus 第 4 轮产物（可测 64）
        r = _json("data/external_corpus_reveal_672h.json").get("cumulative", {})
        catch, miss = int(r.get("catch", 0)), int(r.get("miss", 0))
        ext = {
            "rate_pct": r.get("detect_rate_pct"),
            "rate_pct_all": _pct(catch, int(r.get("total", 0)) or 0),
            "catch": catch, "miss": miss,
            "unknown": int(r.get("unknown", 0)), "not_error": int(r.get("not_error", 0)),
            "total": int(r.get("total", 0)),
            "den": catch + miss,
            "denominator": "catch+miss（unknown 与 not_error 都排除）",
            "source": "data/external_corpus_reveal_672h.json",
        }
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"external_corpus_reveal_672h.json：{e}")
    dash["external"] = ext

    # 逃逸率 / 保护器 / W2（镜像自 web/data/status.json）
    try:
        st = _json("web/data/status.json")
        dash["escape"] = {
            "rate_pct": (st.get("escape") or {}).get("rate_pct"),
            "escaped": (st.get("escape") or {}).get("escaped"),
            "denominator": (st.get("escape") or {}).get("denominator"),
            "variants": (st.get("escape") or {}).get("variants"),
            "blocked": (st.get("escape") or {}).get("blocked"),
            "frozen": (st.get("escape") or {}).get("frozen_616"),
        }
        dash["protectors"] = (st.get("protectors") or {}).get("protectors_total")
        dash["protectors_missing"] = (st.get("protectors") or {}).get("protectors_missing") or []
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"status.json：{e}")

    # 变异率（**内部自证**指标，明确标注；与 status_reconciler_658.py 同一数据源）
    mut: dict[str, Any] = {"source": "data/656_mutation_report_{core,all}.json"}
    for name, key in (("data/656_mutation_report_core.json", "core"),
                      ("data/656_mutation_report_all.json", "all")):
        try:
            rep = _json(name)
            n_mut, n_kill = int(rep.get("mutants", 0)), int(rep.get("killed", 0))
            # 与 status_reconciler_658.py 同一口径：优先 `kill_rate_on_scored`
            mut[key] = rep.get("kill_rate_on_scored")
            mut[key + "_all"] = rep.get("kill_rate_all")
            mut[key + "_frac"] = f"{n_kill}/{n_mut}（全部变异体）"
        except Exception as e:  # noqa: BLE001
            mut[key] = None
            mut[key + "_all"] = None
            unavailable.append(f"{name}：{e}")
    mut["note"] = ("变异率是**内部自证**指标，不作缺陷检测率（656 起沿用，666 重申）。"
                   "`core/all` 是 **on_scored** 口径（分母只算被评分的变异体），"
                   "`*_all` 是全部变异体口径 —— **两个都给，不许只报好看的那个**")
    dash["mutation"] = mut

    n_led = _count_lines(LEDGER)
    dash["ledger_events"] = n_led if n_led >= 0 else None
    if n_led < 0:
        unavailable.append("646_authority_rule_annotation.jsonl 缺失")

    return {
        "schema": "queyi-web-verdicts/667",
        "generated_by": "tools/web_verdicts_667.py",
        "dashboard": dash,
        "unavailable": unavailable,
    }


def build() -> dict[str, Any]:
    fresh = collect()
    rows, excluded = collect_verdicts()
    drift: list[dict[str, Any]] = []
    h = fresh["dashboard"].get("holdout") or {}
    if h.get("drift"):
        drift.append({
            "field": "holdout.rate_pct",
            "stored": h.get("stored_rate_pct"), "fresh": h.get("rate_pct"),
            "note": "web/data/metrics_666.json 的 81.2% 无现算来源；现算为 66.7%（-O1 单档，产物自述）。"
                    "web_metrics_666.py --check **不比对这两个字段** ⇒ 假绿。需人裁决。",
        })
    # 668：反事实**不再靠"数值等于某个已知坏值"来判漂移**（那是把缺陷写死进检查器）。
    # 改成通用不变量：产物自己声明的分母必须等于实际案例数；F1 必须带"上界"声明。
    cf = os.path.join(ROOT, "data", "counterfactual_cases_665.json")
    if os.path.isfile(cf):
        try:
            c = json.loads(open(cf, encoding="utf-8").read())
            den = (c.get("denominator") or {}).get("value")
            n = c.get("cases_total")
            if den != n:
                drift.append({
                    "field": "counterfactual.denominator",
                    "stored": f"声明 {den}", "fresh": f"实际案例 {n}",
                    "note": "产物声明的分母与实际案例数不符 ⇒ P/R/F1 的分母不可信。",
                })
            if "上界" not in str(c.get("honest_note", "")):
                drift.append({
                    "field": "counterfactual.honest_note",
                    "stored": "（缺上界声明）", "fresh": "必须有",
                    "note": "判据与真值标签同源 ⇒ F1 是上界；不声明上界就会被当泛化能力读。",
                })
        except Exception as e:  # noqa: BLE001
            fresh["unavailable"].append(f"counterfactual_cases_665.json：{e}")

    out = dict(fresh)
    out["verdicts"] = rows
    out["verdicts_total"] = len(rows)
    out["excluded"] = excluded
    out["drift"] = drift
    out["compare"] = collect_compare(fresh["dashboard"], drift)
    out["honest_note"] = (
        "全部数字**现算**；仪表盘不写死。判决历史只有 "
        f"{len(rows)} 条（16 机器卡 + 15 缺陷夹具）—— holdout 与外部语料**无逐条结果落盘**，"
        "已登记进 excluded，不伪造行。漂移项一律显形，不静默替换。"
    )
    return out


def selftest() -> int:
    """只读自检：数据源可达、字段齐全、漂移可见、缺项显式登记。"""
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    d = build()
    dsh = d["dashboard"]
    chk("卡数 > 0", (dsh.get("cards_real") or 0) > 0, f"({dsh.get('cards_real')})")
    chk("规则数 > 0", (dsh.get("rules_total") or 0) > 0, f"({dsh.get('rules_total')})")
    chk("holdout 现算可读", (dsh.get("holdout") or {}).get("rate_pct") is not None)
    chk("external 双分母都在", (dsh.get("external") or {}).get("rate_pct") is not None
        and (dsh.get("external") or {}).get("rate_pct_all") is not None,
        f"({(dsh.get('external') or {}).get('rate_pct')} / {(dsh.get('external') or {}).get('rate_pct_all')})")
    chk("判决历史非空", len(d["verdicts"]) > 0, f"({len(d['verdicts'])} 条)")
    chk("时间倒序", all(d["verdicts"][i]["when"] >= d["verdicts"][i + 1]["when"]
                        for i in range(len(d["verdicts"]) - 1)))
    chk("每条都有四态", all(r["state"] in STATE_LABEL for r in d["verdicts"]))
    chk("对比表非空", len(d["compare"]) > 0, f"({len(d['compare'])} 行)")
    # 668：不再断言"必须存在反事实漂移"（那是把某个已知缺陷写死进自检）。
    # 改成不变量：**有漂移就必须带完整字段**；无漂移是合法状态（修好之后就该为空）。
    chk("漂移项结构完整（有则必带 field/stored/fresh/note）",
        all(x.get("field") and x.get("stored") is not None
            and x.get("fresh") is not None and x.get("note") for x in d["drift"]),
        f"（当前 {len(d['drift'])} 项）")
    if d["unavailable"]:
        print(f"  [warn] 不可用项：{'；'.join(d['unavailable'])}")
    print(f"[667 verdicts] selftest：{'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="667 阶段2：判决历史 / 仪表盘 / 数据对比表现算数据")
    ap.add_argument("--check", action="store_true", help="只读：现算 vs 已落盘（漂移可见）")
    ap.add_argument("--write", action="store_true", help="写 web/data/verdicts_667.json")
    ap.add_argument("--selftest", action="store_true", help="自检")
    ap.add_argument("--json", action="store_true", help="打印现算结果（不写盘）")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    fresh = build()

    if a.json:
        print(json.dumps(fresh, ensure_ascii=False, indent=2))
        return 0

    if a.check:
        if not os.path.isfile(OUT):
            print(f"[667 verdicts] ✗ 未落盘 {os.path.relpath(OUT, ROOT)}（先 --write）")
            return 1
        old = json.loads(open(OUT, encoding="utf-8").read())
        drift: list[tuple[str, Any, Any]] = []
        od, nd = old.get("dashboard", {}), fresh.get("dashboard", {})
        for k in ("cards_real", "cards_draft", "cards_total", "rules_total",
                  "ledger_events", "protectors"):
            if od.get(k) != nd.get(k):
                drift.append((k, od.get(k), nd.get(k)))
        for k in ("rate_pct", "catch", "miss", "unknown"):
            if (od.get("holdout") or {}).get(k) != (nd.get("holdout") or {}).get(k):
                drift.append((f"holdout.{k}", (od.get("holdout") or {}).get(k),
                              (nd.get("holdout") or {}).get(k)))
        for k in ("rate_pct", "rate_pct_all", "catch", "miss", "total"):
            if (od.get("external") or {}).get(k) != (nd.get("external") or {}).get(k):
                drift.append((f"external.{k}", (od.get("external") or {}).get(k),
                              (nd.get("external") or {}).get(k)))
        if old.get("verdicts_total") != fresh.get("verdicts_total"):
            drift.append(("verdicts_total", old.get("verdicts_total"), fresh.get("verdicts_total")))
        for d in drift:
            print(f"[667 verdicts] ✗ 漂移 {d[0]}：落盘 {d[1]} → 现算 {d[2]}")
        print("[667 verdicts] " + ("✅ 与现算一致" if not drift else f"❌ {len(drift)} 项漂移（重跑 --write）"))
        return 0 if not drift else 1

    if not a.write:
        ap.print_help()
        return 2

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(fresh, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    d = fresh["dashboard"]
    print(f"[667 verdicts] 写入 {os.path.relpath(OUT, ROOT)}："
          f"卡 {d['cards_real']}(+{d['cards_draft']}) · 规则 {d['rules_total']} · "
          f"判决历史 {fresh['verdicts_total']} 条 · 对比表 {len(fresh['compare'])} 行 · "
          f"漂移 {len(fresh['drift'])} 项")
    if fresh["unavailable"]:
        print("[667 verdicts] ⚠ 不可用项：" + "；".join(fresh["unavailable"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
