# 470 · 今晚 Agent 干活报告 v1.4（系统安全地基与范式升级）

> **投喂对象**：ds v4.1 flash CodeBuddy（强模型）。
> **本文性质**：这是今晚的完整工作指南，整合了 452 第四轮对抗结果、苦力 430 成果、四轮架构复盘。**以本文为准；469 v2.1 作为背景参考，冲突时信本文。**
> **前置阅读（按序）**：本文 → 468（架构总纲，理解系统定位）→ `_adv_v70/REPORT.md`（第四轮对抗完整报告）→ 苦力 430 成果（git log eab076d..c8e38d7）。
> **版本**：v1.4（四轮打磨：v1 初始 → v1.1 系统全貌 → v1.2 五维模型 → v1.3 九处可执行性漏洞 → v1.4 执行协议+时间预算+探针验证+签收修正）。执行中若本文被外部修改，以你开工时 Read 的版本为准，不要中途换版本。

---

## 〇、战略定位：你在建什么

**CPP Bible 是测试场，「阙疑」系统才是产品。** C++ 原子卡是用来压测系统的真实场景，不是最终目的。系统的目标是：让任何大模型在它里面产出的知识都可靠、可复现、可积累，且系统自身能随模型升级而进化。

因此今晚的任务**不是修 C++ 原子卡**，而是**修系统的防御范式**——让烂原子（无论哪个模型写的、哪个知识域的）再也漏不过去。

**系统当前位置**：选择和遗传已机器化（gate/poison/pytest/replay 自动判决 + git 固化），但**变异（新规则/新防御的产生）还靠人**。今晚做的是把"被攻击后修复"这一环做到极致，为后续"自动攻击→自动修复"铺路。

---

## 〇·五、系统全貌（首次接手的模型必读，建立心智模型）

### 1. 一句话理解「阙疑」

阙疑是一套**机器可核验的知识生产/验证系统**：模型生产"原子知识卡"，每张卡的结论必须由**可复现的实验工件**（编译产物、运行输出、反汇编）支撑，经过多层机器门禁 + 独立红队对抗 + 人审签署，才能成为 verified 知识。核心信念是"多闻阙疑"——**主动暴露不确定性，宁可判 refute/infra_error 也不放过无证据的断言**。C++ 库（CPP Bible）是第一个压力测试域，系统本身追求领域无关。

### 2. 知识资产四层（当前实测数量）

| 资产 | 目录 | 数量 | 含义 |
|---|---|---|---|
| 原子 atom | `atoms/{domain}/` | 27 颗（mem 21 / conc 3 / lang 1 / ub 1 / hist 1） | 最小可验证知识点，frontmatter 含 claim/DAL/status/relations/serves/pedagogy |
| 证据卡 evidence | `evidence/{domain}/` | 56 张（mem 45 / conc 6 / lang 2 / ub 2 / hist 1） | 一张原子由多张证据卡支撑，含 fixture/command/artifact_sha256/actual/expected/falsification/matrix |
| 误解 misconception | `misconceptions/` | 80 条（扁平 `MIS-{DOMAIN}-NNN.md`） | 常见错误认知，含 ≥3 反例，原子通过 pedagogy.misconception 引用 |
| 夹具 fixture | `Examples/atoms/_atom_*.cpp` | 56 个 | 可编译运行的最小实验程序，产出 .asm（反汇编）/.out（运行输出）作为工件 |

ID 格式：原子 `ATOM-{DOMAIN}-{TOPIC}-{NNN}`（如 ATOM-CONC-FENCE-001），证据 `EV-{DOMAIN}-NNN`，误解 `MIS-{DOMAIN}-NNN`。原子状态四级（G6）：`draft → rule（机器验证）→ verified（人签）→ archived`；DAL A-E 是**失效后果严重度**（不是证据强度），A/B 强制人审。

### 3. 目录结构（只列关键）

```
CPP-Bible/
├── atoms/ evidence/ misconceptions/ goldens/   # 知识资产（goldens 放待原子化草稿）
├── Examples/atoms/                              # 夹具 .cpp + 工件 .asm/.out
├── tools/                                       # 全部机器门禁与工具（91 个 .py，核心见下）
├── tests/                                       # pytest（15 个 test_*.py）
├── tests/poison/                                # 毒样例（攻击夹具，应被 gate 拦截）
├── Scripts/                                     # 一键脚本（door_check/repo_status/push_attempt）
├── docs/kernel/                                 # 生效规范（G1/G6/M1-M5/S1-S6/tool_assumptions）
├── References/architecture_架构演进/            # 架构演进文档 300-470（多数是调研档，生效规范少）
├── toolchain.toml                               # 编译器/工具链路径（g++/clang/ccache）
├── Book/                                        # C++ 教程正文（测试场的传统内容，437 个示例有行尾漂移，勿 renormalize）
└── _adv_v70/ _adv_v61/ _bypass_test/            # 对抗/绕过测试产物（不入库，.gitignore）
```

### 4. 核心工具与职责分层

