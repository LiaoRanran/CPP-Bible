#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""audit_676k_sample.py — 676k 任务B：标签双标注复核（T17）。

三件事：
  1) 分层抽样：层 = (batch, defect_type)，每层取 max(1, round(10%))，随机种子 6761。
  2) 输出**盲化**重标注输入：只给源码，且**注释全部抹为空白**（保留行号）。
     抹注释的理由：expB/expG 的 .cpp 头部直接写着 `defect_type:` / `planted:` /
     `expected_verdict:`，不抹就等于把原标注喂给重标注者，κ 会虚高。抹掉后重标注者
     只能从代码本身推断 ⇒ 得到的是**保守下界**。
  3) 评分：读回重标注结果，算 Cohen's κ（defect_type / expected_verdict）、
     行号匹配率、planted 一致率、按 defect_type 分组的一致率。

用法：
  python tools/audit_676k_sample.py --sample            # 写抽样清单
  python tools/audit_676k_sample.py --dump-code FILE    # 写盲化源码（重标注输入）
  python tools/audit_676k_sample.py --score             # 读 relabel 结果算一致性
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLINDSPOT = os.path.join(ROOT, "data", "blindspot_676g_sample_manifest.json")
EXPDIR = os.path.join(ROOT, "data", "holdout_expansion")
SAMPLE_OUT = os.path.join(ROOT, "data", "676k_sample_manifest.json")
RELABEL = os.path.join(ROOT, "data", "676k_relabel_results.json")

SEED = 6761
FRACTION = 0.10

EXP_BATCHES = ["expA", "expB", "expC", "expD", "expE", "expF", "expG"]

# --------------------------------------------------------------------------- #
# 统一缺陷分类法（把 70 个原始取值 + 重标注取值都映射到这套 16 类）
# --------------------------------------------------------------------------- #
TAXONOMY = {
    "memory_lifetime": ["memory_safety", "use_after_free", "double_free", "leak", "memory_leak",
                        "resource_leak", "raii_violation", "move_semantics", "smart_pointer",
                        "memory", "MEM", "RAII/UB", "self_move", "dangling_reference"],
    "out_of_bounds": ["out_of_bounds", "heap_overflow", "heap_overread", "heap_underflow",
                      "stack_overflow", "stack_overread", "stack_overflow_write", "global_overflow",
                      "pointer_overflow", "info_leak"],
    "null_deref": ["null_pointer_deref", "null_deref"],
    "uninitialized_read": ["uninitialized_read"],
    "data_race": ["data_race", "race_condition", "CONC"],
    "concurrency_order": ["memory_order", "memory-order", "atomic_ub"],
    "liveness": ["deadlock", "aba_problem", "lock_priority_inversion", "condition_variable",
                 "infinite_loop", "resource_exhaustion"],
    "stl_iterator": ["iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse"],
    "integer_ub": ["integer_overflow", "division_by_zero", "bit_operation"],
    "type_alias_alignment": ["type_punning", "type_confusion", "alignment", "endianness",
                             "ODR", "odr_violation"],
    "optimization_or_compiler": ["optimization_dependent", "compiler-diff", "compiler-bug",
                                 "compiler_warning"],
    "virtual_or_oop": ["virtual_function", "lambda_capture"],
    "embedded_platform": ["volatile_misuse", "interrupt_safety", "register_ub"],
    "logic_or_api": ["logic_error", "API", "api_misuse", "state_machine", "cross_tu_ub",
                     "timing_side_channel"],
    "generic_ub": ["UB", "undefined_behavior", "other_ub", "unspecified", "ambiguity",
                   "historical", "conditional_trigger"],
}
TYPE2CANON = {t: c for c, ts in TAXONOMY.items() for t in ts}
CANON = sorted(TAXONOMY)


def canon(label: str | None) -> str:
    if label is None:
        return "unknown"
    return TYPE2CANON.get(label, "unknown")


