# C++ ULTIMATE BIBLE — SUPREME ENGINEERING SPECIFICATION

> 本文件是《现代 C++ 终极圣经》项目的**最高质量宪章**。由用户于 2026-08-11 下达。
> 落地细则见仓库根 `CONVENTIONS.md`（其 §0 引用本文件，§1/§10/§11 将本宪章的操作要求转为强制规范）。
> 任何写作、扩写、修订活动均优先遵循本宪章的优先级与反幻觉/验证协议。

---

## 当前自评快照（用户下达时）

| 维度 | 评价 |
|---|---|
| 知识覆盖广度 | 9.3/10 |
| 单章深度 | 8.7/10 |
| 工程实践覆盖 | 8.8/10 |
| 源码/底层分析 | 8.5/10 |
| 教材体系结构 | 8.3/10 |
| 代码实例密度 | 8.5/10 |
| 标准准确性 | 7.0/10 |
| 实现细节可靠性 | 6.8/10 |
| 交叉引用/工程完整性 | 6.0/10 |
| 最终成书质量 | 约 7.5～8/10 |

**最弱三项（优先治理）**：交叉引用/工程完整性 (6.0) → 实现细节可靠性 (6.8) → 标准准确性 (7.0)。
→ 对应本宪章 §2（五层真相模型）、§6（验证体系）、§7/§8（标准依据与反幻觉）。

---

## 一、最高原则

1. **正确性 > 完整性 > 深度 > 广度 > 篇幅。** 宁可少写，也绝不允许错误、幻觉、伪深度和未经验证的专业结论进入正文。
2. 不允许为了"看起来高级"而堆砌术语。任何术语都必须真正解释：是什么 / 为什么存在 / 解决什么问题 / 底层如何工作 / 什么时候使用 / 什么时候不要使用 / 代价是什么 / 边界在哪里 / 与其他机制有什么关系。
3. 不允许把"知识点集合"误认为"知识体系"。必须建立 `Prerequisite → Concept → Mechanism → Consequence → Implementation → Engineering → Performance → Trade-off` 完整知识链。
4. 不允许把 C++ 标准、编译器实现、标准库实现、ABI、操作系统、CPU 行为混为一谈。任何涉及这些层级的内容，必须明确标注所属层级。

## 二、五层真相模型

所有重要技术结论必须尽可能归入以下层级：

- `[STANDARD]` ISO C++ 标准保证的行为。
- `[IMPLEMENTATION]` GCC / Clang / MSVC / libstdc++ / libc++ / MSVC STL 等具体实现行为。
- `[ABI]` 名称修饰、对象布局、调用约定、vtable、RTTI、异常 ABI、二进制兼容等。
- `[PLATFORM]` Linux / Windows / macOS / ELF / PE / x86-64 / ARM64 等平台行为。
- `[MICROARCHITECTURE]` CPU cache、branch prediction、TLB、pipeline、SIMD、memory hierarchy 等硬件层行为。

绝不允许：`IMPLEMENTATION → STANDARD`、`ABI → STANDARD`、`PLATFORM → STANDARD`、常见经验 → 必然规律。必须明确告诉读者："标准保证了什么""实现通常做什么""某平台目前怎么做""为什么不能把后者当成前者"。

（仓库落地标签见 `CONVENTIONS.md` §1：`[标准]`/`[实现]`/`[ABI]`/`[平台]`/`[微架构]`/`[经验]`。）

## 三、知识覆盖目标

逐步覆盖 A–BZ 共 73 个领域（基础、类型系统、对象模型、模板、Concepts、constexpr、异常、RTTI、协程、ranges、STL、allocator/PMR、内存管理、并发、atomic、内存模型、lock-free、filesystem、networking、序列化、测试、调试、sanitizer、profiling、benchmark、编译器优化、汇编、ABI、链接、ELF/PE、OS 交互、CPU 架构、cache/SIMD、data-oriented design、泛型/面向对象/函数式、设计模式、架构、CMake、包管理、构建系统、CI/CD、静态分析、安全、嵌入式、游戏、图形、HPC、大型工程、遗留现代化、C 互操作、生态、真实源码分析）。

持续检查："这个领域是否已经覆盖？""覆盖是否只是名词级？""是否真正解释了内部机制？""是否存在知识断层？"

## 四、每一个重要知识点必须达到六层深度

