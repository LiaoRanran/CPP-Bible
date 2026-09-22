# 626 任务 0 · 开工基线台账（只读）

> 主题：**Authority 语义收口**（8 硬伤修复 + 4P0 根治 + 7 交付物 + 13 完成判据）
> 前置：625 已完成（HEAD `528e9ab2`，未 push）。外部大模型审核报告 802 行 / 15 节已读取。

---

## 一、SNAPSHOT_MANIFEST 当前计数（`data/SNAPSHOT_MANIFEST.json`）

| 项 | 值 |
|---|---|
| generated_at | 2026-09-22T05:51:40Z |
| head_commit | `192d7d98ab4cdb4466f5ac7672362d4e6560e73b` |
| live: commits | 1606 |
| live: tools_py | 257 |
| live: tests_py | 263 |
| live: atoms_md | 28 |
| live: evidence_ev_md | 56 |
| frozen: gate | rules 63 / hits 191 / block 0 / warn 186 / advice 5 |
| frozen: poison | 124/124（apparent 63/63，honest 60/63） |
| frozen: replay | confirm 56 / refute 0 / infra_error 0 |
| frozen: mutation_v7 | escaped 1 / 1406 |
| frozen: confidence | cp 0.00337 / cs 0.009062 |
| frozen: human_review | total 388 / approve 354 / modify 34 / reject 0 / mirror 194 |
| frozen: independence | verifier 1 / second_impl 1/63 / discrete_level 1 |
| frozen: trust_root | partially_anchored |

> 注：manifest 为 **2026-09-22 05:51** 快照，当前 gate 规则数已因 624 B1 变为 **67**（manifest 未同步 ⇒ 属「快照血缘」问题，A2/D3 处理）。

## 二、8 硬伤核实结果（全部实测复现）

