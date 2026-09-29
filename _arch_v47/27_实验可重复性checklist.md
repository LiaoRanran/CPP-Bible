# 方向 27：实验可重复性 checklist

## 核心结论

1. **ACM 徽章不是四档而是"两个家族 + 三个独立徽章"，且结果验证徽章几乎没人拿到。** ACM 官方原文逐字：*"We recommend that **three separate badges** related to artifact review be associated with research articles in ACM publications: **Artifacts Evaluated, Artifacts Available and Results Validated**. These badges are considered independent and any one, two or all three can be applied to any given paper"*。其中 `Artifacts Evaluated` 分 Functional / Reusable 两级，`Results Validated` 分 **Results Reproduced**（*"using, in part, artifacts provided by the author"*）与 **Results Replicated**（*"without the use of author-supplied artifacts"*）两级。**EuroSys 2021–2025 五年的真实获得数是 161（Available）/ 136（Functional）/ 75（Results Reproduced）**——从 Available 到 Results Reproduced 只剩 **46.6%**。另有一条对阙疑极有利的条款：*"Artifacts need not be made publicly available to be considered for this badge. However, they do need to be made available to reviewers."*

2. **容差是官方明确允许的，但有一条不可越界的红线。** ACM 逐字：*"In each cases, **exact replication or reproduction of results is not required, or even expected**. Instead, the results must be in agreement to within a tolerance deemed acceptable for experiments of the given type. **In particular, differences in the results should not change the main claims made in the paper.**"* 对阙疑的含义：检出率可以允许小幅波动（如 66.7% → 63.3%），但**账本 Merkle root 必须精确一致**，因为哈希链是离散精确量，容差在这类量上没有意义。论文里应显式区分"可容差量"与"必须精确量"两张清单。

3. **领域层面的复现率统计已经非常惨烈，这为阙疑的"负面/审计类"叙事提供了最强的引用弹药。** 三个可直接引用的硬数字：① **Open Science Collaboration 2015**（270 位作者、100 项心理学研究）：原始研究中 **97%** 报告显著结果，复现中只有 **36%** 显著，平均效应量约为原始的一半；② **Reproducibility Project: Cancer Biology**（8 年、**193 个实验来自 53 篇论文**）：**0% 的实验方案被完整描述**、**仅 2% 的实验有公开数据**、复现效应量平均比原始小 **85%**、原始阳性结果复现率 **40%** 而原始零结果复现率 **80%**；③ **ICML 2026 Open Reproductions Challenge**（**2226 篇论文、1200+ 参与者、6816 份 logbook**）：**51% 的论文至少一条 claim 被验证**，**23% 的论文有 claim 被证伪或有争议**。

---

## 精确数字与案例

### 一、ACM 五个徽章的逐字标准

| 徽章 | 逐字标准（ACM *Artifact Review and Badging* v1.1，2020-08-24） |
|---|---|
| **Artifacts Available** | *"Author-created artifacts relevant to this paper have been placed on a publically accessible archival repository. A DOI or link to this repository along with a unique identifier for the object is provided."* 补充：*"Personal web pages are not acceptable for this purpose."*；*"Artifacts do not need to have been formally evaluated in order for an article to receive this badge."* |
| **Artifacts Evaluated – Functional** | *"The artifacts associated with the research are found to be **documented, consistent, complete, exercisable**, and include appropriate evidence of verification and validation."* 四词定义：Documented = 至少含清单 + 足够说明；Consistent = 与论文相关且实质贡献主结果；Complete = 相关组件尽量齐全（专有件可豁免但须说明获取方式）；**Exercisable = 脚本能成功执行、数据能访问并正确处理**。 |
| **Artifacts Evaluated – Reusable** | *"The artifacts associated with the paper are of a quality that **significantly exceeds minimal functionality**. That is, they have all the qualities of the Artifacts Evaluated – Functional level, but, in addition, they are **very carefully documented and well-structured to the extent that reuse and repurposing is facilitated**. In particular, norms and standards of the research community for artifacts of this type are strictly adhered to."* |
| **Results Reproduced** | *"The main results of the paper have been obtained in a subsequent study by a person or team other than the authors, **using, in part, artifacts provided by the author**."* |
| **Results Replicated** | *"The main results of the paper have been **independently** obtained in a subsequent study by a person or team other than the authors, **without the use of author-supplied artifacts**."* |

