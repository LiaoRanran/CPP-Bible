# 621 开工基线台账（任务 0，只读）

> 批次：621 · 开工：2026-09-22
> 起始 HEAD：`d5edb14`（= 620 收工）· `git log --oneline d5edb14..HEAD` **为空** ⇒ 620 后无新 commit
> 解释器：`.venv\Scripts\python.exe`

---

## 一、SNAPSHOT_MANIFEST 当前计数

| 字段 | manifest 值 | 与 620 收工实测 |
|---|---|---|
| head_commit | `a57de309…`（E1，a57de30） | 落后 1（E2 commit d5edb14 未回写） |
| live_counts.commits | 1570 | 实测 **1571**（+1 = 620 E2） |
| live_counts.tools_py | 241 | 241 |
| live_counts.tests_py | 236 | 236（其中 test_*.py = 235） |
| live_counts.atoms_md | 28 | 28（实际卡 27） |
| live_counts.evidence_ev_md | 56 | 56 |
| FROZEN_VERIFICATION.gate | 63 / 191 / **block 0** / warn 186 / advice 5 | 620 已确认稳态一致（本批不跑门禁复核） |
| FROZEN_VERIFICATION.poison | 124/124（诚实 95.2%） | 冻结值保留 |
| FROZEN_VERIFICATION.replay | 56 / 0 / 0 | 冻结值保留 |
| mutation_v7 | 1593 / 1406 分母 / escaped 1 | 冻结值保留 |

> manifest 的 `head_commit` 记的是**生成时刻**的 HEAD，与承载它的 commit 天然差 1
> （既有工具设计，620 §十.6 已登记），非 621 引入。

## 二、工作树状态（`git status --short`）

```
 M _adv_v80/probes/p57.cpp    （CRLF 假脏，619 已登记）
 M data/metrics_612.md        （时间戳，619 已登记）
?? _arch_v19/  _arch_v19_brief.md  （并行会话存档，非本批）
?? _arch_v20/  _arch_v20_brief.md
```

**621 承诺**：上述遗留保持原状、不清理、不提交（沿用 619 §八 / 620 §十.7 处置）。

## 三、v7 mutation 基线（`data/mutation/full_baseline_v7.json`）

| 维度 | 值 |
|---|---|
| 总 mutation 数 | **1593** |
| blocked | 1405 |
| n_a | 179 |
| escaped | **9**（其中 **equivalent 8** ⇒ **真逃逸仅 1**） |
| equivalent | 8 |
| 覆盖卡数 | **83**（27 原子 + 56 证据） |
| 可判分母 | 1406（= blocked 1405 + 真逃逸 1） |
| 逃逸率契约 | **1 / 1406** |

**算子分布**：M6 724 · M4 251 · M2 195 · M7 139 · M3 107 · M1 92 · M5 85
**口径分布**：strict 811 · warn_only 594 · None 188

**单条记录字段**（A1/A3 需对齐此格式）：
`card, equivalent, kind, new_block, new_warn, op, point, replay_skipped, reproduce, verdict`

示例：
```json
{"card": "evidence/conc/EV-CONC-001.md", "op": "M1", "point": "删 artifact_sha256",
 "reproduce": "…tools/mutation_fuzz.py --cards … --operators M1 --limit 1",
 "verdict": "blocked", "kind": "strict",
 "new_block": ["EV-FM-REQUIRED:evidence/conc/EV-CONC-001.md"], "new_warn": [],
 "replay_skipped": "gate 已严格拦截…", "equivalent": false}
```

> 现有生成器是 `tools/mutation_fuzz.py`（**只读基线生成器**，C++ 侧生成）。
> 621 A1 **不复用其内部状态**，另起纯标准库生成器（620 §九.8 已登记其为 VFDR 恒 0 的瓶颈）。

## 四、620 A2 闭环结果（当前候选空间）

| 项 | 值 |
|---|---|
| 候选空间 | **v7 既有 1593 条**（可判 1406） |
| W1 真逃逸排名 | 57 / 1406（第 3 轮命中） |
| W2 真逃逸排名 | **1 / 1406**（第 1 轮命中） |
| 新逃逸发现 | **0**（结构必然：不生成新 mutation） |
| VFDR | 恒 0.0 |
| 盲区暴露 | W1 57/60 · W2 60/60 |

**620 遗留的核心局限**：候选空间**钉死**在 v7 ⇒ VFDR 恒 0 是结构结果，不是"系统无盲区"。
⇒ 这正是 621 A 线要打破的：**生成新 mutation，让闭环真能发现新逃逸**。

## 五、ci.yml 当前 job 依赖关系

`.github/workflows/ci.yml` 共 **10 个 job**：

| job | needs | 与共享资源的关系 |
|---|---|---|
| `quality` | —（并行） | 读 `Examples/atoms/`（受控目录清洁校验步） |
| `pytest` | —（并行） | 读仓库状态 |
| `replay` | —（并行） | **写** `Examples/atoms/*.asm`（recompile 删旧写新） |
| `gate` | —（并行） | **读** `Examples/atoms/`（EV-ARTIFACT-FILE-EXISTS） |
| `compile` | `[quality, pytest, replay, gate]` | — |
| `publish-check` | `[quality, pytest, replay, gate]` | — |
| `site` / `pdf` / `epub` | `[compile, publish-check]` | — |
| `deploy` | `[site, pdf, epub]` | — |

**竞态病灶**：`replay`（写 `Examples/atoms/`）与 `gate`（读同一目录）**并行且无依赖**
⇒ gate 可能采样到 replay 重编译的"删旧写新"中间窗口 ⇒ 619 的 2 条 BLOCK 误报。
⇒ 621 B1 采用**方案 A**：给 `gate` 加 `needs: [replay]`。

## 六、621 要解决的 620 遗留

| 级别 | 遗留 | 621 对应 |
|---|---|---|
| 🔴 | 闭环候选空间钉死（VFDR 恒 0） | A 线 A1–A4 |
| 🟠 | CI gate∥replay 并发竞态 | B 线 B1–B3 |
| 🟡 | PCK authorized 仅 27/83（56 张证据卡全 draft） | C/D 线（C3 增加 abstain_state，D1 建待审条目） |
| — | 雷6 未知检测/弃权三态 | C 线 C1–C3 |


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true
