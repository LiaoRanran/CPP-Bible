# 457 第八轮极限学习吸收：Agent记忆架构、C++异常实现、覆盖率量化、Agent评估方法论、链接器ODR深化

> 日期：2026-09-13。对抗模型仍在跑 452，本轮并行调研五个方向（2 个系统级 + 3 个内容级）。严格执行 453 证据标准。

---

## 一、Agent 记忆系统：四类记忆的标准化

### 1.1 外部发现（证据等级：一手论文 + 主流框架，硬数据）

- **四类记忆已成主流框架**：Working（上下文窗口，8K-200K tokens）、Episodic（时间戳事件记录，append-only log）、Semantic（事实/偏好/知识，向量库或知识图谱）、Procedural（技能/规则/工作流，prompt templates 或工具 schema）。
- **MemMachine**（arXiv 2604.04853，2026-04）：Ground-Truth-Preserving Memory System——短期记忆保持最近 N 个 episode + LLM 压缩摘要，超窗后转移到长期记忆。核心设计原则：**压缩不能丢失 ground truth**（具体数字/命令/sha 必须保留，只能重组结构）。
- **CraniMem**（arXiv 2026-03）：神经认知启发的门控有界多阶段记忆——目标条件门控（goal-conditioned gating）+ 效用标签（utility tagging）+ 有界情景缓冲 + 结构化长期知识图谱。
- **Procedural memory 是最不成熟但最有趣的层**：LLM 中程序记忆最好表示为指令（prompt templates）而非数据——"总是先用 schema X 验证 JSON 再调 API Y"这类知识写成指令比写成事实更有效。

### 1.2 对阙疑的意义

阙疑目前的记忆其实已经有四类雏形，但比较原始：MEMORY.md（semantic）+ 每日日志（episodic）+ 系统提示词（procedural）+ 上下文窗口（working）。

**落地项 MEM1（立即可做，零成本）**：MEMORY.md 标准化为四段结构——
```
## Working（当前批次状态）
- 当前批次：第六批 CONC 域，3 颗中 2 颗 verified
- 待决事项：push 39 条提交、A3 差异裁决

## Episodic（按日期的事件日志）
- 2026-09-12：ALLOC-002 口径不统一导致方向反转
- 2026-09-13：402 对抗发现 13 个逃逸

## Semantic（铁律/规范/教训）
- 铁律 7：不自行 push
- 教训：nproc 禁入 run_match_keys（d8ff94d）

## Procedural（提示词模板/工具用法）
- 红队提示词：365B / 452
- 工具：gate_engine.py --check / replay --check
```

**落地项 MEM2（立即可做）**：记忆压缩的 ground-truth 保留原则写入规范——总结时**禁止丢失具体数字/sha/命令/文件路径**，只能重组结构。这和铁律 10（无锚不入）一致，是记忆侧的对应。

**落地项 MEM3（待验证假设）**：效用标签——每条记忆标"已验证/待验证/已过时"，过期记忆自动归档到 `memory/archive/`。这和 debt_ledger 的思路一致，但应用于记忆而非规则。

**证据**：MemMachine/CraniMem 一手论文 + 四类记忆主流框架（2026 多篇综述）。

---

## 二、C++ 异常处理实现：零成本模型的代价

### 2.1 外部发现（证据等级：Itanium ABI 规范 + LLVM 文档，一手）

- **Itanium C++ ABI 零成本模型**：正常路径零开销（不保存 pc/寄存器状态），异常抛出时才执行栈展开。设计前提：异常是罕见事件。
- **两层架构**：Base ABI（libgcc，语言无关的 `_Unwind_RaiseException`）+ C++ ABI（libsupc++，personality function 解释 catch 块/析构/作用域）。
- **栈展开机制**：用 DWARF `.eh_frame` 信息逐帧回退；**personality function 是语言相关的封装点**——这使得 ABI 可支持多语言混合（C++/Rust/...）。
- **异常对象**：在堆上分配，引用计数管理生命周期。
- **异常表**：`.gcc_except_table`（ELF）/ `.xdata`（Mach-O）存储每个函数的异常处理表。
- **代价**：代码体积膨胀（异常表占空间）+ 抛出时的运行时开销（栈展开 + RTTI 匹配）。
- **MSVC 用不同模型**（`__CxxFrameHandler`，基于表的 SEH 包装）。

### 2.2 对阙疑的意义

阙疑目前没有专门的 EH 原子——这是 LANG 域的真实知识空白（INLINE-001 是 LANG 首颗，EH 是自然延伸）。

**落地项 EH1（待验证假设，新原子选题）**：ATOM-LANG-EH-001「零成本异常的代价」——
- claim：正常路径零指令（对比 setjmp/longjmp 模型的每帧开销），但代价是 .eh_frame 代码体积膨胀 + 抛出时栈展开开销
- 夹具：同一函数 try/catch vs 无异常，对比 .asm 正常路径指令数 + .eh_frame 大小 + 抛出 1e6 次的耗时
- 活性对照：setjmp/longjmp 模型的正常路径指令（非零）