**授予机制（易被忽略的行政细节）**：徽章是 *"added to papers by the publisher, not by the authors"*（POPL 2026 逐字）；且 ACM 原文说 *"**Editors-in-Chiefs and Conference Steering Committee Chairs** (or an appropriate SIG Chair should a conference not have an extant steering committee) will have the authority to award these badges **post-publication** if warranted. For Results Validated, **a peer-reviewed publication which reports the replication or reproduction must be submitted as evidence**, and if awarded, the badge will contain a link to this paper."* 另外 ACM 明确徽章体系是**可选**的：*"are encouraged, but remain completely optional for ACM journals and conferences"*。

**为什么徽章定义容易被误读**：EuroSys AE 主席在 2025 年总结中把 *"Imprecise badge definitions"* 列为六大持续挑战之一，逐字：*"ACM's badge definitions are descriptive, not prescriptive, potentially leading to inconsistent interpretations even across different editions of the same conference."* 并且 ACM 自己也承认：*"badges included in PDFs and in ACM Digital Library metadata should be linked to a brief explanation of the particular review process which led to the awarding of the badge."*——**即：徽章本身不含"怎么评的"信息，必须另附说明。论文里引用徽章时应同时说明评审流程。**

### 二、真实获得率与参与率

| 会议 / 计划 | 数字 | 出处 |
|---|---|---|
| EuroSys 2021–2025 | **161** Artifacts Available；**136** Functional；**75** Results Reproduced | SIGOPS 博客 / ACM REP '25（DOI 10.1145/3736731.3746152） |
| EuroSys 年度参与率 | *"A steady **58%** of accepted papers participating in AE annually"* | 同上 |
| EuroSys AE 委员会 | 2025 年峰值 **98 人** | 同上 |
| SIGMOD ARI 提交率 | **25%（2023）→ 33%（2024）→ 43%（2025）** | ACM DL 10.1145/3785021 |
| SIGMOD Best Artifact | *"Every year, **up to three** fully reproduced papers with high-quality artifacts are recognized with the 'Best Artifact' award"* | reproducibility.sigmod.org |
| SIGMOD 2024 | *"All papers for which the artifacts are made available received the 'Artifacts Available' badge."* | ACM DL 10.1145/3687998 |
| POPL 2026 | 三个 ACM 徽章：Functional / Reusable（subsumes Functional）/ Available（在 Functional 或 Reusable 之外追加） | popl26.sigplan.org |

**换算出的漏斗**：Available → Functional = **84.5%**（136/161）；Available → Results Reproduced = **46.6%**（75/161）。**这是一个可直接写进论文的"AE 通过率基线"**：如果阙疑拿到 Available，期望约 85% 概率拿到 Functional、约 47% 概率拿到 Results Reproduced。

### 三、领域层面的复现率（三个可引用的"惨烈基线"）

**① Open Science Collaboration 2015（心理学）** —— *"Estimating the Reproducibility of Psychological Science"*, Science, DOI **10.1126/science.aac4716**，约 **270 位作者**：

- 样本：**100 项**实验与相关性研究，取自 2008 年的 *Psychological Science*、*JPSP*、*JEP:LMC*
- 原始研究报告显著结果比例：**97%**；复现研究显著比例：**36%**
- 复现的平均效应量约为原始的**一半**
- 复现团队主观判定"复现成功"比例：**约 39%**
- 认知心理学复现率显著高于社会心理学

**② Reproducibility Project: Cancer Biology（COS + Science Exchange，8 年）**：

| 指标 | 数字 |
|---|---|
| 原始论文 / 实验数 | **53 篇论文 / 193 个实验**（论文发表于 2010–2012） |
| 有公开数据的实验 | **2%** |
| 需要向原作者索取关键试剂的实验 | **70%** |
| 其中原作者愿意分享的比例 | **69%** |
| **实验方案被完整描述的比例** | **0%** |
| 原作者不配合或无回应的实验 | **32%** |
| 原作者非常配合的实验 | **41%** |
| 需要修改才能完成的实验 | **67%** |
| 修改被完整实现的比例 | **41%** |
| 最终完成的复现实验 | **50 个，来自 23 篇论文**，共 **158 个效应** |
| **复现效应量平均比原始小** | **85%** |
| 在多数标准上复现成功的效应 | **46%** |
| 原始阳性结果 vs 原始零结果的复现率 | **40% vs 80%** |

