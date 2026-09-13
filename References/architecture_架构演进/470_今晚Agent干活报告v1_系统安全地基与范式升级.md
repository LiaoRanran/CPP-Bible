# 470 · 今晚 Agent 干活报告 v1（系统安全地基与范式升级）

> **投喂对象**：ds v4.1 flash CodeBuddy（强模型）。
> **本文性质**：这是今晚的完整工作指南，整合了 452 第四轮对抗结果、苦力 430 成果、三轮架构复盘。**以本文为准；469 v2.1 作为背景参考，冲突时信本文。**
> **前置阅读（按序）**：本文 → 468（架构总纲，理解系统定位）→ `_adv_v70/REPORT.md`（第四轮对抗完整报告）→ 苦力 430 成果（git log eab076d..c8e38d7）。

---

## 〇、战略定位：你在建什么

**CPP Bible 是测试场，「阙疑」系统才是产品。** C++ 原子卡是用来压测系统的真实场景，不是最终目的。系统的目标是：让任何大模型在它里面产出的知识都可靠、可复现、可积累，且系统自身能随模型升级而进化。

因此今晚的任务**不是修 C++ 原子卡**，而是**修系统的防御范式**——让烂原子（无论哪个模型写的、哪个知识域的）再也漏不过去。

**系统当前位置**：选择和遗传已机器化（gate/poison/pytest/replay 自动判决 + git 固化），但**变异（新规则/新防御的产生）还靠人**。今晚做的是把"被攻击后修复"这一环做到极致，为后续"自动攻击→自动修复"铺路。

---

## 一、开工第一步：建立你自己的实测基线

**铁律：不采信本文或任何文档的数字，全部实跑。** 开工前把输出贴进 `_worklog_470.md`：

```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
python tools/gate_engine.py --list | Measure-Object -Line    # 规则数（文档写 47，以实跑为准）
python tools/gate_engine.py --check 2>&1 | Select-Object -Last 1
python tools/poison_drill.py 2>&1 | Select-Object -Last 2
python tools/atom_evidence_replay.py --check 2>&1 | Select-Object -Last 3
python -m pytest tests/ -q 2>&1 | Select-Object -Last 3
git status --short
git log --oneline -20
```

同时 Read 以下工具源码（**禁止凭记忆写代码**）：
- `tools/gate_engine.py`（规则注册表、规则函数、denylist、relations 解析）
- `tools/atom_evidence_replay.py`（三分类、run_match、artifact_assert、编译执行）
- `tools/poison_drill.py`（毒样例执行、退出码、RULE-COVERAGE）
- `tools/writer_selfcheck.py`（苦力新建的 7 项自检）

**环境已就绪（不用再装）**：pytest 9.1.1、pyyaml 6.0.3、ruff、mypy、Windows ccache 4.14（`C:\tools\ccache`）、WSL ccache 4.9.1、MSYS2 clang++/clang-tidy 22.1.8（`C:\msys64\mingw64\bin`）。编译器：MinGW GCC 15.3（Qt）/13.1、WSL g++ 13.3/14.2、clang++ 22.1.8。

---

## 二、苦力 430 成果衔接（站在它肩膀上，不要重做）

苦力已完成 8 个独立 commit（eab076d..c8e38d7），门禁全绿。逐项评估你的动作：

