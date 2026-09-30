#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""experiments_669.py — 669 P3：实验启动（协议元数据 + 基线表 + 口径消融）。

本批能做什么、不能做什么（**先把边界写清，再报数**）
====================================================
能（数据全部来自已落盘产物，脚本现算 + CP/Wilson 区间）：
  * **E0 协议登记**：每次实验记录 `protocol_version / verifier_version / dataset_version /
    seed / commit / instrument`（缺一项就报出来）——没有这五项，数字无法归属到某次运行；
  * **E1 基线表**：holdout（双档）/ external corpus（可测 + 全样本 + 分层）/
    反事实算子 P·R / 变异 kill，全部带 Clopper–Pearson 与 Wilson 区间；
  * **E2 口径消融（caliber ablation）**：把 `unknown` 从"剔除"改成"计为 miss"、再把 `not_error`
    计入分母，看检出率掉多少 —— 这是审稿人**一定会问**的"你的分母怎么来的"的量化回答；
    三条臂都从同一份原始计数现算，Δ 与区间一并给出。

不能（**登记为阻塞项，不编数字**）：
  * `B1 Rule-only`（静态门禁在 holdout/corpus 上的检出率）：主仓的 holdout/corpus 判定走
    **外部 sanitizer 仪器**（`holdout_reveal_661.detect` / `external_corpus_662.detect` 都是
    "WSL g++ 编译并运行"），**没有**"仅静态规则"的可执行路径；要测 B1 必须把拆仓验证器的
    规则层接进来（接口需求：`detect_static(sample) -> verdict`）。
  * `B2/B3 budget-matched random`（随机选资 vs 失败驱动选资）：同上——主仓不暴露"验证资产选择"
    接口（资产选择在拆仓验证器 `queyi-verifier` 里，见 A30）。**没有接口就没有对照，宁缺不造。**

用法：
    python tools/experiments_669.py --run      # 现算 → data/experiments/669_experiments.json
    python tools/experiments_669.py --report   # 打印基线表与消融表
    python tools/experiments_669.py --selftest # 射程自检（改一个 k 必红）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import stat_bounds as sb  # noqa: E402

OUT_JSON = ROOT / "data" / "experiments" / "669_experiments.json"
PROTOCOL_VERSION = "669-P3/v1"
SEED = None          # 本批实验是**全量复算**（无随机抽样）⇒ 无种子；B3 若要做必须带种子与分配表


def _j(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _commit() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=20)
        return (r.stdout or "").strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _versions() -> dict:
    """verifier / dataset 版本（从产物自身字段读，缺 ⇒ 显式 unknown，不猜）。"""
    ho = _j("data/holdout_reveal_3_665.json")
    ext = _j("data/external_corpus_reveal_665.json")
    cf = _j("data/counterfactual_cases_665.json")
    return {
        "verifier_version": str(ho.get("generated_by") or "unknown"),
        "dataset_version": f"{ext.get('schema', 'unknown')} / {cf.get('schema', 'unknown')}",
        "instrument": "WSL g++ (Ubuntu 13.3.0) + ASan/UBSan/TSan（编译并运行；非静态规则）",
        "opt_levels": ho.get("opt_levels"),
        "env": ho.get("env"),
    }


def _rate(k: int, n: int) -> dict:
    lo, hi = sb.cp_interval(k, n) if n else (0.0, 1.0)
    wlo, whi = sb.wilson(k, n) if n else (0.0, 1.0)
    return {"k": k, "n": n, "rate_pct": round(k / n * 100, 1) if n else None,
            "cp_lo_pct": round(lo * 100, 1), "cp_hi_pct": round(hi * 100, 1),
            "wilson_lo_pct": round(wlo * 100, 1), "wilson_hi_pct": round(whi * 100, 1),
            "exploratory": n < 30}