**③ ICML 2026 Open Reproductions Challenge（2026-07）**：

- ICML 2026 投稿 **23,918 篇**、接收 **6,352 篇**（*"double the previous year"*）
- 挑战赛覆盖 **2226 篇论文**（约占接收论文的**三分之一**），**1200+ 参与者**，产出 **6816 份 logbook**
- **51% 的论文至少一条 claim 被验证**；**23% 的论文有 claim 被证伪或有争议**
- **266 篇**全部 claim 被验证（完全复现）；**632 篇**部分复现且无证伪
- 工具链：Claude Code、Codex 等 coding agent；判定分四类 verified / falsified / toy / inconclusive

**④ Nature 2016 问卷（1,576 位研究者）**：

- **>70%** 曾尝试复现他人实验并失败；**>一半** 曾无法复现自己的实验
- **52%** 认同存在显著的复现"危机"；但 **<31%** 认为复现失败意味着原结果很可能是错的
- **73%** 认为本领域至少一半论文可信
- **<20%** 曾被其他研究者联系说无法复现其工作
- **24%** 曾发表成功的复现；**13%** 曾发表失败的复现
- **三分之一** 的实验室在过去五年采取了具体改进措施（医学 **41%** 最高，物理与工程 **24%** 最低）
- 归因：**>60%** 指出"发表压力"与"选择性报告"，**>一半** 指出"实验室内缺乏重复""监督不足或统计功效低"
- 改进方案认同度：**接近 90%（>1000 人）** 支持"更稳健的实验设计""更好的统计""更好的导师制"；**最低的"期刊 checklist"也获得 69% 支持**
- 成本估算：一位受访者估计，确保可复现性可使项目时间增加 **30%**

**⑤ Gundersen & Kjensmo（AAAI 2018，400 篇 IJCAI/AAAI 论文）**：*"None of the papers document all of the variables."*；*"between 20% and 30% of the variables for each factor are documented"*；*"The reproducibility scores decrease with increased documentation requirements."*

### 四、可直接使用的 checklist（融合 Pineau v2.0 + NeurIPS 16 问 + ACM 徽章标准）

**Pineau 的 Machine Learning Reproducibility Checklist v2.0（2020-04-07）逐字六组**：

*For all models and algorithms presented, check if you include:* ① 数学设定/算法/模型的清晰描述；② 任何假设的清晰解释；③ 算法复杂度（时间、空间、样本量）分析。
*For any theoretical claim, check if you include:* ① claim 的清晰陈述；② claim 的完整证明。
*For all datasets used, check if you include:* ① 相关统计量（如样本数）；② 训练/验证/测试划分细节；③ 被排除数据的解释与全部预处理步骤；④ 可下载数据集或模拟环境的链接；⑤ 新采集数据的完整采集过程描述（含标注员指令与质控方法）。
*For all shared code related to this work, check if you include:* ① 依赖规格；② 训练代码；③ 评估代码；④（预）训练模型；⑤ README 含结果表 + 精确复现命令。
*For all reported experimental results, check if you include:* ① 考虑过的超参范围、选取最佳配置的方法、以及产生结果所用的全部超参；② 训练与评估的精确次数；③ 用于报告结果的度量或统计量的清晰定义；④ 含集中趋势（如均值）与离散度（如误差棒）的结果描述；⑤ 每个结果的平均运行时间或估算能耗；⑥ 所用计算基础设施的描述。

**该 checklist 的实用建议（逐字）**：*"For each question, have 2 answer fields. The first one is categorical, with choices: {Yes, No, Not applicable}. The second one is for a free-form comment."*；以及 *"it is recommended to require an initial submission of the checklist at an earlier date, such as with the abstract submission (e.g. 1 week earlier), while allowing authors to update the checklist up to the paper deadline."* 该版本还明确 *"the paper and the code are two separate research artefacts, each with their own checklist."*

**把它改造成"可执行的 checklist"（每条对应一条命令，本组建议）**：

