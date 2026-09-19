# 551 · 质变调研（三）：给知识层装数学 —— 论证语义 / 信念修正 / 声明式约束，与一个统一锚点

> 549 给放权刻度盘，550 给验证强度脊柱。本轮强迫自己跳出验证/统计，向外广搜，挖到系统更深的空洞：**知识层现在只有数据结构（nodes/edges/concepts 四表、frontmatter），没有"推理、裁决、撤回"的数学**。三套 1979-1995 的经典符号 AI 框架恰好对症，且它们与 2026 的 LLM 前沿、安全工程、科学方法论一起，惊人地收敛到同一个锚点。检索 2026-09-16。

## 〇、一句话总览（本轮真正的洞察）
三套框架各自需要一个"谁更强/谁更可信"的排序：Dung 论证需要**偏好序**来裁决冲突，AGM 信念修正需要**认知稳固序**来决定先撤谁，SHACL 需要约束的**严重度**。而 550 定的 **S0-S7 验证强度阶梯正好同时充当这三者**——**一个数字三处复用**：它既决定"一条 claim 必须拿出几级证据"，又决定"两条结论打架时谁击败谁"，还决定"地基塌的时候谁先倒"。这把验证阶梯从一个"检查表"升级成整个知识层的统一货币。

## 一、Dung 论证语义：冲突中"哪些结论站得住"的数学
**来源**：Dung 1995 abstract argumentation（只需"论证集 + 攻击关系"即可计算可接受性，不看论证内部内容）；ASPIC+（前提/严格规则/可废止规则构造论证）；SEP defeasible reasoning；已有 2026-07 工作把 Dung 语义用于 AI alignment 目标冲突；概率化 Dung 框架。
**机制**：
- 一个论证集 **admissible（可接受）** = 内部无冲突（conflict-free）+ 能反击所有攻击者（defends itself）；grounded/preferred extension 给出理性可接受的结论集合（grounded 语义可多项式计算）。
- ASPIC+ 区分三种攻击，**这个区分对本系统是钥匙**：
  - **rebut（反驳结论）**：两论证结论直接矛盾 → 对应 `contradicts/conflicts_with`；
  - **undercut（削根，攻击推理规则本身是否适用）**：不否认结论，否认"前提能推出结论" → **红队大多数动作是 undercut**：恒真断言、cat 证据、自标 observation，都是"你的 confirm 推导不成立"，而非"结论本身错"；
  - **undermine（挖前提）**：攻击前提/证据为假 → 工件被清空（E13）、sha 不符、fixture 造假。
**对系统**：515 的 ATOM-REL-CONFLICT 只能查"A 依赖 B 且 B 反驳 A"这种简单环，是手写图遍历。Dung 框架能回答更深的问题：**在所有互相攻击的论证（claim/证据/红队发现）里，哪些最终落在可接受集里？** 偏好序 = 证据强度（S0-S7）：一个 S6 BMC 证明的论证击败 S1 自报的反驳；同强度冲突则都不进 grounded（挂起等人）。零 LLM，纯图算法，与 knowledge_graph 四表天然契合。
**边界**：Dung 只给"形式上可接受"，不给"事实为真"；偏好序必须来自客观证据强度而非模型自述（否则 reward hacking）。

## 二、AGM / 真理维护系统（TMS）：证据塌了怎么级联撤回
**来源**：Doyle TMS 1979（记录每条信念的 justification，矛盾时精确撤回受影响结论集）；AGM 信念修正（contraction 最小扰动移除 / revision 加信念且保持一致 / epistemic entrenchment 越稳固越难撤）；KriraAI RECAP 2026-07（justification tracing 让 LLM agent 信念修正，明确"注意力权重是错误的依赖信号，需显式依赖结构"）。
**机制**：撤回一条基础事实时，按支持路径分三类反应：① 结论无其他支持路径 → 撤销/标 needs_review；② 还有其他路径 → 保留但缩小支持集；③ 用户直接断言的基础事实 → 不被派生规则自动撤回。
**对系统**：现在一颗证据被红队打穿/工件失效（如 E13 工件被清空），依赖它的原子、概念、inference 该级联重审——impact_analysis.py 只做依赖遍历，没有"信念撤回"。落地：knowledge_graph 为每条结论维护 **support set（由哪些证据/签署支撑）**，证据失效时按上面三规则传播，并以 S0-S7 为 entrenchment（高证据级结论更难被一条弱反驳撤掉）。这正是 L4"进化"里"自我修正"的确定性内核，零 LLM。

