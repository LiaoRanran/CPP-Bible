# 535 夜间建设者施工日志 · 批次1 L2 调度完成 + 批次2 V-iso 部分完成

> 依据：`References/architecture_架构演进/535_夜间建设者大活_L2调度+V-iso+529收口落地.md`
> 纪律：一任务一 commit；不 push；不 golden accept；改核心工具跑全量 pytest；数字全为本机实测（跑不出就写"未观测到"）。

## 幂等进度看板（新会话从这里续）

```
批次1 L2 调度层（534 C1–C7）   [x] 全做完（8 commit；task_queue pytest 8→46 例全绿）
批次2 V-iso 阴阳同构
  V1 判据正式化 tools/viso_diff.py   [x] f587bd6（+41 例）
  V2 B0 样板卡 FENCE-001 真阴面      [x] e374517（阴夹具 + negative_controls 声明）
  V3 replay 接入阴性判决分支         [x] 972c362（+10 例）+ ee1d7c8（重钉工具校验和）
  V4 毒样例 N1–N7 + 双指标           [ ] 未开始 —— 施工点见 §2.3
  V5 56 卡迁移 backlog（只排队不降级）[ ] 未开始 —— 施工点见 §2.3
批次3 529 剩余 P0/P1（5 项）          [ ] 未开始
```

---

## 0. 开工实测（2026-09-15，窗口一开始跑，**不照抄提示词**）

| 项 | 实测输出 |
|---|---|
| HEAD | `d976170`（530 收工），工作树：`References/architecture_架构演进/53*.md`、`_arch_*/_adv_*/_worklog_*/_t53*` 等未跟踪沙箱（正常，未提交） |
| `gate_engine.py --check` | `[gate] 规则 60 条 · 命中 141 (block=0 warn=136 advice=5)` |
| `poison_drill.py` | `90/90`；`零覆盖攻击面：无` |
| `atom_evidence_replay.py --check --no-sanitizer` | `confirm=56 refute=0 infra_error=0` |
| `pytest -m fast -q` | **185 passed**（点计数 72+72+41） |
| `knowledge_graph.py build/stats` | 325 节点 / 291 边；CONTRASTS=22、CONTRADICTS=1；跨原子概念 0 / 最大连通分量 3 |
| `kg conflicts` | 候选矛盾 **1 组**（与非 530 收工一致） |
| `task_queue.py list` | `0 条` |
| 受控目录 | `Examples/atoms` / `atoms/` / `tools/golden_state.json` 干净 |

---

## 1. 批次1 · L2 调度层落地（**C1–C7 全部完成**，8 commit）

> 全部在**已落地**的 `tools/task_queue.py`（d976170）上做增量，不重写、不另起文件；d976170 既有 8 例 pytest **零修改**全绿。

