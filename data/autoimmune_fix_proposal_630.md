# 630 A2 · 自身免疫率口径修复方案（两案对比，**不执行**）

> 工具：`tools/autoimmune_fix_proposal_630.py`（只读；不修改任何卡、不改规则）
> 输入：A1 诊断的 **132 条**口径级 warn（23 张卡）

## 一、方案甲：补字段

- 可自动推断（`auto`）：**42 条**；需人填（`human`）：**90 条**
- **填完即可完全干净的卡**（该卡所有条目都 auto）：**0 张**
- 需人审批量处理：**是**（任务书 §十.3 的门槛是 5 条，实测 90 条）

| # | 卡 | 命题 | 字段 | 模式 | 建议值 | 依据 |
|---|---|---|---|---|---|---|
| 1 | `ATOM-CONC-FENCE-001` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 2 | `ATOM-CONC-FENCE-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 3 | `ATOM-CONC-FENCE-001` | `prop-2` | `object` | **human** | —（建议 happens-before） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 4 | `ATOM-CONC-FENCE-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Z10spin_plainv"} | 符号 '_Z10spin_plainv' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口 |
| 5 | `ATOM-CONC-LOCK-001` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 6 | `ATOM-CONC-LOCK-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 7 | `ATOM-CONC-LOCK-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 8 | `ATOM-CONC-LOCK-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Z12bench_singlev"} | 符号 '_Z12bench_singlev' 取自本命题引用卡的 artifact_assert（非通用符号，gate  |
| 9 | `ATOM-CONC-RACE-001` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 10 | `ATOM-CONC-RACE-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 11 | `ATOM-CONC-RACE-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 12 | `ATOM-CONC-RACE-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 13 | `ATOM-CONC-RACE-001` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 14 | `ATOM-CONC-RACE-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Z12bench_singlev"} | 符号 '_Z12bench_singlev' 取自本命题引用卡的 artifact_assert（非通用符号，gate  |
| 15 | `ATOM-HIST-AUTOPTR-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 16 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 17 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 18 | `ATOM-HIST-AUTOPTR-001` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 19 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZNSt8auto_ptr"} | 符号 '_ZNSt8auto_ptr' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径 |
| 20 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZNSt8auto_ptr"} | 符号 '_ZNSt8auto_ptr' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径 |
| 21 | `ATOM-HIST-AUTOPTR-001` | `prop-4` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZNSt8auto_ptr"} | 符号 '_ZNSt8auto_ptr' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径 |
| 22 | `ATOM-MEM-ALIGN-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 23 | `ATOM-MEM-ALIGN-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 24 | `ATOM-MEM-ALIGN-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 25 | `ATOM-MEM-ALIGN-001` | `prop-3` | `object` | **human** | —（建议 alignas 与按字节搬运） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 26 | `ATOM-MEM-ALIGN-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "Padded"} | 符号 'Padded' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 27 | `ATOM-MEM-ALIGN-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "Aligned"} | 符号 'Aligned' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 28 | `ATOM-MEM-ALLOC-001` | `prop-4` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 29 | `ATOM-MEM-ALLOC-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 30 | `ATOM-MEM-ALLOC-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 31 | `ATOM-MEM-ALLOC-001` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 32 | `ATOM-MEM-ALLOC-001` | `prop-4` | `object` | **human** | —（建议 allocator） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 33 | `ATOM-MEM-ALLOC-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "allocation only"} | 符号 'allocation only' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口 |
| 34 | `ATOM-MEM-ALLOC-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "arena"} | 符号 'arena' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 35 | `ATOM-MEM-ALLOC-001` | `prop-3` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "monotonic"} | 符号 'monotonic' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 36 | `ATOM-MEM-LEAK-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 37 | `ATOM-MEM-LEAK-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 38 | `ATOM-MEM-LEAK-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 39 | `ATOM-MEM-LEAK-001` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 40 | `ATOM-MEM-LEAK-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed after scope="} | 符号 'destroyed after scope=' 取自本命题引用卡的 artifact_assert（非通用符号， |
| 41 | `ATOM-MEM-LEAK-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed after scope="} | 符号 'destroyed after scope=' 取自本命题引用卡的 artifact_assert（非通用符号， |
| 42 | `ATOM-MEM-MOVE-002` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 43 | `ATOM-MEM-MOVE-002` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 44 | `ATOM-MEM-MOVE-002` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 45 | `ATOM-MEM-MOVE-002` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 46 | `ATOM-MEM-MOVE-002` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZL8g_allocs"} | 符号 '_ZL8g_allocs' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定 |
| 47 | `ATOM-MEM-MOVE-002` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZL8g_allocs"} | 符号 '_ZL8g_allocs' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定 |
| 48 | `ATOM-MEM-NEW-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 49 | `ATOM-MEM-NEW-001` | `prop-1` | `object` | **human** | —（建议 new / delete 表达式） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 50 | `ATOM-MEM-NEW-001` | `prop-2` | `object` | **human** | —（建议 new[] / delete[] 混用） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 51 | `ATOM-MEM-NEW-001` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 52 | `ATOM-MEM-NEW-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Znwm"} | 符号 '_Znwm' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 53 | `ATOM-MEM-NEW-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Znay"} | 符号 '_Znay' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 54 | `ATOM-MEM-PERF-001` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 55 | `ATOM-MEM-PERF-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 56 | `ATOM-MEM-PERF-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 57 | `ATOM-MEM-PERF-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Znay"} | 符号 '_Znay' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 58 | `ATOM-MEM-PERF-002` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 59 | `ATOM-MEM-PERF-002` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 60 | `ATOM-MEM-PERF-002` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 61 | `ATOM-MEM-PERF-002` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "max_zero_alloc_len"} | 符号 'max_zero_alloc_len' 取自本命题引用卡的 artifact_assert（非通用符号，gate |
| 62 | `ATOM-MEM-PERF-003` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 63 | `ATOM-MEM-PERF-003` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 64 | `ATOM-MEM-PERF-003` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 65 | `ATOM-MEM-PERF-003` | `prop-2` | `object` | **human** | —（建议 libstdc++ 侧的 string 布局） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 66 | `ATOM-MEM-PERF-003` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 67 | `ATOM-MEM-PERF-003` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "first_heap_len="} | 符号 'first_heap_len=' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口 |
| 68 | `ATOM-MEM-RAII-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 69 | `ATOM-MEM-RAII-001` | `prop-1` | `object` | **human** | —（建议 new / delete 表达式） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 70 | `ATOM-MEM-RAII-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 71 | `ATOM-MEM-RAII-001` | `prop-3` | `object` | **human** | —（建议 作用域内对象的析构顺序） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 72 | `ATOM-MEM-RAII-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "g_live"} | 符号 'g_live' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 73 | `ATOM-MEM-RAII-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "dtor C"} | 符号 'dtor C' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 74 | `ATOM-MEM-RAII-002` | `prop-4` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 75 | `ATOM-MEM-RAII-002` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 76 | `ATOM-MEM-RAII-002` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 77 | `ATOM-MEM-RAII-002` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 78 | `ATOM-MEM-RAII-002` | `prop-4` | `object` | **human** | —（建议 Rule of Zero 的隐式特殊成员） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 79 | `ATOM-MEM-RAII-002` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "rule zero"} | 符号 'rule zero' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 80 | `ATOM-MEM-RAII-002` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "Buggy"} | 符号 'Buggy' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 81 | `ATOM-MEM-RAII-002` | `prop-3` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "relocation"} | 符号 'relocation' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 82 | `ATOM-MEM-RVREF-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 83 | `ATOM-MEM-RVREF-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 84 | `ATOM-MEM-RVREF-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 85 | `ATOM-MEM-RVREF-001` | `prop-3` | `object` | **human** | —（建议 std::move 的作用） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 86 | `ATOM-MEM-RVREF-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZN5Probe6copiesE"} | 符号 '_ZN5Probe6copiesE' 取自本命题引用卡的 artifact_assert（非通用符号，gate  |
| 87 | `ATOM-MEM-RVREF-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_ZN5Probe6copiesE"} | 符号 '_ZN5Probe6copiesE' 取自本命题引用卡的 artifact_assert（非通用符号，gate  |
| 88 | `ATOM-MEM-SHARED-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 89 | `ATOM-MEM-SHARED-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 90 | `ATOM-MEM-SHARED-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 91 | `ATOM-MEM-SHARED-001` | `prop-3` | `object` | **human** | —（建议 shared_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 92 | `ATOM-MEM-SHARED-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed"} | 符号 'destroyed' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 93 | `ATOM-MEM-SHARED-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed"} | 符号 'destroyed' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 94 | `ATOM-MEM-SHARED-002` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 95 | `ATOM-MEM-SHARED-002` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 96 | `ATOM-MEM-SHARED-002` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 97 | `ATOM-MEM-SHARED-002` | `prop-3` | `object` | **human** | —（建议 shared_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 98 | `ATOM-MEM-SHARED-002` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv"} | 符号 '_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_rele |
| 99 | `ATOM-MEM-SHARED-002` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv"} | 符号 '_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_rele |
| 100 | `ATOM-MEM-UNIQUE-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 101 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 102 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 103 | `ATOM-MEM-UNIQUE-001` | `prop-3` | `object` | **human** | —（建议 shared_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 104 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "unique_ptr"} | 符号 'unique_ptr' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 105 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed"} | 符号 'destroyed' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 106 | `ATOM-MEM-UNIQUE-002` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 107 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 108 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 109 | `ATOM-MEM-UNIQUE-002` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 110 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "unique_ptrIi12StatelessDelE"} | 符号 'unique_ptrIi12StatelessDelE' 取自本命题引用卡的 artifact_assert（非 |
| 111 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "Sp_counted_deleterIPi6TagDel"} | 符号 'Sp_counted_deleterIPi6TagDel' 取自本命题引用卡的 artifact_assert（ |
| 112 | `ATOM-MEM-VALUE-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 113 | `ATOM-MEM-VALUE-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 114 | `ATOM-MEM-VALUE-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 115 | `ATOM-MEM-VALUE-001` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 116 | `ATOM-MEM-VALUE-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "xvalue"} | 符号 'xvalue' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 117 | `ATOM-MEM-VALUE-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "xvalue"} | 符号 'xvalue' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 118 | `ATOM-MEM-VALUE-002` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 119 | `ATOM-MEM-VALUE-002` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 120 | `ATOM-MEM-VALUE-002` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 121 | `ATOM-MEM-VALUE-002` | `prop-3` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 122 | `ATOM-MEM-VALUE-002` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "sink_lvalue"} | 符号 'sink_lvalue' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 123 | `ATOM-MEM-VALUE-002` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "wrap_forward"} | 符号 'wrap_forward' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定 |
| 124 | `ATOM-MEM-WEAK-001` | `prop-3` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 125 | `ATOM-MEM-WEAK-001` | `prop-1` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 126 | `ATOM-MEM-WEAK-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 127 | `ATOM-MEM-WEAK-001` | `prop-3` | `object` | **human** | —（建议 shared_ptr 的删除器） | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 128 | `ATOM-MEM-WEAK-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed"} | 符号 'destroyed' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 129 | `ATOM-MEM-WEAK-001` | `prop-2` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "destroyed"} | 符号 'destroyed' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |
| 130 | `ATOM-UB-GRAY-001` | `prop-2` | `signed_by` | **human** | "human:<在册实名>" | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 131 | `ATOM-UB-GRAY-001` | `prop-2` | `object` | **human** | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选则应改 claim_type 或补概念条 |
| 132 | `ATOM-UB-GRAY-001` | `prop-1` | `liveness` | **auto** | {"kind": "fixture_symbol", "symbol": "_Z1gv"} | 符号 '_Z1gv' 取自本命题引用卡的 artifact_assert（非通用符号，gate 同口径判定） |

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
| scope | 132 条字段（23 张卡） | 3 条规则 |
| files_touched | 23 张原子卡（受控目录！） | `tools/gate_engine.py`（CORE_TOOLS，单个文件） |
| reversible | 可逆（每张卡改动可单独回滚；建议改动前备份 + 逐卡 commit） | 可逆但需重钉尺子（tool_integrity --update） |
| audit | 好（逐卡 diff 可审；可进 ReviewItemLedger 留痕） | 中（规则 diff 可审，但「为何老卡豁免」的语义落在代码里） |
| debt | 偿付（债消失，不是掩盖） | 固化（债不再报，但字段仍缺） |
| risk | 中——90 条需人填（>5 ⇒ §十.3 需人审批量处理）；改受控目录需遵守 §零.6 并逐条人审 | 高——命题级放权闸在存量上失效；且 gate 规则数/命中数变化会牵动 191/67 等冻结数字；且会改变 gate 冻结数字（191/67）⇒ 需重新建立基线 |
| gate_numbers | 不变（不动规则 ⇒ 191/67 等冻结数字不动） | **变化**（命中数下降 ⇒ §一 baseline 与多批冻结断言要跟着改） |

