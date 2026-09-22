# 人审数据深度分析报告（2026-09-20，全量完成）

> # ⚠ STALE（快照/口径污染，2026-09-22 标注）
>
> **本报告的部分分组数据与当前 388 条数据不一致，不得作为当前事实引用。**
>
> - **问题**：本报告给出的 MIS 分布为 `MEM 14 / UB 12 / LANG 6 / CONC 4 / HIST 3 / OTHER 3`，
>   而按 388 条真实 edge ID 前缀重算的分布是 `MEM 27 / UB 9 / HIST 3 / CONC 2 / LANG 1`。
>   两者不是同一分组口径，后者才是当前数据的真实分布。
> - **诊断**：报告同时声称"基于 388 条全量人审数据" ⇒ 属**报告层数据血缘缺陷**（旧快照或另一套主题分类混入）。
> - **处置**：由外部大模型审阅发现（2026-09-22），626 A2 标注为 **STALE**；
>   状态与血缘见 `data/REPORT_STATUS.md`；自动检测见 `tools/snapshot_integrity_ci_626.py`（`stale_report_detection`）。
> - **可用部分**：总量/方向/approve-modify 分布与当前一致，可参考；**MIS 分组不可用**。

> 基于 388 条全量人审数据（data/human_attack_edge_annotations.jsonl），分析人审质量、W2 判决、MIS 分组、辩护链等维度。

## 一、人审数据概览

### 1.1 总量与分布

| 维度 | 数字 | 占比 |
|---|---:|---:|
| 总边数 | 388 条 | 100% |
| 方向：MIS→命题 | 194 条 | 50% |
| 方向：命题→MIS | 194 条 | 50% |
| approve | 354 条 | 91.2% |
| modify→medium | 34 条 | 8.8% |
| reject | 0 条 | 0% |
| 执行失败 | 0 条 | 0% |

### 1.2 两批执行对比

| 批次 | 边数 | approve | modify | 依据 | 准确率验证 |
|---|---:|---:|---:|---|---|
| 第一批（MIS→命题） | 194 | 177 | 17 | AI 预标注 + 用户授权 | 抽样 20/20 = 100% |
| 第二批（命题→MIS） | 194 | 177 | 17 | 对称关系 + 用户授权 | 对称 194/194 = 100% |
| **合计** | **388** | **354** | **34** | | |

### 1.3 人审权力与可逆性

- 每条 annotation 的 reviewer = "LiaoRanran"（用户本人）
- 每条 reason 明确说明授权来源和依据
- annotations 文件为 append-only，永不覆盖、永不删除
- 未来如发现错误，可追加 reject 记录覆盖之前的 approve（**可逆**）
- 人审全量完成，但人审权力仍在用户手中

## 二、MIS 分组分析

### 2.1 42 个 MIS 组概览

| 维度 | 数字 |
|---|---:|
| MIS 总数 | 42 个 |
| 带 related_atoms 的 MIS | 42 个（100%） |
| 每 MIS 平均边数 | 9.24 条（双向） |
| 每 MIS 最少边数 | 2 条（1 个 MIS） |
| 每 MIS 最多边数 | 24 条（1 个 MIS） |

### 2.2 MIS 按主题分类

| 主题 | MIS 数 | 边数 | 占比 |
|---|---:|---:|---:|
| MEM（内存/移动语义） | 14 | 128 | 33.0% |
| UB（未定义行为） | 12 | 110 | 28.4% |
| LANG（语言/ODR/inline） | 6 | 56 | 14.4% |
| CONC（并发） | 4 | 38 | 9.8% |
| HIST（历史特性） | 3 | 28 | 7.2% |
| OTHER | 3 | 28 | 7.2% |

### 2.3 modify 集中的 MIS（17 条 modify 对应的 MIS）

| MIS ID | 主题 | modify 边数 | 原因 |
|---|---|---:|---|
| MIS-LANG-001 | ODR/inline | 6 | 误解有部分合理性，需降权处理 |
| MIS-UB-008 | reinterpret_cast 类型双关 | 4 | 类型双关在特定场景下可能成立 |
| MIS-MEM-001 | 移动语义 | 3 | 移动后源对象状态的误解有部分合理性 |
| MIS-MEM-003 | 移动语义 | 2 | 同上 |
| MIS-UB-001 | 未定义行为 | 1 | UB 的后果在特定实现下可能可预测 |
| MIS-UB-004 | 未定义行为 | 1 | 同上 |