| 层 | 工具 | 职责 |
|---|---|---|
| **统一入口** | `cppbible.py` | CLI 总入口：`check --stage fast/quality/compile`、`impact`、`cost`、`flashcards`、`env`、`preflight` |
| **L4 结构门禁** | `gate_engine.py` | 47 条规则，解析原子/证据卡 frontmatter，block/warn/advice 三级；含 DAG、冲突关系、签收校验、MSVC 免检 |
| **L3 运行时验证** | `atom_evidence_replay.py` | 执行 command 编译运行夹具，比对 .out 逐字/键、校验 artifact_sha256、artifact_assert 符号区间断言、sanitizer；三分类 confirm/refute/infra_error |
| **对抗演练** | `poison_drill.py` | 50 个毒样例（已知攻击）应被拦 + 阴性样例应放行；RULE-COVERAGE 统计规则覆盖率 + 豁免台账 |
| **基线锁** | `golden_lock.py` | 锁定 atoms/evidence/replay_confirm/replay_infra_error 等计数，恶化即红；`sync/check/show`，**认可权唯人** |
| **L1 自检** | `writer_selfcheck.py` | Writer 产出后零 token 自检 7 项（WC-01..07），接入 quality 门禁 |
| **效率/转化** | `cost_tracker.py` `flashcard_export.py` `impact_analysis.py` | CPVA 成本基线（5765 tok/颗机器侧）、Anki 闪卡导出、上下游依赖遍历 |
| **其他** | `consistency_check.py` `gen_metrics.py` `gray_zone_scan.py` `debt_ledger.py` `toolchain.py` | 一致性评分、指标生成、灰色地带（unspecified vs UB）扫描、技术债台账、工具链解析 |

一键脚本：`python Scripts/repo_status.py`（开工快照）、`python Scripts/door_check.py [--fast]`（收工门禁汇总）、`python Scripts/push_attempt.py [--push]`（推送诊断，默认 dry-run）。WSL 全量预检：`ci_local_precheck.py`（31-32 步，含 TSan 需 `setarch -R`）。

### 5. 验证金字塔（门禁分层，从下到上）

```
L6 长期回归   毒样例防退化 + 对抗探针沉淀（P0-H 要补）+ CI 双编译器矩阵
L5 人审       human: 签收（DAL A/B 强制；当前是字符串，P0-G 要绑 git author）
L4 结构门禁   gate_engine 47 条规则（frontmatter/关系/DAL/状态/签收格式）
L3 运行时     replay 编译运行 + sha 校验 + 符号断言 + sanitizer（P0-A 要加重编译不变量）
L2 红队       独立子 agent 两段式盲读（先只读夹具+工件不读卡，再对照卡）
L1 自检       writer_selfcheck 7 项（零 token，错误左移）
```

> 验证金字塔只是系统**五维成熟度**中的"验证"一维。完整框架见第五节：验证（较强）、信任（弱）、度量（弱）、消费（弱）、进化（最弱）。今晚 P0 只加固验证维，其余四维是后续架构批次。

### 6. 一颗原子的完整生命周期（MCC 六步 + 三权分立）

```
选题(知识图谱空白) → 预言冻结(实验前 commit 预言矩阵，git 时间戳为证)
  → Writer 生产夹具+工件+证据卡+误解+草稿（L1 自检）
  → 独立红队两段式盲读（Writer 与红队必须是不同 agent 实例，不给草稿全文）
  → Gatekeeper 跑 L3/L4 门禁（replay/gate/poison/pytest/golden）
  → 原子化入 atoms/（人签 verified）→ golden_lock sync 基线 → 教学转化(闪卡/Book)
```
三权分立：**Writer 写卡 / 红队攻卡 / Gatekeeper 判卡**，三者不可是同一实例。每个环节的产物切分写死，禁止既当运动员又当裁判。

### 7. 角色分工（多模型协作）

| 角色 | 模型 | 职责 | 权限 |
|---|---|---|---|
| 人（监工/目标设定者） | 用户 | 定方向、做不可逆决策、push、golden 认可、人审签署 | 唯一 push/golden sync 权 |
| 架构师 | 本助手（豆包） | 调研、消化、架构规划、写投喂提示词、复盘 | 只写文档，不改系统代码 |
| 苦力 | 便宜/白嫖模型（如 Qwen flash） | 按提示词干机械杂活、跑门禁、写工具 | 不 push、不 golden、独立 commit |
| 好模型 | ds v4.1 flash CodeBuddy（**今晚的你**） | 范式级修复、系统落地、复杂调试 | 不 push、不 golden、独立 commit |
| 对抗模型 | Seed-Evolving / Trae（异模型族最佳） | 独立红队/渗透，产出可复现探针 | 只在 _adv_*/ 沙箱，零污染正式目录 |

### 8. 当前基线（2026-09-13，以你实跑为准）

gate 47 规则（block=0 / warn≈32，warn 多为新规则暴露的存量真债）· poison 50/50 · replay confirm=56（双平台）· pytest 121+ · atoms 27 / evidence 56 / misconceptions 80 / 夹具 56。本地大量 commit ahead origin 未 push（SSH 数据通道在本机被墙 exit 141，push 由用户换网络执行）。

### 9. 环境与编译器矩阵

- Windows：MinGW GCC 15.3（Qt，toolchain prefer）/ 13.1、clang++ 22.1.8（MSYS2，`C:\msys64\mingw64\bin`）、ccache 4.14（`C:\tools\ccache`）。MinGW **无 TSan/LSan 完整支持**。
- WSL：g++ 13.3/14.2、ccache 4.9.1、riscv64-unknown-elf-g++ 13.2（bare-metal，用 `__atomic_*` 无 `<atomic>` 头）。TSan 须 `setarch -R <cmd>` 前缀，否则 FATAL memory mapping。
- MSVC `cl.exe`：**永久边界**，replay 遇 cl 走 `infra_error:msvc_unavailable`，不尝试编译。
- 跨平台关键事实：`hardware_concurrency()` 走 sysconf 不受 taskset 影响；Windows 走 sha 强校验会跳过 artifact_assert（断言必须在 Linux 工件实测）；sanitizer 类型归并（[thread]/[address]/[leak]）不按子串匹配。

