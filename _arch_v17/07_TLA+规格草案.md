# 07 方向 1 配套：TLA+ 规格草案（replay 状态机）

> 草案大纲 + 关键公式。基于 01 的状态机建模与 04 的不变量。PlusCal 写单卡顺序流程，纯 TLA+ 补并发锁与公平性。
> 说明：这是**可施工的大纲/伪规格**，落地时需按真实代码常量补全（如锁路径、超时秒数）。

---

## 7.1 模块骨架（纯 TLA+）

```tla
---- MODULE ReplayStateMachine ----
EXTENDS Naturals, Sequences, FiniteSets, TLC

\* 抽象状态集合（对应 01 §1.2 的 phase）
CONSTANTS Idle, Parsing, FieldCheck, CompilerGate, Locking, Snapshot,
          Compile, RunMatch, ArtifactSha, RecompileInv, ExtraArts,
          NegativeControls, Sanitizer, Restoring, Confirm,
          Refute, Infra
CONSTANTS LockOk, LockBusy        \* 锁获取结果
CONSTANTS CompileOk, CompileFail  \* 编译抽象结果

VARIABLES
  phase,            \* 当前状态
  cardId,           \* 当前卡（简化为 1..N 的小模型，取 N=3）
  artifactNow,      \* 当前工件字节（抽象为枚举：Original / Modified / Absent）
  artifactSnap,     \* 进入 Snapshot 前的快照
  lockHeld,         \* 布尔：是否持锁
  verdict,          \* Confirm / Refute / Infra / None
  pending,          \* 待处理卡集合

\* ---- 类型不变量 TypeOK ----
TypeOK ==
  /\ phase \in (PhaseSet \union {Refute, Infra})
  /\ artifactNow \in {Original, Modified, Absent}
  /\ lockHeld \in BOOLEAN
  /\ verdict \in {Confirm, Refute, Infra, None}

\* ---- 初始 Init ----
Init ==
  /\ phase = Idle
  /\ artifactNow = Original
  /\ artifactSnap = Original
  /\ lockHeld = FALSE
  /\ verdict = None
  /\ pending = Cards        \* Cards = 1..3（小模型）

\* ---- 取卡 PickCard ----
PickCard ==
  /\ phase = Idle
  /\ pending /= {}
  /\ \E c \in pending : cardId' = c /\ pending' = pending \ {c}
  /\ phase' = Parsing
  /\ UNCHANGED <<artifactNow, artifactSnap, lockHeld, verdict>>

\* ---- 解析 + 字段检查（合并示意） ----
ParseAndCheck ==
  /\ phase \in {Parsing, FieldCheck}
  /\ phase' = CompilerGate
  /\ UNCHANGED <<artifactNow, artifactSnap, lockHeld, verdict, cardId, pending>>

\* ---- 编译器门禁：可用则取锁 ----
CompilerGateOk ==
  /\ phase = CompilerGate
  /\ phase' = Locking
  /\ lockHeld' = TRUE        \* 抽象：拿到锁
  /\ UNCHANGED <<artifactNow, artifactSnap, verdict, cardId, pending>>

\* ---- 快照 ----
DoSnapshot ==
  /\ phase = Locking
  /\ phase' = Compile
  /\ artifactSnap' = artifactNow   \* 记录跑批前字节
  /\ UNCHANGED <<artifactNow, lockHeld, verdict, cardId, pending>>

\* ---- 编译（抽象成功/失败） ----
CompileStep ==
  /\ phase = Compile
  /\ \/ /\ CompileOk
        /\ phase' = RunMatch
        /\ artifactNow' = Modified     \* 重生成工件（待还原）
     \/ /\ CompileFail
        /\ phase' = Restoring          \* 失败也走 finally 还原
  /\ UNCHANGED <<artifactSnap, lockHeld, verdict, cardId, pending>>

\* ---- run_match / artifact_sha / recompile_inv（抽象为一步确认） ----
VerifySteps ==
  /\ phase \in {RunMatch, ArtifactSha, RecompileInv, ExtraArts,
                NegativeControls, Sanitizer}
  /\ phase' = Restoring
  /\ UNCHANGED <<artifactNow, artifactSnap, lockHeld, verdict, cardId, pending>>

\* ---- 还原（关键：finally 路径，必须恢复 + 释放锁） ----
RestoreAndRelease ==
  /\ phase = Restoring
  /\ phase' = Confirm
  /\ artifactNow' = artifactSnap   \* I1 仓库一致性：还原成快照
  /\ lockHeld' = FALSE             \* I5 锁释放
  /\ verdict' = Confirm
  /\ UNCHANGED <<artifactSnap, cardId, pending>>

\* ---- 失败分支（Refute/Infra）也走还原 ----
FailThenRestore ==
  /\ phase \in {Refute, Infra}
  /\ phase' = Restoring
  /\ UNCHANGED <<artifactNow, artifactSnap, lockHeld, verdict, cardId, pending>>

Next ==
  \/ PickCard \/ ParseAndCheck \/ CompilerGateOk \/ DoSnapshot
  \/ CompileStep \/ VerifySteps \/ RestoreAndRelease \/ FailThenRestore

\* ---- 不变量（对应 04） ----
I1_RepoConsistent == phase = Confirm => artifactNow = artifactSnap
I4_NoDoubleLock   == ~(\E s,t \in ... )   \* 抽象：锁互斥（并发模型补）
I5_LockReleased   == lockHeld = TRUE => <> (lockHeld = FALSE)
I7_InfraNotRefute == verdict = Infra => verdict /= Refute

\* ---- 活性 ----
L1_Terminates == []<>(phase \in {Confirm, Refute, Infra})
L4_ErrorRecovery == (phase = Infra) => <>(cardId' \in pending \/ pending = {})

THEOREM Spec => []I1_RepoConsistent          \* 交给 TLAPS 或 TLC 检查
THEOREM Spec => []I5_LockReleased
====
```

