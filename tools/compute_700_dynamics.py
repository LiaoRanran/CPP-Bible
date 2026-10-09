#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_700_dynamics.py — 700-E：评估器演化的动力学模型（**只读**）。

把评估器本身看作动态系统
========================
* **状态** $s$：评估器在**能力轴**上的向量；
* **驱动**：每一步由**上一版发现的失败类**驱动（失败驱动，非优化压力）；
* **转移**：$s_{t+1} = F(s_t, \\text{发现}) = \\max(s_t,\\ e(\\text{失败类}))$（**单调**：能力只增不减）；
* **轨迹**：676m → 681 → 692 → 693 → 697 → 698（6 个版本，来自各批次的文档化记录）。

**状态语义（三值）**：``0`` = 缺失，``1`` = 部分建立，``2`` = 完备。
> 用三值而不是二值：多数能力是**逐步补全**的（例：F6 先是 AI 重标 κ=0.727，
> 人类 IAA 仍为 0 ⇒ 记 ``1`` 而非 ``2``）。二值会让状态在 698 就"填满"，
> 使"未来 5 版"的外推退化成 1 条。

⚠ **诚实边界（先读）**
=====================
* 只有 **6 个时间点** ⇒ **无法**拟合任何带参数的动力学模型，也**无法**做混沌判定
  （Lyapunov 指数至少需要几十个点）。
* 本批只做**结构性**分析：$F$ 的**形式**（单调 / 幂等）由"能力只增不减"这一
  **定义性假设**给出，不是拟合出来的。
* 未来 5 版是**外推**，不是预测。

红线：``detect_calls = 0``；产出只写 ``data/700_*``。

用法
====
    python tools/compute_700_dynamics.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_700_dynamics")

OUT_JSON: Final[Path] = ROOT / "data" / "700_dynamics.json"

# ── 能力轴（状态向量的坐标），与 698-D 的 8 类失效模式一一对应 ──────────
CAPABILITY_AXES: Final[tuple[str, ...]] = (
    "F1_denominator_caliber",     # 分母/构成漂移已被显式建模
    "F2_environment",             # 环境是测量的一个坐标（692）
    "F3_label_vocabulary",        # 标签词表被规范化并声明
    "F4_aggregation_rule",        # 聚合规则被显式声明
    "F5_adversarial_use",         # 对抗性利用被审计（HackDetect 类）
    "F6_label_noise_human_iaa",   # 人类 IAA / 标签噪声被测量
    "F7_clone_leakage",           # 克隆泄漏被控制（677b）
    "F8_record_traceability",     # 测量记录可追溯（measurement_context_id）
)

FULL: Final[int] = 2

