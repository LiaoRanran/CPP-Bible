#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""eval_693_meta_evaluation.py — 693-E5：元评估框架 v2（**只读，0 次 detect**）。

在 686 的元评估上补五个维度（任务书 E5.1）
==========================================
| 维度 | 本批做法 | 数据源 |
|---|---|---|
| **区分度** | 每个资产把 `expected_verdict` 当二分类真值，算 AUC（Mann-Whitney） | A5 帧（566） |
| **稳定性** | ① 种子：682 的 5000 次重跑；② 环境：E1/E2 逐资产 catch 率的 Spearman ρ；③ 跑间：676g 的 `tsan_stability` | 682 / 692 / 676g |
| **公平性** | 逐资产的**按类型 recall 离散度**（min/max/σ）+ 盲区类型数 | A5 帧 |
| **效率** | 逐资产 `wall_seconds`（均值/总计/最慢样本） | 676g 逐格 `wall_seconds` |
| **校准** | LLM 臂的 ECE（用 692-C 的 confidence）；检测器的「确定性过自信」ECE | 692 raw |

并与 **HELM / SV-COMP / DeepFact** 三个框架做**维度对照**（E5.2）。
框架对照是**作者按公开方法论整理的定性对照**，不是实测——报告里显式标注。

用法
====
    python tools/eval_693_meta_evaluation.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("eval_693_meta_evaluation")
OUT_JSON = ROOT / "data" / "693_meta_evaluation_v2.json"
OUT_MD = ROOT / "data" / "693_meta_evaluation_report.md"

A5 = "a5_676f_detection_matrix.json"
M676G = "blindspot_676g_detection_matrix.json"
ENV = "692_environment_paired_experiment.json"
SEED_STAB = "682_a5_seed_stability.json"
LLM_RAW = "692_llm_audit_raw.jsonl"
META686 = "686_meta_metrics.json"

ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker",
          "compile-time", "wunsequenced"]


def _verdict(rec: Any) -> str:
    if isinstance(rec, dict):
        return str(rec.get("verdict", "unknown"))
    return str(rec) if rec else "unknown"


def _auc(y: list[int], s: list[float]) -> float | None:
    """AUC（Mann-Whitney，含并列平均秩）。"""
    pos = [s[i] for i in range(len(y)) if y[i] == 1]
    neg = [s[i] for i in range(len(y)) if y[i] == 0]
    if not pos or not neg:
        return None
    order = sorted(range(len(s)), key=lambda i: s[i])
    ranks = [0.0] * len(s)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and s[order[j + 1]] == s[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    rsum = sum(ranks[i] for i in range(len(y)) if y[i] == 1)
    return round((rsum - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)), 4)


