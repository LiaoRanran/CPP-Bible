# 647 B2 · anti-windup **真上岗**（超预算冻结 · 积压 >80% 喊人清理）

- 当前模式：**enforce**（enforce = 冻结即不入队；shadow = 只标记，`enqueued` 恒 True）
- 阈值（均沿用 636/642 **设计假设值**）：容量 A=100 · 半饱和 50% · 老化 30 天 · 预算 20/周 · **积压警报 80%**

## 一、当前队列与警报

- 队列长度：**107**；占用：**107.0%**；等级：**饱和**
- 周新增：**104**（超预算：True）
- **积压警报：True**（>80% ⇒ 需人审清理；当前 107.0%）
- 队列文件未被改动（sha256 `bffc170772f23e48…`，只读）

## 二、enforce vs shadow 的差别（合成输入，验证机制）

| 队列状态 | 占用% | 积压警报 | 低优先级入队(enforce) | 低优先级入队(shadow) | 高优先级入队(enforce) |
|---|---|---|---|---|---|
| 正常 | 1.0 | — | ✅ | ✅ | ✅ |
| 半饱和 | 51.0 | — | ✅ | ✅ | ✅ |
| 半饱和+超预算 | 51.0 | — | ⛔ 冻结 | — | ✅ |
| 饱和 | 101.0 | ⚠️ | ⛔ 冻结 | — | ✅ |

## 三、对当前队列回放（107 项）

- 优先级分布：`{'高': 4, '中': 61, '低': 42}`
- **会被冻结（enforce 下不入队）**：**85** 项

| 卡 | 规则 | 优先级 | 等待代理(天) | 冻结(真) | 理由 |
|---|---|---|---|---|---|
| `ATOM-MEM-LEAK-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 29.8 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-MOVE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 29.4 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-MOVE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 29.1 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-NEW-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 28.7 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-NEW-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 28.3 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-NEW-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 28.0 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-PERF-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 27.7 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-PERF-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 27.3 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-PERF-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 26.9 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-PERF-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 26.6 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-PERF-003` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 26.2 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-PERF-003` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 25.9 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RAII-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 25.6 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RAII-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 25.2 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RAII-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 24.8 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RAII-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 24.5 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RAII-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 24.2 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RAII-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 23.8 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RVREF-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 23.4 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RVREF-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 23.1 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-RVREF-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 22.8 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-SHARED-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 22.4 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-SHARED-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 22.1 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-SHARED-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 21.7 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-SHARED-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 21.3 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-SHARED-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 21.0 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-SHARED-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 20.7 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-UNIQUE-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 20.3 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-UNIQUE-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 19.9 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-UNIQUE-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 19.6 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-UNIQUE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 19.2 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-UNIQUE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 18.9 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-UNIQUE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 18.6 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-VALUE-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 18.2 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-VALUE-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 17.8 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-VALUE-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 17.5 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-VALUE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 17.2 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-VALUE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 16.8 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-VALUE-002` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 16.4 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |
| `ATOM-MEM-WEAK-001` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 中 | 16.1 | ⛔ | 队列饱和 ⇒ 冻结非高优先级入队 |

## 四、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| 20/周 是 **636 设计假设值**（非实测）⇒ 可能冻得过严，把该审的请求挡在门外 | 低优先级项被长期冻结且无人清理 | `QUEYI_PROTECTOR_MODE=shadow` ⇒ 立刻回到只标记不丢请求；或调大 `base.CAPACITY_PER_WEEK` |
| 冻结 = 不入队 ⇒ 若上层无重试/告警，请求可能**静默消失** | 上游只调用一次 `admit()` 不看返回值 | `admit()` 返回体含 `reason` 与 `backlog`；占用 > 80% 时额外 `needs_human_cleanup` （交人清理）；shadow 下 `enqueued` 恒 True |
| 等待天数是**位置代理**（队列无时间戳）⇒ 老化升级可能误触 | 升级清单出现人工确认不紧急的项 | 用真实到达时间戳替换代理，或调高 `base.AGING_DAYS` |

## 诚实登记

1. **阈值全是 636 设计假设值**（20/周、50%、30 天），**非实测**；
2. **等待天数是位置代理**（队列 jsonl 无时间戳），不是真实等待；
3. **冻结 = 不入队**，与 642 的「只标记」是**生产行为差别**；本模块只返回 `enqueued=False`，**不删任何既有队列条目、不动队列文件**；
4. **真实队列上冻结数为 0**（无「低」优先级项）⇒ 机制由**合成输入**验证（不夸大「已生效」）；
5. 积压警报只**喊人**（`needs_human_cleanup`），**不自动丢弃**请求。
