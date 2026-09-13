# 461 空白项定向调研：DAG调度器、Writer自检7项、突变测试自动化、handoff协议、教学评估

> 日期：2026-09-13。针对460识别的5个后续空白做定向调研。严格执行453证据标准。

---

## 一、DAG调度器：工业界验证了阙疑的方向

### 1.1 外部发现（证据等级：一手论文+工业框架，硬数据）

- **Airflow 3**（2025年4月）：DAG调度器工业标准，全量DAG版本化。新增agentic-workflow支持：持久任务状态、人在回路审批、动态任务映射、内置记忆和上下文管理。
- **Prefect 3**：Python原生，数据依赖图——追踪每个任务产出的artifact，下游任务声明依赖上游输出，**跳过输入未变的任务**，自动重试。
- **Graph Harness**（arXiv 2604.11378，2026-04）：把控制结构从隐式上下文提升为显式静态DAG。三个设计承诺：(1)执行计划是计划版本期间的不可变承诺；(2)规划/执行/恢复分离为三层；(3)恢复动作遵循严格升级协议，防止无限重试。
- **Airflow Resumable Tasks**：用task state store持久化checkpoint，重试时从checkpoint继续而非从头开始。

### 1.2 对阙疑的意义

458的PLAN1/2/3（DAG+checkpoint+失败定位）得到工业界验证，但阙疑不需要重型引擎——任务是文件级的。

**落地项 DAG1（立即可做，零代码）**：阙疑DAG的最小实现——
- 节点 = 文件产出（夹具.cpp / 工件.asm.out / 证据卡.md / 红队报告.md / 原子卡.md）
- 依赖 = 文件sha（上游文件sha变了才重跑下游）
- checkpoint = `_checkpoint.json`（节点名、状态、产出文件、sha、时间戳）
- 这直接把"续作不重跑夹具"的经验做法制度化。

**落地项 DAG2（立即可做）**：输入未变则跳过——如果夹具.cpp的sha没变，跳过重编译和重生成.asm/.out。Prefect的数据依赖图验证了这个模式。

**落地项 DAG3（待验证假设）**：动态任务映射——一批3颗原子，3个夹具可以并行生成（无依赖），然后各自串行走卡→红队→门禁。

**证据**：Airflow 3/Prefect 3/Graph Harness一手，硬数据。

---

## 二、Writer自检7项具体清单（从阙疑红队历史中提取）

### 2.1 这是460识别的空白，现在填上

460说"Writer自检的7项具体清单需要从红队历史中提取"。以下7项全部来自阙疑自己踩过的坑，每一条都有具体的卡/夹具/教训作为来源：

| # | 自检项 | 来源教训 | 检测方式 | 级别 |
|---|---|---|---|---|
| W1 | **断言字面量必须在Linux工件中grep得到** | 第五批040/041：断言写`arena_n1_meta_total_bytes=`但夹具用`report(tag,…)`运行时拼接，Windows走sha路径静默跳过，Linux侧refute | grep断言标签到Linux .asm/.out | block |
| W2 | **夹具注释不写带双引号的完整取值串** | S3-EXPECTED-HARDCODED：规则用`re.finditer(r'"([^"\n]*)"', src)`抓源码所有双引号字面量含注释，注释里写旧值会被误判为actual取值 | 扫描夹具源码注释中的`"..."` | warn |
| W3 | **性能卡command不含性能打印** | EV-MEM-045：逐轮纳秒进run_match逐字比对，任何机器必refute；必须-DBENCH_FULL宏门控双构建 | 检查command是否含性能打印函数调用 | block |
| W4 | **run_match_keys不含环境量** | d8ff94d：hardware_concurrency()进了run_match_keys，本地32核绿CI核数不同必refute；C++ hardware_concurrency()走sysconf读/proc不受taskset限制 | 检查keys是否含nproc/hardware_concurrency/cpu_count | block |
| W5 | **自旋夹具必须有界** | CONC-001：spin_volatile真无限循环，replay真跑600s超时rc=124→refute+CI白挂10分钟 | 检查main()是否有volatile自旋且无上界 | block |
| W6 | **元数据口径统一** | ALLOC-002：Arena只算sizeof(size_t)、Pool漏算8000B free-list堆数组，同口径下pool≈8224B≫bitmap 133B，卡把pool写成"最省32B"方向反转 | 检查卡内"元数据"定义是否覆盖所有分配器自身占用 | warn |
| W7 | **claim锚方向不锚倍数** | PERF-004：修复后倍数18.86×→8.78×（同机同夹具只改断言行），同一台机器跨运行波动2×+ | 检查claim是否含具体倍数/百分比，有则要求同时声明变量域和证伪条件 | warn |

