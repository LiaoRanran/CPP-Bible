# 620 验收报告 · 18 任务（止血 + 雷2闭环 + 雷4全量 + 雷5接口 + 化债）

> 批次：620 · 起始 `d2f412b`（619 收工）· 收工 HEAD 见文末 · **18 commit**
> 状态：**awaiting_review**（不 push、不 golden accept、不打开 delegation）
> 解释器：`.venv\Scripts\python.exe`

---

## 一、任务完成度：18/18

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| 0 | 开工基线 | `data/620_baseline.md` | ✅ |
| 1 | 修复 2 条 BLOCK | `data/620_block_fix_report.md` | ✅（根因=并发竞态，稳态 block=0） |
| 2 | 重钉 SNAPSHOT | `data/SNAPSHOT_MANIFEST.json` + `data/620_snapshot_regen_report.md` | ✅ |
| A1 | 闭环沙箱框架 | `tools/adversarial_loop_620.py` + 11 例单测 | ✅ |
| A2 | 第一轮闭环运行 | `data/adversarial_loop_round1_620.md` + 7 例单测 | ✅ |
| A3 | 权重校准实验 | `tools/adversarial_weight_calibration_620.py` + `data/adversarial_weight_calibration_620.md` + 10 例单测 | ✅ |
| A4 | VFDR 实时计算 | `tools/vfdr_realtime_620.py` + `data/vfdr_realtime_620.md` + 10 例单测 | ✅ |
| B1 | PCK 批量迁移工具 | `tools/pck_batch_migrator_620.py` + 9 例单测 | ✅ |
| B2 | 全量 83 张迁移 | `data/pck/certificates/*.pck.yaml`(83) + `data/pck_migration_report_620.md` + 7 例单测 | ✅ |
| B3 | 状态统计+渲染 | `tools/pck_status_stats_620.py` + `data/pck/rendered/*`(83) + `data/pck_status_report_620.md` + 8 例单测 | ✅ |
| C1 | Authority 接口定义 | `data/human_authority_interface_620.md` | ✅（仅定义，未启用） |
| C2 | Authority 日志 | `tools/authority_log_620.py` + `data/authority/authority_log.jsonl`(388) + 10 例单测 | ✅ |
| C3 | 与 PCK 集成 | `tools/pck_authority_sync_620.py` + `data/pck_authority_sync_report_620.md` + 8 例单测 | ✅ |
| D1 | 619 计数修正 | `data/620_count_correction.md` + 修正 `619_acceptance_report.md` | ✅（57→53） |
| D2 | CI 状态确认 | `data/620_ci_status.md` + 更正 619 报告 CI 段 | ✅ |
| D3 | 工具命名规范 | `data/620_naming_convention.md` | ✅（评估，未执行改名） |
| E1 | 收工门禁 | `tools/run_620_gate.py` + `tests/test_620_gate.py`(10 例) | ✅ |
| E2 | 验收报告 | 本文件 + `_auto/status.json` + `_auto/outbox/620.md` | ✅ |

---

## 二、收工门禁（E1）复跑结果

```
run_620_gate → 验收门: PASS (EXIT=0)
[1/5] 受控目录零污染     ✅ 干净（atoms/ evidence/ Examples/ Book/）
[2/5] 逐工具 --check     ✅ 7/7 通过（run_620_gate 自身不参与，避免自指）
[3/5] pytest（620 新增） ✅ 80 passed
[4/5] gate block=0      ✅ 命中 191（block=0 warn=186 advice=5）【串行，不与 replay 并发】
[5/5] ruff 静态检查      ✅ 17 个文件通过
```

- 门禁自身单测（`tests/test_620_gate.py` 10 例）**单独跑全绿**；
  未纳入 `NEW_TESTS` 是刻意的——否则形成「门禁 → 自己的单测 → 门禁」自指递归。
- `gate` 是唯一跑的监工门禁（任务书允许，用于确认 block=0），**严格串行**。

---

## 三、止血结果（任务 0-2）

### 3.1 2 条 BLOCK 的真相：并发竞态，不是数据回归

619 独立验收曾报「EV-CONC-003/004 引用工件不存在 ⇒ 2 条 BLOCK」。620 复测：

