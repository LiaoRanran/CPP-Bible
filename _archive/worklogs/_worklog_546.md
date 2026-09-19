# 546 建设日志：修复批（L2 队列三洞 → 深度上界 / 未来心跳 / verify 自证）

> 依据：`References/architecture_架构演进/546_修复批_L2队列三洞_深度上界未来心跳verify自证.md`
> 纪律：不 push / 不 golden accept / 只改 `tools/task_queue.py` + `tests/test_task_queue.py` /
> 三个 T 各自一个 commit / 收工前跑全量门禁 / 做不完停在 T 边界。

## 幂等进度看板

```
T-A5 yield 深度上界 + 累计预算账（修无限层级续命）  [x] 236b9fa
T-A3 心跳 UTC 口径 + 未来心跳 clamp/不采信（修永久占坑） [x] 9be6f4f
T-A7 verify 来源标记 + 自证转 needs_review（异方/人签才 done） [x] 7ee082b
收工：三洞探针复跑 + 全量门禁 + 本文件                [x] 本文件
```

## 0. 开工基线（HEAD=`e4d476e`，亲手实测）

| 项 | 实测 |
|---|---|
| 探针 `_adv_v95/probes/probe_l2_attacks.py` | **A7 ESCAPE** · **A3 ESCAPE** · **A5 ESCAPE**（实测 5 级仍可续）· A5b BLOCKED（回卷正确） |
| `pytest tests/test_task_queue.py -q` | **52 项**（51 passed + 1 skipped） |
| `pytest -m fast -q` | 280 项绿 |
| `gate_engine.py --check` | 规则 **60** 条 · 命中 **141 (block=0 warn=136 advice=5)**，exit 0 |
| `poison_drill.py` | **90/90** · 零覆盖攻击面：无 |
| `atom_evidence_replay.py --check --no-sanitizer` | **confirm=56 / refute=0 / infra_error=0** |

三洞的共同形状：**闸门只看"本级/本地"的量**——A5 只看本级剩余预算（不看层级与累计）、
A3 只看"是否早于 now-600s"（不校验心跳本身可不可信）、A7 只看 rc==0（不问考卷是谁出的）。

## 1. T-A5 · yield 深度上界 + 累计预算账（`236b9fa`）

### 1.1 改点（`tools/task_queue.py`）

| # | 改点 | 说明 |
|---|---|---|
| 1 | 新列 `depth INTEGER NOT NULL DEFAULT 0` | 幂等迁移：`SCHEMA_VERSION` 1→2，老库整段重跑只补缺失列；存量行 depth=0（视作根），不丢数据 |
| 2 | `MAX_YIELD_DEPTH = 3` | 子任务 `depth = 父 depth + 1`；`> 3` 且未 `--force` ⇒ reject(2)「不许靠层层让出无限续命」 |
| 3 | `_resolve_depth()` | 手写入队给 `--parent` 时由父行推导 depth（不给"不填 depth 冒充根任务"的口子） |
| 4 | `_root_of()` / `_subtree_issued()` | 累计账：沿 `parent_task` 上溯到根（防环跳数上限），求整棵子树**已下发**预算之和 |
| 5 | 累计池闸门 | `本次 per*n + 子树已发 > 根任务 budget_calls` 且未 `--force` ⇒ reject(2) |
| 6 | overdraw 留痕 | 子预算合计破**父剩余**时，在 `yield` 事件 detail 写 `overdraw=80>50`（下限语义放行，但**不许静默**） |
| 7 | `yield_depth_override` 事件 | 人签 `--force` 破深度上界时留痕（谁放的、放到第几级） |

**为什么深度是主闸**：每级子任务都拿**全新**预算（下限 80 < `YIELD_BUDGET_LEFT` 100）⇒
**每一级**都能"无 force"再让出 ⇒ 层级与总预算双无上界。实测修前 5 级仍可继续。

### 1.2 回归锁（`tests/test_task_queue.py` +2）

