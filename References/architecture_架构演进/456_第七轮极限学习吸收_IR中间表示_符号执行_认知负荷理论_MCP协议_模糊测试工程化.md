# 456 第七轮极限学习吸收：IR中间表示、符号执行、认知负荷理论、MCP协议、模糊测试工程化

> 日期：2026-09-13。对抗模型仍在跑 452，本轮并行调研五个更深方向。严格执行 453 证据标准。

---

## 一、LLVM IR / GIMPLE：比 .asm 更高层的优化观测

### 1.1 外部发现（证据等级：官方文档 + 一手教程，事实级）

- **LLVM 用统一 IR**（SSA 形式），跨架构稳定；**GCC 用三层 IR**：GENERIC（语言无关 AST）→ GIMPLE（三地址码 SSA，主要优化层）→ RTL（寄存器传输语言，机器相关）。
- **Clang `-emit-llvm`** 输出 LLVM IR（.ll）；**GCC `-fdump-tree-optimized`** 输出优化后的 GIMPLE；`-fdump-tree-all` 输出每个 pass 前后的 IR。
- LLVM pass 架构：**analysis pass**（收集信息如循环信息/别名分析/分支概率，结果缓存）+ **transform pass**（变换 IR，如 instruction combine/SROA/GVN/LICM/loop unroll/vectorize）。
- IR 层面能看到 .asm 层面被掩盖的优化决策：内联（call 被替换为内联体）、循环变换（LICM 把不变量移出循环）、向量化（scalar loop → SIMD）。

### 1.2 对阙疑的意义

阙疑目前分析到 .asm 为止，但 IR 层面能提供更清晰的"编译器做了什么"的证据。

**落地项 I1（立即可做，零成本）**：优化类原子的夹具编译时加 GCC GIMPLE dump：
```bash
g++ -O2 -fdump-tree-optimized -c fixture.cpp -o fixture.o
# 输出 fixture.cpp.265t.optimized
```
GIMPLE 比 asm 更易读（三地址码，无寄存器分配干扰），且能直接看到内联/循环变换的决策。作为 .asm 的补充证据写入卡内（可选字段 `ir_artifact`）。
- 注意：阙疑当前无 Clang，LLVM IR 不可用；GCC GIMPLE 可用。

**落地项 I2（待验证假设）**：`-fdump-tree-all` 追踪优化过程——每个 pass 前后的 IR 对比，能展示"这个优化是在哪个 pass 发生的"。但输出文件多（几十个），需要筛选关键 pass（inline/ssa/optimized）。先试点 1 颗原子。

**证据**：GCC 官方 Developer Options + LLVM 官方文档，事实级。

---

## 二、符号执行 + 模型检查：自动生成全路径测试

### 2.1 外部发现（证据等级：一手论文 + 工业实践，硬数据）

- **KLEE**（OSDI 2008，Stanford）：在 LLVM bitcode 上做符号执行，把输入当作符号表达式而非具体值，每条路径累积路径条件（PC），用 SMT solver 判断 PC 是否可满足。在 GNU Coreutils 89 个程序中发现 **84 个 bug**（很多 10+ 年未被人工审查和随机测试发现），**90%+ 分支覆盖率**。
- **CBMC**：C/C++ 有界模型检查器，给定展开深度 d，构造逻辑公式断言"存在输入导致错误"，直接吃源码不需要 LLVM bitcode。
- **SPARC**（arXiv 2602.16671，2026）：场景规划+推理自动生成 C 单元测试，平均比 KLEE 高 31.36% 行覆盖率/26.01% 分支覆盖率，大项目上超过 KLEE。
- 核心挑战：**状态爆炸**（路径数指数增长），缓解手段：约束独立性优化、state merging、coverage-guided 搜索策略。

### 2.2 对阙疑的意义

阙疑的夹具测试目前是手工的"n=1000/8000"两点测试，符号执行可以自动覆盖所有路径。

**落地项 S1（待验证假设，v9.0 试点）**：对夹具的核心函数用 CBMC 做有界模型检查，验证属性（如"arena 元数据不随 n 变"对所有 n∈[1,10000] 成立）。CBMC 直接吃 C++ 源码，不需要 Clang，比 KLEE 更可行。
- 风险：符号执行对含循环/递归的程序有状态爆炸，但教学夹具通常简单（<50行），可能可行。
- 验证方法：选 ALLOC-002 的 meta() 函数，用 CBMC 验证"对任意 n，arena_total == struct_bytes"，看是否能在合理时间内完成。

**不采纳**：KLEE（需要 LLVM bitcode/Clang，当前无 Clang，永久边界）。

---

## 三、认知负荷理论：证据卡瘦身的理论依据

### 3.1 外部发现（证据等级：经典理论 + 元分析，最强）

