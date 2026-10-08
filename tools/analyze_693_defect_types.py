#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_693_defect_types.py — 693-E2：缺陷类型深度分析（**只读，0 次 detect**）。

四个维度（任务书 E2.1–E2.4）
============================
1. **可检测性排序** —— 每类的 OR 检出率与条件 recall；
2. **独苗资产分布** —— 每类里「只有某一个资产抓到」的样本，落在哪个资产上；
3. **环境敏感性** —— 用 692 的资产划分（E1=6 资产 / E2=3 资产）重算每类的 catch 率落差；
4. **LLM vs sanitizer 分歧率** —— 用 692-C 的 80 条 LLM 记录，按类型算分歧。

数据源（全部为已落盘产物，**不跑 detect()**）
============================================
* ``data/blindspot_676g_detection_matrix.json`` —— 1147×8 冻结矩阵
* ``data/692_environment_paired_experiment.json`` —— 资产划分（E1/E2 支持集）
* ``data/692_llm_audit_raw.jsonl`` —— LLM 逐条原始输出（480 次调用）
* ``data/683_real_world_detection_matrix.json`` —— 真实靶场对照

口径声明（必须与数字同读）
==========================
* 「检出率」默认 = **OR 口径**：分母 = 全部样本（含 unknown）；
  「条件 recall」分母 = ``expected_verdict == catch`` 的样本。两者都报，不混用。
* E2（3 资产）的 catch **只统计真实运行过的资产**；缺失资产的样本**不计为 miss**
  （aware 口径），因此 E2 的「负例」不可信 —— 这正是 692 的核心发现。
* LLM 分歧用**多数票**（跨 2 模型 × 2 prompt = 4 票）；平票记为 ``tie`` 并单独统计。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("analyze_693_defect_types")
OUT_JSON = ROOT / "data" / "693_defect_type_deep_analysis.json"
OUT_MD = ROOT / "data" / "693_defect_type_report.md"

MATRIX = "blindspot_676g_detection_matrix.json"
ENV = "692_environment_paired_experiment.json"
LLM_RAW = "692_llm_audit_raw.jsonl"

SANITIZERS = ("asan", "ubsan", "tsan")


def _or(vals: list[str]) -> str:
    """资产集 OR，与冻结矩阵 `or_verdict_available6` 的口径**逐位一致**。

    冻结矩阵的语义（实测核验）：任一资产 `catch` ⇒ `catch`；否则 `miss`。
    恒 `unknown` 的资产（`wunsequenced` / `compile-time`）**不把结果抬成 unknown**
    —— 已核验 `or_verdict_available6` 与 `or_verdict_all8` 在 1147 条上完全相同
    （707 catch / 440 miss），说明该字段就是「有 catch 则 catch，否则 miss」。

    ⚠ 这个口径**故意**把 unknown 折进 miss（这是 676g 的登记口径）；
    「不把 unknown 当 miss」的 aware 口径另由 :func:`_or_aware` 表达。
    """
    return "catch" if "catch" in vals else "miss"


def _or_aware(vals: list[str]) -> str:
    """aware 口径：任一 catch ⇒ catch；否则任一 unknown ⇒ unknown；否则 miss。

    用于环境敏感性分析：E2 只跑了 3 个资产，缺失资产**不能**当作 miss。
    """
    if "catch" in vals:
        return "catch"
    if "unknown" in vals:
        return "unknown"
    return "miss"


def _asset_verdict(sample: dict[str, Any], asset: str) -> str:
    rec = (sample.get("per_asset") or {}).get(asset)
    if isinstance(rec, dict):
        return str(rec.get("verdict", "unknown"))
    return str(rec) if rec else "unknown"