| commit | 项 | 交付 |
|---|---|---|
| `5a5323b` | C1 | `migrate()`：`busy_timeout` 先于 `journal_mode`、建表 + 14 个增量列 + `events` 表**同一** `BEGIN IMMEDIATE`、`PRAGMA user_version` 版本门；`downgrade --yes` 回退（逐列 `DROP COLUMN`） |
| `55efc92` | C1 补 | **`_set_wal()` 幂等 + 显式退避重试**（见 §1.1 最深坑） |
| `176428d` | C2 | `validate_handoff()` 纯函数（goal/next_action/steps_done 产物在盘+哈希逐字/verified_facts 带可解析锚点且 L2 必 `cmd:`/budget_used 非负/yield 期 remaining 非空）；`checkpoint`（校验不过即拒，`--force` 人签留痕）+ `cp_fingerprint`；`enqueue` 扩参（`--touch/--verify-cmd/--budget/--parent/--model/--steps/--goal`）+ 自引用/成环拒（rc=2）；`claim` 交出 handoff 全文 + next_action |
| `107ac68` | C3 | `yield_task`：fail-closed 校验（`--force` 只解预算闸门，不解质量闸门）→ 父转 `yielded`（保留 checkpoint/指纹）→ 残步骤切 ≤4 个子任务（parent 回指、预算按剩余比例且 ≥80、组间串 deps、touch/verify_cmd 继承；子任务继承父 verified_facts 但 `steps_done` 归零）+ `_rollup_parent` 父回卷 |
| `4f80b91` | C4 | touch_set 文件锁：claim 候选循环裁掉与在飞任务相交的候选并点名 `blocked_by_touch`，继续领不冲突的；`next` 只读预览同口径 |
| `0ce3c80` | C5 | 租约语义（`LEASE_GRACE_S=120`：租约内裸 claim 抢不到、软 takeover 拒 rc=2 并给接管命令）+ `--takeover --force --reason` 人担责接管（`events.manual_takeover` 留痕）+ token possession（`data/tasks/workers/<worker>.token` → `claimed_token`，`_authorize` 单点校验） |
| `476526d` | C6 | `complete`（worker 不得自证）：type→verify_cmd 绑定表（`{py}`/`{payload}` 占位）、rc=0 记 `verify_hash`、rc≠0 回 queued（attempts+1）/超限 blocked、无 verify_cmd 必须 `--result-ref`（`HUMAN_REVIEW_REQUIRED`）+ touch 收尾审计（`git status -uall` 比 touch_set，豁免 `data/tasks/**`，审计跑不成显形 `audit_note`）+ `main()` 把业务拒绝收敛成返回码 |
| `6c2441e` | C7 | `resume_plan()`：L1（独立重算哈希：match/mismatch/no_digest/no_file，任一坏 ⇒ `blocked`）/ L2（必重跑 `cmd:`）/ L3（永不继承，进 l3_human）三级清单，挂在 claim 返回体 + CLI 摘要 |

### 1.1 最深坑：534 的归因**不完整**（规格说 X、实测 Y、按 Y 做）

- 规格说（534 §5 坑①）：冷启动竞态根因是 `_connect` 里 `PRAGMA journal_mode=WAL` 排在 `busy_timeout` **之前**，把顺序调对即可（沙箱实测 6/8 → 12/12）。
- 实测 Y：顺序调对 + 单事务 + 版本门之后，**全量 pytest 里仍抓到 1 次冷启动失败**（`migrate` → `PRAGMA journal_mode=WAL` → `database is locked`）。真因更深：**SQLite 在"模式切换"路径上不调用 busy handler**（切换须原子完成、不能半路重试）⇒ `busy_timeout` 对**这一句**完全无效，调顺序只是必要条件。
- 按 Y 做：新增 `_set_wal()`（已是 WAL 直接返回；否则**显式退避重试** ≤10 次），`_connect` 与 `migrate` 共用。
- 证据（可复跑）：①修后并发冷启动用例连跑 **20 次 = 240 轮双进程建库，零失败**；②阴性对照 `_t535_probe/race_negative_control.py`（复原旧顺序 + 去掉重试 + 逐列 ALTER）：4/4 次复现 1–2 轮失败，报错形如 `duplicate column name: claimed_token` / `database is locked`。

### 1.2 其余与规格/提示词的偏差（逐条处置）

