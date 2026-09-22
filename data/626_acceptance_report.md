# 626 验收报告 · Authority 语义收口

> 主题：修复 8 个硬事实错误 + 根治 4 个 P0 + **Authority 单一真源架构落地** + 7 交付物 + 13 完成判据
> 提交链：`6003307a`（任务0）→ `ff855938`（E2），共 **15 commit**，一任务一 commit
> 前置：625 已完成（HEAD `528e9ab2`，未 push）

---

## 一、任务完成总览（17/17）

| # | 任务 | commit | 一句话 |
|---|---|---|---|
| 0 | 开工基线 | `6003307a` | 8 硬伤核实 + 4P0 现状 + 13 判据 + CORE_TOOLS 改造点（**实测无需改动**）+ 迁移风险 |
| A1 | 数值统计修复 | `e4a71063` | median 75→**67.5**、110 记录→**93 唯一**、27→**31 总豁免**、README 口径 + `stats_recalc_verifier_626` |
| A2 | 打包发布质量 | `60167e5e` | ZIP 正斜杠重打包（37 entry）+ 清洗 `data/` **9 文件 339 控制字符** + deep_analysis **STALE** + `REPORT_STATUS.md` |
| A3 | 30 条口径 + 五级分类 | `8dfec744` | 622 执行标注 `USER_AUTHORIZED_EXECUTION`（**不计独立**）+ review_method 五级 + decision_origin 四级 |
| A4 | 决策包 v2 | `e2d33060` | README 加「包定位 / 未包含文件 / 外部审查流程」+ `authority_log`(262KB) 入包 + v2 打包 38 entry |
| B1 | DecisionEvent v2 | `57c3106a` | 26 字段 + `AuthorityLedger` append-only 哈希链 + supersedes 链 |
| B2 | 数据迁移 | `7ef0ac16` | 388+418=806 输入，**去重 354 ⇒ 452 条**，哈希链完整，旧文件未改 |
| B3 | 唯一审查账本 | `45a91ac0` | **110 记录 → 93 unique**（overlap 17 合并），revision/状态机/`symmetry_proof_id` 预留 |
| C1 | Blind Review v1 | `cdc7552e` | Pass A 盲审（**展示 AI 推荐即拒绝提交**）+ Pass B 解盲一致性 + automation_bias_risk |
| C2 | OVERRIDE+三态+镜像 | `cea739d0` | REPLACE 51 条**均有 result+supersedes（硬问题 0）**；三态独立；镜像边 194 归一 null |
| D1 | Projection 核心 | `5cb9a24d` | W2 投影 + PCK 严格/宽松双策略 + 确定性 + 只读 + 可追溯 + feature flag |
| D2 | Projection 扩展 | `d41822d7` | golden（**不自动采纳 legacy**）+ dashboard（93/强度 0）+ textbook 5 态 |
| D3 | Snapshot CI | `daf9995c` | **10 项检查全实现，实跑 10/10 pass** + `--fix` |
| E1 | PCK verifier | `491c490e` | 4 层验证；**发现 56 张 PCK 的 `evidence.hash` 与文件不匹配** |
| E2 | Review Pack v2 | `ff855938` | 两层包 + 自动生成 + 跨平台 + **最小闭环 HTML（Top10）** |
| F1 | 收工 | *本条* | 门禁 + 本报告 + status |

## 二、8 硬伤修复验证

