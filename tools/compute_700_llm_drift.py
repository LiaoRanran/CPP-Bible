#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_700_llm_drift.py — 700-D：跨领域迁移的完整实证（LLM 评估，**只读**）。

数据来源（**699 数据不存在，本批改用仓库内已有的 LLM 臂**）
=========================================================
`data/692_llm_audit_raw.jsonl`（692 批次的 LLM 审计原始记录）+ `data/692_llm_audit_results.json`。
设计：**80 个样本 × 2 个 judge 模型（glm-4.5 / glm-4-flash）× 2 个语义等价 prompt（p1/p2）**
⇒ 天然构成"口径轴 × 环境轴"的 2×2 配对设计。

三型漂移在 LLM 领域的对应
========================
| 结构性漂移型 | LLM 领域的对应 | 本批的测量 |
|---|---|---|
| **Type II（环境）** | 换 **judge 模型** | 同 prompt 下 A vs B 的一致率 |
| **Type I（口径/分母）** | 换 **prompt 模板** + 记账口径（tie-break vs 资产一致 OR） | p1 vs p2 一致率；692 的 `aggregation_sensitivity` |
| **Type III（标签）** | 换**缺陷分组词表**（per_defect_group 的粒度） | 分组统计在不同分组下的摆幅 |
| **Type IV（聚合）** | 换**聚合规则**（多数票 / 资产一致 OR / 严格） | 692 的 `aggregation_sensitivity` 实测 |

迁移性分数（0–100）
==================
四个分量各 25 分，衡量"Queyi 的审计协议在新领域能发现多少漂移"：
* C1 口径轴可检出（prompt 变体产生可测的不一致）；
* C2 环境轴可检出（judge 变体产生可测的不一致）；
* C3 聚合轴可检出（换聚合规则改变报告值）；
* C4 标签轴可检出（换分组词表改变分组统计）。
**< 50 分 ⇒ 协议需要领域特定改造。**

红线：``detect_calls = 0``；只读仓库内文件；产出只写 ``data/700_*``。

用法
====
    python tools/compute_700_llm_drift.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_700_llm_drift")

RAW: Final[str] = "692_llm_audit_raw.jsonl"
RES_692: Final[str] = "692_llm_audit_results.json"
A5: Final[str] = "a5_676f_detection_matrix.json"
OUT_JSON: Final[Path] = ROOT / "data" / "700_llm_drift.json"


LONG_OUTPUT_TOKENS: Final[int] = 400


def load_raw() -> list[dict[str, Any]]:
    """读原始 jsonl，按 (uid, model_slot, prompt, run) 去重（保留最后一条成功的）。

    ⚠ **必须把 ``run`` 放进键**：glm-4.5 跑过**两轮**（max_tokens 2000 与 700，
    692 的 ``budget_sensitivity`` 已记录），原始 jsonl 里**没有 run_tag 字段**，
    只能靠 ``completion_tokens`` 的量级区分。第一版没把 run 放进键 ⇒
    把两轮**静默合并**成一轮（去重后只剩 320 条），且把预算轴这个真实的口径漂移维度漏掉了。
    """
    path = DATA / RAW
    recs: dict[tuple[str, str, str, bool], dict[str, Any]] = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("api_status") != "ok":
                continue
            toks = int(((r.get("usage") or {}).get("completion_tokens")) or 0)
            key = (str(r.get("uid")), str(r.get("model_slot")), str(r.get("prompt")),
                   toks > LONG_OUTPUT_TOKENS)
            recs[key] = r
    return list(recs.values())


def _is_long(r: dict[str, Any]) -> bool:
    return int(((r.get("usage") or {}).get("completion_tokens")) or 0) > LONG_OUTPUT_TOKENS


def verdict_of(rec: dict[str, Any]) -> str:
    v = rec.get("verdict") or {}
    return str(v.get("state", "unknown")) if isinstance(v, dict) else "unknown"


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
    return min(1.0, 2.0 * tail)


