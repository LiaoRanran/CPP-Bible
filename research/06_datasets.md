# 06 · 数据集（D0–D4，v0.1 冻结）

| 集 | 名称 | 内容 | 用途 | 是否进训练 |
|---|---|---|---|---|
| D0 | Development | 自造变异库（full_baseline_v7）+ 可重注入真实缺陷子集 | 训练/调参验证器 | ✅ |
| D1 | Historical | A1 全部 18 个历史真实缺陷（含不可重注入的，登记覆盖） | RQ1 历史回归 | ❌（仅评测） |
| D2 | Blind | data/holdout/ 盲化 seed（reveal 前开发期不可见） | RQ1/RQ2 盲化 | ❌ |
| D3 | External | data/external_corpus_658.md 登记引入的真实源（GCC/Clang/UB/教材…） | RQ2 泛化 | ❌ |
| D4 | Independent | 由独立第三方（或非本仓作者）生成/标注的缺陷集 | RQ2 独立泛化 | ❌ |

**切分纪律**：D2/D4 在评估流程 Phase 3/6 前必须保持 blind；一旦 reveal 写 .revealed 即不可逆。
