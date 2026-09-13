# 463 十轮调研整合：优化报告/覆盖率/CI缓存/文档即代码/知识图谱/Agent评估/幻觉检测/语义检索/AgentUX/上下文管理

> 日期：2026-09-13。十个新方向的调研整合。严格执行453证据标准。

---

## 一、编译器优化报告：从"看asm"到"编译器告诉你做了什么"

### 发现（证据等级：GCC/Clang官方文档，硬数据）

- **GCC**：`-fopt-info-inline`（内联报告）、`-fopt-info-vec-missed`（向量化失败）、`-fopt-info-all=file`（全部优化输出到文件）。filter=optimized/missed/note/all。
- **Clang**：`-Rpass=inline`（做了的优化）、`-Rpass-missed`（没做的）、`-Rpass-analysis`（决策分析）。`-fsave-optimization-record`输出YAML/bitstream，比文本日志更易解析。
- 关键：`-Rpass-missed`直接告诉你"为什么这个循环没被向量化"——这是比asm更高级的优化观测。

### 落地项

- **OPT1（立即可做）**：阙疑性能卡的夹具编译时加`-fopt-info-vec-missed`和`-Rpass-missed`，把"编译器为什么没优化"写入证据卡。这比456的GIMPLE dump更直接——GIMPLE是"优化后长什么样"，opt-info是"编译器为什么这么做"。
- **OPT2（待验证）**：`-fsave-optimization-record`的YAML可以被Python解析，自动提取"哪些优化pass被跳过"，作为性能卡的活性对照。

---

## 二、代码覆盖率：行覆盖不够，突变测试才是断言质量的度量

### 发现（证据等级：工业实践+arXiv，硬数据）

- **行覆盖的虚假安全感**：85%行覆盖但40%突变未被杀=断言执行了代码但没验证结果正确。
- **coverage.py v7.12**（2025-11）：C0（语句）和C1（分支）可分别测量。支持per-test coverage（哪些测试跑了哪些行）。
- **gcovr**：C/C++的gcov报告生成，支持text/HTML/XML/JSON。
- **关键区分**：行覆盖=代码被执行了；分支覆盖=if的两个分支都走了；突变杀灭=断言能区分正确和buggy代码。三者递进。

### 落地项

- **COV1（立即可做）**：阙疑的Python工具代码（gate_engine.py/atom_evidence_replay.py等）用coverage.py测行覆盖率+分支覆盖率。pytest已经有135个测试，可以直接加`coverage run -m pytest`。
- **COV2（待验证）**：和461的MUT2（突变测试自动化）结合，形成"行覆盖率+突变杀灭率"双闭环。目标：工具代码行覆盖≥80%，突变杀灭率≥60%。

---

## 三、CI缓存优化：四级优化栈

### 发现（证据等级：GitHub Actions官方+工业实践，硬数据）

- **四级优化栈**：①跳过未变更包（affected builds）②缓存未变更产物③并行化剩余工作④分布式跨runner。每级叠加。
- **缓存键设计**：`key: ${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}`——内容哈希而非时间戳（和462的BUILD1同构）。
- **动态matrix**：从changed packages生成job列表，而非硬编码。`dorny/paths-filter`输出JSON数组直接喂matrix。
- **自托管runner**：AWS c5.large 49s vs GitHub标准82s（快40%），NVMe工作目录再快15-20%。

### 落地项

