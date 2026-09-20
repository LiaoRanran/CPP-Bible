# 辩护链深度分析报告（2026-09-20，基于人审全量数据）

> 基于 388 条全量人审数据和 W2 分层判决（IN114/OUT7），分析每个节点的辩护链（攻击者+辩护者+可信度+击败关系）。
> 辩护链是论证层的核心概念：一个节点 IN，当且仅当它的所有攻击者都被某个辩护者击败。

## 一、辩护链理论基础

### 1.1 W2 模型下的击败关系

W2（可信度加权击败）模型：
- 攻击边 A→B 构成击败，当且仅当 **cred(A) > cred(B)**（严格大于）
- 同可信度不击败（medium vs medium = 不击败）
- 可信度等级：high > medium > low

### 1.2 辩护链定义

对于节点 X：
- **攻击者（attackers）**：所有有边指向 X 的节点
- **辩护者（defenders）**：所有击败 X 的攻击者的节点
- **IN 的条件**：X 的所有攻击者都被某个辩护者击败，或者 X 没有攻击者
- **OUT 的条件**：X 至少有一个攻击者没有被任何辩护者击败（即该攻击者击败 X）

### 1.3 本项目的可信度分布

| 节点类型 | 数量 | 可信度 | 说明 |
|---|---:|---|---|
| 命题（79 个） | 79 | medium | 经过 gate/poison/replay 三重验证 |
| MIS（35 个 IN） | 35 | medium | 对应边 approve，可信度提升 |
| MIS（7 个 OUT） | 7 | low | 对应边 modify，可信度未提升 |
| **合计** | **121** | | |

## 二、OUT 的 7 个 MIS 辩护链分析

### 2.1 MIS-LANG-001（ODR/inline）

```
MIS-LANG-001（OUT，low）
  攻击者：
    - ATOM-LANG-INLINE-001::prop-1（IN，medium）→ 击败 ✓
    - ATOM-LANG-INLINE-001::prop-2（IN，medium）→ 击败 ✓
    - ATOM-LANG-INLINE-001::prop-3（IN，medium）→ 击败 ✓
  辩护者：无（没有任何节点击败这 3 个攻击者）
  判决：OUT（3 个攻击者全部击败，无辩护者）
```

**击败原因**：MIS-LANG-001 对应的 MIS→命题 边被 modify（不是 approve），所以 MIS 可信度保持 low，被命题 medium 击败。

**复核建议**：MIS-LANG-001 是关于 ODR/inline 的误解，有 6 条 modify 边（modify 最多的 MIS）。建议人工复核：这些误解是否真的应该被击败？还是应该 approve（提升到 medium，同可信度不击败）？

### 2.2 MIS-MEM-001（移动语义）

```
MIS-MEM-001（OUT，low）
  攻击者：
    - ATOM-MEM-MOVE-002::prop-1（IN，medium）→ 击败 ✓
    - ATOM-MEM-MOVE-002::prop-2（IN，medium）→ 击败 ✓
    - ATOM-MEM-MOVE-002::prop-3（IN，medium）→ 击败 ✓
  辩护者：无
  判决：OUT
```

**击败原因**：同 MIS-LANG-001，modify 边不提升 MIS 可信度。

**复核建议**：MIS-MEM-001 是关于"移动后源对象一定是有效但未指定状态"的误解。C++ 标准确实说移动后源对象是"有效但未指定状态"，但这个误解可能忽略了某些类型（如 std::unique_ptr）移动后源对象一定是 nullptr。建议复核。

### 2.3 MIS-MEM-003（移动语义）

```
MIS-MEM-003（OUT，low）
  攻击者：
    - ATOM-MEM-MOVE-002::prop-1（IN，medium）→ 击败 ✓
    - ATOM-MEM-MOVE-002::prop-2（IN，medium）→ 击败 ✓
    - ATOM-MEM-MOVE-002::prop-3（IN，medium）→ 击败 ✓
  辩护者：无
  判决：OUT
```

**复核建议**：MIS-MEM-003 是关于"std::move 会移动对象"的误解（实际上 std::move 只是类型转换，不移动）。这个误解是明确错误的，OUT 判决正确。

### 2.4 MIS-UB-001（未定义行为）

```
MIS-UB-001（OUT，low）
  攻击者：
    - ATOM-UB-GRAY-001::prop-1（IN，medium）→ 击败 ✓
    - ATOM-UB-GRAY-001::prop-2（IN，medium）→ 击败 ✓
  辩护者：无
  判决：OUT
```

