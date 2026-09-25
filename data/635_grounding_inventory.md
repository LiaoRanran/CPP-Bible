# 635 1.4 · 术语接地盘点 + 担保类型映射

- 规则数：**67**
- 接地状态分布：`{'部分接地': 37, '已接地': 24, '未接地': 6}`（已接地 35.8%）
- 担保类型分布：`{'系统性': 31, '即时性': 24, '常规性': 6, '权威性': 6}`

## 一、逐条规则盘点

| 规则 | 标题 | scope | kind | 接地状态 | 担保类型 |
|---|---|---|---|---|---|
| `ATOM-FM-REQUIRED` | 原子卡必填字段完整 | atom | fact | 部分接地 | 系统性 |
| `ATOM-ID-FORMAT` | 原子 ID 格式/域/目录一致 | atom | fact | 部分接地 | 系统性 |
| `ATOM-ID-UNIQUE` | 原子身份唯一（stem==id 且 id 全库唯一） | atom | fact | 部分接地 | 系统性 |
| `ATOM-VERIFIED-BOUND` | verified ⟹ 证据+一手+superiority | atom | fact | 部分接地 | 系统性 |
| `ATOM-NO-UNVERIFIED` | 新原子禁未验证状态 | atom | fact | 部分接地 | 系统性 |
| `ATOM-STATUS-VALUE` | status 取值限于四级枚举 | atom | fact | 部分接地 | 系统性 |
| `ATOM-STATUS-TRANSITION` | 状态跃迁可证（status_history 链） | atom | fact | 部分接地 | 系统性 |
| `ATOM-DAL-MATCH` | DAL 分级与人审要求一致 | atom | fact | 部分接地 | 系统性 |
| `ATOM-REL-TARGET` | 关系目标存在 | atom | fact | 部分接地 | 系统性 |
| `ATOM-REL-DAG` | 学习路径 DAG 无环 | atom | fact | 部分接地 | 系统性 |
| `ATOM-REL-CONFLICT` | relations 矛盾检测：A 支持/依赖 B 且 B 声明 contradicts A（415 D1） | atom | fact | 部分接地 | 系统性 |
| `ATOM-SUPERIORITY-WORDS` | superiority 禁词表 | atom | fact | 部分接地 | 系统性 |
| `EV-FM-REQUIRED` | 证据卡必填字段完整 | evidence | fact | 已接地 | 即时性 |
| `EV-ID-UNIQUE` | 证据身份唯一（stem==id 且 id 全库唯一，N2） | evidence | fact | 已接地 | 即时性 |
| `EV-FALSIFICATION` | 证伪对照存在（非恒真测试） | evidence | fact | 已接地 | 即时性 |
| `EV-MATRIX` | 版本矩阵字段完整 | evidence | fact | 已接地 | 即时性 |
| `ATOM-GRAY-ZONE` | UB 域原子标注灰色地带类别 | atom | fact | 部分接地 | 系统性 |
| `ATOM-MISCONCEPTION-LEVELS` | 误解分层 surface/deep（deep 须 ≥2 反例） | atom | fact | 部分接地 | 系统性 |
| `MIS-LIBRARY` | 误解库自身合规（level 合法 / deep≥2 反例 / 有出处） | atom | fact | 部分接地 | 系统性 |
| `ATOM-MISCONCEPTION-REF` | 原子引用的误解 ID 必须存在 | atom | fact | 部分接地 | 系统性 |
| `ATOM-AUDIENCE` | 认知适切：audience/cognitive_load 合法 + beginner 须有类比段 | atom | fact | 部分接地 | 系统性 |
| `ATOM-PREREQ-READABLE` | 前置可读声明与实算一致 | atom | fact | 部分接地 | 系统性 |
| `EV-SERVES-EXIST` | 证据服务的原子存在 | evidence | fact | 已接地 | 即时性 |
| `DOC-ZERO-PLACEHOLDER` | 新体系零占位符 | repo | fact | 部分接地 | 常规性 |
| `META-MANIFEST` | 双清单一致（ADR-0004） | repo | fact | 部分接地 | 常规性 |
| `S1-AUTHOR-SELF-VERIFY` | verified 须人工签收（Agent 无权定 golden） | atom | fact | 部分接地 | 系统性 |
| `S1-GIT-AUTHOR-BINDING` | 人级签收须与 git 作者一致（479 任务 4，观察期 warn） | atom | fact | 部分接地 | 系统性 |
| `ATOM-VERIFY-REASON` | 人级签署须写理由（494 任务 5 / 491 决策日志） | atom | fact | 部分接地 | 系统性 |
| `EV-ARTIFACT-VERSION-MATCH` | 工件-卡版本绑定（498 任务 2 / 490 版本管理） | evidence | fact | 已接地 | 即时性 |
| `S2-EVIDENCE-VERDICT` | verified 只绑 verdict=confirm 的证据 | atom | fact | 部分接地 | 系统性 |
| `S3-EXPECTED-HARDCODED` | 期望硬编码进夹具=伪证据 | evidence | fact | 已接地 | 即时性 |
| `EV-SELF-SATISFIED-ASSERT` | 断言不得被夹具自身定义满足（P4 自证断言） | evidence | fact | 已接地 | 即时性 |
| `EV-FALSIFICATION-QUANT` | 证伪对照须含量化取值（P5 伪证伪） | evidence | fact | 已接地 | 即时性 |
| `EV-TRIVIAL-OBSERVATION` | actual 禁恒真观测承担主证（P6） | evidence | fact | 已接地 | 即时性 |
| `EV-MATRIX-UNBACKED` | 多编译器矩阵须有留痕说明（P7） | evidence | fact | 已接地 | 即时性 |
| `EV-ZERO-DIAG-WERROR` | 零诊断类判据须 -Werror（W3） | evidence | fact | 已接地 | 即时性 |
| `EV-WERROR-DECL-BIND` | 判据性 -Werror 须落到每条诊断编译行（570，warn） | evidence | fact | 已接地 | 即时性 |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | 断言/键数少于人审基线（572，warn） | evidence | fact | 已接地 | 即时性 |
| `EV-OUT-UNDECLARED-KEY` | .out 读数键须在 run_match_keys 声明（B3 窄化） | evidence | fact | 已接地 | 即时性 |
| `EV-RUN-KEY-DECLARED-EXISTS` | run_match_keys 声明的键必须真在 .out 中存在（500 任务2：M5 反向校验闭合） | evidence | fact | 已接地 | 即时性 |
| `EV-ASSERT-SYMBOL-MAPPED` | 断言文本须可定位（夹具/工件/symbol_map，B2 窄化） | evidence | fact | 已接地 | 即时性 |
| `EV-ARTIFACT-PRODUCER` | 工件产出命令须显式声明、为编译器、且与 command 逐字一致（N4 窄化+373绕过3d） | evidence | fact | 已接地 | 即时性 |
| `EV-ARTIFACT-FILE-EXISTS` | 卡声明的 artifact / artifacts[] 文件必须存在（500 任务3：M8 闭合） | evidence | fact | 已接地 | 即时性 |
| `EV-MSCV-NO-VERIFY` | 含 MSVC(cl) 的卡禁止标 confirm（414 F01 免检链） | evidence | fact | 已接地 | 即时性 |
| `EV-FM-DUP-KEY` | frontmatter 重复键（after-wins 遮蔽，414 F09） | repo | fact | 部分接地 | 常规性 |
| `EV-FM-YAML-HARDENING` | frontmatter 解析硬化（470 P0-D：走私/重复键/语法/一致性） | repo | fact | 部分接地 | 常规性 |
| `EV-ENV-DEPENDENT-KEY` | 环境量读数键（470 P0-E：声明为断言=block/仅留痕=advice） | evidence | fact | 已接地 | 即时性 |
| `ATOM-REL-UNKNOWN` | 未知 relations 类型（472 P1-4：结束同义词枚举，表外即债务） | atom | fact | 部分接地 | 系统性 |
| `ATOM-CLAIM-STRUCTURED` | 新卡必须有命题化 claim_structured（526 规则1；存量 STAGING 只 warn） | atom | fact | 部分接地 | 系统性 |
| `OBSERVATION-NEEDS-ARTIFACT` | observation 命题须有工件断言支撑（526 规则2：零容忍） | atom | fact | 部分接地 | 系统性 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | inference 命题不得由机器独自晋升（526 规则3：核心放权闸） | atom | fact | 部分接地 | 系统性 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | claim 命题 object 须归一化规范概念（图谱可连通，530 任务3） | atom | fact | 部分接地 | 系统性 |
| `OBSERVATION-LIVENESS` | observation 命题须有活性对照（530 任务4：堵「自标观测即全自动」，warn 观察期） | atom | fact | 部分接地 | 系统性 |
| `EV-FIXTURE-NO-ECHO-DATA` | cat 式证据（472 P1-2：experimental→warn，读文件原样打印） | evidence | fact | 已接地 | 即时性 |
| `EV-OUT-STALE-MTIME` | .out 须比夹具新（414 F06 陈旧留痕） | evidence | fact | 已接地 | 即时性 |
| `CARD-PATH-NOT-CANONICAL` | 卡内路径须 posix 规范且大小写与磁盘一致（548 Part 2：M2 跨平台路径异体，warn） | repo | fact | 部分接地 | 常规性 |
| `EV-SERVES-EXIST-HC` | 高复杂度证据 serves 目标必须存在（block 兜底） | evidence | fact | 已接地 | 即时性 |
| `ATOM-REL-TARGET-HC` | 高复杂度原子 relations 目标必须存在（block 兜底） | atom | fact | 部分接地 | 系统性 |
| `ATOM-REL-UNKNOWN-HC` | 高复杂度原子 relations 类型必须已知（block 兜底） | atom | fact | 部分接地 | 系统性 |
| `CARD-PATH-NOT-CANONICAL-HC` | 高复杂度卡路径必须规范（block 兜底） | repo | fact | 部分接地 | 常规性 |
| `PED-MOTIVATION` | 动机先行：先说清为什么需要 | atom | pedagogy | 未接地 | 权威性 |
| `PED-MISCONCEPTION` | 学习者常见误解清单 | atom | pedagogy | 未接地 | 权威性 |
| `PED-SOCRATIC` | 苏格拉底提问链 | atom | pedagogy | 未接地 | 权威性 |
| `PED-PREDICT-FIRST` | 先预测后揭示（生成性学习） | atom | pedagogy | 未接地 | 权威性 |
| `LLM-SUPERIORITY-QUALITY` | superiority 是否真有洞见 | atom | fact | 部分接地 | 系统性 |
| `HYBRID-TEACHING-DEPTH` | 教学深度初筛 + 人工裁定 | atom | pedagogy | 未接地 | 权威性 |
| `HUMAN-GOLDEN-REVIEW` | Golden 样板人审 | repo | meta | 未接地 | 权威性 |

## 二、接地覆盖率

- 已接地 **24/67 = 35.8%**
- 部分接地 **37**
- 未接地 **6**

## 三、未接地清单（优先级排序：教学/元规则优先补实验）

- `PED-MOTIVATION`（动机先行：先说清为什么需要，kind=pedagogy）
- `PED-MISCONCEPTION`（学习者常见误解清单，kind=pedagogy）
- `PED-SOCRATIC`（苏格拉底提问链，kind=pedagogy）
- `PED-PREDICT-FIRST`（先预测后揭示（生成性学习），kind=pedagogy）
- `HYBRID-TEACHING-DEPTH`（教学深度初筛 + 人工裁定，kind=pedagogy）
- `HUMAN-GOLDEN-REVIEW`（Golden 样板人审，kind=meta）

## 诚实登记

1. 分类为**启发式**（按 scope/kind），非人工逐条判定术语级接地；
2. 「未接地」= kind ∈ {pedagogy, meta}（教学/元规则，无外部实验对应）；「部分接地」= atom/repo 结构规则（有规范/约定对应但无直接实验）；
3. 本工具**只读**，不改任何规则。
