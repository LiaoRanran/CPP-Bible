#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_692_fair_comparison.py — 692-B：公平外部对比（clang-tidy / cppcheck × A5 evaluation 566）。

协议先落盘
==========
口径、样本框架、超时、unknown 判据全部写在 ``data/692_fair_comparison_protocol.md``（**跑之前**）。
本脚本只做协议的执行 + 现算汇总，**不改口径**；任何判据变更必须先改协议文件。

定位（写死）
============
convergent validity / cross-regime stress-testing。**不是 leaderboard，不 claim superiority。**
Queyi 审计的是评估装置，不是另一个 verifier。

不跑 detect()
==============
本脚本只调用**外部工具**（clang-tidy / cppcheck），不触碰 Queyi 检测器，
也不写任何冻结矩阵（`data/a5_676f_detection_matrix.json` 只读）。

用法
====
    python tools/run_692_fair_comparison.py            # 真跑（可断点续跑），跑完自动汇总
    python tools/run_692_fair_comparison.py --analyze  # 只从 raw jsonl 汇总
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
RAW = ROOT / "data" / "692_fair_comparison_raw.jsonl"
OUT = ROOT / "data" / "692_fair_comparison_results.json"

CLANG_TIDY = Path(r"C:\msys64\mingw64\bin\clang-tidy.exe")
CPPCHECK = Path(r"C:\msys64\mingw64\bin\cppcheck.exe")

TIMEOUT_S = 60
CT_MAIN_CHECKS = "-*,clang-analyzer-*,bugprone-*,cert-*,cppcoreguidelines-*"
CPP_WARNING = "--enable=warning"
CPP_BROAD = "--enable=warning,performance,portability"

CT_DIAG = re.compile(r"^(?P<file>.+?):(?P<line>\d+):(?P<col>\d+): (?P<sev>warning|error|note): (?P<msg>.*?)(?: \[(?P<check>[^\]]+)\])?$")
CPP_DIAG = re.compile(r"^(?P<file>.+?):(?P<line>-?\d+):(?P<sev>[a-z]+):(?P<id>[a-zA-Z0-9_]+):(?P<msg>.*)$")
CT_FATAL = re.compile(r"(error: unable to handle compilation|error: (?:no such file|expected|unknown type name)|fatal error:)", re.IGNORECASE)
CPP_FATAL = re.compile(r"^(.*?):(\d+):(error|information):(syntaxError|missingIncludeSystem|internalError)", re.MULTILINE | re.IGNORECASE)


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell)


# --------------------------------------------------------------------------------------
# 帧
# --------------------------------------------------------------------------------------
def build_frame() -> list[dict[str, Any]]:
    d = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for s in d["samples"]:
        if s.get("split") != "evaluation":
            continue
        fp = s.get("file_path") or ""
        abs_path = ROOT / fp if fp and fp != "(inline_code)" else None
        rows.append({
            "uid": s["sample_id"],
            "sample_id": s["sample_id"],
            "source_batch": s.get("source_batch"),
            "dataset": s.get("dataset"),
            "defect_group": s.get("defect_group"),
            "defect_type": s.get("defect_type"),
            "expected_verdict": s.get("expected_verdict"),
            "planted": bool(s.get("planted", True)),
            "queiy_or_verdict": s.get("or_verdict"),
            "file_rel": fp,
            "file_abs": str(abs_path) if abs_path else None,
            "file_exists": bool(abs_path and abs_path.exists()),
            "layer": _layer_of(s),
        })
    rows.sort(key=lambda r: r["uid"])
    return rows


def _layer_of(s: dict[str, Any]) -> str:
    pa = s.get("per_asset", {})
    caught = [a for a in ("asan", "ubsan", "tsan") if _verdict(pa.get(a, "unknown")) == "catch"]
    if caught:
        return "sanitizer"
    if any(_verdict(pa.get(a, "unknown")) == "catch" for a in ("compiler-warn", "cross-compile", "linker")):
        return "static"
    return "none"


# --------------------------------------------------------------------------------------
# 工具调用
# --------------------------------------------------------------------------------------
def run_cmd(cmd: list[str]) -> tuple[int, str, float]:
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=str(ROOT), errors="replace")
        return p.returncode, (p.stdout or "") + (p.stderr or ""), time.time() - t0
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or "") if isinstance(e.stdout, str) else "") + ((e.stderr or "") if isinstance(e.stderr, str) else "")
        return -9, out + "\n[timeout]", time.time() - t0