**复核建议**：MIS-UB-001 是关于"UB 的后果在特定实现下可预测"的误解。这个误解有部分合理性（如 GCC 的 -fwrapv 使有符号溢出定义为回绕），但作为通用规则是错误的。建议复核是否应该 modify（保持 low）还是 approve（提升到 medium）。

### 2.5 MIS-UB-004（未定义行为）

```
MIS-UB-004（OUT，low）
  攻击者：
    - ATOM-UB-GRAY-001::prop-1（IN，medium）→ 击败 ✓
    - ATOM-UB-GRAY-001::prop-2（IN，medium）→ 击败 ✓
  辩护者：无
  判决：OUT
```

**复核建议**：同 MIS-UB-001，UB 相关误解有部分合理性。

### 2.6 MIS-UB-008（reinterpret_cast 类型双关）

```
MIS-UB-008（OUT，low）
  攻击者：
    - ATOM-UB-GRAY-001::prop-1（IN，medium）→ 击败 ✓
    - ATOM-UB-GRAY-001::prop-2（IN，medium）→ 击败 ✓
  辩护者：无
  判决：OUT
```

**复核建议**：MIS-UB-008 是关于"reinterpret_cast 类型双关是合法的"的误解。C++ 标准确实说类型双关是 UB（除了 char*），但 GCC/Clang 有 -fstrict-aliasing 选项，且实际代码中类型双关很常见。这个误解有 4 条 modify 边（第二多），建议重点复核。

### 2.7 MIS-UB-014（未定义行为）

```
MIS-UB-014（OUT，low）
  攻击者：
    - ATOM-UB-GRAY-001::prop-1（IN，medium）→ 击败 ✓
    - ATOM-UB-GRAY-001::prop-2（IN，medium）→ 击败 ✓
  辩护者：无
  判决：OUT
```

**复核建议**：同其他 UB 误解。

## 三、IN 的 35 个 MIS 辩护链分析（抽样）

### 3.1 MIS-MEM-002（移动语义，IN，medium）

```
MIS-MEM-002（IN，medium）
  攻击者：
    - ATOM-MEM-MOVE-002::prop-1（IN，medium）→ 不击败（同可信度）
    - ATOM-MEM-MOVE-002::prop-2（IN，medium）→ 不击败
    - ATOM-MEM-MOVE-002::prop-3（IN，medium）→ 不击败
  辩护者：无（不需要，因为攻击者不击败）
  判决：IN（所有攻击者都不击败）
```

**关键发现**：IN 的 MIS 不需要辩护者，因为它们的可信度和攻击者相同（medium），同可信度不击败。这是 W2 模型的特点：**提升可信度本身就是最好的辩护**。

### 3.2 MIS-CONC-001（并发，IN，medium）

```
MIS-CONC-001（IN，medium）
  攻击者：
    - ATOM-CONC-LOCK-001::prop-1（IN，medium）→ 不击败
    - ATOM-CONC-LOCK-001::prop-2（IN，medium）→ 不击败
  辩护者：无
  判决：IN
```

## 四、命题侧辩护链分析

### 4.1 所有 79 个命题全部 IN

```
命题 X（IN，medium）
  攻击者：所有指向 X 的 MIS（共 388 条边，来自 42 个 MIS）
    - 35 个 MIS（medium）→ 不击败（同可信度）
    - 7 个 MIS（low）→ 不击败（low < medium，是 MIS 被命题击败，不是命题被 MIS 击败）
  辩护者：无（不需要，因为没有任何 MIS 击败命题）
  判决：IN（所有 79 个命题全部 IN）
```

**关键发现**：
1. 没有任何 MIS 击败命题（因为 MIS 可信度 ≤ medium，命题可信度 = medium）
2. 7 个 OUT 的 MIS 是被命题击败，不是击败命题
3. 命题侧没有任何风险，全部安全 IN

## 五、辩护链统计

### 5.1 全局统计

| 指标 | 数字 |
|---|---:|
| 总节点数 | 121（79 命题 + 42 MIS） |
| IN 节点数 | 114（79 命题 + 35 MIS） |
| OUT 节点数 | 7（全部是 MIS） |
| UNDEC 节点数 | 0 |
| 总攻击边数 | 388（194 MIS→命题 + 194 命题→MIS） |
| 击败边数 | 17（全部是命题→MIS，且 MIS 可信度=low） |
| 不击败边数 | 371 |
| 平均每个 OUT 节点的攻击者数 | 2.43 |
| 平均每个 OUT 节点的辩护者数 | 0 |
| 平均每个 IN MIS 节点的攻击者数 | 9.24 |
| 平均每个 IN MIS 节点的辩护者数 | 0（不需要） |

