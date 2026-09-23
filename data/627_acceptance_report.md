# 627 批次验收报告

- **批次**：627（固本批）
- **日期**：2026-09-23
- **基线**：`4f2c976c`（626 F1 收工）
- **提交**：12 commit（`f4b19c65`..E1），本地领先远程 43（铁律：627 不 push）
- **inbox**：`_auto/inbox/627.md`（严格执行）

## 一、任务完成度（13/13）

| # | 任务 | 结果 |
|---|---|---|
| 0 | 开工基线台账 | ✅ 4 项技术债量化 + 9 交人项分类 + flag 切换前基线快照 |
| A1 | W2 投影节点归一化 519→121 | ✅ `w2_projection_normalizer_627`（APPROVE∪MODIFY 为生效攻击 + weighted_af_solver 严格大于击败），实跑 IN 114 / OUT 7 / UNDEC 0，diff 工具逐节点对比 **diff=0** |
| A2 | 51 条 supersedes 旧式 ID 重映射 | ✅ `supersedes_remapper_627`（legacy 34 + dec 17 全可恢复 → 有效 v2 event_id；生成 remapped ledger 不破坏原文件 + 重算哈希链；链全可解析） |
| A3 | 56 张 PCK hash 漂移根因分析 | ✅ `pck_hash_drift_analyzer_627`：实测 **content_drift 56 + hash_absent 26 + ref_missing 1 = 83 全有缺口**；子因=行尾/编码/内容变更；只读不修改 |
| A4 | 镜像边 194 条对称性验证 | ✅ `mirror_edge_symmetry_checker_627` 逐条查反向边分类 symmetric/asymmetric；全部 `symmetry_proof_id=null` 需人工验证；只生成不写入 |
| B1 | `QUEYI_AUTHORITY_V2=1` 端到端 | ✅ `authority_v2_e2e_627` 子进程跑 **5 种投影全部成功** + V1 legacy 对照（w2/pck） |
| B2 | V2 回归验证 | ✅ `v2_regression_627` **静态**：CORE_TOOLS 五件全隔离 flag/V2 工具 + legacy W2 求解器未改 + 本批次未改 CORE_TOOLS ⇒ 无回归可达路径（gate/poison/replay **未跑**，留 push 后 CI） |
| B3 | V2 一键启用/回滚 | ✅ `authority_v2_switch_627` 模式文件管控意图 + `run` 子命令读模式设 env 调 626 编译器生效；enable/rollback 零副作用；**默认关闭需人确认** |
| C1 | Blind Review 执行包 Top10 | ✅ `blind_review_execution_pack_627` 从 93 unique 账本按歧义度取 Top10；**Pass A 盲性严格不泄露既有裁定**；含空白决策位 + 人审指南（Pass A/B + automation_bias 风险） |
| C2 | Blind Review 结果回填工具 | ✅ `blind_review_backfill_627` 构造 ITEM_BLIND/human_observed 合法条目 + validate 通过；**append_to_ledger 定义不调用**；`--stage` 只写暂存不落库 |
| D1 | push 前最终检查 | ✅ `pre_push_checklist_627` 10 工具 --check 全过 + ruff/mypy 0 + 627 测试全过 + 受控零污染 + CORE 未改；**静态确认源码无 git push 调用** |
| E1 | 收工门禁 | ✅ `run_627_gate.py --check` **PASS**（11 工具 + 整目录 ruff/mypy 0 + 627 测试 + 受控零污染 + tool_integrity 尺子一致 + CORE 未改 + commit 链连续） |
| E2 | 验收报告 + status/outbox | ✅ 本报告 + `_auto/status.json` → `awaiting_review` + `_auto/outbox/627.md` |

**测试**：627 新增 **≈62 例单测全过**（A1 6 + A2 5 + A3 5 + A4 4 + B1 5 + B2 5 + B3 5 + C1 4 + C2 4 + D1 6 + E1 5 + 迁移/工具内回归）。

## 二、收工门禁（run_627_gate --check）

```
[ok] 整目录 ruff 全绿
[ok] 11 个 627 新工具 --check 全过
[ok] mypy tools/ = 0 errors
[ok] 627 新增测试全过
[ok] 受控目录零污染
[ok] tool_integrity --check（626 尺子 34/34 仍一致）
[ok] CORE_TOOLS 未修改
[ok] commit 链连续
=> 627 收工门禁: PASS ✅
```

## 三、核心诚实结论

1. **A 线（4 项技术债）全部闭环**：
   - W2 粒度对账（519→121 归一化 + diff=0）；
   - 51 条旧式 ID 重映射（全可恢复，不破坏原文件）；
   - 56 张 PCK hash 漂移**根因明确**（content_drift，非随机），处置建议交人；
   - 194 条镜像边对称性**全部待人工验证**（诚实，不可机器代签）。
2. **B 线（V2 启用前置）全部打通**：5 种投影端到端成功 + 静态证明无回归可达路径 + 一键启用/回滚脚本就绪。**但 gate/poison/replay 未实跑**（铁律不跑监工门禁），远程 CI 实跑留 push 后（交人项）。
3. **C 线（Blind Review）工具链完备但强度仍为 0**：执行包 + 回填工具已备，真实盲审**必须由人执行**——独立人审强度仍是 0，这是机器无法代办的部分。
4. **未做（诚实登记）**：未 push、未 golden accept、未代签任何人审、未修改 626 工具与 CORE_TOOLS、未触碰受控目录。

## 四、交人项（排序）

1. **Feature flag 启用裁决**（B1/B2/B3 已备齐前置）；
2. **真实 Blind Review 执行**（C1 包 + C2 回填工具，Top10 优先）；
3. **push 裁决**（D1 清单全绿，远程 CI 实跑 gate/poison/replay）；
4. 56 张 PCK hash 漂移处置（重签 or 换 hash 基线）；
5. 194 条镜像边对称性人工验证；
6. DEBT-001 到期处置（626 遗留）。

## 五、留 628

- gate/poison/replay 远程 CI 实跑（push 后）；
- Blind Review Top10 真实执行 + 回填落库；
- PCK hash 重签（若人裁决）；
- 镜像边 symmetry proof 人工验证；
- flag 启用后 W2 双模真正分支（626 编译器接入 flag 文件，需 628 立项，因 627 不改 626 工具）。

## 六、交付物清单

**工具（12）**：w2_projection_normalizer_627 / w2_projection_diff_627 / supersedes_remapper_627 / pck_hash_drift_analyzer_627 / mirror_edge_symmetry_checker_627 / authority_v2_e2e_627 / v2_regression_627 / authority_v2_switch_627 / blind_review_execution_pack_627 / blind_review_backfill_627 / pre_push_checklist_627 / run_627_gate

**数据（14+）**：w2_normalized_627.json / w2_projection_diff_627.json|md / supersedes_remapped_627.jsonl / pck_hash_drift_627.json|md / mirror_edge_symmetry_627.json|md / authority_v2_e2e_627.json|md / v2_regression_627.json|md / authority_v2_mode.json / authority_v2_enable_guide_627.md / blind_review_pack_top10_627.json / blind_review_human_guide_627.md / blind_review_backfill_staging_627.jsonl / pre_push_checklist_627.json|md / 627_acceptance_report.md

**规范/报告**：本报告 + B 线两份报告 + C 线指南