- `test_a5_depth_cap_blocks_endless_yield`：照探针形态连造到 `MAX_YIELD_DEPTH` 级，
  **第 4 级无 force 必被拒**（exit 2、状态不变、子任务不落库）；人签 `--force` 放行 + 留痕。
- `test_a5_cumulative_budget_pool_caps_total`：根预算 150，一级发 80（C3 下限契约不变），
  二级再发 80 ⇒ 累计 160 > 150 ⇒ 拒；人签放行且 `issued=160/root=150` 进事件。

## 2. T-A3 · 心跳 UTC 口径 + 未来心跳不采信（`9be6f4f`）

### 2.1 改点

| # | 改点 | 说明 |
|---|---|---|
| 1 | `_now()` / `_cutoff()` → **UTC ISO 秒（`…Z`）** | 库里所有时间戳唯一口径（新增 `_fmt_utc`） |
| 2 | `_parse_ts()` | 替代 `time.mktime(strptime(...))`：`…Z`/带 offset 按各自时区解析；裸 ISO（存量本地值）按本地解释 ⇒ 老数据不漂移 |
| 3 | `_age_s()` | 改为 UTC/aware 求年龄；**未来值保留负年龄**（不夹 0，免得抹掉"时钟超前"这条线索） |
| 4 | `_hb_write()` | 写 `heartbeat_at` 的**唯一口径**：`> now+30s`（`HEARTBEAT_FUTURE_TOLERANCE_S`）⇒ clamp 到 now + `heartbeat_clamped` 事件；`claim/checkpoint/complete/done/heartbeat` 全部改走它 |
| 5 | `heartbeat(..., at=)` + CLI `--at` | 外部时钟传入的口子；写端先挡一次（可测），读端再判一次 |
| 6 | `_stale_ids()` | 不再做字符串比较：`_is_future_ts(heartbeat_at)` ⇒ **不采信 ⇒ 立即可接管**；否则按 `_parse_ts` 算真实年龄 |
| 7 | `_sweep_stale()` | 回收未来心跳时留 `heartbeat_clamped`（口径归位） |
| 8 | `claim --takeover` | 未来心跳 ⇒ **不需要 `--force`** 即可接管（事件记 `future_hb=True`）；租约内的正常心跳仍受 `LEASE_GRACE_S` 保护（C5 不回归） |

**为什么是"不采信 ⇒ 立即可接管"而不是"退回 claimed_at"**：后者只是把占坑时长从"永久"缩到
"真实时间之后再过期"，攻击者仍白拿一段独占；前者让"写未来心跳"**换不到任何租约**，才是对齐
"永久占坑"这一威胁模型的正解。写端已 clamp，正常路径（含时钟超前的机器）不可能产出未来值
⇒ 不会误伤在跑的活（回归锁 `test_a3_normal_heartbeat_unchanged` 逐条钉住）。

### 2.2 回归锁（+4）

`test_a3_future_heartbeat_is_clamped_at_write`（写端 clamp + 事件）/ `test_a3_future_heartbeat_in_db_is_swept`
（**探针原形态：直接改库写未来心跳 ⇒ 他人当场接管**）/ `test_a3_normal_heartbeat_unchanged`
（now / now-700s 不 clamp、租约仍生效）/ `test_a3_age_is_timezone_independent`（`Z`/`+08:00`/`-05:00`
同一时刻同一年龄 ⇒ 证明 mktime 依赖已消除）。

## 3. T-A7 · verify 来源标记 + 自证不许裸 done（`7ee082b`）

### 3.1 改点

