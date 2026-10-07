#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""figures_682.py — 682 · 任务C：图表更新（基于 681 修复后的 34 类归一化数据）。

数据源（全部只读）：
  data/blindspot_676g_detection_matrix.json   1147×8 判定矩阵（681 修复后）
  data/681_type_stats_normalized.json         34 类归一化统计（family8 聚合）
  data/682_a5_split_comparison.json           B1 四 split 主端点
  data/682_asset_ablation.json                B3 资产消融（Shapley/LOO/unique）

四张图（每张同时产出 ECharts option JSON + PNG）：
  C1 blindspot_heatmap      34 类 × 8 资产 检出率热力图（高盲区 >50% 标注）
  C2 family_pyramid         8 家族盲区率横向条形（从低到高）
  C3 split_comparison       4 split × 3 方法 分组柱状（含 95%CI 与 Δ 标注）
  C4 asset_complementarity  8 资产 Shapley 边际贡献 + 独占 catch + 退化标注

产物目录：data/682_figures/（4 个 .echarts.json + 4 个 .png + INDEX.md）
红线：不改检测器/样本/既有产物；本脚本只读数据、只写 682_figures/。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "682_figures"
MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
TYPE_STATS = ROOT / "data" / "681_type_stats_normalized.json"
SPLIT_CMP = ROOT / "data" / "682_a5_split_comparison.json"
ABLATION = ROOT / "data" / "682_asset_ablation.json"

ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker",
          "wunsequenced", "compile-time"]
DEGEN = {"wunsequenced", "compile-time"}
FAMILY_ORDER = ["memory", "bounds", "integer", "alias_type", "concurrency", "stl",
                "language_oop", "embedded_link"]
BG = "#ffffff"
FG = "#222222"
HI = "#c0392b"