- **CI1（立即可做）**：阙疑的CI缓存pip依赖（`cache: pip`或`actions/cache` key=hashFiles('requirements.txt')）。当前CI每次重新安装pytest/PyYAML。
- **CI2（立即可做）**：affected builds——只在Examples/atoms/变更时跑replay，只在tools/变更时跑pytest，只在atoms/evidence/变更时跑gate。当前CI全量跑所有检查。
- **CI3（待验证）**：编译产物缓存——Examples/atoms/*.asm.out的缓存键=夹具.cpp sha+command+compiler（462 BUILD1），CI中命中缓存则跳过重编译。

---

## 四、文档即代码：86份架构文档的质量门禁

### 发现（证据等级：GitHub Docs/GitLab官方，硬数据）

- **工具链**：markdownlint（格式）、Vale（文风/术语，Go单二进制，跨平台）、markdown-link-check（死链）、cspell（拼写）、Prettier（格式化）。
- **GitHub Docs content linter**：规则ID化（GHD006 internal-links-old-version, GHD005 hardcoded-data-variable, GHD013 github-owned-action-references），severity=error。
- **GitLab docs测试**：`docs-lint links`（内部链接有效性）、`ui-docs-links lint`、`eslint-docs`。

### 落地项

- **DOC1（立即可做）**：阙疑的References/architecture_架构演进/有86份文档，加markdown-link-check检测死链（特别是引用的arXiv URL和外部链接）。
- **DOC2（立即可做）**：docs/kernel/的规范文档加markdownlint（格式一致性）。当前规范文档的frontmatter格式由gate检查，但正文格式无检查。
- **DOC3（待验证）**：Vale配置阙疑的术语表（如"阙疑""原子卡""证据卡""红队"的统一用法），防止术语漂移。

---

## 五、知识图谱推理：relations DAG升级为可查询图谱

### 发现（证据等级：Neo4j官方+arXiv，硬数据）

- **Neo4j 5.x**：原生向量索引+Cypher查询，符号查询和向量相似度在同一数据库。
- **GraphRAG**（Microsoft）：向量检索→图遍历→剪枝→GNN+LLM生成子图上下文。比纯向量检索准确率显著提升。
- **SGR**（arXiv 2605.16117）：schema-based reasoning——从问题生成schema，再转Cypher查询，缩小搜索空间。
- **关键**：传统KG升级失败率68.3%（2026奇点大会数据）——不是"加个LLM就行"，需要原生设计。

### 落地项

- **KG1（立即可做）**：阙疑的relations DAG（prerequisite/specializes/realizes/evolved_from/contradicts）已经是结构化数据。可以导出为GraphML/JSON，用Python networkx做基本查询（"某原子的所有前置依赖""矛盾环检测"）。不需要Neo4j。
- **KG2（待验证）**：当原子数>100时，考虑导入Neo4j做Cypher查询。当前27颗原子，networkx足够。
- **KG3（待验证）**：GraphRAG式的检索——用户问"虚函数的代价"，先查relations DAG找到相关原子，再综合回答。这是v10+的教学侧功能。

---

## 六、Agent评估基准：从"门禁全绿"到"任务完成率"

### 发现（证据等级：SWE-bench/GAIA官方+arXiv，硬数据）

- **SWE-bench Pro**（2026-01）：顶尖模型~45%。SWE-bench Verified~94%但59.4% hard任务有broken test——Verified分数虚高。
- **GAIA**：L1~75%, L2~60%, L3~45%。L3差距是当前Agent的真实瓶颈。
- **OSWorld**：~22% vs人类72%——GUI操作是最难的基准。
- **关键教训**：基准可能被污染/有broken test，需要contamination-resistant设计（SWE-bench Pro的改进）。

### 落地项

- **EVAL1（立即可做）**：阙疑的Agent评估三指标（457 EVAL1/2/3）——一次过率（Writer一次过门禁的比例）、红队校准率（红队发现的问题中真实问题的比例）、pass@5（5次尝试中成功的次数）。这些不需要外部基准，直接从阙疑的生产数据中统计。
- **EVAL2（待验证）**：建立阙疑自己的"任务完成率"基准——给苦力Agent一组标准化任务（如"生产一颗新原子"），统计完成率、耗时、token消耗。和SWE-bench的设计同构但场景定制。

---

## 七、LLM幻觉检测：实体级验证而非语义相似度

### 发现（证据等级：多篇arXiv，硬数据）

- **HalluGraph**（arXiv 2512.01659）：知识图谱对齐——Entity Grounding（响应中的实体是否出现在源文档）+Relation Preservation（断言的关系是否被上下文支持）。结构化控制文档上近完美区分。
- **FACTUM**（arXiv 2601.05866）：引用可信度四机制评分——Contextual Alignment、Attention Sink Usage、Parametric Force、Pathway Alignment。
- **RAGTruth-Enhance**：发现1.68×更多幻觉案例和3.1×更多幻觉片段——标准基准大幅低估幻觉率。
- **Semantic Illusion**（arXiv 2512.15068）：基于嵌入的幻觉检测有根本局限，用conformal prediction提供有限样本覆盖保证（n≈600时94%覆盖0%假阳性）。

### 落地项

- **HALL1（立即可做）**：阙疑的标准引用验证——原子卡中的标准引用（如[basic.def.odr]）必须能在eel.is或C++标准中grep得到。这是实体级验证，不是语义相似度。和455的C1/C2（标准引用tag化）结合。
- **HALL2（待验证）**：HalluGraph式的关系验证——原子卡claim中的关系（如"A导致B"）必须被证据卡的actual数据支持。这和461的W6（元数据口径统一）同构。

---

## 八、代码语义检索：从grep到结构化搜索

### 发现（证据等级：Sourcegraph/CodeQL官方，硬数据）

- **Sourcegraph Deep Search**：自然语言→AI agent迭代搜索→综合答案+文件链接。Code Finder MCP（2026-08 GA）：专门为agent优化的代码搜索，返回简洁摘要+链接+行范围。
- **CodeQL**：496个安全查询覆盖169 CWE（2.25.4）。CPG（Code Property Graph）思想——AST+CFG+调用图的统一表示。
- **ripgrep+fzf**：本地代码搜索的最小组合。`rg --files | fzf --preview 'bat {}'`。

### 落地项

- **SEARCH1（立即可做）**：阙疑仓库的检索——当前用Grep工具（ripgrep）。可以加一个`tools/knowledge_search.py`（288的T3）——frontmatter+正文+图遍历三路检索。这是苦力Agent的信息搜集能力提升。
- **SEARCH2（待验证）**：当原子数>50时，考虑为原子卡建结构化索引（YAML frontmatter解析+SQLite），支持"按domain/type/DAL/relations查询"。

---

## 九、Agent UX设计：handoff报告的三部分错误消息

### 发现（证据等级：多篇UX研究，事实级）

- **三部分错误消息**：what happened（具体失败）+why（原因）+what to try next（具体下一步，非"重试"）。通用"something went wrong"在agent场景特别有害。
- **渐进式披露**：展示3个决策点而非47个子动作。用户需要知道"为什么系统这么做"的即时英文回答。
- **可逆性优先**：草稿而非发送、软删除而非永久删除、沙箱预览而非实时编辑。
- **进度透明**："Analyzing 847 of 2400 documents"优于"Working..."。
- **三失败模式**：可恢复（自动换方案+通知）、需人工输入（歧义无法解决）、不可恢复（移交+上下文快照）。

### 落地项

- **UX1（立即可做）**：阙疑的handoff报告和红队报告遵循三部分错误消息格式。当前苦力Agent的报告已经有"完成/未完成/待裁决"结构，但错误消息可以更具体。
- **UX2（立即可做）**：苦力Agent的进度报告用"第X步/Y步"而非"正在进行"。和461的DAG checkpoint结合——每个DAG节点有明确的进度。
- **UX3（待验证）**：可逆性——苦力Agent的文件修改先写草稿（`_draft_`前缀），人审通过后再move到正式位置。当前原子卡已经有draft→verified的状态机，但工具修改没有草稿机制。

---

## 十、上下文窗口管理：解决"上下文耗尽"的根因

### 发现（证据等级：多篇arXiv+工业实践，硬数据）

- **Pichay**（arXiv 2603.09023）：LLM上下文的需求调页系统——透明代理，驱逐过期内容，检测缺页（模型重新请求被驱逐的材料），固定工作集页面。140万模拟驱逐的缺页率0.0254%。
- **Self-GC**（arXiv 2607.00692）：自治理上下文——把用户轮次/工具跨度/技能状态变成索引对象，侧通道规划器提议fold/mask/prune动作。33个Hard会话验证。
- **分层记忆**：热状态（当前任务）便宜、冷状态（历史）带外存储。提示缓存（稳定系统内容90%折扣）+选择性压缩。
- **滑动窗口+压缩摘要**：最近N轮逐字保留，更早的压缩为摘要。Google ADK Context Compaction用阈值触发。

### 落地项

- **CTX1（立即可做）**：阙疑的"每日日志+MEMORY.md"已经是分层记忆的雏形——热状态=当前会话上下文，冷状态=每日日志+MEMORY.md。但需要明确"什么进热状态、什么进冷状态"的规则。
- **CTX2（立即可做）**：和461的DAG checkpoint结合——每个DAG节点完成后，把该节点的产出写入checkpoint文件，然后可以从上下文中丢弃详细过程，只保留checkpoint摘要。这直接解决"上下文耗尽导致窗口中断"的问题（第五批6个窗口收不了口的根因之一）。
- **CTX3（待验证）**：Pichay式的缺页检测——如果Agent在后续步骤中需要已被压缩的细节，从checkpoint文件中重新读取（而非重新生成）。

---

## 十一、本轮元批判（按453标准）

### 真增量（改变做法）

1. **OPT1 编译器优化报告**：`-fopt-info-vec-missed`/`-Rpass-missed`直接告诉你"为什么没优化"，比asm更高级。性能卡从"看汇编"升级为"编译器自陈"。
2. **CI1/2 affected builds**：只在相关文件变更时跑对应检查。当前CI全量跑，浪费时间。
3. **CTX2 DAG checkpoint+上下文压缩**：直接解决"上下文耗尽"根因——节点完成后写checkpoint，丢弃详细过程。
4. **EVAL1 任务完成率三指标**：从"门禁全绿"升级为"一次过率/红队校准率/pass@5"，可从生产数据直接统计。

### 换术语（已有实践获得学名）

- 每日日志+MEMORY → 分层记忆（CTX1）
- 草稿→verified状态机 → 可逆性设计（UX3）
- relations DAG → 知识图谱（KG1）
- 标准引用验证 → 实体级幻觉检测（HALL1）

### 明确不采纳/推迟

- Neo4j全量接入——27颗原子，networkx足够
- Sourcegraph/CodeQL全量接入——单仓，ripgrep+knowledge_search.py足够
- SWE-bench/GAIA直接使用——阙疑场景定制，EVAL2自建基准
- Vale文风检查——中文文档，Vale主要面向英文
- Pichay/Self-GC实现——过于学术，阙疑的checkpoint+压缩摘要足够

### 证据越界警示

- SWE-bench Pro的~45%是Python仓库的bug修复，阙疑的C++知识生产场景不同——不要直接对标
- HalluGraph的近完美区分是结构化控制文档，阙疑的自由文本claim可能效果不同
- 自托管runner快40%是AWS c5.large数据，阙疑用GitHub免费runner——不适用

---

## 十二、与已有架构的衔接

| 本轮落地项 | 强化/修正了哪个已有项 |
|---|---|
| OPT1/2 优化报告 | 456 I1（GIMPLE dump）的互补——GIMPLE看结果，opt-info看原因 |
| COV1/2 覆盖率 | 457 COV1的具体工具选择；461 MUT2的双闭环 |
| CI1/2/3 CI优化 | 462 BUILD1（缓存键）在CI侧的应用 |
| DOC1/2/3 文档即代码 | 阙疑86份架构文档的质量门禁；460的空白"文档测试" |
| KG1/2/3 知识图谱 | 415 D1（relations矛盾检测）的扩展；460的"知识图谱推理" |
| EVAL1/2 Agent评估 | 457 EVAL1/2/3的基准化；404五维健康度的客观数据 |
| HALL1/2 幻觉检测 | 455 C1/C2（标准引用tag化）的验证层 |
| SEARCH1/2 语义检索 | 288 T3（knowledge_search.py）的设计依据 |
| UX1/2/3 Agent UX | 461 HAND1（handoff schema）的报告格式规范 |
| CTX1/2/3 上下文管理 | 458 PLAN1/2/3（DAG+checkpoint）的上下文侧应用 |

累计 87 份（374-463）。