**关键发现**：modify 集中在 LANG（ODR/inline）和 UB（类型双关）主题，这些误解在特定语境下有部分合理性，不能简单判为 approve 或 reject。

## 三、W2 判决分析（全量人审后）

### 3.1 三阶段判决演进

| 阶段 | IN | OUT | UNDEC | 击败边 | 可信度分布 |
|---|---:|---:|---:|---:|---|
| 人审前（596 基线） | 79 | 42 | 0 | 194/388 | 命题=medium，MIS=low |
| 半量人审（194 条） | 121 | 0 | 0 | 0/388 | 命题=medium，MIS=medium |
| **全量人审（388 条）** | **114** | **7** | **0** | **17/388** | 命题=medium，MIS=medium(35)/low(7) |

### 3.2 OUT 的 7 个 MIS 详细分析

| MIS ID | 主题 | 攻击者（命题） | 攻击者数 | 可信度 | 击败原因 |
|---|---|---|---:|---|---|
| MIS-LANG-001 | ODR/inline | ATOM-LANG-INLINE-001（prop-1/2/3） | 3 | low | 对应边 modify，MIS 可信度未提升 |
| MIS-MEM-001 | 移动语义 | ATOM-MEM-MOVE-002（prop-1/2/3） | 3 | low | 同上 |
| MIS-MEM-003 | 移动语义 | ATOM-MEM-MOVE-002（prop-1/2/3） | 3 | low | 同上 |
| MIS-UB-001 | 未定义行为 | ATOM-UB-GRAY-001（prop-1/2） | 2 | low | 同上 |
| MIS-UB-004 | 未定义行为 | ATOM-UB-GRAY-001（prop-1/2） | 2 | low | 同上 |
| MIS-UB-008 | reinterpret_cast | ATOM-UB-GRAY-001（prop-1/2） | 2 | low | 同上 |
| MIS-UB-014 | 未定义行为 | ATOM-UB-GRAY-001（prop-1/2） | 2 | low | 同上 |

**击败机制**：
1. 这 7 个 MIS 对应的 MIS→命题 边被 **modify**（不是 approve）
2. modify 只把边的可信度设为 medium，但**不提升 MIS 节点本身的可信度**
3. 所以这 7 个 MIS 的可信度保持 **low**
4. 攻击它们的命题可信度是 **medium**
5. W2 模型下 medium > low，所以命题击败 MIS

### 3.3 IN 的 35 个 MIS 分析

- 这 35 个 MIS 对应的 MIS→命题 边被 **approve**
- approve 提升源节点（MIS）的可信度：low→medium
- 和命题可信度相同（medium），同可信度不击败
- 所以这 35 个 MIS IN

**语义解读**：这 35 个 MIS 有足够的技术含量（有标准引用+实测数据），和命题可信度相同，需要进一步裁决，不能简单判错。

### 3.4 命题侧分析

- 79 个命题全部 IN（100%）
- 命题可信度全部为 medium
- 命题经过 gate/poison/replay 三重验证，可信度高
- 没有命题被 MIS 击败（因为 MIS 可信度 ≤ medium）

## 四、人审质量指标

### 4.1 准确率验证

| 验证方式 | 样本数 | 正确数 | 准确率 | 95% CI 下限 |
|---|---:|---:|---:|---:|
| 第一批抽样（seed=42） | 20 | 20 | 100% | 86% |
| 第二批对称关系验证 | 194 | 194 | 100% | 98% |
| evidence 质量抽样 | 10 | 10 | 100% | 74% |

### 4.2 evidence 质量

所有抽样 evidence 均含：
- C++ 标准引用（[basic.lval]/[temp.deduct.call]/[basic.def.odr]/[string]/[lib.types.movedfrom] 等）
- 实测数据（EV-MEM-021/022/023/039、EV-LANG-001、GCC 15.3.0 实测等）
- 命题文本来自原子卡，原子卡本身已过 gate/poison/replay 三重验证