- Level 1 — WHAT 它是什么？
- Level 2 — WHY 为什么存在？解决什么历史/工程问题？
- Level 3 — HOW 语言规则、编译器、运行时、标准库内部如何实现？
- Level 4 — CONSEQUENCE 它会导致什么行为？什么情况下会踩坑？
- Level 5 — ENGINEERING 真实工程中什么时候使用？什么时候禁止使用？替代方案？trade-off？
- Level 6 — BOUNDARY 它在哪些条件下失效？哪些是 implementation detail？哪些是 UB / unspecified / implementation-defined？

重要主题不得停留在 Level 1～2。

## 五、必须建立"知识依赖图"

每个高级知识点必须能追溯其前置知识（move semantics → value category → reference → object lifetime → temporary materialization → copy elision → exception guarantee → noexcept → container relocation）。不要孤立解释知识，要不断回答："它为什么能够成立？""它依赖什么？""它又影响什么？"

## 六、代码必须进入验证体系

任何具有教学意义的重要代码，都不能仅凭语言模型推断。必须尽可能验证：编译 / 运行 / 输出 / 边界行为 / 异常行为 / UB Sanitizer / 不同编译器 / 不同标准版本 / 必要时 assembly。优先覆盖 GCC、Clang、MSVC 与 C++17/20/23/26。对于无法实际验证的内容：明确写 `[UNVERIFIED]`，绝不伪装成 VERIFIED。

（仓库落地标签见 `CONVENTIONS.md` §10：`[VERIFIED]`/`[UNVERIFIED]`/`[NEEDS-VERIFY]`，由 `tools/verification_audit.py` 审计覆盖度。）

## 七、标准依据体系

涉及标准规则时必须尽可能给出：C++ 标准版本 / feature / 相关 clause / section / feature-test macro / 相关 WG21 proposal / 必要时说明历史变化。不得凭记忆捏造 proposal 编号。不确定时写："需要进一步核验标准来源。"绝不允许："看起来合理，所以应该是真的。"

## 八、反幻觉协议

任何以下内容进入高风险区域：标准条款 / 标准版本 / proposal 编号 / 编译器实现 / ABI / 对象布局 / 内存模型 / 并发 lock-free / allocator / 优化 / 汇编 / CPU 行为 / benchmark / 复杂度 / 标准库内部实现，必须主动进行二次审查。禁止伪造标准条款、proposal、源码位置、benchmark、编译结果、ABI 保证，或把常见实现写成标准保证。如果无法确认：宁可保留不确定性。

## 九、反"AI 水文"协议

禁止：空泛总结 / 重复定义 / 机械模板 / 无意义历史 / 无意义"优缺点"/"面试题"/"代码"/伪深度/术语堆砌/"工业界广泛使用"但无具体场景/"性能更好"但不解释为什么/"底层很复杂"但不解释复杂在哪里。每一段必须至少承担一种功能：定义/解释/推导/证明/机制/实例/实验/反例/比较/工程决策/性能分析/源码分析/标准边界。如果一段删除后不损失知识，应删除。

## 十、反重复协议

同一个知识点允许多次出现，但每次出现必须承担不同作用（建立概念 / 解释机制 / 工程使用 / 底层实现 / 性能架构）。禁止复制粘贴式重复。

## 十一、工程真实性

不要只写"可以这样写"，必须进一步讨论：为什么这样设计？规模变大后怎么样？多线程？异常？性能？ABI？可测试？可维护？错误传播？资源生命周期？失败模式？替代设计？必须大量加入真实工程中的 trade-off / failure mode / anti-pattern / migration / legacy compatibility / debugging / profiling / maintenance / observability / testing。

## 十二、必须建立"反例驱动教学"

优秀知识不能只有正确代码，必须尽可能同时展示：正确版本 / 错误版本 / 为什么错误 / 编译器可能如何处理 / 运行时可能发生什么 / 是否 UB / 如何检测 / 如何修复。尤其针对 UB / lifetime / dangling / aliasing / data race / iterator invalidation / exception safety / ODR / 并发 / template deduction / overload resolution。

## 十三、性能章节必须拒绝玄学

任何"更快/更慢/零开销/cache friendly/branch prediction/减少分配"都必须解释机制。尽可能使用复杂度 / allocation count / cache behavior / branch behavior / instruction count / assembly / benchmark / profiling，并明确 benchmark ≠ universal truth，解释测试环境 / compiler / optimization level / CPU / dataset / measurement method / 可能的 bias。

## 十四、源码阅读必须形成方法论

不仅告诉读者"这是 vector 的源码"，还必须教会：如何定位入口 / 从接口找到实现 / 追踪 template / 阅读 traits / 阅读 allocator / 追踪异常路径 / 阅读 assembly / 识别 ABI / 区分标准要求和实现选择。最终目标：读者能自己阅读 libstdc++ / libc++ / MSVC STL / GCC / Clang / CMake / Linux runtime / 大型 C++ 项目。

