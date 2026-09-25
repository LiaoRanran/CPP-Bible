# 627 开工基线台账（Authority V2 收尾启用 + 626 技术债清算）

> 前置：626 已完成 17/17（HEAD `4f2c976c`，未 push）
> 本批定位：**清债 → 对齐 → 验证 → 可安全启用**（不是新功能批）

---

## 一、4 个技术债的当前状态（已量化）

### 债务 1：W2 投影粒度偏差（**P0**）

| 项 | 值 |
|---|---|
| 位置 | `tools/authority_projection_compiler_626.py` 的 `compile_w2()` |
| 现状 | 以 **`edge_id`** 为节点 ⇒ **519 节点**（IN 484 / OUT 35 / UNDEC 0） |
| 基准 | `data/grounded_labels_w2.json`：以 `prop_id + MIS_id` 为节点 ⇒ **121 节点**（IN 114 / OUT 7 / UNDEC 0） |
| 影响 | 无法对比「V2 投影 vs 旧逻辑」⇒ feature flag 切换没有验证基准 |
| 修复方案 | 新建 `w2_projection_normalizer_627.py`，归一化到 121 节点 |

**627 任务0 阶段已探明的根因与解法（实测）**：
1. 节点宇宙可完美归一：Authority 的 452 条边事件中，**所有 target 都在 121 节点内（0 例外）**，
   所有 source 也都在 121 节点内 ⇒ 归一化不会产生孤立节点。
2. W2 语义是 **`W2_credibility_weighted_grounded`**（`weighted_af_solver.py`）：
   击败关系 `(A,B)` 成立 ⇔ `cred(A) > cred(B)`（**严格大于**）。
3. **626 的关键缺陷**：只把 `result=APPROVE` 当作生效攻击。实测发现
   **7 个 OUT 的 MIS 节点（cred=1）恰恰是被 `result=MODIFY` 的边攻击的**
   （如 `ae-ATOM-LANG-INLINE-001::prop-1->MIS-LANG-001` = MODIFY）。
4. **修正后实测（任务0 预演）**：以 `APPROVE ∪ MODIFY` 为生效攻击 ⇒
   388 条活跃边、17 条击败 ⇒ **IN 114 / OUT 7 / UNDEC 0，与 grounded_labels 逐节点 diff = 0** ✅

### 债务 2：51 条旧式 supersedes 引用（**P0**）

| 类型 | 数量 | 示例 |
|---|---|---|
| `legacy:pre_annotation:*` | **34** | `legacy:pre_annotation:ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1` |
| `dec-0001xx` | **17** | `dec-000178` … `dec-000194` |
| 有效 v2 `event_id` | **0** | — |
| 合计 | **51**（对应 51 条 REPLACE event） | |

- 影响：哈希链的 `supersedes` 指向断裂 ⇒ Authority Ledger 可追溯性半残
- 修复方案：新建 `supersedes_remapper_627.py`，建立旧式 ID → v2 event_id 映射，
  生成 **新文件** `decision_event_v2_ledger_remapped.jsonl`（**原 ledger 保留**）

### 债务 3：56 张 PCK evidence.hash 漂移（**P1**）

- 83 张 PCK 中 **56 张**的 `evidence.hash` 与当前文件重算 SHA-256 不一致
- 影响：B2-R（referential integrity）永远 27/83 pass
- 修复方案：新建 `pck_hash_drift_analyzer_627.py`，分类为 A/B/C/D 四类漂移，
  **只分析 + 给处置建议，不执行**

### 债务 4：feature flag 从未端到端验证（**P0**）

- `QUEYI_AUTHORITY_V2` 在 626 D1 定义，但**从未真跑通过**
- 5 种投影（W2/PCK/golden/dashboard/textbook）在 V2 模式下是否正常工作、是否与旧逻辑一致、是否性能回退 —— 全部未知
- 修复方案：新建 `authority_v2_e2e_627.py`，在**子进程**中切换环境变量做 V1/V2 对比

## 二、9 条交人项的当前状态