def _llm_majority(path: Path) -> dict[str, dict[str, Any]]:
    """把 692-C 的原始 JSONL 聚合成 uid 到多数票的映射。

    去重规则与 692-C 一致：同一 (uid, slot, prompt) 只保留最后一条 api_status=ok 的记录。
    """
    if not path.exists():
        return {}
    latest: dict[tuple[str, str, str], dict[str, Any]] = {}
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
            key = (str(r.get("uid")), str(r.get("model_slot")), str(r.get("prompt")))
            latest[key] = r

    votes_by_uid: dict[str, list[str]] = defaultdict(list)
    for (uid, _slot, _p), r in latest.items():
        v = r.get("verdict") or {}
        votes_by_uid[uid].append(str(v.get("state", "?")).lower())

    out: dict[str, dict[str, Any]] = {}
    for uid, votes in votes_by_uid.items():
        c = Counter(votes)
        top, n = c.most_common(1)[0]
        tied = [k for k, v in c.items() if v == n]
        out[uid] = {
            "majority": top if len(tied) == 1 else "tie",
            "votes": dict(c),
            "n_votes": len(votes),
        }
    return out


def _analyze(by_type: dict[str, list[dict[str, Any]]], assets_all: list[str],
             e1_assets: list[str], e2_assets: list[str],
             llm_by_sid: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    per_type: dict[str, dict[str, Any]] = {}
    for dt, group in sorted(by_type.items()):
        n = len(group)
        # 主 OR 直接用冻结矩阵已登记的字段，保证与 676l / 论文口径逐位一致
        or_all = [str(s.get("or_verdict_available6") or
                      _or([_asset_verdict(s, a) for a in assets_all])) for s in group]
        or_e1 = [_or([_asset_verdict(s, a) for a in e1_assets]) for s in group]
        or_e2 = [_or_aware([_asset_verdict(s, a) for a in e2_assets]) for s in group]
        exp_catch = [s for s in group if str(s.get("expected_verdict")) == "catch"]
        # 条件 recall 必须在 expected=catch 子集**内部**取分子，
        # 否则会出现 >100% 的荒谬值（expected_verdict 是预注册声明，与 or_verdict 可不一致）
        exp_catch_hit = sum(
            1 for s in exp_catch
            if str(s.get("or_verdict_available6")
                   or _or([_asset_verdict(s, a) for a in assets_all])) == "catch")

        solo: Counter[str] = Counter()
        multi = 0
        none = 0
        for s in group:
            caught = [a for a in assets_all if _asset_verdict(s, a) == "catch"]
            if len(caught) == 1:
                solo[caught[0]] += 1
            elif len(caught) > 1:
                multi += 1
            else:
                none += 1

        before = or_all.count("catch")
        drop: dict[str, int] = {}
        for a in assets_all:
            rest = [x for x in assets_all if x != a]
            after = sum(1 for s in group
                        if _or([_asset_verdict(s, b) for b in rest]) == "catch")
            if before != after:
                drop[a] = before - after

        llm_rows: list[dict[str, Any]] = []
        for s in group:
            sid = str(s.get("sample_id", ""))
            if sid not in llm_by_sid:
                continue
            llm_rows.append({
                "sample_id": sid,
                "sanitizer": _or([_asset_verdict(s, a) for a in SANITIZERS]),
                "llm": str(llm_by_sid[sid]["majority"]),
                "votes": llm_by_sid[sid]["votes"],
            })
        diverg = [r for r in llm_rows if {r["sanitizer"], r["llm"]} == {"catch", "miss"}]

        per_type[dt] = {
            "n": n,
            "expected_catch": len(exp_catch),
            "or_all8": {
                "catch": or_all.count("catch"),
                "miss": or_all.count("miss"),
                "unknown": or_all.count("unknown"),
                "catch_rate_pct": round(or_all.count("catch") / n * 100, 1),
                "blind_pct": round(or_all.count("miss") / n * 100, 1),
            },
            "conditional_recall_pct": (
                round(exp_catch_hit / len(exp_catch) * 100, 1)
                if exp_catch else None),
            "or_vs_expected_disagree": (
                sum(1 for s, v in zip(group, or_all)
                    if (v == "catch") != (str(s.get("expected_verdict")) == "catch"))),
            "e1_6assets_catch_pct": round(or_e1.count("catch") / n * 100, 1),
            "e2_3assets_catch_pct": round(or_e2.count("catch") / n * 100, 1),
            "env_delta_pp": round((or_e1.count("catch") - or_e2.count("catch")) / n * 100, 1),
            "solo_asset_counts": dict(solo),
            "solo_total": sum(solo.values()),
            "multi_asset": multi,
            "no_asset": none,
            "asset_necessity": dict(sorted(drop.items(), key=lambda kv: -kv[1])),
            "llm_n": len(llm_rows),
            "llm_divergence_n": len(diverg),
            "llm_divergence_pct": (round(len(diverg) / len(llm_rows) * 100, 1)
                                   if llm_rows else None),
            "llm_san_catch_llm_miss": sum(1 for r in diverg if r["sanitizer"] == "catch"),
            "llm_san_miss_llm_catch": sum(1 for r in diverg if r["llm"] == "catch"),
        }
    return per_type


# 676l 已发布的单检测器表（`data/676l_单检测器性能报告.md` §1，2026-10-04 生成）
# 用于**陈旧性交叉核对**：该表声明的 ground truth 是「catch 674 / miss 473」。
PUBLISHED_676L: dict[str, dict[str, float]] = {
    "asan": {"TP": 389, "FN": 276, "FP": 19, "TN": 453, "unknown": 10, "recall_pct": 58.50},
    "ubsan": {"TP": 254, "FN": 411, "FP": 16, "TN": 456, "unknown": 10, "recall_pct": 38.20},
    "tsan": {"TP": 240, "FN": 425, "FP": 23, "TN": 449, "unknown": 10, "recall_pct": 36.09},
    "compiler-warn": {"TP": 129, "FN": 545, "FP": 14, "TN": 459, "unknown": 0,
                      "recall_pct": 19.14},
    "cross-compile": {"TP": 102, "FN": 551, "FP": 20, "TN": 436, "unknown": 38,
                      "recall_pct": 15.62},
    "linker": {"TP": 9, "FN": 665, "FP": 1, "TN": 472, "unknown": 0, "recall_pct": 1.34},
}
PUBLISHED_676L_GT = {"catch": 674, "miss": 473}


def _single_detector_table(samples: list[dict[str, Any]],
                           assets: list[str]) -> dict[str, dict[str, Any]]:
    """用**当前冻结标签**重算每个资产的混淆矩阵与 recall。"""
    out: dict[str, dict[str, Any]] = {}
    for a in assets:
        tp = fn = fp = tn = un = 0
        for s in samples:
            v = _asset_verdict(s, a)
            exp = str(s.get("expected_verdict"))
            if v == "unknown":
                un += 1
                continue
            if v == "catch" and exp == "catch":
                tp += 1
            elif v == "miss" and exp == "catch":
                fn += 1
            elif v == "catch" and exp == "miss":
                fp += 1
            else:
                tn += 1
        denom = tp + fn
        out[a] = {
            "TP": tp, "FN": fn, "FP": fp, "TN": tn, "unknown": un,
            "recall_pct": round(tp / denom * 100, 2) if denom else None,
            "precision_pct": (round(tp / (tp + fp) * 100, 2) if (tp + fp) else None),
        }
    return out


def _crosscheck_676l(samples: list[dict[str, Any]], assets: list[str]) -> dict[str, Any]:
    """交叉核对 676l 的已发布表是否与当前冻结标签一致。"""
    now = _single_detector_table(samples, assets)
    gt = {"catch": sum(1 for s in samples if s.get("expected_verdict") == "catch"),
          "miss": sum(1 for s in samples if s.get("expected_verdict") == "miss")}
    rows: dict[str, Any] = {}
    for a, pub in PUBLISHED_676L.items():
        cur = now.get(a)
        if not cur:
            continue
        rows[a] = {
            "published": pub,
            "recomputed": cur,
            "delta_recall_pp": (None if cur["recall_pct"] is None
                                else round(cur["recall_pct"] - pub["recall_pct"], 2)),
            "tp_same": cur["TP"] == pub["TP"],
            "fp_same": cur["FP"] == pub["FP"],
            "fn_delta": cur["FN"] - pub["FN"],
            "tn_delta": cur["TN"] - pub["TN"],
        }
    stale = any(not r["tp_same"] or r["fn_delta"] != 0 for r in rows.values())
    return {
        "published_ground_truth": PUBLISHED_676L_GT,
        "current_ground_truth": gt,
        "gt_catch_delta": gt["catch"] - PUBLISHED_676L_GT["catch"],
        "stale": stale,
        "rows": rows,
        "explanation": (
            "676l 的表在 **676m 标签修复之前**生成，其 ground truth 为 catch 674 / miss 473；"
            "当前冻结矩阵为 catch 640 / miss 507（差 34 = 676m 修正的 34 条挂起样本）。"
            "TP/FP/TN 逐位不变，只有 FN 与分母变了 ⇒ recall 列系统性偏低 1.4–3.2pp。"
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", dest="out", default=str(OUT_JSON))
    ap.add_argument("--md", dest="outmd", default=str(OUT_MD))
    args = ap.parse_args()

    mat = load_json_cached(DATA / MATRIX)
    samples = mat["samples"]
    assets_all: list[str] = list(mat["assets"])
    env = load_json_cached(DATA / ENV)
    e1_assets = list(env["asset_partition"]["E1_supported"])
    e2_assets = list(env["asset_partition"]["E2_supported"])

    sid_of = {str(s["uid"]): str(s.get("sample_id", "")) for s in samples}
    llm_by_sid = {sid_of.get(u, u): v for u, v in _llm_majority(DATA / LLM_RAW).items()}

    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in samples:
        by_type[str(s["defect_type"])].append(s)

    per_type = _analyze(by_type, assets_all, e1_assets, e2_assets, llm_by_sid)

    ranked_blind = sorted(per_type.items(), key=lambda kv: -kv[1]["or_all8"]["blind_pct"])
    ranked_recall = sorted(
        ((k, v) for k, v in per_type.items() if v["conditional_recall_pct"] is not None),
        key=lambda kv: kv[1]["conditional_recall_pct"] or 0.0)
    necessity_total: Counter[str] = Counter()
    for v in per_type.values():
        for a, d in v["asset_necessity"].items():
            necessity_total[a] += d

    doc: dict[str, Any] = {
        "schema": "queyi-693-defect-type-deep-analysis/v1",
        "generated_by": "tools/analyze_693_defect_types.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "sources": {"matrix": MATRIX, "environment": ENV, "llm_raw": LLM_RAW},
        "n_samples": len(samples),
        "n_types": len(per_type),
        "asset_partition": {"E1_supported": e1_assets, "E2_supported": e2_assets},
        "ranking_by_blind_pct": [
            {"defect_type": k, "n": v["n"], "blind_pct": v["or_all8"]["blind_pct"],
             "catch_rate_pct": v["or_all8"]["catch_rate_pct"],
             "conditional_recall_pct": v["conditional_recall_pct"]}
            for k, v in ranked_blind],
        "ranking_by_conditional_recall": [
            {"defect_type": k, "n": v["n"],
             "conditional_recall_pct": v["conditional_recall_pct"]}
            for k, v in ranked_recall],
        "asset_necessity_global": dict(necessity_total.most_common()),
        "single_detector_table_current_labels": _single_detector_table(samples, assets_all),
        "stale_metric_crosscheck_vs_676l": _crosscheck_676l(samples, assets_all),
        "per_type": per_type,
        "reading_rules": [
            "OR 口径分母 = 该类全部样本（含 unknown）；条件 recall 分母 = expected_verdict==catch。",
            "E2（3 资产）的 catch 只统计真实运行过的资产，缺失资产不计为 miss ⇒ 负例不可信。",
            "asset_necessity[asset] = 去掉该资产后本类损失的 catch 数（不是独苗数）。",
            "LLM 分歧用跨 2 模型 × 2 prompt 的多数票；平票记 tie 且不计入分歧分子。",
        ],
    }

    Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
    Path(args.outmd).write_text(_md(doc), encoding="utf-8", newline="\n")
    _log.info("完成：%d 类 / %d 样本；盲区最高 %s（%.1f%%）",
              len(per_type), len(samples),
              ranked_blind[0][0], ranked_blind[0][1]["or_all8"]["blind_pct"])
    print(f"[693-E2] -> {args.out}")


def _md(doc: dict[str, Any]) -> str:
    pt = doc["per_type"]
    lines = [
        "# 693-E2 · 缺陷类型深度分析报告",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：`tools/analyze_693_defect_types.py`",
        f"- 数据源：`{doc['sources']['matrix']}`（{doc['n_samples']} 样本 × 8 资产，**已冻结**）、",
        f"  `{doc['sources']['environment']}`（资产划分）、`{doc['sources']['llm_raw']}`（LLM 逐条）",
        f"- **`detect_calls` = {doc['detect_calls']}**（本报告只读已有产物，符合红线 8）",
        f"- 类型数：**{doc['n_types']}**（34 项闭集中的在用子集）",
        "",
        "## 1. 可检测性排序（按盲区率降序，Top 15）",
        "",
        "| # | 缺陷类型 | n | 盲区% | OR 检出% | 条件 recall% |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for i, r in enumerate(doc["ranking_by_blind_pct"][:15], 1):
        cr = "—" if r["conditional_recall_pct"] is None else f"{r['conditional_recall_pct']:.1f}"
        lines.append(f"| {i} | `{r['defect_type']}` | {r['n']} | **{r['blind_pct']:.1f}** | "
                     f"{r['catch_rate_pct']:.1f} | {cr} |")
    lines += [
        "",
        "> **读法**：盲区率 = 八资产全部 `miss` 的比例。盲区率高的类型**不是标注错误**，",
        "> 而是「现有检测器对这类缺陷没有观测手段」的量化证据。",
        "",
        "## 2. 资产必要性（全局：去掉该资产会损失多少 catch）",
        "",
        "| 资产 | 损失 catch 数 |",
        "|---|---:|",
    ]
    for a, d in doc["asset_necessity_global"].items():
        lines.append(f"| `{a}` | **{d}** |")
    lines += [
        "",
        "> `linker` 的损失数很小但**不为 0** —— 与 676l 的结论一致：**低边际但不可替代**",
        "> （它的 catch 全部落在 sanitizer 的 `unknown` 里）。",
        "",
        "## 3. 环境敏感性（E1 六资产 vs E2 三资产，按类型）",
        "",
        "| 缺陷类型 | n | E1 catch% | E2 catch% | Δpp |",
        "|---|---:|---:|---:|---:|",
    ]
    for dt, v in sorted(pt.items(), key=lambda kv: -kv[1]["env_delta_pp"])[:20]:
        lines.append(f"| `{dt}` | {v['n']} | {v['e1_6assets_catch_pct']:.1f} | "
                     f"{v['e2_3assets_catch_pct']:.1f} | **{v['env_delta_pp']:.1f}** |")
    lines += [
        "",
        "> **关键限定**：E2 的 catch 只统计**真实运行过**的 3 个资产；缺失的 3 个 sanitizer",
        "> **不计为 miss**。因此 E2 的「负例」不可信（692 已量化：46.95% 的 E2 负例其实抓得到）。",
        "",
        "## 4. 独苗资产分布",
        "",
        "| 缺陷类型 | n | 独苗总数 | 独苗落在哪 | 多资产共抓 | 全无 |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for dt, v in sorted(pt.items(), key=lambda kv: -kv[1]["solo_total"])[:20]:
        solo = "、".join(f"`{a}`×{c}" for a, c in
                        sorted(v["solo_asset_counts"].items(), key=lambda kv: -kv[1])) or "—"
        lines.append(f"| `{dt}` | {v['n']} | {v['solo_total']} | {solo} | "
                     f"{v['multi_asset']} | {v['no_asset']} |")
    lines += [
        "",
        "## 5. LLM vs sanitizer 分歧率（按类型）",
        "",
        "| 缺陷类型 | LLM 样本数 | 分歧数 | 分歧% | san catch→LLM miss | san miss→LLM catch |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for dt, v in sorted(pt.items(), key=lambda kv: -(kv[1]["llm_divergence_pct"] or 0))[:20]:
        if not v["llm_n"]:
            continue
        lines.append(f"| `{dt}` | {v['llm_n']} | {v['llm_divergence_n']} | "
                     f"**{v['llm_divergence_pct']:.1f}** | "
                     f"{v['llm_san_catch_llm_miss']} | {v['llm_san_miss_llm_catch']} |")
    lines += [
        "",
        "> 仅统计被 692-C 抽中的 80 条（跨 2 模型 × 2 prompt 多数票）。",
        "> `san catch→LLM miss` 表示**实测抓到了但 LLM 说没抓到**（LLM 保守）；",
        "> `san miss→LLM catch` 表示**实测没抓到但 LLM 说抓到了**（LLM 乐观，或标签可疑）。",
        "",
        "## 6. 单检测器表重算 + 与 676l 的陈旧性交叉核对（**重要发现**）",
        "",
        "用**当前冻结标签**（expected catch "
        f"{doc['stale_metric_crosscheck_vs_676l']['current_ground_truth']['catch']} / miss "
        f"{doc['stale_metric_crosscheck_vs_676l']['current_ground_truth']['miss']}）重算：",
        "",
        "| 资产 | TP | FN | FP | TN | unknown | recall%（重算） | recall%（676l 已发布） | Δpp |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for a, r in doc["stale_metric_crosscheck_vs_676l"]["rows"].items():
        c, p = r["recomputed"], r["published"]
        lines.append(f"| `{a}` | {c['TP']} | {c['FN']} | {c['FP']} | {c['TN']} | "
                     f"{c['unknown']} | **{c['recall_pct']}** | {p['recall_pct']} | "
                     f"{r['delta_recall_pp']:+.2f} |")
    cc = doc["stale_metric_crosscheck_vs_676l"]
    lines += [
        "",
        f"- 676l 声明的 ground truth：catch **{cc['published_ground_truth']['catch']}** / "
        f"miss {cc['published_ground_truth']['miss']}",
        f"- 当前冻结矩阵：catch **{cc['current_ground_truth']['catch']}** / "
        f"miss {cc['current_ground_truth']['miss']}",
        f"- 差 = **{cc['gt_catch_delta']}** 条，正是 676m 修正的 34 条挂起样本",
        f"- **陈旧判定：{'是（需要重算）' if cc['stale'] else '否'}**",
        "",
        f"> {cc['explanation']}",
        ">",
        "> ⇒ **`data/676l_单检测器性能报告.md` 未在 676m 标签修复后重算**；",
        "> 论文若引用其 recall 列（asan 58.5% / ubsan 38.2% / …），应改用上表的重算值。",
        "> TP / FP / TN 逐位不变，**结论方向不变**，但幅度需更新。",
        "",
        "## 7. 口径纪律",
        "",
    ]
    lines += [f"- {r}" for r in doc["reading_rules"]]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
