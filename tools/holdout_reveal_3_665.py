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
import re
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
HOLD = os.path.join(ROOT, "data", "holdout", "holdout.json")
R2 = os.path.join(ROOT, "data", "holdout_reveal_2_662.json")
OUT = os.path.join(ROOT, "data", "holdout_reveal_3_665.json")
#: 668：**逐样本明细 + 运行环境**单独落盘到 `data/holdout/`（同一次运行、同一个生成器）。
DETAIL = os.path.join(ROOT, "data", "holdout", "reveal_3_detail_668.json")
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


#: 从 note 文本里解析**实际跑过的档位**（派生量：不另存一份状态，避免第二事实源）
_OPT_RE = re.compile(r"(-O[0-3sg])\(")


def opts_from_note(note: str) -> list[str]:
    """返回该样本实际被编译过的优化档（如 `['-O0', '-O2']`）。"""
    return sorted(set(_OPT_RE.findall(note)))


def env_probe() -> dict:
    """记录**跑出这些数字的环境** —— 数字离开环境就不可复算。"""
    import sys  # 局部 import：只在真要探环境时才需要

    wsl = subprocess_run(["wsl", "-e", "bash", "-lc", "g++ --version | head -1"])[1].strip()
    gpp = (subprocess_run(["g++", "--version"])[1].strip().splitlines() or [""])[0]
    clang = (subprocess_run(["clang++", "--version"])[1].strip().splitlines() or [""])[0]
    return {
        "wsl_gpp": wsl.splitlines()[0].strip() if wsl else "(不可用)",
        "local_gpp": gpp.strip() or "(不可用)",
        "local_clang": clang.strip() or "(不可用)",
        "host": sys.platform,
        "python": sys.version.split()[0],
        "roll": "sanitizer 类在 WSL 里编译运行；warn/cross/link 类用本机编译器；WSL 不可用时记 unknown",
    }


