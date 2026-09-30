# 669d 门禁报告

生成时间：2026-09-30 20:10:51

总体：**PASS**

| 类别 | 条数 | 含义 |
|---|---:|---|
| 未登记 BLOCK | 0 | 新出现的缺口，必须修 |
| 已登记缺口（降级 WARN） | 4 | 已在 669d_known_gaps.json 登记，待 669 工程修 |
| 其他 WARN | 13 | 建议项 |

## 已登记缺口（诚实登记，不静默）

| 规则 | 对象 | 原因 | 负责人 |
|---|---|---|---|
| G-STATS-FROZEN | `research/05_evaluation_protocol.md ← Clopper-Pearson` | 669d D4 已把统计口径冻结在 research/669d_统计口径.md（Clopper-Pearson 95% CI / McNemar / Fisher / BH / Cohen κ）；本批红线禁止改 research 既有协议文件，待 669 工程把该文件内容合入 05_evaluation_protocol.md 后本条自动消解。 | 669 工程（669d 审计登记） |
| G-STATS-FROZEN | `research/05_evaluation_protocol.md ← Fisher` | 669d D4 已把统计口径冻结在 research/669d_统计口径.md（Clopper-Pearson 95% CI / McNemar / Fisher / BH / Cohen κ）；本批红线禁止改 research 既有协议文件，待 669 工程把该文件内容合入 05_evaluation_protocol.md 后本条自动消解。 | 669 工程（669d 审计登记） |
| G-STATS-FROZEN | `research/05_evaluation_protocol.md ← McNemar` | 669d D4 已把统计口径冻结在 research/669d_统计口径.md（Clopper-Pearson 95% CI / McNemar / Fisher / BH / Cohen κ）；本批红线禁止改 research 既有协议文件，待 669 工程把该文件内容合入 05_evaluation_protocol.md 后本条自动消解。 | 669 工程（669d 审计登记） |
| G-BASELINE-EXISTS | `web/data/experiments.json ← escape` | escape 指标（616 冻结 1/1406 = 0.0711%）缺少 static gate 基线的同指标对照。web/data/experiments.json 自陈 baselines.status=planned，属已知待生成项。 | 669 工程（669d 审计登记） |

## 其他 WARN

| 规则 | 对象 | 说明 |
|---|---|---|
| G-STATS-FROZEN | `research/05_evaluation_protocol.md ← Cohen's kappa` | 协议未声明 Cohen's kappa（建议补） |
| G-STATS-FROZEN | `research/05_evaluation_protocol.md ← BH 校正` | 协议未声明 BH 校正（建议补） |
| G-BOUNDARY-REQUIRED | `atoms/` | 未安装 pyyaml ⇒ 无法解析 frontmatter（降级为 WARN） |
| G-BASELINE-EXISTS | `web/data/experiments.json ← catch（抓住）` | 实验结果 [holdout_outcomes] 含指标「catch（抓住）」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← miss（漏）` | 实验结果 [holdout_outcomes] 含指标「miss（漏）」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← 保护器` | 实验结果 [ability] 含指标「保护器」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← 命题` | 实验结果 [ability] 含指标「命题」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← 知识卡（实）` | 实验结果 [ability] 含指标「知识卡（实）」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← 草稿卡` | 实验结果 [ability] 含指标「草稿卡」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← 账本事件` | 实验结果 [ability] 含指标「账本事件」，但 data/baseline.json 无对应基线 |
| G-BASELINE-EXISTS | `web/data/experiments.json ← 门禁规则` | 实验结果 [ability] 含指标「门禁规则」，但 data/baseline.json 无对应基线 |
| G-IRR | `data/irr_records.json` | IRR 记录文件不存在 ⇒ 全部人工标注卡无一致性证据 |
| G-IRR | `atoms/` | 无 pyyaml ⇒ 无法扫卡 |