def _jload(p: Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _jwrite(p: Path, doc) -> None:
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")


# ─────────────────────────────────────────────────────────────────────────────
# 数据准备
# ─────────────────────────────────────────────────────────────────────────────
def per_type_asset_matrix() -> dict:
    mx = _jload(MATRIX)
    samples = mx["samples"]
    types = sorted({s["defect_type"] for s in samples})
    counts = {t: {a: {"n": 0, "catch": 0, "unknown": 0} for a in ASSETS} for t in types}
    for s in samples:
        t = s["defect_type"]
        for a in ASSETS:
            c = counts[t][a]
            c["n"] += 1
            v = s["per_asset"].get(a, {}).get("verdict", "unknown")
            if v == "catch":
                c["catch"] += 1
            elif v == "unknown":
                c["unknown"] += 1
    return {"types": types, "counts": counts, "n_samples": len(samples)}


def family_rows() -> list[dict]:
    ts = _jload(TYPE_STATS)
    fam = ts["family8"]
    rows = [{"family": k, "n": v["n"], "blind": v["blind"], "blind_pct": v["blind_pct"]}
            for k, v in fam.items()]
    rows.sort(key=lambda r: r["blind_pct"])
    return rows


def split_rows() -> list[dict]:
    d = _jload(SPLIT_CMP)["results"]
    order = ["original", "family_random", "family_stratified", "strict_stratified"]
    out = []
    for name in order:
        r = d[name]
        m = r["main_k4"]
        out.append({
            "split": name, "n_evaluation": r["n_evaluation"],
            "fd": m["fd"]["rate_pct"], "random": m["random"]["rate_pct"],
            "static": m["static"]["rate_pct"],
            "random_mean": r["random_mean_rate_pct"],
            "delta_pp": r["delta_fd_random_pp"],
            "delta_ci95_pp": r["delta_fd_random_ci95_pp"],
            "delta_vs_mean_pp": r["delta_fd_random_mean_pp"],
            "mcnemar_p": r["mcnemar_p_fd_random"],
            "fd_assets": m["fd"]["assets"],
        })
    return out


def asset_rows() -> list[dict]:
    ab = _jload(ABLATION)
    sh = ab["shapley"]["original"]
    rows = []
    for a in ASSETS:
        rows.append({
            "asset": a,
            "shapley_pp": sh.get(a, 0.0),
            "loo_delta_pp": ab["leave_one_out"][a]["delta_vs_full_pp"],
            "eval_catch": ab["eval_catch_count"][a],
            "unique_catch": ab["unique_catch_count"][a],
            "degenerate": a in DEGEN,
        })
    rows.sort(key=lambda r: -r["shapley_pp"])
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# C1 热力图
# ─────────────────────────────────────────────────────────────────────────────
def fig_c1() -> dict:
    pm = per_type_asset_matrix()
    ts = _jload(TYPE_STATS)["per_type"]
    types = sorted(pm["types"], key=lambda t: (-ts[t]["blind_pct"], t))
    counts = pm["counts"]
    data = []
    for yi, t in enumerate(types):
        n = counts[t][ASSETS[0]]["n"]
        for xi, a in enumerate(ASSETS):
            if a in DEGEN:
                # 恒 unknown 资产：值填 null（不渲染颜色）。**不得画成 0%（那等于把
                # unknown 当 miss）**——项目口径：unknown 绝不当 miss。
                data.append([xi, yi, None])
                continue
            catch = counts[t][a]["catch"]
            data.append([xi, yi, round(100.0 * catch / n, 2)])
    gt50 = [t for t in types if ts[t]["blind_pct"] > 50.0]
    markup = [{"type": t, "row": types.index(t), "blind_pct": ts[t]["blind_pct"]}
              for t in gt50]
    opt = {
        "title": {
            "text": "C1 · Detection rate by defect type × asset (34 normalized types, n=1147)",
            "subtext": ("681-fixed 34-type canon; value = catch rate (%). Two rightmost columns "
                        "are blank by construction: constant-unknown assets (no local detector) — "
                        "unknown is NOT drawn as 0%/miss. 13 types with >50% blind are marked."),
            "left": "center", "textStyle": {"color": FG},
        },
        "tooltip": {"position": "top", "formatter": "type #{b} × asset {a}: {c}%"},
        "grid": {"left": 150, "right": 90, "top": 80, "bottom": 60},
        "xAxis": {"type": "category", "data": ASSETS, "axisLabel": {"rotate": 30, "color": FG}},
        "yAxis": {"type": "category", "data": types, "axisLabel": {"color": FG}},
        "visualMap": {"min": 0, "max": 100, "calculable": True, "orient": "vertical",
                      "right": 10, "top": "middle", "inRange": {"color": ["#c0392b", "#f6e58d", "#27ae60"]}},
        "series": [{"name": "catch rate (%)", "type": "heatmap", "data": data,
                    "label": {"show": False}, "emphasis": {"itemStyle": {"shadowBlur": 6}}}],
        "queyi:meta": {
            "n_samples": pm["n_samples"], "n_types": len(types), "assets": ASSETS,
            "constant_unknown_assets": sorted(DEGEN),
            "gt50_blind_types": markup,
            "source": "data/blindspot_676g_detection_matrix.json + data/681_type_stats_normalized.json",
            "generated_by": "tools/figures_682.py",
            "note": "热力图列顺序固定 ASSETS；退化两列整列 0（结构恒 unknown，不是检测失败）。",
        },
    }
    _jwrite(OUT / "c1_blindspot_heatmap.echarts.json", opt)
    _png_heatmap(OUT / "c1_blindspot_heatmap.png", types, counts, ts)
    return opt


# ─────────────────────────────────────────────────────────────────────────────
# C2 家族金字塔
# ─────────────────────────────────────────────────────────────────────────────
def fig_c2() -> dict:
    rows = family_rows()
    opt = {
        "title": {"text": "C2 · Blind-spot rate by family (8 families, n=1147)",
                  "subtext": "681-fixed aggregates; horizontal bars sorted low → high",
                  "left": "center", "textStyle": {"color": FG}},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "grid": {"left": 130, "right": 80, "top": 70, "bottom": 40},
        "xAxis": {"type": "value", "max": 80, "name": "blind rate (%)", "axisLabel": {"color": FG}},
        "yAxis": {"type": "category", "data": [r["family"] for r in rows],
                  "axisLabel": {"color": FG}},
        "series": [{
            "name": "blind rate (%)", "type": "bar",
            "data": [{"value": r["blind_pct"],
                      "itemStyle": {"color": HI if r["blind_pct"] > 50 else "#2e86de"}}
                     for r in rows],
            "label": {"show": True, "position": "right",
                      "formatter": "{b}", "color": FG},
            "barWidth": 22,
        }],
        "queyi:meta": {"rows": rows,
                       "source": "data/681_type_stats_normalized.json#family8",
                       "generated_by": "tools/figures_682.py",
                       "note": "家族名取自 681 归一化数据（memory/bounds/integer/alias_type/"
                               "concurrency/stl/language_oop/embedded_link）；>50% 标红。"},
    }
    _jwrite(OUT / "c2_family_pyramid.echarts.json", opt)
    _png_family(OUT / "c2_family_pyramid.png", rows)
    return opt


# ─────────────────────────────────────────────────────────────────────────────
# C3 多 split 对比
# ─────────────────────────────────────────────────────────────────────────────
def fig_c3() -> dict:
    rows = split_rows()
    cats = [r["split"] for r in rows]
    opt = {
        "title": {"text": "C3 · A5 main endpoint across four splits (k=4, FD vs Random vs Static)",
                  "subtext": ("same detection matrix (676f, 1137×8); only the data split changes. "
                              "Δ = FD − pre-registered single-point Random; CI on Δ shown in tooltip."),
                  "left": "center", "textStyle": {"color": FG}},
        "tooltip": {"trigger": "axis",
                    "formatter": "{b}<br/>FD {c0}% / Random {c1}% / Static {c2}%"},
        "legend": {"top": 52, "data": ["FD (failure-driven)", "Random (pre-registered seed)",
                                        "Static baseline"]},
        "grid": {"left": 60, "right": 40, "top": 110, "bottom": 60},
        "xAxis": {"type": "category", "data": cats, "axisLabel": {"color": FG, "rotate": 12}},
        "yAxis": {"type": "value", "max": 70, "name": "detection rate (%)", "axisLabel": {"color": FG}},
        "series": [
            {"name": "FD (failure-driven)", "type": "bar", "barGap": "10%",
             "data": [r["fd"] for r in rows], "itemStyle": {"color": "#27ae60"},
             "label": {"show": True, "position": "top", "formatter": "{c}%"}},
            {"name": "Random (pre-registered seed)", "type": "bar",
             "data": [r["random"] for r in rows], "itemStyle": {"color": "#2e86de"},
             "label": {"show": True, "position": "top", "formatter": "{c}%"}},
            {"name": "Static baseline", "type": "bar",
             "data": [r["static"] for r in rows], "itemStyle": {"color": "#95a5a6"},
             "label": {"show": True, "position": "top", "formatter": "{c}%"}},
        ],
        "queyi:meta": {
            "rows": rows,
            "error_bars": "ECharts 无内置误差棒；Δ 的 95%CI 与 McNemar p 见下表（queyi:table）",
            "table": [{"split": r["split"], "delta_pp": r["delta_pp"],
                       "delta_ci95_pp": r["delta_ci95_pp"], "mcnemar_p": r["mcnemar_p"],
                       "delta_vs_random_mean_pp": r["delta_vs_mean_pp"],
                       "n_evaluation": r["n_evaluation"]} for r in rows],
            "source": "data/682_a5_split_comparison.json (682 B1)",
            "generated_by": "tools/figures_682.py",
        },
    }
    _jwrite(OUT / "c3_split_comparison.echarts.json", opt)
    _png_split(OUT / "c3_split_comparison.png", rows)
    return opt


# ─────────────────────────────────────────────────────────────────────────────
# C4 资产互补性
# ─────────────────────────────────────────────────────────────────────────────
def fig_c4() -> dict:
    rows = asset_rows()
    opt = {
        "title": {"text": "C4 · Asset complementarity: exact Shapley contribution (n=566 eval)",
                  "subtext": ("Shapley over all 2^8 subsets (exact); unique = samples only this asset "
                              "catches; degenerate assets (wunsequenced/compile-time) contribute 0."),
                  "left": "center", "textStyle": {"color": FG}},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"},
                    "formatter": "详见 queyi:meta.table（含 c=评估集 catch / u=独占 catch）"},
        "grid": {"left": 210, "right": 90, "top": 100, "bottom": 40},
        "xAxis": {"type": "value", "name": "Shapley (pp)", "max": 22,
                  "axisLabel": {"color": FG}},
        "yAxis": {"type": "category",
                  "data": [f"{r['asset']}  (c={r['eval_catch']}, u={r['unique_catch']})"
                           for r in rows][::-1],
                  "axisLabel": {"color": FG}},
        "series": [
            {"name": "Shapley contribution (pp)", "type": "bar", "barWidth": 18,
             "data": [{"value": r["shapley_pp"],
                       "itemStyle": {"color": "#95a5a6" if r["degenerate"] else "#8e44ad"}}
                      for r in rows][::-1],
             "label": {"show": True, "position": "right", "formatter": "{c}pp"}},
        ],
        "queyi:meta": {
            "rows": rows,
            "linker_note": ("linker: Shapley +0.71pp，评估集 catch "
                            f"{[r for r in rows if r['asset']=='linker'][0]['eval_catch']} 条、"
                            "全部为独占 catch（其余资产都抓不到）⇒ 低边际但不可替代。"
                            "（676l 全池口径另有「10 个 catch 全落在 asan/ubsan/tsan 的 unknown 里」的登记，"
                            "两个口径分母不同，勿混用。）"),
            "degenerate_note": "compile-time / wunsequenced 全样本 unknown ⇒ Shapley=0、unique=0。",
            "source": "data/682_asset_ablation.json (682 B3)",
            "generated_by": "tools/figures_682.py",
        },
    }
    _jwrite(OUT / "c4_asset_complementarity.echarts.json", opt)
    _png_assets(OUT / "c4_asset_complementarity.png", rows)
    return opt


