# 01 方向 1：TLA+ 核心概念与本项目 replay 状态机建模

> 证据纪律：代码行号来自 `tools/atom_evidence_replay.py`（实测读码，2026-09-19）。外部链接标注【已查证】(2026-09-19 检索) / 【一方称】(源自训练知识、未实抓)。

---

## 1.1 TLA+ 核心概念（准确解释）

TLA+ = **Temporal Logic of Actions**，由 Leslie Lamport 设计，用于**并发与分布式系统**的建模与验证【已查证：lamport.azurewebsites.net/tla/tla.html，检索 2026-09-19】。它的核心是把系统建模为一个**状态序列（行为/behavior）**，用**时序逻辑**描述"所有行为都必须满足"的性质。

- **状态（state）**：变量到值的赋值。TLA+ 规格里用 `VARIABLES` 声明。
- **动作 / 状态迁移（action / transition）**：描述"下一步可能怎样"的关系，通常是 `x' = ...` 形式（`'` 表示下一状态）。所有动作用析取拼成一个 `Next`。
- **初始状态（Init）**：一个谓词，描述合法的起始状态。
- **不变式（Invariant / safety）**：`Inv` 表示"每个可达状态都满足 Inv"。例：类型不变量 `TypeOK`、互斥 `MutexInv`。【已查证：learntla.com/core/temporal-logic.html，检索 2026-09-19】
- **活性（liveness）**：`[]<>P` = "最终总是 P"（P 无限经常成立）；`<>P` = "最终 P 成立一次"。例：`<><terminated>` = "最终会终止"。
- **公平性（fairness）**：`WF_vars(Action)` 弱公平（若 Action 持续可行则终会发生）；`SF_vars(Action)` 强公平。用于排除"某迁移永远被饿死"的非法行为。
- **模块（module）/ 实例化（instance）**：`MODULE` 封装规格，`INSTANCE` 复用并替换参数。
- **THEOREM**：可声明"此规格蕴含某性质"，交给 **TLAPS**（TLA+ 证明管理器，配合 Isabelle/Coq/Z3）做** deductive 证明**【已查证：lamport.azurewebsites.net/tla/tools.html，检索 2026-09-19】。
- **工具链**：**TLC** 模型检查器（穷举有界状态空间）、**SANY** 语法分析、Toolbox（Eclipse IDE）、VS Code 插件【已查证：github.com/tlaplus/tlaplus，检索 2026-09-19】。
- **PlusCal**：算法语言，编译成 TLA+，比纯 TLA+ 易写顺序/循环逻辑【一方称：Lamport《Specifying Systems》第 1-3 章；该书 PDF 在 lamport 站免费】。

### 反例（TLA+ 不适用本项目的点）
1. **不验证"编译结果正确"**：TLA+ 验证的是 replay *状态机* 的正确性，不是 g++ 的正确性。语义正确性超出其范围（那是翻译验证/CompCert 的事）。
2. **不适合验证数值/符号语义**：本项目关心"符号是否存在、二进制是否同代"，这些是离散状态，适合；但"编译后的语义等价"需翻译验证，TLA+ 表达成本高、收益低。

---

## 1.2 replay 状态机的真实建模（基于代码，非想象）

读取 `atom_evidence_replay.py` 的 `_replay_card_impl`（1477-1741）+ `replay_card` 包装（1761-1778）+ `main`（1908-2005），归纳出以下离散状态（用抽象变量 `phase` 表示）：

| 状态 | 进入条件（代码依据） | 退出迁移 |
|---|---|---|
| `Idle` | 主循环取一张卡（1956） | → `Parsing` |
| `Parsing` | `parse_frontmatter`（1478） | 成功 → `FieldCheck`；异常 → `Refute(bad_frontmatter)`(1480) |
| `FieldCheck` | 必填字段校验（1482-1494） | 缺字段 → `Refute(missing_field)`(1494)；否则 → `CompilerGate` |
| `CompilerGate` | MSVC 检测（1515）→ 编译器可用性（1522-1530） | MSVC/cl → `Infra(msvc_unavailable)`(1517)；无 g++ → `Infra(compiler_missing)`(1530)；否则 → `Locking` |
| `Locking` | `_acquire_replay_lock`（1535） | 超时 → `Infra(replay_busy)`(1538)；拿到 → `Snapshot` |
| `Snapshot` | 自治愈备份 + 快照（1540-1548） | → `Compile` |
| `Compile` | `run_commands`（1563）→ `classify_command_failure`（1569） | 失败 → `Refute/Infra`(compile_error/timeout)(1569-1571)；成功 → `RunMatch`(1572) |
| `RunMatch` | stdout 与卡比对（1574-1633） | 不符 → `Refute(run_mismatch/...)`；否则 → `ArtifactSha` |
| `ArtifactSha` | 重生成工件 sha（1643-1682） | 缺 → `Refute(artifact_absent)`；同代命中 → `RecompileInv`；跨编译器 → 结构断言 `Refute(artifact_assert_failed)` 或继续；不同代 → `Refute(sha256_mismatch)` |
| `RecompileInv` | `_recompile_invariant`（1654-1666） | tampered → `Refute(artifact_tampered)`；infra → `Infra(recompile_*)`；否则 → `ExtraArts` |
| `ExtraArts` | 多产物 sha（1687-1703） | 失配 → `Refute`；否则 → `NegativeControls` |
| `NegativeControls` | `check_negative_controls`（1706） | 命中 → 对应 verdict；否则 → `Sanitizer` |
| `Sanitizer` | `check_sanitizer`（1714-1718） | reported → `Refute(sanitizer_reported)`；否则 → `Restoring` |
| `Restoring` | 还原工件（1724-1735）→ 释放锁（1736） | → `Confirm` |
| `Confirm` | 全过（1722） | → `Idle`（取下一卡） |
| `Refute(r)` / `Infra(r)` | 任意阶段判定 | → `Restoring`（仍要还原，1724 finally） → `Idle` |

