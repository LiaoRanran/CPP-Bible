# 564-01 · Oracle 类型学与跨域泛化

> 解剖与联网均在 2026-09-17/18；标注【已实现/设计/未实现/理论未实证】。
> 探针实跑输出见 [_arch_v7/probes/](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/_arch_v7/probes/)。

## 开头一句话（投喂词第四问）

**抽走 g++ 后当场还能跑的通用内核**：三分类语义、claim_structured 分流、V-iso"可证伪条件必须存在"的思想、C-P 上界与样本量算子、分权/异族模型族、grounded 论证、收敛三曲线、task_queue、golden 快照审计、frontmatter 硬化——它们只依赖"存在一个能产生可复现输出的判官"。
**立刻归零的**：P0-A 独立重编译、run_match 逐字比对、artifact_sha/compile_rc、matrix 编译器对拍——它们就是 g++ 本身，不是内核。
**本仓已活着的弱 Oracle 内容（80 条误解库 MIS-*）今天的真实状态**：**字段填满了，机器没有判真伪**——门禁只校验结构（id/name/level 合法、deep 类 refutations≥2、source 非空 warn）和引用完整性（原子引用的 MIS-ID 必须存在），没有任何一道机械判据检查 refutation 文本本身对不对；它们既不 confirm 也不 refute，是**"结构合规但未验证"的第三态，却没有任何字段承认这一点**。
**离重新长出 Oracle 差三块**：①把"判官存在吗"变成接入前必答的显式判定（A3 SOP）；②给弱 Oracle 内容一个诚实状态（不能叫 verified，只能叫 witness-catalog/可证伪性已组织）；③弱判官叠加时的相关性登记（两个都引自同一章 Book 不是独立佐证）。

---

## A0 本仓解剖：弱/无编译 Oracle 的内容今天实际走什么判决（真实数据，不是思想实验）

### A0.1 56 张证据卡：0 张无编译——"历史/语言/UB"卡其实都在借编译器当 Oracle
探针实跑（2026-09-17，逐卡 parse + replay_card）：

| 卡 | 表面域 | 实际判决 | 结论 |
|---|---|---|---|
| [EV-HIST-001](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/evidence/hist/EV-HIST-001.md)（auto_ptr 史） | 历史结论 | `-std=c++14` 真编译成功 + 工件含 `_ZNSt8auto_ptr` 符号 + artifact_sha 复现；actual 另记 c++17/c++23 的 impl 状态 | 【已实现】历史命题"c++17 移除 auto_ptr"被翻译成**编译器可用性证据**：老标准编得过、新标准无该符号——Oracle 还是 g++ |
| [EV-UB-001](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/evidence/ub/EV-UB-001.md)（求值序） | UB 规范 | 6 工具链 × O0/O2 真跑 8 组 run_* + asm 符号断言 + sha/P0-A | 【已实现】强 Oracle |
| [EV-LANG-001](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/evidence/lang/EV-LANG-001.md)（inline ODR） | 语言规则 | 27 条命令全 rc=0、20 个 run_match_file key、多 asm sha | 【已实现】强 Oracle |

全库计数：56/56 有 command，56/56 有 artifact，**0 张无编译卡**。三分类对它们完全有效（全部 confirm，判 compile_rc/run_match/artifact_sha/recompile 四件套）。
⇒ **"历史卡是弱 Oracle"是错觉**：它们是把历史/规范命题精心转译成了编译器可判的命题。这本身就是跨域的第一个真实技巧（A3 复用）。

