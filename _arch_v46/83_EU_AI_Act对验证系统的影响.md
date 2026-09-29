# 方向 83：EU AI Act 对验证系统的影响

> 调研时间：2026-09-29（GMT+8）
> 联网搜索：11 次（WebSearch）+ 4 次原文核对（WebFetch）
> 法规编号：**Regulation (EU) 2024/1689**（即《人工智能法案》/ AI Act）

---

## 核心结论

**结论一：EU AI Act 是目前全球唯一把「自动记录事件（logs）」「技术文档」「合格评定」写成硬性法律义务的 AI 法规——Article 12 第 1 段明确要求高风险 AI 系统「技术上允许在整个生命周期内自动记录事件」，这正是阙疑「append-only 证据链」的监管级需求来源。**

**结论二：阙疑本身不是「高风险 AI 系统」（它是一个开发者工具，不在 Annex III 的 8 类里），因此不会被直接监管；但阙疑可以成为「高风险 AI 系统提供者的合规工具」——因为 Article 11 + Annex IV 的技术文档、Article 12 的日志、Article 15 的准确性要求，都需要可复算的证据。**

**结论三：时间窗口被 Digital Omnibus（2026）推后了——Annex III 高风险义务从 2026-08-02 推迟到 2027-12-02（推迟 14 个月），Annex I 从 2027-08-02 推到 2028-08-02（推迟 22 个月）；这意味着阙疑的合规叙事窗口比原计划多出约 14 个月，但 GPAI 义务（Article 53）与透明度义务（Article 50）已经在 2025-08-02 / 2026-08-02 生效，是当前唯一「已经落地」的抓手。**

---

## 精确数字与案例

### 1. 时间表：Article 113 的原始日期 + Digital Omnibus 的四项推迟

**Regulation (EU) 2024/1689 于 2024-07-12 在《欧盟官方公报》发布，2024-08-01 生效（entry into force）**，之后分阶段适用（application）。

| 日期 | 原定义务 | Digital Omnibus 后 | 状态 |
|---|---|---|---|
| **2025-02-02** | 禁止性实践（Article 5）+ AI 素养 | 不变 | 已生效 |
| **2025-08-02** | GPAI 模型义务（Chapter V, Art. 51–56）、治理、保密性（Art. 78）、部分处罚（Art. 99–100） | 不变 | 已生效 |
| **2026-08-02** | AI Act 其余部分；透明度义务（Article 50）；委员会对 GPAI 的执法权 | Article 50 不变（已生效）；存量系统的内容标识宽限至 **2026-12-02** | 部分已生效 |
| **2026-08-02** | 国家 AI 监管沙盒（Art. 57） | **推迟至 2027-08-02**（推迟 10 个月） | 已延期 |
| **2026-08-02** | Annex III 独立高风险系统 | **推迟至 2027-12-02**（推迟 14 个月） | 已延期 |
| **2027-08-02** | Annex I 嵌入式高风险系统 | **推迟至 2028-08-02**（推迟 22 个月） | 已延期 |
| **2026-12-02** | Article 5(1)(ba)(bb)、5(1a)(1b)（非自愿亲密图像 / CSAM） | 不变 | 待生效 |

**Digital Omnibus 的三条官方延期理由**（据 regulation-ai.eu 整理）：
1. **标准未就绪**——Article 40 要求的协调技术标准（harmonised standards）未在原定 2026-08 前定稿，导致合格评定无法完成；
2. **执法基础设施缺口**——公告机构（notified bodies）尚在指定与认可过程中；
3. **产业与中小企业准备度**——DORA（2025-01）、NIS2（2024-10）叠加，负担过重。

**⚠️ 重要提醒**：`artificialintelligenceact.eu` 的官方实施时间表页面（更新至 2026-08-31）**未提及 Digital Omnibus**，仍列 Annex III 为 2027-12-02 / Annex I 为 2028-08-02（其页面已把这两个日期写进 Article 12 与 Article 113(c) 的「Comes into force」标注）。这说明**Omnibus 的修改已经反映在部分条款页，但主时间表页未同步**——引用时需注明来源与日期。

### 2. 与阙疑最相关的条款：Article 12（记录保存）

**Article 12 第 1 段（原文）**：「High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system.」
（高风险 AI 系统应技术上允许在整个生命周期内自动记录事件（日志）。）

**第 2 段**要求日志能力至少能记录三类事件：
- (a) 识别可能导致风险（Article 79(1)）或重大修改（substantial modification）的情形；
- (b) 支持 Article 72 的上市后监测（post-market monitoring）；
- (c) 支持 Article 26(5) 的运营者监测。

**第 3 段（针对 Annex III 第 1(a) 点，即远程生物识别）**要求日志至少记录：
- (a) 每次使用的时间段（起止日期时间）；
- (b) 系统核对的参考数据库；
- (c) 产生匹配的输入数据；
- (d) **参与结果验证的自然人身份**（依 Article 14(5)）。