def _spearman(a: list[float], b: list[float]) -> float | None:
    """Spearman 秩相关（并列平均秩）。"""
    n = len(a)
    if n < 3 or len(b) != n:
        return None

    def _rank(v: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    ra, rb = _rank(a), _rank(b)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    da = math.sqrt(sum((x - ma) ** 2 for x in ra))
    db = math.sqrt(sum((x - mb) ** 2 for x in rb))
    return round(num / (da * db), 4) if da > 0 and db > 0 else None


def _ece(pairs: list[tuple[float, int]], bins: int = 10) -> dict[str, Any]:
    """期望校准误差（ECE）+ 可靠性曲线。pairs = [(confidence, correct)]。"""
    if not pairs:
        return {"ece": None, "n": 0, "bins": []}
    buckets: list[list[tuple[float, int]]] = [[] for _ in range(bins)]
    for conf, corr in pairs:
        b = min(bins - 1, max(0, int(conf * bins)))
        buckets[b].append((conf, corr))
    ece = 0.0
    rows: list[dict[str, Any]] = []
    for i, bk in enumerate(buckets):
        if not bk:
            continue
        conf_m = sum(c for c, _ in bk) / len(bk)
        acc = sum(v for _, v in bk) / len(bk)
        ece += len(bk) / len(pairs) * abs(acc - conf_m)
        rows.append({"bin": f"[{i / bins:.1f},{(i + 1) / bins:.1f})", "n": len(bk),
                     "mean_confidence": round(conf_m, 4), "accuracy": round(acc, 4),
                     "gap": round(acc - conf_m, 4)})
    return {"ece": round(ece, 4), "n": len(pairs), "bins": rows}


def _llm_pairs(path: Path) -> list[tuple[float, int]]:
    """LLM 臂的 (confidence, 与 expected_verdict 是否一致) 对。

    ⚠ uid 空间是 **A5 矩阵**的 `sample_id`（如 `A012`），不是 676g 的 `sample_id`
    （如 `h41`/`sample_001`）。首次实现误用 676g ⇒ 只有 100/320 条配对成功（已修复）。
    """
    mat = load_json_cached(DATA / A5)
    truth = {str(s.get("sample_id")): str(s.get("expected_verdict"))
             for s in mat["samples"]}
    pairs: list[tuple[float, int]] = []
    if not path.exists():
        return pairs
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
            latest[(str(r.get("uid")), str(r.get("model_slot")),
                    str(r.get("prompt")))] = r
    for r in latest.values():
        v = r.get("verdict") or {}
        state = str(v.get("state", "")).lower()
        conf = v.get("confidence")
        sid = str(r.get("uid"))
        exp = truth.get(sid)
        if exp is None or conf is None or state not in ("catch", "miss"):
            continue
        pairs.append((float(conf), 1 if state == exp else 0))
    return pairs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", dest="out", default=str(OUT_JSON))
    ap.add_argument("--md", dest="outmd", default=str(OUT_MD))
    args = ap.parse_args()

    a5 = load_json_cached(DATA / A5)
    ev = [s for s in a5["samples"] if str(s.get("split")) == "evaluation"]
    _log.info("A5 evaluation 帧 n=%d", len(ev))

    # ── 1. 区分度 ──
    disc: dict[str, Any] = {}
    for a in ASSETS:
        y: list[int] = []
        sc: list[float] = []
        for s in ev:
            v = _verdict((s.get("per_asset") or {}).get(a))
            if v not in ("catch", "miss"):
                continue
            y.append(1 if str(s.get("expected_verdict")) == "catch" else 0)
            sc.append(1.0 if v == "catch" else 0.0)
        disc[a] = {"n_scored": len(y), "auc": _auc(y, sc)}
    # OR 集成
    y_o: list[int] = []
    s_o: list[float] = []
    for s in ev:
        v = str(s.get("or_verdict") or "miss")
        y_o.append(1 if str(s.get("expected_verdict")) == "catch" else 0)
        s_o.append(1.0 if v == "catch" else 0.0)
    disc["OR_all8"] = {"n_scored": len(y_o), "auc": _auc(y_o, s_o)}

    # ── 2. 稳定性 ──
    stab: dict[str, Any] = {}
    ss = load_json_cached(DATA / SEED_STAB) if (DATA / SEED_STAB).exists() else {}
    res = (ss.get("results") or {})
    orig = res.get("original") or {}
    rd = orig.get("random_dist") or {}
    stab["seed_5000_runs"] = {
        "n_runs": orig.get("n_runs"),
        "fd_rate_pct": orig.get("fd_rate_pct"),
        "random_mean_rate_pct": rd.get("mean_rate_pct"),
        "random_sd_pp": rd.get("sd_pp"),
        "fd_percentile_in_random_dist": orig.get("fd_percentile"),
        "note": "682 的 5000 次重跑；FD 的率在随机分布中的位置即稳定性证据",
    }
    env = load_json_cached(DATA / ENV)
    e1 = list(env["asset_partition"]["E1_supported"])
    e2 = list(env["asset_partition"]["E2_supported"])
    shared = [a for a in e2 if a in e1]
    r1 = [round(100.0 * sum(1 for s in ev if _verdict((s.get("per_asset") or {}).get(a))
                            == "catch") / len(ev), 4) for a in shared]
    r2 = list(r1)  # E2 是 E1 的子集资产，同一矩阵上的同一读数
    stab["environment"] = {
        "shared_assets": shared,
        "catch_rate_pct_e1": dict(zip(shared, r1)),
        "spearman_rho": _spearman(r1, r2),
        "note": ("E2 支持的 3 个资产是 E1 的子集 ⇒ 其逐资产读数在冻结矩阵上**完全相同**；"
                 "环境差异体现在**缺失资产**（asan/ubsan/tsan 不在 E2），"
                 "而不是同一资产的读数变化 ⇒ ρ=1 是构造性结果，不是独立证据。"),
    }
    m676 = load_json_cached(DATA / M676G)
    ts = [s.get("tsan_stability") for s in m676["samples"] if s.get("tsan_stability")]
    stab["run_to_run_tsan"] = {
        "n": len(ts),
        "distinct_shapes": len({json.dumps(t, sort_keys=True, ensure_ascii=False)
                                for t in ts if isinstance(t, dict)}),
        "note": "676g 记录的 tsan 跑间稳定性字段；形状种类少说明逐样本结构一致",
    }

    # ── 3. 公平性 ──
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in ev:
        by_type[str(s.get("defect_type"))].append(s)
    fair: dict[str, Any] = {"per_asset": {}}
    for a in ASSETS:
        recalls: list[float] = []
        blind_types = 0
        n_types = 0
        for _dt_, grp in sorted(by_type.items()):
            if len(grp) < 5:
                continue
            n_types += 1
            hit = sum(1 for s in grp if _verdict((s.get("per_asset") or {}).get(a))
                      == "catch")
            recalls.append(hit / len(grp) * 100.0)
            if hit == 0:
                blind_types += 1
        if not recalls:
            continue
        fair["per_asset"][a] = {
            "n_types_ge5": n_types,
            "recall_min_pct": round(min(recalls), 2),
            "recall_max_pct": round(max(recalls), 2),
            "recall_range_pp": round(max(recalls) - min(recalls), 2),
            "recall_sd_pp": round(statistics.pstdev(recalls), 2),
            "types_with_zero_recall": blind_types,
            "disparity_index": round(statistics.pstdev(recalls) / 100.0, 4),
        }
    fair["overall"] = {
        "n_types_ge5": sum(1 for g in by_type.values() if len(g) >= 5),
        "worst_asset_by_range": (max(fair["per_asset"].items(),
                                     key=lambda kv: kv[1]["recall_range_pp"])[0]
                                 if fair["per_asset"] else None),
        "note": "公平性 = 同一资产在不同缺陷类型上的 recall 离散度；离散度大 = 系统性偏科。",
    }

    # ── 4. 效率 ──
    eff: dict[str, Any] = {}
    for a in ASSETS:
        ws = [float((s.get("per_asset") or {}).get(a, {}).get("wall_seconds", 0.0))
              if isinstance((s.get("per_asset") or {}).get(a), dict) else 0.0
              for s in m676["samples"]]
        ws = [x for x in ws if x > 0]
        if not ws:
            eff[a] = {"n": 0, "note": "无 wall_seconds 记录（该资产未真实运行）"}
            continue
        eff[a] = {
            "n": len(ws),
            "mean_s": round(sum(ws) / len(ws), 4),
            "total_s": round(sum(ws), 2),
            "max_s": round(max(ws), 3),
            "p95_s": round(sorted(ws)[int(0.95 * (len(ws) - 1))], 3),
        }
    eff["frame_n"] = len(m676["samples"])

    # ── 5. 校准 ──
    calib: dict[str, Any] = {}
    llm_pairs = _llm_pairs(DATA / LLM_RAW)
    calib["llm_arm"] = _ece(llm_pairs)
    det_pairs: list[tuple[float, int]] = []
    for s in ev:
        for a in ASSETS:
            v = _verdict((s.get("per_asset") or {}).get(a))
            if v not in ("catch", "miss"):
                continue
            corr = 1 if ((v == "catch") == (str(s.get("expected_verdict")) == "catch")) else 0
            det_pairs.append((1.0, corr))
    calib["detectors_deterministic"] = _ece(det_pairs)
    calib["note"] = (
        "检测器是确定性的（自报 confidence 恒为 1）⇒ 其 ECE 恰好等于 1 − accuracy，"
        "读作「过自信程度」；LLM 臂有真实 confidence ⇒ ECE 有实质含义。")

    # ── 6. 框架对照（定性，非实测）──
    frameworks = [
        {"framework": "HELM", "domain": "通用 LLM 评测",
         "dimensions": ["accuracy", "calibration", "robustness", "fairness", "bias",
                        "toxicity", "efficiency"],
         "queiy_has": ["accuracy", "calibration", "robustness(环境)", "fairness(按类型)",
                       "efficiency"],
         "queiy_missing": ["toxicity/bias（不适用）", "多任务覆盖矩阵"],
         "source": "公开方法论（作者整理，非实测）"},
        {"framework": "SV-COMP", "domain": "软件验证竞赛",
         "dimensions": ["soundness", "correctness", "score-based ranking", "witness 校验",
                        "CPU-time/memory limits"],
         "queiy_has": ["soundness（negative 可信性）", "资源限制（60s 超时）",
                       "score-based 组合排序"],
         "queiy_missing": ["形式化 witness 校验", "统一任务定义格式",
                           "第三方裁判（独立复算）"],
         "source": "公开方法论（作者整理，非实测）"},
        {"framework": "DeepFact", "domain": "深度学习模型缺陷检测基准",
         "dimensions": ["label validity", "data leakage", "distribution shift",
                        "baseline fairness"],
         "queiy_has": ["label validity（693-A 人类裁决材料）", "data leakage（模板克隆 62.2%）",
                       "distribution shift（合成→真实靶场）"],
         "queiy_missing": ["跨数据集迁移实验", "训练侧模型"],
         "source": "公开方法论（作者整理，非实测）"},
    ]

    doc: dict[str, Any] = {
        "schema": "queyi-693-meta-evaluation-v2/v1",
        "generated_by": "tools/eval_693_meta_evaluation.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "frame": {"file": A5, "split": "evaluation", "n": len(ev)},
        "predecessor": META686,
        "discrimination": disc,
        "stability": stab,
        "fairness": fair,
        "efficiency": eff,
        "calibration": calib,
        "framework_comparison": frameworks,
        "honest_limits": [
            "框架对照是**作者按公开方法论整理的定性对照**，不是实测运行结果。",
            "环境稳定性的 ρ=1 是构造性的（E2 资产是 E1 子集，同一矩阵读数不变），不构成独立证据。",
            "效率数据来自 676g 的 wall_seconds，含 WSL 冷启动与文件系统开销，**不是算法复杂度**。",
            "检测器的 ECE 是确定性系统的退化读数（confidence≡1），不可与 LLM 的 ECE 直接比较。",
            "本批**未执行**容器环境（无 Docker），故「跨容器稳定性」维度缺失。",
        ],
    }

    Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
    Path(args.outmd).write_text(_md(doc), encoding="utf-8", newline="\n")
    _log.info("完成：AUC(OR)=%s，LLM ECE=%s，效率帧 n=%d",
              disc["OR_all8"]["auc"], calib["llm_arm"]["ece"], eff["frame_n"])
    print(f"[693-E5] -> {args.out}")


def _md(doc: dict[str, Any]) -> str:
    d, s, f, e, c = (doc["discrimination"], doc["stability"], doc["fairness"],
                     doc["efficiency"], doc["calibration"])
    lines = [
        "# 693-E5 · 元评估框架 v2 报告",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：`tools/eval_693_meta_evaluation.py`",
        f"- **`detect_calls` = {doc['detect_calls']}**（只读冻结矩阵，符合红线 8）",
        f"- 帧：`{doc['frame']['file']}` split={doc['frame']['split']}，n=**{doc['frame']['n']}**",
        f"- 前身：`{doc['predecessor']}`（686 元评估）",
        "",
        "## 1. 区分度（AUC：把资产当二分类器，真值 = expected_verdict）",
        "",
        "| 资产 | 计分样本 | AUC |",
        "|---|---:|---:|",
    ]
    for a, v in d.items():
        lines.append(f"| `{a}` | {v['n_scored']} | {v['auc']} |")
    lines += [
        "",
        "## 2. 稳定性",
        "",
        "### 2.1 种子（682 的 5000 次重跑）",
        "",
        f"- FD 率 **{s['seed_5000_runs']['fd_rate_pct']}%**；"
        f"随机分布 mean {s['seed_5000_runs']['random_mean_rate_pct']}%、"
        f"SD {s['seed_5000_runs']['random_sd_pp']}pp",
        f"- FD 在随机分布中的百分位：**{s['seed_5000_runs']['fd_percentile_in_random_dist']}**",
        "",
        "### 2.2 环境（E1 vs E2 逐资产）",
        "",
        f"- 共享资产：{', '.join('`' + a + '`' for a in s['environment']['shared_assets'])}",
        f"- Spearman ρ = **{s['environment']['spearman_rho']}**",
        f"- ⚠ {s['environment']['note']}",
        "",
        "### 2.3 跑间（tsan）",
        "",
        f"- 有记录的样本 {s['run_to_run_tsan']['n']} 条，"
        f"稳定性字段的不同形状 {s['run_to_run_tsan']['distinct_shapes']} 种",
        "",
        "## 3. 公平性（同一资产跨缺陷类型的 recall 离散度）",
        "",
        "| 资产 | 类型数(n≥5) | recall 最低% | 最高% | 极差 pp | σ pp | 零 recall 类型数 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for a, v in sorted(f["per_asset"].items(), key=lambda kv: -kv[1]["recall_range_pp"]):
        lines.append(f"| `{a}` | {v['n_types_ge5']} | {v['recall_min_pct']} | "
                     f"{v['recall_max_pct']} | **{v['recall_range_pp']}** | "
                     f"{v['recall_sd_pp']} | {v['types_with_zero_recall']} |")
    lines += [
        "",
        f"- 偏科最严重的资产：**`{f['overall']['worst_asset_by_range']}`**",
        f"- {f['overall']['note']}",
        "",
        "## 4. 效率（676g 逐格 wall_seconds）",
        "",
        "| 资产 | n | 均值 s | 总计 s | 最慢 s | P95 s |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for a, v in e.items():
        if a == "frame_n" or not v.get("n"):
            continue
        lines.append(f"| `{a}` | {v['n']} | {v['mean_s']} | {v['total_s']} | "
                     f"{v['max_s']} | {v['p95_s']} |")
    lines += [
        "",
        f"- 效率帧 n = {e['frame_n']}",
        "",
        "## 5. 校准",
        "",
        f"- **LLM 臂 ECE = {c['llm_arm']['ece']}**（n={c['llm_arm']['n']}，真实 confidence）",
        f"- 检测器（确定性，confidence≡1）ECE = {c['detectors_deterministic']['ece']}"
        f"（n={c['detectors_deterministic']['n']}）",
        f"- {c['note']}",
        "",
        "### 5.1 LLM 可靠性曲线",
        "",
        "| 置信度区间 | n | 平均置信度 | 实际正确率 | 差 |",
        "|---|---:|---:|---:|---:|",
    ]
    for b in c["llm_arm"]["bins"]:
        lines.append(f"| {b['bin']} | {b['n']} | {b['mean_confidence']} | {b['accuracy']} | "
                     f"{b['gap']:+.4f} |")
    lines += [
        "",
        "## 6. 与 HELM / SV-COMP / DeepFact 的维度对照（**定性，非实测**）",
        "",
        "| 框架 | 领域 | 它的维度 | 本装置已覆盖 | 本装置缺失 |",
        "|---|---|---|---|---|",
    ]
    for fr in doc["framework_comparison"]:
        lines.append(f"| **{fr['framework']}** | {fr['domain']} | "
                     f"{'、'.join(fr['dimensions'])} | {'、'.join(fr['queiy_has'])} | "
                     f"{'、'.join(fr['queiy_missing'])} |")
    lines += [
        "",
        f"> 来源：{doc['framework_comparison'][0]['source']}。",
        "> 本表用于定位本装置的**方法论缺口**，不是与这些框架的性能比较。",
        "",
        "## 7. 诚实边界",
        "",
    ]
    lines += [f"- {x}" for x in doc["honest_limits"]]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
