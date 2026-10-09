# 705-C · 可视化素材说明

所有图表为**数据文件 + ECharts 配置**，未渲染图片。配色学术风格（蓝/橙/红/青）。
数字均来自冻结批次（683/684/688/692/blindspot_676g），与论文一致；缺失项标「待补」。

## 图表清单

- **fd_vs_random**：FD（贪心组合）vs Random 基线，k=1..8（真实靶场 110 复算；论文合成帧锚点 684 greedy 58.49% vs random 42.52%）  → 放 `论文 Figure：组合增益 / 子模`
  - 数据：`figures/data/fd_vs_random.json` ｜ ECharts：`figures/echarts/fd_vs_random.json`
- **capability_heatmap_34x8**：70 细粒度缺陷类型（34 类词表的细粒度展开）× 8 资产 catch% 热力图（合成 1147）  → 放 `论文 Figure：能力边界地图`
  - 数据：`figures/data/capability_heatmap_34x8.json` ｜ ECharts：`figures/echarts/capability_heatmap_34x8.json`
- **environment_wsl_vs_native**：WSL vs native 环境感知对比（692，−35pp）  → 放 `论文 Appendix：环境感知`
  - 数据：`figures/data/environment_wsl_vs_native.json` ｜ ECharts：`figures/echarts/environment_wsl_vs_native.json`
- **realworld_vs_synthetic**：真实 CVE vs 自造语料逐资产 catch%（683 §1.1）  → 放 `论文 Real-World Validation`
  - 数据：`figures/data/realworld_vs_synthetic.json` ｜ ECharts：`figures/echarts/realworld_vs_synthetic.json`
- **unique_hit_distribution**：独苗命中资产分布（27 条，占比 41.5%）  → 放 `论文：资产互补性`
  - 数据：`figures/data/unique_hit_distribution.json` ｜ ECharts：`figures/echarts/unique_hit_distribution.json`
- **per_asset_catch_110**：逐资产 catch/miss/unknown（真实靶场 110）  → 放 `论文：逐资产基线`
  - 数据：`figures/data/per_asset_catch_110.json` ｜ ECharts：`figures/echarts/per_asset_catch_110.json`
- **realworld_by_type**：真实靶场按缺陷类型 OR 检出率  → 放 `论文：类型级分析`
  - 数据：`figures/data/realworld_by_type.json` ｜ ECharts：`figures/echarts/realworld_by_type.json`
- **four_type_family_drift**：四家族真实 vs 合成 OR% 漂移（代理指标，精确 Goodhart 漂移量待补）  → 放 `论文：结构性漂移`
  - 数据：`figures/data/four_type_family_drift.json` ｜ ECharts：`figures/echarts/four_type_family_drift.json`

## 怎么用
- 把 `figures/echarts/<id>.json` 内容贴入 ECharts 官网 `setOption()` 即可预览。
- 数据文件为纯 JSON，可喂任意绘图库（matplotlib/vega/plotly）。

## 诚实边界
- `four_type_family_drift` 的精确 Goodhart 漂移量在本批冻结数据中未独立核算，图以四家族真实/合成 OR% 差作代理。
- 所有数字绑定「本 8 资产 + 本工具链」口径；环境类数字来自 692 配对实验（只读冻结矩阵）。