- **Cognitive Load Theory（CLT）**（Sweller 1988，持续验证至 2025）：工作记忆容量有限（Miller 7±2，Cowan 修订为 **~4 块**），长时记忆本质无限。
- **三种负荷**：
  - **Intrinsic（内在）**：材料本身的复杂度，由元素交互性决定。不能消除，但可通过 sequencing/scaffolding/pretraining 管理。
  - **Extraneous（外在）**：不良设计造成的无效负荷。可以通过设计消除：split-attention（相关信息物理分离→整合）、redundancy（冗余信息→删除）、modality（文字+图示双通道）。
  - **Germane（相关）**：构建心智模型的有效努力。这是"好的"负荷，应该最大化。
- **总负荷必须低于工作记忆容量**，否则学习和理解失败。
- **Expertise Reversal Effect**：对新手有效的教学设计对专家可能无效甚至有害——闪卡给新手、原子卡给进阶者，设计应不同。

### 3.2 对阙疑的意义

**这是本轮最有价值的发现**——直接解决"证据卡从 60 行膨胀到 200+ 行"的问题，且有硬理论支持。

**落地项 CL1（立即可做，零成本）**：证据卡的 extraneous load 审计——
- **Split-attention**：.asm 行号和解释是否分离？学生需要在 asm 和解释之间来回看 → 解释应直接引用对应 asm 行（如 `; asm:42 call malloc`），而非分离描述。
- **Redundancy**：修订记录、处置登记、双平台完整对照是否都必要在卡内？→ 修订记录移到单独的 `changelog/` 文件，卡内只留最新版 + 一行"修订历史见 changelog/XXX.md"。双平台对照只保留差异点，相同的不重复。
- **Modality**：纯文字卡是否可以加结构化摘要（如 claim→证据→反例→边界的四行表格）？markdown 表格是双通道的轻量实现。

**落地项 CL2（立即可做，高价值）**：证据卡**分层设计**——
- **核心层**（<50行）：claim + 关键证据（3-5 条）+ 活性对照 + 证伪条件。学生先看这层。
- **附录层**（单独文件或 `<details>` 折叠）：完整原始输出、修订记录、双平台逐行对照、红队处置登记。需要时翻。
- 这是 scaffolding 的应用：先给简版（降低内在负荷），再给完整版（germane load）。
- 直接回应 402 红队指出的"证据卡承载了太多东西，维护成本接近教学价值"。

**落地项 CL3（待验证假设）**：Expertise reversal——闪卡/MCQ 是给新手的，应该用最简语言+具体例子；原子卡是给进阶学习者的，可以用术语+形式化。当前闪卡直接从原子卡提取，可能对新手太难（内在负荷过高）。v8.0 闪卡工具应支持"新手版/进阶版"双档。

**证据**：Sweller 1988 + Cowan 2001 + 2025-2026 CLT 综述，经典理论+持续验证。

---

## 四、MCP 工具协议：v10+ 平台化的标准

### 4.1 外部发现（证据等级：官方规范 + 一手设计模式论文）

- **MCP（Model Context Protocol）**：Anthropic 2024-11 发布，2025-11 移交 Linux Foundation Agentic AI 基金会。社区 MCP Server 从 135 个（发布时）增长到 5069 个（2025-06）。
- 三能力：**Tools**（函数）、**Resources**（数据）、**Prompts**（模板）。JSON-RPC over stdio 或 Streamable HTTP。
- **关键设计模式**（arXiv 2603.13417，一手）：
  1. **Tool descriptions 比 tool code 更重要**——Agent 按名称和描述选工具，描述就是接口，要像 API 文档一样写。
  2. 从第一天就建 broker 层——用户上下文传播、JWT 提取、context injection。
  3. 超过 10 秒的操作用 **MCP Tasks**（异步，返回 task reference，不阻塞）。
  4. `allowed_tools` 白名单——最小权限原则。
- Claude Code 的定位三分：CLAUDE.md（项目上下文）+ Hooks（生命周期自动化）+ MCP（外部工具）。

### 4.2 对阙疑的意义

阙疑的工具链（gate_engine/replay/poison/golden_lock/cppbible）目前是 CLI 脚本。

**落地项 M1（立即可做，零成本）**：MCP 设计原则指导当前 CLI 工具——`--help` 输出要写得像 API 文档（因为 Agent 是读 --help 来选工具的）。当前 `cppbible.py --help` 是否清晰描述了每个子命令的用途、参数、返回值？审计并改进。

**落地项 M2（待验证假设，v10+）**：把阙疑核心工具包装成 MCP server `cppbible_mcp`——暴露 tools（check_atom/run_replay/run_gate/list_rules）、resources（原子卡/证据卡/规则列表）、prompts（红队提示词/夹具生产提示词）。这样任何支持 MCP 的 Agent（Claude Code/Cursor/Trae）都可以直接调用，不需要知道 CLI 语法。
- 这是 v10+ 平台化工作，当前 v7.0 先把 CLI 做扎实。