### 2.2 落地方式

**落地项 WRITER1（立即可做）**：把这7项写成`docs/kernel/writer_self_check_v1.0.md`，每条含：检测问题+来源（哪次红队/对抗/卡）+正例（合法卡不触发）+反例（问题卡触发）。scicode-lint（arXiv 2603.17893）验证了这个pattern结构（检测问题+文档引用+3正3反测试）。

**落地项 WRITER2（立即可做）**：其中W1/W3/W4/W5可以写成确定性的gate规则（零LLM），W2/W6/W7是建议级（Writer自检清单，人工或LLM检查）。

**证据**：全部来自阙疑自己的红队/对抗/CI历史，一手实证。

---

## 三、突变测试自动化：从手动到算子定义

### 3.1 外部发现（证据等级：工业工具+一手论文，事实级）

- **mutmut**（Python）：AST级突变，知道执行哪些测试加速，并行，交互式UI，`mutmut browse`看存活突变体
- **Stryker**（JS/TS）：工业标准，突变分数阈值和dashboard，AI插件生态
- 三种结果：**Killed**（测试失败=成功）、**Survived**（所有测试通过=关键发现，测试区分不了buggy和正确代码）、**Stillborn/Equivalent**（语法错误或语义等价）
- 全量突变运行昂贵，通常增量运行

### 3.2 对阙疑的意义

阙疑的突变测试对象是**C++夹具.cpp**，不是Python代码。"测试套件"是replay的artifact_assert断言。

**落地项 MUT1（立即可做）**：定义阙疑的突变算子集（针对C++夹具）——
- 关系运算符翻转：`==`→`!=`、`<`→`>=`、`>`→`<=`
- 常量替换：`1`→`0`、`true`→`false`
- 语句删除：删除一行关键打印/计数
- 然后重跑replay：如果突变后replay仍confirm，说明断言杀不死突变=weak断言

**落地项 MUT2（待验证假设）**：自动化——写一个`tools/mutant_kill.py`，定义突变算子，自动生成突变版本，批量跑replay，统计杀灭率。和457 COV1（覆盖率量化）结合，形成"行覆盖率+突变杀灭率"双闭环。

**关键区分**：阙疑不需要mutmut（它是Python AST突变），需要的是针对C++文本的简单突变算子+replay批量执行。

**证据**：mutmut/Stryker工业实践+阙疑454 D1的手动突变经验，事实级。

---

## 四、多Agent handoff协议：不需要A2A，但需要结构化交接

### 4.1 外部发现（证据等级：A2A协议规范+一手论文，硬数据）

- **A2A（Agent2Agent）**：Google 2025年4月发布，捐给Linux基金会。JSON-RPC 2.0 over HTTP/SSE。Agent Card做能力广告。解决**协调问题**（一个agent把整个子任务委派给专门peer agent）。
- **MCP**：Anthropic，解决**工具访问问题**（一个LLM调用外部API）。
- ACP已合并入A2A（2025年8月）。
- 关键区分：MCP=agent到工具，A2A=agent到agent。A2A让agent彼此不共享内存/工具/内部逻辑就能协作。

### 4.2 对阙疑的意义

阙疑的多模型协作（苦力/好模型/对抗）目前是人工handoff（用户复制粘贴）。但阙疑不需要A2A的网络协议层——所有agent都在同一仓库、同一文件系统。

**落地项 HAND1（立即可做）**：定义阙疑内部handoff JSON schema——
```json
{
  "task_id": "G6-417",
  "task_type": "tool_implementation",
  "input_files": ["tools/gate_engine.py", "tests/test_gate_engine.py"],
  "expected_output": ["tools/gate_engine.py(modified)", "tests/test_gate_engine.py(modified)"],
  "acceptance_criteria": ["gate --check block=0", "pytest全绿", "新规则有毒样例覆盖"],
  "constraints": ["不修改atoms/evidence/下任何文件", "不push"],
  "checkpoint": {"last_completed_step": "schema设计", "status": "in_progress"}
}
```

