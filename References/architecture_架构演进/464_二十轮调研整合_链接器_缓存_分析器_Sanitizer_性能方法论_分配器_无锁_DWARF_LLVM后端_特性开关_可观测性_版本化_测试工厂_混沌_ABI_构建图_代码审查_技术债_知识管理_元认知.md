---
id: 464
title: 二十轮调研整合 链接器 缓存 分析器 Sanitizer 性能方法论 分配器 无锁 DWARF LLVM后端 特性开关 可观测性 版本化 测试工厂 混沌 ABI 构建图 代码审查 技术债 知识管理 元认知
status: active
type: architecture-note
created_at: 2026-09-13
---
# 464 · 二十轮调研整合：工具链纵深 × 工程范式 × 学习科学

> 20 个方向的外部调研 → 逐条消化 → 对阙疑的映射与裁决。
> 编号接续 463（十轮整合），本轮覆盖工具链内部机制、工程化范式、知识管理与学习科学三大簇。
> 元原则（448）：业界做法=假设→阙疑场景推演→小范围试点拿数据→数据支持才进规格。

---

## 一、工具链内部机制（7 方向）

### 1. mold 链接器：全流水线并行化

**核心事实**
- mold 比 lld 快 2.4–16.1×，比 GNU ld 快 112×（arXiv 2608.23228）。
- 设计哲学：无单一优化主导，全流水线并行化——符号解析、重定位、输出写入全部并行。
- 关键技术：多线程并行的符号哈希表、mmap 输出文件、增量链接支持。

**对阙疑的映射**
- 阙疑当前用系统默认 ld（MinGW/WSL），链接时间在单文件夹具中可忽略。
- 但多 TU 夹具（如 INLINE-001 的 4 文件+3 文件）链接时间会随文件数增长。
- **真增量**：多 TU 夹具增多后，可评估 mold 作为 CI 链接器加速（需 WSL 安装，当前环境无 mold）。
- **不采纳**：单文件夹具场景下 mold 无收益，不引入新依赖。

### 2. ccache/sccache 编译缓存

**核心事实**
- ccache 三模式：direct mode（哈希源文件直接命中）、preprocessor mode（先预处理再哈希）、depend mode（依赖文件追踪）。
- sccache 支持云存储分布式缓存（blake3 哈希）、多级缓存、Rust/C/C++ 通用。
- 命中率决定收益：头文件稳定时 direct mode 命中率可达 90%+。

**对阙疑的映射**
- 线 C 一直停在用户授权点（WSL 无 pip、Windows 无 ccache）。
- **真增量**：replay 全量跑 56 张卡时，每张卡独立编译——ccache 可将重复编译（同夹具不同卡）从 2min→5s。
- **落地路径**：用户授权后 `apt-get install ccache`（WSL），改 replay 调用前缀 `ccache g++`，WSL /tmp 构建目录。
- **不采纳**：sccache 云存储（单用户无分布式需求）。

### 3. Clang Static Analyzer：路径敏感符号执行

**核心事实**
- CSA 是路径敏感的符号执行分析器，不是简单的模式匹配。
- Z3 约束求解器可补偿精度（默认不启用，因性能开销）。
- 误报是核心问题：路径爆炸导致假阳性，需用户标注抑制。
- KNighter 等研究用 LLM 合成 checker 扩展规则。

**对阙疑的映射**
- 阙疑当前无 Clang（Windows/WSL 全无），CSA 无法本地运行。
- **真增量**：CSA 的"路径敏感"思想可迁移到红队——红队不应只看断言字面量，应追踪"断言→夹具→工件"的数据流路径（402 元结论：攻击按数据流穿链）。
- **不采纳**：安装 Clang+CSA（环境边界，且 MSVC 已定为永久边界）。

### 4. ASan 内部机制：shadow memory 1:8 映射

**核心事实**
- Shadow = (Mem >> 3) + SHADOW_OFFSET，每 8 字节应用内存映射 1 字节 shadow。
- Redzone（空间 bug）+ Quarantine（时间 bug）+ Stack poisoning（栈保护）三层。
- MSan 用 1:1 映射（未初始化检测，开销更大）。
- Memory Tagging（MTE）是硬件替代方案，ARM 已有支持。
- 局限：非线性越界（跳过 redzone）可能漏检；quarantine 耗尽后 temporal bug 漏检。

