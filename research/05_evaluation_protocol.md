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

## Dataset 冻结（D0–D4，v0.1 冻结）

> 五个数据集定死后不再增删；新增须升 v1.1。D2/D4 在 Phase 3/6 之前绝不可用于训练或调参。

- **D0 Development（开发集）**：本仓库 `Examples/atoms/`（147 个真实 C++ 错误夹具）+ `Book/` 实卡，用于 Phase 1 训练/调参验证器。
- **D1 Historical（历史集）**：A1 真实缺陷夹具（`data/defect_fixtures/defects.json`，来自 git log 挖出的 656/657/652/历史 ch 系列修过的错），Phase 2 重注入测 catch/miss。
- **D2 Blind（盲化 holdout）**：`data/holdout/holdout.json`（660 C2 初始化 20 个样本，覆盖 UB/内存越界/未定义行为/编译器差异），Phase 3 reveal（不可逆）。开发期默认不扫。
- **D3 External（外部 corpus）**：A4 引入的外部样本（跨编译器差异、真实编译器 bug、教材错），冻结、不进 D0。
- **D4 Independent（独立生成）**：A3 Agent A/B/C 分离独立生成的样本（对冲开发者知情偏差），冻结、不进 D0。

**冻结纪律**：D2/D4 在 Phase 3/6 之前绝不可用于训练或调参；违反即实验作废。