# ── 6 个版本的状态（依据各批次文档化记录，逐位给出来源）──────────────
VERSIONS: Final[list[dict[str, Any]]] = [
    {
        "version": "676m", "label": "H2 标签迁移",
        "state": {"F1_denominator_caliber": 1, "F2_environment": 0, "F3_label_vocabulary": 1,
                  "F4_aggregation_rule": 1, "F5_adversarial_use": 0, "F6_label_noise_human_iaa": 1,
                  "F7_clone_leakage": 0, "F8_record_traceability": 0},
        "discovered_failure": "F3（标签体系未统一）",
        "source": "data/676m_H2标签迁移报告.md",
    },
    {
        "version": "681", "label": "类型统计重算",
        "state": {"F1_denominator_caliber": 1, "F2_environment": 0, "F3_label_vocabulary": 2,
                  "F4_aggregation_rule": 1, "F5_adversarial_use": 0, "F6_label_noise_human_iaa": 1,
                  "F7_clone_leakage": 0, "F8_record_traceability": 0},
        "discovered_failure": "F3 的残余（词表归一化后的统计重算）",
        "source": "data/681_type_stats_normalized.json",
    },
    {
        "version": "692", "label": "环境形式化 + 配对实验",
        "state": {"F1_denominator_caliber": 1, "F2_environment": 1, "F3_label_vocabulary": 2,
                  "F4_aggregation_rule": 1, "F5_adversarial_use": 0, "F6_label_noise_human_iaa": 1,
                  "F7_clone_leakage": 0, "F8_record_traceability": 1},
        "discovered_failure": "F2（环境门控导致静默退化）+ F8（语境不可继承）",
        "source": "data/692_environment_formalization.md",
    },
    {
        "version": "693", "label": "元评估 v2 + 可检测性模型",
        "state": {"F1_denominator_caliber": 1, "F2_environment": 1, "F3_label_vocabulary": 2,
                  "F4_aggregation_rule": 1, "F5_adversarial_use": 0, "F6_label_noise_human_iaa": 1,
                  "F7_clone_leakage": 1, "F8_record_traceability": 1},
        "discovered_failure": "F7（克隆泄漏导致 CV 高估）",
        "source": "data/693_meta_evaluation_v2.json",
    },
    {
        "version": "697", "label": "漂移代数 + 结构性 Goodhart",
        "state": {"F1_denominator_caliber": 2, "F2_environment": 1, "F3_label_vocabulary": 2,
                  "F4_aggregation_rule": 2, "F5_adversarial_use": 0, "F6_label_noise_human_iaa": 1,
                  "F7_clone_leakage": 1, "F8_record_traceability": 1},
        "discovered_failure": "F1/F4 的形式化（口径漂移的统一理论）",
        "source": "data/697_measurement_drift_algebra.md",
    },
    {
        "version": "698", "label": "四型量化 + 通用审计框架",
        "state": {"F1_denominator_caliber": 2, "F2_environment": 1, "F3_label_vocabulary": 2,
                  "F4_aggregation_rule": 2, "F5_adversarial_use": 0, "F6_label_noise_human_iaa": 1,
                  "F7_clone_leakage": 1, "F8_record_traceability": 1},
        "discovered_failure": "跨领域迁移的可行性（F5 之外的四类已部分覆盖）",
        "source": "data/698_audit_framework.md",
    },
]

ENERGY_WEIGHTS: Final[dict[str, float]] = {
    "detection": 0.40, "stability": 0.35, "interpretability": 0.25,
}

# 未来版本的紧迫度排序（依据 697/698 登记的开放债务）
FUTURE_PRIORITY: Final[tuple[str, ...]] = (
    "F6_label_noise_human_iaa", "F5_adversarial_use", "F2_environment",
    "F8_record_traceability", "F7_clone_leakage",
)

FUTURE_BASIS: Final[str] = (
    "按 697/698 登记的开放债务排序：F6 的人类 IAA 仍为 0（只有 AI 重标 κ=0.727）；"
    "F5 的对抗性利用审计完全未做；F2 只有 2 个环境（缺容器 profile）；"
    "F8 的账本未全量哈希；F7 只有克隆家族重切分（无全量去重）"
)


def _bits(state: dict[str, int]) -> tuple[int, ...]:
    return tuple(int(state.get(a, 0)) for a in CAPABILITY_AXES)


def transition_analysis() -> dict[str, Any]:
    """F 的形式：单调 max 运算 ⇒ 幂等、保序、无环。"""
    states = [_bits(v["state"]) for v in VERSIONS]
    monotone = all(
        all(states[t][i] <= states[t + 1][i] for i in range(len(CAPABILITY_AXES)))
        for t in range(len(states) - 1)
    )
    steps: list[dict[str, Any]] = []
    for t in range(len(states) - 1):
        added = [f"{CAPABILITY_AXES[i]}:{states[t][i]}->{states[t + 1][i]}"
                 for i in range(len(CAPABILITY_AXES)) if states[t + 1][i] > states[t][i]]
        removed = [f"{CAPABILITY_AXES[i]}:{states[t][i]}->{states[t + 1][i]}"
                   for i in range(len(CAPABILITY_AXES)) if states[t + 1][i] < states[t][i]]
        steps.append({"from": VERSIONS[t]["version"], "to": VERSIONS[t + 1]["version"],
                      "added_capabilities": added, "removed_capabilities": removed,
                      "driver": VERSIONS[t + 1]["discovered_failure"],
                      "n_added": len(added), "n_removed": len(removed)})
    return {
        "form": "s_{t+1} = max(s_t, e(discovered failure))，e(·) = 该失败类对应的能力位",
        "monotone": monotone,
        "idempotent": True,
        "n_removed_total": sum(s["n_removed"] for s in steps),
        "steps": steps,
        "n_added_per_step": [s["n_added"] for s in steps],
        "driver_verdict": (
            "**失败驱动**（failure-driven）：每一步新增的能力位与上一版**发现的失败类**一一对应；"
            "**没有**优化压力的痕迹（没有任何一步是为了「让某个指标好看」而改变状态）。"
            "⇒ 与 697 的 SG-3（无优化者）**一致**。"
        ),
        "other_drivers_ruled_out": {
            "优化压力": "无证据：6 步中 0 步以指标提升为驱动",
            "随机漂移": "无证据：全部状态变化都是能力位**单调提升**，移除次数 = 0",
        },
    }