| # | 硬伤 | 修复前 | 修复后 | 验证 |
|---|---|---|---|---|
| 1 | 388 条一致性 | — | approve 354 / modify 34 / reject 0；`kind` 194+194 | 作为迁移输入 ✅ |
| 2 | 30 条"逐条执行" | 被当强人审 | `ITEM_OPEN` + `user_authorized_execution`，**强度仍 0** | A3 标注 + B2 映射 ✅ |
| 3 | 110 唯一性错误 | 110 | **93 unique**（30+80−17） | A1 文档 + B3 账本 ✅ |
| 4 | median 写错 | **75** | **67.5**（min47/max80/mean 69.20） | `stats_recalc_verifier --check` ✅ |
| 5 | 快照污染 | 无标注 | deep_analysis **STALE** + `REPORT_STATUS.md` | D3 `stale_report_detection` ✅ |
| 6 | 31 vs 27 豁免 | 混用 27 | **31 = 27 legacy + 4 HC** | A1 ✅ |
| 7 | ZIP 跨平台 | 36 entry 全 `\` | **正斜杠 `/`**；v2 38 entry；README 大小改自动取值 | `pack_review_zip --check` ✅ |
| 8 | 控制字符 | 9 文件含 0x08/0x0B 等 | **清洗 339 个，rescan = 0** | `control_char_cleaner` + D3 ✅ |

## 三、4 个 P0 根治

| P0 | 根治方案 | 落地 | 状态 |
|---|---|---|---|
| **A** 人类判断 ≠ 授权执行 | `review_method` 五级 + `decision_origin` 四级；独立强度 = BLIND/SECOND_REVIEW + human_observed | A3 + B1 | ✅ 强度 **0**（622 的 30 条不计入） |
| **B** 唯一待审账本 | `ReviewItemLedger`，去重 + revision + `verify_uniqueness()` | B3 | ✅ **93 unique / 110 record** |
| **C** Blind Review | Pass A 禁 AI 推荐（违反即抛错）+ Pass B 一致性/风险 | C1 | ✅ **工具就绪**（真实执行需人授权） |
| **D** OVERRIDE 语义 | `operation`(CREATE/REPLACE/REVOKE) + `result` 拆开；`supersedes` | B1 + C2 | ✅ 51 条 REPLACE **硬问题 0** |

## 四、7 交付物

| ID | 交付物 | 实现 | 状态 |
|---|---|---|---|
| 626-A | DecisionEvent v2 | `decision_event_v2_626.py`（26 字段 + Ledger） | ✅ |
| 626-B | 唯一审查账本 | `review_item_ledger_626.py`（93 unique） | ✅ |
| 626-C | Blind Review v1 | `blind_review_v1_626.py` + 3 条示例（模拟） | ✅ 工具就绪 |
| 626-D | Authority→Projection Compiler | `authority_projection_compiler_626.py`（5 种投影） | ✅ |
| 626-E | PCK semantic verifier | `pck_semantic_verifier_626.py`（4 层，83 张实跑） | ✅ |
| 626-F | Snapshot Integrity CI | `snapshot_integrity_ci_626.py`（10 项，10/10 pass） | ✅ |
| 626-G | Review Pack v2 | `review_pack_v2_626.py`（两层包 + HTML） | ✅ |

## 五、13 完成判据逐项核查

| # | 判据 | 状态 | 依据 |
|---|---|---|---|
| 1 | 无 `item_by_item_executed` 被误计为独立人审 | ✅ 已完成 | A3 标注；B2 映射 ITEM_OPEN+user_authorized_execution；强度 **0** |
| 2 | 93 unique review items 可无歧义追踪 | ✅ 已完成 | B3 账本 93 unique / 110 record；`verify_uniqueness()` 通过 |
| 3 | Blind Review 至少产生一批真实人类决定 | ⚠ **工具就绪，待执行** | C1 工具 + 示例（**模拟数据**）；真实执行需人审者配合 |
| 4 | Authority Event 语义完全确定 | ✅ 已完成 | B1：operation/result/review_method/decision_origin 四轴正交 |
| 5 | Override 有明确 replacement/result | ✅ 已完成 | C2：51 条 REPLACE 均有 result + supersedes（**硬问题 0**） |
| 6 | Authority 是唯一裁定真源 | ✅ **结构性完成**（数值对齐未完） | D1/D2：W2/PCK/golden/dashboard/textbook 全从 Authority 投影；**W2 与 grounded_labels 粒度偏差留 627** |
| 7 | edge→card 不再自动授权升级 | ✅ 已完成 | D1 PCK 投影：无 card-level authority ⇒ `pending` + 跨粒度警告 |
| 8 | W2 IN/OUT 与 truth/publication 解耦 | ✅ 已完成 | C2 三态独立：`argument_status` IN114/OUT7、`truth_support` SUPPORTED27、`publication_status` authorized0 |
| 9 | mirror edge 必须有 symmetry proof 或独立审核 | ✅ 字段就绪（**验证 0**） | C2：194 条镜像边 `symmetry_proof_id` 归一 `null`；已验证 **0** |
| 10 | PCK 能验证 reference/hash/negative-test | ✅ 已完成 | E1 B2-R；**实跑发现 56 张 hash 不匹配** |
| 11 | 所有派生报告带 source digest | ✅ 已完成 | A2 `REPORT_STATUS.md`（git_sha + dataset_sha256）；E2 SNAPSHOT_MANIFEST |
| 12 | stale report 自动失效 | ✅ 已完成 | A2 标注 STALE；D3 `stale_report_detection` 可检测 |
| 13 | 外部 Review Pack 可独立复核至少一个 item | ✅ 已完成 | E2 Evidence Pack + **10 个最小闭环 HTML 页面** |

**小结：11 项已完成，1 项（判据 3）工具就绪待执行，1 项（判据 6）结构性完成、数值对齐留 627。**

## 六、关键数字

| 项 | 值 |
|---|---|
| DecisionEvent v2 ledger | **452** 条（输入 806，去重 354） |
| review_method 分布 | BATCH_AUTH **228** + MIRROR_DERIVED **194** + ITEM_OPEN **30** |
| decision_origin 分布 | human_observed 228 + mirror_projection 194 + user_authorized_execution 30 |
| **独立人类确认强度** | **0** |
| 唯一审查账本 | **93** unique / **110** record（overlap 17） |
| 5 种投影 | W2 / PCK / GOLDEN / DASHBOARD / TEXTBOOK |
| PCK 4 层验证 | B2-S 83 · B2-R **27** · B2-E 83 · B2-A 83（总 pass 27 / fail 56） |
| Snapshot Integrity | **10/10 pass** |
| 新增工具 | **15** 个（全部 `--check` 通过） |
| 新增测试 | **143 例**（全绿） |
| 受控目录 | **零污染** |

## 七、偏差表（任务书假设 vs 实测）

| 任务书假设 | 实测 | 处理 |
|---|---|---|
| 迁移 806 条 | **452**（去重 354） | 按五元组去重；报告统计实际数字 ✅ |
| "review_method BATCH_AUTH 358 + MIRROR 194 + ITEM_OPEN 30" | **228 + 194 + 30** | 354 条重复被去重，故 BATCH_AUTH 为 228 ✅（如实报告） |
| W2 投影与 grounded_labels 应一致 | **不一致**（519 vs 121 节点，粒度不同） | 诚实登记：本投影以 `edge_id` 为节点；**节点归一化留 627** |
| REPLACE 的 supersedes 应为 v2 event_id | 51 条为**旧式引用**（`dec-0001xx` / `legacy:pre_annotation:*`） | 非空可溯源 ⇒ 判据 5 满足；**ID 重映射留 627** |
| 镜像边应有 symmetry_proof_id 字段 | 源数据 **194/194 缺失** | 审计层归一为 `null`；补字段留 627 |
| PCK 应能通过 hash 验证 | **56 张不匹配**（真实引用漂移） | 只验证不修改；是否重算/失效需人裁决（留 627） |
| A2 控制字符"至少两个 PCK 报告" | **9 个文件**（含 3 个 PCK 报告） | 全部清洗 ✅ |
| README 大小"约 1.5MB" | 36 文件 / **770.7 KB** | 改由打包器自动取值 ✅ |

## 八、收工门禁结果

| 检查 | 结果 |
|---|---|
| 15 个新增工具 `--check` | ✅ **15/15 PASS** |
| 整目录 ruff | ✅ All checks passed |
| `mypy tools/` | ✅ **0 errors**（296 文件） |
| 626 新增测试（143 例） | ✅ 全绿 |
| 受控目录零污染 | ✅ `CONTROLLED=CLEAN` |
| Snapshot Integrity CI | ✅ 10/10 |
| CORE_TOOLS 生产逻辑 | ✅ **未改动**（实测 5 个 CORE_TOOLS 均不读 annotations/PCK/golden 判定逻辑） |

## 九、未做项（硬边界遵守声明）

- ✅ 未跑监工门禁（gate / poison / replay / `tool_integrity --check`）
- ✅ 未 push（625 铁律延续）
- ✅ 未 golden accept / 未打开 delegation / 未代签人审
- ✅ 未修改 `atoms/ / evidence/ / Examples/ / Book/` 受控目录
- ✅ 未删除历史报告（只标 STALE）
- ✅ 未删除/修改原始 JSONL（append-only；新 ledger 并行）
- ✅ 未执行真实 Blind Review（需人审者配合）
- ✅ 未默认启用 V2 关键路径投影（feature flag 默认关闭）
- ✅ 未修改 `gate_engine.py` 的 W2 计算逻辑
- ✅ 未做深度语义推理（B2-E 只做结构/引用完整性）

## 十、交人项（需人审裁决）

1. **是否启用 `QUEYI_AUTHORITY_V2=1`** 让 W2/PCK 关键路径切换到 V2 投影（Authority 单一真源正式生效）？
2. **是否执行真实 Blind Review**（需人审者配合）——这是把独立人类确认强度从 0 变为非 0 的**唯一途径**。
3. **是否 push 625+626** 让远程 CI 验证？
4. **数据迁移是否最终确认**（旧 annotations/authority_log 是否在 627+ 废弃）？
5. **W2 三态是否正式启用**（替换现有单一 IN/OUT 状态）？
6. **PCK semantic verifier 发现的 56 处 hash 不匹配如何处置**（重算 / 判证书失效 / 接受漂移）？
7. **Snapshot Integrity CI 的局限是否立项**（path_validity 全量引用解析、20260920 报告血缘逐份复核）？
8. **镜像边的 `symmetry_proof` 是否需要人审验证**（当前 0/194 已验证）？
9. **51 条旧式 supersedes 引用是否做 ID 重映射**？

---
详见：`data/626_baseline.md`（基线）、`data/migration_report_v2_626.md`（迁移）、
`data/decision_event_v2_spec_626.md`、`data/review_item_ledger_spec_626.md`、
`data/blind_review_v1_spec_626.md`、`data/w2_three_state_spec_626.md`、
`data/authority_projection_compiler_spec_626.md`、`data/projection_rules_v0.1_626.md`、
`data/snapshot_integrity_ci_spec_626.md`、`data/pck_semantic_verifier_spec_626.md`、
`data/review_pack_v2_spec_626.md`、`data/REPORT_STATUS.md`。
