# replay 锁一致性现状盘点（606 任务 0）

> 生成时间：2026-09-19 · 从 atom_evidence_replay.py 代码中提取

## 锁实现清单

| 组件 | 位置 | 说明 |
|------|------|------|
| `_replay_lock_path()` | 行944 | 返回 `run_root() / "build" / ".replay_lock"`；580 实现跟随跑批根分片 |
| `_LOCK_WAIT_SEC` | 行947 | 等待上限 120s（超时 → infra_error:replay_busy） |
| `_LOCK_STALE_SEC` | 行948 | 锁龄超 300s 视为陈旧并接管 |
| `_acquire_replay_lock()` | 行953 | O_CREAT\|O_EXCL 独占锁；含 pid 存活检测 + 陈旧锁接管 |
| `_try_unlink_lock()` | 行993 | 容忍删除失败（safe-delete 拦截时不崩）；残留锁由 pid/stale 兜底自愈 |
| `_release_replay_lock()` | 行1010+ | 释放锁（调用 _try_unlink_lock） |

## 锁一致性不变量（I3）

1. **路径正确性**：默认情况下（无 batch_root），锁路径 = 真实 ROOT/build/.replay_lock
2. **跑批根跟随**：在 batch_root 上下文内，锁路径 = batch_root/build/.replay_lock（不指向真实仓库）
3. **无残留**：replay 未运行时，真实仓库 ROOT/build/.replay_lock 不存在
4. **每卡取放**：锁粒度是每卡 acquire/release（非全程持锁），单卡最长 ~10s

## 已有测试

- `tests/test_replay_lock_serial.py`：锁串行化测试
- `tests/test_p0g_lock.py`：golden lock 测试
- 580 的 4 例锁测试（poison P45/P46 + 两个锁测试）

## 本批范围

在 `tools/replay_invariants.py` 中新增 `check_lock_consistency()`，验证：
- 默认路径正确（不变量 1）
- batch_root 内路径跟随（不变量 2）
- 真实仓库无残留锁（不变量 3）

不做并发压力测试（只做单进程路径逻辑检查）。
