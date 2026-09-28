# 04 · 威胁模型（12 类威胁）

1. **自证威胁**：验证器用自己的工具链证明自己 → 用 status_reconciler_658（独立）对冲。
2. **自造分布偏差**：变异算子是我们设计的，验证器"熟悉" → 用盲化 holdout + 外部 corpus 对冲。
3. **holdout 泄漏**：开发期偷看 holdout → 铁律：reveal 不可逆，且默认不扫 data/holdout/。
4. **开发者知情偏差**：生成错误的人同时写验证器 → 用独立生成（A3：Agent A/B/C 分离）。
5. **口径漂移**：文档数字与 git 实际不符 → reconciler 对账。
6. **语义 scope 误用**：把"在我实验里成立"当"普遍成立" → 拆 provenance/semantic scope（C 段）。
7. **度量混淆**：mutation score 当缺陷检测率 → 指标分层（A5 / 08_metrics）。
8. **选择偏差（预算）**：失败驱动只是因为资产多 → B3 budget-matched random 对照。
9. **过拟合到历史缺陷**：A1 缺陷是已知修过的 → 用 blind（A2）+ external（A4）补未知分布。
10. **复现危机**：环境/版本不可复现 → OTS 锚 + 编译器版本锁定（11_reproducibility）。
11. **Authority 操纵**：账本被偷偷改 → 452 条历史账本零改动红线。
12. **AI 署名不清**：LLM 贡献未登记 → 13_ai_use_and_authorship.md + AI_USAGE_LOG。
