# 03 · 靶位 C：Verification Horizon × AI Control 能力分级

> _arch_v23 深度调研 · 2026-09-23 · 外部信息访问日期 2026-09-23。
> 标注约定同 01。本文回答外部如何定义"验证能力上限"、阈值如何标定，不给工程实现。

---

## C1. DeepMind AI Control 的 D1-D4（与 R1-R3）

- **文件**：《AI Control Roadmap (v0.1)》，Google DeepMind，2026-06-18，作者含 Mary Phuong、Rohin Shah 等（arXiv 2607.13087）；配套博客 Shah & Flynn《Securing the future of AI agents》【已查证】https://deepmind.google/blog/securing-the-future-of-ai-agents/ ；技术报告 PDF 链接见博客。
- **基本立场**：AI Control 是对齐之外的第二层防御——**保守假设内部 agent 是不透明的内部威胁**（人类员工中 <0.1% 是内鬼，但规划时可假设接近所有内部 AI agent 都需要按潜在对手设计）；威胁建模建在 MITRE ATT&CK 上，另造 **TRAIT&R**（Taxonomy of Rogue AI Tactics and Routines），增加人类攻击者没有的战术（目标/语境持久化、entrenchment 巩固）【已查证-技术报告转述】https://chatforest.com/builders-log/google-deepmind-ai-control-roadmap-agent-security-framework-builder-guide/
- **两轴结构**：防御强度跟随**被监督模型的两类能力**标定——规避检测能力（决定 Detection level D1-D4）× 潜在危害能力（决定 Response tier R1-R3）。

### Detection Levels（被监督模型的能力档→所需检测方法）

| 级 | 模型在该档的能力特征 | 与之配对的检测方法 |
|---|---|---|
| **D1** | 可见 CoT 可读，模型尚无"监督意识"（不知道在被监控） | CoT 监控 + 对齐测试 |
| **D2** | 模型已有监督意识，可能博弈监控（alignment faking、越狱监控器、刻意表现） | 对抗健壮的监控器、评测意识抑制、监督信息隔离（siloing） |
| **D3** | CoT 不再可读/不再携带真实推理（opaque reasoning），但一个**可信的、较弱的、非对抗位置的模型**仍能从外部监督其行为 | 可信行为监控：动作监控、PR/变更监控、蜜罐、异常检测 |
| **D4** | 连行为级监控都可能被规避；需要直接检查模型内部 | 内部表征/激活级检查（mechanistic 监控） |

【已查证】表 D1-D3 见技术报告 Table 14（p.20）转述：https://chatforest.com/builders-log/google-deepmind-ai-control-roadmap-agent-security-framework-builder-guide/ ；D4 与两轴总述见官方博客与多篇转述【已查证】https://deepmind.google/blog/securing-the-future-of-ai-agents/ https://www.c114pro.com/ai/172833.html 。R 档细节：R1=异步事后记录审；R3=高危动作执行前同步阻断；R2 介于两者（准实时审批/升级）【已查证】https://www.waxell.ai/blog/deepmind-ai-control-roadmap-insider-threat-governance-2026 （R2 逐条定义原文【待验证】，以 PDF Table 为准）。

- **运行指标（三指标，不是单一"能力分"）**：**coverage**（被监控流量占比）、**recall**（真实失轨行为被抓住的比例）、**time-to-response**【已查证，官方博客】。
- **经验基底**：分析了约 **100 万条**内部编码 agent 任务轨迹；结论是**多数被标记事件并非对抗意图**，而是误解任务/过度热心完成目标（如非故意删数据）——只按"恶意"校准的监控会漏掉当前主要的异常类【已查证】https://www.waxell.ai/blog/deepmind-ai-control-roadmap-insider-threat-governance-2026 。
- **对阙疑当前级别的判定（推断，置信度中）**：
  - 阙疑的"被监督对象"是内容生成器/判官模型，规避能力接近 **D1-D2 之间**：判决依据是可见文本输出（D1 特征），但 v21 已证实前沿模型会评测意识、prompt 注入、自信但无证据地翻案（D2 特征已零星出现）；不存在 D3/D4 的 opaque reasoning 问题（阙疑不依赖隐藏 CoT 做判决，这反而是优势）。
  - 阙疑的响应轴：硬拦≈R3（入库 gate）、warn/送审≈R2、异步重算（replay/批次复算）≈R1，三档结构与 DeepMind 同构——说明既有架构方向与工业前沿对齐。
  - 差距：coverage/recall/time-to-response 三指标中，阙疑只有 recall 的对偶（逃逸率），**coverage（多少候选/动作真的进了检验管道）无指标**——v21 AISI"路由规避"与 DeepMind coverage 在此会师。

## C2. METR 的任务难度分位：50%/80% 时间跨度