## 十五、建立"实验室"

整本书不是纯文本，应逐渐形成 `examples/ experiments/ benchmarks/ assembly/ tests/ sanitizers/ compiler-tests/ abi-tests/`。每个重要理论尽可能对应实验（memory_order → litmus test；vector growth → allocation benchmark；virtual dispatch → assembly experiment；copy elision → compiler output；false sharing → benchmark；allocator → allocation experiment；coroutine → 生成的状态机检视）。最终"理论 → 实验 → 结果 → 解释"形成闭环。

（仓库已有 `Examples/`、`Benchmarks/`、`Assembly/`、D5 性能附录与 `_bench_d5_*.cpp` 证据源，朝此目标对齐。）

## 十六、建立"版本时间轴"

对 C++ 特性建立 C++98/03/11/14/17/20/23/26 时间轴：什么时候出现 / 为什么出现 / 解决什么问题 / 之前如何实现 / 现在推荐什么 / 旧代码如何迁移。尤其注意：不要把 C++26 尚未正式标准化/实现状态不稳定的内容写成既定事实。

## 十七、建立"现实世界差异"

对关键机制尽可能比较 GCC / Clang / MSVC / libstdc++ / libc++ / MSVC STL / Linux / Windows / macOS / x86-64 / ARM64，但必须明确：这是实现差异，不是语言规则。

## 十八、教材必须服务不同层次读者

同一主题尽可能提供：入门理解 / 核心规则 / 深入机制 / 底层实现 / 工程实践 / 高级扩展，让初学者能看懂、本科生能系统学习、考研能复习、工程师能查阅、高级开发者能深入、研究者能追踪标准。

## 十九、建立"决策树"

不要只告诉用户"使用 unique_ptr"，要告诉：什么时候 unique_ptr / shared_ptr / 裸指针 / reference / value / observer_ptr / intrusive pointer / custom ownership，形成 需求 → 约束 → 设计选择 → trade-off → 最终方案。

## 二十、最终质量标准

每完成一个章节，必须主动审查：[1] Correctness [2] Standard Accuracy [3] Version Accuracy [4] Implementation Accuracy [5] Depth [6] Engineering Value [7] Examples [8] Verification [9] Counterexamples [10] Dependencies [11] Redundancy [12] Terminology [13] Cross References [14] Maintainability [15] Hallucination Risk。

## 二十一、禁止"为了完成任务而完成任务"

如果当前章节已经足够好：不要强行扩写。如果发现旧章节存在错误：优先修复旧章节。如果发现知识体系存在断层：优先补断层。如果发现大量重复：优先重构。如果发现代码未经验证：优先验证。如果发现标准依据缺失：优先核查。如果发现交叉引用损坏：优先修复。永远优先：Correctness > Consistency > Verification > Depth > Architecture > Expansion。

## 二十二、Agent 工作模式

每次启动任务后：STEP 1 扫描当前仓库。STEP 2 读取目录结构、SUMMARY、索引、相关章节。STEP 3 建立当前知识地图。STEP 4 寻找最高价值缺陷。STEP 5 不要平均用力，优先修复高风险错误 / 知识断层 / 标准错误 / 实现误导 / 大量重复 / 失效链接 / 未经验证代码 / 严重浅层内容。STEP 6 完成一个完整、可验证的小任务。STEP 7 重新审查修改影响。STEP 8 更新交叉引用。STEP 9 记录：修改了什么 / 为什么 / 验证了什么 / 仍有什么不确定 / 下一步最值得做什么。禁止一次性大规模重写整个仓库。

## 二十三、终极目标

最终成果不是"一本很厚的 C++ 书"，而是 C++ Knowledge Graph + Textbook + Reference + Engineering Handbook + Source Code Guide + Experiment Laboratory + Performance Guide + Standards Guide + Debugging Guide + Architecture Guide 的统一体系。让真正优秀的 C++ 工程师/研究者面对这套体系时，不会首先问"这里还缺什么？"，而会开始问"这里的标准依据在哪里？""这个实现为什么这样做？""这个 trade-off 为什么成立？""这个实验能否复现？"

## 最终验收标准

如果一本普通教材做到"讲得全面"，本项目必须做到"讲得全面 + 讲得深 + 讲得准 + 有证据 + 可验证 + 可复现 + 有工程价值 + 有知识网络 + 长期可维护"。唯一的完成标准是：优秀 C++ 工程师/研究者会开始追问标准依据、实现动机、trade-off 与可复现性——而非追问"还缺什么"。
