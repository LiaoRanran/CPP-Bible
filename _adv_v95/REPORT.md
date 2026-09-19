# 545 · 第五轮独立对抗（实战版）REPORT

> 独立对抗者：与建设者不同模型族、零上下文、不继承"我修好了"。
> 本轮只交付**攻击面 A（L2 task_queue）**的 3 条有效探针；B/C/D 面本轮未打（声明未饱和，见末节）。

## 一句话：这批新代码最脆的一环

**预算/让出闸门只看"本级剩余"，不看"层级深度与累计调用数"——`MIN_CHILD_BUDGET(80) < YIELD_BUDGET_LEFT(100)`，一次合法让出后就进入"每级都能无签名再让出"的无限续命链；而 `complete` 的 `verify_cmd` 又由入队者自写，"worker 不得自证"在 enqueuer==worker 时等于没有闸。**

## 严格拦截率

| 项 | 数 |
|---|---|
| 有效探针 | 3（A3 未来心跳 / A5 无限续命 / A7 verify 自证） |
| **逃逸**（错误状态下直推 verified/done 或永久占坑） | **3** |
| 仅 warn 可见化 | 0 |
| 设计内 | 0（三条都是"设计口子被走通"，不是明写允许） |
| **严格拦截率** | **0 / 3 = 0%** |

（A5b 因探针构造只有单组子任务，未真正测到"父 done 子未全 done"的多组场景，判**未覆盖**、不计入分母。）

## 发现

### A5 · yield 无限层级续命 — 严重度 **高**
- **构造**：父 budget=500、used=450（left=50 < 100 ⇒ 无需人签）→ yield → 子 budget=`max(80, 50//1)=80`；此后**每级** left=80-0=80 < 100 ⇒ 每级都无需 `--force`。
- **实测输出**（`probes/probe_l2_attacks.py`）：
  ```
  P(budget=500,used=450,left=50)  --无force--> P.c1(budget=80)
  P.c1(budget=80,used=0)          --无force--> P.c1.c1(budget=80)
  P.c1.c1(budget=80,used=0)       --无force--> P.c1.c1.c1(budget=80)
  … 实测 5 级仍可继续，无深度上限、无累计预算账
  ```
- **击穿点**：`tools/task_queue.py` `yield_task()` 中 `per = max(MIN_CHILD_BUDGET, left // len(groups))`，闸门 `left >= YIELD_BUDGET_LEFT` 只比较**本级**剩余；子任务拿到的是**全新预算**（80），不扣祖先已消耗的 450。
- **后果**：534 §6.5 的"预算闸门防逃"在让出一次后归零——总调用预算无上界，"到顶让出"从兜底变成永动机。
- **建议修**：① 子任务预算从**祖先链累计已消耗**里扣（`per = 祖先剩余预算 - 该分支已用`）；② 加 `MAX_YIELD_DEPTH`（如 2）；③ 令 `MIN_CHILD_BUDGET ≥ YIELD_BUDGET_LEFT`，或子任务的 left 判据带祖先累计。

### A3 · 未来心跳（时钟偏移/跨时区 worker）永久占坑 — 严重度 **中**
- **构造**：claim 后把 `heartbeat_at` 写成 `now+1h`（模拟 worker 机时钟快于调度机 / 跨时区写本地时间）。
- **实测输出**：
  ```
  heartbeat_at=2026-09-16T00:09:03（now+1h）
  claim(B).claimed=None   next_task().next=None   任务状态仍=claimed
  缓解：--force --reason 可接管 ⇒ taken_over=A3
  ```
- **击穿点**：`_sweep_stale` 判据 `heartbeat_at < now-600s`；`_age_s()` 用 `time.mktime(time.strptime(...))` 按**本地时区**解析字符串——写方与读方时区/时钟不一致即可自然产生（无需篡改 DB，跨机场景真实可达）。
- **后果**：任务被"活着"的会话永久占住，stale 回收永不触发；**且系统没有任何告警指出"心跳时间在未来"**，只能等人发现后 `--force` 接管。
- **建议修**：① 心跳一律存 UTC（写读同口径）；② heartbeat/claim 时若 `heartbeat_at > now + 60s`（允许的正常时钟偏移）即**拒绝并告警**；③ `next`/`list` 里把"心跳在未来"的任务单独点名。

### A7 · verify_cmd 自证 — 严重度 **中**
- **构造**：同一人以 `enqueue --verify-cmd "echo attacker-pass"` 入队，再自己 `complete`。
- **实测输出**：`status=done  verify_hash=772fa937d968649a@0.04s rc=0`
- **击穿点**：`complete()` 直接用行内 `verify_cmd`（`shell=True` 执行）。`--verify-cmd` 覆盖 type 默认表是 534 §4.3 明写的设计，但**没有"enqueuer ≠ worker"校验**：同人入队+收尾时，"worker 不得自证"这条不变量不成立。
- **建议修**：`enqueue` 落 `enqueued_by`；`complete` 时若 `enqueued_by == worker` 且 `verify_cmd` 非 type 默认 ⇒ 要求 `--result-ref`（转人审）或人签。

## 对 534/533/543 设计论断的裁决

| 论断 | 裁决 |
|---|---|
| 534 §6.5「预算剩余 ≥100 不许让出」= 防逃闸门 | **部分成立**：只对第一级成立；让出一次后闸门失效（A5） |
| 534 §4.3「worker 不得自证（先跑 verify_cmd 才 done）」 | **不成立（同人场景）**：verify_cmd 由入队者自写（A7） |
| 534 §6.1「心跳 600s ⇒ 机器判死，可被接管」 | **条件成立**：依赖写读双方时钟/时区一致；否则永不判死（A3） |
| 543「yield 父回卷：全子 done ⇒ 父自动 done」 | 本轮**未证伪也未证实**（A5b 探针构造为单组，未覆盖多组场景） |

## 未覆盖（声明未饱和，不硬凑）

- 攻击面 A：A1 handoff 投毒、A2 三级信任混淆、A4 touch 归一化残余（symlink/8.3/.. 穿越/hardlink）、A6 并发建库极限（20/50 进程）——未打。
- 攻击面 B（V-iso 阴阳同构 B1–B6）、C（新旧接缝 C1–C3）、**D（mutation_fuzz D1–D5，文档标"重点"）**——**本轮完全未打**，需续轮。
- 未复跑基线门禁（gate/poison/replay/pytest/mutation_fuzz）：本轮为纯只读+tmp 探针，未触碰正式文件，故未复跑；若续轮要动正式代码，必须先补基线。
- HEAD 实测 `e4d476e`，与文档写的 `205a377` 不一致（文档锚点已过期）。

## 复跑

```
.venv\Scripts\python.exe _adv_v95\probes\probe_l2_attacks.py
```
探针全部落在系统临时目录（每次 `tempfile.mkdtemp()`，仅改 `tq.DB_PATH`/`tq.ANCHOR_ROOT`），仓库零改动、不 commit、不 push。
