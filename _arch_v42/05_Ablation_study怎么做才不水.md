# _arch_v42 · 05 Ablation study 怎么做才不水（方向 5）

> 核心问题：最小 ablation 集（Full vs -X vs random-budget）；每个 ablation 回答什么；样本量；单人怎么跑不烧钱。
> 诚实标注：【论文】；【共识】；【推断】= 对阙疑的判断；【盲区】= 无法核实。

---

## 一、最小 ablation 集（三件套）

1. **Full**：完整系统。
2. **-X**：去掉一个核心组件（如去掉变异基线 / 去掉 Merkle 审计 / 去掉某保护器）。
3. **random-budget**：随机预算对照（证明不是"跑得久/试得多"带来的收益）。

每个 ablation 须先写一句"它要回答的问题"，否则即水【推断，S19/S20】。

## 二、每个 ablation 回答什么（映射到阙疑）

| Ablation | 回答的问题 |
|---|---|
| -变异基线 | 边界错检出是否依赖变异，还是编译/运行已覆盖 |
| -Merkle 审计 | 账本不可篡改是否影响检出可信度 |
| -某保护器（如 B1 冲突仲裁） | 该保护器是否真在判决中起作用的因果证据 |
| random-budget | 检出率是否来自"更多尝试"而非"更对的方法" |

## 三、样本量多大才够

- 经验：每个条件 ≥ 20–30 独立样本才能给误差棒；阙疑盲 holdout 仅 20，刚好在边缘，需扩充或显式标注"探索性"【推断，S19】。
- 用 bootstrap / 置信区间替代大样本；报告 95% CI 而非单点。

## 四、单人怎么跑不烧钱

- 阙疑判决单卡 0.59ms（内部锚），跑 ablation 成本极低；瓶颈在夹具构造，而非算力。
- 复用已有 48 卡 + 15 夹具做 -X，不用新采数据。

## 五、来源

[S19] D'Amour et al., "Underspecification Presents Challenges for Credibility in Modern ML", PNAS 2020（规格不足→ablation 必要）；[S20] 通用 ablation 最佳实践（ML 社区）；[S21] 组件因果 ablation 方法论文（Do-Input-Ablations-Really-Ablate 类）；内部：_arch_v42_brief.md（单卡 0.59ms / 48 卡）。

**盲区**：阙疑各组件的真实边际贡献无实测数据，上表为待验设计。
