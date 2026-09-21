# 620 C3 · Authority 与 PCK 集成同步报告

> Authority 日志条目：**388** · 证书总数：**83**

## 一、同步统计

| 指标 | 值 |
| 证书总数 | 83 |
| 匹配到 Authority 决策 | **25** |
| 无匹配（保持 pending，不代签） | **58** |
| 同步后 B2 验证通过 | 83 / 83 |

## 二、同步后状态分布

| status | 张数 |
| approved | 27 |
| pending | 56 |

## 三、匹配明细（前 30 条）

| cert_id | 匹配决策数 | 生效 status | power |
| ATOM-CONC-FENCE-001 | 0 | approved | — |
| ATOM-CONC-LOCK-001 | 0 | approved | — |
| ATOM-CONC-RACE-001 | 6 | approved | ACCEPT |
| ATOM-HIST-AUTOPTR-001 | 32 | approved | ACCEPT |
| ATOM-LANG-INLINE-001 | 6 | approved | OVERRIDE |
| ATOM-MEM-ALIGN-001 | 6 | approved | ACCEPT |
| ATOM-MEM-ALLOC-001 | 32 | approved | ACCEPT |
| ATOM-MEM-ALLOC-002 | 6 | approved | ACCEPT |
| ATOM-MEM-LEAK-001 | 12 | approved | ACCEPT |
| ATOM-MEM-LEAK-002 | 6 | approved | ACCEPT |
| ATOM-MEM-MOVE-002 | 48 | approved | OVERRIDE |
| ATOM-MEM-NEW-001 | 18 | approved | ACCEPT |
| ATOM-MEM-PERF-001 | 4 | approved | ACCEPT |
| ATOM-MEM-PERF-002 | 12 | approved | ACCEPT |
| ATOM-MEM-PERF-003 | 18 | approved | ACCEPT |
| ATOM-MEM-PERF-004 | 6 | approved | ACCEPT |
| ATOM-MEM-RAII-001 | 12 | approved | ACCEPT |
| ATOM-MEM-RAII-002 | 16 | approved | ACCEPT |
| ATOM-MEM-RVREF-001 | 6 | approved | ACCEPT |
| ATOM-MEM-SHARED-001 | 30 | approved | ACCEPT |
| ATOM-MEM-SHARED-002 | 6 | approved | ACCEPT |
| ATOM-MEM-UNIQUE-001 | 12 | approved | ACCEPT |
| ATOM-MEM-UNIQUE-002 | 12 | approved | ACCEPT |
| ATOM-MEM-VALUE-001 | 6 | approved | ACCEPT |
| ATOM-MEM-VALUE-002 | 12 | approved | ACCEPT |
| ATOM-MEM-WEAK-001 | 24 | approved | ACCEPT |
| ATOM-UB-GRAY-001 | 40 | approved | OVERRIDE |
| EV-CONC-001 | 0 | pending | — |
| EV-CONC-002 | 0 | pending | — |
| EV-CONC-003 | 0 | pending | — |


## 四、同步前后对比

| 指标 | 同步前（B2 迁移后） | 同步后（C3） | 变化 |
|---|---|---|---|
| approved | 23 | **27** | +4（由 Authority 日志匹配补登） |
| pending | 60 | **56** | −4 |
| rejected | 0 | 0 | 不变 |
| B2 验证通过 | 83/83 | **83/83** | 未破坏 |

**+4 的来源**：ATOM-LANG-INLINE-001、ATOM-MEM-ALLOC-002、
ATOM-MEM-LEAK-002、ATOM-MEM-PERF-004 —— 这 4 张原子卡 frontmatter status
未标 erified*（故 B2 派生为 pending），但在**历史人审通道中有真实决策**，
C3 依日志补登为 approved。⇒ **同步是对真实决策的回填，不是凭空提升**。

## 五、与现有人审通道的对比

| 维度 | 现有人审通道（human_attack_edge_annotations.jsonl） | Authority 日志（C2） |
|---|---|---|
| 条数 | 388 | 388（**全部导入**） |
| 形态 | attack_edge 标注 | 统一 AuthorityDecision |
| 防篡改 | 无 | **哈希链**（erify() 已通过） |
| 撤销语义 | 无显式的 | OVERRIDE 追加（不改不删） |
| 弃权语义 | 无 | ABSTAIN 明确可用 |
| reviewer | 有实名 | 必填且校验空名 |

## 六、局限性（诚实登记）

1. **当前是从现有人审通道导入，不是独立的人审记录**：388 条决策的历史来源是
   「AI 预标注 + 用户批量授权」（reason 字段原文即写明"用户授权批量通过"），
   ⇒ 其 eview_method **全部为 atch_authorization**，非逐条独立审阅。
2. **匹配靠子串**：cert_id in decision.target.id。若卡 id 是另一卡 id 的
   子串（当前未发生），可能误匹配；更严谨的映射需 attack_edge → card 的结构化字段。
3. **证据卡（EV-*）零匹配**：历史人审通道只覆盖 attack_edge（→原子卡），
   56 张证据卡**没有任何** Authority 决策，全部保持 pending。
   ⇒ 这与 B3 统计的 "证据卡 0% authorized" 一致，是**真实缺口**，不是工具缺陷。
4. **不代签**：58 张无匹配的证书一律保持 pending，工具不会把它们变成 approved。

## 七、下一步（交人）

- 真正的**逐条**人审应通过 620 C1 的 Authority 接口记录（eview_method: item_by_item），
  而非继续沿用批量授权导入。
- 30 条逐条人审是否走 Authority 接口 —— **人拍板**（620 不代决）。
- 证据卡的 Authority 决策仍为空白，需后续补做。