# ─────────────────────────────────────────────────────────────────────────────
# PNG（PIL；环境无 matplotlib —— 不是"降级凑合"，PIL 为环境内可用的等价渲染）
# ─────────────────────────────────────────────────────────────────────────────
def _font(size: int):
    from PIL import ImageFont
    for name in ("msyh.ttc", "msyhbd.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


def _png_heatmap(path: Path, types: list[str], counts: dict, ts: dict) -> None:
    from PIL import Image, ImageDraw
    W, H = 1240, 1200
    left, top, right, bottom = 350, 108, 30, 90
    cw = (W - left - right) / len(ASSETS)
    ch = (H - top - bottom) / len(types)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_s = _font(13)
    d.text((14, 14), "C1 · Detection rate by type × asset (681-normalized 34 types, n=1147)",
           fill=FG, font=_font(20))
    d.text((14, 44), "row label = type (blind-rate); red columns = types >50% blind; "
                     "value = catch rate %.", fill="#555555", font=f_s)
    def color(p):  # 0% 红 → 100% 绿
        r = int(192 + (39 - 192) * p / 100)
        g = int(57 + (174 - 57) * p / 100)
        b = int(43 + (96 - 43) * p / 100)
        return (r, g, b)
    for xi, a in enumerate(ASSETS):
        lab = a + ("\n(unknown)" if a in DEGEN else "")
        d.text((left + xi * cw + 4, 74), lab, fill="#888888" if a in DEGEN else FG, font=f_s)
    for yi, t in enumerate(types):
        y = top + yi * ch
        bp = ts[t]["blind_pct"]
        col = HI if bp > 50 else FG
        d.text((8, y + ch / 2 - 9), f"{t} ({bp:.0f}%)", fill=col, font=f_s)
        for xi, a in enumerate(ASSETS):
            x = left + xi * cw
            if a in DEGEN:
                # 恒 unknown：浅灰底 + n/a，**不画 0%（unknown 绝不当 miss）**
                d.rectangle([x, y, x + cw - 2, y + ch - 2], fill="#ededed")
                d.text((x + cw / 2 - 10, y + ch / 2 - 8), "n/a", fill="#999999", font=f_s)
                continue
            c = counts[t][a]
            p = 100.0 * c["catch"] / c["n"] if c["n"] else 0.0
            d.rectangle([x, y, x + cw - 2, y + ch - 2], fill=color(p))
    d.text((14, H - 56),
           "wunsequenced / compile-time columns show n/a (constant-unknown: no local detector) — "
           "intentionally NOT drawn as 0%, because unknown is never counted as miss.",
           fill="#555555", font=f_s)
    d.text((14, H - 34),
           "source: data/blindspot_676g_detection_matrix.json + data/681_type_stats_normalized.json "
           "(681-fixed canon; the legacy 70-type heatmap is superseded).", fill="#555555", font=f_s)
    img.save(path)


def _png_family(path: Path, rows: list[dict]) -> None:
    from PIL import Image, ImageDraw
    W, H = 1100, 620
    left, top = 220, 90
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f, fs = _font(18), _font(14)
    d.text((left, 30), "C2 · Blind-spot rate by family (681-normalized, n=1147)", fill=FG, font=_font(22))
    maxv = 80.0
    bw = (W - left - 220) / maxv
    bh = (H - top - 60) / len(rows)
    for i, r in enumerate(rows):
        y = top + i * bh
        d.text((12, y + bh / 2 - 10), f"{r['family']} (n={r['n']})", fill=FG, font=f)
        w = r["blind_pct"] * bw
        col = HI if r["blind_pct"] > 50 else "#2e86de"
        d.rectangle([left, y + 4, left + w, y + bh - 6], fill=col)
        d.text((left + w + 8, y + bh / 2 - 9), f"{r['blind_pct']:.1f}%", fill=FG, font=f)
    for x in range(0, 81, 20):
        xx = left + x * bw
        d.line([xx, top, xx, H - 55], fill="#dddddd")
        d.text((xx - 10, H - 48), f"{x}%", fill=FG, font=fs)
    img.save(path)


def _png_split(path: Path, rows: list[dict]) -> None:
    from PIL import Image, ImageDraw
    W, H = 1150, 660
    left, top = 90, 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f, fs = _font(16), _font(13)
    d.text((left, 20), "C3 · A5 main endpoint across four splits (k=4, n≈566-569 each)",
           fill=FG, font=_font(21))
    d.text((left, 52), "Δ(FD − Random single point) in each group header; CI / McNemar p in "
                       "queyi:meta.table of the ECharts JSON.", fill="#555555", font=fs)
    # 图例（标题下方一行，避免与 x 轴标签争位）
    colors = {"fd": "#27ae60", "random": "#2e86de", "static": "#95a5a6"}
    x = left
    for name, key in (("FD", "fd"), ("Random (single point)", "random"), ("Static", "static")):
        d.rectangle([x, 82, x + 16, 98], fill=colors[key])
        d.text((x + 22, 80), name, fill=FG, font=fs)
        x += 200
    d.line([x, 90, x + 34, 90], fill="#e67e22", width=2)
    d.text((x + 40, 80), "Random 2000-run mean", fill=FG, font=fs)
    maxv = 70.0
    gw = (W - left - 60) / len(rows)
    bh = (H - top - 70) / maxv
    for gi, r in enumerate(rows):
        gx = left + gi * gw
        d.text((gx + 10, top - 36), f"Δ={r['delta_pp']:+.2f}pp", fill=FG, font=f)
        for si, key in enumerate(("fd", "random", "static")):
            v = r[key]
            x = gx + 20 + si * (gw - 40) / 3
            y0 = H - 70 - v * bh
            d.rectangle([x, y0, x + (gw - 40) / 3 - 8, H - 70], fill=colors[key])
            d.text((x, y0 - 20), f"{v:.1f}", fill=FG, font=fs)
        ym = H - 70 - r["random_mean"] * bh
        d.line([gx + 10, ym, gx + gw - 20, ym], fill="#e67e22", width=2)
        d.text((gx + 10, H - 44), r["split"], fill=FG, font=f)
    img.save(path)


def _png_assets(path: Path, rows: list[dict]) -> None:
    from PIL import Image, ImageDraw
    W, H = 1200, 660
    left, top = 300, 130
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f, fs = _font(16), _font(13)
    d.text((left - 200, 20), "C4 · Asset complementarity: exact Shapley contribution "
                             "(n=566 eval)", fill=FG, font=_font(20))
    d.text((left - 200, 52), "grey = degenerate (constant-unknown, contribution 0); "
                             "c = evaluation catches, u = unique catches (no other asset catches).",
           fill="#555555", font=fs)
    maxv = 22.0
    bw = (W - left - 200) / maxv
    bh = (H - top - 60) / len(rows)
    # 网格线先画（避免压在柱子上）
    for x in range(0, 23, 5):
        xx = left + x * bw
        d.line([xx, top - 8, xx, H - 50], fill="#e8e8e8")
        d.text((xx - 12, H - 42), f"{x}", fill=FG, font=fs)
    for i, r in enumerate(rows):
        y = top + i * bh
        d.text((10, y + bh / 2 - 10), f"{r['asset']}  (c={r['eval_catch']}, u={r['unique_catch']})",
               fill=FG, font=f)
        w = r["shapley_pp"] * bw
        col = "#95a5a6" if r["degenerate"] else "#8e44ad"
        d.rectangle([left, y + 4, left + max(w, 2), y + bh - 6], fill=col)
        d.text((left + max(w, 2) + 10, y + bh / 2 - 9), f"{r['shapley_pp']:+.2f}pp",
               fill=FG, font=f)
    d.text((left - 200, H - 20),
           "source: data/682_asset_ablation.json (682 B3, exact Shapley over all 2^8 subsets).",
           fill="#555555", font=fs)
    img.save(path)


# ─────────────────────────────────────────────────────────────────────────────
def main() -> int:
    if not SPLIT_CMP.is_file() or not ABLATION.is_file():
        print("[682-C] 缺 B1/B3 产物（682_a5_split_comparison.json / 682_asset_ablation.json）"
              "⇒ 先跑 tools/analyze_682_sensitivity.py", flush=True)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    fig_c1(); fig_c2(); fig_c3(); fig_c4()
    files = sorted(p.name for p in OUT.iterdir())
    idx = ["# 682 · 图表索引（任务C）\n",
           f"- 生成：`python tools/figures_682.py`；产物目录 `data/682_figures/`",
           "- 数据口径：**681 修复后的 34 类归一化数据** + 682 B1/B3 产物（判定矩阵复用 676f）\n",
           "| 图 | ECharts | PNG | 数据源 |",
           "|---|---|---|---|",
           "| C1 盲区热力图（34×8） | c1_blindspot_heatmap.echarts.json | c1_blindspot_heatmap.png | "
           "data/blindspot_676g_detection_matrix.json + data/681_type_stats_normalized.json |",
           "| C2 家族金字塔 | c2_family_pyramid.echarts.json | c2_family_pyramid.png | "
           "data/681_type_stats_normalized.json#family8 |",
           "| C3 多 split 对比 | c3_split_comparison.echarts.json | c3_split_comparison.png | "
           "data/682_a5_split_comparison.json |",
           "| C4 资产互补性 | c4_asset_complementarity.echarts.json | c4_asset_complementarity.png | "
           "data/682_asset_ablation.json |",
           "",
           "**诚实登记**：",
           "1. 环境无 matplotlib ⇒ PNG 由 Pillow（环境内可用）渲染；ECharts option JSON 为机器可读主产物。",
           "2. 旧 70 类热力图（676g 时代）**未被覆盖**：本批只新增 682_figures/，"
           "论文引用的旧图替换建议见验收报告（不擅自删除既有产物）。",
           "3. C3 的误差棒：ECharts 无内置误差棒，CI 数据在 option 的 `queyi:meta.table` 内，"
           "PNG 中标注 Δ 与 Random 均值线。",
           "",
           f"文件清单：{', '.join(files)}",
           ]
    (OUT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8", newline="\n")
    print(f"[682-C] 写 {len(files)} 个文件 + INDEX.md 到 data/682_figures/", flush=True)
    for p in sorted(OUT.iterdir()):
        size = p.stat().st_size
        if p.suffix == ".json":
            json.loads(p.read_text(encoding="utf-8"))
        if size < 200:
            print(f"[682-C] FAIL 产物过小：{p.name}", flush=True)
            return 1
        print(f"  {p.name:44s} {size:>8d} B", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
