# 609 先量基线（任务0 · 只读）

采集时间：2026-09-19 · 解释器 `.venv\Scripts\python.exe` · HEAD `a07701d`（608 收工）
原则：**只读**，除本文件外未修改任何盘面；未跑全量 pytest / gate / poison / replay / tool_integrity --check。

## 0.1 人审通道现状

| 项 | 实测 | 获取命令 |
|---|---|---|
| 文件 | `data/human_attack_edge_annotations.jsonl` | `Get-Item … | Select-Object Length` |
| 行数 | **0 行** | `Get-Content … -Encoding utf8` → `lines=0` |
| 字节 | **0 字节** | `Length=0` |
| 首行 schema | 无首行（空文件） | `Get-Content … -TotalCount 1` → 空 |

**schema 真源**（从 596 的 `tools/attack_edge_review.py` 读出，第 49-52 行）：

```
ACTIONS  = ("approve", "reject", "modify")
REQUIRED = ("edge_id", "action", "reason", "reviewer", "timestamp")
PROMOTE  = {"low": "medium", "medium": "high", "high": "high"}
STATUSES = ("pending", "approved", "rejected", "modified")
```

> ⚠️ **口径偏差 #1**：任务书写人审记录字段为 `kind`；596 既有实现用的是 `action`（且 `check()` 会把未列出的字段判为"未知字段"）。
> 609 按**任务书口径**落地 `kind`，同时**读取时兼容** `action`（`kind = obj.get("kind") or obj.get("action")`），保证两条通路不互相打断。写入只按 609 的 `kind` schema。

候选边字段（真源 `data/attack_edges_candidates.jsonl` 第 1 行）：
`id / source / target / kind / evidence / confidence / direction / generated_at / generator_version`
（注意：候选边的 `id` 形如 `ae-ATOM-CONC-RACE-001::prop-1->MIS-CONC-003`，**不是**任务书假设的 `MIS-XXX::prop-N` 格式 ⇒ 口径偏差 #2，见下。）

## 0.2 slow 性能基线

| 项 | 实测 | 获取命令 |
|---|---|---|
| 目标 | `tests/test_task_queue_stateful.py` | `pytest tests/test_task_queue_stateful.py -n0 --tb=no -q -p no:cacheprovider` |
| 用例数 | **7 passed** | 输出 `.......` |
| 墙钟 | **72.6 s** | `[Diagnostics.Stopwatch]` 计时：0.2 项 `wallclock=72.6s` |
| 退出码 | 0 | `pytest_exit=0` |
| max_examples | 100（608 D1 预算锁） | `tests/test_task_queue_stateful.py` 第 ~420 行 |
| 已知瓶颈 | 20,952 次 connect/close + WAL pragma ≈ 72% 耗时 | 见 `data/slow_performance_profile.md`（608 D2） |

## 0.3 grounded 数据现状

`python tools/attack_edge_generator.py stats`（∀ 任务书的 `--stats`，实际子命令是 `stats` ⇒ 口径偏差 #3）：

```
[attack] 候选边 388 条 · source MIS 117 个 · target 117 个
[attack] 按 kind {'misconception_refutation': 194, 'related_atom': 194}
[attack] 按 confidence {'low': 388}（实测：MIS 卡面无可信度字段 ⇒ 当前全 low）
[attack] 按 direction {'mis_to_prop': 194, 'prop_to_mis': 194}
[attack] source 分布 Top5 {'MIS-MEM-031': 12, 'ATOM-UB-GRAY-001::prop-1': 10,
                          'ATOM-UB-GRAY-001::prop-2': 10, 'MIS-MEM-024': 9, 'MIS-MEM-026': 9}（共 117 个 MIS）
```

`python tools/weighted_af_solver.py stats`：

```
[w2] 节点 121（命题 79 / 误解 42） · IN 79 / OUT 42 / UNDEC 0
[w2] 命题标签 {'IN': 79} · 误解标签 {'OUT': 42}
[w2] 平均攻击者 3.21（命题 2.46 / 误解 4.62）· 平均辩护者 5.09
[w2] 击败边 194/388 · 3 轮收敛
```

| 任务书预期 | 实测 | 结论 |
|---|---|---|
| 79 命题 / 42 MIS / 388 候选边 | 79 / 42（source 侧去重 117 个 MIS id）/ 388 | 一致 |
| W2 IN79-OUT42-UNDEC0 | IN 79 / OUT 42 / UNDEC 0 | 一致 |
| 支持边 80 条（C1 期望） | 攻击图里只有 194+194 攻击边；"支持边"须由 `solve()` 的 `defenders` 派生 | 见 C1 实现口径 |