# --------------------------------------------------------------------------- #
# 装载
# --------------------------------------------------------------------------- #
def _strip_comment_lines(text: str) -> str:
    """把注释内容替换为等长空白，**保留行号与列位**。"""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "/":
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
        elif c == "/" and nxt == "*":
            out.append("  ")
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append("  ")
            i += 2
        elif c in "\"'":
            q = c
            out.append(c)
            i += 1
            while i < n and text[i] != q:
                out.append(text[i])
                i += 2 if text[i] == "\\" else 1
            if i < n:
                out.append(q)
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def load() -> list[dict]:
    bs = json.load(open(BLINDSPOT, encoding="utf-8"))
    recs = []
    for e in bs["samples"]:
        d = e.get("dir") or ""
        files = e.get("files") or []
        texts = []
        for f in files:
            p = os.path.join(ROOT, d, f) if d else os.path.join(ROOT, f)
            if os.path.exists(p):
                texts.append(open(p, encoding="utf-8", errors="replace").read())
        recs.append({
            "uid": e["uid"],
            "sample_id": e["sample_id"],
            "batch": e["source_batch"],
            "defect_type": e.get("defect_type"),
            "planted": e.get("planted"),
            "expected_verdict": e.get("expected_verdict"),
            "files": files,
            "dir": d,
            "code": "\n".join(texts) if texts else None,
        })
    return recs


