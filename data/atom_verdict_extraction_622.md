# 622 C2 · 原子卡 verdict 提取（27 张）

> 提取总数：**27**（**未修改任何原始卡**）

## 一、提取结果分布

| verdict | 张数 |
| SUPPORTED | 27 |

## 二、置信度分布

| 置信度 | 张数 |
| high | 26 |
| low | 1 |

## 三、提取依据分布

| basis | 张数 |
| `status=verified` | 23 |
| `status=red-team-verified` | 3 |
| `evidence_only` | 1 |

## 四、与 621 C2 的对比

| 项 | 621 C2（分类器 v1） | 622 C2（提取后） |
|---|---|---|
| 原子卡 UNDECIDED | **27 / 27** | **0 / 27** |
| 原子卡 SUPPORTED | 0 | **27** |
| 原子卡 REFUTED | 0 | **0** |

## 五、逐卡明细

| 卡 ID | verdict | 置信度 | basis | status | 证据数 |
| ATOM-CONC-FENCE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-CONC-LOCK-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-CONC-RACE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-HIST-AUTOPTR-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-LANG-INLINE-001 | SUPPORTED | low | `evidence_only` | draft | 2 |
| ATOM-MEM-ALIGN-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-ALLOC-001 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-ALLOC-002 | SUPPORTED | high | `status=red-team-verified` | red-team-verified | 2 |
| ATOM-MEM-LEAK-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-LEAK-002 | SUPPORTED | high | `status=red-team-verified` | red-team-verified | 2 |
| ATOM-MEM-MOVE-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-NEW-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-PERF-001 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-PERF-002 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-PERF-003 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-PERF-004 | SUPPORTED | high | `status=red-team-verified` | red-team-verified | 2 |
| ATOM-MEM-RAII-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-RAII-002 | SUPPORTED | high | `status=verified` | verified | 3 |
| ATOM-MEM-RVREF-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-SHARED-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-SHARED-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-UNIQUE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-UNIQUE-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-VALUE-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-VALUE-002 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-MEM-WEAK-001 | SUPPORTED | high | `status=verified` | verified | 2 |
| ATOM-UB-GRAY-001 | SUPPORTED | high | `status=verified` | verified | 2 |


## 六、结论

- **27 张原子卡的"UNDECIDED"是"缺字段"造成的，不是"真弃权"**：
  用 status / evidence / claim_structured.claim_type 三个既有信号即可提取出 verdict。
- 提取结果：**SUPPORTED 27**（status=verified 23 + status=red-team-verified 3 + evidence_only 1）。
- ⇒ 与 Authority（27 张原子卡全部 pproved）**方向一致**，为 C3 的"对齐"提供了基础。
- ⚠ **但这只解决了 27 张原子卡**；56 张证据卡的问题方向相反（机器 SUPPORTED、人 pending），
  C3 需单独分析。

## 七、局限性声明

1. **规则-based，不是语义理解**：只读 status / evidence / claim_type 三个字段，
   **不判断证据内容是否真的证成主张**。
2. **"status=verified 即 SUPPORTED"是口径假设**：它等价于"信任人审结论"，
   而非"机器独立验证了命题"。⇒ 提取出的 SUPPORTED **继承**了人审的可信度，不是新证据。
3. **唯一 1 张 evidence_only（low）** 是 status=draft 的卡：它**仅因有证据**被判 SUPPORTED，
   置信度低，**需人审确认**。
4. **claim_type 只区分 observation/inference**（实测 50/29），
   未对"inference 型命题证据是否充分"做进一步判定。
5. **不修改原始卡**（硬边界）：提取结果只落 data/。
   是否把 erdict **写回原子卡** = 622 §八.3 **人拍板项**。
6. **未做人审复核**：本批**不代签**；提取结果的可信度上限 = status 字段本身的可信度。