**对阙疑的映射**
- 阙疑已有 ASan/UBSan 双平台 replay，但 TSan 需 `setarch -R`（已知边界）。
- **真增量**：ASan 的"redzone 空间 + quarantine 时间"二分法可作为新原子选题——ALLOC 域的"内存错误的时空二维分类"。
- **真增量**：quarantine 耗尽漏检 = "工具检测能力的边界"，与 LEAK-002 的"LSan 零报告≠无泄漏"同族，可强化 MIS-MEM-031。
- **不采纳**：MSan（MinGW 不支持，WSL 需额外配置）。

### 5. Brendan Gregg 性能方法论：USE 方法 + 火焰图

**核心事实**
- USE 方法：每个资源检查 Utilization（利用率）、Saturation（饱和度）、Errors（错误率）三维度。
- CPU 火焰图（on-CPU）+ off-CPU 火焰图（等待时间）互补。
- 火焰图盲区：采样偏差（高频函数被过度采样）、缺失内核帧（权限不足）、不显示等待时间（需 off-CPU 图）。
- eBPF 可做运行时栈遍历，无需重新编译。
- 2025 SREnext 新方向：GPU/AI 火焰图。

**对阙疑的映射**
- 阙疑性能卡（PERF-003/004、CONC-002）当前只测"总耗时"，无火焰图级别的归因。
- **真增量**：USE 方法可写入性能卡方法论 v2.0——性能 claim 必须声明"瓶颈资源维度"（CPU/内存/锁/IO），而非只报耗时比。
- **真增量**：火焰图盲区清单直接对应红队 can't-miss——"性能卡的耗时归因是否排除了采样偏差？"
- **不采纳**：eBPF（Windows 不支持，WSL2 有限支持）。

### 6. jemalloc/tcmalloc：三级架构

**核心事实**
- tcmalloc：Thread cache（无锁）→ Central cache（有锁）→ Page heap（OS mmap）。小对象 ≤256KB 走 thread cache。
- jemalloc：per-thread tcache + arena 池（减少锁竞争）+ extent 管理。Redis/Firefox 默认。
- ptmalloc（glibc 默认）：全局锁，高并发争用严重；arena 数默认 8×num_cpus。
- mimalloc 是新竞争者（微软，设计更简洁）。
- 权衡：thread cache 增加内存占用和碎片（每个线程缓存有界对象不释放）。

**对阙疑的映射**
- ALLOC-002 已实测 arena/pool/bitmap 三策略的元数据权衡。
- **真增量**：jemalloc 的"arena 减少锁竞争"是 CONC 域新原子选题——"分配器的并发设计：全局锁→per-arena锁→thread cache"。
- **真增量**：tcmalloc 的"thread cache 增加碎片"直接强化 ALLOC-002 的"元数据换灵活性"结论——零锁不是免费的。
- **不采纳**：替换系统分配器（教学场景不需要）。

### 7. 无锁数据结构/RCU：ABA 与内存回收

**核心事实**
- Treiber Stack 是无锁"Hello World"，但包含 CAS 循环、内存回收、ABA 三大核心问题。
- ABA：值 A→B→A，CAS 无法区分。解决方案：tagged pointer（版本号）、hazard pointer、epoch-based reclamation、RCU。
- RCU：读无锁，写拷贝+原子替换指针，旧节点等宽限期后回收。Linux 内核核心机制。
- 2025 arXiv 新研究：coordination-free concurrent lock-free queues（无协调无锁队列）。
- Paul McKenney（RCU 之父）2026 仍活跃：P3347R4 指针生命周期提案。

**对阙疑的映射**
- CONC 域已有 FENCE/LOCK/RACE 三颗，无锁是自然延伸。
- **真增量**：CONC-004 候选选题——"ABA 问题：CAS 成功≠状态未变"，可用 Treiber Stack 实测。
- **真增量**：RCU 的"读无锁写拷贝"是"屏障≠原子类型"（CONC-001）的进阶——连原子类型都不用，靠协议。
- **不采纳**：实现完整 RCU（教学夹具只需演示 ABA + tagged pointer 修复）。