| 苦力 commit | 内容 | 你的动作 |
|---|---|---|
| `e9094d7` F02 编译后覆写"时序约束（语义判据）" | gate 侧文本时序检查 | ⚠️ **升级**：文本检查拦不住无参 helper 脚本内部硬编码覆写（452 E01 实测）。补做 P0-A 的 replay 重编译不变量。苦力的 gate 检查保留为辅助层。 |
| `b9ded6a` F03 恒真符号"收窄为空/纯中文 block" | denylist 收窄 | ⚠️ **升级**：denylist 永远有第 22 个。补做 P0-C 的判别力证明（区间统计）。苦力的收窄保留为过渡。 |
| `b9ded6a` F04/F06/F09 解析器硬化（重复键/Unicode） | 自定义解析器补丁 | ⚠️ **评估**：读自定义 frontmatter 解析器代码，评估切 `yaml.safe_load`（P0-D）。切了之后苦力的补丁作废但毒样例可复用。先做存量兼容性测试。 |
| `eab076d` F01 cl 卡免检 EV-MSCV-NO-VERIFY | MSVC 走 infra_error | ✅ 已覆盖，不重做。 |
| `55b53ae`+`03dabec` writer_selfcheck 7 项 | L1 自检层 | ✅ 已完成。你只核对：测试覆盖是否完整、是否已登记 cppbible cmd_check、WC-02 的 EV-MEM-017 `_Znwm/_Znwy` 拼写缺陷是否已修。 |
| `18ac74d` cost_tracker + CPVA 基线 | 成本追踪 | ✅ 已完成。基线 5765 tok/颗（机器侧）。不重做。 |
| `0f9e1c2` flashcard_export 106 张 | 闪卡导出 | ⚠️ **核实**：是否过滤了 `status != verified`？452 E16 实测 draft 被导出。若未过滤，加过滤后重导出。 |
| `67d26d3` impact_analysis + `c8e38d7` A1-A10 | 架构增量 | ✅ 保留。 |

**苦力修的一笔真债**：`_atom_lock_cost.asm` 曾是异编译器遗留陈旧产物，已重生成核 sha。这正是 P0-A 要防的问题的一个人工修复实例。

---

## 三、今晚必做：P0 安全地基（按优先级）

**每条修复必须**：配毒样例（poison，续号，先 `poison_drill.py --list` 看最大编号）+ pytest 正反例（正例=攻击被拦，反例=合法卡放行）+ 存量零误伤（gate block=0 不新增）+ 独立 commit。

### P0-A【最高】replay 重编译不变量（452 E01 的根本修复）

**问题**：攻击者用 helper 脚本在编译后覆写工件，填正确 sha，replay confirm。文本检查（苦力的时序约束）拦不住脚本内部硬编码。

**根本修复**：replay 执行完 command 后，在**临时目录**用 command 中的编译命令（剥离后置非编译段）重新编译一次，计算新工件 sha256，与卡内 `artifact_sha256` 比对。不一致 → `refute:artifact_tampered`。

**关键实现要点（三轮复盘发现的坑，必须处理）**：
1. **编译确定性**：GCC 产物可能含时间戳/路径，相同源码两次编译 sha 可能不同。重编译时加 `-frandom-seed=<确定性值，如夹具名>` 和 `-ffile-prefix-map=<构建目录>=.` 消除非确定性。**先做实验验证**：对 3 个现有夹具连续编译两次，确认加 flag 后 sha 稳定；若仍不稳定，改用"结构化比对"（提取关键符号/指令序列比对）而非全文件 sha。
2. **临时目录隔离**：重编译输出到 `tempfile.mkdtemp()`，不覆盖原工件（同时解决 452 E09 并发问题，见 P0-G）。
3. **三分类**：重编译本身失败（编译器缺失/超时）→ `infra_error`，不判内容 refute。
4. **多 TU 夹具**（如 INLINE-001 有 3 个 .asm）：逐产物比对，或比对卡内锚定的那个主产物。
5. **跨编译器路径**：Windows 走 sha 强校验、Linux 走 artifact_assert。重编译不变量应在**两条路径都生效**——Windows 侧 sha 比对是重灾区（断言从未被评估），重编译能顺带激活 Windows 侧的断言检查。

**验收**：
- 构造 E01 探针（helper 脚本编译后覆写）→ replay 重编译 sha 不一致 → refute:artifact_tampered
- 现有 56 卡重编译 sha 一致（或差异可解释：确定性 flag 问题）→ confirm 不退化
- 并发跑 6 轮 replay 无假失败（临时目录隔离）
- poison + pytest 绿

### P0-B【高】cat 式证据检测（452 E05）

**问题**：夹具 open 随库数据文件原样打印，输出逐字相等但零计算，run_match confirm。

**修复**：新增 gate 规则 `EV-FIXTURE-NO-ECHO-DATA`（先 warn 观察，不直接 block）：扫描夹具源码，若存在"打开仓库内数据文件（ifstream/fopen/open with r）且读入值未经运算直接流向 stdout 的 run 标签"→ warn。