### 10. 关键规范文档地图

- **生效规范**（违反会 block）：`docs/kernel/G1_layout.md`+`G1_knowledge_map.md`（布局/知识图谱）、`G6_status_levels.md`（四级状态+DAL+签收 principal）、`M1_ontology.md`/`M2_empirical.md`（本体论/实证规范）、`S1_S6_controls.md`（管控）、`tool_assumptions.md`（15 条工具假设）、`non_compressible_facts.md`（不可压缩事实）。
- **架构总纲**：`References/.../468_*.md`（知识生命周期×验证金字塔×能力梯度三维模型）。
- **今晚任务书**：本文 470；469 v2.1 是其前身（含 P0 修复细节，可交叉参考）。
- **对抗报告**：`_adv_v70/REPORT.md`（第四轮，15 探针 14 绕过）；历史收编记录在 `docs/kernel/373_*.md`。
- **注意**：References 下约 170 份文档绝大多数是调研历史档，**不具约束力**；数字可能过时，一切以实跑和 `docs/kernel/` 生效规范为准。

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

**代码导航指引（用 Grep 快速定位，不要盲目 Read 全文件）**：
- `gate_engine.py`：搜 `RULES` 或 `register` 找规则注册表；搜 `def check_` 看规则函数签名（统一返回 `(block, warn, advice)` 三元组）；搜 `denylist` 或 `GENERIC_SYMBOLS` 找恒真符号表；搜 `_relations_norm` 找关系归一化；搜 `CONFLICT_REL` 找冲突关系定义；搜 `principal_ok` 找签收校验。
- `atom_evidence_replay.py`：搜 `def run_commands` 或 `def _run` 找编译执行入口；搜 `def _classify` 或 `infra_error` 找三分类判决；搜 `contains_in` 或 `absent_in` 找符号区间断言（含区间切分函数）；搜 `run_match` 找逐字/键比对；搜 `_command_uses_msvc` 找 MSVC 分流。
- `poison_drill.py`：搜 `gate_exit_code` 找退出码逻辑（苦力已修 F08）；搜 `RULE_COVERAGE` 或 `uncovered` 找覆盖率统计；毒样例格式看 `tests/poison/` 下现有 YAML。
- 新增规则后必须在 `tools/cppbible.py` 的 `cmd_check` 元组中登记（META-MANIFEST 双清单一致），否则会 warn。

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

**⚠️ 升级前必须先验证（不要凭本文判断直接重做）**：
本文说"苦力的 F02 拦不住 E01""苦力的 F03 拦不住 E03"——这些是基于 452 对抗报告的推断。**你开工后第一件事是用 `_adv_v70/probes/` 里的真实探针，分别 against 苦力的 F02/F03 实现实跑一次**，确认：
- E01 探针在苦力的 F02 规则下是否真的 gate block=0 + replay confirm？如果苦力的时序检查其实拦住了，P0-A 的优先级可降。
- E03 探针（`.cfi_startproc`）在苦力的 F03 收窄后是否真的放行？`.cfi_startproc` 不在苦力的 denylist（只拦空/纯中文），所以应该放行——确认这一点后再做 P0-C。
验证结果写进 worklog。**不要因为本文说"要升级"就跳过验证直接重做——如果苦力的方案意外有效，重做就是浪费。**

---

## 二·五、执行协议（怎么推进，而不只是做什么）

> 这一节是 v1.4 新增的核心。之前的版本只告诉你"做什么"，这一节告诉你"怎么推进才不会在一个任务上卡死、不会最后才发现全错、不会跳过难做的部分"。

### 1. 时间预算与降级规则（防止单任务卡死）

每个 P0 任务有**软时间预算**（以你的实际推进速度为准，不是墙钟时间）：

| 任务 | 软预算 | 超时处置 |
|---|---|---|
| P0-A 重编译不变量 | 最高，但**编译确定性实验超过 3 次尝试仍不稳定** → 触发回滚条件（降级为 warn），不要继续死磕 flag 组合 | 按 P0-A 第 7 条回滚 |
| P0-D 切 safe_load | 兼容性测试做完后，若差异 >10 张 → 不硬切，走外层包 safe_load 校验方案 | 按 P0-D 风险控制 |
| P0-B/C/E/F/G | 每个不超过"写规则+毒样例+pytest+存量验证"的正常一轮 | 若规则实现复杂到需要改 replay 核心逻辑，降级为 P1 并记录 |
| P0-H 探针沉淀 | 依赖前面修复，最后做 | 若某个探针因前面修复方式变化而无法复现，标注"探针已过时"跳过，不要硬造毒样例 |

**原则**：宁可 5 个 P0 各做到 80% 并诚实记录缺口，也不要 1 个 P0 做到 100% 其余 7 个没动。P0-A 和 P0-D 是范式级，值得多花时间；其余是规则级，快做快过。

### 2. 每任务检查点（做完一个 P0 必须过的门）

每做完一个 P0（commit 之后），**立即**跑以下增量检查，不要攒到最后：

```
# 增量门禁（不跑全量 replay，省时间）
python tools/gate_engine.py --check          # block 必须仍为 0
python tools/poison_drill.py 2>&1 | Select-Object -Last 3   # 新毒样例必须被拦
python -m pytest tests/ -q -k "<新规则关键词>"   # 只跑相关测试
git diff HEAD~1 --stat                       # 确认只改了该任务该改的文件
```