---

## 二、调试与编译器后端（3 方向）

### 8. DWARF 调试信息：DIE 树 + 行号程序 + CFI

**核心事实**
- DWARF v6 草案 2026-02 发布（sourceware）。
- 三大核心段：.debug_info（DIE 树，类型/变量/函数）、.debug_line（行号程序，地址→源码行映射）、.debug_frame（CFI 调用帧信息，栈展开）。
- DIE = Tag + Attributes，可引用其他 DIE（类型递归）。
- 栈展开可编译 DWARF 加速（"compiled DWARF"研究）。
- -g 生成 DWARF，-O2 优化后变量可能"optimized out"（DWARF 标记）。

**对阙疑的映射**
- 阙疑夹具用 -g 生成 .out 但不检查 DWARF。
- **真增量**：DWARF 的"optimized out"标记是性能卡的新观测维度——"变量被优化消除"可从 DWARF 直接读取，而非从 .asm 推断。
- **真增量**：行号程序（.debug_line）可验证"源码行→指令地址"映射，用于 claim 的"编译器在第几行做了什么优化"。
- **不采纳**：DWARF 解析工具（readelf/llvm-dwarfdump 已够用，不写自定义解析器）。

### 9. LLVM 后端：三种指令选择器 + Greedy 寄存器分配

**核心事实**
- FastISel（-O0，宏展开，快但代码质量差）、SelectionDAG（默认，DAG 重写+模式匹配，慢但好）、GlobalISel（gMIR 两次重写，AArch64 -O0/-O1 默认，x86 迁移中）。
- RAGreedy（Greedy 寄存器分配器）：优先级队列+溢出权重，默认优化构建用。
- RegAllocFast：-O0/debug 用，逐块分配。
- LLVM 20 后端优化聚焦快速路径：early exit（x86 单绑定定义）、SparseSet→vector 替换、regunit difflist 迭代优化。
- 指令选择是 NP-hard（一般情况），编译器用启发式（greedy tree matching / DAG rewriting）。

**对阙疑的映射**
- 阙疑性能卡看 .asm 但不区分"哪个后端阶段产生的指令"。
- **真增量**：FastISel vs SelectionDAG 的差异可作为新原子选题——"-O0 与 -O2 的指令选择差异：不只是优化多少，而是算法不同"。
- **真增量**：RAGreedy 的溢出权重 = "寄存器压力"的量化——性能卡可增加"溢出次数"作为活性观测（从 -fopt-info 或 asm 中 stack slot 计数）。
- **不采纳**：GlobalISel 研究（过于底层，教学价值低）。

### 10. C++ ABI Itanium：vtable 布局 + name mangling + RTTI

**核心事实**
- vtable 布局：offset-to-top（-16）、typeinfo pointer（-8）、虚函数指针（0+）。
- typeinfo 指针：多态类非零，非多态类为零；typeinfo 相等性检查用指针相等。
- -fno-rtti 会删除 RTTI 数据结构并重排 vtable（typeinfo 指针位置变空）。
- name mangling：_Z 前缀 + N（嵌套）+ 长度+名字 + 类型编码。
- 相对 vtable（Relative VTables，LLVM 2021）：用相对偏移替代绝对指针，减少重定位。

**对阙疑的映射**
- 阙疑已有虚函数/RTTI 选题候选（458）。
- **真增量**：vtable 布局的"offset-to-top + typeinfo + 函数指针"三段式可直接做原子卡——用 .asm 验证 vtable 结构（比纯理论硬）。
- **真增量**：-fno-rtti 对 vtable 的影响 = "编译选项改变对象内存布局"，是 ABI 稳定性的反例。
- **不采纳**：name mangling 完整规则（过于琐碎，c++filt 已解决）。

---

## 三、工程化范式（5 方向）

### 11. 特性开关工程化：kill switch / dark launch / canary