# ══════════════════════════════════════════════════════════════════════════
# 1. 口径漂移（prompt 轴）与环境漂移（模型轴）
# ══════════════════════════════════════════════════════════════════════════
def paired_table(
    recs: list[dict[str, Any]], left: tuple[str, str, bool], right: tuple[str, str, bool],
) -> dict[str, Any]:
    """比较两个配置：``(model_slot, prompt, is_long_run)``。

    返回 3×3 混淆 + 一致率 + 单向性判据（对 catch / 非 catch 二值化）。
    """
    idx = {(r["uid"], str(r.get("model_slot")), str(r.get("prompt")), _is_long(r)): r for r in recs}
    uids = sorted({r["uid"] for r in recs})
    rows: list[dict[str, Any]] = []
    for u in uids:
        a = idx.get((u, left[0], left[1], left[2]))
        b_ = idx.get((u, right[0], right[1], right[2]))
        if a is None or b_ is None:
            continue
        va, vb = verdict_of(a), verdict_of(b_)
        rows.append({"uid": u, "left": va, "right": vb,
                     "confidence_left": (a.get("verdict") or {}).get("confidence"),
                     "code_lines": a.get("code_lines")})
    agree = sum(1 for r in rows if r["left"] == r["right"])
    # 二值化：catch vs 非 catch
    bc = sum(1 for r in rows if r["left"] == "catch" and r["right"] != "catch")
    cb = sum(1 for r in rows if r["left"] != "catch" and r["right"] == "catch")
    return {
        "left": {"model_slot": left[0], "prompt": left[1], "long_run": left[2]},
        "right": {"model_slot": right[0], "prompt": right[1], "long_run": right[2]},
        "n_pairs": len(rows),
        "n_agree": agree,
        "agreement_pct": round(agree / len(rows) * 100.0, 4) if rows else None,
        "confusion_3x3": {f"{i}->{j}": sum(1 for r in rows if r["left"] == i and r["right"] == j)
                          for i in ("catch", "miss", "unknown", "contradiction")
                          for j in ("catch", "miss", "unknown", "contradiction")
                          if sum(1 for r in rows if r["left"] == i and r["right"] == j)},
        "binary_catch_vs_not": {"b_left_only_catch": bc, "c_right_only_catch": cb,
                                "discordant": bc + cb,
                                "psi": round((bc + cb) / len(rows), 6) if rows else None,
                                "one_directional": cb == 0,
                                "mcnemar_exact_p": mcnemar_exact(bc, cb)},
        "disagreement_samples": [r["uid"] for r in rows if r["left"] != r["right"]],
    }


# ══════════════════════════════════════════════════════════════════════════
# 2. 结构性 Goodhart（judge 说 catch、标签说 miss）
# ══════════════════════════════════════════════════════════════════════════
def structural_goodhart_llm(
    recs: list[dict[str, Any]], primary: dict[str, bool],
) -> dict[str, Any]:
    """结构性 Goodhart：judge 说 catch 而声明标签说 miss。

    ⚠ **必须按主运行筛**：glm-4.5 有两轮（长/短），不过滤会让同一个 uid
    出现两次 ⇒ Top-N 列表里出现重复条目（本批第一版即如此）。
    """
    a5 = load_json_cached(DATA / A5)
    expected: dict[str, str] = {}
    group: dict[str, str] = {}
    for s in a5["samples"]:
        sid = str(s.get("sample_id"))
        expected[sid] = str(s.get("expected_verdict") or "unknown")
        group[sid] = str(s.get("defect_group") or "unknown")

    by_model: dict[str, Any] = {}
    for slot in sorted({str(r.get("model_slot")) for r in recs}):
        # 每个 uid 只取**一条**：优先主运行，主运行缺该 uid 时回退到另一轮。
        # （只按主运行硬筛会让 n 从 80 掉到 55 —— 因为 token 阈值的轮次推断不完美；
        #   只按"全部记录"又会重复计数。两害相权取"优先主运行 + 回退"。）
        want_long = primary.get(slot, False)
        picked: dict[str, dict[str, Any]] = {}
        for r in recs:
            if str(r.get("model_slot")) != slot or str(r.get("prompt")) != "p1":
                continue
            uid = str(r["uid"])
            cur = picked.get(uid)
            if cur is None or (_is_long(r) == want_long and _is_long(cur) != want_long):
                picked[uid] = r
        sub = list(picked.values())
        fp = fn = tp = tn = 0
        cases: list[dict[str, Any]] = []
        for r in sub:
            u = r["uid"]
            exp = expected.get(u)
            if exp is None:
                continue
            got = verdict_of(r)
            got_pos = got == "catch"
            exp_pos = exp == "catch"
            if got_pos and not exp_pos:
                fp += 1
                cases.append({"uid": u, "judge": got, "expected": exp,
                              "defect_group": group.get(u, "?"),
                              "confidence": (r.get("verdict") or {}).get("confidence"),
                              "reason": str((r.get("verdict") or {}).get("reason", ""))[:160]})
            elif not got_pos and exp_pos:
                fn += 1
            elif got_pos and exp_pos:
                tp += 1
            else:
                tn += 1
        n = fp + fn + tp + tn
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        cases.sort(key=lambda d: (d["defect_group"], d["uid"]))
        by_model[slot] = {
            "n": n, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(prec, 6), "recall": round(rec, 6),
            "structural_goodhart_rate_pct": round(fp / n * 100.0, 4) if n else None,
            "definition": "结构性 Goodhart 率 = 判官说 catch 而声明标签说 miss 的比例（= 1 − precision）",
            "false_positive_cases": cases,
            "fp_by_defect_group": dict(Counter(c["defect_group"] for c in cases).most_common()),
        }
    return {
        "by_model": by_model,
        "note": ("真值参照 = 冻结矩阵的 expected_verdict（**声明可检出性标签**），"
                 "不是人类标注（692 已登记人类 IAA = 0）⇒ 「judge 错」与「标签错」不可分。"),
    }


