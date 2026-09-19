# 04 方向 4：replay 不变量与活性属性的形式化规格

> 基于 01 的状态机建模。每项给：自然语言 + TLA+ 公式草案 + 当前是否满足 + 证据/风险。代码行号来自 `atom_evidence_replay.py`（2026-09-19 读码）。

---

## 4.1 不变量（Invariants / Safety）

记抽象变量：`phase`、`artifactNow`（当前工件字节）、`artifactSnap`（进入 Snapshot 前的快照字节）、`lockHeld`、`verdict`、`assertExpect`（卡期望）、`assertActual`（实际结果）。

**I1 仓库一致性不变量 `RepoConsistent`**
- 自然语言：replay 完成后，真实仓库工件字节 == 跑批前快照。
- 公式草案：`AFTER Restoring: artifactNow = artifactSnap`
- 当前状态：**已满足（代码兜底）**。还原逻辑在 `finally`（1724-1735）：`art_path.write_bytes(original)`（1726）+ 空文件兜底 `_restore_artifact`（1731）。`original` 在 1547 于任何命令前快照。
- 风险/已知违反案例：**2026-09-18 的"还原冲掉未提交编辑"** 是**测试套件**的 `git checkout`（非本工具）所致；本工具的 `_restore_artifact` 仅当工件缺失/空才重建（1081-1091），**不会覆盖非空文件**——故本工具层面该不变量比测试套件更稳。但仍建议 TLC 证明 `finally` 路径真的覆盖所有 20+ return 点。

**I2 判定一致性不变量 `VerdictMatchesAssert`**
- 自然语言：confirm/refute 判定与 `artifact_assert` 一致。
- 公式草案：`verdict = Confirm <=> AssertSatisfied(assertExpect, assertActual)`
- 当前状态：**已满足**。逻辑在 1643-1682（sha 命中 / 跨编译器结构断言）+ 1574-1633（run_match）+ 1706（阴性对照）+ 1714（sanitizer）。
- 风险：跨编译器时降级为结构断言（1670），若 `artifact_assert` 字段缺失则仍可能漏判；建议 TLA+ 形式化"降级分支也须闭合"。

**I3 符号一致性不变量 `SymbolCheckConsistent`**
- 自然语言：检查的符号 == `artifact_assert` 中声明的符号（不多查、不漏查）。
- 当前状态：**部分**。`check_artifact_assert`（663）按卡声明查；但纯标准库无法验证"符号语义 == 断言期望语义"（那是翻译验证，见 02）。

**I4 并发隔离不变量 `ConcurrentIsolation`**
- 自然语言：并发跑批时各 worker 沙箱互不干扰。
- 公式草案：`\A w1,w2: w1.lockAcquired => ~w2.lockAcquired`（互斥）
- 当前状态：**已满足（靠锁）**。锁 `_acquire_replay_lock`（952）用 `O_CREAT|O_EXCL`（970）保证同机串行；pid 存活检测（975-979）+ 陈旧接管（984）。但工具**刻意串行无 `--jobs`**（1911-1917），并发只来自多 worker 进程，锁是进程级文件锁。
- 风险：锁文件落在 `build/.replay_lock`（945），**跑批期各 worker 各有独立锁**（batch_root，945 注释）——多 worker 并发时锁路径分片正确性是关键不变量，值得 TLC 建模。

**I5 锁正确性不变量 `LockEventuallyReleased`**
- 自然语言：锁不会死锁（最终释放）、不会漏锁（需互斥的操作都在锁内）。
- 公式草案：`[] (lockAcquired => <> ~lockHeld)`
- 当前状态：**已满足**。`finally` 中 `_release_replay_lock`（1736）；释放失败不抛（1052-1056，safe-delete 容忍），残留锁由 pid/mtime 兜底自愈。Windows 上**不用 `os.kill(pid,0)`**（会 TerminateProcess，1019-1050）——这是锁正确性的关键防坑。

**I6 manifest 一致性不变量 `ManifestConsistent`**
- 自然语言：`build/replay_manifest.json` 记录的 sha/verdict == 实际。
- 当前状态：**已满足**。`update_manifest`（1888）用 `card_fingerprint`（1805，卡+夹具+工件 sha）作指纹；`MISSING` 强制重跑（1808）。增量跳过仅当指纹相同且上次 confirm（1869-1871）。