**核心事实**
- Kill switch：默认 ON 的 flag，用于即时禁用异常功能，无需重新部署。
- Dark launch：新代码在生产跑真实流量但结果丢弃，用于性能/正确性验证。
- Canary：渐进式流量（1%→5%→25%→100%）。
- Ring deployment：同心圆受众（内部→beta→全量）。
- Progressive delivery 降 MTTR 达 70%（行业数据）。
- OpenFeature 是开放标准（厂商中立 API）。

**对阙疑的映射**
- 阙疑的"铁律 7：不 push"= 手动 kill switch（人是开关）。
- **真增量**：特性开关思想可迁移到规则发布——新 gate 规则先 warn（canary），观察误报率后再升 block（全量）。当前 warn 32 条一次性 accept 缺乏渐进过程。
- **真增量**：dark launch = 红队的"盲读"——新规则在后台跑但不阻断，收集命中数据后再决定是否启用。
- **不采纳**：引入 feature flag 框架（单仓不需要）。

### 12. OpenTelemetry：三信号关联 + context propagation

**核心事实**
- Traces（稳定）、Metrics（稳定）、Logs（稳定）、Profiles（beta）四信号。
- TraceId/SpanId 是日志的一等字段，后端可直接关联日志与追踪。
- Context propagation via traceparent（W3C 标准），跨服务传递。
- 调试三段论：notice with metrics（发现异常）→ pinpoint with traces（定位位置）→ reason in logs（读原因）。

**对阙疑的映射**
- 阙疑的工具日志是散文式（print 到 stdout），无结构化 trace。
- **真增量**：412 成本核算需要"每原子/每批次 token 与窗口数"——OTel 的 trace 模型可直接映射：每个原子生产是一个 trace，每个步骤（夹具/卡/红队/门禁）是一个 span，span 带 token 数和耗时。
- **真增量**：459 的 Agent 可观测性 = OTel 的阙疑化——结构化 trace + 成本归因 + 失败定位。
- **不采纳**：引入 OTel SDK（Python 工具用 JSON 日志即可，不需要 OTLP 导出）。

### 13. semver API 版本化：deprecation 过渡期

**核心事实**
- deprecation 需至少一个 minor 版本过渡期（文档+警告），才能在 major 版本删除。
- 0.x 阶段：任何 breaking change 需显式迁移说明。
- MAJOR = 任何不兼容变更（运行时/类型/行为契约）。
- MINOR = 向后兼容新增。
- PATCH = bug fix，无 API 契约变更。

**对阙疑的映射**
- 阙疑的 gate 规则变更无版本管理——规则从 warn 升 block 是"breaking change"但无过渡期。
- **真增量**：规则版本化——每条规则有 status（experimental/stable/deprecated），experimental 只 warn，stable 可 block，deprecated 给过渡期。
- **真增量**：462 的 DEBT1（warn 量化分级）+ 规则版本化 = "规则的 semver"。
- **不采纳**：工具 CLI 的 semver（内部工具，无外部消费者）。

### 14. 测试数据工厂：Builder + Object Mother + Faker

**核心事实**
- Builder 模式：每个测试只设相关字段，其余用默认值。
- Object Mother：返回命名的常用 fixture（与 Builder 组合：Mother 返回 Builder + 一个场景变更）。
- Faker：生成真实感假数据，但需确定性 seed（可复现）。
- Factory vs Fixture：静态 fixture 用于不变数据，Factory 用于需要变体的场景。
- 新增必填字段时只需改 Builder（测试弹性）。

**对阙疑的映射**
- 阙疑的毒样例（P1–P30）是手写的，每个毒样例是完整 YAML 文件。
- **真增量**：毒样例生成可用 Factory 模式——基础毒样例模板 + 字段覆盖，减少重复（当前 30 个毒样例有大量重复结构）。
- **真增量**：461 的突变测试算子（关系运算符翻转/常量替换/语句删除）= 毒样例的 Faker——自动生成变异体。
- **不采纳**：引入 FactoryBoy 等框架（Python 字典即可）。

### 15. 混沌工程：稳态假设 + 爆炸半径 + Game Day

