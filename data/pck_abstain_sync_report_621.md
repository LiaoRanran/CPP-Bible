# 621 C3 · ABSTAIN 与 PCK 集成同步报告

> 证书总数：**83** · 同步成功 **83** · 无匹配 **0**

## 一、同步后的 abstain_state 分布

| abstain_state | 张数 |
| SUPPORTED | 56 |
| UNDECIDED | 27 |

## 二、human_authority 未被改动（不代签）

| 阶段 | 分布 |
| 同步前 | {'approved': 27, 'pending': 56} |
| 同步后 | {'approved': 27, 'pending': 56} |

- 同步后 B2 验证通过：**83 / 83**

## 三、明细（前 20 条）

| cert_id | abstain_state | 弃权 | human_authority |
| ATOM-CONC-FENCE-001 | UNDECIDED | 是 | approved |
| ATOM-CONC-LOCK-001 | UNDECIDED | 是 | approved |
| ATOM-CONC-RACE-001 | UNDECIDED | 是 | approved |
| ATOM-HIST-AUTOPTR-001 | UNDECIDED | 是 | approved |
| ATOM-LANG-INLINE-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-ALIGN-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-ALLOC-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-ALLOC-002 | UNDECIDED | 是 | approved |
| ATOM-MEM-LEAK-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-LEAK-002 | UNDECIDED | 是 | approved |
| ATOM-MEM-MOVE-002 | UNDECIDED | 是 | approved |
| ATOM-MEM-NEW-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-PERF-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-PERF-002 | UNDECIDED | 是 | approved |
| ATOM-MEM-PERF-003 | UNDECIDED | 是 | approved |
| ATOM-MEM-PERF-004 | UNDECIDED | 是 | approved |
| ATOM-MEM-RAII-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-RAII-002 | UNDECIDED | 是 | approved |
| ATOM-MEM-RVREF-001 | UNDECIDED | 是 | approved |
| ATOM-MEM-SHARED-001 | UNDECIDED | 是 | approved |


## 四、与 PCK 原有 uncertainty 字段的对比

| 字段 | 同步前 | 同步后 |
|---|---|---|
| uncertainty.cs_upper_bound | 0.009062（全局 estimand L1） | **不变** |
| uncertainty.estimand | L1 | **不变** |
| uncertainty.abstain_state | 不存在 | **新增**（SUPPORTED 56 / UNDECIDED 27） |
| uncertainty.abstain_reason | 不存在 | **新增**（判定依据原文） |
| uncertainty.abstain_is_abstain | 不存在 | **新增**（是否弃权态） |
| human_authority.* | approved 27 / pending 56 | **完全不动**（不代签） |

**关键说明**：新增的 bstain_state 与原有的 cs_upper_bound 是**两种不同性质的不确定度**：
- cs_upper_bound = 统计口径的**逃逸率上界**（全局 L1 = 0.9062%）；
- bstain_state = 单卡的**证据充分性/可判定性**（这台卡能不能下结论）。
二者互补，不冲突；bstain_state 填的正是原 schema 里"卡内无本地不确定度"的那个空缺
（620 B2 已把它列为缺失最严重字段第 1 位）。

## 五、局限性声明

1. **不代签**：human_authority 一个字节都没动。abstain_state 是**机器判据**，
   不是人审结论；UNDECIDED **不等于**人"拒绝"，SUPPORTED **不等于**人"接受"。
2. **分类器是规则-based**（C1 §七）：只看字段存在性与日期，不理解证据内容质量。
3. **UNDECIDED 27 张源于原子卡没有 erdict 字段**（C2 §二）：
   这是**元数据口径不一致**的暴露，不是这 27 张卡"真的证据不足"。
4. **CONFLICTED / STALE / INSUFFICIENT_EVIDENCE 均为 0**：因 elations 普遍为空、
   erified_at 缺失 —— 0 应读作"**判不出来**"而非"没有问题"。
5. **未写入渲染产物**：data/pck/rendered/ 的 83 份 markdown 是 620 B3 生成的，
   本批**未重新渲染** ⇒ 渲染件里还看不到 abstain_state（是否展示 = §八 人拍板项 2）。
6. **schema 未在 B1 文档里登记新字段**：data/pck_certificate_schema_619.md 未同步更新
   （619 B1 schema 为冻结件，改它需走人审）⇒ 新字段目前是"实现先行、文档滞后"。