## 三、SHACL：把散落的图校验收敛成声明式约束（closed-world）
**来源**：W3C SHACL 1.2（closed-world、约束导向，验证 RDF 图）；OWL 是 open-world 推理（推出未明说事实），SHACL 是 closed-world 校验（数据不合规即违规），两者互补；SHACL-SPARQL 支持跨节点规则；验证报告机器可读、接 CI/入库门禁。
**对系统**：515 的 relations 矛盾 / serves 悬空 / 误解悬空，以及"每个 atom 唯一 id、每条边目标必须存在、contradicts 不成环、命题不能脱离卡存在"，现在是一堆硬编码 if。应借鉴 SHACL 范式，收敛成**一份声明式 shapes（约束清单，YAML/JSON + 少量 SQL 断言）**：新增图约束改声明而非改代码，违规产出机器可读报告。关键立场：**知识校验用 closed-world（没记录=不合规），与 gate 的 fail-closed 一致**；不必引入 RDF 工具链，借范式即可。

## 四、统一锚点：S0-S7 阶梯 = 证据要求 = 论证偏好 = 认知稳固度
这是本轮最重要的架构动作，三处共用一个量：
| 使用点 | 怎么用 S0-S7 |
|---|---|
| 550 风险匹配（KIL） | claim 危害等级 → 要求达到的最低证据级 |
| Dung 论证裁决 | 冲突时，证据级高的论证击败低的（偏好序）；同级冲突挂起等人 |
| AGM 信念撤回 | 证据失效级联时，entrenchment 高（证据级高）的结论更难撤、优先保留 |
一个 claim 的"信任分"不再是单点布尔（verified/draft），而是它**支撑论证中最弱一环的证据级 + 可接受性状态 + 支持集冗余度**的组合。这让 gate 从二值 block/warn 进化成对知识状态的连续刻画。

## 五、Parser Differential：反复栽的 YAML 坑的统一学名与根治
**来源**：parser differential 安全指南（验证器与消费者对同一输入解析不同→构造"过一个检查、被另一个危险解释"）；重复键各语言 last-wins/报错不一（PyYAML/js-yaml 静默 last-wins，go-yaml 报错；JWT 经典 signed-by-first/consumed-by-last）；YAML 类型标签反序列化 RCE。
**对系统（这是 E07 缩进走私、全角键、flow 截断、547 D1 双解析器不一致的统一根因）**，根治四原则：
1. **单一规范解析器**：gate/replay/poison/mutation/自建零依赖解析器必须收敛到一条解析路径；若必须保留零依赖解析器（workbuddy 无 PyYAML），则做**解析器差分测试**——固定一批"两解析器可能分歧"的畸形样本（重复键/缩进提升/全角/flow/类型标签），CI 断言两解析器判决一致，不一致即 fail。
2. **验证前规范化、验证与消费同源**（normalize before validation, identical parsing）。
3. **歧义即拒绝**（fail-closed，不是 warn）：重复键、缩进提升、未知类型标签一律拒。
4. 新增一类零 LLM 变异算子 **M8 解析器差分**：专门生成多态/边界语法，是 coverage-guided fuzz 在输入层的自然延伸。