| # | 检查项 | 可执行命令 / 证据位置 | 通过判据 |
|---|---|---|---|
| C1 | 依赖已锁定且含哈希 | `uv lock --check && diff <(uv export -f requirements.txt) requirements.lock` | 退出码 0 |
| C2 | 环境可从零重建 | `docker buildx build --no-cache -t q:test .` | 构建成功 |
| C3 | 运行期无网络依赖 | `docker run --rm --network=none q:test python -m pytest -q` | 全部通过 |
| C4 | 随机性已受控 | 检查 `PYTHONHASHSEED=0` 与代码内 `random.seed` / `numpy.random.seed` | grep 命中 |
| C5 | 账本可复算（精确量） | `python gate_engine.py --replay fixtures/ledger_452.jsonl --print-merkle-root \| diff - fixtures/expected_merkle_root.txt` | 输出为空 |
| C6 | 判决结果可复算（可容差量） | `python gate_engine.py --eval-holdout` | 检出率 ≥ 63.3%（19/30） |
| C7 | 结果表与论文一致 | `python scripts/make_table3.py` 输出与论文表 3 逐格比对 | 逐格一致 |
| C8 | 运行时间已声明 | 实测各步骤耗时，写入 REPLICATION.md | ≤ 30 分钟冒烟 / ≤ 2 小时全量 |
| C9 | 许可证存在 | `ls LICENSE && grep -c "SPDX" README.md` | 存在 |
| C10 | 无遥测/无外联 | `grep -rE "requests\.(get\|post)\|urllib\|telemetry" --include=*.py` | 仅出现在允许清单 |
| C11 | 密钥未泄露 | `gitleaks git --log-opts="--all" .` | 无新增命中 |
| C12 | 已知失败项已声明 | REPLICATION.md 的 `Known failing or degraded checks` 一节 | 非空 |
| C13 | 归档已就绪 | Zenodo DOI 可解析 | HTTP 200 |
| C14 | CI 绿标可见 | Actions 页面 URL 公开可访问 | 200 且最近一次为绿 |

### 五、"checklist 会不会只是形式主义"——证据是分裂的

支持派证据：Nature 2016 问卷中 **"期刊 checklist" 获得 69% 支持**（虽为 11 个选项中最低）；NeurIPS 2019 把 checklist 作为三大组件之一（Pineau 等 JMLR 2021）；SIGMOD ARI 提交率 **25% → 33% → 43%** 三年连升；EuroSys AE 参与率稳定 **58%**。

怀疑派证据：Gundersen & Kjensmo 发现 *"The reproducibility scores decrease with increased documentation requirements."*；Nature 2016 中 **<31%** 认为复现失败意味着原结果错误（说明"复现失败"的诊断力本身受质疑）；ACM 自己承认徽章定义 *"descriptive, not prescriptive"* 导致跨届解释不一致。

**对阙疑的定位建议**：不要把 checklist 当作"合规表演"，而当作**"审稿人可执行的核验脚本清单"**（上表 C1–C14 的每一行都有命令）。这样即使审稿人不信 checklist，也能直接跑命令。**这也正好对齐 NeurIPS E&D 的定位——"evaluation itself becomes an object of scientific study"**：把"我们如何验证自己"当成研究对象，而不是当成表格填写。

---

## 对阙疑的 3 条具体行动

1. **2026-12 前建立 `CHECKLIST.md`，用上表 C1–C14，每条附命令与通过判据**。文件结构：`## Machine-readable checks`（C1/C2/C3/C5/C11 的可执行命令，直接给 CI 用）、`## Human-judgment checks`（C4/C8/C10/C12 需人工确认，附证据路径）、`## Paper-side checklist`（照抄 Pineau v2.0 六组，逐条 Yes/No/NA + 自由文本注释，**并额外附一列"证据位置"**）。**同时把 C5（账本精确复算）与 C6（检出率容差复算）明确分开**，并在论文里写一句："本工作区分两类可复现量：账本 Merkle root 要求逐位一致；检出率类指标允许 ±3.4 个百分点波动（源于规则求值顺序对 Python 哈希种子的敏感性）。"

