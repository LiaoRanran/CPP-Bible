#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""baseline_672g.py — 672g B/C：**真 B3** 三臂 baseline（现算 · 只读 · 诚实登记）。

背景
====
672f 的 baseline 三臂里，随机臂是 **Random†（仪器级代理）**：从主仓**仪器池**随机抽
与 FD 同数量的仪器。它是**代理**，不是论文 §5.2 的 B3（`docs/670a_实验结果.md` §3）。

本批（672g）把随机臂升级为**真 B3**：随机挑选**验证资产**这件事，改由**拆仓验证器
`queyi-verifier`** 通过 `select_assets(pool, n, strategy, seed)` 完成。主仓**只调用接口**，
不依赖拆仓内部实现（走 subprocess；池由拆仓声明并返回）。

三条臂（**同一批样本配对**，只变"用不用运行时证据 / 用多少资产 / 怎么挑资产"）
==========================================================================
* **FD（failure-driven / 现状）**：照实读逐样本判决（sanitizer + 本机编译器全用）。
* **Static（rule-only，口径重分箱）**：只认编译期/静态资产；sanitizer 样本记 miss。
* **Random（真 B3）**：调用拆仓 `select_assets`，从**验证资产池**按固定种子随机抽
  与 FD **同数量**的资产；只有 `detector ∈ 选中集合` 且 FD 也 catch 的样本才算 catch。

口径与统计（沿用 672f）
======================
* 分母：holdout 21、corpus 48（671a 扩样后，可测口径）；区间 = Clopper–Pearson 95%。
* 配对精确 McNemar + Cohen's h + Δ 的 95% CI（Newcombe / Wald-on-difference）。
* seed=20260930；random 臂**连跑 2 次哈希一致**。

用法
====
    python tools/baseline_672g.py                 # 只打印摘要
    python tools/baseline_672g.py --run            # 落盘 baseline_random.json + b3_real_672g.json
    python tools/baseline_672g.py --check          # 自检（只读）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import ablation_stats_671b as AS  # noqa: E402
import baseline_670a as B  # noqa: E402  复用 FD/Static 臂定义与口径

VERSION = "1.0"
SEED = 20260930
OUT_DIR = ROOT / "data" / "experiments"

#: 拆仓验证器仓路径（可用环境变量 QUEYI_VERIFIER 覆盖，便于 CI/换机）
QUEYI_VERIFIER = Path(os.environ.get("QUEYI_VERIFIER", r"C:/CodeLearnling/queyi-verifier"))
SELECTOR = QUEYI_VERIFIER / "tools" / "select_assets_672g.py"