**核心事实**
- 混沌工程 = 假设检验，不是随机破坏。假设："在 X 故障下，稳态行为 Y 维持。"
- 稳态 = 可量化指标（成功率/延迟/错误率）。
- 爆炸半径控制：1% 流量起步，kill switch 随时中止。
- Chaos under load：空闲系统测试故障处理代码路径，负载下测试排队动力学/重试风暴/连接池行为。
- Game Day：团队级演练，测试 runbook/告警/值班/沟通，不只是代码。

**对阙疑的映射**
- 阙疑的对抗（368/373/402/452）= 混沌工程的阙疑化——注入"恶意原子"故障，观察门禁是否维持稳态。
- **真增量**：对抗提示词应显式写"稳态假设"——"在 X 攻击下，gate block 应非零 / replay 应 refute"。当前 452 有逃逸登记但缺稳态假设的形式化。
- **真增量**：Chaos under load = 对抗应在"全量 56 卡"负载下跑（而非单卡），观察规则间的交互效应。
- **不采纳**：Game Day（单人项目，无团队响应流程可测）。

---

## 四、构建与质量（3 方向）

### 16. Bazel 构建依赖图：hermeticity + action graph

**核心事实**
- Bazel 模型：repo = BUILD target 图，每个 target 有显式依赖。
- Hermetic build：默认隔离环境，只访问声明的输入。
- Action graph：inputs/command/env 未变则跳过执行（增量构建）。
- Remote caching + remote execution（Remote Execution API）。
- 代价：需手写 BUILD 文件，学习曲线陡。

**对阙疑的映射**
- 阙疑的 replay 每次全量编译 56 张卡，无增量。
- **真增量**：462 BUILD1（工件缓存键=sha256(夹具.cpp)+command+compiler）= Bazel action graph 的阙疑化。
- **真增量**：Bazel 的 hermeticity 思想 = replay 的"命令必须声明全部输入"——当前 command 是字符串，未声明依赖头文件，头文件变更不会触发重编译。
- **不采纳**：迁移到 Bazel（单仓 56 夹具，Make/直接 g++ 已够用）。

### 17. 代码审查自动化：Gerrit patchset + AI 审查

**核心事实**
- Gerrit：patchset 工作流（变更入库前审查），细粒度权限，Jenkins 集成。
- AI 代码审查 2025 趋势：上下文理解+重构建议+性能优化+规范一致性。
- 审查瓶颈：开发者等 review 数小时到数天。
- AI 审查在 CI/CD 中做"first-pass review"，人类审查聚焦高风险变更。

**对阙疑的映射**
- 阙疑的红队 = AI 代码审查的阙疑化（独立子 agent 两段式盲读）。
- **真增量**：Gerrit 的 patchset 思想 = 红队应审查"变更集"而非"最终文件"——当前红队读最终卡，不读 diff，可能漏掉"改了什么"。
- **真增量**：AI 审查的"first-pass"定位 = 红队应先做机械检查（断言/sha/格式），再做语义审查（claim/口径/活性），当前混在一起。
- **不采纳**：部署 Gerrit（GitHub PR 已够用）。

### 18. 技术债量化：SQALE 模型 + debt ratio

**核心事实**
- SQALE 方法：TDR = (Remediation Effort / Development Effort) × 100。
- Development Effort = LOC × 30 分钟/行（SonarQube 默认）。
- TDR < 5% = 良好维护；> 15% = 债务增长快于修复。
- 1M LoC 项目技术债年成本 $306K（SonarSource 2023 数据）。
- 自底向上（静态分析）vs 自顶向下（经济模型）两条量化路径。

**对阙疑的映射**
- 阙疑 warn 32 条是技术债，但无量化。
- **真增量**：462 DEBT1（warn 四级分类 block/warn_real/advice/noise）+ SQALE = 每条 warn 有 remediation effort（修复估计分钟数），总 debt ratio 可算。
- **真增量**：golden_lock 的"warn 8→32 一次性 accept"= 技术债的"借新债"，应记录 debt ratio 变化（当前只记数字，不记比率）。
- **不采纳**：SonarQube 全量接入（Python 工具，SonarQube 对 Python 支持有限，且单仓太小）。

---

## 五、知识管理与学习科学（2 方向）

### 19. Zettelkasten：原子笔记 + 链接网络