### 5.2 击败边分布

| 被击败的 MIS | 击败它的命题数 | 主题 |
|---|---:|---|
| MIS-LANG-001 | 3 | ODR/inline |
| MIS-MEM-001 | 3 | 移动语义 |
| MIS-MEM-003 | 3 | 移动语义 |
| MIS-UB-001 | 2 | 未定义行为 |
| MIS-UB-004 | 2 | 未定义行为 |
| MIS-UB-008 | 2 | reinterpret_cast |
| MIS-UB-014 | 2 | 未定义行为 |
| **合计** | **17** | |

## 六、辩护链的结构性发现

### 6.1 发现 1：OUT 的 MIS 全部无辩护者

所有 7 个 OUT 的 MIS 都没有辩护者（defenders=0）。这是因为：
1. 它们的攻击者是命题（medium）
2. 没有任何节点的可信度 > medium（全库最高就是 medium）
3. 所以没有任何节点能击败命题（命题的攻击者）

**含义**：在当前可信度体系下（最高 medium），OUT 的 MIS 一旦被命题击败，就永远无法被辩护。要改变这个，需要：
- 引入 high 可信度节点（如经过异族独立验证的命题）
- 或者降低某些命题的可信度（如发现命题有错误）

### 6.2 发现 2：提升可信度是最好的辩护

IN 的 35 个 MIS 不需要辩护者，因为它们的可信度和攻击者相同（medium），同可信度不击败。

**含义**：在 W2 模型下，**approve（提升可信度）比找辩护者更有效**。这也是为什么人审全量完成后，35 个 MIS 从 OUT 变成 IN——不是因为找到了辩护者，而是因为提升了可信度。

### 6.3 发现 3：modify 是"存疑"状态

modify 的边不提升 MIS 可信度（保持 low），所以这些 MIS 会被命题击败（OUT）。

**含义**：modify 是一种"存疑"状态——人审认为这个误解有部分合理性，但还不足以 approve。这些 MIS 处于 OUT 状态，等待进一步裁决。

### 6.4 发现 4：命题侧无风险

所有 79 个命题全部 IN，没有任何 MIS 能击败命题。这是因为：
1. 命题可信度 = medium
2. MIS 可信度 ≤ medium
3. 同可信度不击败，low 更不可能击败 medium

**含义**：命题侧是安全的，论证层的风险全部在 MIS 侧（哪些 MIS 应该被击败，哪些不应该）。

## 七、后续建议

### 7.1 短期（610）

1. **OUT 的 7 个 MIS 人工复核**：重点是 MIS-LANG-001（6 条 modify）和 MIS-UB-008（4 条 modify）
2. **辩护链生成工具**：基于全量人审数据，自动生成每个节点的辩护链（攻击者+辩护者+可信度+击败关系）
3. **引入 high 可信度**：经过异族独立验证的命题可以提升到 high，这样可以为 OUT 的 MIS 提供辩护者

### 7.2 中期（611-612）

1. **辩护链可视化**：生成辩护链的可视化图表（节点+边+可信度+击败关系）
2. **因果推理原型**：基于辩护链，做第一个智能原型（如自动推理"如果 X 被推翻，哪些节点会受影响"）
3. **推翻通道联动**：首次真实推翻后，自动更新辩护链和 W2 判决

### 7.3 长期（613+）

1. **多层可信度体系**：引入 high/medium/low 之外的更细粒度可信度（如 verified_by_oracle 的命题可以是 high）
2. **辩护链学习**：基于人审反馈和推翻事件，自动学习哪些辩护链是有效的
3. **智能论证**：基于辩护链，做更复杂的智能推理（如自动生成新的攻击边、自动发现论证漏洞）

## 八、文件清单

| 文件 | 说明 |
|---|---|
| data/defense_chain_analysis_20260920.md | 本报告（辩护链深度分析） |
| data/human_review_deep_analysis_20260920.md | 人审数据深度分析（388 条全量） |
| data/human_review_batch_report_20260919.md | 人审批量执行报告（全量完成版） |
| data/grounded_labels_w2.json | W2 重算结果（IN114/OUT7） |
| data/human_attack_edge_annotations.jsonl | 人审记录（388 条全量，append-only） |
| References/00_导航/16_论证层详情台账_79命题W2求解.md | 论证层详情台账 |
| References/00_导航/17_人审层详情台账_388边42MIS组.md | 人审层详情台账 |