| # | 规格/提示词 | 实测/现状 | 处置 |
|---|---|---|---|
| 1 | 534 §1.1「tasks 表 15 列」 | 实测 `PRAGMA table_info` = **14 列** | 按 14 列写测试常量，规格数字偏差记此 |
| 2 | 535 C2 列清单**不含** `goal`，但 534 §2.2 要求 `--goal` | 无落点则参数是死的 | 补 1 列 `goal TEXT NOT NULL DEFAULT ''`（最小增量，已注释） |
| 3 | 535 C3「退回 pending」vs 534 §3.4「父→`yielded`」 | 若父回 queued，剩余步骤会被下一次 claim 重复执行 | **按 534**：父 `yielded`、残步骤由子任务承接、全子 done ⇒ 父自动 done |
| 4 | 535 C5 未列 token possession，但 C2 列清单含 `claimed_token` | 列不实现就是死列 | 按 534 §6.1 实现（E12 冒名拦截），并注明**诚实边界**：同一 Windows 用户能读 token 文件即可冒充，本机单人场景文件系统权限即信任边界 |
| 5 | complete 收尾审计（534 §4.1） | `git status --porcelain` 默认把非 ASCII 路径输出成**八进制转义**（实测 `References/architecture_/346/236/...` 完全不可读） | 加 `-c core.quotepath=false`，并把"中文名路径可读"写进回归锁 |
| 6 | 沙箱把未声明改动写进 `error` 列 | 成功态的 `done` 行带 error 语义混乱 | 改为 done 事件 detail + 返回体 + CLI stderr 三处显形（沙箱是原型，按纪律 6 工程化重写） |
| 7 | 534 §2.3「非法迁移 exit 2」/ d976170 既有拒绝 exit 1 | 两套口径并存 | 明确定义并写进 docstring：**1 = 既有拒绝路径**（d976170 契约），**2 = 新增 fail-closed 门**（deps 环/handoff 质量/软 takeover/无 verify_cmd 又无 result-ref）；`main()` 统一收敛成返回码（库函数仍抛 `SystemExit`） |
| 8 | 534 §8 的 C6「heartbeat 假活指纹 + doctor」 | 535 的 C1–C7 清单**未要求** | **不做**（按纪律不夹带）；`hb_same_count` 列也一并省掉，留作后续批次（施工点：心跳带 handoff 指纹、连续 2 次相同且间隔达标才报 zombie） |

### 1.3 pytest 覆盖（`tests/test_task_queue.py`：8 例 → **46 例**）

| 批次 | 新增例 | 覆盖要点 |
|---|---|---|
| C1 | 3 | 12 轮双进程冷启动零失败 + user_version/WAL 断言；旧库原地升级幂等；回退往返 + 无 `--yes` 拒绝 |
| C2 | 17 | 扩参落列（touch 归一去重）；自引用/成环 rc=2 且不留半行；`validate_handoff` 10 条机器判据**逐条反例** + 1 条正例；checkpoint 落盘/fail-closed/`--force` 留痕/非本人拒；claim 交 handoff（含坏 path 显形） |
| C3 | 4 | 切子+父回卷主场景；预算闸门；质量闸门硬门；分组上限/碎片/重复切分拒 |
| C4 | 2 | 冲突跳过并点名等待者；预览同口径 + stale 持锁者不算持锁者 |
| C5 | 3 | 租约内裸 claim 拿不到 + 软 takeover rc=2 + force 无 reason 拒 + 接管留痕 attempts 累加；token 缺失/被换/恢复；升级前 NULL token 残留放行 |
| C6 | 6 | 真 git 根审计（未声明文件显形 + 中文路径可读 + `data/tasks` 豁免）；rc≠0 两轮 requeue→blocked；无 verify 必须 result-ref；type 默认表；审计不可见时显形；**CLI 全链**（enqueue→claim→checkpoint→complete→list→yield→takeover rc=2） |
| C7 | 3 | 三级分类 + L1 坏哈希 blocked；validate 拒被偷换的 L1 物证；claim 返回 resume_plan（CLI 摘要 + 库结构） |

### 1.4 留人裁决项（本批**未做**，不代人签）

