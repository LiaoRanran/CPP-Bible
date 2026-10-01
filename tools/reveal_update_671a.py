#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""reveal_update_671a.py — 671a C3：扩样 reveal 之后的**检出率更新**（只算、不改论文）。

职责边界（重要）
================
本工具**只**把新 reveal 的落盘结论算成"论文/前端可以引用的新数字"，写进
`data/experiments/reveal_update_671a.json`。它**不碰** `research/paper_v0.8.md`、
`research/latex/`、`web/data/*.json` —— 论文与前端的数字更新由 **671b** 负责。
所以本文件里有一节 `pending_for_671b`：逐条列出"哪个数变了、从哪变成哪、
哪几个文件/表格要跟着改"，让接手的人不必重新推导。

为什么必须算 CI 而不是只报一个点估计
====================================
分母从 16 抬到 21、32 抬到 48 之后，点估计会动；但**区间宽度**才是样本量给的收益。
两组数字都按 Clopper–Pearson 95%（复用 `tools/stat_bounds.py`，不新造区间公式）给出。

为什么可以"复用旧结论"而不重跑全部样本
======================================
新样本（h31–h40 / d3e-*）是本轮实测（连跑 3 次，逐样本可复现性写在 reveal 产物里）；
旧样本（h1–h30 / d3-*）不重测，直接引用上一轮落盘结论。判据未变时这是可复现的；
判据一旦变，`tools/guard_rerun_671a.py` 会红——两个工具是配套的。

用法
====
    python tools/reveal_update_671a.py            # 现算并落盘
    python tools/reveal_update_671a.py --json     # 机读输出
    python tools/reveal_update_671a.py --selftest # 只读自检（纯函数）
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "data" / "experiments" / "reveal_update_671a.json"
PAPER = ROOT / "research" / "paper_v0.8.md"
WEB_METRICS = ROOT / "web" / "data" / "metrics_666.json"
WEB_VERDICTS = ROOT / "web" / "data" / "verdicts_667.json"

#: 论文/前端**当前引用**的旧数字（来源文件 → 值）；本工具只做"变没变"的对照
CITED_SOURCES = {
    "holdout": ("data/holdout_reveal_3_665.json", "web/data/metrics_666.json::metrics.holdout"),
    "corpus": ("data/external_corpus_reveal_665.json", "web/data/metrics_666.json::metrics.external"),
}

