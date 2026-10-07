#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""figures_683.py — 683-D3：研究报告图表（≥8 张，PNG + ECharts option 双产物）。

策略（不重复造轮子）：
  * C1–C4 复用 682 冻结图表（复制 ECharts JSON 与 PNG 到 docs/figures/，不重画）；
  * C5–C8 由本批产物新画：
      C5 真实靶场 vs 自造语料 逐资产检出率（分组柱）
      C6 真实靶场 项目覆盖（横向条）
      C7 真实靶场 缺陷类型分布（柱）
      C8 Operator 16 配置消融（Pool A k=4，柱 + fd_only 基线）
  * PNG 用 Pillow 渲染（白底，论文友好）；ECharts option 同步落 json。

用法：python tools/figures_683.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "figures"
F682 = ROOT / "data" / "682_figures"
BG, FG, GRAY = "#ffffff", "#222222", "#666666"


def _jload(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def _jwrite(p: Path, doc: dict) -> None:
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")


def _font(size: int):
    from PIL import ImageFont
    for name in ("msyh.ttc", "msyhbd.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


def png_bars(path: Path, title: str, sub: str, labels: list[str], series: list[dict],
             *, ymax: float | None = None, horizontal: bool = False,
             label_size: int = 11) -> None:
    """通用柱状图渲染。series = [{"name":..., "color":..., "values":[...]}]。"""
    from PIL import Image, ImageDraw
    W, H = 1180, 720
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((70, 22), title, fill=FG, font=_font(21))
    d.text((70, 56), sub, fill=GRAY, font=_font(13))
    # 图例
    lx = 70
    for s in series:
        d.rectangle([lx, 90, lx + 16, 106], fill=s["color"])
        d.text((lx + 22, 88), s["name"], fill=FG, font=_font(13))
        lx += 30 + 10 * len(s["name"])
    maxv = ymax or max(max(s["values"]) for s in series) * 1.15
    if not horizontal:
        left, top, bottom, right = 80, 140, H - 110, W - 50
        gw = (right - left) / len(labels)
        bh = (bottom - top) / maxv
        nser = len(series)
        for gi, lab in enumerate(labels):
            gx = left + gi * gw
            for si, s in enumerate(series):
                v = s["values"][gi]
                x = gx + gw * 0.12 + si * (gw * 0.76) / nser
                w = (gw * 0.76) / nser - 6
                y0 = bottom - v * bh
                d.rectangle([x, y0, x + w, bottom], fill=s["color"])
                d.text((x + 2, y0 - 16), f"{v:.1f}", fill=FG, font=_font(10))
            # x 标签（可能两行）
            words = lab.split()
            if len(lab) > 14:
                d.text((gx + 4, bottom + 8), lab[:14], fill=FG, font=_font(label_size))
                d.text((gx + 4, bottom + 24), lab[14:28], fill=FG, font=_font(label_size))
            else:
                d.text((gx + 8, bottom + 8), lab, fill=FG, font=_font(label_size))
        # y 轴刻度
        for t in range(0, int(maxv) + 1, 10):
            y = bottom - t * bh
            d.line([left, y, right, y], fill="#e8e8e8", width=1)
            d.text((left - 34, y - 8), f"{t}", fill=GRAY, font=_font(11))
    else:
        left, top, right = 260, 140, W - 90
        bottom = H - 60
        gw = (bottom - top) / max(len(labels), 1)
        bh = (right - left) / max(max(s["values"]) for s in series) / 1.1
        for gi, lab in enumerate(labels):
            gy = top + gi * gw
            v = series[0]["values"][gi]
            d.text((16, gy + gw / 2 - 8), lab[:30], fill=FG, font=_font(12))
            d.rectangle([left, gy + 6, left + v * bh, gy + gw - 6], fill=series[0]["color"])
            d.text((left + v * bh + 6, gy + gw / 2 - 8), f"{v}", fill=FG, font=_font(12))
    img.save(path)


def fig_c5() -> dict:
    rwm = _jload(ROOT / "data" / "683_real_world_detection_matrix.json")
    g = _jload(ROOT / "data" / "blindspot_676g_detection_matrix.json")
    assets = rwm["assets"]
    rw = [rwm["per_asset_summary"][a]["catch_rate_pct"] or 0 for a in assets]
    syn = []
    for a in assets:
        n = g["n_samples"]
        c = sum(1 for s in g["samples"] if s["per_asset"][a]["verdict"] == "catch")
        syn.append(round(c / n * 100, 2))
    option = {
        "title": {"text": "C5 · 真实靶场 vs 自造语料：逐资产检出率",
                  "subtext": f"真实 n={rwm['n_samples']} / 自造 n={g['n_samples']}；unknown 不进分母",
                  "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 56, "data": ["真实靶场（683）", "自造语料（676g）"]},
        "grid": {"left": 70, "right": 40, "top": 110, "bottom": 60},
        "xAxis": {"type": "category", "data": assets, "axisLabel": {"rotate": 30}},
        "yAxis": {"type": "value", "name": "catch 率 %", "max": 100},
        "series": [{"name": "真实靶场（683）", "type": "bar", "data": rw,
                    "itemStyle": {"color": "#2e86de"}},
                   {"name": "自造语料（676g）", "type": "bar", "data": syn,
                    "itemStyle": {"color": "#27ae60"}}],
    }
    png_bars(OUT / "c5_realworld_vs_synthetic.png",
             "C5 · Real-world vs synthetic: per-asset catch rate",
             f"same 8-asset pipeline; real n={rwm['n_samples']}, synthetic n={g['n_samples']}",
             assets, [{"name": "real (683)", "color": "#2e86de", "values": rw},
                      {"name": "synthetic (676g)", "color": "#27ae60", "values": syn}],
             ymax=100, label_size=10)
    return option


def fig_c6() -> dict:
    rwm = _jload(ROOT / "data" / "683_real_world_detection_matrix.json")
    cnt: dict[str, int] = {}
    for s in rwm["samples"]:
        cnt[s["project"]] = cnt.get(s["project"], 0) + 1
    items = sorted(cnt.items(), key=lambda kv: (kv[1], kv[0]))  # 自下而上
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    option = {
        "title": {"text": "C6 · 真实靶场项目覆盖", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 170, "right": 50, "top": 60, "bottom": 40},
        "xAxis": {"type": "value", "name": "样本数"},
        "yAxis": {"type": "category", "data": labels, "axisLabel": {"fontSize": 11}},
        "series": [{"type": "bar", "data": vals, "itemStyle": {"color": "#2e86de"}}],
    }
    png_bars(OUT / "c6_project_coverage.png",
             f"C6 · Real-world benchmark: {len(labels)} upstream projects",
             "reconstructed defects per project (683)", labels,
             [{"name": "samples", "color": "#2e86de", "values": vals}], horizontal=True)
    return option


def fig_c7() -> dict:
    rwm = _jload(ROOT / "data" / "683_real_world_detection_matrix.json")
    cnt: dict[str, int] = {}
    for s in rwm["samples"]:
        cnt[s["defect_type"]] = cnt.get(s["defect_type"], 0) + 1
    items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    option = {
        "title": {"text": "C7 · 真实靶场缺陷类型分布（34 类词表）", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 60, "right": 40, "top": 60, "bottom": 95},
        "xAxis": {"type": "category", "data": labels, "axisLabel": {"rotate": 40, "fontSize": 10}},
        "yAxis": {"type": "value", "name": "样本数"},
        "series": [{"type": "bar", "data": vals, "itemStyle": {"color": "#e67e22"}}],
    }
    png_bars(OUT / "c7_type_distribution.png",
             "C7 · Real-world defect types (34-type vocabulary)",
             f"{len(labels)} types across 110 samples", labels,
             [{"name": "samples", "color": "#e67e22", "values": vals}], label_size=9)
    return option


def fig_c8() -> dict:
    abl = _jload(ROOT / "data" / "683_operator_ablation.json")
    blk = abl["pools"]["A"]["k_blocks"]["4"]["configs"]
    names = [n for n in blk if not n.startswith("u_")]
    names = sorted(names, key=lambda n: -(blk[n]["rate_pct"] or 0))
    vals = [blk[n]["rate_pct"] for n in names]
    base = blk["fxxx"]["rate_pct"]
    option = {
        "title": {"text": "C8 · Operator 16 配置消融（literal；Pool A，k=4）",
                  "subtext": "等权 on/off 全枚举；compare to fd_only baseline "
                             f"({base}%)", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "grid": {"left": 60, "right": 40, "top": 100, "bottom": 70},
        "xAxis": {"type": "category", "data": names, "axisLabel": {"rotate": 40, "fontSize": 10}},
        "yAxis": {"type": "value", "name": "评估集检出率 %", "min": 45, "max": 58},
        "series": [{"type": "bar", "data": vals, "itemStyle": {"color": "#27ae60"},
                    "markLine": {"data": [{"yAxis": base}]}}],
    }
    png_bars(OUT / "c8_operator_ablation.png",
             "C8 · Operator 16-config ablation (literal, Pool A, k=4)",
             f"equal-weight on/off; fd_only baseline = {base}%",
             names, [{"name": "catch %", "color": "#27ae60", "values": vals}],
             ymax=60, label_size=10)
    return option


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    # C1–C4：复制 682 冻结产物（不重画）
    for stem in ("c1_blindspot_heatmap", "c2_family_pyramid",
                 "c3_split_comparison", "c4_asset_complementarity"):
        for ext in (".png", ".echarts.json"):
            src = F682 / f"{stem}{ext}"
            if src.is_file():
                shutil.copy2(src, OUT / f"{stem}{ext}")
    made = ["c1_blindspot_heatmap", "c2_family_pyramid", "c3_split_comparison",
            "c4_asset_complementarity"]
    # C5–C8：新画（需要 683 产物；缺失时跳过并如实报告）
    for fn, stem in ((fig_c5, "c5_realworld_vs_synthetic"),
                     (fig_c6, "c6_project_coverage"),
                     (fig_c7, "c7_type_distribution"),
                     (fig_c8, "c8_operator_ablation")):
        try:
            opt = fn()
            _jwrite(OUT / f"{stem}.echarts.json", opt)
            made.append(stem)
        except Exception as e:  # noqa: BLE001
            print(f"[683-D3] {stem} 跳过：{type(e).__name__}: {e}")
    idx = ["# docs/figures — 683 图表索引\n",
           f"共 {len(made)} 张（PNG + ECharts option 各一份）。\n"]
    for m in made:
        src = "682 冻结（复用）" if m.startswith(("c1", "c2", "c3", "c4")) else "683 新绘"
        idx.append(f"- `{m}.png` / `{m}.echarts.json` — {src}")
    idx.append("\n> 口径：所有图与 data/ 产物同源；PNG 为 Pillow 渲染（白底），"
               "ECharts option 可在浏览器交互渲染。")
    (OUT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8", newline="\n")
    print(f"[683-D3] docs/figures 完成：{len(made)} 张（{'，'.join(made)}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