**检查点不通过就不要进入下一个 P0**——修到通过为止，或触发回滚条件降级。这比"全部做完再跑全量门禁发现第一个就错了"高效得多。

### 3. 探针可用性前置验证（开工第 0 步，在 P0 之前）

`_adv_v70/probes/` 里的探针是 452 对抗时（基线 9f9652c）构造的，之后苦力改了 F01/F02/F03 等工具，**探针可能已经不能复现了**。开工后、做任何 P0 之前：

1. 选 E01/E03/E07 三个阻断级探针，分别在当前代码上实跑一次（gate + replay）。
2. 记录每个探针的当前状态：仍能逃逸 / 已被苦力修复 / 无法复现（环境变化）。
3. **已被苦力修复的探针**：对应的 P0 任务优先级降低，只需确认苦力的修复覆盖了该攻击面，然后把探针转化为毒样例（P0-H）即可，不需要重做根本修复。
4. **无法复现的探针**：标注原因（如探针依赖的夹具路径已变），在 P0-H 中跳过，不要花时间修探针。

这个验证预计 15 分钟，但能避免"按本文判断重做了一个其实已经被苦力修好的问题"。

### 4. 好模型常见失败模式预警（基于苦力和前序 Agent 的真实踩坑）

以下是本项目中 Agent 反复犯的错，**你要主动避免**：

1. **凭文档记忆写代码，不 Read 磁盘源码**——文档数字系统性失真（430/414/424 的基线数字全错），规则数、毒样例数、卡数以实跑为准。改工具前必须 Grep 定位真实函数。
2. **为了门禁绿而弱化毒样例**——铁律禁止。毒样例必须真的能触发规则，不能写一个"肯定被拦"的 trivial 样例凑数。
3. **插入大段代码后不验证可加载**——苦力遇到过 replace 破坏缩进/循环导致 gate 加载报错。每次改完 `gate_engine.py` 立即 `--check`。
4. **把 warn 当成功**——新增 warn 必须列出具体卡和理由，不能"block=0 就完事"。warn 信噪比是系统健康指标。
5. **并行会话误带入**——提交前 `git diff --cached --stat` 复核，不要把其他会话的改动混进你的 commit。
6. **"基本完成"掩盖缺口**——收工时必须明确写哪些 P0 未闭合、当前还有哪些可复现逃逸。
7. **加规则时不看分布（466 矛盾 2 数据）**：当前 gate 规则中 60% 是机械规则（字段存在/格式/ID），24% 语义，仅 16% 内容规则；但 402 对抗的 13 个逃逸中 11 个落在内容规则覆盖不到的区域。**你今晚加的 P0-B/C/E/F 都是内容/时序规则，这是对的方向**——不要顺手再加机械规则（如"字段必须非空"的变种），那是在已经过剩的区域浪费精力。加规则前先想：这条规则拦的是"直白违规"还是"组合/时序/数据流攻击"？后者才是攻击面集中区。

### 5. 工件安全（所有实验不碰正式工件）

- P0-A 的重编译实验**必须**在 `tempfile.mkdtemp()` 中做，**绝对不要**覆盖 `Examples/atoms/` 下的正式 .asm/.out。
- 如果实验需要修改夹具来测试，先 `cp` 到临时目录再改，不要在原夹具上实验。
- 正式工件的 sha 是 replay 的基线，意外修改会导致全量 replay 飘红。

---

## 三、今晚必做：P0 安全地基（按优先级）

**每条修复必须**：配毒样例（poison，续号，先 `poison_drill.py --list` 看最大编号）+ pytest 正反例（正例=攻击被拦，反例=合法卡放行）+ 存量零误伤（gate block=0 不新增）+ 独立 commit。

**P0 任务间依赖关系（按此顺序执行，避免返工）**：
```
P0-A（重编译不变量）───┐
P0-D（切 safe_load）───┼──→ P0-H（探针沉淀，依赖前面都修完才能验证"修复后被拦"）
P0-B/E/F/G（规则级）───┘
P0-C（判别力）独立，可与 A/D 并行
P0-G2（并发隔离）与 P0-A 的临时目录有重叠，A 做完后 G2 只需补主编译路径
```
- **先做 P0-A 和 P0-D**（两个范式级，风险最高、最可能需要回滚），再做规则级 B/E/F/G。
- **P0-H 最后做**：毒样例要验证"修复后被拦"，必须等对应修复落地。
- **P0-D 若决定不硬切**（兼容性差异太大），则 P0-B/E/F 的规则实现仍用自定义解析器，不需要等 D。
- **P0-C 完全独立**，可随时插入。

### P0-A【最高】replay 重编译不变量（452 E01 的根本修复）

**问题**：攻击者用 helper 脚本在编译后覆写工件，填正确 sha，replay confirm。文本检查（苦力的时序约束）拦不住脚本内部硬编码。

**根本修复**：replay 执行完 command 后，在**临时目录**用 command 中的编译命令（剥离后置非编译段）重新编译一次，计算新工件 sha256，与卡内 `artifact_sha256` 比对。不一致 → `refute:artifact_tampered`。