1. `complete` 的收尾审计在**真实仓库**跑一次会列出 **772 个未跟踪文件**（`_arch_*`/`_adv_*`/`_worklog_*`/`_t53*`… 全是沙箱残渣）。按规格**不自动豁免**（"未声明改动必须显形"）——若要降噪，正路是业务侧用 `--touch` 声明或把沙箱收编进 `.gitignore`，**不建议**给审计加"沙箱前缀白名单"（那等于给藏污留门）。
2. 534 §8 C6 的 `doctor`（stale/zombie/预算将尽巡检）与心跳假活指纹：535 未要求，未实现。
3. `data/tasks/` 运行时态（queue.db/-wal/-shm、workers/*.token、`<id>.handoff.json`）已随 `/data/tasks/` 在 `.gitignore:76` 内，未入库。

---

## 2. 批次2 · V-iso 阴阳同构（**V1/V2 完成；V3–V5 交接**）

### 2.1 V1（`f587bd6`）· 判据正式化 `tools/viso_diff.py` + 41 例

- 判据（533 §2.2，全部 AND）：单 hunk / 新增行=0（delete-only，一行改名替换被结构性击毙）/ 代码删除行 1–3 / 纯注释删除=0 / tokens ≤40 / 比率 ≤2% / 删除行 **100%** 落 anchor 函数体 / `remove` 命中 / `retain` 逐字保留（**连主体删除的唯一硬拦点**）/ 探针符号 Itanium 同源；anchor **重名或找不到一律拒**（不猜第一个）；函数体内字符串字面量含花括号 ⇒ fail-closed 拒。
- `negative_controls` frontmatter schema 校验（533 §2.1）也落在同模块：**纯函数**（文件存在性/anchor 定义数/样板文本/已声明 run 键由调用方注入谓词，不碰盘），v1 只认 `v1` + `delete_mechanism` + `artifact|run_key` 两通道，`run_rc` 显式拒收，命名规约只 warn。
- **修掉一个会误杀全部真夹具的定位 bug**：本仓夹具是 Allman 风格（`int f()` 与 `{` 分两行），原型只看同行的定义判定会把真夹具全判成"找不到 anchor"；现实现继续吞后续行到 `{`/`;`（并配回归锁）。
- 实测复算与 533 §2 校准表**逐字一致**：真阴面 `tokens_changed=5`、`ratio=0.01116`、`coverage=1.0`、`hunks=1`、`inserted=0`；沙箱 5 个攻击样本（43 替换/删错位置/连循环带 fence 删/注释走私/冒名）全部拒收，落原文保留（`loop_kill` 由 retain 拦下）。

### 2.2 V2（`e374517`）· B0 样板卡落位

- `Examples/atoms/_atom_fence_vs_atomic.nc1.cpp`：由 `_t535_probe/make_nc1.py` **带前置断言**生成（fence 行 8 空格形态恰 1 处、同文本 3 处 ⇒ 文本替换无法定位，只能按函数区间定点删除）；`git diff` 恰 1 行。
- `evidence/conc/EV-CONC-001.md`：新增 `negative_controls` nc1（block 式 YAML，533 §2.1 格式），probe 绑定卡上**既有** `artifact_assert` 锚点（`_Z17spin_signal_fencev` ∋ `s_sf_b`，`becomes_absent`）——**不新增断言、不动 sha、不动其余字段**。
- 三处门禁实测**逐字未变**：该卡 replay 仍 `confirm`（新字段对既有流程零影响）；`gate` 仍 60 规则/141 命中/block=0/warn=136/advice=5（新增夹具文件**未触发任何规则**）；`pytest fast` 223 → **264 passed**。

### 2.3 V3（`972c362` + `ee1d7c8`）· replay 阴性判决分支**已落地**

- 新函数 `check_negative_controls(meta, workdir, env, art_path, yang_stdout)` + `replay_card` 的 **④c 插桩**（④b 之后、⑤ sanitizer 之前）；`negative_controls` **字段缺失 ⇒ 整段跳过**（不是"跳过校验"，是根本不进这段代码）。
- 判决分支（全部 `refute`，v1 无第四分类）：`bad_schema`（复用 `viso_diff.validate_nc_schema`，存在性/定义数/样板文本/已声明 run 键由 replay 注入）/ `missing`（阴夹具不在盘）/ `command_missing`（复用 `_artifact_compile_lines` 提不出编译行，或该行不含阳夹具路径）/ `broken`（阴面 rc≠0 而**同次**阳面 rc=0 ⇒ 编译器健康，是夹具写坏——不解析 stderr）/ `diff`（reasons 全量入日志）/ `passed`（阴面**依然通过** ⇒ 零判别力）/ `wrong_direction`（读数朝反方向跑，排障用，同属 passed 桶）。**只有编译器未启动/超时走 `infra_error`**。
- 通道：artifact 用 `_symbol_body` 读符号区间计数（符号缺失 ⇒ `None`，fail-closed 不当 0）；run_key 编译+运行后按 `partition("=")` 提键，与**同次**阳面 stdout 比对（比与 `.out` 比对更强）。
- 指纹：`card_fingerprint` 纳入 `negative_controls[*].fixture` 字节（缺文件 ⇒ `MISSING` 强制重跑）。
- 实测证据：`--card evidence/conc/EV-CONC-001.md --no-sanitizer` 日志出现
  `✅ negative_control nc1 flip verified（artifact _Z17spin_signal_fencev ∋ 's_sf_b': 阳=2 阴=0）`（与 533 §1.4 实测逐字一致）且仍 `confirm`；**56 卡全量 replay 逐字不变**（confirm=56/refute=0/infra=0）。
- 两个实战坑（都已修 + 已注释）：① 命令行里的 tempdir 路径**必须 posix 形态**——`run_commands` 走 shlex（POSIX 规则），Windows 反斜杠被当转义吃掉，`-o C:\Users\…` 会写飞成 `C:Users…` 怪文件（首跑即踩）；② 命名规约期望后缀对 `id: nc1` 会算成 `.ncnc1`（自指式假告警），改成 id 已带 `nc` 前缀时直接用 `.nc1`。
- `atom_evidence_replay.py` 是**被钉校验和的核心工具** ⇒ 按流程 `tool_integrity --update` 重钉（`ee1d7c8`，5 文件表只动一行），复跑 `tool_integrity` OK。
- pytest：`tests/test_negative_controls.py` **+10 例**（各 verdict 分支 + 指纹覆盖；`run_commands` 用替身，**不调真编译器**，故留在 fast 组）。

### 2.4 V4–V5 交接（接下来照着做即可，无需重新设计）

**V4 · 毒样例 N1–N7**（533 §2.5）
- 位置：`tools/atom_evidence_replay.py` 新函数 `check_negative_controls(meta, ...)`，在 `replay_card` 的 ④b 之后、⑤ sanitizer 之前调用；**不改任何既有 return 点**。
- 编译行：复用 `_artifact_compile_lines` / `_token_is_compiler` / `-o` 目标识别；把源路径字面量替换为阴面 fixture（阳 fixture 串不在该行 ⇒ `negative_control_command_missing`），`-o` 指 tempdir，`CCACHE_DISABLE=1`；阴面**不锚 sha、不跑 sanitizer、不碰正式文件**。
- 判决（全归 `refute`，不开第四分类）：`negative_control_bad_schema` / `_missing` / `_command_missing` / `_broken`（阳面同次 rc=0 即编译器健康证据，不解析 stderr）/ `_diff`（转 `viso_diff.judge_min_diff`，reasons 全量入日志）/ `_passed`（阴面也通过=零判别力，方向不符细分 `_wrong_direction`）；编译进程起不来/超时才落 `infra_error`。
- 指纹：`card_fingerprint` 追加遍历 `negative_controls[*].fixture` 字节（缺文件 → `MISSING`），否则阴面被改后仍会沿用旧 confirm。
- 验收：既有 `tests/test_atom_evidence_replay.py` 全绿 + 56 卡 replay 结果逐字不变（confirm=56）+ 该卡日志出现 `nc1 flip verified`。

**V4 · 毒样例 N1–N7**（533 §2.5，进 `poison_drill.py` 沙箱真编译）
N1 阳=阴复制（零判别力）→ `negative_control_passed`（diff 侧先拦零语义）；N2 冒名 → `_diff` 且 reasons ≥3 条；N3 阴面写坏（未闭合括号、同次阳面 rc=0）→ `_broken` **不得落 infra**；N4 形式阴面（42→43 / 删 anchor 外）→ `_diff`；N5 阴面缺失 → `_missing`；N6 连主体删（保留 loop 那类）→ `_diff`（retain 缺 + 比率兜底）；N7 干净卡（存量无字段 + B0 合规）→ confirm 不变。验收双指标：N1–N6 `trap_block_rate=100%`、N7 `clean_pass_rate=100%`，并重算 `RULE-COVERAGE` 与 `poison_surface_map.json`。

**V5 · 56 卡迁移 backlog（只排队，不自动降级）**
按 533 §2.4：B0（已完成）→ B1 asm 11 命题/13 卡 → B2 run 双路径 14 命题/14 卡 → B3 24 命题（B 档只出"建议改 inference"名录交人签，**claim_type 零自动变更**）。同时注册 `OBSERVATION-NEEDS-CONTROL`（warn 观察期，与 530 T4 的活性判据串成三层）；**升 block 只走 G-iso 开关**，批次施工不得自行升级。

---

## 3. 批次3 · 529 剩余 P0/P1

**未开始**（0 项）。清单（按 535 批次3，须先确认源码现状再动）：observation 活性判据 warn 观察期（注意 530 T4 已实现 `OBSERVATION-LIVENESS`，先核对是否已被覆盖，避免重复实现——纪律 7）；帧伪指令恒真收口（`.seh_endproc/.cfi_startproc/.p2align` 纳入通用符号恒真判别 + 判别力统计从 `contains_in` 扩到 `contains/contains_any`）；增量指纹补 `.out`（注意 530 T1 已做 `5eabcf4`，须先核对）；warn 强制分类 accept（530 T5 已做 `da85a2e`，须先核对）；CPVA 全阶段（530 T6 已做 `f3025b4`，须先核对）。**估计 5 项里至少 4 项已被 530 覆盖，动工前必须先跑一遍现状核对，别重复实现。**

---

## 4. 收工门禁（fresh run，2026-09-15，串行执行，HEAD=`e374517`）

| 门禁 | 实测 | 判定 |
|---|---|---|
| `gate_engine.py --check` | `[gate] 规则 60 条 · 命中 141 (block=0 warn=136 advice=5)` | ✅ 与开工逐字一致（本批未改任何规则） |
| `poison_drill.py` | **90/90**；攻击面分类 A1–A11 齐全；**零覆盖攻击面：无** | ✅ 与开工一致 |
| `atom_evidence_replay.py --check --no-sanitizer` | **confirm=56 / refute=0 / infra_error=0**，全量 **168.0s**（开工 136.7s 为 533 沙箱读数，机型/负载不同，非本批引入）；V3 落地后复跑仍 **confirm=56** 逐字不变 | ✅ |
| replay `--incremental` | 56 张全部命中缓存，**0.3s** | ✅ |
| 单卡阴面（V3） | `--card evidence/conc/EV-CONC-001.md` → `✅ negative_control nc1 flip verified（artifact … 阳=2 阴=0）`，verdict 仍 confirm | ✅ |
| `tool_integrity.py` | `OK：5 个核心工具与基准一致`（V3 有意改动 atom_evidence_replay.py 后按流程重钉） | ✅ |
| `pytest -m fast -q` | **274 passed**（开工 185 → 223（批次1 +38）→ 264（V1 +41）→ 274（V3 +10）），无 fail/skip 异常 | ✅ |
| `knowledge_graph.py build/stats` | 325 节点 / 291 边；CONTRASTS=22、CONTRADICTS=1；跨原子概念 0 / 最大连通分量 3 | ✅ 与开工一致 |
| `kg conflicts` | 候选矛盾 **1 组**（ATOM-MEM-MOVE-002 × ATOM-MEM-PERF-001，语义裁决归人） | ✅ |
| `task_queue.py list` | `0 条`（空队列不崩） | ✅ |
| 受控目录 | `git status --porcelain -- Examples/atoms/_atom_fence_vs_atomic.{asm,out} atoms/ tools/golden_state.json` **空** | ✅ 56 卡 sha/信任结论零改动 |
| `consistency_check.py` | 评分 **100/100**（ERROR=0 WARN=0） | ✅ |
| `gen_metrics.py --check` | 全部文档数字与事实源一致 | ✅ |
| ruff（CI 口径 0.6.9） | 本批新增/改动文件 `tools/viso_diff.py`、`tests/test_viso_diff.py`、`tools/task_queue.py`、`tests/test_task_queue.py` → `All checks passed!` | ✅ 零新增 |

### 4.1 交付数字小结

- 批次1：**8 commit**；`tools/task_queue.py` 506 → ~1500 行；`tests/test_task_queue.py` 8 → **46 例**。
- 批次2：**4 commit**；新增 `tools/viso_diff.py`（判据 + schema 校验，纯函数）+ `tests/test_viso_diff.py` **41 例** + `tests/test_negative_controls.py` **10 例**；新增阴夹具 1 个 + 卡字段 1 处 + replay ④c 阴性判决分支；重钉工具校验和。
- 本地 **ahead 12 个提交（未 push）**：`5a5323b → 176428d → 107ac68 → 4f80b91 → 0ce3c80 → 476526d → 6c2441e → 55efc92 → f587bd6 → e374517 → 972c362 → ee1d7c8`。

---

## 5. 未做 / 留给人 / 留给更强的模型（诚实清单）

1. **批次2 V4–V5 未做**（毒样例 N1–N7、56 卡 backlog）——施工点已在 §2.4 写清，属"纯机械、可照做"；V1–V3 已完成并各自带回归锁。
2. **批次3（529 收口）未做**；且开工核对发现 5 项里至少 4 项疑已被 530 覆盖（T1/T4/T5/T6），须先核实现状再动，避免重复实现。
3. **golden 漂移仍留红**：`tools/golden_state.json` 仍为 530 收工时的口径，warn 136 条**全"未分类"**；本批**未 accept、未改基线**（`--accept --classify` 是人审动作）。
4. **CI ruff 15 项存量债仍在**（530 §6.8 记录），本批未夹带清债；本批改动的文件零新增。
5. **不偷跑**：G-supervisor / LLM-as-judge / 模型路由 / 自动 KG 入库 / 在线改权重 —— 本批一律未做，开关未动。
6. 未跟踪沙箱（不入库，可人工删）：`_arch_v2*/`、`_arch_v3/`、`_adv_*/`、`_t535_probe/`（含两份**证据复现脚本**：`race_negative_control.py` C1 阴性对照、`make_nc1.py` 阴夹具生成器）、`_worklog_*.md`、`_t535_*.txt`（pytest 原始输出，可删）。

## 6. 关键证据复跑命令

```powershell
# C1 冷启动并发（240 轮零失败）
.venv\Scripts\python.exe -m pytest tests/test_task_queue.py::test_cold_start_two_processes_12_rounds -q

# C1 阴性对照（朴素迁移应失败 1–2 轮）
.venv\Scripts\python.exe _t535_probe\race_negative_control.py

# 批次2 V1 判据 + 沙箱实证件复算（tokens_changed=5 / ratio=0.01116 / 5 攻击样本全拒）
.venv\Scripts\python.exe -m pytest tests/test_viso_diff.py -q

# B0 阴夹具可重建（幂等，带前置断言）
.venv\Scripts\python.exe _t535_probe\make_nc1.py
```
