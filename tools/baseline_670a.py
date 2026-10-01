#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""baseline_670a.py — 670a B 段：baseline 实验（**现算** · 只读 · 诚实登记）

## 做了什么（可执行的三臂）

被测检测集（全部读**逐样本明细**，不抄汇总数字）：

| 检测集 | 事实源 | 逐样本口径 |
|---|---|---|
| holdout | `data/holdout/reveal_3_detail_671a.json`（671a 扩样后） | `planted is True` 且 `planted_desc` 非空 = 真错 |
| external corpus | `data/external_corpus/reveal_detail_671a.json`.`per_sample[]`（671a 扩样后） | `verdict ∈ {catch,miss}` = 可测 |
| 真实缺陷重注入 | `data/defect_fixtures/defects.json`（经 658 的最小重注入） | `caught` |

三条臂（**同一批样本配对**，只变"用不用运行时证据 / 用多少资产"）：

* **FD（failure-driven / 现状）**：照实读逐样本判决（sanitizer + 本机编译器全用）。
* **Static（rule-only，**不获取运行时证据**）**：按 670d 设计 §1「B1 静态门禁」的定义 ——
  只认**编译期/静态**仪器（`compiler-warn` / `wunsequenced` / `cross-compile` / `linker`），
  **sanitizer（asan/ubsan/tsan）属运行时证据 ⇒ 该样本记 miss**（无运行时证据可用）。
  ⚠️ 这是对既有 reveal 产物的**口径重分箱**（不是重跑）；其有效性依赖"sanitizer = 运行时证据"这一前提。
* **Random†（budget-matched · 仪器级代理）**：`†` = **代理臂，不是论文 §5.2 的 B3**。
  真 B3 需要拆仓验证器暴露 `select_assets(pool, n, strategy, seed)`（主仓不可见）。
  此处把"资产"退化为**检测仪器**：从仪器池按 seed 随机选与 FD **同数量**的仪器，
  只有 detector ∈ 选中集合的样本才算 catch。**结论不得写进论文**（见 `blocked`）。

## 没做的（登记，不编数字）

* 真 B3（budget-matched **验证资产**随机）：`blocked` —— 需要拆仓 `select_assets()`。
* 变异 core 的 baseline 臂：变异 kill 是**内部指标**（`data/656_mutation_report_core.json`），
  不是缺陷检出率，无"检测集"可配对 ⇒ `not_applicable`。

## 口径消融（三口径）

对 holdout / corpus 分别报：全样本口径（catch/total）、可测口径（catch/(catch+miss)）、
排除 unknown 口径 —— 三口径共用同一份原始计数，只变分母。

区间：Clopper–Pearson 95%（`tools/stat_bounds.py`，单一来源）。

用法：
    python tools/baseline_670a.py --run        # 现算并落盘 data/experiments/baseline_*.json
    python tools/baseline_670a.py              # 只打印摘要
    python tools/baseline_670a.py --check       # 自检（只读，exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import stat_bounds as sb  # noqa: E402

VERSION = "1.2"                                  # 672h：切到 672h 扩样分母（holdout 41 / corpus 64）
SEED = 20260930                                  # 670d 设计 §3.1 指定的随机种子
random.seed(SEED)                                # 672f：模块级固定种子（G-SEED-FIXED，两跑必一致）
HOLDOUT_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"      # 672h 第 5 轮
CORPUS_REVEAL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"  # 672h 第 4 轮
OUT_DIR = ROOT / "data" / "experiments"

#: **静态/编译期**仪器（不产生运行时证据）
STATIC_INSTRUMENTS = frozenset({"compiler-warn", "wunsequenced", "cross-compile", "linker"})
#: **运行时**仪器（sanitizer：编译并运行才报）
RUNTIME_INSTRUMENTS = frozenset({"asan", "ubsan", "tsan"})
#: 检测仪器全集（含测量类；random 代理的抽取池）
INSTRUMENT_POOL = tuple(sorted(STATIC_INSTRUMENTS | RUNTIME_INSTRUMENTS
                               | {"measure", "perf-counter", "compile-time"}))


# ── 检测集装载（逐样本）────────────────────────────────────────────────────────
def load_holdout_samples() -> list[dict]:
    """holdout 真错样本（`planted is True`）+ 逐样本 detector/verdict（现算口径）。

    `verdict == "unknown"`（检测器不可用）单独计，不进可测分母。
    """
    d = json.loads(HOLDOUT_DETAIL.read_text(encoding="utf-8"))
    out: list[dict] = []
    for s in d["per_sample"]:
        if s.get("planted") is not True:
            continue
        out.append({"id": s["id"], "detector": str(s.get("detector") or "unknown"),
                    "verdict": str(s.get("verdict")), "set": "holdout"})
    return out


