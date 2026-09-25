# 613 基线 0.2 · 学习者镜像数据缺口台账

> 生成：`python tools/613_baseline.py` ｜ 时间：2026-09-20T23:54:27
> 口径：只读统计；CI 结论取自 GitHub Actions API；**未运行**监工类 --check。

## 掌握度存储 `data/learner_state_612.jsonl`

- 记录数：**27** ｜ 字段：{'user_id': 27, 'kc_id': 27, 'mastery_prob': 27, 'correct': 27, 'kind': 27, 'timestamp': 27, 'simulated': 27}
- 覆盖 KC 数=27 ｜ 已掌握(≥0.5)=0 ｜ 平均掌握度=0.100

## KC 台账 `data/kc_inventory_612.json`

- KC 数：**0**

## 真实学习行为数据源

- `data/learner_behavior.jsonl`：**存在**（0 条）
- 结论：**无真实学习行为数据**（612 原型全为模拟数据）⇒ 线 C 必须先建接入层（C1）。

> 缺口判定：掌握度是 612 `simulate()` 生成的模拟值，非真实行为递推 ⇒ 镜像仍为空壳。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `direct_experiment`
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