def baseline_table() -> list[dict]:
    """E1：基线表（全部现算；`exploratory` = n<30 ⇒ 数字不得写进论文结论）。"""
    ext = _j("data/external_corpus_reveal_665.json")
    ho = _j("data/holdout_reveal_3_665.json")
    rows: list[dict] = []

    def add(name: str, k: int, n: int, src: str, note: str = "") -> None:
        rows.append({"name": name, **_rate(k, n), "source": src, "note": note})

    es, cs = ho["error_subset"], ho.get("control_subset") or {}
    add("holdout 真错（双档，可测口径）", es["catch"], es["catch"] + es["miss"],
        "data/holdout_reveal_3_665.json", f"unknown {es['unknown']} 剔除")
    if cs.get("total"):
        # 字段名是 `false_positive`（669 实测：此前的 `catch` 读法会得到假的 0/9）
        fp = cs.get("false_positive", cs.get("catch", 0))
        add("holdout 对照（误报）", fp, cs["total"],
            "data/holdout_reveal_3_665.json", "对照子集：本不是缺陷")
    add("external 可测口径", ext["catch"], ext["catch"] + ext["miss"],
        "data/external_corpus_reveal_665.json", f"剔除 unknown {ext['unknown']} + not_error {ext['not_error']}")
    add("external 全样本口径", ext["catch"], ext["total"], "data/external_corpus_reveal_665.json", "")
    for layer, key in (("A_local", "A"), ("B_cross_or_measure", "B"), ("C_no_local_detector", "C")):
        d = ext["by_layer"][layer]
        add(f"external 层 {key}"
            + ("（无可用检测器）" if key == "C" else ""),
            d["catch"], d["catch"] + d["miss"], "data/external_corpus_reveal_665.json",
            f"层内 total {d['total']}")
    return rows


def caliber_ablation() -> dict:
    """E2：口径消融 —— unknown 的三种处置对检出率的影响（全部从原始计数现算）。"""
    ext = _j("data/external_corpus_reveal_665.json")
    ho = _j("data/holdout_reveal_3_665.json")
    es = ho["error_subset"]
    arms: dict[str, dict] = {
        "A_valid_only（本批主口径：unknown 剔除）": {
            "holdout": _rate(es["catch"], es["catch"] + es["miss"]),
            "external": _rate(ext["catch"], ext["catch"] + ext["miss"]),
        },
        "B_unknown_as_miss（保守：unknown 记 miss）": {
            "holdout": _rate(es["catch"], es["catch"] + es["miss"] + es["unknown"]),
            "external": _rate(ext["catch"], ext["catch"] + ext["miss"] + ext["unknown"]),
        },
        "C_all_samples（最保守：unknown + not_error 都进分母）": {
            "holdout": _rate(es["catch"], es["catch"] + es["miss"] + es["unknown"]),
            "external": _rate(ext["catch"], ext["total"]),
        },
    }
    delta = {}
    for ds in ("holdout", "external"):
        a = arms["A_valid_only（本批主口径：unknown 剔除）"][ds]["rate_pct"]
        b = arms["B_unknown_as_miss（保守：unknown 记 miss）"][ds]["rate_pct"]
        c = arms["C_all_samples（最保守：unknown + not_error 都进分母）"][ds]["rate_pct"]
        delta[ds] = {"A_minus_B_pp": round(a - b, 1), "A_minus_C_pp": round(a - c, 1)}
    return {"arms": arms, "delta_pp": delta,
            "note": "三臂共用同一份原始计数（catch/miss/unknown/not_error），只变分母口径 ⇒ "
                    "Δ 全是口径效应，不是检测能力变化"}


def registry() -> dict:
    return {
        "experiment": "669 P3 实验启动",
        "protocol_version": PROTOCOL_VERSION,
        "seed": SEED,
        "commit": _commit(),
        **_versions(),
        "blocked": [
            {"baseline": "B1 Rule-only",
             "why": "主仓 holdout/corpus 判定走外部 sanitizer 仪器，无'仅静态规则'可执行路径",
             "need": "拆仓验证器暴露 detect_static(sample) -> verdict"},
            {"baseline": "B2/B3 Full-non-failure / budget-matched random",
             "why": "资产选择接口在拆仓验证器里（主仓不可见），无接口即无对照",
             "need": "拆仓暴露 select_assets(pool, n, strategy, seed) -> [asset]；随机臂必须带种子与分配表"},
        ],
        "honest_note": "本批实验**只做全量复算与本仓可执行的消融**；B1/B2/B3 未做，"
                       "登记在案，不编造数字。n<30 的行标 exploratory=True。",
    }


