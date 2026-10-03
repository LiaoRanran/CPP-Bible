#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""blindspot_676g_viz.py — 676g 任务 G：盲区地图可视化（ECharts）。

输入  data/blindspot_676g_stats.json
输出  data/blindspot_676g_visualization.html

图表（数据全部来自 stats JSON，与判定矩阵一致）：
  1. 热力图：行=缺陷类型（按盲区比例降序、family 分组），列=6 可用资产，值=catch 率。
  2. 条形图：各类型盲区比例降序（miss 与 unknown 堆叠，区分确定漏报与无法判定）。
  3. 雷达图：每个资产在 8 个 family 上的 catch 覆盖率。
  4. 条形图：批次盲区比例 + planted 对比。
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATS = HERE / "blindspot_676g_stats.json"
OUT = HERE / "blindspot_676g_visualization.html"

ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"]
ASSET_LABEL = {"asan": "ASan", "ubsan": "UBSan", "tsan": "TSan",
               "compiler-warn": "compiler-warn", "cross-compile": "cross-compile",
               "linker": "linker"}
FAMILY_LABEL = {
    "memory": "内存安全", "ub": "未定义行为", "concurrency": "并发",
    "stl": "标准库/STL", "embedded_platform": "嵌入式/平台",
    "language_raii": "语言语义/RAII", "link_odr": "链接/ODR",
    "logic_semantic": "逻辑/语义", "api_misuse": "API 误用", "other": "其他",
}