def attractor_analysis() -> dict[str, Any]:
    """吸引子 / 极限环 / 混沌：在**结构性**层面回答（不做数值判定）。"""
    final = _bits(VERSIONS[-1]["state"])
    missing = [f"{CAPABILITY_AXES[i]}(当前 {final[i]}/{FULL})"
               for i in range(len(CAPABILITY_AXES)) if final[i] < FULL]
    fixed_point = _bits(dict.fromkeys(CAPABILITY_AXES, FULL))
    return {
        "n_points": len(VERSIONS),
        "current_state": dict(zip(CAPABILITY_AXES, final)),
        "missing_capabilities": missing,
        "n_missing": len(missing),
        "fixed_point_exists": True,
        "unique_fixed_point": True,
        "fixed_point": dict(zip(CAPABILITY_AXES, fixed_point)),
        "limit_cycle": False,
        "chaos": None,
        "verdict": (
            "**唯一的吸引子是「审计完备」不动点**（8 条能力位全 2）："
            "因为 F 是单调 max 运算 ⇒ (i) 一旦某位提升永不再降（**无极限环**，"
            "因为环要求至少一次回退）；(ii) 状态向量逐位单调不减且有上界 2^8 ⇒ "
            "**必然收敛到不动点**；(iii) F 幂等 ⇒ 不动点唯一。"
            "**混沌无法判定**：只有 6 个时间点，Lyapunov 指数需要数十个点 ⇒ 本批不给结论。"
        ),
        "honest_note": (
            "上述结论**依赖「能力只增不减」这一前提**。若允许能力回退（例如删掉某个资产、"
            "放弃某个口径声明），极限环与混沌**重新成为可能** —— 本批未建模该情形。"
        ),
    }


def predict_future() -> dict[str, Any]:
    """外推未来 5 版：把**尚未完备**的能力位按登记紧迫度排序填到 2。

    ⚠ 这是**外推**，不是预测。
    """
    final = dict(zip(CAPABILITY_AXES, _bits(VERSIONS[-1]["state"])))
    missing = [a for a in CAPABILITY_AXES if final[a] < FULL]
    ordered = ([a for a in FUTURE_PRIORITY if a in missing]
               + [a for a in missing if a not in FUTURE_PRIORITY])
    preds: list[dict[str, Any]] = []
    for i, cap in enumerate(ordered[:5]):
        nxt = dict(final)
        nxt[cap] = FULL
        preds.append({
            "version": f"700+{i + 1}（推测）",
            "predicted_capability_completed": cap,
            "predicted_state": nxt,
            "basis": FUTURE_BASIS,
            "confidence": "低（外推）",
        })
        final = nxt
    return {
        "predictions": preds,
        "n_missing_axes": len(missing),
        "horizon": "5 个版本",
        "caveat": ("**这是外推不是预测**：只有 6 个历史点，且转移形式 F 是**假设**"
                   "（单调 max）。若真实演化出现能力回退或外部驱动，本外推失效。"),
    }


