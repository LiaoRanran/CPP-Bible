# 08 · 指标（主指标 + 次指标）

## 主指标（回答 RQ1–RQ3，外部效度）
- **Defect detection rate** = catch / (catch+miss) 于 D1/D2；
- **Holdout 四元组** = (catch, miss, unknown, false_positive) 于 D2；
- **Budget gain Δ** = detect(失败驱动, N) − detect(随机, N) 于 B3。

## 次指标（回答内部效度，不代替主指标）
- **Test adequacy**：mutation score（core 97.3% / all 81.5%）、coverage、property coverage；
- **Replayability**：证据 replay 成功率；
- **Meta-consistency**：reconciler 检出漂移的样本数 / 植入漂移样本数（RQ4）。

## 禁区（A5）
mutation score **不得**用于宣称外部效度；主/次指标在报告中**分栏**，禁止混算单一"准确率"。
