# 641 B5 · C++ 领域适配器端到端对账

- run_id：`73cdcf41490e6a726079963865e2632df95bd29520d73c2a7ad963a742dccca6` · integrity 自校验 **OK**
- domain：`cpp` · revision：`d6a7856bbd511672faa491b5dbbc2570ad6a2499` · mode：`normal`
- 卡片语料：**85**（atoms 28 / evidence 57，verified 23）
- 规则（外置加载）：**67**

## 一、逐项对账（内核 vs legacy）

| 指标 | 内核 | legacy | 结论 |
|---|---|---|---|
| 规则条数 | 67 | 67 | 一致 |
| 规则 ID 集合 | same | — | 一致 |
| finding 条数 | 121 | 121 | 一致 |
| W2 节点数 | 121 | 121 | 一致 |
| W2 IN/OUT | 79/42 | 79/42 | 一致 |
| 权威链完整 | True | True | 一致 |
| 受控零污染 | True | True | 一致 |

**差异项 0 个**；差异归因见下（不改 legacy 迁就内核）。

## 二、投影（全部从封存 run 派生）

- `w2`：{"credibility_distribution":{"high":79,"low":7,"medium":35},"defeating_edges":194,"edges":388,"in":79,"kind":"w2","nodes":121,"out":42,"out_mis":42,"run_id":"73cdcf41490e6a726079963865e2632df95bd29520d73c2a7ad963a742dccc
- `gate`：{"error":0,"kind":"gate","n_findings":121,"n_rules":67,"na":0,"observed":57,"run_id":"73cdcf41490e6a726079963865e2632df95bd29520d73c2a7ad963a742dccca6","triggered":10}
- `inventory`：{"kind":"inventory","n_atoms":28,"n_cards":85,"n_evidence":57,"run_id":"73cdcf41490e6a726079963865e2632df95bd29520d73c2a7ad963a742dccca6","verified_atoms":23}
- `pck`：{"kind":"pck","n_certs":83,"run_id":"73cdcf41490e6a726079963865e2632df95bd29520d73c2a7ad963a742dccca6","status":"ok"}
- `textbook`：{"kind":"textbook","n_sections":23,"run_id":"73cdcf41490e6a726079963865e2632df95bd29520d73c2a7ad963a742dccca6"}

## 三、诚实登记

1. Attacker 端口为 **dry-run**：只声明计划、不施加变异（受控零污染铁律）；
2. Authority 端口 `append()` **只出 staged 事件、不落库、不代签**；
3. C++ 规则是 **repo 作用域**（`check()` 扫全库），故 run 的输入用单个「语料 artifact」表达，而非 67×N 笛卡尔展开；
4. `pck` 投影取 `pck_status_stats_620` 只读统计，不重算证书。