def main() -> int:
    rv = _load_rv661()
    # 读 **canonical 合并视图**（旧 20 + 665 的 10）。直接读 holdout.json 不行：
    # 那个文件是 holdout_658.py 的产物，旧工具一跑就会把 665 的追加抹掉（本批踩过）。
    h = _load_ext665().load_merged()
    r2 = json.load(open(R2, encoding="utf-8")) if os.path.isfile(R2) else {}
    # 668：**先读上一次的落盘**，好在明细里给出"哪个样本变了"（重跑不是覆盖，是留痕）
    old_map: dict = {}
    if os.path.isfile(OUT):
        try:
            old_map = {x["id"]: x.get("verdict") for x in
                       json.load(open(OUT, encoding="utf-8")).get("results", [])}
        except Exception:  # noqa: BLE001
            old_map = {}
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
    opt_levels = list(getattr(rv, "OPT_LEVELS", ()))
    env = env_probe()
    rep = {
        "schema": "queyi-holdout-reveal/v3",
        "reveal_index": 3,
        "revealed_at": time.strftime("%Y-%m-%d"),
        "generated_by": "tools/holdout_reveal_3_665.py",
        "detector_reuse": "复用 tools/holdout_reveal_661.py::detect（同一判据）；新样本仅切换 ATOMS 目录",
        # 668：口径与分母**由生成器写进产物**（666 的 81.2% 就是因为口径写在工具注释里、
        # 数字写在文档里、两边没人对过）。谁引用这个数字，就必须引用这两个字段。
        "caliber": (f"sanitizer 类：{' + '.join(opt_levels)} 两档都跑，任一档报出即 catch；"
                    "warn/cross/link 类：单次本机编译；unknown = 检测器不可用（不计入分母）"),
        "opt_levels": opt_levels,
        "denominator": {
            "value": denom,
            "meaning": "catch+miss（可测真错样本）",
            "excluded": {"detector_unknown": err_unknown, "label_unknown": unknown_label},
            "all_error_labeled": err_total,
        },
        "env": env,
        "per_sample_detail": "data/holdout/reveal_3_detail_668.json",
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
            # 666 A5 备注：pipeline 已改为 -O0/-O2 双档；本节是 665 当时的 -O0/-O1 对照留证。
        "why": ("本次 miss 样本在 pipeline 默认的 -O1 下可能被优化掉整段内存操作"
                    "（无可观测副作用）⇒ 报不出不等于检测器不会报，而是夹具与编译档的组合结果。"),
            "rows": sens,
        },
        "honest_addendum": (
            "666 A5 起**口径已变**：pipeline 不再只跑单一 `-O1`，而是**先 -O0、再 -O2 两档都跑**"
            "（`rv661.detect` 读 `rv661.OPT_LEVELS`），任一档报出即判 catch。"
            "所以本报告的 `detect_rate_pct` 是**双档口径**；它高于 665 当时的 66.7% "
            "**不是**因为验证器变强，而是因为旧口径把'只在 -O0 暴露'的缺陷记成了假 miss。"
            "本节的 -O0/-O1 敏感性复跑因此退化为**历史对照**，保留作证据。"
            "【668 补】666 期间对外声称的 **81.2%（13/16）从未出现在任何产物里**："
            "当时只改了 `detect` 的档位、**没有重跑本工具**，13/16 是未经落盘的估计。"
            "668 重跑后真实值是 `error_subset.detect_rate_pct`（见本文件），"
            "逐样本变化见 `data/holdout/reveal_3_detail_668.json::changed_vs_previous_run`。"),
        "results": results,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # —— 668：逐样本明细 + 环境，落到 data/holdout/（同一次运行、同一个生成器）——
    opt_levels = list(getattr(rv, "OPT_LEVELS", ()))
    per_sample = [
        {"id": r["id"], "planted": r["planted"], "detector": r["detector"],
         "verdict": r["verdict"], "opts_seen": opts_from_note(r["note"]),
         "is_665_new": r["is_665_new"],
         "source": ("data/cards_665/fixtures" if r["is_665_new"] else "Examples/atoms"),
         "note": r["note"]}
        for r in results
    ]
    detail = {
        "schema": "queyi-holdout-reveal-detail/1",
        "generated_by": "tools/holdout_reveal_3_665.py",
        "generated_at": time.strftime("%Y-%m-%d"),
        "summary_for": "data/holdout_reveal_3_665.json",
        "caliber": rep["caliber"],
        "opt_levels": opt_levels,
        "denominator": rep["denominator"],
        "env": env,
        "per_sample": per_sample,
        "changed_vs_previous_run": [
            {"id": r["id"], "before": old_map.get(r["id"]), "after": r["verdict"],
             "planted": r["planted"], "detector": r["detector"]}
            for r in results
            if old_map and old_map.get(r["id"]) != r["verdict"]
        ],
        "note": ("`opts_seen` 是从 note 文本**解析**出来的派生量（不另存状态）。"
                 "本文件与主报告由**同一次运行**写出，两者不一致即为缺陷。"
                 "`changed_vs_previous_run` 说明'重跑改变了哪些判定'——"
                 "**变化本身不是能力提升**，是口径/测量配置变化的结果。"),
    }
    os.makedirs(os.path.dirname(DETAIL), exist_ok=True)
    with open(DETAIL, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(detail, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print(f"\n真错子集({err_total}): catch={err_catch} miss={err_miss} unknown={err_unknown} → 检出率={rate:.1f}%")
    print(f"对照子集({ctrl_total}): false_positive={ctrl_fp}；unknown 标签={unknown_label}")
    print(f"reveal_2 检出率={prev.get('detect_rate_pct')}% → reveal_3={rate:.1f}%")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    print(f"已写 {os.path.relpath(DETAIL, ROOT)}（逐样本 {len(per_sample)} 条 + 环境）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
