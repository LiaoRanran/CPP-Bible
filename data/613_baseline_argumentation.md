# 613 基线 0.3 · 论证层桥接边人审状态台账

> 生成：`python tools/613_baseline.py` ｜ 时间：2026-09-20T23:54:27
> 口径：只读统计；CI 结论取自 GitHub Actions API；**未运行**监工类 --check。

## 桥接候选边

- 工件：`bridge_edge_candidates_611.jsonl` ｜ 候选数：**98**
- 字段：['basis', 'components', 'direction', 'edge_id', 'kind', 'note', 'priority', 'source', 'target']
- 优先级分布：{'weak': 98}

## 桥接边人审记录

- `data/bridge_edge_review_612.jsonl`：存在 ｜ 记录数：**0**
- 结论：**桥接边人审记录为空** ⇒ 98 条候选边无一条经过人审确认。

## W2 判决现状 `data/grounded_labels_w2.json`

- 判决分布：{'IN': 114, 'OUT': 7}
- 节点总数=121
- 顶层键：['credibility_levels', 'defeating_edges', 'edges', 'model', 'nodes', 'rounds', 'summary', 'tool', 'version']

> 口径提醒：W2 判决存在 keep-low(IN114/OUT7) 与 upgrade-medium(IN121/OUT0) 双口径（611 遗留未裁决）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `human_review`
- `materiality_flag`: false


## 635 V26-2 系统误差二分（不可合并为单一健康分）

**可收敛指标**（加样本可改善）：
- 逃逸率：多测 mutation 可更准确估计漏报率（统计量）
- τ_d（逃逸→修补间隔）：样本量增加可收紧分位数
- 接地覆盖率：可补实验把「部分/未接地」转「已接地」
- 工具数/测试数：持续增加

**不可收敛指标**（加样本无效，须换方法）：
- coverage 缺口：剩下的是**没测过的攻击面**，不是测不准
- 自身免疫率：是**规则设计问题**，不是样本问题
- Horizon 断崖（60-80 桶）：是**载体天花板**，不是样本量
- N/A 率：主因是载体无法施加（634 B3），加样本无效
- gate 规则数：是**设计选择**，非估计量