**边界**：合法夹具也可能读文件（演示文件格式）。判据聚焦"读入值是否经过计算"——静态分析数据流（读入变量 → 是否参与算术/函数调用 → 再输出）。静态分析做不到完美时，退化为"读文件+直接 cout 同一变量"模式匹配，warn 即可。

**验收**：E05 探针 warn；存量 56 卡若有同类，列出来交人裁决。

### P0-C【高】判别力证明（452 E03 的根本修复）

**问题**：contains_in/absent_in 的 text 若在每个函数符号区间都出现（如 `.cfi_startproc`/`mov`/`ret`），对"该函数有没有某行为"零判别力。苦力的 denylist 收窄是打地鼠。

**根本修复**：评估 contains_in/absent_in 断言时，统计 text 在工件**各函数符号区间**的出现分布：
- 复用 replay 已有的符号区间切分逻辑（contains_in/absent_in 已支持区间语义）。
- **阈值不要拍脑袋**（复盘教训）：设 text 出现的函数区间数为 `k`，工件总函数区间数为 `N`。
  - `k/N ≥ 0.8` 且 `N ≥ 3` → block（新卡）/ warn（存量）："断言符号在 80%+ 函数区间出现，无判别力"。
  - `N < 3`（工件太小）→ 不判 block，降 advice（小工件统计无意义）。
  - 通用符号（main/call/ret 等，见苦力的 denylist）维持苦力的处理。
- **同时保留苦力的 denylist 收窄**作为快速路径（空/纯中文直接 block），判别力统计作为深度路径。

**验收**：
- E03 探针（contains `.cfi_startproc`，在所有函数区间出现）→ block
- 真实机制符号（lock xchg 只在特定函数、fence 只在 writer 函数）→ 放行
- 存量 56 卡全量跑，列出所有被判别力统计命中的断言，逐条确认是真恒真还是误伤
- poison + pytest

### P0-D【高】YAML 解析切标准库（452 E07/H8/H18 的根本修复）

**问题**：自定义 frontmatter 解析器有 7 种同构变换攻击（缩进走私 E07、flow-map 重复键 H8、锚点 merge H18、同义词丢弃 H14…）。每修一种就有下一种。

**根本修复**：把证据卡/原子卡的 frontmatter 解析切换到 `yaml.safe_load`（pyyaml 已装）。

**实施步骤（谨慎，兼容性优先）**：
1. 先写一个**兼容性测试脚本**（不改动现有解析器）：用 safe_load 解析全量 evidence/（56 张）+ atoms/（28 颗），把结果与现有自定义解析器的结果逐字段 diff。
2. 分类差异：①完全一致 → 安全切换；②safe_load 报错（依赖自定义解析宽容行为，如未加引号中文冒号）→ 列出具体卡，批量修正卡格式；③语义差异（重复键 after-wins 行为不同）→ 加重复键检测。
3. **重复键检测**：safe_load 默认 after-wins 不报错。用 `yaml.add_constructor` 或自定义 loader 检测同一映射内重复键（含 flow-map），发现即报错（E07/H8 根本消除）。
4. 切换后，苦力的 F04/F06/F09 自定义解析补丁若被 safe_load 覆盖，保留毒样例、删除冗余补丁代码。
5. H14 冲突同义词：在解析后的规范化阶段（`_relations_norm`），把 `contradiction/conflicts/cancels/opposes/conflicts_with` 归一到 CONFLICT_REL；未知关系键 warn。

**风险控制**：如果存量卡兼容性差异 >10 张且修正成本高，**不要硬切**——保留自定义解析器但在其外层包一层 safe_load 校验（safe_load 能解析就用 safe_load，不能就 warn 并回退），把结果写进 worklog 交人裁决。

**验收**：E07 缩进走私探针 → 重复键报错或 verdict 正确解析为 refute；存量卡解析结果不退化；poison + pytest。

### P0-E【中高】环境量进 run_match_keys 立规则（452 E07/H7）

**问题**：d8ff94d 修了存量卡但没立规则，nproc/hardware_concurrency/时间戳/PID 进 keys 会本机绿 CI 红。

**修复**：gate 规则 `EV-OUT-NO-ENV-KEY`（block 新卡，存量 warn）：run_match_keys / actual run 标签值若来自 `hardware_concurrency`、`file_size`（非确定文件）、`__DATE__/__TIME__/__FILE__`、`getenv`、PID、`chrono now/clock`、`nproc`、`uname` → block。

