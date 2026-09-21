#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""617 A1 · 逃逸率 estimand 三层拆分枚举器（纯标准库，只读 frozen baseline）

按逃逸类型（blocked / escaped / equivalent）枚举三层 estimand：
  L1 描述性   —— 观测样本内经验率（永远有效，仅描述已观测）
  L2 推断性   —— L2a 固定终点(CP/Wilson) + L2b anytime(CS)，标注连续查看下有效性
  L3 外推     —— 对部署泛化的折扣(shrinkage)，需独立性 + 他验

铁律：本工具只读 standing baseline 数字，不做任何重跑。L2 推断边界取自 616 复算；
Wilson 仅为可复算近似代理（精确 CP 见 data/616_baseline.md）。escaped/equivalent 的
精确 L2b 待 A2(e-process mixture)/A3(conformal) 补全，此处标 None(无效)。
"""
import argparse
import json
import math
import sys

# frozen baseline (data/mutation/full_baseline_v7.json / 616)
FROZEN = {
    "variants": 1593,
    "blocked": 1405,
    "escaped": 1,
    "n_a": 179,
    "equivalent": 8,
    "judge_denom": 1406,  # blocked + escaped
}

# standing baseline 推断层（616 复算，连续查看下仅 L2b 有效）
INFERENCE = {
    "blocked": {"cp_fixed_upper_95": 0.003370, "cs_anytime_upper_95": 0.009062},
    "escaped": {"cp_fixed_upper_95": None, "cs_anytime_upper_95": None},
    "equivalent": {"cp_fixed_upper_95": None, "cs_anytime_upper_95": None},
}

L3_PRIOR = 0.05  # 外推保守先验（worst-case-ish），shrinkage 目标


def wilson_upper(k, n, z=1.96):
    """Wilson 得分区间上界（标准库近似，仅作可复算代理，非精确 CP）。"""
    if n == 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return center + half


def layer_l1(escape_type):
    """L1 描述性：观测样本内的经验率。

    三种逃逸 regime 的 L1 口径（与 data/estimand_three_layer.md 一致）：
      blocked    —— 已观测到的逃逸（judge 集内）：1 / 1406（= blocked+escaped 可判分母）。
      escaped    —— 声称零逃逸的 regime（replay/部署未观测逃逸）：0 / 1593（名义 0，L2a 无效）。
      equivalent —— 语义等价误判：8 / 1593。
    """
    if escape_type == "blocked":
        k, n = 1, FROZEN["judge_denom"]
    elif escape_type == "escaped":
        k, n = 0, FROZEN["variants"]
    elif escape_type == "equivalent":
        k, n = FROZEN["equivalent"], FROZEN["variants"]
    else:
        raise ValueError("escape_type must be blocked/escaped/equivalent")
    return {
        "k": k,
        "n": n,
        "rate": k / n,
        "validity": "valid_descriptive",
        "applies_to": "observed_frozen_sample_only",
    }


def layer_l2(escape_type):
    """L2 推断性：固定终点 vs anytime-valid。"""
    inf = INFERENCE[escape_type]
    l1 = layer_l1(escape_type)
    return {
        "fixed_endpoint_cp_upper_95": inf["cp_fixed_upper_95"],
        "fixed_endpoint_wilson_upper_95_approx": wilson_upper(l1["k"], l1["n"]),
        "anytime_cs_upper_95": inf["cs_anytime_upper_95"],
        "note": (
            "L2a 固定终点仅当停止点预注册且非连续查看有效；"
            "L2b anytime(e-process)在连续决策下有效。"
            "escaped/equivalent 精确 L2 需 e-process mixture / conformal（见 A2/A3）。"
        ),
    }


def layer_l3(escape_type, independence_level=1.0):
    """L3 因果/外推：对部署泛化的折扣。independence_level∈[0,1]，越小折扣越多。"""
    if not (0.0 <= independence_level <= 1.0):
        raise ValueError("independence_level must be in [0,1]")
    l1 = layer_l1(escape_type)["rate"]
    shrink = l1 + (1 - independence_level) * (L3_PRIOR - l1)
    return {
        "deployment_extrapolation_rate": shrink,
        "independence_level": independence_level,
        "note": (
            "L3 外推需独立第二实现 + 他验；当前信任根 partially_anchored，"
            "L3 为保守上界（shrinkage 向先验 0.05 收缩）。"
        ),
    }


def enumerate_layers(escape_type, independence_level=1.0):
    return {
        "escape_type": escape_type,
        "L1_descriptive": layer_l1(escape_type),
        "L2_inferential": layer_l2(escape_type),
        "L3_causal_extrapolation": layer_l3(escape_type, independence_level),
    }


def selftest():
    """只读自验证（不写任何文件）。返回失败项列表，空列表 = 通过。"""
    fails = []
    for t in ("blocked", "escaped", "equivalent"):
        e = enumerate_layers(t, 0.153)
        l1 = e["L1_descriptive"]
        if not (0 <= l1["k"] <= l1["n"]):
            fails.append("%s L1 k>n：%s/%s" % (t, l1["k"], l1["n"]))
        if abs(l1["rate"] - l1["k"] / l1["n"]) > 1e-12:
            fails.append("%s L1 rate 与 k/n 不一致" % t)
        l2 = e["L2_inferential"]
        if t in ("escaped", "equivalent") and l2["anytime_cs_upper_95"] is not None:
            fails.append("%s L2b 应为 None 占位（禁填 0）" % t)
        l3 = e["L3_causal_extrapolation"]["deployment_extrapolation_rate"]
        lo, hi = min(l1["rate"], L3_PRIOR), max(l1["rate"], L3_PRIOR)
        if not (lo - 1e-12 <= l3 <= hi + 1e-12):
            fails.append("%s L3 未落在 [L1, prior] 区间" % t)
    b = layer_l2("blocked")
    if not (0.0 < b["fixed_endpoint_cp_upper_95"] < 1.0):
        fails.append("blocked L2a 非正上界")
    if not (0.0 < b["anytime_cs_upper_95"] < 1.0):
        fails.append("blocked L2b 非正上界")
    if b["anytime_cs_upper_95"] <= b["fixed_endpoint_cp_upper_95"]:
        fails.append("blocked CS 应宽于 CP（连续查看代价）")
    if wilson_upper(0, 0) is not None:
        fails.append("wilson_upper(0,0) 应为 None（n=0 不得填 0）")
    w = wilson_upper(1, FROZEN["judge_denom"])
    if w is None or not (0.0 < w < 1.0):
        fails.append("wilson_upper(1, judge_denom) 越界")
    # L3 shrinkage 端点退化
    if abs(layer_l3("blocked", 1.0)["deployment_extrapolation_rate"]
           - layer_l1("blocked")["rate"]) > 1e-12:
        fails.append("L3 在 independence_level=1 时未退化为 L1")
    if abs(layer_l3("blocked", 0.0)["deployment_extrapolation_rate"] - L3_PRIOR) > 1e-12:
        fails.append("L3 在 independence_level=0 时未退化为 prior")
    return fails


def main():
    ap = argparse.ArgumentParser(description="617 A1 逃逸率 estimand 三层枚举器")
    ap.add_argument("--escape-type", choices=["blocked", "escaped", "equivalent"])
    ap.add_argument("--independence-level", type=float, default=1.0)
    ap.add_argument("--check", action="store_true", help="只读自验证（不写文件），exit 0=通过")
    args = ap.parse_args()
    if args.check:
        fails = selftest()
        for f in fails:
            print("FAIL: %s" % f)
        print("617 A1 --check: %s" % ("PASS" if not fails else "FAIL"))
        sys.exit(0 if not fails else 1)
    if args.escape_type is None:
        ap.error("--escape-type is required")
    out = enumerate_layers(args.escape_type, args.independence_level)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
