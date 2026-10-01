#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_reveal_4_671a.py — 671a C1：h31–h40 扩样的第 4 轮 reveal。

为什么要有它（而不是重跑 holdout_reveal_3_665.py）
=================================================
669d 把 10 条补充种子（h31–h40）并入 canonical `data/holdout/holdout.json`，但**没有重跑
reveal** —— 所以现在 `data/holdout_reveal_3_665.json` 的分母只覆盖并入前的种子。
若直接重跑 `holdout_reveal_3_665.py`，会有两个真问题：

  1. 它的 `PLAN` 里没有 h31–h40 ⇒ 这 10 条会被当成 `unknown`（"无本地检测器"），
     而它们**大多有本地检测器**（h31/h34=TSan、h32/h40=ASan、h33=UBSan、h36=compiler-warn）
     ⇒ 会把"没跑"错记成"检测不到"，重演 665 的静默掉分形态；
  2. 它会**覆写** `data/holdout/reveal_3_detail_668.json`（668 的逐样本留痕）——
     历史测量不该被新测量抹掉（665/668 两批都强调过这一点）。

所以本工具**另起一轮**（reveal 4）：判据仍只有一个版本——`holdout_reveal_661.detect`
（含 666 起的 `-O0`/`-O2` 双档 + `setarch -R` 关 ASLR）。新样本的复现计划**不手抄**，
直接从 `data/holdout/holdout_extension_669d.json` 的 `detector` + `atom_ref` 现推导。

口径（写进产物，谁引用数字都必须引用这两个字段）
================================================
* 真错分母 = `catch + miss`（可测）；`unknown`（检测器不可用）**不计入分母**；
  `planted is False` 的对照样本另算（catch ⇒ false_positive）。
* 每个样本连跑 `--runs` 次（默认 3），逐次结论必须一致才算 `reproducible=true`；
  不一致的样本会被**显式列出**（环境抖动的结论不进论文）。
* 历史轮次（h1–h30）的结论**复用** `data/holdout_reveal_3_665.json`（不重跑、不覆盖），
  累计口径里的每一行都标了 `source`（`reused_reveal_3` / `measured_671a`）。

输出
====
* `data/holdout_reveal_4_671a.json` —— 轮次报告（本轮 + 累计 + CP 95% CI）
* `data/holdout/reveal_3_detail_671a.json` —— 逐样本明细（受理单指定文件名；
  文件名沿用 `reveal_3_detail_668.json` 的"批次后缀"约定，`reveal_index` 字段写明是第 4 轮）

用法
====
    python tools/holdout_reveal_4_671a.py                 # 跑 h31–h40，连跑 3 次
    python tools/holdout_reveal_4_671a.py --samples h31-h35
    python tools/holdout_reveal_4_671a.py --runs 1 --no-write
    python tools/holdout_reveal_4_671a.py --selftest      # 只读自检（计划推导/解析/汇总）

已知限制（诚实登记）
====================
* h31–h40 是 669d 在 holdout **已 reveal 之后**并入的 ⇒ **不具备盲态**；
  本轮只用于**增大样本量**，不得据此 Claim 外部效度提升。
* 累计口径里的 h1–h30 是**复用**上一轮的落盘结论，本轮没有重测它们
  （判据未变 ⇒ 复用成立；判据一旦变，`tools/guard_rerun_671a.py` 会要求重跑）。
* WSL 不可用时 sanitizer 类会降级为 `unknown`（本工具**如实登记**，绝不编数字）——
  此时报告里的 `env.caliber_warning` 会写明"分母被环境压缩"，供引用者核对。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
HOLD = ROOT / "data" / "holdout" / "holdout.json"
EXT = ROOT / "data" / "holdout" / "holdout_extension_669d.json"
R3 = ROOT / "data" / "holdout_reveal_3_665.json"
OUT = ROOT / "data" / "holdout_reveal_4_671a.json"
#: 受理单指定文件名（见模块头「输出」；reveal_index 字段写明真实轮次 = 4）
DETAIL = ROOT / "data" / "holdout" / "reveal_3_detail_671a.json"
DEFAULT_SAMPLES = "h31-h40"
N_RUNS = 3

#: 669d 扩展文件里的 detector 字段 → rv661.detect 认的 kind（只做**归一**，不改判据）
KIND_ALIAS = {
    "-wunsequenced": "wunsequenced",
    "wunsequenced": "wunsequenced",
    "-": "unknown",
    "": "unknown",
    "perf-counter": "unknown",       # 本机无 perf 检测器 ⇒ 诚实记 unknown（661 同款）
}