**核心事实**
- 三原则：Atomicity（一卡一想法）、Autonomy（独立可读）、Connectivity（链接优先于分类）。
- 三类笔记：fleeting（快速捕捉）、literature（来源处理）、permanent（持久链接知识）。
- Luhmann 90,000 张卡 40 年，产出 70+ 本书。
- 失败原因：手动写原子笔记成本高、链接维护成本高、无即时反馈。
- 2026 趋势：AI 自动生成永久笔记 + 双向链接 + 间隔重复集成。

**对阙疑的映射**
- 阙疑的原子卡（ATOM-*）= Zettelkasten 的 permanent note（一卡一 claim，独立可读，relations 链接）。
- **真增量**：Zettelkasten 的"每新卡必须链接 ≥2 现有卡"= 阙疑 relations 的硬约束——当前 relations 是可选的，应升级为"新原子必须有 ≥1 个 prerequisite/specializes"。
- **真增量**：fleeting note = 每日日志（2026-09-13.md），literature note = 调研文档（464），permanent note = 原子卡——三层笔记体系已存在但未显式命名。
- **不采纳**：Obsidian/Roam 等工具（Markdown 文件已够用）。

### 20. 元认知/学习科学：间隔重复 + 主动回忆 + 交错练习

**核心事实**
- 间隔重复：Cepeda 2006 元分析 254 研究，SMD=0.42（中等效应）；FSRS 算法 2022-2026 成为新标准（替代 SM-2）。
- 主动回忆（测试效应）：回忆比重读好，80% vs 34% 保留率（多项研究）。
- 交错练习：混合主题比集中练习好，虽然当下更难。
- 元认知：准确区分"知道"与"不知道"是学习效率最强预测因子（Metcalfe 2009，强元认知学生高 23%）。
- 一个月不复习遗忘 80%。

**对阙疑的映射**
- 阙疑的教学转化（405）有闪卡/MCQ/学习路径 DAG，但未接入间隔重复。
- **真增量**：闪卡系统应集成 FSRS 调度（而非简单的"全部复习"）——405 的闪卡设计需加"下次复习时间"字段。
- **真增量**：主动回忆 = 闪卡正面是问题（不是答案）——405 已提"正面是问题"，但需强化为硬约束。
- **真增量**：元认知 = 学习者自评"我懂了吗"——教学代理应加"自信度自评"字段，与实际测试正确率对比，校准元认知。
- **不采纳**：Anki 集成（独立工具，不在阙疑范围内）。

---

## 六、真增量汇总（按优先级）

### P0（直接解决已知问题）
| ID | 方向 | 增量 | 对应已知问题 |
|---|---|---|---|
| 464-T1 | ccache | replay 全量 2min→5s | 线 C 停在授权点 |
| 464-T2 | 特性开关 | 规则 warn→block 渐进发布 | warn 32 一次性 accept |
| 464-T3 | 混沌工程 | 对抗稳态假设形式化 | 452 缺稳态假设 |
| 464-T4 | OTel | 每原子 trace+span 成本归因 | 412 成本核算无数据来源 |

### P1（增强现有能力）
| ID | 方向 | 增量 |
|---|---|---|
| 464-T5 | ASan | 时空二维分类新原子 + quarantine 漏检强化 MIS |
| 464-T6 | USE 方法 | 性能卡必须声明瓶颈资源维度 |
| 464-T7 | 无锁/RCU | CONC-004 ABA 问题选题 |
| 464-T8 | DWARF | optimized out 作为性能卡观测维度 |
| 464-T9 | LLVM 后端 | -O0/-O2 指令选择差异新原子 |
| 464-T10 | Itanium ABI | vtable 布局实测原子卡 |
| 464-T11 | 测试工厂 | 毒样例 Factory 模式 + 突变体自动生成 |
| 464-T12 | semver | 规则版本化（experimental/stable/deprecated） |
| 464-T13 | SQALE | warn 量化 + debt ratio |
| 464-T14 | Zettelkasten | 新原子必须 ≥1 relations 链接 |

