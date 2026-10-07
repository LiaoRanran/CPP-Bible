# 691 治理 claim 强化（B3）：452 事件账本 / 67 规则 / 规则哈希钉定

- 触发：690 指出治理 claim 经三轮评审**从未被检验**——既是未测风险，也是差异化机会
- 红线：**不新增未实测数字**；只使用既有产物中的计数与机制事实

---

## 1. 现状核查（689 状态）

| 问题 | 689 状态 |
|---|---|
| 治理机制写在哪 | §2 的 *Integrity mechanism* 段（3 句）+ 附录 `app:pinning` |
| 是否给具体计数 | 附录有（452 事件、67 规则），**正文只有定性句**（"hash-chained roots"） |
| 是否给"规则变更可审计"的定位 | ❌ 正文无 |
| 诚实边界 | ✅ 正文已有三处（`app:pinning`、tab:claim、tab:threats T10/T11） |
| 是否有"检测到篡改"的实例 | ❌ 无（**不得编造**，本批不声称） |

## 2. 691 强化内容（正文 §2，原文摘录）

> Evidence is content-addressed and the current state is protected by hash-chained roots over
> controlled directories; measurement events are recorded in an append-only authority ledger
> (**452 events**) under a rule manifest whose hash is pinned (`rules_sha256`, **67 rules**,
> v1.0.0). The point of pinning the *ruleset* rather than only the data is that a rule change then
> becomes **auditable instead of invisible**: a claim can be checked against the rule configuration
> under which it was produced, which is how we detected the caliber-drift instance in §3 (failure
> mode 1).

**定位转变（本批的核心增量）**：治理机制从"完整性措施"升级为**审计协议的一部分**——
它让"测出台账/规则被改过"成为可能，而不是宣称"改不了"。这与 §3 的 8 类失败模式（mode 1
caliber drift）形成闭环：审计协议要求 claim 携带 $Q=(D,A,E,\Theta,P)$，而 $\Theta$ 的**版本可钉定**
正是该要求可执行的前提。

## 3. 诚实边界（**强化而非新增**，原文摘录）

> This is **tamper-evident current-state integrity with partial historical reproducibility**—*not*
> an immutable log and **not tamper-proofing**: an actor controlling both the artifacts and the root
> can recompute both, and because the 452 existing ledger events predate rule-hash pinning,
> historical states are reproducible only under an unchanged-ruleset assumption (`app:pinning`).
> The remaining gap is disclosed rather than closed: the reconciler assumes an enumerable write
> surface, which parallel development is the easiest way to break (`app:humanize`).

| 边界 | 说明 |
|---|---|
| 非 immutable | 同一方控制工件与根即可重算两者 |
| 非 tamper-proof | 只提供**篡改证据**，不提供**阻止篡改** |
| 452 事件未携带 ruleset hash | 历史重放需假定规则未变（已登记为 future work） |
| 写入面可枚举假设 | 并行开发是最容易破坏它的方式（本文自己踩过） |

## 4. 与近邻的差异化（可迁移价值）

| 系统 | 治理/审计对象 | Queyi 的差异 |
|---|---|---|
| DeepFact（AtS） | benchmark 标签与理由 | 不治理**测量口径与规则版本** |
| Who Grades the Grader | 度量函数（anchor guards） | 不记录**规则哈希与事件账本** |
| SV-COMP | witness validation | 不审计**评估器自身的配置漂移** |
| HELM / Model Cards | 文档清单 | 非**可执行**且非**失败驱动** |

⇒ 治理层是 Queyi 在"评估器审计"方向**未被占用的差异点之一**（但**不声称首次**，
且**不声称不可篡改**）。

## 5. 未做（诚实清单）

- **没有**"检测到篡改企图 N 次"之类的实例计数——本批未做篡改检测实验，不得编造；
- **没有**对 452 事件逐条做哈希校验的公开报告（仅总数与 append-only 事实）；
- 规则哈希钉定的**回填**（把 `rules_sha256` 写进 452 条历史事件）仍为 future work。