def load_corpus_samples() -> list[dict]:
    """external corpus 逐样本（671a 明细 `per_sample[]` 现读；含 not_error 对照）。"""
    d = json.loads(CORPUS_REVEAL.read_text(encoding="utf-8"))
    return [{"id": r["id"], "detector": str(r.get("detector") or "unknown"),
             "verdict": str(r.get("verdict")), "layer": str(r.get("layer") or "?"),
             "set": "corpus"} for r in d["per_sample"]]


# ── 三臂 ──────────────────────────────────────────────────────────────────────
def _fd(samples: list[dict]) -> dict[str, str]:
    """FD 臂：照实读（unknown 保持 unknown）。"""
    return {s["id"]: s["verdict"] for s in samples}


def _static(samples: list[dict]) -> dict[str, str]:
    """Static 臂（rule-only）：只认编译期仪器；运行时仪器样本记 miss；unknown 保持 unknown。"""
    out: dict[str, str] = {}
    for s in samples:
        v = s["verdict"]
        if v == "unknown":
            out[s["id"]] = "unknown"
        elif v == "not_error":
            out[s["id"]] = "not_error"
        elif s["detector"] in STATIC_INSTRUMENTS:
            out[s["id"]] = v
        else:
            out[s["id"]] = "miss"        # 无运行时证据 ⇒ 该真错看不到
    return out


def _instrument_budget(samples: list[dict], fd: dict[str, str]) -> list[str]:
    """FD 在**被判 catch 的样本**上用到的仪器集合（= 失败驱动"选出来的资产"）。"""
    used = {s["detector"] for s in samples
            if fd.get(s["id"]) == "catch" and s["detector"] in INSTRUMENT_POOL}
    return sorted(used)


def _random_proxy(samples: list[dict], fd: dict[str, str], seed: int = SEED) -> tuple[dict[str, str], dict]:
    """Random† 代理臂：从仪器池按 seed 随机抽与 FD **同数量**的仪器。

    只有 `detector ∈ 选中集合` 的样本才可能 catch（且 FD 必须也 catch）。
    ⚠️ 代理口径：资产=仪器，**不是**验证资产；真 B3 见 `blocked`。
    """
    used = _instrument_budget(samples, fd)
    rng = random.Random(seed)
    picked = sorted(rng.sample(list(INSTRUMENT_POOL), len(used))) if used else []
    out: dict[str, str] = {}
    for s in samples:
        v = s["verdict"]
        if v == "unknown":
            out[s["id"]] = "unknown"
        elif v == "not_error":
            out[s["id"]] = "not_error"
        elif s["detector"] in picked and fd.get(s["id"]) == "catch":
            out[s["id"]] = "catch"
        else:
            out[s["id"]] = "miss"
    return out, {"pool": list(INSTRUMENT_POOL), "fd_used": used, "picked": picked,
                 "seed": seed, "shared_by_fd_and_random": sorted(set(used) & set(picked))}


# ── 口径（三口径消融）────────────────────────────────────────────────────────
def caliber(verdicts: dict[str, str]) -> dict:
    """三口径 ── 共用同一份原始计数，只变分母。

    * all_samples：catch / 全部样本
    * measurable ：catch / (catch + miss)          ← 主口径
    * no_unknown ：catch / (catch + miss + not_error)（把对照也进分母，`not_error` 记 miss）
    """
    c = sum(1 for v in verdicts.values() if v == "catch")
    m = sum(1 for v in verdicts.values() if v == "miss")
    u = sum(1 for v in verdicts.values() if v == "unknown")
    ne = sum(1 for v in verdicts.values() if v == "not_error")
    total = len(verdicts)
    return {
        "catch": c, "miss": m, "unknown": u, "not_error": ne, "total": total,
        "all_samples": _prop(c, total),
        "measurable": _prop(c, c + m),
        "no_unknown": _prop(c, c + m + ne),
        "delta_pp": {
            "measurable_minus_all": _pp(c, c + m) - _pp(c, total),
            "measurable_minus_no_unknown": _pp(c, c + m) - _pp(c, c + m + ne),
        },
    }


def _prop(k: int, n: int) -> dict:
    """比例 + Clopper–Pearson 95%（`n == 0` ⇒ 不可判，**不臆造率**，与 stat_bounds 的 fail-loud 一致）。"""
    if n <= 0:
        return {"k": k, "n": n, "point": None, "cp_low": None, "cp_high": None,
                "note": "n=0 ⇒ 无可测样本，拒绝给率（fail-loud）"}
    return {"k": k, "n": n, **sb.proportion(k, n)}