**关键实现要点（四轮复盘发现的坑，必须处理）**：
1. **编译确定性**：GCC 产物可能含时间戳/路径，相同源码两次编译 sha 可能不同。重编译时在原编译命令基础上**追加** `-frandom-seed=<确定性值，如夹具 basename>` 和 `-ffile-prefix-map=<构建目录>=.`（**不修改卡内 command**，只在 replay 重编译时注入）。clang 同样支持这两个 flag。**先做实验验证**：对 3 个现有夹具连续编译两次，确认加 flag 后 sha 稳定；若仍不稳定，改用"结构化比对"（提取关键符号/指令序列比对）而非全文件 sha，并在 worklog 记录哪些夹具不稳定。
2. **⚠️ ccache 陷阱（最易踩）**：环境已装 ccache（Win `C:\tools\ccache`、WSL `/usr/bin/ccache`），重编译时若 ccache 命中缓存，"重编译"直接返回缓存工件，**sha 对比退化为"缓存 vs 缓存"恒真，完全失去检测意义**。重编译必须设 `CCACHE_DISABLE=1`（或 `CCACHE_RECACHE=1` + `CCACHE_DIR` 指向临时空目录）。WSL 侧通过环境变量传入，Windows 侧同理。**这一条是 P0-A 能否生效的前提。**
3. **临时目录隔离**：重编译输出到 `tempfile.mkdtemp()`，不覆盖原工件（同时解决 452 E09 并发问题，见 P0-G2）。
4. **三分类**：重编译本身失败（编译器缺失/超时/链接错）→ `infra_error`，不判内容 refute。
5. **多 TU 夹具**（如 INLINE-001 有 3 个 .asm）：逐产物比对，或比对卡内锚定的那个主产物；多产物时卡内 `artifact_sha256` 只锚一个，其余产物在 `actual` 中留痕。
6. **跨编译器路径**：Windows 走 sha 强校验、Linux 走 artifact_assert。重编译不变量应在**两条路径都生效**——Windows 侧 sha 比对是重灾区（断言从未被评估），重编译能顺带激活 Windows 侧的断言检查。
7. **回滚条件**：若加确定性 flag 后仍有 >3 张存量卡重编译 sha 不一致且无法用结构化比对解释，**停止 P0-A**，保留现有 sha 校验，把"重编译不变量"降级为 warn（仅告警不 refute），写进 worklog 交人裁决。不要为了让 P0-A 通过而放宽存量卡的 sha。
8. **结构化比对的具体方案（若全文件 sha 不稳定时用）**：不要泛泛说"结构化比对"，按以下优先级：
   - **方案 1（首选）**：比对符号表——用 `nm <工件>` 或 `objdump -t` 提取符号名+地址，排序后 diff。符号表比全文件稳定（不受路径/时间戳影响）。
   - **方案 2**：比对关键指令序列——用 `objdump -d` 反汇编，提取每个函数的指令助记符序列（去掉地址和立即数），按函数名分组后 diff。这能检测"函数体被替换"但容忍"地址偏移不同"。
   - **方案 3（最后手段）**：只比对卡内 `artifact_assert` 中 contains_in/absent_in 断言涉及的符号区间——如果这些区间的指令序列一致，就认为工件未被篡改。这是最弱的比对，但比全文件 sha 稳定。
   - 实现时先试方案 1，若符号表也不稳定（极小概率）再试方案 2。方案 3 只在 P0-A 降级为 warn 时使用。

**验收**：
- 构造 E01 探针（helper 脚本编译后覆写）→ replay 重编译 sha 不一致 → refute:artifact_tampered
- 现有 56 卡重编译 sha 一致（或差异可解释：确定性 flag 问题）→ confirm 不退化
- 并发跑 6 轮 replay 无假失败（临时目录隔离）
- poison + pytest 绿

### P0-B【高】cat 式证据检测（452 E05）

**问题**：夹具 open 随库数据文件原样打印，输出逐字相等但零计算，run_match confirm。

**修复**：新增 gate 规则 `EV-FIXTURE-NO-ECHO-DATA`（先 warn 观察，不直接 block）。

**实现方案（务实，不做不可能的 C++ 数据流分析）**：
- 不要用 Python ast 做 C++ 数据流分析（ast 是 Python 的，解析不了 C++）。
- **方案 A（推荐，先做）**：正则模式匹配——扫描夹具源码中 `ifstream|fopen|open(.*O_RDONLY|std::ifstream` 打开仓库内相对路径文件，且读入变量在 ≤3 行内直接出现在 `cout|printf|fprintf` 中（中间无算术/函数调用）。匹配到 → warn。
- **方案 B（有余力）**：用 clang-tidy 的 `readability-identifier-naming` 或自定义 matcher 做更精确的数据流，但 clang-tidy 集成成本高，先不做。
- 方案 A 的误报率会较高（合法夹具也可能读文件后直接打印），所以**只 warn 不 block**，且列出所有命中的存量卡交人裁决。

**边界**：合法夹具也可能读文件（演示文件格式）。判据聚焦"读入值是否经过计算"——方案 A 的"≤3 行内直接输出"是保守近似，会漏掉"读入后经函数间接输出"的情况，但作为 warn 级检测足够。

**验收**：E05 探针 warn；存量 56 卡若有同类，列出来交人裁决。

### P0-C【高】判别力证明（452 E03 的根本修复）

**问题**：contains_in/absent_in 的 text 若在每个函数符号区间都出现（如 `.cfi_startproc`/`mov`/`ret`），对"该函数有没有某行为"零判别力。苦力的 denylist 收窄是打地鼠。

**根本修复**：评估 contains_in/absent_in 断言时，统计 text 在工件**各函数符号区间**的出现分布。**必须区分两种断言的语义**：

