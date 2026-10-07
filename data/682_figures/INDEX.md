# 682 · 图表索引（任务C）

- 生成：`python tools/figures_682.py`；产物目录 `data/682_figures/`
- 数据口径：**681 修复后的 34 类归一化数据** + 682 B1/B3 产物（判定矩阵复用 676f）

| 图 | ECharts | PNG | 数据源 |
|---|---|---|---|
| C1 盲区热力图（34×8） | c1_blindspot_heatmap.echarts.json | c1_blindspot_heatmap.png | data/blindspot_676g_detection_matrix.json + data/681_type_stats_normalized.json |
| C2 家族金字塔 | c2_family_pyramid.echarts.json | c2_family_pyramid.png | data/681_type_stats_normalized.json#family8 |
| C3 多 split 对比 | c3_split_comparison.echarts.json | c3_split_comparison.png | data/682_a5_split_comparison.json |
| C4 资产互补性 | c4_asset_complementarity.echarts.json | c4_asset_complementarity.png | data/682_asset_ablation.json |

**诚实登记**：
1. 环境无 matplotlib ⇒ PNG 由 Pillow（环境内可用）渲染；ECharts option JSON 为机器可读主产物。
2. 旧 70 类热力图（676g 时代）**未被覆盖**：本批只新增 682_figures/，论文引用的旧图替换建议见验收报告（不擅自删除既有产物）。
3. C3 的误差棒：ECharts 无内置误差棒，CI 数据在 option 的 `queyi:meta.table` 内，PNG 中标注 Δ 与 Random 均值线。

文件清单：INDEX.md, c1_blindspot_heatmap.echarts.json, c1_blindspot_heatmap.png, c2_family_pyramid.echarts.json, c2_family_pyramid.png, c3_split_comparison.echarts.json, c3_split_comparison.png, c4_asset_complementarity.echarts.json, c4_asset_complementarity.png