## 六、预注册 + holdout 盲测：给对抗/变异装"防自欺"制度（"阙疑"的操作化）
**来源**：arXiv 2606.11217《Preregistration for Experiments with AI Agents》（2026）；可重复性危机文献（Simmons/Nosek）；HARKing/p-hacking/researcher degrees of freedom；confirmatory（计划、错误受控）vs exploratory（数据驱动、需复现）必须分开。
**对系统（直接针对几轮已暴露的风险：542 把假逃逸当真洞、545 只打 3 个就报 0/3、看到结果再调算子）**：
1. 每轮对抗/变异**先落盘预注册**：这轮打哪些面、逃逸的判定口径、分母是什么、预期覆盖哪些规则，锁了再跑，按预注册口径报告。
2. 跑中意外发现的新洞标 **exploratory**，进入下一轮 confirmatory 预注册，不许直接当结论（防 HARKing）。
3. **固定 holdout 盲测集**：规则/算子在一批毒样例上调，必须在没碰过的 holdout 集上验收才算数（防过拟合到已知逃逸、防数字注水）。
4. 报告必须带"未覆盖清单"（547 已要求，提升为硬制度）。
零 LLM，纯流程纪律，是系统可信度的元保障。

## 七、Agent 护栏 2026 业界形态：系统方向被验证 + 几个可直接补强点
**来源**：Forge Guardrails（2026-09，洞察"agentic 失败多为执行前可检测错误而非模型质量错误"，四层 schema/依赖/沙箱/输出认证，8B+验证达 99%）；AWS Strands 三 checkpoint（工具调用前 hook、入站、出站验证）；六层护栏（输入验证/提示约束/工具白名单/输出 schema/动作确认 HITL/成本上限）。
**最关键原则**："summarization agent should be **structurally unable** to call a payments tool, not merely unlikely"（最小权限要结构强制，不是概率上不太会）。
**对系统（本元系统本质就是知识生产 agent 的护栏层，业界形态背书）**，补强点：
- 工具/目录最小权限结构强制（苦力在结构上无法写受控目录，而非靠提示词叮嘱）；
- 破坏性动作 HITL hook（commit/push/golden accept 必须人——已有，保持）；
- 成本与迭代上限（task_queue budget 已有雏形，对齐 500 请求/ token 天花板）；
- 尽量把错误在**写入前**拦（gate 前置为 commit hook / 入库门禁，Forge 的"执行前可检测"）。

## 八、落地优先级建议（接到 549/550 批次后）
- **批次 J（最高，不变）**：549 共形门 + RIPR。
- **批次 K**：550 KIL 风险分级 + S0-S7 阶梯字段。
- **批次 K2（本轮，知识层数学，零 LLM，可与 K 同批）**：
  - support set 数据结构 + AGM 三规则撤回传播（TMS，最高性价比，直接服务"证据塌了级联重审"）；
  - 图约束收敛成声明式 shapes（SHACL 范式，先收编现有 515 规则）；
  - Dung 可接受性先做 grounded 语义的最小实现（undercut/rebut/undermine 三分类标注历史红队发现）。
- **批次 M（工程根治，独立小批）**：解析器单一化 + 解析器差分测试 + M8 算子。
- **批次 N（流程制度，几乎不写码）**：对抗/变异预注册模板 + holdout 盲测集切分规范。
- **等模型档不变**：LLM 阴面/LLM fuzz/LLM 辅助 property 起草，EIR 门开后；Dung 偏好与 AGM entrenchment 永远用客观证据级，不用模型自述。

## 九、给监工的一句话
这一轮的发现是：**系统的"智能"短板不在更猛的模型，而在知识层缺三套 1979-1995 就成熟的符号数学**——冲突了谁站得住（Dung）、地基塌了撤谁（AGM/TMS）、合不合规（SHACL）。它们和验证强度阶梯焊死后，系统第一次能对知识做"裁决 + 级联撤回 + 连续信任刻画"，而不只是存取。这些全是确定性的、零 LLM 的、现在就能让苦力砌的地基——模型变强只是往这个已经会推理、会自我修正的骨架里灌更多产能。