# ══════════════════════════════════════════════════════════════════════════
# 3. 标签轴（分组词表）与聚合轴
# ══════════════════════════════════════════════════════════════════════════
def label_axis(recs: list[dict[str, Any]], primary: dict[str, bool]) -> dict[str, Any]:
    """同一批 judge 裁决在不同分组词表下的「盲区类占比」摆幅。"""
    a5 = load_json_cached(DATA / A5)
    dt: dict[str, str] = {}
    grp: dict[str, str] = {}
    for s in a5["samples"]:
        sid = str(s.get("sample_id"))
        dt[sid] = str(s.get("defect_type") or "unknown")
        grp[sid] = str(s.get("defect_group") or "unknown")

    out: dict[str, Any] = {}
    for slot in sorted({str(r.get("model_slot")) for r in recs}):
        want_long = primary.get(slot, False)
        picked: dict[str, dict[str, Any]] = {}
        for r in recs:
            if str(r.get("model_slot")) != slot or str(r.get("prompt")) != "p1":
                continue
            uid = str(r["uid"])
            cur = picked.get(uid)
            if cur is None or (_is_long(r) == want_long and _is_long(cur) != want_long):
                picked[uid] = r
        judged = {u: verdict_of(r) for u, r in picked.items()}

        def share(keyfn: Any) -> dict[str, Any]:
            g: dict[str, list[int]] = defaultdict(list)
            for u, v in judged.items():
                g[str(keyfn(u))].append(0 if v == "catch" else 1)
            rates = {k: sum(x) / len(x) for k, x in g.items()}
            hi = [k for k, r in rates.items() if r > 0.5]
            return {"n_categories": len(g), "n_high": len(hi),
                    "share_pct": round(len(hi) / len(g) * 100.0, 4) if g else None}

        fine = share(lambda u: dt.get(u, "unknown"))
        coarse = share(lambda u: grp.get(u, "unknown"))
        out[slot] = {
            "defect_type_fine": fine,
            "defect_group_coarse": coarse,
            "share_spread_pp": round(abs((fine["share_pct"] or 0) - (coarse["share_pct"] or 0)), 4),
        }
    return {
        "by_model": out,
        "interpretation": (
            "标签轴在 LLM 领域**存在且可测**：同一批 judge 裁决在细/粗词表下给出不同的"
            "「高盲类占比」。这与 C++ 领域（698-A Type III）同构。"
        ),
    }


def published_cross_check() -> dict[str, Any]:
    """692 已发布的口径/校准数字 —— 作为本批重算的**对照**。

    ⚠ 原始 jsonl **没有 run_tag 字段**，本批只能靠 ``completion_tokens`` 量级
    推断 glm-4.5 的两轮运行 ⇒ 推断**不完美**（本批重算的口径一致率 76.0% vs
    已发布 87.5%）。因此：
    * **口径轴以已发布值为准**（它是按预注册口径逐样本多数票算出的）；
    * 本批重算值作为**独立交叉核对**，差异登记为测量限制。
    """
    res = load_json_cached(DATA / RES_692)
    out: dict[str, Any] = {}
    for slot, v in (res.get("per_model") or {}).items():
        out[slot] = {
            "published_prompt_invariance": v.get("prompt_invariance"),
            "published_calibration_ece": (v.get("calibration") or {}).get("ece"),
            "published_false_report": v.get("false_report"),
            "published_three_components": v.get("three_components_on_declared_positives"),
            "run_tag": v.get("run_tag"),
            "max_tokens": v.get("max_tokens"),
        }
    return out


