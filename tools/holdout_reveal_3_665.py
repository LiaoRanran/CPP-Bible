#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_reveal_3_665.py — 665 C2：扩样后的第三次 reveal（reveal_3）。

相对 reveal_2（662）改了什么
============================
1. 样本：20 → 30（665 C1 追加 h21–h30，**全部 planted=true 真错**）
   ⇒ 真错分母 7 → **17**；对照 8；unknown 标签 5。
2. 判据：**不新增检测器**——老样本走 `rv661.detect` + `rv661.PLAN`；
   新样本只是把 `rv661.ATOMS` 临时指向我们的夹具目录后走同一套 `detect`
   （同一个 `detect` = 同一判据，不让"换个文件位置"变成"换个口径"）。
3. 分母仍然是 **catch+miss**（可测样本）；unknown = 检测器不可用，**不计入分母**。

诚实前置（写在工具里）
======================
* 这批新样本是在 holdout **已 reveal 之后**追加的 ⇒ **不具备盲态**。
  所以本 reveal **不能**用来 Claim"外部效度提升"；它的用处只有一个：
  **把可测真错样本从 5 个抬到 17 个**，让点估计不再是 4/5。
* `.revealed` 不可回盲；本工具只在 `data/` 写报告，不改 holdout 的 revealed 标记。

输出：data/holdout_reveal_3_665.json
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
HOLD = os.path.join(ROOT, "data", "holdout", "holdout.json")
R2 = os.path.join(ROOT, "data", "holdout_reveal_2_662.json")
OUT = os.path.join(ROOT, "data", "holdout_reveal_3_665.json")
FIXTURES = os.path.join(ROOT, "data", "cards_665", "fixtures")

#: 665 C1 新增样本的复现计划（文件名相对 `data/cards_665/fixtures/`）
NEW_PLAN = {
    "h21": ("ubsan", ["ig-01.cpp"]),
    "h22": ("asan", ["ig-02.cpp"]),
    "h23": ("asan", ["ig-07.cpp"]),
    "h24": ("ubsan", ["ig-08.cpp"]),
    "h25": ("asan", ["ig-14.cpp"]),
    "h26": ("asan", ["h26.cpp"]),
    "h27": ("asan", ["h27.cpp"]),
    "h28": ("asan", ["h28.cpp"]),
    "h29": ("ubsan", ["h29.cpp"]),
    "h30": ("asan", ["h30.cpp"]),
}