| # | 改点 | 说明 |
|---|---|---|
| 1 | 新列 `verify_source TEXT NOT NULL DEFAULT ''` | `SCHEMA_VERSION` 2→3；取值 `default`（type 默认表）/ `custom`（enqueue `--verify-cmd` 自带）/ 空（无 verify，走 `--result-ref`） |
| 2 | `enqueue` 落来源 | 自带 `--verify-cmd` ⇒ `custom`；否则看 `DEFAULT_VERIFY_CMDS` ⇒ `default`；都没有 ⇒ 空 |
| 3 | `complete` 自证判定 | rc=0 且来源 `custom` 且**无凭据** ⇒ 转 `needs_review`，`verify_hash` 前缀 `SELF_VERIFIED`，事件 `needs_review` |
| 4 | 异方 `--second-party <名>` | ≠ 收尾者 ⇒ done + 事件 `second_party_confirm` + hash 后缀 `2nd=<名>`；= 收尾者 ⇒ reject(2) |
| 5 | 人签 `--force --reason` | 必须给原因（与 takeover 同纪律）⇒ done + 事件 `human_signoff_done` + `human=<reason>` |
| 6 | 两步/一步都支持 | 首次 complete 就带凭据 ⇒ 直接 done；先转 `needs_review` 再来确认 ⇒ 同样 done（`_authorize(status="needs_review")`：同一把锁——名字 + token） |
| 7 | `STATUSES` += `needs_review`；CLI 接线 + 提示 | `complete --second-party/--force/--reason`；转 needs_review 时 stderr 明说怎么解锁 |
| 8 | 子任务继承来源 | `yield` 的子任务继承 `verify_cmd` **和** `verify_source`（custom 不许靠切子任务洗白） |

**关键裁决（写进偏差表 §4.2）**：任务书写的是"收尾 worker == 入队者（produced_by_model）才算自证"，
但 `produced_by_model` 是 `--model`（可省略，省略即 NULL）⇒ **身份常常无从比对**。
按本仓一贯的 fail-closed 取齐：**`custom` 来源一律不裸 done**，由异方/人签补上复核这一环。

### 3.2 回归锁（+4）

`test_a7_custom_verify_self_certified_goes_needs_review`（探针原形态 `echo attacker-pass`
⇒ `needs_review` + `SELF_VERIFIED`；无凭据重试仍拒；本人当第二方拒）/
`test_a7_second_party_or_human_signoff_completes`（异方、人签两条都 done 且留痕；人签无 reason ⇒ 拒）/
`test_a7_default_verify_still_done_and_source_recorded`（**同人但用 type 默认 verify 仍可 done**；三种来源都落库；无 verify + `--result-ref` 仍是 `HUMAN_REVIEW_REQUIRED`）/
`test_a7_child_inherits_verify_source`（子任务继承来源，同样不许自证裸 done）。

## 4. 偏差表（与本批任务书不一致处，**逐条给理由**）

| # | 任务书写法 | 实际做法 | 理由（实测/推导） |
|---|---|---|---|
| 4.1 | 累计池 = **父剩余**：`per*n > left` ⇒ 拒 | 累计池 = **根任务 budget_calls**；破父剩余只留痕不拒 | `per = max(MIN_CHILD_BUDGET, left//n)` 下，`per*n > left` **等价于**"下限生效"（`left//n < 80` ⇒ `per*n = 80n > left`）。照此实现 ⇒ 每次下限生效都拒 ⇒ **与 534 §6.5 闸门② 及既有 C3 回归锁（budget=150/used=100 ⇒ 子 80）直接冲突**，而任务书同时要求"C3 不回归"。取根预算做累计池（真·上界，终结"每级凭空发 80"），破父剩余则 `overdraw=` 进事件 |
| 4.2 | 自证 = 收尾者 == 入队者（`produced_by_model`） | `custom` 来源一律转 `needs_review` | `produced_by_model` 可空 ⇒ 身份无从比对 ⇒ fail-closed。代价：异人收尾 custom 任务也需一次 `--second-party`（显式、留痕） |
| 4.3 | 4 个既有测试因此要动 | `test_c6_complete_runs_verify_and_audits_touch` / `test_c6_audit_unavailable_is_visible` / `test_c6_cli_full_chain` / `test_t4_sandbox_paths_exempt_formal_dirs_still_caught` 各补 `--second-party bob`（**被测性质一字未改**） | 它们都自带 `--verify-cmd`（custom）且断言 done；不加凭据则断言的是"自证可 done"，正是本批要修的洞 |
| 4.4 | 探针应打印 BLOCKED | A5 以 `SystemExit(2)` 中断（探针未捕获），单独复跑 `a5b_rollup_partial()` 证明回卷不回归 | 闸门的既有表达就是 exit 2（与预算闸、质量闸同款）；不改探针文件（它是独立对手方脚本） |
| 4.5 | ruff 门禁 | CI 口径 `ruff==0.6.9`：两文件 **All checks passed**；本地 0.16.5 报 19 项（基线同文件 2 项） | 0.16.5 规则集漂移（I001/SIM118/RUF015/UP017/PLW1510），新增项沿用文件既有写法（`.keys()` / `timezone.utc`）；与 530 §6.8 同一存量话题，不随本批改 |