**对阙疑的意义**：Article 12 的「自动记录 + 可追溯 + 参与人身份」三要素，与阙疑的「append-only 哈希链 + 证据带 provenance」在结构上同构。**阙疑的哈希链设计可以直接映射为 Article 12 的合规实现**——这是阙疑最强的「卖点翻译」。

### 3. 技术文档：Article 11 + Annex IV

- **Article 11(1)**：高风险 AI 系统的技术文档应在该系统投放市场或投入使用前编制，并保持更新；**至少包含 Annex IV 所列要素**。
- **Article 11(2)**：中小企业（SMEs，含初创企业）与小型中型企业（SMCs）可**以简化形式**提供 Annex IV 要素；委员会应为此建立简化表格。
- **Annex IV** 涵盖：系统的一般描述、详细描述（开发方法、设计规格、架构、数据要求）、监测/运行/控制信息、风险管理描述、上市后变更、已采用的协调标准清单、EU 符合性声明副本等。

**对阙疑的意义**：Annex IV 的「协调标准清单」一项意味着**如果阙疑能成为一个协调标准的参考实现，就能获得「presumption of conformity」的地位**。

### 4. 高风险要求（Article 8–15）全表

| 条款 | 标题 | 核心要求（对阙疑的映射） |
|---|---|---|
| Article 8 | 合规要求 | 高风险系统须符合 Section 2 要求 |
| **Article 9** | 风险管理系统 | 须建立、实施、文档化并维护**贯穿全生命周期的持续迭代过程**；含识别、分析、评估、缓解 |
| **Article 10** | 数据与数据治理 | 训练/验证/测试数据集须符合质量标准（相关性、代表性、无偏、完整） |
| **Article 11** | 技术文档 | 见上（Annex IV） |
| **Article 12** | 记录保存 | 见上（自动日志） |
| **Article 13** | 透明度与向部署者提供信息 | 须提供足以让部署者理解能力与局限的信息 |
| **Article 14** | 人类监督 | 须设计为可被自然人有效监督（含「停止」能力、自动化偏差的防范） |
| **Article 15** | 准确性、鲁棒性、网络安全 | 须在其整个生命周期内达到**适当水平的准确性**，并在技术文档中**声明准确度指标与水平**；须对错误、故障、不一致具有鲁棒性；须抗未授权访问 |

**Article 15 的关键词是「declare the accuracy metrics and the level of accuracy」**——即**必须公开声明准确度数字**。这与阙疑论文 v0.3 的做法（公开 holdout 66.7% / corpus 43.8% / 反事实 P=R=F1=0）**方向一致，但阙疑做得更彻底（连负结果都公开）**。

### 5. 合格评定：Article 43

- 对 **Annex III 第 2–8 点**的高风险系统：提供者须遵循**基于内部控制的合格评定程序**（Annex VI）；
- 对 **Annex III 第 1 点**（生物识别）的系统：若已应用协调标准，可走内部控制；否则须**涉及公告机构（notified body）的合格评定**（Annex VII）；
- 对 **Annex I** 覆盖的系统：须遵循**已有的部门立法**下的合格评定程序。

**对阙疑的意义**：合格评定的核心是「**第三方可复算的证据**」——这正是阙疑「独立对账器」的定位。

### 6. 罚款：Article 99 三档

| 档位 | 上限 | 适用 |
|---|---|---|
| 最高档 | **€35,000,000 或全球年营业额 7%**（取高者） | 违反 Article 5 禁止性实践 |
| 中档 | **€15,000,000 或全球年营业额 3%**（取高者） | 违反大部分其他义务（含高风险要求、GPAI 义务等） |
| 低档 | **€7,500,000 或全球年营业额 1%**（取高者） | 向监管机构提供不正确/不完整/误导性信息 |

**对阙疑的意义**：**中档 3% 全球营业额**是悬在所有高风险 AI 提供者头上的剑。一个「可被独立复算的验证证据包」可以直接降低这项法律风险——这是阙疑商业化叙事里最硬的一句话。

### 7. GPAI 义务：Article 51–56（已于 2025-08-02 生效）

**Article 53（GPAI 模型提供者义务）第 1 段**：
- (a) 编制并更新模型技术文档，含**训练与测试过程及评估结果**，至少包含 Annex XI 所列信息，供 AI Office 与国家主管机构索取；
- (b) 向下游 AI 系统提供者提供信息与文档，至少包含 Annex XII 要素，使其能理解模型能力与局限；
- (c) 制定遵守欧盟版权法的政策，包括通过**最先进技术**识别并遵守 Directive (EU) 2019/790 Article 4(3) 的权利保留（reservation of rights）；
- (d) 编制并**公开**一份关于训练内容的**足够详细的摘要**，按 AI Office 提供的模板。

