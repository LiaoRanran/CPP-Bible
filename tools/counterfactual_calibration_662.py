#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""counterfactual_calibration_662.py — 662 B3：反事实引文算子校准。

现状：算子 `tools/counterfactual_citation_658.py` 用 token 重叠≥0.3 或显式引用 id 判 dependent。
校准：用 10 个正例（data/counterfactual_cases_660.json，label=dependent）+ 10 个构造负例
（把引文换成与断言无关的文本 → label=independent），扫描阈值 τ，算 precision/recall/F1。
输出：data/counterfactual_calibration_662.json
"""
from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "counterfactual_cases_660.json")
OUT = os.path.join(ROOT, "data", "counterfactual_calibration_662.json")


def toks(t):
    return set(re.findall(r"[一-鿿a-zA-Z0-9_]+", t.lower()))


def score(assertion, cid, ctext):
    """返回 (cites_id, overlap_ratio)。"""
    cites = cid.lower() in assertion.lower()
    a, c = toks(assertion), toks(ctext)
    return cites, (len(a & c) / max(1, len(c)))


def pred(assertion, cid, ctext, tau):
    cites, ratio = score(assertion, cid, ctext)
    return cites or ratio >= tau


def main() -> int:
    pos = json.load(open(CASES, encoding="utf-8"))["cases"]
    # 负例：同断言 + 换成与断言无关的引文（且不显式引用 id）
    negs = []
    for i, c in enumerate(pos):
        negs.append({"_src": c["id"], "original_assertion": c["original_assertion"],
                     "cid": "Cit-901", "ctext": f"本引文与上面的断言无关，编号 {i}"})

    labels = [(c["original_assertion"], c["original_citation"]["id"], c["original_citation"]["text"], True)
              for c in pos]
    labels += [(n["original_assertion"], n["cid"], n["ctext"], False) for n in negs]

    rows = []
    best = None
    for tau in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6]:
        tp = fp = fn = tn = 0
        for a, cid, ctext, y in labels:
            p = pred(a, cid, ctext, tau)
            if p and y:
                tp += 1
            elif p and not y:
                fp += 1
            elif (not p) and y:
                fn += 1
            else:
                tn += 1
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        rows.append({"tau": tau, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
                     "precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3)})
        if best is None or f1 > best["f1"]:
            best = rows[-1]

    rep = {
        "schema": "queyi-counterfactual-calibration/v1",
        "generated_at": "2026-09-28",
        "generated_by": "tools/counterfactual_calibration_662.py",
        "dataset": {"positive": len(pos), "negative": len(negs), "total": len(labels),
                    "source": "data/counterfactual_cases_660.json（正例）+ 构造负例"},
        "current_threshold": 0.3,
        "best": best,
        "sweep": rows,
        "honest_note": ("负例是**构造**的（同断言+无关引文），故 P/R 反映的是'区分显式引用 vs 无关引文'，"
                        "非真实分布上的精度；真实语料需 B1 外部 corpus 的引文级标注（本批未做）。"),
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for r in rows:
        print(f"  tau={r['tau']:<5} P={r['precision']:<5} R={r['recall']:<5} F1={r['f1']:<5} "
              f"(tp={r['tp']} fp={r['fp']} fn={r['fn']} tn={r['tn']})")
    print(f"\n最佳 τ={best['tau']} → P={best['precision']} R={best['recall']} F1={best['f1']}")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