- **contains_in**（断言"符号在某区间内存在"）：若符号在太多函数区间都出现，说明它是"背景噪音"，无法证明"该函数有某行为"。这才是"无判别力"。
  - 设 text 出现的函数区间数为 `k`，工件总函数区间数为 `N`。
  - `k/N ≥ 0.8` 且 `N ≥ 3` → block（新卡）/ warn（存量）："断言符号在 80%+ 函数区间出现，无判别力"。
  - `N < 3`（工件太小）→ 不判 block，降 advice。
  - 额外考量**出现次数分布**：若符号在 ≤2 个函数区间但每个区间出现 >50 次（如循环内的 `mov`），也可能是背景噪音——标记为 advice（不 block，因为可能是真的高频操作），提示红队人工判断。
- **absent_in**（断言"符号在某区间内不存在"）：判别力统计**不适用**。若符号在其他函数区间出现但在目标区间不出现，这是强断言（证明"这个函数没有某行为"）。absent_in 的问题是"目标区间是否正确"（符号区间切分是否准确），不是"出现频率"。对 absent_in 只做苦力的 denylist 收窄（空/纯中文 block），不做频率统计。

- **通用符号**（main/call/ret 等，见苦力的 denylist）维持苦力的处理，作为快速路径。
- **同时保留苦力的 denylist 收窄**作为快速路径（空/纯中文直接 block），判别力统计作为 contains_in 的深度路径。

**实现提示**：先 Read `atom_evidence_replay.py` 中 contains_in/absent_in 的现有实现，确认符号区间切分函数名和调用方式，再在评估 contains_in 时插入频率统计。不要改 absent_in 的逻辑。

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
3. **重复键检测（具体做法）**：pyyaml 的 `safe_load` 默认 after-wins 不报错。标准做法是子类化 `yaml.SafeLoader` 并重写 `construct_mapping`，在加载时检查 `deep=True` 下的重复键：
   ```python
   class UniqueKeyLoader(yaml.SafeLoader):
       def construct_mapping(self, node, deep=False):
           mapping = super().construct_mapping(node, deep=deep)
           seen = set()
           for key_node, _ in node.value:
               key = self.construct_object(key_node, deep=deep)
               if key in seen:
                   raise yaml.constructor.ConstructorError(
                       None, None, f"duplicate key: {key}", key_node.start_mark)
               seen.add(key)
           return mapping
   ```
   用 `yaml.load(stream, Loader=UniqueKeyLoader)` 替代 `yaml.safe_load`。这同时覆盖 block-style 和 flow-style 重复键（E07/H8 根本消除）。注意：pyyaml 6.x 的 `construct_mapping` 签名可能略有不同，先 Read 已装的 pyyaml 版本（6.0.3）确认。
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

**G1 签收绑定（轻量，不用 GPG）**：gate 校验 `human:` 签收时，用 `git log --format='%an' -- <file>` 取**该文件所有历史 commit 的 author 集合**（不是只取最后一个），签收人不在集合中 → warn"签收人与该文件的任何提交者都不一致"。
- 为什么不用最后一个 commit：卡可能在多个 commit 中被修改（Agent 写初稿→人改一个字→Agent 再修），最后一个 commit 的 author 不一定是签署人。用所有历史 author 的集合更准确。
- 单人项目 author=liaoranran 通过；Agent commit 的 author 不是 liaoranran 会被标记（但如果人也改过该文件，集合中含 liaoranran 则通过——这是合理的，因为人确实接触过该文件）。
- 更精确的方案（有余力时）：用 `git blame -L <签收行号>` 定位 `human:` 那一行最后是谁改的。但 blame 成本高，先用 author 集合方案。

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

**探针→毒样例转化标准**：
- 探针是"完整攻击演示"（含夹具+卡+replay结果+分析），毒样例是"最小攻击片段"（只含触发规则的 frontmatter/夹具/断言）。
- 转化时**裁剪掉与攻击无关的部分**：如果探针用了一个 50 行的夹具但攻击只依赖其中 3 行，毒样例用 3 行的最小夹具。
- 每个毒样例必须有**对应的阴性样例**（合法卡，验证规则不误伤）——这是 pytest 反例的来源。
- 毒样例编号续 `poison_drill.py --list` 的最大编号，不要跳号。
- 若某个探针在"探针可用性前置验证"中已被标记为"无法复现"或"已被苦力修复"，跳过转化，在 worklog 中注明。

---

## 四、今晚可选（P1/P2，P0 完成后量力，可跨窗口）

- **P1-1 writer_selfcheck 收尾**：核对苦力的 7 项 WC 测试覆盖、cppbible 登记、quality 门禁接入；核实 EV-MEM-017 `_Znwm/_Znwy` 是否已修，修了则评估 WC-02 升 fail。
- **P1-2 闪卡 verified 过滤**：flashcard_export 加 `status == verified` 过滤（E16），重导出确认 draft 不再出现。
- **P2-1 ccache 接入 replay**：环境已就绪（Win `C:\tools\ccache\ccache.exe`、WSL `/usr/bin/ccache`）。给 replay 的 WSL 编译调用前缀 ccache，构建目录固定 /tmp，实测二次 replay 耗时（预期 2min→~10s），记录数字。Windows 侧同理。**注意 ccache 与 P0-A 重编译的交互**：重编译也要走 ccache 否则两次编译都 miss。
- **P2-2 规则渐进发布**：gate 规则加 `status: experimental|stable|deprecated`，新规则默认 experimental=warn。
- **P2-3 成本 trace 补全**：cost_tracker 目前只采机器侧（5765 tok/颗）。补一个手填字段模板：红队轮次、红队工具调用数、窗口数，让单颗真实成本（估算 ~2 万 tok）可追踪。**关键认知（466 中期调整 3）**：ccache 省的是编译时间（秒级），红队 token 才是最大成本（分钟级——一次红队子 agent 53 次工具调用）。成本优化的真正杠杆是**减少红队轮次**（错误左移+红队分层触发），而不是加速编译。trace 数据要能回答"红队占单颗总成本的百分比"，这个数字下降才是真优化。