**第 2 段（开源例外）**：第 1 段 (a)(b) **不适用于**以自由开源许可发布、且参数（含权重、架构信息、使用信息）公开的模型；**但该例外不适用于有系统性风险的 GPAI 模型**。

**第 3 段**：GPAI 提供者须与委员会和各国主管机构合作。
**第 4 段**：可通过遵守 Article 56 的**行为准则（codes of practice）**证明合规；协调标准发布后，遵守标准可获得**合规推定（presumption of conformity）**。
**第 7 段**：所获信息（含商业秘密）按 Article 78 保密处理。

**Article 51（系统性风险分类）**：训练累计算力 **> 10^25 FLOP** 即被推定为具有高影响能力（high-impact capabilities），构成系统性风险；委员会也可依职权指定。

**对阙疑的意义**：**「评估结果必须写进技术文档」**（Article 53(1)(a)）是阙疑的直接机会——如果阙疑的验证报告格式能对齐 Annex XI，就能成为 GPAI 提供者的现成工具。

### 8. Annex III 的 8 类高风险

Annex III（依 Article 6(2)）列出的 8 个领域：
1. **生物识别**（Biometrics）——含远程生物识别、情绪识别（部分）；
2. **关键基础设施**（Critical infrastructure）——能源、水、交通等安全管理组件；
3. **教育**（Education and vocational training）——录取、评估、监考等；
4. **就业与人力资源**（Employment）——招聘、筛选、绩效评估、解雇；
5. **基本公共服务**（Essential services）——含信用评分、保险定价、紧急服务调度等；
6. **执法**（Law enforcement）；
7. **移民与边境管理**（Migration, asylum and border control）；
8. **司法与民主进程**（Administration of justice and democratic processes）。

**重要豁免**：Annex III 第 5(b) 点**明确排除**用于检测金融欺诈的 AI；第 1 点排除一对一生物特征验证；算法交易不在 Annex III 中。

**对阙疑的意义**：**C++ 代码验证工具不在上述 8 类中，因此阙疑不是高风险系统，不受直接监管**。这一点必须在论文里写清楚——**它让阙疑可以自由地公开负结果，而不承担 Article 15 的「声明准确度」法律责任**。

### 9. 协调标准：CEN-CENELEC JTC 21

- **CEN 与 CENELEC 的联合技术委员会 JTC 21**（官网 jtc21.eu）负责制定支持 AI Act 的欧洲标准；
- 欧盟委员会页面（2025-10-30 更新）说明：CEN 与 CENELEC 发布协调标准后，委员会评估其是否满足要求，随后在《欧盟官方公报》引用，方产生合规推定；
- **Digital Omnibus 的第一条延期理由就是「标准未就绪」**——这意味着 2026 年内 JTC 21 的标准仍未定稿。

**对阙疑的意义**：**标准未定稿 = 定义权窗口仍开着**。阙疑若能以「独立对账协议」的形式向 JTC 21 提交意见，是低成本高回报的动作。

---

## 对阙疑的 3 条具体行动

**行动 1：新增一份 `compliance_mapping.md`，把阙疑的每个产出物映射到 EU AI Act 的具体条款。**
- 具体做法：在 `_arch_v46/`（或 `research/`）下建立映射表，至少覆盖：
  - 哈希链 → Article 12(1)「automatic recording of events (logs) over the lifetime」
  - 证据带 provenance → Article 12(2)(a)「identifying situations that may result in risk」
  - 四态判决 → Article 15「declare the accuracy metrics and the level of accuracy」
  - 技术文档结构 → Article 11(1) + Annex IV
- 时间点：2026-12 前。
- 理由：**这是把技术语言翻译成法律语言的唯一路径，也是论文 Related Work 里最有说服力的一段。**

**行动 2：把「阙疑不是高风险系统」写成论文的显式声明，并附 Annex III 逐条排除说明。**
- 具体做法：在论文 Threats to Validity 或 Scope 章节新增一段，列出 Annex III 的 8 类并说明阙疑均不落入；同时引用 regulation-ai.eu 的 Annex III 第 5(b) 点金融欺诈豁免作为「附件确实存在豁免」的旁证。
- 理由：**审稿人（尤其是来自监管/法律背景的）会问「你这算不算高风险」**；提前答掉，减少一个拒稿理由。
- 时间点：投稿前 1 个月。

**行动 3：以「Annex XI 对齐」为目标，重排阙疑的验证报告输出格式。**
- 具体做法：阅读 Article 53(1)(a) 与 Annex XI，把 `gate_engine.py` 的报告输出（建议新增 `--format annex-xi`）调整为包含「训练与测试过程 + 评估结果」的字段结构。
- 理由：**GPAI 义务已于 2025-08-02 生效，是当前唯一「已经落地」的抓手**；对齐 Annex XI 能让阙疑直接切入 GPAI 提供者的合规流程。
- 时间点：2027-03 前。

