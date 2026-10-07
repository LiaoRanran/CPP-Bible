# 688 · C2 TMLR 投稿详细策略

- **批次**：688 ｜ **来源**：TMLR 官方（jmlr.org/tmlr）+ 2026 公开报道（OpenReview 运作、2022 创刊、ISSN 2835-8856、强调 significance & readability 而非纯新颖性、2026-09 主编面询实验）
- **官方**：<https://www.jmlr.org/tmlr/> ｜ OpenReview：<https://openreview.net/group?id=TMLR>

## 1. TMLR 基本属性
- JMLR 旗下**开放获取期刊**，2022 创刊，ISSN 2835-8856；基于 **OpenReview** 透明评审（审稿意见公开）。
- **无固定截稿日期**（rolling submission），审稿较快，适合作为"先发可引用"的落点。
- 评审重心：**significance（意义）与 readability（可读性）优于 pure novelty**；重视可复现性。
- 2026-09 主编面询实验（抽取待拒稿论文约作者谈基础要素）显示其**高度重视作者真正理解自家工作**——本论文经 686 自我批判打磨、主张克制，恰好契合。

## 2. 匹配度
| 维度 | 匹配 | 说明 |
|---|---|---|
| Significance | 高 | 评估治理/失败驱动评估的议题有社区价值 |
| Readability | 中高 | 论文经多轮精修、结构清晰 |
| Novelty | 中 | 非新算法；但评估框架/治理视角有新意（符合 TMLR 不唯新颖）|
| Reproducibility | 中（待补）| 同 NeurIPS——须匿名代码托管 |
| **Scope 风险** | **中低** | 见下 |

## 3. Scope 风险（须诚实标注）
- TMLR 是 **"Machine Learning Research"** 期刊，scope 为 ML。本论文主体是 **C++ 验证器评估**，ML 内容稀薄（若有 LLM-as-verifier 第四臂则可补 ML 相关，但当前未实装）。
- 风险：若 AE 认为"无 ML 核心贡献"可能 **desk-reject 或转投**。缓解：在 framing 上明确"本文提出**通用评估治理框架（AGEA）**，以 C++ 验证器为实例化案例"——把 ML/评估方法论作为主贡献层（685 已铺此桥）。

## 4. 需要的额外材料
- **Reproducibility checklist**：TMLR 要求填复现清单（数据/代码/环境/随机种子/计算资源）；本仓库已有 AI_USAGE_LOG、REPRODUCE.md、固定种子审计（676h），可直接转写。
- **代码与数据**：须公开且可运行；匿名托管。
- **可复现性声明**：明确"条件复现"（686 #9）并给 B2 量化（59.09%→23.64%）。

## 5. 与 NeurIPS E&D 的对比
| | TMLR | NeurIPS E&D |
|---|---|---|
| 类型 | 期刊（rolling）| 会议（年截稿）|
| 新颖性要求 | 较低（重意义/可读）| 中等（重洞察/失败模式）|
| 双盲 | 透明评审（OpenReview，作者可见）| 双盲默认 |
| 背书/门槛 | **无需 endorsement** | 会议投稿，无 arXiv 背书问题 |
| Scope | ML 严格 | 评估/数据宽泛 |
| 周期 | 数月 | 半年+ |
| DOI/可引用 | 有 | 会议录 |

- **优势**：TMLR 无 endorsement 门槛、rolling、可作为"先发可引用"落点，且对本论文"非新算法但有意义"的特质更宽容。
- **劣势**：ML scope 风险；期刊影响力/认知度在 ML 圈略低于 NeurIPS。

## 6. 实操建议
- 将 TMLR 作为**并行/前置**落点：先投 TMLR 拿评审与 DOI，再视结果与 NeurIPS 2027 协调（注意期刊与会议重叠政策——TMLR 允许 conference 版，但须在投稿时声明）。
- 投稿前完成：匿名代码托管、Reproducibility checklist、scope framing（AGEA 通用框架层）。

## 7. 诚实边界
- TMLR 的 ML scope 是真实风险；若论文 ML 内容不足，优先补 LLM-as-verifier 臂（684/685 已规划）或转投 SE 顶会（FSE/ICSE 的 evaluation track）作为备选（本策略未覆盖，仅提示）。
- "TMLR 录取率"未抓取，行业常识约 **中等偏宽（高于顶会）**；不作官方数据引用。