### A0.2 80 条误解库：本仓第一个真正"无机械判官"的人口
[misconceptions/](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/misconceptions) 80 条 MIS-*.md，形态（以 [MIS-CONC-001](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/misconceptions/MIS-CONC-001.md) 为例）：trigger_patterns + refutations（多条）+ source（指向 Book 章节）+ related_atoms。
机器今天对它们判什么（[gate_engine.py:754-801](file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools/gate_engine.py#L754-L801)）：
- `MIS-LIBRARY`（block）：id/name 非空、level∈{surface,deep}、deep 的 refutations≥2；source 缺失仅 warn；
- `ATOM-MISCONCEPTION-REF`（block）：原子 pedagogy.misconceptions 引用的 ID 必须存在。
**机器不判什么**：refutation 文本的真假、trigger_patterns 是否真是常见错误说法、source 指向的 Book 段落是否真支持该反驳。一条写得结构完美但内容错误的 MIS 条目（例如声称"volatile 提供原子性"）**全绿入库**。
⇒ 定性：这是**引用闭包 + 结构校验型弱 Oracle**（判官=人写的 Book + 人自己），当前没有任何可复现实验支撑其内容。56 张证据卡中若有卡的 related 原子引用了它，教学结论被当作反例使用，但反例本身未经机验。

### A0.3 136 条 warn 与存在性/计时类内容
- warn（136 条，最大头 ATOM-CLAIM-CONCEPT-NORMALIZED 77 条）**不是 Oracle 判决，是"等人"队列**——机器没有判，把判断显式留给人；这是诚实设计，但 B 块要问人是否真在判（见 02）。
- 含 run_commands 的存在性卡仍走真编译，不存在"无 Oracle 证据卡"人口（56/56 已证）。

## A1 Oracle 类型学（强度维度全部可计算）

| Oracle 类型 | 可复现性 | 错误率能否给上界 | 单次成本（本仓口径） | 对人依赖 | 能证什么 | 不能证什么 | 典型失效 |
|---|---|---|---|---|---|---|---|
| 可复现实验（g++ 真编译/真跑） | 高（sha 锁工具链） | 能（563：0 失效 C-P 上界） | 0.08–1.8s/编译，全量 127s | 零（写夹具时高） | "此刻此编译器确实产生它" | 跨编译器/跨版本成立；语义层因果 | 编译器自身 miscompile；夹具偷看答案（cat 式 E05） |
| 差分对拍（多编译器/多 O） | 高 | 能（分歧率） | 乘工具链数 | 低 | "结论非单家实现偶然" | 谁对（全错时沉默） | 共同错误模式；UB 下实现各异但都合法 |
| 形式证明/模型检验 | 极高（证明可机核） | 证明本身近乎零错，**建模错误无界** | 极高（人力周/月） | 建模时极高 | 模型内性质 | 模型外现实 | 规约写错证明了错东西；C++ 内存模型/并发开放问题（561） |
| 统计检验/RCT | 中高（依赖预注册） | 能（功效/置信区间） | 中 | 中（设计） | 总体效应区间 | 单次事件因果 | p-hack、选择偏差、分布漂移 |
| 高保真仿真 | 中 | 部分（与现实对标误差） | 高 | 高（标定） | 仿真世界内行为 | 现实世界 | 仿真器偏差、未建模通道 |
| 多独立来源交叉 | 低-中 | 只有来源独立时才能用 563 二项框架 | 低（检索） | 高（甄别） | 收敛性/可查性 | 事实本身 | 同源复制（全部抄一处）、集体错、引文腐烂 |
| 权威 ground-truth 基准（标准文本/cppreference） | 中（版本化后高） | 不能给数值上界 | 低 | 高（解释） | "规范怎么写" | 实现是否如此 | 草案变动、误读、标准与实现背离 |
| 引用闭包可验 | 高（链存在性可机判） | 不能 | 极低 | 中 | "每条声称可溯源" | 源内容真伪 | 挂名引用、源本身错（MIS 库现状） |
| 纯人签 | 低 | 能测但靠盲审设计（见 02） | 高且会疲劳 | 完全 | 不可机验域的兜底 | — | rubber-stamp/automation bias/利益冲突 |

**关键可计算量**：每种 Oracle 都应登记四元组 `{reproducible: bool, error_bound: {n,k,conf} 或 null, cost_s, human_dependency: 0-3, independence_group}`——这正是 562-A3 `verified_by_oracle` 字段的强度展开。

## A2 内核迁移盘点：抽走 g++ 后

### 当场还能跑（领域无关，只要求"存在可复现判官"）
| 机制 | 为什么领域无关 |
|---|---|
| claim 二分/三分类 observation/inference | 分的是"证据强度"，不是证据种类 |
| V-iso 阴阳同构思想 | 要求"可证伪条件存在且实测翻转"——任何能干预的判官（仿真/统计/第二人盲读）都可做阴面 |
| C-P/Wilson/rule-of-three（563 stat_bounds） | 纯数学 |
| 分权 model_family / 异族只读对抗 | 组织机制 |
| grounded 论证 + AGM 最小级联 | 图论，与领域无关 |
| 收敛三曲线、放权门 enter/exit | 元层计量 |
| task_queue/handoff/lease/touch | 纯工程 |
| golden 快照审计思想（四桶+--classify 强制） | 需要替换的只是"复算命令" |
| frontmatter 硬化/路径规范/毒样例 drill 框架 | 载荷随域换，框架不换 |
| Red Gate/出生证明义务（563 N7） | "先让它能失败"普适 |

### 立刻归零（编译器强耦合）及其弱 Oracle 域等价物
| 归零项 | 弱 Oracle 域的等价物 |
|---|---|
| P0-A 独立重编译 | "判官结果由第二个独立判官复算"——双来源/双分析者盲复算；没有第二判官时该命题不得升 verified |
| run_match 逐字比对 | 仿真：跨种子/跨求解器复算；规范域：条文版本+引文逐字定位；历史域：二手独立史料对读 |
| artifact_sha256 | 数据集快照哈希/标准文本版本号 DOI/标准条款编号 |
| compile_rc | 任何判官的结构化 verdict（统计检验的 p 阈值、仿真收敛判据） |
| matrix GCC×clang×MSVC | 多独立实验室/多数据集/多模型族交叉（相关性必须登记，见 A3） |
| asm 符号/区间断言 | 取决于新域有没有"可干预的中间产物"；纯文本历史域没有——只能降到引用闭包+人签 |
| poison 真编译载荷 | 针对新判官盲区的对抗样本（如统计域：伪造预注册、p-hack 样本；规范域：假引文） |

## A3 Oracle 发现 SOP（进入新领域的可复现步骤）

1. **列判官候选**：该域有没有"输入相同→输出可复现"的东西？（程序/数据集/标准文本/可重复实验/独立档案）按 A1 九类归类。
2. **强度试金石（三问，全可机判）**：
   a. 同一输入独立跑两次，输出一致吗？（reproducibility，n=2 起步）
   b. 能不能造出一个**明知错误**的输入，判官必须抓到？（阴面翻转，不翻转=没有判官，V-iso 直接适用）
   c. 判官的错误率能否随样本给 C-P 上界？不能则该域永远只能产出 witness/inference，不产 verified。
3. **相关性登记**：多判官/多来源必须填 independence_group——同源（同一数据集/同一标准译本/同一本教科书）的 k 个来源算 1 个独立佐证。563 的二项框架只对独立事件成立（563 §2 已警告）。
4. **冲突仲裁序**：可复现实验 > 形式证明（在其模型内）> 差分共识 > 规范文本 > 多来源交叉 > 人签；**强度按"错误率上界最小"排，不按声音大小排**；冲突不可判时命题留 UNDEC（grounded 不轻信，563-03）。
5. **弱 Oracle 叠加判定**：弱判官叠加只在独立性成立时变强（563：n 个独立零否决才缩上界）；相关性未知时禁止把"3 个来源都这么说"写成置信度提升。
6. **接入闸门**：新域首批命题必须 ≥10 条走完整阴面（先故意写错，判官翻转率 10/10 才允许该判官上岗）——样本量小所以这只是上岗烟测，长期错误率仍按 563 累积。
7. **无 Oracle 域的处理**：只组织可证伪性与证据链（trigger→refutation 指针→出处版本），**永不产 verified**；条目状态显式标 `witness`/`unverified`，禁止与 observation 混桶。是否接：只要该域命题能被写成"什么证据会使我错"，就接（当索引组织）；写不出证伪条件的不接（不可证伪命题不属本系统，562 Refutability Gap 同口径）。

## A4 诚实声明（本轮回答不了/不保证的）
- 跨域泛化**没有做过真实工程落地**：A3 是方法与可证伪假设，不是"保证能泛化"的结论；第一个试验场建议就是把现有 80 条 MIS 按 A3.7 重分级（零编译成本，可检验 SOP 本身是否可操作）。
- 多来源交叉在历史/规范域的"独立性"如何机械判定，本轮只有规则（同源登记）没有算法；疑似要靠人声明+抽查。