def _load_rv661():
    spec = importlib.util.spec_from_file_location("rv661", os.path.join(HERE, "holdout_reveal_661.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sensitivity_opt(rv, missed: list[dict]) -> list[dict]:
    """对未检出的新增样本做**优化档敏感性**复跑（-O0 vs -O1）。

    为什么需要：本次实测发现 `asan` 类样本（use-after-free / double-free / leak）在
    pipeline 标准的 `-O1` 下会被**优化掉整个内存操作**（无可观测副作用）⇒ ASan 无从报告。
    这**不是** ASan 不会报，而是"测试夹具 + 编译档"组合让它没得报。
    同一套 `-O0` 复跑能把这条争议讲成可复算的数字，而不是口头辩解。

    判据复用 rv661 的关键字（不为敏感性再造一套"命中"定义）。
    """
    rows = []
    for r in missed:
        kind = r["detector"]
        if kind not in rv.SAN:
            continue
        src = _to_wsl_if_win(r["src"])
        for opt in ("-O1", "-O0"):
            bin_path = f"/tmp/sens_{r['id']}_{opt.strip('-')}"
            cmd_c = (f"g++ -std=c++17 {opt} -g -fsanitize={rv.SAN[kind]} -pthread {src} -o {bin_path}")
            rc_c, out_c = subprocess_run(["wsl", "-e", "bash", "-lc", cmd_c], timeout=180)
            if rc_c != 0:
                rows.append({"id": r["id"], "opt": opt, "verdict": "compile-fail", "note": out_c[:120]})
                continue
            _, out = subprocess_run(["wsl", "-e", "bash", "-lc", bin_path], timeout=120)
            low = out.lower()
            hit = ("ThreadSanitizer" in out if kind == "tsan" else
                   ("AddressSanitizer" in out or "LeakSanitizer" in out
                    or "detected memory leaks" in low or "double-free" in low) if kind == "asan"
                   else "runtime error" in out)
            rows.append({"id": r["id"], "opt": opt, "verdict": ("catch" if hit else "miss"),
                         "note": (out.strip().splitlines() or [""])[0][:120]})
    return rows


def _to_wsl_if_win(p: str) -> str:
    p = p.replace("\\", "/")
    return ("/mnt/" + p[0].lower() + p[2:]) if len(p) > 1 and p[1] == ":" else p


def subprocess_run(cmd, timeout: int = 180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -1, f"EXC: {e}"


def _load_ext665():
    spec = importlib.util.spec_from_file_location("ext665", os.path.join(HERE, "holdout_extend_665.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main() -> int:
    rv = _load_rv661()
    # 读 **canonical 合并视图**（旧 20 + 665 的 10）。直接读 holdout.json 不行：
    # 那个文件是 holdout_658.py 的产物，旧工具一跑就会把 665 的追加抹掉（本批踩过）。
    h = _load_ext665().load_merged()
    r2 = json.load(open(R2, encoding="utf-8")) if os.path.isfile(R2) else {}
    r2_map = {x["id"]: x for x in r2.get("results", [])}

    results = []
    err_total = err_catch = err_miss = err_unknown = 0
    ctrl_total = ctrl_fp = 0
    unknown_label = 0
    new_sample_fails = []
    rv.PLAN = {**rv.PLAN, **NEW_PLAN}          # 同判据：只是把新样本登记进 PLAN

    for s in h["seeds"]:
        sid = s["id"]
        kind, files = rv.PLAN.get(sid, ("unknown", []))
        old_atoms = rv.ATOMS
        if sid in NEW_PLAN:                     # 新样本夹具不在 Examples/atoms 下
            rv.ATOMS = FIXTURES
        try:
            verdict, note = rv.detect(kind, files)
        finally:
            rv.ATOMS = old_atoms
        if verdict == "unknown" and s.get("planted") is True:
            new_sample_fails.append({"id": sid, "detector": kind, "note": note[:160]})
        lab = s.get("planted")
        if lab is True:
            err_total += 1
            if verdict == "catch":
                err_catch += 1
            elif verdict == "miss":
                err_miss += 1
            else:
                err_unknown += 1
        elif lab is False:
            ctrl_total += 1
            if verdict == "catch":
                ctrl_fp += 1
        else:
            unknown_label += 1
        prev = r2_map.get(sid, {}).get("verdict")
        results.append({"id": sid, "planted": lab, "detector": kind, "verdict": verdict,
                        "note": note[:240], "is_665_new": sid in NEW_PLAN,
                        "reveal_2": prev, "changed_vs_reveal_2": (prev is not None and prev != verdict)})
        print(f"  {sid:<4} {str(lab):<7} {kind:<14} {verdict:<8} {note[:52]}")

    # —— 优化档敏感性：只对"本批新增且被判 miss"的样本做（-O1 是 pipeline 默认档）——
    missed_new = [{"id": s["id"], "detector": NEW_PLAN[s["id"]][0],
                   "src": os.path.join(ROOT, str(s["atom_ref"]))}
                  for s in h["seeds"]
                  if s["id"] in NEW_PLAN and s.get("planted") is True
                  and next(r for r in results if r["id"] == s["id"])["verdict"] == "miss"]
    sens = sensitivity_opt(rv, missed_new) if missed_new else []
    if sens:
        print("\n[敏感性] miss 样本在 -O0/-O1 下的对照：")
        for row in sens:
            print(f"  {row['id']:<4} {row['opt']:<4} {row['verdict']:<12} {row['note'][:60]}")

    denom = err_catch + err_miss
    rate = (err_catch / denom * 100) if denom else 0.0
    prev = r2.get("error_subset", {})
    rep = {
        "schema": "queyi-holdout-reveal/v3",
        "reveal_index": 3,
        "revealed_at": time.strftime("%Y-%m-%d"),
        "generated_by": "tools/holdout_reveal_3_665.py",
        "detector_reuse": "复用 tools/holdout_reveal_661.py::detect（同一判据）；新样本仅切换 ATOMS 目录",
        "labels": {"error": err_total, "control": ctrl_total, "unknown": unknown_label},
        "error_subset": {"total": err_total, "catch": err_catch, "miss": err_miss,
                         "unknown": err_unknown, "detect_rate_pct": round(rate, 1)},
        "control_subset": {"total": ctrl_total, "false_positive": ctrl_fp},
        "compare_reveal_2": {
            "before_total": prev.get("catch", 0) + prev.get("miss", 0) + prev.get("unknown", 0),
            "before_rate_pct": prev.get("detect_rate_pct"),
            "after_total": err_total,
            "after_rate_pct": round(rate, 1),
            "changed_verdicts": [r["id"] for r in results if r["changed_vs_reveal_2"]],
            "note": ("注意口径：分母从 7 抬到 17 之后，检出率的变化只说明**样本构成变了**，"
                     "不说明验证器变好/变差；两轮都把 unknown（检测器不可用）留在分母之外。"),
        },
        "honest_note": ("665 C1 追加的 10 个样本**不具备盲态**（在原 holdout reveal 之后追加），"
                        "本轮只用于**增大样本量**（可测真错 5 → 见 error_subset 分母），"
                        "**不得**据此 Claim 外部效度提升。"),
        "new_sample_unknown": new_sample_fails,
        "opt_sensitivity": {
            "why": ("本次 miss 样本在 pipeline 默认的 -O1 下可能被优化掉整段内存操作"
                    "（无可观测副作用）⇒ 报不出不等于检测器不会报，而是夹具与编译档的组合结果。"),
            "rows": sens,
        },
        "honest_addendum": ("敏感性只用来解释 miss 的**成因**，不回改检出率："
                            "报告正文的 66.7% 仍是 -O1 pipeline 口径下的数字。"),
        "results": results,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n真错子集({err_total}): catch={err_catch} miss={err_miss} unknown={err_unknown} → 检出率={rate:.1f}%")
    print(f"对照子集({ctrl_total}): false_positive={ctrl_fp}；unknown 标签={unknown_label}")
    print(f"reveal_2 检出率={prev.get('detect_rate_pct')}% → reveal_3={rate:.1f}%")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