## 5. 收工实测（三个 commit 之后，逐条对照任务书收工条件）

| 条件 | 实测 |
|---|---|
| 三个 T 各自一个 commit，只改 `task_queue.py` + `test_task_queue.py` | `236b9fa`（T-A5）/ `9be6f4f`（T-A3）/ `7ee082b`（T-A7）；`git show --stat` 各 2 文件 |
| 三洞探针复跑：A5/A3/A7 从 ESCAPE 变 BLOCKED | **A7 BLOCKED**（status=`needs_review`，`verify_hash=SELF_VERIFIED 772fa937…rc=0`）；**A3 BLOCKED**（`claim(B)` 当场接管到 A3，`heartbeat_clamped` 留痕）；**A5 BLOCKED**（第 4 级 `yield 深度 4 > 上界 3 … exit 2`）；A5b 仍 BLOCKED（父回卷不回归） |
| 门禁不回归 | gate **规则 60 · 命中 141 (block=0 warn=136 advice=5)** exit 0；poison **90/90**（零覆盖攻击面：无）；replay **confirm=56 / refute=0 / infra_error=0** —— 与 §0 基线**逐字一致** |
| pytest 不许回归 | `tests/test_task_queue.py`：**62 项绿**（52 基线 + 本批 10 锁，1 skipped 为既有）；`pytest -m fast`：**290 项，exit 0**（基线 280 + 10） |
| downgrade 兼容 | `test_downgrade_roundtrip` 仍绿（`depth`/`verify_source` 进 `NEW_COLS` ⇒ 回退一并 DROP，可再升回） |

> `pytest -m fast` 首次跑 EXIT=1：不是用例失败（进度点全为 `.`），是 pytest 回收旧 basetemp 被环境
> 的 safe-delete 拦截；加 `--basetemp` 后 EXIT=0。如实记录，不粉饰。

## 6. 未做与交人项（诚实边界）

1. **`needs_review` 目前没有消费者**：人会看到状态与 stderr 提示，但队列层没有"待复核清单/提醒"
   的命令（`list --status needs_review` 可查，无推送）。下一轮若要闭环，应给 `next` 或新增
   `review` 子命令列出待复核项，并配一条毒样例/回归锁。
2. **`--second-party` 是声明式**：名字进事件，但没做第二方 token 双因子（本机单人场景的信任边界
   仍是文件系统权限，与 `worker_secret` 同一条边界）。跨用户/CI 场景须升级为签名/keyring。
3. **自动 Supervisor Loop 仍未做**（530 T7 的既有约定：v1 由人执行 `task_queue next` 派活）。
   本批只把"人不在环里时系统会被怎么钻"的三个洞补上，**不构成"可以自动调度"的证据**。
4. **老库混时区尾巴**：存量行（裸本地 ISO）按本地时区解释、新行按 UTC，混在同一列里。
   存量数据属瞬态（heartbeat 只在 claimed 期有意义），未做一次性换算迁移；若未来要跨机搬迁库，
   应加一次性 backfill。
5. 本批 commit 未 push（沙箱纪律）。