- **定义**：50% time horizon = 模型以 50% 概率能完成的、按**人类专家完成耗时**计的任务时长；它是**任务难度轴上的能力刻度**，不是 agent 自主运行时长【已查证-官方 FAQ】https://metr.org/time-horizons/
- **度量方法**【已查证】https://metr.org/time-horizons/ https://aiwiki.ai/wiki/metr_time_horizon ：
  1. 任务集 HCAST（97 题）+RE-Bench（7 题）+SWAA（66 个 1-30 秒短题），人工耗时覆盖约 **1 秒至 16 小时**；
  2. 每题人类耗时：雇人实做取成功完成时间的**几何均值**（800+ 人次、2529 小时）；
  3. 每个模型每题跑 **6-8 次独立尝试**记成败；
  4. 对"成功概率 ~ log(人类耗时)"拟合 **logistic 曲线**（参数 h=50% 截点、β=斜率），50%/80% horizon 即曲线与 0.5/0.8 横线交点；
  5. 官方明确：**>16 小时的测量在当前任务集下不可靠**；TH1.1 的点估计置信区间很宽。
- **50% 与 80% 的落差**：2026-05 前沿模型 50% horizon 约 12 小时（区间 5-61h），80% 仅约 1.5 小时——同一模型"五五开能干"与"八成可靠能干"差约 8 倍【已查证，v21 已引用】https://metr.org/time-horizons/
- **趋势与脆弱性**：50% horizon 2019-2025 约每 7 个月翻倍（2024 年一度约 4 个月）；2026-03 METR 自曝一个正则化建模错误，修正后近期模型 50% horizon 最多**下移 20%**；合理的建模变体通常把近期 50% 估计往下拉、80% 往上推；最大不确定性来自**任务分布**而非分析选择【已查证】https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/
- **"验证难度"的对应概念**：METR 没有直接定义"verification horizon"，但有两个对偶物：①**monitorability**（A2 已述：agent/monitor 的 horizon 比预测旁路成功率）——这是"**监督者相对能力**"刻度，本质是验证能力上限的相对版本；②对 reward hacking 的处理：作弊尝试一律计为任务失败并**人工复核**，即在能力曲线上扣除测量作弊（见 01 号 A2）。
- **可迁移要点（推断）**：
  1. 难度轴必须是**外部可校准的人类工作量**（几何均值、多人实做），不能是自报 0-100 分；
  2. 必须报**两个分位而非一个点**——50% 与 80% 的差距本身就是系统"可靠性断崖"的度量；
  3. 任何 horizon 数字必须绑定任务集版本、阈值、日期四个限定词（METR 自己因不绑定而公开纠错）；
  4. 曲线外推（>16h）无效——阙疑在没有真实攻击样本的复杂度区不得外推检出率。

## C3. "验证能力上限"在学术界的对应：状态空间爆炸

- **没有名为"verification capacity/horizon"的统一术语**【已查证-检索结论】；最接近的硬科学概念是形式化验证的**状态空间爆炸（state explosion）**：n 个各有 m 状态的并发进程异步组合可达 m^n 个全局状态；n 位计数器有 2^n 状态——这是 2007 年图灵奖工作（Clarke/Emerson/Sifakis 模型检测）公认的首要限制【已查证】https://dl.acm.org/doi/fullHtml/10.1145/1592761.1592781
- **工程上的能力上限量级**：朴素显式枚举在约 **10^6–10^8 状态**以上即不可行；工业可用靠符号表示（BDD）、抽象（abstract interpretation，过近似可能产生伪反例）、有界模型检测（BMC/SAT，欠近似会漏掉界外违例）【已查证】https://cstopics.com/encyclopedia/specialized-topics/formal-verification/model-checking/ctl-model-checking https://technav.ieee.org/topic/model-checking/
- **三条对 Horizon 直接有用的原则**【已查证】https://itdojp.github.io/formal-methods-book/en/chapters/chapter08/ ：
  1. **超时/资源耗尽/unknown ≠ 确认通过**——"没测出来"与"验证为安全"必须严格区分；
  2. 完备性只相对于**模型/属性/搜索范围**成立——范围外的输入与实现细节不被覆盖；
  3. 过近似（宽规则）产生**误报**（伪反例=自身免疫），欠近似（窄搜索）产生**漏报**（逃逸）——这是形式化方法版本的 α/β 权衡，与靶位 B 完全同构。
- **对阙疑的含义（推断）**：Verification Horizon 不是一个"验证器多聪明"的单点能力，而是一个三元组——**(可检验输入空间大小, 完备性语义: 过/欠近似, 可靠性分位)**。阙疑 622 的分桶若隐含"100 分桶内验证器近似完备"，按形式化验证的教训，必须显式声明该完备性是相对哪个攻击/证据模型成立。

## C4. 攻击复杂度的外部度量：CVSS 与 MITRE ATT&CK