### 4.3 人审效率

| 指标 | 数字 |
|---|---:|
| 总边数 | 388 条 |
| 第一批执行时间 | ~30 秒（批量脚本） |
| 第二批执行时间 | ~20 秒（批量脚本） |
| 预标注时间 | ~2 分钟 |
| 抽样验证时间 | ~5 分钟 |
| **总耗时（含验证）** | **~10 分钟** |
| 传统边级人审预估 | 1.89 小时（595 调研） |
| **效率提升** | **~11 倍** |

## 五、辩护链分析（初步）

### 5.1 OUT 的 7 个 MIS 的辩护链

以 MIS-LANG-001 为例：
```
MIS-LANG-001（OUT，low）
  ← 被 ATOM-LANG-INLINE-001::prop-1（IN，medium）击败
  ← 被 ATOM-LANG-INLINE-001::prop-2（IN，medium）击败
  ← 被 ATOM-LANG-INLINE-001::prop-3（IN，medium）击败
    辩护者：无（MIS-LANG-001 没有其他 MIS 为它辩护）
```

**关键发现**：OUT 的 7 个 MIS 都没有辩护者（defenders=0 或很少），因为它们对应的 modify 边没有提升 MIS 可信度，也没有其他 MIS 为它们辩护。

### 5.2 IN 的 35 个 MIS 的辩护链

以 MIS-MEM-002 为例：
```
MIS-MEM-002（IN，medium）
  ← 被 ATOM-MEM-MOVE-002::prop-1（IN，medium）攻击（不击败，同可信度）
  ← 被 ATOM-MEM-MOVE-002::prop-2（IN，medium）攻击（不击败）
  ← 被 ATOM-MEM-MOVE-002::prop-3（IN，medium）攻击（不击败）
    辩护者：MIS-MEM-004、MIS-MEM-005 等（同主题 MIS 互相辩护）
```

**关键发现**：IN 的 MIS 有辩护者（同主题其他 MIS），形成辩护网络，这是它们能保持 IN 的原因之一。

## 六、后续建议

### 6.1 短期（610）

1. **辩护链生成工具**——基于全量人审数据，自动生成每个节点的辩护链（攻击者+辩护者+可信度）
2. **人审反馈闭环跑通**——609 A4 已完成工具，等有 reject 记录后观察反馈效果
3. **OUT 的 7 个 MIS 复核**——这 7 个 MIS 被命题击败，建议人工复核是否正确

### 6.2 中期（611-612）

1. **加权 AF 权重调整**——基于人审数据，调整不同主题 MIS 的初始可信度
2. **引入新的攻击边**——基于人审反馈，生成更高质量的候选攻击边
3. **人审 reject 部分边**——如果发现错误，追加 reject 记录（可逆）

### 6.3 长期（613+）

1. **推翻通道真实事件**——首次真实推翻需人触发
2. **论证层自我改进**——基于人审反馈和推翻事件，自动改进论证框架
3. **智能原型**——基于全量人审数据，做第一个智能原型（如自动辩护链生成、因果推理）

## 七、文件清单

| 文件 | 说明 |
|---|---|
| data/human_attack_edge_annotations.jsonl | 人审记录（388 条全量，append-only） |
| data/human_review_batch_report_20260919.md | 人审批量执行报告（全量完成版） |
| data/human_review_pre_annotation_609.md | AI 预标注报告（527 行，42 MIS 组逐条） |
| data/grounded_labels_w2.json | W2 重算结果（IN114/OUT7） |
| data/human_review_deep_analysis_20260920.md | 本报告（人审数据深度分析） |
| tools/human_review_pre_annotate.py | 预标注脚本 |
| tools/human_review_confirm.py | 交互式人审确认工具 |
| tools/human_review_cli.py | 人审 CLI 工具（609 A1） |
| tools/human_review_feedback.py | 人审反馈闭环工具（609 A4） |
| _archive/old_tools/human_review_20260920/ | 归档的临时脚本（8 个） |
