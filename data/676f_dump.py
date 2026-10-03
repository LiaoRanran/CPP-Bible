#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""676f：把结果 JSON 里的关键块打成人类可读摘要（写报告用，只读）。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "data" / "a5_676f_results.json").read_text(encoding="utf-8"))


def line(*parts):
    print("  ".join(str(p) for p in parts))


print("### 样本统计")
s = d["sample_stats"]
line("n_total", s["n_total"], "| 派生", s["n_derivation"], "| 评估", s["n_evaluation"],
     "| planted=true", s["n_planted_true"], "| planted=false", s["n_planted_false"],
     "| legacy", s["n_legacy"], "| expansion", s["n_expansion"])
line("批次", s["by_batch"])
line("类型组", s["by_group"])
line("切分×类型组", s["by_split_x_group"])
line("去重", s["dedup"]["by_id"], s["dedup"]["by_content"])

print("\n### 矩阵质量")
q = d["matrix_quality"]
line("覆盖缺格", q["coverage"]["n_missing_cells"])
line("unknown 比例", q["unknown_ratio"])
line("OR 分布", q["or_verdict_distribution"])
line("墙钟(按资产)", q["wall_seconds_by_asset"])
v = q["verify_old_vs_673r"]
line("旧样本抽检 vs 673r：", v.get("agree"), "/", v.get("n_cells"), "=", v.get("agree_pct"), "%  差异",
     len(v.get("diffs", [])))
st = q["stability_concurrency"]
if st.get("status") == "ok":
    line("稳定性(并发样本 tsan 3 轮)：n=", st["n_samples"], "三轮全同", st["all_rounds_identical"],
         "=", st["identical_pct"], "%  翻转样本", st["flip_samples"])
    mism = [k for k, x in st["per_sample"].items() if not x["matches_mode"]]
    line("  与矩阵值一致性：不一致", len(mism), mism[:12])

print("\n### 派生集 fail_hits")
line(d["derivation_fail_hits"])

print("\n### 主分析（8 候选）")
for r in d["primary_main_8candidates"]["by_k_compact"]:
    line(f"k={r['k']}", f"FD {r['fd_rate_pct']}% ({r['fd_k']}/{r['n']})",
         f"Rnd {r['random_rate_pct']}%", f"Static {r['static_rate_pct']}%",
         f"fullpool {r['full_pool_rate_pct']}%",
         f"Δ {r['delta_fd_minus_random_pp']:+.2f}pp CI {r['delta_ci95_pp']}",
         f"p {r['mcnemar_p']:.4g} b={r['b']} c={r['c']}",
         f"2000次均值 {r['random_2000']['mean_rate_pct']}% FD严格更优 {r['random_2000']['fd_strictly_better_frac']}",
         "| FD资产", r["fd_assets"])

print("\n### 并列分析（剔除退化，候选 %d）" % len(d["co_primary_excl_degenerate"]["candidates"]))
line("候选", d["co_primary_excl_degenerate"]["candidates"])
for r in d["co_primary_excl_degenerate"]["by_k_compact"]:
    line(f"k={r['k']}", f"FD {r['fd_rate_pct']}%", f"Rnd {r['random_rate_pct']}%",
         f"Static {r['static_rate_pct']}%", f"Δ {r['delta_fd_minus_random_pp']:+.2f}pp",
         f"CI {r['delta_ci95_pp']}", f"p {r['mcnemar_p']:.4g}",
         f"均值 {r['random_2000']['mean_rate_pct']}% 更优 {r['random_2000']['fd_strictly_better_frac']}",
         "| FD资产", r["fd_assets"])
line("派生集口径候选", d["co_primary_excl_degenerate"]["candidates_derivation_rule"])
for r in d["co_primary_excl_degenerate"]["by_k_compact_derivation_rule"]:
    line(f"  k={r['k']}", f"FD {r['fd_rate_pct']}%", f"Rnd {r['random_rate_pct']}%",
         f"Δ {r['delta_fd_minus_random_pp']:+.2f}pp p {r['mcnemar_p']:.4g}")

print("\n### 逐资产（全池 / 派生 / 评估 catch 率）")
ad = d["asset_diagnostics"]
for a in ad["full_pool"]:
    f, de, e = ad["full_pool"][a], ad["derivation"][a], ad["evaluation"][a]
    line(f"{a:15s}", f"全池 {f['catch']:4d}/{f['n']} {f['catch_rate_pct']:6.2f}% unk {f['unknown_rate_pct']:5.2f}%",
         f"| 派生 {de['catch_rate_pct']:6.2f}%", f"| 评估 {e['catch_rate_pct']:6.2f}%")
line("退化（全池率）", d["asset_diagnostics"]["degenerate_full_pool"])
line("退化（派生集率）", d["asset_diagnostics"]["degenerate_derivation"])

print("\n### 子组（各缺陷组，k=4，评估集）")
for g, blk in d["subgroups"].items():
    if blk.get("status") == "skip":
        line(f"{g:22s} skip: {blk['why']}")
        continue
    line(f"{g:22s} n_der={blk['n_derivation']:4d} n_ev={blk['n_evaluation']:4d}",
         f"FD {blk['fd_rate_pct']}% Rnd {blk['random_rate_pct']}% Static {blk['static_rate_pct']}%",
         f"Δ {blk['delta_fd_minus_random_pp']:+.2f}pp p {blk['mcnemar_p']:.4g}",
         f"CI {blk['delta_ci95_pp']}")
print("  多重校正：", d["subgroup_multiplicity"].get("n_tests"))
for r in (d["subgroup_multiplicity"].get("rows") or []):
    line(f"   {r['group']:22s} p_raw {r['p_raw']:.4g} p_bh {r['p_bh_fdr']:.4g} p_bonf {r['p_bonferroni']:.4g} Δ {r['delta_pp']:+.2f} n {r['n_evaluation']}")

print("\n### planted=false / planted=true / expG-planted=false（k=4）")
for name in ("planted_false", "planted_true", "expG_planted_false_only"):
    b = d[name]
    if b.get("status") == "skip":
        line(name, "skip")
        continue
    line(f"{name:24s} n_der={b['n_derivation']:4d} n_ev={b['n_evaluation']:4d}",
         f"OR检出 {b['or_catch_rate_evaluation_pct']}% | FD {b['fd_rate_pct']}% Rnd {b['random_rate_pct']}%",
         f"Δ {b['delta_fd_minus_random_pp']:+.2f}pp p {b['mcnemar_p']:.4g} CI {b['delta_ci95_pp']}",
         "批次", b.get("n_evaluation_batches"))

print("\n### 旧口径时间切分视角（派生=legacy / 评估=扩样）")
lv = d["legacy_time_split_view"]
line(lv["note"])
line("legacy fail_hits", lv["fail_hits"])
line("主（8 候选）", lv["primary_8candidates"]["fd_rate_pct"], "vs", lv["primary_8candidates"]["random_rate_pct"],
     "Δ", lv["primary_8candidates"]["delta_fd_minus_random_pp"], "p", lv["primary_8candidates"]["mcnemar_p"])
line("并列", lv["co_candidates"], lv["co_primary"]["fd_rate_pct"], "vs", lv["co_primary"]["random_rate_pct"],
     "Δ", lv["co_primary"]["delta_fd_minus_random_pp"], "p", lv["co_primary"]["mcnemar_p"])

print("\n### oracle 连续性（不作证据）")
o = d["oracle_fullset_continuity"]["primary"]
line("FD", o["fd_rate_pct"], "Rnd", o["random_rate_pct"], "Δ", o["delta_fd_minus_random_pp"], "p", o["mcnemar_p"])