**注意**：`hardware_concurrency` 走 sysconf 不受 taskset 影响（已实证），不能用"CI 钉核数"绕过。CONC-002 的 nproc 兜底（insufficient_cores）是**合法范式**（打印核数用于守卫，不作为逐字 key），用它做反例毒样例。

**验收**：E07 探针 block；CONC-002 合法兜底放行。

### P0-F【中】零诊断判据字段面 + pragma 消音（452 E10/H16）

**修复**：①"零诊断/无警告/zero warning"声明扫描面从 falsification 扩到 expected/hypothesis/actual 全文；②检测夹具用 `#pragma GCC diagnostic ignored` / `-w` / `-isystem` 压制本应作为证据的警告；③零诊断证据必须配套 `-Werror` 可复现编译命令，否则降 warn。

**验收**：H16/H16B 探针 block/warn；真用 -Werror 的 INLINE-001 不误伤。

### P0-G【中】签收 git author 绑定（452 E12）+ 并发隔离（E09）

**G1 签收绑定（轻量，不用 GPG）**：gate 校验 `human:` 签收时，读该卡文件 `git log --format='%an' -1 -- <file>`，author 不含签收人 → warn"签收人与 git 提交者不一致"。单人项目 author=liaoranran 通过；Agent commit 的 author 不是 liaoranran 会被标记。

**G2 并发隔离**：replay 编译输出从固定 `Examples/atoms/` 改为每进程 `tempfile.mkdtemp()`，编译后原子写入（先 .tmp 再 rename）。若 P0-A 已用临时目录重编译，此处只需确保**主编译路径**也隔离。

**验收**：G1 探针（human:liaoranran 但 author=agent）warn；G2 并发 6 轮 replay 无假失败。

### P0-H【中】对抗探针沉淀为毒样例（防退化）

**问题**：452 的 15 个探针在 `_adv_v70/` 不入库，修完 E01/E03/E07 后没有回归保护，可能退化。

**修复**：把以下阻断级探针转化为正式 poison 毒样例（放 `tests/poison/` 或 poison_drill 的探针目录，遵循现有格式）：
- E01（helper 脚本编译后覆写）→ 验证 P0-A 拦住
- E03（恒真符号 .cfi_startproc）→ 验证 P0-C 拦住
- E05（cat 式证据）→ 验证 P0-B 拦住
- E07（缩进走私 verdict）→ 验证 P0-D 拦住
- E10（零诊断字段位移/pragma）→ 验证 P0-F 拦住
- E12（签收自证）→ 验证 P0-G1 拦住

**注意**：探针转化时去掉 `_adv_v70/` 的临时路径，用 poison 标准格式；每个毒样例必须验证"修复前能逃逸、修复后被拦"。

---

## 四、今晚可选（P1/P2，P0 完成后量力，可跨窗口）

- **P1-1 writer_selfcheck 收尾**：核对苦力的 7 项 WC 测试覆盖、cppbible 登记、quality 门禁接入；核实 EV-MEM-017 `_Znwm/_Znwy` 是否已修，修了则评估 WC-02 升 fail。
- **P1-2 闪卡 verified 过滤**：flashcard_export 加 `status == verified` 过滤（E16），重导出确认 draft 不再出现。
- **P2-1 ccache 接入 replay**：环境已就绪（Win `C:\tools\ccache\ccache.exe`、WSL `/usr/bin/ccache`）。给 replay 的 WSL 编译调用前缀 ccache，构建目录固定 /tmp，实测二次 replay 耗时（预期 2min→~10s），记录数字。Windows 侧同理。**注意 ccache 与 P0-A 重编译的交互**：重编译也要走 ccache 否则两次编译都 miss。
- **P2-2 规则渐进发布**：gate 规则加 `status: experimental|stable|deprecated`，新规则默认 experimental=warn。
- **P2-3 成本 trace 补全**：cost_tracker 目前只采机器侧（5765 tok/颗）。补一个手填字段模板：红队轮次、红队工具调用数、窗口数，让单颗真实成本（估算 ~2 万 tok）可追踪。

---

## 五、架构方向（**今晚不做**，但你要知道系统往哪走）

