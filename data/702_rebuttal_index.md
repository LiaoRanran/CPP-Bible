# 702 · Rebuttal 弹药库索引（Rebuttal Arsenal Index）

> 目的：把分散在各批次的 rebuttal 相关文件汇总成一张索引，标明**哪个版本最新、覆盖哪些问题、红线在哪**。
> 检查时间：2026-10-09｜范围：`data/*rebuttal*`、`data/*redlines*`、`research/rebuttal_prep*`。

---

## 1. 文件清单与定位

| 文件 | 批次 | 角色 | 规模 / 覆盖 |
|---|---|---|---|
| `research/rebuttal_prep.md` | — | 母本（v1.2，Q1–Q18） | 最初版问答框架，三段式纪律来源 |
| `data/686_rebuttal_arsenal.md` | 686 | **初始弹药库** | ≥20 Q&A，8 类（因果识别 / 外部效度 / …） |
| `data/686_rebuttal_redlines.md` | 686 | **红线清单 D2** | 绝对不能说的话（避免暴露弱点/与数据矛盾） |
| `data/690_rebuttal_arsenal.md` | 690 | 弹药库 D1 | 9 条主弹药，分"质疑类/高风险接受类" |
| `data/690_rebuttal_redlines.md` | 690 | 红线清单 D3 | 发出前逐句检查表，补 8 条"过度认错"隐性红线 |
| `data/692_rebuttal_v3.md` | 692 | **增量修订版** | 同步 691 的 8 项变动 + 数字速查 + Q19/20/21；v2 §1–§7 仍有效 |
| `data/697_rebuttal_arsenal_v2.md` | 697 | **★ 最新弹药库** | 35 问 + 20 红线 + 数字速查；继承 686/686_redlines/rebuttal_prep + 695 文献 + 697-A/B |

---

## 2. 哪个版本最新？

**最新 = `data/697_rebuttal_arsenal_v2.md`（697-E）**。

继承关系（按时间）：
`rebuttal_prep.md (v1.2)` → `686_arsenal + 686_redlines` → `690_arsenal + 690_redlines` →
`692_rebuttal_v3`（增量） → **`697_rebuttal_arsenal_v2`**（当前最新，35 问 + 20 红线）。

> 使用规则：以 697 v2 为**主入口**；692 v3 中未被 697 覆盖的问答仍以 692 v3 为准（其 §1–§7 主体有效）。

---

## 3. 红线文件在哪（重要）

> 702 任务书点名的 `687_rebuttal_supplement.md` **在仓库中不存在**（诚实标注：未找到）。
> 实际红线分散在两份文件，投稿前必须逐句对照：

- `data/686_rebuttal_redlines.md`（D2，初始红线，如"不可说 FD 优于 Random""不可说标签已通过 κ 验证"）
- `data/690_rebuttal_redlines.md`（D3，发出前检查表，补 8 条"过度认错"隐性红线）

**红线核心（任何 rebuttal 段发出前必查）**：
1. 不可声称"演化算子优于 Random / 提升召回"（与 14/14 同构消融矛盾）
2. 不可声称"合成与真实等价"（TOST ±10pp 未通过）
3. 不可声称"Merkle 提供完整历史溯源"（仅 current-state tamper-evident）
4. 不可声称"标签已通过 κ=0.727 验证"（那是 AI 自洽，非人类 IRR）
5. 不可假装 1137 与 1147 无差异（同一批两种口径，须主动脚注）
6. 题名已非 "Evolving Verifiers"——任何材料出现旧题名即为缺陷

---

## 4. 覆盖的问题主题（去重后）

- 因果识别：+24pp 是否退化资产造成 / 是否克隆泄漏 / 是否随机抽坏资产
- 外部效度：合成 vs 真实、跨工具对比定位、LLM 第四臂
- 方法学：测量漂移代数、结构性被动 Goodhart（4 类）、能力边界地图、公理独立性 + 不完备（A8 缺失）
- 诚实边界：human IAA=0、Docker 未实测、WSL 硬依赖、模板克隆率
- 与其他工作的区分：DeepFact / Who Grades the Grader / SV-COMP / HELM

---

## 5. 使用建议

1. 写 rebuttal 前：**先读 697 v2 的纪律段 + 690_redlines 检查表**。
2. 每条回应**必须给复算入口**（脚本名 / JSON 字段 / tex 行号）。
3. 不升级 claim；不引入新主张；被批评时**不要过度认错**（失真同罪）。
4. E&D rebuttal 通常 500–1500 字：建议正文只放前 5 条主弹药，其余进 appendix。

> 本索引为**快照**；若 697 之后有新批次弹药库，以最新者为准。