**I7 错误处理不变量 `InfraNotRefute`**
- 自然语言：infra_error 与 refute 严格分流，不把环境故障误判为内容证伪。
- 当前状态：**已满足**。`classify_command_failure`（508-529）：rc==127 且编译器 → infra；rc==124 超时 → infra；其余 → refute。`_recompile_invariant` 的 unavailable/infra 也走 infra（1660-1665）。fail-closed：infra 也 exit 1（2001）。

**I8 还原幂等不变量 `RestoreIdempotent`**
- 自然语言：连续还原两次，仓库状态相同。
- 当前状态：**已满足**。`_restore_artifact`（1081）幂等（缺失/空才重建）；`write_bytes(original)` 幂等。

---

## 4.2 活性属性（Liveness）

**L1 终止性 `Terminates`**
- 公式：`[]<> (phase \in {Confirm, Refute, Infra})`
- 当前状态：已满足（每卡最终出判定；死循环会被 `compile_timeout` rc==124 兜成 infra）。

**L2 公平性 `NoStarvation`**
- 公式：`\A card: WF_card(PickNext)`（弱公平：卡持续可处理终会被处理）
- 当前状态：仅跑批多 worker 时需；单卡复算 vacuous。值得在并发模型中加 `WF`。

**L3 进度性 `Progress`**
- 公式：`处理 N 张卡时间 ~ O(N)`（无超线性）
- 当前状态：已满足（串行；增量模式把全量 245s → 单卡 2.3s，1785-1787 注释）。

**L4 错误恢复性 `ErrorRecovery`**
- 公式：`<> Infra(r) => <> (next card processed)`
- 当前状态：已满足（主循环 1956-1968 不因单卡异常中断整批；异常在 `replay_card` 包装 1772 重抛但 main 未 catch → 实际上单卡抛异常会中断整批！这是**潜在活性违反**，见 4.4 风险）。

---

## 4.3 已知违反不变量的案例
- **测试套件 `git checkout` 冲掉未提交编辑（2026-09-18）**：违反 I1，但**根因在测试套件不在 `atom_evidence_replay.py`**（本工具还原是快照写回，非 git checkout）。需在 580 回路 RED 修复后复测。
- **单卡异常中断整批（潜在）**：`replay_card` 包装在 1772 `raise` 重抛，main 主循环 1956 未 try → 一张卡抛异常整批中止，违反 L4。建议包一层 try 记 infra 续跑（对齐 508 的 fail-closed 精神）。

---

## 4.4 模型检查计划
- **检查哪些**：I1（仓库一致性，最关键、最易在 20+ return 点漏还原）、I4/I5（并发锁）、I7（infra/refute 分流）。
- **抽象层级**：不建模 g++ 编译，只把 `Compile` 当"成功/失败"布尔；不建模 56 卡，取 2-3 卡小模型 + 2 worker 并发。
- **预期结果**：证明 I1/I4/I5/I7 在规格下恒真；或**发现单卡异常路径未走 `finally` 还原**（即 L4 风险）的 bug。

---

## 4.5 不变量优先级（先查什么）
1. **I1 仓库一致性**（最高危，历史已出事）
2. **I5 锁释放**（并发正确性基石）
3. **I7 infra/refute 分流**（fail-closed 防逃生舱）
4. **I4 并发隔离**（跑批多 worker 时）
5. I2/I6（已有明确实现，风险低）
6. I3/I8（辅助）

---

## 4.6 成本-收益
- 成本：TLA+ 规格编写 1-2 天 + TLC 几分钟-几小时。
- 收益：把"隐式不变量"变"可证不变量"；防未来回归；活文档。对当前最痛的 I1 已代码兜底，模型检查价值在"证明兜底真的全覆盖"。

---

## 4.7 外部一手来源
- 【已查证】TLA+ 时序/活性：learntla.com/core/temporal-logic.html、will62794.github.io Liveness and Fairness（2026-09-19）
- 【一方称】Lamport《Specifying Systems》Invariants/Liveness 章节