#: 论文里 `87.5%（14/16` / `87.5% (14/16` 两种写法都要认（表格用半角、行文用全角）
CITE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*[（(]\s*(\d+)\s*/\s*(\d+)")


def jload(p: Path) -> Any:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_stat_bounds():
    spec = importlib.util.spec_from_file_location("stat_bounds", HERE / "stat_bounds.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ─────────────────────────────────────────────────────────────────────────────
# 纯函数（可单测）
# ─────────────────────────────────────────────────────────────────────────────

def cp(k: int, n: int, conf: float = 0.95) -> dict[str, Any]:
    if n <= 0:
        return {"k": k, "n": n, "point": None, "cp_low": None, "cp_high": None, "conf": conf,
                "note": "n=0 ⇒ 拒绝给率（fail-loud）"}
    p = load_stat_bounds().proportion(k, n, conf)
    return {"k": k, "n": n, "point": p["point"], "cp_low": p["cp_low"],
            "cp_high": p["cp_high"], "conf": conf}


def rate_pct(k: int, n: int) -> float | None:
    if n <= 0:
        return None
    return round(k / n * 100, 1)


def update_block(label: str, old_k: int, old_n: int, new_k: int, new_n: int) -> dict[str, Any]:
    """一组"旧口径 → 新口径"的对照（点估计 + CP95 + 差值）。"""
    old_rate, new_rate = rate_pct(old_k, old_n), rate_pct(new_k, new_n)
    delta = (None if (old_rate is None or new_rate is None) else round(new_rate - old_rate, 1))
    return {
        "label": label,
        "before": {"k": old_k, "n": old_n, "rate_pct": old_rate, **cp(old_k, old_n)},
        "after": {"k": new_k, "n": new_n, "rate_pct": new_rate, **cp(new_k, new_n)},
        "delta_pp": delta,
        "interpretation": "分母与样本构成同时变了 ⇒ 差值是**测量对象**的变化，不是验证器变强/变弱",
    }


def interval_width_pp(block: dict[str, Any]) -> dict[str, Any]:
    """CP 区间宽度（pp）：样本量的收益看这里，不看点估计。"""
    def w(side: str) -> float | None:
        b = block[side]
        if b.get("cp_low") is None or b.get("cp_high") is None:
            return None
        return round((b["cp_high"] - b["cp_low"]) * 100, 1)
    bw, aw = w("before"), w("after")
    return {"before_pp": bw, "after_pp": aw,
            "narrowed_pp": (None if (bw is None or aw is None) else round(bw - aw, 1))}


def extract_citations(text: str) -> list[dict[str, Any]]:
    """从论文正文里抓 `pct%（k/n` 三元组（只读；本工具不改论文）。"""
    out: list[dict[str, Any]] = []
    for m in CITE_RE.finditer(text or ""):
        out.append({"pct": float(m.group(1)), "k": int(m.group(2)), "n": int(m.group(3)),
                    "pos": m.start()})
    return out


def cited_kn(text: str, k: int, n: int) -> float | None:
    """论文里有没有 `k/n` 的率；有则返回该率（用于"论文是否引用了旧分母"）。"""
    for c in extract_citations(text):
        if c["k"] == k and c["n"] == n:
            return c["pct"]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 现算
# ─────────────────────────────────────────────────────────────────────────────

def build(root: Path = ROOT) -> dict[str, Any]:
    h4 = jload(root / "data" / "holdout_reveal_4_671a.json") or {}
    h3 = jload(root / "data" / "holdout_reveal_3_665.json") or {}
    c_new = jload(root / "data" / "external_corpus_reveal_671a.json") or {}
    c_old = jload(root / "data" / "external_corpus_reveal_665.json") or {}
    paper = (root / "research" / "paper_v0.8.md")
    paper_txt = paper.read_text(encoding="utf-8") if paper.is_file() else ""

    h_cum = (h4.get("cumulative") or {}).get("error_subset") or {}
    h_den = (h4.get("cumulative") or {}).get("denominator") or {}
    h_ctrl = (h4.get("cumulative") or {}).get("control_subset") or {}
    h_old = h3.get("error_subset") or {}
    h_old_den = (h3.get("denominator") or {}).get("value")
    h_old_ctrl = h3.get("control_subset") or {}

    c_cum = c_new.get("cumulative") or {}
    c_old_den = (c_old.get("denominator") or {}).get("value")

    holdout_block = update_block("holdout 检出率（可测口径，真错子集）",
                                 int(h_old.get("catch", 0)), int(h_old_den or 0),
                                 int(h_cum.get("catch", 0)), int(h_den.get("value") or 0))
    corpus_block = update_block("外部 corpus 检出率（可测口径）",
                                int(c_old.get("catch", 0)), int(c_old_den or 0),
                                int(c_cum.get("catch", 0)), int(c_cum.get("denominator", {}).get("value") or 0))

    layers: dict[str, Any] = {}
    for lay, d in (c_new.get("cumulative_by_layer") or {}).items():
        n = int(d["denominator"]["value"])
        layers[lay] = {"total": d["total"], "measurable": n, "catch": d["catch"],
                       "miss": d["miss"], "unknown": d["unknown"],
                       "rate_pct": rate_pct(int(d["catch"]), n),
                       **({"cp95": cp(int(d["catch"]), n)} if n else
                          {"cp95": cp(0, 0), "note": "该层本机无检测器 ⇒ 拒绝给率"})}

    # —— 论文/前端引用的是哪一套数字（只读对照，不改）——
    cited_holdout = cited_kn(paper_txt, int(h_old.get("catch", 0)), int(h_old_den or 0))
    cited_corpus = cited_kn(paper_txt, int(c_old.get("catch", 0)), int(c_old_den or 0))
    web_metrics = jload(root / "web" / "data" / "metrics_666.json") or {}
    web_m = web_metrics.get("metrics") or {}
    web_holdout = (web_m.get("holdout") or {}).get("rate_pct")
    web_corpus = (web_m.get("external") or {}).get("rate_pct")

    pending: list[dict[str, Any]] = []
    if holdout_block["after"]["rate_pct"] != holdout_block["before"]["rate_pct"]:
        pending.append({
            "key": "holdout_rate_pct",
            "from": {"k": holdout_block["before"]["k"], "n": holdout_block["before"]["n"],
                     "rate_pct": holdout_block["before"]["rate_pct"]},
            "to": {"k": holdout_block["after"]["k"], "n": holdout_block["after"]["n"],
                   "rate_pct": holdout_block["after"]["rate_pct"]},
            "cited_by": {
                "paper_v0_8": cited_holdout,
                "web_metrics_666": web_holdout,
                "artifact": CITED_SOURCES["holdout"][0],
            },
            "action": ("论文 §6.1 三臂表 / 摘要 / §7.3 样本量表 / Fig.2/3 与前端 metrics / verdicts "
                       "里的 holdout 率需按新分母（含 h31–h40）重算；**由 671b 执行**"),
        })
    if corpus_block["after"]["rate_pct"] != corpus_block["before"]["rate_pct"]:
        pending.append({
            "key": "corpus_rate_pct",
            "from": {"k": corpus_block["before"]["k"], "n": corpus_block["before"]["n"],
                     "rate_pct": corpus_block["before"]["rate_pct"]},
            "to": {"k": corpus_block["after"]["k"], "n": corpus_block["after"]["n"],
                   "rate_pct": corpus_block["after"]["rate_pct"]},
            "cited_by": {
                "paper_v0_8": cited_corpus,
                "web_metrics_666": web_corpus,
                "artifact": CITED_SOURCES["corpus"][0],
            },
            "action": ("corpus 率**必须分层引用**（669d declared）：六层数字见本文件 `corpus.layers`；"
                       "由 671b 决定哪几层进论文表"),
        })
    old_fp, old_ctrl = int(h_old_ctrl.get("false_positive", 0)), int(h_old_ctrl.get("total", 0))
    new_fp, new_ctrl = int(h_ctrl.get("false_positive", 0)), int(h_ctrl.get("total", 0))
    detail = jload(root / "data" / "holdout" / "reveal_3_detail_671a.json") or {}
    new_fp_ids = [r["id"] for r in (detail.get("per_sample") or [])
                  if r.get("planted") is False and r.get("verdict") == "catch"
                  and r.get("source") == "measured_671a"]
    if (new_fp, new_ctrl) != (old_fp, old_ctrl):
        pending.append({
            "key": "holdout_false_positive",
            "from": {"fp": old_fp, "total": old_ctrl, "rate_pct": rate_pct(old_fp, old_ctrl)},
            "to": {"fp": new_fp, "total": new_ctrl, "rate_pct": rate_pct(new_fp, new_ctrl)},
            "who_added": new_fp_ids,
            "action": ("对照样本增加 ⇒ 论文里 FPR（11.1% = 1/9）需同步；"
                       f"{new_fp_ids} 属「未指定/历史类对照被判为检出」⇒ 要么改口径说明，"
                       "要么登记为假阳性；由 671b 裁定"),
        })

    return {
        "schema": "queyi-reveal-update/671a",
        "generated_by": "tools/reveal_update_671a.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {
            "holdout_new": "data/holdout_reveal_4_671a.json",
            "holdout_old": "data/holdout_reveal_3_665.json",
            "holdout_detail_new": "data/holdout/reveal_3_detail_671a.json",
            "corpus_new": "data/external_corpus_reveal_671a.json",
            "corpus_old": "data/external_corpus_reveal_665.json",
            "corpus_detail_new": "data/external_corpus/reveal_detail_671a.json",
        },
        "caliber": ("真错分母 = catch+miss（可测）；unknown（检测器不可用）不进分母；"
                    "planted=False 的对照单列（catch ⇒ false_positive）"),
        "holdout": {
            **holdout_block,
            "interval_width": interval_width_pp(holdout_block),
            "false_positive": {"before": {"fp": old_fp, "total": old_ctrl,
                                          "rate_pct": rate_pct(old_fp, old_ctrl)},
                               "after": {"fp": new_fp, "total": new_ctrl,
                                         "rate_pct": rate_pct(new_fp, new_ctrl)}},
            "added_samples": (h4.get("samples_requested") or []),
            "reproducible": (h4.get("reproducibility") or {}).get("all_reproducible"),
            "round4_only": (h4.get("round4") or {}).get("error_subset"),
        },
        "corpus": {
            **corpus_block,
            "interval_width": interval_width_pp(corpus_block),
            "layers": layers,
            "added_samples": (c_new.get("samples_requested") or []),
            "reproducible": (c_new.get("reproducibility") or {}).get("all_reproducible"),
            "caliber_change": c_new.get("caliber_change"),
            "new_only": (c_new.get("new_samples") or {}),
        },
        "pending_for_671b": pending,
        "not_modified": ["research/paper_v0.8.md", "research/latex/*", "web/data/*.json"],
        "recompute": {
            "holdout": "python tools/holdout_reveal_4_671a.py --runs 3",
            "corpus": "python tools/external_corpus_reveal_671a.py --runs 3",
            "update": "python tools/reveal_update_671a.py",
            "note": "三次结果必须逐样本一致（reveal 产物里的 reproducibility 字段）",
        },
        "honest_note": ("扩样样本（h31–h40 / d3e-*）在 reveal 之后并入 ⇒ **无盲态**，"
                        "只用于增大样本量；本文件不给「外部效度」结论，"
                        "只给可复算的新数字与「待更新清单」。"),
    }


def render(rep: dict[str, Any]) -> str:
    h, c = rep["holdout"], rep["corpus"]
    L = ["[reveal update 671a]",
         f"  holdout  {h['before']['k']}/{h['before']['n']} = {h['before']['rate_pct']}%"
         f"  →  {h['after']['k']}/{h['after']['n']} = {h['after']['rate_pct']}%"
         f"  （Δ{h['delta_pp']}pp；CP95 宽度 {h['interval_width']['before_pp']}→"
         f"{h['interval_width']['after_pp']}pp）",
         f"  corpus   {c['before']['k']}/{c['before']['n']} = {c['before']['rate_pct']}%"
         f"  →  {c['after']['k']}/{c['after']['n']} = {c['after']['rate_pct']}%"
         f"  （Δ{c['delta_pp']}pp；CP95 宽度 {c['interval_width']['before_pp']}→"
         f"{c['interval_width']['after_pp']}pp）"]
    for lay, d in sorted(c["layers"].items()):
        L.append(f"    corpus/{lay:<15} {d['catch']}/{d['measurable']} = {d['rate_pct']}%"
                 if d["measurable"] else f"    corpus/{lay:<15} 可测 0 ⇒ 拒绝给率")
    L.append(f"  对照假阳性 {h['false_positive']['before']['fp']}/"
             f"{h['false_positive']['before']['total']} → "
             f"{h['false_positive']['after']['fp']}/{h['false_positive']['after']['total']}")
    for p in rep["pending_for_671b"]:
        L.append(f"  [待 671b] {p['key']}: {p['from'].get('rate_pct') or p['from']} → "
                 f"{p['to'].get('rate_pct') or p['to']}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("rate_pct 空分母拒绝给率", rate_pct(3, 0) is None)
    chk("rate_pct 正常", rate_pct(14, 16) == 87.5)
    b = update_block("t", 14, 16, 17, 21)
    chk("update_block 点估计", b["before"]["rate_pct"] == 87.5 and b["after"]["rate_pct"] == 81.0)
    chk("update_block CP 由 stat_bounds 现算",
        abs(b["after"]["cp_low"] - 0.5809) < 0.005 and abs(b["after"]["cp_high"] - 0.9455) < 0.005)
    w = interval_width_pp(update_block("t", 14, 16, 17, 21))
    chk("区间宽度可算", w["after_pp"] is not None and w["before_pp"] is not None)
    chk("n=0 时区间宽度为 None（不编数字）", interval_width_pp(update_block("t", 0, 0, 1, 2))["before_pp"] is None)
    chk("extract_citations 认全角括号", extract_citations("**87.5%（14/16）**")[0]["n"] == 16)
    chk("extract_citations 认半角括号", extract_citations("87.5% (14/16)")[0]["k"] == 14)
    chk("cited_kn 命中", cited_kn("x 43.8%（14/32）y", 14, 32) == 43.8)
    chk("cited_kn 未命中", cited_kn("x 43.8%（14/32）y", 14, 16) is None)
    rep = build()
    chk("build 产出 holdout/corpus 两块", "holdout" in rep and "corpus" in rep)
    chk("build 待更新清单非空（扩样必然会动分母）", len(rep["pending_for_671b"]) >= 1)
    chk("build 不改论文（not_modified 有声明）", "research/paper_v0.8.md" in rep["not_modified"])
    chk("分层都给 CP 或显式拒给率",
        all(("cp95" in d) for d in rep["corpus"]["layers"].values()))
    chk("产出 JSON 里没有 NaN", "NaN" not in json.dumps(rep))
    print(f"reveal_update_671a selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671a C3：扩样 reveal 后的检出率更新（只算不改论文）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    rep = build()
    if not a.no_write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
        if not a.no_write:
            print(f"已写 {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