2. **2027-01 前写 `research/27_reproducibility_checklist.md`，把三个领域基线数字固定下来供论文引用**：① OSC 2015（**97% → 36%**，DOI 10.1126/science.aac4716）；② RP:CB（**0% 方案完整描述 / 2% 公开数据 / 85% 效应量缩水 / 阳性 40% vs 零结果 80%**）；③ ICML 2026 Challenge（**2226 篇 / 51% 至少一 claim 验证 / 23% 被证伪**）。同时记录 ACM 徽章漏斗（EuroSys **161/136/75**，即 84.5% / 46.6%）与 SIGMOD ARI 提交率（**25%→33%→43%**）。**在论文 Introduction 或 Threats to Validity 中用一段把阙疑的工作放到这个背景里**：例如"在 ICML 2026 的 2226 篇复现尝试中 23% 出现 claim 被证伪；本文采用 append-only 哈希链与独立对账器，使判决结果本身可被第三方在不信任内核的前提下复算，从而把'是否成立'从主观判断转为可复算量。"

3. **2027-03 前做一次"徽章可达性评估"，把结论写进投稿策略（2027-05 前定稿）**：逐条对照 ACM 三个徽章自查——(i) **Artifacts Available**：是否已放到 *"publically accessible archival repository"* 并给出 DOI？（GitHub 不算，须 Zenodo/Software Heritage；POPL 2026 逐字强调 *"this is not the same as putting the code on GitHub, GitLab, BitBucket, or your personal website!"*）；(ii) **Functional**：四个词 documented / consistent / complete / **exercisable** 是否都有证据？(iii) **Reusable**：是否 *"significantly exceeds minimal functionality"* 且有社区规范文档（API 文档、扩展指南、非论文用例示例）？**结论写成一张表放进 `research/27_reproducibility_checklist.md`**，明确"哪些能做到、哪些做不到、做不到的写进 Limitations"。注意徽章是**会议可选授予**的，NeurIPS E&D 不采用 ACM 徽章体系，因此**在 E&D 投稿时徽章是加分叙事而非硬指标**——不要把精力全押在徽章上。

---

## 盲区（诚实标注）

- **ACM "Artifacts Available" 的授予是否要求作者主动申请、以及是否在无 AE 的会议上也可申请，未逐字核实**。ACM 原文只说 EIC/Steering Chair/SIG Chair 有权在发表后授予，未说明申请流程。
- **EuroSys 的 161/136/75 是"artifact 件数"而非"论文数"**（一篇论文可提交多件），且 EuroSys 是系统会议，**向 ML 会议外推需谨慎**。
- **SIGMOD ARI 的 "43% in 2025 from 33% in 2024 (and 25% in 2023)" 来自 ACM DL 的会议论文集前言**，本组只取到摘要片段，**未读到各年度的绝对篇数与各徽章的具体获得数**。
- **ICML 2026 Open Reproductions Challenge 的数字来自第三方新闻聚合站（welcome.ai，转自 Hugging Face 内容）**，本组**未找到官方公告页逐字核实**。"51% / 23% / 266 / 632 / 2226 / 6816" 这些数字**在引用前必须找官方来源复核**；且该挑战用 AI agent 自动判定 claim，其判定效度本身未经验证。
- **Nature 2016 问卷的原始页面被 Cloudflare 拦截**，本组读取的是 BioEd Online 的转载版；转载版与原文的差异未核实。问卷本身是**自选样本**（Nature 自己承认 *"probably selected for respondents who are more receptive to and aware of concerns about reproducibility"*），**存在明显选择偏差**。
- **RP:CB 的数字来自 COS 项目页的简化摘要**，其中 "0% of protocols completely described" 的判定口径（何谓"完整描述"）未核实；"85% smaller" 与 "46% replicated" 的具体统计方法未读原文。
- **OSC 2015 的"36%"来自 CASRAI 科普指南的转述**（原始 Science 论文未直读）；且该指南自己指出术语问题：*"The 2015 project tested replicability in this stricter sense, even though its title uses 'reproducibility'"*——**引用时须区分 reproducibility 与 replicability**，否则会被审稿人指出术语误用。
- **Pineau checklist v2.0 PDF 中有一处排版提示**：*"This version (v. 2.0), is renamed the Machine Learning Paper Paper Reproducibility Checklist"*（"Paper" 重复），且文中写 *"For a detailed analysis of the use of version 2.1 of the ML reproducibility checklist at NeurIPS2019: - Add arXiv link."*——**说明该 PDF 是未完成的草稿版本**，"2.0 与 2.1" 的关系未澄清。本组读取的是 v2.0（标注 2020-04-07）。
- **"NeurIPS E&D 不采用 ACM 徽章体系"是本组基于方向 20 检索结果的推断**，官方 CFP 未提及徽章，但也未明文排除。
- **C1–C14 的通过判据（如 ±3.4 个百分点）是本组拟定的示例值，非实测结果**；`PYTHONHASHSEED` 是否真的影响阙疑的规则求值顺序**未实测**（见方向 22 盲区）。

