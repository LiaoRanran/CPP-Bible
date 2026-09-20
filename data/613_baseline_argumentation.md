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