def _pp(k: int, n: int) -> float:
    return round(k / n * 100, 1) if n else 0.0


# ── 真实缺陷重注入（静态门禁的另一条真路径）────────────────────────────────────
def defect_reinjection() -> dict:
    """真实缺陷重注入检出（661 B2 的 6 个重注入器；逐条**现跑**，不抄汇总）。

    静态门禁口径：这些重注入器都是**静态判定**（哈希/SPDX/对比度/序列化/锚/围栏），
    不编译不运行 ⇒ 它们本身就是"静态臂"，故 FD 与 Static 在本行**同值**（Δ=0，如实登记）。
    """
    import defect_injection_661 as di  # noqa: E402
    defects = json.loads((ROOT / "data" / "defect_fixtures" / "defects.json")
                         .read_text(encoding="utf-8"))["defects"]
    rows = []
    caught = 0
    for d in defects:
        fn = di.REINJECTORS.get(d["id"])
        if not fn:
            continue
        r = fn()
        caught += bool(r["caught"])
        rows.append({"id": d["id"], "caught": bool(r["caught"]), "gate": r["gate"]})
    n = len(rows)
    covered = sum(1 for d in defects if str(d.get("gate_caught", "")).startswith("yes"))
    return {"k": caught, "n": n, **_prop(caught, n),
            "rows": rows, "reinjectable": n, "defects_total": len(defects),
            "covered_by_gate_declared": covered,
            "arms_note": "FD == Static（重注入器本身即静态判定）⇒ Δ=0；"
                         "random 臂 N/A（资产=规则，主仓无 select_assets 接口）。",
            "note": "静态门禁在**可机械重注入子集**上的检出；不可重注入的缺陷缺原错误版本，"
                    "只能登记历史 gate_caught 覆盖（软指标）。"}


# ── 汇总 ─────────────────────────────────────────────────────────────────────
def run() -> dict:
    hs = load_holdout_samples()
    cs = load_corpus_samples()
    fd_h, fd_c = _fd(hs), _fd(cs)
    st_h, st_c = _static(hs), _static(cs)
    rn_h, rn_h_meta = _random_proxy(hs, fd_h)
    rn_c, rn_c_meta = _random_proxy(cs, fd_c)
    return {
        "schema": "queyi-baseline-experiment/670a",
        "version": VERSION,
        "seed": SEED,
        "holdout": {
            "n_samples": len(hs),
            "fd": caliber(fd_h), "static": caliber(st_h), "random_proxy": caliber(rn_h),
            "random_proxy_selection": rn_h_meta,
        },
        "corpus": {
            "n_samples": len(cs),
            "fd": caliber(fd_c), "static": caliber(st_c), "random_proxy": caliber(rn_c),
            "random_proxy_selection": rn_c_meta,
            "by_layer": _corpus_layers(cs, fd_c, st_c),
        },
        "defect_reinjection": defect_reinjection(),
        "mutation_core": {"status": "not_applicable",
                          "why": "变异 kill 是**内部指标**（data/656_mutation_report_core.json），"
                                 "不是缺陷检出率 ⇒ 没有「检测集」可与 baseline 臂配对",
                          "raw_source": "data/656_mutation_report_core.json"},
        "blocked": [
            {"baseline": "B3 budget-matched random（**验证资产**口径，论文 §5.2）",
             "why": "资产选择接口在拆仓验证器 queyi-verifier 里（主仓不可见）；"
                    "主仓无 select_assets(pool, n, strategy, seed)",
             "status": "BLOCKED",
             "need": "queyi-verifier 暴露 select_assets(pool, n, strategy, seed) -> [asset] + 分配表"},
            {"baseline": "B1 rule-only（真·静态规则判定器）",
             "why": "主仓 holdout/corpus 判定走外部 sanitizer 仪器，无 detect_static(sample) 可执行路径",
             "status": "PROXY（本文件 static 臂 = 口径重分箱，不是重跑）",
             "need": "queyi-verifier 暴露 detect_static(sample) -> verdict"},
        ],
        "honest_note": "FD 与 Static 是**同一批样本**的口径重分箱（配对可比）；"
                       "random_proxy 是仪器级代理，**不是**论文 B3，结论不得进论文。"
                       "所有率由逐样本现算，区间用 tools/stat_bounds.py 的 Clopper–Pearson 95%。",
    }


def _corpus_layers(cs: list[dict], fd: dict, st: dict) -> dict:
    out: dict[str, dict] = {}
    for layer in sorted({s.get("layer", "?") for s in cs}):
        ids = [s["id"] for s in cs if s.get("layer") == layer]
        out[layer] = {"n": len(ids),
                      "fd": caliber({i: fd[i] for i in ids}),
                      "static": caliber({i: st[i] for i in ids})}
    return out