---

## 来源

1. Artifact Review and Badging — Current (v1.1) — https://www.acm.org/publications/policies/artifact-review-and-badging-current — 逐字：*"We recommend that three separate badges related to artifact review be associated with research articles in ACM publications: Artifacts Evaluated, Artifacts Available and Results Validated. These badges are considered independent and any one, two or all three can be applied to any given paper"*；*"Artifacts need not be made publicly available to be considered for this badge. However, they do need to be made available to reviewers."*；Reusable *"significantly exceeds minimal functionality"*；*"exact replication or reproduction of results is not required, or even expected… differences in the results should not change the main claims made in the paper."*；*"Personal web pages are not acceptable for this purpose."*；*"Editors-in-Chiefs and Conference Steering Committee Chairs… will have the authority to award these badges post-publication"*；*"badges included in PDFs and in ACM Digital Library metadata should be linked to a brief explanation of the particular review process"* — ACM — 2020-08-24
2. Lessons from Five Years of Artifact Evaluation at EuroSys — https://www.sigops.org/2025/lessons-from-five-years-of-artifact-evaluation-at-eurosys/ — **161** Artifacts Available / **136** Functional / **75** Results Reproduced；*"A steady 58% of accepted papers participating in AE annually"*；2025 年 **98** 名委员；*"ACM's badge definitions are descriptive, not prescriptive, potentially leading to inconsistent interpretations"* — EuroSys AE Chairs（D'Elia, Doudali, Giuffrida, Matos, Payer, Pirelli, Portokalidis, Schiavoni, Signorello, Vahldiek-Oberwagner）— 2025-08-05；全文 ACM REP '25 DOI 10.1145/3736731.3746152
3. Reproducibility Reports of the 2025 International Conference on Management of Data — https://dl.acm.org/doi/proceedings/10.1145/3785021 — 逐字：*"the overall ARI submission rate has increased to 43% in 2025 from 33% in 2024 (and 25% in 2023)"* — ACM SIGMOD — 2026-02-23
4. ACM SIGMOD Availability & Reproducibility Initiative — https://reproducibility.sigmod.org/ — 逐字：*"Every year, up to three fully reproduced papers with high-quality artifacts are recognized with the 'Best Artifact' award"*；reports 页 *"Following is the list of papers that passed the reproducibility test, the functionality test, and/or have made their [artifacts available]"* — ACM SIGMOD — 2026
5. Reproducibility Reports of the 2024 International Conference on Management of Data — https://dl.acm.org/doi/abs/10.1145/3687998 — 逐字：*"All papers for which the artifacts are made available received the 'Artifacts Available' badge."* — ACM SIGMOD — 2024
6. POPL 2026 Artifact Evaluation — https://popl26.sigplan.org/track/POPL-2026-artifact-evaluation — 逐字：*"Badges are added to papers by the publisher, not by the authors."*；三徽章（Functional / Reusable subsumes Functional / Available in addition）；*"Available… not the same as putting the code on GitHub, GitLab, BitBucket, or your personal website!"* — ACM SIGPLAN — 2026
7. The Machine Learning Reproducibility Checklist (v2.0, Apr. 7 2020) — https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf — 逐字六组共 **22** 条检查项（模型与算法 3 条、理论 claim 2 条、数据集 5 条、代码 5 条、实验结果 6 条 + 一条）与 *"the paper and the code are two separate research artefacts, each with their own checklist"* — Joelle Pineau，McGill — v2.0，2020-04-07
8. Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program) — https://jmlr.org/papers/v22/20-303.html — 逐字：*"The program contained three components: a code submission policy, a community-wide reproducibility challenge, and the inclusion of the Machine Learning Reproducibility checklist as part of the paper submission process."* — Pineau, Vincent-Lamarre, Sinha, Larivière, Beygelzimer, d'Alché-Buc, Fox, Larochelle — JMLR 22(164):1−20, 2021
9. Estimating the Reproducibility of Psychological Science — https://www.science.org/doi/10.1126/science.aac4716 — DOI 10.1126/science.aac4716；**100 项研究 / 约 270 位作者**；**97% → 36%**；效应量约减半；主观复现率约 **39%** — Open Science Collaboration — Science，2015-08-28（**本组读取的是 CASRAI 转述版**：https://casrai.org/guides/psychology-replication-crisis ，2026-08-24）
10. Reproducibility Project: Cancer Biology — https://www.cos.io/rpcb — 逐字：*"193 experiments from 53 papers"*；**2%** experiments with open data；**70%** required asking for key reagents；**69%** of those willing to share；**0%** of protocols completely described；**32%** authors not helpful；**41%** very helpful；**67%** required modifications；**41%** completely implemented；*"50 replication experiments from 23 of the original papers were completed, generating data about the replicability of a total of 158 effects"*；*"Replication effect sizes were 85% smaller on average"*；*"46% of effects replicated successfully on more criteria than they failed"*；*"Original positive results were half as likely to replicate successfully (40%) than original null results (80%)"* — Center for Open Science + Science Exchange — 8 年项目，2026 页面
11. 1,500 scientists lift the lid on reproducibility — https://www.nature.com/articles/533452a（转载：https://www.bioedonline.org/news/nature-news-archive/1500-scientists-lift-the-lid-on-reproducibility/ ）— 逐字：*"More than 70% of researchers have tried and failed to reproduce another scientist's experiments, and more than half have failed to reproduce their own experiments."*；**1,576** respondents；**52%** agree crisis；**<31%** think failure means wrong；psychology ~**40%**、cancer biology ~**10%**（*"The best-known analyses, from psychology and cancer biology, found rates of around 40% and 10%, respectively."*）；**73%** trust half；**<20%** contacted；**24%** published successful replication、**13%** failed；one-third labs acted（medicine **41%**、physics/engineering **24%**）；**>60%** cited pressure to publish & selective reporting；~**90%** endorsed robust design/better stats/better mentorship；journal checklists **69%**（最低）；~**80%** want funders/publishers to do more；时间成本 +**30%** — Nature 533, 452–454，doi:10.1038/533452a — 2016-05-25
12. State of the Art: Reproducibility in Artificial Intelligence — https://ojs.aaai.org/index.php/AAAI/article/view/11503 — 逐字：*"A total of 400 research papers from the conference series IJCAI and AAAI have been surveyed"*；*"None of the papers document all of the variables."*；*"between 20% and 30% of the variables for each factor are documented"*；*"The reproducibility scores decrease with increased documentation requirements."* — Gundersen & Kjensmo，NTNU — AAAI 2018，DOI 10.1609/aaai.v32i1.11503
13. Reproducibility Crisis in AI Research Uncovered by ICML Challenge — https://www.welcome.ai/content/reproducibility-crisis-in-ai-research-uncovered-by-icml-challenge — **2,226** papers；**1,200+** participants；**6,816** logbooks；**51%** had at least one claim verified；**23%** falsified or contested；**266** fully reproduced；**632** partially reproduced without falsifications；ICML 2026 **23,918** submitted / **6,352** accepted — Welcome.AI（**第三方新闻聚合，未核实官方来源**）— 2026-08-13
14. The paper has a GitHub, the GitHub has a README, the README has nothing — https://papers.miccai.org/miccai-2026/paper/0729_paper.pdf — 3,722 篇 MICCAI 论文；**65.5%** 有链接、**54.1%** 有实际代码、**~13%** 空壳 — Bolelli et al.，University of Modena and Reggio Emilia — MICCAI 2026
15. When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation — https://bytez.com/docs/arxiv/2602.16763/paper（arXiv:2602.16763）— 逐字：*"We define benchmark saturation as the loss of reliable discriminative power among top-performing models under comparison."*；**60** 个基准、**14** 个属性；**29** 个高/极高饱和（Sindex ≥ 0.7），其中 **14** 个极高（≥ 0.9）；饱和比例 **42.9%（<24 个月）→ 54.5%（>60 个月）**；*"benchmark saturation is a neutral, not a negative phenomenon"* — 2026（**与本方向的关系：饱和基准会削弱 checklist 中"结果表可复现"的诊断价值**）