| # | 交人项 | 627 可否自动处理 | 说明 |
|---|---|---|---|
| 1 | 是否启用 `QUEYI_AUTHORITY_V2=1` | **部分** | 627 做端到端验证 + 一键启用脚本；**启用动作仍需人确认** |
| 2 | 是否执行真实 Blind Review | **否** | C1 只准备执行包，C2 只实现回填工具；**执行需人审者** |
| 3 | 是否 push 625+626+627 | **否** | D1 只做 push 前检查；**push 需人授权** |
| 4 | 数据迁移是否最终确认 | **否** | 旧 annotations/authority_log 废弃属治理决定，需人 |
| 5 | W2 三态是否正式启用 | **否** | 替换现有单一 IN/OUT 状态属架构决定，需人 |
| 6 | 56 处 PCK hash 漂移如何处置 | **否（但可自动分类）** | A3 给出逐张建议；**处置需人裁决** |
| 7 | Snapshot CI 局限是否立项 | **否** | 立项需人 |
| 8 | 镜像边 symmetry_proof 是否人审验证 | **部分** | A4 自动验证对称性并分类；**写入需人确认** |
| 9 | 51 条旧式 supersedes 是否做 ID 重映射 | **是（A2）** | 627 自动生成 remapped ledger（原文件保留） |

**小结**：9 条中 **1 条可全自动（#9）**、**3 条可自动准备/部分处理（#1/#6/#8）**、**5 条必须人裁决**。

## 三、feature flag 切换前基线快照（用于 B 线对比）

| 维度 | 基线值 | 来源 |
|---|---|---|
| gate 规则数 | **67 / 191**（block=0） | 任务书基线（626 后） |
| poison | **124 / 124**（95.5%） | 任务书基线 |
| replay | **56 / 0 / 0** | 任务书基线 |
| commits | ~1671 | 任务书基线 |
| tools / tests | ~292 / ~326 | 任务书基线 |
| DecisionEvent v2 ledger | **452** 条 | 实测 |
| review_method | BATCH_AUTH 228 / MIRROR_DERIVED 194 / ITEM_OPEN 30 | 实测 |
| decision_origin | human_observed 228 / mirror_projection 194 / user_authorized_execution 30 | 实测 |
| result 分布 | APPROVE 367 / MODIFY 85 | 实测 |
| operation 分布 | CREATE 401 / REPLACE 51 | 实测 |
| **独立人类确认强度** | **0** | 实测 |
| 唯一审查账本 | **93 unique / 110 record** | 实测 |
| W2 投影（626） | 519 节点 | 实测 |
| grounded_labels | 121 节点（IN114/OUT7） | 实测 |
| PCK hash 不匹配 | **56 / 83** | 实测 |

> 注：**本批不跑监工门禁**（gate/poison/replay/tool_integrity --check），
> 上述 gate/poison/replay 数字取自 626 验收基线，作为 V2 切换后的对比基准。

## 四、CORE_TOOLS 改造点评估

**结论：627 不需要改任何 CORE_TOOLS 的生产逻辑。**

| CORE_TOOLS | 是否需改造 | 理由 |
|---|---|---|
| `gate_engine.py` | 否 | V2 投影是新增工具，不替换现有 W2；判据 9 明确不改其 W2 计算逻辑 |
| `atom_evidence_replay.py` | 否 | replay 判决不受投影层影响 |
| `poison_drill.py` | 否 | 同上 |
| `toolchain.py` | 否 | 同上 |
| `cppbible.py` | 否 | 同上 |

**V2 切换机制**：只在新增工具中通过 `QUEYI_AUTHORITY_V2` 环境变量实现；
回滚 = 设 `QUEYI_AUTHORITY_V2=0`。B2 将用**静态分析**确认 CORE_TOOLS 代码中不读取该 flag。

## 五、本批约束确认

- 不跑监工门禁 · 不 push · 不 golden accept · 不打开 delegation · 不代签人审
- 不修改 `atoms/ / evidence/ / Examples/ / Book/` 受控目录
- 不删除历史报告（只标 STALE）· 不删除/修改原始 JSONL（append-only）
- 不执行真实 Blind Review · 不默认启用 V2 关键路径
- **不修改 626 的工具文件**（A1-A4、B1-B3 全部新建 `*_627.py`）


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true


## 635 V26-2 系统误差二分（不可合并为单一健康分）

**可收敛指标**（加样本可改善）：
- 逃逸率：多测 mutation 可更准确估计漏报率（统计量）
- τ_d（逃逸→修补间隔）：样本量增加可收紧分位数
- 接地覆盖率：可补实验把「部分/未接地」转「已接地」
- 工具数/测试数：持续增加

**不可收敛指标**（加样本无效，须换方法）：
- coverage 缺口：剩下的是**没测过的攻击面**，不是测不准
- 自身免疫率：是**规则设计问题**，不是样本问题
- Horizon 断崖（60-80 桶）：是**载体天花板**，不是样本量
- N/A 率：主因是载体无法施加（634 B3），加样本无效
- gate 规则数：是**设计选择**，非估计量
