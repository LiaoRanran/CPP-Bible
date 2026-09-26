# 630 A2 · 自身免疫率口径修复方案（两案对比，**不执行**）

> 工具：`tools/autoimmune_fix_proposal_630.py`（只读；不修改任何卡、不改规则）
> 输入：A1 诊断的 **65 条**口径级 warn（23 张卡）

## 一、方案甲：补字段

- 可自动推断（`auto`）：**0 条**；需人填（`human`）：**65 条**
- **填完即可完全干净的卡**（该卡所有条目都 auto）：**0 张**
- 需人审批量处理：**是**（任务书 §十.3 的门槛是 5 条，实测 65 条）

| # | 卡 | 命题 | 字段 | 模式 | 建议值 | 依据 |
|---|---|---|---|---|---|---|
| 1 | `ATOM-CONC-FENCE-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 2 | `ATOM-CONC-FENCE-001` | `prop-2` | `object` | **human** | —（建议 happens-before） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 3 | `ATOM-CONC-LOCK-001` | `prop-1` | `object` | **human** | —（建议 std::move 的性能收益） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 4 | `ATOM-CONC-LOCK-001` | `prop-2` | `object` | **human** | —（建议 std::move 的性能收益） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 5 | `ATOM-CONC-RACE-001` | `prop-1` | `object` | **human** | —（建议 数据竞争） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 6 | `ATOM-CONC-RACE-001` | `prop-2` | `object` | **human** | —（建议 数据竞争） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 7 | `ATOM-CONC-RACE-001` | `prop-3` | `object` | **human** | —（建议 数据竞争） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 8 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `object` | **human** | —（建议 auto_ptr 的历史定位） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 9 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `object` | **human** | —（建议 auto_ptr 的历史定位） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 10 | `ATOM-HIST-AUTOPTR-001` | `prop-3` | `object` | **human** | —（建议 auto_ptr 的历史定位） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 11 | `ATOM-MEM-ALIGN-001` | `prop-1` | `object` | **human** | —（建议 内存序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 12 | `ATOM-MEM-ALIGN-001` | `prop-2` | `object` | **human** | —（建议 内存序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 13 | `ATOM-MEM-ALIGN-001` | `prop-3` | `object` | **human** | —（建议 未测序修改与严格别名） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 14 | `ATOM-MEM-ALLOC-001` | `prop-1` | `object` | **human** | —（建议 allocator） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 15 | `ATOM-MEM-ALLOC-001` | `prop-2` | `object` | **human** | —（建议 allocator） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 16 | `ATOM-MEM-ALLOC-001` | `prop-3` | `object` | **human** | —（建议 allocator） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 17 | `ATOM-MEM-ALLOC-001` | `prop-4` | `object` | **human** | —（建议 allocator） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 18 | `ATOM-MEM-LEAK-001` | `prop-1` | `object` | **human** | —（建议 内存序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 19 | `ATOM-MEM-LEAK-001` | `prop-2` | `object` | **human** | —（建议 内存序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 20 | `ATOM-MEM-LEAK-001` | `prop-3` | `object` | **human** | —（建议 内存序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 21 | `ATOM-MEM-MOVE-002` | `prop-1` | `object` | **human** | —（建议 移动转移与析构次数） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 22 | `ATOM-MEM-MOVE-002` | `prop-2` | `object` | **human** | —（建议 移动转移与析构次数） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 23 | `ATOM-MEM-MOVE-002` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 24 | `ATOM-MEM-NEW-001` | `prop-1` | `object` | **human** | —（建议 new / delete 表达式） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 25 | `ATOM-MEM-NEW-001` | `prop-2` | `object` | **human** | —（建议 new / delete 表达式） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 26 | `ATOM-MEM-NEW-001` | `prop-3` | `object` | **human** | —（建议 new / delete 表达式） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 27 | `ATOM-MEM-PERF-001` | `prop-1` | `object` | **human** | —（建议 小对象分配策略的快慢） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 28 | `ATOM-MEM-PERF-001` | `prop-2` | `object` | **human** | —（建议 小对象分配策略的快慢） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 29 | `ATOM-MEM-PERF-002` | `prop-1` | `object` | **human** | —（建议 libstdc++ 侧的 string 布局） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 30 | `ATOM-MEM-PERF-002` | `prop-2` | `object` | **human** | —（建议 libstdc++ 侧的 string 布局） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 31 | `ATOM-MEM-PERF-003` | `prop-1` | `object` | **human** | —（建议 libstdc++ 侧的 string 布局） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 32 | `ATOM-MEM-PERF-003` | `prop-2` | `object` | **human** | —（建议 libstdc++ 侧的 string 布局） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 33 | `ATOM-MEM-PERF-003` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 34 | `ATOM-MEM-RAII-001` | `prop-1` | `object` | **human** | —（建议 RAII 的异常安全性） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 35 | `ATOM-MEM-RAII-001` | `prop-2` | `object` | **human** | —（建议 作用域内对象的析构顺序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 36 | `ATOM-MEM-RAII-001` | `prop-3` | `object` | **human** | —（建议 RAII 的异常安全性） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 37 | `ATOM-MEM-RAII-002` | `prop-1` | `object` | **human** | —（建议 Rule of Zero 的隐式特殊成员） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 38 | `ATOM-MEM-RAII-002` | `prop-2` | `object` | **human** | —（建议 特殊成员函数的取舍） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 39 | `ATOM-MEM-RAII-002` | `prop-3` | `object` | **human** | —（建议 移动构造的 noexcept） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 40 | `ATOM-MEM-RAII-002` | `prop-4` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 41 | `ATOM-MEM-RVREF-001` | `prop-1` | `object` | **human** | —（建议 std::move 的作用） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 42 | `ATOM-MEM-RVREF-001` | `prop-2` | `object` | **human** | —（建议 std::move 的作用） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 43 | `ATOM-MEM-RVREF-001` | `prop-3` | `object` | **human** | —（建议 std::move 的作用） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 44 | `ATOM-MEM-SHARED-001` | `prop-1` | `object` | **human** | —（建议 shared_ptr 的引用计数与析构） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 45 | `ATOM-MEM-SHARED-001` | `prop-2` | `object` | **human** | —（建议 shared_ptr 的引用计数与析构） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 46 | `ATOM-MEM-SHARED-001` | `prop-3` | `object` | **human** | —（建议 shared_ptr 的引用计数与析构） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 47 | `ATOM-MEM-SHARED-002` | `prop-1` | `object` | **human** | —（建议 shared_ptr 的引用计数与析构） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 48 | `ATOM-MEM-SHARED-002` | `prop-2` | `object` | **human** | —（建议 shared_ptr 的引用计数与析构） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 49 | `ATOM-MEM-SHARED-002` | `prop-3` | `object` | **human** | —（建议 shared_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 50 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `object` | **human** | —（建议 unique_ptr 的大小） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 51 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `object` | **human** | —（建议 unique_ptr 的所有权语义） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 52 | `ATOM-MEM-UNIQUE-001` | `prop-3` | `object` | **human** | —（建议 unique_ptr 的所有权语义） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 53 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `object` | **human** | —（建议 unique_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 54 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `object` | **human** | —（建议 unique_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 55 | `ATOM-MEM-UNIQUE-002` | `prop-3` | `object` | **human** | —（建议 unique_ptr 的大小） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 56 | `ATOM-MEM-VALUE-001` | `prop-1` | `object` | **human** | —（建议 从 xvalue 移动后的源与目标） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 57 | `ATOM-MEM-VALUE-001` | `prop-2` | `object` | **human** | —（建议 移动收益的有无） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 58 | `ATOM-MEM-VALUE-001` | `prop-3` | `object` | **human** | —（建议 从 xvalue 移动后的源与目标） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 59 | `ATOM-MEM-VALUE-002` | `prop-1` | `object` | **human** | —（建议 转发链里有无 std::forward） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 60 | `ATOM-MEM-VALUE-002` | `prop-2` | `object` | **human** | —（建议 转发链里有无 std::forward） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 61 | `ATOM-MEM-VALUE-002` | `prop-3` | `object` | **human** | —（建议 转发链里有无 std::forward） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 62 | `ATOM-MEM-WEAK-001` | `prop-1` | `object` | **human** | —（建议 weak_ptr 的语义） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 63 | `ATOM-MEM-WEAK-001` | `prop-2` | `object` | **human** | —（建议 weak_ptr 的语义） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 64 | `ATOM-MEM-WEAK-001` | `prop-3` | `object` | **human** | —（建议 weak_ptr 的语义） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 65 | `ATOM-UB-GRAY-001` | `prop-2` | `object` | **human** | —（建议 函数实参的求值顺序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |

## 二、方案乙：调规则

| 规则 | 改法 | blast radius | 风险 |
|---|---|---|---|
| `OBSERVATION-LIVENESS` | 给老卡加豁免分支：`created_at` 早于规则引入批次（530/575）的卡只 `advice` 不 `warn` | 改 `gate_engine.py`（CORE_TOOLS）⇒ 必须同 commit 跑 tool_integrity --update；覆盖全库 27 张原子卡 + 未来所有卡（豁免条件一旦按卡龄写死，会长期生效） | 高——命题级放权闸在存量上失效；且 gate 规则数/命中数变化会牵动 191/67 等冻结数字 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 放宽判据：object 只要**短于 N 字**即视为概念短语（不查规范集） | 改 CORE_TOOLS；全库所有 claim 命题；会同时放行真正不合规的 object | 中高——等于把「能否与图谱连通」的检查降级为长度检查 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | 把卡级签署兜底从 warn 降为 advice（进一步放宽） | 改 CORE_TOOLS；全库所有 inference 命题 | 高——这是 526 的「核心放权闸」，降级会让「机器不能替 inference 背书」这条铁线失效 |

- **CORE_TOOLS 铁律提醒**：方案乙必然修改 `tools/gate_engine.py` ⇒ 按 §零.7必须同 commit 跑 `tool_integrity.py --update` 重钉尺子。

## 三、两案对比

| 维度 | 方案甲（补字段） | 方案乙（调规则） |
|---|---|---|
| scope | 65 条字段（23 张卡） | 3 条规则 |
| files_touched | 23 张原子卡（受控目录！） | `tools/gate_engine.py`（CORE_TOOLS，单个文件） |
| reversible | 可逆（每张卡改动可单独回滚；建议改动前备份 + 逐卡 commit） | 可逆但需重钉尺子（tool_integrity --update） |
| audit | 好（逐卡 diff 可审；可进 ReviewItemLedger 留痕） | 中（规则 diff 可审，但「为何老卡豁免」的语义落在代码里） |
| debt | 偿付（债消失，不是掩盖） | 固化（债不再报，但字段仍缺） |
| risk | 中——65 条需人填（>5 ⇒ §十.3 需人审批量处理）；改受控目录需遵守 §零.6 并逐条人审 | 高——命题级放权闸在存量上失效；且 gate 规则数/命中数变化会牵动 191/67 等冻结数字；且会改变 gate 冻结数字（191/67）⇒ 需重新建立基线 |
| gate_numbers | 不变（不动规则 ⇒ 191/67 等冻结数字不动） | **变化**（命中数下降 ⇒ §一 baseline 与多批冻结断言要跟着改） |

## 四、推荐：**方案甲**（附前置条件）

理由（三条，按权重）：

1. **不动 gate 冻结数字**：乙会改变命中数 191/67，牵动 §一 baseline 与**多批已冻结的断言**（627/629 的测试都用这些数字）⇒ 成本外溢到测试债；
2. **乙的收益是假的**：老卡字段仍缺，只是不再报；「命题级放权」在存量上失效，而放权闸正是 526 的核心防线；
3. **甲可审计、可回滚、可分批**：逐卡 diff + 逐卡 commit，进 ReviewItemLedger 留痕。

**前置条件（必须人做）**：

- 65 条需人填（>5 ⇒ 触发 §十.3「需人审批量处理」）；其中 `signed_by` **只能由在册人签**（机器代签 = 违反 §零.3，且签错会从 warn 升 block）；
- 修改受控目录 `atoms/` 需遵守人工授权流程（本批**不执行**）；
- 若人选择乙，必须同时处理「gate 数字变化 ⇒ 多批测试断言同步更新」的连带债。

## 五、诚实登记

- `suggest`（object 的相似候选）是**机械相似度**（difflib，cutoff 0.3），**不是语义判断**，仅供人参考；
- 本工具**没有**执行任何修复：atoms/ 零改动（自检断言 `git diff --quiet -- atoms`）；
- 方案乙的 blast radius 是**基于源码结构**的静态判断，未实际改动规则做验证。