def summary(r: dict) -> str:
    L = ["=== 670a baseline 三臂 × 三口径（现算）===",
         f"seed={r['seed']}  （random 臂为**仪器级代理**，非论文 B3）", ""]
    for name in ("holdout", "corpus"):
        blk = r[name]
        L.append(f"[{name}] 样本 {blk['n_samples']}")
        for arm in ("fd", "static", "random_proxy"):
            c = blk[arm]
            mm = c["measurable"]
            L.append(f"  {arm:13s} measurable {mm['k']}/{mm['n']} = {mm['point'] * 100:5.1f}%  "
                     f"CP95[{mm['cp_low'] * 100:.1f},{mm['cp_high'] * 100:.1f}]  "
                     f"| all {c['all_samples']['k']}/{c['all_samples']['n']}")
        L.append("")
    d = r["defect_reinjection"]
    L.append(f"[defect 重注入] FD/Static（同一静态门禁）= {d['k']}/{d['n']} = {d['point'] * 100:.1f}%  "
             f"（不可重注入 {d['defects_total'] - d['reinjectable']} 条只登记覆盖）")
    L.append("[mutation core] not_applicable（内部指标，无检测集可配对）")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run()
    h = r["holdout"]
    chk("holdout 真错样本数 > 0", h["n_samples"] > 0, f"({h['n_samples']})")
    for arm in ("fd", "static", "random_proxy"):
        c = h[arm]
        chk(f"holdout.{arm} 判决划分自洽",
            c["catch"] + c["miss"] + c["unknown"] + c["not_error"] == c["total"])
    chk("static ≤ fd（去掉运行时证据不可能抓更多）",
        h["static"]["catch"] <= h["fd"]["catch"],
        f"({h['static']['catch']} <= {h['fd']['catch']})")
    chk("random_proxy ≤ fd", h["random_proxy"]["catch"] <= h["fd"]["catch"])
    chk("random 臂与 FD 同资产预算",
        len(h["random_proxy_selection"]["picked"])
        == len(h["random_proxy_selection"]["fd_used"]))
    chk("random 臂可复现（同 seed 两跑一致）",
        _random_proxy(load_holdout_samples(), _fd(load_holdout_samples()))[1]["picked"]
        == h["random_proxy_selection"]["picked"])
    c = r["corpus"]
    chk("corpus 样本数 == 60（671a 扩样后，现读 reveal 逐样本）", c["n_samples"] == 60, f"({c['n_samples']})")
    chk("defect 重注入全部命中（静态夹具）",
        r["defect_reinjection"]["k"] == r["defect_reinjection"]["n"])
    chk("blocked 恰 2 条（真 B3 + 真 detect_static）", len(r["blocked"]) == 2)
    print(f"670a baseline selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="670a B 段 baseline 实验（现算·只读）")
    ap.add_argument("--run", action="store_true", help="现算并落盘 data/experiments/baseline_*.json")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    r = run()
    print(summary(r))
    if a.run:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        static_doc = {"schema": r["schema"], "arm": "static（rule-only / 无运行时证据）",
                      "caliber_definition": "只认编译期仪器；sanitizer 样本记 miss；unknown 不计入可测分母",
                      "holdout": r["holdout"]["static"], "corpus": r["corpus"]["static"],
                      "corpus_by_layer": {k: v["static"] for k, v in r["corpus"]["by_layer"].items()},
                      "defect_reinjection": r["defect_reinjection"],
                      "blocked": r["blocked"], "honest_note": r["honest_note"]}
        random_doc = {"schema": r["schema"], "arm": "random_proxy†（仪器级预算对齐；**非论文 B3**）",
                      "seed": SEED,
                      "selection": {"holdout": r["holdout"]["random_proxy_selection"],
                                    "corpus": r["corpus"]["random_proxy_selection"]},
                      "holdout": r["holdout"]["random_proxy"], "corpus": r["corpus"]["random_proxy"],
                      "blocked": r["blocked"], "honest_note": r["honest_note"]}
        fdoc = {"schema": r["schema"], "arm": "failure-driven（现状）",
                "holdout": r["holdout"]["fd"], "corpus": r["corpus"]["fd"],
                "corpus_by_layer": {k: v["fd"] for k, v in r["corpus"]["by_layer"].items()},
                "mutation_core": r["mutation_core"], "honest_note": r["honest_note"]}
        for name, doc in (("baseline_static.json", static_doc),
                          ("baseline_random.json", random_doc),
                          ("baseline_fd.json", fdoc)):
            (OUT_DIR / name).write_text(
                json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                encoding="utf-8", newline="\n")
            print(f"[670a] 已写 {(OUT_DIR / name).relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
