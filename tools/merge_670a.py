#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""merge_670a.py — 670a C 段：669d 扩样**并入** canonical 数据集（幂等 · 现算 · 诚实登记）

## 为什么可以并（原作者授权）

* `data/holdout/holdout_extension_669d.json`.`iron_rule`：
  「合并进 holdout.json **由 669 工程执行**（红线：669d 不碰 holdout.json）」⇒ 本批即执行方。
* `data/external_corpus/external_corpus_669d.json`.`env_dependency`.`declared`：
  「本文件的任何检出率必须**按 expected_detector 分层报告**，禁止合并成一个数」
  ⇒ 并**数据集**可以，但**率必须分层**（本工具产 `data/experiments/corpus_layered_670a.json`）。

## 不能并的（登记，不硬做）

* `data/counterfactual_cases_669d.json`.`honest_note` ⑤ 明写：
  「本扩样与 `counterfactual_cases_665.json` 的 10 条 **不可合并计算**」
  （`denominator.why_it_matters`：「互不重叠、不可合并计算（不同样本集）」）。
  ⇒ 合并会伪造一个**池化 F1**，直接违背 `research/669d_统计口径.md` 的冻结口径。
  本工具**拒绝**合并反事实集，只登记（`--counterfactual-blocked` 打印理由）。

## 幂等

按 `id` 去重追加；重复运行不重复添加（与 665 的 `merged()` 同约定）。

用法：
    python tools/merge_670a.py --merge        # 幂等并入 holdout（→40）与 corpus（→60）+ 分层报告
    python tools/merge_670a.py --check        # 自检（只读）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import counts_659 as counts  # noqa: E402
import stat_bounds as sb  # noqa: E402

VERSION = "1.0"
HOLDOUT = ROOT / "data" / "holdout" / "holdout.json"
HOLDOUT_EXT = ROOT / "data" / "holdout" / "holdout_extension_669d.json"
CORPUS = ROOT / "data" / "external_corpus" / "external_corpus_665.json"
CORPUS_EXT = ROOT / "data" / "external_corpus" / "external_corpus_669d.json"
CORPUS_REVEAL = ROOT / "data" / "external_corpus_reveal_665.json"
CORPUS_LAYERED = ROOT / "data" / "experiments" / "corpus_layered_670a.json"
CF_EXT = ROOT / "data" / "counterfactual_cases_669d.json"

#: 分层口径（669d `env_dependency.hedge` 的五类）
LAYER_OF_DETECTOR = {
    "asan": "sanitizer", "ubsan": "sanitizer", "tsan": "sanitizer",
    "compiler-warn": "compiler-warn", "-Wunsequenced": "compiler-warn",
    "wunsequenced": "compiler-warn",
    "cross-compile": "cross-compile",
    "perf-counter": "perf",
    "compile-time": "compile-time", "standard": "compile-time",
}


def _load(p: Path) -> dict:
    data: dict = json.loads(p.read_text(encoding="utf-8"))   # 666 A1 约定：注解消 no-any-return
    return data


def _dump(p: Path, d: dict) -> None:
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8", newline="\n")


# ── C1 holdout ────────────────────────────────────────────────────────────────
def merge_holdout(apply: bool = True) -> dict:
    base, ext = _load(HOLDOUT), _load(HOLDOUT_EXT)
    have = {s["id"] for s in base["seeds"]}
    added = [s for s in ext["seeds"] if s["id"] not in have]
    seeds = base["seeds"] + added
    out = dict(base)
    out["seeds"] = seeds
    out["count"] = len(seeds)
    out["extend_669d"] = {
        "source": HOLDOUT_EXT.relative_to(ROOT).as_posix(),
        "added": len(added), "added_ids": [s["id"] for s in added],
        "total_after": len(seeds),
        "caliber": ext.get("caliber", {}),
        "honest_note": "669d 扩样并入 canonical holdout（幂等按 id 去重）。"
                       "**检出率另算**：reveal 产物 `data/holdout_reveal_3_665.json` 只覆盖并入前的种子，"
                       "新增种子须重跑 `tools/holdout_reveal_3_665.py` 才能进分母（见 670a 验收报告）。",
    }
    if apply:
        _dump(HOLDOUT, out)
    return {"count": out["count"], "added": len(added), "added_ids": [s["id"] for s in added]}


# ── C2 corpus ─────────────────────────────────────────────────────────────────
def merge_corpus(apply: bool = True) -> dict:
    base, ext = _load(CORPUS), _load(CORPUS_EXT)
    have = {s["id"] for s in base["samples"]}
    added = [s for s in ext["samples"] if s["id"] not in have]
    samples = base["samples"] + added
    out = dict(base)
    out["samples"] = samples
    out["count"] = len(samples)
    out["extend_669d"] = {
        "source": CORPUS_EXT.relative_to(ROOT).as_posix(),
        "added": len(added), "added_ids": [s["id"] for s in added],
        "total_after": len(samples),
        "env_dependency": ext.get("env_dependency", {}),
        "honest_note": "669d 扩样并入 canonical corpus（幂等按 id 去重）。"
                       "**率一律分层报告**（669d `env_dependency.declared`），禁止合并成一个数；"
                       "分层检出率见 `data/experiments/corpus_layered_670a.json`。"
                       "新增 20 条尚未 reveal ⇒ 层内标 `pending_reveal`，不进分母。",
    }
    if apply:
        _dump(CORPUS, out)
    return {"count": out["count"], "added": len(added), "added_ids": [s["id"] for s in added]}