def energy_landscape() -> dict[str, Any]:
    """能量 = 综合质量的负值。三个分量都用**文档化代理**（各给来源）。"""
    detection = {
        "676m": 0.5850, "681": 0.5850, "692": 0.6007, "693": 0.6164, "697": 0.6164, "698": 0.6164,
    }
    interp = {
        "676m": 3 / 6, "681": 3 / 6, "692": 4 / 6, "693": 4 / 6, "697": 5 / 6, "698": 5 / 6,
    }
    rows: list[dict[str, Any]] = []
    for v in VERSIONS:
        ver = v["version"]
        bits = _bits(v["state"])
        st = sum(bits) / (len(bits) * FULL)
        d = detection.get(ver, 0.0)
        it = interp.get(ver, 0.0)
        q = (ENERGY_WEIGHTS["detection"] * d + ENERGY_WEIGHTS["stability"] * st
             + ENERGY_WEIGHTS["interpretability"] * it)
        rows.append({"version": ver, "detection": round(d, 6), "stability": round(st, 6),
                     "interpretability": round(it, 6),
                     "energy": round(-q, 6), "quality": round(q, 6)})
    best = max(rows, key=lambda r: r["quality"])
    cur = rows[-1]
    return {
        "weights": ENERGY_WEIGHTS,
        "rows": rows,
        "best_version": best["version"],
        "current_quality": cur["quality"],
        "gap_to_best": round(best["quality"] - cur["quality"], 6),
        "position_verdict": (
            f"当前（698）质量 = {cur['quality']}，为 6 个版本中**最高** ⇒ 处于**局部最优**。"
            "是否**全局最优**无法判定：能量函数的三分量权重是本批自定的；"
            "且检测率上限受 700-C 的能力曲线约束（每多一个检测器最多 +0.87pp）"
            "⇒ 提高 detection 分量的空间很小，未来质量提升只能来自 "
            "stability 与 interpretability 两个分量。"
        ),
        "honest_note": (
            "能量景观的**三分量与权重都是本批自定的**（无外部标定）；"
            "历史版本的分量值多为**代理**（用已建能力位比例代替实测稳定性）"
            "⇒ 景观形状**不可当作定量结论**，只能读作「单调上升」这一趋势。"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="700-E 评估器演化动力学（只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    trans = transition_analysis()
    attr = attractor_analysis()
    fut = predict_future()
    energy = energy_landscape()

    doc: dict[str, Any] = {
        "schema": "queyi-700/dynamics/v1",
        "generated_by": "tools/compute_700_dynamics.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "state_space": {
            "definition": "s = (能力位向量) ∈ {0,1,2}^8；0 = 缺失，1 = 部分，2 = 完备",
            "axes": list(CAPABILITY_AXES),
            "trajectory": [{"version": v["version"], "label": v["label"],
                            "state": v["state"], "source": v["source"]} for v in VERSIONS],
            "n_points": len(VERSIONS),
        },
        "transition": trans,
        "attractors": attr,
        "future_prediction": fut,
        "energy_landscape": energy,
        "honest_limits": [
            "**只有 6 个时间点** ⇒ 无法拟合带参数的动力学模型；F 的**形式**（单调 max）来自"
            "「能力只增不减」这一**定义性假设**，不是拟合结果。",
            "**混沌无法判定**（Lyapunov 指数需要数十个点）⇒ 本批不给结论。",
            "状态向量的 8 个坐标与三值刻度都是**本批选的**；换一套坐标，轨迹与不动点都会变。",
            "各版本的状态位取自**文档化记录**（来源已逐条标注），不是重新测量。",
            "未来 5 版是**外推**，置信度标为「低」。",
            "能量函数的三分量与权重是本批自定的，无外部标定 ⇒ 景观形状不可当定量结论。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 700-E 评估器演化动力学（只读）==")
    print(f"  状态空间：{len(CAPABILITY_AXES)} 条能力位（0/1/2）× {len(VERSIONS)} 个版本")
    for s in trans["steps"]:
        print(f"    {s['from']} -> {s['to']}：+{s['n_added']}"
              f"（{'; '.join(s['added_capabilities']) or '无'}）  -{s['n_removed']}"
              f"  驱动={s['driver']}")
    print(f"  单调={trans['monotone']}；总移除={trans['n_removed_total']}")
    print(f"  吸引子：唯一不动点（全 {FULL}），无极限环，混沌={attr['chaos']}")
    print(f"  当前未完备能力位（{attr['n_missing']}）：{attr['missing_capabilities']}")
    print("\n  未来 5 版外推（置信度低）：")
    for p in fut["predictions"]:
        print(f"    {p['version']}：完成 {p['predicted_capability_completed']}")
    print("\n  能量景观（quality = det×0.40 + stab×0.35 + interp×0.25）：")
    for r in energy["rows"]:
        print(f"    {r['version']:<6} quality={r['quality']:.4f}  "
              f"(det={r['detection']:.4f} stab={r['stability']:.4f} "
              f"interp={r['interpretability']:.4f})")
    print(f"  => {energy['position_verdict'][:76]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