## 四、推荐：**方案甲**（附前置条件）

理由（三条，按权重）：

1. **不动 gate 冻结数字**：乙会改变命中数 191/67，牵动 §一 baseline 与**多批已冻结的断言**（627/629 的测试都用这些数字）⇒ 成本外溢到测试债；
2. **乙的收益是假的**：老卡字段仍缺，只是不再报；「命题级放权」在存量上失效，而放权闸正是 526 的核心防线；
3. **甲可审计、可回滚、可分批**：逐卡 diff + 逐卡 commit，进 ReviewItemLedger 留痕。

**前置条件（必须人做）**：

- 90 条需人填（>5 ⇒ 触发 §十.3「需人审批量处理」）；其中 `signed_by` **只能由在册人签**（机器代签 = 违反 §零.3，且签错会从 warn 升 block）；
- 修改受控目录 `atoms/` 需遵守人工授权流程（本批**不执行**）；
- 若人选择乙，必须同时处理「gate 数字变化 ⇒ 多批测试断言同步更新」的连带债。

## 五、诚实登记

- `suggest`（object 的相似候选）是**机械相似度**（difflib，cutoff 0.3），**不是语义判断**，仅供人参考；
- 本工具**没有**执行任何修复：atoms/ 零改动（自检断言 `git diff --quiet -- atoms`）；
- 方案乙的 blast radius 是**基于源码结构**的静态判断，未实际改动规则做验证。
