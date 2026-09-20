# _arch_v3 交接说明（HANDOFF）——给 534 新会话（无上下文）

> **【2026-09-15 更新】534 已由新会话按本指引完成**：主交付 `534_L2调度层施工规格.md`；
> 增量原型在 `probe_queue/tq_ext.py`（以 d976170 为基线，非下面说的重造 tq.py）；
> 8 场景实测全 PASS（`probe_queue/probe_report2.json`，含 kill-9→takeover 零上下文续跑）；
> d976170 既有 8 条 pytest 回归全绿。待苦力按规格 §8 的 C1–C7 批次落地。
> 以下为旧文（当时的回收指引，保留作过程记录）。

> 本目录由"534 旧口径会话"（在 533 同一会话里接着喂，带"从零设计 task_queue"的错误假设）产生，**该会话已主动停手**。本文件是给下一个**全新**会话的回收指引，避免它从零摸索或误用重造物。

## 一句话
落地版队列 **已由苦力在 `tools/task_queue.py`（commit d976170，约 506 行）实现**，含 init/enqueue/claim/next/heartbeat/done/fail/blocked/list，且已带 deps 门、stale 接管、双连接争抢只中一个。你**不是从零设计队列**——先读 `References/architecture_架构演进/534_...md` 第 0 步的 d976170 锚点，再读 `tools/task_queue.py`，然后在它之上做 534 列的四件增量（handoff 断点续跑 / yield / touch_set 锁 / complete 验证门禁）。

## 不要用（重造物，别当基线）
- `probe_queue/tq.py`（约 830 行）：按旧口径平行重造的队列，与 d976170 功能重复。**不要读它当参考实现，不要把它当基线**。留着只为可复跑证据，新交付以 `tools/task_queue.py` 为准。

## 可回收（思路可继承，但要改驱动对象）
- `probe_queue/worker_sim.py` + `run_probe.py` + fixtures：kill-9 续跑的**编排思路**（零上下文新进程验哈希续步、S1–S8 场景设计）可继承；但它现在驱动的是上面那个平行 `tq.py`，新会话要**改造成驱动 `tools/task_queue.py`（d976170）** 才能作数。
- 已实测跑通、可直接采信的结论：
  - 并发 claim 10+3 轮零双领（争抢原子性成立）；
  - touch_set 文件冲突时正确避让（该设计思路成立，落到落地版即可）。

## 现场发现、直接写进设计的真实点
- **租约语义（重要）**：一个任务已被 claim 且心跳健康时，**裸 `next` 不能把它抢走**——否则新会话一进来就把别人正在干的活顶了。要接管，必须由人显式 `takeover <task>`（或心跳过期后 stale 回收）。把这个写进 534 的状态机与 next 过滤逻辑。

## 新会话第一步顺序
1. 读本文件；
2. 读盘上改版 534 投喂词（第 0 步有 d976170 锚点）；
3. Read `tools/task_queue.py` + `tests/test_task_queue.py`，列"已有/缺失"清单；
4. 按 534 执行，正式目录零改动，产出落本目录 `_arch_v3/`。
