# _arch_v44 · 08 Benchmark 设计方法论（方向 8）

> 核心问题：好 benchmark 设计、防污染、难度分层、标注质量、被刷榜、MMLU/HumanEval/SWE-bench 教训。
> 诚实标注：【官方】；【实证】；【论文】；【推断】；【盲区】。

---

## 一、好 benchmark 设计

- 四要素：明确构念（测什么）/ 无污染构建（盲集+冻结哈希）/ 难度分层 / 可复现评估（脚本+容器）。阙疑天然有 append-only 账本+Merkle，是强项。

## 二、防污染

- 方法：①盲 holdout 不参与训练/调参 ②数据冻结+哈希校验 ③定期换新（防记忆）④公开集与私有集分离。SWE-bench 教训：Verified 被污染+缺陷测试→Pro【实证】。

## 三、难度分层 & 标注质量

- 分层：易（单点事实）/ 中（需推理）/ 难（需多步+边界）。阙疑可据变异密度（10–11 变异/卡）分层。
- 标注：双人独立+Cohen's kappa≥0.6 才入；单人用自检+重标（方向 16）。

## 四、被刷榜 & 三大教训

- 刷榜应对：私有测试集+排行榜需提交预测不公开标签+定期重置。
- 教训：MMLU（知识记忆易污染）、HumanEval（单函数易过拟合）、SWE-bench（缺陷测试+污染）【实证】。阙疑应回避「benchmark」自称，定位「审计语料+案例研究」。

## 五、对阙疑的 3 条具体行动

1. **重命名对外定位**：把「benchmark」改称「evaluation corpus + audit case study」，在 repo README 与论文标题规避刷榜联想。
2. **建污染防火墙**：盲 holdout 20 单独加密存储，CI 跑评估时只注入哈希校验不解密标签，确保未泄露给调参。
3. **做难度三分层的 corpus 看板**：按变异密度把 48 卡+外部 20 条分易/中/难三层，报告每层检出率，补 construct 可信度。

## 六、来源

[S30] SWE-bench 系列（Verified/Pro）；[S31] MMLU (Hendrycks et al., 2020)；[S32] HumanEval (Chen et al., 2021)；[S33] "Benchmarking Benchmark Leakage" 类论文；内部：_arch_v44_brief.md（变异密度 10–11/卡）。

**盲区**：阙疑是否真有私有/公开分离机制未确认；三大 benchmark 具体泄漏率无统一定量。
