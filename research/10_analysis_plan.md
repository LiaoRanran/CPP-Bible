# 10 · 结果分析计划（Analysis Plan）

1. **分层报告**： adequacy / detection / generalization 三栏分开（A5 / 08_metrics），不混。
2. **主假设检验（H1）**：对 D1+D2 的 catch/(catch+miss) 做与 B0 的二项检验，报 p 与 Clopper-Pearson 95% 区间。
3. **预算增益（H3）**：B3 下失败驱动 vs 随机的配对比较（同 N 资产），报 Δ 与置信区间；
   若 Δ 不显著 → 承认"只是测多了"，不夸失败驱动。
4. **泛化（H2）**：D2 reveal 后检测率 vs D0 变异检测率之差，是否超预设容差（威胁 2）。
5. **元状态（H4）**：植入漂移样本，reconciler 检出率是否 = 100%（威胁 1/5）。
6. **未知即成功**：补完证据仍 unknown 的样本如实报告，不为降 unknown 而补假边界（658 诚实要求）。
7. **负面结果 likewise**：miss/unknown 多 → 正是价值，不隐藏。
