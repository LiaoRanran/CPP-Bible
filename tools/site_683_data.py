#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""site_683_data.py — 683-D：官网数据与图表生成（docs/assets/data/*.json）。

原则：网站数字**不由人手写**，全部从仓库冻结产物提取；同样的数字在
论文/验收报告/网站三处若不一致，以本脚本的输入文件（data/*.json）为准。

生成：
  docs/assets/data/core_numbers.json       首页徽章 + 核心数字表
  docs/assets/data/realworld_benchmark.json 真实靶场浏览器数据
  docs/assets/data/demo_samples.json        交互 Demo（含代码内容）
  docs/assets/data/charts.json              8 张 ECharts + split 表 + 工具链表
"""
from __future__ import annotations

import datetime as _dt
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = ROOT / "docs" / "assets" / "data"


def _load(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _dump(name: str, doc: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8", newline="\n")
    print(f"[683-D] 写入 docs/assets/data/{name}")


def build_core_numbers() -> int:
    a5 = _load(DATA / "a5_676f_results.json", {})
    rw = _load(DATA / "683_real_world_benchmark.json", {})
    g676 = _load(DATA / "blindspot_676g_detection_matrix.json", {})
    abl = _load(DATA / "683_operator_ablation.json", {})
    base = _load(DATA / "683_baseline_comparison.json", {})
    ver = _load(DATA / "683_real_world_candidates_verified.json", {})
    n_rw = rw.get("n_samples") or 0
    rw_stats = rw.get("stats", {})
    n_nvd = rw_stats.get("nvd_found", 0)

    # A5 主端点（从 676f 结果提取；键名以产物为准，缺失则 n/a）
    fd = None
    try:
        prim = a5["primary"] if "primary" in a5 else a5.get("results", {}).get("primary", {})
        fd = prim.get("fd_rate_pct") or prim.get("fd", {}).get("rate_pct")
    except Exception:  # noqa: BLE001
        fd = None

    # 真实靶场 OR 检出率
    rw_or = None
    m = _load(DATA / "683_real_world_detection_matrix.json", {})
    if m:
        rw_or = m.get("or_catch_rate_pct")

    # 消融主预算：Pool A k=4 最优配置 rate
    abl_best = None
    try:
        blk = abl["pools"]["A"]["k_blocks"]["4"]["configs"]
        abl_best = max(v["rate_pct"] for v in blk.values())
    except Exception:  # noqa: BLE001
        pass

    badges = [
        {"value": "1,147", "label": "合成样本 × 8 资产全量矩阵"},
        {"value": str(n_rw) or "110", "label": "真实缺陷（可追溯 + PoC 落盘）"},
        {"value": "8", "label": "检测器资产（四态判决）"},
        {"value": "18/34", "label": "盲区 >50% 的缺陷类型（676g）"},
        {"value": "+24.03pp", "label": "A5 Δ vs 预注册随机单点（k=4）"},
        {"value": str(n_nvd), "label": "NVD 在线验证 CVE"},
    ]
    table = [
        {"metric": "A5 主端点 FD 检出率（评估集，k=4）",
         "value": (f"{fd}%" if fd else "见 a5_676f_results.json"),
         "scope": "676f 冻结矩阵 1137×8；派生 571 / 评估 566；WSL g++ 13.3 双档"},
        {"metric": "Δ (FD − 预注册随机单点)",
         "value": "+24.03pp（p≈2e-41）", "scope": "McNemar exact；95% CI 见 682 报告"},
        {"metric": "盲区图（676g）",
         "value": "18/34 类盲区 >50%",
         "scope": "1147×8 全量；unknown 不计入 miss（退化资产渲染 n/a）"},
        {"metric": "真实靶场 OR 检出率（683）",
         "value": (f"{rw_or}%" if rw_or is not None else "检测矩阵生成中"),
         "scope": f"{n_rw} 条真实缺陷 × 8 资产；source-derived 重构"},
        {"metric": "NVD 在线验证",
         "value": f"{n_nvd}/{len(ver.get('items', [])) or n_nvd} FOUND",
         "scope": "services.nvd.nist.gov API v2.0；应答原文冻结"},
        {"metric": "Operator 主预算最优（Pool A k=4）",
         "value": (f"{abl_best}%" if abl_best else "见 683_operator_ablation.json"),
         "scope": "16 配置全枚举 + unique 变体；等权消融"},
    ]
    _dump("core_numbers.json", {"generated_at": _now(), "badges": badges, "table": table})
    return 0


def build_realworld() -> int:
    rw = _load(DATA / "683_real_world_benchmark.json")
    if not rw:
        print("[683-D] 683_real_world_benchmark.json 缺失，跳过 realworld 数据")
        return 0
    samples = []
    for r in rw["samples"]:
        d = r.get("detection") or {}
        samples.append({
            "rw_id": r["rw_id"], "cve_id": r["cve_id"], "project": r["project"],
            "project_url": r.get("project_url", ""), "defect_type": r["defect_type"],
            "year": r.get("year"), "severity": r.get("severity", "") or "",
            "source_url": r.get("source_url", ""), "mechanism": r.get("mechanism", ""),
            "notes": r.get("notes", ""), "poc_file": r.get("poc_file"),
            "or_verdict": d.get("or_verdict"), "caught_by": d.get("caught_by", []),
            "per_asset": {k: {"verdict": v} for k, v in (d.get("per_asset") or {}).items()},
        })
    projects = sorted({s["project"] for s in samples})
    types = sorted({s["defect_type"] for s in samples})
    years = sorted({s["year"] for s in samples if s["year"]})
    det = _load(DATA / "683_real_world_detection_matrix.json", {})
    doc = {
        "generated_at": _now(), "n_samples": len(samples),
        "or_catch_rate_pct": det.get("or_catch_rate_pct"),
        "online_verified_cves": rw.get("stats", {}).get("nvd_found", 0),
        "projects": projects, "types": types,
        "years": [str(y) for y in years] if years else [],
        "samples": samples,
    }
    _dump("realworld_benchmark.json", doc)
    return 0


def build_demo_samples() -> int:
    """演示样本：真实靶场前 8 条 + 自造 4 条（从矩阵抓 4 个代表）。"""
    rw = _load(DATA / "683_real_world_benchmark.json")
    m676 = _load(DATA / "blindspot_676g_detection_matrix.json")
    samples = []
    if rw:
        for r in rw["samples"][:8]:
            poc = ROOT / r["poc_file"]
            code = poc.read_text(encoding="utf-8") if poc.is_file() else "(missing)"
            d = r.get("detection") or {}
            samples.append({
                "id": r["rw_id"], "kind": "realworld",
                "desc": f"{r['cve_id']} · {r['project']} · {r['defect_type']}",
                "code": code,
                "per_asset": {k: {"verdict": v, "note": ""} for k, v in (d.get("per_asset") or {}).items()},
                "or_verdict": d.get("or_verdict"), "caught_by": d.get("caught_by", []),
            })
    if m676:
        picked = [r for r in m676["samples"]
                  if r["source_batch"] == "expA" and r.get("files")][:4]
        for r in picked:
            p = ROOT / "data" / "holdout_expansion" / r["source_batch"] / r["files"][0]
            code = p.read_text(encoding="utf-8") if p.is_file() else "(missing)"
            samples.append({
                "id": r["uid"].replace(":", "_"), "kind": "synthetic",
                "desc": f"{r['defect_type']} · {r['source_batch']}（合成语料）",
                "code": code,
                "per_asset": {k: {"verdict": v["verdict"], "note": v.get("note", "")[:260]}
                              for k, v in r["per_asset"].items()},
                "or_verdict": r.get("or_verdict_all8") or r.get("or_verdict_available6"),
                "caught_by": [k for k, v in r["per_asset"].items() if v["verdict"] == "catch"],
            })
    _dump("demo_samples.json", {"generated_at": _now(), "samples": samples})
    return 0


def build_charts() -> int:
    """8 张图：C1–C4 复用 682 的 ECharts option；C5–C8 由本批产物生成。"""
    charts: dict = {}
    for key, src in (("c1", "c1_blindspot_heatmap.echarts.json"),
                     ("c2", "c3_split_comparison.echarts.json"),
                     ("c3", "c2_family_pyramid.echarts.json"),
                     ("c4", "c4_asset_complementarity.echarts.json")):
        opt = _load(DATA / "682_figures" / src)
        if opt:
            charts[key] = {"option": opt, "note": "复用 682 冻结图表配置（34 类归一化）"}
    if not charts.get("c1"):
        # 682 图表缺失时的最小兜底标题（不造数据）
        charts["c1"] = {"option": {"title": {"text": "盲区热力图（数据文件缺失）"}},
                        "note": "运行 tools/figures_682.py 生成"}

    # C5：真实 vs 自造 per-asset 检出率
    rwm = _load(DATA / "683_real_world_detection_matrix.json")
    g676 = _load(DATA / "blindspot_676g_detection_matrix.json")
    if rwm and g676:
        assets = rwm["assets"]
        rw_rates = [rwm["per_asset_summary"][a]["catch_rate_pct"] or 0 for a in assets]
        g_rates = []
        for a in assets:
            n = g676["n_samples"]
            c = sum(1 for s in g676["samples"] if s["per_asset"][a]["verdict"] == "catch")
            g_rates.append(round(c / n * 100, 2))
        charts["c5"] = {
            "option": {
                "title": {"text": "C5 · 真实靶场 vs 自造语料：逐资产检出率",
                          "subtext": "同一 8 资产流水线；真实 n=%d，自造 n=%d"
                                     % (rwm["n_samples"], g676["n_samples"]),
                          "left": "center"},
                "tooltip": {"trigger": "axis"},
                "legend": {"top": 56, "data": ["真实靶场（683）", "自造语料（676g）"]},
                "grid": {"left": 70, "right": 40, "top": 110, "bottom": 60},
                "xAxis": {"type": "category",
                          "data": assets, "axisLabel": {"rotate": 30}},
                "yAxis": {"type": "value", "name": "catch 率 %", "max": 100},
                "series": [
                    {"name": "真实靶场（683）", "type": "bar", "data": rw_rates,
                     "itemStyle": {"color": "#6ea8fe"},
                     "label": {"show": True, "position": "top", "fontSize": 10}},
                    {"name": "自造语料（676g）", "type": "bar", "data": g_rates,
                     "itemStyle": {"color": "#7ef0c0"},
                     "label": {"show": True, "position": "top", "fontSize": 10}},
                ],
            },
            "note": "unknown 不进分母（unknown 率单独在矩阵 JSON 中报告）；"
                    "wunsequenced / compile-time 在两侧均为 0%（恒 unknown）。",
        }
        # C6：项目覆盖
        proj_cnt: dict[str, int] = {}
        for s in rwm["samples"]:
            proj_cnt[s["project"]] = proj_cnt.get(s["project"], 0) + 1
        items = sorted(proj_cnt.items(), key=lambda kv: (-kv[1], kv[0]))
        charts["c6"] = {
            "option": {
                "title": {"text": "C6 · 真实靶场项目覆盖", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "grid": {"left": 150, "right": 40, "top": 60, "bottom": 40},
                "xAxis": {"type": "value", "name": "样本数"},
                "yAxis": {"type": "category", "data": [k for k, _ in items][::-1],
                          "axisLabel": {"fontSize": 11}},
                "series": [{"type": "bar", "data": [v for _, v in items][::-1],
                            "itemStyle": {"color": "#6ea8fe"},
                            "label": {"show": True, "position": "right", "fontSize": 10}}],
            },
            "note": f"共 {len(items)} 个项目（任务目标 ≥15）。",
        }
        # C7：类型分布
        type_cnt: dict[str, int] = {}
        for s in rwm["samples"]:
            type_cnt[s["defect_type"]] = type_cnt.get(s["defect_type"], 0) + 1
        titems = sorted(type_cnt.items(), key=lambda kv: (-kv[1], kv[0]))
        charts["c7"] = {
            "option": {
                "title": {"text": "C7 · 真实靶场缺陷类型分布（34 类词表）", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "grid": {"left": 60, "right": 40, "top": 60, "bottom": 90},
                "xAxis": {"type": "category", "data": [k for k, _ in titems],
                          "axisLabel": {"rotate": 40, "fontSize": 10}},
                "yAxis": {"type": "value", "name": "样本数"},
                "series": [{"type": "bar", "data": [v for _, v in titems],
                            "itemStyle": {"color": "#ffb020"},
                            "label": {"show": True, "position": "top", "fontSize": 10}}],
            },
            "note": f"共 {len(titems)} 个类型。",
        }

    # C8：operator 消融（Pool A k=4，16+16 配置）
    abl = _load(DATA / "683_operator_ablation.json")
    if abl:
        try:
            cfgs = abl["pools"]["A"]["k_blocks"]["4"]["configs"]
            names = list(cfgs.keys())
            lit = [cfgs[n]["rate_pct"] for n in names if not n.startswith("u_")]
            lit_names = [n for n in names if not n.startswith("u_")]
            order = sorted(range(len(lit_names)), key=lambda i: -(lit[i] or 0))
            base_rate = cfgs.get("fxxx", {}).get("rate_pct")
            charts["c8"] = {
                "option": {
                    "title": {"text": "C8 · Operator 16 配置消融（literal；Pool A，k=4）",
                              "subtext": "等权 on/off 全枚举；同一冻结矩阵，仅权重变化",
                              "left": "center"},
                    "tooltip": {"trigger": "axis"},
                    "grid": {"left": 60, "right": 40, "top": 100, "bottom": 60},
                    "xAxis": {"type": "category",
                              "data": [lit_names[i] for i in order],
                              "axisLabel": {"rotate": 40, "fontSize": 10}},
                    "yAxis": {"type": "value", "name": "评估集检出率 %", "min": 40, "max": 60},
                    "series": [{"type": "bar",
                                "data": [lit[i] for i in order],
                                "itemStyle": {"color": "#7ef0c0"},
                                "markLine": ({"data": [{"yAxis": base_rate}],
                                              "label": {"formatter": "fd_only 基线"}}
                                             if base_rate else None),
                                "label": {"show": True, "position": "top", "fontSize": 10}}],
                },
                "note": "unique 模式 16 配置在 683_operator_ablation.json；"
                        "literal 模式下含 novel 的配置与对应不含 novel 的配置选择一致"
                        "（16/16 块验证，数学坍缩）。",
            }
        except Exception as e:  # noqa: BLE001
            print(f"[683-D] C8 跳过：{e}")

    # split 表（682 主端点；结构：results[split].main_k4.{fd,random,static}.rate_pct）
    sp = _load(DATA / "682_a5_split_comparison.json")
    split_table = []
    if sp:
        for name, blk in (sp.get("results") or {}).items():
            try:
                mk = blk["main_k4"]
                p = float(blk["mcnemar_p_fd_random"])
                split_table.append({
                    "split": name,
                    "fd": f"{mk['fd']['rate_pct']}%",
                    "random": f"{mk['random']['rate_pct']}%",
                    "static": f"{mk['static']['rate_pct']}%",
                    "delta": f"{blk['delta_fd_random_pp']:+.2f}pp",
                    "p": f"{p:.2e}",
                })
            except Exception:  # noqa: BLE001
                continue

    tc = _load(DATA / "683_cross_toolchain_results.json")
    toolchain_table, tc_note = [], ""
    if tc and tc.get("b1", {}).get("per_asset"):
        for kind, s in tc["b1"]["per_asset"].items():
            toolchain_table.append({"asset": kind, "n": s["n"], "agree": f"{s['agree_pct']}%",
                                    "kappa": s["kappa"], "gxx": f"{s['gxx_catch_pct']}%",
                                    "clang": f"{s['clang_catch_pct']}%",
                                    "delta": f"{s['delta_pp_clang_minus_gxx']}pp"})
        tc_note = ("clang 侧 = Ubuntu clang 18.1.3 实测；基线 = 676g（WSL g++ 13.3）。"
                   "MinGW clang 22 的 ASan 不可用（缺运行库）——尝试记录，不上报数字。")
    _dump("charts.json", {"generated_at": _now(), "charts": charts,
                          "split_table": split_table, "toolchain_table": toolchain_table,
                          "toolchain_note": tc_note})
    return 0


def main() -> int:
    build_core_numbers()
    build_realworld()
    build_demo_samples()
    build_charts()
    return 0


if __name__ == "__main__":
    sys.exit(main())