---

## 五、模糊测试工程化：毒样例的自动化升级

### 5.1 外部发现（证据等级：官方文档 + 工业实践，事实级）

- **libFuzzer**（LLVM）：in-process，coverage-guided，进化式 fuzzing，和 sanitizer 紧密耦合（ASan/UBSan/MSan）。"unit fuzzing"——像单元测试但不需要手写输入。
- **AFL++**：最成熟的 coverage-guided fuzzer，SHM 64KB bitmap 反馈（每条边一个 byte），CMPLOG/RedQueen 路径约束求解。
- **核心循环**：seed corpus → mutate（flip bits/insert bytes/splice）→ execute → measure coverage → new coverage → add to corpus → repeat。
- **工程实践**：dictionary（格式感知）、多 fuzzer 并行（不同变异算法增加覆盖率）、coverage gap 分析、**首字节模式选择器**（一个输入轰炸多个代码路径，Ghostty 实践）。

### 5.2 对阙疑的意义

阙疑的毒样例（poison_drill）本质上是手工 fuzzing——手工构造违反规则的原子卡验证 gate 能拦住。

**落地项 F1（立即可做，零新工具）**：coverage-guided 思路用于毒样例设计——每条 block 规则的毒样例应覆盖该规则的**不同触发路径**。如 ATOM-REL-CONFLICT 有三类矛盾（A依赖B且BcontradictsA / A自身矛盾 / A自引用），每类都要有毒样例，而非只覆盖一类。
- 这是 451 IPT（同构扰动测试）的具体化：每条规则的毒样例从单点变异升级为"触发路径全覆盖"。

**落地项 F2（待验证假设，v8.0）**：毒样例自动生成——对每条 block 规则，用 LLM 自动生成 N 个变异毒样例（451 IPT 六族：重命名/重排/等价改写/编码变体/注释包装/时序变体），验证 gate 拦截率。拦截率 < 90% 的规则标 weak，必须加强。
- 和 454 突变体杀灭测试（D1）互补：突变测试是"改夹具看断言杀不杀"，毒样例 fuzzing 是"改原子卡看 gate 拦不拦"。

---

## 六、本轮元批判（按 453 标准）

### 真增量（改变做法）

1. **认知负荷理论（CL1/CL2/CL3）**：证据卡瘦身的理论依据，直接解决 402 指出的"证据卡膨胀"问题。分层设计（核心层<50行+附录层）是立即可做的高价值改动。
2. **GIMPLE dump（I1）**：比 .asm 更高层的优化观测，零成本（加编译 flag），PERF 类原子直接受益。
3. **毒样例触发路径全覆盖（F1）**：coverage-guided 思路用于毒样例设计，零新工具。
4. **CLI --help 即 API 文档（M1）**：MCP 设计原则的即时应用。

### 换术语（已有实践获得学名）

- 符号执行 → 443 的 metamorphic_relation + 454 的 PBT，符号执行是自动化全路径版本
- 模糊测试 → poison_drill 是手工 fuzzing，F2 是自动化版本
- MCP → 阙疑的 CLI 工具是 MCP 的前身

### 明确不采纳/推迟

- KLEE（需要 Clang/LLVM bitcode，永久边界）
- 全 MCP server 包装（v10+ 平台化，当前先做扎实 CLI）
- CBMC 全量应用（v9.0 试点，先验证教学夹具是否可行）

### 证据越界警示

- KLEE 的 90%+ 覆盖率是 Coreutils 场景（C 语言、系统工具），不能直接平移到 C++ 教学夹具场景
- CLT 的 ~4 块工作记忆是通用认知科学结论，对 C++ 学习者的具体负荷阈值需要阙疑自己的数据

---

## 七、与已有架构的衔接

| 本轮落地项 | 强化/修正了哪个已有项 |
|---|---|
| I1 GIMPLE dump | 455 O1/O2 optimization remarks 的互补（remarks 说"做了什么"，GIMPLE 展示"做成了什么样"） |
| S1 CBMC 试点 | 454 T2 PBT 的全路径版本；443 metamorphic_relation 的形式化验证 |
| CL1/CL2 证据卡分层瘦身 | 直接解决 402 红队"证据卡膨胀"问题；451 H9 证据卡瘦身的理论依据 |
| CL3 新手/进阶双档 | 405 教学转化四层的受众细分 |
| M1 --help 即 API | 432 多模型协作的工具接口标准化 |
| M2 MCP server | v10+ 范式跃迁（449 生态插件化）的具体路径 |
| F1 毒样例路径全覆盖 | 451 IPT 六族的具体化；poison_drill 的 RULE-COVERAGE 升级 |
| F2 毒样例自动生成 | 446 规则自动进化（counterexample mining）的实现路径 |

累计 80 份（374-456）。