# --------------------------------------------------------------------------- #
# 抽样
# --------------------------------------------------------------------------- #
def do_sample(recs: list[dict]) -> dict:
    rng = random.Random(SEED)
    strata = collections.defaultdict(list)
    for r in recs:
        strata[(r["batch"], r["defect_type"] or "?")].append(r)

    picked = []
    per_stratum = {}
    for key in sorted(strata):
        members = sorted(strata[key], key=lambda x: x["uid"])
        n = len(members)
        k = max(1, int(round(FRACTION * n)))
        k = min(k, n)
        chosen = rng.sample(members, k)
        per_stratum[f"{key[0]}|{key[1]}"] = {"n": n, "k": k}
        picked.extend(chosen)

    picked.sort(key=lambda x: x["uid"])
    out = {
        "schema": "queyi-audit-676k-sample/v1",
        "generated_by": "tools/audit_676k_sample.py",
        "seed": SEED,
        "fraction": FRACTION,
        "n_population": len(recs),
        "n_strata": len(strata),
        "n_sampled": len(picked),
        "per_stratum": per_stratum,
        "sampled": [
            {"uid": r["uid"], "batch": r["batch"], "defect_type": r["defect_type"],
             "files": r["files"], "dir": r["dir"]}
            for r in picked
        ],
    }
    with open(SAMPLE_OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    return out


def load_sample_manifest() -> dict:
    return json.load(open(SAMPLE_OUT, encoding="utf-8"))


def do_dump(path: str) -> None:
    man = load_sample_manifest()
    recs = {r["uid"]: r for r in load()}
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 676k 盲化重标注输入 · seed={SEED} · n={man['n_sampled']}\n")
        f.write("# 注释已抹为空白（保留行号）；不含任何原始标注字段。\n\n")
        for i, s in enumerate(man["sampled"], 1):
            r = recs[s["uid"]]
            f.write(f"===== [{i}] uid={s['uid']} batch={s['batch']} files={s['files']} =====\n")
            code = r["code"] or "(no source on disk)"
            f.write(_strip_comment_lines(code).rstrip() + "\n\n")
    print(f"wrote {path} ({man['n_sampled']} samples)")


# --------------------------------------------------------------------------- #
# 评分
# --------------------------------------------------------------------------- #
def cohen_kappa(pairs: list[tuple[str, str]]) -> dict:
    """Cohen's kappa = (Po - Pe) / (1 - Pe)。"""
    n = len(pairs)
    if n == 0:
        return {"n": 0, "po": None, "pe": None, "kappa": None}
    labels = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    po = sum(1 for a, b in pairs if a == b) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    k = (po - pe) / (1 - pe) if pe != 1 else 1.0
    return {"n": n, "po": round(po, 6), "pe": round(pe, 6), "kappa": round(k, 6),
            "labels": labels}


def do_score() -> dict:
    man = load_sample_manifest()
    rel = json.load(open(RELABEL, encoding="utf-8"))
    relmap = {r["uid"]: r for r in rel["relabels"]}
    recs = {r["uid"]: r for r in load()}

    rows = []
    for s in man["sampled"]:
        uid = s["uid"]
        r = recs[uid]
        g = relmap.get(uid)
        if g is None:
            continue
        rows.append({
            "uid": uid,
            "batch": s["batch"],
            "orig_type": r["defect_type"],
            "rel_type": g["defect_type"],
            "orig_canon": canon(r["defect_type"]),
            "rel_canon": canon(g["defect_type"]),
            "orig_verdict": r["expected_verdict"],
            "rel_verdict": g["expected_verdict"],
            "orig_line": None,  # 由 do_score 外部补入（见 --line-source）
            "rel_line": g["defect_line"],
            "orig_planted": r["planted"],
            "rel_planted": g["planted"],
            "note": g.get("note", ""),
        })

    # 行号：原始行号从扩展批次 .json 读（holdout/corpus 清单无行号 ⇒ 跳过）
    for row in rows:
        uid = row["uid"]
        batch, sid = uid.split(":", 1)
        if batch in EXP_BATCHES:
            # 各批次的 json 文件名规则不同：expD/expF 的 uid 里是 D013/F013，文件名是 sample_D013.json
            stem = sid if sid.startswith("sample_") else f"sample_{sid}"
            p = os.path.join(EXPDIR, batch, stem + ".json")
            if os.path.exists(p):
                d = json.load(open(p, encoding="utf-8"))
                loc = d.get("defect_location") or {}
                row["orig_line"] = loc.get("line")

    verdict_pairs = [(r["orig_verdict"] or "unknown", r["rel_verdict"]) for r in rows]
    type_pairs_canon = [(r["orig_canon"], r["rel_canon"]) for r in rows]
    type_pairs_raw = [(r["orig_type"] or "unknown", r["rel_type"]) for r in rows]
    planted_pairs = [
        (str(r["orig_planted"]).lower(), str(r["rel_planted"]).lower())
        for r in rows if r["orig_planted"] is not None
    ]
    line_rows = [r for r in rows if r["orig_line"] is not None and r["rel_line"] is not None]
    line_hit = sum(1 for r in line_rows if r["orig_line"] == r["rel_line"])

    by_type = collections.defaultdict(list)
    for r in rows:
        by_type[r["orig_type"] or "unknown"].append(r)
    per_type = {}
    for t, rs in sorted(by_type.items()):
        ok = sum(1 for r in rs if r["orig_canon"] == r["rel_canon"])
        per_type[t] = {"n": len(rs), "canon_agree": ok,
                       "rate": round(ok / len(rs), 4)}

    result = {
        "schema": "queyi-audit-676k-relabel-score/v1",
        "n_scored": len(rows),
        "kappa_defect_type_canon": cohen_kappa(type_pairs_canon),
        "kappa_defect_type_raw": cohen_kappa(type_pairs_raw),
        "kappa_expected_verdict": cohen_kappa(verdict_pairs),
        "planted_agreement": cohen_kappa(planted_pairs),
        "line": {"n": len(line_rows), "exact": line_hit,
                 "rate": round(line_hit / len(line_rows), 4) if line_rows else None},
        "per_defect_type": per_type,
        "rows": rows,
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--dump-code")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()

    if args.sample:
        out = do_sample(load())
        print(f"抽样完成：总体 {out['n_population']}，层数 {out['n_strata']}，"
              f"抽中 {out['n_sampled']} → {SAMPLE_OUT}")
        return 0
    if args.dump_code:
        do_dump(args.dump_code)
        return 0
    if args.score:
        res = do_score()
        if args.json:
            json.dump(res, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"n={res['n_scored']}")
        print(f"defect_type (统一分类法)  κ={res['kappa_defect_type_canon']['kappa']} "
              f"Po={res['kappa_defect_type_canon']['po']}")
        print(f"defect_type (原始字符串)  κ={res['kappa_defect_type_raw']['kappa']} "
              f"Po={res['kappa_defect_type_raw']['po']}")
        print(f"expected_verdict          κ={res['kappa_expected_verdict']['kappa']} "
              f"Po={res['kappa_expected_verdict']['po']}")
        print(f"planted                   κ={res['planted_agreement']['kappa']} "
              f"Po={res['planted_agreement']['po']}")
        print(f"行号精确匹配 {res['line']['exact']}/{res['line']['n']} = {res['line']['rate']}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
