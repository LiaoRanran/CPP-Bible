# 622 开工基线台账（任务 0，只读）

> 批次：622 · 开工：2026-09-22
> 起始 HEAD：`44f9694`（= 621 收工）· `git log 44f9694..HEAD` **为空** ⇒ 621 后无新 commit
> 解释器：`.venv\Scripts\python.exe`

---

## 一、SNAPSHOT_MANIFEST 当前计数

| 字段 | manifest 值 | 备注 |
|---|---|---|
| head_commit | `15e73d4`（621 E1） | 落后于实际 HEAD `44f9694`（E2 及补正未回写） |
| live_counts.commits | 1587 | — |
| live_counts.tools_py | 251 | — |
| live_counts.tests_py | 250 | 其中 `test_*.py` = 249 |
| live_counts.atoms_md | 28 | 实际卡 27 |
| live_counts.evidence_ev_md | 56 | — |
| FROZEN_VERIFICATION.gate | 63 / 191 / **block 0** | 622 不跑门禁复核（硬边界） |
| FROZEN_VERIFICATION.poison | 124/124（诚实 95.2%） | 冻结值保留 |
| FROZEN_VERIFICATION.replay | 56 / 0 / 0 | 冻结值保留 |

## 二、工作树状态（`git status --short`）

```
 M _adv_v80/probes/p57.cpp    （CRLF 假脏，619 起已登记）
 M data/metrics_612.md        （时间戳，619 起已登记）
?? _arch_v19/  _arch_v19_brief.md  （并行会话存档，非本批）
?? _arch_v20/  _arch_v20_brief.md
```

**622 承诺**：保持原状、不清理、不提交（沿用 619/620/621 处置）。

## 三、远程 / push 状态（B1 前置）

| 项 | 值 |
|---|---|
| `origin/master` | **`d2f412b`**（= 619 收工） |
| 本地领先 | **37 commit**（620 的 18 + 621 的 18 + 并行 PM 1） |
| 待 push 范围 | **`d2f412b..HEAD`**（620–622） |
| 620/621 是否已 push | **否** |

> ⇒ 620 B1/B3 改的 ci.yml（竞态修复）**从未在远程 CI 实跑过**，这正是 622 B1 要解决的。

## 四、ci.yml 当前依赖关系（确认 621 B1/B3 已落地）

| job | needs | 说明 |
|---|---|---|
| `quality` | **`[replay]`** | ✅ 621 B3 追加（Worktree Cleanliness 读 `Examples/atoms/`） |
| `concurrency-safety` | — | ✅ 621 B3 新增（静态校验"写者先、读者后"） |
| `pytest` | — | — |
| `replay` | — | **写者**（recompile 重写 `Examples/atoms/*.asm`） |
| `gate` | **`[replay]`** | ✅ 621 B1 修复（读工件） |
| `compile` | `[quality, pytest, replay, gate]` | — |
| `publish-check` | `[quality, pytest, replay, gate]` | — |
| `site` / `pdf` / `epub` | `[compile, publish-check]` | — |
| `deploy` | `[site, pdf, epub]` | — |

## 五、621 A2 的 50 条新 mutation（A2 待实跑）

| 维度 | 值 |
|---|---|
| 总数 | **50**（覆盖 50/83 张卡，每卡 1 条） |
| 策略分布 | rule_blind_spot **17** · evidence_ambiguity **17** · provenance_inconsistency **16** |
| 算子分布 | M7 13 · M6 10 · M2 8 · M1 6 · M5 5 · M4 4 · M3 4 |
| 判决（621 的**预测**） | blocked 36 · n_a 14 · escaped **0** |
| 新颖性（621 A3） | 50/50 落在 0.5 档（**卡×算子组合与 v7 100% 重合**） |

**单条结构**（A1 沙箱需按此施加）：
```json
{"mutation_id": "MUT-621-…", "attack_type": "rule_blind_spot",
 "target_rule": "EV-FM-REQUIRED", "target_card": "atoms/conc/ATOM-CONC-FENCE-001.md",
 "content": "{\"detail\":…,\"op\":\"M1\",\"point\":…,\"target_rule\":…,\"target_card\":…}",
 "generated_at": "…"}
```
> ⚠ `content` 是**描述性 JSON**（op + point + detail），**不是可执行 patch** ⇒
> A1 沙箱 API 必须自己把 `op`/`point` 映射成**真实卡面修改**。

## 六、621 C2 的 ABSTAIN 分类（C 线待升级）

| 状态 | 张数 |
|---|---|
| SUPPORTED | **56**（全部证据卡） |
| UNDECIDED | **27**（全部原子卡） |
| 其余 4 态 | 0 |

**已知病灶**：原子卡**没有 `verdict` 字段**（用 `status`）⇒ 分类器只能弃权。
**已知反相关**：SUPPORTED×pending 56 · UNDECIDED×approved 27。

## 七、615 的 30 条逐条复核决策清单（D1 待执行）

| 项 | 值 |
|---|---|
| 来源文件 | `data/human_review_item_by_item_30_615.md` |
| 总条数 | **30** |
| 建议 modify | **17**（MIS-LANG-001 / MIS-MEM-001 / MIS-MEM-003 / MIS-UB-001 / MIS-UB-004 / MIS-UB-008 / MIS-UB-014 的 OUT7 正向边） |
| 建议 approve | **13**（MIS-MEM-002/004/005/012/017 → ATOM-MEM-MOVE-002） |
| 621 D1 状态 | 已转成 30 条**待审条目**（`data/authority/pending_review_621.jsonl`，status=pending），**决策日志未动** |

## 八、Authority 日志现状（D1 前置）

| 项 | 值 |
|---|---|
| 条目数 | **388** |
| power 分布 | ACCEPT **354** · OVERRIDE **34** |
| review_method | 全部 `batch_authorization`（导入自历史人审通道） |
| D1 目标 | 执行 30 条后 → **388 + 30 = 418** |

## 九、本批要解决的 621 五个遗留

| 级别 | 遗留 | 622 对应 |
|---|---|---|
| 🔴 | 沙箱 apply API 缺失（新逃逸恒 0 的根因） | **A1**（核心） |
| 🟠 | CI 竞态修复未 push | **B1/B2** |
| 🟡 | ABSTAIN 与 Authority 完全反相关 | **C1/C3** |
| 🟡 | 原子卡 27 张全 UNDECIDED（缺 verdict） | **C2/C3** |
| 🟡 | 30 条逐条人审未执行 | **D1/D2** |
| — | 雷7 Verification Horizon 未启动 | **E1/E2** |


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