- `gate --check` 连跑 3 次均为 **191 命中 / block=0**（与冻结基线逐字一致）；
- `Examples/atoms/_atom_lock_cost.asm` **确实存在**（28190 字节，git 已跟踪）；
- 两卡 `artifact_sha256` 与 replay 独立重编译结果**逐字相符**；
- 该文件 `LastWriteTime = 2026/9/21 22:44:25` —— 恰在 619 验收会话期间，
  由 `atom_evidence_replay --check` 的 recompile **删旧写新**重写；
- 619 验收把 `gate` 与 `replay` **并行**发起 ⇒ gate 采样到重编译的"删旧未写新"窗口。

⇒ **这 2 条 BLOCK 是瞬时误报**。因此**未修改任何卡片、未补产工件、未改 gate_engine**
（改正确的数据去迎合误报本身就是错误）。已在 619 独立验收报告追加「更正附录」。

**派生纪律（620 起执行）**：`gate` 与 `replay` **禁止并发**；已写入 620 基线台账与 E1 门禁。

### 3.2 SNAPSHOT 重钉

旧 manifest 的 `FROZEN_VERIFICATION.gate = 191/block=0` **本就正确**（任务1 已证伪"失准"判断），
故**保持不变**；仅刷新 `generated_at` / `head_commit` / `commits`。

---

## 四、A 线：攻击-验证迭代闭环（雷2 第二阶段）

| 权重 | 可判 | 真逃逸排名 | 命中轮次 | 新逃逸 | VFDR | 收敛 |
|---|---|---|---|---|---|---|
| W1 | 1406 | 57 | **第 3 轮** | 0 | 0.0 | 是 |
| W2 | 1406 | **1** | **第 1 轮** | 0 | 0.0 | 是 |

- **W2 第 1 轮就打到唯一真逃逸，W1 需 3 轮** —— 与 619 A1 敏感度分析一致（W1 57 / W2 1）。
- **新逃逸 0 条，且这是结构必然**：不生成新 mutation ⇒ 候选空间钉死在 v7 既有 1593 条，
  其判决早已存在。故"0 新逃逸"**不能**解读为"系统无盲区"。
- 权重校准（6 种）：W1 57 / W2 **1** / W3 57 / W4 792 / W5 297 / W6 帕累托（真逃逸不在前沿上）。
  **W3 无法"验证器分歧优先"**（verifier_disagreement 恒 N/A ⇒ 等价 W1 缩放，重叠 100%）。
- 盲区暴露：W1 57/60、W2 60/60（风险信号，未证实可逃逸）。

---

## 五、B 线：PCK 全量迁移 83 张（雷4 第二阶段）

| 指标 | 值 |
|---|---|
| 自动发现卡 | **83**（原子 27 + 证据 56） |
| 生成 / B2 验证通过 | **83 / 83（100%）** |
| 5 级状态 | authorized **27** / unverified **56** / 其余 0 |
| verifiers = 1 | 83/83（100%，verifier_disagreement 恒 N/A） |
| cs_upper_bound = 0.009062 | 83/83（全局 estimand，卡内无本地 CS） |
| 渲染产物 | 83 份 `data/pck/rendered/` |

**关键诚实发现**：
- **全部 56 张证据卡 status 为 draft** ⇒ 0% authorized；原子卡 23/27（85.2%）。
- **619 的 10 张试点是精选**（authorized 40%），全量真实水平只有 **27.7%**
  ⇒ 试点数字不能外推，这正是做全量迁移的价值。
- 缺失最严重字段：卡内本地 uncertainty（83）、逐条人审（83）、第二 verifier（83）、
  approved（60）、first_authorized_at（57）。

---

## 六、C 线：Human Authority 接口（雷5）

- **C1 仅定义不实现**：四权力 ACCEPT/REJECT/OVERRIDE/ABSTAIN + `Model ≠ Verifier ≠ Authority`
  + No single principal + AuthorityDecision 数据结构 + 与现有人审通道/golden_lock 的映射。
  刻意**不实现 Authority 类**（实现即等于造出机器 Authority，违反第一原则）。
  ⚠ 提示词要求"读 37 号路线图雷5节"，**仓库内未检索到该章节**，已按提示词规格+现有系统推导并如实登记。