**落地项 EH2（立即可做）**：EH 类原子的 sanitizer 配置——UBSan 的 `-fsanitize=function` 可以检测函数类型不匹配（throw 时的类型转换错误）。写入 454 S1 Sanitizer 矩阵的 EH 行。

**证据**：Itanium C++ ABI 规范（refspecs.linuxfoundation.org）+ LLVM ExceptionHandling 文档，一手。

---

## 三、代码覆盖率量化：行覆盖率 ≠ 测试有效性

### 3.1 外部发现（证据等级：一手实验 + 经典研究，硬数据）

- **行覆盖率陷阱**（2026 实验，Botmonster）：AI 生成测试套件 **93.1% 行覆盖率但只有 58.6% 突变测试杀灭率**——超过 1/3 的真实 bug 会在 CI 全绿时溜过。
- **覆盖率 vs 突变测试的本质区别**：覆盖率测"执行了没有"，突变测试测"执行了能不能检测出错误"。覆盖率是必要不充分条件。
- **2014 经典研究**：控制测试数量后，覆盖率只是低到中等的缺陷预测因子（Inozemtseva & Holmes）。
- **gcov**（GCC 内置）/ **llvm-cov**（Clang）/ **LCOV**（gcov HTML 前端）是 C/C++ 覆盖率金标准。
- **SPARC**（arXiv 2602.16671）：场景规划+推理生成测试，比 vanilla prompting 高 31.36% 行覆盖率，突变分数提升 20.78%。

### 3.2 对阙疑的意义

阙疑的夹具目前没有覆盖率量化——不知道断言覆盖了多少代码路径。这可能是 402 F03（断言判别力不足）的根因之一：断言只覆盖了部分路径。

**落地项 COV1（立即可做，零新工具）**：对每颗新原子的夹具跑 gcov，记录行覆盖率/分支覆盖率，写入证据卡的 `coverage` 字段。低覆盖率（<80% 行）的夹具标 weak，必须补测试路径。
```bash
g++ -O0 --coverage fixture.cpp -o fixture
./fixture
gcov fixture.cpp  # 输出 fixture.cpp.gcov
```

**落地项 COV2（待验证假设）**：覆盖率 + 突变测试双指标闭环——454 的突变体杀灭测试（D1）和覆盖率结合，形成"执行了（COV1）+ 能检测（D1）"的双维度。写入夹具方法论 v2.0（443）的验收标准。

**证据**：2026 Botmonster 实验（93.1% vs 58.6%）+ Inozemtseva & Holmes 2014 + gcov 官方文档。

---

## 四、Agent 评估方法论：从"门禁全绿"到"任务完成率"

### 4.1 外部发现（证据等级：一手基准 + 工业实践，硬数据）

- **SWE-bench**：核心指标 **Resolved Rate**——生成的 patch 必须通过所有 fail-to-pass 测试（修了 bug）+ 所有 pass-to-pass 测试（没引入回归）。2294 Full / 500 Verified / 300 Lite。
- **SWE-bench Pro**（arXiv 2509.16941，2026-08）：长程软件工程任务，**GPT-5 只有 23.3% pass@1**——长程任务是当前 agent 的真正瓶颈。
- **IDE-Bench**（arXiv 2601.20886）：6000 runs，15 models，评估 pass@1/pass@5（同一任务独立跑 1/5 次至少成功一次的比例）。
- **MarketBench**（arXiv 2604.23897）：**自我评估能力**——模型预测自己成功率的能力，当前模型很差（校准度低）。
- **辅助指标**：Patch Apply Rate（补丁能语法正确应用）、Localization Success Rate（定位到正确文件）。

### 4.2 对阙疑的意义

阙疑目前的评估是"门禁全绿"（gate/replay/poison/pytest 全过），但没有端到端的"任务完成率"评估。

**落地项 EVAL1（立即可做，零成本）**：定义阙疑自己的**原子生产 Resolved Rate**——从 claim 到 verified 原子的完整闭环率，细分：
- 一次过率（红队零阻断直接 verified）
- 重修后过率（红队打回后修复 verified）
- 未完成率（卡在卡层/草稿未原子化）
- 目前 27 颗 verified，但没有这个细分统计——从第六批开始记录。

**落地项 EVAL2（立即可做）**：**红队预测校准率**——红队报告"阻断"的条目，经修复验证后确实是真问题的比例。MarketBench 指出模型自我评估差，阙疑的红队预测能力需要量化。373/402 两次对抗已经有数据，可以回溯统计。

**落地项 EVAL3（待验证假设）**：**pass@5 概念引入**——同一颗原子用不同提示词变体生产 5 次，看几次能过门禁。这是"提示词鲁棒性"的量化，也是 407 提示词压缩的验证手段。

**证据**：SWE-bench 官方 + SWE-bench Pro/IDE-Bench/MarketBench 一手论文。