def main() -> int:
    st = json.loads(STATS.read_text(encoding="utf-8"))
    types = st["by_type"]

    # 热力图：family 分组内按盲区比例降序
    fam_order = []
    for r in types:
        if r["family"] not in fam_order:
            fam_order.append(r["family"])
    rows = []
    for f in fam_order:
        rows.extend([r for r in types if r["family"] == f])
    y_labels = [f"{r['defect_type']} ({r['n']})" for r in rows]
    heat = []
    for yi, r in enumerate(rows):
        for xi, a in enumerate(ASSETS):
            heat.append([xi, yi, round(r["asset_catch_rate"].get(a, 0) * 100, 1)])

    # 条形图：盲区比例（miss/unknown 堆叠）
    bar_types = [r["defect_type"] for r in rows]
    bar_miss = [round(r["miss_ratio"] * 100, 1) for r in rows]
    bar_unknown = [round(r["unknown_ratio"] * 100, 1) for r in rows]

    # 雷达：资产 × family 覆盖率
    fams = [f for f in fam_order]
    fam_types = {f: [r for r in types if r["family"] == f] for f in fams}
    radar_ind = [{"name": FAMILY_LABEL.get(f, f), "max": 100} for f in fams]
    radar_series = []
    for a in ASSETS:
        vals = []
        for f in fams:
            rs = fam_types[f]
            num = sum(r["asset_catch"].get(a, 0) for r in rs)
            den = sum(r["n"] for r in rs)
            vals.append(round(num / den * 100, 1) if den else 0)
        radar_series.append({"value": vals, "name": ASSET_LABEL[a]})

    # 批次 + planted
    batches = st["by_batch"]
    batch_names = sorted(batches.keys())
    batch_blind = [round(batches[b]["blindspot_ratio"] * 100, 1) for b in batch_names]
    planted = st["by_planted"]

    payload = {
        "y_labels": y_labels, "x_assets": [ASSET_LABEL[a] for a in ASSETS],
        "heat": heat, "bar_types": bar_types, "bar_miss": bar_miss,
        "bar_unknown": bar_unknown, "radar_ind": radar_ind,
        "radar_series": radar_series, "batch_names": batch_names,
        "batch_blind": batch_blind, "planted": planted,
        "bands": st["blindspot_bands"], "total": st["total"],
        "n_types": st["n_types"],
        "caliber": st["caliber"],
    }

    html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>676g · 检测器盲区地图</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
  body { font-family: "Segoe UI", "Microsoft YaHei", sans-serif; margin: 0;
         background: #f7f8fa; color: #222; }
  header { padding: 20px 28px 8px; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .sub { color: #666; font-size: 13px; margin-bottom: 6px; }
  .caliber { background: #fffbe6; border: 1px solid #ffe58f; border-radius: 6px;
             padding: 8px 12px; font-size: 12.5px; margin: 10px 28px; line-height: 1.7; }
  .card { background: #fff; border-radius: 10px; margin: 14px 28px; padding: 14px;
          box-shadow: 0 1px 4px rgba(0,0,0,.06); }
  .chart { width: 100%; height: 620px; }
  .chart-tall { width: 100%; height: 1150px; }
  h2 { font-size: 15.5px; margin: 4px 4px 10px; color: #333; }
</style>
</head>
<body>
<header>
  <h1>检测器盲区地图 — 全量 __NT__ 样本 × 8 资产（676g）</h1>
  <div class="sub">检测器：WSL g++ 13.3（ASan/UBSan/TSan，-O0/-O2 双档）+ 本机 MinGW g++ 13.1 / clang++ 22.1.8
  （compiler-warn / wunsequenced / cross-compile / linker）；矩阵 schema queyi-blindspot-matrix/676g</div>
</header>
<div class="caliber" id="caliber"></div>
<div class="card"><h2>① 类型 × 资产 catch 率热力图（按盲区比例降序、按缺陷家族分组；点击图例可筛选）</h2>
  <div id="heat" class="chart-tall"></div></div>
<div class="card"><h2>② 各类型盲区比例排序（蓝=确定漏报 miss，橙=全部 unknown 无法判定）</h2>
  <div id="bar" class="chart"></div></div>
<div class="card"><h2>③ 资产 × 缺陷家族 覆盖率雷达（catch 率 %）</h2>
  <div id="radar" class="chart"></div></div>
<div class="card"><h2>④ 批次盲区比例 与 planted 对比</h2>
  <div id="batch" class="chart"></div></div>
<script>
const D = __PAYLOAD__;
document.getElementById('caliber').innerHTML =
  '<b>口径</b>：样本级 catch = 8 资产任一 catch；miss = 无 catch 且 ≥1 可用资产确定 miss；' +
  'unknown = 6 可用资产全部 unknown；<b>盲区比例 = (miss+unknown)/n</b>。' +
  'wunsequenced（MinGW 不认 -Wunsequenced）与 compile-time（无本地检测器）结构性恒 unknown、永不 catch，' +
  '故 OR 口径下 8 资产与 6 可用资产完全等价；两资产仍单列于按资产统计并注明。' +
  '本图 catch 率均为 "catch 样本数 / 类型样本数"。总盲区 <b>' +
  (D.total.blindspot_ratio*100).toFixed(1) + '%</b>（catch ' + D.total.catch + ' / miss ' +
  D.total.miss + ' / unknown ' + D.total.unknown + '，n=' + D.total.n + '）';

const heat = echarts.init(document.getElementById('heat'));
heat.setOption({
  tooltip: { position: 'top', formatter: p => D.y_labels[p.value[1]] + '<br>' +
            D.x_assets[p.value[0]] + ' catch 率: <b>' + p.value[2] + '%</b>' },
  grid: { left: 190, right: 120, top: 10, bottom: 60 },
  xAxis: { type: 'category', data: D.x_assets, splitArea: { show: true } },
  yAxis: { type: 'category', data: D.y_labels, splitArea: { show: true },
           axisLabel: { fontSize: 11 } },
  visualMap: { min: 0, max: 100, calculable: true, orient: 'vertical',
               right: 8, top: 'center',
               inRange: { color: ['#a50026', '#d73027', '#f46d43', '#fdae61',
                                  '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'] },
               formatter: v => v + '%' },
  series: [{ type: 'heatmap', data: D.heat, label: { show: true, fontSize: 9,
             formatter: p => p.value[2] > 0 ? p.value[2] : '' } }]
});

const bar = echarts.init(document.getElementById('bar'));
bar.setOption({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' },
             valueFormatter: v => v + '%' },
  legend: { data: ['miss（确定漏报）', 'unknown（无法判定）'] },
  grid: { left: 190, right: 40, top: 40, bottom: 40 },
  xAxis: { type: 'value', axisLabel: { formatter: '{value}%' }, max: 100 },
  yAxis: { type: 'category', data: D.bar_types, axisLabel: { fontSize: 11 } },
  series: [
    { name: 'miss（确定漏报）', type: 'bar', stack: 'b', data: D.bar_miss,
      itemStyle: { color: '#4393c3' } },
    { name: 'unknown（无法判定）', type: 'bar', stack: 'b', data: D.bar_unknown,
      itemStyle: { color: '#f4a582' } }
  ]
});

const radar = echarts.init(document.getElementById('radar'));
radar.setOption({
  tooltip: {},
  legend: { top: 0 },
  radar: { indicator: D.radar_ind, radius: '62%' },
  series: [{ type: 'radar', data: D.radar_series,
             areaStyle: { opacity: 0.08 }, lineStyle: { width: 2 } }]
});

const batch = echarts.init(document.getElementById('batch'));
const P = D.planted;
batch.setOption({
  tooltip: { valueFormatter: v => v + '%' },
  legend: {},
  grid: { left: 60, right: 40, top: 40, bottom: 40 },
  xAxis: { type: 'category',
           data: D.batch_names.concat(['planted=true', 'planted=false (n=74)', 'corpus planted=null']) },
  axisLabel: { rotate: 30 },
  yAxis: { type: 'value', axisLabel: { formatter: '{value}%' }, max: 100 },
  series: [
    { name: '盲区比例', type: 'bar',
      data: D.batch_blind.concat([P['true'] ? +(P['true'].blindspot_ratio*100).toFixed(1) : null,
                                  P['false'] ? +(P['false'].blindspot_ratio*100).toFixed(1) : null,
                                  P['null'] ? +(P['null'].blindspot_ratio*100).toFixed(1) : null]),
      itemStyle: { color: '#d73027' },
      label: { show: true, position: 'top', formatter: '{c}%' } }
  ]
});

window.addEventListener('resize', () => { heat.resize(); bar.resize(); radar.resize(); batch.resize(); });
</script>
</body>
</html>
"""
    html = html.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    html = html.replace("__NT__", str(st["total"]["n"]))
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"[676g] viz: {len(rows)} 类型 × {len(ASSETS)} 资产热力图等 4 图；"
          f"写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
