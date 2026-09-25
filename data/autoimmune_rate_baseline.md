# 629 A1 · 自身免疫率基线（误报度量，v22 唯一净新增范式输入）

> 工具：`tools/autoimmune_rate_framework.py`（纯标准库，只读；只读 `import gate_engine` → `run()`，**不跑 `--check` 全量入口**）
> 干净卡口径：主口径 `status ∈ ['verified']`；扩展口径 `['verified', 'red-team-verified']`

## 一、定义与操作化

- **自身免疫事件** = 一张**已知正确**的卡被 gate 标 `warn`/`block`（= 免疫系统攻击自身好细胞）。
- **自身免疫率** = 被 warn/block 的干净卡数 ÷ 干净卡总数（本工具主指标）。
- 与**逃逸率**（漏报）对偶：逃逸率怕漏放坏卡，自身免疫率怕误杀好卡。两者是 gate 的两向错误，必须同时盯——只压逃逸率会把 gate 调得越来越疑神疑鬼。

## 二、干净卡集（只读实测）

- 主口径干净卡：**23 张**（任务书写 28 张；实测 27 张卡中 verified 23 张，差异见 `data/629_baseline.md`）
- 扩展口径（含 red-team-verified）：**26 张**

| 卡 ID | status | warn 规则 | block | advice |
|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-CONC-LOCK-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-CONC-RACE-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED`, `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-HIST-AUTOPTR-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-ALIGN-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-ALLOC-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-LEAK-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-MOVE-002` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-NEW-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-PERF-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-PERF-002` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-PERF-003` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED`, `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-RAII-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-RAII-002` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-RVREF-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-SHARED-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-SHARED-002` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-UNIQUE-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-UNIQUE-002` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-VALUE-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-VALUE-002` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-MEM-WEAK-001` | verified | `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |
| `ATOM-UB-GRAY-001` | verified | `ATOM-REL-TARGET`, `ATOM-REL-TARGET`, `ATOM-CLAIM-CONCEPT-NORMALIZED` | `INFERENCE-NOT-MACHINE-VERIFIED` | — |

## 三、自身免疫率

| 口径 | 干净卡 | 被 warn/block | 自身免疫率 |
|---|---|---|---|
| 主口径 status=verified | 23 | 23 | **100.0%** |
| 扩展口径 +red-team-verified | 26 | 26 | **100.0%** |

- warn 事件 67 次 · block 事件 25 次 · advice 0 次（advice 不计自身免疫）
- warn 规则命中分布：`ATOM-CLAIM-CONCEPT-NORMALIZED`×65、`ATOM-REL-TARGET`×2

## 四、与逃逸率并列（gate 的两向错误）

| 方向 | 指标 | 值 | 来源 |
|---|---|---|---|
| 漏报 | 逃逸率 | 1/1406（CS anytime 上界 0.9062%） | §一 standing baseline（616 修正） |
| 误报 | 自身免疫率 | 100.0%（23/23） | 本工具实测 |

## 五、关键诚实结论：自身免疫率 = 100%（23/23 张已验证卡被 warn）

这个数字**不能直接读成「gate 100% 误杀」**，也不能读成「23 张卡全有问题」。按 warn 规则的性质分桶后：

| 桶 | 判据 | 卡数 | 占干净卡比 | 解读 |
|---|---|---|---|---|
| 硬缺陷（真阳性嫌疑） | 命中 `ATOM-REL-TARGET`/`ATOM-STATUS-TRANSITION`/`EV-MATRIX-UNBACKED` | 1 | 4.3% | 引用/结构性问题 ⇒ **卡本身待修**，不是 gate 过敏 |
| 命题级口径（自身免疫嫌疑） | 仅命中 `ATOM-CLAIM-CONCEPT-NORMALIZED`/`INFERENCE-NOT-MACHINE-VERIFIED`/`OBSERVATION-LIVENESS` | 22 | 95.7% | 卡级已合格，规则要求**命题级**字段 ⇒ **规则口径对老卡过严**（自身免疫） |

- 硬缺陷卡：['ATOM-UB-GRAY-001']
- 仅口径卡：['ATOM-CONC-FENCE-001', 'ATOM-CONC-LOCK-001', 'ATOM-CONC-RACE-001', 'ATOM-HIST-AUTOPTR-001', 'ATOM-MEM-ALIGN-001', 'ATOM-MEM-ALLOC-001', 'ATOM-MEM-LEAK-001', 'ATOM-MEM-MOVE-002', 'ATOM-MEM-NEW-001', 'ATOM-MEM-PERF-001', 'ATOM-MEM-PERF-002', 'ATOM-MEM-PERF-003', 'ATOM-MEM-RAII-001', 'ATOM-MEM-RAII-002', 'ATOM-MEM-RVREF-001', 'ATOM-MEM-SHARED-001', 'ATOM-MEM-SHARED-002', 'ATOM-MEM-UNIQUE-001', 'ATOM-MEM-UNIQUE-002', 'ATOM-MEM-VALUE-001', 'ATOM-MEM-VALUE-002', 'ATOM-MEM-WEAK-001']

### 三个规则为何在「已验证卡」上几乎必然触发（口径错配根因）

- `OBSERVATION-LIVENESS`：要求**命题级** `liveness` 字段；而 27 张老卡的 observation 命题只挂证据卡 id（卡级活性条件），字段形态早于该规则 ⇒ 必然 warn。
- `ATOM-CLAIM-CONCEPT-NORMALIZED`：要求 `object` 是**规范概念短语**；老卡写的是自然语言句子/数字串 ⇒ 65 次命中里绝大多数是「形态不合规」而非「概念错」。
- `INFERENCE-NOT-MACHINE-VERIFIED`：要求**命题级**机器验证；老卡只有**卡级**人签（status_history 有人签）⇒ 规则自己也承认「视为已签」，只是建议精确到命题。

### 结论（可执行）

1. **warn 层目前不适合当「卡是否合格」的判据**：23/23 已验证卡全 warn ⇒ 该层实际是**TODO 债清单**（列「还差哪些字段」），不是质量评级。
2. 与逃逸率对偶看：gate 在**拦坏卡**方向几乎无漏（逃逸 1/1406 = 0.07%），在**不扰好卡**方向 100% 触发 —— 两个方向的不对称说明 gate 的设计偏向**宁枉勿纵**（可接受，但必须显式承认，且不可用 warn 数当 quality gate）。
3. 需要人审裁决的口径题（本批只登记，不代签）：命题级字段是「新卡必需、老卡豁免」还是「老卡补齐字段」？详见 A3 仪表盘与验收报告交人项。

### 与 A2 探针的关系

A1 度量的是「已验证卡被 warn 多少」（含大量口径错配），A2 用**语义不变的格式微扰动副本**区分「形式过敏」与「内容真问题」，两者互补，见 `data/autoimmune_probe_results.md`。

## 六、局限

- 样本只有 23 张已验证卡（任务书预期 28），比例指标置信区间宽（±1 张 = ±4.3pp），**不足以支撑统计结论**，只能做趋势基线。
- `ge.run()` 是全库求值后按 `target` 过滤（gate 无常量级单卡入口）；跨卡规则（EV-ID-UNIQUE / 关系 / serves / 概念归一）命中已按 `Finding.target` 严格归属，但「跨卡规则只报一条」的聚合特性可能**低估**自身免疫事件数。
- 只覆盖 **gate 规则层**误报；`poison_drill` / `replay` / 编译门误报未纳入（本批不跑监工门禁）。


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