---

## 五、链接器与 ODR 深化：弱符号与不可观测的 ODR 违反

### 5.1 外部发现（证据等级：ELF 规范 + C++ ABI 讲义，一手）

- **ODR 两种形式**：①普通外部链接实体（全程序恰好一个定义，违反 → "multiple definition" 错误）②特殊实体（类/模板/inline 函数/inline 变量可多 TU 定义但必须**逐词法一致**）。
- **弱符号**：未初始化全局变量（BSS 段）、inline 函数、`__attribute__((weak))`——链接器允许多个弱定义，**选一个丢弃其余**；强符号总是覆盖弱符号。
- **ODR 违反的不可观测性**：有些被链接器捕获（强符号冲突）、有些**完全不捕获**（不一致的 inline 定义，链接器静默选一个）、有些只在优化/LTO 后才显现。
- **inline 的真正目的**：允许多 TU 定义仍满足 ODR，**不是"优化提示"**——这是常见误解。
- **链接性三分类**：external（全局可见）、internal（static/匿名命名空间/const 变量）、no linkage（局部变量/类型定义）。

### 5.2 对阙疑的意义

INLINE-001 已经触及了弱符号合并（-O0 换链接顺序程序就变），但可以深化。

**落地项 ODR1（待验证假设，新原子选题）**：ATOM-LANG-ODR-001「ODR 违反的不可观测性」——
- claim：两个不一致的 inline 定义，链接器静默选一个，程序行为取决于链接顺序，且**零诊断**（IFNDR，和 INLINE-001 同族但更聚焦"不可观测"）
- 夹具：两个 TU 各定义一个不一致的 inline 函数，对比不同链接顺序的输出 + `nm` 输出显示弱符号 + `-Werror` 零警告
- 和 INLINE-001 的关系：INLINE-001 展示"顺序依赖"，ODR-001 展示"不可观测的不一致"——contrasts 关系

**落地项 ODR2（立即可做）**：INLINE-001 证据卡补充 `nm` 输出作为机制证据——显示 inline 函数是弱符号（`W` 标记），目前只有运行时输出，缺少链接器层面的机制证据。

**证据**：ELF 符号规范 + Dr. Zoltán Porkoláb C++ ABI 讲义 + Itanium ABI，一手。

---

## 六、本轮元批判（按 453 标准）

### 真增量（改变做法）

1. **记忆四类标准化（MEM1/MEM2）**：MEMORY.md 从"自由文本"升级为结构化四段，ground-truth 保留原则防止总结丢数据。零成本。
2. **覆盖率量化（COV1）**：夹具验收从"断言通过"升级为"断言通过 + 覆盖率达标"，直接解决 402 F03 的根因。零新工具（gcov 是 GCC 内置）。
3. **Agent 评估三指标（EVAL1/EVAL2）**：从"门禁全绿"升级为"一次过率 + 红队校准率"，量化系统自身的性能。零成本（回溯已有数据）。
4. **EH/ODR 新原子选题（EH1/ODR1）**：LANG 域的自然延伸，填补知识空白。

### 换术语（已有实践获得学名）

- 四类记忆 → 阙疑已有雏形（MEMORY.md/日志/提示词/上下文），只是没标准化
- 突变测试 + 覆盖率 → 454 D1 已有突变测试，COV2 是补覆盖率维度
- pass@5 → 407 提示词压缩已有多版本概念，EVAL3 是量化

### 明确不采纳/推迟

- CraniMem 的目标条件门控——过于复杂，当前阙疑不需要
- SWE-bench 式的外部基准——阙疑是知识生产系统不是软件工程 agent，指标需要自定义（EVAL1 已做）
- MSVC 异常模型——永久边界（无 cl.exe）

### 证据越界警示

- "93.1% 覆盖率 vs 58.6% 突变率"是 AI 生成测试的特定实验，不能直接平移到阙疑的手工夹具场景，但方向（覆盖率≠有效性）成立
- SWE-bench Pro 的 23.3% 是通用编码 agent，阙疑的原子生产是窄域任务，不可比

---

## 七、与已有架构的衔接

| 本轮落地项 | 强化/修正了哪个已有项 |
|---|---|
| MEM1/MEM2 记忆标准化 | 404 五维健康度的"记忆维"具体化；铁律 10 在记忆侧的对应 |
| MEM3 效用标签 | debt_ledger 思路在记忆侧的延伸 |
| EH1/EH2 异常原子 | LANG 域第二颗；454 S1 Sanitizer 矩阵补 EH 行 |
| COV1/COV2 覆盖率 | 443 夹具方法论 v2.0 验收标准；454 D1 突变测试的互补维度 |
| EVAL1/EVAL2/EVAL3 评估 | 404 五维健康度的"效率维"量化；412 成本核算的性能侧 |
| ODR1/ODR2 ODR 深化 | INLINE-001 的自然延伸；relations contrasts 的新案例 |

累计 81 份（374-457）。