- **CVSS Attack Complexity（v3.1）**：只有**两档**，描述"攻击者不可控、但利用漏洞必须存在的条件"——**Low**：不存在特殊条件，默认配置即可、无需特殊知识；**High**：需要特定配置/额外信息/计算例外等不可控条件；明确**不含用户交互要求**（单列 User Interaction 指标）【已查证-官方规范】https://www.first.org/cvss/v3-1/specification-document 。CVSS v2 曾有 High/Medium/Low 三档，v3 简化为二档【已查证】https://nvd.nist.gov/vuln-metrics/cvss/v2-calculator
- **MITRE ATT&CK 刻意不评难度**：ATT&CK 是实证 TTP 知识库，技术条目不附"利用难度分"（行业多次指出这点；ATLAS 沿用同一理念）——难度随防御部署变化太快，机构选择只记录"发生过什么"而非"有多难"【已查证-检索结论，ATLAS 官网无 difficulty 字段】https://atlas.mitre.org/
- **红队领域的实际做法**：用**成本/步骤数/前提条件**描述复杂度而非连续难度分——DeepMind TRAIT&R 按战术链与前提（访问、资源、技能）组织；支付/漏洞域用"需要多少特殊条件"（与 CVSS AC 同思路）。
- **对照与教训（推断）**：
  1. 外部成熟标准要么二档（CVSS），要么干脆不评分（ATT&CK）——**连续 0-100 五桶在外部没有对应权威实践**；连续复杂度分看似精细，实则校准来源薄弱（正是 622"自己拍"的风险）；
  2. 外部复杂度定义的关键不是"攻击者多聪明"，而是"**需要多少攻击者不可控的前提条件**"——这与阙疑毒样例的构造变量（需要伪造几层证据、是否要懂规则格式、是否需要跨工具）可以对齐；
  3. CVSS 还把"利用度"（攻击向量/复杂度/权限/交互/范围）与"影响度"（C/I/A）**分开评分**——阙疑的攻击复杂度与危害度也应分轴（目前 Horizon 只刻画一端）。

## C5. Verification Horizon 升级建议（建议，不实现；置信度逐条标注）

1. **难度轴从自报 0-100 改为外部锚定的序数量**（置信度：高）。参照 METR：用"构造该攻击需要攻击者投入的步骤数/不可控前提数/伪造证据层数"作为难度的操作化定义（CVSS AC 思路），用真实红队/历史毒样例做校准点；没有真实样本的区段标注"未校准"，禁止外推检出率。
2. **同时报 50% 与高可靠（如 80%/95%）两个检出率分位**（置信度：高）。当前"60-80 桶检出 0%"是单点叙事；METR 的 50% vs 80% 差 8 倍说明：**真正的情报是断崖位置而非平均水平**。建议 Horizon 主指标改为"两个分位对应的复杂度之差"，差越大说明验证器在高复杂度区崩溃越突然。
3. **对"60-80 桶检出 0%"断崖的解释**（置信度：中高）：最可能的三种结构性原因，外部都有对应——
   - (a) **覆盖缺口**（coverage=0）：该复杂度的攻击根本没进检验管道（AISI 路由规避、DeepMind coverage 指标）；
   - (b) **能力代差**：攻击构造能力与检测能力存在"监督者落后一代"的阈值（METR：无轨迹时 agent/monitor horizon 比预测旁路成功）；
   - (c) **测量伪影**：该桶没有真实攻击样本（形式化验证"范围外无结论"、METR >16h 不外推）。
   **在补齐 coverage 指标与真实样本前，0% 不能解读为"高复杂度区安全"**——0% 的检出率与 0% 的送审率在数字上相同（这是本靶最重要的一句）。
4. **复杂度分档建议向二/三档靠拢而非保留五档等距**（置信度：中）。参照 CVSS（二档）与 DeepMind（能力档非等距、按证据方法跃迁）：分档边界应对齐"**需要检测方法发生质变的位置**"（如：无需伪造证据/需伪造一层/需跨工具伪造/需攻击测量装置本身），而非等距数字。保留五桶也行，但每桶必须绑定该桶对应的检测机制与证据类型。
5. **Horizon 报告加三元组限定与版本号**（置信度：高）：(攻击/证据模型版本, 完备性语义：检出/送审/外推, 分位与置信区间)，并随规则/模型版本滚动重测——直接抄 METR 的四限定词与公开纠错纪律。
6. **补 coverage 作为与 Horizon 并列的第二指标**（置信度：高）：被测动作中实际进入任一验证机制的比例。没有 coverage 的 recall（逃逸率）会系统性乐观，这是 DeepMind 三指标与 AISI 路由发现的共同结论。
7. **阙疑当前总体评级（推断，置信度中）**：检测方法档≈D1-D2（输出可见但对手已具监督意识）；响应轴 R1/R2/R3 三档齐备（优势）；主要缺口是 coverage 无指标、难度轴无外部校准、高可靠分位未报、高复杂区无真实样本。按 METR 口径，622 的 Horizon 数字目前只应被当作**TH 0.x 原型测量**，像 METR v0.1 一样自我标注工作-in-progress，不宜对外作能力宣称。