# ─────────────────────────────────────────────────────────────────────────────
# 载入（惰性 importlib：与 665 同套路，避免模块级耦合）
# ─────────────────────────────────────────────────────────────────────────────

def load_rv661():
    spec = importlib.util.spec_from_file_location("rv661", HERE / "holdout_reveal_661.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_stat_bounds():
    spec = importlib.util.spec_from_file_location("stat_bounds", HERE / "stat_bounds.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# 样本选择与计划推导（纯函数，可单测）
# ─────────────────────────────────────────────────────────────────────────────

def split_range(part: str, all_ids: list[str]) -> tuple[str, str] | None:
    """把 `h31-h40` 拆成 (lo, hi)；不是范围（单个 id）⇒ None。

    为什么不能用 `partition("-")`：id 自身带 `-`（如 `d3e-01-d3e-20`），
    必须在**每个** `-` 位置试探、只接受两半都是已知 id 的那个切法。
    """
    if part in all_ids:
        return None
    for i, ch in enumerate(part):
        if ch != "-" or i == 0 or i == len(part) - 1:
            continue
        lo, hi = part[:i].strip(), part[i + 1:].strip()
        if lo in all_ids and hi in all_ids:
            return lo, hi
    raise SystemExit(f"--samples 无法解析（既不是已知 id，也不是「id-id」范围）：{part}")


def parse_samples(spec: str, all_ids: list[str]) -> list[str]:
    """解析 `--samples`：`all` / `h31-h40` / `h31,h32`。返回按 all_ids 顺序的 id 列表。

    非法范围**直接报错**（不静默返回空列表——"没选中样本"与"选了但没跑"必须能区分）。
    """
    spec = (spec or "").strip()
    if spec in ("", "all"):
        return list(all_ids)
    want: set[str] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        rng = split_range(part, all_ids)
        if rng is None:
            want.add(part)
            continue
        i, j = all_ids.index(rng[0]), all_ids.index(rng[1])
        if i > j:
            raise SystemExit(f"--samples 范围反序：{part}")
        want.update(all_ids[i:j + 1])
    return [s for s in all_ids if s in want]


def norm_kind(kind: str | None) -> str:
    k = str(kind or "").strip()
    return KIND_ALIAS.get(k.lower(), k)


def plan_from_extension(ext_seeds: list[dict]) -> dict[str, tuple[str, list[str]]]:
    """从 669d 扩展文件现推导 `{id: (kind, [夹具文件名])}`。

    刻意**不手抄** PLAN：669d 的 `detector`/`atom_ref` 是唯一事实源，
    手抄一份就会有两份计划，迟早分叉（665 的两条 honest_note 都在讲这个）。
    """
    plan: dict[str, tuple[str, list[str]]] = {}
    for s in ext_seeds:
        sid = str(s.get("id"))
        ref = str(s.get("atom_ref") or "")
        base = os.path.basename(ref.replace("\\", "/"))
        plan[sid] = (norm_kind(s.get("detector")), [base] if base else [])
    return plan


# ─────────────────────────────────────────────────────────────────────────────
# 测量
# ─────────────────────────────────────────────────────────────────────────────

def measure_once(rv, plan: dict[str, tuple[str, list[str]]], ids: list[str]) -> list[dict]:
    """跑一遍：逐样本 `rv661.detect`。返回逐样本行（不做统计口径）。"""
    rows: list[dict] = []
    for sid in ids:
        kind, files = plan.get(sid, ("unknown", []))
        verdict, note = rv.detect(kind, files)
        rows.append({"id": sid, "detector": kind, "files": files,
                     "verdict": verdict, "note": str(note)[:240]})
        print(f"  {sid:<4} {kind:<14} {verdict:<8} {str(note)[:64]}")
    return rows


def merge_runs(id_list: list[str], runs: list[list[dict]]) -> list[dict]:
    """把多次运行的结论合并：逐样本列出每轮 verdict + 是否可复现。"""
    by_id: dict[str, list[dict]] = {}
    for run in runs:
        for r in run:
            by_id.setdefault(r["id"], []).append(r)
    out: list[dict] = []
    for sid in id_list:
        rs = by_id.get(sid, [])
        vs = [r["verdict"] for r in rs]
        first = rs[0] if rs else {"detector": "unknown", "note": "未跑", "files": []}
        out.append({
            "id": sid, "detector": first["detector"], "files": first["files"],
            "verdict": vs[0] if vs else "unknown",
            "verdicts_per_run": vs,
            "reproducible": bool(vs) and len(set(vs)) == 1,
            "note": first["note"],
        })
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 统计口径
# ─────────────────────────────────────────────────────────────────────────────

def tally(rows: list[dict], labels: dict[str, bool | None]) -> dict[str, Any]:
    """按标签统计：error（planted true）/ control（false）/ unknown 标签。

    分母口径：可测真错 = catch + miss；unknown（检测器不可用）**不进分母**。
    """
    err_catch = err_miss = err_unknown = 0
    err_total = ctrl_total = ctrl_fp = 0
    label_unknown = 0
    for r in rows:
        lab = labels.get(r["id"])
        v = r["verdict"]
        if lab is True:
            err_total += 1
            if v == "catch":
                err_catch += 1
            elif v == "miss":
                err_miss += 1
            else:
                err_unknown += 1
        elif lab is False:
            ctrl_total += 1
            if v == "catch":
                ctrl_fp += 1
        else:
            label_unknown += 1
    denom = err_catch + err_miss
    return {
        "labels": {"error": err_total, "control": ctrl_total, "unknown": label_unknown},
        "error_subset": {"total": err_total, "catch": err_catch, "miss": err_miss,
                         "unknown": err_unknown,
                         "detect_rate_pct": round(err_catch / denom * 100, 1) if denom else None},
        "control_subset": {"total": ctrl_total, "false_positive": ctrl_fp},
        "denominator": {"value": denom, "meaning": "catch+miss（可测真错样本）",
                        "excluded": {"detector_unknown": err_unknown,
                                     "label_unknown": label_unknown}},
    }


def cp_interval(k: int, n: int, conf: float = 0.95) -> dict[str, Any]:
    """Clopper–Pearson 双侧区间（复用 tools/stat_bounds.py，不新造区间公式）。"""
    if n <= 0:
        return {"k": k, "n": n, "point": None, "cp_low": None, "cp_high": None,
                "conf": conf, "note": "n=0 ⇒ 拒绝给率（fail-loud，与 670a 同款）"}
    sb = load_stat_bounds()
    p = sb.proportion(k, n, conf)
    return {"k": k, "n": n, "point": p["point"], "cp_low": p["cp_low"],
            "cp_high": p["cp_high"], "conf": conf}


# ─────────────────────────────────────────────────────────────────────────────
# 环境探测（数字离开环境不可复算）
# ─────────────────────────────────────────────────────────────────────────────

def env_probe() -> dict[str, Any]:
    import shutil
    import subprocess
    import sys

    def run(cmd: list[str], timeout: int = 60) -> tuple[int, str]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()
        except Exception as e:  # noqa: BLE001
            return -1, f"EXC: {type(e).__name__}: {e}"

    rc, wsl_gpp = run(["wsl", "-e", "bash", "-lc", "g++ --version | head -1"])
    rc2, local_gpp = run(["g++", "--version"])
    rc3, local_clang = run(["clang++", "--version"])
    wsl_ok = rc == 0 and "g++" in wsl_gpp
    return {
        "wsl_available": wsl_ok,
        "wsl_gpp": (wsl_gpp.splitlines() or ["(不可用)"])[0],
        "local_gpp": (local_gpp.splitlines() or ["(不可用)"])[0],
        "local_clang": (local_clang.splitlines() or ["(不可用)"])[0],
        "host": sys.platform,
        "python": sys.version.split()[0],
        "local_gpp_present": shutil.which("g++") is not None,
        "caliber_warning": ("WSL 不可用 ⇒ sanitizer 类样本会降级为 unknown，可测分母被环境压缩"
                            "（这正是 669d env_dependency 要防的静默掉分形态）") if not wsl_ok else "",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────

def run(ids: list[str], runs_n: int, write: bool = True) -> dict[str, Any]:
    h = jload(HOLD)
    ext = jload(EXT)
    seeds: dict[str, dict] = {str(s["id"]): s for s in h["seeds"]}
    labels = {sid: s.get("planted") for sid, s in seeds.items()}
    plan = plan_from_extension(ext["seeds"])
    missing_plan = [i for i in ids if i not in plan]
    if missing_plan:
        raise SystemExit(f"这些样本在 669d 扩展文件里没有复现计划（拒绝猜）：{missing_plan}")

    env = env_probe()
    all_runs: list[list[dict]] = []
    for i in range(max(1, runs_n)):
        print(f"[run {i + 1}/{max(1, runs_n)}] 样本 {ids[0]}–{ids[-1]}（{len(ids)} 条）")
        all_runs.append(measure_once(load_rv661(), plan, ids))
    rows = merge_runs(ids, all_runs)

    # 历史轮次（h1–h30）：**复用**上一轮落盘结论，不重跑、不覆盖
    r3 = jload(R3) if R3.is_file() else {}
    r3_map = {str(x["id"]): x for x in r3.get("results", [])}
    historical_ids = [sid for sid in (str(s["id"]) for s in h["seeds"])
                      if sid not in set(ids) and sid in r3_map]
    hist_rows = [{"id": sid, "detector": r3_map[sid].get("detector", "unknown"),
                  "verdict": r3_map[sid].get("verdict", "unknown"),
                  "note": str(r3_map[sid].get("note", ""))[:240],
                  "files": [], "verdicts_per_run": [r3_map[sid].get("verdict")],
                  "reproducible": None, "source": "reused_reveal_3"}
                 for sid in historical_ids]
    for r in rows:
        r["source"] = "measured_671a"
    cand = rows + hist_rows
    cand_ids = ids + historical_ids

    round4 = tally(rows, labels)
    cumulative = tally(cand, labels)
    round4["cp95"] = cp_interval(round4["error_subset"]["catch"],
                                 round4["denominator"]["value"])
    cumulative["cp95"] = cp_interval(cumulative["error_subset"]["catch"],
                                     cumulative["denominator"]["value"])

    unstable = [r["id"] for r in rows if not r["reproducible"]]
    det_unknown_new = [r["id"] for r in rows if r["verdict"] == "unknown"
                       and labels.get(r["id"]) is True]

    r3_err = (r3.get("error_subset") or {})
    r3_den = (r3.get("denominator") or {}).get("value")
    rep: dict[str, Any] = {
        "schema": "queyi-holdout-reveal/v4",
        "reveal_index": 4,
        "generated_by": "tools/holdout_reveal_4_671a.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "round_label": f"{ids[0]}–{ids[-1]}（{len(ids)} 条，669d 扩样补充种子）",
        "runs": max(1, runs_n),
        "samples_requested": ids,
        "detector_reuse": ("复用 tools/holdout_reveal_661.py::detect（唯一判据；含 -O0/-O2 双档 + "
                           "setarch -R 关 ASLR）；新样本的 (detector, 夹具) 由 "
                           "data/holdout/holdout_extension_669d.json 现推导，不手抄"),
        "caliber": ("真错分母 = catch+miss（可测）；unknown（检测器不可用）与标签 unknown 均不进分母；"
                    "planted=False 的对照样本单列（catch ⇒ false_positive）"),
        "historical_reuse": {
            "from": str(R3.relative_to(ROOT).as_posix()),
            "ids": historical_ids,
            "why": "判据未变 ⇒ 历史结论可复用；本轮不重跑、不覆盖 reveal_3 的落盘（668 逐样本留痕必须保留）",
        },
        "env": env,
        "round4": round4,
        "cumulative": cumulative,
        "compare_reveal_3": {
            "before_denominator": r3_den,
            "before_catch": r3_err.get("catch"),
            "before_rate_pct": r3_err.get("detect_rate_pct"),
            "after_denominator": cumulative["denominator"]["value"],
            "after_catch": cumulative["error_subset"]["catch"],
            "after_rate_pct": cumulative["error_subset"]["detect_rate_pct"],
            "note": ("分母扩大 ⇒ 率的差异只说明**样本构成变了**，不说明验证器变好/变差；"
                     "两轮都把 unknown 留在分母之外。"),
        },
        "reproducibility": {"runs": max(1, runs_n), "unstable_samples": unstable,
                            "all_reproducible": not unstable},
        "new_sample_unknown": det_unknown_new,
        "honest_note": ("h31–h40 是 669d 在 holdout reveal **之后**并入的补充种子 ⇒ **不具备盲态**；"
                        "本轮只用于增大样本量，不得据此 Claim 外部效度提升。"
                        "累计口径里 h1–h30 复用 reveal_3 的落盘结论（本轮未重测）。"),
        "detail": DETAIL.relative_to(ROOT).as_posix(),
    }
    detail = {
        "schema": "queyi-holdout-reveal-detail/v2",
        "reveal_index": 4,
        "generated_by": "tools/holdout_reveal_4_671a.py",
        "generated_at": rep["generated_at"],
        "summary_for": OUT.relative_to(ROOT).as_posix(),
        "naming_note": ("文件名 `reveal_3_detail_671a.json` 沿用 671a 受理单的指定路径与 668 的"
                        "「批次后缀」命名约定；内容为**第 4 轮** reveal（h31–h40）"
                        "⇒ 以本文件的 `reveal_index` 字段为准，不覆盖 reveal_3_detail_668.json"),
        "samples_requested": ids,
        "runs": max(1, runs_n),
        "caliber": rep["caliber"],
        "env": env,
        "per_sample": [{**r, "is_669d_new": r["id"] in plan,
                        "planted": labels.get(r["id"])}
                       for r in cand],
        "round4_summary": round4,
        "cumulative_summary": cumulative,
        "unstable_samples": unstable,
        "note": ("`verdicts_per_run` 是每一轮的原始结论；`reproducible=false` 的样本说明结论随环境抖动，"
                 "引用前必须复核。`source` 标明该行是**本轮实测**还是**复用 reveal_3**。"),
    }

    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        DETAIL.parent.mkdir(parents=True, exist_ok=True)
        DETAIL.write_text(json.dumps(detail, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    return rep


def render(rep: dict[str, Any]) -> str:
    r4, cu = rep["round4"], rep["cumulative"]
    L = [f"[holdout reveal 4] {rep['round_label']}  连跑 {rep['runs']} 次  "
         f"WSL={'可用' if rep['env']['wsl_available'] else '不可用'}",
         f"  本轮  真错 {r4['error_subset']['total']}: catch={r4['error_subset']['catch']} "
         f"miss={r4['error_subset']['miss']} unknown={r4['error_subset']['unknown']} "
         f"⇒ 可测 {r4['denominator']['value']}，检出率={r4['error_subset']['detect_rate_pct']}%",
         f"  累计  真错 {cu['error_subset']['total']}: catch={cu['error_subset']['catch']} "
         f"miss={cu['error_subset']['miss']} unknown={cu['error_subset']['unknown']} "
         f"⇒ 可测 {cu['denominator']['value']}，检出率={cu['error_subset']['detect_rate_pct']}%",
         f"  对照  累计 fp={cu['control_subset']['false_positive']}/{cu['control_subset']['total']}",
         f"  CP95  可测口径 [{cu['cp95']['cp_low']:.4f}, {cu['cp95']['cp_high']:.4f}]"
         if cu["cp95"]["cp_low"] is not None else "  CP95  n=0（拒绝给率）"]
    if rep["reproducibility"]["unstable_samples"]:
        L.append(f"  [警告] 结论不稳的样本：{rep['reproducibility']['unstable_samples']}")
    if rep["env"]["caliber_warning"]:
        L.append(f"  [警告] {rep['env']['caliber_warning']}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    ids = ["h1", "h2", "h3", "h4", "h5"]
    chk("parse_samples 区间", parse_samples("h2-h4", ids) == ["h2", "h3", "h4"])
    chk("parse_samples 逗号", parse_samples("h1,h5", ids) == ["h1", "h5"])
    chk("parse_samples all", parse_samples("all", ids) == ids)
    chk("norm_kind 归一 -Wunsequenced/-", norm_kind("-Wunsequenced") == "wunsequenced"
        and norm_kind("-") == "unknown")
    ext = jload(EXT)
    plan = plan_from_extension(ext["seeds"])
    chk("扩展计划推导非空（10 条）", len(plan) == 10)
    chk("计划里每个 id 都有夹具名", all(v[1] for v in plan.values()))
    h = jload(HOLD)
    chk("扩展 id 都在 holdout.json 里",
        all(str(s["id"]) in {str(x["id"]) for x in h["seeds"]} for s in ext["seeds"]))
    t = tally([{"id": "a", "verdict": "catch"}, {"id": "b", "verdict": "miss"},
               {"id": "c", "verdict": "unknown"}, {"id": "d", "verdict": "catch"}],
              {"a": True, "b": True, "c": True, "d": False})
    chk("tally 分母 = catch+miss（unknown 不进）", t["denominator"]["value"] == 2)
    chk("tally 对照 catch 计 fp", t["control_subset"]["false_positive"] == 1)
    cpi = cp_interval(14, 16)
    chk("CP 区间调用 stat_bounds", 0.61 < cpi["cp_low"] < 0.63 and 0.98 < cpi["cp_high"] < 0.99)
    chk("n=0 拒绝给率", cp_interval(0, 0)["point"] is None)
    print(f"holdout_reveal_4_671a selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671a C1：h31–h40 扩样的第 4 轮 holdout reveal")
    ap.add_argument("--samples", default=DEFAULT_SAMPLES, help=f"默认 {DEFAULT_SAMPLES}")
    ap.add_argument("--runs", type=int, default=N_RUNS, help=f"连跑次数（默认 {N_RUNS}）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    h = jload(HOLD)
    all_ids = [str(s["id"]) for s in h["seeds"]]
    ids = parse_samples(a.samples, all_ids)
    rep = run(ids, a.runs, write=not a.no_write)
    print()
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    if not a.no_write:
        print(f"已写 {OUT.relative_to(ROOT).as_posix()}")
        print(f"已写 {DETAIL.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
