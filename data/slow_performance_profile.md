# 608 D0 · slow 测试性能剖析（test_task_queue_stateful.py）

> 实跑日期：2026-09-20｜工具：`python -m cProfile -m pytest tests/test_task_queue_stateful.py::TestTQ`
> 实测 `TestTQ` 实例（状态机，max_examples=120）：cProfile 耗时 **87.9s**（含 profiling 开销；去开销约 66s）。
> 整模块 79.4s，占 slow 门禁 ~39%（监工实测）。

## 1. 热点（cProfile，按 tottime 降序，截断 Top15）

| 函数 | tottime(s) | ncalls | 含义 |
|---|---|---|---|
| `sqlite3.Connection.execute` | 34.28 | 98,723 | 每条 SQL |
| `sqlite3.Connection.close` | 17.39 | 20,952 | **每次调用都关连接** |
| `_sqlite3.connect` | 8.04 | 20,952 | **每次调用都开连接** |
| `task_queue._set_wal`（PRAGMA wal） | 28.30(cum) | 20,952 | **每次开连接都重设 WAL** |
| `nt.mkdir` | 4.13 | 22,114 | 临时目录创建 |
| `_descendants_sum`（测试内） | 0.44 | 38,917 | 预算账：O(rows)，**非瓶颈** |
| `hypothesis … _draw` | ~4.6(cum) | 63,827 | 随机数据生成 |

**结论**：整模块 16.6M 函数调用中，**sqlite 连接开/关 + WAL pragma 占 ~60s（≈72%）**。
根因：`task_queue.py` 的库函数**每次调用都 `connect()` + `PRAGMA journal_mode=WAL` + `close()`**；
状态机在 120 例 × ~百步 × 多 `tq.*` 调用下，累计 **20,952 次连接生命周期**。
判定用不变量 `inv_db_consistency` 的全表扫描本身只 0.44s（不是瓶颈）。

## 2. 加速点（按"是否改变测试判决"分类）

### ✅ 可在测试内安全做（不改判决逻辑）
- **最小样例预算**：`max_examples=120 → 100`（文档注释本身写"100-200 例"，100 即下限）。
  连接开/关总量与步数近似线性 ⇒ 省 ~17%（66s→~55s），覆盖度损失最小（在下限内）。
- **夹具共享**：7 个确定性用例各自 `_new_db()`（建临时库 + init + WAL）开销小，**不合并**（合并破坏隔离、改变判决）。
  状态机每例自带临时库、不可跨例共享（隔离是铁律），故"夹具共享"在状态机场景无解。

### ⚠️ 需进一步分析（改变连接生命周期 = 改 task_queue.py 库行为，超出 D1 测试修改范围）
- **连接复用 / 连接池**：`task_queue._connect()` 改为每 DB 复用单个连接（或 WAL pragma 只在 init 设一次）。
  预计砍掉 ~60% 运行时（20,952 次连接生命周期→接近 0 次额外开销）。属库级改动，blast radius 大，需独立回归验证，**不在此批 D1 测试修改内**，登记为后续分析项（质量信号，非失败）。
- **`_set_wal` 去重**：即便不池化，也可在 `init()` 内一次性设 PRAGMA，之后 `_connect` 不再重设（省 28s cum）。

## 3. 实施原则（硬纪律）
- D1 只改 `test_task_queue_stateful.py` 的**样例预算**，**绝不**动 `@rule`/`@invariant` 的断言（不改判决）。
- 任何会降覆盖度的加速点（如 max_examples<100）**不做**，登记为"需进一步分析"。
- 库级连接复用（task_queue.py）属更大改造，**不在此批**，移交后续。

## 4. 量化收益预期（实跑前，待 D1 落地后复测）
- max_examples 120→100：≈ −17%（79.4s→~66s 模块；TestTQ 66s→~55s）。
- 库级连接复用（未来）：≈ −60%（整模块 → ~32s）。
