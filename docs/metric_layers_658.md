# 658 A5 · 指标分层（论文用，禁止混用）

> 核心警告：**mutation score = 97% ≠ 真实世界错误检测能力 = 97%**。

## 三层指标，必须分开报告

### 1. Test adequacy（测试充分度）
回答"测试有多狠"：
- mutation score（core 97.3% / all 81.5%）—— 对**自造变异分布**的检出率
- coverage（行/分支/路径）
- property coverage（覆盖了多少条属性）

→ 这是**内部**指标，只说明"测得多不多"，不说明"能不能抓真错"。

### 2. Defect detection（缺陷检测）
回答"抓真错抓得怎么样"：
- historical defects（A1）：已修过的真实错，重注入后几个门禁会红 → **真实缺陷检出率**
- blind seeded defects（A2）：盲化 holdout 的 catch / miss / unknown / false_positive
- external defects（A4）：外部 corpus 的检出率

→ 这是**外部效度**指标，但每个来源分布不同，不能互相替代。

### 3. Generalization（泛化）
回答"换个分布还灵不灵"：
- frozen holdout（A2 一旦 reveal 就冻结，不再当训练/调参用）
- 跨语义 scope（C 段）的稳健性

## 为什么分开

把 mutation score 当 defect detection 会**系统性高估**外部效度：
- 变异算子是我们自己设计的，验证器天然"熟悉"这些变异形态；
- 真实错误（编译器 bug、UB、教材错、跨编译器差异）形态不在变异分布里；
- ⇒ mutation 97% 仅对该变异分布成立，单点上界 Clopper-Pearson 95% = 0.337%（见 F 段）。

## 报告模板（验收报告必须分栏）

| 层 | 指标 | 本批值 | 含义 |
|---|---|---|---|
| adequacy | mutation core/all | 97.3% / 81.5% | 只对自造变异成立 |
| detection | 真实缺陷重注入 | 2/2（可重注入子集） | 受限于原错误版本缺失 |
| detection | 盲化 holdout | 5/5 catch, 0 miss | 演示协议，非对抗 |
| generalization | frozen holdout | 待 reveal 冻结后 | 后续批次 |