- **C2 日志**：append-only JSONL + 哈希链；导入历史决策 **388 条**，链校验 `chain_ok=True`。
  空名签收/非法 power/空 reason/缺 overrides 全部 **fail-closed**；篡改可被检测。
- **C3 集成**：83 张证书同步，**匹配 25 张 / 无匹配 58 张**；
  无匹配者**保持 pending，绝不代签**。approved 23 → 27（+4 为历史人审真实决策回填）。
  同步后 B2 验证仍 **83/83**。

---

## 七、D 线：化债

| 任务 | 结论 |
|---|---|
| D1 计数修正 | 619 自报 57 例 → **实测 53 例**（pytest 实跑）；619 报告两处已修正并标注 |
| D2 CI 状态 | `origin/master` 实测 = **`d2f412b`**（619 收工），**非** 619 所称 `cbd0fbd`(616) ⇒ 619 报告该句已更正；617/618/619 **已在 CI 覆盖范围内**；620 未 push ⇒ **未被 CI 覆盖** |
| D3 命名规范 | 240 工具中仅 **41** 带批次后缀；41 个全部被引用，引用处 **318** ⇒ **建议存量不改名**（成本≫收益），新批次强制 `_NNN`（620 已执行） |

---

## 八、核心数字（收工时实测）

| 维度 | 619 收工 | 620 收工 | 变化 |
|---|---|---|---|
| commits | 1553 | **1570** | +17（620 收工后 +1 = 1571） |
| tools/*.py | 233 | **241** | **+8**（620 新增 8 个工具） |
| tests/test_*.py | 225 | **235** | **+10**（620 新增 10 个单测文件） |
| 新增单测例数 | —(53) | **90** | 80（9 个功能文件）+ 10（门禁自身） |
| atoms / evidence | 28 / 56 | 28 / 56 | 不变 |
| 本地领先 origin/master | 0 | **17**（收工后 18） | 620 全部未 push |

---

## 九、交人项（不可代决，留 621）

1. **攻击目标权重拍板**：W1（保守）vs **W2**（校准锚定，第 1 轮即命中真逃逸）。建议 W2 作闭环锚定。
2. **是否启用 Authority 接口**替换现有人审通道；30 条逐条人审是否走该接口。
3. **PCK 是否成为权威源**（83 张已就绪）。
4. **schema 升级**：支持 `abstain` / `conditionally_authorized`（当前恒 0，字段缺失）。
5. **是否 push**（620 未 push，故 8 工具 + 90 单测未经 CI 实跑）。
6. **工具命名**：是否接受"新批次强制 `_NNN`、存量 41 个不改名"。
7. **CI 竞态修复**：`gate` 与 `replay` 在 CI 中是**并行 job**，理论上可复现 620 任务1 的竞态
   ⇒ 建议给 `gate` 加 `needs: [replay]` 或让 replay 原子替换写文件（本批不改 CI）。
8. **沙箱 API**：`mutation_fuzz` 缺"施加到副本"接口 ⇒ VFDR 结构恒 0 的根本瓶颈。

---

## 十、遗留与诚实登记

1. **A 线未测到迭代增益**：0 新逃逸是"不能生成新 mutation"的结构结果，非攻防成果。
2. **C1 未引用到路线图雷5原文**（仓库内检索不到），定义依据提示词规格推导。
3. **C2/C3 的 388 条决策来源是"AI 预标注 + 用户批量授权"**，全部 `batch_authorization`，
   非逐条独立审阅 —— 导入不等于"人真的逐条审过"。
4. **C3 匹配靠子串**（`cert_id in decision.target.id`），理论上存在误匹配风险。
5. **D 线均为评估/修正，未执行改名、未改 CI**。
6. **manifest 自指限制**：`SNAPSHOT_MANIFEST.json` 的 `head_commit` 记的是生成时刻的 HEAD，
   与承载它的 commit 天然差 1，属既有工具设计，非 620 引入。
7. 工作树遗留脏文件（CRLF 假脏 `p57.cpp`、时间戳 `metrics_612.md`、未跟踪 `_arch_v19/20/`）
   保持原状、不清理、不提交（沿用 619 §八 处置）。