| # | 硬伤 | 位置 | 当前值（错） | 正确值（实测） | 修复方案 |
|---|---|---|---|---|---|
| 1 | 388 条一致性 | `data/human_attack_edge_annotations.jsonl` / `attack_edges_candidates.jsonl` | — | 388/388 一一对应；approve 354 / modify 34 / reject 0；`kind`=misconception_refutation 194 + related_atom 194 | 无需修数，作为迁移输入 |
| 2 | 30 条"逐条执行"未新增独立人审 | `authority_log.jsonl` `review_method` | `item_by_item_executed` 被当强人审 | **batch_authorization 388 + item_by_item_executed 30 = 418** | A3：加 `USER_AUTHORIZED_EXECUTION` 标注，独立确认强度=0 |
| 3 | 624 "80新增/累计110" 唯一性错误 | `human_review_item_by_item_624.md` | 110 | **615=30、624=80、overlap=17、union=93** | A1：头部加去重说明；B3：唯一审查账本 |
| 4 | reason median 写错 | `human_review_honesty_615.md:31` | **75** | **67.5**（min47/max80/mean 69.20） | A1：改 67.5 + 外部核验说明 |
| 5 | 2026-09-20 报告快照污染 | `human_review_deep_analysis_20260920.md` | MIS 分布 MEM14/UB12/... | 真值 MEM27/UB9/HIST3/CONC2/LANG1 | A2：STALE 标注 + REPORT_STATUS |
| 6 | 31 条豁免 vs 27 legacy | `exemption_expiry_615.md` / README | 混用 27 | **31 = 27 legacy + 4 HC**（`624_b2_regression`） | A1：口径区分 |
| 7 | ZIP 跨平台 | `阙疑_人审决策包_20260922.zip` | 36 entry 全反斜杠 `\`；README 称"约1.5MB" | 压缩后 **100.4 KB**（102,850 B）；应统一 `/` | A2：`pack_review_zip.py` 正斜杠；A4 v2 重打包 |
| 8 | 控制字符损坏 | `data/` 扫描 | — | **9 个文件**含控制字符（PCK 报告含 `0x08`/`0x0B`：pck_authority_sync_report_620 / pck_status_report_620 / pck_abstain_sync_report_621 等） | A2：`control_char_cleaner.py` |

## 三、4 个 P0 现状与根治方案

| P0 | 当前 schema | 问题 | 根治方案 | 任务 |
|---|---|---|---|---|
| **A 人类判断 vs 人类授权执行** | `review_method: batch_authorization \| item_by_item_executed` | 两者混淆，"授权执行"被计为"独立人审" | 五级 `BATCH_AUTH/MIRROR_DERIVED/ITEM_OPEN/ITEM_BLIND/ITEM_SECOND_REVIEW` + `decision_origin` 四级 | A3 + B1 |
| **B 唯一待审项账本** | 615(30) + 624(80) 列表相加 = 110 | 重复计数，实际 93 unique | `ReviewItemLedger`（revision 管理 + 去重） | B3 |
| **C Blind Review** | 无 | AI 推荐出现在第一视图 ⇒ automation bias | `BlindReviewSession` Pass A 盲审（禁 AI 推荐）+ Pass B 解盲 | C1 |
| **D OVERRIDE 语义** | `power: OVERRIDE`（动作+结果合一） | 51 条 OVERRIDE 语义不明 | 拆为 `operation: CREATE/REPLACE/REVOKE` + `result: APPROVE/REJECT/MODIFY/ABSTAIN` | B1 + C2 |

## 四、7 交付物要求

| ID | 交付物 | 任务 |
|---|---|---|
| 626-A | DecisionEvent v2（24 字段 + AuthorityLedger append-only 哈希链） | B1/B2 |
| 626-B | 唯一审查账本（93 unique / 110 record） | B3 |
| 626-C | Blind Review v1（Pass A/B） | C1 |
| 626-D | Authority→Projection Compiler（W2/PCK/golden/dashboard/textbook） | D1/D2 |
| 626-E | PCK semantic verifier（B2-S/B2-R/B2-E/B2-A 四层） | E1 |
| 626-F | Snapshot Integrity CI（10 项检查） | D3 |
| 626-G | Review Pack v2（Review Pack + Evidence Pack 两层） | E2 |

## 五、13 完成判据

1. 没有任何 `item_by_item_executed` 被误计为 independent human review
2. 93 unique review items 可无歧义追踪
3. Blind review 至少产生一批真实人类决定（**工具就绪，执行需人授权**）
4. Authority Event 语义完全确定
5. Override 有明确 replacement/result
6. Authority 是唯一裁定真源
7. edge → card 不再自动授权升级
8. W2 IN/OUT 与 truth/publication status 解耦
9. mirror edge 必须有 symmetry proof 或独立审核
10. PCK 能验证 reference/hash/negative-test 关系
11. 所有派生报告带 source digest
12. stale report 自动失效
13. 外部 Review Pack 可以独立复核至少一个完整 item

## 六、Authority 相关文件清单 + 数据量

| 文件 | 条数/大小 | 说明 |
|---|---|---|
| `data/human_attack_edge_annotations.jsonl` | 388 条 | 字段：edge_id/action/reason/reviewer/timestamp（**无** review_method/is_mirror） |
| `data/attack_edges_candidates.jsonl` | 388 条 | 字段含 `kind`（misconception_refutation 194 / related_atom 194）⇒ "镜像边 194" 的真实来源 |
| `data/authority/authority_log.jsonl` | 418 条 / 267,921 B | power: ACCEPT 367 / OVERRIDE 51；review_method: batch_authorization 388 + item_by_item_executed 30 |
| `data/authority/pending_review_621.jsonl` | 17,398 B | 待审队列 |
| `data/pck/certificates/*.pck.yaml` | 83 张 | human_authority.status: approved 27 / pending 56（32.5%） |
| `data/grounded_labels_w2.json` | IN 114 / OUT 7 / UNDEC 0（nodes 121） | W2 grounded 语义 |

## 七、CORE_TOOLS 改造点（**结论：无需改动**）

实测扫描 5 个 CORE_TOOLS：

- `gate_engine.py`：未直接读取 annotations / PCK / golden_lock ✅
- `atom_evidence_replay.py`：仅注释/文档提及 golden_lock ✅
- `poison_drill.py`：未读取 annotations / PCK / golden ✅
- `toolchain.py`：无 ✅
- `cppbible.py`:247：仅**调用** `tools/golden_lock.py check`（不改逻辑）✅

⇒ **626 全部功能以新增工具实现，CORE_TOOLS 生产逻辑零改动**，`tool_integrity --update` 非必需（仅当触及 RULER_TOOLS 时）。

## 八、数据迁移风险评估 + 向后兼容方案

| 风险 | 等级 | 缓解 |
|---|---|---|
| 迁移丢数据 | 高 | **只读旧文件**，只写新 ledger；旧文件不删不改（append-only） |
| 哈希链断裂 | 中 | seq 按 `decided_at` 升序分配；append 时校验 prev_hash；`verify_chain()` |
| 重复计数 | 高 | 五元组 `(target_type,target_id,operation,result,decided_at)` 去重；622 的 30 条标注 supersedes |
| 语义漂移（OVERRIDE） | 中 | `power:OVERRIDE` → `operation:REPLACE`，`action` → `result`，逐个校验 |
| 切换风险 | 高 | 统一 feature flag `QUEYI_AUTHORITY_V2`；**dashboard 投影默认启用 V2**，W2/PCK 关键路径默认旧逻辑 |
| 回滚 | — | `QUEYI_AUTHORITY_V2=0` 立即回滚 625 行为；新 ledger 保留供审计不删 |

**迁移输入**：annotations 388 + authority_log 418 = 806（**去重后实际条数在 B2 实测统计，不预设 806**）。
