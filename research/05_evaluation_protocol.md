# 05 · 评估流程（Phase 0–7，v0.1 冻结）

> 流程定死后不再改；改则升 v1.1。

- **Phase 0 · 快照**：跑 status_reconciler_658 --check，确认元状态干净（HEAD/ahead/质量/dirty 一致）。
- **Phase 1 · 构建 D0**：用 Development 集训练/调参验证器（不得碰 D2/D4）。
- **Phase 2 · 历史回归（RQ1 部分）**：A1 真实缺陷夹具重注入，记 catch/miss。
- **Phase 3 · 盲化 reveal（RQ1/RQ2）**：holdout_658 --reveal（不可逆），记 catch/miss/unknown/fp。
- **Phase 4 · 预算对照（RQ3）**：B3 跑"随机选 N 资产"与"失败驱动选 N 资产"，同 D0 上比检测增益。
- **Phase 5 · 消融（见 09）**：A0–A4 逐一去掉组件，看检测率掉多少。
- **Phase 6 · 外部 corpus（RQ2 补充）**：A4 引入的外部样本（冻结、不进 D0）。
- **Phase 7 · 对账 + 报告**：reconciler 复核元状态；产出分层指标报告（adequacy/detection/generalization 分栏）。

**冻结纪律**：D2/D4 在 Phase 3/6 之前绝不可用于训练或调参；违反即实验作废。
