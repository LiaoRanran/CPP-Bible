# 01 · 研究问题（RQ1–RQ4，v0.1 冻结）

> 冻结：这四个问题定死后不再增删；新增须升 v1.1。

## RQ1 — 真实缺陷检测能力
queyi 对**历史真实缺陷**（A1）与**盲化 holdout**（A2）的 catch / miss / unknown / false_positive 各多少？
（≠ mutation score）

## RQ2 — 泛化（frozen holdout）
在**冻结后**才 reveal 的 holdout 上，检测率是否随分布变化显著下降？
（测"换个分布还灵不灵"）

## RQ3 — 预算匹配对照（failure-driven vs random）
同样加 N 个验证资产，**失败驱动选择**是否显著优于**随机选**（B3 budget-matched random）？
（回应审稿人"只是因为测多了"的质疑）

## RQ4 — 元状态可验证性
独立对账器（status_reconciler_658，不依赖 queyi core）能否检测出"文档状态 vs git 实际状态"的漂移？
（仪表盘保真）