def call_clang_tidy(path: str) -> dict[str, Any]:
    rc, raw, secs = run_cmd([str(CLANG_TIDY), path, "--checks=" + CT_MAIN_CHECKS, "--", "-std=c++17", "-fsyntax-only"])
    diags = []
    for line in raw.splitlines():
        m = CT_DIAG.match(line.strip())
        if m and m.group("sev") in ("warning", "error"):
            diags.append({
                "line": int(m.group("line")),
                "severity": m.group("sev"),
                "check": m.group("check") or "",
                "msg": m.group("msg")[:200],
            })
    fatal = bool(CT_FATAL.search(raw))
    status = "ok" if (rc >= 0 and not fatal) else ("timeout" if rc == -9 else "compile_error")
    return {"rc": rc, "seconds": round(secs, 3), "status": status, "diags": diags, "raw_head": raw[:8000]}


def call_cppcheck(path: str, enable: str) -> dict[str, Any]:
    tmpl = "{file}:{line}:{severity}:{id}:{message}"
    rc, raw, secs = run_cmd([str(CPPCHECK), enable, "--std=c++17", "--quiet", "--template=" + tmpl, path])
    diags = []
    for line in raw.splitlines():
        m = CPP_DIAG.match(line.strip())
        if m:
            diags.append({
                "line": int(m.group("line")),
                "severity": m.group("sev"),
                "id": m.group("id"),
                "msg": m.group("msg")[:200],
            })
    fatal = bool(CPP_FATAL.search(raw))
    status = "ok" if (rc >= 0 and not fatal) else ("timeout" if rc == -9 else "tool_error")
    return {"rc": rc, "seconds": round(secs, 3), "status": status, "diags": diags, "raw_head": raw[:8000]}


# --------------------------------------------------------------------------------------
# 跑（断点续跑）
# --------------------------------------------------------------------------------------
def done_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    if RAW.exists():
        for line in RAW.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            keys.add((str(r["uid"]), str(r["tool"])))
    return keys


def do_run(limit: int | None) -> int:
    frame = build_frame()
    have = done_keys()
    todo = [r for r in frame if (r["uid"], "clang-tidy") not in have or (r["uid"], "cppcheck") not in have]
    if limit:
        todo = todo[:limit]
    print(f"frame={len(frame)} done_pairs={len(have)} todo_samples={len(todo)}", flush=True)
    with RAW.open("a", encoding="utf-8") as fh:
        for i, r in enumerate(todo, 1):
            for tool in ("clang-tidy", "cppcheck"):
                if (r["uid"], tool) in have:
                    continue
                if not r["file_exists"]:
                    rec = {"uid": r["uid"], "tool": tool, "status": "no_source", "rc": None, "seconds": 0.0,
                           "diags": [], "raw_head": "", "file_rel": r["file_rel"]}
                elif tool == "clang-tidy":
                    rec = {"uid": r["uid"], "tool": tool, **call_clang_tidy(str(r["file_abs"])), "file_rel": r["file_rel"]}
                else:
                    rec = {"uid": r["uid"], "tool": tool, **call_cppcheck(str(r["file_abs"]), CPP_BROAD), "file_rel": r["file_rel"],
                           "enable": CPP_BROAD}
                rec["ts"] = _dt.datetime.now().astimezone().isoformat(timespec="seconds")
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
            if i % 25 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
    return 0


# --------------------------------------------------------------------------------------
# 汇总
# --------------------------------------------------------------------------------------
CALIBERS: tuple[tuple[str, str], ...] = (
    ("T1_clang_tidy_C_main", "clang-tidy 预注册主口径（analyzer+bugprone+cert+cppcoreguidelines）"),
    ("T2_clang_tidy_C_A", "clang-tidy 探索口径（仅 clang-analyzer-*；673e 事后口径，本批先声明）"),
    ("T3_cppcheck_warning", "cppcheck severity ∈ {error, warning}"),
    ("T4_cppcheck_broad", "cppcheck warning+performance+portability（全量诊断）"),
)


def reports_for(caliber: str, rec: dict[str, Any]) -> bool | None:
    """该记录在该口径下是否「有报告」。``None`` = 不可判定（unknown）。"""
    if rec["status"] in ("no_source", "timeout", "compile_error", "tool_error"):
        return None
    diags = rec["diags"]
    if caliber.startswith("T1"):
        return len(diags) > 0
    if caliber.startswith("T2"):
        return any(str(d.get("check", "")).startswith("clang-analyzer-") for d in diags)
    if caliber.startswith("T3"):
        return any(str(d.get("severity")) in ("error", "warning") for d in diags)
    return len(diags) > 0