# ── 拆仓接口调用（subprocess；不 import 拆仓内部实现）─────────────────────────
def _call_selector(args: list[str]) -> dict:
    """调用拆仓 select_assets 接口，返回其 JSON 输出（fail-loud）。"""
    if not SELECTOR.is_file():
        raise FileNotFoundError(
            f"拆仓选择器不存在：{SELECTOR}（设 QUEYI_VERIFIER 指向 queyi-verifier 仓）")
    proc = subprocess.run([sys.executable, str(SELECTOR), *args, "--json"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"拆仓 select_assets 调用失败（rc={proc.returncode}）：{proc.stderr.strip()}")
    out: dict[str, Any] = json.loads(proc.stdout)      # 673b A1：显式收窄（json.loads ⇒ Any）
    return out


def verifier_pool() -> list[str]:
    """取拆仓声明的验证资产池（本仓不硬编码池定义 ⇒ 池产权在拆仓）。"""
    return list(_call_selector(["--print-pool"])["pool"])


def verifier_select(n: int, seed: int = SEED) -> dict:
    """取拆仓的真随机验证资产选择（含分配表）。"""
    return _call_selector(["--n", str(n), "--strategy", "random", "--seed", str(seed)])


# ── 真 B3 随机臂 ──────────────────────────────────────────────────────────────
def fd_used_assets(samples: list[dict], fd: dict[str, str], pool: list[str]) -> list[str]:
    """FD 在 catch 样本上实际用到的**池内**资产（= 预算锚）。"""
    used = {s["detector"] for s in samples
            if fd.get(s["id"]) == "catch" and s["detector"] in set(pool)}
    return sorted(used)


def arm_random_real(samples: list[dict], fd: dict[str, str], picked: list[str]) -> dict[str, str]:
    """真 B3 随机臂：只有 detector ∈ picked 且 FD 也 catch 的样本才 catch。"""
    ps = set(picked)
    out: dict[str, str] = {}
    for s in samples:
        v = s["verdict"]
        if v == "unknown":
            out[s["id"]] = "unknown"
        elif v == "not_error":
            out[s["id"]] = "not_error"
        elif s["detector"] in ps and fd.get(s["id"]) == "catch":
            out[s["id"]] = "catch"
        else:
            out[s["id"]] = "miss"
    return out


# ── 单次跑批 ──────────────────────────────────────────────────────────────────
def run_once() -> dict:
    pool = verifier_pool()
    hs = B.load_holdout_samples()
    cs = B.load_corpus_samples()
    out: dict = {"schema": "queyi-baseline-experiment/672g", "version": VERSION,
                 "seed": SEED, "asset_pool": pool,
                 "pool_owner": "queyi-verifier::tools/select_assets_672g.py::ASSET_POOL",
                 "random_arm": "真 B3（拆仓 select_assets 验证资产口径，非仪器级代理）"}
    for name, samples in (("holdout", hs), ("corpus", cs)):
        fd = B._fd(samples)
        st = B._static(samples)
        used = fd_used_assets(samples, fd, pool)
        sel = verifier_select(len(used))
        picked = list(sel["picked"])
        rn = arm_random_real(samples, fd, picked)
        out[name] = {
            "n_samples": len(samples),
            "fd": B.caliber(fd), "static": B.caliber(st), "random": B.caliber(rn),
            "random_selection": {
                "pool": pool, "fd_used": used, "picked": picked, "seed": SEED,
                "shared_by_fd_and_random": sorted(set(used) & set(picked)),
                "allocation_table": sel.get("allocation_table", []),
            },
            "fd_vs_static": _paired(fd, st, len(samples)),
            "fd_vs_random": _paired(fd, rn, len(samples)),
        }
    return out


def _paired(a: dict[str, str], b: dict[str, str], n_total: int) -> dict:
    """配对统计（a=FD，b=对照臂）：McNemar + Cohen's h + Δ 的两种 CI。"""
    ids = [i for i in a if a[i] in ("catch", "miss") and b[i] in ("catch", "miss")]
    ka = sum(1 for i in ids if a[i] == "catch")
    kb = sum(1 for i in ids if b[i] == "catch")
    n = len(ids)
    bb = sum(1 for i in ids if a[i] == "catch" and b[i] != "catch")
    cc = sum(1 for i in ids if a[i] != "catch" and b[i] == "catch")
    mc = AS.mcnemar_exact(bb, cc)
    ci = AS.delta_ci_paired(bb, cc, n)
    h = AS.cohens_h(ka / n, kb / n) if n else {"h": None, "magnitude": None}
    return {"n_pairs": n, "fd_catch": ka, "other_catch": kb,
            "discordant_fd_catch": bb, "discordant_other_catch": cc,
            "delta_pp": round((ka - kb) / n * 100, 4) if n else None,
            "ci_paired_wald_pp": [round(ci["ci_low"] * 100, 4), round(ci["ci_high"] * 100, 4)],
            "ci_crosses_zero": ci["crosses_zero"],
            "mcnemar_p": mc["p_value"], "cohens_h": round(h["h"], 4) if h["h"] is not None else None,
            "cohens_h_magnitude": h["magnitude"]}


# ── 复现性（连跑 2 次哈希一致）─────────────────────────────────────────────────
def _canon(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False, sort_keys=True)


def reproducibility() -> dict:
    r1 = run_once()
    r2 = run_once()
    h1 = hashlib.sha256(_canon(r1).encode("utf-8")).hexdigest()
    h2 = hashlib.sha256(_canon(r2).encode("utf-8")).hexdigest()
    picks1 = {k: r1[k]["random_selection"]["picked"] for k in ("holdout", "corpus")}
    picks2 = {k: r2[k]["random_selection"]["picked"] for k in ("holdout", "corpus")}
    return {"run1_sha256": h1, "run2_sha256": h2, "identical": h1 == h2,
            "picks_identical": picks1 == picks2, "picks": picks1}


# ── 摘要 ──────────────────────────────────────────────────────────────────────
def summary(r: dict) -> str:
    L = ["=== 672g 真 B3 三臂 × 可测口径（现算）===",
         f"seed={r['seed']}  池={r['asset_pool']}（{len(r['asset_pool'])} 项，拆仓声明）", ""]
    for name in ("holdout", "corpus"):
        blk = r[name]
        L.append(f"[{name}] 样本 {blk['n_samples']}")
        for arm in ("fd", "static", "random"):
            mm = blk[arm]["measurable"]
            L.append(f"  {arm:7s} {mm['k']}/{mm['n']} = {mm['point'] * 100:5.1f}%  "
                     f"CP95[{mm['cp_low'] * 100:.1f},{mm['cp_high'] * 100:.1f}]")
        sel = blk["random_selection"]
        L.append(f"    random 选中 {sel['picked']}  (FD 用了 {sel['fd_used']})")
        for cmp_ in ("fd_vs_static", "fd_vs_random"):
            p = blk[cmp_]
            L.append(f"    {cmp_}: Δ={p['delta_pp']:+.1f}pp "
                     f"CI[{p['ci_paired_wald_pp'][0]:.1f},{p['ci_paired_wald_pp'][1]:.1f}] "
                     f"p={p['mcnemar_p']:.2e} h={p['cohens_h']:.2f}")
        L.append("")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    pool = verifier_pool()
    chk("拆仓池可取得且大小 = 8", len(pool) == 8, f"({len(pool)})")
    chk("池不含测量仪器（measure/perf-counter）",
        "measure" not in pool and "perf-counter" not in pool)
    r = run_once()
    for name in ("holdout", "corpus"):
        blk = r[name]
        for arm in ("fd", "static", "random"):
            c = blk[arm]
            chk(f"{name}.{arm} 判决划分自洽",
                c["catch"] + c["miss"] + c["unknown"] + c["not_error"] == c["total"])
        chk(f"{name} 预算对齐（picked == fd_used 数量）",
            len(blk["random_selection"]["picked"]) == len(blk["random_selection"]["fd_used"]))
        chk(f"{name} picked ⊆ pool",
            set(blk["random_selection"]["picked"]) <= set(pool))
        chk(f"{name} random ≤ fd（子集不可能抓更多）",
            blk["random"]["catch"] <= blk["fd"]["catch"])
    rep = reproducibility()
    chk("连跑 2 次哈希一致", rep["identical"] is True,
        f"({rep['run1_sha256'][:12]} vs {rep['run2_sha256'][:12]})")
    print(f"baseline_672g selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672g B/C：真 B3 三臂 baseline（现算·只读）")
    ap.add_argument("--run", action="store_true", help="落盘 baseline_random.json + b3_real_672g.json")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()

    r = run_once()
    print(summary(r))
    if a.run:
        rep = reproducibility()
        r["reproducibility"] = rep
        r["honest_note"] = (
            "真 B3：随机臂由拆仓验证器 queyi-verifier 的 select_assets 选出（池=验证资产，"
            "非测量仪器）。样本量 n=21/48 ⇒ 只读方向 + CI，幅度不写成确认性点估计。")
        # 1) 真 B3 全量明细
        (OUT_DIR / "b3_real_672g.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        # 2) baseline_random.json 升级为真 B3（保持 672f 的 schema：holdout/corpus.measurable）
        random_doc = {
            "schema": "queyi-baseline-experiment/670a",
            "arm": "random（真 B3 · 拆仓 select_assets 验证资产口径；672g 替换 670a 的 Random† 代理）",
            "seed": SEED,
            "pool_owner": r["pool_owner"],
            "selection": {k: r[k]["random_selection"] for k in ("holdout", "corpus")},
            "holdout": r["holdout"]["random"], "corpus": r["corpus"]["random"],
            "blocked": [{"baseline": "B3 budget-matched random（验证资产口径，论文 §5.2）",
                         "status": "RESOLVED（672g：拆仓 queyi-verifier 已暴露 select_assets）"}],
            "honest_note": r["honest_note"],
        }
        (OUT_DIR / "baseline_random.json").write_text(
            json.dumps(random_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print("[672g] 已写 b3_real_672g.json + baseline_random.json（真 B3）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