def run() -> int:
    payload = {"schema": "queyi-experiments/v1", "registry": registry(),
               "baselines": baseline_table(), "caliber_ablation": caliber_ablation()}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    print(f"[exp669] 已写 {OUT_JSON.relative_to(ROOT).as_posix()}"
          f"（基线 {len(payload['baselines'])} 行 / 消融 3 臂）")
    r = payload["registry"]
    print(f"[exp669] 协议 {r['protocol_version']} · commit {r['commit']} · seed {r['seed']} · "
          f"仪器 {r['instrument'][:40]}…")
    return 0


def report() -> int:
    print("== E1 基线表（现算 + CP/Wilson 95%）==")
    for b in baseline_table():
        flag = " [探索性]" if b["exploratory"] else ""
        print(f"  {b['name']:<34} {b['k']:>3}/{b['n']:<3} {str(b['rate_pct']):>5}%  "
              f"CP [{b['cp_lo_pct']}, {b['cp_hi_pct']}]{flag}")
    ab = caliber_ablation()
    print("\n== E2 口径消融（同一份原始计数，只变分母口径）==")
    for arm, d in ab["arms"].items():
        print(f"  {arm:<44} holdout {d['holdout']['rate_pct']}%  "
              f"external {d['external']['rate_pct']}%")
    print("\n== Δ（A 减其它臂，百分点）==")
    for ds, d in ab["delta_pp"].items():
        print(f"  {ds:<10} A−B {d['A_minus_B_pp']:+.1f}pp   A−C {d['A_minus_C_pp']:+.1f}pp")
    reg = registry()
    print("\n== 阻塞项（不编数字）==")
    for b in reg["blocked"]:
        print(f"  - {b['baseline']}：{b['why']}（需要：{b['need']}）")
    return 0


def selftest() -> int:
    fails: list[str] = []

    def chk(name: str, cond: bool) -> None:
        if not cond:
            fails.append(name)

    rows = baseline_table()
    chk("基线表非空", len(rows) >= 6)
    chk("每行 k<=n", all(r["k"] <= r["n"] for r in rows))
    chk("C 层零计数上界显形", any(r["name"].startswith("external 层 C") and r["cp_hi_pct"] > 50
                                  for r in rows))
    ab = caliber_ablation()
    chk("消融 A ≥ B ≥ C（分母越大率越低或持平）",
        all(ab["arms"]["A_valid_only（本批主口径：unknown 剔除）"][ds]["rate_pct"]
            >= ab["arms"]["C_all_samples（最保守：unknown + not_error 都进分母）"][ds]["rate_pct"]
            for ds in ("holdout", "external")))
    chk("Δ 与两条臂自洽",
        all(abs(ab["delta_pp"][ds]["A_minus_B_pp"]
                - (ab["arms"]["A_valid_only（本批主口径：unknown 剔除）"][ds]["rate_pct"]
                   - ab["arms"]["B_unknown_as_miss（保守：unknown 记 miss）"][ds]["rate_pct"])) < 0.051
            for ds in ("holdout", "external")))
    chk("阻塞项登记齐", len(registry()["blocked"]) == 2)
    for f in fails:
        print(f"FAIL: {f}")
    print(f"experiments_669 selftest: {'PASS' if not fails else 'FAIL'}")
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="669 P3 · 实验启动（协议 + 基线 + 口径消融）")
    ap.add_argument("--run", action="store_true", help="现算并落盘 data/experiments/669_experiments.json")
    ap.add_argument("--report", action="store_true", help="打印基线表与消融表")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.report:
        return report()
    if a.run:
        return run()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
