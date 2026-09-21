#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 A3 · escaped/equivalent 的 L2b 精确工具（e-process mixture + L3 shrinkage）

- L2b：e-process mixture 的 anytime 上界。混合先验取 Beta(1,1)（均匀），e-值
  M(θ) = B(k+1, n-k+1) / (θ^k · (1-θ)^{n-k})，解 M(θ) = 1/α 得上界（二分，取 θ>k/n 的增支）。
  对 escaped（声称零逃逸 regime：k=0, n=variants）与 equivalent（k=8, n=variants）分别计算。
  给出**正上界**（禁填 0），补 617 A1 枚举器中 escaped/equivalent 的 None 占位。
  注：Beta(1,1) 混合先验较保守（anytime 保证的代价），上界宽于固定样本 CP，属诚实保守。
- L3：shrinkage 外推上界 = L1 + (1 - independence_level) · (prior - L1)，prior=0.05，independence_level=0.153。
  明确标注"外推假设，非直接测量"。
- 纯标准库（math）；读取 data/SNAPSHOT_MANIFEST_617.json 的 mutation_v7 数字（不编造）。
"""
import argparse
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "SNAPSHOT_MANIFEST_617.json")
PRIOR = 0.05
INDEPENDENCE_LEVEL = 0.153  # B1 连续性 scalar（A2 采用）


def _beta(a, b):
    return math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


def eprocess_upper_bound(k, n, alpha=0.05, iters=300):
    """e-process mixture（Beta(1,1)）anytime 上界：解 M(θ)=1/α。

    M(θ) = B(k+1, n-k+1) / (θ^k · (1-θ)^{n-k})，在 θ>k/n 的增支上二分取上界。
    """
    target = 1.0 / alpha
    log_coef = math.lgamma(k + 1) + math.lgamma(n - k + 1) - math.lgamma(n + 2)

    def M(theta):
        if theta <= 0.0 or theta >= 1.0:
            return float("inf")
        # 对数空间计算，避免 (1-theta)^(n-k) 在 theta→1 时下溢为 0
        log_m = log_coef - k * math.log(theta) - (n - k) * math.log(1.0 - theta)
        if log_m > 700.0:  # exp 溢出保护（M→∞ 即 >target）
            return float("inf")
        return math.exp(log_m)

    lo = max(1e-12, (k + 1) / (n + 2.0))  # 落在增支（θ>k/n 附近）
    hi = 1.0 - 1e-12
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if M(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def layer_l3(rate_l1, independence_level=INDEPENDENCE_LEVEL, prior=PRIOR):
    """L3 外推 shrinkage 上界（外推假设，非直接测量）。"""
    return rate_l1 + (1.0 - independence_level) * (prior - rate_l1)


def compute(manifest_path=MANIFEST):
    with open(manifest_path, encoding="utf-8") as f:
        m = json.load(f)
    mv = m["verification_baseline_frozen"]["mutation_v7"]
    n = mv["variants"]          # 1593
    equiv_k = mv["equivalent"]  # 8
    # escaped 为"声称零逃逸"regime（replay/部署未观测逃逸）：k=0, n=variants（同 A1 layer_l1）
    esc_k = 0

    esc_l1 = esc_k / n
    equiv_l1 = equiv_k / n

    esc_l2b = eprocess_upper_bound(esc_k, n)
    equiv_l2b = eprocess_upper_bound(equiv_k, n)

    esc_l3 = layer_l3(esc_l1)
    equiv_l3 = layer_l3(equiv_l1)

    return {
        "n_variants": n,
        "prior": PRIOR,
        "independence_level": INDEPENDENCE_LEVEL,
        "escaped": {
            "k": esc_k, "n": n,
            "L1_descriptive_rate": esc_l1,
            "L2b_eprocess_anytime_upper_95": esc_l2b,
            "L3_extrapolation_upper_95": esc_l3,
        },
        "equivalent": {
            "k": equiv_k, "n": n,
            "L1_descriptive_rate": equiv_l1,
            "L2b_eprocess_anytime_upper_95": equiv_l2b,
            "L3_extrapolation_upper_95": equiv_l3,
        },
        "method": {
            "L2b": "e-process mixture, Beta(1,1) prior; M(theta)=B(k+1,n-k+1)/(theta^k(1-theta)^(n-k)); solve M=1/alpha",
            "L3": "shrinkage: L1 + (1-independence_level)*(prior-L1), prior=0.05, independence_level=0.153",
        },
    }


def render_markdown(r):
    L = []
    L.append("# escaped/equivalent L2b 精确上界（618 A3 · e-process mixture + L3 shrinkage）\n")
    L.append("> 纯标准库；数字取自 `data/SNAPSHOT_MANIFEST_617.json` 的 mutation_v7"
             "（variants=%d, equivalent=%d）；escaped 为声称零逃逸 regime（k=0, n=%d，同 617 A1 `layer_l1`）。\n"
             % (r["n_variants"], r["equivalent"]["k"], r["n_variants"]))
    L.append("> **L3 明确标注：外推假设，非直接测量**（依赖独立性 scalar=%s，verifier=1 硬上限）。\n"
             % r["independence_level"])
    for name in ("escaped", "equivalent"):
        d = r[name]
        L.append("## %s（k=%d, n=%d）\n" % (name, d["k"], d["n"]))
        L.append("- L1 描述性经验率：`%.6f%%`" % (d["L1_descriptive_rate"] * 100))
        L.append("- **L2b e-process mixture anytime 上界（95%%）：`%.6f%%`**"
                 "（正上界，禁填 0；区别于 A1 枚举器 None 占位；Beta(1,1) 混合先验，保守）"
                 % (d["L2b_eprocess_anytime_upper_95"] * 100))
        L.append("- L3 shrinkage 外推上界（95%%）：`%.6f%%` ⚠️ **外推假设，非直接测量**\n"
                 % (d["L3_extrapolation_upper_95"] * 100))
    L.append("## 与 617 A1 枚举器的关系\n")
    L.append("- 617 A1 `tools/escape_rate_estimand.py` 对 escaped/equivalent 的 `anytime_cs_upper_95` 标 `None`"
             "（有意为之的诚实占位，禁填 0）。")
    L.append("- 本工具给出 617 A2 方法文档（`data/confidence_sequence_l3_shrinkage.md`）的**可执行 L2b**：e-process mixture 正上界。")
    L.append("- blocked 类型的 L2b 仍由 A1 的置信序列 CS=`0.9062%%` 承担（任何时刻上界）；本工具仅补 escaped/equivalent 两类。")
    L.append("\n## 方法\n")
    L.append("- L2b：e-process mixture（Beta(1,1) 混合先验），解 M(θ)=1/α，"
             "M(θ)=B(k+1,n-k+1)/(θ^k·(1-θ)^{n-k})；在 θ>k/n 增支二分取上界。")
    L.append("- L3：shrinkage = L1 + (1 - %s) × (%s - L1)，prior=%s。" % (r["independence_level"], r["prior"], r["prior"]))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="618 A3 escaped/equivalent L2b (e-process) + L3")
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "escape_rate_l2b_618.md"))
    args = ap.parse_args()
    r = compute(args.manifest)
    txt = render_markdown(r)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