def _triple(catch: int, miss: int, unknown: int) -> dict[str, Any]:
    """声明正例层（stratum）的三组件。分母 = 该层的全部样本（含 unknown）——不跨层合并。"""
    denom = catch + miss
    total = catch + miss + unknown
    return {
        "catch": catch, "miss": miss, "unknown": unknown, "total": total,
        "catch_rate_pct": round(catch / total * 100, 4) if total else None,
        "unknown_rate_pct": round(unknown / total * 100, 4) if total else None,
        "conditional_recall_pct": round(catch / denom * 100, 4) if denom else None,
    }


def analyze() -> int:
    frame = build_frame()
    n_pos = sum(1 for r in frame if r["expected_verdict"] == "catch")
    n_neg = len(frame) - n_pos
    raw: dict[tuple[str, str], dict[str, Any]] = {}
    for line in RAW.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        raw[(r["uid"], r["tool"])] = r

    out: dict[str, Any] = {
        "schema": "queyi-692/fair-comparison/v1",
        "generated_by": "tools/run_692_fair_comparison.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "protocol": "data/692_fair_comparison_protocol.md",
        "frame": {
            "source": "data/a5_676f_detection_matrix.json split=evaluation",
            "n": len(frame),
            "n_with_source": sum(1 for r in frame if r["file_exists"]),
            "n_no_source": sum(1 for r in frame if not r["file_exists"]),
            "expected_catch": n_pos,
            "expected_miss": n_neg,
            "planted_false": sum(1 for r in frame if not r["planted"]),
            "declared_negatives_composition": {
                "planted_true_outside_declared_region": sum(
                    1 for r in frame if r["expected_verdict"] == "miss" and r["planted"]),
                "planted_false_controls": sum(
                    1 for r in frame if r["expected_verdict"] == "miss" and not r["planted"]),
                "note": "declared_negatives 不是「干净样本」：多数是落在参考协议声称可检出区之外的植入缺陷 "
                        "⇒ 该层上的 false_report_rate 是能力分歧率，FP 只能读 planted=false 层。",
            },
        },
        "tools": {
            "clang-tidy": {"binary": str(CLANG_TIDY), "checks_T1": CT_MAIN_CHECKS},
            "cppcheck": {"binary": str(CPPCHECK), "enable_T4": CPP_BROAD, "enable_T3": CPP_WARNING},
        },
        "calibers": {},
        "queiy_reference": {},
        "cross_disagreement": {},
        "honest_limits": [
            "clang-tidy 与 cppcheck 虽同在本机 Windows native 运行，但不是同一编译环境（cppcheck 无编译期）；与 Queyi 的 WSL+sanitizer 检测环境本质不同（静态 vs 动态）⇒ 非容器化同环境。",
            "truth labels = 冻结矩阵 expected_verdict（声明可检出性），非人审真值；人类 IAA 仍为 0。",
            "外部工具无 unknown 概念：其「无报告」在真错样本上记 miss（已知不对称）。",
            "T2 为 673e 的事后口径，本批在跑之前声明，不洗成预注册。",
        ],
    }

    for caliber, desc in CALIBERS:
        tool = "clang-tidy" if caliber.startswith("T") and "clang" in caliber else "cppcheck"
        pos_catch = pos_miss = pos_unknown = 0
        neg_report = neg_silent = neg_unknown = 0
        ctrl_report = ctrl_silent = ctrl_unknown = 0
        pristine_report = pristine_silent = pristine_unknown = 0
        per_group: dict[str, dict[str, int]] = {}
        unknown_samples: list[str] = []
        for r in frame:
            rec = raw.get((r["uid"], tool))
            rep = reports_for(caliber, rec) if rec else None
            g = str(r["defect_group"])
            per_group.setdefault(g, {"catch": 0, "miss": 0, "unknown": 0})
            # 控制层（planted == false）：唯一能读作「无缺陷样本上仍报」的层
            if not r["planted"]:
                if rep is None:
                    ctrl_unknown += 1
                elif rep:
                    ctrl_report += 1
                else:
                    ctrl_silent += 1
                # 最干净的一层：既未植入、参考也不期望检出（=论文口径的 FPR 控制样本）
                if r["expected_verdict"] == "miss":
                    if rep is None:
                        pristine_unknown += 1
                    elif rep:
                        pristine_report += 1
                    else:
                        pristine_silent += 1
            if rep is None:
                if r["file_exists"]:
                    unknown_samples.append(r["uid"])
                if r["expected_verdict"] == "catch":
                    pos_unknown += 1
                    per_group[g]["unknown"] += 1
                else:
                    neg_unknown += 1
                continue
            if r["expected_verdict"] == "catch":
                if rep:
                    pos_catch += 1
                    per_group[g]["catch"] += 1
                else:
                    pos_miss += 1
                    per_group[g]["miss"] += 1
            else:
                if rep:
                    neg_report += 1
                else:
                    neg_silent += 1
        frame_unknown = pos_unknown + neg_unknown
        out["calibers"][caliber] = {
            "tool": tool,
            "description": desc,
            "strata": {"declared_positives": n_pos, "declared_negatives": n_neg},
            "three_components_on_declared_positives": _triple(pos_catch, pos_miss, pos_unknown),
            "false_report": {"reported_on_expected_miss": neg_report, "silent_on_expected_miss": neg_silent,
                             "unknown_on_expected_miss": neg_unknown,
                             "false_report_rate_pct": round(neg_report / (neg_report + neg_silent) * 100, 4)
                             if (neg_report + neg_silent) else None},
            "control_stratum_planted_false": {
                "n": ctrl_report + ctrl_silent + ctrl_unknown,
                "reported": ctrl_report, "silent": ctrl_silent, "unknown": ctrl_unknown,
                "report_rate_pct": round(ctrl_report / (ctrl_report + ctrl_silent) * 100, 4)
                if (ctrl_report + ctrl_silent) else None,
                "note": "planted=false 的样本（真正「未植入缺陷」的对照）上仍出报告的比例；"
                        "这是本帧唯一可读作 FP 的量。declared_negatives 层含 232 条 planted=true "
                        "但落在参考协议声称可检出区之外的样本 ⇒ 该层的 false_report_rate 只能读作"
                        "「能力分歧率」，不能读作误报率。",
            },
            "pristine_negative_stratum": {
                "n": pristine_report + pristine_silent + pristine_unknown,
                "reported": pristine_report, "silent": pristine_silent, "unknown": pristine_unknown,
                "report_rate_pct": round(pristine_report / (pristine_report + pristine_silent) * 100, 4)
                if (pristine_report + pristine_silent) else None,
                "note": "planted=false 且 expected=miss：既未植入缺陷、参考也不期望检出 ⇒ 这是本帧唯一的"
                        "「干净对照」层，其 report_rate 才可读作 FP 率。",
            },
            "frame_coverage_pct": round((len(frame) - frame_unknown) / len(frame) * 100, 4) if frame else None,
            "frame_unknown": frame_unknown,
            "per_defect_group": {k: v for k, v in sorted(per_group.items())},
            "unknown_samples": unknown_samples,
            "zero_discrimination_flag": (neg_report / (neg_report + neg_silent) >= 0.95)
            if (neg_report + neg_silent) else None,
        }

    # Queyi 参照（同一样本集，冻结矩阵 or_verdict）
    q_catch = sum(1 for r in frame if r["queiy_or_verdict"] == "catch" and r["expected_verdict"] == "catch")
    q_miss = sum(1 for r in frame if r["queiy_or_verdict"] == "miss" and r["expected_verdict"] == "catch")
    q_unk = sum(1 for r in frame if r["queiy_or_verdict"] == "unknown" and r["expected_verdict"] == "catch")
    q_fp = sum(1 for r in frame if r["queiy_or_verdict"] == "catch" and r["expected_verdict"] == "miss")
    q_tn = sum(1 for r in frame if r["queiy_or_verdict"] != "catch" and r["expected_verdict"] == "miss")
    q_unk_neg = sum(1 for r in frame if r["queiy_or_verdict"] == "unknown" and r["expected_verdict"] == "miss")
    q_triple = _triple(q_catch, q_miss, q_unk)
    q_triple["frame_coverage_pct"] = round((len(frame) - q_unk - q_unk_neg) / len(frame) * 100, 4) if frame else None
    q_ctrl = [r for r in frame if not r["planted"]]
    q_ctrl_rep = sum(1 for r in q_ctrl if r["queiy_or_verdict"] == "catch")
    q_ctrl_val = sum(1 for r in q_ctrl if r["queiy_or_verdict"] in ("catch", "miss"))
    q_pris = [r for r in q_ctrl if r["expected_verdict"] == "miss"]
    q_pris_rep = sum(1 for r in q_pris if r["queiy_or_verdict"] == "catch")
    q_pris_val = sum(1 for r in q_pris if r["queiy_or_verdict"] in ("catch", "miss"))
    out["queiy_reference"] = {
        "verdict_source": "a5_676f_detection_matrix.or_verdict（8 资产 OR，WSL/g++13.3 + native 3 资产混合环境）",
        "strata": {"declared_positives": n_pos, "declared_negatives": n_neg},
        "three_components_on_declared_positives": q_triple,
        "false_report": {"reported_on_expected_miss": q_fp, "silent_on_expected_miss": q_tn,
                         "unknown_on_expected_miss": q_unk_neg,
                         "false_report_rate_pct": round(q_fp / (q_fp + q_tn) * 100, 4) if (q_fp + q_tn) else None},
        "control_stratum_planted_false": {
            "n": len(q_ctrl), "reported": q_ctrl_rep, "silent": q_ctrl_val - q_ctrl_rep,
            "report_rate_pct": round(q_ctrl_rep / q_ctrl_val * 100, 4) if q_ctrl_val else None,
        },
        "pristine_negative_stratum": {
            "n": len(q_pris), "reported": q_pris_rep, "silent": q_pris_val - q_pris_rep,
            "report_rate_pct": round(q_pris_rep / q_pris_val * 100, 4) if q_pris_val else None,
        },
        "note": "Queyi 侧 8 资产池跨两个 OS（3 sanitizer 在 WSL）；环境感知口径见 data/692_environment_paired_experiment.json。",
    }

    # 交叉分歧（以 T1 与 T4 为主口径对，另附全部口径）
    for caliber, _ in CALIBERS:
        tool = "clang-tidy" if "clang" in caliber else "cppcheck"
        pairs = {"queyi_yes_tool_yes": 0, "queyi_yes_tool_no": 0, "queyi_no_tool_yes": 0, "queyi_no_tool_no": 0}
        qy_tool_no: list[dict[str, Any]] = []
        qn_tool_yes: list[dict[str, Any]] = []
        for r in frame:
            rec = raw.get((r["uid"], tool))
            rep = reports_for(caliber, rec) if rec else None
            if rep is None:
                continue
            qy = r["queiy_or_verdict"] == "catch"
            key = f"queyi_{'yes' if qy else 'no'}_tool_{'yes' if rep else 'no'}"
            pairs[key] += 1
            if qy and not rep:
                qy_tool_no.append({"uid": r["uid"], "defect_group": r["defect_group"], "layer": r["layer"],
                                   "expected": r["expected_verdict"]})
            if rep and not qy:
                qn_tool_yes.append({"uid": r["uid"], "defect_group": r["defect_group"], "layer": r["layer"],
                                    "expected": r["expected_verdict"]})
        def _gcount(rows: list[dict[str, Any]]) -> dict[str, int]:
            o: dict[str, int] = {}
            for x in rows:
                o[str(x["defect_group"])] = o.get(str(x["defect_group"]), 0) + 1
            return dict(sorted(o.items(), key=lambda kv: (-kv[1], kv[0])))
        out["cross_disagreement"][caliber] = {
            "pairs": pairs,
            "queyi_catch_tool_silent": {"n": len(qy_tool_no), "by_group": _gcount(qy_tool_no)},
            "tool_report_queyi_no_catch": {"n": len(qn_tool_yes), "by_group": _gcount(qn_tool_yes)},
        }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for caliber, _ in CALIBERS:
        c = out["calibers"][caliber]
        t = c["three_components_on_declared_positives"]
        print(f"{caliber:26s} catch={t['catch']:4d} miss={t['miss']:4d} unk={t['unknown']:4d} "
              f"recall={t['conditional_recall_pct']} fp_rate={c['false_report']['false_report_rate_pct']} "
              f"frame_cov={c['frame_coverage_pct']}")
    qr = out["queiy_reference"]
    print(f"{'Queyi_OR_reference':26s} catch={qr['three_components_on_declared_positives']['catch']:4d} "
          f"miss={qr['three_components_on_declared_positives']['miss']:4d} "
          f"unk={qr['three_components_on_declared_positives']['unknown']:4d} "
          f"recall={qr['three_components_on_declared_positives']['conditional_recall_pct']} "
          f"fp_rate={qr['false_report']['false_report_rate_pct']} "
          f"frame_cov={qr['three_components_on_declared_positives']['frame_coverage_pct']}")
    print("wrote", OUT)
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyze", action="store_true", help="只汇总，不跑工具")
    ap.add_argument("--limit", type=int, default=None, help="本次最多跑多少样本（调试用）")
    a = ap.parse_args(argv)
    if a.analyze:
        return analyze()
    do_run(a.limit)
    return analyze()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