---

## 五、架构方向（**今晚不做**，但你要知道系统往哪走）

四轮复盘（三轮深度批判 + 一轮信任/度量/消费视角）收敛出系统的**五维成熟度模型**。验证是地基（今晚 P0 在加固），其余四维是系统从"脚本集合"变成"产品"的支柱。**不要在今晚实现它们**，但如果 P0 做完有余力，可以写设计笔记到 `_worklog_470.md`。

### 五维成熟度总览

| 维度 | 当前状态 | 核心问题 | 定义了什么 |
|---|---|---|---|
| **验证** | ✅ 较强（L1-L4 齐全，今晚 P0 后更强） | 运行时不变量、判别力、标准解析待补 | 知识可核验 |
| **信任** | 🟡 弱 | 信任根是人审字符串；编译器可信假设未显式化 | 验证结果可信 |
| **度量** | 🟡 弱 | 只有生产侧成本，无攻击成本/信噪比/过期 | 系统可观测、可判断是否在进步 |
| **消费** | 🟡 弱 | 知识图谱建了但没被教学利用 | 知识有价值 |
| **进化** | ❌ 最弱 | 变异（新规则/新防御）全靠人 | 系统自己变强 |

### 维度 1：验证（今晚 P0 加固，不赘述）

见第三节 P0-A~H。验证是其余四维的前提——验证不可信，度量/信任/消费/进化都无从谈起。

### 维度 2：信任（信任链的根在哪里）

**问题**：顺着"原子为什么可信"追到底——原子←证据卡←replay←编译命令+sha←工件没被篡改←**人审签署**。而人审目前只是字符串（E12，P0-G 绑 git author 但 `--author` 仍可伪造）。整个系统的信任根最终落在"人是诚实的"，在放权自动化趋势下越来越弱。

**方向**：
- 高 DAL（A/B）原子的**多模型交叉签署**：两个不同模型族的红队独立验证，交集才放行，差集标记为模型盲区
- 编译器可信假设显式化：每卡声明"本结论依赖 GCC/Clang 版本 X 的行为"，编译器大版本升级时触发批量重验证
- 接受"系统内信任"而非"绝对信任"：verified = "通过了当前最强验证"，不是"绝对正确"

**诚实的系统边界（466 矛盾 5）**：DAL A/B（错用即 UB 且难复现）的判定需要语义理解，gate 只能做机械检查，红队可以做语义审查但结论需要人仲裁——而人（用户）不是 C++ 专家。**这意味着"离开了人也能自己纠错"的目标在 DAL A/B 类原子上有硬上限**。缓解方向：①多模型交叉签署降低对单人专家的依赖；②把 DAL A/B 的判定标准尽可能形式化（如"UB 必须有 sanitizer 报告或标准条文引用"），减少对"专家直觉"的依赖；③接受 DAL C/D/E 全自动、DAL A/B 半自动的混合自治模式，而不是追求 100% 无人。

### 维度 3：度量（没有度量就无法判断是否在进步）——**下一批次最高优先级**

**问题**：系统目前只有生产侧成本（5765 tok/颗机器侧），缺少四个关键度量：
1. **攻击成本**（比拦截率更本质）：每轮对抗的 token/工具调用/探针数/逃逸数，计算"每逃逸成本"。这个指标上升 = 防御在生效（攻击者 ROI 下降），比波动的拦截率稳定。452 拦截率 7% 但攻击成本明显高于 368 第一轮，说明防御在生效但拦截率看不出来。
2. **warn 信噪比**：每条 warn 被后续证实为真问题的比例。warn 从 8→32 且一次性 accept 成基线，"狼来了"效应已发生——人/模型开始忽略 warn，系统在悄悄从 fail-closed 滑向 fail-open。需要 warn 老化机制（超 N 版本未处理的 warn 升级或明确标注"已知接受"）。
3. **知识半衰期**：verified 原子会因编译器升级/标准演进而过期。replay 的 sha refute 是隐性过期检测，但缺少"最后验证时间"字段、定期全量 replay、编译器大版本升级时的批量重验证触发。
4. **红队 ROI**：writer_selfcheck 拦住了多少问题、红队每轮发现多少真问题、一次过率——这些决定"红队分层触发"是否可行，目前零数据。

**方向**：`tools/metrics.py` 统一采集上述指标，`docs/kernel/metrics_baseline.md` 记录基线，每次批次结束自动更新。**度量先行**——没有度量，进化和消费是否生效都无法判断。

### 维度 4：消费（知识图谱建了但没被用）

**问题**：原子有 relations（prerequisite/specializes/realizes/evolved_from/contradicts）、serves、pedagogy.misconception，但只被用于 gate 检查和依赖遍历。**教学消费侧几乎为零**：闪卡导出是扁平 106 张，没有利用 prerequisite 做学习路径；学一颗原子时没有"先学前置""这颗和那颗矛盾"的推荐；misconception 没有被用于诊断性测试。