## 7.2 PlusCal 主流程（示意，编译成上述 TLA+）
```pluscal
--algorithm replay {
  variables art = "original", lock = FALSE, v = "none";
  { while (pending /= {}) {
      with (c \in pending) { cardId := c; pending := pending \ {c}; }
      phase := "Parsing";
      phase := "CompilerGate";
      lock := TRUE;                       \* 取锁
      art_snap := art;                    \* 快照
      phase := "Compile";
      if (compile_ok) {
        art := "modified";                \* 重生成
        phase := "Verify";
      } else { phase := "Restoring"; }
      art := art_snap;                    \* finally：还原
      lock := FALSE;                      \* finally：释放
      v := "confirm";
      phase := "Confirm";
  } }
}
```

## 7.3 并发锁（纯 TLA+ 补，对应 I4/I5）
- 建模 `workers = 1..W`（W=2），每 worker 独立 `lockHeld[w]`；`Acquire(w)` 要求 `\A w2: ~lockHeld[w2]`（互斥）。
- 公平性：`WF_vars(Acquire(w))` 保证无 worker 饿死（L2 NoStarvation）。
- Windows 坑（代码 1019-1050）：不能用 `os.kill(pid,0)` 探活（会 TerminateProcess）→ 规格里用"pid 存活"抽象谓词，落地实现用 `OpenProcess`/`GetExitCodeProcess`。

## 7.4 预期模型检查结果
- TLC 应证明 I1/I5/I7 在规格下恒真。
- **故意删掉一处 `art := art_snap`（模拟漏还原）应导致 I1 违反**——以此验证规格能抓真实 bug（见 06 §6.6 测试策略）。
- 若 `FailThenRestore` 缺省（Refute 不还原），I1 违反 → 证明 finally 还原不可省（对应 04 §4.3）。

## 7.5 外部一手来源
- 【已查证】TLA+ tools：lamport.azurewebsites.net/tla/tools.html（2026-09-19）
- 【已查证】Learn TLA+：docs.tlapl.us/learning:start（2026-09-19）
- 【一方称】Lamport《Specifying Systems》PlusCal 章