### P2（远期/新原子选题库）
| ID | 方向 | 增量 |
|---|---|---|
| 464-T15 | jemalloc | 分配器并发设计新原子 |
| 464-T16 | 学习科学 | 闪卡 FSRS 调度 + 元认知自评 |
| 464-T17 | mold | 多 TU 夹具增多后评估 |
| 464-T18 | CSA | 路径敏感思想迁移到红队 |
| 464-T19 | Bazel | replay 命令声明全部输入 |
| 464-T20 | Gerrit | 红队审查 diff 而非最终文件 |

---

## 七、换术语（已有对应，仅命名升级）

| 业界术语 | 阙疑已有 | 命名升级 |
|---|---|---|
| Progressive delivery | 铁律 7 不 push | 规则渐进发布 |
| Dark launch | 红队盲读 | 后台试运行 |
| Kill switch | 人审签署 | 人工熔断 |
| Game Day | 对抗批次 | 对抗演练 |
| Hermetic build | replay 沙箱 |  hermetic 复现 |
| Atomic notes | 原子卡 | 一卡一 claim |
| Permanent notes | atoms/ 目录 | 持久知识层 |

---

## 八、不采纳清单（附理由）

| 方向 | 不采纳项 | 理由 |
|---|---|---|
| mold | 引入 mold 链接器 | 单文件夹具链接时间可忽略 |
| CSA | 安装 Clang+CSA | 环境边界，MSVC 已永久边界 |
| ASan | MSan | MinGW 不支持 |
| USE/eBPF | eBPF  profiling | Windows 不支持 |
| 分配器 | 替换系统分配器 | 教学场景不需要 |
| DWARF | 自定义解析器 | readelf/llvm-dwarfdump 已够用 |
| LLVM | GlobalISel 研究 | 过于底层 |
| ABI | name mangling 完整规则 | c++filt 已解决 |
| 特性开关 | feature flag 框架 | 单仓不需要 |
| OTel | OTel SDK + OTLP 导出 | JSON 日志即可 |
| semver | 工具 CLI semver | 内部工具无外部消费者 |
| 测试工厂 | FactoryBoy 框架 | Python 字典即可 |
| 混沌 | Game Day | 单人项目无团队流程 |
| Bazel | 迁移到 Bazel | 单仓 56 夹具，直接 g++ 已够用 |
| 代码审查 | 部署 Gerrit | GitHub PR 已够用 |
| 技术债 | SonarQube 全量 | Python 支持有限+单仓太小 |
| Zettelkasten | Obsidian/Roam | Markdown 已够用 |
| 学习科学 | Anki 集成 | 独立工具 |

---

## 九、与 460/462/463 的关系

- 460：7 层 40 落地项全景图（宏观蓝图）
- 462：增量构建/属性测试/差分测试/结构化输出/技术债量化（5 项具体规格）
- 463：优化报告/覆盖率/CI 缓存/文档即代码/知识图谱/Agent 评估/幻觉检测/语义检索/Agent UX/上下文管理（10 方向，真增量 4）
- **464**：20 方向纵深，真增量 20（P0×4 + P1×10 + P2×6），重点在工具链内部机制（7 方向）和工程范式（5 方向）

**464 的独特价值**：前 463 份调研偏"Agent 系统/方法论"，464 首次大规模覆盖"C++ 工具链内部机制"（链接器/分配器/Sanitizer/ABI/LLVM 后端/DWARF），为新原子选题库提供了 8 个候选方向（T5/T7/T9/T10/T15 + 458/459 已有选题），直接解决"MEM 域边际递减、需要新域选题"的问题。

---

## 十、下一步

1. **P0 四项**可直接写入下一轮苦力提示词（T1 ccache 需用户授权，T2/T3/T4 零成本）。
2. **新原子选题库**：T5（ASan 时空分类）、T7（ABA）、T9（指令选择差异）、T10（vtable 布局）、T15（分配器并发）——5 个候选，可排入 CONC/ALLOC/UB 域后续批次。
3. **规则版本化**（T12）+ **warn 量化**（T13）+ **渐进发布**（T2）= 规则治理三件套，可合并为一个苦力批次。
4. **465** 候选方向：形式化验证深化（Lean/Coq）、属性测试实战（Hypothesis）、差分测试框架、LLM 评估基准（SWE-bench 适配）、Agent 安全（prompt injection 防御）。