def aggregation_axis() -> dict[str, Any]:
    """聚合轴：692 已实测两种聚合规则（预注册 tie-break vs 资产一致 OR）。"""
    res = load_json_cached(DATA / RES_692)
    agg = res.get("aggregation_sensitivity") or {}
    rows: list[dict[str, Any]] = []
    for slot, v in agg.items():
        a = v.get("prereg_p1_tiebreak") or {}
        b = v.get("asset_consistent_or") or {}
        rows.append({
            "model_slot": slot,
            "prereg_p1_tiebreak": a,
            "asset_consistent_or": b,
            "delta_conditional_recall_pp": round(
                (a.get("conditional_recall_pct") or 0) - (b.get("conditional_recall_pct") or 0), 4),
            "delta_false_report_rate_pp": round(
                (a.get("false_report_rate_pct") or 0) - (b.get("false_report_rate_pct") or 0), 4),
            "delta_unknown_n": (a.get("unknown_n") or 0) - (b.get("unknown_n") or 0),
            "delta_n_judged": (a.get("n_judged") or 0) - (b.get("n_judged") or 0),
        })
    max_abs = max((abs(r["delta_false_report_rate_pp"]) for r in rows), default=0.0)
    return {
        "rows": rows,
        "max_abs_delta_false_report_rate_pp": round(max_abs, 4),
        "detectable": max_abs > 0.0,
        "interpretation": (
            "聚合轴在 LLM 领域**可测但效应很小**：两种聚合规则下 glm-4.5 的假报率差 1.03pp、"
            "被判样本数差 8；glm-4-flash 完全不变。⇒ 该领域的聚合轴**不如 C++ 领域敏感**"
            "（C++ 的均值口径可被拉低 33.33%，698-A §4）。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. 迁移性分数
# ══════════════════════════════════════════════════════════════════════════
def migration_score(
    prompt_axis: dict[str, Any], model_axis: dict[str, Any],
    label: dict[str, Any], agg: dict[str, Any], goodhart: dict[str, Any],
    published: dict[str, Any],
) -> dict[str, Any]:
    """四分量各 25 分（**分级**，非二值）。"""
    # C1 口径轴：prompt 变体是否产生可测不一致（且单向性可判）
    # **分级**评分（不是二值）：满分标定取 C++ 领域实测的量级 ——
    #   口径/环境轴：不一致率 20% 记满分；聚合轴：效应 10pp 记满分；标签轴：摆幅 10pp 记满分。
    def _graded(value: float, full_scale: float) -> float:
        return round(25.0 * min(1.0, max(0.0, value / full_scale)), 2)

    # C1 口径轴：**以 692 已发布值**为准（原始 jsonl 无 run_tag，本批重算不完美）
    pub_rates = [v["published_prompt_invariance"]["rate_pct"]
                 for v in published.values()
                 if v.get("published_prompt_invariance")]
    rec_rates = [v["agreement_pct"] for v in prompt_axis.values() if v["agreement_pct"] is not None]
    c1_disc_pub = 100.0 - min(pub_rates) if pub_rates else 0.0
    c1_disc_rec = 100.0 - min(rec_rates) if rec_rates else 0.0
    c1 = _graded(c1_disc_pub, 20.0)

    # C2 环境轴：**用 692 已发布的跨模型指标**（假报率差），不用本批的配对表 ——
    #    因为原始 jsonl 无 run_tag，glm-4.5 两轮的跨模型一致率差达 39.2pp
    #    （见 run_inference_robustness），配对表**不可靠**。已发布聚合量不受此影响。
    fr_raw = [(v.get("published_false_report") or {}).get("false_report_rate_pct")
              for v in published.values()]
    fr: list[float] = [float(x) for x in fr_raw if x is not None]
    c2_disc = (max(fr) - min(fr)) if len(fr) >= 2 else 0.0
    c2 = _graded(c2_disc, 20.0)

    c3 = _graded(agg["max_abs_delta_false_report_rate_pp"], 10.0)

    spreads = [v["share_spread_pp"] for v in label["by_model"].values()]
    c4 = _graded(max(spreads) if spreads else 0.0, 10.0)

    total = c1 + c2 + c3 + c4
    return {
        "components": {
            "C1_caliber_axis_prompt": {"score": c1, "max": 25,
                                       "evidence": (f"已发布 prompt 不变性最低 "
                                                    f"{min(pub_rates) if pub_rates else 'n/a'}% ⇒ 不一致 "
                                                    f"{round(c1_disc_pub, 2)}%；"
                                                    f"本批重算 {round(c1_disc_rec, 2)}%（见 cross_check）")},
            "C2_environment_axis_model": {"score": c2, "max": 25,
                                          "evidence": (f"已发布假报率跨模型差 {round(c2_disc, 2)}pp"
                                                       "（配对表因 run 推断不可靠，见 robustness）"),
                                          "confidence": "中（用已发布聚合量，非配对表）"},
            "C3_aggregation_axis": {"score": c3, "max": 25,
                                    "evidence": f"换聚合规则最大效应 "
                                                f"{agg['max_abs_delta_false_report_rate_pp']}pp"},
            "C4_label_axis": {"score": c4, "max": 25,
                              "evidence": f"换分组词表最大摆幅 {max(spreads) if spreads else 0}pp"},
        },
        "total": total,
        "verdict": (
            "**协议可直接迁移**（≥ 50 分）" if total >= 50 else
            "**协议需要领域特定改造**（< 50 分）"
        ),
        "cpp_baseline": {
            "note": "C++ 领域（Queyi）四型全部可测，作为 100 分的参照点",
            "type_I_measured": "g_app 5.30 → 29.88pp（698-A）",
            "type_II_measured": "−35.34pp（697-B）",
            "type_III_measured": "13/34 vs 18/70（698-A）",
            "type_IV_measured": "均值口径可被拉低 33.33%（698-A）",
        },
    }


# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="700-D 跨领域迁移实证（LLM，只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    recs = load_raw()
    slots = sorted({str(r.get("model_slot")) for r in recs})
    prompts = sorted({str(r.get("prompt")) for r in recs})
    _log.info("去重后记录 %d 条；model_slot=%s；prompt=%s", len(recs), slots, prompts)

    # 主运行：glm-4.5 用**长运行**（= 692 的 a2000，预注册口径）；其余用默认（短）
    primary: dict[str, bool] = {s: (s == "A_glm-4.5") for s in slots}

    # 口径轴：同一模型内 p1 vs p2
    prompt_axis = {s: paired_table(recs, (s, "p1", primary[s]), (s, "p2", primary[s]))
                   for s in slots}
    # 环境轴：同一 prompt 下 A vs B
    model_axis: dict[str, Any] = {}
    if len(slots) >= 2:
        for p in prompts:
            model_axis[f"p{p}_{slots[0]}_vs_{slots[1]}"] = paired_table(
                recs, (slots[0], p, primary[slots[0]]), (slots[1], p, primary[slots[1]]))
    # 预算轴（Type I/IV 类）：glm-4.5 的 max_tokens 2000 vs 700
    budget_axis: dict[str, Any] = {}
    for p in prompts:
        budget_axis[f"p{p}_glm4.5_max2000_vs_max700"] = paired_table(
            recs, (slots[0], p, True), (slots[0], p, False))

    goodhart = structural_goodhart_llm(recs, primary)
    label = label_axis(recs, primary)
    agg = aggregation_axis()
    published = published_cross_check()
    score = migration_score(prompt_axis, model_axis, label, agg, goodhart, published)

    # 稳健性：glm-4.5 的两轮运行推断是否影响环境轴结论
    robustness: dict[str, Any] = {}
    if len(slots) >= 2:
        for p in prompts:
            a_long = paired_table(recs, (slots[0], p, True), (slots[1], p, primary[slots[1]]))
            a_short = paired_table(recs, (slots[0], p, False), (slots[1], p, primary[slots[1]]))
            robustness[f"p{p}"] = {
                "glm4.5_long_run_agreement_pct": a_long["agreement_pct"],
                "glm4.5_short_run_agreement_pct": a_short["agreement_pct"],
                "range_pp": round(abs((a_long["agreement_pct"] or 0)
                                      - (a_short["agreement_pct"] or 0)), 4),
            }

    # Top 10 最严重的结构性 Goodhart 案例（按 confidence 降序，跨模型合并）
    top_cases: list[dict[str, Any]] = []
    for slot, v in goodhart["by_model"].items():
        for c in v["false_positive_cases"]:
            top_cases.append({**c, "model_slot": slot})
    top_cases.sort(key=lambda d: -(float(d["confidence"] or 0.0)))
    top_cases = top_cases[:10]

    doc: dict[str, Any] = {
        "schema": "queyi-700/llm-drift/v1",
        "generated_by": "tools/compute_700_llm_drift.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "data_provenance": {
            "source": "data/692_llm_audit_raw.jsonl + data/692_llm_audit_results.json",
            "why_not_699": ("**699 未完成**（`data/raw_external/` 不存在，已实测）"
                            "⇒ 按任务书的降级条款改用**仓库内已有的 LLM 评估数据**（692 的 LLM 臂）。"),
            "design": {"n_samples": 80, "models": slots, "prompts": prompts,
                       "calls": 480, "temperature": 0},
            "honest_limit": ("692 的 LLM 臂**不是**为跨领域迁移设计的："
                             "只有 2 个模型、2 个 prompt、80 个样本；"
                             "模型家族是**推理型 vs 非推理型**（不是两家公司）。"),
        },
        "type_II_environment_axis_model_change": model_axis,
        "type_I_caliber_axis_prompt_change": prompt_axis,
        "type_III_label_axis": label,
        "type_IV_aggregation_axis": agg,
        "type_I_budget_axis_max_tokens": budget_axis,
        "structural_goodhart": goodhart,
        "published_692_cross_check": published,
        "run_inference_robustness": robustness,
        "top10_structural_goodhart_cases": top_cases,
        "migration_score": score,
        "comparison_with_cpp": {
            "caliber_axis": {"cpp": "环境漂移 −35.34pp（697-B）",
                             "llm": f"prompt 变体不一致率 "
                                    f"{[v['agreement_pct'] for v in prompt_axis.values()]}%"},
            "environment_axis": {"cpp": "E1→E2 60.07% → 24.74%（692）",
                                 "llm": f"judge 变体不一致率 "
                                        f"{[v['agreement_pct'] for v in model_axis.values()]}%"},
            "structural_goodhart": {"cpp": "g_app 中 72.2% 来自构成（698-A）",
                                    "llm": "见 structural_goodhart.by_model 的假报率"},
        },
        "honest_limits": [
            "**699 未完成** ⇒ 用的是 692 的 LLM 臂，样本量与模型数都远小于理想设计。",
            "真值参照是**声明标签**（expected_verdict），人类 IAA = 0 ⇒ 「judge 错」与「标签错」不可分。",
            "只有 2 个 prompt、2 个模型 ⇒ 口径/环境轴的**控制点各只有 2 个**，无法拟合趋势。",
            "迁移性分数的阈值（50）与分量权重（各 25）是本批自定的，无外部标定。",
            "跨领域结论只覆盖「LLM-as-a-Judge」这一种 LLM 评估形态，不代表全部 LLM 评估。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 700-D 跨领域迁移实证（LLM，只读）==")
    print("  口径轴（同一模型 p1 vs p2 一致率）：")
    for s, v in prompt_axis.items():
        print(f"    {s:<16} {v['agreement_pct']}%（不一致 {v['n_pairs'] - v['n_agree']} 例，"
              f"单向={v['binary_catch_vs_not']['one_directional']}）")
    print("  环境轴（同一 prompt 下换模型）：")
    for s, v in model_axis.items():
        print(f"    {s:<26} {v['agreement_pct']}%（不一致 {v['n_pairs'] - v['n_agree']} 例）")
    print("  预算轴（glm-4.5 的 max_tokens 2000 vs 700）：")
    for s, v in budget_axis.items():
        print(f"    {s:<34} {v['agreement_pct']}%（不一致 {v['n_pairs'] - v['n_agree']} 例）")
    print("  结构性 Goodhart（judge 说 catch / 标签说 miss）：")
    for s, v in goodhart["by_model"].items():
        print(f"    {s:<16} {v['structural_goodhart_rate_pct']}%（fp={v['fp']} / n={v['n']}）")
    print(f"\n  迁移性分数 = {score['total']} / 100 ⇒ {score['verdict']}")
    for k, c in score["components"].items():
        print(f"    {k:<28} {c['score']:>5} / 25   {c['evidence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