**方向**：
- 闪卡导出按 relations 排序（prerequisite 在前），生成"学习路径"而非扁平列表
- 基于 misconception 的诊断性测试（先测误解，再推对应原子）
- 基于 DAL 的学习优先级（高 DAL 原子优先学）

### 维度 5：进化（变异自动化，定义"可进化"）

**问题**：进化 = 变异 + 选择 + 遗传。选择（门禁）和遗传（git）已机器化，**变异（新规则/新防御的产生）全靠人**——人写提示词→好模型写代码→人审批。这是系统从"被攻击后修复"到"自我攻击+自我修复"的唯一瓶颈。

**方向**：把 452 成熟的对抗模式（两阶段盲读、沙箱 monkeypatch、可复现探针、零污染自证）固化为 `tools/auto_redteam.py`：
- 新规则上线后自动跑一轮攻击（不需要人投喂提示词）
- 发现逃逸后自动生成"规则候选+毒样例候选"（人只审批）
- 探针自动沉淀为永久毒样例（防退化，P0-H 是手动版，auto_redteam 是自动版）
- 定期（如每周）自动发起全量对抗，产出"系统健康报告"

### 下一批次优先级（今晚 P0 之后）

**度量（维度 3）先行**，因为没有度量就无法判断进化和消费是否在生效。然后是：
1. 进化（auto_redteam，变异自动化）——系统从"人驱动"到"自驱动"的定义性一跃
2. 消费（知识图谱教学利用）——让知识资产产生价值
3. 信任（多模型交叉签署+编译器假设显式化）——高 DAL 原子的可靠性保障
4. 验证器可插拔（replay 抽象为引擎+插件）——领域无关的技术基础
5. 文档生效状态（docs/status.json）——可维护性

**注意**：原"四拼图"（变异自动化/验证器可插拔/文档状态/自监控）已全部融入上述五维——自监控归入度量，文档状态归入度量的可维护性子项。

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
11. **fail-closed 设计原则（第四轮复盘教训）**：错误代价不对称——假阴性（坏卡流入 verified）的代价远高于假阳性（好卡被拦）。新增规则时，**不确定就 block/warn，不要为了"少误伤"而放宽到静默放行**。warn 不是"没事"，是"需要人看一眼"——如果一条规则的 warn 永远没人处理，它就等于不存在。每条新规则必须有明确的"处理期限"或"已知接受"标注，禁止 warn 无限累积。
12. **规则渐进发布（466 矛盾 2 教训）**：新规则不要一上来就 block。流程：先 `experimental`（只记录不输出）→ 观察 1 批次（看命中哪些卡、是真问题还是误报）→ 确认精确率后升 warn → 再观察 → 升 block。P0-B（cat 证据）已按此做（先 warn），P0-E/F 等新规则也应遵循。**跳过观察期直接 block 是 warn 信噪比恶化的根因**——466 实测 32 条 warn 中 17 条是误报，就是因为规则没经过观察期。

---

## 七、收工交付（无论做到哪）

写 `_worklog_470.md`，包含：
1. 每个 P0/P1/P2 项的状态（完成/部分/未做）、commit hash、实测门禁数字。
2. 新增规则名与毒样例编号、pytest 新增用例数。
3. **P0-A 编译确定性实验结果**（加 flag 前后两次编译 sha 是否稳定；ccache 是否禁用；哪些夹具仍不稳定）——这是后续 replay 不变量的基础，必须有结论。
4. **P0-D 存量兼容性测试结果**（safe_load vs 自定义解析器的 diff 分类统计；是否决定硬切）。
5. **苦力方案验证结果**：E01 探针 against 苦力 F02 的实跑结果（是否真拦不住）、E03 探针 against 苦力 F03 的实跑结果。如果苦力的方案意外有效，说明本文的"升级"判断有误，记录下来。
6. **每个 P0 的回滚条件是否触发**：P0-A 是否因 >3 张卡不稳定而降级为 warn？P0-D 是否因兼容性差异 >10 张而不硬切？触发了回滚的任务，写明原因和替代方案。
7. **本地试点数据（466 立即行动 2："实现了"≠"验证了"）**：每个 P0 修复不能只说"规则加了、毒样例配了、pytest 过了"，必须有**在 1-2 颗真实存量原子上跑过的前后对比**——例如 P0-C 判别力统计跑完全量 56 卡后，命中了哪些卡的哪些断言、是真恒真还是误伤、逐条裁决。缺这个的落地项标"已实现未验证"，不计入"已闭合"。
8. 所有"与文档不符"的发现（苦力报告说 430/414/424 的基线数字系统性失真，以你实测为准）。
8. 未完成项的下一步精确命令。
9. 最终再跑一遍第一节全套门禁，贴最终基线。
10. 列所有本地 commit（`git log --oneline` 从开工点到收工），注明**未 push**、ahead 数交用户。
11. 若 P0 有未闭合项，明确写"当前系统仍存在哪些可复现逃逸"，**不得用"基本完成"掩盖**。

**优先级纪律**：P0-A（重编译不变量）和 P0-D（切 safe_load）是本晚最高价值——前者是运行时防御范式，后者一次性消除整个解析器攻击面。P0-C（判别力）次之。P0-B/E/F/G/H 是规则级，相对独立。安全地基闭合前不要转去做 ccache/闪卡等增量功能。
