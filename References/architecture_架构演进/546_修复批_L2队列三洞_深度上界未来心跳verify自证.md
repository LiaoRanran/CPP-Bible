# 546 · 修复批：L2 task_queue 三洞（A5 无限续命 / A3 未来心跳 / A7 verify 自证）

> 你是建设苦力。545 异族对抗的 3 个 L2 逃逸已由监工**独立复跑探针确认是真洞**（`_adv_v95/probes/probe_l2_attacks.py`，0/3 全逃逸；A5b 父回卷守住）。本批逐个修，每个都把异族探针转成回归锁。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`e4d476e`，门禁用 `.venv\Scripts\python.exe`。**先 Read `tools/task_queue.py` 相关函数（行号会漂移）再改。**

## 开工基线
先复跑探针确认你也能复现 3 个 ESCAPE：`.venv\Scripts\python.exe _adv_v95\probes\probe_l2_attacks.py`。
再跑 `pytest tests/test_task_queue.py -q`（约 49 例）记绿，改动后不许回归。

---

## T-A5（高）· yield 深度与累计预算上界
**洞**：`yield_task`（约 952-1030）每级子任务预算 `per=max(MIN_CHILD_BUDGET, left//n)`（约 990）发的是**全新预算**，闸门（约 980）只看本级 `left`；无深度字段、无累计账。实测 P→c1→c1.c1… 5 级仍可无 --force 继续。
**修法（最小且不破坏正常父子回卷）**：
1. tasks 表加 `depth INTEGER NOT NULL DEFAULT 0`（迁移走既有 user_version/ALTER 幂等模式）；enqueue 根任务 depth=0，yield 出的子任务 `depth = 父depth + 1`。
2. 加常量 `MAX_YIELD_DEPTH = 3`：yield 时若**任一子任务 depth 会 > MAX_YIELD_DEPTH** 且未 `--force` → reject（人签 --force 才放行，留痕）。
3. 累计预算账：子任务预算之和从父任务的**剩余预算池**扣（不是每级凭空发 80）；若 `per*n > left` 且非 force → reject「子预算超出父剩余，需人签」。保留 MIN_CHILD_BUDGET 下限语义，但不许突破父池。
4. 回归锁：把探针 A5 转成 pytest——构造 5 级嵌套，断言第 4 级（depth>3）无 force 被 reject、带 force 放行且留痕；正常 1-2 级 yield + 父回卷（现有 C3 测试）不回归。
独立 commit。

## T-A3（中）· 未来心跳 clamp + 年龄用 UTC
**洞**：`_age_s`（约 879-884）用 `time.mktime(strptime(...))` 本地时区；heartbeat_at 可被写成 now+1h，`_sweep_stale` 的 `heartbeat_at < now-600` 永不命中 → 任务恒 claimed、他人 claim/next 都拿不到，跨机时钟偏移即可自然触发。
**修法**：
1. 所有写 heartbeat_at 的入口（claim/heartbeat）统一存**时区无关的 epoch 秒或 UTC ISO**；写入时若传入时间 > now+30s 容差，**clamp 到 now**（不允许未来心跳），并在事件流留 `heartbeat_clamped`。
2. `_age_s` 改为对同一存储口径求年龄（epoch 相减或 UTC aware 解析），消除 mktime 本地时区依赖。
3. 回归锁：探针 A3 转 pytest——写 now+1h 心跳，断言被 clamp、他人可在 stale 后正常接管；正常心跳（now、now-700s）的 claim/sweep 行为不回归。
独立 commit。

## T-A7（中）· verify 自证：自定义 verify + 同人收尾不得裸 done
**洞**：`complete`（约 1151-1204）取 `row['verify_cmd']`（约 1151）后 `subprocess.run(verify, shell=True)`（约 1161）。enqueue 时 `--verify-cmd "echo attacker-pass"` 由同一人自带，complete rc=0 直接 done——自己给自己出考卷。（注：`--verify-cmd` 覆盖 type 默认表是 534 §4.3 明写的灵活设计，不取消，补制衡。）
**修法（黑名单列不全，走来源标记+异方制衡）**：
1. 记录 verify 来源：用 type 默认表的标 `default`，enqueue 时 `--verify-cmd` 覆盖的标 `custom`（加列或入 events，幂等迁移）。
2. complete 时若 `verify 来源=custom` **且** 收尾 worker == 入队者（produced_by_model/claimed_by 同人）→ **不允许裸 done**：状态转 `needs_review`、verify_hash 标 `SELF_VERIFIED`，需异方 `--second-party` 或人签才 done。
3. type 默认 verify（default 来源）维持现状直接 done。
4. 回归锁：探针 A7 转 pytest——同人 custom `echo pass` 断言转 needs_review 而非 done；同人但用 type 默认 verify 仍可 done；异方确认后可 done。
独立 commit。

---

## 收工（每个 T 都要）
- 三洞探针复跑：A5/A3/A7 从 ESCAPE 变 BLOCKED/转人审；A5b 仍守住。
- `pytest tests/test_task_queue.py -q` 全绿（现有约 49 例 + 新增回归锁）；ruff 0.6.9 过。
- 全量门禁 fresh run：gate（60/block=0/warn=136）、poison 90/90、replay confirm=56、`pytest -m fast -q` 全绿；task_queue 改动不碰 atoms/evidence/golden_state。
- 写 `_worklog_546.md`（每洞改前改后探针输出、迁移怎么做的、force/人签口子留在哪、每条 commit）。
**不 push、不 --no-verify、不 golden accept；改 task_queue 表结构走幂等迁移（老库不丢数据）；做不完停在 T 边界。**