## 0.4 信任根现状

任务书的 `python tools/merkle_integrity.py check_all` **不存在**（实际子命令为
`build / build-all / prove / verify / consistency / stats` ⇒ 口径偏差 #4），改用 `stats`：

```
[merkle] 台账 data/supply_chain/merkle_roots.json（algo=sha256-path-bound-count-bound-v1）
  - Book:                Book              · root 0a36f80b46c4d317… · 文件 183 · 高 8
  - Examples:            Examples          · root 2e8063fe0d1aee5c… · 文件 1541 · 高 11
  - atoms:               atoms             · root 11c0b3d982017229… · 文件  29 · 高 5
  - evidence:            evidence          · root bfc1d80e19a9a75e… · 文件  57 · 高 6
  - mutation_baselines:  data/mutation     · root 42829d7851991a3f… · 文件   7 · 高 3
```

| 目录 | 根前 8 位（完整 64 位见 `data/supply_chain/merkle_roots.json`） | 文件数 | 树高 |
|---|---|---|---|
| Book | `0a36f80b` | 183 | 8 |
| Examples | `2e8063fe` | 1541 | 11 |
| atoms | `11c0b3d9` | 29 | 5 |
| evidence | `bfc1d80e` | 57 | 6 |
| mutation_baselines | `42829d78` | 7 | 3 |

> `stats` 是**只读**读数，不重算 Merkle；未跑重建/上链。本批不改任何 Merkle 根。

## 0.5 度量现状

| 项 | 实测 | 备注 |
|---|---|---|
| `data/metrics.jsonl` 行数 | **10**（任务书预期 ~11） | 本地文件、被 gitignore |
| 末行 escape_rate_history | v1…v7 共 7 个版本点 | 见下 |
| v7（当前权威） | judged=1406 · n_a=179 · **numerator=1 / denominator=1406** | point=0.000711238 |
| v7 C-P95 | cp_lower=1.80068e-05 · **cp_upper=0.003956325504751501 = 0.3956%** | 点估计 0.0711% |

各版本note（原文摘录，用于 E1 的"口径修正 ≠ 单调收敛"标注）：
- v1：`574 修 M5 尺子后，M5 活雷未收（口径修正）`
- v4：`575 命题级活性锚，M5 规则已拦但被 diff 键吞（口径修正）`
- v5：`578 _findings_key 并入文案后，587 起 1/1375（口径修正）`
- v6：`588 发现器补全后 1/1379，被 v7 取代（口径修正）`
- v7：`591 当前口径：589 T2 注释净化 un-mask 27 条 fixture 路径变异 ⇒ M2 可判 141→168；唯一 escaped=1（M1/EV-CONC-001 冻结 TCE）`

metrics.jsonl 末行另有 `build_reproducibility`（total 10 / reproducible 10 / 100%）与
`invariants_all_pass=true`，可供 E2 引用。

## 0.6 既有工具版本

```
HEAD:      a07701d  608 收工：outbox/608.md 交付报告 + status.json 置 awaiting_review
                    （A/B/C/D 四线交付；修复并行化债会话误删的 596 人审通道文件 + A3 脆弱断言）
git status: M  _auto/status.json
            ?? _auto/inbox/609.md
```

工作树仅有 `_auto/` 下的协议文件变动（609 提示词入库 + status.json 被上一会话置位）；
未出现两条长期 CRLF 假脏（`data/mutation/full_baseline_v4.json`、`evidence/conc/EV-CONC-001.md`）——本批也不提交不还原。

## 基线口径偏差清单（供各线引用）

| # | 任务书假设 | 实测 | 609 处理 |
|---|---|---|---|
| 1 | annotations 字段 `kind` | 596 既有是 `action` | 609 写 `kind`、**读时兼容** `action` |
| 2 | edge_id 格式 `MIS-XXX::prop-N` | 实际 `ae-<source>-><target>` | 按真实 388 条 `id` 全集校验 |
| 3 | `attack_edge_generator.py --stats` | 实际是子命令 `stats` | 一律按真实 CLI 调用 |
| 4 | `merkle_integrity.py check_all` | 无此子命令，只有 `stats` 等 | 用 `stats`（只读） |
| 5 | metrics.jsonl ~11 行 | 实测 10 行 | 按实记录 |
| 6 | 388 边全部 MIS→命题 | 实际 117 个 MIS/命题混合源 | 按真实分布渲染 |


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true