---

## 盲区（诚实标注）

1. **Digital Omnibus 的日期变更**来自第三方解读站 `regulation-ai.eu`（更新至 2026-09-12），**未在 EUR-Lex 上核对 Omnibus 正式文本编号与 OJ 发布日期**。该站自称「Editorial, not legal advice」。**引用 2027-12-02 / 2028-08-02 这两个日期时必须注明「据 Digital Omnibus 2026，未在 EUR-Lex 二次核实」**。
2. **`artificialintelligenceact.eu` 官方时间表页（2026-08-31 更新）未提及 Omnibus**，但其 Article 12 / Article 113 页已把 Annex III 写成 2027-12-02。**两处存在信息不同步**，我无法判断哪一处是「最终状态」。
3. **Annex III 的 8 类分类标题**来自多个二手解读站（confir.eu / euai.app / aiactinfo.eu）的汇总，**未逐字核对 EUR-Lex 的 Annex III 原文**；8 类的精确边界与子项（如第 1 点的 1(a)/1(b) 区分）我**只确认了第 1(a) 点与第 5(b) 点的存在**。
4. **Article 99 的三档罚款金额**（€35M/7%、€15M/3%、€7.5M/1%）来自多个合规解读站，**未在 EUR-Lex 核对 Article 99 原文**；「取高者（whichever is higher）」的表述我采信二手来源。
5. **Article 51 的 10^25 FLOP 阈值**来自多个解读站（casrai.org / regulatoryai.eu / confir.eu / deepinspect.ai），**未核对 Article 51 原文的「推定」措辞**（是 presumption 还是 hard threshold，我采信「presumption」）。
6. **CEN-CENELEC JTC 21 的标准清单与进度**我**未打开 jtc21.eu 的具体标准编号列表**，因此**无法给出任何标准编号（如 prEN xxxxx）**——这是一个明确的未核实项。
7. **Article 43 的合格评定路径**（Annex VI / VII 的分配）来自二手解读，**未核对原文**。
8. **「Digital Omnibus 2026」的正式法律形式**（是否为 Regulation 或 Directive、是否有正式编号）**未查到**。
9. **Article 12 的生效日期**在 artificialintelligenceact.eu 上被标注为「2 December 2027 (Annex III) / 2 August 2028 (Annex I)」，**这本身可能就是 Omnibus 后的状态**，但页面未说明，属推断。

---

## 来源

1. European Union. *Regulation (EU) 2024/1689*（AI Act）. OJ 2024-07-12；生效 2024-08-01.
2. *Article 53: Obligations for Providers of General-Purpose AI Models*. https://artificialintelligenceact.eu/article/53/ （原文核对，2026-09-29）
3. *Chapter III: High-Risk AI Systems*. https://artificialintelligenceact.eu/chapter/3/ （原文核对，2026-09-29）
4. *Article 12: Record-Keeping*. https://artificialintelligenceact.eu/article/12/ （原文核对，2026-09-29）
5. *Implementation Timeline*. https://artificialintelligenceact.eu/implementation-timeline/ （更新至 2026-08-31，**未含 Omnibus**）
6. *EU AI Act Digital Omnibus 2026: What It Changes*. https://www.regulation-ai.eu/en/omnibus/ （更新 2026-09-12）
7. European Commission. *Digital Omnibus on AI Regulation Proposal*, 2025-11-19. https://digital-strategy.ec.europa.eu/en/library/digital-omnibus-ai-regulation-proposal
8. *EU's Digital Omnibus proposes major delay to AI Act high-risk rules*. CADEP, 2025-11-19. https://cadeproject.org/updates/eus-digital-omnibus-proposes-major-delay-to-ai-act-high-risk-rules/
9. European Commission. *Standardisation of the AI Act*, 2025-10-30. https://digital-strategy.ec.europa.eu/en/policies/ai-act-standardisation
10. CEN-CENELEC JTC 21. https://jtc21.eu/
11. *Article 99: Penalties*. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-99
12. *EU AI Act penalties: Article 99 fines (€35M / €15M / €7.5M)*. https://www.witness-compliance.eu/en/eu-ai-act/penalties
13. *Annex III: High-Risk AI Systems Referred to in Article 6(2)*. https://artificialintelligenceact.eu/annex/3/
14. *Annex IV: Technical Documentation Referred to in Article 11(1)*. https://artificialintelligenceact.eu/annex/4/
15. *Article 43: Conformity Assessment*. https://artificialintelligenceact.eu/article/43/
16. European Commission. *Guidelines for providers of general-purpose AI models*, 2026-04-28. https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers
17. *EU AI Act Article 51 — GPAI models with systemic risk explained*. https://www.regulatoryai.eu/article-51-explained/