三轮复盘确认系统从"脚本集合"进化到"产品"还缺四块拼图。**不要在今晚实现它们**，但如果 P0 做完有余力，可以写设计笔记到 `_worklog_470.md`：

1. **变异自动化（最高架构优先级）**：当前"对抗→修复→新规则"全靠人投喂提示词。方向：把 452 成熟的对抗模式（两阶段盲读、沙箱 monkeypatch、可复现探针）固化为 `tools/auto_redteam.py`，新规则上线后自动跑一轮攻击，发现逃逸自动生成规则候选，人只审批。这定义了"可进化"。
2. **验证器可插拔**：`atom_evidence_replay.py` 硬编码 C++ 编译。方向：抽象为"证据验证引擎"，C++ 编译复现是第一个验证器插件，未来 Python/数学/历史域换插件不换骨架。这定义了"领域无关"。
3. **文档生效状态**：References 下约 170 份架构文档无 active/deprecated/historical 区分。方向：`docs/status.json` 标注每份文档状态，新模型开工只读 active。
4. **系统自监控**：五种系统失败模式（规则冲突、工具退化、基线漂移、性能退化、warn 信任退化）目前零监控。方向：规则一致性检查、基线自动校验、gate 性能基线、warn 信噪比追踪。

---

## 六、统一工程铁律（每个 commit 遵守）

1. **重读磁盘**：改任何工具前先 Read 当前源码，规则注册表/关系归一/三分类/豁免文件以代码为准。
2. **一条修复一个 commit**，message：`fix(gate): P0-x <漏洞> 闭合（452 En）` / `feat(...)`。
3. **每条新规则配毒样例 + pytest 正反例**（正例=攻击被拦，反例=合法卡放行）。
4. **存量零误伤**：每改一条规则，`gate --check` block 必须仍为 0（新增 warn 列出具体卡和理由）；replay confirm 数不下降、无新增 refute。
5. **门禁全绿才提交**：gate block=0、poison 全拦截+阴性放行、pytest 全过、replay 不退化。**Windows replay 与 WSL 预检严禁并行**（同写 .asm 出假红）。
6. **不 push、不 golden sync/accept、不删毒样例、不 renormalize Examples/**（push 权在用户；golden 认可权唯人）。
7. **数字以实跑为准**，文档（含本文）与代码冲突时信代码，在 worklog 记录文档错误。
8. **插入大段代码后立即 `gate_engine.py --check`** 验证文件可加载（历史教训：replace 破坏过缩进/循环）。
9. **安全停止**：任何 P0 任务若发现"修复会破坏 >5 张存量卡且无法快速修正"，**停止该任务**，把现象、受影响卡、可选方案写进 worklog，继续下一个任务，不要硬改。
10. **同仓并行**：可能有其他会话在入库。提交前 `git diff --cached --stat` 复核，避免把并行会话的改动误带入你的 commit（苦力遇到过 55b53ae 误删事件）。

---

## 七、收工交付（无论做到哪）

写 `_worklog_470.md`，包含：
1. 每个 P0/P1/P2 项的状态（完成/部分/未做）、commit hash、实测门禁数字。
2. 新增规则名与毒样例编号、pytest 新增用例数。
3. **P0-A 编译确定性实验结果**（加 flag 前后两次编译 sha 是否稳定）——这是后续 replay 不变量的基础，必须有结论。
4. **P0-D 存量兼容性测试结果**（safe_load vs 自定义解析器的 diff 分类统计）。
5. 所有"与文档不符"的发现（苦力报告说 430/414/424 的基线数字系统性失真，以你实测为准）。
6. 未完成项的下一步精确命令。
7. 最终再跑一遍第一节全套门禁，贴最终基线。
8. 列所有本地 commit（`git log --oneline` 从开工点到收工），注明**未 push**、ahead 数交用户。
9. 若 P0 有未闭合项，明确写"当前系统仍存在哪些可复现逃逸"，**不得用"基本完成"掩盖**。

**优先级纪律**：P0-A（重编译不变量）和 P0-D（切 safe_load）是本晚最高价值——前者是运行时防御范式，后者一次性消除整个解析器攻击面。P0-C（判别力）次之。P0-B/E/F/G/H 是规则级，相对独立。安全地基闭合前不要转去做 ccache/闪卡等增量功能。