def layered_report(apply: bool = True) -> dict:
    """按 expected_detector 分层报告检出率（**现算**：逐样本 verdict）。

    已 reveal 的样本取其 reveal 判决；669d 新增样本标 `pending_reveal`（不进分母）。
    """
    corpus = _load(CORPUS)
    reveal = _load(CORPUS_REVEAL)
    verdict = {r["id"]: r["verdict"] for r in reveal["results"]}
    layers: dict[str, dict] = {}
    for s in corpus["samples"]:
        det = str(s.get("expected_detector") or "unknown")
        layer = LAYER_OF_DETECTOR.get(det, "other")
        bucket = layers.setdefault(layer, {"n": 0, "catch": 0, "miss": 0, "unknown": 0,
                                           "not_error": 0, "pending_reveal": 0,
                                           "detectors": {}})
        bucket["n"] += 1
        bucket["detectors"][det] = bucket["detectors"].get(det, 0) + 1
        v = verdict.get(s["id"])
        if v is None:
            bucket["pending_reveal"] += 1
        elif v in bucket:
            bucket[v] += 1
        else:                                            # not_error / measure 等
            bucket["not_error"] += 1
    for layer, b in layers.items():
        k, n = b["catch"], b["catch"] + b["miss"]
        b["measurable"] = n
        if n:
            b.update(sb.proportion(k, n))
        else:
            b.update({"point": None, "cp_low": None, "cp_high": None,
                      "note": "层内无可测样本 ⇒ 拒绝给率（fail-loud）"})
    doc = {
        "schema": "queyi-corpus-layered/670a",
        "generated_by": "tools/merge_670a.py --merge",
        "corpus": CORPUS.relative_to(ROOT).as_posix(),
        "corpus_count": corpus["count"],
        "reveal_covered": len(reveal["results"]),
        "pending_reveal": corpus["count"] - len(reveal["results"]),
        "layers": layers,
        "honest_note": "分层率由**逐样本 verdict 现算**；`pending_reveal` 的样本不进任何分母。"
                       "⚠ 禁止把各层相加成一个总数（669d env_dependency.declared）。"
                       "已 reveal 部分 = `external_corpus_reveal_665.json` 的样本，"
                       "其层名映射来自本工具 LAYER_OF_DETECTOR（与 662 的 A/B/C 分层不同口径，"
                       "此处按 669d 要求的 expected_detector 五类分层）。",
    }
    if apply:
        CORPUS_LAYERED.parent.mkdir(parents=True, exist_ok=True)
        _dump(CORPUS_LAYERED, doc)
    return doc


# ── C3 反事实：拒绝池化 ───────────────────────────────────────────────────────
def counterfactual_blocked() -> dict:
    ext = _load(CF_EXT)
    return {
        "merged": False,
        "reason": "669d 原作者明写不可合并计算",
        "evidence": {
            "file": CF_EXT.relative_to(ROOT).as_posix(),
            "honest_note_5": ext["honest_note"].split("⑤")[-1].strip(),
            "denominator_why": ext["denominator"]["why_it_matters"],
        },
        "consequence_if_merged": "会得到一个**池化 F1**（20+10=30 条不同样本集混算），"
                                 "与 `research/669d_统计口径.md` 的冻结口径冲突 ⇒ 本批拒绝执行。",
        "instead": "两个样本集**各自**报 P/R/F1（665: 10 条；669d: 20 条），"
                   "并在论文/报告中并列，不做池化。",
    }


# ── 自检 ──────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    hs, ext = _load(HOLDOUT), _load(HOLDOUT_EXT)
    ids = [s["id"] for s in hs["seeds"]]
    chk("holdout seeds 唯一（幂等前提）", len(ids) == len(set(ids)))
    chk("holdout count == len(seeds)", hs["count"] == len(hs["seeds"]))
    chk("669d holdout 扩样已并入", set(s["id"] for s in ext["seeds"]) <= set(ids))
    cs = _load(CORPUS)
    cids = [s["id"] for s in cs["samples"]]
    chk("corpus samples 唯一", len(cids) == len(set(cids)))
    chk("corpus count == len(samples)", cs["count"] == len(cs["samples"]))
    chk("669d corpus 扩样已并入", set(s["id"] for s in _load(CORPUS_EXT)["samples"]) <= set(cids))
    lay = layered_report(apply=False)
    tot = sum(b["n"] for b in lay["layers"].values())
    chk("分层覆盖全部样本", tot == cs["count"], f"({tot} vs {cs['count']})")
    chk("分层无 pooled 率字段", "pooled_rate" not in json.dumps(lay))
    chk("反事实已登记拒绝池化", counterfactual_blocked()["merged"] is False)
    chk("counts 权威源可用", counts.CARDS_REAL > 0)
    print(f"670a merge selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="670a C 段：669d 扩样并入（幂等）")
    ap.add_argument("--merge", action="store_true", help="执行并入 + 写分层报告")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--counterfactual-blocked", action="store_true", help="打印反事实拒绝池化的理由")
    a = ap.parse_args(argv)
    if a.counterfactual_blocked:
        print(json.dumps(counterfactual_blocked(), ensure_ascii=False, indent=2))
        return 0
    if a.check:
        return selftest()
    if a.merge:
        h = merge_holdout(True)
        c = merge_corpus(True)
        lay = layered_report(True)
        print(f"[670a] holdout {h['count']}（+{h['added']}）· corpus {c['count']}（+{c['added']}）· "
              f"分层报告 → {CORPUS_LAYERED.relative_to(ROOT).as_posix()}"
              f"（层 {sorted(lay['layers'])}，pending_reveal {lay['pending_reveal']}）")
        return 0
    return selftest()


if __name__ == "__main__":
    raise SystemExit(main())