**落地项 HAND2（待验证假设）**：handoff和DAG checkpoint结合——每个DAG节点的产出就是handoff的input_files，验收标准就是节点的exit criteria。

**证据**：A2A协议规范+阙疑现有handoff经验，硬数据。

---

## 五、教学效果评估：当前无用户，先做代理指标

### 5.1 外部发现（证据等级：元分析+RCT，硬数据）

- **间隔重复**：2026元分析21415医学学习者，SMD=0.78（大效应）。间隔重复组11.42→16.24，传统组11.58→11.89。
- **主动回忆**：93.5% vs 79%保留率（Engageli 2024）。
- **形成性评估**：118研究元分析，g=0.25（中等效应）。
- **AI辅助学习**：36对照研究7229参与者，g=0.499（中到大效应）。
- **Price et al. 2025**：26258执业医师RCT，之前答错的题58%后来答对vs对照组43%（d=0.62）。

### 5.2 对阙疑的意义

阙疑目前没有用户，教学效果无法实测。但可以先做**内容质量代理指标**。

**落地项 TEACH1（立即可做）**：教学内容质量代理检查——
- 闪卡正面是问题不是陈述（主动回忆设计，454 L1）
- 错误示例题型有desirable difficulty（454 L2）
- 概念间关联密度（relations DAG的边数/节点数）
- 这些不是真实学习数据，但是内容质量的可量化代理

**落地项 TEACH2（待验证假设）**：当有用户后，收集闪卡正确率/错误率/复习间隔，用SMD=0.78的间隔重复效应作为基准线。这是v8.0+的事。

**证据**：2026元分析+RCT，硬数据。

---

## 六、本轮元批判（按453标准）

### 真增量（改变做法）

1. **Writer自检7项具体清单（WRITER1/2）**：460识别的空白，现在从阙疑自己的红队历史中提取了7项，每项有来源教训+检测方式+级别。其中4项可以写成确定性gate规则。这是零外部依赖、立即可做的高价值项。
2. **DAG最小实现（DAG1/2）**：不需要Airflow/Prefect重型引擎，用文件sha+JSON checkpoint即可。输入未变则跳过直接解决"续作重跑"问题。
3. **handoff JSON schema（HAND1）**：把人工复制粘贴升级为结构化交接，和DAG checkpoint结合。

### 换术语（已有实践获得学名）

- 突变体杀灭 → 454 D1已有手动突变，MUT1/2是给它算子定义和自动化
- handoff协议 → 阙疑一直在做人工handoff，HAND1是结构化
- 教学代理指标 → 454 L1/L2已有闪卡设计，TEACH1是加量化检查

### 明确不采纳/推迟

- Airflow/Prefect/Temporal全量接入——过于重型，阙疑任务是文件级的，JSON checkpoint足够
- A2A网络协议层——阙疑agent在同一文件系统，不需要HTTP/SSE
- 教学效果真实数据——当前无用户，v8.0+再做
- mutmut直接使用——它是Python AST突变，阙疑需要C++文本突变

### 证据越界警示

- Airflow 3的agentic-workflow是通用场景，阙疑的窄域任务更简单——不要过度设计
- A2A的能力广告是跨厂商场景，阙疑的agent角色固定（苦力/好模型/对抗）——不需要动态发现
- 间隔重复SMD=0.78是医学学习者，C++学习可能不同——但方向成立

---

## 七、与已有架构的衔接

| 本轮落地项 | 强化/修正了哪个已有项 |
|---|---|
| WRITER1/2 Writer自检7项 | 460 T1（Writer自检层）的具体填充；420/413的执行清单 |
| DAG1/2/3 DAG最小实现 | 458 PLAN1/2/3的具体实现方案；460 P1/P2的落地 |
| MUT1/2 突变测试自动化 | 454 D1（突变体杀灭）的自动化；457 COV1的双闭环 |
| HAND1/2 handoff schema | 432/308多模型协作的交接格式；458 PLAN1的DAG节点产出 |
| TEACH1/2 教学评估 | 405/448教学转化的评估层；454 L1/L2的量化检查 |

累计 85 份（374-461）。
