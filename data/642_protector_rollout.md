# 642 A6 · 五个保护器联调 + 灰度报告（**零生产判决被改变**）

> 灰度原则：flag 只加标记 / anti-windup 只标记不丢请求 / blind 只标记历史 + 盲化新项 /
> 校准只记账 / MDL 只对新规则。**没有任何判决、规则、账本被改写。**

## 一、联调结果：各保护器触发次数

| 保护器 | 触发 |
|---|---|
| A1 | `{"卡片": 23, "标记": 2, "判决被改变": 0}` |
| A2 | `{"队列": 65, "queued_pending": 65, "冻结": 0, "升级": 0}` |
| A3 | `{"历史判决": 452, "违规标记": 258, "账本未变": true}` |
| A4 | `{"规则": 67, "有样本": 0, "用代理": 67}` |
| A5 | `{"ADMIT": 1, "REJECT_编码长度": 1, "PENDING_HUMAN": 1, "REJECT_豁免率": 1, "REFUSE_已有规则": 1, "REJECT_热力图缺失": 1}` |

## 二、零漂移实证（联调前 vs 联调后）

| 生产工件 | 前 | 后 | 相同 |
|---|---|---|---|
| `gate_engine.py` | `03cd20dcdbee…` | `03cd20dcdbee…` | ✅ |
| `atom_evidence_replay.py` | `4b142e68a97a…` | `4b142e68a97a…` | ✅ |
| `poison_drill.py` | `37f638004c4d…` | `37f638004c4d…` | ✅ |
| `toolchain.py` | `5920bff6af16…` | `5920bff6af16…` | ✅ |
| `cppbible.py` | `4454db9b4992…` | `4454db9b4992…` | ✅ |
| `decision_ledger` | `ec8cbf5cca2d…` | `ec8cbf5cca2d…` | ✅ |
| `authority_log` | `01b17c520cde…` | `01b17c520cde…` | ✅ |
| `human_queue` | `79c88f6ff7f5…` | `79c88f6ff7f5…` | ✅ |
| `verified_cards` | `078616367855…` | `078616367855…` | ✅ |

- **漂移项：零**；**生产判决被改变：0**

## 三、标记清单（按保护器分区，**可叠加、不互相覆盖**）

| 保护器 | 标记键空间 | 本次标记 |
|---|---|---|
| A1 | `conflict_flag`, `conflict_types`, `conflict_strength` | `{"conflict_flag": false, "conflict_types": ["RR"], "conflict_strength": 0.0}` |
| A2 | `queued_pending`, `frozen`, `upgraded`, `priority_out` | `{"queued_pending": true, "frozen": false, "upgraded": false, "priority_out": "高"}` |
| A3 | `blind_state`, `masked`, `residual` | `{"blind_state": "BLIND", "masked": 25.85, "residual": -9.95}` |
| A4 | `total_count`, `error_count`, `known_error_rate` | `{"total_count": 0, "error_count": 0, "known_error_rate": 0.1881}` |
| A5 | `decision`, `detail` | `{"decision": "ADMIT", "detail": "长度 OK（savings 531.9 > cost 184）· 豁免率 0.1 < 0.3"}` |

### 3.1 可叠加 + 回滚（机械验证）

- 五个保护器的键空间**互不重叠** ⇒ 叠加后全集 = 15 个键；
- 同名键值冲突 ⇒ `MarkConflictError`（**不静默覆盖**）；
- `rollback_marks()` 按保护器精确摘除，逐个回滚到底 ⇒ `marks == {}`。

## 四、误判风险评估（含回滚动作）

| 保护器 | 风险 | 回滚动作 |
|---|---|---|
| A1 | θ=0.3 为 636 初值，未用真实样本回填 ⇒ 可能过紧（误标）或过松（漏标） | `--mode shadow` 立即回到只出报告；θ 调整需人审后改 THETA 并重跑 |
| A1 | RR 型是**全局规则集属性**（block 44 + warn 16 恒定共存）⇒ 所有卡 RR=1，区分度有限 | 报告已按型分列；如需按型定阈，643 再拆 θ_RR/θ_EE |
| A1 | `agreement` 用「被引用证据存在率」近似，**非统计一致度** | 只加标记不改判决 ⇒ 最坏后果是人工复核队列变长，不影响任何判 pass/fail |
| A1 | 占位判决（verified ⇒ pass）与 gate 真实判决未必一致 | 占位判决的 `reason` 字段自带声明；生产判决唯一来源仍是 gate_engine |
| A2 | 周处理能力 20/周是 636 假设值，非实测 ⇒ 预算冻结可能过严 | 调高 CAPACITY_PER_WEEK 或把 `frozen` 降级为纯标记（本批本就是纯标记）；灰度期不丢任何入队请求 ⇒ 回滚成本为零 |
| A2 | 等待天数用位置代理（无时间戳）⇒ 靠前项被过度老化 | 把代理换成真实到达时间戳（需队列写入方补字段）或调高 AGING_DAYS |
| A2 | 半饱和 50% 线是设计值 | 调 HALF_SATURATION_PCT；或 `--report` 只看不采信（灰度） |
| A3 | 盲化降低人审吞吐（审者失去 AI 提示） | 只对**新开单**生效 ⇒ 停止新开 ITEM_BLIND 单即可回到旧流程；已开单可 `reveal_after_human()` 立即揭盲 |
| A3 | 协议级盲化非密码学承诺（载荷仍在内存） | 真实盲性需前端 + 流程纪律（交人项）；本批不接管前端 |
| A3 | 分歧率无历史基线 ⇒ 新开单样本少时不可解读 | 无已揭盲条时返回 **None**（不编造）；样本充足后再解读 |
| A4 | 代理初值被当成实测值使用（最危险） | 每个值都带 `is_proxy` 字段 + 报告显式标注；对接方必须判 `is_proxy` 再决定是否采信 |
| A4 | 「未被推翻」被当成「没错」（短窗口必然全未推翻） | 只统计 `total_count`，**不把 0 当作证据**；报告登记「未推翻 ≠ 证明无误」 |
| A4 | 「命中规则」缺失（ledger 无 rule_id）⇒ 归入 `__unattributed__` | 不改判定；把未归属量作为**数据缺口指标**上报（信号而非噪声） |
| A5 | 编码长度是**启发式**（非严格 MDL）⇒ 可能误杀好规则 | 侧车元数据里 `REJECT_*` **保留全部信息**（savings/cost/理由）⇒ 人可直接改判并重新入库；**没有任何规则被删除** |
| A5 | 热力图缺失被判必 reject ⇒ 可能扼杀新方向 | 先在沙箱跑攻击补齐热力图，再重提；或人工豁免（本批不自动化） |
| A5 | 豁免率阈值 0.30 是启发式 | 阈值是单一常量 `EXEMPT_RATE_THRESHOLD`，改动一行 + 重跑报告即可 |

## 诚实登记

1. **联调通过 ≠ 保护器有效**（§十.1）：本模块只证明「灰度期零副作用 + 标记可叠加 + 可回滚」，**不证明**拦截后更安全；有效性需 643+ 真实运行数据；
2. **零漂移的强度**：指纹覆盖 5 个 CORE_TOOLS 字节 + 452 判决账本 + 权威日志 + 人审队列 + verified 卡清单；**未覆盖**受控目录全量（那是 642 门禁的另一项）；
3. **A2/A3/A5 的「触发」多数是标记量**，不是被拦截量（灰度期不拦截）；
4. **A5 候选是合成**（本批无真实新规则提案）；
5. 本批**未启用任何 block**：A1 的 block 模式显式未实现（留 643）。