> 关键观察：**除 `Parsing` 的 `bad_frontmatter` 外，几乎所有失败分支都走 `finally` 的 `Restoring`（1724）**，即"无论判定如何，都要还原工件 + 释放锁"。这正是仓库一致性不变量与锁正确性的落点。

### 不变量（候选，形式化见 04）
- `RepoConsistent`：退出 `Restoring` 后，工件字节 == 进入 `Snapshot` 前的快照（1726 `art_path.write_bytes(original)`）。
- `LockEventuallyReleased`：`Locking` 进入后，最终必到 `_release_replay_lock`（1736）。
- `VerdictMatchesAssert`：`Confirm/Refute` 的判定与 `artifact_assert` 一致（1643-1682 逻辑）。
- `InfraNotRefute`：`Infra` 与 `Refute` 严格分流（classify 508-529 + 1458-1463）。

### 活性（候选）
- `Terminates`：`[]<> (phase = Confirm \/ Refute \/ Infra)`（每卡最终出判定）。
- `NoStarvation`：并发跑批中每张卡最终被处理（公平性 `WF`）。
- `Progress`：N 张卡处理时间 ~O(N)（串行，无 `--jobs`，1911-1917）。

---

## 1.3 TLA+ 规格结构（草案大纲，详见 07）

```
MODULE ReplayStateMachine
EXTENDS Naturals, Sequences, TLC
VARIABLES phase, card, artifactBytes, lockHeld, verged
Init == phase = "Idle" /\ lockHeld = FALSE /\ verged = FALSE
Next == \/ PickCard \/ Parse \/ ... \/ Restore \/ ReleaseLock
Invariants == TypeOK /\ RepoConsistent /\ LockEventuallyReleased ...
THEOREM Spec => []RepoConsistent        \*  deductive（TLAPS）
```

---

## 1.4 PlusCal vs 纯 TLA+ 选择

- **本项目 replay 主体是"单卡顺序流水线 + 失败即还原"**，顺序语义为主 → **PlusCal 写主流程更可读**（循环取卡、顺序校验）。
- **但并发面（每卡锁、跨进程跑批）是纯 TLA+ 的强项**（PlusCal 的并发是进程级，建模"锁文件 O_EXCL + pid 存活检测"不够直观）。
- **建议**：用 **PlusCal 写单卡顺序流程**生成 TLA+，再**手写纯 TLA+ 补并发锁与公平性**。这样兼得可读性（顺序部分）与表达力（并发部分）。

---

## 1.5 模型检查可行性

- **状态空间**：抽象后每卡状态 ≈ 16 个 `phase` × 少量布尔（`lockHeld/verged/artifactChanged`）。56 张卡不需要全建模——**取 2-3 张卡的简化模型**即可暴露状态机 bug（brief 方向 4 也建议小模型）。
- **需抽象掉的细节**：不建模 g++ 编译过程，只把 `Compile` 当"成功/失败"抽象动作；不建模具体 sha 值，只建模"命中/未命中"布尔。
- **TLC 能发现**：死锁（某状态无出边）、不变量违反（`RepoConsistent` 被打破）、迁移遗漏（`Refute` 后忘记还原）、活性失败（某卡永远卡在 `Locking`）。
- **TLC 不能发现**：编译结果正确性、符号语义、`_recompile_invariant` 的语义（那是翻译验证）。

### 成本-收益
- **成本**：TLA+ 入门 1-2 天（PlusCal 更快）、规格编写 1-2 天、TLC 检查几分钟-几小时、Windows 装 tlc（Java 运行时，已有则可）。
- **收益**：把"隐式状态机"变"显式可检查规格"——既是 bug 猎手（防回归），又是**活文档**（新人读规格即懂 replay）。
- **诚实结论**：对"修复已知 bug"收益中（当前最痛的 bug 是仓库一致性，已在 `Restoring` finally 里兜底，模型检查更像是"证明它真的兜住了"）；对"防未来回归"收益高。

---

## 1.6 反例（TLA+ 不适用 / 过度处）
1. **79 命题推理（592 prop_closure）不需要 TLA+**：那是图可达性，纯标准库 BFS 已够，ITP/TLA+ 都杀鸡用牛刀。
2. **编译语义等价不用 TLA+**：C++ 语义太复杂，TLA+ 建模成本高、且 TLC 无法验证"两个程序语义等价"——这是翻译验证（Alive2/SMT）的地盘。
3. **单用户场景弱化公平性价值**：并发只在"跑批多 worker"时出现，日常单卡复算无并发，公平性约束几乎 vacuous——建模时要明确"仅跑批期需公平性"。

---

## 1.7 外部一手来源
- 【已查证】TLA+ 主页与工具：lamport.azurewebsites.net/tla/tla.html、/tla/tools.html（2026-09-19）
- 【已查证】TLA+ 学习站：docs.tlapl.us/learning:start（2026-09-19）
- 【已查证】TLC 仓库：github.com/tlaplus/tlaplus（2026-09-19）
- 【已查证】时序属性教程：learntla.com/core/temporal-logic.html、will62794.github.io Liveness and Fairness in TLA+（2026-09-19）
- 【一方称】Lamport《Specifying Systems》（免费 PDF，TLA+ 权威教材，含 PlusCal）
